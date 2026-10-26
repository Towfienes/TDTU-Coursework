using System.Globalization;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Localization;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Payments;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Data.Seeding;
using SaigonBite.Web.Infrastructure;
using SaigonBite.Web.Services;
using SaigonBite.Web.Services.Payments;

var builder = WebApplication.CreateBuilder(args);

// ---------------------------------------------------------------------------------------------------
// Data tier: SQL Server by default, SQLite when USE_SQLITE=1 (CONTRACT.md, Tier 3 Code-First).
// ---------------------------------------------------------------------------------------------------
var useSqlite = string.Equals(
                     Environment.GetEnvironmentVariable("USE_SQLITE"), "1", StringComparison.Ordinal)
                 || builder.Configuration.GetValue("UseSqlite", false);

builder.Services.AddDbContext<SaigonBiteDbContext>(options =>
{
    if (useSqlite)
    {
        var path = builder.Configuration["SqlitePath"] ?? "App_Data/saigonbite.dev.db";
        var full = Path.GetFullPath(path);
        Directory.CreateDirectory(Path.GetDirectoryName(full)!);
        options.UseSqlite($"Data Source={full}");
        return;
    }

    var connectionString = builder.Configuration.GetConnectionString("Default");
    if (string.IsNullOrWhiteSpace(connectionString))
    {
        throw new InvalidOperationException(
            "ConnectionStrings:Default is required for SQL Server. Set it in appsettings.json, in "
            + "user-secrets, or in the ConnectionStrings__Default environment variable, or run with "
            + "USE_SQLITE=1 for the SQLite development database.");
    }

    options.UseSqlServer(connectionString, sql => sql.EnableRetryOnFailure());
});

// ---------------------------------------------------------------------------------------------------
// Business services. All pricing, state and payment decisions come from SaigonBite.Core (AGENTS.md
// hard rules 2, 3 and 4); these registrations only orchestrate them.
// ---------------------------------------------------------------------------------------------------
builder.Services.AddHttpContextAccessor();
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromHours(4);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
    options.Cookie.Name = ".SaigonBite.Session";
});

builder.Services.AddScoped<IPasswordHasher<User>, PasswordHasher<User>>();
builder.Services.AddScoped<IAccountService, AccountService>();
builder.Services.AddScoped<IHubLoadService, HubLoadService>();
builder.Services.AddScoped<IPlatformSettingsService, PlatformSettingsService>();
builder.Services.AddScoped<IPricingService, PricingService>();
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddScoped<IReportService, ReportService>();
builder.Services.AddScoped<ICartService, CartService>();

// One registration line adds every IPaymentStrategy Core ships, plus IPaymentStrategyResolver (BR13,
// NFR2). A new payment method therefore needs no edit here.
builder.Services.AddCorePaymentStrategies();
builder.Services.AddHttpClient();

