# Feature Specification: SaigonBite Platform

**Feature Branch**: `001-saigonbite-platform`
**Created**: 2026-10-23
**Status**: Draft (Part 1 baseline)
**Input**: Three course documents — `SE_FP_SaigonBite_CaseStudy_Sem01_2627.pdf`,
`SE_FinalProject_Requirements_SaigonBite_Sem01_2627.pdf`,
`SE_FP_SaigonBite_StudentSurvivalGuide_Sem01_2627.pdf`

Constitution: `.specify/memory/constitution.md` (Principles I–VI are binding).

---

## User Scenarios & Testing

### User Story 1 - A local customer orders lunch from a quiet hub (Priority: P1)

A customer registers with a Vietnamese mobile number, picks a hub in District 1, builds an order from
one brand, sees an itemised price that includes the Quiet Kitchen discount and the delivery fee, pays
by MoMo, and tracks the order until it is delivered.

**Why this priority**: this is the end-to-end spine of the product. Every business rule in BR1–BR12
is exercised, and no other story can be demonstrated without it.

**Independent Test**: place one order at a hub at 20 % load, 3.2 km, 15:00, rain off, no voucher —
the worked example of the specification must return S = 200,000, Q = 20,000 and total = 205,000.

**Acceptance Scenarios**:

1. **Given** a hub at 20 % load and a subtotal of 200,000, **When** the order is placed at 15:00,
   **Then** the Quiet Kitchen discount is 20,000 and the rounded total is 205,000 (BR7, BR10, BR11).
2. **Given** a subtotal of 49,999, **When** the customer submits, **Then** the order is rejected with
   the minimum-order message (BR1).
3. **Given** a subtotal of exactly 300,000, **When** the order is placed, **Then** delivery fee and
   rush surcharge are waived while the rain surcharge still applies (BR6).

---

### User Story 2 - A foreign tourist orders to a hotel (Priority: P1)

A tourist registers with a passport number, nationality and email, verifies with a simulated email
code, orders to a hotel name and room number, and pays with Apple Pay or PayPal.

**Why this priority**: actor generalization and the Strategy pattern are separately graded; this story
is the only one that proves both.

**Independent Test**: register a tourist with passport `B1234567`, place an order, and confirm that
MoMo and VNPay are refused for that actor while Apple Pay and PayPal are offered.

**Acceptance Scenarios**:

1. **Given** a tourist account, **When** the payment list renders, **Then** it contains Apple Pay,
   PayPal and Cash on Delivery, and does not contain MoMo or VNPay (BR13).
2. **Given** a passport of 5 characters, **When** registration is submitted, **Then** it is rejected
   (BR18).
3. **Given** a hotel delivery address, **When** the order is placed, **Then** the hotel name and room
   are stored on the order and shown to the shipper.

---

### User Story 3 - Kitchen staff and shipper drive the order to Delivered (Priority: P1)

Kitchen staff confirm and prepare an order at their own hub, mark it ready, a shipper takes it, and on
a COD order the shipper must confirm cash collected before the order can become Delivered.

**Why this priority**: the state machine (BR15) and the COD rule (BR14) carry their own rubric lines
and their own invalid-transition test quota of five cases.

**Independent Test**: attempt `Placed → Preparing` directly and confirm the business layer rejects it
even though the UI never offers it.

**Acceptance Scenarios**:

1. **Given** an order in `Placed`, **When** kitchen staff confirm it, **Then** state becomes
   `Confirmed` and an `OrderStatusHistory` row is written (BR15, NFR5).
2. **Given** a COD order in `Out for Delivery` with cash not confirmed, **When** the shipper marks it
   delivered, **Then** the transition is rejected (BR14).
3. **Given** an order in `Preparing`, **When** the customer requests cancellation, **Then** it is
   refused because cancellation is only allowed in `Placed` or `Confirmed` (BR16).

---

### User Story 4 - The operator sees where the kitchens are overloaded (Priority: P2)

An admin opens the dashboard, reads the Revenue report by brand category and payment method for a
date range, and reads the Hub Utilization report with orders handled, average preparation time,
current load and the number of Quiet Kitchen discounts granted.

**Why this priority**: the case study makes two reports mandatory and Tier 4 makes the dashboard
interactive, but neither blocks the ordering spine.

**Independent Test**: seed one cancelled order and confirm it is excluded from the revenue totals.

**Acceptance Scenarios**:

