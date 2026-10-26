# Lecture 4 - Naive_bayes_classification.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 4 - Naive_bayes_classification.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
             TON DUC THANG UNIVERSITY
              Faculty of Information Technology
                      Computer Science

   Naïve Bayes Classification
                     LÊ ANH CƯỜNG




07/04/2022           IT701010 - Chapter 4 - Naïve Bayes Classification   1
```

## Trang PDF 2

```text
Outline
• Classification problems
• What kind of machine learning type for NB
  classifier
• Text categorization with NB
• MultiNominal NB classification
• Gausian NB classification
• Benulli NB classification
07/04/2022      IT701010 - Chapter 4 - Naïve Bayes Classification   2
```

## Trang PDF 3

```text
Classification Problem and Applications

             N A M E R A N K                           Y E A R S TE N U R E D
             M ik e   A s s is t a n t P r o f                  3                    no
             M a ry   A s s is t a n t P r o f                  7                    yes
             B ill    P ro fe s s o r                           2                    yes
             J im     A s s o c ia t e P r o f                  7                    yes
             D ave    A s s is t a n t P r o f                  6                    no
             A nne    A s s o c ia t e P r o f                  3                    no


07/04/2022                       IT701010 - Chapter 4 - Naïve Bayes Classification         3
```

## Trang PDF 4

```text
Classification Problem and Applications
               age income student credit_rating buys_computer
             <=30  high      no fair                 no
             <=30  high      no excellent            no
             31…40 high      no fair                 yes
             >40   medium    no fair                 yes
             >40   low      yes fair                 yes
             >40   low      yes excellent            no
             31…40 low      yes excellent            yes
             <=30  medium    no fair                 no
             <=30  low      yes fair                 yes
             >40   medium yes fair                   yes
             <=30  medium yes excellent              yes
             31…40 medium    no excellent            yes
             31…40 high     yes fair                 yes
             >40   medium    no excellent            no
07/04/2022             IT701010 - Chapter 4 - Naïve Bayes Classification   4
```

## Trang PDF 5

```text
Classification Problem and Applications
Is this spam?




07/04/2022     IT701010 - Chapter 4 - Naïve Bayes Classification   5
```

## Trang PDF 6

```text
Positive or negative movie review?
  •unbelievably disappointing
  •Full of zany characters and richly applied
   satire, and some great plot twists
  • this is the greatest screwball comedy ever
   filmed
  • It was pathetic. The worst part about it was
   the boxing scenes.
07/04/2022        IT701010 - Chapter 4 - Naïve Bayes Classification   6
```

## Trang PDF 7

```text
             What is the subject of this article?

  MEDLINE Article                    MeSH Subject Category Hierarchy
                                                        • Antogonists and
                                                          Inhibitors
                                                        • Blood Supply
                          ?                             • Chemistry
                                                        • Drug Therapy
                                                        • Embryology
                                                        • Epidemiology
07/04/2022                                              •…
                        IT701010 - Chapter 4 - Naïve Bayes Classification   7
```

## Trang PDF 8

```text
Outline
• Classification problems
• What kind of machine learning type for NB
  classifier
• Text categorization with NB
• MultiNominal NB classification
• Gausian NB classification
• Benulli NB classification
07/04/2022      IT701010 - Chapter 4 - Naïve Bayes Classification   8
```

## Trang PDF 9

```text
Probabilistic models
 • Probabilistic models see features and target variables as random
   variables.
 • The process of modelling represents and manipulates the level of
   uncertainty with respect to these variables.
 • There are two types of probabilistic models: Predictive (or
   Discriminative) and Generative.
 • Predictive probability models use the idea of a conditional
   probability distribution P (Y |X) from which Y can be predicted
   from X.
 • Generative models estimate the joint distribution P (Y, X).
07/04/2022                IT701010 - Chapter 4 - Naïve Bayes Classification   9
```

## Trang PDF 10

```text
Probabilistic models
      • Once we know the joint distribution for the generative models,
        we can derive any conditional or marginal distribution
        involving the same variables.
      • Thus, the generative model is capable of creating new data
        points and their labels, knowing the joint probability
        distribution.
      • The joint distribution looks for a relationship between two
        variables. Once this relationship is inferred, it is possible to
        infer new data points.



