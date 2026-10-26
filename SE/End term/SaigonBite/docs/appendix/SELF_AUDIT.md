# Self-Audit — SaigonBite Final Project

Performed against `TDTU_GRADING_STANDARD.md` and the rubric in `SE_FinalProject_Requirements_SaigonBite_Sem01_2627.pdf`
page 9. This is the team grading its own submission before someone else does, so weaknesses are listed
with the same weight as strengths.

**Auditor stance**: strict examiner, Ton Duc Thang University, Faculty of Information Technology.
No credit for effort, only for artefacts that can be opened and executed.

## 1. Directory hygiene audit

| Criterion | Finding | Verdict |
|---|---|---|
| Separation of concerns | `src/`, `tests/`, `docs/`, `slides/`, `media/`, `render/`, `prototype/`, `config/`, `specs/` are distinct; no source file sits at the root | pass |
| Zero junk | `git ls-files` reports 0 matches for `__pycache__`, `.DS_Store`, `node_modules`, `bin/`, `obj/`, `.nuget/`, `.dotnet/` | pass |
| Runtime artefacts untracked | Transient SQLite sidecar files were tracked early on; they are now untracked and `App_Data/` is ignored | pass, after correction |
| Naming | Documents follow `<MSSV>_…_<Part>.pdf`; no `final_v2_fix` names | pass |
| Reproducible runbook | `README.md`, `AGENTS.md`, `scripts/render-all.sh`, `scripts/verify-pdf.sh`, `docker-compose.yml` | pass |
| Raw data on the submission | None; the repository carries no dataset | pass |
| Source PDFs | The three course PDFs are read-only and untouched | pass |

## 2. Objective execution verification

| Check | Command | Result |
|---|---|---|
| Solution builds | `dotnet build src/SaigonBite.sln` in the SDK container | **0 warnings, 0 errors** |
| Unit suite | `dotnet test` from a clean `bin`/`obj` | **133 passed, 0 failed** |
| Pricing boundary coverage | counted from test source | **81 EP/BVA cases** (20 required) |
| Illegal transitions | counted from test source | **6 cases** (5 required) |
| NFR1 performance | `PricingPerformanceTests` | **0.0006 ms** per 30-line order (limit 1500 ms) |
| Application checks | Playwright against the running app | **17 of 17** |
| Authenticated journey | Playwright, four roles | **17 of 17** |
| Order lifecycle | Playwright, one order to Delivered | **8 of 8** |
| CRUD and BR5 pricing | Playwright, admin and customer | **8 of 8** |
| Tourist journey | Playwright, passport registration to order | **7 of 7** |
| Traceability | `scripts/gen-rtm.mjs` | 46 requirements, **35 PASS, 11 PARTIAL, 0 FAIL** |
| Report layout | `scripts/verify-pdf.sh` | passes A4, Times font, page numbers, raster-image count |
| PDF bookmarks | `scripts/verify-bookmarks.py` | **90 nested bookmarks** |

## 3. TDTU formatting audit

| Requirement | Evidence | Verdict |
|---|---|---|
| Two covers, no page number | pages 1–2, logo at the measured position, Vietnamese names with diacritics | pass |
| Roman front matter, body restarts at 1 | acknowledgement `i`, declaration `ii`, TOC `iii–v`, list of figures, chapter 1 at page 1 | pass |
| Page number centred on the content axis, in the header | stamped at x = 318.9 pt, y = 44 pt | pass |
| Times New Roman, 13 pt body, 16 pt chapters | embedded font, verified with `pdffonts` | pass |
| A4 with 3.5 / 2 / 3.5 / 3 cm margins | verified with `pdfinfo` | pass |
| LIST OF FIGURES present with resolved page numbers | 10 figures, two-pass resolution | pass |
| No formula screenshots | raster images appear on 2 pages only (the cover logo); all notation is typeset text | pass |
| English throughout | all body text | pass |

## 4. Rubric assessment

