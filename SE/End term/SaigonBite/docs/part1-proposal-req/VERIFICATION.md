# TeamG4 Part 1 verification — updated 25 October 2026

Scope: the Part1 PDF/DOCX, workbook, five-slide PDF/PPTX and Vietnamese notes. The user changed the group code to TeamG4 and required the supplied SE course template for this assignment only. The shared TDTU standard is unchanged. Previous A4/TNR reports are superseded for this submission.

## Portal checklist

| Requirement | Evidence | Status |
| --- | --- | --- |
| Report name and title page | TeamG4_SE_Final_Report_SaigonBite.pdf; page1 has team, all3 names/IDs, ThS. advisor, tier/date/version and Abstract | PASS |
| Follow course DOCX | Exact section geometry/styles/opaque parts retained; only documented content slots changed; COURSE_TEMPLATE.md | PASS |
| Proposal with SDLC, roles and ownership | Section1.1, pages5–7; Scrum cadence, milestone plan, complete CRUD ownership | PASS |
| Problem Statement | Section1.2, page7 | PASS |
| Functional Requirements | Section1.3, pages7–11; all47 IDs/statements/sources; R1/R2 included | PASS |
| Quality Attributes | Section1.4, pages11–12; four mandatory + two team-defined targets/verification | PASS |
| Ambiguity Log | Section1.5, pages12–13; five genuine assumptions with pending instructor answers | PASS |
| Explicit Place and Manage Orders owner | Page5 and slide4: Ngô Lâm Tiến,524H0195, main UC D/UC1 | PASS |
| Slides for5–7 minute pitch | Five editable PPTX slides + projection PDF; planned VI script6:15, all3 speakers have explicit ownership claims | FILES PASS; live performance pending |
| Updated tracking workbook | Original14-sheet instructor layout; all47FR/6NFR/5A match canonical register;53 linked RTM rows, ownership,7-week plan/risks and Tier4 evidence plan | PASS |
| Supporting student marking sheet | Original5-sheet MarkingSheet; TeamG4 roster,19/20 team Part1 estimate (14.5+4.5); pitch Yes explicitly team self-assessment, not independently verified; all lecturer inputs blank | FILE CHECKS PASS; self-assessment only |

Deadline from the supplied portal screenshot:07:00 Monday26 October2026, UTC+7. The team leader uploads the report and slides in portal-accepted formats and provides/updates the workbook as directed. Actual upload was not performed.

## Executed checks

- `node render/build-part1.mjs`:17 pages; one title, IP, TOC, Feedback, Part1 sections1.1–1.5, References, Appendix A/B/C. Retained Calibri, Letter, footer numbering and source heading/table colors. No global report layout was applied.
- `uv run --with pymupdf --with pypdf --with openpyxl python scripts/verify-part1.py`: all47FR/6NFR/5A text, owners/sources/IDs, four Tier4 criteria, all14 TOC links and page targets, native headings/bookmarks/fields, template geometry and preserve-only package bytes checked. All17 footer labels, visible-glyph margins and body fonts checked. Decimal final-only rounding/boundary examples checked independently; no application PASS inferred.
- `node render/build-workbook.mjs`:fills the original49,701-byte instructor workbook. All14 sheets/order/headings/input colours/dropdowns retained; Requirements/RTM extended by8 rows to53. Canonical report IDs retained. Tier cap responds to chosen/confirmed tier changes. Bundled LibreOffice recalculates shared-formula caches; final file reopened for visual previews. The preview renderer's array-SEARCH limitation is handled by showing Calc's verified cached ownership value; the XLSX retains the original ownership formula.
- `python3 scripts/verify-workbook.py`:PASS source SHA256,14-sheet template fidelity,53 requirements/RTM links,5 ambiguity assumptions,3 names/IDs,owned D=OK,tier cap10,FR47/NFR6 counts,all unaffected formulas and future-phase recording sheets. No formula errors. Instructor-only cells are unfilled; no application execution verdicts claimed. Details:WORKBOOK_TEMPLATE.md.
- Teamwork revision:both Excel files name the same planned reviewer rotation (Phú→Tiến, Tiến→Thành, Thành→Phú). Task board T10–T12 records joint contracts, requirement cross-review and end-to-end integration as To do. Both verifiers check reviewer separation/consistency; commit counts remain Not verified. The tracking workbook has19 preview regions including the new task-board view. No completed review, meeting or execution record was invented; self-mark19/20 is unchanged.
- `node render/build-marking-sheet.mjs` and `python3 scripts/verify-marking-sheet.py`:PASS original5 sheets, non-input content/formulas/styles/dropdowns, student-only edits,19/20 Part1 team estimate,7 Yes/2 Partial/31 No with40 notes, all lecturer inputs blank, cached totals and zero formula errors. Pitch Yes/4.5 are explicitly self-assessment requested by the team; no live delivery/timing/Q&A verification claimed. Recalculated by LibreOffice; nine rendered ranges cover all5 sheets. See MARKING_SHEET.md for why the whole-project subtotal is not a final grade.
- `node slides/build-deck.mjs`:all5 slides within their content boxes; TeamG4 on the cover. `node slides/export-pptx.mjs`:5 editable slides and5 VI notes. Bundled LibreOffice converted the PPTX to5 PDF pages.
- Packaged DOCX renderer ran after both fill/cache passes. All17 final pages inspected individually, plus contact sheets. Reference/render-and-diff, source/final section audits and style audits were run. Direct formatting in source title/subheads/tables was retained intentionally. Source header @PTKT is byte-identical and renders with the same fallback font as the reference; report body is Calibri.
- Source DOCX SHA256 unchanged, including the Downloads original. Three source PDFs unchanged. The14-sheet workbook source is retained byte-identically (SHA256 e6efb91f2a497825ee9707b54cab24ac38d47054ad8bdd5bac389f228c957dab). The marking source is also retained unchanged (22,029 bytes; SHA25613a7cf73629bcd98f4b8b9e348c1db255f808ec56a89e097d1b41317967daae7). Former four-sheet baseline and generated workbook/ZIP are backed up in../.archive/part1-before-workbook-template/. All current report copies match. Eight-file clean package includes the supporting marking sheet; ZIP bytes/CRC checked.
- Syntax checks on new/modified Python, Node and shell files; `git diff --check`. JEV advisory rules on new Python builder:PASS, zero violations; no live model review claimed. Existing application edits were retained.

## Human and external checks

- LIVE PITCH PENDING:rehearse5–7 minutes with all3 members; every member must speak and claim D/A/B.6:15 is a plan, not a measured rehearsal.
- INSTRUCTOR DECISION PENDING:the proposed Core MVC/EF Core variant versus ASP.NET MVC/Entity Framework named in the tier table. Tier4 cap10.0 requires its full accepted foundation plus live sandbox, interactive Admin dashboard and executed automated tests at later stages. No awarded score or tier approval is claimed.
- UNAVAILABLE:Microsoft Word/PowerPoint/Excel native-app testing and full historical DSH prompts/outputs. The original blank workbook is now available and used. Recover original AI records for the instructor's48-hour request; their absence is disclosed in Appendix B.
- SHARING PENDING:the workbook Instructions sheet asks for one shared Google Drive workbook accessible to the instructor. No folder publication or sharing was performed here.
- SKIPPED:application unit/E2E/performance runs, live sandbox transactions, Part2/3/final PDF regeneration, real signatures, live presentation and portal upload. No successful execution or instructor answer was invented.
