namespace SaigonBite.Core.Payments;

/// <summary>
/// The five payment methods of BR13, stored on the order as <c>Order.PaymentMethod?</c>.
/// </summary>
/// <remarks>
/// Adding a method is a change request exercise (NFR2): add one enum member, one
/// <see cref="IPaymentStrategy"/> class and one registration line. No existing strategy is edited.
/// </remarks>
public enum PaymentMethod
{
    /// <summary>MoMo e-wallet — Local Customer only (BR13).</summary>
    Momo = 0,

    /// <summary>VNPay gateway — Local Customer only; Tier 4 live sandbox (BR13).</summary>
    VnPay = 1,

    /// <summary>Apple Pay — Foreign Tourist only (BR13).</summary>
    ApplePay = 2,

    /// <summary>PayPal — Foreign Tourist only (BR13).</summary>
    PayPal = 3,

    /// <summary>Cash on Delivery — both customer groups, capped by BR14.</summary>
    CashOnDelivery = 4,
}
