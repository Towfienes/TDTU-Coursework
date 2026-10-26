using SaigonBite.Core.Orders;

namespace SaigonBite.Core.Payments;

/// <summary>
/// English messages and reference formats shared by the payment strategies.
/// </summary>
/// <remarks>
/// Messages are English source text (AGENTS.md rule 1); the web layer maps the machine-readable
/// reason onto a <c>.resx</c> entry for the Vietnamese interface (FR-S1).
/// </remarks>
internal static class PaymentStrategyMessages
{
    /// <summary>The mock gateway's reference for an order: stable across runs, greppable in the database.</summary>
    internal static string MockReference(string key, Guid orderId) =>
        string.Concat(key.ToUpperInvariant(), "-MOCK-", orderId.ToString("N"));

    /// <summary>BR13 refusal: the method belongs to the other customer group.</summary>
    internal static string MethodNotAvailableForActor(string key, CustomerType customerType) => string.Concat(
        "BR13: the ", key, " method is not offered to a ", customerType, " customer.");

    /// <summary>BR14 refusal: Cash on Delivery above the 1,000,000 VND cap.</summary>
    internal static string CashOnDeliveryAboveCap(long amount, long cap) => string.Concat(
        "BR14: Cash on Delivery is allowed only up to ",
        cap.ToString("N0", System.Globalization.CultureInfo.InvariantCulture),
        " VND; this order totals ",
        amount.ToString("N0", System.Globalization.CultureInfo.InvariantCulture),
        " VND. Please pay online.");

    /// <summary>A charge was attempted for a non-positive amount, which no gateway accepts.</summary>
    internal static string NonPositiveAmount(string key, long amount) => string.Concat(
        key, " cannot charge a non-positive amount (", amount, " VND).");
}
