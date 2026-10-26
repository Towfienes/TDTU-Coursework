using System.Text.Json;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Orders;
using SaigonBite.Web.Data;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.Services;
using SaigonBite.Web.ViewModels;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// Administrator dashboard (FR-S3, Tier 4): R1 and R2 as Chart.js charts plus tables, the heavy-rain flag
/// (FR-S4) and account management (FR-E4).
/// </summary>
public class AdminController : Controller
{
    private readonly SaigonBiteDbContext _db;
    private readonly IReportService _reports;
    private readonly IPlatformSettingsService _settings;

    /// <summary>Creates the controller.</summary>
    public AdminController(
        SaigonBiteDbContext db, IReportService reports, IPlatformSettingsService settings)
    {
        _db = db;
        _reports = reports;
        _settings = settings;
    }

    /// <summary>Interactive dashboard: both reports, the order funnel and the rain-flag switch.</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/admin")]
    public async Task<IActionResult> Index(
        DateOnly? from, DateOnly? to, CancellationToken cancellationToken)
    {
        var end = to ?? VietnamTime.Today;
        var start = from ?? end.AddDays(-6);
        if (start > end)
        {
            (start, end) = (end, start);
        }

        var revenue = await _reports.BuildRevenueAsync(start, end, cancellationToken);
        var utilisation = await _reports.BuildUtilisationAsync(start, end, cancellationToken);
        var statusCounts = await _reports.CountOrdersByStatusAsync(cancellationToken);

        ViewData["From"] = start;
        ViewData["To"] = end;

        return View(new DashboardVm
        {
            Revenue = revenue,
            Utilisation = utilisation,
            StatusCounts = statusCounts,
            RainFlag = await _settings.GetRainFlagAsync(cancellationToken),
            CategoryChartJson = BuildBarChart(
                "Revenue by brand category (₫)",
                revenue.ByCategory.Select(c => c.Category).ToList(),
                revenue.ByCategory.Select(c => c.Revenue).ToList()),
            PaymentChartJson = BuildPieChart(
                "Revenue by payment method (₫)",
                revenue.ByPayment.Select(p => p.Method).ToList(),
                revenue.ByPayment.Select(p => p.Revenue).ToList()),
            LoadChartJson = BuildBarChart(
                "Current hub load (%)",
                utilisation.Rows.Select(r => r.HubName).ToList(),
                utilisation.Rows.Select(r => (long)r.CurrentLoadPercent).ToList()),
        });
    }

    /// <summary>Toggles the global heavy-rain flag that BR5 and BR5's snapshot depend on (FR-S4).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/admin/rain-flag")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> RainFlag(bool enabled, CancellationToken cancellationToken)
    {
        var value = await _settings.SetRainFlagAsync(enabled, cancellationToken);
        TempData["Message"] = value
            ? "Heavy-rain flag is ON: new orders include the 10,000 ₫ surcharge (BR5)."
            : "Heavy-rain flag is OFF: no rain surcharge on new orders (BR5).";
        return RedirectToAction(nameof(Index));
    }

    /// <summary>Account list for FR-E4 (view every account of every role and customer type).</summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/admin/users")]
    public async Task<IActionResult> Users(CancellationToken cancellationToken)
    {
        var users = await _db.Users
            .IgnoreQueryFilters()
            .AsNoTracking()
            .Include(u => u.Hub)
            .OrderBy(u => u.Role)
            .ThenBy(u => u.DisplayName)
            .ToListAsync(cancellationToken);

        return View(users);
    }

    /// <summary>
    /// Deactivates or reactivates an account — the FR-E4 removal, a soft delete, never a hard delete.
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpPost("/admin/users/{id:int}/toggle")]
    [HttpPost("Admin/ToggleUser")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> ToggleUser(int id, CancellationToken cancellationToken)
    {
        var user = await _db.Users
            .IgnoreQueryFilters()
            .FirstOrDefaultAsync(u => u.Id == id, cancellationToken);

        if (user is null)
        {
            return NotFound();
        }

        if (user.Id == User.GetUserId())
        {
            TempData["Error"] = "You cannot deactivate your own account.";
            return RedirectToAction(nameof(Users));
        }

        user.IsDeleted = !user.IsDeleted;
        await _db.SaveChangesAsync(cancellationToken);
        TempData["Message"] =
            $"{user.DisplayName} is now {(user.IsDeleted ? "deactivated" : "active")} (FR-E4).";
        return RedirectToAction(nameof(Users));
    }

    private static string BuildBarChart(string label, IReadOnlyList<string> labels, IReadOnlyList<long> values) =>
        JsonSerializer.Serialize(new
        {
            type = "bar",
            data = new
            {
                labels,
                datasets = new[]
                {
                    new
                    {
                        label,
                        data = values,
                        backgroundColor = "#c2410c",
                        borderRadius = 6,
                        maxBarThickness = 48,
                    },
                },
            },
            options = new
            {
                responsive = true,
                maintainAspectRatio = false,
                plugins = new { legend = new { display = false } },
                scales = new
                {
                    y = new { beginAtZero = true, ticks = new { precision = 0 } },
                    x = new { ticks = new { autoSkip = false } },
                },
            },
        });

    private static string BuildPieChart(string label, IReadOnlyList<string> labels, IReadOnlyList<long> values) =>
        JsonSerializer.Serialize(new
        {
            type = "doughnut",
            data = new
            {
                labels,
                datasets = new[]
                {
                    new
                    {
                        label,
                        data = values,
                        backgroundColor = new[]
                        {
                            "#c2410c", "#0f766e", "#a16207", "#7c3aed", "#0369a1", "#b91c1c",
                        },
                        borderWidth = 0,
                    },
                },
            },
            options = new
            {
                responsive = true,
                maintainAspectRatio = false,
                plugins = new { legend = new { position = "bottom" } },
            },
        });
}
