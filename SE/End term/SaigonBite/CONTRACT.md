# CONTRACT — shared type and file ownership

Every agent codes against this file. Do not rename anything here. If a signature must change,
change it in this file in the same commit and note it in `.handover/LATEST.md`.

Target: .NET 8, ASP.NET Core MVC, EF Core 8 Code-First, SQL Server (SQLite for tests).
No `dotnet` on the host — build with:
`docker run --rm -v "$PWD":/w -w /w mcr.microsoft.com/dotnet/sdk:8.0 dotnet build`

## File ownership (do not write outside your rows)

| Path | Owner |
|---|---|
| `src/SaigonBite.Core/**` | Agent A (domain) |
| `tests/SaigonBite.UnitTests/**` | Agent A (domain tests) |
| `src/SaigonBite.Web/**` | Agent B (web) |
| `src/SaigonBite.sln` | Agent B |
| `tests/SaigonBite.E2ETests/**` | Agent D (e2e) |
| `docs/part2-design/**` | Agent C (design) |
| `slides/**`, `prototype/**` | Agent D |
| `docs/part3-qa/**` | whoever produces the evidence; append only |
| `config/**`, `specs/**`, `render/**` | coordinator only |

## Namespace and project layout

```
src/SaigonBite.Core/SaigonBite.Core.csproj      -> namespace SaigonBite.Core
src/SaigonBite.Web/SaigonBite.Web.csproj        -> namespace SaigonBite.Web
tests/SaigonBite.UnitTests/…                    -> namespace SaigonBite.UnitTests
```

`SaigonBite.Core` must not reference ASP.NET Core, EF Core, or any I/O assembly.

## Enumerations

```csharp
namespace SaigonBite.Core.Orders;
public enum OrderStatus { Placed = 0, Confirmed = 1, Preparing = 2, Ready = 3,
                          OutForDelivery = 4, Delivered = 5, Cancelled = 6, Failed = 7 }
public enum ActorRole { Customer = 0, KitchenStaff = 1, Shipper = 2, Admin = 3, System = 4 }
public enum CustomerType { Local = 0, Tourist = 1 }
public enum PaymentMethod { Momo = 0, VnPay = 1, ApplePay = 2, PayPal = 3, CashOnDelivery = 4 }
public enum VoucherType { Percent = 0, Fixed = 1 }
```

## Pricing (BR1–BR12) — pure, no I/O

```csharp
namespace SaigonBite.Core.Pricing;

public sealed record PriceLineRequest(int MenuItemId, int Quantity, long UnitPrice);

public sealed record PriceContext
{
    public required IReadOnlyList<PriceLineRequest> Lines { get; init; }
    public required decimal DistanceKm { get; init; }
    public required DateTime PlacementTime { get; init; }   // Vietnam local, UTC+7
    public required bool RainFlagOn { get; init; }
    public required int HubLoadPercent { get; init; }        // 0..100, snapshot, new order excluded
    public bool HubRejectsNewOrders { get; init; }           // BR8, load >= 90
    public VoucherRequest? Voucher { get; init; }
}

public sealed record VoucherRequest(
    VoucherType Type, long Value, long MaxDiscount, long MinSubtotal, bool IsActive,
    DateOnly ValidFrom, DateOnly ValidTo);

public sealed record PriceResult
{
    public required long Subtotal { get; init; }          // S
    public required long QuietKitchenDiscount { get; init; } // Q
    public required long VoucherDiscount { get; init; }      // V
    public required long FoodTotal { get; init; }            // F = S - Q - V
    public required long DeliveryFee { get; init; }          // D
    public required long RushSurcharge { get; init; }        // R
    public required long RainSurcharge { get; init; }        // R2
    public required long Total { get; init; }                // rounded once, BR11
    public required IReadOnlyList<PriceRejection> Rejections { get; init; }
    public bool IsAccepted => Rejections.Count == 0;
}

public sealed record PriceRejection(string Code, string Message); // e.g. "BR1"

public static class PricingEngine
{
    public static PriceResult Calculate(PriceContext context);
}
```

Rejection codes, in evaluation order: `BR1` minimum order, `BR2` coverage,
`BR8` hub protection, `BR12` line limits or cross-hub item.

