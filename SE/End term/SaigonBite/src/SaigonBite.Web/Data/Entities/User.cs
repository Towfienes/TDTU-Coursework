using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Web.Infrastructure;

namespace SaigonBite.Web.Data.Entities;

/// <summary>
/// One row per person: the two customer types plus kitchen staff, shippers and administrators.
/// </summary>
/// <remarks>
/// FR-E4 / BR18 require Local Customers and Foreign Tourists to live in one schema with a
/// discriminator. <see cref="CustomerType"/> is that discriminator (null for staff roles), and the
/// type-specific attributes hang off <see cref="LocalProfile"/> and <see cref="TouristProfile"/> so the
/// generalization is visible in the database as well as in the class diagram.
/// </remarks>
public class User
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>
    /// Unique sign-in identifier (FR-E3): the Vietnamese mobile number for a Local Customer, the email
    /// address for a Foreign Tourist, a short handle for staff and administrator accounts.
    /// </summary>
    public string Username { get; set; } = string.Empty;

    /// <summary>Hash produced by the ASP.NET Core password hasher — never the plaintext (NFR4).</summary>
    public string PasswordHash { get; set; } = string.Empty;

    /// <summary>One of <see cref="Roles"/>; drives the server-side role policies (FR-S2, NFR4).</summary>
    public string Role { get; set; } = Roles.Customer;

    /// <summary>BR18 discriminator: <c>Local</c>, <c>Tourist</c>, or null for staff accounts.</summary>
    public CustomerType? CustomerType { get; set; }

    /// <summary>Home hub of a Kitchen Staff account (BR15: the actor must belong to the order's hub).</summary>
    public int? HubId { get; set; }

    /// <summary>Navigation for <see cref="HubId"/>.</summary>
    public Hub? Hub { get; set; }

    /// <summary>Friendly name shown in the interface; never used as an identifier.</summary>
    public string DisplayName { get; set; } = string.Empty;

    /// <summary>Soft-delete flag (FR-E4 "deactivate"; never a hard delete of an account).</summary>
    public bool IsDeleted { get; set; }

    /// <summary>Vietnam local creation timestamp (UTC+7).</summary>
    public DateTime CreatedAt { get; set; }

    /// <summary>Local Customer profile: mobile number (BR18).</summary>
    public LocalCustomerProfile? LocalProfile { get; set; }

    /// <summary>Foreign Tourist profile: passport, nationality, email (BR18).</summary>
    public TouristProfile? TouristProfile { get; set; }
}

/// <summary>Attributes that only a Local Customer carries (FR-E1, BR18).</summary>
public class LocalCustomerProfile
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Owner of the profile.</summary>
    public int UserId { get; set; }

    /// <summary>Navigation for <see cref="UserId"/>.</summary>
    public User? User { get; set; }

    /// <summary>Ten digits starting 03, 05, 07, 08 or 09 (BR18).</summary>
    public string Mobile { get; set; } = string.Empty;
}

/// <summary>Attributes that only a Foreign Tourist carries (FR-E2, BR18).</summary>
public class TouristProfile
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Owner of the profile.</summary>
    public int UserId { get; set; }

    /// <summary>Navigation for <see cref="UserId"/>.</summary>
    public User? User { get; set; }

    /// <summary>Six to nine letters or digits (BR18).</summary>
    public string PassportNumber { get; set; } = string.Empty;

    /// <summary>Country of citizenship, free text.</summary>
    public string Nationality { get; set; } = string.Empty;

    /// <summary>Verified email address; the simulated email code is sent here (FR-E2).</summary>
    public string Email { get; set; } = string.Empty;
}