// ---------------------------------------------------------------------------------------------------
// Cookie authentication and the four role policies (FR-S2, NFR4). Roles are enforced on the server.
// ---------------------------------------------------------------------------------------------------
builder.Services
    .AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(options =>
    {
        options.LoginPath = "/account/login";
        options.LogoutPath = "/account/logout";
        options.AccessDeniedPath = "/account/denied";
        options.ExpireTimeSpan = TimeSpan.FromHours(8);
        options.SlidingExpiration = true;
        options.Cookie.Name = ".SaigonBite.Auth";
        options.Cookie.HttpOnly = true;
        options.Cookie.SameSite = SameSiteMode.Lax;
        options.Cookie.SecurePolicy = CookieSecurePolicy.SameAsRequest;

        // An authenticated actor who reaches another role's function gets a plain 403 instead of a redirect,
        // so the refusal is visible to tests and to NFR4 verification. Anonymous visitors still go to the
        // sign-in page, which is the friendlier browser behaviour.
        options.Events.OnRedirectToAccessDenied = context =>
        {
            context.Response.StatusCode = StatusCodes.Status403Forbidden;
            return Task.CompletedTask;
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy(Policies.Customer, policy => policy.RequireRole(Roles.Customer));
    options.AddPolicy(Policies.KitchenStaff, policy => policy.RequireRole(Roles.KitchenStaff));
    options.AddPolicy(Policies.Shipper, policy => policy.RequireRole(Roles.Shipper));
    options.AddPolicy(Policies.Admin, policy => policy.RequireRole(Roles.Admin));
    options.AddPolicy(
        Policies.Kitchen, policy => policy.RequireRole(Roles.KitchenStaff, Roles.Admin));
    options.AddPolicy(
        Policies.Delivery,
        policy => policy.RequireRole(Roles.Shipper, Roles.KitchenStaff, Roles.Admin));
});

// ---------------------------------------------------------------------------------------------------
// Localisation: English and Vietnamese resources, switched by query string or the language cookie
// that the EN/VI toggle writes (FR-S1, NFR3).
// ---------------------------------------------------------------------------------------------------
// The marker type SaigonBite.Web.SharedResource sits beside Resources/SharedResource.resx, so the
// resource base name is the type's full name; no ResourcesPath prefix is added here.
builder.Services.AddLocalization();
builder.Services.AddControllersWithViews();

builder.Services.Configure<RequestLocalizationOptions>(options =>
{
    var supported = new[] { new CultureInfo("en"), new CultureInfo("vi") };
    options.DefaultRequestCulture = new RequestCulture("en");
    options.SupportedCultures = supported;
    options.SupportedUICultures = supported;
    options.RequestCultureProviders = new List<IRequestCultureProvider>
    {
        new QueryStringRequestCultureProvider(),
        new CookieRequestCultureProvider(),
        new AcceptLanguageHeaderRequestCultureProvider(),
    };
});

var app = builder.Build();

// ---------------------------------------------------------------------------------------------------
// Pipeline.
// ---------------------------------------------------------------------------------------------------
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/home/error");
    app.UseHsts();
}

app.UseStatusCodePagesWithReExecute("/home/status/{0}");

app.Use(async (context, next) =>
{
    // Baseline hardening headers for a server-rendered application (NFR4).
    context.Response.Headers["X-Content-Type-Options"] = "nosniff";
    context.Response.Headers["X-Frame-Options"] = "DENY";
    context.Response.Headers["Referrer-Policy"] = "same-origin";
    await next();
});

app.UseStaticFiles();
app.UseRouting();
app.UseRequestLocalization();
app.UseSession();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.MapGet("/health", () => Results.Ok(new
{
    status = "ok",
    database = useSqlite ? "sqlite" : "sqlserver",
    culture = CultureInfo.CurrentUICulture.Name,
}));

// ---------------------------------------------------------------------------------------------------
// Database creation and development seed data (CONTRACT.md seed requirement).
// ---------------------------------------------------------------------------------------------------
using (var scope = app.Services.CreateScope())
{
    var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
    var db = scope.ServiceProvider.GetRequiredService<SaigonBiteDbContext>();

    if (useSqlite)
    {
        // SQLite development path: EnsureCreated, because the migration set is generated for SQL Server
        // and provider-specific DDL cannot be replayed on SQLite. See Data/Migrations/README.md.
        await db.Database.EnsureCreatedAsync();
    }
    else
    {
        await db.Database.MigrateAsync();
    }

    if (app.Environment.IsDevelopment())
    {
        await DbSeeder.SeedAsync(scope.ServiceProvider);
        logger.LogInformation("Development seed data ensured.");
    }
}

var strategies = PaymentStrategyRegistration.Describe(app.Services);
app.Logger.LogInformation(
    "Registered {Count} payment strategies (BR13): {Strategies}",
    strategies.Count,
    string.Join(", ", strategies));
app.Logger.LogInformation(
    "SaigonBite started. Database provider: {Provider}. Environment: {Environment}.",
    useSqlite ? "SQLite" : "SQL Server",
    app.Environment.EnvironmentName);

app.Run();
