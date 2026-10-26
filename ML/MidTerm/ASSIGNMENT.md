# Midterm requirements and confirmed decisions

Source: the assignment screenshot supplied by the user on 2026-10-14.

## Question 1 — 5 points

For **Linear Regression** and **Logistic Regression**, separately:
1. Describe the model, prediction formula and problem solved.
2. Define an appropriate loss.
3. Derive gradients with respect to parameters.
4. Present training with Gradient Descent.
5. Implement from scratch in Python using real or synthetic data, split train/test, plot training loss, evaluate appropriate metrics.

## Question 2 — 5 points

Use an OpenML classification dataset.
1. Prepare/preprocess, visualize, clean, transform and scale data.
2. Apply as many classification methods as appropriate; evaluate and compare.
3. Present overfitting and how to address it for these models.

## Confirmed report information

- Advisor display: **Lê Anh Cường, Ph.D.**, name first followed by the degree in English; no “Thầy”. This follows the user's latest correction. PhD verified at <https://it.tdtu.edu.vn/nlplab/people>.
- Student order: **Ngô Lâm Tiến — 524H0195; Nguyễn Công Thành — 524H0191; Nguyễn Lê Nhật Tâm — 524H0186**.
- Report date: **October 14, 2026**, “today” verified on the clock in Asia/Ho_Chi_Minh. No submission deadline needed.
- English report, shared standard `../../TDTU_REPORT_STYLE.md`; editable LaTeX, native mathematics, original logo.
- Academic theory is restricted to `../Introduction to machine learning`. OpenML supplies the dataset and its provenance; faculty page supplies the advisor's degree, not additional ML theory.

## Implementation choices

- Q1: NumPy full-batch GD on separately generated synthetic regression/binary classification data. sklearn only helps with splitting/evaluation; it does not train either scratch model.
- Q2: OpenML credit-g ID 31, version 1; locally preserved official ARFF and metadata.
- Asked whether Q2 must also be entirely from scratch. No additional constraint supplied; proceed with sklearn comparison methods and the reused scratch logistic model. This is an implementation assumption, not an invented rubric requirement.
- 14 learned classifier entries: scratch logistic, perceptron, kNN, Gaussian NB, Bernoulli NB, decision tree, three SVM kernels, MLP, bagging, random forest, AdaBoost, gradient boosting. Three SVM variants are not three independent model families. Majority baseline is the 15th entry.
- Fixed 80/20 stratified split, seed 42; common stratified 5-fold CV within development data, macro F1 for model selection; all configurations fixed before held-out test evaluation.
- Keep raw data immutable. Audit missing values, duplicates, finite numeric values and schema. Preserve legitimate extremes; no invented cleaning.
