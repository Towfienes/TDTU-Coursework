# Lecture 11-12 - DL introduction.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 11-12 - DL introduction.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
           Introduction of Deep Learning
             with Convolutional Neural
           Networks and Long Short Term
                      Memory
                    Lê Anh Cường
                        TDTU


11/17/22             Lê Anh Cường - 2020   1
```

## Trang PDF 2

```text
Outline
1. How to recognize Deep Learning networks/models:
      • Traditional statistical machine learning vs Deep Learning
      • Vanilla Neural Networks vs Deep Learning Networks
      • History of DL development
2. Convolutional Neural Network (CNN)
3. Reccurent Neural Network (RNN) and Long Short Term Memory
   (LSTM)
4. Transformer Models


11/17/22                              Lê Anh Cường - 2020           2
```

## Trang PDF 3

```text
AI, ML, NN and DL




11/17/22            Lê Anh Cường - 2020   3
```

## Trang PDF 4

```text
Traditional Statistical Machine Learning
vs Deep Learning




11/17/22            Lê Anh Cường - 2020    4
```

## Trang PDF 5

```text
Traditional Statistical Machine Learning
vs Deep Learning




11/17/22            Lê Anh Cường - 2020    5
```

## Trang PDF 6

```text
DL as Representation Learning




11/17/22          Lê Anh Cường - 2020   6
```

## Trang PDF 7

```text
End-to-End Model




11/17/22           Lê Anh Cường - 2020   7
```

## Trang PDF 8

```text
ML vs DL in Performance




11/17/22          Lê Anh Cường - 2020   8
```

## Trang PDF 9

```text
History of Deep Learning




  11/17/22             Lê Anh Cường - 2020   9
```

## Trang PDF 10

```text
Recent Deep Learning models
• Generative Adversarial Network (2014)
• Residual Neural Network (2015)
• Transformer (2017)




11/17/22                     Lê Anh Cường - 2020   10
```

## Trang PDF 11

```text
When the term Deep Learning?




11/17/22         Lê Anh Cường - 2020   11
```

## Trang PDF 12

```text
Deep Belief Network




11/17/22          Lê Anh Cường - 2020   12
```

## Trang PDF 13

```text
An autoencoder is a type of artificial neural network used to learn efficient data codings in
an unsupervised manner.[1] The aim of an autoencoder is to learn a representation (encoding)
for a set of data, typically for dimensionality reduction
  11/17/22                               Lê Anh Cường - 2020                                13
```

## Trang PDF 14

```text
An autoencoder is a type of artificial neural
network used to learn efficient data codings in
an unsupervised manner.[1] The aim of an                                A restricted Boltzmann machine (RBM) is
autoencoder is to learn                                                 a generative stochastic artificial neural network that
a representation (encoding) for a set of data,                          can learn a probability distribution over its set of
typically for dimensionality reduction                                  inputs.


11/17/22                                          Lê Anh Cường - 2020                                                    14
```

## Trang PDF 15

```text
Recognition of DL
• Deep: i.e. many layers/levels of data representation
• Big Data (large enough): for learning good features
• High Performance Computing: for doing with complex networks and
  big data




11/17/22                    Lê Anh Cường - 2020                     15
```

## Trang PDF 16

```text
      Convolutional Neural Network




11/17/22          Lê Anh Cường - 2020   16
```

## Trang PDF 17

```text
Outline
• What is CNN?
• Why CNN?
• CNN Explanation
• Implementation




11/17/22            Lê Anh Cường - 2020   17
```

## Trang PDF 18

```text
ConvNet History

• Convolutional neural networks, also called ConvNets, were first introduced in the 1980s
  by Yann LeCun for building an image recognition neural network.
• LeNet-5, a pioneering 7-level convolutional network by LeCun et al. in 1998, that
  classifies digits, was applied by several banks to recognize hand-written numbers on
  checks.
• Although CNNs were invented in the 1980s, their breakthrough in the 2000s required
  fast implementations on graphics processing units (GPUs).
• A similar GPU-based CNN by Alex Krizhevsky et al. won the ImageNet Large Scale
  Visual Recognition Challenge 2012. A very deep CNN with over 100 layers by
  Microsoft won the ImageNet 2015 contest




