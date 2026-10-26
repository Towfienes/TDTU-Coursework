# Lecture 6 - Unsupervised Learning and Clustering.pdf

Nguồn: `ML/Introduction to machine learning/Lecture 6 - Unsupervised Learning and Clustering.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
                   Machine Learning
             TON DUC THANG UNIVERSITY
              Faculty of Information Technology
                      Computer Science



                  Clustering
                     LÊ ANH CƯỜNG




09/04/2022             IT701010 - Chapter 6 - Clustering   1
```

## Trang PDF 2

```text
                                  Content

     ◼       Cluster Analysis: Basic Concepts

     ◼       Partitioning Methods

     ◼       Hierarchical Methods

     ◼       Density-Based Methods

     ◼       Grid-Based Methods

     ◼       Evaluation of Clustering

     ◼       Summary
09/04/2022                     IT701010 - Chapter 6 - Clustering   2
```

## Trang PDF 3

```text
                    What is Cluster Analysis?

   ◼    Cluster: A collection of data objects
         ◼ similar (or related) to one another within the same
           group
         ◼ dissimilar (or unrelated) to the objects in other groups


   ◼    Cluster analysis (or clustering, data segmentation, …)
         ◼   Finding similarities between data according to the
             characteristics found in the data and grouping similar
             data objects into clusters

   ◼    Unsupervised learning: no predefined classes (i.e., learning by
        observations vs. learning by examples: supervised)

09/04/2022                       IT701010 - Chapter 6 - Clustering        3
```

## Trang PDF 4

```text
                     Clustering for Data Understanding
                              and Applications
     ◼       Biology: taxonomy of living things: kingdom, phylum, class, order, family,
             genus and species
     ◼       Information retrieval: document clustering
     ◼       Land use: Identification of areas of similar land use in an earth observation
             database
     ◼       Marketing: Help marketers discover distinct groups in their customer bases,
             and then use this knowledge to develop targeted marketing programs
     ◼       City-planning: Identifying groups of houses according to their house type,
             value, and geographical location
     ◼       Earth-quake studies: Observed earth quake epicenters should be clustered
             along continent faults
     ◼       Climate: understanding earth climate, find patterns of atmospheric and ocean
     ◼       Economic Science: market resarch




09/04/2022                               IT701010 - Chapter 6 - Clustering                   4
```

## Trang PDF 5

```text
                      Clustering as a Preprocessing Tool
                                   (Utility)
     ◼       Summarization:
             ◼   Preprocessing for regression, PCA, classification,
                 and association analysis
     ◼       Compression:
             ◼   Image processing: vector quantization
     ◼       Finding K-nearest Neighbors
             ◼   Localizing search to one or a small number of
                 clusters
     ◼       Outlier detection
             ◼   Outliers are often viewed as those “far away” from
09/04/2022       any cluster       IT701010 - Chapter 6 - Clustering   5
```

## Trang PDF 6

```text
                            Quality: What Is Good
                                 Clustering?
     ◼       A good clustering method will produce high quality clusters

             ◼   high intra-class similarity: cohesive within clusters
             ◼   low inter-class similarity: distinctive between
                 clusters
     ◼       The quality of a clustering method depends on

             ◼   the similarity measure used by the method
             ◼   its implementation
             ◼   Its ability to discover some or all of the hidden
09/04/2022
                 patterns           IT701010 - Chapter 6 - Clustering      6
```

## Trang PDF 7

```text
                 Measure the Quality of Clustering
   ◼     Dissimilarity/Similarity metric
         ◼   Similarity is expressed in terms of a distance
             function, typically metric: d(i, j)
         ◼   The definitions of distance functions are usually
             rather different for interval-scaled, boolean,
             categorical, ordinal ratio, and vector variables
         ◼   Weights should be associated with different
             variables based on applications and data semantics
   ◼     Quality of clustering:
         ◼   There is usually a separate “quality” function that
             measures the “goodness” of a cluster.
         ◼   It is hard to define “similar enough” or “good
             enough”
             ◼   The answer is typically highly subjective
09/04/2022                        IT701010 - Chapter 6 - Clustering   7
```

## Trang PDF 8

```text
                  Considerations for Cluster Analysis
     ◼       Partitioning criteria
              ◼ Single level vs. hierarchical partitioning (often, multi-level hierarchical
                 partitioning is desirable)
     ◼       Separation of clusters
              ◼ Exclusive (e.g., one customer belongs to only one region) vs. non-
                 exclusive (e.g., one document may belong to more than one class)
     ◼       Similarity measure
              ◼ Distance-based (e.g., Euclidian, road network, vector) vs. connectivity-
                 based (e.g., density or contiguity)
     ◼       Clustering space
              ◼ Full space (often when low dimensional) vs. subspaces (often in high-
                 dimensional clustering)




09/04/2022                                IT701010 - Chapter 6 - Clustering                   8
```

## Trang PDF 9

```text
                     Requirements and Challenges
     ◼       Scalability
              ◼ Clustering all the data instead of only on samples

     ◼       Ability to deal with different types of attributes
              ◼ Numerical, binary, categorical, ordinal, linked, and mixture of these

     ◼       Constraint-based clustering
              ◼  User may give inputs on constraints
              ◼  Use domain knowledge to determine input parameters
     ◼       Interpretability and usability
     ◼       Others
              ◼ Discovery of clusters with arbitrary shape

              ◼ Ability to deal with noisy data

              ◼ Incremental clustering and insensitivity to input order

              ◼ High dimensionality




09/04/2022                               IT701010 - Chapter 6 - Clustering              9
```

## Trang PDF 10

```text
                  Major Clustering Approaches (I)

    ◼    Partitioning approach:
          ◼ Construct various partitions and then evaluate them by some criterion,
             e.g., minimizing the sum of square errors
          ◼ Typical methods: k-means, k-medoids, CLARANS

    ◼    Hierarchical approach:
          ◼ Create a hierarchical decomposition of the set of data (or objects) using
             some criterion
          ◼ Typical methods: Diana, Agnes, BIRCH, CAMELEON

    ◼    Density-based approach:
          ◼ Based on connectivity and density functions

          ◼ Typical methods: DBSACN, OPTICS, DenClue

    ◼    Grid-based approach:
          ◼ based on a multiple-level granularity structure

          ◼ Typical methods: STING, WaveCluster, CLIQUE




09/04/2022                            IT701010 - Chapter 6 - Clustering                 10
```

