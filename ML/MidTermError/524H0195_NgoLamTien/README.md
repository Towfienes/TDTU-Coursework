# BÁO CÁO VÀ MÃ NGUỒN BÀI TẬP GIỮA KỲ
## Môn học: Introduction to Machine Learning (Nhập môn Học máy)

### Thông tin nhóm sinh viên:
- **Ngô Lâm Tiến** - MSSV: **524H0195** (Nhóm trưởng)
- **Nguyễn Công Thành** - MSSV: **524H0191**
- **Nguyễn Lê Nhật Tâm** - MSSV: **524H0186**

---

### Cấu trúc bài nộp:
- `Bao_Cao_Giua_Ky_ML.pdf`: File báo cáo hoàn chỉnh trình bày lý thuyết đạo hàm, thuật toán Gradient Descent, tiền xử lý dữ liệu và kết quả thực nghiệm.
- `notebooks/`:
  - `Q1_Linear_Regression.ipynb`: Đạo hàm, cài đặt từ đầu (scratch) và thực nghiệm Hồi quy tuyến tính (Linear Regression).
  - `Q1_Logistic_Regression.ipynb`: Đạo hàm, cài đặt từ đầu (scratch) và thực nghiệm Hồi quy Logistic (Logistic Regression).
  - `Q2_Classification.ipynb`: Tiền xử lý dữ liệu German Credit (OpenML), huấn luyện và so sánh 12 mô hình phân loại, phân tích hiện tượng Overfitting và các giải pháp khắc phục.
- `src/`: Các module mã nguồn Python:
  - `q1_models.py`: Cài đặt LinearRegressionGD và LogisticRegressionGD bằng NumPy cùng hàm Gradient Checking độc lập.
  - `data.py`: Tải và kiểm tra tính toàn vẹn dữ liệu `credit-g`.
  - `q2_classification.py`: Pipeline tiền xử lý và huấn luyện đánh giá 12 mô hình phân loại (5-fold Cross-Validation).
- `data/`: Dữ liệu bài toán German Credit (`credit-g.arff`).
- `figures/`: Các biểu đồ trực quan hóa dữ liệu và biểu đồ đo lường huấn luyện.
- `results/`: Kết quả đo lường và đánh giá thực nghiệm.
- `requirements.txt`: Danh sách các thư viện cần thiết.

---

### Hướng dẫn cài đặt và chạy thực nghiệm:

1. **Cài đặt môi trường:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy Jupyter Notebook:**
   - Mở Jupyter Notebook hoặc VS Code:
     ```bash
     jupyter notebook
     ```
   - Mở và chạy các file trong thư mục `notebooks/`:
     - `Q1_Linear_Regression.ipynb`
     - `Q1_Logistic_Regression.ipynb`
     - `Q2_Classification.ipynb`
