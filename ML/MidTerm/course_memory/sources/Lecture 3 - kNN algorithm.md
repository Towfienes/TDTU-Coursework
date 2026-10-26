# Lecture 3 - kNN algorithm.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 3 - kNN algorithm.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
          Lecture 3
K-Nearest-Neighbors Algorithm
    and Data Conversion
           Lê Anh Cường
               TDTU
```

## Trang PDF 2

```text
Supervised Learning
• Classification   The main difference between them is that the
                   output variable in regression is numerical (or
• Regression       continuous) while that for classification is
                   categorical (or discrete).




                                                                    2
```

## Trang PDF 3

```text
Unsupervised Learning
 Unsupervised Learning is a machine learning technique in
 which the users do not need to supervise the model. Instead,
 it allows the model to work on its own to discover patterns and
 information that was previously undetected.




                                                                   3
```

## Trang PDF 4

```text
KNN is a Method in Instance-Based Learning
• Instance-based learning is often termed lazy learning, as there is typically
  no “transformation” of training instances into more general “statements”



                                       New
                                     instance




     Supervised
      examples
                                     kNN                   label



                         Directly
                       computation
```

## Trang PDF 5

```text
KNN is a Method in Instance-Based Learning
• Instance-based learning is often termed lazy learning, as there is typically
  no “transformation” of training instances into more general “statements”

                    Directly                 label
                  computation

                                                        New              label
                                    kNN
                                                      instance




     Supervised
      examples                    Learning             Model




                       Generalization                  label
```

## Trang PDF 6

```text
K-Nearest-Neighbors Algorithm
• A case is classified by a majority voting of its neighbors, with the case
  being assigned to the class most common among its K nearest
  neighbors measured by a Distance Function.

• If K=1, then the case is simply assigned to the class of its nearest
  neighbor
```

## Trang PDF 7

```text
What is the most possible label for c?
• Solution: Looking for the nearest K neighbors of c.
• Take the majority label as c’s label
• Let’s suppose k = 3:
```

## Trang PDF 8

```text
Distance Function Measurements
```

## Trang PDF 9

```text

```

## Trang PDF 10

```text

```

## Trang PDF 11

```text
Example
          class
```

## Trang PDF 12

```text
Example
```

## Trang PDF 13

```text
kNN for Classification
 • A simple implementation of KNN classification is a majority voting
   mechanism.


• Given: training examples D={xi, yi}, and a new example x
where
   • xi: attribute-value representation of the example ith
   • yi: corresponding label or class of example ith
• Algorithm:
   • Compute distance D(x,xj) for every xj of the training data D
   • Select k closest instances xi1, …, xik with their labels are yi1,..yik
   • y = majority (yi1,..yik) is the predicted label of x
```

## Trang PDF 14

```text
Example
```

## Trang PDF 15

```text
kNN for Regression
 • A simple implementation of KNN regression is to calculate the
   average of the numerical target of the K nearest neighbors.
```

## Trang PDF 16

```text
Example
```

## Trang PDF 17

```text
Distance-weighted k-NN

                                         k
        • Replace   fˆ (q ) = arg max ∑ δ (v, f ( xi ))                            by:
                               v∈V    i =1

                                     k
                                                   1
                fˆ (q) = argmax ∑                            2   δ (v, f (x i ))
                            v ∈V     i=1     d( x i, x q )



    €
```

## Trang PDF 18

```text
Issues with Distance Metrics
• Most distance measures were designed for linear/real-valued
  attributes
• Two important questions in the context of machine learning:
   • How to handle nominal attributes
   • What to do when attribute types are mixed
```

## Trang PDF 19

```text

```

## Trang PDF 20

```text
Hamming Distance
• For category variables, Hamming distance can be used.
```

## Trang PDF 21

```text
Normalization
```

## Trang PDF 22

```text
Normalization
```

## Trang PDF 23

```text
Exercise
```

## Trang PDF 24

```text
What to do when attribute types are mixed
• Convert categorical values into numerical values
   • Binary values: convert to 0 and 1, for example ’male’, ‘female’
   • Multiple degress, such as ‘low’, ‘average’, and ‘high’: convert to 1, 2, 3
   • if the values are “Red”, “Green”, “Blue” (or more generally, something that
     has no intrinsic order): convert to [1,0,0], [0,1,0], [0,0,1]
• Normalize or scale the data into the same interval.
```

## Trang PDF 25

```text
Exercise
```

## Trang PDF 26

```text
KDTree




 https://viblo.asia/p/gioi-thieu-thuat-toan-kd-trees-nearest-
 neighbour-search-RQqKLvjzl7z
```

## Trang PDF 27

```text
Nearest Neighbor via KDTree
```

## Trang PDF 28

```text
Summary
   • kNN can deal with complex and arbitrary decision
     boundaries.
   • Despite its simplicity, researchers have shown that the
     classification accuracy of kNN can be quite strong and
     in many cases as accurate as those elaborated
     methods.
   • kNN is slow at the classification time
   • kNN does not produce an understandable model



                                                               28
```