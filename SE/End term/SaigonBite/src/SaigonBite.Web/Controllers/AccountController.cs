using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Localization;
using Microsoft.AspNetCore.Mvc;
using SaigonBite.Core.Orders;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.Services;
using SaigonBite.Web.ViewModels;

namespace SaigonBite.Web.Controllers;

/// <summary>
/// Registration and sign-in for both customer types, plus the EN/VI language toggle (FR-E1, FR-E2,
/// FR-S1, BR18).
/// </summary>
/// <remarks>
/// Registration is two steps because the specification asks for a simulated OTP (Local Customer) and a
/// simulated email code (Foreign Tourist). The pending ticket lives in the session with the password
/// already hashed, so the plaintext never leaves the POST that read it.
/// </remarks>
public class AccountController : Controller
{
    private readonly IAccountService _accounts;
    private readonly ILogger<AccountController> _logger;

    /// <summary>Creates the controller.</summary>
    public AccountController(IAccountService accounts, ILogger<AccountController> logger)
    {
        _accounts = accounts;
        _logger = logger;
    }

    /// <summary>Sign-in form.</summary>
    [AllowAnonymous]
    [HttpGet("/account/login")]
    public IActionResult Login(string? returnUrl = null) =>
        View(new LoginVm { ReturnUrl = returnUrl });