1. **Given** a date range containing two delivered and one cancelled order, **When** revenue is
   reported, **Then** only the two delivered orders are counted (R1).
2. **Given** a hub with three orders that moved Confirmed → Ready, **When** utilization is reported,
   **Then** the average preparation time is the mean of those three intervals (R2).

---

### User Story 5 - An admin curates brands, hubs and vouchers (Priority: P2)

The admin creates a hub with a kitchen capacity, adds brands and menu items, toggles item
availability, and issues a percentage voucher with a cap and a minimum subtotal.

**Why this priority**: CRUD completeness is graded per student, but the domain works with seeded data
while these screens are still being built.

**Independent Test**: soft-delete a menu item that appears in a delivered order and confirm the order
history and the revenue report are unchanged.

**Acceptance Scenarios**:

1. **Given** an item referenced by a delivered order, **When** it is deleted, **Then** it is flagged
   inactive and the order still renders its name and price (soft delete).
2. **Given** a voucher with a minimum subtotal of 100,000, **When** an order of 90,000 applies it,
   **Then** the voucher is refused (BR9).

---

### Edge Cases

- Hub load exactly 30 % → no Quiet Kitchen discount (BR7 boundary).
- Hub load exactly 90 % → new orders refused (BR8 boundary).
- Distance exactly 8.0 km accepted, 8.01 km rejected (BR2).
- Delivery 2.01 km counts as one extra kilometre above 2 km (BR3).
- Order placed at 13:00 exactly → no rush surcharge, the window is end-exclusive (BR4).
- Rounded total exactly 1,000,000 → COD allowed; 1,001,000 → COD refused (BR14).
- Raw total 64,950 → rounds to 65,000; no intermediate rounding (BR11).
- An order edited after placement re-prices with the stored snapshot, not current conditions (BR17).
- A hub whose capacity would make load divide by zero is rejected at creation.

---

## Requirements

Generated baseline: `config/part1.json` (24 October 2026). All verification below is planned for Part 3.

### Functional Requirements

