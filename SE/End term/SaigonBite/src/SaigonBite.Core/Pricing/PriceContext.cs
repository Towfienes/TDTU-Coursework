using SaigonBite.Core.Payments;

namespace SaigonBite.Core.Pricing;

/// <summary>
/// The complete, immutable snapshot the pricing engine is allowed to read (BR1–BR12, BR17).
/// </summary>
/// <remarks>
/// <para>
/// BR17 requires that a later recalculation of an editable order reuses the snapshot taken at
/// placement (timestamp, hub load, rain flag) instead of current conditions. That is expressed here:
/// the engine never reads the clock, the database or a global rain flag — every input arrives in this
/// context, so replaying a stored snapshot reproduces the stored price exactly (FR-D14, NFR6).
/// </para>
/// </remarks>
public sealed record PriceContext
{
    /// <summary>Order lines. BR12 restricts the count to 1..30.</summary>
    public required IReadOnlyList<PriceLineRequest> Lines { get; init; }

    /// <summary>Hub-to-address distance in km; BR2 rejects anything above 8.0, BR3 turns it into the fee.</summary>
    public required decimal DistanceKm { get; init; }

    /// <summary>Placement timestamp in Vietnam local time (UTC+7). BR4 and the BR9 validity check read it.</summary>
    public required DateTime PlacementTime { get; init; }

    /// <summary>Heavy-rain flag as snapshotted at placement (BR5, FR-S4).</summary>
    public required bool RainFlagOn { get; init; }

    /// <summary>
    /// Hub load percentage as snapshotted at placement, 0..100, excluding the new order (BR8).
    /// BR7 discounts when this is below 30.
    /// </summary>
    public required int HubLoadPercent { get; init; }

    /// <summary>
    /// True when the hub refuses new orders because its load is 90 % or above (BR8).
    /// </summary>
    /// <remarks>
    /// This flag and <see cref="HubLoadPercent"/> are two views of the same snapshot fact. The engine
    /// rejects when either says "overloaded", so a caller that only fills one of them still gets the
    /// BR8 protection instead of silently selling into a saturated kitchen.
    /// </remarks>
    public bool HubRejectsNewOrders { get; init; }

    /// <summary>At most one voucher per order (BR9). Null means no voucher was chosen.</summary>
    public VoucherRequest? Voucher { get; init; }
}
