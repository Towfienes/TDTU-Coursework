# Verification record — 2026-10-14

Final report: `output/pdf/midterm_report.pdf`, **38 physical pages** (two unnumbered covers; i–iv front matter; 1–32 body/references).

SHA-256: **ab1efc3f64b00f8d817e6a15200a60937439f5373be7863ae8a7ca55b98e9c88**.

## Academic and experiment checks

- Both Q1 models have separate definitions, prediction equations, losses, gradient derivations, GD updates, data splits, training curves and appropriate test metrics.
- Model optimization in Q1 uses NumPy, not a library optimizer. Finite differences independently verify every weight and intercept derivative for both objectives.
- Q2 uses the official OpenML ARFF (ID 31, v1), with MD5 matching official metadata, no substituted dataset. All 1,000 original records are preserved.
- Audit: no missing cells, duplicate rows or non-finite numeric values. Report distinguishes descriptive extremes from verified errors; no invented cleaning or deleted records.
- 800 development / 200 held-out test rows, disjoint IDs; common five-fold stratified CV inside development. Preprocessing is inside each fold's pipeline. EDA uses development records only.
- 14 learned classifier entries, including three SVM variants, plus a majority baseline. Scope of exclusions is explained using the lecture topics.
- All model/parameter selections finish before any held-out test prediction. Selected model is MLP by development macro F1, not by test performance.
- All 15 exported Q2 test metric sets are independently recomputed from saved predictions; row IDs, fold sizes, target counts and CV winner are checked.
- Actual training/validation gaps, tree-depth diagnostic and base-versus-selected comparisons support overfitting discussion. Potential remedies are not falsely reported as improvements already achieved.
- The final experiment run and the six unit/artifact tests pass. `build_report_data.py` passes its frozen-selection and metric-range assertions.
- References use supplied course files and the actual OpenML dataset. Academic theory is not imported from old projects or external ML sources. The advisor degree was separately verified from TDTU's official faculty page.

## Report checks

- Read the shared standard and visually compared representative reference pages for covers, front matter, contents, body, mathematics and references.
- Rendered the final PDF and visually inspected **all 38 pages**. After the final widow/orphan adjustment, inspected all changed pages again. No blank page, clipping, overlapping text, missing glyph, hanging heading, broken word across a page boundary or footer number remains.
- A4: 595.28 × 841.89 bp. Geometry: left 3.5 cm, right 2 cm, top 3.5 cm, bottom 3 cm. Body 13 pt with 22.44 pt line spacing; headings 14/16 pt, report type 24 pt, course title 22 pt.
- PDF embeds only Times New Roman regular/bold/italic/bold-italic and Cambria Math. No silent substitute font. Measured text sizes are approximately 12.95/13.95/15.94 bp due to TeX point conversion, consistent with the shared standard's rounding tolerance.
- Original logo copied byte-for-byte into `report/assets/`; original PDF and DOCX reference hashes still match the shared standard.
- Header numbers centered at x ≈ 318.9 bp, glyph tops ≈ 43.9–44.5 bp; exactly one header number on each numbered page, none on covers, no footer numbers.
- Native LaTeX equations remain editable. The derivation pages have no image objects; raster images are only the logo and experiment plots.
- Automatic TOC's 25 visible chapter/section entries match their final PDF pages. Six automatic LOF entries match actual figure numbers and pages. Longer captions wrap without colliding with the page-number column.
- Final TeX log has no overfull box, missing character, undefined command, unresolved reference or duplicate PDF destination. A harmless underfull paragraph warning and system fontconfig/font-path warnings remain.
- All 17 original course-file hashes match the earlier inventory. `Template_EN.docx` and `524H0195_524H0191.pdf` remain unchanged.
- No placeholder, old author/ID, old advisor/date, copied unrelated topic or fabricated signature remains. AI assistance is disclosed in the front matter.

## Limits and checks not performed

- This is a scientific result for one historical dataset and one test split. Modest grids and selection on CV are not a statistical superiority claim.
- Q1 logistic reaches 5,000 updates before the strict gradient-norm tolerance. MLP reaches a fixed 500-epoch budget and produces recorded maximum-iteration warnings; optimization convergence is not claimed or hidden.
- Runtime was verified in the recorded local Python environment; a clean environment on another operating system was not tested. Rebuilding needs Times New Roman, Cambria Math and a compatible TeX engine.
- The report matches measured layout and reviewed visual patterns; it is not claimed to be pixel-identical to a document with different text, three authors and a longer course title. Three author lines and the two-line course title preserve fonts and block order.
- No DOCX or presentation deck was requested or generated; editable LaTeX and the final PDF are included.
- JEV returned a local fallback decision; no successful live provider inference is claimed. Native tools performed the work. Code graph coverage was refreshed and checked for all five Python implementation/test files; coverage is best-effort, supplemented by source and runtime verification.
