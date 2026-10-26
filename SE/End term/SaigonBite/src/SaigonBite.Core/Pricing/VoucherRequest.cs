using SaigonBite.Core.Payments;

namespace SaigonBite.Core.Pricing;

/// <summary>
/// A voucher as snapshotted at placement, mirroring the <c>Voucher</c> entity (BR9, FR-C1).
/// </summary>
/// <param name="Type">PERCENT or FIXED.</param>
/// <param name="Value">Percentage points for <see cref="VoucherType.Percent"/>, or whole VND for <see cref="VoucherType.Fixed"/>.</param>
/// <param name="MaxDiscount">Cap in whole VND. Ignored for <see cref="VoucherType.Fixed"/>, which is already a cap.</param>
/// <param name="MinSubtotal">Minimum item subtotal S required to use the voucher, checked against S and not against the food total.</param>
/// <param name="IsActive">Administrator's active flag (FR-C2).</param>
/// <param name="ValidFrom">First day the voucher may be used, inclusive.</param>
/// <param name="ValidTo">Last day the voucher may be used, inclusive.</param>
public sealed record VoucherRequest(
    VoucherType Type,
    long Value,
    long MaxDiscount,
    long MinSubtotal,
    bool IsActive,
    DateOnly ValidFrom,
    DateOnly ValidTo);
