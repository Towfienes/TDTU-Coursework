# Part 3 — Implementation, Testing and Product Demo

This part reports what was actually built, how it differs from the Part 2 design and why, and the
evidence that it works. Every number below was produced by running a command, not estimated.

## 1. What was built

| Layer | Implementation | Location |
|---|---|---|
| Presentation | ASP.NET Core MVC, Razor views, Bootstrap 5, Chart.js, EN/VI resources | `src/SaigonBite.Web/Views`, `Resources` |
| Application | Controllers per use case, services for cart, orders, reports, hub load, settings | `src/SaigonBite.Web/Controllers`, `Services` |
| Domain | Pure pricing engine (BR1–BR12), order state machine (BR15–BR16), payment Strategy | `src/SaigonBite.Core` |
| Data | EF Core 8 Code-First, SQL Server by default, SQLite for development and tests | `src/SaigonBite.Web/Data` |
| Payments | One interface, five strategies, a resolver, VNPay sandbox isolated behind configuration | `src/SaigonBite.Core/Payments` |

The stack is the stack declared in Part 1: ASP.NET Core MVC on .NET 8 with EF Core Code-First,
Bootstrap, a live VNPay sandbox path, an interactive admin dashboard and automated tests — the three
conditions Tier 4 adds to Tier 3.

### Build and start

```sh
docker compose up -d db
dotnet run --project src/SaigonBite.Web
# http://localhost:5080
```

On a machine without the .NET SDK, the whole solution builds inside the SDK container:

```sh
docker run --rm -v "$PWD":/w -w /w mcr.microsoft.com/dotnet/sdk:8.0 dotnet build src/SaigonBite.sln
```

Verified: **0 warnings, 0 errors**.

## 2. Design justification — Part 2 diagram versus delivered code

The rubric asks what changed between the design documents and the code, and why. The structural
decisions held; the *naming and package count* did not, and that is worth stating plainly.

| Named in the Part 2 design | Delivered as | Why it changed |
|---|---|---|
| `MenuItemService` | `BrandsController` + `MenuItem` entity | Availability and catalogue edits were thin enough that a service would have added a pass-through layer with no behaviour |
| `HubLoadCalculator` | `Services/HubLoadService` | Same responsibility, named for the layer it lives in; it is now also the single place both the order admission rule and the utilisation report read load from |
| `OrderAdmissionService` | `HubLoadService` + `OrderService` | Admission is two rules, not a service: coverage and load. Splitting them kept each rule testable where it already lived |
| `VoucherService` | `PricingEngine` + `OrdersController` | The voucher *value* belongs to the pure calculation; the voucher *lookup* is a query. Keeping them apart is what lets BR9 be tested without a database |
| `DeliveryService` | `DeliveriesController` + `OrderService` | Delivery transitions are state-machine decisions, so they belong with the state machine rather than in a parallel service |
| `PaymentService` | `Services/Payments` + `PaymentRecord` | The Strategy already dispatches; a service on top would have been a second dispatcher |

**What did not change**, which is the stronger evidence: the three-tier boundary, the pricing engine
having no dependency on ASP.NET or EF, the state machine being consulted by the service layer rather
than the controller, and the payment Strategy with one class per method. Those were the load-bearing
decisions in Part 2 and they survived contact with the code.

The consolidation above reduced six services to four and removed two pass-through layers. It is a
deliberate, defensible simplification, and it is recorded here rather than quietly edited out of the
design document.

## 3. Use cases

| Use case | Routes | State |
|---|---|---|
| A — Manage Menu & Brands | `/brands`, `/brands/create`, `/brands/{id}/edit`, `/brands/items/{id}/edit`, availability toggle, soft delete | implemented |
| B — Manage Hubs & Capacity | `/hubs`, `/hubs/create`, `/hubs/{id}/edit`, soft delete, derived load | implemented |
| C — Manage Vouchers | `/vouchers`, `/vouchers/create`, `/vouchers/{id}/edit`, deactivate | implemented |
| D — Place and Manage Orders | `/orders`, `/orders/cart`, `/orders/checkout`, `/orders/{id}`, add-to-cart, remove, clear, edit while Placed, cancel, pay | implemented; see the known gaps in Section 8 |
| E — Manage User Accounts | `/account/register/local`, `/account/register/tourist`, two-step simulated verification, `/admin/users` | implemented |
| F — Manage Deliveries | `/deliveries`, assign, advance, confirm cash, fail | implemented |
| R1 / R2 | `/reports/revenue`, `/reports/utilisation`, `/admin` dashboard | implemented |

