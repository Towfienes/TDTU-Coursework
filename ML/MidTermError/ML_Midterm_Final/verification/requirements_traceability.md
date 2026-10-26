# Requirement to evidence matrix

Authority: the complete original `Machine Learning - Mid Exam.docx` OOXML extraction, preserved in workspace `audit_trail/assignment_extracted.txt`. No embedded figures, tables or footnote/endnote parts were present. The recovery mission adds stronger verification expectations without replacing the lecturer’s requirements. Academic deliverables are English.

Final status: **READY FOR STUDENT REVIEW**. Confirmed members: Ngô Lâm Tiến 524H0195; Nguyễn Công Thành 524H0191; Nguyễn Lê Nhật Tâm 524H0186. Section information was not supplied and remains clearly marked. No important technical verification blocker remains. Actual student uploads remain the students’ responsibility.

| Requirement | Implementation location | Report section | Verification method | Supporting evidence | Status |
|---|---|---|---|---|---|
| Linear Model and prediction | src/q1_models.py: LinearRegressionGD | 2–4 | Formula/source and prediction tests | Central scratch class source displayed in notebook | VERIFIED |
| Linear Loss definition | src/q1_models.py: LinearRegressionGD | 2–4 | Independent loss assertions | Half-MSE for linear; stable BCE for logistic | VERIFIED |
| Linear Weight/intercept gradients | src/q1_models.py: LinearRegressionGD | 2–4 | Chain-rule derivation and finite differences | 16 shape/seed subcases per model; absolute tolerance 1e-7 | VERIFIED |
| Linear Batch GD algorithm | src/q1_models.py: LinearRegressionGD | 2–4 | One-update and convergence checks | tests/test_q1.py; final gradient norms | VERIFIED |
| Linear Python implementation from scratch | src/q1_models.py: LinearRegressionGD | 2–4 | Class source review: NumPy updates only | sklearn fits are separate validation references | VERIFIED |
| Linear Dataset | src/q1_models.py: LinearRegressionGD | 2–4 | Fixed-seed synthetic regeneration | results/q1_arrays.npz | VERIFIED |
| Linear Train/test split | src/q1_models.py: LinearRegressionGD | 2–4 | Train-only scaling and clean rerun | 288/72 records | VERIFIED |
| Linear Training loss plot | src/q1_models.py: LinearRegressionGD | 2–4 | Array/source/figure hash checks | Initial plus 1,200 post-update objectives | VERIFIED |
| Linear Appropriate test metrics | src/q1_models.py: LinearRegressionGD | 2–4 | Independent rerun and reference checks | results/q1_metrics.json; report metric assertions | VERIFIED |
| Logistic Model and prediction | src/q1_models.py: LogisticRegressionGD | 5–7 | Formula/source and prediction tests | Central scratch class source displayed in notebook | VERIFIED |
| Logistic Loss definition | src/q1_models.py: LogisticRegressionGD | 5–7 | Independent loss assertions | Half-MSE for linear; stable BCE for logistic | VERIFIED |
| Logistic Weight/intercept gradients | src/q1_models.py: LogisticRegressionGD | 5–7 | Chain-rule derivation and finite differences | 16 shape/seed subcases per model; absolute tolerance 1e-7 | VERIFIED |
| Logistic Batch GD algorithm | src/q1_models.py: LogisticRegressionGD | 5–7 | One-update and convergence checks | tests/test_q1.py; final gradient norms | VERIFIED |
| Logistic Python implementation from scratch | src/q1_models.py: LogisticRegressionGD | 5–7 | Class source review: NumPy updates only | sklearn fits are separate validation references | VERIFIED |
| Logistic Dataset | src/q1_models.py: LogisticRegressionGD | 5–7 | Fixed-seed synthetic regeneration | results/q1_arrays.npz | VERIFIED |
| Logistic Train/test split | src/q1_models.py: LogisticRegressionGD | 5–7 | Train-only scaling and clean rerun | 480/120 records | VERIFIED |
| Logistic Training loss plot | src/q1_models.py: LogisticRegressionGD | 5–7 | Array/source/figure hash checks | Initial plus 2,400 post-update objectives | VERIFIED |
| Logistic Appropriate test metrics | src/q1_models.py: LogisticRegressionGD | 5–7 | Independent rerun and reference checks | results/q1_metrics.json; report metric assertions | VERIFIED |
| Genuine OpenML classification data | src/data.py; data/raw; data/metadata | 8 | Official API/download and checksums | credit-g ID 31 v1; official MD5; raw SHA-256 | VERIFIED |
| Data preparation and visualization | src/q2_classification.py: exploratory | 9 | Development-only statistics and plots | q2_eda.json; q2_numeric_description.csv; figures | VERIFIED |
| Justified cleaning | src/data.py; exploratory | 9 | Schema, missing and duplicate checks | Zero missing/duplicate rows; no deletions or injected problems | VERIFIED |
| Transformation and scaling | src/q2_classification.py: make_pipeline | 10 | All five fold-specific imputers/scalers/encoders checked | 640-row fold fits; unknown-category test; finite matrices | VERIFIED |
| Multiple classifiers | src/q2_classification.py: models | 11 | Execute all predefined candidates | 12 predictors plus separate Dummy baseline | VERIFIED |
| Fair comparison and protected holdout | evaluate_cv; q2_selection.json | 11–13 | Same five folds; metric recalculation; source review | 65 benchmark fold records; predictions; selection before test | VERIFIED |
| Overfitting analysis across families | results/q2_fold_scores.csv | 14 | Train/CV gap recomputation | Gaps for all 13 candidate rows | VERIFIED |
| Empirical overfitting controls | src/q2_classification.py: run_studies | 15 | CV-only 20 configurations and 100 fold records | Tree/KNN/RBF studies, original/selected gaps and complexity curve | VERIFIED |
| English PDF theory/data/methods/results | src/build_report.py; report | All | Numerical assertions; every page visually inspected | 19-page A4 PDF; numerical_trace.json; PDF QA | VERIFIED |
| Executable source and educational notebooks | src; notebooks | 18 | Fresh kernels and clean-extraction reproduction | 3 notebooks; 21 code cells; no exceptions | VERIFIED |
| Mathematical/data/experiment/artifact tests | tests; verification | 18 | Unit/integration tests, lint and syntax | 14 tests pass; genuine logs; checksum list | VERIFIED |
| Clean ZIP integrity and reproducibility | verification; final ZIP | 18 | CRC, extraction, pinned environment and complete rerun | execution_results.md; reproduction_summary.json | VERIFIED |
| Accurate group metadata | report/report_source/metadata.json | Cover | Explicit user confirmation and PDF extraction | Thành ID corrected to 524H0191 | VERIFIED |
| Every member submits PDF and code | README.md | Cover, 18 | Communicated requirement; student action remains | All three members must each upload | PARTIAL |

`PARTIAL` on the final row records an external student action, not a missing artifact or an assumed submission. No upload or grading outcome is claimed. Other-family empirical controls, nested CV and deployment checks are not claimed; Sections 14–16 distinguish measured studies from theoretical advice.
