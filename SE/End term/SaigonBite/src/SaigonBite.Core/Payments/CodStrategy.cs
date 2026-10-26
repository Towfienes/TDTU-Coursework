using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// Cash on Delivery — offered to both customer groups, capped by BR14.
/// </summary>
/// <remarks>
/// <para>
/// BR14: "Allowed only if the rounded total is 1,000,000 or less" (boundary 1,000,000 / 1,001,000).
/// The amount is the already-rounded <see cref="Pricing.PriceResult.Total"/>, so the comparison is made
/// against exactly the number the customer was shown.
/// </para>
/// <para>
/// A COD charge succeeds immediately but is not yet a payment: it sets
/// <see cref="PaymentResult.RequiresCashConfirmation"/> so the shipper must confirm cash collected before
/// the order may become Delivered (BR14, FR-F3).
/// </para>
/// </remarks>
public sealed class CodStrategy : IPaymentStrategy
{
    /// <summary>The key persisted on <c>PaymentRecord.StrategyKey</c>.</summary>
    public const string StrategyKey = "cash-on-delivery";

    /// <summary>BR14 — COD is allowed only when the rounded total is at or below this amount.</summary>
    public const long MaximumCodTotal = 1_000_000;

    /// <inheritdoc />
    public PaymentMethod Method => PaymentMethod.CashOnDelivery;

    /// <inheritdoc />
    public string Key => StrategyKey;

    /// <inheritdoc />
    /// <remarks>Both groups may pay cash (BR13); the amount condition is per order and lives in <see cref="ChargeAsync"/>.</remarks>
    public bool IsAvailableFor(CustomerType customerType) =>
        customerType is CustomerType.Local or CustomerType.Tourist;

    /// <inheritdoc />
    /// <remarks>Refuses above the BR14 cap; otherwise accepts the COD order and flags the cash-confirmation duty.</remarks>
    public Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken ct = default)
    {
        ArgumentNullException.ThrowIfNull(request);

        if (!IsAvailableFor(request.CustomerType))
        {
            return Task.FromResult(PaymentResult.Failed(
                PaymentStrategyMessages.MethodNotAvailableForActor(Key, request.CustomerType)));
        }

        if (request.Amount > MaximumCodTotal)
        {
            return Task.FromResult(PaymentResult.Failed(
                PaymentStrategyMessages.CashOnDeliveryAboveCap(request.Amount, MaximumCodTotal)));
        }

        if (request.Amount <= 0)
        {
            return Task.FromResult(PaymentResult.Failed(
                PaymentStrategyMessages.NonPositiveAmount(Key, request.Amount)));
        }

        // No gateway is called: COD is accepted at checkout and settled at the door (BR14).
        return Task.FromResult(new PaymentResult(
            Success: true,
            GatewayReference: PaymentStrategyMessages.MockReference(Key, request.OrderId),
            Error: null,
            RequiresCashConfirmation: true));
    }
}