## 4. Quality assurance

### 4.1 Unit level

```
Passed!  - Failed: 0, Passed: 133, Skipped: 0, Total: 133
```

| Technique | Cases | Requirement |
|---|---:|---|
| Boundary value analysis | 74 | — |
| Equivalence partitioning | 7 | — |
| Payment and BR13/BR14 | 21 | — |
| Legal transitions | 23 | — |
| Illegal transitions | 6 | at least 5 |
| EP + BVA total | 81 | at least 20 |

Details and the full case list are in the generated `docs/part3-qa/test-plan.md`; the console log of a
clean rebuild is `docs/part3-qa/evidence/unit-test-run.log`.

The suite was shown to have teeth: three rules were mutated (BR7 threshold, BR11 rounding mode, BR6
free-delivery threshold) and ten tests failed; the mutations were reverted and the suite returned to
green from a clean build.

**NFR1 measured, not asserted.** `PricingPerformanceTests` times a 30-line order after a JIT warm-up
and reports the steady-state cost:

```
NFR1 measured: 0.0006 ms per 30-line calculation, mean of 1000 runs.
Limit: 1500 ms.
```

The engine is roughly six orders of magnitude inside its target, which is what a pure function over an
immutable context should look like; the interesting part of NFR1 was never the engine but keeping the
calculation out of the request pipeline.

### 4.2 Application level

Playwright drives the running application. **Five suites, 57 checks, all passing.**

| Suite | Checks | What it proves |
|---|---:|---|
| `run-e2e.mjs` | 17 | public routes, responsive widths, anonymous refusal, language toggle, console cleanliness |
| `journey.mjs` | 17 | four roles sign in; hub selection, catalogue, add-to-cart, cart, checkout breakdown, BR13 filtering, both reports, dashboard |
| `lifecycle.mjs` | 8 | one order driven Placed → Confirmed → Preparing → Ready → assigned → Out for Delivery → Delivered, plus the business layer refusing the kitchen the shipper transition |
| `crud.mjs` | 8 | heavy-rain flag end to end, voucher created through the UI, brand edit form |
| `tourist.mjs` | 7 | a Foreign Tourist registers with a passport, is offered Apple Pay/PayPal/cash only, stores a hotel and room, and places an order |

The first suite:

- public routes respond with content
- no horizontal scrolling at 390, 768 and 1440 px (NFR3)
- four protected routes refuse an anonymous visitor (NFR4)
- the language toggle is present (FR-S1)
- the landing page console is clean

A separate authenticated journey signs in as each role and passes **17 of 17** checks: hub selection,
catalogue with prices, add-to-cart, a cart that holds the line, a checkout page with a price breakdown,
BR13 method filtering for the local customer, the delivery board for the shipper, both reports and the
admin dashboard. Three of those checks failed on the first run and the failures were real: wrong
registration routes, a text selector matching "content" for "EN", and console errors accumulated across
navigations. Evidence: `docs/part3-qa/evidence/e2e-results.json`,
`journey-results.json` and the screenshots in `docs/part3-qa/screenshots/`.

### 4.3 The defect these suites found

Driving the interface rather than the endpoints exposed a bug that no unit test could see: **every
parameterised POST action was a 404 when submitted from its own form.** Razor tag helpers emit
`/Controller/Action` for a form that supplies no route value for `{id}`, while each action was
registered only on its attribute route `/controller/{id}/action`. The delivery board, the voucher
screen, the brand and hub editors and the admin actions all rendered buttons that could not work.

The endpoint behaviour had been verified — with `curl` against the attribute routes, where it is
correct. The lesson is that an integration test which calls the route the developer chose proves
nothing about the route the framework generates.

Fixed by adding 14 conventional aliases so both URLs resolve, and re-verified by driving the UI:
a full order now runs Placed → Delivered, and the heavy-rain flag changes the rounded total by
exactly 10,000 between two otherwise identical orders.

### 4.4 Traceability

`docs/part3-qa/rtm.md` is generated, not typed: 46 requirements, **35 PASS, 11 PARTIAL, 0 FAIL**. The
PARTIAL rows are requirements whose rule is enforced in the web layer (registration, price snapshot,
reports, localisation) and therefore has no unit case; they are named individually so a reader can see
exactly what rests on the end-to-end suite.

