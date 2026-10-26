# Requirement to evidence matrix

Authority: `Machine Learning - Mid Exam.docx`, complete OOXML extraction in `audit_trail/assignment_extracted.txt`. The document has no embedded figures, footnote/endnote parts or tables. Each group member must submit PDF and code.

Initial status before repair:

| Requirement | Implementation | Report section | Verification | Evidence | Status |
|---|---|---|---|---|---|
| Q1 model descriptions and prediction formulas | src/q1_models.py | 2, 5 | Formula/code comparison | Original PDF and source | PARTIAL |
| Q1 losses and gradient derivations | src/q1_models.py | 2, 5 | Chain rule and finite differences | Original 7-test run | PARTIAL |
| Q1 Gradient Descent from scratch | src/q1_models.py | 3, 6 | Source review, updates and reference comparison | Pending expanded tests | PARTIAL |
| Q1 train/test splits, loss plots, metrics | Q1 scripts and notebooks | 4, 7 | Independent rerun | Pending new results | PARTIAL |
| Q2 data from OpenML | src/data.py | 8 | Official download and checksum | Original source was sklearn mirror | NOT SATISFIED |
| Q2 preparation, visualization, cleaning, transformation, scaling | src/q2_classification.py | 9, 10 | Fold-specific statistics and encoding | Pending new dataset | PARTIAL |
| Q2 multiple classifiers and comparison | src/q2_classification.py | 11, 12 | Fixed stratified folds, metrics | Pending rerun | PARTIAL |
| Q2 overfitting and solutions over model families | src/q2_classification.py | 13, 14 | Train/CV gaps and 3 family studies | Original only Tree empirical | PARTIAL |
| English PDF with theory, data, solutions and results | src/build_report.py | All | Render every page and compare values | Pending new PDF | PARTIAL |
| Executable code and three executed notebooks | src, notebooks | Appendix | Clean-kernel, clean extraction | Pending rerun | PARTIAL |
| Every group member submits | README.md | Cover | Student action | Cannot execute submission for students | PARTIAL |
| Accurate student metadata | report/report_source/metadata.json | Cover | User confirmation | Duplicate supplied student ID | BLOCKED |
