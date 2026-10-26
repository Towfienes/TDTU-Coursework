using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;

namespace SaigonBite.Web.Data.Entities;

/// <summary>
/// A placed order with the full BR10 breakdown and the BR17 price snapshot.
/// </summary>
/// <remarks>
/// Orders are never deleted and never soft-deleted (CONTRACT.md): every financial and reporting figure
/// is derived from these rows, so a delete would falsify R1 and R2. The recorded money fields are the
/// output of <c>PricingEngine.Calculate</c> at placement; the web layer stores them, it never computes
/// them.
/// </remarks>
public class Order
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Customer who placed the order.</summary>
    public int CustomerId { get; set; }

    /// <summary>Navigation for <see cref="CustomerId"/>.</summary>
    public User? Customer { get; set; }

    /// <summary>Hub the order was placed at; one order belongs to exactly one hub (FR-D1).</summary>
    public int HubId { get; set; }

    /// <summary>Navigation for <see cref="HubId"/>.</summary>
    public Hub? Hub { get; set; }

    /// <summary>Current state of the BR15 machine.</summary>
    public OrderStatus Status { get; set; } = OrderStatus.Placed;

    /// <summary>BR17 snapshot, part 1: Vietnam local placement timestamp, also read by BR4.</summary>
    public DateTime PlacedAt { get; set; }

    /// <summary>Simulated delivery distance in km; BR2 rejects above 8.0 and BR3 prices it.</summary>
    public decimal DistanceKm { get; set; }

    /// <summary>BR17 snapshot, part 2: hub load percentage at placement, excluding this order (BR8).</summary>
    public int HubLoadPercent { get; set; }

    /// <summary>BR17 snapshot, part 3: heavy-rain flag at placement (BR5).</summary>
    public bool RainFlag { get; set; }

    /// <summary>BR10 step 1 — item subtotal S.</summary>
    public long Subtotal { get; set; }

    /// <summary>BR10 step 2 — Quiet Kitchen discount Q (BR7).</summary>
    public long QuietKitchenDiscount { get; set; }

    /// <summary>BR10 step 3 — voucher discount V (BR9).</summary>
    public long VoucherDiscount { get; set; }

    /// <summary>BR10 step 4 — food total F = S − Q − V.</summary>
    public long FoodTotal { get; set; }

    /// <summary>BR10 step 5 — delivery fee D (BR3, BR6).</summary>
    public long DeliveryFee { get; set; }

    /// <summary>BR10 step 6 — rush surcharge R (BR4, BR6).</summary>
    public long RushSurcharge { get; set; }

    /// <summary>BR10 step 7 — rain surcharge R2 (BR5).</summary>
    public long RainSurcharge { get; set; }

    /// <summary>BR10 step 9 / BR11 — rounded total, the amount charged and counted by R1.</summary>
    public long Total { get; set; }

    /// <summary>Voucher applied at placement, if any; kept for replay and reporting (FR-C3).</summary>
    public int? VoucherId { get; set; }

    /// <summary>Navigation for <see cref="VoucherId"/>.</summary>
    public Voucher? Voucher { get; set; }

    /// <summary>Code text at placement, kept even if the voucher row is renamed or deactivated (FR-A4).</summary>
    public string? VoucherCode { get; set; }

    /// <summary>Manual shipper assignment (Ambiguity A1, FR-F1).</summary>
    public int? AssignedShipperId { get; set; }

    /// <summary>Navigation for <see cref="AssignedShipperId"/>.</summary>
    public User? AssignedShipper { get; set; }

    /// <summary>When the shipper was assigned (Ambiguity A1).</summary>
    public DateTime? AssignedAt { get; set; }

    /// <summary>Payment method chosen at checkout (BR13); null while unpaid.</summary>
    public PaymentMethod? PaymentMethod { get; set; }

    /// <summary>BR14: a COD order may only become Delivered after the shipper confirms the cash.</summary>
    public bool IsCashConfirmed { get; set; }

    /// <summary>Tourist delivery address, part 1 (User Story 2): hotel name shown to the shipper.</summary>
    public string? HotelName { get; set; }

    /// <summary>Tourist delivery address, part 2: room number shown to the shipper.</summary>
    public string? RoomNumber { get; set; }

    /// <summary>Optional customer note for the kitchen.</summary>
    public string? Notes { get; set; }

    /// <summary>Set when the order reaches Delivered, used for delivery reporting.</summary>
    public DateTime? DeliveredAt { get; set; }

    /// <summary>Priced lines (1..30 per BR12).</summary>
    public ICollection<OrderLine> Lines { get; set; } = new List<OrderLine>();

    /// <summary>Audit trail of every accepted and rejected transition (FR-S5, NFR5).</summary>
    public ICollection<OrderStatusHistory> History { get; set; } = new List<OrderStatusHistory>();

    /// <summary>Payment attempts, successful or not (FR-P3, NFR5).</summary>
    public ICollection<PaymentRecord> Payments { get; set; } = new List<PaymentRecord>();
}