## Trang PDF 11

```text
                 Major Clustering Approaches (II)
    ◼    Model-based:
          ◼ A model is hypothesized for each of the clusters and tries to find the best
            fit of that model to each other
          ◼ Typical methods: EM, SOM, COBWEB

    ◼    Frequent pattern-based:
          ◼ Based on the analysis of frequent patterns

          ◼ Typical methods: p-Cluster

    ◼    User-guided or constraint-based:
          ◼ Clustering by considering user-specified or application-specific constraints

          ◼ Typical methods: COD (obstacles), constrained clustering

    ◼    Link-based clustering:
          ◼ Objects are often linked together in various ways

          ◼ Massive links can be used to cluster objects: SimRank, LinkClus




09/04/2022                            IT701010 - Chapter 6 - Clustering                    11
```

## Trang PDF 12

```text
  Chapter 10. Cluster Analysis: Basic Concepts and
                      Methods
   ◼ Cluster Analysis: Basic Concepts


     ◼       Partitioning Methods

     ◼       Hierarchical Methods

     ◼       Density-Based Methods

     ◼       Grid-Based Methods

     ◼       Evaluation of Clustering

     ◼       Summary
09/04/2022                   IT701010 - Chapter 6 - Clustering   12
                                                                 12
```

## Trang PDF 13

```text
             Partitioning Algorithms: Basic Concept

   ◼    Partitioning method: Partitioning a database D of n objects into a set of k
        clusters, such that the sum of squared distances is minimized (where ci is the
        centroid or medoid of cluster Ci)

                           E =  ik=1 pCi ( p − ci ) 2

   ◼    Given k, find a partition of k clusters that optimizes the chosen partitioning
        criterion
         ◼   Global optimal: exhaustively enumerate all partitions
         ◼   Heuristic methods: k-means and k-medoids algorithms
         ◼   k-means (MacQueen’67, Lloyd’57/’82): Each cluster is represented by the
             center of the cluster
         ◼   k-medoids or PAM (Partition around medoids) (Kaufman &
             Rousseeuw’87): Each cluster is represented by one of the objects in the
             cluster
09/04/2022                            IT701010 - Chapter 6 - Clustering                  13
```

## Trang PDF 14

```text
                   The K-Means Clustering Method
      ◼      Given k, the k-means algorithm is implemented in four
             steps:
             ◼   Partition objects into k nonempty subsets
             ◼   Compute seed points as the centroids of the
                 clusters of the current partitioning (the centroid
                 is the center, i.e., mean point, of the cluster)
             ◼   Assign each object to the cluster with the
                 nearest seed point
             ◼   Go back to Step 2, stop when the assignment
                 does not change
09/04/2022                         IT701010 - Chapter 6 - Clustering   14
```

## Trang PDF 15

```text
                       An Example of K-Means Clustering

                                  K=2


                                  Arbitrarily                                          Update the
                                  partition                                            cluster
                                  objects into k                                       centroids
                                  groups

          The initial data set                                    Loop if                           Reassign objects
                                                                  needed
◼   Partition objects into k nonempty
    subsets
◼   Repeat
      ◼      Compute centroid (i.e., mean                                              Update the
                                                                                       cluster
             point) for each partition
                                                                                       centroids
      ◼      Assign each object to the cluster
             of its nearest centroid
◼   Until no change
09/04/2022                                         IT701010 - Chapter 6 - Clustering                                   15
```

## Trang PDF 16

```text
                   Comments on the K-Means Method

    ◼    Strength: Efficient: O(tkn), where n is # objects, k is # clusters, and t is #
         iterations. Normally, k, t << n.
                  ◼   Comparing: PAM: O(k(n-k)2 ), CLARA: O(ks2 + k(n-k))
    ◼    Comment: Often terminates at a local optimal.
    ◼    Weakness
             ◼   Applicable only to objects in a continuous n-dimensional space
                  ◼   Using the k-modes method for categorical data
                  ◼   In comparison, k-medoids can be applied to a wide range of data
             ◼   Need to specify k, the number of clusters, in advance
             ◼   Sensitive to noisy data and outliers
             ◼   Not suitable to discover clusters with non-convex shapes


09/04/2022                                IT701010 - Chapter 6 - Clustering               16
```

## Trang PDF 17

```text
             Distance (dissimilarity) measures




09/04/2022              IT701010 - Chapter 6 - Clustering   17
```

## Trang PDF 18

```text
               Example




09/04/2022   IT701010 - Chapter 6 - Clustering   18
```

## Trang PDF 19

```text
09/04/2022   IT701010 - Chapter 6 - Clustering   19
```

## Trang PDF 20

```text
09/04/2022   IT701010 - Chapter 6 - Clustering   20
```

## Trang PDF 21

```text
              Exercise




09/04/2022   IT701010 - Chapter 6 - Clustering   21
```

## Trang PDF 22

```text
                    Variations of the K-Means Method

     ◼       Most of the variants of the k-means which differ in

              ◼   Selection of the initial k means

              ◼   Dissimilarity calculations

              ◼   Strategies to calculate cluster means

     ◼       Handling categorical data: k-modes

              ◼   Replacing means of clusters with modes

              ◼   Using new dissimilarity measures to deal with categorical objects

              ◼   Using a frequency-based method to update modes of clusters

              ◼   A mixture of categorical and numerical data: k-prototype method


09/04/2022                                 IT701010 - Chapter 6 - Clustering          22
```

## Trang PDF 23

```text
             K-modes




09/04/2022   IT701010 - Chapter 6 - Clustering   23
```

## Trang PDF 24

