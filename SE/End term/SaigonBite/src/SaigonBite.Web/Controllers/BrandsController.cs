using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.Services;
using SaigonBite.Web.ViewModels;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// Use case A — Manage Menu &amp; Brands (FR-A1 to FR-A6): public browsing for every visitor, full CRUD for
/// the administrator, availability toggling and soft delete.
/// </summary>
public class BrandsController : Controller
{
    private readonly SaigonBiteDbContext _db;
    private readonly IHubLoadService _load;
    private readonly ILogger<BrandsController> _logger;

    /// <summary>Creates the controller.</summary>
    public BrandsController(
        SaigonBiteDbContext db, IHubLoadService load, ILogger<BrandsController> logger)
    {
        _db = db;
        _load = load;
        _logger = logger;
    }

    /// <summary>
    /// Public menu of one hub, filterable by category (FR-A2). Also the page a customer builds a basket from.
    /// </summary>
    [AllowAnonymous]
    [HttpGet("/brands")]
    public async Task<IActionResult> Index(int? hubId, string? category, CancellationToken cancellationToken)
    {
        var hubs = await _db.Hubs.AsNoTracking().OrderBy(h => h.Name).ToListAsync(cancellationToken);
        var selectedHub = hubId is null ? null : hubs.FirstOrDefault(h => h.Id == hubId);

        var query = _db.Brands.AsNoTracking().Include(b => b.MenuItems).AsQueryable();
        if (selectedHub is not null)
        {
            // BR12: only the brands this hub operates are orderable from it.
            query = query.Where(b => b.HubBrands.Any(hb => hb.HubId == selectedHub.Id));
        }

        var brands = await query.OrderBy(b => b.Name).ToListAsync(cancellationToken);

        var items = brands
            .SelectMany(b => b.MenuItems)
            .Where(m => string.IsNullOrWhiteSpace(category) || m.Category == category)
            .OrderBy(m => m.Category)
            .ThenBy(m => m.Name)
            .ToList();

        var categories = brands
            .SelectMany(b => b.MenuItems)
            .Select(m => m.Category)
            .Distinct()
            .OrderBy(c => c)
            .ToList();

        // FR-B2: show the live load so a customer can see which kitchen is quiet (BR7).
        var loads = await _load.GetLoadPercentsAsync(hubs.Select(h => h.Id), cancellationToken);

        return View(new MenuPageVm
        {
            Hub = selectedHub,
            Hubs = hubs,
            Loads = loads,
            Brands = brands,
            Items = items,
            Categories = categories,
            Category = category,
        });
    }

    /// <summary>Brand detail with its menu, including unavailable items marked as such (FR-A5).</summary>
    [AllowAnonymous]
    [HttpGet("/brands/{id:int}")]
    public async Task<IActionResult> Details(int id, CancellationToken cancellationToken)
    {
        var brand = await _db.Brands
            .AsNoTracking()
            .Include(b => b.MenuItems)
            .Include(b => b.HubBrands).ThenInclude(hb => hb.Hub)
            .FirstOrDefaultAsync(b => b.Id == id, cancellationToken);

        if (brand is null)
        {
            return NotFound();
        }

        return View(brand);
    }

    /// <summary>Create form for a brand (FR-A1).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/brands/create")]
    public async Task<IActionResult> Create(CancellationToken cancellationToken)
    {
        ViewData["Hubs"] = await _db.Hubs.AsNoTracking().OrderBy(h => h.Name).ToListAsync(cancellationToken);
        return View(new BrandFormVm());
    }

