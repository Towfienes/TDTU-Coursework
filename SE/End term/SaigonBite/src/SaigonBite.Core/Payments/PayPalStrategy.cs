using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// PayPal — Foreign Tourist only (BR13).
/// </summary>
/// <remarks>Simulated against the documented mock gateway of <see cref="OnlineGatewayStrategy"/>.</remarks>
public sealed class PayPalStrategy : OnlineGatewayStrategy
{
    /// <summary>The key persisted on <c>PaymentRecord.StrategyKey</c>.</summary>
    public const string StrategyKey = "paypal";

    /// <inheritdoc />
    public override PaymentMethod Method => PaymentMethod.PayPal;

    /// <inheritdoc />
    public override string Key => StrategyKey;

    /// <inheritdoc />
    protected override CustomerType BelongsTo => CustomerType.Tourist;
}
