# Lecture 5 - Decision tree.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 5 - Decision tree.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
Decision Tree
   Lê Anh Cường
       TDTU
```

## Trang PDF 2

```text
Outline
• What kind of machine learning type for Decision Tree classifier
• Decion Tree for classification
• How to build Decision Tree
   • Entropy
   • Information Gain and Feature selection
```

## Trang PDF 3

```text
Decision Tree: example




               Fig1. Loan approval example
```

## Trang PDF 4

```text
DT: Segmentation
```

## Trang PDF 5

```text

```

## Trang PDF 6

```text
How?
```

## Trang PDF 7

```text
Decision Tree: example
```

## Trang PDF 8

```text
Machine Learning Type of Decision Tree

  • Logical models use a logical expression to divide the instance
    space into segments and hence construct grouping models.
  • A logical expression is an expression that returns a Boolean value,
    i.e., a True or False outcome.
  • Once the data is grouped using a logical expression, the data is
    divided into homogeneous groupings for the problem we are trying
    to solve.
  • There are mainly two kinds of logical models: Tree
    models and Rule models.
```

## Trang PDF 9

```text
Machine Learning Type of Decision Tree

• Rule models consist of a collection of implications or IF-THEN rules.
• For tree-based models, the ‘if-part’ deﬁnes a segment and the ‘then-part’
  deﬁnes the behaviour of the model for this segment. Rule models follow the
  same reasoning.
• Tree models can be seen as a particular type of rule model where the if-
  parts of the rules are organised in a tree structure.
```

## Trang PDF 10

```text
     How does DT work?
                                                            age income student credit_rating buys_computer
                                                          <=30  high      no fair                 no
                                                          <=30  high      no excellent            no
                           age?                           31…40 high      no fair                 yes
                                                          >40   medium    no fair                 yes
                                                          >40   low      yes fair                 yes
                                                          >40   low      yes excellent            no
             <=30      overcast
                        31..40          >40               31…40 low      yes excellent            yes
                                                          <=30  medium    no fair                 no
                                                          <=30  low      yes fair                 yes
                                                          >40   medium yes fair                   yes
          student?         yes          credit rating?    <=30  medium yes excellent              yes
                                                          31…40 medium    no excellent            yes
                                                          31…40 high     yes fair                 yes
     no          yes              excellent       fair    >40   medium    no excellent            no



no                   yes           no               yes
```

## Trang PDF 11

```text
Decision Tree: General Architecture
```

## Trang PDF 12

```text
How to build Decision Tree for Classification?
```

## Trang PDF 13

```text
Problem example
```

## Trang PDF 14

```text
 Building Decision Trees
Attribute: Outlook, Temp, Humidity, Windy
```

## Trang PDF 15

```text
Which attribute for Segmentation?
```

## Trang PDF 16

```text
The Algorithm for building DT
```

## Trang PDF 17

```text
ID3 Algorithm for learning/building
Decision Tree
```

## Trang PDF 18

```text
Entropy
```

## Trang PDF 19

```text
     Attribute Selection Measures

      ID3 (Iterative Dichotomiser) decision tree algorithm uses information gain.




https://www.datacamp.com/community/tutorials/decision-tree-classification-python
```

## Trang PDF 20

```text
Attribute Selection Measures




Where,
•Info(D) is the average amount of information needed to identify the class label of a tuple in D.
•|Dj|/|D| acts as the weight of the jth partition.
•InfoA(D) is the expected informa-tion required to classify a tuple from D based on the
partitioning by A.
The attribute A with the highest information gain, Gain(A), is chosen as the splitting attribute at
node N().
```

## Trang PDF 21

```text
Attribute: ‘Outlook’
```

## Trang PDF 22

```text
Information Gain
```

## Trang PDF 23

```text
Attribute: ‘Humidity’
```

## Trang PDF 24

```text
IG of all attributes
```

## Trang PDF 25

```text
What is next?
```

## Trang PDF 26

```text
Continue for the remain data
```

## Trang PDF 27

```text
Overfitting in Decision Trees
```

## Trang PDF 28

```text
Avoiding Overfitting in Decision Trees
• How can we avoid overfitting?
   • Stop growing when data split is not statistically significant
   • Acquire more training data
   • Remove irrelevant attributes (manual process – not always possible)
   • Grow full tree, then post-prune
• How to select “best” tree:
   • Measure performance over training data
   • Measure performance over separate validation data set
   • Add complexity penalty to performance measure (heuristic: simpler is better)
```

## Trang PDF 29

```text
   Avoiding Overfitting in Decision Trees
   • Limiting Max-Depth
   • Pruning


It reduces the size of the
decision tree which might
slightly   increase    the
training     error     but
drastically decrease the
testing error. For this, it
become more adaptable.
```

## Trang PDF 30

```text
Pruning Decision Trees
```

## Trang PDF 31

```text
Gain Ratio
  •   Information gain is biased for the attribute with many outcomes. It means it prefers
      the attribute with a large number of distinct values. For instance, consider an
      attribute with a unique identifier such as customer_ID has zero info(D) because of
      pure partition. This maximizes the information gain and creates useless partitioning.
  •   C4.5, an improvement of ID3, uses an extension to information gain known as the
      gain ratio. Gain ratio handles the issue of bias by normalizing the information gain
      using Split Info.
```

## Trang PDF 32

```text
Gain Ratio
```

## Trang PDF 33

```text
Gini index
 Another decision tree algorithm CART (Classification and Regression Tree) uses the Gini
 method to create split points.




   Where, pi is the probability that a tuple in D belongs to class Ci.
   The Gini Index considers a binary split for each attribute. You can compute a weighted sum
   of the impurity of each partition. If a binary split on attribute A partitions data D into D1
   and D2, the Gini index of D is:
```

## Trang PDF 34

```text
Gini index
```

## Trang PDF 35

```text
DT using sklearn




 https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html
```

## Trang PDF 36

```text
DT for Regression




        https://www.saedsayad.com/decision_tree_reg.htm
```

## Trang PDF 37

```text
    DT Regressor
    • The ID3 algorithm can be used to construct a decision tree for regression by
      replacing Information Gain with Standard Deviation Reduction


Standard deviation
for one attribute:
```

## Trang PDF 38

```text

```

## Trang PDF 39

```text

```

## Trang PDF 40

```text

```

## Trang PDF 41

```text

```

## Trang PDF 42

```text

```

## Trang PDF 43

```text

```

## Trang PDF 44

```text

```

## Trang PDF 45

```text

```

## Trang PDF 46

```text

```

## Trang PDF 47

```text
sklearn.tree.DecisionTreeRegressor
```