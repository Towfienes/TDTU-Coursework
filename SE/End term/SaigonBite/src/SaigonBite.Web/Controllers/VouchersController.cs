using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Payments;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.ViewModels;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// Use case C — Manage Vouchers (FR-C1 to FR-C3, BR9). Only the administrator reaches these actions.
/// </summary>
/// <remarks>
/// A voucher is never deleted: FR-C2 exposes "deactivate", which sets <see cref="Voucher.IsActive"/>. The
/// discount arithmetic itself is Core's, so this controller stores the parameters and nothing else.
/// </remarks>
public class VouchersController : Controller
{
    private readonly SaigonBiteDbContext _db;

    /// <summary>Creates the controller.</summary>
    public VouchersController(SaigonBiteDbContext db) => _db = db;

    /// <summary>Lists every voucher, active or not (FR-C2).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/vouchers")]
    public async Task<IActionResult> Index(CancellationToken cancellationToken)
    {
        var vouchers = await _db.Vouchers
            .AsNoTracking()
            .OrderByDescending(v => v.IsActive)
            .ThenBy(v => v.Code)
            .ToListAsync(cancellationToken);

        return View(vouchers);
    }

    /// <summary>Create form for a voucher (FR-C1).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/vouchers/create")]
    public IActionResult Create() => View(new VoucherFormVm());

    /// <summary>Creates a voucher (FR-C1, BR9).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/vouchers/create")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(VoucherFormVm form, CancellationToken cancellationToken)
    {
        var error = await ValidateAsync(form, existingId: null, cancellationToken);
        if (error is not null)
        {
            ModelState.AddModelError(string.Empty, error);
        }

        if (!ModelState.IsValid)
        {
            return View(form);
        }

        _db.Vouchers.Add(new Voucher
        {
            Code = form.Code.Trim().ToUpperInvariant(),
            Type = form.Type,
            Value = form.Value,
            MaxDiscount = form.Type == VoucherType.Percent ? form.MaxDiscount : form.Value,
            MinSubtotal = form.MinSubtotal,
            ValidFrom = form.ValidFrom,
            ValidTo = form.ValidTo,
            IsActive = form.IsActive,
        });

        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Voucher {form.Code.ToUpperInvariant()} created.";
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Edit form for a voucher (FR-C2).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/vouchers/{id:int}/edit")]
    public async Task<IActionResult> Edit(int id, CancellationToken cancellationToken)
    {
        var voucher = await _db.Vouchers.AsNoTracking()
            .FirstOrDefaultAsync(v => v.Id == id, cancellationToken);

        if (voucher is null)
        {
            return NotFound();
        }

        return View(new VoucherFormVm
        {
            Id = voucher.Id,
            Code = voucher.Code,
            Type = voucher.Type,
            Value = voucher.Value,
            MaxDiscount = voucher.MaxDiscount,
            MinSubtotal = voucher.MinSubtotal,
            ValidFrom = voucher.ValidFrom,
            ValidTo = voucher.ValidTo,
            IsActive = voucher.IsActive,
        });
    }

    /// <summary>Saves a voucher edit (FR-C2).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/vouchers/{id:int}/edit")]
    [HttpPost("Vouchers/Edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, VoucherFormVm form, CancellationToken cancellationToken)
    {
        var voucher = await _db.Vouchers.FirstOrDefaultAsync(v => v.Id == id, cancellationToken);
        if (voucher is null)
        {
            return NotFound();
        }

        var error = await ValidateAsync(form, existingId: id, cancellationToken);
        if (error is not null)
        {
            ModelState.AddModelError(string.Empty, error);
        }

        if (!ModelState.IsValid)
        {
            return View(form);
        }

        voucher.Code = form.Code.Trim().ToUpperInvariant();
        voucher.Type = form.Type;
        voucher.Value = form.Value;
        voucher.MaxDiscount = form.Type == VoucherType.Percent ? form.MaxDiscount : form.Value;
        voucher.MinSubtotal = form.MinSubtotal;
        voucher.ValidFrom = form.ValidFrom;
        voucher.ValidTo = form.ValidTo;
        voucher.IsActive = form.IsActive;

        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] = $"Voucher {voucher.Code} updated.";
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Deactivates or reactivates a voucher — the FR-C2 removal, never a hard delete.</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/vouchers/{id:int}/toggle")]
    [HttpPost("Vouchers/Toggle")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Toggle(int id, CancellationToken cancellationToken)
    {
        var voucher = await _db.Vouchers.FirstOrDefaultAsync(v => v.Id == id, cancellationToken);
        if (voucher is null)
        {
            return NotFound();
        }

        voucher.IsActive = !voucher.IsActive;
        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] =
            $"Voucher {voucher.Code} is now {(voucher.IsActive ? "active" : "inactive")} (FR-C2).";
        return RedirectToAction(nameof(Index));
    }

    private async Task<string?> ValidateAsync(
        VoucherFormVm form, int? existingId, CancellationToken cancellationToken)
    {
        var code = form.Code.Trim().ToUpperInvariant();

        if (code.Length == 0)
        {
            return "A voucher code is required.";
        }

        if (await _db.Vouchers.AnyAsync(
                v => v.Code == code && (existingId == null || v.Id != existingId), cancellationToken))
        {
            return "A voucher with that code already exists.";
        }

        if (form.ValidTo < form.ValidFrom)
        {
            return "The validity window ends before it starts (BR9).";
        }

        // BR9: a percentage voucher without a cap could discount an unbounded amount, so require one.
        if (form.Type == VoucherType.Percent && (form.Value <= 0 || form.Value > 100))
        {
            return "A percentage voucher needs a value between 1 and 100 (BR9).";
        }

        if (form.Type == VoucherType.Percent && form.MaxDiscount <= 0)
        {
            return "A percentage voucher needs a maximum discount above zero (BR9).";
        }

        return null;
    }
}
