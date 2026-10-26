# BÁO CÁO PHÂN TÍCH HỒI QUY TUYẾN TÍNH BỘI (CHAPTER 7: EXERCISE)
**Dự đoán doanh số bán hàng hàng tháng (Sales) dựa trên các kênh quảng cáo**

---

## TỔNG QUAN BÀI TOÁN & DỮ LIỆU
Doanh nghiệp thu thập dữ liệu về chi phí quảng cáo hàng tháng trên 4 kênh truyền thông và doanh số bán hàng tương ứng (đơn vị: ngàn USD):
- **TV:** Chi phí quảng cáo trên truyền hình.
- **Radio:** Chi phí quảng cáo trên đài phát thanh.
- **Newspaper:** Chi phí quảng cáo trên báo giấy.
- **Online:** Chi phí quảng cáo trực tuyến.
- **Sales:** Doanh số bán hàng hàng tháng (biến phụ thuộc).

> **Ghi chú về tập dữ liệu:** Đề bài nêu giả định *"Dữ liệu được thu thập trong 30 tháng gần nhất"*, đồng thời cung cấp tệp dữ liệu đính kèm `regression_sales_data_1000.xlsx` gồm 1000 quan sát. Báo cáo này trình bày đối chiếu chi tiết cả trên **mẫu 30 tháng gần nhất** (chuẩn theo kịch bản đề bài) và **toàn bộ 1000 quan sát** (toàn bộ file dữ liệu) nhằm đảm bảo kết quả toàn diện, chính xác và minh bạch 100%.

---

## 1. THE STATISTICAL MODEL (MÔ HÌNH THỐNG KÊ)

### a. Viết mô hình hồi quy tuyến tính bội
Phương trình mô hình hồi quy tuyến tính bội lý thuyết tổng thể có dạng:
$$\text{Sales} = \beta_0 + \beta_1 \cdot \text{TV} + \beta_2 \cdot \text{Radio} + \beta_3 \cdot \text{Newspaper} + \beta_4 \cdot \text{Online} + \epsilon$$

**Định nghĩa và ý nghĩa các thành phần:**
- $\text{Sales}$: Biến phụ thuộc (Dependent variable) – Doanh số bán hàng hàng tháng (ngàn USD).
- $\text{TV}, \text{Radio}, \text{Newspaper}, \text{Online}$: Các biến độc lập (Independent/Explanatory variables) – Chi phí quảng cáo trên các kênh tương ứng (ngàn USD).
- $\beta_0$: Hệ số chặn (Intercept) – Mức doanh số bán hàng kỳ vọng khi doanh nghiệp không chi tiêu cho bất kỳ kênh quảng cáo nào ($\text{TV} = \text{Radio} = \text{Newspaper} = \text{Online} = 0$).
- $\beta_1, \beta_2, \beta_3, \beta_4$: Các hệ số hồi quy riêng phần (Partial regression slope coefficients) – Đo lường mức thay đổi kỳ vọng của doanh số bán hàng khi chi phí quảng cáo ở kênh tương ứng tăng thêm 1 đơn vị (1 ngàn USD), trong điều kiện chi phí của tất cả các kênh khác giữ nguyên không đổi (*ceteris paribus*).
- $\epsilon$: Thành phần sai số ngẫu nhiên (Random disturbance / Error term) – Đại diện cho các yếu tố không quan sát được hoặc không đưa vào mô hình (chất lượng sản phẩm, đối thủ cạnh tranh, tính thời vụ, thị hiếu tiêu dùng,...).

