# 📚 Homework 1: Data Preprocessing & kNN

**Sinh viên:** Ngô Lâm Tiên | **MSSV:** 524H0195  
**Môn học:** Machine Learning | **Năm học:** 2025–2026

---

## 📁 Danh sách File Nộp

| File | Mô tả |
|------|-------|
| `HW1_DataPreprocessing_KNN.ipynb` | **Notebook chính** — toàn bộ code thực hành |
| `HW1_DataPreprocessing_Presentation.pptx` | **Slide thuyết trình lý thuyết** (12 slides) |
| `generate_hw1_presentation.py` | Script tạo slide (python-pptx) |
| `README_HW1.md` | File này |

---

## 🎯 Yêu cầu đã hoàn thành

### Phần 1: Thuyết trình lý thuyết (`HW1_DataPreprocessing_Presentation.pptx`)

| Slide | Nội dung |
|-------|---------|
| 1 | Cover — thông tin sinh viên |
| 2 | Agenda / Table of Contents |
| 3 | Data Preprocessing tổng quan |
| 4 | **Data Cleaning** (Missing, Duplicate, Inconsistent, Invalid) |
| 5 | **Missing-Value Handling** (4 chiến lược) |
| 6 | **Data Conversion & Categorical Encoding** (Label, Ordinal, One-Hot, Target, Text, Datetime) |
| 7 | **Feature Scaling** (Min-Max, Standard, Robust, Log) |
| 8 | **Feature Engineering** (Binning, Interaction, Aggregation, Polynomial, Text) |
| 9 | **Preprocessing Pipeline** (sklearn ColumnTransformer + Pipeline) |
| 10 | Bài thực hành — Telco Churn |
| 11 | Kết quả so sánh mô hình |
| 12 | Thank You / Q&A |

---

### Phần 2: Bài thực hành (`HW1_DataPreprocessing_KNN.ipynb`)

#### Dataset: **Telco Customer Churn**
- **Mục tiêu:** Dự đoán khách hàng có rời bỏ dịch vụ không (Yes/No)
- **Feature types:** Numerical, Categorical, Binary, Text (customerID)
- **Kích thước:** ~1,500 mẫu, 17 features

#### ✅ Data Cleaning
- **Missing values:** Median impute (numerical), Mode impute (categorical)
- **Duplicate rows:** Xóa 30 dòng trùng lặp
- **Inconsistent data:** Chuẩn hoá casing (gender: 'male' → 'Male')
- **Invalid values:** tenure < 0 → NaN; MonthlyCharges > 500 → NaN

#### ✅ Feature Engineering & Conversion
| Feature | Loại | Xử lý |
|---------|-------|-------|
| `customerID` | Text (ID thuần) | **DROP** (không có giá trị dự đoán) |
| `ContractRank` | Ordinal | Ánh xạ: Month-to-month=0, One year=1, Two year=2 |
| `ChargesPerMonth` | Numerical | TotalCharges / tenure |
| `NumServices` | Numerical | Đếm dịch vụ thêm (OnlineSecurity, TechSupport, ...) |
| `TenureGroup` | Categorical bins | pd.cut(tenure, bins=[0,12,24,48,72]) |

#### ✅ Preprocessing Pipeline (sklearn)
```python
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler())
])
cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer([
    ('num', num_pipeline, numerical_cols),
    ('bin', bin_pipeline, binary_cols),
    ('cat', cat_pipeline, categorical_cols),
])
```

#### ✅ Mô hình đã huấn luyện & so sánh

| # | Mô hình | Ghi chú |
|---|---------|---------|
| 1 | **kNN (k=7)** | K-Nearest Neighbors — mô hình chính |
| 2 | **Decision Tree** | Cây quyết định (max_depth=8) |
| 3 | **Naive Bayes** | Gaussian Naive Bayes |
| 4 | **Logistic Regression** | Hồi quy logistic |
| 5 | **Random Forest** | Ensemble 100 cây 🏆 |

#### ✅ Đánh giá mô hình
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix (visualized cho từng mô hình)
- Classification Report chi tiết
- 5-Fold Cross Validation (StratifiedKFold)
- kNN: Hyperparameter tuning — tìm k tối ưu (k=1..30)

---

## 🚀 Cách chạy

### Notebook
```bash
# Dùng Jupyter Notebook
jupyter notebook HW1_DataPreprocessing_KNN.ipynb

# Hoặc dùng VS Code với Jupyter extension
code HW1_DataPreprocessing_KNN.ipynb
```

### Tạo lại Presentation
```bash
python3 generate_hw1_presentation.py
```

---

## 📦 Thư viện cần thiết
```
pandas >= 1.5
numpy >= 1.21
scikit-learn >= 1.1
matplotlib >= 3.5
seaborn >= 0.11
```