07/04/2022                  IT701010 - Chapter 4 - Naïve Bayes Classification   10
```

## Trang PDF 11

```text
Naïve Bayes
     • Naive bayes is a Generative model which is based on the joint probability,
       p( B, A), of the inputs B and the label A.
     • It makes their predictions by using Bayes rules to calculate p(A | B), and
       then picking the most likely label A.
     • Discriminative classifiers model the posterior p(A | B) directly, or learn a
       direct map from inputs B to the class labels .




07/04/2022                     IT701010 - Chapter 4 - Naïve Bayes Classification      11
```

## Trang PDF 12

```text
Naïve Bayes




07/04/2022    IT701010 - Chapter 4 - Naïve Bayes Classification   12
```

## Trang PDF 13

```text
Text Classification: definition
•Input:
      • a document d
      • a fixed set of classes C = {c1, c2,…, cJ}

•Output: a predicted class c  C


07/04/2022              IT701010 - Chapter 4 - Naïve Bayes Classification   13
```

## Trang PDF 14

```text
             Classification Methods:
             Supervised Machine Learning
• Input:
      • a document d
      • a fixed set of classes C = {c1, c2,…, cJ}
      • A training set of m hand-labeled documents
        (d1,c1),....,(dm,cm)
• Output:
      • a learned classifier γ:d → c

07/04/2022                IT701010 - Chapter 4 - Naïve Bayes Classification   14
```

## Trang PDF 15

```text
  Naïve Bayes Intuition
• Simple (“naïve”) classification method based on Bayes
  rule
• Relies on very simple representation of document
   • Bag of words




  07/04/2022        IT701010 - Chapter 4 - Naïve Bayes Classification   15
```

## Trang PDF 16

```text
             The bag of words representation
               I love this movie! It's sweet,




γ(
               but with satirical humor. The
               dialogue is great and the
               adventure scenes are fun… It
               manages to be whimsical and
               romantic while laughing at the
               conventions of the fairy tale
               genre. I would recommend it to
               just about anyone. I've seen
               it several times, and I'm
                                                                            )=c
               always happy to see it again
               whenever I have a friend who
               hasn't seen it yet.
07/04/2022              IT701010 - Chapter 4 - Naïve Bayes Classification     16
```

## Trang PDF 17

```text
  Bayes’ Rule Applied to Documents and
  Classes
• For a document d and a class c


                         P(d | c)P(c)
              P(c | d) =
                            P(d)
 07/04/2022       IT701010 - Chapter 4 - Naïve Bayes Classification   17
```

## Trang PDF 18

```text
Naïve Bayes Classifier (I)

             cMAP = argmax P(c | d)                                       MAP is “maximum a
                                                                          posteriori” = most likely
                      cÎC                                                 class


                          P(d | c)P(c)
                 = argmax                                                         Bayes Rule

                     cÎC     P(d)
                 = argmax P(d | c)P(c)                                             Dropping the
                                                                                   denominator
                     cÎC
07/04/2022            IT701010 - Chapter 4 - Naïve Bayes Classification                           18
```

## Trang PDF 19

```text
 Naïve Bayes Classifier (II)

cMAP = argmax P(d | c)P(c)
                  cÎC

              = argmax P(x1, x2,… , xn | c)P(c)
                                                                             Document d
                                                                             represented as
                                                                             features x1..xn
                  cÎC




 07/04/2022              IT701010 - Chapter 4 - Naïve Bayes Classification              19
```

## Trang PDF 20

```text
             Naïve Bayes Classifier (IV)

 cMAP = argmax P(x1, x2,… , xn | c)P(c)
                   cÎC

                O(|X|n•|C|) parameters                                           How often does this class
                                                                                 occur?

                Could only be estimated if a very, very
                large number of training examples was                            We can just count the
                available.                                                       relative frequencies in a
                                                                                 corpus

