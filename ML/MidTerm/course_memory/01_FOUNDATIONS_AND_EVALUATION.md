# Nền tảng và đánh giá mô hình

Mã nguồn và tên file đầy đủ nằm ở [00_SOURCES.md](00_SOURCES.md). Trang là trang PDF đếm từ 1. Đây là ghi chú diễn giải bằng tiếng Việt từ tài liệu được cung cấp; các công thức được chuẩn hóa ký hiệu để dễ đối chiếu. Không có nguồn kiến thức ngoài thư mục môn học.

## 1. Môn học cần hiểu gì

Nguồn: L1 trang 4-11, 17-32, 34-39; SYL phần course objectives, CLOs, assessment và schedule.

AI là lĩnh vực xây dựng phương pháp mô phỏng khả năng học, hiểu, giải quyết vấn đề và ra quyết định. ML xây dựng mô hình từ dữ liệu để dự đoán hoặc ra quyết định. Sơ đồ trong slide đặt ML trong AI, neural networks trong ML và deep learning trong neural networks.

Ba thành phần cần phân biệt: **data, model, learning algorithm**. Chọn dạng mô hình trước; học tìm cấu trúc hoặc tham số từ ví dụ; inference dùng mô hình đã học trên đầu vào mới. Ví dụ quan hệ chiều cao-cân nặng: chọn $y=w_0+w_1x$, học $w_0,w_1$, rồi tính cân nặng dự đoán.

Luồng tổng quát: dữ liệu → biểu diễn/trích xuất đặc trưng → thuật toán học với loại mô hình đã chọn → mô hình đã học; đầu vào mới phải qua biểu diễn tương ứng rồi mới suy luận. Cần hiểu cấu trúc, cách dự đoán, thuật toán học, đánh giá, tiền xử lý và overfitting của mỗi mô hình.

- Supervised learning: ví dụ có đầu vào và nhãn/đích. Classification dự đoán nhãn rời rạc; regression dự đoán đại lượng thực.
- Unsupervised learning: khám phá cấu trúc không có lớp định sẵn; clustering là nội dung chính trong bộ slide.
- Reinforcement learning: xuất hiện ở sơ đồ và đề cương; không có bài giảng chi tiết riêng trong thư mục này.

Lịch sử và ứng dụng ở L1 là bối cảnh học thuật: retail, banking, transportation, logistics, translation, computer vision, healthcare và games. Những mốc thời gian và hình hiệu năng chỉ phản ánh bài giảng, không được dùng như kết luận về hiện trạng công nghệ.

Đề cương mã 503044: 3 tín chỉ, 45 giờ lý thuyết và 90 giờ tự học; mục tiêu bao gồm mô tả mô hình, cài đặt Python, phân tích thực nghiệm và đánh giá lý thuyết/thực hành. Tài liệu có mục sách tham khảo nhưng không có nội dung các sách đó; không được tuyên bố đã đọc các sách.

## 2. Học từ ví dụ và cực tiểu rủi ro

Nguồn: L2 trang 3-11.

$$D=\{(x_i,y_i)\}_{i=1}^N,\quad x_i\in\mathbb R^d.$$

Mục tiêu là học một hàm gần đúng $h:X\to Y$ có khả năng **generalize** từ số ví dụ hữu hạn sang dữ liệu mới. Nhãn nhị phân có thể mã hóa bằng $\{0,1\}$ hoặc $\{-1,+1\}$; phải chọn nhất quán với thuật toán.

Loss trên một ví dụ:

$$L(y,h(x))=(y-h(x))^2\quad\text{(regression)},$$
$$L(y,h(x))=\mathbf1[y\ne h(x)]\quad\text{(classification)}.$$

Expected risk là trung bình loss trên phân phối toàn bộ dữ liệu; empirical risk là trung bình trên tập học:

$$R(h)=\mathbb E_{(x,y)}[L(y,h(x))],\qquad
R_{\mathrm{emp}}(h)=\frac1N\sum_{i=1}^N L(y_i,h(x_i)).$$

Empirical risk minimization chọn

$$g=\arg\min_{h\in\mathcal H}R_{\mathrm{emp}}(h).$$

Không được đồng nhất loss train thấp với khả năng dự đoán tốt. Hình L2 trang 11 phân biệt underfit/high bias, vừa đủ và overfit/high variance. Cây quyết định cho thấy accuracy train tăng khi cây lớn nhưng accuracy test có thể giảm (DT trang 27, DTN trang 29).

## 3. Xác suất và học tham số

Nguồn: L2 trang 12-25; NB trang 9-12, 17-29.

$$P(A\mid B)=\frac{P(A,B)}{P(B)},\quad
P(X,Y)=P(Y\mid X)P(X),\quad P(X)=\sum_Y P(X,Y).$$

PMF cho biến rời rạc không âm và tổng bằng 1; PDF cho biến liên tục không âm và tích phân bằng 1. Xác suất trên khoảng liên tục là tích phân mật độ trên khoảng đó. Không coi giá trị mật độ Gaussian là xác suất của một điểm.