/// <summary>
/// One priced line. Name, price, brand and category are copied at placement so the historical order
/// keeps rendering correctly after the menu item is edited or soft-deleted (FR-A4, BR12).
/// </summary>
public class OrderLine
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Owning order.</summary>
    public int OrderId { get; set; }

    /// <summary>Navigation for <see cref="OrderId"/>.</summary>
    public Order? Order { get; set; }

    /// <summary>Menu item the line came from; kept as a reference, never deleted (BR12).</summary>
    public int MenuItemId { get; set; }

    /// <summary>Item name at placement.</summary>
    public string ItemName { get; set; } = string.Empty;

    /// <summary>Unit price at placement, in whole VND.</summary>
    public long UnitPrice { get; set; }

    /// <summary>Quantity, 1..20 per line (BR12).</summary>
    public int Quantity { get; set; }

    /// <summary>Brand name at placement — R1 groups revenue by brand category (FR-R1).</summary>
    public string BrandName { get; set; } = string.Empty;

    /// <summary>Category at placement — R1 groups revenue by category (FR-R1).</summary>
    public string CategoryName { get; set; } = string.Empty;

    /// <summary>
    /// True when an edit removed the line (FR-D12, BR17). Order lines are never deleted
    /// (CONTRACT.md), so an edit flags the row instead and the priced lines are the ones with
    /// <c>IsRemoved == false</c>. This keeps the original placement visible for audit.
    /// </summary>
    public bool IsRemoved { get; set; }

    /// <summary>Line subtotal as stored (unit price × quantity).</summary>
    public long LineTotal => UnitPrice * Quantity;
}

/// <summary>
/// One row per attempted status change, accepted or rejected (FR-S5, NFR5, BR15).
/// </summary>
public class OrderStatusHistory
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Order the attempt belongs to.</summary>
    public int OrderId { get; set; }

    /// <summary>Navigation for <see cref="OrderId"/>.</summary>
    public Order? Order { get; set; }

    /// <summary>State before the attempt.</summary>
    public OrderStatus FromStatus { get; set; }

    /// <summary>State the actor attempted.</summary>
    public OrderStatus ToStatus { get; set; }

    /// <summary>Actor role that attempted the change.</summary>
    public ActorRole ActorRole { get; set; }

    /// <summary>Actor identity, null for system-generated rows.</summary>
    public int? ActorId { get; set; }

    /// <summary>Reason text: supplied by staff for BR16 cancellations, or the rejection message.</summary>
    public string? Reason { get; set; }

    /// <summary>Vietnam local timestamp of the attempt.</summary>
    public DateTime OccurredAt { get; set; }

    /// <summary>
    /// True when the transition was applied, false when the business layer rejected it. Rejected
    /// attempts must be auditable too (FR-S5), and the state did not change, so the flag is what
    /// separates "refused" from "applied".
    /// </summary>
    public bool Applied { get; set; }
}

/// <summary>
/// One payment attempt against a gateway strategy (FR-P3, NFR5, Ambiguity A2 refunds).
/// </summary>
/// <remarks>
/// A refund is recorded as a negative-amount row with the same strategy key, so the simulated ledger
/// stays append-only: nothing is edited or deleted when an online order is cancelled or fails.
/// </remarks>
public class PaymentRecord
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Order the attempt belongs to.</summary>
    public int OrderId { get; set; }

    /// <summary>Navigation for <see cref="OrderId"/>.</summary>
    public Order? Order { get; set; }

    /// <summary>Stable key of the strategy that handled the attempt (CONTRACT.md).</summary>
    public string StrategyKey { get; set; } = string.Empty;

    /// <summary>Amount in whole VND; negative for a refund.</summary>
    public long Amount { get; set; }

    /// <summary>Gateway reference returned by the strategy; null on failure.</summary>
    public string? GatewayReference { get; set; }

    /// <summary>Whether the gateway call succeeded.</summary>
    public bool Success { get; set; }

    /// <summary>Vietnam local timestamp of the attempt.</summary>
    public DateTime CreatedAt { get; set; }
}

/// <summary>
/// Platform-wide settings that are not tied to a user, currently the heavy-rain flag of BR5/FR-S4.
/// </summary>
public class PlatformSetting
{
    /// <summary>Setting key, for example <c>RainFlag</c>.</summary>
    public string Key { get; set; } = string.Empty;

    /// <summary>Stored value; booleans are stored as <c>true</c>/<c>false</c>.</summary>
    public string Value { get; set; } = string.Empty;
}
