# Tasks: SaigonBite Platform

**Spec**: `spec.md` | **Plan**: `plan.md` | **Tier**: 4

Legend — owner: `T` = 524H0195 Ngô Lâm Tiến · `H` = 524H0191 Nguyễn Công Thành · `X` = third member
(`<TBD>`). `[P]` = can run in parallel with its neighbours.

## Phase 0 — Repository and specification (done)

- [x] **T000** `specify init`, `git init`, `.gitignore`, directory layout — T
- [x] **T001** `config/team.json` as the single source of people, dates and tier — T
- [x] **T002** Constitution `.specify/memory/constitution.md` (Principles I–VI) — T
- [x] **T003** `spec.md` — 46 FRs, 6 NFRs, ownership, BR matrix, 5 ambiguities — T
- [x] **T004** `plan.md` — stack, structure, phases, risks — T

## Phase 1 — Part 1 deliverable (deadline 7:00 Mon 26 Oct 2026)

- [ ] **T010** Render `docs/part1-proposal-req/SaigonBite_Part1.pdf` to the TDTU layout — T
- [ ] **T011** RTM seed: every FR → UC → design element → code component → test case — H
- [ ] **T012** Ambiguity log exported to Chapter 5 with the five adopted assumptions — T
- [ ] **T013** `slides/Part1_Pitch` — 5 slides, one speaking block per member — X
- [ ] **T014** Contribution statement draft and AI usage log — T
- [ ] **T015** Layout verification pass — covers, TOC, LOF, fonts, margins, page numbers — T

## Phase 2 — Pricing engine (BR1–BR12)

- [ ] **T020** `PriceContext` and `PriceResult` records — T
- [ ] **T021** Write the specification's worked example as the first failing test — T
- [ ] **T022** BR1 minimum order + boundary 49,999 / 50,000 — T
- [ ] **T023** BR2 coverage + boundary 8.0 / 8.01 — T
- [ ] **T024** BR3 delivery tiers + whole-km round-up, both discontinuities — T
- [ ] **T025** BR4 rush windows, inclusive start / exclusive end — T
- [ ] **T026** BR5 rain surcharge from the snapshot flag — T
- [ ] **T027** BR6 free delivery at 300,000, rain still charged — T
- [ ] **T028** BR7 Quiet Kitchen below 30 %, none at exactly 30 % — T
- [ ] **T029** BR9 voucher PERCENT / FIXED, cap, minimum subtotal against S — T
- [ ] **T030** BR10 nine-step order implemented literally — T
- [ ] **T031** BR11 single rounding at the end, halves up — T
- [ ] **T032** Extract `PricingEngine` as a pure static-free class; no `DbContext` in scope — T
- [ ] **T033** Count the EP/BVA cases and assert ≥ 20 in the test report — T

## Phase 3 — Data model

- [ ] **T040** Entities: User, profiles, Hub, Brand, MenuItem, Voucher, Order, OrderLine, OrderStatusHistory, PaymentRecord — H
- [ ] **T041** EF configurations, the customer discriminator, soft-delete query filters — H
- [ ] **T042** `SaigonBiteDbContext` + initial migration (Code-First) — H
- [ ] **T043** Seed data: 5 hubs, 3 brands per hub, ~60 items, 5 vouchers, one account per role — X
- [ ] **T044** `data-model.md` with the ERD and the constraints each entity carries — H

## Phase 4 — Order state machine (BR15, BR16)

- [ ] **T050** `OrderStatus` enum and the legal transition table — T
- [ ] **T051** `OrderStateMachine.CanTransition(from, to, actor)` — T
- [ ] **T052** Five illegal-transition tests, each asserting a domain exception — T
- [ ] **T053** `OrderStatusHistory` written on every accepted and rejected attempt — T
- [ ] **T054** Cancellation rules per BR16 and Ambiguity A5 — T

## Phase 5 — Payments (BR13, BR14)

- [ ] **T060** `IPaymentStrategy` with `Key`, `IsAvailableFor(actorType)`, `Charge(amount, ref)` — T
- [ ] **T061** `MomoStrategy`, `VnPayStrategy`, `ApplePayStrategy`, `PayPalStrategy`, `CodStrategy` — T
- [ ] **T062** `PaymentStrategyResolver` + DI registration — T
- [ ] **T063** BR14 COD ceiling at 1,000,000, applied to the rounded total — T
- [ ] **T064** VNPay sandbox integration behind configuration; mock gateway when keys absent — T
- [ ] **T065** `PaymentRecord` persisted per attempt with the strategy key and outcome — T

## Phase 6 — Use cases

- [ ] **T070** A — Brands & Menu CRUD, availability toggle, soft delete — H
- [ ] **T071** B — Hubs & Capacity CRUD, derived load, 90 % refusal — X
- [ ] **T072** C — Vouchers CRUD, one per order, validity window — T
- [ ] **T073** D — cart from one hub, line limits 1–30 and 1–20, price breakdown, checkout, tracking, edit while Placed — T
- [ ] **T074** E — registration for both customer types, simulated OTP and email code, deactivate — H
- [ ] **T075** F — shipper assignment, status advance, cash confirmation, failed delivery — X

## Phase 7 — Reports and dashboard

- [ ] **T080** R1 Revenue by brand category and payment method, excluding Cancelled and Failed — H
- [ ] **T081** R2 Hub utilization: orders, average Confirmed→Ready, load, Quiet Kitchen count — X
- [ ] **T082** Admin dashboard with Chart.js and both report tables — X
- [ ] **T083** Heavy-rain flag toggle — X

## Phase 8 — Quality

- [ ] **T090** English/Vietnamese resources and a persistent toggle — H
- [ ] **T091** Role-based authorisation on every controller action, plus one test per role — H
- [ ] **T092** Responsive verification at 390 / 768 / 1440 px — X
- [ ] **T093** Measure the 1.5 s performance target on a 30-line order and record the figure — T
- [ ] **T094** Playwright: local customer order to Delivered; tourist order to Delivered — T
- [ ] **T095** Test plan table with Test ID, input, expected, actual, pass/fail and FR/BR — all

## Phase 9 — Documents

- [ ] **T100** Part 2 — use case diagram with actor generalization — X
- [ ] **T101** Part 2 — use case specifications and sequence/activity diagrams — all
- [ ] **T102** Part 2 — order state diagram with actors — T
- [ ] **T103** Part 2 — CRC cards then class diagram / ERD showing the Strategy — H
- [ ] **T104** Part 2 — architecture diagram and quality-principle discussion — H
- [ ] **T105** Part 2 — interactive prototype and Figma import guide — X
- [ ] **T106** Part 3 — Change Request Impact Note, one page — X
- [ ] **T107** Part 3 — design justification: Part 2 diagrams versus delivered code — H
- [ ] **T108** Final — consolidated PDF with bookmarks and Lessons Learnt — T
- [ ] **T109** Final — video demo and narration script — T

## Dependencies

`T032` before `T033` · `T042` before every `T07x` · `T050–T051` before `T053` · `T060` before `T061`
(method per class) · `T083` before demonstrating BR5 · Phase 1 tests before Phase 2 implementation.

## Verification commands

```sh
dotnet test --logger "console;verbosity=normal"    # counts EP/BVA and invalid-transition cases
npx playwright test                                # end-to-end
bash scripts/verify-pdf.sh                         # layout gates
```
