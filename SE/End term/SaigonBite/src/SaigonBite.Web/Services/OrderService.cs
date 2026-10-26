using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Core.Pricing;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;

namespace SaigonBite.Web.Services;

/// <summary>Outcome of a state-machine request: success means the row was written and the state moved.</summary>
public sealed record TransitionOutcome(bool Success, string Message)
{
    /// <summary>Successful transition.</summary>
    public static TransitionOutcome Ok(string message) => new(true, message);

    /// <summary>Rejected transition; the message is shown verbatim to the actor.</summary>
    public static TransitionOutcome Rejected(string message) => new(false, message);
}

/// <summary>Outcome of a checkout attempt, including the FR-B5 alternatives when the hub is full.</summary>
public sealed record PlaceOrderResult(
    bool Placed,
    int? OrderId,
    IReadOnlyList<PriceRejection> Rejections,
    string? Error,
    bool PaymentSucceeded,
    string? PaymentError,
    IReadOnlyList<Hub> AlternativeHubs)
{
    /// <summary>A refusal that is not a BR10 pricing rejection (validation or payment guard).</summary>
    public static PlaceOrderResult Refused(
        string error, IReadOnlyList<PriceRejection>? rejections = null,
        IReadOnlyList<Hub>? alternatives = null) =>
        new(false, null, rejections ?? Array.Empty<PriceRejection>(), error, false, null,
            alternatives ?? Array.Empty<Hub>());
}

/// <summary>
/// BR14 boundary guard for Cash on Delivery. The <c>CodStrategy</c> in Core re-checks the amount when it
/// is charged; this type exists so the checkout screen never offers a COD button that Core would refuse.
/// </summary>
public static class PaymentPolicy
{
    /// <summary>
    /// Rounded total above which COD is refused (BR14). The number is Core's own constant so the boundary
    /// guard and <c>CodStrategy</c> can never disagree.
    /// </summary>
    public const long CashOnDeliveryCeiling = CodStrategy.MaximumCodTotal;

    /// <summary>True when COD may be offered for a rounded total (BR14).</summary>
    public static bool IsCashAllowed(long roundedTotal) => roundedTotal <= CashOnDeliveryCeiling;
}

/// <summary>
/// Orchestrates the order use case (D) and the delivery transitions (F). Every price comes from
/// <see cref="IPricingService"/>, every legality question from <c>OrderStateMachine</c>, and every
/// attempt is written to <see cref="OrderStatusHistory"/> — accepted or rejected (FR-S5, NFR5).
/// </summary>
public interface IOrderService
{
    /// <summary>Prices a basket without writing anything (cart and checkout screens).</summary>
    Task<(PriceComputation? Computation, IReadOnlyList<ResolvedLine> Lines, string? Error)> PreviewAsync(
        int hubId, IReadOnlyList<CartLine> lines, decimal distanceKm, string? voucherCode,
        CancellationToken cancellationToken = default);

    /// <summary>Places an order with the BR17 snapshot, BR10 breakdown and BR13/BR14 payment guards.</summary>
    Task<PlaceOrderResult> PlaceAsync(
        int customerId, CustomerType customerType, int hubId, IReadOnlyList<CartLine> lines,
        decimal distanceKm, string? voucherCode, PaymentMethod method,
        string? hotelName, string? roomNumber, string? notes,
        CancellationToken cancellationToken = default);

    /// <summary>Re-prices and replaces the lines of a Placed order using the stored snapshot (BR17).</summary>
    Task<TransitionOutcome> EditAsync(
        int orderId, int customerId, IReadOnlyList<CartLine> lines,
        CancellationToken cancellationToken = default);

    /// <summary>Customer cancellation in Placed or Confirmed (BR16), with the simulated refund.</summary>
    Task<TransitionOutcome> CancelByCustomerAsync(
        int orderId, int customerId, CancellationToken cancellationToken = default);

    /// <summary>Staff cancellation: kitchen rejection in Placed, admin cancellation in Confirmed (BR16, A5).</summary>
    Task<TransitionOutcome> CancelByStaffAsync(
        int orderId, ActorRole actorRole, int actorId, int? actorHubId, string? reason,
        CancellationToken cancellationToken = default);

