using System.Security.Cryptography;
using System.Text;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR13 payment methods by actor and BR14 Cash on Delivery, exercised through the Strategy pattern.
/// </summary>
/// <remarks>
/// BR13 partitions the five methods by customer group; BR14 partitions the rounded total at
/// 1,000,000 / 1,001,000. The resolver is created with an environment reader that returns null, so these
/// tests never depend on, or touch, the machine's VNPay credentials.
/// </remarks>
public sealed class PaymentStrategyTests
{
    private static readonly Guid OrderId = Guid.Parse("11111111-2222-3333-4444-555555555555");

    private static PaymentStrategyResolver CreateResolver() => PaymentStrategyResolver.CreateDefault(readEnvironment: _ => null);

    private static PaymentRequest Request(long amount, PaymentMethod method, CustomerType customerType) =>
        new(OrderId, amount, method, customerType, ReturnUrl: "https://localhost/payments/return");

    [Fact]
    public void BR13_local_customer_is_offered_momo_vnpay_and_cash()
    {
        var methods = CreateResolver()
            .AvailableFor(CustomerType.Local)
            .Select(strategy => strategy.Method)
            .ToArray();

        Assert.Equal(
            new[] { PaymentMethod.Momo, PaymentMethod.VnPay, PaymentMethod.CashOnDelivery },
            methods);
    }

    [Fact]
    public void BR13_tourist_is_offered_apple_pay_paypal_and_cash()
    {
        var methods = CreateResolver()
            .AvailableFor(CustomerType.Tourist)
            .Select(strategy => strategy.Method)
            .ToArray();

        Assert.Equal(
            new[] { PaymentMethod.ApplePay, PaymentMethod.PayPal, PaymentMethod.CashOnDelivery },
            methods);
    }

    [Fact]
    public void BR13_local_customer_is_never_offered_a_tourist_method()
    {
        var offered = CreateResolver().AvailableFor(CustomerType.Local);

        Assert.DoesNotContain(offered, strategy => strategy.Method == PaymentMethod.ApplePay);
        Assert.DoesNotContain(offered, strategy => strategy.Method == PaymentMethod.PayPal);
    }

    [Fact]
    public void BR13_tourist_is_never_offered_a_local_method()
    {
        var offered = CreateResolver().AvailableFor(CustomerType.Tourist);

        Assert.DoesNotContain(offered, strategy => strategy.Method == PaymentMethod.Momo);
        Assert.DoesNotContain(offered, strategy => strategy.Method == PaymentMethod.VnPay);
    }

    [Fact]
    public async Task BR13_momo_charge_is_refused_for_a_tourist()
    {
        // The resolver hands the strategy over, but the strategy itself refuses the foreign actor group,
        // so a mis-wired controller cannot complete the charge.
        var strategy = CreateResolver().Resolve(PaymentMethod.Momo);

        var result = await strategy.ChargeAsync(Request(200_000, PaymentMethod.Momo, CustomerType.Tourist));

        Assert.False(result.Success);
        Assert.Null(result.GatewayReference);
        Assert.Contains("BR13", result.Error!, StringComparison.Ordinal);
    }

    [Fact]
    public async Task BR13_local_momo_charge_succeeds_with_a_stable_reference()
    {
        var strategy = CreateResolver().Resolve(PaymentMethod.Momo);

        var first = await strategy.ChargeAsync(Request(205_000, PaymentMethod.Momo, CustomerType.Local));
        var second = await strategy.ChargeAsync(Request(205_000, PaymentMethod.Momo, CustomerType.Local));

        Assert.True(first.Success);
        Assert.False(first.RequiresCashConfirmation);
        Assert.StartsWith("MOMO-MOCK-", first.GatewayReference!, StringComparison.Ordinal);
        Assert.Equal(first.GatewayReference, second.GatewayReference);
    }

    [Fact]
    public void PaymentStrategyResolver_resolves_every_registered_method_to_its_own_strategy()
    {
        var resolver = CreateResolver();

        Assert.Equal(PaymentMethod.Momo, resolver.Resolve(PaymentMethod.Momo).Method);
        Assert.Equal(PaymentMethod.VnPay, resolver.Resolve(PaymentMethod.VnPay).Method);
        Assert.Equal(PaymentMethod.ApplePay, resolver.Resolve(PaymentMethod.ApplePay).Method);
        Assert.Equal(PaymentMethod.PayPal, resolver.Resolve(PaymentMethod.PayPal).Method);
        Assert.Equal(PaymentMethod.CashOnDelivery, resolver.Resolve(PaymentMethod.CashOnDelivery).Method);
    }