- **FR-A1**: The system shall let an administrator create a brand (name, description, operating hubs) and create its menu items (name, category, positive VND price, brand and availability). (BR12). UC A; owner 524H0191.
- **FR-A2**: The system shall let any visitor view brands and menu items filtered by hub and by category. (BR12). UC A; owner 524H0191.
- **FR-A3**: The system shall let an administrator edit brand details and a menu item’s name, category, price and brand. (BR12). UC A; owner 524H0191.
- **FR-A4**: The system shall soft-delete brands and menu items, so that historical orders and reports keep their names and prices. (BR12). UC A; owner 524H0191.
- **FR-A5**: The system shall let an administrator set item availability; unavailable or inactive items shall not be orderable. (BR12). UC A; owner 524H0191.
- **FR-A6**: The system shall reject any order line whose item belongs to a brand the chosen hub does not operate. (BR12). UC A; owner 524H0191.
- **FR-B1**: The system shall let an administrator create a hub with a district, an address and a whole-number kitchen capacity greater than zero. (BR8). UC B; owner 524H0179.
- **FR-B2**: The system shall display hub load as 100 times the count of Confirmed or Preparing orders divided by positive integer kitchen capacity; the new order is not counted. (BR8). UC B; owner 524H0179.
- **FR-B3**: The system shall let an administrator edit a hub’s district, address and positive integer capacity, and recompute displayed load after a capacity change. (BR8). UC B; owner 524H0179.
- **FR-B4**: The system shall soft-delete a hub, removing it from ordering while preserving its historical orders and report rows. (BR8). UC B; owner 524H0179.
- **FR-B5**: The system shall refuse a new order when the chosen hub’s load is 90 % or above and shall ask the customer to choose another hub. (BR8). UC B; owner 524H0179.
- **FR-C1**: The system shall let an administrator create a voucher with a code, a type (PERCENT or FIXED), a value, a maximum discount, a minimum subtotal, validity dates and an active flag. (BR9). UC C; owner 524H0195.
- **FR-C2**: The system shall let an administrator view, edit and deactivate vouchers. (BR9). UC C; owner 524H0195.
- **FR-C3**: The system shall accept at most one active voucher within its validity dates and check its minimum-subtotal condition against S before discounts. (BR9). UC C; owner 524H0195.
- **FR-D1**: The system shall let a customer build an order from the menus of one hub, with 1 to 30 lines and a quantity of 1 to 20 per line. (BR12). UC D; owner 524H0195.
- **FR-D2**: The system shall reject an order whose item subtotal is below 50,000. (BR1). UC D; owner 524H0195.
- **FR-D3**: The system shall reject an order whose delivery distance exceeds 8.0 km. (BR2). UC D; owner 524H0195.
- **FR-D4**: The system shall charge D = 15,000 for d ≤ 2 km; 15,000 + 5,000 × ceil(d − 2) for 2 < d ≤ 5; and 30,000 + 7,000 × ceil(d − 5) for 5 < d ≤ 8. (BR3). UC D; owner 524H0195.
- **FR-D5**: The system shall charge R = 20% of non-waived D when placement time in Vietnam (UTC+7) is in [11:00, 13:00) or [17:30, 19:30); otherwise R = 0. (BR4). UC D; owner 524H0195.
- **FR-D6**: The system shall add a flat 10,000 rain surcharge while the administrator’s heavy-rain flag is on, using the flag value snapshotted on the order. (BR5). UC D; owner 524H0195.
- **FR-D7**: The system shall waive the delivery fee and the rush surcharge when the item subtotal is 300,000 or more, while the rain surcharge still applies. (BR6). UC D; owner 524H0195.
- **FR-D8**: The system shall apply a Quiet Kitchen discount of 10 % of the item subtotal when the hub load at placement is below 30 %. (BR7). UC D; owner 524H0195.
- **FR-D9**: The system shall calculate PERCENT voucher V on S − Q, limited by the voucher cap and S − Q; FIXED V shall not exceed S − Q. (BR9). UC D; owner 524H0195.
- **FR-D10**: The system shall calculate S, Q, V, F = S − Q − V, D, R, R2 and raw total = F + D + R + R2 in BR10 order, retain fractional values without intermediate rounding or truncation, then round once to the nearest 1,000 VND, half up. (BR10, BR11). UC D; owner 524H0195.
- **FR-D11**: The system shall show an itemised price breakdown — subtotal, Quiet Kitchen discount, voucher, food total, delivery fee, rush surcharge, rain surcharge, rounded total — before payment. (BR10). UC D; owner 524H0195.
- **FR-D12**: The system shall allow items to be edited only while the order is Placed, and any recalculation shall reuse the stored placement snapshot. (BR17). UC D; owner 524H0195.
- **FR-D13**: The system shall allow Customer cancellation in Placed or Confirmed, Kitchen Staff rejection in Placed with a reason, and Admin cancellation in Confirmed; online-paid cancellations shall be refunded in full (simulated). (BR16). UC D; owner 524H0195.
- **FR-D14**: The system shall store a price snapshot of timestamp, hub load and rain flag at placement so that the price stays reproducible. (BR17). UC D; owner 524H0195.
- **FR-E1**: The system shall register a Local Customer with a Vietnamese mobile number of exactly ten digits starting 03, 05, 07, 08 or 09, and a simulated OTP. (BR18). UC E; owner 524H0191.
- **FR-E2**: The system shall register a Foreign Tourist with a passport number of 6 to 9 letters or digits, a nationality, a valid email and a simulated email code. (BR18). UC E; owner 524H0191.
- **FR-E3**: The system shall enforce a unique identifier and a password of at least eight characters stored as a hash. (BR18). UC E; owner 524H0191.
- **FR-E4**: The system shall store both customer types in one schema using a discriminator, and let an administrator view, edit and deactivate accounts. (BR18). UC E; owner 524H0191.
- **FR-F1**: The system shall let an administrator assign an available shipper to a Ready order and record the shipper and assignment time (assumption A1). (BR15). UC F; owner 524H0179.
- **FR-F2**: The system shall enforce all eight transitions and actor/condition constraints in Specification section 2C in the business layer and reject every other transition; Delivered, Cancelled and Failed are terminal. (BR15). UC F; owner 524H0179.
- **FR-F3**: The system shall require a shipper to confirm cash collected before a COD order may become Delivered. (BR14). UC F; owner 524H0179.
- **FR-F4**: The system shall let the assigned shipper move Out for Delivery to terminal Failed when the customer is unreachable, recording a reason; financial settlement follows assumption A2. (BR15, BR16). UC F; owner 524H0179.
- **FR-P1**: The system shall offer only the payment methods that belong to the customer’s actor group: MoMo, VNPay and cash for Local Customers; Apple Pay, PayPal and cash for Foreign Tourists. (BR13). UC D; owner 524H0195.
- **FR-P2**: The system shall refuse Cash on Delivery when the rounded total exceeds 1,000,000. (BR14). UC D; owner 524H0195.
- **FR-P3**: The system shall record each payment attempt with order, selected method, timestamp and success/failure outcome; only an actor-permitted Strategy may be selected. (BR13). UC D; owner 524H0195.
- **FR-P4**: The system shall integrate the live VNPay sandbox API for eligible Local Customer orders, authenticate callbacks and validate the order and amount before recording success, and process repeated callbacks idempotently. (Tier 4 instructor table; BR13). UC D; owner 524H0195.

