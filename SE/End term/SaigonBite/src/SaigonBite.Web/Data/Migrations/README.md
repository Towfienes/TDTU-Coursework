# Migrations

`InitialCreate` was generated with `dotnet ef migrations add InitialCreate` (EF Core 8.0.10, SQL Server
provider) from `Data/DesignTimeDbContextFactory.cs`. It creates 13 tables and the check constraints that
back BR8 (hub capacity > 0) and BR12 (line quantity 1..20).

**Which path runs where**

| Provider | How the schema is created | Why |
|---|---|---|
| SQL Server (`ConnectionStrings:Default`, no `USE_SQLITE`) | `Database.Migrate()` - this migration set | Deployment target, Tier 3 Code-First |
| SQLite (`USE_SQLITE=1`) | `Database.EnsureCreated()` | Provider-specific DDL (identity columns, `nvarchar`, `datetime2`) cannot be replayed from a SQL Server migration on SQLite |

The application therefore never applies these migrations to SQLite; it builds the same model with the
SQLite provider instead. `SaigonBiteDbContextModelSnapshot.cs` stays the single source of truth for the
model, and `dotnet ef migrations add` keeps it current.

Regenerate (inside the SDK container, `dotnet-ef` installed as a global tool):

```sh
docker run --rm -v "$PWD":/w -w /w mcr.microsoft.com/dotnet/sdk:8.0 sh -lc '
  dotnet tool install --global dotnet-ef --version 8.0.10 &&
  export PATH="$PATH:/w/.dotnet/.dotnet/tools" &&
  dotnet ef migrations add <Name> --project src/SaigonBite.Web --startup-project src/SaigonBite.Web \
    --output-dir Data/Migrations'
```
