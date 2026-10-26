using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Core.Pricing;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.Services;
using SaigonBite.Web.ViewModels;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// Use case D — Place and Manage Orders (FR-D1 to FR-D14): basket from one hub, itemised checkout, tracking,
/// editing while Placed, and cancellation.
/// </summary>
/// <remarks>
/// Nothing here prices, discounts or decides legality. The basket holds identifiers and quantities, the
/// engine returns the BR10 breakdown, the state machine answers every transition question, and Core's
/// payment strategies answer BR13/BR14. The controller only orchestrates and renders (AGENTS.md rules 2-4).
/// </remarks>
public class OrdersController : Controller
{
    private readonly SaigonBiteDbContext _db;
    private readonly ICartService _cart;
    private readonly IPricingService _pricing;
    private readonly IOrderService _orders;
    private readonly IPaymentStrategyResolver _payments;
    private readonly IPlatformSettingsService _settings;
    private readonly IHubLoadService _load;

    /// <summary>Creates the controller.</summary>
    public OrdersController(
        SaigonBiteDbContext db, ICartService cart, IPricingService pricing, IOrderService orders,
        IPaymentStrategyResolver payments, IPlatformSettingsService settings, IHubLoadService load)
    {
        _db = db;
        _cart = cart;
        _pricing = pricing;
        _orders = orders;
        _payments = payments;
        _settings = settings;
        _load = load;
    }

    /// <summary>Adds a menu item to the basket (FR-D1, BR12: one hub, 1..30 lines, 1..20 per line).</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpPost("/orders/add-to-cart")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> AddToCart(AddToCartVm form, CancellationToken cancellationToken)
    {
        var cart = _cart.Get();

        // FR-D1: a basket belongs to exactly one hub.
        if (cart.HubId is not null && cart.HubId != form.HubId && cart.Lines.Count > 0)
        {
            TempData["Error"] =
                "Your basket is bound to one hub (FR-D1). Clear it before ordering from another hub.";
            return RedirectBack(form.ReturnUrl);
        }

        var item = await _db.MenuItems
            .AsNoTracking()
            .Include(m => m.Brand)
            .FirstOrDefaultAsync(m => m.Id == form.MenuItemId, cancellationToken);

        var operated = item is not null && await _db.HubBrands
            .AnyAsync(hb => hb.HubId == form.HubId && hb.BrandId == item.BrandId, cancellationToken);

        if (item is null || !item.IsAvailable || !operated)
        {
            TempData["Error"] = "That item is not orderable at this hub (FR-A5, FR-A6, BR12).";
            return RedirectBack(form.ReturnUrl);
        }

        var quantity = Math.Clamp(form.Quantity, 1, CartLimits.MaxQuantityPerLine);
        cart.HubId = form.HubId;

        var existing = cart.Lines.FirstOrDefault(l => l.MenuItemId == form.MenuItemId);
        if (existing is null)
        {
            if (cart.Lines.Count >= CartLimits.MaxLines)
            {
                TempData["Error"] = $"BR12: an order may contain at most {CartLimits.MaxLines} lines.";
                return RedirectBack(form.ReturnUrl);
            }

            cart.Lines.Add(new CartLine { MenuItemId = form.MenuItemId, Quantity = quantity });
        }
        else
        {
            existing.Quantity = Math.Min(existing.Quantity + quantity, CartLimits.MaxQuantityPerLine);
        }

        _cart.Save(cart);
        TempData["Message"] = $"{item.Name} added to your basket.";
        return RedirectBack(form.ReturnUrl);
    }

    /// <summary>The basket with a live BR10 breakdown (FR-D11).</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpGet("/orders/cart")]
    public async Task<IActionResult> Cart(CancellationToken cancellationToken)
    {
        var cart = _cart.Get();
        var hub = cart.HubId is null
            ? null
            : await _db.Hubs.AsNoTracking().FirstOrDefaultAsync(h => h.Id == cart.HubId, cancellationToken);

        if (hub is null || cart.Lines.Count == 0)
        {
            return View(new CartPageVm());
        }

        var (computation, lines, error) =
            await _orders.PreviewAsync(hub.Id, cart.Lines, cart.DistanceKm, voucherCode: null, cancellationToken);

        return View(new CartPageVm
        {
            Hub = hub,
            Lines = lines,
            Computation = computation,
            Error = error,
            Rejections = computation?.Result.Rejections ?? Array.Empty<PriceRejection>(),
            DistanceKm = cart.DistanceKm,
            Breakdown = computation is null
                ? null
                : BreakdownVm.FromPrice(
                    computation.Result,
                    await LoadAsync(hub.Id, cancellationToken),
                    VietnamTime.Now,
                    await _settings.GetRainFlagAsync(cancellationToken),
                    computation.Voucher?.Code,
                    computation.VoucherNotice),
        });
    }

