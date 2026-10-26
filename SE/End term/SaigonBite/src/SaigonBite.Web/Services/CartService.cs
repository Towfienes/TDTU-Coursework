using System.Text.Json;
using Microsoft.AspNetCore.Http;

namespace SaigonBite.Web.Services;

/// <summary>One line of the session cart: menu item and quantity only, never a price.</summary>
public sealed class CartLine
{
    /// <summary>Identifier of the menu item.</summary>
    public int MenuItemId { get; set; }

    /// <summary>Quantity, constrained to 1..20 by BR12.</summary>
    public int Quantity { get; set; }
}

/// <summary>
/// The basket: at most one hub and up to 30 lines (BR12, FR-D1). Prices are deliberately absent — they
/// are read from the database at pricing time, so a customer cannot submit their own price.
/// </summary>
public sealed class CartState
{
    /// <summary>Hub the basket is bound to; null while empty.</summary>
    public int? HubId { get; set; }

    /// <summary>Lines of the basket.</summary>
    public List<CartLine> Lines { get; set; } = new();

    /// <summary>Simulated delivery distance in km, carried from the basket to checkout (BR2, BR3).</summary>
    public decimal DistanceKm { get; set; } = 3.2m;
}

/// <summary>
/// Session-backed basket. It only holds identifiers and quantities; every amount shown or charged comes
/// from <c>PricingEngine</c> through the order service (AGENTS.md hard rules 2 and 3).
/// </summary>
public interface ICartService
{
    /// <summary>Current basket, never null.</summary>
    CartState Get();

    /// <summary>Replaces the basket.</summary>
    void Save(CartState state);

    /// <summary>Empties the basket.</summary>
    void Clear();

    /// <summary>Total number of units in the basket, shown on the navigation bar.</summary>
    int TotalUnits();
}

/// <inheritdoc />
public sealed class CartService : ICartService
{
    /// <summary>Session key holding the serialized basket.</summary>
    public const string SessionKey = "SaigonBite.Cart";

    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web);

    private readonly ISession _session;

    /// <summary>Creates the service over the current HTTP session.</summary>
    /// <remarks>
    /// A basket only exists for a signed-in customer, and the controller reaches this service after the
    /// authorisation filter has run, so the session is always present here.
    /// </remarks>
    public CartService(IHttpContextAccessor accessor)
    {
        var context = accessor.HttpContext
            ?? throw new InvalidOperationException("No HTTP context is available for the current request.");
        _session = context.Session;
    }

    /// <inheritdoc />
    public CartState Get()
    {
        var json = _session.GetString(SessionKey);
        if (string.IsNullOrWhiteSpace(json))
        {
            return new CartState();
        }

        try
        {
            return JsonSerializer.Deserialize<CartState>(json, JsonOptions) ?? new CartState();
        }
        catch (JsonException)
        {
            // A stale or corrupted basket must never break navigation; start clean.
            return new CartState();
        }
    }

    /// <inheritdoc />
    public void Save(CartState state) =>
        _session.SetString(SessionKey, JsonSerializer.Serialize(state, JsonOptions));

    /// <inheritdoc />
    public void Clear() => _session.Remove(SessionKey);

    /// <inheritdoc />
    public int TotalUnits() => Get().Lines.Sum(l => l.Quantity);
}