    /// <summary>Forwards a transition the actor requested, letting the state machine decide (BR15).</summary>
    Task<TransitionOutcome> AdvanceAsync(
        int orderId, OrderStatus to, ActorRole actorRole, int actorId, int? actorHubId, string? reason,
        CancellationToken cancellationToken = default);

    /// <summary>Manual shipper assignment in Ready (FR-F1, Ambiguity A1).</summary>
    Task<TransitionOutcome> AssignShipperAsync(
        int orderId, int shipperId, int actorId, CancellationToken cancellationToken = default);

    /// <summary>BR14 cash confirmation by the assigned shipper.</summary>
    Task<TransitionOutcome> ConfirmCashAsync(
        int orderId, int shipperId, CancellationToken cancellationToken = default);

    /// <summary>Failed delivery with a reason, moving the order to the terminal Failed state (FR-F4).</summary>
    Task<TransitionOutcome> FailAsync(
        int orderId, int shipperId, string? reason, CancellationToken cancellationToken = default);

    /// <summary>Retries the payment of a Placed order that has no successful payment yet (FR-P3).</summary>
    Task<TransitionOutcome> PayAsync(
        int orderId, int customerId, CustomerType customerType, PaymentMethod method,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// FR-B5: other hubs that operate every brand in the basket and are still below the BR8 ceiling, so the
    /// checkout screen can offer them the moment the chosen hub refuses the order.
    /// </summary>
    Task<IReadOnlyList<Hub>> SuggestAlternativeHubsAsync(
        int hubId, IReadOnlyList<int> menuItemIds, CancellationToken cancellationToken = default);
}

/// <inheritdoc />
public sealed class OrderService : IOrderService
{
    private readonly SaigonBiteDbContext _db;
    private readonly IPricingService _pricing;
    private readonly IHubLoadService _load;
    private readonly IPlatformSettingsService _settings;
    private readonly IPaymentStrategyResolver _payments;

    /// <summary>Creates the orchestrator.</summary>
    public OrderService(
        SaigonBiteDbContext db, IPricingService pricing, IHubLoadService load,
        IPlatformSettingsService settings, IPaymentStrategyResolver payments)
    {
        _db = db;
        _pricing = pricing;
        _load = load;
        _settings = settings;
        _payments = payments;
    }

    /// <inheritdoc />
    public Task<(PriceComputation? Computation, IReadOnlyList<ResolvedLine> Lines, string? Error)> PreviewAsync(
        int hubId, IReadOnlyList<CartLine> lines, decimal distanceKm, string? voucherCode,
        CancellationToken cancellationToken = default) =>
        _pricing.PriceCartAsync(
            hubId, lines, distanceKm, voucherCode, placedAt: null, rainFlag: null, hubLoadPercent: null,
            cancellationToken);