### b. Các giả định cơ bản của mô hình hồi quy tuyến tính
Để ước lượng OLS (Ordinary Least Squares) là ước lượng tuyến tính không chệch tốt nhất (BLUE - Best Linear Unbiased Estimator) theo định lý Gauss-Markov, mô hình cần thỏa mãn 6 giả định:
1. **Tính tuyến tính của tham số (Linearity in parameters):** Mô hình phải tuyến tính theo các hệ số $\beta_j$, biến độc lập có thể phi tuyến nhưng tham số phải ở dạng tuyến tính.
2. **Kỳ vọng có điều kiện của sai số bằng 0 (Zero conditional mean of errors):** $E(\epsilon \mid X) = 0$. Giả định này khẳng định các biến giải thích là ngoại sinh (exogenous), không có hiện tượng bỏ sót biến quan trọng gây nội sinh (endogeneity).
3. **Phương sai sai số không đổi (Homoscedasticity):** $\text{Var}(\epsilon_i \mid X) = \sigma^2 = \text{const}$ với mọi quan sát $i$. Phương sai của sai số không thay đổi theo độ lớn của các biến độc lập.
4. **Không có tự tương quan (No autocorrelation):** $\text{Cov}(\epsilon_i, \epsilon_j) = 0$ với mọi $i \neq j$. Sai số của các tháng khác nhau độc lập với nhau.
5. **Không có đa cộng tuyến hoàn hảo (No perfect multicollinearity):** Giữa các biến độc lập không tồn tại mối quan hệ phụ thuộc tuyến tính hoàn hảo (hạng của ma trận $X$ bằng số tham số $k+1$).
6. **Sai số có phân phối chuẩn (Normality of errors):** $\epsilon \sim \mathcal{N}(0, \sigma^2)$. Giả định này đảm bảo tính hợp lệ của phân phối $t$ và phân phối $F$ trong các kiểm định giả thuyết ở mẫu hữu hạn.

---

## 2. INFERENCES ABOUT THE REGRESSION COEFFICIENTS (SUY DIỄN THỐNG KÊ VỀ CÁC HỆ SỐ HỒI QUY)

### a. Ước lượng mô hình hồi quy từ dữ liệu

#### Bảng kết quả ước lượng trên mẫu 30 tháng ($N = 30$ theo đề bài):
| Biến số | Hệ số ước lượng ($\hat{\beta}$) | Sai số chuẩn (Std Err) | Giá trị thống kê $t$ | $p$-value | Khoảng tin cậy 95% |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **const** | **6.8486** | 3.572 | 1.917 | 0.067 | [-0.508, 14.206] |
| **TV** | **0.0360** | 0.013 | 2.706 | **0.012** | [0.009, 0.063] |
| **Radio** | **0.2480** | 0.071 | 3.480 | **0.002** | [0.101, 0.395] |
| **Newspaper** | **-0.0069** | 0.044 | -0.158 | **0.876** | [-0.097, 0.083] |
| **Online** | **0.0590** | 0.028 | 2.089 | **0.047** | [0.001, 0.117] |

- **Hệ số xác định ($R^2$):** $0.4922$ (Mô hình giải thích được 49.22% sự biến thiên của doanh số).
- **Adjusted $R^2$:** $0.4109$
- **Kiểm định $F$ toàn phần:** $F(4, 25) = 6.058$, $p\text{-value} = 0.0015 < 0.05$ (Mô hình hồi quy có ý nghĩa thống kê tổng thể).
- **Phương trình hồi quy mẫu:**
$$\widehat{\text{Sales}} = 6.8486 + 0.0360 \cdot \text{TV} + 0.2480 \cdot \text{Radio} - 0.0069 \cdot \text{Newspaper} + 0.0590 \cdot \text{Online}$$

#### Bảng kết quả đối chiếu trên toàn bộ dữ liệu ($N = 1000$):
| Biến số | Hệ số ước lượng ($\hat{\beta}$) | Sai số chuẩn (Std Err) | Giá trị thống kê $t$ | $p$-value | Khoảng tin cậy 95% |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **const** | **5.0173** | 0.503 | 9.976 | < 0.001 | [4.030, 6.004] |
| **TV** | **0.0380** | 0.002 | 19.720 | < 0.001 | [0.034, 0.042] |
| **Radio** | **0.2945** | 0.009 | 31.092 | < 0.001 | [0.276, 0.313] |
| **Newspaper** | **0.0272** | 0.007 | 4.087 | < 0.001 | [0.014, 0.040] |
| **Online** | **0.0530** | 0.005 | 11.337 | < 0.001 | [0.044, 0.062] |
- $R^2 = 0.5872$, $\text{Adjusted } R^2 = 0.5856$, $F(4, 995) = 353.9$, $p < 0.001$.

### b. Kiểm định giả thuyết về các hệ số
Thiết lập cặp giả thuyết thống kê cho từng biến độc lập $X_i$:
- $H_0: \beta_i = 0$ (Kênh quảng cáo $X_i$ không có ảnh hưởng đến doanh số bán hàng).
- $H_1: \beta_i \neq 0$ (Kênh quảng cáo $X_i$ có ảnh hưởng đến doanh số bán hàng).

**Quy tắc quyết định ở mức ý nghĩa $\alpha = 0.05$:**
- Bác bỏ $H_0$ nếu $p\text{-value} \le 0.05$.
- Không bác bỏ $H_0$ nếu $p\text{-value} > 0.05$.

