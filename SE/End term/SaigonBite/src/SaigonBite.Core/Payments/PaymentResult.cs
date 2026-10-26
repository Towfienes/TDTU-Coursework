namespace SaigonBite.Core.Payments;

/// <summary>
/// The outcome of one payment attempt, mapped onto a <c>PaymentRecord</c> (FR-P3, NFR5).
/// </summary>
/// <param name="Success">True when the gateway accepted the charge, or when COD accepted the order.</param>
/// <param name="GatewayReference">
/// Gateway transaction reference, signed sandbox URL, or the deterministic mock reference. Null on failure.
/// </param>
/// <param name="Error">Business or transport refusal in English, e.g. a BR13 or BR14 violation. Null on success.</param>
/// <param name="RequiresCashConfirmation">
/// True only for Cash on Delivery: the shipper must confirm cash collected before the order may become
/// Delivered (BR14). Every online method returns false.
/// </param>
public sealed record PaymentResult(
    bool Success,
    string? GatewayReference,
    string? Error,
    bool RequiresCashConfirmation)
{
    /// <summary>Convenience constructor for a successful online charge.</summary>
    public static PaymentResult Paid(string gatewayReference) => new(true, gatewayReference, null, false);

    /// <summary>Convenience constructor for a refusal or a failed call.</summary>
    public static PaymentResult Failed(string error) => new(false, null, error, false);
}
