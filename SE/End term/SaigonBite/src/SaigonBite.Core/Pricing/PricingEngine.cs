using System.Globalization;
using SaigonBite.Core.Payments;

namespace SaigonBite.Core.Pricing;

/// <summary>
/// The single, pure implementation of the SaigonBite price calculation (BR1–BR12, FR-D2…FR-D11).
/// </summary>
/// <remarks>
/// <para>
/// Purity is a hard project rule (AGENTS.md rule 2) and a testable property (NFR6):
/// </para>
/// <list type="bullet">
///   <item><description>No I/O, no database, no <see cref="HttpClient"/>, no logging.</description></item>
///   <item><description>
///     No clock access. <see cref="DateTime.Now"/>, <see cref="DateTime.Today"/>,
///     <see cref="DateTime.UtcNow"/> and <see cref="DateTimeOffset.Now"/> are never read; the
///     placement time, the hub load and the rain flag all arrive inside <see cref="PriceContext"/>
///     as the order's stored snapshot (BR17).
///   </description></item>
///   <item><description>
///     No mutable static state: every field below is a <c>const</c>, so identical inputs always
///     produce an identical <see cref="PriceResult"/>.
///   </description></item>
/// </list>
/// <para>
/// The nine steps of BR10 are executed in order and the raw total is rounded exactly once, in step 9
/// (BR11). Steps 1–8 therefore work in whole or fractional VND and never round.
/// </para>
/// </remarks>
public static class PricingEngine
{
    /// <summary>BR1 — minimum item subtotal S, inclusive (boundary 49,999 / 50,000).</summary>
    public const long MinimumSubtotal = 50_000;

    /// <summary>BR2 — maximum delivery distance in km, inclusive (boundary 8.0 / 8.01).</summary>
    public const decimal MaximumDistanceKm = 8.0m;

    /// <summary>BR3 — flat fee for the first 2.0 km.</summary>
    public const long BaseFee = 15_000;

    /// <summary>BR3 — fee per whole km above 2.0 km, up to 5.0 km.</summary>
    public const long FeePerKmAbove2 = 5_000;

    /// <summary>BR3 — fee already accrued at exactly 5.0 km (15,000 + 5,000 × 3).</summary>
    public const long FeeAt5Km = 30_000;

    /// <summary>BR3 — fee per whole km above 5.0 km, up to 8.0 km.</summary>
    public const long FeePerKmAbove5 = 7_000;

    /// <summary>BR7/BR9 — the Quiet Kitchen discount is 10 % of S.</summary>
    public const int QuietKitchenPercent = 10;

    /// <summary>BR7/BR8 — the Quiet Kitchen load threshold, in percent: strictly below it earns the discount.</summary>
    public const int QuietKitchenLoadThresholdPercent = 30;

    /// <summary>BR8 — at this load or above the hub refuses new orders.</summary>
    public const int HubRejectionLoadPercent = 90;

    /// <summary>BR5 — flat heavy-rain surcharge.</summary>
    public const long RainSurchargeAmount = 10_000;

    /// <summary>BR6 — subtotal at or above which delivery and rush surcharges are waived.</summary>
    public const long FreeDeliverySubtotal = 300_000;

    /// <summary>BR4 — rush-hour multiplier applied to D, as a percentage.</summary>
    public const int RushSurchargePercent = 20;

    /// <summary>BR4 — first rush window opens at 11:00 (inclusive).</summary>
    public static readonly TimeOnly RushWindowMorningStart = new(11, 0);

    /// <summary>BR4 — first rush window closes at 13:00 (exclusive).</summary>
    public static readonly TimeOnly RushWindowMorningEnd = new(13, 0);

    /// <summary>BR4 — second rush window opens at 17:30 (inclusive).</summary>
    public static readonly TimeOnly RushWindowEveningStart = new(17, 30);

    /// <summary>BR4 — second rush window closes at 19:30 (exclusive).</summary>
    public static readonly TimeOnly RushWindowEveningEnd = new(19, 30);

    /// <summary>BR12 — minimum quantity per line.</summary>
    public const int MinimumLineQuantity = 1;

    /// <summary>BR12 — maximum quantity per line.</summary>
    public const int MaximumLineQuantity = 20;

    /// <summary>BR12 — maximum number of lines per order.</summary>
    public const int MaximumLineCount = 30;

    /// <summary>BR11 — the granularity the final total is rounded to.</summary>
    public const long RoundingGranularity = 1_000;

