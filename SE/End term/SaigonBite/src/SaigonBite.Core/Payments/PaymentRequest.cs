using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// The input of a single payment attempt (BR13, BR14, FR-P3).
/// </summary>
/// <param name="OrderId">Order being paid; used as the gateway transaction reference prefix.</param>
/// <param name="Amount">
/// The rounded order total from <see cref="Pricing.PriceResult.Total"/>, in whole VND. BR14 compares this
/// value against 1,000,000 for Cash on Delivery; BR11 has already rounded it once, so no further rounding
/// happens here.
/// </param>
/// <param name="Method">Chosen method; must agree with the resolved strategy's <see cref="IPaymentStrategy.Method"/>.</param>
/// <param name="CustomerType">Paying actor's group; BR13 refuses a method from the other group.</param>
/// <param name="ReturnUrl">Absolute URL the gateway returns the customer to (VNPay sandbox requires one).</param>
public sealed record PaymentRequest(
    Guid OrderId,
    long Amount,
    PaymentMethod Method,
    CustomerType CustomerType,
    string? ReturnUrl);
