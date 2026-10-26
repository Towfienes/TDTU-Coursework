# SaigonBite — interactive prototype (Part 2 substitute)

Part 2 asks for a **four-stage Figma prototype** with a public link. No member of this
repository can create the Figma account or the public link from here, so this folder
contains the closest honest substitute: a **clickable HTML prototype** that behaves like the
finished design, plus **1440 × 900 PNGs of every screen** ready to drop into the Part 2
document and into Figma.

> **The public Figma link must be created by the team.** Nothing in this folder can produce
> it. The import guide below says exactly how to get from these files to that link in one
> sitting.

---

## 1. What is in this folder

| Path | What it is |
|---|---|
| `index.html` | The whole prototype: one file, inline CSS and JS, **no network requests**, no build step. |
| `screens/01-hubs.png` … `screens/09-dashboard.png` | Each screen rendered at **1440 × 900** with the workspace Chromium build. |
| `build-screens.mjs` | Re-renders the PNGs and fails if the page makes one external request. |

Open `index.html` in any browser — `file://` is enough. There is no server, no npm install
and no font download: the interface uses the operating system's UI font stack.

## 2. The nine screens

| # | Screen | File | Route | What it demonstrates |
|---|---|---|---|---|
| 1 | Hub and brand browsing | `01-hubs.png` | `#hubs` | Three hubs with capacity, current load and the Quiet Kitchen / Refused state; brands filtered by the selected hub (BR12) |
| 2 | Menu with availability | `02-menu.png` | `#menu` | Ten dishes with VND prices, a sold-out item that cannot be ordered, brand filter chips |
| 3 | Cart | `03-cart.png` | `#cart` | Quantity editing, one-hub rule, live price preview |
| 4 | Checkout | `04-checkout.png` | `#checkout` | The **full breakdown**: subtotal, Quiet Kitchen discount, voucher, food total, delivery fee, rush surcharge, rain surcharge, raw total, rounded total — numbered **1–9** in the exact order of BR10 |
| 5 | Payment | `05-payment.png` | `#payment` | MoMo / VNPay / cash for a Local Customer, Apple Pay / PayPal / cash for a Foreign Tourist, COD refused above 1,000,000 (BR13, BR14) |
| 6 | Order tracking | `06-track.png` | `#track` | The six forward states plus Cancelled and Failed, a role switch, only the legal transitions offered, an illegal move rejected in the business layer, an audit trail, and the BR15 state machine |
| 7 | Revenue report | `07-revenue.png` | `#revenue` | R1 by brand category and by payment method, with cancelled and failed orders excluded |
| 8 | Hub utilization report | `08-utilization.png` | `#utilization` | R2: orders handled, average preparation time, current load, Quiet Kitchen discounts granted |
| 9 | Admin dashboard | `09-dashboard.png` | `#dashboard` | Two charts drawn in inline SVG (revenue by category, load against the 90 % threshold) plus orders by state |

Every screen is reachable from the left navigation, from any other screen.

## 3. What actually works

The prototype is not a set of static pictures — the flows below were executed in Chromium
and produced the printed results:

| Interaction | Result |
|---|---|
| Add a dish | Cart count and subtotal update; the dish button shows the quantity already in the cart |
| Apply voucher `SAIGON10` | 252,000 ₫ basket → 229,000 ₫ (10 % of the discounted food amount, capped at 30,000) |
| Hub load raised to 95 % | Order refused with the BR8 message; the checkout button is disabled |
| Distance raised to 8.5 km | Order refused with BR2 |
| Placement time 12:30 + rain on | +20 % rush surcharge and +10,000 rain surcharge applied, total re-rounded once |
| Customer type switched | Payment list changes from MoMo/VNPay/cash to Apple Pay/PayPal/cash |
| Pay → Track | A new order is created in `Placed` with its first audit row |
| Attempt `Placed → Preparing` | `Rejected by the business layer: Placed → Preparing (BR15)` |
| Kitchen staff advance | Placed → Confirmed → Preparing → Ready, each step written to the audit trail |
| Shipper before assignment | "Out for delivery" is disabled until a shipper is assigned (ambiguity A1) |
| Language toggle | Every label, dish, hub, status and payment name switches EN ⇄ VI |

The pricing function in `index.html` implements BR1–BR11 literally — including rounding once
at the end. With the default basket it reproduces the specification's worked example:
**subtotal 200,000, Quiet Kitchen 20,000, delivery 25,000, total 205,000**.

## 4. Responsive behaviour

The layout was checked at **390, 768, 1024 and 1440 px** on all nine screens: no screen has
horizontal page overflow at any of the four widths (tables scroll inside their own card, and
the state-machine diagram scrolls inside its card on a phone). Below 980 px the sidebar
becomes a horizontal strip; below 640 px the grids collapse to one column.

