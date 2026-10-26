# Implementation Plan: SaigonBite Platform

**Branch**: `001-saigonbite-platform` | **Date**: 2026-10-23 | **Spec**: `specs/001-saigonbite-platform/spec.md`

**Constitution**: `.specify/memory/constitution.md` · **Tier**: 4 (cap 10.0, floor 9.5)

## Summary

Build a three-tier ASP.NET Core MVC application that serves two customer types from one schema,
prices orders with a pure function that implements BR1–BR12 literally, drives orders through an
eight-state machine enforced in the business layer, and settles payments through a Strategy with one
class per method. Deliver two reports, an interactive admin dashboard and an automated test suite of
at least 20 equivalence/boundary cases plus 5 illegal-transition cases.

## Technical Context

**Language/Version**: C# 12 on .NET 8 (LTS)
**Primary Dependencies**: ASP.NET Core MVC, EF Core 8 (Code-First + Migrations), Bootstrap 5,
Chart.js, xUnit, FluentValidation, BCrypt.Net
**Storage**: SQL Server 2022 (Docker for development); SQLite only as a test double
**Testing**: xUnit for the pricing engine and the state machine; Playwright for end-to-end flows
**Target Platform**: Linux container for build and test, Windows or Linux for demo
**Project Type**: web application, three tiers
**Performance Goals**: price calculation under 1.5 s for 30 line items (NFR1); reports under 1 s on
seeded data
**Constraints**: no pricing logic outside the engine; no state transition accepted outside the state
machine; no edits to existing payment classes when a method is added
**Scale/Scope**: 5 hub records, ~60 menu items, 6 use cases, ~25 screens, 3 roles plus 2 customer types

## Constitution Check

*GATE: must pass before implementation; re-checked before every deliverable.*

| Principle | Gate | How this plan satisfies it |
|---|---|---|
| I — Traceable requirements | Every FR has an ID, a BR, an owner and a test | `spec.md` Requirement → BR Matrix; RTM in `docs/part1-proposal-req` |
| II — Pricing is pure | `PricingEngine.Calculate` performs no I/O | Engine takes `PriceContext`, returns `PriceResult`, no `DbContext` reference |
| III — State machine in business layer | Illegal transitions rejected server-side | `OrderStateMachine` consulted by `OrderService`, never by a view |
| IV — Payments are a Strategy | New method = one class + one registration | `IPaymentStrategy` + `PaymentStrategyResolver` + DI registration |
| V — TDTU layout | Reports match the measured standard | HTML/CSS renderer with the measured margins, TNR, roman front matter |
| VI — Evidence beats assertion | Test counts and screenshots from real runs | `dotnet test` output and Playwright artefacts archived in `docs/part3-qa/` |

No gate fails. No complexity waiver requested.

## Project Structure

### Documentation

```text
specs/001-saigonbite-platform/
├── spec.md            # requirements, ownership, BR matrix, ambiguity log
├── plan.md            # this file
├── tasks.md           # executable work items
├── data-model.md      # entities, relationships, constraints
├── research.md        # technical decisions and rejected alternatives
└── quickstart.md      # how to run
```

### Source code

```text
src/SaigonBite.Web/
├── Controllers/            # thin; no business rules
│   ├── AccountController.cs        (E — registration, login, language toggle)
│   ├── BrandsController.cs         (A)
│   ├── HubsController.cs           (B)
│   ├── VouchersController.cs       (C)
│   ├── OrdersController.cs         (D)
│   ├── DeliveriesController.cs     (F)
│   ├── ReportsController.cs        (R1, R2)
│   └── AdminController.cs          (dashboard, rain flag)
├── Domain/
│   ├── Pricing/
│   │   ├── PricingEngine.cs        # BR1–BR12, pure
│   │   ├── PriceContext.cs
│   │   └── PriceResult.cs
│   ├── Orders/
│   │   ├── OrderStateMachine.cs    # BR15, BR16
│   │   └── OrderStatus.cs
│   └── Payments/
│       ├── IPaymentStrategy.cs
│       ├── MomoStrategy.cs  VnPayStrategy.cs  ApplePayStrategy.cs
│       ├── PayPalStrategy.cs  CodStrategy.cs
│       └── PaymentStrategyResolver.cs
├── Services/               # orchestration, transactions, audit
├── Data/
│   ├── SaigonBiteDbContext.cs
│   ├── Configurations/     # EF entity configurations
│   └── Migrations/
├── Views/                  # Razor + Bootstrap 5, no logic beyond presentation
├── Resources/              # .resx for English and Vietnamese
└── wwwroot/

tests/
├── SaigonBite.UnitTests/           # pricing EP/BVA, state machine
└── SaigonBite.E2ETests/            # Playwright
```

**Structure decision**: classic three tiers — presentation (Controllers + Views), business
(Domain + Services), data (EF Core). The pricing engine and the state machine have no dependency on
EF or ASP.NET, so they are unit-testable in isolation, which is what makes the 20-case EP/BVA quota
cheap to satisfy.

## Phase Plan

| Phase | Content | Gate |
|---|---|---|
| 0 | Repository, configuration, spec artefacts | `git status` clean |
| 1 | Pricing engine + its 20 EP/BVA tests (test-first) | all boundary tests green |
| 2 | Domain model, EF Code-First migration, seed data | migration applies, seed loads |
| 3 | Order state machine + 5 illegal-transition tests | zero illegal transitions accepted |
| 4 | Payments Strategy + VNPay sandbox + mock gateway | new method added without touching existing classes |
| 5 | Use cases A, B, C, E, F — CRUD screens | each UC demonstrates create/read/update/delete |
| 6 | Use case D — cart, breakdown, checkout, tracking | worked example reproduces 205,000 |
| 7 | Reports R1, R2 + admin dashboard | totals correct on seeded data |
| 8 | i18n EN/VI, RBAC hardening | 390/768/1440 px verified, per-role tests green |
| 9 | Playwright E2E, performance measurement | NFR1 measured and recorded |
| 10 | Documents: Part 1 → Part 2 → Part 3 → Final | layout gates pass |

## Risks

| Risk | Mitigation |
|---|---|
| .NET SDK absent on this machine | Build and test inside `mcr.microsoft.com/dotnet/sdk:8.0`; the repo stays SDK-version-agnostic |
| SQL Server container heavy | SQLite for unit tests, SQL Server for the demo, EF provider swap in `Program.cs` |
| Pricing boundary mistakes | Write the 20 EP/BVA cases before the engine; the specification's own worked example is the first test |
| Rounding done twice | A single `RoundToThousand` call at step 9; a test asserts no intermediate rounding |
| Change Request arrives in Week 5 | The Strategy plus resolver makes it one class and one line; the impact note is prepared in advance |

## Verification

`dotnet build` clean · `dotnet test` green with counted cases · Playwright green · `verify-pdf.sh`
passes layout gates · RTM shows no orphan requirement.