```text
                              Exercise

       Cluster these elements into 2 clusters




09/04/2022                 IT701010 - Chapter 6 - Clustering   24
```

## Trang PDF 25

```text
               K-modes




09/04/2022   IT701010 - Chapter 6 - Clustering   25
```

## Trang PDF 26

```text
             K-modes




09/04/2022   IT701010 - Chapter 6 - Clustering   26
```

## Trang PDF 27

```text
                         What Is the Problem of the K-Means
                                      Method?

    ◼    The k-means algorithm is sensitive to outliers !

             ◼   Since an object with an extremely large value may substantially distort the
                 distribution of the data

    ◼    K-Medoids: Instead of taking the mean value of the object in a cluster as a
         reference point, medoids can be used, which is the most centrally located
         object in a cluster

                           10                                                                  10
                           9                                                                   9
                           8                                                                   8
                           7                                                                   7
                           6                                                                   6
                           5                                                                   5
                           4                                                                   4
                           3                                                                   3
                           2                                                                   2
                           1                                                                   1
                           0                                                                   0
                                0   1   2   3   4   5   6   7   8    9   10                         0   1   2   3   4   5   6   7   8   9   10



09/04/2022                                                          IT701010 - Chapter 6 - Clustering                                            27
```

## Trang PDF 28

```text
                               PAM: A Typical K-Medoids Algorithm
                                                                                                                                                                                                        Total Cost = 20
  10                                                                10                                                                                                 10


  9                                                                  9                                                                                                  9


  8                                                                  8                                                                                                  8


  7                                                                  7                                                                                                  7


  6
                                                       Arbitrary     6
                                                                                                                                                         Assign         6


  5
                                                       choose k      5
                                                                                                                                                         each           5


  4                                                    object as     4                                                                                   remaining      4


  3                                                    initial       3
                                                                                                                                                         object to      3


  2
                                                       medoids       2
                                                                                                                                                         nearest        2


  1                                                                  1                                                                                                  1


  0                                                                  0
                                                                                                                                                         medoids        0

       0   1   2   3   4   5   6   7   8   9   10                        0       1       2   3   4       5       6       7       8       9        10                        0       1       2   3   4        5       6       7       8       9        10




 K=2                                                                                                                                                                            Randomly select a
                                                                             Total Cost = 26                                                                                    nonmedoid object,Oramdom
                                                                     10                                                                                                 10


       Do loop                                                           9

                                                                         8
                                                                                                                                                       Compute
                                                                                                                                                                            9

                                                                                                                                                                            8
                                                    Swapping O           7                                                                             total cost of        7

       Until no change                              and Oramdom          6
                                                                                                                                                       swapping             6

                                                                         5                                                                                                  5

                                                    If quality is        4                                                                                                  4


                                                    improved.            3                                                                                                  3

                                                                         2                                                                                                  2

                                                                         1                                                                                                  1

                                                                         0                                                                                                  0
                                                                             0       1   2   3   4   5       6       7       8       9       10                                 0       1   2   3   4    5       6       7       8       9       10


09/04/2022                                                               IT701010 - Chapter 6 - Clustering                                                                                                                                       28
                                                                                                                                                                                                                                                 28
```

## Trang PDF 29

```text
                      The K-Medoid Clustering Method

    ◼    K-Medoids Clustering: Find representative objects (medoids) in clusters

             ◼   PAM (Partitioning Around Medoids, Kaufmann & Rousseeuw 1987)

                  ◼   Starts from an initial set of medoids and iteratively replaces one of the
                      medoids by one of the non-medoids if it improves the total distance of
                      the resulting clustering

                  ◼   PAM works effectively for small data sets, but does not scale well for
                      large data sets (due to the computational complexity)

    ◼    Efficiency improvement on PAM

             ◼   CLARA (Kaufmann & Rousseeuw, 1990): PAM on samples

             ◼   CLARANS (Ng & Han, 1994): Randomized re-sampling

09/04/2022                                  IT701010 - Chapter 6 - Clustering                     29
```

## Trang PDF 30

```text
               Example




09/04/2022   IT701010 - Chapter 6 - Clustering   30
```

## Trang PDF 31

```text
09/04/2022   IT701010 - Chapter 6 - Clustering   31
```

## Trang PDF 32

```text
                Exercise




09/04/2022   IT701010 - Chapter 6 - Clustering   32
```

## Trang PDF 33

```text
                           Project

    ◼ Given a set of N sentences.
    ◼ Cluster these N sentences into k clusters.




09/04/2022             IT701010 - Chapter 6 - Clustering   33
```

## Trang PDF 34

```text
  Chapter 10. Cluster Analysis: Basic Concepts and
                      Methods

     ◼       Cluster Analysis: Basic Concepts
     ◼       Partitioning Methods
     ◼       Hierarchical Methods
     ◼       Density-Based Methods
     ◼       Grid-Based Methods
     ◼       Evaluation of Clustering
     ◼       Summary
09/04/2022                   IT701010 - Chapter 6 - Clustering   34
```

## Trang PDF 35

```text
                       Hierarchical Clustering
    ◼    Use distance matrix as clustering criteria. This method does
         not require the number of clusters k as an input, but needs a
         termination condition

              Step 0    Step 1   Step 2 Step 3 Step 4
                                                                          agglomerative
                                                                          (AGNES)
              a
                        ab
              b                                abcde
              c
                                       cde
              d
                                 de
              e
                                                                           divisive
              Step 4    Step 3   Step 2 Step 1 Step 0                      (DIANA)
09/04/2022                            IT701010 - Chapter 6 - Clustering                   35
```

## Trang PDF 36