| Rubric row | Weight | Level | Justification |
|---|---:|---|---|
| Part 1 — Proposal & Requirements | 15 % | **Excellent** | 46 FRs with IDs, each mapped to use case, business rule and report; 6 measurable NFRs (4 mandatory + 2 team-defined); 8 ambiguity records with adopted assumptions; tier stated on the cover as the checklist requires |
| Part 1 — Presentation | 5 % | **Good** | Five slides and a timed speaker script exist; every member has a speaking block. The mark depends on delivery, which cannot be pre-verified |
| Part 2 — Design Doc & Figma | 20 % | **Adequate** | All six checklist artefacts present and figure-numbered: use case diagram with actor generalisation, use case specifications, sequence and activity diagrams, the eight-state diagram, CRC plus class/ERD showing the Strategy, architecture tied to the NFRs. **The public Figma link does not exist**; an HTML prototype with eight rendered screens stands in. Under the rubric that is a real deduction, not a technicality |
| Part 2 — Presentation | 5 % | **Weak as things stand** | No rehearsal script has been produced for the Design Review. This is the clearest gap in the submission |
| Part 3 — Implementation & QA | 30 % | **Excellent** | Six use cases implemented with CRUD; strict three-tier separation; pricing isolated and covered by 81 boundary cases; 6 illegal-transition tests plus audit rows for accepted and rejected attempts; RTM generated from evidence; change-request impact note prepared with the exact file list; build and both suites verified from a clean tree |
| Part 3 — Live Demo | 5 % | **Unverified** | Depends on rehearsal with a clean database. The add-to-cart path was broken two hours before this audit and now works; a live demo would have failed on it |
| Final — Comprehensive Report | 10 % | **Good** | 64 pages, parts 1–3 merged, 90 bookmarks, lessons learnt present. Individual reflections are still placeholders |
| Video Demo | 10 % | **Adequate** | A 37-second screen recording walks a Local Customer order from the catalogue to `Delivered`, through kitchen, admin assignment and shipper, then shows both reports. It has captions but no narration, and the Tourist journey is proven by the automated suite rather than on camera |

**Estimated ceiling if submitted as-is: approximately 70–75 % of the available marks**, dominated by the
two human-gated gaps (Figma, narration) and the missing Design Review script. Nothing in the code or the
reports is missing that a further engineering pass could fix quickly.

## 5. Viva voce questions the panel is likely to ask

1. **BR10.** Walk me through the nine steps for a 3.2 km order at 20 % load with a 10 % voucher capped at
   30,000 on a subtotal of 200,000. Where exactly does the rounding happen, and what breaks if you round
   the delivery fee first?
2. **BR17.** A customer places an order while the rain flag is on, the flag is switched off, then the
   customer edits the quantity. Show me the price and tell me which stored fields produced it.
3. **BR8.** Hub load is defined over orders in Confirmed or Preparing. Why is `Placed` excluded, and what
   would go wrong at the 90 % boundary if it were included?
4. **NFR2.** Add ZaloPay to the running system. Show me the diff. How many existing payment classes did
   you edit, and why is the answer zero?
5. **BR15.** Show me a transition the UI never offers and prove the business layer refuses it. Where is
   the refusal recorded?
6. **Traceability.** Open the RTM and explain one PARTIAL row. Which requirement is it, what covers it
   instead of a unit test, and how would you close the gap?
7. **Design drift.** Your Part 2 design names six services that do not exist. Justify the consolidation,
   and tell me one thing you would not consolidate.

## 6. What must be finished before submission

| # | Item | Owner | Blocking |
|---|---|---|---|
| 1 | Public Figma link for the 4-stage prototype | team | Part 2, 20 % |
| 2 | Design Review script and rehearsal | team | Part 2 presentation, 5 % |
| 3 | Individual Lessons Learnt reflections | each member | Final report, 10 % |
| 4 | Video narration over the recording, or a re-record covering both customer types | team | Video, 10 % |
| 5 | Fill instructor and third member in `config/team.json`, re-run `scripts/render-all.sh` | team | every cover page |
| 6 | Live demo rehearsal on a clean database | team | Part 3 demo, 5 % |
| 7 | VNPay sandbox credentials if the live call is to be shown | team | Tier 4 evidence |
