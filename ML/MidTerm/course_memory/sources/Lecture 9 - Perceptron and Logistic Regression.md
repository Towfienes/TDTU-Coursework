# Lecture 9 - Perceptron and Logistic Regression.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 9 - Perceptron and Logistic Regression.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
  Perceptron and
Logistic Regression
      Lê Anh Cường
          TDTU
```

## Trang PDF 2

```text
Outline
1. Biological Neuron and Artificial Neural Network
2. Perceptron and Learning Perceptron
3. Information Theory
4. Logistic function
5. Logistic classification with Cross Entropy Loss
```

## Trang PDF 3

```text
References
• https://www.xenonstack.com/blog/artificial-neural-network-
  applications/

• https://peterroelants.github.io/posts/cross-entropy-logistic/
• https://peterroelants.github.io/posts/cross-entropy-softmax/
```

## Trang PDF 4

```text
Biological Neuron



 •Function of Dendrite (đuôi gai)
 It receives signals from other neurons.
 •Soma (cell body)
 It sums all the incoming signals to generate input.
 •Axon Structure (cấu trúc trục)
 When the sum reaches a threshold value, neuron fires and the signal travels down the axon to the
 other neurons.
 •Synapses Working (khớp thần kinh)
 The point of interconnection of one neuron with other neurons. The amount of signal transmitted
 depend upon the strength (synaptic weights) of the connections.
 The connections can be inhibitory (decreasing strength) or excitatory (increasing strength) in nature.
```

## Trang PDF 5

```text
     Perceptron
• The perceptron is the elementary unit of an Artificial Neural Network.
```

## Trang PDF 6

```text
Components of a Perceptron
```

## Trang PDF 7

```text
Components of a Perceptron
1.Input Values: A set of values or a dataset for predicting the output value. They are also
described as a dataset’s features and dataset.
2.Weights: The real value of each feature is known as weight. It tells the importance of that
feature in predicting the output value.
3.Bias: The activation function is shifted towards the left or right using bias. You may understand
it simply as the y-intercept in the line equation.
4.Summation Function: The summation function binds the weights and inputs together. It is a
function to find their sum.
5.Activation Function: It introduces non-linearity in the perceptron model.
```

## Trang PDF 8

```text
Activation functions
```

## Trang PDF 9

```text
Activation functions
```

## Trang PDF 10

```text
Multi Layer Perceptron
• A multi layer perceptron
  (MLP) is a class of feed
  forward artificial neural
  network. MLP consists of at
  least three layers of nodes:
  an input layer, a hidden
  layer and an output layer.
  Except for the input nodes,
  each node is a neuron that
  uses a nonlinear activation
  function. MLP utilizes a
  supervised          learning
  technique called back
  propagation for training.
```

## Trang PDF 11

```text
Learning Perceptron
```

## Trang PDF 12

```text
Learning Perceptron
```

## Trang PDF 13

```text
Learning Perceptron: Loss function


      Loss function counts the missed classified, in that case yi and
      sgn(wTx) are opposite signs, therefore: −yisgn(wTxi)=1.
      However, it is discrete then difficult to calculate derivative
```

## Trang PDF 14

```text
Learning Perceptron: update weight
                            Loss function




                             derivative




                           Update weight
```

## Trang PDF 15

```text
Part II: Logistic Regression
```

## Trang PDF 16

```text
Example: house studying
Một nhóm 20 sinh viên dành thời gian trong khoảng từ 0 đến 6 giờ cho việc ôn thi. Thời
gian ôn thi này ảnh hưởng đến xác suất sinh viên vượt qua kỳ thi như thế nào?
```

## Trang PDF 17

```text
Example: house studying
```

## Trang PDF 18

```text
Example: house studying
```

## Trang PDF 19

```text
Logistic Regression
```

## Trang PDF 20

```text
Logistic Regression
```

## Trang PDF 21

```text
Logistic Regression
• Logistic regression is basically a
  supervised classification algorithm.
  In a classification problem, the
  target variable(or output), y, can
  take only discrete values for given
  set of features(or inputs), X.
• Contrary to popular belief, logistic
  regression a regression model. The
  model builds a regression model to
  predict the probability that a given
  data entry belongs to the category
  numbered as “1”.
```

## Trang PDF 22

```text
Entropy
```

## Trang PDF 23

```text
Kullback–Leibler Divergence
```

## Trang PDF 24

```text
Cross Entropy
```

## Trang PDF 25

```text
Cross Entropy
```

## Trang PDF 26

```text
Cross Entropy
```

## Trang PDF 27

```text
Cross Entropy in Machine Learning
```

## Trang PDF 28

```text
Cross Entropy: especial case
and machine learning
```

## Trang PDF 29

```text
Logistic Regression
```

## Trang PDF 30

```text
Logistic Function
```

## Trang PDF 31

```text

```

## Trang PDF 32

```text

```

## Trang PDF 33

```text

```

## Trang PDF 34

```text

```

## Trang PDF 35

```text
Cross-entropy loss function
for the logistic function
```

## Trang PDF 36

```text
Cross-entropy ~ Log likelihood
```

## Trang PDF 37

```text

```

## Trang PDF 38

```text

```

## Trang PDF 39

```text
Gradient Descent
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