### c. Kết luận về ý nghĩa thống kê ($\alpha = 0.05$)
1. **Trên mẫu 30 tháng gần nhất:**
   - **TV ($p = 0.012 \le 0.05$):** Bác bỏ $H_0$. TV **có ảnh hưởng thống kê dương** đến doanh số. Mỗi 1 ngàn USD chi cho TV giúp tăng trung bình 36 USD doanh số.
   - **Radio ($p = 0.002 \le 0.05$):** Bác bỏ $H_0$. Radio **có ảnh hưởng thống kê dương mạnh nhất**. Mỗi 1 ngàn USD chi cho Radio giúp tăng trung bình 248 USD doanh số.
   - **Online ($p = 0.047 \le 0.05$):** Bác bỏ $H_0$. Online **có ảnh hưởng thống kê dương**. Mỗi 1 ngàn USD chi cho Online giúp tăng trung bình 59 USD doanh số.
   - **Newspaper ($p = 0.876 > 0.05$):** Không bác bỏ $H_0$. Chi phí quảng cáo báo giấy **KHÔNG có ảnh hưởng thống kê** đến doanh số bán hàng.
2. **Trên toàn bộ mẫu 1000 dòng:**
   - Do cỡ mẫu lớn, cả 4 biến đều có $p < 0.001$, tuy nhiên mức độ ảnh hưởng của Newspaper là nhỏ nhất ($\hat{\beta} = 0.0272, t = 4.087$).

---

## 3. MULTICOLLINEARITY (ĐA CỘNG TUYẾN)

### a. Tính hệ số VIF (Variance Inflation Factor)
Hệ số phóng đại phương sai của biến $X_j$ được tính theo công thức:
$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$
Trong đó $R_j^2$ là hệ số xác định khi hồi quy biến $X_j$ theo các biến độc lập còn lại.

**Bảng giá trị VIF tính được:**
| Biến số | VIF ($N = 30$) | VIF ($N = 1000$) | Đánh giá so với ngưỡng an toàn ($\text{VIF} < 5$) |
| :--- | :---: | :---: | :--- |
| **TV** | **1.0237** | **1.0024** | Hoàn toàn không có đa cộng tuyến |
| **Radio** | **1.0739** | **1.0048** | Hoàn toàn không có đa cộng tuyến |
| **Newspaper** | **1.0953** | **1.0012** | Hoàn toàn không có đa cộng tuyến |
| **Online** | **1.0446** | **1.0039** | Hoàn toàn không có đa cộng tuyến |

### b. Phát hiện biến có khả năng gây đa cộng tuyến
- **Tiêu chuẩn kiểm tra:**
  - $\text{VIF} < 5$: Mức độ cộng tuyến rất thấp, mô hình an toàn.
  - $5 \le \text{VIF} < 10$: Đa cộng tuyến mức độ trung bình.
  - $\text{VIF} \ge 10$: Đa cộng tuyến nghiêm trọng, làm sai lệch ước lượng OLS.
- **Kết luận:** Cả 4 biến đều có hệ số $\text{VIF} \approx 1.00 - 1.10$, thấp hơn rất nhiều so với ngưỡng cảnh báo 5. **Không có biến nào có khả năng gây đa cộng tuyến.** Các kênh quảng cáo gần như độc lập tuyến tính với nhau.

### c. Các giải pháp xử lý khi xảy ra đa cộng tuyến
Nếu mô hình hồi quy xuất hiện đa cộng tuyến cao, các giải pháp chuẩn bao gồm:
1. **Giữ lại biến:** Áp dụng khi đa cộng tuyến nhẹ, hoặc khi mục tiêu hàng đầu là dự đoán chính xác $Y$ (dự báo tổng thể không bị ảnh hưởng), hoặc biến có ý nghĩa lý thuyết bắt buộc phải có mặt.
2. **Loại bỏ biến (Drop collinear variables):** Loại bớt biến có VIF cao nhất trong nhóm biến bị cộng tuyến.
3. **Biến đổi biến (Feature Engineering):**
   - Kết hợp các biến tương quan thành một chỉ số tổng hợp (ví dụ: gộp chi phí quảng cáo truyền thống).
   - Áp dụng phương pháp Phân tích thành phần chính (PCA) để tạo các biến mới trực giao.