```text
                                         AGNES (Agglomerative Nesting)
    ◼    Introduced in Kaufmann and Rousseeuw (1990)
    ◼    Implemented in statistical packages, e.g., Splus
    ◼    Use the single-link method and the dissimilarity matrix
    ◼    Merge nodes that have the least dissimilarity
    ◼    Go on in a non-descending fashion
    ◼    Eventually all nodes belong to the same cluster
        10                                                10                                                10


         9                                                 9                                                 9


         8                                                 8                                                 8


         7                                                 7                                                 7


         6                                                 6                                                 6


         5                                                 5                                                 5


         4                                                 4                                                 4


         3                                                 3                                                 3


         2                                                 2                                                 2


         1                                                 1                                                 1


         0                                                 0                                                 0
             0   1   2   3   4   5   6   7   8   9   10        0   1   2   3   4   5   6   7   8   9   10        0   1   2   3   4   5   6   7   8   9   10




09/04/2022                                                IT701010 - Chapter 6 - Clustering                                                                   36
```

## Trang PDF 37

```text
Dendrogram: Shows How Clusters are Merged

             Decompose data objects into a several levels of nested
             partitioning (tree of clusters), called a dendrogram

             A clustering of the data objects is obtained by cutting the
             dendrogram at the desired level, then each connected
             component forms a cluster




37
09/04/2022                          IT701010 - Chapter 6 - Clustering
```

## Trang PDF 38

```text
                                                 DIANA (Divisive Analysis)

     ◼       Introduced in Kaufmann and Rousseeuw (1990)
     ◼       Implemented in statistical analysis packages, e.g., Splus
     ◼       Inverse order of AGNES
     ◼       Eventually each node forms a cluster on its own


         10                                                                                                     10
                                                              10

             9                                                                                                   9
                                                               9

             8                                                                                                   8
                                                               8

             7                                                                                                   7
                                                               7

             6                                                                                                   6
                                                               6

             5                                                                                                   5
                                                               5

             4                                                                                                   4
                                                               4

             3                                                                                                   3
                                                               3

             2                                                                                                   2
                                                               2

             1                                                                                                   1
                                                               1

             0                                                                                                   0
                                                               0
                 0   1   2   3   4   5   6   7   8   9   10                                                          0   1   2   3   4   5   6   7   8   9   10
                                                                   0   1   2   3   4   5   6   7   8   9   10




09/04/2022                                                             IT701010 - Chapter 6 - Clustering                                                          38
```

## Trang PDF 39

```text
                        Distance between                                      X       X

                            Clusters
    ◼    Single link: smallest distance between an element in one cluster and an
         element in the other, i.e., dist(Ki, Kj) = min(tip, tjq)

    ◼    Complete link: largest distance between an element in one cluster and an
         element in the other, i.e., dist(Ki, Kj) = max(tip, tjq)

    ◼    Average: avg distance between an element in one cluster and an element in
         the other, i.e., dist(Ki, Kj) = avg(tip, tjq)

    ◼    Centroid: distance between the centroids of two clusters, i.e., dist(Ki, Kj) =
         dist(Ci, Cj)

    ◼    Medoid: distance between the medoids of two clusters, i.e., dist(Ki, Kj) =
         dist(Mi, Mj)
             ◼   Medoid: a chosen, centrally located object in the cluster
09/04/2022                                IT701010 - Chapter 6 - Clustering               39
```

## Trang PDF 40

```text
                   Centroid, Radius and Diameter of a
                    Cluster (for numerical data sets)
     ◼       Centroid: the “middle” of a cluster                                  iN= 1(t )
                                                                           Cm =       N
                                                                                          ip




     ◼       Radius: square root of average distance from any point of the
             cluster to its centroid                    N (t − cm ) 2
                                                 Rm = i =1 ip
                                                              N
     ◼       Diameter: square root of average mean squared distance
             between all pairs of points in the cluster

                                                               N  N (t − t ) 2
                                                         Dm = i =1 i =1 ip iq
                                                                   N ( N −1)

09/04/2022                             IT701010 - Chapter 6 - Clustering                       40
```

## Trang PDF 41

```text
                    Extensions to Hierarchical Clustering
    ◼    Major weakness of agglomerative clustering methods

             ◼   Can never undo what was done previously

             ◼   Do not scale well: time complexity of at least O(n2), where n
                 is the number of total objects
    ◼    Integration of hierarchical & distance-based clustering

             ◼   BIRCH (1996): uses CF-tree and incrementally adjusts the
                 quality of sub-clusters

             ◼   CHAMELEON (1999): hierarchical clustering using dynamic
                 modeling

09/04/2022                            IT701010 - Chapter 6 - Clustering          41
```

## Trang PDF 42

```text
                     BIRCH (Balanced Iterative Reducing
                      and Clustering Using Hierarchies)
    ◼    Zhang, Ramakrishnan & Livny, SIGMOD’96
    ◼    Incrementally construct a CF (Clustering Feature) tree, a hierarchical data
         structure for multiphase clustering
             ◼   Phase 1: scan DB to build an initial in-memory CF tree (a multi-level
                 compression of the data that tries to preserve the inherent clustering
                 structure of the data)
             ◼   Phase 2: use an arbitrary clustering algorithm to cluster the leaf nodes of
                 the CF-tree
    ◼    Scales linearly: finds a good clustering with a single scan and improves the
         quality with a few additional scans
    ◼    Weakness: handles only numeric data, and sensitive to the order of the data
         record

09/04/2022                                IT701010 - Chapter 6 - Clustering                    42
```

## Trang PDF 43

```text
             Clustering Feature Vector in BIRCH

    Clustering Feature (CF): CF = (N, LS, SS)
    N: Number of data points
                                              N
    LS: linear sum of N points:  X i
                                          i =1


                                                                               CF = (5, (16,30),(54,190))
    SS: square sum of N points
                N      2    10

                                                                                      (3,4)
                 Xi
                             9


                             8




                i =1
                             7


                             6
                                                                                      (2,6)
                             5


                             4                                                        (4,5)
                             3


                             2


                             1
                                                                                      (4,7)
                             0
                                 0    1   2   3   4   5   6   7   8   9   10
                                                                                      (3,8)

43
09/04/2022                           IT701010 - Chapter 6 - Clustering
```

## Trang PDF 44