11/17/22                                   Lê Anh Cường - 2020                              18
```

## Trang PDF 19

```text
A general architecture of Convolutional
Neural Networks




11/17/22           Lê Anh Cường - 2020    19
```

## Trang PDF 20

```text
What is Convolutional Neural Network
     • Convolutional Neural Networks (CNNs) are simply neural networks
       that use Convolution Operation which is a specialized kind of linear
       operation.

     • CNNs are regularized versions of multilayer perceptrons.

     • CNNs take advantage of the hierarchical pattern in data and assemble
       more complex patterns using smaller and simpler patterns.




11/17/22                             Lê Anh Cường - 2020                      20
```

## Trang PDF 21

```text
Why ConvNets over Feed-Forward Neural
Nets?

•   A ConvNet is able to successfully
    capture the Spatial and Temporal
    dependencies.
•   The architecture performs a better
    fitting to the image dataset due to the
    reduction in the number of
    parameters.
•   The network can be trained to
    understand the sophistication of the
    image better.



11/17/22                                      Lê Anh Cường - 2020   21
```

## Trang PDF 22

```text
Convolution Layer — The Kernel




           The objective of the
           Convolution Operation is
           to extract the high-level
           features such as edges,
           from the input image.

11/17/22                               Lê Anh Cường - 2020   22
```

## Trang PDF 23

```text
Convolution Layer — The Kernel


                           Kernel




11/17/22          Lê Anh Cường - 2020   23
```

## Trang PDF 24

```text
Multi-Channel Input and Filter




                A common convolution layer actually consist of multiple such
                filters. For the sake of simplicity in the discussion to follow,
                assume the presence of only one filter unless specified, since
                the same behavior is replicated across all the filters.

  11/17/22                                Lê Anh Cường - 2020                      24
```

## Trang PDF 25

```text
a multi-input channel convolution kernel




11/17/22           Lê Anh Cường - 2020     25
```

## Trang PDF 26

```text
 2D Convolutions
• The filter can move in 2 directions and thus the final output is 2D.
• 2D convolutions are the most common convolutions, and are heavily used in
  Computer Vision.




 11/17/22                         Lê Anh Cường - 2020                         26
```

## Trang PDF 27

```text
1D Convolutions




11/17/22          Lê Anh Cường - 2020   27
```

## Trang PDF 28

```text
1D Convolution with 2D input




11/17/22           Lê Anh Cường - 2020   28
```

## Trang PDF 29

```text
Stride




 11/17/22   Lê Anh Cường - 2020   29
```

## Trang PDF 30

```text
Padding




11/17/22   Lê Anh Cường - 2020   30
```

## Trang PDF 31

```text
ReLU Operation




11/17/22         Lê Anh Cường - 2020   31
```

## Trang PDF 32

```text
ReLU




11/17/22   Lê Anh Cường - 2020   32
```

## Trang PDF 33

```text
Pooling Layer




11/17/22        Lê Anh Cường - 2020   33
```

## Trang PDF 34

```text
Pooling Layer

 • The Pooling layer is responsible for
   reducing the spatial size of the
   Convolved Feature. This is to decrease
   the computational power required to
   process the data through dimensionality
   reduction.
 • Furthermore, it is useful for extracting
   dominant features .




11/17/22                          Lê Anh Cường - 2020   34
```

## Trang PDF 35

```text
Example for Convolutional Operations




11/17/22          Lê Anh Cường - 2020   35
```

## Trang PDF 36

```text
11/17/22   Lê Anh Cường - 2020   36
```

## Trang PDF 37

```text
Recognition of characters: X , O, /, \




11/17/22             Lê Anh Cường - 2020   37
```

## Trang PDF 38

```text
11/17/22   Lê Anh Cường - 2020   38
```

## Trang PDF 39

```text
Classification — Fully Connected Layer (FC
Layer)




11/17/22           Lê Anh Cường - 2020       39
```

## Trang PDF 40

```text
Multi-Layer CNNs




 11/17/22          Lê Anh Cường - 2020   40
