# Abalone measurements and shell rings — Theory N4

**Data Analysis and Visualization · Endterm · VibeCoding_Expert**  
Advisor: **Ho Thi Linh, Ph.D.** · Report date: **20 October 2026**.

The project covers all six rubric components with UCI Abalone: EDA 15%, distributions 15%, hypothesis tests 15%, correlation 15%, multiple regression 20%, code 20%. The source has 4,177 records and 9 columns. Detailed analysis uses 3,341 training observations; 836 are held out for the final comparison of prespecified models.

**Current status: verified review copy.** The user confirmed the dataset choice. The YouTube URL, actual video duration and verified contribution/completion records remain pending. Proposed roles/shares were requested by the user and are labelled as proposals. The analytical work can be reviewed and used to record the video now.

## Open these first

- `report/VibeCoding_Expert_DAV_Theory_Endterm_Report_REVIEW.docx` and `.pdf`: English report, color figures, native equations and generated indexes.
- `slides/VibeCoding_Expert_DAV_Theory_Endterm_Presentation_REVIEW.pptx` and `.pdf`: 16 main slides plus 3 appendices; original TDTU logo, colored analytical charts/images and monochrome slide framing.
- `notebooks/VibeCoding_Expert_DAV_Theory_Endterm_Analysis.ipynb`: executed analysis with saved outputs.
- `slides/Speaker_Notes_VI.md`, `slides/Demo_VI.md`, `slides/Viva_VI.md`: 12 minute narration, code demo and defence preparation.
- `REQUIREMENTS.md`, `WORKLOG.md`, `PLAN.md`: requirement mapping, actual process and decisions.
- `results/QA_CHECKS.md`, `results/INTERNAL_AUDIT.md`: evidence and limitations; internal scores are not lecturer grades.

## Reproduce the analysis in three steps

Run from this project folder using Python 3.12 and uv. Linux/macOS commands:

1. Create an isolated environment:

   ```bash
   uv venv --python 3.12 .venv
   ```

2. Install the exact locked dependencies:

   ```bash
   uv pip install --python .venv/bin/python -r requirements.txt
   ```

3. Run tests, the complete notebook in a new kernel, and artifact verification:

   ```bash
   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
   OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python tools/run_notebook.py
   PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/verify_project.py
   ```

Dependency installation needs network access or a package cache. The analysis itself runs offline from the bundled raw file. The runner registers only a temporary kernel specification for its own interpreter. The setup explicitly enables the inline plotting backend even if the environment contains `MPLBACKEND=Agg`.

`tools/build_notebook.py` regenerates source and clears outputs; execute the runner again if it is used. Document builds are separate and consume exported results; rerunning the notebook does not rewrite Word/PowerPoint.

## Method decisions

- Keep raw and codebook unchanged. The two source Height = 0 values at zero-based indexes 1257 and 3996 become NaN in the analysis copy. No simulated missingness or automatic IQR deletion.
- Source continuous values were scaled; use stored units. I means infant, not a third biological sex. Rings + 1.5 is a derived age approximation and is excluded from predictors.
- Fixed stratified 80/20 split, seed 42; all detailed inference and development use train. Median/scaling are fit only within training folds. Random-source holdout is not geographic external validation.
- Length/Normal and Whole_weight/Normal/Lognormal are prespecified distribution candidates. AD Monte Carlo refits parameters for 1,999 samples; three-test Holm family. All reject; p resolution is 1/2,000, never report p=0.
- Primary hypothesis family: Welch Rings M−F; group×historical ring-band Chi-square; Welch Length ANOVA. Holm adjusts three primary p-values. Conditional post-hoc comparisons have a separate Holm family; reported 95% CIs are not simultaneous intervals.
- Pearson/Spearman use numeric source variables and pairwise n; nominal group is not assigned an arbitrary order.
- Mean baseline, compact model and full original-input OLS share five CV folds and one final holdout. Test MAE/RMSE/R² use continuous unmodified predictions. HC3 intervals do not correct collinearity or nonlinear mean structure.
- Cook sensitivity filters only inner-training rows and leaves validation unchanged. Primary full OLS retains influence flags. Stored-unit coefficient comparison avoids comparing slopes with different scalers.
- Report and slide figures use color; slide backgrounds, text, rules and ordinary tables remain monochrome. Both use the same numerical snapshots. Report and slide builders never run a second analytical pipeline.