4. **Hồi quy điều quy hóa (Regularization):**
   - **Ridge Regression ($L_2$ regularization):** Co cụm các hệ số về gần 0, giải quyết sự bất ổn định của ma trận nghịch đảo.
   - **Lasso Regression ($L_1$ regularization):** Triệt tiêu các hệ số của biến dư thừa về đúng bằng 0 (tự động lựa chọn biến).
   - **Elastic Net:** Kết hợp cả chuẩn $L_1$ và $L_2$.

---

## 4. INCLUDE / EXCLUDE DECISIONS (QUYẾT ĐỊNH GIỮ LẠI / LOẠI BỎ BIẾN)

### a. Đề xuất giữ lại hay loại bỏ biến
- **Về đa cộng tuyến:** Hệ số VIF của tất cả các biến đều $\approx 1$, không có biến nào bị đa cộng tuyến. Do đó không cần loại bỏ biến nào vì lý do đa cộng tuyến.
- **Về ý nghĩa thống kê:**
  - Trên mẫu 30 tháng (chuẩn đề bài): Biến **`Newspaper`** có $p\text{-value} = 0.876 > 0.05$ và hệ số âm rất bé ($-0.0069$), chứng tỏ chi phí quảng cáo báo giấy hoàn toàn không đóng góp vào việc gia tăng doanh số.
  - **Đề xuất dứt khoát:** **LOẠI BỎ biến `Newspaper`, GIỮ LẠI 3 biến `TV`, `Radio`, và `Online`.**
  - Trên mẫu 1000 quan sát: Mặc dù `Newspaper` có $p < 0.05$ do cỡ mẫu lớn, nhưng tỷ lệ đóng góp của nó vào $R^2$ là cực kỳ nhỏ (chưa tới 0.7%). Việc giữ lại 3 kênh `TV`, `Radio`, `Online` vẫn là giải pháp thực tiễn tối ưu và tinh gọn nhất.

### b. Giải thích tác động đến mô hình khi loại bỏ biến
1. **Khi loại bỏ biến không có ý nghĩa thống kê (`Newspaper`):**
   - **Nguyên lý tinh gọn (Principle of Parsimony):** Mô hình trở nên đơn giản, tập trung vào các động lực thúc đẩy doanh số thực sự.
   - **Tăng hệ số Adjusted $R^2$:** Loại bỏ biến không đóng góp giúp loại bỏ phạt bậc tự do, đưa Adjusted $R^2$ tăng từ **$0.4109$** lên **$0.4334$** (tăng thêm 2.25%).
   - **Giảm chỉ số AIC và BIC:** $\text{AIC}$ giảm từ $159.2$ xuống $157.3$, $\text{BIC}$ giảm từ $166.2$ xuống $162.9$, khẳng định mô hình 3 biến tối ưu hơn.
   - **Giảm phương sai ước lượng:** Sai số chuẩn của các hệ số còn lại ổn định hơn, tránh hiện tượng overfitting.
   - **Ý nghĩa quản trị kinh doanh:** Giúp doanh nghiệp không lãng phí ngân sách tiếp thị vào kênh báo giấy không sinh lời.
2. **Khi loại bỏ biến bị đa cộng tuyến (nếu có):**
   - Giúp giảm sai số chuẩn của các hệ số hồi quy còn lại, làm cho các hệ số trở nên ổn định, không bị đảo dấu phi lý và dễ diễn giải.

---

## 5. STEPWISE REGRESSION (HỒI QUY TỪNG BƯỚC)

Quy trình hồi quy từng bước được thực hiện trên mẫu 30 tháng theo chuẩn phương pháp **Backward Elimination** và **Forward Selection** với ngưỡng $\alpha = 0.05$.

### a. & b. Các bước thực hiện hồi quy Stepwise

#### Quy trình Backward Elimination (Loại trừ dần):
- **Bước 1 (Mô hình đầy đủ 4 biến):**
  - Biến trong mô hình: `['TV', 'Radio', 'Newspaper', 'Online']`
  - $R^2 = 0.4922, \text{Adjusted } R^2 = 0.4109, \text{AIC} = 159.23$
  - Biến có $p\text{-value}$ lớn nhất: **`Newspaper`** với $p = 0.8759 > 0.05$.
  - $\rightarrow$ **Loại bỏ `Newspaper`** khỏi mô hình.