## 5. Taking these screens into Figma — the four required stages

Part 2 grades four stages. Create **one Figma file** with four pages, in this order.

### Stage 1 — `01 Sketch`
1. New Figma file → page `01 Sketch`.
2. Place `screens/01-hubs.png` … `09-dashboard.png` on the page at 25 % opacity as
   underlays, or redraw freehand with the pencil / FigJam-style strokes.
3. Frame names: `S1 Hubs — sketch`, `S2 Menu — sketch`, … `S9 Dashboard — sketch`.
4. Keep it deliberately rough: boxes and arrows, no real text. The sketch stage is graded on
   *structure*, not polish.

### Stage 2 — `02 Wireframe`
1. Duplicate page 1 → rename `02 Wireframe`.
2. Redraw each screen in greyscale: rectangles for cards, grey bars for text, no colour, no
   images. Use a 12-column grid at 1440 px wide, 24 px gutters — the HTML uses exactly this
   grid, so the wireframe will match the final layout.
3. Frame names: `S1 Hubs — wireframe`, …, `S9 Dashboard — wireframe`.

### Stage 3 — `03 Visual`
1. Duplicate page 2 → rename `03 Visual`.
2. Either rebuild the UI in Figma, or drop the PNGs in as a tracing reference and rebuild the
   main components: top bar, sidebar, hub card, dish card, price row, payment option, metric
   tile, chart card.
3. Match the tokens used here:

   | Token | Value |
   |---|---|
   | Ink | `#14201E` |
   | Muted ink | `#6B7A76` |
   | Brand (jade) | `#14654F`, dark `#0E4C3B`, soft `#E4EFEA` |
   | Accent (terracotta) | `#C2410C`, soft `#FCEDE5` |
   | Paper / card | `#F6F4EF` / `#FFFFFF` |
   | Line | `#E3DFD5` |
   | Radius | 12 px cards, 8–10 px controls |
   | Type | system UI stack, 14 px body, 26 px page title |

4. Frame names: `S1 Hubs — visual 1440`, …, `S9 Dashboard — visual 1440`.
   Add `… — mobile 390` variants for at least the menu, checkout and tracking screens: the
   HTML already collapses to one column at that width.

### Stage 4 — `04 Prototype`
1. Duplicate page 3 → rename `04 Prototype`.
2. Select each visual frame and add prototype links:

   | From | Trigger | To |
   |---|---|---|
   | S1 Hubs | click on a hub card | S1 Hubs (selected state) |
   | S1 Hubs | "View menu" | S2 Menu |
   | S2 Menu | "+ Add" | S3 Cart |
   | S3 Cart | "Continue to payment" | S4 Checkout |
   | S4 Checkout | "Continue to payment" | S5 Payment |
   | S5 Payment | "Pay" | S6 Track order |
   | S5 Payment | customer-type switch | S5 Payment (tourist variant) |
   | S6 Track | role switch + "Confirmed" | S6 Track (next state) |
   | Sidebar | Revenue / Hub utilization / Dashboard | S7 / S8 / S9 |

3. Set the presentation to **Fit** or **Fill**, device **Desktop 1440 × 900**, and enable
   "Show prototype interactions".
4. Publish: **Share → Anyone with the link → Can view → Copy link**. That link goes into
   Part 2 §Figma deliverable and into `docs/part2-design/`.

### Frame names, at a glance

```
01 Sketch      S1 Hubs — sketch … S9 Dashboard — sketch
02 Wireframe   S1 Hubs — wireframe … S9 Dashboard — wireframe
03 Visual      S1 Hubs — visual 1440 … S9 Dashboard — visual 1440
               S2 Menu — mobile 390, S4 Checkout — mobile 390, S6 Track — mobile 390
04 Prototype   (the same frames, wired — no new frames needed)
```

## 6. Rebuilding the PNGs

```sh
node prototype/build-screens.mjs
```

Renders all nine screens at 1440 × 900 with
`/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome`, and exits non-zero
if the page makes any request that is not `file:` or `data:`.

## 7. What this folder does not do

- It does **not** create the Figma file or the public link — a person must do that once, using
  the steps above.
- It does **not** call a real payment gateway. The payment step is simulated: pressing *Pay*
  places the order and moves the screen to tracking. The .NET implementation is what calls the
  VNPay sandbox (Tier 4).
- It does **not** persist data: refreshing the page restores the seeded basket. That is
  deliberate — the prototype demonstrates flows, not storage.
- The report figures are **seeded demo data**, labelled "Demo data" on screen. They are not
  measured results and must not be presented as such in the report.
