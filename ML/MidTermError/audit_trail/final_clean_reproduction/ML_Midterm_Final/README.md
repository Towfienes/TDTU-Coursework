# Introduction to Machine Learning Midterm

English academic report, NumPy scratch regressions and verified OpenML credit-g classification. Original materials are preserved outside this final directory in the workspace and `audit_trail/`. This package contains newly executed results, three educational notebooks and a requirement/evidence matrix.

**READY FOR STUDENT REVIEW after the successful checks documented in `verification/`.** Member details confirmed by the group:

| Member | Supplied student ID |
|---|---|
| Ngô Lâm Tiến | 524H0195 |
| Nguyễn Công Thành | 524H0191 |
| Nguyễn Lê Nhật Tâm | 524H0186 |

The group confirmed Nguyễn Công Thành’s corrected ID as 524H0191. Section information was not supplied; add it to `report/report_source/metadata.json` if your lecturer requires it, then rebuild the report. Every member must submit the PDF and code, as required by the lecturer. Review `STUDY_GUIDE.md` before submission.

## Files

- `report/Machine_Learning_Midterm_Final.pdf`: English theory, derivations, data, methods, measured results and limitations.
- `src/q1_models.py`: both NumPy learning algorithms, synthetic experiments and independently labeled reference checks.
- `src/data.py`: official OpenML acquisition and raw checksum/schema verification.
- `src/q2_classification.py`: 12 predictive classifiers, majority baseline and 20 capacity-control configurations.
- `notebooks/*.ipynb`: executed teaching notebooks with narrative, code, plots and interpretations.
- `data/raw/credit-g.arff`: unmodified official dataset ID 31, version 1.
- `data/metadata/`: official JSON response, provenance, split, folds and attribution/license notice.
- `results/`: metrics, prediction arrays, test predictions, per-fold scores and genuine logs.
- `figures/`: experiment and mathematical typesetting outputs used in the report.
- `verification/`: requirement matrix, audit, execution details, PDF QA, environment and checksums.
- `report/report_source/`: editable metadata, generated manuscript, numerical/figure trace and licensed fonts. The editable report builder is `src/build_report.py`; `manuscript.md` is a generated reading copy.

## CachyOS / Arch Linux and fish

Use Python 3.14 (tested: 3.14.7). Start in the extracted `ML_Midterm_Final` directory. Installation requires internet; all experiments can subsequently run offline using the verified ARFF. No GPU, TeX engine or heavyweight ML framework is needed.

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
set -gx OMP_NUM_THREADS 1
set -gx OPENBLAS_NUM_THREADS 1
set -gx MKL_NUM_THREADS 1
python -m src.data
python -m src.q1_models
python -m src.q2_classification
python notebooks/execute.py
python -m src.build_report
python -m unittest discover -s tests -v
python -m ruff check src tests notebooks/execute.py
```

The notebook runner creates fresh kernels using the active Python executable, clears saved outputs before executing, and fails on exceptions. It does not depend on a separately registered system Jupyter kernel. To execute one notebook:

```fish
python notebooks/execute.py Q1_Linear_Regression.ipynb
python notebooks/execute.py Q1_Logistic_Regression.ipynb
python notebooks/execute.py Q2_Classification.ipynb
```

For interactive editing, installing JupyterLab is optional; it is not needed for headless reproduction:

```fish
python -m pip install jupyterlab
jupyter lab
```

## Verify or reacquire OpenML data

The default `python -m src.data` verifies the packaged official MD5, local SHA-256 and schema without network access. For a fresh official API download:

```fish
python -m src.data --download
```

This never silently switches dataset and rejects bytes that differ from an existing cache. Reacquisition refreshes the recorded retrieval timestamp, so its metadata checksum will change even when the ARFF is identical. See `data/metadata/provenance.json` and `DATA_LICENSE.md`; retain Hofmann/UCI attribution under CC BY 4.0.

## Protocol and limits

Q1 uses the original valid synthetic data and losses. Histories now include each post-update objective; gradients, input shapes, stability and one-step updates are tested. sklearn least squares/LBFGS are validation references only and never train scratch weights.

Q2 has a fixed stratified 800/200 split and five identical development folds. Pipeline preprocessing fits inside folds. Primary selection metric is macro-F1, with alphabetical ties and baseline excluded. The choice is saved before test predictions. Capacity settings are selected from development CV only. All 13 fixed candidate test rows are descriptive; there is no tuning in response to their test results. Fold mean and sample SD are retained, not interpreted as significance tests.

The three empirical mitigation families are Decision Tree, KNN and RBF SVM; other family controls are theoretical suggestions. CV improvements selected on the same folds can be optimistic. The historical credit data are not a deployment or fairness assessment, and the educational metric does not optimize its asymmetric cost matrix.

## PDF reconstruction and QA

`python -m src.build_report` reads result files and bundled fonts; it does not rerun ML or use external images. After changing report source, metrics or student metadata, rerender and inspect every page. On Arch, Poppler provides `pdftoppm`, `pdftotext`, `pdfinfo` and `pdffonts` (install `poppler` if needed):

```fish
mkdir -p ../pdf-review
pdftoppm -r 160 -png report/Machine_Learning_Midterm_Final.pdf ../pdf-review/page
pdfinfo report/Machine_Learning_Midterm_Final.pdf
```

Figures and captions must stay together; check all math, tables, page numbering and student names. Equations are high-resolution mathtext-rendered LaTeX images, so equation glyphs are not searchable PDF text. Body text remains searchable and fonts are embedded.

## Archive integrity

Check the supplied package before reproducing (scripts intentionally regenerate some outputs):

```fish
sha256sum -c verification/checksums.sha256
```

The checksum list excludes itself. Environment files, transient caches and PDF inspection images are not bundled. Exact installed transitive versions are recorded in `verification/environment_versions.txt`. Numerical reproduction tolerances are assertions in source/tests; timestamps, elapsed durations and PDF binary metadata are not expected to be identical across runs.