```text
                             CF-Tree in BIRCH
     ◼       Clustering feature:
             ◼ Summary of the statistics for a given subcluster: the
               0-th, 1st, and 2nd moments of the subcluster from the
               statistical point of view
             ◼ Registers crucial measurements for computing cluster
               and utilizes storage efficiently
             A CF tree is a height-balanced tree that stores the clustering
             features for a hierarchical clustering
             ◼ A nonleaf node in a tree has descendants or “children”
             ◼ The nonleaf nodes store sums of the CFs of their
               children
     ◼       A CF tree has two parameters
             ◼ Branching factor: max # of children
             ◼ Threshold: max diameter of sub-clusters stored at the
               leaf nodes
09/04/2022                           IT701010 - Chapter 6 - Clustering        44
```

## Trang PDF 45

```text
                           The CF Tree Structure
                                         Root

    B=7               CF1      CF2 CF3                                     CF6
                      child1   child2 child3                               child6
    L=6

                            Non-leaf node
             CF1      CF2 CF3                               CF5
             child1   child2 child3                         child5


                           Leaf node                                                Leaf node
     prev CF1 CF2              CF6 next                   prev CF1 CF2               CF4 next



09/04/2022                             IT701010 - Chapter 6 - Clustering                        45
```

## Trang PDF 46

```text
                                The Birch Algorithm
     ◼       Cluster Diameter
                                              1
                                                     (x − x )
                                                               2

                                          n( n − 1)     i   j
     ◼       For each point in the input
              ◼ Find closest leaf entry

              ◼ Add point to leaf entry and update CF

              ◼ If entry diameter > max_diameter, then split leaf, and possibly parents

     ◼       Algorithm is O(n)
     ◼       Concerns
              ◼ Sensitive to insertion order of data points

              ◼ Since we fix the size of leaf nodes, so clusters may not be so natural

              ◼ Clusters tend to be spherical given the radius and diameter measures




09/04/2022                               IT701010 - Chapter 6 - Clustering                46
```

## Trang PDF 47

```text
              CHAMELEON: Hierarchical Clustering
                Using Dynamic Modeling (1999)
   ◼     CHAMELEON: G. Karypis, E. H. Han, and V. Kumar, 1999
   ◼     Measures the similarity based on a dynamic model
         ◼   Two clusters are merged only if the interconnectivity and
             closeness (proximity) between two clusters are high relative
             to the internal interconnectivity of the clusters and closeness
             of items within the clusters
   ◼     Graph-based, and a two-phase algorithm
         1. Use a graph-partitioning algorithm: cluster objects into a
            large number of relatively small sub-clusters
         2. Use an agglomerative hierarchical clustering algorithm: find
            the genuine clusters by repeatedly combining these sub-
            clusters
09/04/2022                          IT701010 - Chapter 6 - Clustering          47
```

## Trang PDF 48

```text
                                Overall Framework of
                                  CHAMELEON
             Construct (K-NN)
             Sparse Graph                            Partition the Graph




 Data Set



  K-NN Graph
    P and q are connected if                                                     Merge Partition
    q is among the top k
    closest neighbors of p
                                                                           Relative interconnectivity:
                                                                           connectivity of c1 and c2
                                                                           over internal connectivity
                                  Final Clusters
                                                                           Relative closeness:
                                                                           closeness of c1 and c2 over
                                                                           internal closeness
09/04/2022                          IT701010 - Chapter 6 - Clustering                               48
```

## Trang PDF 49

```text
             CHAMELEON (Clustering Complex
                     Objects)




09/04/2022           IT701010 - Chapter 6 - Clustering   49
```

## Trang PDF 50

```text
                   Probabilistic Hierarchical Clustering
     ◼       Algorithmic hierarchical clustering
              ◼   Nontrivial to choose a good distance measure
              ◼   Hard to handle missing attribute values
              ◼   Optimization goal not clear: heuristic, local search
     ◼       Probabilistic hierarchical clustering
              ◼   Use probabilistic models to measure distances between clusters
              ◼   Generative model: Regard the set of data objects to be clustered as a
                  sample of the underlying data generation mechanism to be analyzed
              ◼   Easy to understand, same efficiency as algorithmic agglomerative
                  clustering method, can handle partially observed data
     ◼       In practice, assume the generative models adopt common distributions
             functions, e.g., Gaussian distribution or Bernoulli distribution, governed by
             parameters

09/04/2022                                 IT701010 - Chapter 6 - Clustering                 50
```

## Trang PDF 51

```text
                                 Generative Model
     ◼       Given a set of 1-D points X = {x1, …, xn} for clustering
             analysis & assuming they are generated by a Gaussian
             distribution:

     ◼       The probability that a point xi ∈ X is generated by the model

     ◼       The likelihood that X is generated by the model:


     ◼       The task of learning the generative model: find the
             parameters μ and σ2 such that


                                                                             the maximum likelihood




09/04/2022                               IT701010 - Chapter 6 - Clustering                       51
```

## Trang PDF 52

```text
 A Probabilistic Hierarchical Clustering Algorithm
   ◼    For a set of objects partitioned into m clusters C1, . . . ,Cm, the quality can be
        measured by,

         where P() is the maximum likelihood
   ◼    Distance between clusters C1 and C2:
   ◼    Algorithm: Progressively merge points and clusters
         Input: D = {o1, ..., on}: a data set containing n objects
         Output: A hierarchy of clusters
         Method
             Create a cluster for each object Ci = {oi}, 1 ≤ i ≤ n;
             For i = 1 to n {
                  Find pair of clusters Ci and Cj such that
                       Ci,Cj = argmaxi ≠ j {log (P(Ci∪Cj )/(P(Ci)P(Cj ))};
                  If log (P(Ci∪Cj )/(P(Ci)P(Cj )) > 0 then merge Ci and Cj }




09/04/2022                             IT701010 - Chapter 6 - Clustering                     52
```

## Trang PDF 53

```text
  Chapter 10. Cluster Analysis: Basic Concepts and
                      Methods

     ◼       Cluster Analysis: Basic Concepts
     ◼       Partitioning Methods
     ◼       Hierarchical Methods
     ◼       Density-Based Methods
     ◼       Grid-Based Methods
     ◼       Evaluation of Clustering
     ◼       Summary
09/04/2022                   IT701010 - Chapter 6 - Clustering   53
```

