# Lecture 2 - Principle of Machine Learning.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 2 - Principle of Machine Learning.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
               Lecture 2
Basic Principles of Statistical Machine
Learning and Naive Bayes Classifiers
              LÊ ANH CƯỜNG
           Ton Duc Thang University




                                          1
```

## Trang PDF 2

```text
Outline
1. The general model of learning from examples
2. Empirical risk minimization inductive principle
3. Probability Theory and Bayesian Classification
4. Generative and Discriminative Models
5. Naive Bayesian Classification




                                                     2
```

## Trang PDF 3

```text
The General Model of Learning from Examples
• Suppose that there is a functional relationship between two sets of
  objects X and Y:
                                 f: X -> Y
• Given a finite set of examples:
           D = {(xi,yi) | i=1,2,…,N} , where xi X and yi. Y

• The task here is to derive (i.e. to learn) the objective function f



                                                                        3
```

## Trang PDF 4

```text
Objective of Learning
• Learn to generalize from a finite set of examples
• The learnt function then can predict output y given a new input x




                                                                      4
```

## Trang PDF 5

```text
Classification and Regression
• y = f(x)
• If y is the real value ie Y = R then we have a regression problem
• If y is a value in a given finite discrete set, then we have a
  classification problem




                                                                      5
```

## Trang PDF 6

```text
Data Representation
• x is a vector of features
                              x = (x1, x2, ..., xd)
                                   X = Rd
• y is a real number in the regression problem
• y is in classification problem:
   • binary classification, y = {0,1} or {-1,+1}
   • multiple classes: y = {1, 2, ..., k} or one-hot vector (0,...0,1,0,...0)




                                                                                6
```

## Trang PDF 7

```text
Loss function
• Suppose that (x,y) is an example. We want to find the difference
  between the ground true value y and the predicted value h(x)
• For regression:

• For classification:




                                                                     7
```

## Trang PDF 8

```text
Expected Risk and Empirical Risk
• Expected risk/loss is the mean of L(y,h(x)) over the whole space X x Y




• Empirical risk/loss is the mean of L(y,h(x)) over the training dataset D




                                                                         8
```

## Trang PDF 9

```text
Empirical Risk

• For regression:




• For classification:




                        9
```

## Trang PDF 10

```text
Empirical risk minimization inductive principle.
(Nguyên lý quy nạp cực tiểu sai số thực nghiệm)

• We will consider the objective function f by the approximation function g as
  follows:




                                                                                 10
```

## Trang PDF 11

```text
Overfitting




              11
```

## Trang PDF 12

```text
Probability Theory for Statistical Machine
Learning
• Probability theory is a mathematical framework for quantifying our uncertainty about the
  world. It allows to reason effectively in situations where being certain is impossible.
  Probability theory is at the foundation of many machine learning algorithms.
• Probability Theory simply talks about how likely is the event to occur, and its value
  always lies between 0 and 1 (inclusive of 0 and 1)




                                                                                             12
```

## Trang PDF 13

```text
Some basic probabilities




                           13
```

## Trang PDF 14

```text
Probability Theory for Statistical Machine
Learning
Discrete Probability Distribution: The           Continuous Probability Distribution: The
mathematical definition of a discrete            mathematical definition of a continuous
                                                 probability function, f(x), is a function that
probability function, p(x), is a function that   satisfies the following properties. This is
satisfies the following properties. This is      referred as Probability Density Function.
referred as Probability Mass Function.




                                                                                        14
```

## Trang PDF 15

```text
Probability Theory for Statistical Machine
Learning




                                             15
```

## Trang PDF 16

```text
Discriminate and Generative Models
 Let's say you have input data x and you want to classify the data into labels y.
 A generative model learns the joint probability distribution p(x,y) and a
 discriminative model learns the conditional probability distribution p(y|x)




                                                                                    16
```

## Trang PDF 17

```text
Discriminate and Generative Models
 Let's say you have input data x and you want to classify the data into labels y. A generative
 model learns the joint probability distribution p(x,y) and a discriminative model learns
 the conditional probability distribution p(y|x)



 Some popular discriminative algorithms are:            Some popular generative algorithms are:
 •k-nearest neighbors (k-NN)                            •Naive Bayes Classifier
 •Logistic regression                                   •Generative Adversarial Networks
 •Support Vector Machines                               •Gaussian Mixture Model
 •Decision Trees                                        •Hidden Markov Model
 •Random Forest                                         •Probabilistic context-free grammar
 •Artificial Neural Networks (ANNs)



                                                                                                 17
