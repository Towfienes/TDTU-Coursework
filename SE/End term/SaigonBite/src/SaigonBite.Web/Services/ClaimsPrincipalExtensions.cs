using System.Security.Claims;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Web.Infrastructure;

namespace SaigonBite.Web.Services;

/// <summary>
/// Typed accessors for the claims written at sign-in. Controllers use these instead of parsing cookie
/// values by hand, which keeps the BR13/BR15 checks readable and consistent (FR-S2).
/// </summary>
public static class ClaimsPrincipalExtensions
{
    /// <summary>Claim type carrying the BR18 customer discriminator.</summary>
    public const string CustomerTypeClaim = "CustomerType";

    /// <summary>Claim type carrying the home hub of a Kitchen Staff account.</summary>
    public const string HubIdClaim = "HubId";

    /// <summary>Primary key of the signed-in account, or null.</summary>
    public static int? GetUserId(this ClaimsPrincipal principal) =>
        int.TryParse(principal.FindFirstValue(ClaimTypes.NameIdentifier), out var id) ? id : null;

    /// <summary>Role name of the signed-in account, or null.</summary>
    public static string? GetRole(this ClaimsPrincipal principal) =>
        principal.FindFirstValue(ClaimTypes.Role);

    /// <summary>BR18 discriminator of the signed-in customer, or null for staff accounts.</summary>
    public static CustomerType? GetCustomerType(this ClaimsPrincipal principal) =>
        int.TryParse(principal.FindFirstValue(CustomerTypeClaim), out var value)
            ? (CustomerType)value
            : null;

    /// <summary>Home hub of the signed-in Kitchen Staff account, or null.</summary>
    public static int? GetHubId(this ClaimsPrincipal principal) =>
        int.TryParse(principal.FindFirstValue(HubIdClaim), out var value) ? value : null;

    /// <summary>Display name for the navigation bar, falling back to the username.</summary>
    public static string GetDisplayName(this ClaimsPrincipal principal) =>
        principal.FindFirstValue(ClaimTypes.GivenName)
        ?? principal.Identity?.Name
        ?? string.Empty;

    /// <summary>Maps the signed-in role to the <see cref="ActorRole"/> the state machine expects (BR15).</summary>
    public static ActorRole GetActorRole(this ClaimsPrincipal principal) =>
        principal.GetRole() switch
        {
            Roles.Customer => ActorRole.Customer,
            Roles.KitchenStaff => ActorRole.KitchenStaff,
            Roles.Shipper => ActorRole.Shipper,
            Roles.Admin => ActorRole.Admin,
            _ => ActorRole.System,
        };
}