## Trang PDF 54

```text
                 Density-Based Clustering Methods
     ◼ Clustering based on density (local cluster criterion), such as
       density-connected points
     ◼ Major features:

             ◼ Discover clusters of arbitrary shape
             ◼ Handle noise

             ◼ One scan

             ◼ Need density parameters as termination condition

     ◼       Several interesting studies:
             ◼ DBSCAN: Ester, et al. (KDD’96)
             ◼ OPTICS: Ankerst, et al (SIGMOD’99).

             ◼ DENCLUE: Hinneburg & D. Keim (KDD’98)

             ◼ CLIQUE: Agrawal, et al. (SIGMOD’98) (more grid-
               based)
09/04/2022                           IT701010 - Chapter 6 - Clustering   54
```

## Trang PDF 55

```text
                  Density-Based Clustering: Basic Concepts
    ◼    Two parameters:
             ◼   Eps: Maximum radius of the neighbourhood
             ◼   MinPts: Minimum number of points in an Eps-
                 neighbourhood of that point
    ◼    NEps(p): {q belongs to D | dist(p,q) ≤ Eps}
    ◼    Directly density-reachable: A point p is directly density-
         reachable from a point q w.r.t. Eps, MinPts if
             ◼   p belongs to NEps(q)                                      p   MinPts = 5
             ◼   core point condition:                                         Eps = 1 cm
                                                                       q
                       |NEps (q)| ≥ MinPts
09/04/2022                         IT701010 - Chapter 6 - Clustering                        55
```

## Trang PDF 56

```text
               Density-Reachable and Density-Connected
   ◼    Density-reachable:
         ◼   A point p is density-reachable                                      p
             from a point q w.r.t. Eps, MinPts
             if there is a chain of points p1, …,                   q
                                                                            p1
             pn, p1 = q, pn = p such that pi+1 is
             directly density-reachable from
             pi
   ◼    Density-connected
         ◼   A point p is density-connected to p                                     q
             a point q w.r.t. Eps, MinPts if
             there is a point o such that both,                         o
             p and q are density-reachable
             from o w.r.t. Eps and MinPts
09/04/2022                      IT701010 - Chapter 6 - Clustering                        56
```

## Trang PDF 57

```text
                DBSCAN: Density-Based Spatial
              Clustering of Applications with Noise
   ◼ Relies on a density-based notion of cluster: A cluster is defined
     as a maximal set of density-connected points
   ◼ Discovers clusters of arbitrary shape in spatial databases with
     noise



                                                                  Outlier

                  Border
                                                                      Eps = 1cm
                      Core                                            MinPts = 5


09/04/2022                    IT701010 - Chapter 6 - Clustering                    57
```

## Trang PDF 58

```text
                DBSCAN: The Algorithm
    ◼    Arbitrary select a point p

    ◼    Retrieve all points density-reachable from p w.r.t. Eps and
         MinPts

    ◼    If p is a core point, a cluster is formed

    ◼    If p is a border point, no points are density-reachable from p
         and DBSCAN visits the next point of the database

    ◼    Continue the process until all of the points have been processed




09/04/2022                         IT701010 - Chapter 6 - Clustering        58
```

## Trang PDF 59

```text
             DBSCAN: Sensitive to Parameters




09/04/2022              IT701010 - Chapter 6 - Clustering   59
```

## Trang PDF 60

```text
                  OPTICS: A Cluster-Ordering Method
                               (1999)
    ◼    OPTICS: Ordering Points To Identify the Clustering Structure
             ◼ Ankerst, Breunig, Kriegel, and Sander
               (SIGMOD’99)
             ◼ Produces a special order of the database wrt its
               density-based clustering structure
             ◼ This cluster-ordering contains info equiv to the
               density-based clusterings corresponding to a broad
               range of parameter settings
             ◼ Good for both automatic and interactive cluster
               analysis, including finding intrinsic clustering
               structure
             ◼ Can be represented graphically or using
               visualization techniques
09/04/2022                      IT701010 - Chapter 6 - Clustering       60
```

## Trang PDF 61

```text
                      OPTICS: Some Extension from
                               DBSCAN
   ◼    Index-based:
              ◼   k = number of dimensions
              ◼   N = 20
              ◼   p = 75%                                                           D
              ◼   M = N(1-p) = 5
         ◼   Complexity: O(NlogN)
   ◼    Core Distance:                                   p1
         ◼   min eps s.t. point is core
   ◼    Reachability Distance                            o
                                      p2                                        o
       Max (core-distance (o), d (o, p))                           MinPts = 5
       r(p1, o) = 2.8cm. r(p2,o) = 4cm
09/04/2022
                                                                   e = 3 cm
                                   IT701010 - Chapter 6 - Clustering                    61
```

## Trang PDF 62

```text
       Reachability
       -distance




   undefined
             e
                      e
             e‘


                                                              Cluster-order
                                                              of the objects
62
09/04/2022                IT701010 - Chapter 6 - Clustering
```

## Trang PDF 63

```text
             Density-Based Clustering: OPTICS & Its
                          Applications




09/04/2022              IT701010 - Chapter 6 - Clustering   63
```

## Trang PDF 64

```text
                              DENCLUE: Using Statistical Density
                                       Functions
     ◼       DENsity-based CLUstEring by Hinneburg & Keim (KDD’98)
                                                                                                                          total influence
     ◼       Using statistical density functions:                                                                         on x
                                                                                                                    d ( x , xi ) 2
                                                            2                                                   −
                                                                                            ( x ) =  i =1 e
                                                 d ( x,y)                                                   N
                                             −                                    D                                    2 2
                  f Gaussian ( x , y ) = e          2 2                     f   Gaussian

                                                                                                                                  d ( x , xi ) 2
                                       influence of y                                                                         −
                                                                                         ( x, xi ) = i =1 ( xi − x)  e
                                                                                                        N
     ◼       Major features
                                       on x                                f     D
                                                                                 Gaussian
                                                                                                                                     2 2


                                                                                                                       gradient of x in
              ◼    Solid mathematical foundation                                                                       the direction of
                                                                                                                       xi
              ◼    Good for data sets with large amounts of noise
              ◼    Allows a compact mathematical description of arbitrarily shaped clusters
                   in high-dimensional data sets
              ◼    Significant faster than existing algorithm (e.g., DBSCAN)
              ◼    But needs a large number of parameters
09/04/2022                                                      IT701010 - Chapter 6 - Clustering                                                  64
```