    /// <inheritdoc />
    public async Task<PlaceOrderResult> PlaceAsync(
        int customerId, CustomerType customerType, int hubId, IReadOnlyList<CartLine> lines,
        decimal distanceKm, string? voucherCode, PaymentMethod method,
        string? hotelName, string? roomNumber, string? notes,
        CancellationToken cancellationToken = default)
    {
        var hub = await _db.Hubs.FirstOrDefaultAsync(h => h.Id == hubId, cancellationToken);
        if (hub is null)
        {
            return PlaceOrderResult.Refused("That hub is no longer available.");
        }

        var (resolved, lineError) = await _pricing.ResolveCartLinesAsync(hubId, lines, cancellationToken);
        if (lineError is not null)
        {
            return PlaceOrderResult.Refused(lineError);
        }

        var placedAt = VietnamTime.Now;
        var rainFlag = await _settings.GetRainFlagAsync(cancellationToken);
        var hubLoad = await _load.GetLoadPercentAsync(hubId, cancellationToken);

        var (voucher, voucherError) =
            await _pricing.ResolveVoucherAsync(voucherCode, placedAt, cancellationToken);
        if (voucherError is not null)
        {
            return PlaceOrderResult.Refused(voucherError);
        }

        var computation = _pricing.Compute(
            hub, resolved, new PriceConditions(placedAt, distanceKm, rainFlag, hubLoad, voucher));
        var price = computation.Result;

        // BR1, BR2, BR8, BR12: the engine is authoritative. Every rejection is surfaced with its code.
        if (!price.IsAccepted)
        {
            var alternatives = price.Rejections.Any(r => r.Code == PriceRejection.HubProtection)
                ? await SuggestAlternativeHubsAsync(
                    hub.Id, resolved.Select(l => l.MenuItemId).ToList(), cancellationToken)
                : Array.Empty<Hub>();
            return new PlaceOrderResult(
                false, null, price.Rejections, null, false, null, alternatives);
        }

        // BR13: a customer may only use a method that belongs to their group. Checked before the order
        // row exists so a refused method cannot leave a half-placed order behind.
        var strategy = _payments.AvailableFor(customerType).FirstOrDefault(s => s.Method == method);
        if (strategy is null)
        {
            return PlaceOrderResult.Refused(
                "That payment method is not available for this customer type (BR13).");
        }

        // BR14: COD is refused above a rounded total of 1,000,000.
        if (method == PaymentMethod.CashOnDelivery && !PaymentPolicy.IsCashAllowed(price.Total))
        {
            return PlaceOrderResult.Refused(
                "Cash on Delivery is not available above 1,000,000 ₫ (BR14). Please choose another method.");
        }

        var order = new Order
        {
            CustomerId = customerId,
            HubId = hubId,
            Status = OrderStatus.Placed,

            // BR17 / FR-D14: the snapshot that makes the price reproducible.
            PlacedAt = placedAt,
            HubLoadPercent = hubLoad,
            RainFlag = rainFlag,
            DistanceKm = distanceKm,

            // BR10 breakdown exactly as the engine returned it.
            Subtotal = price.Subtotal,
            QuietKitchenDiscount = price.QuietKitchenDiscount,
            VoucherDiscount = price.VoucherDiscount,
            FoodTotal = price.FoodTotal,
            DeliveryFee = price.DeliveryFee,
            RushSurcharge = price.RushSurcharge,
            RainSurcharge = price.RainSurcharge,
            Total = price.Total,

            VoucherId = voucher?.Id,
            VoucherCode = voucher?.Code,
            PaymentMethod = method,
            IsCashConfirmed = false,
            HotelName = string.IsNullOrWhiteSpace(hotelName) ? null : hotelName.Trim(),
            RoomNumber = string.IsNullOrWhiteSpace(roomNumber) ? null : roomNumber.Trim(),
            Notes = string.IsNullOrWhiteSpace(notes) ? null : notes.Trim(),
        };

        foreach (var line in resolved)
        {
            order.Lines.Add(new OrderLine
            {
                MenuItemId = line.MenuItemId,
                ItemName = line.ItemName,
                BrandName = line.BrandName,
                CategoryName = line.CategoryName,
                UnitPrice = line.UnitPrice,
                Quantity = line.Quantity,
                IsRemoved = false,
            });
        }

        // Placement itself is audited so the trail starts at Placed (FR-S5).
        order.History.Add(new OrderStatusHistory
        {
            FromStatus = OrderStatus.Placed,
            ToStatus = OrderStatus.Placed,
            ActorRole = ActorRole.Customer,
            ActorId = customerId,
            Reason = "Order placed",
            OccurredAt = placedAt,
            Applied = true,
        });

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        var payment = await ChargeAsync(
            order, strategy, customerType, cancellationToken);

        return new PlaceOrderResult(
            true, order.Id, Array.Empty<PriceRejection>(), null,
            payment.Success, payment.Error, Array.Empty<Hub>());
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> EditAsync(
        int orderId, int customerId, IReadOnlyList<CartLine> lines,
        CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders
            .Include(o => o.Lines)
            .FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);

        if (order is null || order.CustomerId != customerId)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        // BR17 / FR-D12: items may be edited only while the order is Placed.
        if (order.Status != OrderStatus.Placed)
        {
            return TransitionOutcome.Rejected(
                $"Items can only be edited while the order is Placed; this order is {order.Status} (BR17).");
        }

        var (resolved, lineError) = await _pricing.ResolveCartLinesAsync(order.HubId, lines, cancellationToken);
        if (lineError is not null)
        {
            return TransitionOutcome.Rejected(lineError);
        }

        var hub = await _db.Hubs.FirstOrDefaultAsync(h => h.Id == order.HubId, cancellationToken);
        if (hub is null)
        {
            return TransitionOutcome.Rejected("The hub of this order is no longer available.");
        }

        var voucher = order.VoucherId is null
            ? null
            : await _db.Vouchers.AsNoTracking()
                .FirstOrDefaultAsync(v => v.Id == order.VoucherId, cancellationToken);

        // BR17: re-price with the STORED snapshot, never with the current clock, load or rain flag.
        var computation = _pricing.Compute(
            hub, resolved,
            new PriceConditions(order.PlacedAt, order.DistanceKm, order.RainFlag, order.HubLoadPercent, voucher));
        var price = computation.Result;

        if (!price.IsAccepted)
        {
            var codes = string.Join(", ", price.Rejections.Select(r => r.Code));
            return TransitionOutcome.Rejected(
                $"The edited basket is no longer valid ({codes}). Nothing was changed.");
        }

        // Keep the placed prices for lines that survived, use the current menu price for new ones: the
        // snapshot rule protects the conditions, not a stale price for an item added afterwards.
        foreach (var line in order.Lines)
        {
            line.IsRemoved = true;
        }

        foreach (var line in resolved)
        {
            var existing = order.Lines.FirstOrDefault(l => l.MenuItemId == line.MenuItemId);
            if (existing is null)
            {
                order.Lines.Add(new OrderLine
                {
                    MenuItemId = line.MenuItemId,
                    ItemName = line.ItemName,
                    BrandName = line.BrandName,
                    CategoryName = line.CategoryName,
                    UnitPrice = line.UnitPrice,
                    Quantity = line.Quantity,
                    IsRemoved = false,
                });
            }
            else
            {
                existing.IsRemoved = false;
                existing.Quantity = line.Quantity;
                existing.ItemName = line.ItemName;
                existing.UnitPrice = line.UnitPrice;
            }
        }

        order.Subtotal = price.Subtotal;
        order.QuietKitchenDiscount = price.QuietKitchenDiscount;
        order.VoucherDiscount = price.VoucherDiscount;
        order.FoodTotal = price.FoodTotal;
        order.DeliveryFee = price.DeliveryFee;
        order.RushSurcharge = price.RushSurcharge;
        order.RainSurcharge = price.RainSurcharge;
        order.Total = price.Total;

        // An edit is not a state change (BR15), but it changes what will be charged, so it is audited.
        _db.OrderStatusHistories.Add(new OrderStatusHistory
        {
            OrderId = order.Id,
            FromStatus = OrderStatus.Placed,
            ToStatus = OrderStatus.Placed,
            ActorRole = ActorRole.Customer,
            ActorId = customerId,
            Reason = $"Items edited; re-priced from the BR17 snapshot (total {price.Total:N0} ₫)",
            OccurredAt = VietnamTime.Now,
            Applied = true,
        });

        await _db.SaveChangesAsync(cancellationToken);
        return TransitionOutcome.Ok("Order updated and re-priced from its placement snapshot (BR17).");
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> CancelByCustomerAsync(
        int orderId, int customerId, CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);
        if (order is null || order.CustomerId != customerId)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        // BR16: the customer cancels in Placed or Confirmed, without a reason (Ambiguity A5).
        return await ApplyTransitionAsync(
            order, OrderStatus.Cancelled, ActorRole.Customer, customerId, actorHubId: null,
            reason: "Cancelled by the customer", cancellationToken);
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> CancelByStaffAsync(
        int orderId, ActorRole actorRole, int actorId, int? actorHubId, string? reason,
        CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);
        if (order is null)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        return await ApplyTransitionAsync(
            order, OrderStatus.Cancelled, actorRole, actorId, actorHubId, reason, cancellationToken);
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> AdvanceAsync(
        int orderId, OrderStatus to, ActorRole actorRole, int actorId, int? actorHubId, string? reason,
        CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);
        if (order is null)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        return await ApplyTransitionAsync(
            order, to, actorRole, actorId, actorHubId, reason, cancellationToken);
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> AssignShipperAsync(
        int orderId, int shipperId, int actorId, CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);
        if (order is null)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        // FR-F1: a shipper may only be assigned to an order in Ready.
        if (order.Status != OrderStatus.Ready)
        {
            return TransitionOutcome.Rejected(
                "A shipper can only be assigned while the order is Ready (FR-F1).");
        }

        var shipper = await _db.Users.AsNoTracking()
            .FirstOrDefaultAsync(u => u.Id == shipperId, cancellationToken);
        if (shipper is null || shipper.Role != Infrastructure.Roles.Shipper)
        {
            return TransitionOutcome.Rejected("That account is not a shipper.");
        }

        order.AssignedShipperId = shipperId;
        order.AssignedAt = VietnamTime.Now;

        _db.OrderStatusHistories.Add(new OrderStatusHistory
        {
            OrderId = order.Id,
            FromStatus = OrderStatus.Ready,
            ToStatus = OrderStatus.Ready,
            ActorRole = ActorRole.Admin,
            ActorId = actorId,
            Reason = $"Shipper {shipper.DisplayName} assigned (FR-F1, Ambiguity A1)",
            OccurredAt = VietnamTime.Now,
            Applied = true,
        });

        await _db.SaveChangesAsync(cancellationToken);
        return TransitionOutcome.Ok($"{shipper.DisplayName} is assigned to the order.");
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> ConfirmCashAsync(
        int orderId, int shipperId, CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);
        if (order is null)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        // BR14: only the assigned shipper confirms the cash, and only on a COD order.
        if (order.AssignedShipperId != shipperId)
        {
            return TransitionOutcome.Rejected("Only the assigned shipper may confirm the cash (BR14).");
        }

        if (order.PaymentMethod != PaymentMethod.CashOnDelivery)
        {
            return TransitionOutcome.Rejected("This order is not a Cash on Delivery order (BR14).");
        }

        if (order.Status != OrderStatus.OutForDelivery && order.Status != OrderStatus.Ready)
        {
            return TransitionOutcome.Rejected(
                "Cash can only be confirmed once the order is out for delivery (BR14).");
        }

        order.IsCashConfirmed = true;

        _db.OrderStatusHistories.Add(new OrderStatusHistory
        {
            OrderId = order.Id,
            FromStatus = order.Status,
            ToStatus = order.Status,
            ActorRole = ActorRole.Shipper,
            ActorId = shipperId,
            Reason = "Cash collected (BR14)",
            OccurredAt = VietnamTime.Now,
            Applied = true,
        });

        await _db.SaveChangesAsync(cancellationToken);
        return TransitionOutcome.Ok("Cash confirmed. The order may now be marked Delivered (BR14).");
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> FailAsync(
        int orderId, int shipperId, string? reason, CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);
        if (order is null)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        if (order.AssignedShipperId != shipperId)
        {
            return TransitionOutcome.Rejected("Only the assigned shipper may fail this delivery (BR15).");
        }

        // FR-F4: a failed delivery requires a reason from the shipper.
        if (string.IsNullOrWhiteSpace(reason))
        {
            return TransitionOutcome.Rejected("A reason is required to report a failed delivery (FR-F4).");
        }

        return await ApplyTransitionAsync(
            order, OrderStatus.Failed, ActorRole.Shipper, shipperId, actorHubId: null,
            reason: reason.Trim(), cancellationToken);
    }

