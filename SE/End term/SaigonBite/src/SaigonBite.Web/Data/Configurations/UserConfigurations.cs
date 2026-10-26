using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;

namespace SaigonBite.Web.Data.Configurations;

/// <summary>
/// Mapping for <see cref="User"/>, including the FR-E4 discriminator and the soft-delete filter.
/// </summary>
public sealed class UserConfiguration : IEntityTypeConfiguration<User>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("Users");
        builder.HasKey(u => u.Id);

        builder.Property(u => u.Username).IsRequired().HasMaxLength(100);
        builder.HasIndex(u => u.Username).IsUnique();

        builder.Property(u => u.PasswordHash).IsRequired().HasMaxLength(256);
        builder.Property(u => u.Role).IsRequired().HasMaxLength(30);
        builder.Property(u => u.DisplayName).IsRequired().HasMaxLength(120);
        builder.Property(u => u.CreatedAt).IsRequired();

        // FR-E4 / BR18: one table, discriminator column, null for staff accounts.
        builder.Property(u => u.CustomerType).HasConversion<string>().HasMaxLength(20);

        builder.HasOne(u => u.Hub)
            .WithMany()
            .HasForeignKey(u => u.HubId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne(u => u.LocalProfile)
            .WithOne(p => p!.User)
            .HasForeignKey<LocalCustomerProfile>(p => p.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasOne(u => u.TouristProfile)
            .WithOne(p => p!.User)
            .HasForeignKey<TouristProfile>(p => p.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        // Soft-delete filter (FR-E4 "deactivate", CONTRACT.md).
        builder.HasQueryFilter(u => !u.IsDeleted);
    }
}

/// <summary>Mapping for <see cref="LocalCustomerProfile"/> (BR18 mobile number).</summary>
public sealed class LocalCustomerProfileConfiguration : IEntityTypeConfiguration<LocalCustomerProfile>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<LocalCustomerProfile> builder)
    {
        builder.ToTable("LocalCustomerProfiles");
        builder.HasKey(p => p.Id);
        builder.Property(p => p.Mobile).IsRequired().HasMaxLength(10);
        builder.HasIndex(p => p.UserId).IsUnique();
    }
}

/// <summary>Mapping for <see cref="TouristProfile"/> (BR18 passport, nationality, email).</summary>
public sealed class TouristProfileConfiguration : IEntityTypeConfiguration<TouristProfile>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<TouristProfile> builder)
    {
        builder.ToTable("TouristProfiles");
        builder.HasKey(p => p.Id);
        builder.Property(p => p.PassportNumber).IsRequired().HasMaxLength(9);
        builder.Property(p => p.Nationality).IsRequired().HasMaxLength(80);
        builder.Property(p => p.Email).IsRequired().HasMaxLength(160);
        builder.HasIndex(p => p.UserId).IsUnique();
        builder.HasIndex(p => p.PassportNumber).IsUnique();
    }
}
