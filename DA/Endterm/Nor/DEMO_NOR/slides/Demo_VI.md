# Transcript demo notebook — chia theo 6 phần

Dùng tại slide 15. Kéo notebook đến phần nào thì đọc đoạn **Lời đọc** của phần đó. Các dòng **Dừng màn hình** và **Tìm nhanh** chỉ hướng dẫn thao tác, không đọc thành lời.

Dự kiến khoảng **2 phút**, gồm chuyển cửa sổ; toàn bài slide và demo dự kiến **13 phút 20 giây**. Đây là kế hoạch để luyện, chưa phải thời lượng quay thực tế. Chỉ nói đoạn demo một lần, rồi quay về slide 16; slide 17–19 là phụ lục.

Mở sẵn notebook đã có output, hoặc `NOTEBOOK_DOC_OFFLINE.html` trong gói DEMO_NOR. Dùng tiêu đề sáu phần để định vị; số `In [n]` có thể thay đổi khi chạy riêng cell. Trong HTML, dùng Ctrl+F với tiêu đề tiếng Anh. Không cần chạy lại toàn bộ notebook trong lúc đọc.

**Câu mở khi chuyển từ slide 15 sang notebook:**

> Để minh họa quy trình phân tích, em xin chuyển sang notebook và lần lượt giới thiệu sáu phần chính.

## 1. Exploratory data analysis
### Khám phá và kiểm tra dữ liệu · khoảng 25 giây · 00:00–00:25

**Dừng màn hình:** Mục 1.1–1.2 và các output tiếp theo, `In [2]` đến `In [5]`. Dừng ở bảng chia tập rồi kéo qua bảng mô tả hoặc biểu đồ.

**Tìm nhanh:** `Original shape:` hoặc tiêu đề `1. Exploratory data analysis`.

**Lời đọc:**

> Ở phần một, chúng em đọc dữ liệu và kiểm tra cấu trúc, dữ liệu thiếu, trùng lặp và giá trị bất thường. Bộ dữ liệu có 4.177 quan sát và chín cột. Hai giá trị chiều cao bằng không được đánh dấu thiếu. Sau đó, chúng em giữ riêng 836 quan sát kiểm tra; thống kê mô tả và biểu đồ trên tập huấn luyện giúp nhận diện phân bố và các điểm cần xem xét.

## 2. Probability distributions
### Phân tích phân phối xác suất · khoảng 20 giây · 00:25–00:45

**Dừng màn hình:** `In [6]` đến `In [8]`. Dừng ở bảng kiểm định và một biểu đồ phân phối.

**Tìm nhanh:** `distribution_rows=[]` hoặc tiêu đề `2. Probability distributions`.

**Lời đọc:**

> Ở phần hai, chúng em kiểm tra phân phối chuẩn cho chiều dài, cùng phân phối chuẩn và lognormal cho khối lượng. Kiểm định Anderson–Darling dùng mô phỏng và ước lượng lại tham số. Cả ba giả thuyết đều bị bác bỏ sau điều chỉnh Holm. Vì vậy, các phân phối ứng viên này chưa mô tả đầy đủ dữ liệu.

## 3. Hypothesis testing
### Kiểm định giả thuyết · khoảng 20 giây · 00:45–01:05

**Dừng màn hình:** `In [9]` và `In [10]`. Dừng ở bảng có cột `p`, `p_holm` và dòng khoảng tin cậy Welch.

**Tìm nhanh:** `Welch difference and CI:` hoặc tiêu đề `3. Hypothesis testing`.

**Lời đọc:**

> Phần ba áp dụng Welch t-test, Chi-square và Welch ANOVA cho ba câu hỏi nghiên cứu. Kết quả được điều chỉnh Holm và đọc cùng độ lớn khác biệt. Chẳng hạn, số vòng trung bình của M thấp hơn F khoảng 0,355 vòng. Có bằng chứng thống kê về chênh lệch, nhưng không thể từ đó kết luận nguyên nhân sinh học.

## 4. Pearson and Spearman correlation
### Phân tích tương quan · khoảng 15 giây · 01:05–01:20

**Dừng màn hình:** `In [11]` và `In [12]`. Dừng ở bảng tương quan với Rings hoặc heatmap; chỉ hàng Shell weight.

**Tìm nhanh:** `correlations=` hoặc tiêu đề `4. Pearson and Spearman correlation`.

**Lời đọc:**

> Ở phần bốn, Pearson đo liên hệ tuyến tính, còn Spearman đo liên hệ theo thứ hạng. Khối lượng vỏ có tương quan nổi bật với số vòng: lần lượt khoảng 0,628 và 0,693. Đây là liên hệ giữa từng cặp biến, chưa phải đóng góp riêng trong mô hình đa biến.

## 5. Multiple linear regression
### Hồi quy tuyến tính đa biến · khoảng 30 giây · 01:20–01:50

**Dừng màn hình:** `In [13]` đến `In [16]`. Dừng ở vòng lặp fit/predict rồi bảng `test_metrics`; không cần đọc hết bảng hệ số và chẩn đoán.

**Tìm nhanh:** `display(test_metrics)` hoặc tiêu đề `5. Multiple linear regression`.

**Lời đọc:**

> Phần năm so sánh baseline, mô hình gọn và mô hình đầy đủ. Trong kiểm định chéo năm phần, quy trình điền thiếu và chuẩn hóa được học lại trên phần huấn luyện của từng vòng, nhằm hạn chế rò rỉ dữ liệu. Trên tập test giữ riêng, mô hình đầy đủ đạt RMSE khoảng 2,25 vòng, so với 3,27 của baseline. Chúng em cũng kiểm tra phần dư, đa cộng tuyến và độ nhạy với các quan sát có ảnh hưởng.

## 6. Synthesis and reproducible exports
### Tổng hợp và xuất kết quả · khoảng 10 giây · 01:50–02:00

**Dừng màn hình:** `In [17]` và đoạn tổng kết ngay phía trên. Chỉ phần xuất summary, không đọc các mảng số dài.

**Tìm nhanh:** `summary={` hoặc tiêu đề `6. Synthesis and reproducible exports`.

**Lời đọc:**

> Cuối cùng, notebook xuất các bảng, hình và số liệu tổng hợp để truy vết kết quả trong báo cáo. Mô hình cải thiện dự đoán, nhưng vẫn có sai số và giới hạn khái quát. Em xin trở lại slide kết luận.

## Nhớ khi thao tác

- Kéo lần lượt từ phần 1 đến phần 6; ở mỗi phần dừng một bảng hoặc một biểu đồ tiêu biểu, nói xong mới kéo tiếp.
- Phần 5: `a` và `b` là train/validation bên trong kiểm định chéo; tập test 836 dòng được giữ riêng. Không gọi `b` là tập test.
- Notebook gọi `regression_pipeline` từ `src/analysis.py`. Nếu chỉ hiện lời gọi hàm, giải thích cách tổ chức quy trình; không nói phần thân imputer/scaler đang hiện trên màn hình.
- R² không phải tỷ lệ dự đoán đúng. Tương quan không chứng minh nhân quả; điểm được gắn cờ không tự động là dữ liệu sai.
- Mở và kiểm tra notebook trước khi quay. Nếu Jupyter gặp lỗi, chuyển sang HTML offline; giới thiệu đúng là đang trình bày code và kết quả đã lưu.
