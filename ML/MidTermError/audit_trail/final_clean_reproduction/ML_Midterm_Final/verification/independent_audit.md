# Independent academic audit

Initial inspection: 9 October 2026. Original Word instructions are authoritative; all originals remain unchanged at workspace root. Extracted original archive is preserved in `audit_trail/original_project`. Graph tier 2 covered all four original Python files; notebook source was read directly because freshness was untracked. All original modules and notebook source cells, saved outputs, metadata and dependency specifications were read. All 13 original PDF pages were rendered and inspected using four contact sheets; this initial review is less detailed than the final individual-page inspection.

| Issue | Severity | Affected evidence | Reproduction | Repair and required verification |
|---|---|---|---|---|
| Q2 data generated with sklearn, not retrieved from OpenML | High | `data/SOURCE.md`, `src/q2_classification.py` | `get_data` defaults to `load_iris` mirror | Retrieve official credit-g ID 31 v1, retain raw bytes and metadata, verify official MD5 and local SHA-256 |
| Empirical mitigation only for Decision Tree | Medium | Q2 script, report section 9 | Only depth study is executed | Run identical training-only folds for Tree, KNN and RBF SVM; disclose negative outcomes |
| Gradient check fails for one feature | Medium | Q1 `gradient_check` | X shape (3,1) raises matmul dimension error | Shape-independent initialization and finite differences across multiple shapes/seeds |
| Shape/finiteness validation missing | Medium | Both scratch `fit` methods | Empty or malformed inputs can produce NaN/broadcast errors | Reject invalid shapes/nonfinite data; test predictions, threshold and optimizer inputs |
| Last recorded loss is before last update | Low | Both scratch optimizers | One update has only initial loss in history | Record initial objective and every post-update objective; test one-step update |
| Numerical convergence not explicitly monitored | Medium | Q1 training loops | No finite-gradient check or final gradient norm | Monitor finiteness, report final gradient norm, compare independent reference |
| Scratch classes duplicated in notebooks | Medium | Both Q1 notebooks | Independent class definitions duplicate source | Import central implementation, show source and stepwise experiments in notebook |
| Q2 warning suppression conceals diagnostics | Medium | Q2 script | Suppresses UserWarning during model fitting | Keep warning logs and raise model failures |
| Tree pre-pruning described as early stopping | Low | Original PDF section 9.2 | Text inspection | Correct terminology, explain capacity control separately |
| Student metadata blank; supplied IDs conflict | Medium | PDF cover; user input | Two supplied members share 524H0195 | Preserve supplied names/IDs and mark confirmation until user resolves |
| Original PDF table metrics rounded; folds not retained | Low | Results files | CV vector and split indices absent | Save folds, indices, predictions and experiment manifest |

Original regression tests: 7 passed locally. This does not establish coverage of the cases above. Original metrics are archival evidence only; final claims will use newly executed results.

## Change policy

Preserve Q1 datasets, losses, gradients and update algorithm where valid. Replace Q2 Iris study with official mixed-type credit-g to satisfy provenance and support substantive encoding/scaling. Do not invent missing values or delete valid outliers. Keep raw data immutable and all learned preprocessing inside folds. Tests, notebooks, figures, report, README, and checksums must follow the same changed source.

## Final review

Completed against the original assignment, source, fresh outputs and final report. Tier 2 graph verification indexed the final project and checked coverage/freshness for all eight Python source/test/runner files; none had a recorded issue. This best-effort indexing evidence was supplemented by source review and execution.

The one-feature gradient failure was reproduced before repair; the old suite’s seven passes did not cover it. Final finite differences exercise both models across four seeds and four shapes. NumPy alone updates scratch weights; sklearn reference estimators are separate validation fits. BCE stability, intercept updates and post-update loss recording have direct assertions. Logistic optimization remains a finite-iteration approximation with its reference discrepancy disclosed.

The official ARFF was downloaded and its MD5 compared to API metadata, rather than inferred from a sklearn mirror. Schema and SHA-256 are verified offline. Source review confirms that only Xtr/ytr enter CV and capacity studies, with selection persisted before test predictions. HistGradientBoosting remains overfit by its train/CV gap despite winning validation; this is reported. Test winners do not replace the chosen procedure. Larger KNN settings reduce the gap but can worsen validation; this negative trade-off remains. RBF mitigation improves CV while leaving a large gap. Same-fold capacity selection is disclosed as optimistic.

Tests recalculate test accuracy, macro-F1 and AUC for every candidate, and CV means/SD/gaps from stored folds. All charts derive from executed arrays/data and their hashes bind the report to the figures. Class histogram overlays were corrected to common bin edges. All 19 PDF pages were individually reviewed, with final changed pages reinspected. Member metadata was resolved by explicit user confirmation of Nguyễn Công Thành 524H0191.

Fresh-kernel notebooks, 14 tests, lint, syntax and clean-extraction reproduction passed. No unresolved actionable implementation defect was found in this bounded review; no bug-free claim or grade is implied. See execution_results.md for failures/reruns and requirements_traceability.md for individual requirements.

Git status is **UNAVAILABLE**: this workspace is not a Git checkout. Original-to-final `git diff --no-index` comparisons were inspected. Q1 preserves valid equations/data while adding validation and evidence; Q2 replacement is justified by provenance and mixed-feature preparation. No unrelated credentials, environment directories or caches are packaged. All three original input SHA-256 values remain unchanged.
