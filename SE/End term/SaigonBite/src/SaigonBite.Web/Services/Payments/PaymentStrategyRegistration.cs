using System.Reflection;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;

namespace SaigonBite.Web.Services.Payments;

/// <summary>
/// Registers every <see cref="IPaymentStrategy"/> that Core ships, plus the resolver Core provides.
/// </summary>
/// <remarks>
/// NFR2 / AGENTS.md hard rule 4: adding a payment method is one new class in Core and one registration
/// line. The registration below is that one line: it discovers strategies by reflection, so a new
/// strategy needs no edit to this file either, and no existing strategy class is ever touched.
/// </remarks>
public static class PaymentStrategyRegistration
{
    /// <summary>Adds every Core payment strategy and the resolver to the container.</summary>
    public static IServiceCollection AddCorePaymentStrategies(this IServiceCollection services)
    {
        var coreAssembly = typeof(IPaymentStrategy).Assembly;

        var strategyTypes = coreAssembly.GetTypes()
            .Where(t => t is { IsClass: true, IsAbstract: false, IsPublic: true })
            .Where(t => typeof(IPaymentStrategy).IsAssignableFrom(t))
            .OrderBy(t => t.Name, StringComparer.Ordinal)
            .ToList();

        if (strategyTypes.Count == 0)
        {
            throw new InvalidOperationException(
                "SaigonBite.Core exposes no IPaymentStrategy implementation. BR13 requires one class per "
                + "payment method (MoMo, VNPay, Apple Pay, PayPal, Cash on Delivery).");
        }

        foreach (var type in strategyTypes)
        {
            var captured = type;

            // ActivatorUtilities honours the optional constructor parameters Core's strategies use
            // (VnPayStrategy takes HttpClient?, an environment reader and a clock), so a strategy can accept
            // collaborators without this registration changing.
            services.AddTransient(
                typeof(IPaymentStrategy),
                provider => (IPaymentStrategy)ActivatorUtilities.CreateInstance(provider, captured));
        }

        // Prefer Core's resolver so the strategy selection rule lives with the strategies. If Core does
        // not ship one, the tiny adapter below - which only filters on IsAvailableFor (BR13) - is used.
        var resolverType = coreAssembly.GetTypes()
            .Where(t => t is { IsClass: true, IsAbstract: false, IsPublic: true })
            .Where(t => typeof(IPaymentStrategyResolver).IsAssignableFrom(t))
            .FirstOrDefault(t => t.GetConstructors()
                .Any(c => c.GetParameters().Length == 1
                          && c.GetParameters()[0].ParameterType
                              == typeof(IEnumerable<IPaymentStrategy>)));

        if (resolverType is not null)
        {
            services.AddTransient(typeof(IPaymentStrategyResolver), resolverType);
        }
        else
        {
            services.AddTransient<IPaymentStrategyResolver, PaymentStrategyResolverAdapter>();
        }

        return services;
    }

    /// <summary>Names of the strategies Core ships, for the startup log and the checkout screen.</summary>
    public static IReadOnlyList<string> Describe(IServiceProvider services)
    {
        using var scope = services.CreateScope();
        return scope.ServiceProvider
            .GetServices<IPaymentStrategy>()
            .OrderBy(s => s.Method)
            .Select(s => $"{s.Method} ({s.Key})")
            .ToList();
    }
}

/// <summary>
/// Fallback <see cref="IPaymentStrategyResolver"/> used only when Core does not provide one.
/// </summary>
/// <remarks>
/// It implements the contract's selection rule and nothing else: BR13 availability is delegated to
/// <see cref="IPaymentStrategy.IsAvailableFor(CustomerType)"/> on each strategy, so a strategy can still
/// change its own eligibility without this class being edited.
/// </remarks>
public sealed class PaymentStrategyResolverAdapter : IPaymentStrategyResolver
{
    private readonly IReadOnlyList<IPaymentStrategy> _strategies;

    /// <summary>Creates the adapter over every registered strategy.</summary>
    public PaymentStrategyResolverAdapter(IEnumerable<IPaymentStrategy> strategies) =>
        _strategies = strategies.ToList();

    /// <inheritdoc />
    public IPaymentStrategy Resolve(PaymentMethod method) =>
        _strategies.FirstOrDefault(s => s.Method == method)
        ?? throw new InvalidOperationException(
            $"No IPaymentStrategy is registered for {method} (BR13).");

    /// <inheritdoc />
    public IReadOnlyList<IPaymentStrategy> AvailableFor(CustomerType customerType) =>
        _strategies.Where(s => s.IsAvailableFor(customerType)).ToList();
}
