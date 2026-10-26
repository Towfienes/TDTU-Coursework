namespace SaigonBite.Core.Payments;

/// <summary>
/// Voucher kinds of BR9, mirroring the <c>Voucher.Type</c> column of the E section entity list.
/// </summary>
/// <remarks>
/// The enum lives in the payments module with the rest of the money vocabulary, but only the pricing
/// engine interprets it — see <see cref="Pricing.PricingEngine.VoucherDiscount"/>.
/// </remarks>
public enum VoucherType
{
    /// <summary>Percentage off the discounted food amount S − Q, capped at <c>MaxDiscount</c>.</summary>
    Percent = 0,

    /// <summary>Flat amount off, never more than S − Q.</summary>
    Fixed = 1,
}
