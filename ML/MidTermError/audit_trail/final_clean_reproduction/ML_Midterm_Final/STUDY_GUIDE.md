# Study guide and oral defense

## Understand the work

Linear Regression predicts a continuous conditional mean using an affine function. Squared error measures numerical residual size; under the synthetic Gaussian noise assumption, least squares is maximum likelihood. The implemented training loss is MSE/2, so its gradient has no extra factor of two. RMSE has target units, unlike MSE.

Logistic Regression transforms a linear score with sigmoid into a binary probability. Bernoulli negative log-likelihood is binary cross-entropy. Its derivative with respect to the logit simplifies to p-y because the sigmoid derivative cancels the denominator from differentiating BCE. The loss is computed using logaddexp to avoid log(0) and overflow.

Gradient Descent evaluates the objective and both gradients at current parameters, then subtracts learning rate times each gradient. A negative gradient is a local descent direction, but an excessive step can increase the loss. Our implementation uses full batches, zero initialization and fixed iterations, and records the initial and final post-update losses. Finite differences independently check the derivative numerically.

Train/test splitting reserves observations to assess a fixed trained procedure. Cross-validation within the training partition helps select models without reading test labels. Data leakage occurs when held-out information influences training or selection; examples include fitting a scaler on all data or changing C after seeing test accuracy. Pipelines learn imputation, scaling and categories separately inside each fold.

OpenML credit-g has 1,000 rows, 20 predictors and a 700/300 good/bad split. Numeric variables are standardized, categorical variables are one-hot encoded, and the official raw artifact is retained. There are no missing cells or exact duplicates, so cleaning does not mean inventing or deleting observations. Unusually high amounts are not automatically corrupt.

High training accuracy can reflect memorization. Our unrestricted tree achieves perfect training F1 but much lower validation F1. Leaf-size restrictions, larger KNN neighborhoods and less localized SVM kernels change capacity. Stronger restriction can also underfit, so validation evidence matters. The selected study scores are descriptive because the same folds pick their settings.

The final benchmark model was chosen by mean five-fold macro-F1 on development data, before generating test predictions. HistGradientBoosting wins under that rule. Some candidates perform better on this particular test split, but using those scores to replace it would turn the test set into another validation set. The original asymmetric credit cost matrix is not the optimized objective; these results do not support real lending decisions.

## Questions and concise answers

1. **Why is the intercept separate from weights?** It shifts the prediction independently of the feature values; its derivative is the average residual because its coefficient is one for every observation.

2. **Why divide squared error by 2m?** Dividing by m averages observations, while one half cancels the derivative of the square. It changes scale and therefore learning-rate behavior, not the optimum.

3. **Derive the linear gradient.** With e=Xw+b-y, differentiation gives dJ/dw=Xᵀe/m and dJ/db=mean(e). Each residual contributes e_i*x_ij to weight j.

4. **Why does Logistic Regression use BCE?** The target is Bernoulli; taking the negative logarithm of p^y(1-p)^(1-y) gives BCE. The sigmoid chain rule yields a logit gradient p-y.

5. **What makes the implementation from scratch?** NumPy computes parameters, loss, gradients, prediction and updates. sklearn generates/splits/scales data and evaluates metrics; independently labeled sklearn fits validate results but never supply scratch weights.

6. **How do you know the gradients are correct?** We derive them and compare central finite differences on four seeds and four shapes for each model, including one feature. All 32 comparisons must meet maximum absolute error below 1e-7. This is numerical evidence for tested cases, not a proof for every floating-point input.

7. **How is OpenML origin established?** An official API response gives ID 31, version 1 and the ARFF URL/checksum. Downloaded MD5 matches that response; recorded SHA-256 identifies the retained bytes. Parser validation and acquisition logs provide further evidence.

8. **Where can scaling leak information?** A scaler fitted before splitting or before CV learns held-out means and variances. Our scaler is inside the estimator Pipeline and is fitted only on the current fold's training rows.

9. **Why macro-F1 rather than accuracy?** A majority predictor scores 70% accuracy while missing every bad-credit case. Macro-F1 weights each class equally. Balanced accuracy and bad-credit recall help explain the remaining trade-offs.

10. **Does pruning always improve performance?** No. It restricts capacity and can reduce variance or introduce excessive bias. We report all tested settings; minimum leaf size improves tree CV here, while some shallow settings underfit. Tree pre-pruning is not iterative early stopping.

11. **Why not choose the highest test score?** The final test is for evaluating a preselected procedure. Selecting from test results would consume that independence. We choose the CV winner even if another candidate happens to look better on test.

12. **What remains uncertain?** The study uses one historical dataset and one holdout split, finite optimization iterations and nonnested capacity selection. Fairness, calibration, cost-sensitive policy and population transfer are not tested. Member identities have been confirmed by the group.

## What to show during defense

Open the scratch loss/gradient and update code, point to the finite-difference tests, inspect `provenance.json`, explain the Pipeline structure, then show saved fold scores and the selection file written before test prediction. Use the loss curve, train/validation gap table and confusion matrix to connect mathematics with observed behavior. Every group member should understand these steps and submit the required PDF and code.