## Trang PDF 65

```text
                    Denclue: Technical Essence
    ◼    Uses grid cells but only keeps information about grid cells that do actually
         contain data points and manages these cells in a tree-based access structure
    ◼    Influence function: describes the impact of a data point within its
         neighborhood
    ◼    Overall density of the data space can be calculated as the sum of the influence
         function of all data points
    ◼    Clusters can be determined mathematically by identifying density attractors
    ◼    Density attractors are local maximal of the overall density function
    ◼    Center defined clusters: assign to each density attractor the points density
         attracted to it
    ◼    Arbitrary shaped cluster: merge density attractors that are connected through
         paths of high density (> threshold)




09/04/2022                            IT701010 - Chapter 6 - Clustering                    65
```

## Trang PDF 66

```text
             Density Attractor




09/04/2022      IT701010 - Chapter 6 - Clustering   66
```

## Trang PDF 67

```text
             Center-Defined and Arbitrary




09/04/2022            IT701010 - Chapter 6 - Clustering   67
```

## Trang PDF 68

```text
  Chapter 10. Cluster Analysis: Basic Concepts and
                      Methods

     ◼       Cluster Analysis: Basic Concepts
     ◼       Partitioning Methods
     ◼       Hierarchical Methods
     ◼       Density-Based Methods
     ◼       Grid-Based Methods
     ◼       Evaluation of Clustering
     ◼       Summary
09/04/2022                   IT701010 - Chapter 6 - Clustering   68
```

## Trang PDF 69

```text
                      Grid-Based Clustering Method

     ◼ Using multi-resolution grid data structure
     ◼ Several interesting methods

             ◼ STING (a STatistical INformation Grid approach)
               by Wang, Yang and Muntz (1997)
             ◼ WaveCluster by Sheikholeslami, Chatterjee, and
               Zhang (VLDB’98)
                  ◼   A multi-resolution clustering approach using wavelet
                      method
             ◼   CLIQUE: Agrawal, et al. (SIGMOD’98)
                  ◼   Both grid-based and subspace clustering



09/04/2022                            IT701010 - Chapter 6 - Clustering      69
```

## Trang PDF 70

```text
              STING: A Statistical Information Grid
                          Approach
    ◼ Wang, Yang and Muntz (VLDB’97)
    ◼ The spatial area is divided into rectangular cells

    ◼ There are several levels of cells corresponding to different levels
      of resolution




09/04/2022                     IT701010 - Chapter 6 - Clustering            70
```

## Trang PDF 71

```text
                 The STING Clustering Method
    ◼ Each cell at a high level is partitioned into a number of smaller
      cells in the next lower level
    ◼ Statistical info of each cell is calculated and stored beforehand
      and is used to answer queries
    ◼ Parameters of higher level cells can be easily calculated from
      parameters of lower level cell
             ◼ count, mean, s, min, max
             ◼ type of distribution—normal, uniform, etc.
    ◼ Use a top-down approach to answer spatial data queries
    ◼ Start from a pre-selected layer—typically with a small number
      of cells
    ◼ For each cell in the current level compute the confidence interval




09/04/2022                      IT701010 - Chapter 6 - Clustering          71
```

## Trang PDF 72

```text
                 STING Algorithm and Its Analysis

     ◼ Remove the irrelevant cells from further consideration
     ◼ When finish examining the current layer, proceed to the next
       lower level
     ◼ Repeat this process until the bottom layer is reached

     ◼ Advantages:

             ◼ Query-independent, easy to parallelize, incremental
               update
             ◼ O(K), where K is the number of grid cells at the
               lowest level
     ◼       Disadvantages:
             ◼   All the cluster boundaries are either horizontal or
                 vertical, and no diagonal boundary is detected
09/04/2022                        IT701010 - Chapter 6 - Clustering    72
```

## Trang PDF 73

```text
                 CLIQUE (Clustering In QUEst)

   ◼    Agrawal, Gehrke, Gunopulos, Raghavan (SIGMOD’98)
   ◼    Automatically identifying subspaces of a high dimensional data space that allow
        better clustering than original space
   ◼    CLIQUE can be considered as both density-based and grid-based
         ◼   It partitions each dimension into the same number of equal length interval
         ◼   It partitions an m-dimensional data space into non-overlapping rectangular
             units
         ◼   A unit is dense if the fraction of total data points contained in the unit
             exceeds the input model parameter
         ◼   A cluster is a maximal set of connected dense units within a subspace



09/04/2022                              IT701010 - Chapter 6 - Clustering                 73
```

## Trang PDF 74

```text
                CLIQUE: The Major Steps

  ◼   Partition the data space and find the number of points that lie
      inside each cell of the partition.
  ◼   Identify the subspaces that contain clusters using the Apriori
      principle
  ◼   Identify clusters
      ◼ Determine dense units in all subspaces of interests
      ◼ Determine connected dense units in all subspaces of
        interests.
  ◼   Generate minimal description for the clusters
      ◼      Determine maximal regions that cover a cluster of
             connected dense units for each cluster
           ◼ Determination of minimal cover for each cluster
09/04/2022                    IT701010 - Chapter 6 - Clustering         74
```

## Trang PDF 75

```text
               Salary                                                             Vacation


               (10,000)                                                           (week)



   0 1 2 3 4 5 6 7                                                    0 1 2 3 4 5 6 7
                                                      age                                                       age
                    20    30   40   50              60                                 20    30   40     50   60


    =3
                                         Vacation



                                                          30                 50
                                                                                                   age




09/04/2022                                           IT701010 - Chapter 6 - Clustering                                75
```

