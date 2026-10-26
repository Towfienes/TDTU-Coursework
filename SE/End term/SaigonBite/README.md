# SaigonBite — Cloud-Kitchen Food Delivery Hub

Final Project · Introduction to Software Engineering · Sem01_2627 · Ton Duc Thang University

**Tier 4 proposed — ceiling 10.0/10 under the instructor table** (ASP.NET Core MVC Code-First + EF Core + Bootstrap 5 + VNPay sandbox + interactive
dashboard + automated tests). The complete Tier 3 foundation is required. ASP.NET Core MVC / EF Core is the proposed variant; instructor acceptance of that variant is pending. The cap is not an awarded score.

The current tier table is archived unchanged at `docs/references/instructor-technology-tiers.png`; its data and four acceptance criteria are in `config/part1.json` (`technology`). Ceilings: Tier 1 = 7.0, Tier 1B = 7.5, Tier 2 = 8.5, Tier 3 = 9.5, Tier 4 = 10.0. The report section 1.1 and workbook Team & Tier sheet reproduce the table; Tier Checklist records the implementation/evidence plan. Live VNPay evidence, working dashboard filters and executed automated test reports remain later-phase obligations.

## Part 1 build and verification

The report and workbook use `config/part1.json`; `config/team.json` supplies administrative data and team code **TeamG4**. Part 1 alone follows the original `../SE_Sem01_2627_Report_Template.docx` supplied by the instructor: Calibri, Letter page, footer page numbers, and sections1.1–1.5. The global TDTU report standard is unchanged. Course source PDFs, DOCX and workbook template are kept unchanged.

```sh
node render/build-part1.mjs
node render/build-workbook.mjs
node render/build-marking-sheet.mjs
node slides/build-deck.mjs
node slides/export-pptx.mjs
uv run --with pymupdf --with pypdf --with openpyxl python scripts/verify-part1.py
```

`build-workbook.mjs` and `export-pptx.mjs` use installed Codex runtime libraries. The workbook builder also uses bundled LibreOffice to recalculate exported shared-formula caches. Output files and remaining human checks are listed in `docs/part1-proposal-req/VERIFICATION.md`. The clean upload folder is `../Part1_Submission/`; do not upload the whole workspace. The course DOCX was found in Downloads and copied unchanged beside the course PDFs. `build-part1.mjs` calls the bundled Python/OOXML builder and packaged DOCX renderer. The original 49,701-byte instructor workbook was found in Downloads on 25 October and copied unchanged beside the PDFs; all 14 sheets are retained. See `docs/part1-proposal-req/WORKBOOK_TEMPLATE.md` for provenance and the eight-row Requirements/RTM extension. Run `python3 scripts/verify-workbook.py` for workbook-only checks.

The supporting self-assessment workbook is `TeamG4_SE_MarkingSheet_SaigonBite.xlsx`, derived from the original five-sheet instructor marking template. At the team's request, its Part1 self-estimate is19/20 (document14.5/15, pitch4.5/5); pitch participation is Yes as team self-assessment, not independently verified live evidence. Later parts remain unscored and all lecturer inputs remain blank. See `docs/part1-proposal-req/MARKING_SHEET.md`; run `python3 scripts/verify-marking-sheet.py` for its checks.

Both Excel deliverables record planned peer reviewers, joint requirement/contract reviews and an integrated client journey. Expected teamwork evidence is scoped PRs, reviewer comments and linked FR/test records. Unverified collaboration remains a plan; durable instructions are scoped to `../AGENTS.md`.

## Run the application

```sh
docker compose up -d db      # SQL Server
dotnet run --project src/SaigonBite.Web
# http://localhost:5080
```

## Test

```sh
dotnet test                  # pricing EP/BVA suite + state machine tests
npx playwright test          # end-to-end flows
```

## Layout

| Path | Contents |
|---|---|
| `config/team.json` | single source for names, IDs, instructor, dates, tier |
| `specs/001-saigonbite-platform/` | `spec.md`, `plan.md`, `tasks.md` — requirements and plan |
| `docs/part1-proposal-req/` | TeamG4 Part1 PDF/DOCX, tracking workbook and verification |
| `docs/part2-design/` | Part 2 — UML, CRC, ERD, architecture, prototype |
| `docs/part3-qa/` | Part 3 — test plan, EP/BVA matrix, evidence |
| `docs/final/` | consolidated report with bookmarks |
| `docs/appendix/` | AI usage log, contribution statement, handover checklist |
| `src/` `tests/` | application and test suites |
| `media/` | video demo and narration script |
| `slides/` | presentation decks |

## Requirements

The Part 1 source is `config/part1.json`; `specs/001-saigonbite-platform/spec.md` is its current readable baseline. Business rules BR1–BR18 come from the course
specification and are cited by ID throughout the code and tests.

## Deadlines

| Deliverable | Due |
|---|---|
| Part 1 — Proposal & Requirements | 7:00 Mon 26 Oct 2026 |
| Part 2 — Design & Figma | 7:00 Mon 9 Nov 2026 |
| Part 3 — Code, QA, Demo | 7:00 Mon 30 Nov 2026 |
| Final consolidated report + video | 7 Dec 2026 |
