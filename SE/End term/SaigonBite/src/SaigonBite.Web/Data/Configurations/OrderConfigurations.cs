using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Web.Data.Entities;

namespace SaigonBite.Web.Data.Configurations;

/// <summary>Mapping for <see cref="Voucher"/> (FR-C1, BR9).</summary>
public sealed class VoucherConfiguration : IEntityTypeConfiguration<Voucher>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<Voucher> builder)
    {
        builder.ToTable("Vouchers");
        builder.HasKey(v => v.Id);

        builder.Property(v => v.Code).IsRequired().HasMaxLength(40);
        builder.HasIndex(v => v.Code).IsUnique();

        // Stored as text so a report or a DBA reads "Percent"/"Fixed" without a lookup table.
        builder.Property(v => v.Type).HasConversion<string>().HasMaxLength(20).IsRequired();

        builder.Property(v => v.Value).IsRequired();
        builder.Property(v => v.MaxDiscount).IsRequired();
        builder.Property(v => v.MinSubtotal).IsRequired();
        builder.Property(v => v.ValidFrom).IsRequired();
        builder.Property(v => v.ValidTo).IsRequired();
        builder.Property(v => v.IsActive).IsRequired();
    }
}

/// <summary>
/// Mapping for <see cref="Order"/>: BR17 snapshot columns, BR10 money columns, BR15 status and the
/// R1/R2 indexes. Orders carry no soft-delete flag by design (CONTRACT.md).
/// </summary>
public sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");
        builder.HasKey(o => o.Id);

        builder.Property(o => o.Status).HasConversion<string>().HasMaxLength(20).IsRequired();
        builder.Property(o => o.PaymentMethod).HasConversion<string>().HasMaxLength(20);

        builder.Property(o => o.PlacedAt).IsRequired();
        builder.Property(o => o.DistanceKm).HasPrecision(4, 2).IsRequired();
        builder.Property(o => o.HubLoadPercent).IsRequired();
        builder.Property(o => o.RainFlag).IsRequired();

        builder.Property(o => o.Subtotal).IsRequired();
        builder.Property(o => o.QuietKitchenDiscount).IsRequired();
        builder.Property(o => o.VoucherDiscount).IsRequired();
        builder.Property(o => o.FoodTotal).IsRequired();
        builder.Property(o => o.DeliveryFee).IsRequired();
        builder.Property(o => o.RushSurcharge).IsRequired();
        builder.Property(o => o.RainSurcharge).IsRequired();
        builder.Property(o => o.Total).IsRequired();

        builder.Property(o => o.VoucherCode).HasMaxLength(40);
        builder.Property(o => o.HotelName).HasMaxLength(120);
        builder.Property(o => o.RoomNumber).HasMaxLength(20);
        builder.Property(o => o.Notes).HasMaxLength(400);

        builder.HasOne(o => o.Customer)
            .WithMany()
            .HasForeignKey(o => o.CustomerId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne(o => o.Hub)
            .WithMany(h => h.Orders)
            .HasForeignKey(o => o.HubId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne(o => o.Voucher)
            .WithMany()
            .HasForeignKey(o => o.VoucherId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne(o => o.AssignedShipper)
            .WithMany()
            .HasForeignKey(o => o.AssignedShipperId)
            .OnDelete(DeleteBehavior.Restrict);

        // BR8 reads the live load per hub and status; R1/R2 filter by date range.
        builder.HasIndex(o => new { o.HubId, o.Status });
        builder.HasIndex(o => new { o.CustomerId, o.PlacedAt });
        builder.HasIndex(o => o.PlacedAt);
    }
}

/// <summary>Mapping for <see cref="OrderLine"/>, the priced line snapshot (BR12, FR-A4).</summary>
public sealed class OrderLineConfiguration : IEntityTypeConfiguration<OrderLine>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<OrderLine> builder)
    {
        builder.ToTable("OrderLines");
        builder.HasKey(l => l.Id);

        builder.Property(l => l.ItemName).IsRequired().HasMaxLength(120);
        builder.Property(l => l.BrandName).IsRequired().HasMaxLength(120);
        builder.Property(l => l.CategoryName).IsRequired().HasMaxLength(60);
        builder.Property(l => l.UnitPrice).IsRequired();
        builder.Property(l => l.Quantity).IsRequired();
        builder.Property(l => l.IsRemoved).IsRequired();

        // BR12: quantity 1..20 per line, enforced in the database as well as in the controller.
        builder.ToTable(t => t.HasCheckConstraint("CK_OrderLines_Quantity", "[Quantity] >= 1 AND [Quantity] <= 20"));

        builder.HasOne(l => l.Order)
            .WithMany(o => o.Lines)
            .HasForeignKey(l => l.OrderId)
            .OnDelete(DeleteBehavior.Cascade);

        // The menu item is referenced, never deleted; history keeps the snapshot columns above.
        builder.HasOne<MenuItem>()
            .WithMany()
            .HasForeignKey(l => l.MenuItemId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasIndex(l => new { l.OrderId, l.IsRemoved });
        builder.HasIndex(l => l.CategoryName);
    }
}

/// <summary>Mapping for <see cref="OrderStatusHistory"/> (FR-S5, NFR5).</summary>
public sealed class OrderStatusHistoryConfiguration : IEntityTypeConfiguration<OrderStatusHistory>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<OrderStatusHistory> builder)
    {
        builder.ToTable("OrderStatusHistory");
        builder.HasKey(h => h.Id);

        builder.Property(h => h.FromStatus).HasConversion<string>().HasMaxLength(20).IsRequired();
        builder.Property(h => h.ToStatus).HasConversion<string>().HasMaxLength(20).IsRequired();
        builder.Property(h => h.ActorRole).HasConversion<string>().HasMaxLength(20).IsRequired();
        builder.Property(h => h.OccurredAt).IsRequired();
        builder.Property(h => h.Applied).IsRequired();
        builder.Property(h => h.Reason).HasMaxLength(400);

        builder.HasOne(h => h.Order)
            .WithMany(o => o.History)
            .HasForeignKey(h => h.OrderId)
            .OnDelete(DeleteBehavior.Cascade);

        // R2 computes Confirmed -> Ready intervals from this table.
        builder.HasIndex(h => new { h.OrderId, h.ToStatus, h.OccurredAt });
    }
}

/// <summary>Mapping for <see cref="PaymentRecord"/> (FR-P3, NFR5).</summary>
public sealed class PaymentRecordConfiguration : IEntityTypeConfiguration<PaymentRecord>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<PaymentRecord> builder)
    {
        builder.ToTable("PaymentRecords");
        builder.HasKey(p => p.Id);

        builder.Property(p => p.StrategyKey).IsRequired().HasMaxLength(60);
        builder.Property(p => p.Amount).IsRequired();
        builder.Property(p => p.GatewayReference).HasMaxLength(120);
        builder.Property(p => p.Success).IsRequired();
        builder.Property(p => p.CreatedAt).IsRequired();

        builder.HasOne(p => p.Order)
            .WithMany(o => o.Payments)
            .HasForeignKey(p => p.OrderId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasIndex(p => p.OrderId);
    }
}

/// <summary>Mapping for <see cref="PlatformSetting"/> (BR5 heavy-rain flag, FR-S4).</summary>
public sealed class PlatformSettingConfiguration : IEntityTypeConfiguration<PlatformSetting>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<PlatformSetting> builder)
    {
        builder.ToTable("PlatformSettings");
        builder.HasKey(s => s.Key);
        builder.Property(s => s.Key).HasMaxLength(60);
        builder.Property(s => s.Value).IsRequired().HasMaxLength(200);
    }
}