Bayes:

$$P(c\mid x)=\frac{P(x\mid c)P(c)}{P(x)}.$$

Prior $P(c)$ là xác suất lớp trước quan sát; likelihood $P(x\mid c)$ biểu diễn dữ liệu trong lớp; posterior $P(c\mid x)$ là xác suất lớp sau quan sát. Khi so sánh lớp cho cùng $x$, mẫu số $P(x)$ giống nhau nên:

$$\hat c=\arg\max_c P(c\mid x)=\arg\max_c P(x\mid c)P(c).$$

Với 0-1 loss, rủi ro khi chọn $c_j$ ở đầu vào $x$ là $1-P(c_j\mid x)$; vì vậy chọn posterior lớn nhất tối thiểu hóa rủi ro tại $x$ (L2 trang 20-21).

Generative models học phân phối chung $P(x,y)$; Naive Bayes là ví dụ chính. Discriminative models học $P(y\mid x)$ hoặc trực tiếp ánh xạ đầu vào sang lớp/biên quyết định. Danh sách ở slide có kNN, logistic, SVM, decision trees, random forests và ANNs; không cần ép mỗi mô hình đều trả ra posterior được hiệu chỉnh.

Maximum likelihood estimation theo giả định các ví dụ độc lập:

$$\hat\theta=\arg\max_\theta\prod_i p(x_i\mid\theta)
=\arg\max_\theta\sum_i\log p(x_i\mid\theta).$$

Gaussian một chiều:

$$p(x\mid\mu,\sigma^2)=\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\left[-\frac{(x-\mu)^2}{2\sigma^2}\right],$$
$$\hat\mu=\frac1N\sum_i x_i,\qquad
\hat\sigma^2=\frac1N\sum_i(x_i-\hat\mu)^2.$$

Mẫu số $N$ là quy ước MLE trong slide. Ví dụ điểm $3,6,5,9,8$ cho $\mu=6.2$, $\sigma\approx2.14$.

## 4. Chuẩn bị dữ liệu và thư viện

Nguồn: PREP trang 2-17; KNN trang 18-25; NB trang 36-40; SYL chương 2.

PREP chia việc xây dựng hệ thống thành define problem, prepare data, evaluate models, finalize model. Dữ liệu structured có cấu trúc/schema định sẵn; unstructured gồm văn bản và multimedia.

Sáu hoạt động được nêu: collection; cleaning (missing values, duplicates, outliers, errors); normalization; transformation/encoding; chia training-validation-testing; augmentation. Đây là danh sách hoạt động có thể dùng, **không phải bắt buộc xóa mọi outlier hoặc thêm dữ liệu tổng hợp**.

KNN nhấn mạnh xử lý các thang đo khác nhau. Ví dụ age và loan cho thấy giá trị tiền có thể chi phối khoảng cách nếu không chuẩn hóa.

$$x'=\frac{x-x_{\min}}{x_{\max}-x_{\min}}.$$

Quy tắc mã hóa trong slide: nhị phân thành 0/1; mức có thứ tự low/average/high thành 1/2/3; màu không có thứ tự thành one-hot. Không dùng ID mẫu làm predictor chỉ vì nó là số: slide KNN trang 25 phân biệt case ID, predictors và target.

Suy luận triển khai từ nguyên tắc unseen test: các giá trị min/max, vocabulary và tham số tiền xử lý học từ train; áp dụng cùng phép biến đổi cho validation/test. NB trang 37 minh họa `fit_transform(X_train)` và `transform(X_test)`. Nếu chia fold, việc học biểu diễn phải theo tập train của fold đó. Đây là cách cụ thể hóa yêu cầu không chỉnh theo test, không phải kết quả một thí nghiệm đã chạy.

NumPy: `ndarray`, dtype đồng nhất, shape/reshape, indexing/slicing, lọc theo điều kiện, phép toán ma trận, vectorization và broadcasting. Pandas: DataFrame, đọc/chọn dữ liệu, xử lý missing values, thay đổi kiểu và vẽ đồ thị. Matplotlib có trong đề cương và các đoạn code minh họa. scikit-learn và Keras xuất hiện trong code slide; việc được dùng thư viện cho bài giữa kỳ vẫn phải theo đề.

## 5. Đánh giá classification

Nguồn: EVAL trang 4-16, 24-27; NB trang 34-36.

EVAL dùng **hàng actual, cột predicted**:

| Actual / Predicted | Positive | Negative |
|---|---:|---:|
| Positive | TP | FN |
| Negative | FP | TN |

$$\mathrm{Accuracy}=\frac{TP+TN}{TP+FP+FN+TN},\quad
\mathrm{Error}=1-\mathrm{Accuracy}.$$
$$\mathrm{Precision}=\frac{TP}{TP+FP},\quad
\mathrm{Recall}=\mathrm{Sensitivity}=\mathrm{TPR}=\frac{TP}{TP+FN}.$$
$$\mathrm{Specificity}=\frac{TN}{TN+FP},\quad
\mathrm{FPR}=\frac{FP}{FP+TN}.$$
$$F_1=\frac{2PR}{P+R},\qquad
F_\beta=\frac{(1+\beta^2)PR}{\beta^2P+R}.$$