07/04/2022                   IT701010 - Chapter 4 - Naïve Bayes Classification                          20
```

## Trang PDF 21

```text
               Multinomial Naïve Bayes Independence
               Assumptions
                    P(x1, x2,… , xn | c)
• Bag of Words assumption: Assume position doesn’t
  matter
• Conditional Independence: Assume the feature
  probabilities P(xi|cj) are independent given the class c.

  P(x1,… , xn | c) = P(x1 | c)·P(x2 | c)·P(x3 | c)·...·P(xn | c)
  07/04/2022            IT701010 - Chapter 4 - Naïve Bayes Classification   21
```

## Trang PDF 22

```text
             Multinomial Naïve Bayes Classifier

 cMAP = argmax P(x1, x2,… , xn | c)P(c)
                  cÎC


    cNB = argmax P(c j )Õ P(x | c)
                  cÎC                          xÎX



07/04/2022              IT701010 - Chapter 4 - Naïve Bayes Classification   22
```

## Trang PDF 23

```text
             Applying Multinomial Naive Bayes
             Classifiers to Text Classification

 positions  all word positions in test document



             cNB = argmax P(c j )
                     c j ÎC
                                                              Õ P(x | c )     i   j
                                                       iÎ positions


07/04/2022                IT701010 - Chapter 4 - Naïve Bayes Classification           23
```

## Trang PDF 24

```text
                                                                               Sec.13.3


             Learning the Multinomial Naïve Bayes Model

•First attempt: maximum likelihood estimates
    • simply use the frequencies in the data

                                          doccount(C = c j )
                       P̂(c j ) =
                                                            N doc
                                               count(wi , c j )
                   P̂(wi | c j ) =
                                            å count(w, c j )
07/04/2022                                 wÎV
                           IT701010 - Chapter 4 - Naïve Bayes Classification         24
```

## Trang PDF 25

```text
    Parameter estimation

                   count(wi , c j )            fraction of times word wi appears
P̂(wi | c j ) =
                  å count(w, c j )           among all words in documents of topic cj
                  wÎV


  •Create mega-document for topic j by
   concatenating all docs in this topic
       • Use frequency of w in mega-document

    07/04/2022                        IT701010 - Chapter 4 - Naïve Bayes Classification   25
```

## Trang PDF 26

```text
An Example
• I like this book: c1
• I do not like this movie: c2
• She loves this book: c1
• He do not like this book: c2
• I and her love the movie: c1
• P(c1)= ? P(c2)=?
• P(this|c1) = ?
• P(this|c2) = ?
07/04/2022          IT701010 - Chapter 4 - Naïve Bayes Classification   26
```

## Trang PDF 27

```text
                                                                                       Sec.13.3


      Problem with Maximum Likelihood
• What if we have seen no training documents with the word fantastic and classified
  in the topic positive (thumbs-up)?
                                                count("fantastic", positive)
                     P̂("fantastic" positive) =                              = 0
                                                   å count(w, positive)
                                                           wÎV
• Zero probabilities cannot be conditioned away, no matter the other evidence!


                      cMAP = argmaxc P̂(c)Õ P̂(xi | c)
                                                                        i




      07/04/2022                   IT701010 - Chapter 4 - Naïve Bayes Classification         27
```

## Trang PDF 28

```text
             Laplace (add-1) smoothing for Naïve Bayes

                           count(wi , c) +1
             P̂(wi | c) =
                          å (count(w, c))+1)
                       wÎV

                              count(wi , c) +1
                     =
                       æ                   ö
                       çç å count(w, c)÷÷ + V
                        è wÎV              ø
07/04/2022                 IT701010 - Chapter 4 - Naïve Bayes Classification   28
```

## Trang PDF 29

```text
                 Multinomial Naïve Bayes: Learning

• From training corpus, extract Vocabulary
• Calculate P(cj) terms                            • Calculate P(wk | cj) terms
   • For each cj in C do              • Textj  single doc containing all docsj
          docsj  all docs with class • For each word wk in Vocabulary
          =c                               nk  # of occurrences of wk in Textj
                 j           | docs j |
           P(c j ) ¬                                                                                nk + a
                       | total # documents|                                P(wk | c j ) ¬
                                                                                            n + a | Vocabulary |

    07/04/2022                      IT701010 - Chapter 4 - Naïve Bayes Classification                      29
