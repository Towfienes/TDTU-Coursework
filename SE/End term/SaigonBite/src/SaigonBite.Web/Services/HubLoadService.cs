using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Orders;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;

namespace SaigonBite.Web.Services;

/// <summary>
/// Derives BR8 hub load from the database: orders currently in <c>Confirmed</c> or <c>Preparing</c>
/// divided by the hub's kitchen capacity, with the new order excluded.
/// </summary>
public interface IHubLoadService
{
    /// <summary>Load percentage of one hub, floored to a whole number (0..100).</summary>
    Task<int> GetLoadPercentAsync(int hubId, CancellationToken cancellationToken = default);

    /// <summary>Load percentages for several hubs in one query, keyed by hub id.</summary>
    Task<IReadOnlyDictionary<int, int>> GetLoadPercentsAsync(
        IEnumerable<int> hubIds, CancellationToken cancellationToken = default);

    /// <summary>
    /// FR-B5: other live hubs that operate every brand in the basket and are below the BR8 ceiling, used
    /// when the chosen hub refuses a new order.
    /// </summary>
    Task<IReadOnlyList<Hub>> SuggestAlternativeHubsAsync(
        int excludedHubId, IReadOnlyCollection<int> brandIds, CancellationToken cancellationToken = default);
}

/// <inheritdoc />
public sealed class HubLoadService : IHubLoadService
{
    private readonly SaigonBiteDbContext _db;

    /// <summary>Creates the service over the scoped context.</summary>
    public HubLoadService(SaigonBiteDbContext db) => _db = db;

    /// <inheritdoc />
    public async Task<int> GetLoadPercentAsync(int hubId, CancellationToken cancellationToken = default)
    {
        var loads = await GetLoadPercentsAsync(new[] { hubId }, cancellationToken);
        return loads.TryGetValue(hubId, out var value) ? value : 0;
    }

    /// <inheritdoc />
    /// <remarks>
    /// The division is floored rather than rounded. BR7 grants the Quiet Kitchen discount only when load
    /// is strictly below 30 %, so 3 busy slots out of 11 must read as 27 % and not as 30 %; flooring
    /// never inflates a load into a discount-denying band, and 9/10 still reads as exactly 90 % for the
    /// BR8 refusal.
    /// </remarks>
    public async Task<IReadOnlyDictionary<int, int>> GetLoadPercentsAsync(
        IEnumerable<int> hubIds, CancellationToken cancellationToken = default)
    {
        var ids = hubIds.Distinct().ToList();
        if (ids.Count == 0)
        {
            return new Dictionary<int, int>();
        }

        // IgnoreQueryFilters: a soft-deleted hub still has historical orders, and BR8 must remain
        // computable for the utilisation report (FR-B4 keeps the rows).
        var hubs = await _db.Hubs
            .IgnoreQueryFilters()
            .AsNoTracking()
            .Where(h => ids.Contains(h.Id))
            .Select(h => new { h.Id, h.KitchenCapacity })
            .ToListAsync(cancellationToken);

        var busy = await _db.Orders
            .AsNoTracking()
            .Where(o => ids.Contains(o.HubId)
                        && (o.Status == OrderStatus.Confirmed || o.Status == OrderStatus.Preparing))
            .GroupBy(o => o.HubId)
            .Select(g => new { HubId = g.Key, Count = g.Count() })
            .ToListAsync(cancellationToken);

        var busyByHub = busy.ToDictionary(b => b.HubId, b => b.Count);
        var result = new Dictionary<int, int>();

        foreach (var hub in hubs)
        {
            if (hub.KitchenCapacity <= 0)
            {
                // FR-B1 forbids a zero capacity; defensively no orders are ever admitted.
                result[hub.Id] = 100;
                continue;
            }

            var count = busyByHub.TryGetValue(hub.Id, out var c) ? c : 0;
            result[hub.Id] = (int)Math.Floor(count * 100m / hub.KitchenCapacity);
        }

        return result;
    }

    /// <summary>
    /// Hubs that can still accept an order for the same basket: every other live hub that operates all
    /// the brands in the basket and is below the BR8 ceiling. Used by the FR-B5 "choose another hub".
    /// </summary>
    public async Task<IReadOnlyList<Hub>> SuggestAlternativeHubsAsync(
        int excludedHubId, IReadOnlyCollection<int> brandIds, CancellationToken cancellationToken = default)
    {
        if (brandIds.Count == 0)
        {
            return Array.Empty<Hub>();
        }

        var candidates = await _db.Hubs
            .AsNoTracking()
            .Where(h => h.Id != excludedHubId)
            .Where(h => h.HubBrands.Count(hb => brandIds.Contains(hb.BrandId)) == brandIds.Count)
            .OrderBy(h => h.District)
            .ToListAsync(cancellationToken);

        var loads = await GetLoadPercentsAsync(candidates.Select(h => h.Id), cancellationToken);

        return candidates
            .Where(h => !loads.TryGetValue(h.Id, out var load) || load < 90)
            .ToList();
    }
}
