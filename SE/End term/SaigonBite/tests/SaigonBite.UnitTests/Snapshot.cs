using SaigonBite.Core.Payments;
using SaigonBite.Core.Pricing;

namespace SaigonBite.UnitTests;

/// <summary>
/// Builds the <see cref="PriceContext"/> snapshots the pricing tests price (BR17).
/// </summary>
/// <remarks>
/// Defaults are chosen to isolate one rule per test: S = 200,000, 3.2 km (D = 25,000), 15:00 (no rush
/// window), rain off, 20 % hub load (Quiet Kitchen discount active), no voucher. Each test overrides only
/// the input its rule is about, so a failure names exactly one rule.
/// </remarks>
internal static class Snapshot
{
    /// <summary>Tuesday 20 October 2026, 15:00 — outside both BR4 rush windows.</summary>
    internal static readonly DateTime QuietAfternoon = new(2026, 10, 20, 15, 0, 0, DateTimeKind.Unspecified);

    /// <summary>A placement date comfortably inside <see cref="ValidVoucher"/>'s validity window.</summary>
    internal static readonly DateOnly DefaultValidFrom = new(2026, 1, 1);

    /// <inheritdoc cref="DefaultValidFrom"/>
    internal static readonly DateOnly DefaultValidTo = new(2026, 12, 31);

    /// <summary>
    /// A context with one line worth <paramref name="subtotal"/>, and every other input at its neutral
    /// default.
    /// </summary>
    internal static PriceContext With(
        long subtotal = 200_000,
        decimal distanceKm = 3.2m,
        DateTime? placedAt = null,
        bool rain = false,
        int hubLoadPercent = 20,
        VoucherRequest? voucher = null,
        bool hubRejectsNewOrders = false) =>
        new()
        {
            Lines = [new PriceLineRequest(MenuItemId: 1, Quantity: 1, UnitPrice: subtotal)],
            DistanceKm = distanceKm,
            PlacementTime = placedAt ?? QuietAfternoon,
            RainFlagOn = rain,
            HubLoadPercent = hubLoadPercent,
            HubRejectsNewOrders = hubRejectsNewOrders,
            Voucher = voucher,
        };

    /// <summary>A context from explicit lines, for the BR12 line-limit tests.</summary>
    internal static PriceContext WithLines(
        IReadOnlyList<PriceLineRequest> lines,
        decimal distanceKm = 3.2m,
        DateTime? placedAt = null,
        int hubLoadPercent = 20) =>
        new()
        {
            Lines = lines,
            DistanceKm = distanceKm,
            PlacementTime = placedAt ?? QuietAfternoon,
            RainFlagOn = false,
            HubLoadPercent = hubLoadPercent,
        };

    /// <summary><paramref name="lineCount"/> lines of one unit each, priced so the subtotal clears BR1.</summary>
    internal static PriceContext WithLineCount(int lineCount, long unitPrice = 2_000) =>
        WithLines(Enumerable
            .Range(1, lineCount)
            .Select(index => new PriceLineRequest(MenuItemId: index, Quantity: 1, UnitPrice: unitPrice))
            .ToList());

    /// <summary>A PERCENT voucher, active and inside its default validity window unless overridden.</summary>
    internal static VoucherRequest Percent(
        long percent,
        long maxDiscount,
        long minSubtotal = 0,
        bool active = true,
        DateOnly? validFrom = null,
        DateOnly? validTo = null) =>
        new(VoucherType.Percent, percent, maxDiscount, minSubtotal, active,
            validFrom ?? DefaultValidFrom, validTo ?? DefaultValidTo);

    /// <summary>A FIXED voucher, active and inside its default validity window unless overridden.</summary>
    internal static VoucherRequest Fixed(
        long amount,
        long minSubtotal = 0,
        bool active = true,
        DateOnly? validFrom = null,
        DateOnly? validTo = null) =>
        new(VoucherType.Fixed, amount, amount, minSubtotal, active,
            validFrom ?? DefaultValidFrom, validTo ?? DefaultValidTo);

    /// <summary>An explicit clock time on <see cref="QuietAfternoon"/>'s date.</summary>
    internal static DateTime At(int hour, int minute) =>
        new(2026, 10, 20, hour, minute, 0, DateTimeKind.Unspecified);
}