    /// <summary>Verifies credentials and issues the cookie (NFR4).</summary>
    [AllowAnonymous]
    [HttpPost("/account/login")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Login(LoginVm model, CancellationToken cancellationToken)
    {
        var user = await _accounts.ValidateCredentialsAsync(model.Username, model.Password, cancellationToken);
        if (user is null)
        {
            _logger.LogWarning("Failed sign-in attempt for {Username}.", model.Username);
            ModelState.AddModelError(string.Empty, "Invalid username or password.");
            return View(model);
        }

        await HttpContext.SignInAsync(
            CookieAuthenticationDefaults.AuthenticationScheme,
            _accounts.BuildPrincipal(user),
            new AuthenticationProperties { IsPersistent = true });

        if (!string.IsNullOrWhiteSpace(model.ReturnUrl) && Url.IsLocalUrl(model.ReturnUrl))
        {
            return LocalRedirect(model.ReturnUrl);
        }

        return RedirectToRoleHome(user.Role);
    }

    /// <summary>Clears the authentication cookie.</summary>
    [Authorize]
    [HttpPost("/account/logout")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Logout()
    {
        await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
        HttpContext.Session.Clear();
        return RedirectToAction(nameof(HomeController.Index), "Home");
    }

    /// <summary>Shown when an authenticated actor reaches a function outside their role (FR-S2).</summary>
    [AllowAnonymous]
    [HttpGet("/account/denied")]
    public IActionResult Denied() => View();

    /// <summary>Local Customer registration form (FR-E1).</summary>
    [AllowAnonymous]
    [HttpGet("/account/register/local")]
    public IActionResult RegisterLocal() => View(new RegisterLocalVm());

    /// <summary>Validates the BR18 rules and issues a simulated OTP.</summary>
    [AllowAnonymous]
    [HttpPost("/account/register/local")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> RegisterLocal(RegisterLocalVm model, CancellationToken cancellationToken)
    {
        if (!string.Equals(model.Password, model.ConfirmPassword, StringComparison.Ordinal))
        {
            ModelState.AddModelError(nameof(model.ConfirmPassword), "The two passwords do not match.");
            return View(model);
        }

        var (result, ticket) = await _accounts.StartLocalRegistrationAsync(
            model.Mobile, model.Password, model.DisplayName, cancellationToken);

        if (!result.Success || ticket is null)
        {
            ModelState.AddModelError(string.Empty, result.Error ?? "Registration was refused.");
            return View(model);
        }

        HttpContext.Session.SetString(AccountService.LocalTicketKey, AccountService.Serialize(ticket));
        TempData["DevCode"] = ticket.Code;
        TempData["Mobile"] = ticket.Username;
        return RedirectToAction(nameof(VerifyLocal));
    }

    /// <summary>OTP step for a Local Customer (FR-E1).</summary>
    [AllowAnonymous]
    [HttpGet("/account/register/local/verify")]
    public IActionResult VerifyLocal()
    {
        var ticket = AccountService.Deserialize(HttpContext.Session.GetString(AccountService.LocalTicketKey));
        if (ticket is null)
        {
            return RedirectToAction(nameof(RegisterLocal));
        }

        ViewData["Mobile"] = ticket.Username;
        return View(new VerifyCodeVm());
    }

    /// <summary>Completes Local Customer registration when the OTP matches.</summary>
    [AllowAnonymous]
    [HttpPost("/account/register/local/verify")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> VerifyLocal(VerifyCodeVm model, CancellationToken cancellationToken)
    {
        var ticket = AccountService.Deserialize(HttpContext.Session.GetString(AccountService.LocalTicketKey));
        if (ticket is null)
        {
            return RedirectToAction(nameof(RegisterLocal));
        }

        var result = await _accounts.CompleteRegistrationAsync(
            ticket, CustomerType.Local, model.Code, cancellationToken);

        if (!result.Success)
        {
            ModelState.AddModelError(string.Empty, result.Error ?? "The code was refused.");
            ViewData["Mobile"] = ticket.Username;
            return View(model);
        }

        HttpContext.Session.Remove(AccountService.LocalTicketKey);
        TempData["Registered"] = ticket.Username;
        return RedirectToAction(nameof(Login));
    }

    /// <summary>Foreign Tourist registration form (FR-E2).</summary>
    [AllowAnonymous]
    [HttpGet("/account/register/tourist")]
    public IActionResult RegisterTourist() => View(new RegisterTouristVm());

    /// <summary>Validates the BR18 rules and issues a simulated email code.</summary>
    [AllowAnonymous]
    [HttpPost("/account/register/tourist")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> RegisterTourist(
        RegisterTouristVm model, CancellationToken cancellationToken)
    {
        if (!string.Equals(model.Password, model.ConfirmPassword, StringComparison.Ordinal))
        {
            ModelState.AddModelError(nameof(model.ConfirmPassword), "The two passwords do not match.");
            return View(model);
        }

        var (result, ticket) = await _accounts.StartTouristRegistrationAsync(
            model.Email, model.PassportNumber, model.Nationality, model.Password, model.DisplayName,
            cancellationToken);

        if (!result.Success || ticket is null)
        {
            ModelState.AddModelError(string.Empty, result.Error ?? "Registration was refused.");
            return View(model);
        }

        HttpContext.Session.SetString(AccountService.TouristTicketKey, AccountService.Serialize(ticket));
        TempData["DevCode"] = ticket.Code;
        TempData["Email"] = ticket.Username;
        return RedirectToAction(nameof(VerifyTourist));
    }

    /// <summary>Email-code step for a Foreign Tourist (FR-E2).</summary>
    [AllowAnonymous]
    [HttpGet("/account/register/tourist/verify")]
    public IActionResult VerifyTourist()
    {
        var ticket = AccountService.Deserialize(HttpContext.Session.GetString(AccountService.TouristTicketKey));
        if (ticket is null)
        {
            return RedirectToAction(nameof(RegisterTourist));
        }

        ViewData["Email"] = ticket.Username;
        return View(new VerifyCodeVm());
    }

    /// <summary>Completes Foreign Tourist registration when the email code matches.</summary>
    [AllowAnonymous]
    [HttpPost("/account/register/tourist/verify")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> VerifyTourist(VerifyCodeVm model, CancellationToken cancellationToken)
    {
        var ticket = AccountService.Deserialize(HttpContext.Session.GetString(AccountService.TouristTicketKey));
        if (ticket is null)
        {
            return RedirectToAction(nameof(RegisterTourist));
        }

        var result = await _accounts.CompleteRegistrationAsync(
            ticket, CustomerType.Tourist, model.Code, cancellationToken);

        if (!result.Success)
        {
            ModelState.AddModelError(string.Empty, result.Error ?? "The code was refused.");
            ViewData["Email"] = ticket.Username;
            return View(model);
        }

        HttpContext.Session.Remove(AccountService.TouristTicketKey);
        TempData["Registered"] = ticket.Username;
        return RedirectToAction(nameof(Login));
    }

    /// <summary>
    /// Writes the culture cookie behind the visible EN/VI toggle (FR-S1, NFR3). The cookie is the standard
    /// ASP.NET Core culture cookie, so the request-localisation middleware picks it up on the next request.
    /// </summary>
    [AllowAnonymous]
    [HttpGet("/account/language")]
    public IActionResult Language(string culture, string? returnUrl)
    {
        var chosen = string.Equals(culture, "vi", StringComparison.OrdinalIgnoreCase) ? "vi" : "en";

        Response.Cookies.Append(
            CookieRequestCultureProvider.DefaultCookieName,
            CookieRequestCultureProvider.MakeCookieValue(new RequestCulture(chosen)),
            new CookieOptions
            {
                Expires = DateTimeOffset.UtcNow.AddYears(1),
                IsEssential = true,
                HttpOnly = false,
                SameSite = SameSiteMode.Lax,
            });

        return Url.IsLocalUrl(returnUrl ?? string.Empty)
            ? LocalRedirect(returnUrl!)
            : RedirectToAction(nameof(HomeController.Index), "Home");
    }

    private IActionResult RedirectToRoleHome(string role) => role switch
    {
        Roles.Admin => RedirectToAction("Index", "Admin"),
        Roles.KitchenStaff => RedirectToAction("Index", "Deliveries"),
        Roles.Shipper => RedirectToAction("Index", "Deliveries"),
        _ => RedirectToAction("Index", "Brands"),
    };
}
