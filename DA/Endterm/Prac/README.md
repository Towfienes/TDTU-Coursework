# Endterm — Data Analysis and Visualization

**VibeCoding_Expert** · Advisor: **Ho Thi Linh, Ph.D.** · Report date: **20 October 2026**.

| Member | Student ID |
|---|---|
| NGO LAM TIEN | 524H0195 |
| NGUYEN CONG THANH | 524H0191 |
| NGUYEN LE NHAT TAM | 524H0186 |
| NGO BINH MINH | 524H0169 |

This project completes assignment Parts I–IV using the Portuguese-language subject of UCI Student Performance. The original CSV has 649 records and 33 columns. The executed notebook is the computational source of the report and presentation.

## Start here

- **Report:** `report/VibeCoding_Expert_DAV_Endterm_Report.docx` and `.pdf`.
- **Presentation:** `slides/VibeCoding_Expert_DAV_Endterm_Presentation.pptx` and `.pdf`; 22 main slides plus 3 appendices.
- **Analysis:** `notebooks/VibeCoding_Expert_DAV_Endterm_Analysis.ipynb`, with saved outputs.
- **Requirements/evidence:** `REQUIREMENTS.md`.
- **Vietnamese delivery support:** `slides/Speaker_Notes_VI.md`, `slides/Demo_VI.md`, `slides/Viva_VI.md`.
- **Process and decisions:** `PLAN.md`, `WORKLOG.md`.
- **Verification:** `results/QA_CHECKS.md`, `results/INTERNAL_AUDIT.md` and `results/package_verification.json`.

## Reproduce the analysis in three steps

Use Python 3.12 and [uv](https://docs.astral.sh/uv/). The commands below are for Linux/macOS and run from the extracted project folder.

1. Create the environment:

   ```bash
   uv venv --python 3.12 .venv
   ```

2. Install the exact locked dependencies:

   ```bash
   uv pip install --python .venv/bin/python -r requirements.txt
   ```

3. Test and execute all notebook cells in a fresh kernel:

   ```bash
   .venv/bin/python -m unittest discover -s tests -v
   .venv/bin/python tools/run_notebook.py
   .venv/bin/python tools/verify_project.py
   ```

Dependency installation needs a network connection unless packages are already cached. The analysis itself uses the bundled CSV and runs offline. The runner creates a temporary kernel specification for its own interpreter, so no global Jupyter kernel registration is required. Open the saved notebook with a Jupyter-capable editor to inspect output tables horizontally.

`tools/build_notebook.py` regenerates the notebook source and clears outputs; it is an authoring command, not necessary for normal reproduction. If used, execute `tools/run_notebook.py` afterwards.

## Method and interpretation

- The missing-data demonstration masks 32 distinct absences cells using seed 42: approximately 4.93%, the nearest integer to 5% of 649.
- Mean imputation and deletion start from the same corrupted frame. They retain 649 and 617 records respectively.
- Parts II–IV use the validated original complete measurements. Artificial missingness is not presented as an observed defect of UCI data.
- Performance bands 0–9, 10–14 and 15–20 are analyst-defined descriptions.
- Spearman association ranks original numeric/ordinal factors; earlier grades are separated from contextual factors. Derived columns never explain their own source outcome.
- Within-school normalization describes relative position. Correlation and unadjusted group means do not identify causal effects.
- Top/bottom tables contain exactly ten records, use stable source-order ties, and retain all 37 original/derived columns in notebook/CSV exports. Source indexes are zero-based; the five-record chart explicitly uses one-based row numbers.
- The codebook is ambiguous about the upper failures code. Recorded values are retained without silently editing the source.

## Folder guide

| Folder | Contents |
|---|---|
| `data/raw/` | Original small CSV, unchanged |
| `data/processed/` | Mask, treatment variants and feature table |
| `notebooks/` | Readable, executed I–IV notebook |
| `src/`, `tests/` | Shared analytical operations and boundary checks |
| `results/` | Summary, manifest, figures, tables and verification evidence |
| `report/`, `slides/` | Final editable documents, PDFs and speaking support |
| `references/` | Assignment images, source metadata/codebook, retained template |
| `tools/` | Notebook, document and packaging/reproduction utilities |

## Rebuild documents

Re-running the notebook does not automatically rewrite the Word/PowerPoint files. Document builds are a separate authoring workflow and need the Codex bundled document runtime, Times New Roman, Cambria Math, Arial, DejaVu Sans Mono and the installed Documents/Presentations skill tools.

Set `TASK_RUNTIME` to the local bundled runtime directory. The default location on the authoring machine was `$HOME/.cache/codex-runtimes/codex-primary-runtime`; it is not included in the submission.

```bash
export TASK_RUNTIME="$HOME/.cache/codex-runtimes/codex-primary-runtime"
"$TASK_RUNTIME/dependencies/python/bin/python" tools/build_report.py
"$TASK_RUNTIME/dependencies/python/bin/python" tools/update_fields.py \
  .build/report_draft.docx report/VibeCoding_Expert_DAV_Endterm_Report.docx \
  --index .build/report_index.json \
  --soffice "$TASK_RUNTIME/dependencies/bin/override/soffice"
CODEX_PRIMARY_RUNTIME_ROOT="$TASK_RUNTIME" \
  "$TASK_RUNTIME/dependencies/node/bin/node" tools/build_slides.mjs
"$TASK_RUNTIME/dependencies/bin/override/soffice" --headless --convert-to pdf \
  --outdir slides slides/VibeCoding_Expert_DAV_Endterm_Presentation.pptx
```

The report builder starts from the retained template copy. Native Word TOC/SEQ/PAGEREF fields are preserved; page-reference caches are populated programmatically from actual rendered headings/captions until pagination stabilizes. The final DOCX is not round-tripped through a LibreOffice save. After document edits, rebuild and inspect all affected pages/slides; do not assume old page references remain valid.

Slide chart values are rounded only to 12 significant digits for portable Excel chart workbooks; the unrounded analytical results remain in the notebook/CSV. The box plot is editable slide geometry using the exported Seaborn-compatible statistics.

Document builders consume `results/summary.json` and saved chart files. They do not recompute statistical results. For another machine, the analysis can be reproduced without the document-authoring runtime.

## Source and attribution

Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. [DOI: 10.24432/C5TG7T](https://doi.org/10.24432/C5TG7T). CC BY 4.0.

The raw checksum is `a7594a11d7771c0efe1a740824e0e833da9c4cad07c39a9766a874575563fb3f`. See `references/dataset_source.json` for the retrieval record and `references/student.txt` for the original codebook.

## Submission and presentation

Submit `524H0195_524H0191_524H0186_524H0169.zip` by **23:00 on 22 October 2026, Vietnam time**. It contains one folder of the same name. The package excludes environments, caches, temporary Office files and private render/QA images.

The presentation is planned for approximately 24.5 minutes including a three-minute code demonstration, before Q&A. Speaking responsibilities are proposals, not records of completed contributions. Rehearse with the group and use the final PDF as a projection fallback.