    /// <inheritdoc />
    public async Task<TransitionOutcome> PayAsync(
        int orderId, int customerId, CustomerType customerType, PaymentMethod method,
        CancellationToken cancellationToken = default)
    {
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, cancellationToken);
        if (order is null || order.CustomerId != customerId)
        {
            return TransitionOutcome.Rejected("Order not found.");
        }

        if (order.Status != OrderStatus.Placed)
        {
            return TransitionOutcome.Rejected("Payment can only be retried while the order is Placed.");
        }

        var alreadyPaid = await _db.PaymentRecords
            .AnyAsync(p => p.OrderId == order.Id && p.Success && p.Amount > 0, cancellationToken);
        if (alreadyPaid)
        {
            return TransitionOutcome.Rejected("This order is already paid.");
        }

        var strategy = _payments.AvailableFor(customerType).FirstOrDefault(s => s.Method == method);
        if (strategy is null)
        {
            return TransitionOutcome.Rejected("That payment method is not available (BR13).");
        }

        if (method == PaymentMethod.CashOnDelivery && !PaymentPolicy.IsCashAllowed(order.Total))
        {
            return TransitionOutcome.Rejected(
                "Cash on Delivery is not available above 1,000,000 ₫ (BR14).");
        }

        order.PaymentMethod = method;
        await _db.SaveChangesAsync(cancellationToken);