    /// <summary>
    /// Prices one order against its snapshot and returns every line of the BR10 breakdown.
    /// </summary>
    /// <param name="context">The complete snapshot; the engine reads nothing else.</param>
    /// <returns>
    /// The breakdown, plus every applicable rejection in the contract order BR1, BR2, BR8, BR12.
    /// Money fields are populated even when rejected, for display only (see <see cref="PriceResult.Rejections"/>).
    /// </returns>
    /// <exception cref="ArgumentNullException"><paramref name="context"/> is null.</exception>
    public static PriceResult Calculate(PriceContext context)
    {
        ArgumentNullException.ThrowIfNull(context);

        var lines = context.Lines;
        var rejections = new List<PriceRejection>(capacity: 4);

        // Step 1 (BR10): S = Σ price × quantity, before any discount.
        var subtotal = SumLines(lines);

        // Rejections are collected first so the caller always sees all of them, in contract order.
        CollectRejections(context, lines, subtotal, rejections);

        // Step 2 (BR10, BR7): Q = 10 % of S while the hub is below 30 % load.
        var quietKitchenDiscount = QuietKitchenDiscount(subtotal, context.HubLoadPercent);

        // Step 3 (BR10, BR9): V from at most one voucher, measured against the discounted food amount.
        var voucherDiscount = VoucherDiscount(context.Voucher, subtotal, quietKitchenDiscount, context.PlacementTime);

        // Step 4 (BR10): F = S − Q − V.
        var foodTotal = subtotal - quietKitchenDiscount - voucherDiscount;

        // Step 5 (BR10, BR3, BR6): D by distance tier, waived at S ≥ 300,000.
        var deliveryFee = subtotal >= FreeDeliverySubtotal ? 0 : DistanceFee(context.DistanceKm);

        // Step 6 (BR10, BR4, BR6): R = 20 % of D, and only when D was not waived.
        var rushSurcharge = RushSurcharge(context.PlacementTime, deliveryFee);

        // Step 7 (BR10, BR5): R2 = 10,000 flat while the rain flag is on; BR6 does not waive it.
        var rainSurcharge = context.RainFlagOn ? RainSurchargeAmount : 0;

        // Step 8 (BR10): raw total.
        var rawTotal = foodTotal + deliveryFee + rushSurcharge + rainSurcharge;

        // Step 9 (BR10, BR11): the one and only rounding, half up.
        var total = RoundToNearestThousand(rawTotal);

        return new PriceResult
        {
            Subtotal = subtotal,
            QuietKitchenDiscount = quietKitchenDiscount,
            VoucherDiscount = voucherDiscount,
            FoodTotal = foodTotal,
            DeliveryFee = deliveryFee,
            RushSurcharge = rushSurcharge,
            RainSurcharge = rainSurcharge,
            Total = total,

            // The shared empty array keeps accepted results value-equal to each other under record
            // equality, which is what the determinism test asserts (NFR6).
            Rejections = rejections.Count == 0 ? Array.Empty<PriceRejection>() : rejections,
        };
    }

    /// <summary>
    /// BR3 — delivery fee for a distance already inside the BR2 coverage limit.
    /// </summary>
    /// <param name="distanceKm">Distance from hub to delivery address.</param>
    /// <remarks>
    /// <para>The specification's tier table, implemented literally:</para>
    /// <list type="bullet">
    ///   <item><description>up to and including 2.0 km → 15,000;</description></item>
    ///   <item><description>
    ///     over 2.0 km up to and including 5.0 km → 15,000 + 5,000 × ⌈d − 2⌉;
    ///   </description></item>
    ///   <item><description>
    ///     over 5.0 km up to 8.0 km → 30,000 + 7,000 × ⌈d − 5⌉.
    ///   </description></item>
    /// </list>
    /// <para>
    /// The tier change at 5.0 km is discontinuous — 5.0 km costs 30,000 and 5.01 km costs 37,000
    /// because the third tier restarts from a 30,000 base plus one whole 7,000-km step. That is the
    /// specification's own arithmetic, recorded as ambiguity A4; it is implemented as written and
    /// pinned by boundary tests rather than "smoothed".
    /// </para>
    /// <para>
    /// Callers should supply a distance with at most two decimals. The engine does not pre-round it:
    /// rounding the input would silently change which kilometre step BR3 charges for.
    /// </para>
    /// </remarks>
    public static long DistanceFee(decimal distanceKm)
    {
        if (distanceKm <= 2.0m)
        {
            return BaseFee;
        }

        if (distanceKm <= 5.0m)
        {
            return BaseFee + (FeePerKmAbove2 * ExtraWholeKilometres(distanceKm - 2.0m));
        }

        return FeeAt5Km + (FeePerKmAbove5 * ExtraWholeKilometres(distanceKm - 5.0m));
    }

