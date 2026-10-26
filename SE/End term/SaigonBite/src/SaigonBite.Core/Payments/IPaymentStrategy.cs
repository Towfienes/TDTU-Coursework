using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// One payment strategy per BR13 method (section G: "one payment interface, one class per method").
/// </summary>
/// <remarks>
/// NFR2 — adding a method means one new implementation plus one registration; no existing strategy is
/// touched. Implementations must never mutate shared state: the resolver hands the same instance to
/// every request.
/// </remarks>
public interface IPaymentStrategy
{
    /// <summary>The method this strategy implements.</summary>
    PaymentMethod Method { get; }

    /// <summary>
    /// Stable string stored on <c>PaymentRecord.StrategyKey</c> (FR-P3), e.g. <c>momo</c> or
    /// <c>cash-on-delivery</c>. It is persisted, so it must not change once orders exist.
    /// </summary>
    string Key { get; }

    /// <summary>
    /// BR13 — true when this method belongs to <paramref name="customerType"/>'s group.
    /// </summary>
    bool IsAvailableFor(CustomerType customerType);

    /// <summary>
    /// Attempts the payment.
    /// </summary>
    /// <param name="request">Order, rounded total and the customer type making the payment.</param>
    /// <param name="ct">Cancellation token.</param>
    /// <returns>
    /// A result rather than an exception for business refusals (wrong actor group, BR14 amount cap);
    /// failures are recorded on the <c>PaymentRecord</c> with <see cref="PaymentResult.Success"/> false.
    /// </returns>
    Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken ct = default);
}
