using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Core.Pricing;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Services;

namespace SaigonBite.Web.ViewModels;

/// <summary>
/// The itemised BR10 breakdown every money screen renders (FR-D11). The panel never shows only a total.
/// </summary>
public sealed class BreakdownVm
{
    /// <summary>Step 1 — item subtotal S.</summary>
    public long Subtotal { get; init; }

    /// <summary>Step 2 — Quiet Kitchen discount Q (BR7).</summary>
    public long QuietKitchenDiscount { get; init; }

    /// <summary>Step 3 — voucher discount V (BR9).</summary>
    public long VoucherDiscount { get; init; }

    /// <summary>Step 4 — food total F.</summary>
    public long FoodTotal { get; init; }

    /// <summary>Step 5 — delivery fee D (BR3, BR6).</summary>
    public long DeliveryFee { get; init; }

    /// <summary>Step 6 — rush surcharge R (BR4).</summary>
    public long RushSurcharge { get; init; }

    /// <summary>Step 7 — rain surcharge R2 (BR5).</summary>
    public long RainSurcharge { get; init; }

    /// <summary>Step 9 — rounded total (BR11).</summary>
    public long Total { get; init; }

    /// <summary>BR17 snapshot: hub load at placement.</summary>
    public int HubLoadPercent { get; init; }

    /// <summary>BR17 snapshot: placement timestamp.</summary>
    public DateTime PlacedAt { get; init; }

    /// <summary>BR17 snapshot: heavy-rain flag.</summary>
    public bool RainFlag { get; init; }

    /// <summary>Voucher code applied, if any.</summary>
    public string? VoucherCode { get; init; }

    /// <summary>BR9 explanation when a submitted voucher was refused.</summary>
    public string? VoucherNotice { get; init; }

    /// <summary>Builds the panel from a stored order.</summary>
    public static BreakdownVm FromOrder(Order order) => new()
    {
        Subtotal = order.Subtotal,
        QuietKitchenDiscount = order.QuietKitchenDiscount,
        VoucherDiscount = order.VoucherDiscount,
        FoodTotal = order.FoodTotal,
        DeliveryFee = order.DeliveryFee,
        RushSurcharge = order.RushSurcharge,
        RainSurcharge = order.RainSurcharge,
        Total = order.Total,
        HubLoadPercent = order.HubLoadPercent,
        PlacedAt = order.PlacedAt,
        RainFlag = order.RainFlag,
        VoucherCode = order.VoucherCode,
    };

    /// <summary>Builds the panel from a live engine result (cart and checkout previews).</summary>
    public static BreakdownVm FromPrice(
        PriceResult price, int hubLoadPercent, DateTime placedAt, bool rainFlag,
        string? voucherCode, string? voucherNotice) => new()
    {
        Subtotal = price.Subtotal,
        QuietKitchenDiscount = price.QuietKitchenDiscount,
        VoucherDiscount = price.VoucherDiscount,
        FoodTotal = price.FoodTotal,
        DeliveryFee = price.DeliveryFee,
        RushSurcharge = price.RushSurcharge,
        RainSurcharge = price.RainSurcharge,
        Total = price.Total,
        HubLoadPercent = hubLoadPercent,
        PlacedAt = placedAt,
        RainFlag = rainFlag,
        VoucherCode = voucherCode,
        VoucherNotice = voucherNotice,
    };
}

/// <summary>The public menu of one hub, filtered by category (FR-A2).</summary>
public sealed class MenuPageVm
{
    /// <summary>Hub whose menu is shown, or null when no hub is selected.</summary>
    public Hub? Hub { get; init; }

    /// <summary>Every live hub, for the hub selector.</summary>
    public IReadOnlyList<Hub> Hubs { get; init; } = new List<Hub>();

    /// <summary>Current load percentage per hub (FR-B2).</summary>
    public IReadOnlyDictionary<int, int> Loads { get; init; } = new Dictionary<int, int>();

    /// <summary>Brands operated by the selected hub with their items.</summary>
    public IReadOnlyList<Brand> Brands { get; init; } = new List<Brand>();

    /// <summary>Menu items of the selected hub, already filtered.</summary>
    public IReadOnlyList<MenuItem> Items { get; init; } = new List<MenuItem>();