    /// <summary>Removes one line from the basket.</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpPost("/orders/cart/remove")]
    [ValidateAntiForgeryToken]
    public IActionResult RemoveLine(int menuItemId)
    {
        var cart = _cart.Get();
        cart.Lines.RemoveAll(l => l.MenuItemId == menuItemId);
        if (cart.Lines.Count == 0)
        {
            cart.HubId = null;
        }

        _cart.Save(cart);
        return RedirectToAction(nameof(Cart));
    }

    /// <summary>Empties the basket.</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpPost("/orders/cart/clear")]
    [ValidateAntiForgeryToken]
    public IActionResult Clear()
    {
        _cart.Clear();
        return RedirectToAction(nameof(Cart));
    }

    /// <summary>
    /// Checkout: the full BR10 breakdown before payment (FR-D11), the BR13 method list and the FR-B5 hub
    /// alternatives when the hub refuses new orders.
    /// </summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpGet("/orders/checkout")]
    public async Task<IActionResult> Checkout(CancellationToken cancellationToken)
    {
        var cart = _cart.Get();
        if (cart.HubId is null || cart.Lines.Count == 0)
        {
            return RedirectToAction(nameof(Cart));
        }

        return View(await BuildCheckoutAsync(
            new CheckoutFormVm { DistanceKm = cart.DistanceKm }, cart, cancellationToken));
    }

    /// <summary>
    /// Previews or places the order. The posted distance and voucher are re-priced server-side; the posted
    /// method is checked against BR13 and BR14 before anything is written.
    /// </summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpPost("/orders/checkout")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Checkout(CheckoutFormVm form, CancellationToken cancellationToken)
    {
        var cart = _cart.Get();
        if (cart.HubId is null || cart.Lines.Count == 0)
        {
            return RedirectToAction(nameof(Cart));
        }

        cart.DistanceKm = form.DistanceKm;
        _cart.Save(cart);

        var customerType = User.GetCustomerType() ?? CustomerType.Local;
        var customerId = User.GetUserId() ?? 0;

        if (!form.Place)
        {
            // "Update price" — the same computation the placement will repeat, so what is shown is what is
            // charged.
            return View(await BuildCheckoutAsync(form, cart, cancellationToken));
        }

        if (form.Method is null)
        {
            TempData["Error"] = "Choose a payment method (BR13).";
            return View(await BuildCheckoutAsync(form, cart, cancellationToken));
        }

        var result = await _orders.PlaceAsync(
            customerId, customerType, cart.HubId.Value, cart.Lines, form.DistanceKm, form.VoucherCode,
            form.Method.Value, form.HotelName, form.RoomNumber, form.Notes, cancellationToken);

        if (!result.Placed)
        {
            var vm = await BuildCheckoutAsync(form, cart, cancellationToken);
            vm.Error = result.Error;
            vm.Rejections = result.Rejections;
            vm.AlternativeHubs = result.AlternativeHubs;
            return View(vm);
        }

        _cart.Clear();

        if (result.PaymentSucceeded)
        {
            TempData["Message"] = "Order placed and payment recorded.";
        }
        else
        {
            TempData["Error"] =
                result.PaymentError ?? "The order was placed but the payment did not succeed. Retry from the order.";
        }

        return RedirectToAction(nameof(Details), new { id = result.OrderId });
    }

    /// <summary>The signed-in customer's orders, newest first.</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpGet("/orders")]
    public async Task<IActionResult> Index(CancellationToken cancellationToken)
    {
        var customerId = User.GetUserId() ?? 0;
        var orders = await _db.Orders
            .AsNoTracking()
            .Include(o => o.Hub)
            .Where(o => o.CustomerId == customerId)
            .OrderByDescending(o => o.PlacedAt)
            .ToListAsync(cancellationToken);

        return View(new OrderListVm { Orders = orders });
    }

    /// <summary>Order tracking with the breakdown, the audit trail and the permitted actions (FR-D11, FR-S5).</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpGet("/orders/{id:int}")]
    public async Task<IActionResult> Details(int id, CancellationToken cancellationToken)
    {
        var order = await LoadOrderAsync(id, cancellationToken);
        if (order is null)
        {
            return NotFound();
        }

        if (order.CustomerId != (User.GetUserId() ?? 0))
        {
            // Server-side ownership check: a customer may not read another customer's order (FR-S2, NFR4).
            return Forbid();
        }

        return View(await BuildDetailsAsync(order, cancellationToken));
    }