    /// <summary>BR4 — true when the placement time falls in a rush window, start inclusive, end exclusive.</summary>
    public static bool IsRushHour(DateTime placementTime)
    {
        var timeOfDay = TimeOnly.FromDateTime(placementTime);

        return (timeOfDay >= RushWindowMorningStart && timeOfDay < RushWindowMorningEnd)
            || (timeOfDay >= RushWindowEveningStart && timeOfDay < RushWindowEveningEnd);
    }

    /// <summary>
    /// BR4 — rush surcharge R = 20 % of D, or 0 outside a rush window and 0 when D was waived by BR6.
    /// </summary>
    public static long RushSurcharge(DateTime placementTime, long deliveryFee)
    {
        if (deliveryFee <= 0 || !IsRushHour(placementTime))
        {
            return 0;
        }

        // Integer division is exact for every fee BR3 can produce (each is a multiple of 1,000,
        // and 1,000 × 20 / 100 = 200), so no rounding happens before step 9 (BR11).
        return deliveryFee * RushSurchargePercent / 100;
    }

    /// <summary>
    /// BR7 — Quiet Kitchen discount Q = 10 % of S when the snapshot load is below 30 %, else 0.
    /// </summary>
    /// <param name="subtotal">Item subtotal S.</param>
    /// <param name="hubLoadPercent">Hub load at placement, 0..100.</param>
    /// <remarks>
    /// A non-integral 10 % is truncated toward zero, never rounded up: the platform never credits more
    /// than the 10 % the rule promises, and the shortfall is below one đồng.
    /// </remarks>
    public static long QuietKitchenDiscount(long subtotal, int hubLoadPercent)
    {
        if (hubLoadPercent >= QuietKitchenLoadThresholdPercent || subtotal <= 0)
        {
            return 0;
        }

        return subtotal * QuietKitchenPercent / 100;
    }

    /// <summary>
    /// BR9 — voucher discount V, or 0 when the voucher may not be used for this order.
    /// </summary>
    /// <param name="voucher">The single voucher the customer chose, or null.</param>
    /// <param name="subtotal">Item subtotal S, against which the minimum-subtotal condition is checked.</param>
    /// <param name="quietKitchenDiscount">Q already granted; PERCENT vouchers apply to S − Q.</param>
    /// <param name="placementTime">Placement timestamp in Vietnam local time, used for the validity check.</param>
    /// <remarks>
    /// <para>A voucher is refused — yielding V = 0 and leaving the order placeable — when it is inactive,
    /// when the placement date falls outside its validity dates (both ends inclusive), or when S is below
    /// its minimum subtotal. BR9 restricts refusal to the <em>voucher</em>, not the order, so this method
    /// adds no <see cref="PriceRejection"/>; the checkout screen shows V = 0 instead.</para>
    /// <para>PERCENT: V = p % of (S − Q), capped at the voucher's maximum discount.
    /// FIXED: V = the voucher amount, but never more than S − Q.</para>
    /// </remarks>
    public static long VoucherDiscount(VoucherRequest? voucher, long subtotal, long quietKitchenDiscount, DateTime placementTime)
    {
        if (voucher is null || !voucher.IsActive)
        {
            return 0;
        }

        if (subtotal < voucher.MinSubtotal)
        {
            return 0;
        }

        var placementDate = DateOnly.FromDateTime(placementTime);

        if (placementDate < voucher.ValidFrom || placementDate > voucher.ValidTo)
        {
            return 0;
        }

        var discountedFoodAmount = subtotal - quietKitchenDiscount;

        if (discountedFoodAmount <= 0)
        {
            return 0;
        }

        return voucher.Type switch
        {
            // Truncated toward zero for the same reason as the Quiet Kitchen discount.
            VoucherType.Percent => Math.Min(
                discountedFoodAmount * voucher.Value / 100,
                voucher.MaxDiscount),

            VoucherType.Fixed => Math.Min(voucher.Value, discountedFoodAmount),

            _ => 0,
        };
    }