    [Fact]
    public void PaymentStrategyResolver_uses_distinct_persistable_keys()
    {
        var keys = CreateResolver()
            .AvailableFor(CustomerType.Local)
            .Concat(PaymentStrategyResolver.CreateDefault(readEnvironment: _ => null).AvailableFor(CustomerType.Tourist))
            .Select(strategy => strategy.Key)
            .Distinct(StringComparer.Ordinal)
            .ToArray();

        Assert.Equal(5, keys.Length);
        Assert.All(keys, key => Assert.False(string.IsNullOrWhiteSpace(key)));
    }

    [Fact]
    public void PaymentStrategyResolver_refuses_an_unregistered_method()
    {
        var resolver = CreateResolver();

        Assert.Throws<NotSupportedException>(() => resolver.Resolve((PaymentMethod)99));
    }

    [Fact]
    public void PaymentStrategyResolver_refuses_two_strategies_for_one_method()
    {
        Assert.Throws<ArgumentException>(() => new PaymentStrategyResolver(
            new IPaymentStrategy[] { new MomoStrategy(), new MomoStrategy() }));
    }

    [Fact]
    public async Task BR14_cash_on_delivery_at_1000000_is_allowed()
    {
        var strategy = CreateResolver().Resolve(PaymentMethod.CashOnDelivery);

        var result = await strategy.ChargeAsync(Request(1_000_000, PaymentMethod.CashOnDelivery, CustomerType.Local));

        Assert.True(result.Success);
        Assert.Null(result.Error);
        Assert.True(result.RequiresCashConfirmation);   // BR14: the shipper must confirm cash first
    }

    [Fact]
    public async Task BR14_cash_on_delivery_at_1001000_is_refused()
    {
        var strategy = CreateResolver().Resolve(PaymentMethod.CashOnDelivery);

        var result = await strategy.ChargeAsync(Request(1_001_000, PaymentMethod.CashOnDelivery, CustomerType.Local));

        Assert.False(result.Success);
        Assert.Contains("BR14", result.Error!, StringComparison.Ordinal);
        Assert.False(result.RequiresCashConfirmation);
    }

    [Fact]
    public async Task BR14_cash_on_delivery_at_1000001_is_refused()
    {
        // Boundary value analysis on the exact next đồng above the cap.
        var strategy = CreateResolver().Resolve(PaymentMethod.CashOnDelivery);

        var result = await strategy.ChargeAsync(Request(1_000_001, PaymentMethod.CashOnDelivery, CustomerType.Tourist));

        Assert.False(result.Success);
    }

    [Fact]
    public void BR14_cash_on_delivery_is_offered_to_both_customer_groups()
    {
        var strategy = CreateResolver().Resolve(PaymentMethod.CashOnDelivery);

        Assert.True(strategy.IsAvailableFor(CustomerType.Local));
        Assert.True(strategy.IsAvailableFor(CustomerType.Tourist));
        Assert.Equal("cash-on-delivery", strategy.Key);
    }

    [Fact]
    public async Task BR13_an_online_strategy_refuses_a_non_positive_amount()
    {
        var strategy = CreateResolver().Resolve(PaymentMethod.PayPal);

        var result = await strategy.ChargeAsync(Request(0, PaymentMethod.PayPal, CustomerType.Tourist));

        Assert.False(result.Success);
    }

    [Fact]
    public async Task VNPay_without_environment_returns_the_documented_mock_result()
    {
        var strategy = new VnPayStrategy(readEnvironment: _ => null);

        var result = await strategy.ChargeAsync(Request(205_000, PaymentMethod.VnPay, CustomerType.Local));

        Assert.False(strategy.IsSandboxConfigured);
        Assert.True(result.Success);
        Assert.StartsWith("VNPAY-MOCK-", result.GatewayReference!, StringComparison.Ordinal);
        Assert.False(result.RequiresCashConfirmation);
    }