        var payment = await ChargeAsync(order, strategy, customerType, cancellationToken);
        return payment.Success
            ? TransitionOutcome.Ok("Payment accepted.")
            : TransitionOutcome.Rejected(payment.Error ?? "The payment was refused by the gateway.");
    }

    /// <summary>
    /// Shared transition routine. It asks the state machine first, then applies the extra conditions the
    /// state table lists (hub of the order, assigned shipper, BR14 cash), and writes exactly one audit row
    /// whether the transition was applied or refused (FR-S5).
    /// </summary>
    private async Task<TransitionOutcome> ApplyTransitionAsync(
        Order order, OrderStatus to, ActorRole actorRole, int actorId, int? actorHubId, string? reason,
        CancellationToken cancellationToken)
    {
        var from = order.Status;
        var decision = OrderStateMachine.CanTransition(from, to, actorRole);

        if (!decision.Allowed)
        {
            await WriteHistoryAsync(
                order, from, to, actorRole, actorId,
                decision.Reason ?? $"Transition {from} → {to} is not allowed for {actorRole} (BR15).",
                applied: false, cancellationToken);
            return TransitionOutcome.Rejected(
                decision.Reason ?? $"Transition {from} → {to} is not allowed for {actorRole} (BR15).");
        }

        // BR16 / Ambiguity A5: Core encodes the obligation in TransitionResult.Reason - an allowed move
        // with a non-null Reason is legal but conditional. The caller only enforces that a reason was
        // actually supplied, and never drops Core's wording.
        var reasonRequired = decision.Reason is not null;
        if (reasonRequired && string.IsNullOrWhiteSpace(reason))
        {
            var message = decision.Reason
                          ?? $"A reason is required when {actorRole} moves {from} → {to} (BR16, Ambiguity A5).";
            await WriteHistoryAsync(order, from, to, actorRole, actorId, message, applied: false,
                cancellationToken);
            return TransitionOutcome.Rejected(message);
        }

        // BR15 state table, "Condition" column: kitchen staff act only on their own hub.
        if (actorRole == ActorRole.KitchenStaff && actorHubId != order.HubId)
        {
            var message = "Kitchen staff may only act on orders of their own hub (BR15).";
            await WriteHistoryAsync(order, from, to, actorRole, actorId, message, applied: false,
                cancellationToken);
            return TransitionOutcome.Rejected(message);
        }

        // BR15: Ready → Out for Delivery requires an assigned shipper, and only that shipper may advance.
        if (to == OrderStatus.OutForDelivery)
        {
            if (order.AssignedShipperId is null)
            {
                var message = "No shipper is assigned to this order yet (FR-F1, BR15).";
                await WriteHistoryAsync(order, from, to, actorRole, actorId, message, applied: false,
                    cancellationToken);
                return TransitionOutcome.Rejected(message);
            }

            if (actorRole == ActorRole.Shipper && order.AssignedShipperId != actorId)
            {
                var message = "Only the assigned shipper may pick this order up (BR15).";
                await WriteHistoryAsync(order, from, to, actorRole, actorId, message, applied: false,
                    cancellationToken);
                return TransitionOutcome.Rejected(message);
            }
        }

        if (to == OrderStatus.Delivered && actorRole == ActorRole.Shipper
            && order.AssignedShipperId != actorId)
        {
            var message = "Only the assigned shipper may deliver this order (BR15).";
            await WriteHistoryAsync(order, from, to, actorRole, actorId, message, applied: false,
                cancellationToken);
            return TransitionOutcome.Rejected(message);
        }

        // BR14: a COD order may not become Delivered before the cash is confirmed.
        if (to == OrderStatus.Delivered
            && order.PaymentMethod == PaymentMethod.CashOnDelivery
            && !order.IsCashConfirmed)
        {
            var message = "Confirm the cash collected before marking a COD order Delivered (BR14).";
            await WriteHistoryAsync(order, from, to, actorRole, actorId, message, applied: false,
                cancellationToken);
            return TransitionOutcome.Rejected(message);
        }

        order.Status = to;
        if (to == OrderStatus.Delivered)
        {
            order.DeliveredAt = VietnamTime.Now;
        }

        await WriteHistoryAsync(
            order, from, to, actorRole, actorId,
            reason ?? decision.Reason ?? $"{from} → {to} by {actorRole}",
            applied: true, cancellationToken);

        // BR16 / Ambiguity A2: an online-paid order that is cancelled or fails is refunded in full.
        if (to is OrderStatus.Cancelled or OrderStatus.Failed)
        {
            await RefundAsync(order, cancellationToken);
        }

        return TransitionOutcome.Ok($"Order is now {to}.");
    }

