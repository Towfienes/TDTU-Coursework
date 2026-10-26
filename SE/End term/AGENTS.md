# SE End term — SaigonBite grading target

These instructions apply only to this directory and its descendants. Do not apply
this course's technology tiers or report-template exception elsewhere in TDTU.

## Durable user decision — 24 October 2026

Build SaigonBite for **TeamG4** around the instructor's **Tier 4** requirements,
with the aim of satisfying the maximum-score rubric. Tier 4 has a **10.0/10
ceiling**, not a guaranteed or already-awarded mark. Part 1 records the proposal;
later implementation must produce the actual evidence below. Do not downgrade
the target or silently remove a Tier 4 capability.

Source: the instructor table supplied by the user, retained at
`SaigonBite/docs/references/instructor-technology-tiers.png`. Canonical tier data
and acceptance plan: `SaigonBite/config/part1.json` → `technology`.

| Tier | Ceiling /10 | Required stack and architecture |
| --- | ---: | --- |
| Tier 1 | 7.0 | C# WinForms + local SQL database / Excel; 3-Tier architecture. |
| Tier 1B | 7.5 | Core PHP / CodeIgniter + MySQL + Bootstrap; MVC. |
| Tier 2 | 8.5 | ASP.NET Web Forms/MVC, Database First + SQL Server + Bootstrap; MVC. |
| Tier 3 | 9.5 | ASP.NET MVC, Code First + Entity Framework + Bootstrap; MVC. |
| Tier 4 | 10.0 | Complete Tier 3 foundation + live sandbox API + interactive Admin dashboard + automated tests. |

## Implementation and evidence gates

1. **Foundation:** retain MVC separation, Code-First models/migrations, Entity
   Framework and Bootstrap. SQL Server is the proposed submission database;
   SQLite is only a labelled local fallback. The existing Core MVC/EF Core
   variant is proposed; obtain instructor confirmation because the table names
   ASP.NET MVC/Entity Framework. Do not invent approval or silently switch stacks.
2. **Live sandbox API:** deliver a real VNPay sandbox transaction/callback path
   for eligible customers, authenticated callbacks, order/amount checks and
   idempotent handling of duplicate callbacks. Keep redacted provider transaction
   and callback evidence for success, failure/cancellation and invalid/replayed
   callbacks. Mock-only demonstrations do not satisfy this gate. Never commit keys.
3. **Interactive Admin dashboard:** implement R1 Revenue and R2 Hub Utilization
   as working charts and tables backed by authorised server data. Demonstrate
   revenue date-range/hub controls, consistent chart/table totals and refusal of
   non-Admin access. Static screens or hardcoded charts do not establish this gate.
4. **Automated tests:** execute unit/integration/E2E tests for pricing, state
   transitions, ordering, payment callbacks and dashboard interaction. Cover at
   least 20 EP/BVA cases and five forbidden transitions as required by the course.
   Retain reproducible commands/fixtures, commit IDs, counts and actual PASS/FAIL
   reports. Planned test IDs are not execution evidence.
5. **Core rubric:** all three main CRUD use cases, BR1–BR18, both customer types,
   payment Strategy, all six NFRs and R1/R2 remain required. Tie every capability
   to FR/NFR IDs, its owner, code and tests; Tier 4 additions do not replace these.

Ownership: Ngô Lâm Tiến 524H0195 → D (Place and Manage Orders), pricing/payments;
Nguyễn Công Thành 524H0191 → A, data foundation/R1; Nguyễn Trọng Phú 524H0179 → B/R2.
Thành and Phú own the dashboard/report views; all three own tests for their scopes.
Use the canonical team/register files for current administrative data and IDs.
Do not certify old application counts without rerunning their relevant checks.

## Teamwork in the Excel deliverables

Show concrete coordination: one accountable owner, a named peer reviewer,
shared-contract decisions, joint requirement checks and an integrated client
journey. Current planned rotation: Phú reviews Tiến, Tiến reviews Thành,
Thành reviews Phú. Link actual future evidence to scoped PRs, review comments,
FR/test IDs and integration logs. Record planned work as planned until evidence
exists; do not invent completed meetings, reviews, commits or test outcomes.
Keep the tracking workbook and student marking notes consistent. Self-marks
remain estimates; instructor marks and Contribution Factors belong to the lecturer.

## Report and submission scope

- The team Excel follows the original 49,701-byte instructor workbook
  `SE_Sem01_2627_Team_Workbook_Template.xlsx` (SHA256
  `e6efb91f2a497825ee9707b54cab24ac38d47054ad8bdd5bac389f228c957dab`).
  Preserve its 14 sheets, headers, student/instructor colours, dropdowns and
  formulas. Extend Requirements and RTM together when more slots are needed.
  Keep canonical report IDs and leave instructor-only answers/confirmation blank.
  The former filled four-sheet file is archived, not the authoritative template.
- The separate MarkingSheet uses `SE_FP_SaigonBite_MarkingSheet_Sem01_2627.xlsx`.
  Fill student self-marks/checklist with evidence for the current checkpoint.
  Keep every lecturer mark/comment, confirmed tier, marking date, commit count
  and Contribution Factor input blank until supplied by the lecturer. Do not
  interpret the template's calculated zeros as assigned grades.
- Part 1 alone follows `SE_Sem01_2627_Report_Template.docx`, retained unchanged.
  Use its Calibri/Letter/footer layout and sections 1.1–1.5. The global TDTU report
  standard and other assignments are unchanged.
- Current clean files: `Part1_Submission/`; convenience archive:
  `TeamG4_SE_Part1_SaigonBite.zip`.
- The supplied portal notice explicitly requests the report PDF and Presentation
  1 slides, and requires updating the team workbook. It does **not** establish
  that ZIP-only submission is accepted. Submit the required individual formats
  unless the portal/instructor explicitly permits a ZIP instead.
- Every member must speak and claim the assigned main use case in the live
  5–7 minute pitch. A generated file or planned speaking script is not proof of
  rehearsal, presentation or successful portal upload.
