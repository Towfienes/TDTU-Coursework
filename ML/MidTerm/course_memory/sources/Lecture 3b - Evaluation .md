# Lecture 3b - Evaluation .pdf

Nguồn: `ML/Introduction to machine learning/Lecture 3b - Evaluation .pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
Evaluation of Machine
   Learning Models
       Lê Anh Cường
```

## Trang PDF 2

```text
Content
• Evaluation for classification
• Evaluation for regression
```

## Trang PDF 3

```text
Content
• Evaluation for classification
• Evaluation for regression
```

## Trang PDF 4

```text
Classifier Evaluation Metrics: Confusion
Matrix
   Confusion Matrix:
      Actual class\Predicted class           C1                     ¬ C1
                  C1                 True Positives (TP)    False Negatives (FN)
                 ¬ C1                False Positives (FP)   True Negatives (TN)



   • Given m classes, an entry, CMi,j in a confusion matrix indicates #
     of tuples in class i that were labeled by the classifier as class j
   • May have extra rows/columns to provide totals
```

## Trang PDF 5

```text
Classifier Evaluation Metrics: Confusion
Matrix
    Example of Confusion Matrix:

          Actual class\Predicted buy_computer buy_computer    Total
                   class             = yes        = no
           buy_computer = yes       6954           46         7000
           buy_computer = no        412           2588        3000
                  Total             7366          2634       10000


    • Given m classes, an entry, CMi,j in a confusion matrix indicates #
      of tuples in class i that were labeled by the classifier as class j
    • May have extra rows/columns to provide totals
```

## Trang PDF 6

```text
Classifier Evaluation Metrics: Accuracy,
Error Rate, Sensitivity and Specificity


                      • Classifier Accuracy, or recognition
  A\P   C    ¬C         rate: percentage of test set tuples
   C    TP FN     P     that are correctly classified
  ¬C    FP TN     N       Accuracy = (TP + TN)/All
        P’   N’ All   • Error rate: 1 – accuracy, or
                          Error rate = (FP + FN)/All




                                                              6
```

## Trang PDF 7

```text
Classifier Evaluation Metrics: Accuracy,
Error Rate, Sensitivity and Specificity

                    ◼   Class Imbalance Problem:
                         ◼ One class may be rare, e.g. fraud, or HIV-

A\P   C    ¬C              positive
C     TP FN     P        ◼ Significant majority of the negative class

¬C    FP TN     N          and minority of the positive class
      P’   N’ All        ◼ Sensitivity: True Positive recognition

                           rate
                            ◼ Sensitivity = TP/P

                         ◼ Specificity: True Negative recognition

                           rate
                            ◼ Specificity = TN/N



                                                                        7
```

## Trang PDF 8

```text
       Classifier Evaluation Metrics:
       Precision and Recall, and F-measures
• Precision: exactness – what % of tuples that the classifier
  labeled as positive are actually positive




• Recall: completeness – what % of positive tuples did the
  classifier label as positive?
• Perfect score is 1.0




                                                                8
```

## Trang PDF 9

```text
Classifier Evaluation Metrics:
Precision and Recall, and F-measures

• Inverse relationship between precision & recall
• F measure (F1 or F-score): harmonic mean of precision and
  recall,



• Fß: weighted measure of precision and recall
    • assigns ß times as much weight to recall as to precision




                                                                 9
```

## Trang PDF 10

```text
Classifier Evaluation Metrics: Example

    Actual Class\Predicted class   cancer = yes   cancer = no   Total   Recognition(%)
           cancer = yes                90            210        300     Sensitivity = ?
            cancer = no                140           9560       9700    Specificity = ?
               Total                   230           9770       10000    Accuracy = ?


•   Precision = ?
•   Recall = ?
•   F-score=?




                                                                                          10
```

## Trang PDF 11

```text
Classifier Evaluation Metrics: Example

     Actual Class\Predicted class   cancer = yes   cancer = no   Total    Recognition(%)
            cancer = yes                90            210        300     30.00 (sensitivity
             cancer = no                140           9560       9700    98.56 (specificity)
                Total                   230           9770       10000   96.40 (accuracy)



 •    Precision = 90/230 = 39.13%
 •    Recall = 90/300 = 30.00%




                                                                                           11
```