Phải xác định positive class, thứ tự nhãn, cách average và cách xử lý mẫu số bằng 0 khi thực hiện; slide chưa quy định mọi tình huống biên.

Ví dụ EVAL trang 10-11: TP=90, FN=210, FP=140, TN=9560. Accuracy=96.4% nhưng recall=30%, precision≈39.13%, specificity≈98.56%. Suy ra bằng công thức slide: $F_1=180/530\approx33.96\%$. Accuracy cao có thể che khả năng nhận ra lớp hiếm kém.

Macro: tính metric từng lớp rồi lấy trung bình. Micro: gộp TP/FP/FN các lớp rồi tính metric. NB trang 35 cho macro precision 0.7 và micro precision $100/120\approx0.83$; micro chịu ảnh hưởng lớn từ lớp phổ biến. Không lấy trung bình precision và recall để gọi là F1.

ROC vẽ TPR theo FPR qua nhiều ngưỡng phân loại; giảm ngưỡng làm nhiều mẫu được gán positive hơn. AUC là diện tích dưới đường ROC; slide mô tả 1 là hoàn hảo và khoảng 0.5 gần đường chéo. AUC và accuracy là các phép đo khác nhau. Không lấy predicted hard labels thay cho xác suất/score khi muốn khảo sát nhiều ngưỡng.

## 6. Chia dữ liệu và so sánh mô hình

Nguồn: EVAL trang 17-25; NB trang 36; PREP trang 6.

- Holdout: chia train và test độc lập; ví dụ 2/3-1/3 trong slide chỉ là minh họa.
- Repeated random holdout: lặp việc chia và lấy trung bình kết quả.
- k-fold: chia thành $k$ phần loại trừ nhau, lần lượt dùng một phần để đánh giá, phần còn lại học. Leave-one-out dùng một mẫu mỗi fold; stratified giữ gần phân bố lớp ban đầu.
- Bootstrap: lấy mẫu có hoàn lại; khoảng 63.2% mẫu gốc xuất hiện, khoảng 36.8% không được chọn. Slide trình bày .632 bootstrap kết hợp accuracy ngoài mẫu và trên train theo trọng số 0.632/0.368.

Training học mô hình, development/validation hỗ trợ lựa chọn, unseen test dùng đánh giá cuối. NB trang 36 nói tránh tuning to the test set. So sánh mô hình trên cùng cách chia giúp kết quả có ý nghĩa; không dùng những tập test khác nhau rồi kết luận chỉ từ chênh lệch metric.

EVAL trang 19-23 giới thiệu kiểm định t cho chênh lệch error qua 10 fold, null hypothesis hai mô hình có cùng mean error, $k-1$ bậc tự do. Trang 21 dùng chênh lệch theo cùng fold:

$$d_i=\mathrm{err}(M_1)_i-\mathrm{err}(M_2)_i,\quad
\bar d=\frac1k\sum_i d_i,\quad
t=\frac{\bar d}{\sqrt{v/k}}.$$

Slide viết $v=(1/k)\sum_i(d_i-\bar d)^2$. Có điểm cần làm rõ về quy ước phương sai và critical value, ghi tại `04_SOURCE_CAVEATS.md`; chưa coi đây là công thức cài đặt đã được xác nhận cho bài thi. Không kết luận “hai mô hình bằng nhau” chỉ vì chưa bác bỏ null hypothesis.

Chọn mô hình còn xét tốc độ train/predict, robustness, scalability và interpretability (EVAL trang 25), không chỉ metric tốt nhất.

## 7. Đánh giá regression

Nguồn: EVAL trang 29-37.

$$\mathrm{MSE}=\frac1N\sum_i(y_i-\hat y_i)^2,\qquad
\mathrm{RMSE}=\sqrt{\mathrm{MSE}},\qquad
\mathrm{MAE}=\frac1N\sum_i|y_i-\hat y_i|.$$
$$SS_{\mathrm{res}}=\sum_i(y_i-\hat y_i)^2,\qquad
SS_{\mathrm{tot}}=\sum_i(y_i-\bar y)^2,\qquad
R^2=1-\frac{SS_{\mathrm{res}}}{SS_{\mathrm{tot}}}.$$

MSE có đơn vị bình phương; RMSE và MAE có đơn vị của đích. $R^2=1$ là khớp hoàn hảo; 0 tương ứng mức sai số bằng việc dùng trung bình của tập đang đánh giá; âm nghĩa là sai số lớn hơn mức đó. Không dùng $R^2$ khi target không biến thiên mà không xử lý mẫu số 0. Hệ số này không tự chứng minh mô hình đúng hoặc quan hệ nhân quả.

Phân biệt **MSE đánh giá** với loss $\mathrm{MSE}/2$ trong bài linear regression: hai giá trị khác hệ số, dù có cùng điểm cực tiểu.
