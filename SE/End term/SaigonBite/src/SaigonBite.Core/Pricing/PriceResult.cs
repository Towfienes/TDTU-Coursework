namespace SaigonBite.Core.Pricing;

/// <summary>
/// The itemised breakdown required by BR10 and displayed by FR-D11 before payment.
/// All money is whole VND; the only rounding in the whole calculation is applied to
/// <see cref="Total"/> (BR11).
/// </summary>
public sealed record PriceResult
{
    /// <summary>Step 1 — item subtotal S = Σ unit price × quantity (BR10).</summary>
    public required long Subtotal { get; init; }

    /// <summary>Step 2 — Quiet Kitchen discount Q, 10 % of S when hub load is below 30 % (BR7).</summary>
    public required long QuietKitchenDiscount { get; init; }

    /// <summary>Step 3 — voucher discount V, at most one voucher (BR9).</summary>
    public required long VoucherDiscount { get; init; }

    /// <summary>Step 4 — food total F = S − Q − V (BR10).</summary>
    public required long FoodTotal { get; init; }

    /// <summary>Step 5 — delivery fee D by distance tier, zeroed by the BR6 waiver (BR3, BR6).</summary>
    public required long DeliveryFee { get; init; }

    /// <summary>Step 6 — rush-hour surcharge R = 20 % of D, zero when D is waived (BR4, BR6).</summary>
    public required long RushSurcharge { get; init; }

    /// <summary>Step 7 — flat heavy-rain surcharge R2 = 10,000 (BR5). Survives the BR6 waiver.</summary>
    public required long RainSurcharge { get; init; }

    /// <summary>Step 9 — raw total F + D + R + R2 rounded once to the nearest 1,000, half up (BR11).</summary>
    public required long Total { get; init; }

    /// <summary>
    /// Every applicable rejection in the contract order BR1, BR2, BR8, BR12 (empty when accepted).
    /// </summary>
    /// <remarks>
    /// The money fields are still populated for a rejected order so the checkout screen can show the
    /// customer what they built and what is missing. They are informational only: the order may be
    /// charged and placed only when <see cref="IsAccepted"/> is true.
    /// </remarks>
    public required IReadOnlyList<PriceRejection> Rejections { get; init; }

    /// <summary>True when no rule rejected the order, i.e. the breakdown may be charged.</summary>
    public bool IsAccepted => Rejections.Count == 0;
}
