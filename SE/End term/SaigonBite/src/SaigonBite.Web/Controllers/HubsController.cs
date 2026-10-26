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
/// Use case B — Manage Hubs &amp; Capacity (FR-B1 to FR-B5): create, edit capacity, soft delete, and show
/// the derived load that BR8 and BR7 depend on.
/// </summary>
public class HubsController : Controller
{
    private readonly SaigonBiteDbContext _db;
    private readonly IHubLoadService _load;

    /// <summary>Creates the controller.</summary>
    public HubsController(SaigonBiteDbContext db, IHubLoadService load)
    {
        _db = db;
        _load = load;
    }

    /// <summary>
    /// Hub board with the live load percentage (FR-B2). Public, because a customer must be able to see which
    /// kitchen is quiet before ordering (BR7) and which one is refusing orders (BR8).
    /// </summary>
    [AllowAnonymous]
    [HttpGet("/hubs")]
    public async Task<IActionResult> Index(CancellationToken cancellationToken)
    {
        var hubs = await _db.Hubs.AsNoTracking().OrderBy(h => h.Name).ToListAsync(cancellationToken);
        var loads = await _load.GetLoadPercentsAsync(hubs.Select(h => h.Id), cancellationToken);

        var busy = await _db.Orders
            .AsNoTracking()
            .Where(o => o.Status == OrderStatus.Confirmed || o.Status == OrderStatus.Preparing)
            .GroupBy(o => o.HubId)
            .Select(g => new { HubId = g.Key, Count = g.Count() })
            .ToListAsync(cancellationToken);
        var busyByHub = busy.ToDictionary(b => b.HubId, b => b.Count);

        var rows = hubs.Select(h => new HubRowVm
        {
            Hub = h,
            LoadPercent = loads.TryGetValue(h.Id, out var value) ? value : 0,
            BusyOrders = busyByHub.TryGetValue(h.Id, out var count) ? count : 0,
        }).ToList();

        return View(rows);
    }

    /// <summary>Create form for a hub (FR-B1).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/hubs/create")]
    public IActionResult Create() => View(new HubFormVm());

    /// <summary>Creates a hub; BR8 needs a capacity of at least one (FR-B1).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/hubs/create")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(HubFormVm form, CancellationToken cancellationToken)
    {
        // FR-B1 / BR8: a zero capacity would make the load division undefined.
        if (form.KitchenCapacity <= 0)
        {
            ModelState.AddModelError(
                nameof(form.KitchenCapacity), "BR8: the kitchen capacity must be a whole number above zero.");
        }

        if (!ModelState.IsValid)
        {
            return View(form);
        }

        var hub = new Hub
        {
            Name = form.Name.Trim(),
            District = form.District.Trim(),
            Address = form.Address.Trim(),
            KitchenCapacity = form.KitchenCapacity,
        };

        _db.Hubs.Add(hub);
        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Hub {hub.Name} created.";
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Edit form for a hub (FR-B3).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/hubs/{id:int}/edit")]
    public async Task<IActionResult> Edit(int id, CancellationToken cancellationToken)
    {
        var hub = await _db.Hubs.AsNoTracking().FirstOrDefaultAsync(h => h.Id == id, cancellationToken);
        if (hub is null)
        {
            return NotFound();
        }

        return View(new HubFormVm
        {
            Id = hub.Id,
            Name = hub.Name,
            District = hub.District,
            Address = hub.Address,
            KitchenCapacity = hub.KitchenCapacity,
        });
    }

    /// <summary>
    /// Saves a hub edit. The load is derived on every read, so changing the capacity recomputes it
    /// immediately (FR-B3) without any denormalized field to forget.
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/hubs/{id:int}/edit")]
    [HttpPost("Hubs/Edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, HubFormVm form, CancellationToken cancellationToken)
    {
        var hub = await _db.Hubs.FirstOrDefaultAsync(h => h.Id == id, cancellationToken);
        if (hub is null)
        {
            return NotFound();
        }

        if (form.KitchenCapacity <= 0)
        {
            ModelState.AddModelError(
                nameof(form.KitchenCapacity), "BR8: the kitchen capacity must be a whole number above zero.");
        }

        if (!ModelState.IsValid)
        {
            return View(form);
        }

        hub.Name = form.Name.Trim();
        hub.District = form.District.Trim();
        hub.Address = form.Address.Trim();
        hub.KitchenCapacity = form.KitchenCapacity;

        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Hub {hub.Name} updated. Load recomputed from the new capacity (FR-B3).";
        return RedirectToAction(nameof(Index));
    }

    /// <summary>
    /// Soft-deletes a hub (FR-B4): it leaves ordering but its historical orders and R2 rows survive.
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/hubs/{id:int}/delete")]
    [HttpPost("Hubs/Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(int id, CancellationToken cancellationToken)
    {
        var hub = await _db.Hubs.FirstOrDefaultAsync(h => h.Id == id, cancellationToken);
        if (hub is null)
        {
            return NotFound();
        }

        hub.IsDeleted = true;
        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Hub {hub.Name} deleted. Its orders and report rows are preserved (FR-B4).";
        return RedirectToAction(nameof(Index));
    }
}
