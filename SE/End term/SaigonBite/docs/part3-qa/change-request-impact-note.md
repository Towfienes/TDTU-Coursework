# Change Request Impact Note

**Use case affected**: D — Place and Manage Orders (payment module)
**Prepared**: before the Week 5 change request, as evidence that the design anticipates it
**Status**: template — the actual change request text arrives in Week 5 and Section 1 is filled then

---

## 1. The change request

> To be transcribed verbatim from the instructor when issued in Week 5.

The most likely form, which the architecture is built to absorb, is **a new payment method** — for
example ZaloPay for local customers, or a credit-card gateway for tourists. Section 3 answers that
case. If the instructor instead changes a pricing rule, Section 4 answers that case.

## 2. Why the change is local, not structural

The payment module has been a Strategy since Part 2, for exactly this reason:

- one interface, `IPaymentStrategy`, with a single `ChargeAsync` entry point
- one class per method, each declaring its own `Key` and `IsAvailableFor(customerType)`
- one resolver, `PaymentStrategyResolver`, that selects a strategy by `PaymentMethod`
- every class is registered in dependency injection in `Program.cs`, one line each

The order service never names a concrete gateway. It asks the resolver for the strategy that matches
the order's method and calls the interface. Consequently **admitting a new method is an addition, not
an edit**: no existing payment class is opened.

## 3. Expected impact — new payment method

| Item | Change | Files |
|---|---|---|
| New strategy class | Add `ZaloPayStrategy : IPaymentStrategy` implementing `Key = "zalo-pay"`, `IsAvailableFor`, and `ChargeAsync` | `src/SaigonBite.Core/Payments/ZaloPayStrategy.cs` (new) |
| Registration | One `AddScoped<IPaymentStrategy, ZaloPayStrategy>()` line | `src/SaigonBite.Web/Program.cs` (+1 line) |
| Actor mapping (BR13) | Declare which customer type may use it, inside the new class only | new class |
| Enum value | Add `PaymentMethod.ZaloPay` | `src/SaigonBite.Core/Payments/PaymentMethod.cs` (+1 member) |
| Seed data | Add a demo payment row for the new method | `Data/DbSeeder.cs` |
| Tests | Add the new method to the BR13 matrix test and the strategy contract test | `tests/SaigonBite.UnitTests/PaymentStrategyTests.cs` |
| Documentation | One row in the payment table of the consolidated report | `docs/final/` |

**Files modified among existing payment classes: zero.** That is the claim the rubric tests, and it
is verifiable with `git diff --stat` on the change commit.

Estimated effort: under one hour, dominated by the gateway's own signing requirement — not by the
application's structure.

## 4. Alternate case — a pricing rule change

Pricing is one pure function, `PricingEngine.Calculate(PriceContext)`, with no I/O. A rule change
therefore touches two files:

| Item | Change | Files |
|---|---|---|
| Rule | Edit the single step concerned, keeping the BR10 order | `src/SaigonBite.Core/Pricing/PricingEngine.cs` |
| Boundary tests | Add the boundary pair for the new threshold | `tests/SaigonBite.UnitTests/Pricing*Tests.cs` |

No controller, view, entity or migration changes, because no pricing logic exists in those layers.

## 5. Verification performed after the change

```sh
dotnet test          # full suite must stay green, plus the new method's cases
git diff --stat      # must show no modification under Payments/ except PaymentMethod.cs
```

The diff is attached to this note when the change is implemented.