```

## Trang PDF 30

```text
             Laplace (add-1) smoothing: unknown words

  Add one extra word to the vocabulary, the “unknown word” wu


                                     count(wu, c) +1
               P̂(wu | c) =
                              æ                ö
                              çç å count(w, c)÷÷ + V +1
                               è wÎV           ø
                                                         1
                         =
                              æ                ö
                              çç å count(w, c)÷÷ + V +1
07/04/2022
                               è wÎV           ø
                               IT701010 - Chapter 4 - Naïve Bayes Classification   30
```

## Trang PDF 31

```text
                                                       Doc        Words                                           Class
                               Nc   Training           1          Chinese Beijing Chinese                         c
                     P̂(c) =
                               N                       2          Chinese Chinese Shanghai                        c
                                                       3          Chinese Macao                                   c
                  count(w, c) +1
P̂(w | c) =                                            4          Tokyo Japan Chinese                             j
                  count(c)+ | V |   Test               5          Chinese Chinese Chinese Tokyo Japan             ?
   Priors:
   P(c)= 3
          4 1                                                                      Choosing a class:
   P(j)=    4                                                                      P(c|d5)  3/4 * (3/7)3 * 1/14 * 1/14
        Conditional Probabilities:                                                                  ≈ 0.0003
        P(Chinese|c) = (5+1) / (8+6) = 6/14 = 3/7
        P(Tokyo|c) = (0+1) / (8+6) = 1/14
        P(Japan|c) = (0+1) / (8+6) = 1/14                                          P(j|d5)  1/4 * (2/9)3 * 2/9 * 2/9
        P(Chinese|j) = (1+1) / (3+6) = 2/9                                                          ≈ 0.0001
        P(Tokyo|j) = (1+1) / (3+6) = 2/9
        P(Japan|j)    = (1+1) / (3+6) = 2/9
     07/04/2022                            IT701010 - Chapter 4 - Naïve Bayes Classification                        31
```

## Trang PDF 32

```text
                                                                                                      Sec. 15.2.4


   Evaluation: Classic Reuters-21578 Data Set
    • Most (over)used data set, 21,578 docs (each 90 types, 200 toknens)
    • 9603 training, 3299 test articles (ModApte/Lewis split)
    • 118 categories
       • An article can be in more than one category
       • Learn 118 binary category distinctions
    • Average document (with at least one category) has 1.24 classes
    • Only about 10 out of 118 categories are large
                         • Earn (2877, 1087)                                  • Trade (369,119)
                         • Acquisitions (1650, 179)                           • Interest (347, 131)
Common categories        • Money-fx (538, 179)                                • Ship (197, 89)
                         • Grain (433, 149)                                   • Wheat (212, 71)
