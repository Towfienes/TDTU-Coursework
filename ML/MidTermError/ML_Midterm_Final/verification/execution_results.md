# Execution and independent reproduction results

Status: **READY FOR STUDENT REVIEW**. Recorded execution on 9 October 2026; no guaranteed grade or completed student upload is claimed.

## Environment and execution

A new `.venv-midterm` was created outside the submission and the pinned requirements were genuinely installed using uv. Python 3.14.7 and all 11 direct dependency versions were independently checked against requirements.txt in clean-extraction verification. Exact transitive versions are in environment_versions.txt. The initial install log remains in workspace audit_trail/clean_install.log. Runtime uses one CPU thread per BLAS/OpenMP library and estimator n_jobs=1. No GPU or TeX installation is needed.

The documented invocation is `python -m src.<module>` from the extracted project root. Dataset verification, both experiments, report building, notebook execution, tests, lint and syntax checks were separately executed. Final original-directory logs are in results/.

## Automated results — PASS

- 14 unittest methods: 5 Q1, 6 Q2, 3 artifact methods. The gradient method additionally contains 32 model/seed/shape subcases, including one feature and one sample, with absolute error below 1e-7.
- Central formulas, intercept updates, objective history, extreme logits, invalid inputs, deterministic convergence and independent reference discrepancies were checked.
- All five fold-specific preprocessing fits were checked against their own 640-row statistics and categorical levels; unknown categories transform without error. Raw corruption is rejected.
- All 13 candidate test accuracies, macro-F1 and AUC were recalculated from persisted predictions. Benchmark CV means, sample SD and gaps plus all 20 study means were recalculated from stored fold records. Source review verifies that test arrays never enter selection.
- 3 notebooks, each with 7 executed code cells: 21 cells total, fresh kernel for each notebook, no error outputs, multiple inline plots in every notebook. Source hashes, timing and Python executable are recorded in notebook_execution.json.
- Ruff lint and Python compileall passed. No swallowed classifier or notebook failures.
- Strict PDF parsing, ten printed numerical assertions, member metadata, embedded text fonts, numerical trace and figure hashes passed. Visual review covered every page; see pdf_quality_assurance.md.

## First clean extraction — PASS

The submission candidate ZIP was extracted into a previously nonexistent directory. All declared dependencies were verified in the separately installed environment. Tests ran before regeneration, then all notebooks, both experiments, the PDF builder and tests ran again. Offline dataset verification, lint and syntax also passed. Logs are copied into verification/clean_*.log; the exact record is clean_reproduction_summary.json.

| Check | Exit code | Seconds |
|---|---|---|
| data | 0 | 0.845 |
| tests_before | 0 | 2.094 |
| notebooks | 0 | 15.714 |
| q1 | 0 | 1.822 |
| q2 | 0 | 12.684 |
| report | 0 | 1.509 |
| tests_after | 0 | 1.990 |
| lint | 0 | 0.024 |
| syntax | 0 | 0.039 |

Q1 metric JSON and arrays, Q2 selection/summary and four CSV result tables matched the report inputs. Floating CSV/array comparisons used rtol=atol=1e-12; JSON comparisons were exact except elapsed duration. All experiment figure PNGs were byte-identical. The rebuilt 19-page PDF had identical extracted text on every page. PDF creation metadata, elapsed durations and notebook execution timestamps are intentionally not treated as scientific discrepancies.

After assembling the sealed final ZIP, a second complete extraction/rerun is performed with the same checks. Its immutable-archive execution record is kept outside the ZIP in workspace audit_trail/final_clean_reproduction/reproduction_summary.json to avoid changing the tested archive to insert its own results. The archive’s SHA-256 appears in that external record; internal file hashes are in checksums.sha256.

## Genuine intermediate failures and repairs

1. Original tests passed 7 methods, while a separately reproduced one-feature gradient check failed with a matmul dimension error. Shape-independent probing fixed it; expanded tests and new experiments passed.
2. An intermediate artifact run failed one figure-hash assertion because it ran after figures changed but before the PDF trace was rebuilt. The actual failed log is preserved in workspace audit_trail/intermediate_artifact_failure.log. Sequential figure → report → artifact testing then passed all 14 methods. No final stale trace remains.
3. Calling q2_classification.py by filesystem path from the parent directory failed to import src. The documented project-root module invocation succeeded. An attempted log copy used the wrong relative path, so the overwritten stderr was not retained as a file; the exception is preserved in the native tool transcript and audit_trail/wrong_invocation_failure.md. No scientific result was inferred from that failed invocation.
4. Initial PDF layout had orphan continuation pages. Those intermediate files remain only outside the final ZIP. Final layout is 19 inspected pages.
5. Fresh ipykernel execution prints a TCP transport warning; kernel communication is local and warnings remain in genuine logs. All cells finish without exceptions. This warning is not relabeled as an ML result or suppressed.

## Limits and unavailable checks

Git status is **UNAVAILABLE** because there is no Git repository; no-index diffs were reviewed instead. veraPDF is **UNAVAILABLE**; formal PDF/A/PDF/UA conformance and physical printer output were not checked. Nested CV, independent external-population evaluation, calibration, fairness and operational credit-cost optimization were **NOT PERFORMED** and are not claimed. Same-fold mitigation choices can overestimate improvement; small CV differences are not significance claims. All three original input file hashes remain unchanged. Section information is not supplied; all member identities are confirmed. Every group member must still submit the PDF and code personally.
