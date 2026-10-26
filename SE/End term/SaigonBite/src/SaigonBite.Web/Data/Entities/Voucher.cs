using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;

namespace SaigonBite.Web.Data.Entities;

/// <summary>
/// A discount code (FR-C1, BR9). At most one voucher may be applied to an order (FR-C3).
/// </summary>
/// <remarks>
/// The row is never deleted: FR-C2 exposes "deactivate", expressed by <see cref="IsActive"/>. That flag
/// is the soft-delete equivalent for vouchers, and it is the value snapshotted into the BR17 context of
/// an order so a later recalculation cannot resurrect an expired code.
/// </remarks>
public class Voucher
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Code the customer types, unique and case-insensitive (FR-C1).</summary>
    public string Code { get; set; } = string.Empty;

    /// <summary>PERCENT or FIXED (BR9).</summary>
    public VoucherType Type { get; set; }

    /// <summary>Percentage points for PERCENT, whole VND for FIXED.</summary>
    public long Value { get; set; }

    /// <summary>Maximum discount in VND for a PERCENT voucher; ignored for FIXED (BR9).</summary>
    public long MaxDiscount { get; set; }

    /// <summary>Minimum item subtotal S required, checked against S and not against the food total (BR9).</summary>
    public long MinSubtotal { get; set; }

    /// <summary>First usable day, inclusive.</summary>
    public DateOnly ValidFrom { get; set; }

    /// <summary>Last usable day, inclusive.</summary>
    public DateOnly ValidTo { get; set; }

    /// <summary>Active flag; deactivating keeps the row for history (FR-C2, BR9).</summary>
    public bool IsActive { get; set; } = true;
}
