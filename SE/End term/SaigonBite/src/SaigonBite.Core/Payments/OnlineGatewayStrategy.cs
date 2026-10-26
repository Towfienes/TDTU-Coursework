using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// Shared behaviour for the three simulated online gateways (MoMo, Apple Pay, PayPal): BR13 actor
/// gating plus a deterministic mock reference.
/// </summary>
/// <remarks>
/// <para>
/// The specification allows standard tiers to simulate payments "against a mock gateway with a
/// documented interface" (section G). This base class <em>is</em> that documented interface: it returns
/// a success whose reference is reproducibly derived from the order id, so a demo, a test and a report
/// screenshot all show the same value for the same order.
/// </para>
/// <para>
/// VNPay does not derive from this class because Tier 4 requires it to call its live sandbox; see
/// <see cref="VnPayStrategy"/>.
/// </para>
/// <para>
/// A strategy for a new method either derives from this class (if it is simulated) or implements
/// <see cref="IPaymentStrategy"/> directly (if it calls a real gateway). Neither choice edits any
/// existing strategy, which is the NFR2 change-request evidence.
/// </para>
/// </remarks>
public abstract class OnlineGatewayStrategy : IPaymentStrategy
{
    /// <inheritdoc />
    public abstract PaymentMethod Method { get; }

    /// <inheritdoc />
    public abstract string Key { get; }

    /// <summary>The single customer group BR13 grants this method to.</summary>
    protected abstract CustomerType BelongsTo { get; }

    /// <inheritdoc />
    public bool IsAvailableFor(CustomerType customerType) => customerType == BelongsTo;

    /// <inheritdoc />
    /// <remarks>
    /// Refuses an actor group that BR13 does not grant the method to, then returns the documented mock
    /// success. Refusing here as well as in the resolver means a mis-wired controller cannot complete a
    /// foreign payment.
    /// </remarks>
    public Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken ct = default)
    {
        ArgumentNullException.ThrowIfNull(request);

        if (!IsAvailableFor(request.CustomerType))
        {
            return Task.FromResult(PaymentResult.Failed(PaymentStrategyMessages.MethodNotAvailableForActor(Key, request.CustomerType)));
        }

        if (request.Amount <= 0)
        {
            return Task.FromResult(PaymentResult.Failed(PaymentStrategyMessages.NonPositiveAmount(Key, request.Amount)));
        }

        return Task.FromResult(PaymentResult.Paid(PaymentStrategyMessages.MockReference(Key, request.OrderId)));
    }
}
