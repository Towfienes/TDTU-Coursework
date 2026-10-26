using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Web.Data;

namespace SaigonBite.Web.Services;

/// <summary>One row of R1 grouped by brand category (FR-R1).</summary>
public sealed record RevenueByCategory(string Category, long LineCount, long Revenue);

/// <summary>One row of R1 grouped by payment method (FR-R1).</summary>
public sealed record RevenueByPaymentMethod(string Method, int OrderCount, long Revenue);

/// <summary>R1 — revenue for a date range, both groupings, excluding Cancelled and Failed orders.</summary>
public sealed record RevenueReport(
    DateOnly From,
    DateOnly To,
    long TotalRevenue,
    int OrderCount,
    IReadOnlyList<RevenueByCategory> ByCategory,
    IReadOnlyList<RevenueByPaymentMethod> ByPayment);

/// <summary>One row of R2 (FR-R2).</summary>
public sealed record HubUtilisationRow(
    int HubId,
    string HubName,
    string District,
    bool IsDeleted,
    int KitchenCapacity,
    int OrdersHandled,
    double AveragePreparationMinutes,
    int CurrentLoadPercent,
    int QuietKitchenCount);

/// <summary>R2 — hub utilisation for a date range (FR-R2).</summary>
public sealed record HubUtilisationReport(
    DateOnly From,
    DateOnly To,
    IReadOnlyList<HubUtilisationRow> Rows)
{
    /// <summary>Number of hubs at 90 % load or more, i.e. refusing new orders (BR8).</summary>
    public int RefusingHubCount => Rows.Count(r => r.CurrentLoadPercent >= 90);
}

/// <summary>
/// The two mandatory reports (R1, R2) plus the aggregates the admin dashboard needs (FR-S3).
/// </summary>
/// <remarks>
/// Report reads deliberately bypass the soft-delete filters where a deleted entity still owns historical
/// rows: FR-A4 and FR-B4 require reports to keep their names and prices. Category and brand names are
/// read from the <see cref="Data.Entities.OrderLine"/> snapshot columns, so editing or deleting a menu
/// item cannot rewrite a past report.
/// </remarks>
public interface IReportService
{
    /// <summary>R1 for a date range (FR-R1).</summary>
    Task<RevenueReport> BuildRevenueAsync(
        DateOnly from, DateOnly to, CancellationToken cancellationToken = default);

    /// <summary>R2 for a date range (FR-R2).</summary>
    Task<HubUtilisationReport> BuildUtilisationAsync(
        DateOnly from, DateOnly to, CancellationToken cancellationToken = default);

    /// <summary>Orders per status for the dashboard (FR-S3).</summary>
    Task<IReadOnlyDictionary<OrderStatus, int>> CountOrdersByStatusAsync(
        CancellationToken cancellationToken = default);
}

/// <inheritdoc />
public sealed class ReportService : IReportService
{
    private readonly SaigonBiteDbContext _db;
    private readonly IHubLoadService _load;

    /// <summary>Creates the report service.</summary>
    public ReportService(SaigonBiteDbContext db, IHubLoadService load)
    {
        _db = db;
        _load = load;
    }

    /// <inheritdoc />
    public async Task<RevenueReport> BuildRevenueAsync(
        DateOnly from, DateOnly to, CancellationToken cancellationToken = default)
    {
        var (start, end) = Range(from, to);

        // FR-R1: Cancelled and Failed orders are excluded from revenue.
        var orders = await _db.Orders
            .AsNoTracking()
            .Where(o => o.PlacedAt >= start && o.PlacedAt < end)
            .Where(o => o.Status != OrderStatus.Cancelled && o.Status != OrderStatus.Failed)
            .Select(o => new { o.Id, o.Total, o.PaymentMethod, o.Subtotal })
            .ToListAsync(cancellationToken);

        var orderIds = orders.Select(o => o.Id).ToList();
        var lines = await _db.OrderLines
            .AsNoTracking()
            .Where(l => orderIds.Contains(l.OrderId) && !l.IsRemoved)
            .Select(l => new { l.OrderId, l.CategoryName, l.UnitPrice, l.Quantity })
            .ToListAsync(cancellationToken);

        // Revenue is allocated to categories pro rata of each order's line subtotal, so the category
        // table and the payment table report the same grand total. The rounding remainder goes to the
        // largest category of that order, which keeps the sum exact without a second rounding rule.
        var byCategory = new Dictionary<string, (long Lines, long Revenue)>(StringComparer.OrdinalIgnoreCase);

        foreach (var order in orders)
        {
            var orderLines = lines.Where(l => l.OrderId == order.Id).ToList();
            var baseSubtotal = orderLines.Sum(l => l.UnitPrice * l.Quantity);

            var grouped = orderLines
                .GroupBy(l => string.IsNullOrWhiteSpace(l.CategoryName) ? "Uncategorised" : l.CategoryName)
                .Select(g => new { Category = g.Key, Lines = (long)g.Sum(l => l.Quantity), Subtotal = g.Sum(l => l.UnitPrice * l.Quantity) })
                .OrderByDescending(g => g.Subtotal)
                .ToList();

            if (grouped.Count == 0 || baseSubtotal <= 0)
            {
                if (!byCategory.TryGetValue("Uncategorised", out var none))
                {
                    none = (0, 0);
                }

                byCategory["Uncategorised"] = (none.Lines, none.Revenue + order.Total);
                continue;
            }

            // Pro-rata shares are floored; the first (largest) category absorbs the remainder, so the
            // category table always sums to exactly the order total that R1 reports by payment method.
            var shares = new long[grouped.Count];
            long reserved = 0;
            for (var i = 1; i < grouped.Count; i++)
            {
                shares[i] = (long)(order.Total * (decimal)grouped[i].Subtotal / baseSubtotal);
                reserved += shares[i];
            }

            shares[0] = order.Total - reserved;

            for (var i = 0; i < grouped.Count; i++)
            {
                var key = grouped[i].Category;
                if (!byCategory.TryGetValue(key, out var current))
                {
                    current = (0, 0);
                }

                byCategory[key] = (current.Lines + grouped[i].Lines, current.Revenue + shares[i]);
            }
        }

        var categories = byCategory
            .Select(kv => new RevenueByCategory(kv.Key, kv.Value.Lines, kv.Value.Revenue))
            .OrderByDescending(c => c.Revenue)
            .ToList();

        var payments = orders
            .GroupBy(o => o.PaymentMethod)
            .Select(g => new RevenueByPaymentMethod(
                g.Key?.ToString() ?? "Unspecified", g.Count(), g.Sum(o => o.Total)))
            .OrderByDescending(p => p.Revenue)
            .ToList();

        return new RevenueReport(
            from, to, orders.Sum(o => o.Total), orders.Count, categories, payments);
    }

