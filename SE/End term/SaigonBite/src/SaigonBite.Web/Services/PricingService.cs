using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Pricing;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;

namespace SaigonBite.Web.Services;

/// <summary>One line resolved against the database: identifiers, snapshot text and the authoritative price.</summary>
public sealed record ResolvedLine(
    int MenuItemId, string ItemName, string BrandName, string CategoryName, long UnitPrice, int Quantity)
{
    /// <summary>Line subtotal used for the BR10 step 1 display before the engine runs.</summary>
    public long LineTotal => UnitPrice * Quantity;
}

/// <summary>
/// The BR17 snapshot inputs plus the optional voucher, i.e. everything except the lines. Passing this
/// record is what makes a re-price reuse stored conditions instead of current ones.
/// </summary>
public sealed record PriceConditions(
    DateTime PlacedAt, decimal DistanceKm, bool RainFlag, int HubLoadPercent, Voucher? Voucher);

/// <summary>
/// Result of one pricing run: the engine output, the voucher actually offered and a notice when a
/// voucher code was refused by its own BR9 window or minimum.
/// </summary>
public sealed record PriceComputation(
    PriceResult Result,
    Voucher? Voucher,
    string? VoucherNotice)
{
    /// <summary>True when the engine accepted every rule.</summary>
    public bool IsAccepted => Result.IsAccepted;
}

/// <summary>
/// Boundary adapter around <c>PricingEngine.Calculate</c> (AGENTS.md hard rule 2). It resolves what the
/// engine is not allowed to know (database prices, hub operating links) and then hands a pure
/// <see cref="PriceContext"/> to Core. No amount is computed here.
/// </summary>
public interface IPricingService
{
    /// <summary>
    /// Resolves cart lines against the live menu of one hub: available items only (FR-A5) whose brand the
    /// hub operates (FR-A6, BR12), with the database price and the BR12 quantity limits.
    /// </summary>
    Task<(IReadOnlyList<ResolvedLine> Lines, string? Error)> ResolveCartLinesAsync(
        int hubId, IReadOnlyList<CartLine> lines, CancellationToken cancellationToken = default);

    /// <summary>Finds a voucher code and validates its active flag and validity window (BR9).</summary>
    Task<(Voucher? Voucher, string? Error)> ResolveVoucherAsync(
        string? code, DateTime placedAt, CancellationToken cancellationToken = default);

    /// <summary>Runs the pure engine once and adds the BR9 minimum-subtotal notice for display.</summary>
    PriceComputation Compute(Hub hub, IReadOnlyList<ResolvedLine> lines, PriceConditions conditions);

    /// <summary>Convenience overload that resolves, prices and returns both halves.</summary>
    Task<(PriceComputation? Computation, IReadOnlyList<ResolvedLine> Lines, string? Error)> PriceCartAsync(
        int hubId, IReadOnlyList<CartLine> lines, decimal distanceKm, string? voucherCode,
        DateTime? placedAt, bool? rainFlag, int? hubLoadPercent,
        CancellationToken cancellationToken = default);
}

/// <inheritdoc />
public sealed class PricingService : IPricingService
{
    private readonly SaigonBiteDbContext _db;
    private readonly IHubLoadService _load;
    private readonly IPlatformSettingsService _settings;

    /// <summary>Creates the adapter over the scoped context, the load service and the rain flag.</summary>
    public PricingService(
        SaigonBiteDbContext db, IHubLoadService load, IPlatformSettingsService settings)
    {
        _db = db;
        _load = load;
        _settings = settings;
    }

    /// <inheritdoc />
    public async Task<(IReadOnlyList<ResolvedLine> Lines, string? Error)> ResolveCartLinesAsync(
        int hubId, IReadOnlyList<CartLine> lines, CancellationToken cancellationToken = default)
    {
        if (lines.Count == 0)
        {
            return (Array.Empty<ResolvedLine>(), "The basket is empty.");
        }

        // BR12: at most 30 lines, each with a quantity of 1..20.
        if (lines.Count > CartLimits.MaxLines)
        {
            return (Array.Empty<ResolvedLine>(),
                $"BR12: an order may contain at most {CartLimits.MaxLines} lines.");
        }

        if (lines.Any(l => l.Quantity < 1 || l.Quantity > CartLimits.MaxQuantityPerLine))
        {
            return (Array.Empty<ResolvedLine>(),
                $"BR12: a line quantity must be between 1 and {CartLimits.MaxQuantityPerLine}.");
        }

        var ids = lines.Select(l => l.MenuItemId).Distinct().ToList();

        // FR-A5 + FR-A6 + BR12: only available items of brands this hub operates.
        var items = await _db.MenuItems
            .AsNoTracking()
            .Where(m => ids.Contains(m.Id) && m.IsAvailable)
            .Where(m => m.Brand!.HubBrands.Any(hb => hb.HubId == hubId))
            .Select(m => new
            {
                m.Id,
                m.Name,
                m.Price,
                m.Category,
                BrandName = m.Brand!.Name,
            })
            .ToListAsync(cancellationToken);

        if (items.Count != ids.Count)
        {
            return (Array.Empty<ResolvedLine>(),
                "One or more items are unavailable or are not operated by this hub (FR-A5, FR-A6, BR12).");
        }

        var resolved = lines
            .Select(l =>
            {
                var item = items.First(i => i.Id == l.MenuItemId);
                return new ResolvedLine(
                    item.Id, item.Name, item.BrandName, item.Category, item.Price, l.Quantity);
            })
            .ToList();

        return (resolved, null);
    }

