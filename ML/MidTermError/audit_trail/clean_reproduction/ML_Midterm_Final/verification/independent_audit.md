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

Pending execution and adversarial review; see execution_results.md and requirements_traceability.md for final evidence.
