using Microsoft.EntityFrameworkCore;
using System.Security.Claims;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Identity;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;

namespace SaigonBite.Web.Services;

/// <summary>Outcome of a registration attempt, carrying the message to render.</summary>
public sealed record RegistrationResult(bool Success, int? UserId, string? Error)
{
    /// <summary>Refusal with a reason (BR18 validation, duplicate identifier).</summary>
    public static RegistrationResult Refused(string error) => new(false, null, error);
}

/// <summary>A registration waiting for its simulated OTP or email code (FR-E1, FR-E2).</summary>
public sealed class RegistrationTicket
{
    /// <summary>Sign-in identifier being claimed.</summary>
    public string Username { get; set; } = string.Empty;

    /// <summary>Already-hashed password; the plaintext is never kept.</summary>
    public string PasswordHash { get; set; } = string.Empty;

    /// <summary>Display name.</summary>
    public string DisplayName { get; set; } = string.Empty;

    /// <summary>BR18 mobile number for a Local Customer.</summary>
    public string? Mobile { get; set; }

    /// <summary>BR18 passport number for a Foreign Tourist.</summary>
    public string? PassportNumber { get; set; }

    /// <summary>Nationality for a Foreign Tourist.</summary>
    public string? Nationality { get; set; }

    /// <summary>Email for a Foreign Tourist.</summary>
    public string? Email { get; set; }

    /// <summary>Simulated verification code; shown in the development UI only.</summary>
    public string Code { get; set; } = string.Empty;
}

/// <summary>
/// Registration and sign-in plumbing for both customer types (FR-E1, FR-E2, FR-E3, BR18).
/// </summary>
/// <remarks>
/// Validation lives here, not in the view: BR18 defines the mobile prefix and length, the passport
/// pattern, the email requirement, the eight-character minimum and the uniqueness of the identifier.
/// Passwords are stored through <see cref="PasswordHasher{TUser}"/> (NFR4) — <see cref="User.PasswordHash"/>
/// is never assigned a plaintext value anywhere in this project.
/// </remarks>
public interface IAccountService
{
    /// <summary>Validates a BR18 Local Customer registration and issues a simulated OTP ticket.</summary>
    Task<(RegistrationResult Result, RegistrationTicket? Ticket)> StartLocalRegistrationAsync(
        string mobile, string password, string displayName, CancellationToken cancellationToken = default);

    /// <summary>Validates a BR18 Foreign Tourist registration and issues a simulated email code.</summary>
    Task<(RegistrationResult Result, RegistrationTicket? Ticket)> StartTouristRegistrationAsync(
        string email, string passportNumber, string nationality, string password, string displayName,
        CancellationToken cancellationToken = default);

    /// <summary>Completes a pending ticket when the code matches, creating the account.</summary>
    Task<RegistrationResult> CompleteRegistrationAsync(
        RegistrationTicket ticket, CustomerType customerType, string submittedCode,
        CancellationToken cancellationToken = default);

    /// <summary>Verifies a username/password pair and returns the account, or null.</summary>
    Task<User?> ValidateCredentialsAsync(
        string username, string password, CancellationToken cancellationToken = default);

    /// <summary>Builds the cookie claims for a verified account.</summary>
    ClaimsPrincipal BuildPrincipal(User user);
}

/// <inheritdoc />
public sealed class AccountService : IAccountService
{
    private static readonly Regex VietnameseMobile = new(@"^0(3|5|7|8|9)\d{8}$", RegexOptions.Compiled);
    private static readonly Regex PassportNumber = new(@"^[A-Za-z0-9]{6,9}$", RegexOptions.Compiled);
    private static readonly Regex EmailAddress = new(@"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$", RegexOptions.Compiled);

    private readonly SaigonBiteDbContext _db;
    private readonly IPasswordHasher<User> _hasher;

    /// <summary>Creates the service.</summary>
    public AccountService(SaigonBiteDbContext db, IPasswordHasher<User> hasher)
    {
        _db = db;
        _hasher = hasher;
    }

    /// <inheritdoc />
    public async Task<(RegistrationResult Result, RegistrationTicket? Ticket)> StartLocalRegistrationAsync(
        string mobile, string password, string displayName, CancellationToken cancellationToken = default)
    {
        var normalised = (mobile ?? string.Empty).Trim();

        // BR18: exactly ten digits starting 03, 05, 07, 08 or 09.
        if (!VietnameseMobile.IsMatch(normalised))
        {
            return (RegistrationResult.Refused(
                "BR18: a Vietnamese mobile number has 10 digits and starts with 03, 05, 07, 08 or 09."), null);
        }

        var passwordError = ValidatePassword(password);
        if (passwordError is not null)
        {
            return (RegistrationResult.Refused(passwordError), null);
        }

        if (await _db.Users.IgnoreQueryFilters().AnyAsync(u => u.Username == normalised, cancellationToken))
        {
            return (RegistrationResult.Refused("BR18: that mobile number is already registered."), null);
        }

        var ticket = new RegistrationTicket
        {
            Username = normalised,
            Mobile = normalised,
            DisplayName = string.IsNullOrWhiteSpace(displayName) ? normalised : displayName.Trim(),
            Code = GenerateCode(),
            PasswordHash = string.Empty,
        };

        // Hash against the final entity shape so verification does not need the plaintext.
        ticket.PasswordHash = _hasher.HashPassword(new User { Username = normalised }, password);
        return (new RegistrationResult(true, null, null), ticket);
    }

