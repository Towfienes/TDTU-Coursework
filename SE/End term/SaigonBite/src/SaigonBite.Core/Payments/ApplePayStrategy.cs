using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// Apple Pay — Foreign Tourist only (BR13).
/// </summary>
/// <remarks>Simulated against the documented mock gateway of <see cref="OnlineGatewayStrategy"/>.</remarks>
public sealed class ApplePayStrategy : OnlineGatewayStrategy
{
    /// <summary>The key persisted on <c>PaymentRecord.StrategyKey</c>.</summary>
    public const string StrategyKey = "apple-pay";

    /// <inheritdoc />
    public override PaymentMethod Method => PaymentMethod.ApplePay;

    /// <inheritdoc />
    public override string Key => StrategyKey;

    /// <inheritdoc />
    protected override CustomerType BelongsTo => CustomerType.Tourist;
}
