# SaigonBite Constitution

Project: SaigonBite — Cloud-Kitchen Food Delivery Hub for Ho Chi Minh City
Course: Introduction to Software Engineering · Sem01_2627 · Ton Duc Thang University
Ratified: 2026-10-23

## Core Principles

### I. Requirements Are Identified and Traceable
Every functional requirement carries an `FR…` identifier and every quality attribute an `NFR…`
identifier. Each FR cites the business rules (`BR1`–`BR18`) it depends on, the use case that owns it,
and the test case that proves it. No requirement may exist without a test, and no test may exist
without a requirement. The Requirements Traceability Matrix is created in Part 1 and updated every
week; it is never written at the end.

### II. Pricing Is a Pure Function
The whole of BR1–BR12 lives in one pure function
`PricingEngine.Calculate(PriceContext) → PriceResult`. It reads only its argument, performs no I/O,
touches no database, and holds no state. Pricing must never appear in a controller, a view, an EF
entity, or a stored procedure. The calculation order of BR10 is implemented literally, step by step,
and rounding happens exactly once, at the end, per BR11.

### III. The State Machine Is Enforced in the Business Layer
Only the transitions listed in the specification are legal. The business layer rejects every other
transition regardless of what the UI offers; hiding a button is not enforcement. Every accepted and
every rejected transition writes an `OrderStatusHistory` row recording actor, timestamp, previous
state and next state.

### IV. Payments Are a Strategy, Not a Branch
One `IPaymentStrategy` interface, one class per payment method, one resolver selected by dependency
injection. Adding a payment method means adding one class and one registration line. Existing payment
classes are never edited to admit a new method — this is the property the Week 5 Change Request tests.

### V. Documents Meet the TDTU Layout Standard
Reports are written in English and follow `TDTU_REPORT_STYLE.md`: two covers, acknowledgement,
declaration, table of contents, list of figures when figures exist, Times New Roman, A4 with the
measured margins, centred page numbers, roman front matter. Mathematical notation is native
(MathML or typeset text) — a screenshot of a formula is a defect, not a shortcut.

### VI. Evidence Beats Assertion
No claim of success without a command that produced it. Test counts are counted, screenshots come
from a real run, and any step that could not be executed is reported as `SKIPPED` or `UNAVAILABLE`
rather than assumed. Names, student IDs, instructors, dates, results and citations are never
invented; an unknown value stays `TBD` and is listed in the handover checklist.

## Additional Constraints

**Technology tier.** Tier 4 is declared: ASP.NET Core MVC on .NET 8 with EF Core Code-First,
SQL Server, Bootstrap 5, a live VNPay sandbox integration, an interactive admin dashboard, and
automated tests. Tier 4 is a superset of Tier 3, so an incomplete fourth-tier item degrades to the
Tier 3 cap rather than to nothing; the team must never present a stack it does not actually run.

**Team structure.** Three members, one main use case with complete CRUD each:
`524H0195` owns D (Place and Manage Orders) plus the shared pricing and payment module,
`524H0191` owns A (Manage Menu and Brands) and report R1,
the third member owns B (Manage Hubs and Capacity) and report R2.
Secondary scopes are assigned so that every entity in the specification has an owner.

**Source hierarchy.** The Project Requirements document wins over the Survival Guide; the source PDFs
win over any inference. The three source PDFs are read-only.

## Development Workflow and Quality Gates

1. A requirement is written before the code that satisfies it.
2. A failing test is written before the fix or the feature.
3. A commit is small, meaningful and authored by the member who owns the touched use case;
   the specification requires more than ten such commits per student.
4. Before any deliverable is declared complete: build clean, tests green, layout verified by
   rendering, `git status` clean, no junk files, and this constitution re-checked.
5. AI assistance is declared in `docs/appendix/AI_USAGE_LOG.md` for every session.

## Governance

This constitution supersedes local convenience. An amendment requires a written note in
`docs/adr/` explaining the change, the reason, and the migration cost. Complexity must be justified
against a rubric line; unused abstraction is removed rather than defended. Every reviewer — human or
agent — verifies compliance with Principles I–VI before approving a deliverable.

**Version**: 1.0.0 | **Ratified**: 2026-10-23 | **Last Amended**: 2026-10-23