    /// <inheritdoc />
    public async Task<(RegistrationResult Result, RegistrationTicket? Ticket)> StartTouristRegistrationAsync(
        string email, string passportNumber, string nationality, string password, string displayName,
        CancellationToken cancellationToken = default)
    {
        var mail = (email ?? string.Empty).Trim();
        var passport = (passportNumber ?? string.Empty).Trim();
        var country = (nationality ?? string.Empty).Trim();

        if (!EmailAddress.IsMatch(mail))
        {
            return (RegistrationResult.Refused("BR18: a valid email address is required."), null);
        }

        // BR18: six to nine letters or digits.
        if (!PassportNumber.IsMatch(passport))
        {
            return (RegistrationResult.Refused(
                "BR18: a passport number has 6 to 9 letters or digits."), null);
        }

        if (country.Length < 2)
        {
            return (RegistrationResult.Refused("BR18: a nationality is required."), null);
        }

        var passwordError = ValidatePassword(password);
        if (passwordError is not null)
        {
            return (RegistrationResult.Refused(passwordError), null);
        }

        if (await _db.Users.IgnoreQueryFilters().AnyAsync(u => u.Username == mail, cancellationToken))
        {
            return (RegistrationResult.Refused("BR18: that email address is already registered."), null);
        }

        if (await _db.TouristProfiles.AnyAsync(p => p.PassportNumber == passport, cancellationToken))
        {
            return (RegistrationResult.Refused("BR18: that passport number is already registered."), null);
        }

        var ticket = new RegistrationTicket
        {
            Username = mail,
            Email = mail,
            PassportNumber = passport,
            Nationality = country,
            DisplayName = string.IsNullOrWhiteSpace(displayName) ? mail : displayName.Trim(),
            Code = GenerateCode(),
            PasswordHash = string.Empty,
        };

        ticket.PasswordHash = _hasher.HashPassword(new User { Username = mail }, password);
        return (new RegistrationResult(true, null, null), ticket);
    }

    /// <inheritdoc />
    public async Task<RegistrationResult> CompleteRegistrationAsync(
        RegistrationTicket ticket, CustomerType customerType, string submittedCode,
        CancellationToken cancellationToken = default)
    {
        if (!string.Equals(ticket.Code, (submittedCode ?? string.Empty).Trim(), StringComparison.Ordinal))
        {
            return RegistrationResult.Refused("The verification code does not match.");
        }

        var user = new User
        {
            Username = ticket.Username,
            PasswordHash = ticket.PasswordHash,
            Role = Roles.Customer,
            CustomerType = customerType,
            DisplayName = ticket.DisplayName,
            CreatedAt = VietnamTime.Now,
        };

        if (customerType == CustomerType.Local && ticket.Mobile is not null)
        {
            user.LocalProfile = new LocalCustomerProfile { Mobile = ticket.Mobile };
        }
        else if (customerType == CustomerType.Tourist && ticket.PassportNumber is not null)
        {
            user.TouristProfile = new TouristProfile
            {
                PassportNumber = ticket.PassportNumber,
                Nationality = ticket.Nationality ?? string.Empty,
                Email = ticket.Email ?? ticket.Username,
            };
        }

        _db.Users.Add(user);
        await _db.SaveChangesAsync(cancellationToken);

        return new RegistrationResult(true, user.Id, null);
    }

    /// <inheritdoc />
    public async Task<User?> ValidateCredentialsAsync(
        string username, string password, CancellationToken cancellationToken = default)
    {
        var normalised = (username ?? string.Empty).Trim();
        if (normalised.Length == 0 || string.IsNullOrEmpty(password))
        {
            return null;
        }

        var user = await _db.Users
            .AsNoTracking()
            .FirstOrDefaultAsync(u => u.Username == normalised, cancellationToken);

        if (user is null)
        {
            return null;
        }

        var attempt = _hasher.VerifyHashedPassword(user, user.PasswordHash, password);
        return attempt == PasswordVerificationResult.Failed ? null : user;
    }

    /// <inheritdoc />
    public ClaimsPrincipal BuildPrincipal(User user)
    {
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new(ClaimTypes.Name, user.Username),
            new(ClaimTypes.GivenName, user.DisplayName),
            new(ClaimTypes.Role, user.Role),
        };

        if (user.CustomerType is not null)
        {
            claims.Add(new Claim(
                ClaimsPrincipalExtensions.CustomerTypeClaim, ((int)user.CustomerType.Value).ToString()));
        }

        if (user.HubId is not null)
        {
            claims.Add(new Claim(ClaimsPrincipalExtensions.HubIdClaim, user.HubId.Value.ToString()));
        }

        var identity = new ClaimsIdentity(claims, "SaigonBiteCookie");
        return new ClaimsPrincipal(identity);
    }

    private static string? ValidatePassword(string password)
    {
        // BR18: at least eight characters, stored hashed (NFR4).
        if (string.IsNullOrWhiteSpace(password) || password.Length < 8)
        {
            return "BR18: the password must be at least 8 characters long.";
        }

        return null;
    }

    private static string GenerateCode() =>
        System.Security.Cryptography.RandomNumberGenerator.GetInt32(100000, 999999).ToString();

    /// <summary>Session key for a pending Local Customer registration.</summary>
    public const string LocalTicketKey = "SaigonBite.Registration.Local";

    /// <summary>Session key for a pending Foreign Tourist registration.</summary>
    public const string TouristTicketKey = "SaigonBite.Registration.Tourist";

    /// <summary>Serializes a pending ticket for the session.</summary>
    public static string Serialize(RegistrationTicket ticket) =>
        JsonSerializer.Serialize(ticket, new JsonSerializerOptions(JsonSerializerDefaults.Web));

    /// <summary>Reads a pending ticket from the session.</summary>
    public static RegistrationTicket? Deserialize(string? json) =>
        string.IsNullOrWhiteSpace(json)
            ? null
            : JsonSerializer.Deserialize<RegistrationTicket>(
                json, new JsonSerializerOptions(JsonSerializerDefaults.Web));
}
