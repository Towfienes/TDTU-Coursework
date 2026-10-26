using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// Resolves a <see cref="PaymentMethod"/> to its strategy and lists what each customer group may use
/// (BR13, FR-P1).
/// </summary>
/// <remarks>
/// <para>
/// Registration is the extension point NFR2 measures: adding a method means adding one
/// <see cref="IPaymentStrategy"/> and one entry in the collection passed to the constructor (in
/// ASP.NET Core, one <c>services.AddSingleton&lt;IPaymentStrategy, XStrategy&gt;()</c> line). No existing
/// strategy class is opened.
/// </para>
/// <para>
/// The resolver itself is immutable: the strategies are copied into a dictionary at construction, so
/// concurrent checkout requests only read it.
/// </para>
/// </remarks>
public sealed class PaymentStrategyResolver : IPaymentStrategyResolver
{
    private readonly IReadOnlyDictionary<PaymentMethod, IPaymentStrategy> _byMethod;
    private readonly IReadOnlyList<IPaymentStrategy> _registered;

    /// <summary>Creates a resolver over the registered strategies, in registration order.</summary>
    /// <param name="strategies">Every registered strategy; duplicates of a method are rejected.</param>
    /// <exception cref="ArgumentNullException"><paramref name="strategies"/> is null.</exception>
    /// <exception cref="ArgumentException">Two strategies claim the same <see cref="PaymentMethod"/>.</exception>
    public PaymentStrategyResolver(IEnumerable<IPaymentStrategy> strategies)
    {
        ArgumentNullException.ThrowIfNull(strategies);

        var registered = strategies.ToList();
        var byMethod = new Dictionary<PaymentMethod, IPaymentStrategy>(registered.Count);

        foreach (var strategy in registered)
        {
            if (!byMethod.TryAdd(strategy.Method, strategy))
            {
                throw new ArgumentException(
                    string.Concat(
                        "Two payment strategies are registered for ",
                        strategy.Method.ToString(),
                        "; exactly one strategy per method is allowed."),
                    nameof(strategies));
            }
        }

        _registered = registered;
        _byMethod = byMethod;
    }

    /// <summary>Creates the resolver with all five BR13 strategies registered.</summary>
    /// <param name="httpClient">Optional transport passed to <see cref="VnPayStrategy"/>.</param>
    /// <param name="readEnvironment">Optional environment accessor passed to <see cref="VnPayStrategy"/>.</param>
    public static PaymentStrategyResolver CreateDefault(
        HttpClient? httpClient = null,
        Func<string, string?>? readEnvironment = null) =>
        new(new IPaymentStrategy[]
        {
            new MomoStrategy(),
            new VnPayStrategy(httpClient, readEnvironment),
            new ApplePayStrategy(),
            new PayPalStrategy(),
            new CodStrategy(),
        });

    /// <inheritdoc />
    /// <exception cref="NotSupportedException">Nothing is registered for <paramref name="method"/>.</exception>
    public IPaymentStrategy Resolve(PaymentMethod method) =>
        _byMethod.TryGetValue(method, out var strategy)
            ? strategy
            : throw new NotSupportedException(
                string.Concat("No payment strategy is registered for ", method.ToString(), "."));

    /// <inheritdoc />
    public IReadOnlyList<IPaymentStrategy> AvailableFor(CustomerType customerType) =>
        _registered.Where(strategy => strategy.IsAvailableFor(customerType)).ToList();
}
