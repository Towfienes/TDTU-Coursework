using System.Globalization;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text;

namespace SaigonBite.Core.Payments;

/// <summary>
/// The three environment variables that switch VNPay from the mock gateway to the live sandbox
/// (Tier 4 requirement, BR13).
/// </summary>
/// <param name="TmnCode">Merchant terminal code, from <c>VNPAY_TMN_CODE</c>.</param>
/// <param name="HashSecret">Merchant hash secret, from <c>VNPAY_HASH_SECRET</c>.</param>
/// <param name="PaymentUrl">Sandbox payment endpoint, from <c>VNPAY_URL</c>.</param>
/// <remarks>
/// Secrets are read from the environment at call time and never logged, echoed into a payment result or
/// stored in source (NFR4).
/// </remarks>
public sealed record VnPaySandboxConfig(string TmnCode, string HashSecret, string PaymentUrl)
{
    /// <summary>Environment variable holding the merchant terminal code.</summary>
    public const string TmnCodeVariable = "VNPAY_TMN_CODE";

    /// <summary>Environment variable holding the merchant hash secret.</summary>
    public const string HashSecretVariable = "VNPAY_HASH_SECRET";

    /// <summary>Environment variable holding the sandbox payment endpoint.</summary>
    public const string UrlVariable = "VNPAY_URL";

    /// <summary>
    /// Reads the sandbox configuration, or null when any of the three variables is missing or blank.
    /// </summary>
    /// <param name="read">Environment accessor; production passes <see cref="Environment.GetEnvironmentVariable(string)"/>,
    /// tests pass a fake so the mock path is exercised without touching process state.</param>
    public static VnPaySandboxConfig? FromEnvironment(Func<string, string?> read)
    {
        ArgumentNullException.ThrowIfNull(read);

        var tmnCode = read(TmnCodeVariable);
        var hashSecret = read(HashSecretVariable);
        var paymentUrl = read(UrlVariable);

        if (string.IsNullOrWhiteSpace(tmnCode) || string.IsNullOrWhiteSpace(hashSecret) || string.IsNullOrWhiteSpace(paymentUrl))
        {
            return null;
        }

        return new VnPaySandboxConfig(tmnCode.Trim(), hashSecret.Trim(), paymentUrl.Trim());
    }
}

/// <summary>
/// The VNPay sandbox integration, kept in its own file so it is obviously separable from the strategy
/// and from the other methods (BR13, Tier 4).
/// </summary>
/// <remarks>
/// <para>
/// VNPay is a redirect gateway, not a server-to-server charge API: the merchant builds a signed payment
/// URL, the customer pays on the VNPay page, and VNPay returns the customer to the merchant's return URL
/// with a signed result. This class therefore does two things and nothing more:
/// </para>
/// <list type="number">
///   <item><description>
///     <see cref="BuildPaymentUrl"/> — builds the VNPay 2.1.0 request: parameters sorted by name,
///     URL-encoded values, then an HMAC-SHA512 signature over the query string.
///   </description></item>
///   <item><description>
///     <see cref="ChargeAsync"/> — calls the configured sandbox endpoint to confirm it accepts the request,
///     and returns the signed URL as the gateway reference. The authoritative success or failure of the
///     payment itself is <c>vnp_ResponseCode</c> on the return URL, verified by
///     <see cref="TryVerifyReturnUrl"/>.
///   </description></item>
/// </list>
/// <para>
/// No network call happens here unless the caller constructs this class; when the three environment
/// variables are absent, <see cref="VnPayStrategy"/> never reaches this type at all.
/// </para>
/// </remarks>
public sealed class VnPaySandboxClient
{
    /// <summary>VNPay API version this request format targets.</summary>
    public const string ApiVersion = "2.1.0";

    /// <summary>VNPay multiplies the amount by 100 on the wire; the order itself stays in whole VND.</summary>
    public const int AmountMultiplier = 100;

    /// <summary>Vietnam has no daylight saving, so the gateway clock is UTC+7 all year.</summary>
    public static readonly TimeSpan VietnamOffset = TimeSpan.FromHours(7);

    private static readonly HttpClient DefaultHttpClient = new() { Timeout = TimeSpan.FromSeconds(15) };

    private readonly HttpClient _httpClient;
    private readonly Func<DateTimeOffset> _clock;

