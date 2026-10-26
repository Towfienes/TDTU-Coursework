using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Orders;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.Services;
using SaigonBite.Web.ViewModels;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// Use case F — Manage Deliveries (FR-F1 to FR-F4): assign a shipper, advance along the lifecycle, confirm
/// cash, and report a failed delivery.
/// </summary>
/// <remarks>
/// The board renders the buttons the actor is entitled to, and every POST goes through
/// <see cref="IOrderService"/>, which asks <c>OrderStateMachine</c> again. Hiding a button is presentation;
/// the rejection happens in the business layer (BR15, NFR4).
/// </remarks>
public class DeliveriesController : Controller
{
    private readonly SaigonBiteDbContext _db;
    private readonly IOrderService _orders;

    /// <summary>Creates the controller.</summary>
    public DeliveriesController(SaigonBiteDbContext db, IOrderService orders)
    {
        _db = db;
        _orders = orders;
    }

    /// <summary>Role-aware delivery board: kitchen queue, shipper runs, or the administrator's dispatcher view.</summary>
    [Authorize(Policy = Policies.Delivery)]
    [HttpGet("/deliveries")]
    public async Task<IActionResult> Index(CancellationToken cancellationToken)
    {
        var role = User.GetActorRole();

        if (role == ActorRole.Admin)
        {
            var active = new[]
            {
                OrderStatus.Placed, OrderStatus.Confirmed, OrderStatus.Preparing,
                OrderStatus.Ready, OrderStatus.OutForDelivery,
            };

            // IgnoreQueryFilters: a deactivated customer or a soft-deleted hub must not hide an active
            // order from the dispatcher - orders survive soft deletes (CONTRACT.md, FR-E4).
            var orders = await _db.Orders
                .IgnoreQueryFilters()
                .AsNoTracking()
                .Include(o => o.Hub)
                .Include(o => o.Customer)
                .Include(o => o.AssignedShipper)
                .Include(o => o.Lines)
                .Where(o => active.Contains(o.Status))
                .OrderBy(o => o.PlacedAt)
                .ToListAsync(cancellationToken);

            var shippers = await _db.Users
                .AsNoTracking()
                .Where(u => u.Role == Roles.Shipper)
                .OrderBy(u => u.DisplayName)
                .ToListAsync(cancellationToken);

            return View(new DeliveryBoardVm { Mode = "Admin", Orders = orders, Shippers = shippers });
        }

        if (role == ActorRole.KitchenStaff)
        {
            var hubId = User.GetHubId();
            var hub = hubId is null
                ? null
                : await _db.Hubs.AsNoTracking().FirstOrDefaultAsync(h => h.Id == hubId, cancellationToken);

            var statuses = new[]
            {
                OrderStatus.Placed, OrderStatus.Confirmed, OrderStatus.Preparing, OrderStatus.Ready,
            };

            var orders = await _db.Orders
                .IgnoreQueryFilters()
                .AsNoTracking()
                .Include(o => o.Hub)
                .Include(o => o.Customer)
                .Include(o => o.Lines)
                .Where(o => o.HubId == hubId && statuses.Contains(o.Status))
                .OrderBy(o => o.PlacedAt)
                .ToListAsync(cancellationToken);

            return View(new DeliveryBoardVm { Mode = "Kitchen", Orders = orders, KitchenHub = hub });
        }

        // Shipper: only the runs assigned to this account (Ambiguity A1: manual assignment).
        var shipperId = User.GetUserId() ?? 0;
        var runs = await _db.Orders
            .IgnoreQueryFilters()
            .AsNoTracking()
            .Include(o => o.Hub)
            .Include(o => o.Customer)
            .Include(o => o.Lines)
            .Where(o => o.AssignedShipperId == shipperId
                        && (o.Status == OrderStatus.Ready || o.Status == OrderStatus.OutForDelivery))
            .OrderBy(o => o.PlacedAt)
            .ToListAsync(cancellationToken);

        return View(new DeliveryBoardVm { Mode = "Shipper", Orders = runs });
    }

    /// <summary>
    /// Advances an order to the requested state. The state machine decides; the result is rendered as a
    /// message and every attempt is audited (FR-F2, BR15, FR-S5).
    /// </summary>
    [Authorize(Policy = Policies.Delivery)]
    [HttpPost("/deliveries/{id:int}/advance")]
    [HttpPost("Deliveries/Advance")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Advance(
        int id, OrderStatus? to, string? reason, CancellationToken cancellationToken)
    {
        if (to is null)
        {
            TempData["Error"] = "Choose the next state.";
            return RedirectToAction(nameof(Index));
        }

        var outcome = await _orders.AdvanceAsync(
            id, to.Value, User.GetActorRole(), User.GetUserId() ?? 0, User.GetHubId(), reason,
            cancellationToken);

        TempData[outcome.Success ? "Message" : "Error"] = outcome.Message;
        return RedirectToAction(nameof(Index));
    }

    /// <summary>
    /// Staff cancellation: kitchen staff reject a Placed order, the administrator cancels a Confirmed one.
    /// Both must supply a reason (BR16, Ambiguity A5).
    /// </summary>
    [Authorize(Policy = Policies.Kitchen)]
    [HttpPost("/deliveries/{id:int}/cancel")]
    [HttpPost("Deliveries/Cancel")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Cancel(int id, string? reason, CancellationToken cancellationToken)
    {
        var outcome = await _orders.CancelByStaffAsync(
            id, User.GetActorRole(), User.GetUserId() ?? 0, User.GetHubId(), reason, cancellationToken);

        TempData[outcome.Success ? "Message" : "Error"] = outcome.Message;
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Assigns a shipper to a Ready order (FR-F1).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/deliveries/{id:int}/assign")]
    [HttpPost("Deliveries/Assign")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Assign(int id, int shipperId, CancellationToken cancellationToken)
    {
        var outcome = await _orders.AssignShipperAsync(
            id, shipperId, User.GetUserId() ?? 0, cancellationToken);

        TempData[outcome.Success ? "Message" : "Error"] = outcome.Message;
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Confirms cash collected on a COD order (FR-F3, BR14).</summary>
    [Authorize(Policy = Policies.Shipper)]
    [HttpPost("/deliveries/{id:int}/confirm-cash")]
    [HttpPost("Deliveries/ConfirmCash")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> ConfirmCash(int id, CancellationToken cancellationToken)
    {
        var outcome = await _orders.ConfirmCashAsync(id, User.GetUserId() ?? 0, cancellationToken);
        TempData[outcome.Success ? "Message" : "Error"] = outcome.Message;
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Reports a failed delivery with a reason (FR-F4); the order becomes terminal Failed.</summary>
    [Authorize(Policy = Policies.Shipper)]
    [HttpPost("/deliveries/{id:int}/fail")]
    [HttpPost("Deliveries/Fail")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Fail(int id, string? reason, CancellationToken cancellationToken)
    {
        var outcome = await _orders.FailAsync(
            id, User.GetUserId() ?? 0, reason, cancellationToken);

        TempData[outcome.Success ? "Message" : "Error"] = outcome.Message;
        return RedirectToAction(nameof(Index));
    }
}
