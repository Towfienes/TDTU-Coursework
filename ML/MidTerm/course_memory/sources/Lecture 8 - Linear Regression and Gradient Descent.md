# Lecture 8 - Linear Regression and Gradient Descent.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 8 - Linear Regression and Gradient Descent.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
      Linear Regression
and Gradient Descent Algorithm
           LÊ ANH CƯỜNG
               TDTU




                                 1
```

## Trang PDF 2

```text
Recap from the previous lecture
• Role of machine learning and
  artificial intelligence.
• A general diagram of AI systems.
• Concepts: knowledge, reasoning,
  inference, model, learning.
• Issues in machine learning.
• Understanding machine learning
  concepts through examples.


                                     2
```

## Trang PDF 3

```text
Outline
1. Supervised learning for classification and regression problems
2. Linear Regression (LR) model
3. Training LR by Gradient Descent Algorithm
4. Implementation LR




                                                                    3
```

## Trang PDF 4

```text
Supervised learning vs Unsupervised learning
                             input




    Training   Learning      Model
      data




                             output


                                           4
```

## Trang PDF 5

```text
Regression vs Classification
• Classification is about predicting a label and Regression is about
  predicting a quantity.
• Classification is the problem of predicting a discrete class label output
  for an example. The predicted label is from a set of predefined labels.
   • For example: predict an email is spam or ham
• Regression is the problem of predicting a continuous quantity output
  for an example.
   • For example: predict house price from its features (i.e. information).



                                                                              5
```

## Trang PDF 6

```text
Regression (Hồi qui)
• From Height, predict Weight?

                                 Training data
                                 (x1, y1)
                                 (x2, y2)
                                 .
                                 .
                                 .
                                 (xn, yn)




                                                 6
```

## Trang PDF 7

```text
Linear Regression
• How is the relationship between Height and Weight?




                                                       7
```

## Trang PDF 8

```text
Linear Regression
Suppose that Weight linearly depends on Height




                                                 8
```

## Trang PDF 9

```text
Simple Linear Regression: one variable

Training data: (x1, y1), (x2, y2). . . (xn, yn)


! = # x = %& + %( )

Learn w0 and w1




                                                  9
```

## Trang PDF 10

```text
 Loss Function

 Training data: (x1, y1), (x2, y2). . . (xn, yn)




! = # x = %& + %( )


Prediction by the model: x -> f(x)
For every training example (xi, yi) we
compare f(xi) with yi
                                                   10
```

## Trang PDF 11

```text
   Loss Function
Training data:
(x1, y1), (x2, y2). . . (xn, yn)




! = # x = %& + %( )

                             MSE: Mean Square Error




                                                      11
```

## Trang PDF 12

```text
  Loss Function

Training data:
(x1, y1), (x2, y2). . . (xn, yn)                ! = # x = %& + %( )




                                   4              4
                              1                 1
                  Loss = - =    1(# )2 − !2 ) = 1((%& + %()2 ) − !2 )8
                                             8
                             20                2n
                                   23(           23(


                                                                         12
```

## Trang PDF 13

```text
Simple Linear Regression: one variable

! = # x = %& + %( )
                4                  4
            1              8
                               1
Loss = - =    1(# )2 − !2 ) =    1((%& + %( )2 ) − !2 )8
           20                 20
                23(               23(


Parameters: %& , %(
Goal: minimize Loss function
      :;          :;
         = 0,        =0
     :<=         :<?

                                                           13
```

## Trang PDF 14

```text
Linear Regression: Learning
Goal: minimize Loss function           *
       !"        !"                 1
      !#
         = 0,   !#
                   = 0          4=
                                   27
                                      8(. /,) − 1, )9 =
        $          (                  ,-)

                                           *
                                     1
                                  =    8((:; + :) /,) ) − 1, )9
                                    27
                                        ,-)
 !"     )
      = ∑*
         ,-) . /,) − 1,
!#$     *
 !"     )
   =   ∑*
        ,-) (. /,) − 1, ) /,)
!#(  *



                                                                  14
```

## Trang PDF 15

```text
Linear Regression: Learning by Gradient
Descent




                                          15
```

## Trang PDF 16

```text
Linear Regression: Learning by Gradient
Descent
                              Update parameters:



                                            Learning rate




                                           &'
                               !" = !" − %
                                           &!"


                                                     16
```

## Trang PDF 17

```text
Linear Regression: Learning by Gradient
Descent




                                          17
```

## Trang PDF 18

```text
Learning progress




                    18
```

## Trang PDF 19

```text
 Multiple Linear Regression
(!i, yi)
!i = () i1, …, )k )

-i = . Xi = 01 )i0 + 04 )i1+ … + 05 )ik
                      ?              ?
            1             A
                              1
Loss = 9 =    <(. X − -= ) =    <((0B1 + 0B4 ) + ⋯ + 0B5 )) − -= )A =
           2;                2;
                  =>4               =>4



                DE        4
                  =   ∑?
                       =>4 (. X = − -= ) )=I
               DF   ? G

                                                                        19
```

## Trang PDF 20

```text
Issues:
Linear Regression is sensitive with outliers




                                               20
```

## Trang PDF 21

```text
Summary
• Supervised learning vs unsupervised learning.
• Classification vs regression
• Linear regression form.
• Learning Linear Regression model by Gradient Descent algorithm?
• One variable and Multiple variable of Linear Regression




                                                                    21
```

## Trang PDF 22

```text
Exercise
• Implement Linear Regression for the problem of house pricing with
  multiple variables:
   • Firstly derive steps and mathematical formulas in the algorithm.
   • Secondly, implementation using python.




                                                                        22
```

## Trang PDF 23

```text
Answer the questions:
1. What is the objective of a supervised learning model? General model?
2. What is linear regression model?
3. Formulating the linear regression model with single variable?
   • Function y = f(x)
   • Loss function
4. Learning parameters by Gradient Descent
   • Update parameters?
   • Learning rate?
5. Implementation
6. What are limitations of linear regression
                                                                          23
```

## Trang PDF 24

```text
24
```

## Trang PDF 25

```text
25
```