## Trang PDF 12

```text
Example: Iris dataset
```

## Trang PDF 13

```text
ROC curve

 An ROC curve (receiver operating characteristic curve) is a graph showing the performance of a
 classification model at all classification thresholds. This curve plots two parameters:
 •True Positive Rate
 •False Positive Rate


 True Positive Rate (TPR) is a synonym for recall and is
 therefore defined as follows:




 False Positive Rate (FPR) is defined as follows:


                                                     https://developers.google.com/machine-learning/crash-
                                                     course/classification/roc-and-auc
```

## Trang PDF 14

```text
ROC curve

   An ROC curve plots TPR vs. FPR at different classification thresholds. Lowering the
   classification threshold classifies more items as positive, thus increasing both False
   Positives and True Positives. The following figure shows a typical ROC curve.



                                                                      To compute the points in an
                                                                      ROC curve, we could evaluate a
                                                                      logistic regression model many
                                                                      times with different
                                                                      classification thresholds, but
                                                                      this would be inefficient.
                                                                      Fortunately, there's an efficient,
                                                                      sorting-based algorithm that
                                                                      can provide this information for
                                                                      us, called AUC.
```

## Trang PDF 15

```text
Example:
https://heartbeat.fritz.ai/introduction-to-machine-learning-model-evaluation-fa859e1b2d7f
```

## Trang PDF 16

```text
Example
```

## Trang PDF 17

```text
   Evaluating Classifier Accuracy:
   Holdout & Cross-Validation Methods
• Holdout method
   • Given data is randomly partitioned into two independent sets
       • Training set (e.g., 2/3) for model construction
       • Test set (e.g., 1/3) for accuracy estimation
   • Random sampling: a variation of holdout
       • Repeat holdout k times, accuracy = avg. of the accuracies obtained
• Cross-validation (k-fold, where k = 10 is most popular)
    • Randomly partition the data into k mutually exclusive subsets,
      each approximately equal size
    • At i-th iteration, use Di as test set and others as training set
    • Leave-one-out: k folds where k = # of tuples, for small sized
      data
    • *Stratified cross-validation*: folds are stratified so that class
      dist. in each fold is approx. the same as that in the initial data
                                                                              17
```

## Trang PDF 18

```text
Evaluating Classifier Accuracy: Bootstrap
 • Bootstrap
     • Works well with small data sets
     • Samples the given training tuples uniformly with replacement
         • i.e., each time a tuple is selected, it is equally likely to be selected
           again and re-added to the training set
 • Several bootstrap methods, and a common one is .632 boostrap
     • A data set with d tuples is sampled d times, with replacement, resulting in
       a training set of d samples. The data tuples that did not make it into the
       training set end up forming the test set. About 63.2% of the original data
       end up in the bootstrap, and the remaining 36.8% form the test set (since
       (1 – 1/d)d ≈ e-1 = 0.368)
     • Repeat the sampling procedure k times, overall accuracy of the model:


                                                                                      18
```

## Trang PDF 19

```text
     Estimating Confidence Intervals:
     Classifier Models M1 vs. M2

• Suppose we have 2 classifiers, M1 and M2, which one is better?

• Use 10-fold cross-validation to obtain            and

• These mean error rates are just estimates of error on the true population of
 future data cases

• What if the difference between the 2 error rates is just attributed to chance?
   • Use a test of statistical significance
   • Obtain confidence limits for our error estimates


                                                                              19
```

## Trang PDF 20

```text
     Estimating Confidence Intervals:
     Null Hypothesis

• Perform 10-fold cross-validation

• Assume samples follow a t distribution with k–1 degrees of freedom (here, k=10)
• Use t-test (or Student’s t-test)
• Null Hypothesis: M1 & M2 are the same
• If we can reject null hypothesis, then
   • we conclude that the difference between M1 & M2 is statistically significant
   • Chose model with lower error rate


                                                                            20
```

## Trang PDF 21