    /// <summary>
    /// BR11 — round a raw total once, to the nearest 1,000, with halves rounding up.
    /// </summary>
    /// <param name="rawTotal">The step-8 total in whole VND.</param>
    /// <remarks>
    /// 64,950 → 65,000 and 64,500 → 65,000 (the half rounds up); 64,499 → 64,000.
    /// </remarks>
    public static long RoundToNearestThousand(long rawTotal)
    {
        var thousands = (decimal)rawTotal / RoundingGranularity;

        return (long)(Math.Round(thousands, 0, MidpointRounding.AwayFromZero) * RoundingGranularity);
    }

    /// <summary>BR3 — a partial kilometre counts as a whole one, so ⌈x⌉ with x &gt; 0.</summary>
    private static long ExtraWholeKilometres(decimal partialKm) => (long)Math.Ceiling(partialKm);

    /// <summary>Step 1 of BR10, in <see cref="long"/> VND.</summary>
    private static long SumLines(IReadOnlyList<PriceLineRequest>? lines)
    {
        if (lines is null)
        {
            return 0;
        }

        var subtotal = 0L;

        foreach (var line in lines)
        {
            subtotal += line.UnitPrice * line.Quantity;
        }

        return subtotal;
    }

    /// <summary>
    /// Appends every applicable rejection in the contract order: BR1, BR2, BR8, BR12.
    /// </summary>
    private static void CollectRejections(
        PriceContext context,
        IReadOnlyList<PriceLineRequest>? lines,
        long subtotal,
        List<PriceRejection> rejections)
    {
        // BR1 — minimum order, checked against S before any discount.
        if (subtotal < MinimumSubtotal)
        {
            rejections.Add(new PriceRejection(
                PriceRejection.MinimumOrder,
                string.Format(
                    CultureInfo.InvariantCulture,
                    "BR1: the item subtotal {0} VND is below the {1} VND minimum order.",
                    subtotal.ToString("N0", CultureInfo.InvariantCulture),
                    MinimumSubtotal.ToString("N0", CultureInfo.InvariantCulture))));
        }

        // BR2 — coverage.
        if (context.DistanceKm > MaximumDistanceKm)
        {
            rejections.Add(new PriceRejection(
                PriceRejection.Coverage,
                string.Format(
                    CultureInfo.InvariantCulture,
                    "BR2: the delivery distance {0} km exceeds the {1} km coverage limit. Please choose another address or hub.",
                    context.DistanceKm.ToString("0.##", CultureInfo.InvariantCulture),
                    MaximumDistanceKm.ToString("0.0", CultureInfo.InvariantCulture))));
        }

        // BR8 — hub protection. The flag and the percentage are two views of one snapshot fact;
        // either one may be used to reject, so a partially filled context cannot bypass the rule.
        if (context.HubRejectsNewOrders || context.HubLoadPercent >= HubRejectionLoadPercent)
        {
            rejections.Add(new PriceRejection(
                PriceRejection.HubProtection,
                string.Format(
                    CultureInfo.InvariantCulture,
                    "BR8: the chosen hub is at {0}% load and refuses new orders at {1}% or above. Please choose another hub.",
                    context.HubLoadPercent,
                    HubRejectionLoadPercent)));
        }

        // BR12 — line limits. One rejection carries every problem found, so the code appears once.
        var lineProblems = DescribeLineProblems(lines);

        if (lineProblems is not null)
        {
            rejections.Add(new PriceRejection(PriceRejection.OrderLines, "BR12: " + lineProblems));
        }
    }

    /// <summary>
    /// BR12 — returns a description of every line-limit violation, or null when the order is legal.
    /// </summary>
    private static string? DescribeLineProblems(IReadOnlyList<PriceLineRequest>? lines)
    {
        if (lines is null || lines.Count == 0)
        {
            return string.Format(
                CultureInfo.InvariantCulture,
                "an order needs at least {0} line, but none was supplied.",
                MinimumLineQuantity);
        }

        if (lines.Count > MaximumLineCount)
        {
            return string.Format(
                CultureInfo.InvariantCulture,
                "the order has {0} lines and at most {1} are allowed.",
                lines.Count,
                MaximumLineCount);
        }

        for (var index = 0; index < lines.Count; index++)
        {
            var quantity = lines[index].Quantity;

            if (quantity < MinimumLineQuantity || quantity > MaximumLineQuantity)
            {
                return string.Format(
                    CultureInfo.InvariantCulture,
                    "line {0} (menu item {1}) has quantity {2}; each line must be between {3} and {4}.",
                    index + 1,
                    lines[index].MenuItemId,
                    quantity,
                    MinimumLineQuantity,
                    MaximumLineQuantity);
            }
        }

        return null;
    }
}