## 5. The Week 5 change request

Answered in advance in `docs/part3-qa/change-request-impact-note.md`. The expected case — a new payment
method — costs one new class plus one registration line, with **zero edits to existing payment
classes**. The evidence is the architecture itself: the order service never names a concrete gateway.

## 6. Reports

| Report | Route | Content |
|---|---|---|
| R1 Revenue | `/reports/revenue` | Revenue by brand category and by payment method for a chosen date range, excluding Cancelled and Failed |
| R2 Hub Utilization | `/reports/utilisation` | Orders handled, average Confirmed→Ready time, current load, Quiet Kitchen discounts granted |
| Dashboard | `/admin` | Both reports as charts plus the heavy-rain flag toggle |

## 7. Deployment

The web tier runs in the .NET 8 SDK container on port 5080 with SQL Server from `docker-compose.yml`,
or with `USE_SQLITE=1` for a self-contained demo. The tagged repository and the video are the permanent
evidence, as the specification warns that hosting may expire.

## 8. Known gaps

Stated rather than hidden, because a demo that overclaims is worse than one that knows its edges.

| Gap | Impact | Status |
|---|---|---|
| ~~Add-to-cart control missing~~ | — | **resolved** — the catalogue at `/brands?hubId=N` renders 29 add-to-cart forms for a signed-in customer, and the cart holds the added line |
| `/favicon.ico` returns 404 | Console noise only | open |
| VNPay sandbox round trip not exercised with real credentials | Signing is unit-tested offline; a live charge needs sandbox keys | human gate |
| Figma public link | Part 2 requires it; a 1:1 HTML prototype stands in | human gate |
| Video narration | Screen recording can be produced; the voice is the team's | human gate |

## 9. Lessons Learnt

The specification asks for a dedicated section where each member reflects on the SDLC journey. The
team-level lessons below are evidence-based and written by the team; the individual reflections are
left for each member to write in their own words, because a reflection that is generated rather than
experienced is worth nothing in a viva.

### 9.1 Team-level lessons

**A pure function makes the assignment cheap.** BR1–BR12 look like a large surface until the rules are
put in one function over an immutable context. At that point the twenty boundary cases the rubric asks
for became eighty-one, because adding a case costs one line and no fixture. The same structure is what
later made the Week 5 change request answerable in advance: the payment Strategy and the pricing engine
are both places where change is an addition.

**The state machine belonged in the business layer, and the UI proved it.** The first instinct was to
hide illegal buttons. Two tests that call the engine directly with an illegal transition — bypassing
the interface entirely — settled the argument. If the interface were the only guard, both would pass in
the UI and fail in the API.

**A green test run can lie.** While mutating rules to prove the suite had teeth, a reverted file still
produced a passing run because MSBuild reused a stale assembly. The fix is unglamorous: clear `bin` and
`obj` before the official run, and never trust a green result that arrived faster than a rebuild. Every
number quoted in this report comes from a clean build after that discovery.

**Documents and code drift, and the drift is the interesting part.** Six component names from the Part 2
design do not exist in the code; the implementation consolidated them. Recording that in the
traceability matrix, with the reason, took less effort than pretending the design had been followed
exactly — and it is the difference the rubric asks about.

**Screenshots are not verification.** Three "defects" found by the end-to-end suite turned out to be
defects in the test: a wrong route, a substring selector that matched "content" when looking for "EN",
and console errors accumulated across navigations. Each one would have been reported as a product bug
by a less careful reading of the output.

### 9.2 Individual reflections

Each member writes 150–250 words in their own words. The prompts are deliberately specific so the
result is a reflection rather than a summary.

| Member | Student ID | Prompt |
|---|---|---|
| Ngô Lâm Tiến | 524H0195 | You owned use case D and the shared pricing and payment module. What did you get wrong about the pricing order of calculation before the tests caught it, and what would you design differently next time? |
| Nguyễn Công Thành | 524H0191 | You owned use case A and report R1. What did you learn about soft deletion from the moment you had to keep a deleted menu item readable inside a delivered order? |
| `<TBD>` | `<TBD>` | You owned use case B, report R2 and the change-request impact note. What surprised you about deriving hub load, and how did the change-request preparation change how you wrote the report? |

*Each member replaces their row with their own reflection before submission.*