    [Fact]
    public void VNPay_sandbox_configuration_needs_all_three_variables()
    {
        var complete = new Dictionary<string, string?>
        {
            [VnPaySandboxConfig.TmnCodeVariable] = "TMN123",
            [VnPaySandboxConfig.HashSecretVariable] = "SECRET",
            [VnPaySandboxConfig.UrlVariable] = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html",
        };

        Assert.NotNull(VnPaySandboxConfig.FromEnvironment(name => complete.GetValueOrDefault(name)));

        complete[VnPaySandboxConfig.HashSecretVariable] = null;
        Assert.Null(VnPaySandboxConfig.FromEnvironment(name => complete.GetValueOrDefault(name)));
    }

    [Fact]
    public void VNPay_payment_url_is_sorted_and_signed_with_hmac_sha512()
    {
        var config = new VnPaySandboxConfig(
            TmnCode: "TMN123",
            HashSecret: "SECRETKEY",
            PaymentUrl: "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html");

        var request = new PaymentRequest(OrderId, 205_000, PaymentMethod.VnPay, CustomerType.Local, "https://localhost/return");
        var now = new DateTimeOffset(2026, 10, 20, 8, 0, 0, TimeSpan.Zero);   // 15:00 in Vietnam

        var url = VnPaySandboxClient.BuildPaymentUrl(config, request, now);

        Assert.StartsWith("https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?", url, StringComparison.Ordinal);
        Assert.Contains("vnp_Amount=20500000", url, StringComparison.Ordinal);   // VNPay expects amount × 100
        Assert.Contains("vnp_CreateDate=20261020150000", url, StringComparison.Ordinal);   // UTC+7 wall clock
        Assert.Contains("vnp_TxnRef=11111111222233334444555555555555", url, StringComparison.Ordinal);

        // Parse the query the way ASP.NET Core hands a return-URL callback to the application: decoded
        // values, which is what VerifySignature expects to re-encode.
        var parameters = url[(url.IndexOf('?', StringComparison.Ordinal) + 1)..]
            .Split('&', StringSplitOptions.RemoveEmptyEntries)
            .Select(pair => pair.Split('=', 2))
            .ToDictionary(
                parts => parts[0],
                parts => parts.Length > 1 ? Uri.UnescapeDataString(parts[1]) : string.Empty);

        Assert.True(VnPaySandboxClient.VerifySignature(parameters, config.HashSecret));

        // Any tampering with a signed value must fail verification.
        parameters["vnp_Amount"] = "1";
        Assert.False(VnPaySandboxClient.VerifySignature(parameters, config.HashSecret));
    }

    [Fact]
    public void VNPay_signature_matches_an_independently_computed_hmac()
    {
        var parameters = new Dictionary<string, string>
        {
            ["vnp_Command"] = "pay",
            ["vnp_Amount"] = "20500000",
            ["vnp_TmnCode"] = "TMN123",
        };

        var query = VnPaySandboxClient.BuildSignedQuery(parameters, "SECRETKEY");

        const string signData = "vnp_Amount=20500000&vnp_Command=pay&vnp_TmnCode=TMN123";
        using var hmac = new HMACSHA512(Encoding.UTF8.GetBytes("SECRETKEY"));
        var expected = Convert.ToHexString(hmac.ComputeHash(Encoding.UTF8.GetBytes(signData))).ToLowerInvariant();

        Assert.Equal(string.Concat(signData, "&vnp_SecureHash=", expected), query);
        Assert.Equal(128, expected.Length);   // SHA-512 → 128 hex characters
    }

    [Fact]
    public void VNPay_return_url_without_a_signature_is_not_trusted()
    {
        var returned = new Dictionary<string, string>
        {
            ["vnp_ResponseCode"] = "00",
            ["vnp_TxnRef"] = "11111111222233334444555555555555",
        };

        Assert.False(VnPaySandboxClient.TryVerifyReturnUrl(returned, "SECRETKEY", out var responseCode));
        Assert.Equal("00", responseCode);
    }

    [Fact]
    public void VNPay_payment_url_requires_a_return_url()
    {
        var config = new VnPaySandboxConfig("TMN123", "SECRETKEY", "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html");
        var request = new PaymentRequest(OrderId, 205_000, PaymentMethod.VnPay, CustomerType.Local, ReturnUrl: null);

        Assert.Throws<ArgumentException>(() =>
            VnPaySandboxClient.BuildPaymentUrl(config, request, DateTimeOffset.UtcNow));
    }
}
