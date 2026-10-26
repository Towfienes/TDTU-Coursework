using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.Services;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// The two mandatory reports: R1 revenue and R2 hub utilisation (FR-R1, FR-R2). Administrator only.
/// </summary>
public class ReportsController : Controller
{
    private readonly IReportService _reports;

    /// <summary>Creates the controller.</summary>
    public ReportsController(IReportService reports) => _reports = reports;

    /// <summary>
    /// R1 — revenue for a date range by brand category and by payment method, excluding Cancelled and Failed
    /// orders (FR-R1).
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/reports/revenue")]
    public async Task<IActionResult> Revenue(
        DateOnly? from, DateOnly? to, CancellationToken cancellationToken)
    {
        var (start, end) = Normalise(from, to);
        ViewData["From"] = start;
        ViewData["To"] = end;
        var report = await _reports.BuildRevenueAsync(start, end, cancellationToken);
        return View(report);
    }

    /// <summary>
    /// R2 — per hub: orders handled, average Confirmed→Ready time, current load and Quiet Kitchen count
    /// (FR-R2).
    /// </summary>
    [Authorize(Policy = Policies.Admin)]
    [HttpGet("/reports/utilisation")]
    public async Task<IActionResult> Utilisation(
        DateOnly? from, DateOnly? to, CancellationToken cancellationToken)
    {
        var (start, end) = Normalise(from, to);
        ViewData["From"] = start;
        ViewData["To"] = end;
        var report = await _reports.BuildUtilisationAsync(start, end, cancellationToken);
        return View(report);
    }

    private static (DateOnly From, DateOnly To) Normalise(DateOnly? from, DateOnly? to)
    {
        var end = to ?? VietnamTime.Today;
        var start = from ?? end.AddDays(-6);

        if (start > end)
        {
            (start, end) = (end, start);
        }

        return (start, end);
    }
}
