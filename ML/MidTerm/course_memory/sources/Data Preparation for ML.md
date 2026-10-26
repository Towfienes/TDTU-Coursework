# Data Preparation for ML.pdf

Nguồn: `ML/Introduction to machine learning/Data Preparation for ML.pdf`

Bản trích xuất văn bản tự động; công thức/hình có thể cần xem PDF gốc. Trang dưới đây là trang PDF, đếm từ 1.

## Trang PDF 1

```text
Data Preparation for
Machine Learning
      LÊ ANH CƯỜNG
   Ton Duc Thang University




                              1
```

## Trang PDF 2

```text
A General Machine Learning Diagram
                                                      Feature
                                         New input
                                                     Extraction



           Feature                                    Learnt
  Data                       Model Learning
          Extraction                                  Model



                                                       output
                                Model kind
                                 Selection


                       SVM, NB, DT, LR, NN, kNN,…

                                                                  2
```

## Trang PDF 3

```text
Basic Steps in Building ML Systems
• Step 1: Define Problem.
• Step 2: Prepare Data.
• Step 3: Evaluate Models.
• Step 4: Finalize Model.




                                     3
```

## Trang PDF 4

```text
     Structured data vs unstructured data
• Structured data is data that has been predefined        • Unstructured data is information that is not
  and formatted to a set structure before being             arranged according to a preset data model
  placed in data storage, which is often referred to as     or schema, and therefore cannot be stored
  schema-on-write. The best example of structured           in a traditional relational database or
  data is the relational database.                          RDBMS. Text and multimedia are two
                                                            common types of unstructured content.




                                                                                                           4
```

## Trang PDF 5

```text
ChatGPT




          5
```

## Trang PDF 6

```text
Data Preparation for using in Machine
Learning
1.Data collection: Gathering relevant data from various sources such as databases, APIs, and web
scraping.
2.Data cleaning: Removing missing values, duplicates, and outliers, and handling errors and
inconsistencies in the data.
3.Data normalization: Scaling the data so that it has the same range of values, allowing the
machine learning algorithms to treat all the features equally.
4.Data transformation: Converting the data into a suitable format for the machine learning
algorithm, such as encoding categorical variables, transforming skewed or imbalanced data, and
creating new features.
5.Data split: Dividing the data into training, validation, and testing sets for model evaluation and
selection.
6.Data augmentation: Creating additional synthetic data to overcome the limitations of limited
data availability and to increase the robustness of the model.

                                                                                                       6
```

## Trang PDF 7

```text
Liblaries for ML
• Numpy
• Pandas




                   7
```

## Trang PDF 8

```text
What is Numpy
• NumPy is the fundamental package for scientific computing in Python. It is a Python library
  that provides a multidimensional array object, various derived objects (such as masked
  arrays and matrices), and an assortment of routines for fast operations on arrays, including
  mathematical, logical, shape manipulation, sorting, selecting, I/O, discrete Fourier
  transforms, basic linear algebra, basic statistical operations, random simulation and much
  more.

• At the core of the NumPy package, is the ndarray object. This encapsulates n-
  dimensional arrays of homogeneous data types, with many operations being
  performed in compiled code for performance




                                                                                                 8
```

## Trang PDF 9

```text
Why Numpy?




             9
```

## Trang PDF 10

```text
Why Numpy?
NumPy (Numerical Python) is a library commonly used for scientific computing and data analysis,
and it is widely used in the machine learning community for several reasons:
• Numerical Computation: NumPy provides fast and efficient operations for numerical
  computation, such as vectorized operations and linear algebra.
• Array Handling: NumPy provides a multi-dimensional array data structure, known as a numpy
  array, which is well suited for handling large arrays of numerical data.
• Broadcasting: NumPy supports broadcasting, which allows operations to be performed on arrays
  with different shapes. This is particularly useful in machine learning when performing element-
  wise operations on arrays of different shapes.
• Interoperability: NumPy is compatible with other popular libraries used in the machine learning
  community, such as SciPy, Matplotlib, and scikit-learn, tensorflow,... making it easier to integrate
  with existing machine learning workflows.
• Performance: NumPy provides fast execution speeds, due to its use of low-level, highly optimized
  C code for array operations.

                                                                                                   10
```

## Trang PDF 11

```text
ndarray in Numpy




                   11
```

## Trang PDF 12

```text
What is Pandas
• Pandas is widely used in the field of data analysis and data
  manipulation, and is an essential tool for many data scientists and
  machine learning practitioners.
• It provides an easy-to-use and efficient data structure (DataFrame) to
  store and manipulate data, as well as a variety of functions to clean,
  preprocess, and transform data into a suitable format for machine
  learning models.
• Additionally, Pandas integrates well with other popular data science
  libraries such as NumPy and Matplotlib, making it a versatile tool for
  end-to-end data analysis and machine learning workflows.

                                                                      12
```

## Trang PDF 13

```text
Highlights of Pandas




                       13
```

## Trang PDF 14

```text
Practice
• Numpy
• Pandas + KNN




                 14
```

## Trang PDF 15

```text
Numpy
• Tạo mảng (Creating Array)
• Kích thước khuôn và ép khuôn (Shape and reshape)
• Chỉ số phần tử trong mảng (Array Indexing)
• Tách mảng con (Array Slicing)
• Lọc giá trị mảng bằng điều kiện (Array extraction by Condition)
• Tính toán trên ma trận (Operations on matrices)




                                                                    15
```

## Trang PDF 16

```text
Pandas
1. Read data (Đọc dữ liệu từ file, hiểu cấu trúc của dataframe)
2. Exact data (Trích xuất dữ liệu, trích chọn dữ liệu)
3. Draw graph (Vẽ đồ thị dữ liệu)
4. Transform data type (Chuyển đổi dữ liệu, xử lý dữ liệu)




                                                                  16
```

## Trang PDF 17

```text
Exercise
• https://www.machinelearningplus.com/python/101-numpy-exercises-
  python/
• https://www.machinelearningplus.com/python/101-pandas-exercises-
  python/




                                                                     17
```