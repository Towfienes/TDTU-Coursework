using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using SaigonBite.Web.Data.Entities;

namespace SaigonBite.Web.Data.Configurations;

/// <summary>Mapping for <see cref="Hub"/>: capacity check constraint and soft-delete filter (BR8, FR-B4).</summary>
public sealed class HubConfiguration : IEntityTypeConfiguration<Hub>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<Hub> builder)
    {
        builder.ToTable("Hubs");
        builder.HasKey(h => h.Id);

        builder.Property(h => h.Name).IsRequired().HasMaxLength(120);
        builder.Property(h => h.District).IsRequired().HasMaxLength(80);
        builder.Property(h => h.Address).IsRequired().HasMaxLength(200);
        builder.Property(h => h.KitchenCapacity).IsRequired();

        // FR-B1: the capacity is a whole number of concurrent orders and must be greater than zero,
        // otherwise BR8's division is undefined.
        builder.ToTable(t => t.HasCheckConstraint("CK_Hubs_KitchenCapacity", "[KitchenCapacity] > 0"));

        builder.HasQueryFilter(h => !h.IsDeleted);
    }
}

/// <summary>Mapping for <see cref="Brand"/> (FR-A1, FR-A4).</summary>
public sealed class BrandConfiguration : IEntityTypeConfiguration<Brand>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<Brand> builder)
    {
        builder.ToTable("Brands");
        builder.HasKey(b => b.Id);

        builder.Property(b => b.Name).IsRequired().HasMaxLength(120);
        builder.Property(b => b.Description).IsRequired().HasMaxLength(400);
        builder.HasIndex(b => b.Name).IsUnique();

        builder.HasQueryFilter(b => !b.IsDeleted);
    }
}

/// <summary>Mapping for the <see cref="HubBrand"/> operating link (BR12).</summary>
public sealed class HubBrandConfiguration : IEntityTypeConfiguration<HubBrand>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<HubBrand> builder)
    {
        builder.ToTable("HubBrands");
        builder.HasKey(hb => new { hb.HubId, hb.BrandId });

        builder.HasOne(hb => hb.Hub)
            .WithMany(h => h.HubBrands)
            .HasForeignKey(hb => hb.HubId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasOne(hb => hb.Brand)
            .WithMany(b => b.HubBrands)
            .HasForeignKey(hb => hb.BrandId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}

/// <summary>Mapping for <see cref="MenuItem"/>: availability, price and soft-delete filter (FR-A5, BR12).</summary>
public sealed class MenuItemConfiguration : IEntityTypeConfiguration<MenuItem>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<MenuItem> builder)
    {
        builder.ToTable("MenuItems");
        builder.HasKey(m => m.Id);

        builder.Property(m => m.Category).IsRequired().HasMaxLength(60);
        builder.Property(m => m.Name).IsRequired().HasMaxLength(120);
        builder.Property(m => m.Price).IsRequired();
        builder.Property(m => m.IsAvailable).IsRequired();

        builder.HasOne(m => m.Brand)
            .WithMany(b => b.MenuItems)
            .HasForeignKey(m => m.BrandId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasIndex(m => new { m.BrandId, m.Category });

        builder.HasQueryFilter(m => !m.IsDeleted);
    }
}
