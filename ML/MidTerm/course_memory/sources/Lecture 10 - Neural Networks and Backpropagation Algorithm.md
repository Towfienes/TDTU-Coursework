# Lecture 10 - Neural Networks and Backpropagation Algorithm.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 10 - Neural Networks and Backpropagation Algorithm.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
       Neural Networks
and Backpropagation Algorithm
           Lê Anh Cường
               TDTU
```

## Trang PDF 2

```text
Outline
• General architecture of Neural Networks (NN)
• Forward computation for Feed-Forward Neural Networks (FFNN)
• Backpropagation for learning NN’s parameters
• Implementation
```

## Trang PDF 3

```text
Neural Network
```

## Trang PDF 4

```text
Neural Network
```

## Trang PDF 5

```text
Neural Network
```

## Trang PDF 6

```text
Neural Network: Definition
• Artificial neural networks (ANNs), usually simply
  called neural networks (NNs).
• An ANN is based on a collection of connected units
  or nodes called artificial neurons.
• Each connection can transmit a signal to other
  neurons.
• The connections are called edges which typically
  have a weight that adjusts as learning proceeds. The
  weight increases or decreases the strength of the
  signal at a connection.
• Different layers may perform different
  transformations on their inputs.
```

## Trang PDF 7

```text
NN Types
```

## Trang PDF 8

```text
Recurrent Neural Network
```

## Trang PDF 9

```text
Multiple Perceptron vs Neural Networks




https://en.wikipedia.org/wiki/Multilayer_perceptron
```

## Trang PDF 10

```text
Outline
• General architecture of Neural Networks (NN)
• Forward computation for Feed-Forword Neural Networks (FFNN)
• Backpropagation for learning NN’s parameters
• Implementation
```

## Trang PDF 11

```text
FFNN and forward Computation
```

## Trang PDF 12

```text
A Neural
```

## Trang PDF 13

```text
Example




      https://stevenmiller888.github.io/mind-how-to-build-a-neural-network/
```

## Trang PDF 14

```text
Example
```

## Trang PDF 15

```text
Example
```

## Trang PDF 16

```text
Example
```

## Trang PDF 17

```text
Outline
• General architecture of Neural Networks (NN)
• Forward computation for Feed-Forword Neural Networks (FFNN)
• Backpropagation for learning FFNN’s parameters
• Implementation
```

## Trang PDF 18

```text
Backpropagation for NN

• The backpropagation algorithm was originally introduced in the 1970s, but its
  importance wasn't fully appreciated until a famous 1986 paper by David
  Rumelhart, Geoffrey Hinton, and Ronald Williams.
• The paper describes several neural networks where backpropagation works
  far faster than earlier approaches to learning, making it possible to use
  neural nets to solve problems which had previously been insoluble.
• Today, the backpropagation algorithm is the workhorse of learning in neural
  networks.
```

## Trang PDF 19

```text
Loss/Cost function
```

## Trang PDF 20

```text
Loss/Cost function
```

## Trang PDF 21

```text
Learning Weights by Gradient Descent


                                          &C
                              !" = !" − %
                                          &!"
```

## Trang PDF 22

```text
    layer         layer     layer
     l-1            l        l+1


          .         .
          .         .




k             j


      .                 .
      .                 .
```

## Trang PDF 23

```text

```

## Trang PDF 24

```text

```

## Trang PDF 25

```text
Gradient Calculation
```

## Trang PDF 26

```text
Calculate for Gradient at the last layer L
```

## Trang PDF 27

```text
Gradient Calculation
```

## Trang PDF 28

```text
Gradient Calculation
```

## Trang PDF 29

```text
Gradient Calculation
```

## Trang PDF 30

```text
Gradient Calculation
```

## Trang PDF 31

```text

```

## Trang PDF 32

```text
The backpropagation algorithm
```

## Trang PDF 33

```text
Outline
• General architecture of Neural Networks (NN)
• Forward computation for Feed-Forword Neural Networks (FFNN)
• Backpropagation for learning FFNN’s parameters
• Implementation
```

## Trang PDF 34

```text
Reference
• http://neuralnetworksanddeeplearning.com/chap2.html
```