    /// <summary>Categories available in the current selection.</summary>
    public IReadOnlyList<string> Categories { get; init; } = new List<string>();

    /// <summary>Selected category filter.</summary>
    public string? Category { get; init; }
}

/// <summary>The basket screen: lines, live price and the BR12 error if any.</summary>
public sealed class CartPageVm
{
    /// <summary>Hub the basket is bound to.</summary>
    public Hub? Hub { get; init; }

    /// <summary>Resolved lines with their database prices.</summary>
    public IReadOnlyList<ResolvedLine> Lines { get; init; } = new List<ResolvedLine>();

    /// <summary>Live engine result, or null when the basket cannot be priced.</summary>
    public PriceComputation? Computation { get; init; }

    /// <summary>Validation or pricing error shown above the basket.</summary>
    public string? Error { get; init; }

    /// <summary>Rejection list with BR codes (FR-D2, FR-D3, BR8, BR12).</summary>
    public IReadOnlyList<PriceRejection> Rejections { get; init; } = new List<PriceRejection>();

    /// <summary>Simulated delivery distance used for the preview.</summary>
    public decimal DistanceKm { get; init; }

    /// <summary>The BR10 panel, when a price exists.</summary>
    public BreakdownVm? Breakdown { get; init; }
}

/// <summary>The checkout screen: breakdown before payment (FR-D11), BR13 methods and the FR-B5 offer.</summary>
public sealed class CheckoutPageVm
{
    /// <summary>Hub of the basket.</summary>
    public Hub? Hub { get; set; }

    /// <summary>Resolved lines.</summary>
    public IReadOnlyList<ResolvedLine> Lines { get; set; } = new List<ResolvedLine>();

    /// <summary>Engine result.</summary>
    public PriceComputation? Computation { get; set; }

    /// <summary>BR10 panel.</summary>
    public BreakdownVm? Breakdown { get; set; }

    /// <summary>Error from validation or a refused voucher.</summary>
    public string? Error { get; set; }

    /// <summary>Rejections returned by the engine (BR1, BR2, BR8, BR12).</summary>
    public IReadOnlyList<PriceRejection> Rejections { get; set; } = new List<PriceRejection>();

    /// <summary>Payment strategies available to this customer type (BR13).</summary>
    public IReadOnlyList<IPaymentStrategy> PaymentOptions { get; set; } = new List<IPaymentStrategy>();

    /// <summary>Selected method, echoed back on validation errors.</summary>
    public string? SelectedMethod { get; set; }

    /// <summary>Simulated distance in km.</summary>
    public decimal DistanceKm { get; set; } = 3.2m;

    /// <summary>Voucher code the customer typed.</summary>
    public string? VoucherCode { get; set; }

    /// <summary>Codes the customer may use, for the picker.</summary>
    public IReadOnlyList<string> VoucherCodes { get; set; } = new List<string>();

    /// <summary>Tourist hotel name (User Story 2).</summary>
    public string? HotelName { get; set; }

    /// <summary>Tourist room number.</summary>
    public string? RoomNumber { get; set; }

    /// <summary>Free-text note for the kitchen.</summary>
    public string? Notes { get; set; }

    /// <summary>Other hubs offered when this one is full (FR-B5, BR8).</summary>
    public IReadOnlyList<Hub> AlternativeHubs { get; set; } = new List<Hub>();

    /// <summary>Customer group, used to decide whether COD is offered (BR14).</summary>
    public CustomerType CustomerType { get; set; }

    /// <summary>True when the rounded total still allows Cash on Delivery (BR14).</summary>
    public bool CashAllowed => Computation is null
                               || PaymentPolicy.IsCashAllowed(Computation.Result.Total);
}

/// <summary>Order tracking screen with the lifecycle trail (FR-D11, FR-S5).</summary>
public sealed class OrderDetailsVm
{
    /// <summary>The order with its lines and history loaded.</summary>
    public required Order Order { get; init; }

    /// <summary>Lines that are still part of the order (edits flag rows instead of deleting them).</summary>
    public IReadOnlyList<OrderLine> Lines { get; init; } = new List<OrderLine>();

    /// <summary>Audit trail, oldest first.</summary>
    public IReadOnlyList<OrderStatusHistory> History { get; init; } = new List<OrderStatusHistory>();