```

## Trang PDF 41

```text
11/17/22   Lê Anh Cường - 2020   41
```

## Trang PDF 42

```text
Well known CNNs

       There are various
       architectures of CNNs
       available which have been
       key in building algorithms
       which power and shall
       power AI as a whole in the
       foreseeable future.




11/17/22                            Lê Anh Cường - 2020   42
```

## Trang PDF 43

```text
LeNet
LeNet is a convolutional neural network structure proposed by Yann
LeCun et al. in 1998. In general, LeNet refers to lenet-5 and is a
simple convolutional neural network.



LeNet5 was one of the earliest convolutional neural networks and
promoted the development of deep learning. Since 1988, after years of
research and many successful iterations, the pioneering work has been
named LeNet5.




11/17/22                                  Lê Anh Cường - 2020           43
```

## Trang PDF 44

```text
LeNet-5                      http://datahacker.rs/deep-learning-lenet-5-architecture/




The goal of !"#"$−5 was to recognize handwritten digits. So, it takes as an input 32×32×1 image. It is a
grayscale image, thus the number of channels is 1. Here is a picture of it’s arhitecture. In the first step we
use 65×5 filters with a stride %=1 and &'()**+&,. Therefore we end up with a 28×28×6 volume. Notice that,
because we are using %=1 and &'()**+&,, the image dimensions reduce from 32×32 to 28×28.
Next, !"#"$ applies (''-+&,. When this paper was written ./"0),"(''-+&, was much more in use, so here we
will use ./"0),"(''-+&,. However, nowadays we would probably use 1)2(''-+&, instead. So, here we will
implement ./"0),"(''- with filter 3=2 and stride %=2. We get a 14×14×6 volume, so we reduced dimensions
of an image by a factor of 2 and due to use of a stride of 2.
11/17/22                                      Lê Anh Cường - 2020                                         44
```

## Trang PDF 45

```text
CNN for Natural Language Processing




 11/17/22             Lê Anh Cường - 2020   45
```

## Trang PDF 46

```text
CNN Implementation




11/17/22        Lê Anh Cường - 2020   46
```

## Trang PDF 47

```text
RECURRENT NEURAL NETWORKS




11/17/22       Lê Anh Cường - 2020   47
```

## Trang PDF 48

```text
RNN for Sequential Data




11/17/22          Lê Anh Cường - 2020   48
```

## Trang PDF 49

```text
Different Types of RNN




11/17/22           Lê Anh Cường - 2020   49
```

## Trang PDF 50

```text
Outline
1. How to recognize Deep Learning networks/models:
      • Traditional statistical machine learning vs Deep Learning
      • Vanilla Neural Networks vs Deep Learning Networks
      • History of DL development
2. Convolutional Neural Network (CNN)
3. Reccurent Neural Network (RNN) and Long Short Term Memory
   (LSTM)
4. Transformer Models


11/17/22                              Lê Anh Cường - 2020           50
```

## Trang PDF 51

```text
Outline
• What is RNN?
• RNN: the Architecture and Forward Computation
• RNN with Progapagation algorithm
• Long-Short Term Memory




11/17/22                    Lê Anh Cường - 2020   51
```

## Trang PDF 52

```text
What is Recurrent Neural Network (RNN)?




11/17/22          Lê Anh Cường - 2020     52
```

## Trang PDF 53

```text
Automatic Email Reply




11/17/22          Lê Anh Cường - 2020   53
```

## Trang PDF 54

```text
Part Of Speech Tagging
Sentiment Analysis




11/17/22          Lê Anh Cường - 2020   54
```

## Trang PDF 55

```text
Image Captioning




11/17/22           Lê Anh Cường - 2020   55
```

## Trang PDF 56

```text
RNN Architectures




11/17/22            Lê Anh Cường - 2020   56
```

## Trang PDF 57

```text
What is Recurrent Neural Network (RNN)?
• The idea behind RNNs is to make use of Sequential Information.
• RNNs are called recurrent because they perform the same task
  for every element of a sequence.
• RNNs have a “memory” which captures information about what has
  been calculated so far.




11/17/22                    Lê Anh Cường - 2020                    57
```

## Trang PDF 58

```text
What is Recurrent Neural Network (RNN)?




11/17/22          Lê Anh Cường - 2020     58
```

## Trang PDF 59

```text
Forward Computation in RNN




11/17/22         Lê Anh Cường - 2020   59
```

## Trang PDF 60

```text
Forward Computation in RNN




11/17/22         Lê Anh Cường - 2020   60
```

## Trang PDF 61

```text
Example


            https://www.analyticsvidhya.com/blog/2017/12/introduction-
            to-recurrent-neural-networks/



           https://medium.com/towards-artificial-intelligence/whirlwind-
           tour-of-rnns-a11effb7808f




11/17/22                           Lê Anh Cường - 2020                     61
```

## Trang PDF 62

```text

```

## Trang PDF 63

```text

```

## Trang PDF 64

```text
11/17/22   Lê Anh Cường - 2020   64
```

## Trang PDF 65

```text
BackPropagation Through Time (BPTT)

  The loss, or error, to be
  the cross entropy loss, given by:




11/17/22                              Lê Anh Cường - 2020   65
```

## Trang PDF 66

```text
BackPropagation Through Time (BPTT)




11/17/22          Lê Anh Cường - 2020   66
```

## Trang PDF 67

```text
11/17/22   Lê Anh Cường - 2020   67
```

## Trang PDF 68

```text
11/17/22   Lê Anh Cường - 2020   68
```

## Trang PDF 69

```text
           W ~ small -> Vanishing problem


11/17/22     Lê Anh Cường - 2020            69
```

## Trang PDF 70

```text
Sigmoid and Tanh funtions




11/17/22          Lê Anh Cường - 2020   70
```

## Trang PDF 71

```text
RNN: Vanishing Problem

           “During back propagation, recurrent neural networks suffer from the
           vanishing gradient problem. Gradients are values used to update a neural
           networks weights.
           The vanishing gradient problem is when the gradient shrinks as it back
           propagates through time. If a gradient value becomes extremely small, it
           doesn’t contribute too much learning.”




11/17/22                                  Lê Anh Cường - 2020                         71
```

## Trang PDF 72

```text
Limitation of RNN
           consider the sentence:
            “ I grew up in France …                  I speak fluent French”




11/17/22                       Lê Anh Cường - 2020                            72
```

## Trang PDF 73

```text
LSTM’s and GRU’s as a Solution
These gates can learn which data in a sequence is important to keep or throw away




11/17/22                              Lê Anh Cường - 2020                           73
```

## Trang PDF 74

```text
LSTM Networks

• Long Short Term Memory networks – usually just called “LSTMs” – are
  a special kind of RNN, capable of learning Long-Term Dependencies.
• They were introduced by Hochreiter & Schmidhuber (1997), and were
  refined and popularized by many people, they work tremendously well
  on a large variety of problems, and are now widely used.
• LSTMs are explicitly designed to avoid the long-term dependency
  problem.




11/17/22                     Lê Anh Cường - 2020                    74
```

## Trang PDF 75

```text
                                 When you read the review,
                                 your brain subconsciously only
                                 remembers              important
                                 keywords. You pick up words
                                 like “amazing” and “perfectly
                                 balanced breakfast”. You don’t
                                 care much for words like “this”,
                                 “gave“, “all”, “should”, etc.




11/17/22   Lê Anh Cường - 2020                                 75
```

## Trang PDF 76

```text
Longer Memories through LSTMs

• Adding a forgetting mechanism.
• Adding a saving mechanism.
      • When the model sees a new image, it needs to learn whether any information
        about the image is worth using and saving.




11/17/22                            Lê Anh Cường - 2020                         76
```

## Trang PDF 77

```text
           https://en.wikipedia.org/wiki/Long_short-term_memory
11/17/22                          Lê Anh Cường - 2020             77
```

## Trang PDF 78

```text
LSTM Cell
• Forget gate
```

## Trang PDF 79

```text
• Input Gate
```

## Trang PDF 80

```text
Output Gate
```

## Trang PDF 81

```text
LSTM Memory Cell




11/17/22           Lê Anh Cường - 2020   81
```

## Trang PDF 82

```text
How does LSTM prevent Vanishing




11/17/22         Lê Anh Cường - 2020   82
```

## Trang PDF 83

```text
BackPropagation Through Time in LSTM




11/17/22         Lê Anh Cường - 2020   83
```

## Trang PDF 84

```text
Backpropagation through time in LSTM




11/17/22          Lê Anh Cường - 2020   84
```

## Trang PDF 85

```text
                                 vanilla
                                  RNN




11/17/22   Lê Anh Cường - 2020             85
```

## Trang PDF 86

```text
  Backpropagating through time for gradient
  computation

   Now, notice equation (2) means that the gradient behaves similarly to the forget gate,
   and if the forget gate decides that a certain piece of information should be remembered, it
   will be open and have values closer to 1 to allow for information flow.
   For simplicity, we can think of the forget gate’s action as:


                                                              So we get:

Finally:




                                                                              And the gradients do not vanish!
  11/17/22                                     Lê Anh Cường - 2020                                     86
```

## Trang PDF 87

```text
LSTM Architecture




11/17/22            Lê Anh Cường - 2020   87
```

## Trang PDF 88

```text
Stacked LSTM




11/17/22       Lê Anh Cường - 2020   88
```

## Trang PDF 89

```text
BiLSTM




11/17/22   Lê Anh Cường - 2020   89
```

## Trang PDF 90

```text
Neural Machine Translation




11/17/22          Lê Anh Cường - 2020   90
```

## Trang PDF 91

```text
  Attention based NMT

sinh_viên một   là    tôi




   I     am     a    student




                               Lê Anh Cường   91
```

## Trang PDF 92

```text
Outline
1. How to recognize Deep Learning networks/models:
      • Traditional statistical machine learning vs Deep Learning
      • Vanilla Neural Networks vs Deep Learning Networks
      • History of DL development
2. Convolutional Neural Network (CNN)
3. Reccurent Neural Network (RNN) and Long Short Term Memory
   (LSTM)
4. Transformer Models


11/17/22                              Lê Anh Cường - 2020           92
```

## Trang PDF 93

```text
Word Representation
1. Word Embeddings/Word2vec
2. Word pre-train models
3. Transformer based models




                          Lê Anh Cường   93
```

## Trang PDF 94

```text
Lê Anh Cường   94
```

## Trang PDF 95

```text
Word Embeddings
(Semantic Distributed Representation)
   • Embed the words into a space of abstract
     concepts
   • The words are placed in a space of n<< |V|
     dimensions.




                                         Lê Anh Cường   95
```

## Trang PDF 96

```text
Learning Word2Vec




                    Lê Anh Cường   96
```

## Trang PDF 97

```text
Pretrain word representations data and tools
 ØWord2vec: CBOW, Skip-gram
 ØGlove (word embeddings)
 ØFastText (FastText is an open-source library developed by
  the Facebook AI Research




                               Lê Anh Cường                   97
```

## Trang PDF 98

```text
Some Experiments




                   Lê Anh Cường   98
```

## Trang PDF 99

```text
 Stage 2: Pre-train Models
 • Pretrain word presentation:         • Pretrain models: generate context-
   word2vec, word embeddings             word2ve (dynamic word embeddings)


                      vector                                    vector



   Word              Generate                     Prtrain      Generate
embeddings        representation                  Model     representation
  dataset

                      word                                      word


                    sentence                                  sentence
                                   Lê Anh Cường                               99
```

## Trang PDF 100

```text
ELMo (Embeddings from Language Models) -
2018
ELMo: Deep contextualized word
representations (2018)
Ø The main idea of the Embeddings from
   Language Models (ELMo) can be divided into
   two main tasks, first we train an LSTM-based
   language model on some corpus, and then
   we use the hidden states of the LSTM for
   each token to generate a vector
   representation of each word.
Ø It’s been shown to outperform GloVe and
   Word2Vec embeddings on a wide variety of
   NLP tasks.




                                                  Lê Anh Cường   100
```

## Trang PDF 101

```text
Using ELMo




             Lê Anh Cường   101
```

## Trang PDF 102

```text
Using ELMo: Experiments




                  Lê Anh Cường   102
```

## Trang PDF 103

```text
The Transformer
Self & Multi-Head Attention
State-Of-The-Art models in Natura Language Processing




                              Lê Anh Cường              103
```

## Trang PDF 104

```text
Why? Motivation
RNN
ØSequential
 computation inhibits
 parallelization.
ØNo explicit modeling of
 long and short range
 dependencies.




                           Lê Anh Cường   104
```

## Trang PDF 105

```text
Why? Motivation
§ Convolutional Neural
  Network
  § Exploits local dependencies
  § Long-distance
    dependencies require many
    layers.




                              Lê Anh Cường   105
```

## Trang PDF 106

```text
Why? Motivation
§ Attention
  § Attention between encoder
    and decoder is crucial in
    NMT.
  § Why not use attention for
    representations?




                            Lê Anh Cường   106
```

## Trang PDF 107

```text
Solution: Transformer Model
(Mô hình chuyển đổi)
• Self-Attention
• Multi-Head Attention




                         Lê Anh Cường   107
```

## Trang PDF 108

```text
Transformer Model




                    Lê Anh Cường   108
```

## Trang PDF 109

```text
What is Self-Attention?
For encoding




                      Lê Anh Cường   109
```

## Trang PDF 110

```text
Multi-Head Attention




                   Lê Anh Cường   110
```

## Trang PDF 111

```text
Lê Anh Cường   111
```

## Trang PDF 112

```text
Lê Anh Cường   112
```

## Trang PDF 113

```text
Lê Anh Cường   113
```

## Trang PDF 114

```text
Lê Anh Cường   114
```

## Trang PDF 115

```text
               The word embedding is
               transformed into three separate
               matrices -- Queries, Keys, and
               Values.




Lê Anh Cường                              115
```

## Trang PDF 116

```text
11/17/22   Lê Anh Cường - 2020   116
```

## Trang PDF 117

```text
Multi-Head Attention




                       Lê Anh Cường   117
```

## Trang PDF 118

```text
Positional Encoding




                      Lê Anh Cường   118
```

## Trang PDF 119

```text
Lê Anh Cường   119
```

## Trang PDF 120

```text
Encoder – Decoder Architecture




                   Lê Anh Cường   120
```

## Trang PDF 121

```text
Lê Anh Cường   121
```

## Trang PDF 122

```text
Lê Anh Cường   122
```

## Trang PDF 123

```text
A Transformer
Architecture




                Lê Anh Cường   123
```

## Trang PDF 124

```text
Lê Anh Cường   124
```

## Trang PDF 125

```text
Lê Anh Cường   125
```

## Trang PDF 126

```text
BERT(Bidirectional Encoder Representations
from Transformers)




                   Lê Anh Cường              126
```

## Trang PDF 127

```text
Lê Anh Cường   127
```

## Trang PDF 128

```text
Next Sentence Prediction (NSP)




                   Lê Anh Cường   128
```

## Trang PDF 129

```text
How to use BERT (Fine-tuning)




                   Lê Anh Cường   129
```

## Trang PDF 130

```text
Using BERT




             Lê Anh Cường   130
```

## Trang PDF 131

```text
Using
BERT




        Lê Anh Cường   131
```

## Trang PDF 132

```text
Lê Anh Cường   132
```

## Trang PDF 133

```text
Lê Anh Cường   133
```

## Trang PDF 134

```text
Lê Anh Cường   134
```

## Trang PDF 135

```text
References
• https://towardsdatascience.com/illustrated-guide-to-lstms-and-gru-s-
  a-step-by-step-explanation-44e9eb85bf21
• https://mc.ai/how-do-lstm-networks-solve-the-problem-of-vanishing-
  gradients/
• https://medium.com/datadriveninvestor/how-do-lstm-networks-
  solve-the-problem-of-vanishing-gradients-a6784971a577
• http://jalammar.github.io/illustrated-transformer/



11/17/22                      Lê Anh Cường - 2020                   135
```

## Trang PDF 136

```text
           THANK YOU!




11/17/22     Lê Anh Cường - 2020   136
```