(#train, #test)                                                               • Corn (182, 56)
   07/04/2022            • Crude
                            IT701010(389,
                                     - Chapter189)
                                               4 - Naïve Bayes Classification                               32
```

## Trang PDF 33

```text
                                                                                                           Sec. 15.2.4

     Reuters Text Categorization data set (Reuters-
     21578) document
<REUTERS TOPICS="YES" LEWISSPLIT="TRAIN" CGISPLIT="TRAINING-SET" OLDID="12981"
NEWID="798">
<DATE> 2-MAR-1987 16:51:43.42</DATE>
<TOPICS><D>livestock</D><D>hog</D></TOPICS>
<TITLE>AMERICAN PORK CONGRESS KICKS OFF TOMORROW</TITLE>
<DATELINE> CHICAGO, March 2 - </DATELINE><BODY>The American Pork Congress kicks off tomorrow,
March 3, in Indianapolis with 160 of the nations pork producers from 44 member states determining industry positions
on a number of issues, according to the National Pork Producers Council, NPPC.
   Delegates to the three day Congress will be considering 26 resolutions concerning various issues, including the future
direction of farm policy and the tax law as it applies to the agriculture sector. The delegates will also debate whether to
endorse concepts of a national PRV (pseudorabies virus) control and eradication program, the NPPC said.
  A large trade show, in conjunction with the congress, will feature the latest in technology in all areas of the industry,
the NPPC added. Reuter
    07/04/2022
&#3;</BODY></TEXT></REUTERS>                IT701010 - Chapter 4 - Naïve Bayes Classification                      33
```

## Trang PDF 34

```text
                                                                      Sec. 15.2.4


Micro- vs. Macro-Averaging
• If we have more than one class, how do we
   combine multiple performance measures into one
   quantity?
• Macroaveraging: Compute performance for each
  class, then average.
• Microaveraging: Collect decisions for all classes,
  compute contingency table, evaluate.

07/04/2022        IT701010 - Chapter 4 - Naïve Bayes Classification         34
```

## Trang PDF 35

```text
                                                                                                                           Sec. 15.2.4


                     Micro- vs. Macro-Averaging: Example
         Class 1                               Class 2                                            Micro Ave. Table
                     Truth:   Truth:                           Truth:          Truth:                             Truth:      Truth:
                     yes      no                               yes             no                                 yes         no
Classifier: yes      10       10       Classifier: yes         90              10               Classifier: yes   100         20

Classifier: no       10       970      Classifier: no          10              890              Classifier: no    20          1860



   • Macroaveraged precision: (0.5 + 0.9)/2 = 0.7
   • Microaveraged precision: 100/120 = .83
   • Microaveraged score is dominated by score on common classes
        07/04/2022                          IT701010 - Chapter 4 - Naïve Bayes Classification                                      35
```

## Trang PDF 36

```text
                  Development Test Sets and Cross-validation

   Training set                   Development Test Set                                    Test Set
• Metric: P/R/F1 or Accuracy
• Unseen test set                                                                        Training Set Dev Test
   • avoid overfitting (‘tuning to the test set’)
   • more conservative estimate of performance Training Set                                                 Dev Test
• Cross-validation over multiple splits
       • Handle sampling errors from different datasets                                  Dev Test         Training Set
   • Pool results over each split
   • Compute pooled dev set performance
     07/04/2022                      IT701010 - Chapter 4 - Naïve Bayes Classification
                                                                                                     Test Set   36
```

## Trang PDF 37

```text
Code




             https://www.programmersought.com/article/10835149414/
07/04/2022                        IT701010 - Chapter 4 - Naïve Bayes Classification   37
```

## Trang PDF 38

```text
Gaussian Naive Bayes

     • In Gaussian Naive Bayes, continuous values associated with each
       feature are assumed to be distributed according to a Gaussian
       distribution.
     • A Gaussian distribution is also called Normal distribution. When
       plotted, it gives a bell shaped curve which is symmetric about the mean
       of the feature values as shown below:




07/04/2022                    IT701010 - Chapter 4 - Naïve Bayes Classification   38
```

## Trang PDF 39

```text
Gaussian Naive Bayes




The likelihood of the features is assumed to be Gaussian, hence, conditional
probability is given by:



07/04/2022                   IT701010 - Chapter 4 - Naïve Bayes Classification   39
```

## Trang PDF 40

```text
07/04/2022   IT701010 - Chapter 4 - Naïve Bayes Classification   40
```

## Trang PDF 41

```text
Bernoulli Naive Bayes

     •Bernoulli Naive Bayes: In the multivariate Bernoulli event model,
     features are independent booleans (binary variables) describing inputs. Like
     the multinomial model, this model is popular for document classification
     tasks, where binary term occurrence(i.e. a word occurs in a document or
     not) features are used rather than term frequencies(i.e. frequency of a word
     in the document).




07/04/2022                     IT701010 - Chapter 4 - Naïve Bayes Classification    41
```

## Trang PDF 42

```text
Code




    https://towardsdatascience.com/sentiment-analysis-introduction-to-naive-bayes-
    algorithm-96831d77ac91



07/04/2022                   IT701010 - Chapter 4 - Naïve Bayes Classification   42
```