    /// <summary>Creates a client.</summary>
    /// <param name="httpClient">Transport; a shared default client is used when null.</param>
    /// <param name="clock">Clock used for <c>vnp_CreateDate</c>; defaults to <see cref="DateTimeOffset.UtcNow"/>.</param>
    public VnPaySandboxClient(HttpClient? httpClient = null, Func<DateTimeOffset>? clock = null)
    {
        _httpClient = httpClient ?? DefaultHttpClient;
        _clock = clock ?? (() => DateTimeOffset.UtcNow);
    }

    /// <summary>
    /// Builds the signed VNPay 2.1.0 payment URL for an order.
    /// </summary>
    /// <param name="config">Merchant sandbox credentials.</param>
    /// <param name="request">Order and rounded amount being paid.</param>
    /// <param name="now">Reference time; converted to UTC+7 for the gateway timestamps.</param>
    /// <exception cref="ArgumentException">The request carries no return URL, which VNPay requires.</exception>
    public static string BuildPaymentUrl(VnPaySandboxConfig config, PaymentRequest request, DateTimeOffset now)
    {
        ArgumentNullException.ThrowIfNull(config);
        ArgumentNullException.ThrowIfNull(request);

        if (string.IsNullOrWhiteSpace(request.ReturnUrl))
        {
            throw new ArgumentException(
                "VNPay requires a return URL; set PaymentRequest.ReturnUrl before calling the sandbox.",
                nameof(request));
        }

        var created = now.ToOffset(VietnamOffset);

        var parameters = new SortedDictionary<string, string>(StringComparer.Ordinal)
        {
            ["vnp_Version"] = ApiVersion,
            ["vnp_Command"] = "pay",
            ["vnp_TmnCode"] = config.TmnCode,
            ["vnp_Amount"] = (request.Amount * AmountMultiplier).ToString(CultureInfo.InvariantCulture),
            ["vnp_CreateDate"] = created.ToString("yyyyMMddHHmmss", CultureInfo.InvariantCulture),
            ["vnp_ExpireDate"] = created.AddMinutes(15).ToString("yyyyMMddHHmmss", CultureInfo.InvariantCulture),
            ["vnp_CurrCode"] = "VND",
            ["vnp_IpAddr"] = "127.0.0.1",
            ["vnp_Locale"] = "vn",
            // Kept to ASCII without spaces: the gateway re-encodes the order info when it signs.
            ["vnp_OrderInfo"] = string.Concat("SaigonBite-Order-", request.OrderId.ToString("N")),
            ["vnp_OrderType"] = "other",
            ["vnp_ReturnUrl"] = request.ReturnUrl,
            ["vnp_TxnRef"] = RequestReference(request.OrderId),
        };

        var signedQuery = BuildSignedQuery(parameters, config.HashSecret);
        var separator = config.PaymentUrl.Contains('?') ? "&" : "?";

        return string.Concat(config.PaymentUrl, separator, signedQuery);
    }

    /// <summary>The <c>vnp_TxnRef</c> for an order: the order id without separators.</summary>
    public static string RequestReference(Guid orderId) => orderId.ToString("N");

    /// <summary>
    /// Builds the URL-encoded, sorted query string and appends its HMAC-SHA512 signature.
    /// </summary>
    /// <param name="parameters">Request parameters.</param>
    /// <param name="hashSecret">Merchant hash secret.</param>
    public static string BuildSignedQuery(IEnumerable<KeyValuePair<string, string>> parameters, string hashSecret)
    {
        var signData = BuildSignData(parameters);

        return string.Concat(signData, "&vnp_SecureHash=", Sign(signData, hashSecret));
    }

    /// <summary>The part of the query that VNPay signs: sorted, URL-encoded <c>key=value</c> pairs joined by <c>&amp;</c>.</summary>
    public static string BuildSignData(IEnumerable<KeyValuePair<string, string>> parameters)
    {
        ArgumentNullException.ThrowIfNull(parameters);

        var pairs = parameters
            .Where(pair => !string.Equals(pair.Key, "vnp_SecureHash", StringComparison.Ordinal)
                        && !string.Equals(pair.Key, "vnp_SecureHashType", StringComparison.Ordinal))
            .OrderBy(pair => pair.Key, StringComparer.Ordinal)
            .Select(pair => string.Concat(pair.Key, "=", Uri.EscapeDataString(pair.Value ?? string.Empty)));

        return string.Join("&", pairs);
    }

