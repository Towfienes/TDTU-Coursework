using SaigonBite.Core.Payments;

namespace SaigonBite.Core.Pricing;

/// <summary>
/// Why an order cannot be priced as submitted (BR1, BR2, BR8, BR12).
/// </summary>
/// <param name="Code">
/// One of <c>BR1</c>, <c>BR2</c>, <c>BR8</c>, <c>BR12</c> — the rule identifier from the specification,
/// so the web layer can localise the message against the right <c>.resx</c> key (FR-S1).
/// </param>
/// <param name="Message">Human-readable English explanation, including the offending value.</param>
/// <remarks>
/// BR9 (voucher refused) deliberately produces no rejection: the specification says the <em>voucher</em>
/// is refused, not the order, so an unusable voucher simply yields <c>V = 0</c> and the order proceeds.
/// </remarks>
public sealed record PriceRejection(string Code, string Message)
{
    /// <summary>BR1 — item subtotal below 50,000 VND.</summary>
    public const string MinimumOrder = "BR1";

    /// <summary>BR2 — delivery distance above 8.0 km.</summary>
    public const string Coverage = "BR2";

    /// <summary>BR8 — hub at 90 % load or above refuses new orders.</summary>
    public const string HubProtection = "BR8";

    /// <summary>BR12 — line count or line quantity outside its limit.</summary>
    public const string OrderLines = "BR12";
}