    /// <summary>Edit form for a Placed order (FR-D12, BR17).</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpGet("/orders/{id:int}/edit")]
    public async Task<IActionResult> Edit(int id, CancellationToken cancellationToken)
    {
        var order = await LoadOrderAsync(id, cancellationToken);
        if (order is null)
        {
            return NotFound();
        }

        if (order.CustomerId != (User.GetUserId() ?? 0))
        {
            return Forbid();
        }

        if (order.Status != OrderStatus.Placed)
        {
            TempData["Error"] = $"Items can only be edited while the order is Placed; it is {order.Status} (BR17).";
            return RedirectToAction(nameof(Details), new { id });
        }

        return View(await BuildEditAsync(order, cancellationToken));
    }

    /// <summary>
    /// Saves an edit and re-prices it against the placement snapshot (FR-D12, BR17). The engine decides again,
    /// so an edit that breaks BR1, BR2 or BR12 is refused instead of being written.
    /// </summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpPost("/orders/{id:int}/edit")]
    [HttpPost("Orders/Edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, EditOrderVm form, CancellationToken cancellationToken)
    {
        var order = await LoadOrderAsync(id, cancellationToken);
        if (order is null)
        {
            return NotFound();
        }

        if (order.CustomerId != (User.GetUserId() ?? 0))
        {
            return Forbid();
        }

        var lines = form.Lines
            .Where(l => l.Quantity > 0)
            .Select(l => new CartLine { MenuItemId = l.MenuItemId, Quantity = l.Quantity })
            .ToList();

        if (form.NewMenuItemId is not null && form.NewQuantity > 0)
        {
            var existing = lines.FirstOrDefault(l => l.MenuItemId == form.NewMenuItemId.Value);
            if (existing is null)
            {
                lines.Add(new CartLine { MenuItemId = form.NewMenuItemId.Value, Quantity = form.NewQuantity });
            }
            else
            {
                existing.Quantity = Math.Min(
                    existing.Quantity + form.NewQuantity, CartLimits.MaxQuantityPerLine);
            }
        }

        if (lines.Count == 0)
        {
            TempData["Error"] = "An order needs at least one line (BR12).";
            return RedirectToAction(nameof(Edit), new { id });
        }

        var outcome = await _orders.EditAsync(id, User.GetUserId() ?? 0, lines, cancellationToken);
        if (!outcome.Success)
        {
            TempData["Error"] = outcome.Message;
            return RedirectToAction(nameof(Edit), new { id });
        }

        TempData["Message"] = outcome.Message;
        return RedirectToAction(nameof(Details), new { id });
    }

    /// <summary>Customer cancellation in Placed or Confirmed (FR-D13, BR16).</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpPost("/orders/{id:int}/cancel")]
    [HttpPost("Orders/Cancel")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Cancel(int id, CancellationToken cancellationToken)
    {
        var outcome = await _orders.CancelByCustomerAsync(
            id, User.GetUserId() ?? 0, cancellationToken);

        if (outcome.Success)
        {
            TempData["Message"] = outcome.Message + " An online payment is refunded in full (BR16).";
        }
        else
        {
            TempData["Error"] = outcome.Message;
        }

        return RedirectToAction(nameof(Details), new { id });
    }

    /// <summary>Retries the payment of a Placed order (FR-P3, BR13).</summary>
    [Authorize(Policy = Policies.Customer)]
    [HttpPost("/orders/{id:int}/pay")]
    [HttpPost("Orders/Pay")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Pay(int id, PaymentMethod method, CancellationToken cancellationToken)
    {
        var outcome = await _orders.PayAsync(
            id, User.GetUserId() ?? 0, User.GetCustomerType() ?? CustomerType.Local, method, cancellationToken);

        if (outcome.Success)
        {
            TempData["Message"] = outcome.Message;
        }
        else
        {
            TempData["Error"] = outcome.Message;
        }

        return RedirectToAction(nameof(Details), new { id });
    }

    private async Task<CheckoutPageVm> BuildCheckoutAsync(
        CheckoutFormVm form, CartState cart, CancellationToken cancellationToken)
    {
        var customerType = User.GetCustomerType() ?? CustomerType.Local;
        var hub = await _db.Hubs.AsNoTracking()
            .FirstOrDefaultAsync(h => h.Id == cart.HubId, cancellationToken);

        var vm = new CheckoutPageVm
        {
            Hub = hub,
            DistanceKm = form.DistanceKm,
            VoucherCode = form.VoucherCode,
            SelectedMethod = form.Method?.ToString(),
            HotelName = form.HotelName,
            RoomNumber = form.RoomNumber,
            Notes = form.Notes,
            CustomerType = customerType,
            PaymentOptions = _payments.AvailableFor(customerType),
            VoucherCodes = await _db.Vouchers
                .AsNoTracking()
                .Where(v => v.IsActive && v.ValidTo >= VietnamTime.Today && v.ValidFrom <= VietnamTime.Today)
                .OrderBy(v => v.Code)
                .Select(v => v.Code)
                .ToListAsync(cancellationToken),
        };

        if (hub is null)
        {
            vm.Error = "That hub is no longer available.";
            return vm;
        }

        var (computation, lines, error) = await _orders.PreviewAsync(
            hub.Id, cart.Lines, form.DistanceKm, form.VoucherCode, cancellationToken);

        vm.Lines = lines;
        vm.Computation = computation;
        vm.Error = error;
        vm.Rejections = computation?.Result.Rejections ?? Array.Empty<PriceRejection>();

        // FR-B5: when the hub refuses the order for BR8, offer the other hubs that can take the same basket
        // immediately, instead of only reporting the refusal.
        if (vm.Rejections.Any(r => r.Code == PriceRejection.HubProtection))
        {
            vm.AlternativeHubs = await _orders.SuggestAlternativeHubsAsync(
                hub.Id, lines.Select(l => l.MenuItemId).ToList(), cancellationToken);
        }

        if (computation is not null)
        {
            vm.Breakdown = BreakdownVm.FromPrice(
                computation.Result,
                await LoadAsync(hub.Id, cancellationToken),
                VietnamTime.Now,
                await _settings.GetRainFlagAsync(cancellationToken),
                computation.Voucher?.Code,
                computation.VoucherNotice);
        }

        return vm;
    }

    private Task<OrderDetailsVm> BuildDetailsAsync(Order order, CancellationToken cancellationToken)
    {
        var customerType = User.GetCustomerType() ?? CustomerType.Local;
        var canRetryPayment = order.Status == OrderStatus.Placed
                              && !order.Payments.Any(p => p.Success && p.Amount > 0);

        var vm = new OrderDetailsVm
        {
            Order = order,
            Lines = order.Lines.Where(l => !l.IsRemoved).OrderBy(l => l.Id).ToList(),
            History = order.History.OrderBy(h => h.OccurredAt).ThenBy(h => h.Id).ToList(),
            Payments = order.Payments.OrderBy(p => p.CreatedAt).ToList(),
            AllowedNext = OrderStateMachine.AllowedNext(order.Status, ActorRole.Customer),
            Breakdown = BreakdownVm.FromOrder(order),
            CanEdit = order.Status == OrderStatus.Placed,
            CanCancel = OrderStateMachine.CanTransition(
                order.Status, OrderStatus.Cancelled, ActorRole.Customer).Allowed,
            CanRetryPayment = canRetryPayment,
            PaymentOptions = _payments.AvailableFor(customerType),
        };

        return Task.FromResult(vm);
    }

    private async Task<EditOrderVm> BuildEditAsync(Order order, CancellationToken cancellationToken)
    {
        var lines = order.Lines.Where(l => !l.IsRemoved).OrderBy(l => l.Id).ToList();
        var inOrder = lines.Select(l => l.MenuItemId).ToHashSet();

        var addable = await _db.MenuItems
            .AsNoTracking()
            .Where(m => m.IsAvailable)
            .Where(m => m.Brand!.HubBrands.Any(hb => hb.HubId == order.HubId))
            .Where(m => !inOrder.Contains(m.Id))
            .OrderBy(m => m.Category)
            .ThenBy(m => m.Name)
            .ToListAsync(cancellationToken);

        return new EditOrderVm
        {
            OrderId = order.Id,
            Lines = lines.Select(l => new EditLineVm { MenuItemId = l.MenuItemId, Quantity = l.Quantity }).ToList(),
            AddableItems = addable,
        };
    }

    private async Task<Order?> LoadOrderAsync(int id, CancellationToken cancellationToken) =>
        await _db.Orders
            .Include(o => o.Hub)
            .Include(o => o.AssignedShipper)
            .Include(o => o.Lines)
            .Include(o => o.History)
            .Include(o => o.Payments)
            .FirstOrDefaultAsync(o => o.Id == id, cancellationToken);

    private async Task<int> LoadAsync(int hubId, CancellationToken cancellationToken) =>
        await _load.GetLoadPercentAsync(hubId, cancellationToken);

    private IActionResult RedirectBack(string? returnUrl) =>
        Url.IsLocalUrl(returnUrl ?? string.Empty) ? LocalRedirect(returnUrl!) : RedirectToAction(nameof(Cart));
}
