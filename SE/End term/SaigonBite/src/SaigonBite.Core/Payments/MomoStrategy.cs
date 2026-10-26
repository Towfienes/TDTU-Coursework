using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// MoMo e-wallet — Local Customer only (BR13).
/// </summary>
/// <remarks>
/// Simulated against the documented mock gateway of <see cref="OnlineGatewayStrategy"/>; the
/// <c>StrategyKey</c> <c>momo</c> is what <c>PaymentRecord</c> stores (FR-P3).
/// </remarks>
public sealed class MomoStrategy : OnlineGatewayStrategy
{
    /// <summary>The key persisted on <c>PaymentRecord.StrategyKey</c>.</summary>
    public const string StrategyKey = "momo";

    /// <inheritdoc />
    public override PaymentMethod Method => PaymentMethod.Momo;

    /// <inheritdoc />
    public override string Key => StrategyKey;

    /// <inheritdoc />
    protected override CustomerType BelongsTo => CustomerType.Local;
}
