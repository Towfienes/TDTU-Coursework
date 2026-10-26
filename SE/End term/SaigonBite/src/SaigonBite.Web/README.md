# SaigonBite.Web — presentation tier

ASP.NET Core MVC (`net8.0`) for the SaigonBite cloud-kitchen platform (Tier 3: ASP.NET MVC Code-First +
EF Core + Bootstrap 5, with the Tier 4 additions the project targets: interactive admin dashboard,
automated tests elsewhere in the repo).

This project owns the web boundary only: the entities, the DbContext, the migrations, the Razor views, the
resources and the controllers. **All pricing (BR1–BR12, BR17), the order state machine (BR15, BR16) and the
payment strategies (BR13, BR14) come from `SaigonBite.Core`.** No amount is computed here and no transition
is decided here.

---

## Run

The host has no .NET SDK; everything runs inside the SDK container from the repository root.

```sh
# build (repository root)
docker run --rm -v "$PWD":/w -w /w -e NUGET_PACKAGES=/w/.nuget -e DOTNET_CLI_HOME=/w/.dotnet \
  mcr.microsoft.com/dotnet/sdk:8.0 sh -lc 'dotnet build src/SaigonBite.sln'

# run with the SQLite development database (creates and seeds App_Data/saigonbite.dev.db)
docker run --rm -p 5091:8080 -v "$PWD":/w -w /w -e NUGET_PACKAGES=/w/.nuget -e DOTNET_CLI_HOME=/w/.dotnet \
  -e USE_SQLITE=1 -e ASPNETCORE_ENVIRONMENT=Development -e ASPNETCORE_URLS=http://0.0.0.0:8080 \
  mcr.microsoft.com/dotnet/sdk:8.0 \
  sh -lc 'cd src/SaigonBite.Web && dotnet bin/Debug/net8.0/SaigonBite.Web.dll'
```

Then open <http://localhost:5091> and switch the interface with the **EN / VI** toggle in the header.

SQL Server is the deployment target. Supply `ConnectionStrings:Default` (configuration,
user-secrets or the `ConnectionStrings__Default` environment variable) and do **not** set `USE_SQLITE`; the
application then applies the migrations in `Data/Migrations`.

---

## Seeded development accounts

Seeding runs only when `ASPNETCORE_ENVIRONMENT=Development` **and** the database has no accounts. All
seeded accounts share the password **`Saigon@123`** (10 characters, BR18 requires at least 8).

| Role | Sign-in identifier | Notes |
|---|---|---|
| Local Customer | `0901234567` | 10 digits, prefix 09 (BR18) |
| Foreign Tourist | `emma.wilson@example.com` | passport `B1234567`, Australia (BR18) |
| Kitchen Staff | `kitchen1` | home hub: SaigonBite Ben Thanh (District 1) |
| Kitchen Staff | `kitchen2` | home hub: SaigonBite Tan Dinh (District 3) |
| Shipper | `shipper1` | receives manual assignments (Ambiguity A1) |
| Shipper | `shipper2` | — |
| System Administrator | `admin` | dashboard, CRUD, reports, heavy-rain flag |

Seed content: 5 hubs, 6 brands (3 operated per hub), 60 menu items, 5 vouchers
(`WELCOME10`, `LUNCH15`, `FIXED20`, `TOURIST50`, `EXPIRED10`) and 10 historical orders spanning every
lifecycle state, so R1 and R2 are populated on the first run.

Every seeded price is produced by `PricingEngine.Calculate`; the seeder refuses to insert an order the
engine would reject.

---

## Migration path (stated explicitly)

* **Initial Code-First migration — generated with `dotnet ef migrations add InitialCreate`** for the SQL
  Server provider. The files are in `Data/Migrations/` (`20261022174930_InitialCreate.cs`, its designer and
  `SaigonBiteDbContextModelSnapshot.cs`). `dotnet-ef` 8.0.10 was installed inside the SDK container; the
  repository does not depend on a host tool.
* **SQLite development path — `Database.EnsureCreated()`.** Provider-specific DDL cannot be replayed
  across providers, so a SQL Server migration set is not applied to SQLite. `Program.cs` branches on
  `USE_SQLITE` and uses `EnsureCreated` for SQLite, `Migrate()` for SQL Server.
* To regenerate after a model change:

  ```sh
  docker run --rm -v "$PWD":/w -w /w -e NUGET_PACKAGES=/w/.nuget -e DOTNET_CLI_HOME=/w/.dotnet \
    mcr.microsoft.com/dotnet/sdk:8.0 sh -lc '
      dotnet tool install --global dotnet-ef --version 8.0.10 &&
      export PATH="$PATH:/w/.dotnet/.dotnet/tools" &&
      dotnet ef migrations add <Name> --project src/SaigonBite.Web --startup-project src/SaigonBite.Web \
        --output-dir Data/Migrations'
  ```

---

## Layout

| Path | Contents |
|---|---|
| `Controllers/` | thin controllers: Account (E), Brands (A), Hubs (B), Vouchers (C), Orders (D), Deliveries (F), Reports (R1/R2), Admin (dashboard, rain flag, accounts) |
| `Data/Entities/` | `User` + the two profile tables (BR18 discriminator), `Hub`, `Brand`, `HubBrand`, `MenuItem`, `Voucher`, `Order`, `OrderLine`, `OrderStatusHistory`, `PaymentRecord`, `PlatformSetting` |
| `Data/Configurations/` | one `IEntityTypeConfiguration<T>` per entity; soft-delete query filters; no-delete guard in `SaigonBiteDbContext` |
| `Data/Seeding/` | development seed |
| `Services/` | orchestration: pricing adapter, order/delivery transitions, hub load, reports, cart, payments registration |
| `ViewModels/` | screen models, including `BreakdownVm` for the BR10 panel |
| `Views/` | Razor + Bootstrap 5 (vendored in `wwwroot/vendor`, so the demo works offline) |
| `Resources/` | `SharedResource.resx` (English) and `SharedResource.vi.resx` (Vietnamese) |

## Business rules at the web boundary

* Rejections from `PricingEngine` are surfaced per code (`BR1`, `BR2`, `BR8`, `BR12`) with the engine's
  message plus, for `BR8`, the other hubs that can take the same basket (FR-B5).
* The BR17 snapshot (timestamp, hub load, rain flag) is stored at placement; an edit re-prices with the
  stored snapshot, not with current conditions.
* `OrderStatusHistory` gets a row for every accepted **and** rejected transition (`Applied` distinguishes
  them), including the reason supplied for BR16 staff cancellations.
* BR13 is enforced by asking the resolver for the customer type's methods and re-checking before charging;
  BR14 is enforced on the rounded total, both when offering COD and when charging it.
* Orders and order lines are never deleted. Editing marks a line `IsRemoved`; `SaveChanges` refuses any
  hard delete.