```text
     Estimating Confidence Intervals: t-test


• If only 1 test set available: pairwise comparison
   • For ith round of 10-fold cross-validation, the same cross partitioning is used to
     obtain err(M1)i and err(M2)i                          and
   • Average over 10 rounds to get
   • t-test computes t-statistic with k-1 degrees of freedom:
                                                             where

• If two test sets available: use non-paired t-test

                 wh
                 ere
            where k1 & k2 are # of cross-validation samples used
                                                              21
                                                                 for M1 &
```

## Trang PDF 22

```text
Estimating Confidence Intervals:
Table for t-distribution




         • Symmetric
         • Significance level,
           e.g., sig = 0.05 or 5%
           means M1 & M2 are
           significantly different
           for 95% of
           population
         • Confidence limit, z =
           sig/2

                                     22
```

## Trang PDF 23

```text
     Estimating Confidence Intervals:
     Statistical Significance

• Are M1 & M2 significantly different?
    • Compute t. Select significance level (e.g. sig = 5%)
    • Consult table for t-distribution: Find t value corresponding to k-1 degrees of
      freedom (here, 9)
    • t-distribution is symmetric: typically upper % points of distribution shown →
      look up value for confidence limit z=sig/2 (here, 0.025)
    • If t > z or t < -z, then t value lies in rejection region:
       • Reject null hypothesis that mean error rates of M1 & M2 are same
       • Conclude: statistically significant difference between M1 & M2
   • Otherwise, conclude that any difference is chance



                                                                              23
```

## Trang PDF 24

```text
Model Selection: ROC Curves
  •   ROC (Receiver Operating
      Characteristics) curves: for visual
      comparison of classification models
  •   Originated from signal detection theory
  •   Shows the trade-off between the true
      positive rate and the false positive rate
  •   The area under the ROC curve is a            ◼   Vertical axis
      measure of the accuracy of the model             represents the true
  •   Rank the test tuples in decreasing               positive rate
      order: the one that is most likely to        ◼   Horizontal axis rep.
      belong to the positive class appears at          the false positive rate
      the top of the list                          ◼   The plot also shows a
  •   The closer to the diagonal line (i.e., the       diagonal line
      closer the area is to 0.5), the less         ◼   A model with perfect
      accurate is the model                            accuracy will have an
                                                       area of 1.0
                                                                             24
```

## Trang PDF 25

```text
Issues Affecting Model Selection
  • Accuracy
     • classifier accuracy: predicting class label
  • Speed
      • time to construct the model (training time)
      • time to use the model (classification/prediction time)
  • Robustness: handling noise and missing values
  • Scalability: efficiency in disk-resident databases
  • Interpretability
      • understanding and insight provided by the model
  • Other measures, e.g., goodness of rules, such as decision tree
    size or compactness of classification rules
                                                                     25
```

## Trang PDF 26

```text
Example
```

## Trang PDF 27

```text
Example
```

## Trang PDF 28

```text
Content
• Evaluation for classification
• Evaluation for regression
```

## Trang PDF 29

```text
Metrics
    Mean squared error




    •on average how far are our predictions from the true values (in squared
    distance)?
    •Interpretation downside: the units are squared units
    •Square root of MSE (RMSE = root mean squared error) is often used:
```

## Trang PDF 30

```text
Metrics
       Mean squared error                                 RMSE = root mean squared error




       Mean absolute error




 Where ∥yi−^yi∥‖yi−y^i‖ indicates the absolute value of the
 residual
 •Very interpretable: on average how far are our predictions
 from the true values
```

## Trang PDF 31

```text
Metrics
    Mean squared error                         RMSE = root mean squared error




    Mean absolute error                        R-squared




                          • Define the total sum of squares (TSS) as the sum of squared
                            deviations of each response yiyi from the mean response ¯yy¯:
```

## Trang PDF 32

```text
Example
```

## Trang PDF 33

```text
R² (Coefficient of Determination)
 Definition:
 •You can interpret the R² as the proportion of variation in the dependent variable that
 is predicted by the statistical model
 •It indicates how well the model’s predictions match the observed data.
```

## Trang PDF 34

```text

```

## Trang PDF 35

```text
R² (Coefficient of Determination)
```

## Trang PDF 36

```text
R² example
```

## Trang PDF 37

```text

```