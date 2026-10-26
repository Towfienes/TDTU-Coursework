# Lecture 7 - SVM 2024.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 7 - SVM 2024.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
Support Vector Machines

         Lê Anh Cường
            TDTU
```

## Trang PDF 2

```text
History of Neural Network




  12/18/2024           Lê Anh Cường - 2020   2
```

## Trang PDF 3

```text
What is SVM
•   Suppose we have a dataset that has two classes (green and blue). We
    want to classify that the new data point as either blue or green.
```

## Trang PDF 4

```text
Hyperplane
```

## Trang PDF 5

```text
What is SVM
• To classify these points, we can have
  many decision boundaries, but the
  question is which is the best and how do
  we find it?

• Since we are plotting the data points
  in a 2-dimensional graph we call this
  decision boundary a straight line but if
  we have more dimensions, we call this
  decision boundary a “hyperplane”
```

## Trang PDF 6

```text
SVM aims to maximize the margin
• The best hyperplane is that plane that has the maximum distance from both the classes, and this is
  the main aim of SVM. This is done by finding different hyperplanes which classify the labels in the
  best way then it will choose the one which is farthest from the data points or the one which has a
  maximum margin.
```

## Trang PDF 7

```text

```

## Trang PDF 8

```text
SVM Learning: Maximize Margin
```

## Trang PDF 9

```text

```

## Trang PDF 10

```text

```

## Trang PDF 11

```text

```

## Trang PDF 12

```text
Hard margin
```

## Trang PDF 13

```text
Soft margin
```

## Trang PDF 14

```text
Kernels in Support Vector Machine
  • The most interesting feature of SVM is that it can even work with a non-linear
    dataset and for this, we use “Kernel Trick” which makes it easier to classifies
    the points. Suppose we have a dataset like this:
```

## Trang PDF 15

```text
Data Transform from the original space to
higher dimension space
```

## Trang PDF 16

```text

```

## Trang PDF 17

```text
Data Transform from the original space to
higher dimension space
```

## Trang PDF 18

```text
Kernel Functions
• Role of Kernel Functions in Support Vector Machines (SVM)
   • Kernel functions play a crucial role in SVM by enabling the algorithm to solve
     non-linear classification or regression problems. The kernel function
     implicitly maps input data into a higher-dimensional space where the data
     becomes linearly separable, even if it is not linearly separable in the original
     input space.
```

## Trang PDF 19

```text
Kernel Definition
```

## Trang PDF 20

```text
Kernel definition: an important point
```

## Trang PDF 21

```text
Kernel Example
```

## Trang PDF 22

```text
Kernel example
```

## Trang PDF 23

```text
Kernel example


                 Prove it?
```

## Trang PDF 24

```text
Kernel Method
```

## Trang PDF 25

```text
Different kernel
```

## Trang PDF 26

```text

```

## Trang PDF 27

```text

```

## Trang PDF 28

```text

```

## Trang PDF 29

```text
Learning SVM
The original SVM optimization problem is given as follows:




Using the concept of Duality, the original SVM can be reformulated into its dual form, which is as follows.
```

## Trang PDF 30

```text
Learning SVM with Kernel function
```

## Trang PDF 31

```text
Inference in SVM
```

## Trang PDF 32

```text
Dual optimization problem
```

## Trang PDF 33

```text
SVM with Kernel
```

## Trang PDF 34

```text

```

## Trang PDF 35

```text
     Summary of SVM
•1
•2
•3
•4
•5
```