    /// <summary>Writes one immutable audit row for an accepted or refused transition (FR-S5, NFR5).</summary>
    private async Task WriteHistoryAsync(
        Order order, OrderStatus from, OrderStatus to, ActorRole actorRole, int actorId, string reason,
        bool applied, CancellationToken cancellationToken)
    {
        _db.OrderStatusHistories.Add(new OrderStatusHistory
        {
            OrderId = order.Id,
            FromStatus = from,
            ToStatus = to,
            ActorRole = actorRole,
            ActorId = actorId,
            Reason = reason.Length > 400 ? reason[..400] : reason,
            OccurredAt = VietnamTime.Now,
            Applied = applied,
        });

        await _db.SaveChangesAsync(cancellationToken);
    }

    /// <summary>
    /// Simulated full refund for an online-paid order (BR16, Ambiguity A2). Stored as a negative-amount
    /// <see cref="PaymentRecord"/> so the ledger stays append-only; COD orders collect nothing and are
    /// skipped.
    /// </summary>
    private async Task RefundAsync(Order order, CancellationToken cancellationToken)
    {
        if (order.PaymentMethod is null || order.PaymentMethod == PaymentMethod.CashOnDelivery)
        {
            return;
        }

        var paid = await _db.PaymentRecords
            .Where(p => p.OrderId == order.Id && p.Success && p.Amount > 0)
            .OrderByDescending(p => p.Id)
            .FirstOrDefaultAsync(cancellationToken);

        if (paid is null)
        {
            return;
        }

        _db.PaymentRecords.Add(new PaymentRecord
        {
            OrderId = order.Id,
            StrategyKey = paid.StrategyKey,
            Amount = -paid.Amount,
            GatewayReference = $"REFUND-{order.Id}",
            Success = true,
            CreatedAt = VietnamTime.Now,
        });

        await _db.SaveChangesAsync(cancellationToken);
    }

