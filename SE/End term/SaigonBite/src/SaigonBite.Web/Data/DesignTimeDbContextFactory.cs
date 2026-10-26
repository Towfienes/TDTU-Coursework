using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace SaigonBite.Web.Data;

/// <summary>
/// Design-time factory used only by <c>dotnet ef</c>. Keeping it here means the migration tools never have
/// to boot the web application, never need a live database and never read a real connection string.
/// </summary>
/// <remarks>
/// <para>
/// The migration set under <c>Data/Migrations</c> is generated for the SQL Server provider, which is the
/// Tier 3 target (CONTRACT.md). Running the application with <c>USE_SQLITE=1</c> uses
/// <c>Database.EnsureCreated()</c> instead, because provider-specific DDL cannot be replayed on SQLite.
/// </para>
/// <para>
/// Generate a fresh migration from the repository root with:
/// </para>
/// <code>
/// dotnet ef migrations add &lt;Name&gt; --project src/SaigonBite.Web --startup-project src/SaigonBite.Web --output-dir Data/Migrations
/// </code>
/// </remarks>
public sealed class DesignTimeDbContextFactory : IDesignTimeDbContextFactory<SaigonBiteDbContext>
{
    /// <summary>Placeholder used only to let the design-time tool build the model; no connection is opened.</summary>
    private const string DesignTimeSqlServer =
        "Server=(localdb)\\design-time;Database=SaigonBiteDesign;Trusted_Connection=True;TrustServerCertificate=True";

    /// <inheritdoc />
    public SaigonBiteDbContext CreateDbContext(string[] args)
    {
        var options = new DbContextOptionsBuilder<SaigonBiteDbContext>();

        if (string.Equals(Environment.GetEnvironmentVariable("USE_SQLITE"), "1", StringComparison.Ordinal))
        {
            options.UseSqlite("Data Source=App_Data/design-time.db");
        }
        else
        {
            var connectionString =
                Environment.GetEnvironmentVariable("ConnectionStrings__Default") ?? DesignTimeSqlServer;
            options.UseSqlServer(connectionString);
        }

        return new SaigonBiteDbContext(options.Options);
    }
}
