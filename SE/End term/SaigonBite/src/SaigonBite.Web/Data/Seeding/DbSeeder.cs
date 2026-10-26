using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;
using SaigonBite.Core.Pricing;
using SaigonBite.Web.Data;
using SaigonBite.Web.Data.Entities;
using SaigonBite.Web.Infrastructure;

namespace SaigonBite.Web.Data.Seeding;

/// <summary>
/// Development seed data (CONTRACT.md): 5 hubs, 3 brands per hub, ~60 menu items, 5 vouchers and one
/// account per role, plus a handful of historical orders so R1 and R2 are not empty on first run.
/// </summary>
/// <remarks>
/// <para>
/// Seeded prices are produced by <c>PricingEngine.Calculate</c>, never typed by hand, so the demo data
/// obeys BR1–BR12 exactly like a real order. The BR17 snapshot fields are filled with the values the
/// seed chose, which is what makes those historical orders reproducible.
/// </para>
/// <para>
/// Every account uses the documented development password <see cref="DemoPassword"/>. Seeding is called
/// only when the environment is Development and the database is empty, so it can never touch a real
/// deployment.
/// </para>
/// </remarks>
public static class DbSeeder
{
    /// <summary>Documented development password shared by the seeded accounts (at least 8 characters, BR18).</summary>
    public const string DemoPassword = "Saigon@123";