## Results to interpret

The full model has test MAE 1.5996 rings, RMSE 2.2509 rings, R² 0.5259; baseline RMSE 3.2693. One full-model prediction lies outside observed 1–29. Shell weight has training Spearman rho 0.6928 with Rings. Marginal group differences and correlations are observational; they do not establish biological causation.

These numbers are checked against `results/summary.json` and test prediction CSVs. Read residual diagnostics, VIF and source-sampling limits alongside performance. A failed distribution fit is a supported conclusion, not a reason to search until a preferred p-value appears.

## Rebuild documents

Requires the Codex bundled document runtime and its installed Documents/Presentations tools, plus Times New Roman, Cambria Math, Arial and DejaVu Sans Mono. The notebook does not require this authoring runtime.

```bash
export TASK_RUNTIME="$HOME/.cache/codex-runtimes/codex-primary-runtime"
"$TASK_RUNTIME/dependencies/python/bin/python" tools/build_report.py
"$TASK_RUNTIME/dependencies/python/bin/python" tools/update_fields.py \
  .build/report_draft.docx report/VibeCoding_Expert_DAV_Theory_Endterm_Report_REVIEW.docx \
  --index .build/report_index.json \
  --soffice "$TASK_RUNTIME/dependencies/bin/override/soffice"
CODEX_PRIMARY_RUNTIME_ROOT="$TASK_RUNTIME" \
  "$TASK_RUNTIME/dependencies/node/bin/node" tools/build_slides.mjs
"$TASK_RUNTIME/dependencies/bin/override/soffice" --headless --convert-to pdf \
  --outdir slides slides/VibeCoding_Expert_DAV_Theory_Endterm_Presentation_REVIEW.pptx
```

The report starts from the retained template copy. Native TOC/SEQ/PAGEREF fields remain editable; cached page references are populated from rendered headings/captions until pagination stabilizes. Do not save the DOCX through a LibreOffice round trip. References and covers are excluded from this assignment's TOC. After edits, render and inspect the actual pages and slide PDF, especially native charts.

Chart snapshots use 12 significant digits to fit portable Excel workbook precision; analytical CSV/JSON retain original precision. Both report heatmaps are exported individually so their annotations remain readable. Polygonal density profiles on slides are connected observed bin densities, not a new fitted distribution.

## Video and individual submission

The script targets 720 seconds; each group member should rehearse their assigned part. Video must be 7–15 minutes and submitted by the end of **21 October 2026**. Report/code are due **23:55 on 22 October 2026, Vietnam time**. Every member submits individually.

When real facts are available, edit `project.json`: `youtube_url`, `video_duration_seconds`, `contributions_confirmed` and each author's actual `tasks`, `contribution_percent`, `completion_percent`. Proposed fields are separate and must not be treated as completed work. Confirm contribution shares total 100 and actual completion is reported honestly. Check:

```bash
.venv/bin/python tools/check_readiness.py
```

Then rebuild documents; for the report output path omit `_REVIEW` once readiness is satisfied. The slide builder chooses its suffix automatically. Update the slide 2 narration from review instructions to the actual link, and visually verify the revised documents before release.

```bash
.venv/bin/python tools/package_submission.py
```

Default packaging creates `packages/VibeCoding_Expert_DAV_Theory_Endterm_REVIEW.zip` and four review ZIPs, one per MSSV. The extracted reproduction passed 7 tests, all 17 code cells, and comparison of all 24 analytical CSVs plus the structured summary. Each archive is approximately 9.33 MiB. They are clearly labelled and should not be uploaded as final submissions. `--release` requires confirmed facts, rebuilt unsuffixed deliverables and successful verification; it creates four ZIPs named only by student ID. It does not upload files or send messages.

## Project layout and attribution

`data/` preserves raw and processed data; `src/` holds shared operations; `tests/` checks boundaries; `results/` contains tables/figures/manifest/receipts; `report/` and `slides/` contain editable documents and PDFs; `tools/` contains authoring, verification and packaging commands; `references/` retains the assignment and codebook. Environments, caches and private QA renders are excluded from packages.

Nash, W., Sellers, T., Talbot, S., Cawthorn, A., & Ford, W. (1994). *Abalone* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55C7W. CC BY 4.0. Raw SHA256: `de37cdcdcaaa50c309d514f248f7c2302a5f1f88c168905eba23fe2fbc78449f`.