    /// <summary>HMAC-SHA512 of <paramref name="signData"/> with the merchant secret, as lowercase hex.</summary>
    public static string Sign(string signData, string hashSecret)
    {
        ArgumentNullException.ThrowIfNull(signData);
        ArgumentNullException.ThrowIfNull(hashSecret);

        var key = Encoding.UTF8.GetBytes(hashSecret);
        var data = Encoding.UTF8.GetBytes(signData);
        var hash = HMACSHA512.HashData(key, data);

        return Convert.ToHexString(hash).ToLowerInvariant();
    }

    /// <summary>
    /// Verifies a signature the gateway sent back on the return URL.
    /// </summary>
    /// <param name="returnedParameters">Every query parameter VNPay returned, including <c>vnp_SecureHash</c>.</param>
    /// <param name="hashSecret">Merchant hash secret.</param>
    /// <returns>True when the signature matches, i.e. the result was not tampered with.</returns>
    public static bool VerifySignature(IReadOnlyDictionary<string, string> returnedParameters, string hashSecret)
    {
        ArgumentNullException.ThrowIfNull(returnedParameters);

        if (!returnedParameters.TryGetValue("vnp_SecureHash", out var receivedHash) || string.IsNullOrEmpty(receivedHash))
        {
            return false;
        }

        var expected = Sign(BuildSignData(returnedParameters), hashSecret);

        return CryptographicOperations.FixedTimeEquals(
            Encoding.ASCII.GetBytes(expected),
            Encoding.ASCII.GetBytes(receivedHash.ToLowerInvariant()));
    }

    /// <summary>
    /// Verifies a return-URL callback and extracts <c>vnp_ResponseCode</c> (BR13, FR-P3).
    /// </summary>
    /// <param name="returnedParameters">Every query parameter VNPay returned.</param>
    /// <param name="hashSecret">Merchant hash secret.</param>
    /// <param name="responseCode">The gateway response code; <c>"00"</c> means paid.</param>
    /// <returns>True when the signature is valid and the response code <c>"00"</c> means the order is paid.</returns>
    public static bool TryVerifyReturnUrl(
        IReadOnlyDictionary<string, string> returnedParameters,
        string hashSecret,
        out string? responseCode)
    {
        ArgumentNullException.ThrowIfNull(returnedParameters);

        responseCode = returnedParameters.TryGetValue("vnp_ResponseCode", out var code) ? code : null;

        return VerifySignature(returnedParameters, hashSecret);
    }

    /// <summary>
    /// Calls the configured sandbox endpoint for an order and returns the signed payment URL on success.
    /// </summary>
    /// <param name="config">Merchant sandbox credentials.</param>
    /// <param name="request">Order and rounded amount being paid.</param>
    /// <param name="ct">Cancellation token.</param>
    /// <remarks>
    /// A non-success HTTP status, a transport error or a timeout is reported as a failed
    /// <see cref="PaymentResult"/> rather than an exception, so the caller can record the attempt on the
    /// <c>PaymentRecord</c> (FR-P3, NFR5).
    /// </remarks>
    public async Task<PaymentResult> ChargeAsync(VnPaySandboxConfig config, PaymentRequest request, CancellationToken ct = default)
    {
        ArgumentNullException.ThrowIfNull(config);
        ArgumentNullException.ThrowIfNull(request);

        string paymentUrl;

        try
        {
            paymentUrl = BuildPaymentUrl(config, request, _clock());
        }
        catch (ArgumentException ex)
        {
            return PaymentResult.Failed(string.Concat("BR13: VNPay request could not be built: ", ex.Message));
        }

        try
        {
            using var response = await _httpClient
                .GetAsync(paymentUrl, HttpCompletionOption.ResponseHeadersRead, ct)
                .ConfigureAwait(false);

            if (!response.IsSuccessStatusCode)
            {
                return PaymentResult.Failed(string.Concat(
                    "VNPay sandbox rejected the request with HTTP ",
                    ((int)response.StatusCode).ToString(CultureInfo.InvariantCulture),
                    " (",
                    response.ReasonPhrase ?? "no reason",
                    ")."));
            }
        }
        catch (OperationCanceledException) when (ct.IsCancellationRequested)
        {
            throw;
        }
        catch (Exception ex) when (ex is HttpRequestException or OperationCanceledException)
        {
            return PaymentResult.Failed(string.Concat("VNPay sandbox is unreachable: ", ex.Message));
        }

        // The sandbox has accepted the request. It now shows its payment page, and the authoritative
        // outcome arrives on ReturnUrl and is validated by VerifyReturnUrl (vnp_ResponseCode == "00").
        return PaymentResult.Paid(paymentUrl);
    }
}