    /// <summary>
    /// Creates a brand and its operating hubs. FR-A1 requires at least one hub, otherwise no customer could
    /// ever order from the brand (BR12).
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/brands/create")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(BrandFormVm form, CancellationToken cancellationToken)
    {
        if (form.HubIds.Count == 0)
        {
            ModelState.AddModelError(nameof(form.HubIds), "FR-A1: choose at least one operating hub.");
        }

        if (await _db.Brands.AnyAsync(b => b.Name == form.Name, cancellationToken))
        {
            ModelState.AddModelError(nameof(form.Name), "A brand with that name already exists.");
        }

        if (!ModelState.IsValid)
        {
            ViewData["Hubs"] = await _db.Hubs.AsNoTracking().OrderBy(h => h.Name).ToListAsync(cancellationToken);
            return View(form);
        }

        var brand = new Brand { Name = form.Name.Trim(), Description = form.Description.Trim() };
        foreach (var hubId in form.HubIds.Distinct())
        {
            brand.HubBrands.Add(new HubBrand { HubId = hubId });
        }

        _db.Brands.Add(brand);
        await _db.SaveChangesAsync(cancellationToken);
        _logger.LogInformation("Brand {Brand} created with {HubCount} hubs.", brand.Name, form.HubIds.Count);
        TempData["Message"] = $"Brand {brand.Name} created.";
        return RedirectToAction(nameof(Details), new { id = brand.Id });
    }

    /// <summary>Edit form for a brand (FR-A3).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/brands/{id:int}/edit")]
    public async Task<IActionResult> Edit(int id, CancellationToken cancellationToken)
    {
        var brand = await _db.Brands
            .Include(b => b.HubBrands)
            .FirstOrDefaultAsync(b => b.Id == id, cancellationToken);

        if (brand is null)
        {
            return NotFound();
        }

        ViewData["Hubs"] = await _db.Hubs.AsNoTracking().OrderBy(h => h.Name).ToListAsync(cancellationToken);
        return View(new BrandFormVm
        {
            Id = brand.Id,
            Name = brand.Name,
            Description = brand.Description,
            HubIds = brand.HubBrands.Select(hb => hb.HubId).ToList(),
        });
    }

