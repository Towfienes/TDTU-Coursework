# Introduction to Machine Learning — Midterm

## Deliverable

- **English report:** `output/pdf/midterm_report.pdf`.
- **Editable native-math source:** `report/midterm_report.tex` and `report/style.tex`.
- **Scratch implementations:** `src/models.py`.
- **Complete experiment runner:** `src/run_experiments.py`.
- **Tests:** `tests/test_models.py`, `tests/test_experiments.py`.
- **Real experiment artifacts:** `results/` (JSON/CSV, split IDs, fold IDs, test predictions, figures, and Q1 NPZ datasets).
- **Original OpenML data and provenance:** `data/`.
- **Assignment and confirmed personal information:** `ASSIGNMENT.md`.
- **Course knowledge for continuity:** `course_memory/`.
- **Verification record:** `VERIFICATION.md` (38 rendered pages reviewed; all six tests pass).

Advisor display: **Lê Anh Cường, Ph.D.** Students: **Ngô Lâm Tiến (524H0195), Nguyễn Công Thành (524H0191), Nguyễn Lê Nhật Tâm (524H0186)**. Report date: **October 14, 2026**, verified in Asia/Ho_Chi_Minh; no deadline required. The latest user instruction is name first, degree in English after the comma, without “Thầy”.

The theory is restricted to the supplied lecture folder. The shared visual standard is `../../TDTU_REPORT_STYLE.md`; its original PDF and DOCX are preserved unchanged. The report uses the original logo, Times New Roman, Cambria Math, native LaTeX equations, two covers, Roman front matter, automatic contents/figure list, and Arabic body numbering in the top header.

## Reproduce the experiments

From this folder, with Python 3.14.7 (the recorded environment):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_experiments.py
python -m unittest discover -s tests -v
python src/build_report_data.py
```

The official ARFF is already included, so running experiments needs no OpenML network access. Its MD5 and schema are checked by the loader. Install Python dependencies once; the provided code does not install anything at runtime. Running the experiment replaces the generated files in `results/`, while leaving `data/` and course sources intact.

Six tests check both gradients, exact fitting, extreme-logit stability, input validation, training-only preprocessing, and exported metric/split consistency. The artifact test requires a completed experiment run; the supplied results already satisfy it.

## Build the report

Use Tectonic 0.17.0 (the supplied run used `/tmp/tdtu_tectonic/tectonic`) or a compatible XeLaTeX installation. Times New Roman and Cambria Math must be installed; the source does not silently substitute another font.

```bash
python src/build_report_data.py
cd report
tectonic -X compile midterm_report.tex --outdir ../output/pdf --keep-logs --keep-intermediates
```

Tectonic reruns the TeX passes to resolve contents, figure lists and references. Its first use may download TeX packages. Alternatively run XeLaTeX from `report/` at least twice with the same output directory until references stabilize. Build from the original directory structure: the unchanged original logo is included at `report/assets/tdtu-logo.png`.

`src/build_report_data.py` reads the metrics into report tables. Its explicit selected-setting descriptions match this frozen experiment; if candidate grids or selection change, update these descriptions and the surrounding interpretation before rebuilding. Do not interpret a rebuild alone as validating changed scientific claims.

## Design and findings

Question 1 uses separate synthetic datasets, training-only min–max scaling and NumPy full-batch GD. The linear model learns three weights and an intercept on 480 records, evaluates on 120, and stops by training gradient norm. The logistic model trains on 640 and evaluates on 160 using a fixed 0.5 threshold; its 5,000-update budget is reached before the strict gradient tolerance.

Question 2 uses **credit-g, OpenML ID 31, version 1**, with 1,000 records, 20 mixed predictors and 700 good / 300 bad labels. Positive class is **bad = 1**. Data are divided into 800 development and 200 test records, with identical five-fold stratified CV for all candidates and macro F1 for selection. Scaling and one-hot fitting happen inside each fold. All selections precede all held-out test predictions.

The 14 learned entries include three SVM kernel variants; they are not 14 independent model families. A majority baseline is added as the 15th table entry. Q1 optimization is from scratch; Q2 comparative library estimators are explicitly acknowledged. No additional “all Q2 models from scratch” constraint was supplied after clarification.

- Q1 linear: test RMSE **0.5114**, R² **0.9947**.
- Q1 logistic: test accuracy **0.8125**, positive F1 **0.8515**, AUC **0.8576**.
- Q2 CV-selected **MLP**: CV macro F1 **0.6955**, test accuracy **0.7900**, test macro F1 **0.7305**, AUC **0.8133**.
- MLP bad-class recall is only **0.5333**: 28 of 60 bad examples are missed. Scratch logistic has almost identical test macro F1 (**0.7301**).
- Unlimited trees reach train macro F1 **1.000** versus CV **0.614**. Selecting depth 6 / leaf size 5 gives train **0.777** and CV **0.656**.

The MLP uses a fixed 500-epoch SGD budget and retains maximum-iteration warnings in `results/warnings.json`; convergence is not claimed. This is one dataset and one held-out split, with modest grids; tiny score differences do not establish statistical superiority. No test-informed retuning was performed. The report discloses AI assistance accurately and contains no fabricated signature.

## Resume after context loss

1. Read this README and `ASSIGNMENT.md` for the active task and confirmed identities.
2. Read `../../AGENTS.md` and `../../TDTU_REPORT_STYLE.md` before modifying the report.
3. Read `course_memory/00_SOURCES.md`, then the three topic notes and `04_SOURCE_CAVEATS.md`.
4. Use the source index to consult the original slide and its actual PDF page for formulas; extracted text can omit image equations.
5. Treat `results/` as the actual experiments. Keep original course files and template references unchanged.
6. Render and inspect every page after a report edit; verify automatic lists/page numbers and update `VERIFICATION.md`.

The course memory covers all 15 PDFs (680 pages) and the Word syllabus. Originals are fingerprinted in `course_memory/inventory.json`. `.DS_Store` is metadata, not a lecture. Other old ML project folders were not used as academic sources or copied implementations.