    /// <summary>
    /// Calls the Core strategy and records the attempt (FR-P3, NFR5). Core decides success; this method
    /// only stores the outcome.
    /// </summary>
    private async Task<PaymentResult> ChargeAsync(
        Order order, IPaymentStrategy strategy, CustomerType customerType,
        CancellationToken cancellationToken)
    {
        var request = new PaymentRequest(
            Guid.Parse($"00000000-0000-0000-0000-{order.Id:D12}"),
            order.Total,
            strategy.Method,
            customerType,
            ReturnUrl: null);

        PaymentResult result;
        try
        {
            result = await strategy.ChargeAsync(request, cancellationToken);
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            result = PaymentResult.Failed(ex.Message);
        }

        _db.PaymentRecords.Add(new PaymentRecord
        {
            OrderId = order.Id,
            StrategyKey = strategy.Key,
            Amount = order.Total,
            GatewayReference = result.GatewayReference,
            Success = result.Success,
            CreatedAt = VietnamTime.Now,
        });

        await _db.SaveChangesAsync(cancellationToken);
        return result;
    }

    /// <inheritdoc />
    public async Task<IReadOnlyList<Hub>> SuggestAlternativeHubsAsync(
        int hubId, IReadOnlyList<int> menuItemIds, CancellationToken cancellationToken = default)
    {
        if (menuItemIds.Count == 0)
        {
            return Array.Empty<Hub>();
        }

        var brandIds = await _db.MenuItems
            .AsNoTracking()
            .Where(m => menuItemIds.Contains(m.Id))
            .Select(m => m.BrandId)
            .Distinct()
            .ToListAsync(cancellationToken);

        return await _load.SuggestAlternativeHubsAsync(hubId, brandIds, cancellationToken);
    }
}