    /// <summary>Saves a brand edit and re-links its hubs (FR-A3, BR12).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/brands/{id:int}/edit")]
    [HttpPost("Brands/Edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, BrandFormVm form, CancellationToken cancellationToken)
    {
        var brand = await _db.Brands
            .Include(b => b.HubBrands)
            .FirstOrDefaultAsync(b => b.Id == id, cancellationToken);

        if (brand is null)
        {
            return NotFound();
        }

        if (form.HubIds.Count == 0)
        {
            ModelState.AddModelError(nameof(form.HubIds), "FR-A1: a brand must operate at least one hub.");
        }

        if (!ModelState.IsValid)
        {
            ViewData["Hubs"] = await _db.Hubs.AsNoTracking().OrderBy(h => h.Name).ToListAsync(cancellationToken);
            return View(form);
        }

        brand.Name = form.Name.Trim();
        brand.Description = form.Description.Trim();

        var wanted = form.HubIds.Distinct().ToHashSet();
        foreach (var link in brand.HubBrands.Where(hb => !wanted.Contains(hb.HubId)).ToList())
        {
            _db.HubBrands.Remove(link);
        }

        foreach (var hubId in wanted.Where(h => brand.HubBrands.All(hb => hb.HubId != h)))
        {
            brand.HubBrands.Add(new HubBrand { HubId = hubId, BrandId = brand.Id });
        }

        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Brand {brand.Name} updated.";
        return RedirectToAction(nameof(Details), new { id = brand.Id });
    }

    /// <summary>
    /// Soft-deletes a brand (FR-A4). The row stays so historical orders and reports keep the name; the brand
    /// simply disappears from the menu.
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/brands/{id:int}/delete")]
    [HttpPost("Brands/Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(int id, CancellationToken cancellationToken)
    {
        var brand = await _db.Brands.FirstOrDefaultAsync(b => b.Id == id, cancellationToken);
        if (brand is null)
        {
            return NotFound();
        }

        brand.IsDeleted = true;
        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Brand {brand.Name} deleted. Historical orders keep its name (FR-A4).";
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Create form for a menu item (FR-A3).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/brands/{brandId:int}/items/create")]
    public async Task<IActionResult> CreateItem(int brandId, CancellationToken cancellationToken)
    {
        var brand = await _db.Brands.AsNoTracking()
            .FirstOrDefaultAsync(b => b.Id == brandId, cancellationToken);
        if (brand is null)
        {
            return NotFound();
        }

        ViewData["BrandName"] = brand.Name;
        return View(new MenuItemFormVm { BrandId = brandId });
    }

    /// <summary>Creates a menu item (FR-A3).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/brands/{brandId:int}/items/create")]
    [HttpPost("Brands/CreateItem")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> CreateItem(int brandId, MenuItemFormVm form, CancellationToken cancellationToken)
    {
        var brand = await _db.Brands.AsNoTracking()
            .FirstOrDefaultAsync(b => b.Id == brandId, cancellationToken);
        if (brand is null)
        {
            return NotFound();
        }

        if (!ModelState.IsValid)
        {
            ViewData["BrandName"] = brand.Name;
            return View(form);
        }

        _db.MenuItems.Add(new MenuItem
        {
            BrandId = brandId,
            Name = form.Name.Trim(),
            Category = form.Category.Trim(),
            Price = form.Price,
            IsAvailable = form.IsAvailable,
        });

        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Item {form.Name} created.";
        return RedirectToAction(nameof(Details), new { id = brandId });
    }

    /// <summary>Edit form for a menu item (FR-A3).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/brands/items/{id:int}/edit")]
    public async Task<IActionResult> EditItem(int id, CancellationToken cancellationToken)
    {
        var item = await _db.MenuItems.AsNoTracking()
            .FirstOrDefaultAsync(m => m.Id == id, cancellationToken);
        if (item is null)
        {
            return NotFound();
        }

        return View(new MenuItemFormVm
        {
            Id = item.Id,
            BrandId = item.BrandId,
            Name = item.Name,
            Category = item.Category,
            Price = item.Price,
            IsAvailable = item.IsAvailable,
        });
    }

    /// <summary>Saves name, category, price and availability (FR-A3, FR-A5).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/brands/items/{id:int}/edit")]
    [HttpPost("Brands/EditItem")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> EditItem(int id, MenuItemFormVm form, CancellationToken cancellationToken)
    {
        var item = await _db.MenuItems.FirstOrDefaultAsync(m => m.Id == id, cancellationToken);
        if (item is null)
        {
            return NotFound();
        }

        if (!ModelState.IsValid)
        {
            return View(form);
        }

        item.Name = form.Name.Trim();
        item.Category = form.Category.Trim();
        item.Price = form.Price;
        item.IsAvailable = form.IsAvailable;

        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Item {item.Name} updated.";
        return RedirectToAction(nameof(Details), new { id = item.BrandId });
    }

    /// <summary>Toggles availability without deleting the item (FR-A5, BR12).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/brands/items/{id:int}/availability")]
    [HttpPost("Brands/ToggleAvailability")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> ToggleAvailability(int id, CancellationToken cancellationToken)
    {
        var item = await _db.MenuItems.FirstOrDefaultAsync(m => m.Id == id, cancellationToken);
        if (item is null)
        {
            return NotFound();
        }

        item.IsAvailable = !item.IsAvailable;
        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"{item.Name} is now {(item.IsAvailable ? "available" : "unavailable")}.";
        return RedirectToAction(nameof(Details), new { id = item.BrandId });
    }

    /// <summary>
    /// Soft-deletes a menu item (FR-A4). The row survives so delivered orders and R1 keep its name and price.
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/brands/items/{id:int}/delete")]
    [HttpPost("Brands/DeleteItem")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteItem(int id, CancellationToken cancellationToken)
    {
        var item = await _db.MenuItems.FirstOrDefaultAsync(m => m.Id == id, cancellationToken);
        if (item is null)
        {
            return NotFound();
        }

        item.IsDeleted = true;
        item.IsAvailable = false;
        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"{item.Name} deleted. Past orders keep its name and price (FR-A4).";
        return RedirectToAction(nameof(Details), new { id = item.BrandId });
    }
}
