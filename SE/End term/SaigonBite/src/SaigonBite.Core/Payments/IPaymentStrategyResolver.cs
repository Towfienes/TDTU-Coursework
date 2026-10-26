using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// Selects the payment strategy for a method, and lists the methods an actor group may see (BR13, FR-P1).
/// </summary>
public interface IPaymentStrategyResolver
{
    /// <summary>
    /// Returns the strategy registered for <paramref name="method"/>.
    /// </summary>
    /// <remarks>
    /// This lookup is actor-agnostic for signature stability; BR13 is enforced by
    /// <see cref="IPaymentStrategy.IsAvailableFor"/> and re-checked inside every strategy, so resolving
    /// a foreign method cannot complete a charge.
    /// </remarks>
    /// <exception cref="NotSupportedException">No strategy is registered for the method.</exception>
    IPaymentStrategy Resolve(PaymentMethod method);

    /// <summary>Every method offered to <paramref name="customerType"/>, in registration order (BR13).</summary>
    IReadOnlyList<IPaymentStrategy> AvailableFor(CustomerType customerType);
}
