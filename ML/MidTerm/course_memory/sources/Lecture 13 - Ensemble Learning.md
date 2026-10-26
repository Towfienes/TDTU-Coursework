# Lecture 13 - Ensemble Learning.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 13 - Ensemble Learning.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
 TON DUC THANG UNIVERSITY
  Faculty of Information Technology
          Computer Science



Ensemble Learning
           Lê Anh Cường
```

## Trang PDF 2

```text
What is Ensemble Learning?

• Ensemble learning, in general, is a model that makes
  predictions based on a number of different models.
• By combining individual models, the ensemble model tends
  to be more flexible (less bias) and less data-sensitive (less
  variance).




09/04/2022              IT701010 - Chapter 13 - Ensemble Learning   2
```

## Trang PDF 3

```text
Ensemble Models

Two most popular ensemble methods
are bagging and boosting.
• Bagging: Training a bunch of individual models in a parallel
  way. Each model is trained by a random subset of the data.
• Boosting: Training a bunch of individual models in a
  sequential way. Each individual model learns from mistakes
  made by the previous model.


09/04/2022             IT701010 - Chapter 13 - Ensemble Learning   3
```

## Trang PDF 4

```text
Decision Tree




09/04/2022      IT701010 - Chapter 13 - Ensemble Learning   4
```

## Trang PDF 5

```text
Decision Tree




09/04/2022      IT701010 - Chapter 13 - Ensemble Learning   5
```

## Trang PDF 6

```text
Choose attributes for partitioning




09/04/2022           IT701010 - Chapter 13 - Ensemble Learning   6
```

## Trang PDF 7

```text
Entropy




09/04/2022   IT701010 - Chapter 13 - Ensemble Learning   7
```

## Trang PDF 8

```text
Entropy of partition




09/04/2022             IT701010 - Chapter 13 - Ensemble Learning   8
```

## Trang PDF 9

```text
 Information gain of attributes




09/04/2022           IT701010 - Chapter 13 - Ensemble Learning   9
```

## Trang PDF 10

```text
Bagging vs Boosting




09/04/2022        IT701010 - Chapter 13 - Ensemble Learning   10
```

## Trang PDF 11

```text
Random Forest
• Random forest is an ensemble model using bagging as the ensemble method and decision tree as
  the individual model.




09/04/2022                          IT701010 - Chapter 13 - Ensemble Learning                    11
```

## Trang PDF 12

```text
Random Forest

• Step 1: Select n (e.g. 1000) random subsets from the
  training set
• Step 2: Train n (e.g. 1000) decision trees
      • one random subset is used to train one decision tree
      • the optimal splits for each decision tree are based on a random
        subset of features (e.g. 10 features in total, randomly select 5 out of
        10 features to split)
• Step 3: Each individual tree predicts the records/candidates
  in the test set, independently.
• Step 4: Make the final prediction
09/04/2022                    IT701010 - Chapter 13 - Ensemble Learning       12
```

## Trang PDF 13

```text
AdaBoost (Adaptive Boosting)

• AdaBoost is a boosting ensemble model and works especially
  well with the decision tree.
• Boosting model’s key is learning from the previous mistakes,
  e.g. misclassification data points.




09/04/2022            IT701010 - Chapter 13 - Ensemble Learning   13
```

## Trang PDF 14

```text
AdaBoost (Adaptive Boosting)




09/04/2022        IT701010 - Chapter 13 - Ensemble Learning   14
```

## Trang PDF 15

```text
AdaBoost (Adaptive Boosting)




09/04/2022        IT701010 - Chapter 13 - Ensemble Learning   15
```

## Trang PDF 16

```text
AdaBoost (Adaptive Boosting)

• Step 0: Initialize the weights of data points. if the training
  set has 100 data points, then each point’s initial weight should
  be 1/100 = 0.01.
• Step 1: Train a decision tree
• Step 2: Calculate the weighted error rate (e) of the decision
  tree. The weighted error rate (e) is just how many wrong
  predictions out of total and you treat the wrong predictions
  differently based on its data point’s weight. The higher the
  weight, the more the corresponding error will be
  weighted during the calculation of the (e).
09/04/2022              IT701010 - Chapter 13 - Ensemble Learning   16
```

## Trang PDF 17

```text
AdaBoost (Adaptive Boosting)

• Step 3: Calculate this decision tree’s weight in the ensemble
      • the weight of this tree = learning rate * log( (1 — e) / e)
      • the higher weighted error rate of a tree, the less decision power the tree will be
        given during the later voting
      • the lower weighted error rate of a tree, the higher decision power the tree will
        be given during the later voting
• Step 4: Update weights of wrongly classified points
      the weight of each data point =
      • if the model got this data point correct, the weight stays the same
      • if the model got this data point wrong, the new weight of this point = old
        weight * np.exp(weight of this tree)
• Step 5: Repeat Step 1(until the number of trees we set to train is
  reached)

09/04/2022                        IT701010 - Chapter 13 - Ensemble Learning             17
```

## Trang PDF 18

```text
AdaBoost (Adaptive Boosting)

• Step 6: Make the final prediction
      • The AdaBoost makes a new prediction by adding up the weight (of each tree) multiply the prediction (of
        each tree). Obviously, the tree with higher weight will have more power of influence the final decision.




09/04/2022                                IT701010 - Chapter 13 - Ensemble Learning                            18
```

## Trang PDF 19

```text
Gradient Boosting
• Gradient Boosting learns from the mistake — residual error directly, rather than
  update the weights of data points.




09/04/2022                     IT701010 - Chapter 13 - Ensemble Learning             19
```

## Trang PDF 20

```text
Gradient Boosting

• Step 1: Train a decision tree
• Step 2: Apply the decision tree just trained to predict
• Step 3: Calculate the residual of this decision tree, Save
  residual errors as the new y
• Step 4: Repeat Step 1 (until the number of trees we set to
  train is reached)
• Step 5: Make the final prediction


09/04/2022             IT701010 - Chapter 13 - Ensemble Learning   20
```

## Trang PDF 21

```text
09/04/2022   IT701010 - Chapter 13 - Ensemble Learning   21
```

## Trang PDF 22

```text
                                                                Gradient Descent




                                                         Consider model boosting is a function
                                                         of W, then each learner is a parameter
                                                         w.




09/04/2022   IT701010 - Chapter 13 - Ensemble Learning                                   22
```

## Trang PDF 23

```text
Gradient Boosting

• The Gradient Boosting makes a new prediction by simply
  adding up the predictions (of all trees)




09/04/2022            IT701010 - Chapter 13 - Ensemble Learning   23
```

## Trang PDF 24

```text
References

• https://towardsdatascience.com/basic-ensemble-learning-
  random-forest-adaboost-gradient-boosting-step-by-step-
  explained-95d49d1e2725
• https://viblo.asia/p/gradient-boosting-tat-tan-tat-ve-thuat-
  toan-manh-me-nhat-trong-machine-learning-
  YWOZrN7vZQ0




09/04/2022              IT701010 - Chapter 13 - Ensemble Learning   24
```