    /// <inheritdoc />
    public async Task<HubUtilisationReport> BuildUtilisationAsync(
        DateOnly from, DateOnly to, CancellationToken cancellationToken = default)
    {
        var (start, end) = Range(from, to);

        // FR-B4: a soft-deleted hub keeps its report row, so the filter is bypassed and the row is marked.
        var hubs = await _db.Hubs
            .IgnoreQueryFilters()
            .AsNoTracking()
            .OrderBy(h => h.Name)
            .Select(h => new { h.Id, h.Name, h.District, h.IsDeleted, h.KitchenCapacity })
            .ToListAsync(cancellationToken);

        var orders = await _db.Orders
            .AsNoTracking()
            .Where(o => o.PlacedAt >= start && o.PlacedAt < end)
            .Select(o => new { o.Id, o.HubId, o.Status, o.QuietKitchenDiscount })
            .ToListAsync(cancellationToken);

        var orderIds = orders.Select(o => o.Id).ToList();

        // Only applied rows count: a rejected attempt did not prepare anything (FR-S5).
        var history = await _db.OrderStatusHistories
            .AsNoTracking()
            .Where(h => orderIds.Contains(h.OrderId) && h.Applied)
            .Where(h => h.ToStatus == OrderStatus.Confirmed || h.ToStatus == OrderStatus.Ready)
            .Select(h => new { h.OrderId, h.ToStatus, h.OccurredAt })
            .ToListAsync(cancellationToken);

        var confirmedAt = history
            .Where(h => h.ToStatus == OrderStatus.Confirmed)
            .GroupBy(h => h.OrderId)
            .ToDictionary(g => g.Key, g => g.Min(h => h.OccurredAt));

        var readyAt = history
            .Where(h => h.ToStatus == OrderStatus.Ready)
            .GroupBy(h => h.OrderId)
            .ToDictionary(g => g.Key, g => g.Min(h => h.OccurredAt));

        var loads = await _load.GetLoadPercentsAsync(hubs.Select(h => h.Id), cancellationToken);

        var rows = new List<HubUtilisationRow>();

        foreach (var hub in hubs)
        {
            var hubOrders = orders.Where(o => o.HubId == hub.Id).ToList();

            // "Orders handled" = orders the kitchen accepted (a Confirmed transition exists), so an
            // order rejected in Placed is not counted as work the hub performed.
            var handled = hubOrders.Count(o => confirmedAt.ContainsKey(o.Id));

            var durations = hubOrders
                .Where(o => confirmedAt.ContainsKey(o.Id) && readyAt.ContainsKey(o.Id))
                .Select(o => (readyAt[o.Id] - confirmedAt[o.Id]).TotalMinutes)
                .Where(minutes => minutes >= 0)
                .ToList();

            rows.Add(new HubUtilisationRow(
                hub.Id,
                hub.Name,
                hub.District,
                hub.IsDeleted,
                hub.KitchenCapacity,
                handled,
                durations.Count == 0 ? 0 : Math.Round(durations.Average(), 1),
                loads.TryGetValue(hub.Id, out var load) ? load : 0,
                hubOrders.Count(o => o.QuietKitchenDiscount > 0)));
        }

        return new HubUtilisationReport(from, to, rows);
    }

    /// <inheritdoc />
    public async Task<IReadOnlyDictionary<OrderStatus, int>> CountOrdersByStatusAsync(
        CancellationToken cancellationToken = default)
    {
        var counts = await _db.Orders
            .AsNoTracking()
            .GroupBy(o => o.Status)
            .Select(g => new { Status = g.Key, Count = g.Count() })
            .ToListAsync(cancellationToken);

        return counts.ToDictionary(c => c.Status, c => c.Count);
    }

    private static (DateTime Start, DateTime End) Range(DateOnly from, DateOnly to)
    {
        if (to < from)
        {
            (from, to) = (to, from);
        }

        var start = from.ToDateTime(TimeOnly.MinValue);
        var end = to.AddDays(1).ToDateTime(TimeOnly.MinValue);
        return (start, end);
    }
}
