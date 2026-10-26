using Microsoft.EntityFrameworkCore;
using SaigonBite.Web.Data.Entities;

namespace SaigonBite.Web.Data;

/// <summary>
/// The single EF Core Code-First context (CONTRACT.md). Owns the whole persistence model of the web
/// tier: catalogue, accounts, orders, audit rows and payment records.
/// </summary>
/// <remarks>
/// <para>
/// Two invariants are enforced here rather than in a controller (AGENTS.md hard rule 7):
/// soft-delete query filters keep deactivated rows out of the shopping and account screens while the
/// rows themselves survive for reports, and <see cref="SaveChanges(bool)"/> refuses any hard delete,
/// because orders and order lines are never deletable and everything else uses a flag.
/// </para>
/// <para>
/// Finance is stored as whole VND in <see cref="long"/> columns exactly as the pricing engine returns
/// it, so no conversion can introduce a rounding step that BR11 forbids.
/// </para>
/// </remarks>
public class SaigonBiteDbContext : DbContext
{
    /// <summary>Creates the context with the provider configured by <c>Program.cs</c>.</summary>
    public SaigonBiteDbContext(DbContextOptions<SaigonBiteDbContext> options) : base(options)
    {
    }

    /// <summary>Accounts of every role and both customer types (FR-E4).</summary>
    public DbSet<User> Users => Set<User>();

    /// <summary>Local Customer profile rows (BR18).</summary>
    public DbSet<LocalCustomerProfile> LocalCustomerProfiles => Set<LocalCustomerProfile>();

    /// <summary>Foreign Tourist profile rows (BR18).</summary>
    public DbSet<TouristProfile> TouristProfiles => Set<TouristProfile>();

    /// <summary>Cloud kitchens and their capacity (BR8, FR-B1).</summary>
    public DbSet<Hub> Hubs => Set<Hub>();

    /// <summary>Virtual brands (FR-A1).</summary>
    public DbSet<Brand> Brands => Set<Brand>();

    /// <summary>Hub–brand operating links (BR12).</summary>
    public DbSet<HubBrand> HubBrands => Set<HubBrand>();

    /// <summary>Menu items with their availability flag (FR-A5).</summary>
    public DbSet<MenuItem> MenuItems => Set<MenuItem>();

    /// <summary>Discount codes (FR-C1, BR9).</summary>
    public DbSet<Voucher> Vouchers => Set<Voucher>();

    /// <summary>Placed orders with the BR17 snapshot and BR10 breakdown.</summary>
    public DbSet<Order> Orders => Set<Order>();

    /// <summary>Order lines with their price snapshot.</summary>
    public DbSet<OrderLine> OrderLines => Set<OrderLine>();

    /// <summary>Audit trail of accepted and rejected transitions (FR-S5).</summary>
    public DbSet<OrderStatusHistory> OrderStatusHistories => Set<OrderStatusHistory>();

    /// <summary>Payment attempts and simulated refunds (FR-P3, Ambiguity A2).</summary>
    public DbSet<PaymentRecord> PaymentRecords => Set<PaymentRecord>();

    /// <summary>Platform settings, currently the heavy-rain flag (FR-S4).</summary>
    public DbSet<PlatformSetting> PlatformSettings => Set<PlatformSetting>();

    /// <inheritdoc />
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // One IEntityTypeConfiguration<T> per entity, discovered from this assembly.
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(SaigonBiteDbContext).Assembly);
    }

    /// <inheritdoc />
    public override int SaveChanges(bool acceptAllChangesOnSuccess)
    {
        GuardAgainstHardDeletes();
        return base.SaveChanges(acceptAllChangesOnSuccess);
    }

    /// <inheritdoc />
    public override Task<int> SaveChangesAsync(
        bool acceptAllChangesOnSuccess, CancellationToken cancellationToken = default)
    {
        GuardAgainstHardDeletes();
        return base.SaveChangesAsync(acceptAllChangesOnSuccess, cancellationToken);
    }

    /// <summary>
    /// Rejects any <see cref="EntityState.Deleted"/> entry. Orders and order lines are never deletable
    /// (CONTRACT.md), and every other order-referenced entity carries a soft-delete flag instead
    /// (FR-A4, FR-B4, FR-E4), so a hard delete is always a bug.
    /// </summary>
    private void GuardAgainstHardDeletes()
    {
        var offenders = ChangeTracker.Entries()
            .Where(e => e.State == EntityState.Deleted)
            // HubBrand is a pure operating link: it is not referenced by any order (order lines snapshot
            // the brand name), and re-linking a brand to fewer hubs legitimately removes rows.
            .Where(e => e.Entity is not HubBrand)
            .Select(e => e.Entity.GetType().Name)
            .Distinct()
            .ToList();

        if (offenders.Count > 0)
        {
            throw new InvalidOperationException(
                "Hard delete is not allowed by CONTRACT.md. Soft-delete the row instead, and keep "
                + "order lines by clearing OrderLine.IsRemoved rather than removing the row "
                + $"({string.Join(", ", offenders)}).");
        }
    }
}