    /// <inheritdoc />
    public async Task<(Voucher? Voucher, string? Error)> ResolveVoucherAsync(
        string? code, DateTime placedAt, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(code))
        {
            return (null, null);
        }

        var normalised = code.Trim().ToUpperInvariant();
        var voucher = await _db.Vouchers
            .AsNoTracking()
            .FirstOrDefaultAsync(v => v.Code == normalised, cancellationToken);

        if (voucher is null)
        {
            return (null, "That voucher code does not exist.");
        }

        // BR9: a voucher must be active and inside its validity window. The engine receives the same
        // flags in VoucherRequest and re-checks them; this guard exists so the customer is told why.
        if (!voucher.IsActive)
        {
            return (null, "That voucher is no longer active.");
        }

        var day = DateOnly.FromDateTime(placedAt);
        if (day < voucher.ValidFrom || day > voucher.ValidTo)
        {
            return (null, "That voucher is outside its validity window.");
        }

        return (voucher, null);
    }

    /// <inheritdoc />
    public PriceComputation Compute(Hub hub, IReadOnlyList<ResolvedLine> lines, PriceConditions conditions)
    {
        var context = new PriceContext
        {
            Lines = lines
                .Select(l => new PriceLineRequest(l.MenuItemId, l.Quantity, l.UnitPrice))
                .ToList(),
            DistanceKm = conditions.DistanceKm,
            PlacementTime = conditions.PlacedAt,
            RainFlagOn = conditions.RainFlag,
            HubLoadPercent = conditions.HubLoadPercent,

            // BR8: 90 % or above means the hub refuses new orders. The engine is told explicitly so it
            // can reject with the BR8 code even if it only inspected one of the two fields.
            HubRejectsNewOrders = conditions.HubLoadPercent >= 90,
            Voucher = conditions.Voucher is null
                ? null
                : new VoucherRequest(
                    conditions.Voucher.Type,
                    conditions.Voucher.Value,
                    conditions.Voucher.MaxDiscount,
                    conditions.Voucher.MinSubtotal,
                    conditions.Voucher.IsActive,
                    conditions.Voucher.ValidFrom,
                    conditions.Voucher.ValidTo),
        };

        var result = PricingEngine.Calculate(context);

        // BR9 minimum is checked against S; when the engine declined the voucher, say so instead of
        // showing a silently missing discount. The comparison reads the engine's own subtotal.
        string? notice = null;
        if (conditions.Voucher is not null
            && result.VoucherDiscount == 0
            && conditions.Voucher.Value > 0
            && result.Subtotal < conditions.Voucher.MinSubtotal)
        {
            notice = $"Voucher {conditions.Voucher.Code} needs a subtotal of at least "
                     + $"{conditions.Voucher.MinSubtotal:N0} ₫ and was not applied.";
        }

        return new PriceComputation(result, conditions.Voucher, notice);
    }

    /// <inheritdoc />
    public async Task<(PriceComputation? Computation, IReadOnlyList<ResolvedLine> Lines, string? Error)>
        PriceCartAsync(
            int hubId, IReadOnlyList<CartLine> lines, decimal distanceKm, string? voucherCode,
            DateTime? placedAt, bool? rainFlag, int? hubLoadPercent,
            CancellationToken cancellationToken = default)
    {
        var hub = await _db.Hubs
            .AsNoTracking()
            .FirstOrDefaultAsync(h => h.Id == hubId, cancellationToken);

        if (hub is null)
        {
            return (null, Array.Empty<ResolvedLine>(), "That hub is no longer available.");
        }

        var (resolved, error) = await ResolveCartLinesAsync(hubId, lines, cancellationToken);
        if (error is not null)
        {
            return (null, Array.Empty<ResolvedLine>(), error);
        }

        var placed = placedAt ?? VietnamTime.Now;
        var (voucher, voucherError) = await ResolveVoucherAsync(voucherCode, placed, cancellationToken);
        if (voucherError is not null)
        {
            return (null, resolved, voucherError);
        }

        // BR17: an edit passes the stored snapshot; a new order passes the current conditions.
        var rain = rainFlag ?? await _settings.GetRainFlagAsync(cancellationToken);
        var load = hubLoadPercent ?? await _load.GetLoadPercentAsync(hubId, cancellationToken);

        var computation = Compute(hub, resolved, new PriceConditions(placed, distanceKm, rain, load, voucher));
        return (computation, resolved, null);
    }
}

/// <summary>BR12 limits shared by the cart service, the pricing adapter and the controllers.</summary>
public static class CartLimits
{
    /// <summary>At most 30 lines per order (BR12, FR-D1).</summary>
    public const int MaxLines = 30;

    /// <summary>Quantity 1..20 per line (BR12, FR-D1).</summary>
    public const int MaxQuantityPerLine = 20;
}