- **FR-R1**: The system shall produce a Revenue report for a chosen date range showing total revenue by brand category and by payment method, excluding Cancelled and Failed orders. (R1). UC A; owner 524H0191.
- **FR-R2**: The system shall produce a Hub Utilization report showing, per hub, orders handled, average preparation time from Confirmed to Ready, current load percentage and the number of Quiet Kitchen discounts granted. (R2). UC B; owner 524H0179.
- **FR-S1**: The system shall let any user switch the interface between English and Vietnamese, and the choice shall persist for the session. (NFR3). UC E; owner 524H0191.
- **FR-S2**: The system shall restrict each role to its own functions on the server, not only in the interface. (NFR4). UC E; owner 524H0191.
- **FR-S3**: The system shall provide an interactive administrator dashboard for R1 and R2 with revenue date-range and hub-selection controls that refresh the respective charts and tables from the same authorised report data. (Tier 4 instructor table; R1, R2). UC A/B; owner 524H0191 / 524H0179.
- **FR-S4**: The system shall let an administrator toggle the heavy-rain flag that the rain surcharge depends on. (BR5). UC D; owner 524H0195.
- **FR-S5**: The system shall append an audit record for each status change (actor, timestamp, old/new state) and payment attempt (actor, timestamp, method, outcome), without an application-level edit/delete operation. (BR15, NFR5). UC D; owner 524H0195.

### Quality Attributes (NFRs)

- **NFR1** (Performance): Price calculation for a valid order of 30 lines completes in under 1.5 seconds server-side. Source: Case Study section 4B; BR12. Planned check: Time the engine with 30 valid lines on the documented test machine; record environment, elapsed times and pass/fail in Part 3.
- **NFR2** (Maintainability): Use MVC separation. Adding a payment method requires one new Strategy class and one registration, with zero edits to existing payment classes. Source: Case Study section 4B; BR13. Planned check: Add a sample method in a disposable branch; inspect the diff and rerun existing payment tests. This criterion applies to a payment-extension change request.
- **NFR3** (Usability): All required screens support English/Vietnamese and operate without horizontal page scrolling at 390, 768 and 1440 px; culture switching preserves the cart and session. Source: Case Study section 4B. Planned check: Check each screen and language at the three widths, verify resource keys and repeat switching with a non-empty cart.
- **NFR4** (Security): Passwords are hashed, never stored as plaintext; every role is refused every server action outside its authorised role and resource scope. Source: Case Study section 4B; BR18. Planned check: Inspect stored password representation; run an access matrix for both customer types, Kitchen Staff, Shipper and Admin, including other users’ orders and hubs.
- **NFR5** (Auditability): 100% of accepted status changes and payment attempts append a record with actor and timestamp; status changes include old/new state, payment attempts include method/outcome. No application update/delete endpoint is provided. Source: Team-defined; BR15; R2. Planned check: Reconcile accepted transitions and payment attempts against audit rows and verify ordinary roles cannot change recorded history.
- **NFR6** (Reliability): Zero forbidden transitions are accepted; repeated pricing with identical lines and the stored placement snapshot returns identical components and rounded total. Source: Team-defined; BR10, BR11, BR15, BR17. Planned check: Enumerate the state/actor matrix, include at least five forbidden transitions, and repeat boundary pricing inputs against a fixed snapshot.

### Key Entities

- **User** — one row per person, with a `CustomerType` discriminator (`Local`, `Tourist`, `Staff`,
  `Shipper`, `Admin`) plus `LocalCustomerProfile` (mobile) and `TouristProfile` (passport,
  nationality, email). Passwords hashed.