```

## Trang PDF 18

```text
Bayesian Classification




                          18
```

## Trang PDF 19

```text
Bayesian Classification




                          19
```

## Trang PDF 20

```text
Bayesian Classification and Expected Risk




Then, the expected Risk at input x will be:




                                              20
```

## Trang PDF 21

```text
Bayesian Classification and Expected Risk
• Suppose h(x) = cj, then:



• It means:



• So that to minimize the Expected Risk, it is equivalent to choose for
  maximizing P(cj|x)


                                                                          21
```

## Trang PDF 22

```text
Maximum Likelihood Estimation
• We are given a data set D = {x1,x2,...,xN}
• Suppose that the given examples come from the probability
  distribution with parameter θ
• We need to estimate θ that maximize p(D)
                        θ = argmax p(x1,x2,…,xN|θ)
• p(D) is likelihood of D
                           θ = argmax ∏ p(xi|θ)



                                                              22
```

## Trang PDF 23

```text
Maximum Likelihood Estimation

                          θ = argmax ∏ p(xi|θ)
• To make the calculation more convenient, we can use Maximum Log-
  likelihood:
                       θ = argmax∑ log(p(xi|θ))




                                                                     23
```

## Trang PDF 24

```text
Example
Suppose the problem is that there are 5 students taking the test with scores of 3, 6,
5, 9, 8 respectively. To model the scores of these students, we assume that the data
points are segregated. distributed according to the Gaussian distribution:




                                                                                    24
```

## Trang PDF 25

```text
Example




          μ = 6.2 and σ = 2.14
                                 25
```

## Trang PDF 26

```text
Naive Bayesian Classification




                                26
```

## Trang PDF 27

```text
27
```

## Trang PDF 28

```text
Naive Bayesian Classification
1. Model
2. Parameter Estimation with Different Distribution of Data




                                                              28
```

## Trang PDF 29

```text
NB Classification
• Bayesian classification




                            29
```

## Trang PDF 30

```text
NB Classification
• How to estimate the model’s parameters:



• X is represented by a vector of feature values




                                                   30
```

## Trang PDF 31

```text
NB classification
• How to estimate the model’s parameters:
The task now is to calculate/estimate the probabilities:



where P(cj) is the probability of a class cj, and P(xj|ck) is the probability
of a value xj (of a feature jth) with the condition of class ck.
These probabilities are estimated based on the probability distribution
of:


                                                                                31
```

## Trang PDF 32

```text
NB classification
• How to estimate the model’s parameters:
These probabilities are estimated based on the probability distribution of:

where: c is the class variable
        x is feature value variable

for example: P(c=N), P(c=P)
             P(outlook = sunny | c=P)


                                                                              32
```

## Trang PDF 33

```text
NB Classification
• What are the parameters of the NB Model?



• What is the inference process of the NB Model?
   • given input:

   • we have: ?




                                                   33
```

## Trang PDF 34

```text
NB Classification
• What are the parameters of the NB Model?



• What is the inference process of the NB Model?
   • given input:

   • we have:




                                                   34
```

## Trang PDF 35

```text
NB Classification
• Parameter Estimation



• Then:




                         35
```

## Trang PDF 36

```text
Multinomial NB




                 36
```

## Trang PDF 37

```text
Gaussian NB
 When working with continuous data, an assumption often taken is that the
 continuous values associated with each class are distributed according to a normal
 (or Gaussian) distribution. The likelihood of the features is assumed to be”




                                                                                      37
```

## Trang PDF 38

```text
Other NB Classifiers
• Complement Naive Bayes
• Bernoulli Naive Bayes
• Categorical Naive Bayes




 Reference:
 • https://scikit-learn.org/stable/modules/naive_bayes.html


                                                              38
```

## Trang PDF 39

```text
Practice
• https://www.kaggle.com/code/prashant111/naive-bayes-classifier-in-
  python




                                                                       39
```