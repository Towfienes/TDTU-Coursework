# Introduction to Machine Learning — Midterm project

A complete, reproducible English-language project for both questions in `Machine Learning - Mid Exam.docx`.

> **Before submitting:** Edit the **Student name / ID** and **Group / section** fields on page 1 of the PDF (or ask for an updated PDF). The PDF intentionally leaves them blank. Every group member must submit per the instructions. Review the report and code so you can explain the methods and experimental design.

## Deliverables

- `report/Machine_Learning_Midterm_Report.pdf` — 13-page report with theoretical descriptions, prediction formulas, loss definitions, gradient derivations, Gradient Descent algorithms, experimental plots, comparison table, overfitting analysis, limitations and references.
- `notebooks/Q1_Linear_Regression.ipynb` — self-contained NumPy implementation, train/test split, loss curve, metrics.
- `notebooks/Q1_Logistic_Regression.ipynb` — stable sigmoid and cross-entropy, gradients, train/test split, loss curve and classification metrics.
- `notebooks/Q2_Classification.ipynb` — dataset exploration, preprocessing, 13 classifiers, train-only stratified CV, test comparison and overfitting mitigation.
- `src/q1_models.py`, `src/q2_classification.py` — executable source code and reproducible experiments.
- `src/build_report.py` — rebuild report PDF after running experiments (requires ReportLab and locally installed Lato or DejaVu Sans fonts).
- `data/iris_openml_61_offline_mirror.csv` — bundled Iris dataset for offline reproduction.
- `results/*.json`, `results/*.csv` — results actually produced from the Python experiments (not fabricated values).
- `figures/*.png` — charts referenced by the PDF.
- `tests/test_submission.py` — offline unit and integration checks.

## Dataset provenance: important

Question 2 uses **Fisher's Iris dataset**, registered as **OpenML dataset ID 61, version 1**: <https://www.openml.org/d/61>. It is a dataset listed by OpenML as requested by the question.

Direct HTTP access to OpenML was unavailable in the execution environment. For reproducible **offline** experimental results, the package includes the Fisher Iris observations from **scikit-learn's bundled `load_iris` copy** in a local CSV. **The reported run is not claimed to have downloaded this CSV from OpenML live.** Its 150 examples, four numeric measurements and three classes correspond to the registered Iris classification problem. The script removes one exact duplicate row, leaving 149 rows for its model comparison. Imputation is included in the pipeline as a preventative measure; the raw mirror has no missing cells.

For a **direct OpenML download**, if your machine has internet access, run:

```fish
python -m src.q2_classification --use-openml-live
```

This uses `sklearn.datasets.fetch_openml(data_id=61)`. If fetching fails, it raises a clear error instead of silently mislabelling offline data. It regenerates Q2 results for the live source. Re-run `python -m src.build_report` to rebuild the PDF if its results change.

## CachyOS / Arch Linux with fish shell

From the **project root**, in a fish terminal:

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
python -m src.q1_models
python -m src.q2_classification
python -m unittest discover -s tests -v
jupyter lab
```

Open notebooks from `notebooks/` using the started Jupyter Lab. The notebooks already contain saved outputs from verified runs. Run them with the working directory set to the **project root** so imports of `src` and paths to `figures/` resolve correctly. Most notebook launchers started using `jupyter lab` in the root will do this; if not, navigate to the root before running notebook cells or configure the notebook working directory.

Regenerate the PDF (optional) with:

```fish
python -m src.build_report
```

For Arch package dependencies if needed: `sudo pacman -S python python-pip ttf-lato`. Avoid mixing system-managed Python packages with pip; use the virtual environment above.

## Question 1 method details

**Linear Regression** minimizes `0.5 * mean((prediction - target)**2)` with analytic gradients `(X.T @ errors) / n` and `mean(errors)`.

**Logistic Regression** predicts `sigmoid(X @ weights + intercept)` and minimizes stable binary cross-entropy `mean(logaddexp(0, logits) - labels*logits)`. Its gradients use `prediction_probability - labels`. The optimizer for both is batch Gradient Descent implemented exclusively in NumPy. No scikit-learn Regression/LogisticRegression estimator is used in the Question 1 training code.

The code checks analytic gradients using finite differences with a tolerance of `1e-6`.

## Question 2 methodological controls

1. Remove exact duplicate rows and inspect types, missing values and target class balance.
2. Stratify a 70/30 train/test split. Training examples are only used for CV and fitting; held-out test rows remain untouched during model selection.
3. Impute and standardize features inside each CV fold via an sklearn Pipeline; this prevents preprocessing leakage.
4. Compare 13 algorithms (including a majority-class baseline) using **5-fold training-only macro-F1**.
5. Choose the champion from the **training-only CV** means; report held-out accuracy, macro-precision/recall/F1 and confusion matrix. **Do not choose the champion based on test accuracy**.
6. Illustrate overfitting by varying tree depth; choose a pruned tree using training CV and compare it with an unrestricted tree.

`results/q2_model_comparison.csv` is sorted by mean cross-validation macro-F1, not test accuracy. With a small Iris test split, a model that happened to obtain a higher test score is not necessarily more reliable.

## Report scope and references

The PDF includes mathematical derivations, dataset preparation, plots, quantitative results, conclusions, and caveats. References and source links appear in section 11. The assignment asks that **every group member submit the PDF and code**.