- **Hub** — district, address, `KitchenCapacity` (whole number ≥ 1), derived load; soft-deletable.
- **Brand** — name, description, many-to-many with Hub; soft-deletable.
- **MenuItem** — brand, category, price, `IsAvailable`; soft-deletable.
- **Voucher** — code, type, value, `MaxDiscount`, `MinSubtotal`, validity window, active flag.
- **Order** — customer, hub, lines, status, price snapshot (timestamp, hub load, rain flag), applied
  discounts and fees, payment record, assigned shipper; soft-delete never applies — orders are never
  deleted.
- **OrderLine** — menu item snapshot (name, unit price), quantity 1–20.
- **OrderStatusHistory** — order, actor, from state, to state, timestamp, reason.
- **PaymentRecord** — order, strategy key, amount, gateway reference, outcome.

---

## Use Case Ownership (TDTU Part 1)

- Ngô Lâm Tiến (524H0195): main UC D — Place and Manage Orders; secondary: C - Manage Vouchers; Pricing Engine (BR1-BR12); Payment Strategy Module; reports: none.
- Nguyễn Công Thành (524H0191): main UC A — Manage Menu & Brands; secondary: E - Manage User Accounts; reports: R1 - Revenue Report.
- Nguyễn Trọng Phú (524H0179): main UC B — Manage Hubs & Capacity; secondary: F - Manage Deliveries; Change Request Impact Note; reports: R2 - Hub Utilization Report.

## Requirement → Business Rule Matrix

| FR | Use case | Rules | Report | Planned design | Planned component | Planned tests |
|---|---|---|---|---|---|---|
| FR-A1 | A | BR12 | — | Brand entity, menu admin | BrandsController | TC-A-01 |
| FR-A2 | A | BR12 | — | Catalogue view | BrandsController | TC-A-02 |
| FR-A3 | A | BR12 | — | Menu edit form | BrandsController | TC-A-03 |
| FR-A4 | A | BR12 | — | Soft-delete filter | DbContext filters | TC-A-04 |
| FR-A5 | A | BR12 | — | Availability flag | MenuItemService | TC-A-05 |
| FR-A6 | A | BR12 | — | Hub-brand relation | OrderService | TC-A-06 |
| FR-B1 | B | BR8 | — | Hub entity | HubsController | TC-B-01 |
| FR-B2 | B | BR8 | — | Derived load | HubLoadCalculator | TC-B-02 |
| FR-B3 | B | BR8 | — | Capacity edit | HubsController | TC-B-03 |
| FR-B4 | B | BR8 | — | Soft-delete filter | DbContext filters | TC-B-04 |
| FR-B5 | B | BR8 | — | Admission rule | OrderAdmissionService | TC-B-05 |
| FR-C1 | C | BR9 | — | Voucher entity | VouchersController | TC-C-01 |
| FR-C2 | C | BR9 | — | Voucher admin | VouchersController | TC-C-02 |
| FR-C3 | C | BR9 | — | Voucher validation | VoucherService | TC-C-03 |
| FR-D1 | D | BR12 | — | Cart, line limits | OrdersController | TC-D-01 |
| FR-D2 | D | BR1 | — | Minimum order | PricingEngine | TC-D-02, 03 |
| FR-D3 | D | BR2 | — | Coverage check | PricingEngine | TC-D-04, 05 |
| FR-D4 | D | BR3 | — | Distance tiers | PricingEngine | TC-D-06…08 |
| FR-D5 | D | BR4 | — | Rush windows | PricingEngine | TC-D-09…11 |
| FR-D6 | D | BR5 | — | Rain surcharge | PricingEngine | TC-D-12, 13 |
| FR-D7 | D | BR6 | — | Free-delivery waiver | PricingEngine | TC-D-14, 15 |
| FR-D8 | D | BR7 | — | Quiet Kitchen rule | PricingEngine | TC-D-16, 17 |
| FR-D9 | D | BR9 | — | Voucher application | PricingEngine | TC-D-18…20 |
| FR-D10 | D | BR10, BR11 | — | Nine-step order | PricingEngine | TC-D-21, 22 |
| FR-D11 | D | BR10 | — | Breakdown view | OrdersController | TC-D-23 |
| FR-D12 | D | BR17 | — | Edit while Placed | OrderService | TC-D-24 |
| FR-D13 | D | BR16 | — | Cancellation rules | OrderStateMachine | TC-D-25, 26 |
| FR-D14 | D | BR17 | — | Price snapshot | Order entity | TC-D-27 |
| FR-E1 | E | BR18 | — | Local validation | AccountController | TC-E-01, 02 |
| FR-E2 | E | BR18 | — | Tourist validation | AccountController | TC-E-03, 04 |
| FR-E3 | E | BR18 | — | Hash + uniqueness | AccountService | TC-E-05 |
| FR-E4 | E | BR18 | — | Discriminator schema | DbContext | TC-E-06 |
| FR-F1 | F | BR15 | — | Shipper assignment | DeliveriesController | TC-F-01 |
| FR-F2 | F | BR15 | — | State machine | OrderStateMachine | TC-F-02, 03 |
| FR-F3 | F | BR14 | — | Cash confirmation | DeliveryService | TC-F-04 |
| FR-F4 | F | BR15, BR16 | — | Failure path | DeliveryService | TC-F-05 |
| FR-P1 | D | BR13 | — | Actor-method map | PaymentStrategyResolver | TC-P-01, 02 |
| FR-P2 | D | BR14 | — | COD ceiling | CodStrategy | TC-P-03 |
| FR-P3 | D | BR13 | — | Payment record | PaymentService | TC-P-04 |
| FR-P4 | D | Tier 4 instructor table; BR13 | — | Sandbox adapter and callback validation | VnPayStrategy / PaymentService | TC-P-05–09 |
| FR-R1 | A | R1 | R1 | Revenue aggregation | ReportService | TC-RT-01, 02 |
| FR-R2 | B | R2 | R2 | Utilisation aggregation | ReportService | TC-RT-03, 04 |
| FR-S1 | E | NFR3 | — | Resource files | Localisation | TC-S-01 |
| FR-S2 | E | NFR4 | — | Authorisation policy | Policies | TC-S-02 |
| FR-S3 | A/B | Tier 4 instructor table; R1, R2 | R1, R2 | Dashboard | AdminController | TC-S-03a–c |
| FR-S4 | D | BR5 | — | Rain flag | AdminController | TC-S-04 |
| FR-S5 | D | BR15, NFR5 | — | Audit writer | OrderStatusHistory | TC-S-05 |

