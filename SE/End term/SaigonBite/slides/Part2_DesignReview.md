# Presentation 2 — Design Review (7–10 minutes)

Course requirement: a 7–10 minute walkthrough of the CRC cards, the database logic and the Figma
prototype. Every member speaks and answers at least one individual question about their own use case.

Target: **9 minutes** with 30 seconds of buffer. Three speakers, three blocks.

## Slide plan

| # | Slide | Speaker | Time |
|---|---|---|---|
| 1 | Title, tier, what changed since Part 1 | 524H0195 | 0:00–0:30 |
| 2 | Use case diagram with actor generalisation | `<TBD>` | 0:30–1:45 |
| 3 | Order state machine, eight states | 524H0195 | 1:45–3:15 |
| 4 | CRC cards → class diagram, Strategy for payments | 524H0191 | 3:15–5:00 |
| 5 | Database logic: one schema for two customer types | 524H0191 | 5:00–6:15 |
| 6 | Architecture and where the pricing rules live | 524H0195 | 6:15–7:15 |
| 7 | Prototype walkthrough: four stages, five screens | `<TBD>` | 7:15–8:45 |
| 8 | What we expect the Week 5 change request to cost | 524H0195 | 8:45–9:00 |

## Script (English, projected; speak from these notes, do not read)

### 1 — Opening (30 s, 524H0195)

"We submitted a requirement set with forty-six numbered requirements. This is the design that
satisfies them. Three decisions carry most of the weight: actors are generalised in one schema, the
order lifecycle is a state machine enforced in the business layer, and payments are a Strategy. I will
take the state machine and the architecture; my colleagues take the structure and the database."

### 2 — Actors (75 s, `<TBD>`)

Point at the diagram.

"One abstract Customer, two concrete types. The reason this is a design decision and not a drawing is
that the two types differ in three places: how they register, which payment methods they may choose,
and what a delivery address looks like. A Local Customer gives a mobile number; a Tourist gives a
passport, a nationality and an email, and may give a hotel and room.

We kept one Users table with a discriminator and one profile table per type. The alternative — two
separate customer tables — would make the revenue report a union of two queries and would break the
moment an admin searches for a customer without knowing which kind they are."

### 3 — Order lifecycle (90 s, 524H0195)

"Eight states. Three are terminal. The table on the slide is the whole contract: from each state, which
state, by which actor, under which guard.

Two things worth pointing at. First, `Placed → Cancelled` is available to the customer without a reason,
but to kitchen staff only with one — that asymmetry comes from a conflict between two sections of the
specification, and we resolved it in the ambiguity log as A5. Second, the guard on
`Out for Delivery → Delivered` for a cash order is not a state condition at all: it is the cash
confirmation. We kept it out of the state machine and in the order service, because the machine should
not need to know about money.

The important claim is where it is enforced. A transition is refused by the service layer and written
to the order status history as a refused attempt. The interface never decides."

### 4 — CRC to class diagram (105 s, 524H0191)

"We wrote the CRC cards first — responsibilities and collaborators, no attributes. The card for
`PricingEngine` lists exactly two things: calculate the total from a snapshot, and return the reasons a
calculation is not allowed. No card mentions a database.

The class diagram then shows the Strategy for payments. One interface, one class per method, one
resolver. The order service asks the resolver for the strategy matching the order's method; it never
names a concrete gateway. That single decision is why the Week 5 change request costs one class and one
registration line instead of a branch inside an existing class."

### 5 — Database logic (75 s, 524H0191)

"Two points about the schema. Money is stored as whole dong in a 64-bit integer, never as a floating
point number, because BR11 rounds to a thousand and a float cannot represent that exactly.

And nothing referenced by an order is hard-deleted. Hubs, brands, menu items and users carry an
inactive flag, and the order line stores the item name and unit price it was sold at. If a menu item is
removed next month, a delivered order from last month still renders correctly and the revenue report
still adds up."

### 6 — Architecture (60 s, 524H0195)

"Three tiers, and the dependency arrow points one way. The pricing engine and the state machine depend
on nothing above them and on no framework. That is not purity for its own sake: it is what let us write
eighty-one boundary cases that run in under half a second and need no database, no web server and no
browser. The performance requirement in the specification is met by six orders of magnitude, and the
reason is structural."

### 7 — Prototype (90 s, `<TBD>`)

"Four stages: sketch, wireframe, visual, interactive. Five screens matter for this review — the hub and
menu browse, the checkout with the full price breakdown, the payment step showing that a Tourist sees
Apple Pay and PayPal and a Local Customer sees MoMo and VNPay, the order tracking screen with the eight
states, and the two reports.

The checkout screen is the one to look at. It shows every component of BR10 separately, in the order
the rule specifies, ending in one rounded total. If the breakdown and the total ever disagree, the
design is wrong, not the arithmetic."

### 8 — Change request (15 s, 524H0195)

"We expect the change request in Week 5 to be a new payment method. It is one class and one registration
line. There is a one-page impact note prepared with the exact file list."

## Anticipated questions

| Question | Answer |
|---|---|
| Why not put the cash confirmation inside the state machine? | The machine models order state; cash confirmation is an order-level fact that gates one transition. Putting money in the machine would make every other transition carry a field it never uses |
| Why one Users table instead of two? | Reports and admin search span both types; two tables would force a union and a discriminator-by-table anyway |
| What if a hub has capacity zero? | Rejected at creation by a check constraint; load would be a division by zero, which the specification does not define |
| Where would a new pricing rule go? | One step in the pricing engine plus its boundary pair. No controller, view, entity or migration changes |
| Why store the item name on the order line? | So a delivered order is reproducible after the menu changes; the same reason the price snapshot exists |
| Which requirement is hardest to test? | BR17, because it needs a sequence — place, change the world, edit — rather than a single call |
