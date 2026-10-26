# Independent Verification — Machine Learning Mid Exam

**Review date:** 2026-10-08  
**Original assignment:** `Machine Learning - Mid Exam.docx`  
**Submission:** `Machine_Learning_Midterm_Complete.zip`  
**Status:** Technically reproducible; **one important dataset provenance caveat**; do not claim a guaranteed full mark.

## Scope and method

The supplied ZIP was independently decompressed into an audit directory. Its content was inspected, its internal SHA-256 manifest was checked, and both training scripts were executed **again** without relying on the original saved execution logs. All three Jupyter notebooks were independently executed cell-by-cell via `nbclient` using the extracted project root as working directory. The 13-page PDF was inspected for theory, outputs, and overfitting analysis. Online OpenML metadata was consulted to verify the dataset listing, but **a live OpenML dataset download was not demonstrated**.

## Checks and observed evidence

| Check | Independently observed | Verdict |
|---|---|---|
| Archive integrity | `unzip -t` reported no errors, 33 entries | PASS |
| Internal SHA-256 manifest | All 32 manifest entries reported OK | PASS |
| PDF output | 13 pages; displayed formulas, figures and results inspected | PASS (spot check) |
| Unit tests | `python -m unittest discover -s tests -v`: **7 tests, OK** | PASS |
| Linear Regression scratch learning | NumPy loss, gradients, batch GD, synthetic split, training curve, MSE/RMSE/MAE/R2 | PASS |
| Logistic Regression scratch learning | NumPy sigmoid, stable BCE, gradients, batch GD, split, learning curve, accuracy/F1/AUC/CM | PASS |
| Numerical gradient check | Linear 2.226696160789743e-09, Logistic 8.302217247013743e-11 | PASS |
| Repeat original numeric experiments | Reexecuted `src.q1_models` and `src.q2_classification`; JSON summaries and comparison CSV exactly matched original files | PASS |
| Rerun Jupyter notebooks | Linear: 5 code cells; Logistic: 5; Q2: 4; all independently executed without errors | PASS |
| Classifier comparisons | **12 predictive algorithms plus one majority-class baseline**; 5-fold training-only macro-F1 CV and held-out test metrics | PASS |
| Overfitting | Measured unrestricted vs pre-pruned Decision Tree; CV-selected depth 3; method-family mitigation advice provided | PARTIAL for strict per-algorithm experimental interpretation |
| OpenML source | Iris registered as OpenML ID 61/version 1. Actual experiment reads a CSV generated using scikit-learn `load_iris`, not OpenML itself | **CONDITIONAL / NOT DIRECTLY VERIFIED** |
| Submission identity | Student name/ID and group/section left blank in PDF | MUST COMPLETE |

## Reproduced exact results

- Linear Regression: R2 = **0.9654916280448091**; RMSE = **0.6462153566954975**.
- Logistic Regression: accuracy = **0.8833333333333333**.
- Q2 cross-validation-selected algorithm: **Gaussian Naive Bayes**; test accuracy = **0.9111111111111111**.
- Data source recorded in result JSON: `Bundled offline mirror (scikit-learn Fisher Iris); OpenML dataset 61`.
- Bundled Iris CSV: 150 rows / 5 columns; 1 duplicated row; 149 rows after cleaning; its four numeric columns match the local scikit-learn Iris copy exactly.

## Mathematical check

**Linear regression**: let `e = Xw + b - y`. For `J = ||e||^2 / (2m)`, the chain rule gives `grad_w J = X.T @ e / m` and `dJ/db = mean(e)`.

**Binary logistic regression**: let `z = Xw+b`, `p = sigmoid(z)`. For binary cross entropy `J = -mean(y log p + (1-y) log(1-p))`, `dJ/dz = p-y`. Therefore `grad_w J = X.T @ (p-y) / m` and `dJ/db = mean(p-y)`.

The submitted implementations use these expressions and independently pass finite-difference checks. This verifies the tested formulas/code to numerical precision; it is not a formal proof of the correctness of every possible input scenario.

## Important caveats before academic submission

1. **OpenML provenance**: OpenML lists Iris as dataset ID 61 version 1 (https://www.openml.org/d/61). The actual experiment uses a bundled offline CSV originating from `sklearn.datasets.load_iris`. No row-by-row equality against a live OpenML download was proved. If the lecturer requires a dataset *downloaded from OpenML*, run with `--use-openml-live` on a networked machine, inspect any changed metrics, regenerate plots and PDF, and record the download provenance.
2. **Overfitting depth**: Empirical overfitting mitigation is demonstrated for Decision Tree. Recommendations for other model families are theoretical, not individually experimental; a strict assessor might expect more.
3. **Report terminology**: Section 9.2 labels tree pre-pruning as `early stopping via tree pre-pruning`; the clearer term is **tree pre-pruning / limiting max_depth** (not standard iterative early stopping).
4. **Report metadata**: Student ID/name/group fields are not completed.
5. **Score**: A successful execution and a rubric mapping do not guarantee the lecturer will award 10/10.

## How to reproduce on CachyOS/Arch (fish)

After extracting the ZIP and opening `ML_Midterm_Submission` as your current directory:

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m src.q1_models
python -m src.q2_classification
jupyter lab
```

To request direct OpenML data (requires internet):

```fish
python -m src.q2_classification --use-openml-live
python -m src.build_report
```

**Sources of verification:** local submitted artifacts and independent executions. For OpenML metadata: https://www.openml.org/d/61 and https://scikit-learn.org/stable/datasets/loading_other_datasets.html.