NFR mappings and verdicts: see Chapter 6 of the generated Part 1 PDF; all six NFRs have planned checks.

## Ambiguity Log

### A1 — Shipper assignment

Gap: Section 2C leaves the assignment mechanism open.

Assumption: An Admin manually selects an available shipper for a Ready order. The system stores assignment time and shipper. Automatic dispatch is outside the initial scope.

Impact: FR-F1; UC F; assignment screen and service.

Instructor answer: Not asked; working assumption pending instructor review.

### A2 — Settlement after Failed delivery

Gap: Section 2C leaves the financial result of Failed delivery open.

Assumption: Refund online-paid orders in full in the simulated ledger; collect no COD cash. Preserve Failed as its own terminal state and exclude it from R1 revenue.

Impact: FR-F4; UC F/D; payment/refund policy and R1.

Instructor answer: Not asked; working assumption pending instructor review.

### A3 — Tourist delivery address

Gap: Hotel and room are allowed, but a field structure is not prescribed.

Assumption: Store street/address text plus optional hotel name and room. Require a usable delivery address for either customer type; tourists are not required to supply a Vietnamese phone.

Impact: FR-E2 and FR-D1; address validation and checkout.

Instructor answer: Not asked; working assumption pending instructor review.

### A4 — Invalid voucher user flow

Gap: BR9 specifies eligibility but not whether a refused voucher should block the whole order.

Assumption: Show the refusal and the corrected breakdown with V=0; require the customer to review and confirm that total before placing the order. Never silently submit a higher total.

Impact: FR-C3 and FR-D9/D11; checkout confirmation.

Instructor answer: Not asked; working assumption pending instructor review.

### A5 — Catalogue price change before a Placed edit

Gap: BR17 fixes timestamp/load/rain but does not explicitly say which item prices apply when the catalogue changes before an edit.

Assumption: Existing lines retain their recorded unit prices; newly added items use the current catalogue price after availability/membership validation. Recalculation still uses the original timestamp, load and rain snapshot.

Impact: FR-D12/D14 and FR-A4; order-line price storage and edit tests.

Instructor answer: Not asked; working assumption pending instructor review.

## Success Criteria