    /// <summary>Payment attempts and simulated refunds.</summary>
    public IReadOnlyList<PaymentRecord> Payments { get; init; } = new List<PaymentRecord>();

    /// <summary>States the signed-in actor may move the order to (BR15, rendered as buttons).</summary>
    public IReadOnlyCollection<OrderStatus> AllowedNext { get; init; } = Array.Empty<OrderStatus>();

    /// <summary>BR10 panel built from the stored snapshot.</summary>
    public BreakdownVm? Breakdown { get; init; }

    /// <summary>True when this order can still be edited (Placed, BR17).</summary>
    public bool CanEdit { get; init; }

    /// <summary>True when the customer may cancel (Placed or Confirmed, BR16).</summary>
    public bool CanCancel { get; init; }

    /// <summary>True when the order has no successful positive payment yet (FR-P3 retry).</summary>
    public bool CanRetryPayment { get; init; }

    /// <summary>Payment methods offered on the retry form (BR13).</summary>
    public IReadOnlyList<IPaymentStrategy> PaymentOptions { get; init; } = new List<IPaymentStrategy>();
}

/// <summary>One row of the order list.</summary>
public sealed class OrderListVm
{
    /// <summary>Orders of the signed-in customer, newest first.</summary>
    public IReadOnlyList<Order> Orders { get; init; } = new List<Order>();
}

/// <summary>A hub row on the public and admin screens (FR-B2).</summary>
public sealed class HubRowVm
{
    /// <summary>The hub.</summary>
    public required Hub Hub { get; init; }

    /// <summary>Derived load percentage (BR8).</summary>
    public int LoadPercent { get; init; }

    /// <summary>Orders in Confirmed or Preparing, the numerator of the load.</summary>
    public int BusyOrders { get; init; }

    /// <summary>True when the hub currently refuses new orders (BR8).</summary>
    public bool IsFull => LoadPercent >= 90;
}

/// <summary>Home page data: hubs with their live load and the brand catalogue (FR-B2, FR-A2).</summary>
public sealed class HomePageVm
{
    /// <summary>Hubs with load.</summary>
    public IReadOnlyList<HubRowVm> Hubs { get; init; } = new List<HubRowVm>();

    /// <summary>Live brands.</summary>
    public IReadOnlyList<Brand> Brands { get; init; } = new List<Brand>();

    /// <summary>Current heavy-rain flag (BR5, FR-S4).</summary>
    public bool RainFlag { get; init; }
}

/// <summary>The role-aware delivery board (FR-F1, FR-F2).</summary>
public sealed class DeliveryBoardVm
{
    /// <summary>"Kitchen", "Shipper" or "Admin" — which view of the board to render.</summary>
    public string Mode { get; init; } = "Kitchen";

    /// <summary>Orders to show.</summary>
    public IReadOnlyList<Order> Orders { get; init; } = new List<Order>();

    /// <summary>Shippers available for assignment (admin only).</summary>
    public IReadOnlyList<User> Shippers { get; init; } = new List<User>();

    /// <summary>Home hub of a kitchen staff account, for the heading.</summary>
    public Hub? KitchenHub { get; init; }
}

/// <summary>The interactive administrator dashboard (FR-S3, R1, R2).</summary>
public sealed class DashboardVm
{
    /// <summary>R1 for the chosen range.</summary>
    public required RevenueReport Revenue { get; init; }

    /// <summary>R2 for the chosen range.</summary>
    public required HubUtilisationReport Utilisation { get; init; }

    /// <summary>Orders per status, for the tiles.</summary>
    public IReadOnlyDictionary<OrderStatus, int> StatusCounts { get; init; } =
        new Dictionary<OrderStatus, int>();

    /// <summary>Current heavy-rain flag (BR5).</summary>
    public bool RainFlag { get; init; }

    /// <summary>JSON for the Chart.js revenue-by-category chart.</summary>
    public string CategoryChartJson { get; init; } = "{}";

    /// <summary>JSON for the Chart.js revenue-by-payment-method chart.</summary>
    public string PaymentChartJson { get; init; } = "{}";

    /// <summary>JSON for the Chart.js hub-load chart.</summary>
    public string LoadChartJson { get; init; } = "{}";
}
