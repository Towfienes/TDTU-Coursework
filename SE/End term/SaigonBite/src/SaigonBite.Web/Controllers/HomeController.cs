using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Services;
using SaigonBite.Web.ViewModels;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// Landing page and shared error screens. The landing page is the one place that shows every hub with its
/// live BR8 load, so a customer can see which kitchen is quiet before starting an order (FR-B2, BR7).
/// </summary>
public class HomeController : Controller
{
    private readonly SaigonBiteDbContext _db;
    private readonly IHubLoadService _load;
    private readonly IPlatformSettingsService _settings;

    /// <summary>Creates the controller.</summary>
    public HomeController(
        SaigonBiteDbContext db, IHubLoadService load, IPlatformSettingsService settings)
    {
        _db = db;
        _load = load;
        _settings = settings;
    }

    /// <summary>Hero page with the hub load board and the brand catalogue.</summary>
    [AllowAnonymous]
    public async Task<IActionResult> Index(CancellationToken cancellationToken)
    {
        var hubs = await _db.Hubs
            .AsNoTracking()
            .OrderBy(h => h.Name)
            .ToListAsync(cancellationToken);

        var loads = await _load.GetLoadPercentsAsync(hubs.Select(h => h.Id), cancellationToken);
        var busy = await _db.Orders
            .AsNoTracking()
            .Where(o => o.Status == Core.Orders.OrderStatus.Confirmed
                        || o.Status == Core.Orders.OrderStatus.Preparing)
            .GroupBy(o => o.HubId)
            .Select(g => new { HubId = g.Key, Count = g.Count() })
            .ToListAsync(cancellationToken);
        var busyByHub = busy.ToDictionary(b => b.HubId, b => b.Count);

        var brands = await _db.Brands
            .AsNoTracking()
            .OrderBy(b => b.Name)
            .ToListAsync(cancellationToken);

        return View(new HomePageVm
        {
            Hubs = hubs.Select(h => new HubRowVm
            {
                Hub = h,
                LoadPercent = loads.TryGetValue(h.Id, out var value) ? value : 0,
                BusyOrders = busyByHub.TryGetValue(h.Id, out var count) ? count : 0,
            }).ToList(),
            Brands = brands,
            RainFlag = await _settings.GetRainFlagAsync(cancellationToken),
        });
    }

    /// <summary>Generic error page.</summary>
    [AllowAnonymous]
    public IActionResult Error() => View("~/Views/Shared/Error.cshtml");

    /// <summary>Status-code page used by the status-code re-execute middleware.</summary>
    [AllowAnonymous]
    public IActionResult Status(int code)
    {
        ViewData["StatusCode"] = code;
        return View("~/Views/Shared/Status.cshtml");
    }
}
