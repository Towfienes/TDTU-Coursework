using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// VNPay — Local Customer only (BR13), with a real sandbox call when the merchant environment is set.
/// </summary>
/// <remarks>
/// <para>
/// Tier 4 requires one live sandbox integration. The switch is deliberate and configuration-only:
/// </para>
/// <list type="bullet">
///   <item><description>
///     When <c>VNPAY_TMN_CODE</c>, <c>VNPAY_HASH_SECRET</c> and <c>VNPAY_URL</c> are all present, the
///     strategy builds the signed VNPay 2.1.0 payment URL and calls the sandbox through
///     <see cref="VnPaySandboxClient"/>.
///   </description></item>
///   <item><description>
///     When any of them is absent, the strategy returns the documented mock result
///     <c>VNPAY-MOCK-&lt;order id&gt;</c> so the demo, the unit tests and a fresh checkout all work with
///     no credentials. Nothing else about the strategy changes.
///   </description></item>
/// </list>
/// <para>
/// No secret is ever returned in a <see cref="PaymentResult"/>; only the signed URL (which VNPay needs
/// the customer to open) is exposed as the gateway reference.
/// </para>
/// </remarks>
public sealed class VnPayStrategy : IPaymentStrategy
{
    /// <summary>The key persisted on <c>PaymentRecord.StrategyKey</c>.</summary>
    public const string StrategyKey = "vnpay";

    private readonly Func<string, string?> _readEnvironment;
    private readonly VnPaySandboxClient _sandbox;

    /// <summary>Creates the strategy.</summary>
    /// <param name="httpClient">Transport for the sandbox call; a shared default client is used when null.</param>
    /// <param name="readEnvironment">Environment accessor; defaults to <see cref="Environment.GetEnvironmentVariable(string)"/>.</param>
    /// <param name="clock">Clock for the signed timestamps; defaults to <see cref="DateTimeOffset.UtcNow"/>.</param>
    public VnPayStrategy(
        HttpClient? httpClient = null,
        Func<string, string?>? readEnvironment = null,
        Func<DateTimeOffset>? clock = null)
    {
        _readEnvironment = readEnvironment ?? Environment.GetEnvironmentVariable;
        _sandbox = new VnPaySandboxClient(httpClient, clock);
    }

    /// <inheritdoc />
    public PaymentMethod Method => PaymentMethod.VnPay;

    /// <inheritdoc />
    public string Key => StrategyKey;

    /// <inheritdoc />
    public bool IsAvailableFor(CustomerType customerType) => customerType == CustomerType.Local;

    /// <summary>True when the sandbox is configured, i.e. the next charge makes a real HTTP call.</summary>
    public bool IsSandboxConfigured => VnPaySandboxConfig.FromEnvironment(_readEnvironment) is not null;

    /// <inheritdoc />
    /// <remarks>
    /// BR13 is re-checked here so a mis-wired controller cannot charge a tourist with VNPay. An amount of
    /// zero or less is refused before any gateway is contacted.
    /// </remarks>
    public async Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken ct = default)
    {
        ArgumentNullException.ThrowIfNull(request);

        if (!IsAvailableFor(request.CustomerType))
        {
            return PaymentResult.Failed(PaymentStrategyMessages.MethodNotAvailableForActor(Key, request.CustomerType));
        }

        if (request.Amount <= 0)
        {
            return PaymentResult.Failed(PaymentStrategyMessages.NonPositiveAmount(Key, request.Amount));
        }

        var config = VnPaySandboxConfig.FromEnvironment(_readEnvironment);

        if (config is null)
        {
            // Documented fallback (§2G "mock gateway with a documented interface"): no credentials, no call.
            return PaymentResult.Paid(PaymentStrategyMessages.MockReference(Key, request.OrderId));
        }

        return await _sandbox.ChargeAsync(config, request, ct).ConfigureAwait(false);
    }
}