- **Bước 2 (Mô hình 3 biến):**
  - Biến trong mô hình: `['TV', 'Radio', 'Online']`
  - $R^2 = 0.4917, \text{Adjusted } R^2 = 0.4330, \text{AIC} = 157.26$
  - Các biến đều có $p \le 0.05$: `TV` ($p = 0.010$), `Radio` ($p = 0.001$), `Online` ($p = 0.043$).
  - Biến có p-value cao nhất là `Online` ($p = 0.043 \le 0.05$).
  - $\rightarrow$ **Dừng lại!** Đạt được mô hình tối ưu cuối cùng.

#### Quy trình Forward Selection (Lựa chọn tiến dần):
- **Bước 1:** Bắt đầu từ mô hình rỗng, biến đơn có tương quan cao nhất và $p$-value nhỏ nhất là **`Radio`** ($p = 0.0086$). Thêm `Radio` ($R^2 = 0.2219$).
- **Bước 2:** Trong các biến còn lại, biến đóng góp tốt nhất tiếp theo là **`TV`** ($p = 0.0081$). Thêm `TV` ($R^2 = 0.4029$).
- **Bước 3:** Biến tiếp theo có $p \le 0.05$ là **`Online`** ($p = 0.0427$). Thêm `Online` ($R^2 = 0.4917$).
- **Bước 4:** Biến còn lại duy nhất là `Newspaper` có $p = 0.8759 > 0.05$. Không thêm.
- $\rightarrow$ **Dừng lại!** Cả hai phương pháp đều hội tụ về tập 3 biến: `TV, Radio, Online`.

---

### c. Trình bày mô hình cuối cùng và So sánh với mô hình đầy đủ

#### 1. Phương trình mô hình cuối cùng (Final Model):
$$\widehat{\text{Sales}} = 6.6305 + 0.0360 \cdot \text{TV} + 0.2508 \cdot \text{Radio} + 0.0583 \cdot \text{Online}$$

#### 2. Bảng so sánh toàn diện giữa Mô hình đầy đủ và Mô hình cuối cùng:
| Tiêu chí so sánh | Mô hình đầy đủ (Full Model) | Mô hình cuối cùng (Final Model) | Đánh giá thay đổi |
| :--- | :---: | :---: | :--- |
| **Số biến độc lập** | 4 | 3 | Tinh gọn hơn 1 biến (`Newspaper`) |
| **Các biến được chọn** | TV, Radio, Newspaper, Online | TV, Radio, Online | Loại bỏ kênh báo giấy không hiệu quả |
| **$R^2$ (Hệ số xác định)** | **0.4922** | **0.4917** | Hầu như không đổi (chỉ giảm 0.0005) |
| **Adjusted $R^2$ (Hiệu chỉnh)** | **0.4109** | **0.4330** | **Tăng thêm 2.21%** (Mô hình tốt hơn) |
| **$F$-statistic** | **6.058** | **8.383** | **Tăng rõ rệt** (Mức tin cậy cao hơn) |
| **$p$-value ($F$)** | $0.00150$ | $0.00046$ | Ý nghĩa thống kê tổng thể mạnh hơn |
| **AIC** | **159.23** | **157.26** | **Giảm 1.97** (Tối ưu hơn) |
| **BIC** | **166.23** | **162.86** | **Giảm 3.37** (Tối ưu hơn) |

#### 3. Kết luận và Khuyến nghị kinh doanh:
1. **Về mặt thống kê:** Mô hình cuối cùng gồm 3 biến (`TV`, `Radio`, `Online`) là mô hình tối ưu nhất. Mô hình giữ được toàn bộ năng lực giải thích biến thiên của doanh số ($R^2 \approx 49.2\%$), trong khi Adjusted $R^2$ tăng lên, $F$-statistic tăng mạnh, các chỉ số AIC/BIC đều giảm.
2. **Về mặt thực tiễn phân bổ ngân sách tiếp thị:**
   - **Kênh Radio** có hệ số tác động cao nhất ($\hat{\beta}_2 = 0.2508$), mang lại tỷ suất gia tăng doanh số lớn nhất.
   - **Kênh Online** ($\hat{\beta}_4 = 0.0583$) và **TV** ($\hat{\beta}_1 = 0.0360$) có tác động tích cực và ổn định đến doanh số.
   - **Kênh Newspaper** không mang lại giá trị gia tăng rõ rệt cho doanh số bán hàng. Doanh nghiệp nên cắt giảm chi phí quảng cáo trên báo giấy và tái đầu tư vào Radio và Online để đạt hiệu quả doanh thu tối đa.

---
*Báo cáo được khởi tạo tự động dựa trên dữ liệu thực tế tại thư mục `/home/towfienes/TDTU/DA`.*