## Trang PDF 76

```text
                   Strength and Weakness of CLIQUE

    ◼    Strength
             ◼ automatically finds subspaces of the highest
               dimensionality such that high density clusters exist
               in those subspaces
             ◼ insensitive to the order of records in input and does
               not presume some canonical data distribution
             ◼ scales linearly with the size of input and has good
               scalability as the number of dimensions in the data
               increases
    ◼    Weakness
             ◼   The accuracy of the clustering result may be
                 degraded at the expense of simplicity of the method

09/04/2022                        IT701010 - Chapter 6 - Clustering    76
```

## Trang PDF 77

```text
                    Chapter 10. Cluster Analysis: Basic
                         Concepts and Methods

     ◼       Cluster Analysis: Basic Concepts

     ◼       Partitioning Methods

     ◼       Hierarchical Methods

     ◼       Density-Based Methods

     ◼       Grid-Based Methods

     ◼       Evaluation of Clustering

     ◼       Summary
09/04/2022                     IT701010 - Chapter 6 - Clustering   77
```

## Trang PDF 78

```text
                         Assessing Clustering Tendency

     ◼       Assess if non-random structure exists in the data by measuring the probability
             that the data is generated by a uniform data distribution
     ◼       Test spatial randomness by statistic test: Hopkins Static
              ◼ Given a dataset D regarded as a sample of a random variable o, determine
                 how far away o is from being uniformly distributed in the data space
              ◼ Sample n points, p1, …, pn, uniformly from D. For each pi, find its
                 nearest neighbor in D: xi = min{dist (pi, v)} where v in D
              ◼ Sample n points, q1, …, qn, uniformly from D. For each qi, find its
                 nearest neighbor in D – {qi}: yi = min{dist (qi, v)} where v in D and v ≠ qi
              ◼ Calculate the Hopkins Statistic:



              ◼   If D is uniformly distributed, ∑ xi and ∑ yi will be close to each other and
                  H is close to 0.5. If D is highly skewed, H is close to 0




09/04/2022                                 IT701010 - Chapter 6 - Clustering                     78
                                                                                                 78
```

## Trang PDF 79

```text
                 Determine the Number of Clusters
   ◼    Empirical method
         ◼ # of clusters ≈√n/2 for a dataset of n points

   ◼    Elbow method
         ◼ Use the turning point in the curve of sum of within cluster variance w.r.t
           the # of clusters
   ◼    Cross validation method
         ◼ Divide a given data set into m parts

         ◼ Use m – 1 parts to obtain a clustering model

         ◼ Use the remaining part to test the quality of the clustering

             ◼ E.g., For each point in the test set, find the closest centroid, and use the
               sum of squared distance between all points in the test set and the closest
               centroids to measure how well the model fits the test set
         ◼ For any k > 0, repeat it m times, compare the overall quality measure w.r.t.
           different k’s, and find # of clusters that fits the data the best




09/04/2022                            IT701010 - Chapter 6 - Clustering                       79
                                                                                              79
```

## Trang PDF 80

```text
                       Measuring Clustering Quality
    ◼    Two methods: extrinsic vs. intrinsic
    ◼    Extrinsic: supervised, i.e., the ground truth is available
             ◼   Compare a clustering against the ground truth using
                 certain clustering quality measure
             ◼   Ex. BCubed precision and recall metrics
    ◼    Intrinsic: unsupervised, i.e., the ground truth is unavailable
             ◼   Evaluate the goodness of a clustering by considering
                 how well the clusters are separated, and how
                 compact the clusters are
             ◼   Ex. Silhouette coefficient
09/04/2022                         IT701010 - Chapter 6 - Clustering      80
                                                                          80
```

## Trang PDF 81

```text
                  Measuring Clustering Quality: Extrinsic
                                Methods

     ◼ Clustering quality measure: Q(C, Cg), for a clustering C given
       the ground truth Cg.
     ◼ Q is good if it satisfies the following 4 essential criteria

             ◼ Cluster homogeneity: the purer, the better
             ◼ Cluster completeness: should assign objects belong
               to the same category in the ground truth to the same
               cluster
             ◼ Rag bag: putting a heterogeneous object into a pure
               cluster should be penalized more than putting it into
               a rag bag (i.e., “miscellaneous” or “other” category)
             ◼ Small cluster preservation: splitting a small category
               into pieces is more harmful than splitting a large
               category into pieces
09/04/2022                      IT701010 - Chapter 6 - Clustering       81
                                                                        81
```

## Trang PDF 82

```text
                    Chapter 10. Cluster Analysis: Basic
                         Concepts and Methods

     ◼       Cluster Analysis: Basic Concepts

     ◼       Partitioning Methods

     ◼       Hierarchical Methods

     ◼       Density-Based Methods

     ◼       Grid-Based Methods

     ◼       Evaluation of Clustering

     ◼       Summary
09/04/2022                     IT701010 - Chapter 6 - Clustering   82
```

## Trang PDF 83

```text
                                    Summary
     ◼       Cluster analysis groups objects based on their similarity and has wide
             applications
     ◼       Measure of similarity can be computed for various types of data
     ◼       Clustering algorithms can be categorized into partitioning methods,
             hierarchical methods, density-based methods, grid-based methods, and
             model-based methods
     ◼       K-means and K-medoids algorithms are popular partitioning-based
             clustering algorithms
     ◼       Birch and Chameleon are interesting hierarchical clustering algorithms, and
             there are also probabilistic hierarchical clustering algorithms
     ◼       DBSCAN, OPTICS, and DENCLU are interesting density-based algorithms
     ◼       STING and CLIQUE are grid-based methods, where CLIQUE is also a
             subspace clustering algorithm
     ◼       Quality of clustering results can be evaluated in various ways




09/04/2022                              IT701010 - Chapter 6 - Clustering                  83
```