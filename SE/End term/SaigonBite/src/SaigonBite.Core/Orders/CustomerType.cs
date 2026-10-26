namespace SaigonBite.Core.Orders;

/// <summary>
/// The two customer groups of the actor model (BR13). They share one user schema and differ in
/// registration data and in the payment methods offered to them.
/// </summary>
public enum CustomerType
{
    /// <summary>Vietnamese customer; MoMo, VNPay or Cash on Delivery (BR13).</summary>
    Local = 0,

    /// <summary>Foreign tourist; Apple Pay, PayPal or Cash on Delivery (BR13).</summary>
    Tourist = 1,
}
