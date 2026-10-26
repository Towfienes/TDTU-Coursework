# AGENTS.md — SaigonBite

Project rules for any agent working in this repo. Read `MASTERPROMPT.md` first.

The user's durable Tier 4 implementation target and evidence gates are in
[`../AGENTS.md`](../AGENTS.md). They apply only to SE/End term. Build toward all
four gates (foundation, live sandbox, interactive Admin dashboard, automated
tests) plus the core rubric; Part 1's proposed target is not proof of completion.

## Source of truth

| Document | Wins on |
|---|---|
| `../SE_FinalProject_Requirements_SaigonBite_Sem01_2627.pdf` | BR1–BR18, state machine, rubric, tier |
| `../SE_FP_SaigonBite_CaseStudy_Sem01_2627.pdf` | context, vision, FR1–FR9 |
| `../SE_FP_SaigonBite_StudentSurvivalGuide_Sem01_2627.pdf` | deadlines, checklists |
| `../SE_Sem01_2627_Report_Template.docx` | Part 1 only: structure, Calibri, Letter, footer numbering; user override on 24 Oct 2026 |
| `../SE_Sem01_2627_Team_Workbook_Template.xlsx` | Original 14-sheet Excel structure, input colours, dropdowns and formulas; downloaded 25 Oct 2026 |
| `../SE_FP_SaigonBite_MarkingSheet_Sem01_2627.xlsx` | Original five-sheet self/lecturer marking template; preserve formulas and lecturer-only green cells |
| `../../../TDTU_REPORT_STYLE.md` | default report layout outside this Part 1 exception |
| `../../../TDTU_GRADING_STANDARD.md` | self-audit, viva questions |

Never edit the three source PDFs.

## Hard rules

1. Every requirement has an ID (`FR…`, `NFR…`) and cites the BRs it depends on.
2. Pricing lives in one pure function, outside controllers/views/entities.
3. The order state machine is enforced in the business layer, not the UI.
4. Payments use the Strategy pattern: adding a method = one new class + one registration.
5. Reports are written in English. Part 1 uses the retained SE course DOCX verbatim for style/structure; other reports retain their existing rules. Do not change the global TDTU standard for this one assignment.
6. No formula screenshots. Use MathML or rendered text.
7. Every status transition writes an `OrderStatusHistory` row.
8. AI use is logged in `docs/appendix/AI_USAGE_LOG.md`.

## Commands

```sh
bash scripts/render-all.sh      # regenerate every PDF/deck from config/team.json
bash scripts/verify-pdf.sh      # layout gates: covers, TOC, LOF, fonts, margins
docker compose up -d db         # SQL Server
dotnet test                     # xUnit suite
npx playwright test             # E2E
```

## Never invent

Student names, IDs, instructor name/title, dates, results, citations, signatures.
Unknown → `<TBD>` in bold plus a line in `docs/appendix/HANDOVER_NEEDED.md`.

## Done means verified

Run the command, quote the output, then claim success. Otherwise write SKIPPED or UNAVAILABLE.

## Part 1 baseline

Use `config/part1.json` for the report/workbook FR, NFR and ambiguity IDs. Do not reinstate old SaigonRide or intermediate-truncation assumptions. Planned tests and component mappings are not execution evidence. Run the Part 1 build/check commands in README.md after edits.

Part 1 team code is `config/team.json` → `project.team_id` = **TeamG4**. Build with `node render/build-part1.mjs` (calls the bundled Python builder), then run the README checks. Retain the original DOCX unchanged; editable output is TeamG4_SE_Final_Report_SaigonBite.docx. Preserve title/IP/TOC/Feedback, sections1.1–1.5 and Appendix A contribution/B AI. Omit guidance and future Part2/3 placeholders from the separate Part1 submission. The Part1 verifier checks course-template fidelity, not the former A4/TNR gates.