## Order state machine (BR15, BR16)

```csharp
namespace SaigonBite.Core.Orders;

public sealed record TransitionResult(bool Allowed, string? Reason);

public static class OrderStateMachine
{
    public static TransitionResult CanTransition(OrderStatus from, OrderStatus to, ActorRole actor);
    public static bool IsTerminal(OrderStatus status);
    public static IReadOnlyCollection<OrderStatus> AllowedNext(OrderStatus from, ActorRole actor);
}
```

A reason is required when `ActorRole.KitchenStaff` moves `Placed → Cancelled` and when
`ActorRole.Admin` moves `Confirmed → Cancelled` (ambiguity A5). Encode that requirement in the
result reason, not in the caller.

## Payments (BR13, BR14) — Strategy

```csharp
namespace SaigonBite.Core.Payments;

public sealed record PaymentRequest(Guid OrderId, long Amount, PaymentMethod Method,
                                    CustomerType CustomerType, string? ReturnUrl);

public sealed record PaymentResult(bool Success, string? GatewayReference, string? Error,
                                   bool RequiresCashConfirmation);

public interface IPaymentStrategy
{
    PaymentMethod Method { get; }
    string Key { get; }                                  // stable string stored on PaymentRecord
    bool IsAvailableFor(CustomerType customerType);      // BR13
    Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken ct = default);
}

public interface IPaymentStrategyResolver
{
    IPaymentStrategy Resolve(PaymentMethod method);
    IReadOnlyList<IPaymentStrategy> AvailableFor(CustomerType customerType);
}
```

Adding a method means one new `IPaymentStrategy` class plus one DI registration line.
Never edit an existing strategy.

## EF entities (Agent B owns them under `src/SaigonBite.Web/Data`)

`User` (Id, Username, PasswordHash, Role, CustomerType?, IsDeleted) ·
`LocalCustomerProfile` (Mobile) · `TouristProfile` (PassportNumber, Nationality, Email) ·
`Hub` (Name, District, Address, KitchenCapacity, IsDeleted) ·
`Brand` (Name, Description, IsDeleted) · `HubBrand` (join) ·
`MenuItem` (BrandId, Category, Name, Price, IsAvailable, IsDeleted) ·
`Voucher` (Code, Type, Value, MaxDiscount, MinSubtotal, ValidFrom, ValidTo, IsActive) ·
`Order` (CustomerId, HubId, Status, PlacedAt, DistanceKm, HubLoadPercent, RainFlag,
Subtotal, QuietKitchenDiscount, VoucherDiscount, FoodTotal, DeliveryFee, RushSurcharge,
RainSurcharge, Total, AssignedShipperId?, PaymentMethod?, IsCashConfirmed) ·
`OrderLine` (MenuItemId, ItemName, UnitPrice, Quantity) ·
`OrderStatusHistory` (OrderId, FromStatus, ToStatus, ActorRole, ActorId, Reason, OccurredAt) ·
`PaymentRecord` (OrderId, StrategyKey, Amount, GatewayReference, Success, CreatedAt).

Money is `long` VND. Every entity referenced by orders uses a soft-delete flag, never a hard delete.
`Order` and `OrderLine` are never deleted.

## Web routes (Agent B)

`/account` register (local, tourist), login, language toggle · `/brands` CRUD ·
`/hubs` CRUD · `/vouchers` CRUD · `/orders` cart, checkout, breakdown, track, edit, cancel ·
`/deliveries` assign, advance, confirm cash, fail · `/reports/revenue`, `/reports/utilisation` ·
`/admin` dashboard, rain flag. Role policies: `Customer`, `KitchenStaff`, `Shipper`, `Admin`.

## Rules every agent follows

1. English source comments and documents; Vietnamese only in `.resx` values.
2. Cite the FR and BR identifiers in XML doc comments on public types and in test names.
   Example: `[Fact] public void BR1_subtotal_49999_is_rejected()`.
3. Never invent a student name, student ID, instructor, date or result. Use `TBD`.
4. No formula screenshots anywhere; use MathML or typeset text.
5. Do not edit `specs/**`, `config/**`, `render/**`, or the three source PDFs.