    /// <summary>Seeds the database when it holds no accounts yet.</summary>
    public static async Task SeedAsync(IServiceProvider services, CancellationToken cancellationToken = default)
    {
        var db = services.GetRequiredService<SaigonBiteDbContext>();
        var hasher = services.GetRequiredService<IPasswordHasher<User>>();
        var logger = services.GetRequiredService<ILoggerFactory>().CreateLogger(typeof(DbSeeder));

        if (await db.Users.IgnoreQueryFilters().AnyAsync(cancellationToken))
        {
            return;
        }

        // One transaction for the whole seed. A failure part-way (for example an invalid seeded price)
        // must roll back to an empty database instead of leaving a half-seeded one that the next start
        // would silently accept because "some users exist".
        await using var transaction = await db.Database.BeginTransactionAsync(cancellationToken);

        // -------------------------------------------------------------------------------------------
        // Hubs (FR-B1): capacity is a whole number of concurrent orders and must be greater than zero.
        // -------------------------------------------------------------------------------------------
        var hubs = new List<Hub>
        {
            new() { Name = "SaigonBite Ben Thanh", District = "District 1", Address = "12 Le Loi, Ben Nghe", KitchenCapacity = 10 },
            new() { Name = "SaigonBite Tan Dinh", District = "District 3", Address = "48 Hai Ba Trung, Tan Dinh", KitchenCapacity = 8 },
            new() { Name = "SaigonBite Cho Lon", District = "District 5", Address = "210 Nguyen Trai, Ward 3", KitchenCapacity = 12 },
            new() { Name = "SaigonBite Phu My Hung", District = "District 7", Address = "15 Nguyen Van Linh, Tan Phu", KitchenCapacity = 6 },
            new() { Name = "SaigonBite Binh Thanh", District = "Binh Thanh", Address = "77 Xo Viet Nghe Tinh, Ward 25", KitchenCapacity = 15 },
        };
        db.Hubs.AddRange(hubs);

        // -------------------------------------------------------------------------------------------
        // Brands (FR-A1).
        // -------------------------------------------------------------------------------------------
        var brands = new List<Brand>
        {
            new() { Name = "Pho Ong Ba", Description = "Ha Noi style beef pho simmered for twelve hours." },
            new() { Name = "Banh Mi Saigon", Description = "Crisp baguettes filled to order on the pavement." },
            new() { Name = "Com Tam Co Ba", Description = "Broken rice plates with grilled pork and pickles." },
            new() { Name = "Bun Bo Hue", Description = "Spicy lemongrass beef noodle soup from the centre." },
            new() { Name = "Goi Cuon Nha", Description = "Fresh rolls, banh xeo and shareable snacks." },
            new() { Name = "Ca Phe Saigon", Description = "Robusta coffee, teas and smoothies." },
        };
        db.Brands.AddRange(brands);
        await db.SaveChangesAsync(cancellationToken);

        // Each hub operates three brands (BR12: an item is orderable only at a hub that runs its brand).
        var operatingPlan = new[]
        {
            new[] { 0, 1, 5 },
            new[] { 0, 2, 4 },
            new[] { 1, 3, 5 },
            new[] { 2, 4, 5 },
            new[] { 0, 1, 3 },
        };

        for (var hubIndex = 0; hubIndex < hubs.Count; hubIndex++)
        {
            foreach (var brandIndex in operatingPlan[hubIndex])
            {
                db.HubBrands.Add(new HubBrand { HubId = hubs[hubIndex].Id, BrandId = brands[brandIndex].Id });
            }
        }

        // -------------------------------------------------------------------------------------------
        // Menu items: ten per brand, sixty in total, spread over the reporting categories of R1.
        // -------------------------------------------------------------------------------------------
        var menuByBrand = new Dictionary<string, (string Category, long Price)[]>
        {
            ["Pho Ong Ba"] = new[]
            {
                ("Noodles", 65_000L), ("Noodles", 65_000L), ("Noodles", 60_000L), ("Noodles", 55_000L),
                ("Noodles", 70_000L), ("Snacks", 45_000L), ("Snacks", 20_000L), ("Drinks", 10_000L),
                ("Drinks", 25_000L), ("Dessert", 30_000L),
            },
            ["Banh Mi Saigon"] = new[]
            {
                ("Banh Mi", 45_000L), ("Banh Mi", 40_000L), ("Banh Mi", 35_000L), ("Banh Mi", 35_000L),
                ("Banh Mi", 30_000L), ("Banh Mi", 50_000L), ("Snacks", 30_000L), ("Snacks", 35_000L),
                ("Drinks", 29_000L), ("Drinks", 20_000L),
            },
            ["Com Tam Co Ba"] = new[]
            {
                ("Rice", 70_000L), ("Rice", 65_000L), ("Rice", 75_000L), ("Rice", 60_000L),
                ("Rice", 95_000L), ("Rice", 40_000L), ("Snacks", 35_000L), ("Drinks", 30_000L),
                ("Dessert", 25_000L), ("Dessert", 30_000L),
            },
            ["Bun Bo Hue"] = new[]
            {
                ("Noodles", 65_000L), ("Noodles", 70_000L), ("Noodles", 60_000L), ("Noodles", 60_000L),
                ("Noodles", 55_000L), ("Snacks", 40_000L), ("Snacks", 30_000L), ("Drinks", 25_000L),
                ("Drinks", 35_000L), ("Dessert", 30_000L),
            },
            ["Goi Cuon Nha"] = new[]
            {
                ("Snacks", 40_000L), ("Snacks", 35_000L), ("Snacks", 30_000L), ("Snacks", 55_000L),
                ("Snacks", 45_000L), ("Snacks", 45_000L), ("Snacks", 50_000L), ("Snacks", 15_000L),
                ("Snacks", 5_000L), ("Dessert", 30_000L),
            },
            ["Ca Phe Saigon"] = new[]
            {
                ("Drinks", 25_000L), ("Drinks", 29_000L), ("Drinks", 32_000L), ("Drinks", 35_000L),
                ("Drinks", 45_000L), ("Drinks", 45_000L), ("Drinks", 45_000L), ("Drinks", 40_000L),
                ("Drinks", 35_000L), ("Snacks", 30_000L),
            },
        };

        var itemNames = new Dictionary<string, string[]>
        {
            ["Pho Ong Ba"] = new[]
            {
                "Pho Bo Tai", "Pho Bo Vien", "Pho Ga", "Pho Chay", "Pho Tai Nam",
                "Banh Pho Chien", "Trung Chien", "Tra Da", "Tra Chanh", "Che Dau",
            },
            ["Banh Mi Saigon"] = new[]
            {
                "Banh Mi Thit Nuong", "Banh Mi Ga", "Banh Mi Bi", "Banh Mi Chay", "Banh Mi Trung",
                "Banh Mi Heo Quay", "Khoai Tay Chien", "Goi Cuon Tom", "Ca Phe Sua Da", "Nuoc Mia",
            },
            ["Com Tam Co Ba"] = new[]
            {
                "Com Tam Suon Nuong", "Com Tam Bi Cha", "Com Ga Xoi Mo", "Com Chien Duong Chau",
                "Com Bo Luc Lac", "Canh Chua", "Cha Gio", "Tra Dao", "Sua Chua", "Banh Flan",
            },
            ["Bun Bo Hue"] = new[]
            {
                "Bun Bo Hue", "Bun Bo Gio", "Bun Cha", "Bun Thit Nuong", "Bun Oc",
                "Cha Hue", "Nem Chua", "Tra Sen", "Sinh To Dua", "Banh Bot Loc",
            },
            ["Goi Cuon Nha"] = new[]
            {
                "Goi Cuon Tom Tuoi", "Goi Cuon Thit", "Goi Cuon Chay", "Banh Xeo", "Banh Khot",
                "Cha Gio Tom", "Nem Nuong", "Rau Song", "Nuoc Mam", "Che Ba Mau",
            },
            ["Ca Phe Saigon"] = new[]
            {
                "Ca Phe Den", "Ca Phe Sua Da Dac Biet", "Bac Xiu", "Tra Sen Vang", "Tra Dao Cam Sa",
                "Sinh To Bo", "Sinh To Xoai", "Nuoc Cam", "Sua Dua", "Banh Mi Op La",
            },
        };

        var menuItems = new List<MenuItem>();
        foreach (var brand in brands)
        {
            var shapes = menuByBrand[brand.Name];
            var names = itemNames[brand.Name];
            for (var i = 0; i < names.Length; i++)
            {
                menuItems.Add(new MenuItem
                {
                    BrandId = brand.Id,
                    Name = names[i],
                    Category = shapes[i].Category,
                    Price = shapes[i].Price,
                    IsAvailable = true,
                });
            }
        }

        // FR-A5: one item is deliberately unavailable so the availability rule can be demonstrated.
        menuItems.First(m => m.Name == "Banh Mi Heo Quay").IsAvailable = false;
        db.MenuItems.AddRange(menuItems);

        // -------------------------------------------------------------------------------------------
        // Vouchers (FR-C1, BR9). Dates are relative to today so the demo never presents an expired set.
        // -------------------------------------------------------------------------------------------
        var today = VietnamTime.Today;
        db.Vouchers.AddRange(
            new Voucher
            {
                Code = "WELCOME10", Type = VoucherType.Percent, Value = 10, MaxDiscount = 30_000,
                MinSubtotal = 100_000, ValidFrom = today.AddDays(-30), ValidTo = today.AddDays(60),
                IsActive = true,
            },
            new Voucher
            {
                Code = "LUNCH15", Type = VoucherType.Percent, Value = 15, MaxDiscount = 50_000,
                MinSubtotal = 200_000, ValidFrom = today.AddDays(-30), ValidTo = today.AddDays(60),
                IsActive = true,
            },
            new Voucher
            {
                Code = "FIXED20", Type = VoucherType.Fixed, Value = 20_000, MaxDiscount = 20_000,
                MinSubtotal = 150_000, ValidFrom = today.AddDays(-30), ValidTo = today.AddDays(60),
                IsActive = true,
            },
            new Voucher
            {
                Code = "TOURIST50", Type = VoucherType.Fixed, Value = 50_000, MaxDiscount = 50_000,
                MinSubtotal = 250_000, ValidFrom = today.AddDays(-30), ValidTo = today.AddDays(60),
                IsActive = true,
            },
            new Voucher
            {
                Code = "EXPIRED10", Type = VoucherType.Percent, Value = 10, MaxDiscount = 20_000,
                MinSubtotal = 100_000, ValidFrom = today.AddDays(-90), ValidTo = today.AddDays(-10),
                IsActive = false,
            });

        // -------------------------------------------------------------------------------------------
        // Accounts: one per role plus both customer types (FR-E4, BR18).
        // -------------------------------------------------------------------------------------------
        var localCustomer = NewUser("0901234567", "Lan Nguyen", Roles.Customer, hasher, CustomerType.Local);
        localCustomer.LocalProfile = new LocalCustomerProfile { Mobile = "0901234567" };

        var touristCustomer = NewUser(
            "emma.wilson@example.com", "Emma Wilson", Roles.Customer, hasher, CustomerType.Tourist);
        touristCustomer.TouristProfile = new TouristProfile
        {
            PassportNumber = "B1234567",
            Nationality = "Australia",
            Email = "emma.wilson@example.com",
        };

        var kitchenStaff = NewUser("kitchen1", "Chef Minh", Roles.KitchenStaff, hasher, customerType: null);
        kitchenStaff.HubId = hubs[0].Id;
        var kitchenStaffTwo = NewUser("kitchen2", "Chef Hoa", Roles.KitchenStaff, hasher, customerType: null);
        kitchenStaffTwo.HubId = hubs[1].Id;

        var shipper = NewUser("shipper1", "Bao Tran", Roles.Shipper, hasher, customerType: null);
        var shipperTwo = NewUser("shipper2", "Dung Pham", Roles.Shipper, hasher, customerType: null);
        var admin = NewUser("admin", "System Administrator", Roles.Admin, hasher, customerType: null);

        db.Users.AddRange(
            localCustomer, touristCustomer, kitchenStaff, kitchenStaffTwo, shipper, shipperTwo, admin);
        await db.SaveChangesAsync(cancellationToken);

        db.PlatformSettings.Add(new PlatformSetting { Key = "RainFlag", Value = "false" });
        await db.SaveChangesAsync(cancellationToken);

        // -------------------------------------------------------------------------------------------
        // Historical orders so R1/R2 have data on the first run (FR-R1, FR-R2).
        // -------------------------------------------------------------------------------------------
        var itemsByName = menuItems.ToDictionary(m => m.Name, m => m);
        var vouchersByCode = await db.Vouchers.ToDictionaryAsync(v => v.Code, cancellationToken);

        async Task SeedOrderAsync(
            int daysAgo, int hour, int minute, int customerId, int hubIndex, OrderStatus status,
            PaymentMethod method, decimal distanceKm, int loadPercent, bool rain, string? voucherCode,
            (string Name, int Quantity)[] lines, bool cashConfirmed = false)
        {
            var hub = hubs[hubIndex];
            var placedAt = today.AddDays(-daysAgo).ToDateTime(new TimeOnly(hour, minute));
            // A seeded order for "today" at 18:00 must not sit in the future when the demo runs at 01:00,
            // or it sorts above an order the presenter has just placed. Move it back a day in that case.
            if (placedAt > DateTime.Now)
            {
                placedAt = placedAt.AddDays(-1);
            }
            var voucher = voucherCode is null ? null : vouchersByCode[voucherCode];

            var context = new PriceContext
            {
                Lines = lines
                    .Select(l => new PriceLineRequest(itemsByName[l.Name].Id, l.Quantity, itemsByName[l.Name].Price))
                    .ToList(),
                DistanceKm = distanceKm,
                PlacementTime = placedAt,
                RainFlagOn = rain,
                HubLoadPercent = loadPercent,
                HubRejectsNewOrders = loadPercent >= 90,
                Voucher = voucher is null
                    ? null
                    : new VoucherRequest(
                        voucher.Type, voucher.Value, voucher.MaxDiscount, voucher.MinSubtotal,
                        voucher.IsActive, voucher.ValidFrom, voucher.ValidTo),
            };

            var price = PricingEngine.Calculate(context);
            if (!price.IsAccepted)
            {
                // Seed data must never store an order the engine would refuse; fail loudly instead.
                throw new InvalidOperationException(
                    "Seed order rejected by the pricing engine: "
                    + string.Join(", ", price.Rejections.Select(r => $"{r.Code} {r.Message}")));
            }

            var order = new Order
            {
                CustomerId = customerId,
                HubId = hub.Id,
                Status = status,
                PlacedAt = placedAt,
                DistanceKm = distanceKm,
                HubLoadPercent = loadPercent,
                RainFlag = rain,
                Subtotal = price.Subtotal,
                QuietKitchenDiscount = price.QuietKitchenDiscount,
                VoucherDiscount = price.VoucherDiscount,
                FoodTotal = price.FoodTotal,
                DeliveryFee = price.DeliveryFee,
                RushSurcharge = price.RushSurcharge,
                RainSurcharge = price.RainSurcharge,
                Total = price.Total,
                VoucherId = voucher?.Id,
                VoucherCode = voucher?.Code,
                PaymentMethod = method,
                IsCashConfirmed = cashConfirmed,
                AssignedShipperId = status is OrderStatus.OutForDelivery or OrderStatus.Delivered or OrderStatus.Failed
                    ? shipper.Id
                    : null,
                AssignedAt = status is OrderStatus.OutForDelivery or OrderStatus.Delivered or OrderStatus.Failed
                    ? placedAt.AddMinutes(14)
                    : null,
                DeliveredAt = status == OrderStatus.Delivered ? placedAt.AddMinutes(32) : null,
            };

            foreach (var line in lines)
            {
                var item = itemsByName[line.Name];
                order.Lines.Add(new OrderLine
                {
                    MenuItemId = item.Id,
                    ItemName = item.Name,
                    BrandName = brands.First(b => b.Id == item.BrandId).Name,
                    CategoryName = item.Category,
                    UnitPrice = item.Price,
                    Quantity = line.Quantity,
                    IsRemoved = false,
                });
            }

            // History mirrors the BR15 chain up to the seeded state, so R2 can average Confirmed -> Ready.
            var chain = new List<(OrderStatus From, OrderStatus To, ActorRole Actor, int Minutes, string? Reason)>
            {
                (OrderStatus.Placed, OrderStatus.Confirmed, ActorRole.KitchenStaff, 2, "Confirmed by kitchen"),
                (OrderStatus.Confirmed, OrderStatus.Preparing, ActorRole.KitchenStaff, 4, "Preparing"),
                (OrderStatus.Preparing, OrderStatus.Ready, ActorRole.KitchenStaff, 13, "Ready for pickup"),
                (OrderStatus.Ready, OrderStatus.OutForDelivery, ActorRole.Shipper, 16, "Picked up"),
                (OrderStatus.OutForDelivery, OrderStatus.Delivered, ActorRole.Shipper, 31, "Delivered"),
            };

            var terminalMinutes = status switch
            {
                OrderStatus.Placed => 0,
                OrderStatus.Confirmed => 2,
                OrderStatus.Preparing => 4,
                OrderStatus.Ready => 13,
                OrderStatus.OutForDelivery => 16,
                OrderStatus.Delivered => 31,
                OrderStatus.Cancelled => 3,
                OrderStatus.Failed => 20,
                _ => 0,
            };

            foreach (var step in chain)
            {
                if (step.Minutes > terminalMinutes)
                {
                    break;
                }

                order.History.Add(new OrderStatusHistory
                {
                    FromStatus = step.From,
                    ToStatus = step.To,
                    ActorRole = step.Actor,
                    ActorId = step.Actor == ActorRole.KitchenStaff ? kitchenStaff.Id : shipper.Id,
                    Reason = step.Reason,
                    OccurredAt = placedAt.AddMinutes(step.Minutes),
                    Applied = true,
                });
            }

            if (status == OrderStatus.Cancelled)
            {
                order.History.Add(new OrderStatusHistory
                {
                    FromStatus = OrderStatus.Placed,
                    ToStatus = OrderStatus.Cancelled,
                    ActorRole = ActorRole.Customer,
                    ActorId = customerId,
                    Reason = "Cancelled by the customer",
                    OccurredAt = placedAt.AddMinutes(terminalMinutes),
                    Applied = true,
                });
            }

            if (status == OrderStatus.Failed)
            {
                order.History.Add(new OrderStatusHistory
                {
                    FromStatus = OrderStatus.OutForDelivery,
                    ToStatus = OrderStatus.Failed,
                    ActorRole = ActorRole.Shipper,
                    ActorId = shipper.Id,
                    Reason = "Customer unreachable",
                    OccurredAt = placedAt.AddMinutes(terminalMinutes),
                    Applied = true,
                });
            }

            db.Orders.Add(order);
            await db.SaveChangesAsync(cancellationToken);

            // Payment history: online methods are charged at placement; COD is collected on delivery.
            if (method != PaymentMethod.CashOnDelivery)
            {
                db.PaymentRecords.Add(new PaymentRecord
                {
                    OrderId = order.Id,
                    StrategyKey = method.ToString(),
                    Amount = order.Total,
                    GatewayReference = $"SEED-{order.Id:D6}",
                    Success = true,
                    CreatedAt = placedAt,
                });

                if (status is OrderStatus.Cancelled or OrderStatus.Failed)
                {
                    db.PaymentRecords.Add(new PaymentRecord
                    {
                        OrderId = order.Id,
                        StrategyKey = method.ToString(),
                        Amount = -order.Total,
                        GatewayReference = $"REFUND-{order.Id}",
                        Success = true,
                        CreatedAt = placedAt.AddMinutes(terminalMinutes + 1),
                    });
                }

                await db.SaveChangesAsync(cancellationToken);
            }
        }

        // Hub 1 (capacity 10): a normal day with a Quiet Kitchen order (load 20 % < 30 %).
        await SeedOrderAsync(0, 11, 15, localCustomer.Id, 0, OrderStatus.Delivered, PaymentMethod.Momo,
            3.2m, 20, false, null,
            new[] { ("Pho Bo Tai", 1), ("Tra Da", 1) });

        await SeedOrderAsync(0, 12, 5, touristCustomer.Id, 0, OrderStatus.OutForDelivery,
            PaymentMethod.ApplePay, 2.4m, 25, true, "TOURIST50",
            new[] { ("Banh Mi Thit Nuong", 2), ("Ca Phe Sua Da", 2) });

        await SeedOrderAsync(0, 18, 40, localCustomer.Id, 1, OrderStatus.Preparing, PaymentMethod.VnPay,
            5.1m, 50, false, "WELCOME10",
            new[] { ("Com Tam Suon Nuong", 2), ("Tra Dao", 2) });

        await SeedOrderAsync(1, 12, 30, localCustomer.Id, 2, OrderStatus.Delivered,
            PaymentMethod.CashOnDelivery, 4.0m, 33, false, null,
            new[] { ("Bun Bo Hue", 2), ("Cha Hue", 1) }, cashConfirmed: true);

        await SeedOrderAsync(1, 19, 0, touristCustomer.Id, 3, OrderStatus.Cancelled, PaymentMethod.PayPal,
            6.2m, 16, false, null,
            new[] { ("Banh Xeo", 2), ("Che Ba Mau", 2) });

        await SeedOrderAsync(2, 11, 45, localCustomer.Id, 0, OrderStatus.Delivered, PaymentMethod.Momo,
            3.8m, 45, true, "LUNCH15",
            new[] { ("Pho Tai Nam", 3), ("Banh Pho Chien", 2), ("Tra Chanh", 3) });

        await SeedOrderAsync(2, 17, 55, touristCustomer.Id, 4, OrderStatus.Delivered,
            PaymentMethod.PayPal, 7.4m, 28, false, null,
            new[] { ("Banh Mi Thit Nuong", 3), ("Nuoc Mia", 3) });

        await SeedOrderAsync(3, 12, 10, localCustomer.Id, 1, OrderStatus.Failed,
            PaymentMethod.CashOnDelivery, 2.9m, 62, false, null,
            new[] { ("Com Tam Bi Cha", 2), ("Sua Chua", 2) });

        await SeedOrderAsync(3, 18, 20, localCustomer.Id, 2, OrderStatus.Delivered,
            PaymentMethod.VnPay, 4.6m, 19, false, "FIXED20",
            new[] { ("Bun Cha", 2), ("Nem Chua", 2), ("Tra Sen", 2) });

        await SeedOrderAsync(4, 11, 30, touristCustomer.Id, 0, OrderStatus.Ready,
            PaymentMethod.CashOnDelivery, 3.0m, 38, false, null,
            new[] { ("Pho Ga", 1), ("Goi Cuon Tom", 2) });

        await transaction.CommitAsync(cancellationToken);

        logger.LogInformation(
            "Seeded {Hubs} hubs, {Brands} brands, {Items} menu items, {Vouchers} vouchers, {Users} accounts "
            + "and 10 historical orders.",
            hubs.Count, brands.Count, menuItems.Count, 5, 7);
    }

    private static User NewUser(
        string username, string displayName, string role, IPasswordHasher<User> hasher,
        CustomerType? customerType)
    {
        var user = new User
        {
            Username = username,
            DisplayName = displayName,
            Role = role,
            CustomerType = customerType,
            CreatedAt = VietnamTime.Now,
        };

        user.PasswordHash = hasher.HashPassword(user, DemoPassword);
        return user;
    }
}