- **SC-001**: The worked example of the specification (S = 200,000, load 20 %, 3.2 km, 15:00, rain
  off, no voucher) reproduces Q = 20,000, D = 25,000 and a rounded total of 205,000.
- **SC-002**: At least 20 equivalence-partitioning and boundary-value test cases cover every numeric
  threshold in BR1–BR12 and BR14, and at least 5 test cases attempt an illegal state transition and
  are rejected.
- **SC-003**: A Local Customer and a Foreign Tourist each complete a full order to `Delivered` in one
  automated end-to-end run.
- **SC-004**: Both mandatory reports return correct totals for a seeded data set within one second.
- **SC-005**: A new payment method can be added by creating one class and one registration line,
  demonstrated by a payment-extension experiment (or a matching Week 5 change request) with zero edits to existing payment classes.

## Assumptions

- Distance between hub and delivery address is stored on the order (simulated, not geocoded).
- Payments are simulated against a mock gateway, except the VNPay sandbox path required by Tier 4.
- OTP and email verification codes are simulated and displayed in the development UI.
- One order belongs to exactly one hub and may contain items from several brands that hub operates.
- Time is Vietnam local time (UTC+7); money is VND; fractional intermediates are retained and only the final rounded total is a whole multiple of 1,000.
- The heavy-rain flag is global for the platform, snapshotted per order at placement.

## Instructor technology-tier update — 24 October 2026

Source: `docs/references/instructor-technology-tiers.png`. The screenshot has no publication date. Maximum scores are ceilings, not awarded marks.

| Tier | Ceiling /10 | Required stack |
| --- | ---: | --- |
| Tier 1 | 7.0 | C# WinForms + local SQL database / Excel. 3-Tier architecture. |
| Tier 1B | 7.5 | Core PHP (or CodeIgniter) + MySQL + Bootstrap. MVC architecture. |
| Tier 2 | 8.5 | ASP.NET Web Forms/MVC (Database First) + SQL Server + Bootstrap. MVC. |
| Tier 3 | 9.5 | ASP.NET MVC (Code First) + Entity Framework + Bootstrap. MVC. |
| Tier 4 | 10.0 | Tier 3 plus live sandbox API, interactive Admin dashboard and automated tests. |

Target: Tier 4 (10.0 ceiling), retaining the Tier 3 foundation plus all three additions. The current ASP.NET Core MVC / EF Core variant needs instructor confirmation because the source names ASP.NET MVC / Entity Framework. No approval is inferred.

- **Tier 3 foundation** — ASP.NET Core MVC, EF Core Code-First migrations, SQL Server and Bootstrap 5. Retain the MVC layers; confirm the Core variant with the instructor because the table names ASP.NET MVC. Owner: 524H0191. Evidence: Part 2 architecture/ERD and migration design; Part 3 reproducible SQL Server setup, migration history and complete CRUD demonstration. SQLite is a local fallback, not the submitted database baseline. Trace: UC A/B/D; NFR3/4. Status: Planned.
- **Live sandbox API** — Use the VNPay sandbox for actor-eligible orders. Validate callbacks and order/amount; prevent duplicate settlement. Keep mock payments explicitly labelled. Owner: 524H0195. Evidence: Part 3 redacted provider transaction IDs and callback logs for success, cancellation/failure, invalid signature and repeated callback; automated TC-P-05–09. Credentials are excluded. Mock-only evidence does not meet this criterion. Trace: FR-P1/P3/P4; FR-S5. Status: Planned.
- **Interactive Admin dashboard** — Provide R1 Revenue and R2 Hub Utilization with charts and tables. Revenue date-range and hub-selection controls refresh their respective views from authorised server data. Owner: 524H0191 / 524H0179. Evidence: Part 2 dashboard prototype; Part 3 recorded filter interaction, chart/table reconciliation against seeded data, and denied non-Admin access. Automated TC-S-03a–c. Trace: FR-R1/R2; FR-S2/S3. Status: Planned.
- **Automated tests** — Run unit tests for pricing/state rules and integration/E2E tests for orders, sandbox callbacks and the Admin dashboard. Cover at least 20 EP/BVA cases and five forbidden transitions. Owner: 524H0195 / 524H0191 / 524H0179. Evidence: Part 3 versioned commands and fixtures, commit identifier and execution reports with counts and PASS/FAIL outcomes. Planned test IDs and screenshots alone do not establish execution. Trace: RTM; TC-P-05–09; TC-S-03a–c. Status: Planned.
