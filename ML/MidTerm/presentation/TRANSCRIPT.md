# Transcript thuyết trình — Midterm ML

**Đề tài:** Hồi quy & Phân loại — Câu 1 (Gradient Descent tự cài đặt) và Câu 2 (phân loại trên OpenML credit-g)  
**Thời lượng:** tổng lời thoại 1329 từ, đọc ở nhịp ~150 từ/phút ≈ **8:52**; phần còn lại của slot 10 phút dành cho chuyển slide và hỏi đáp.  
**Người trình bày:** Tiến (Câu 1) · Thành (Câu 2: dữ liệu, quy trình, chọn mô hình) · Tâm (đọc kết quả, overfitting, kết luận)

> File này được sinh từ `src/talk_content.json` bằng `python3 src/build_talk.py`; speaker notes trong `midterm_presentation.pptx` dùng cùng nguồn.
> Muốn sửa lời thoại thì sửa file JSON rồi dựng lại, đừng sửa trực tiếp file này. Số liệu đã đối chiếu với `../results/*.json`.

## Phân chia và mốc thời gian

| Người | Slide | Bắt đầu | Thời lượng | Số từ |
|---|---|---|---|---|
| Tiến | 1–7 | 0:00 | 4:14 | 636 |
| Thành | 8–11 | 4:14 | 2:34 | 384 |
| Tâm | 12–14 | 6:48 | 2:04 | 309 |

## Mẹo giữ nhịp

- Mốc kiểm tra: bắt đầu slide 5 ở **2:16**, slide 8 ở **4:14**, slide 12 ở **6:48**. Trễ hơn 30 giây thì bỏ câu kiểm chứng gradient ở slide 4 và câu về kNN ở slide 10.
- Không đọc công thức từng ký hiệu: nói ý nghĩa rồi chỉ vào slide.
- Nói chậm lại ở câu chốt của mỗi slide (dòng **Chốt** bên dưới).

## Lời thoại theo slide

### Slide 1 — Hồi quy & Phân loại
**Tiến** · bắt đầu 0:00 · ~22s

> Kính thưa thầy và các bạn. Nhóm em xin trình bày báo cáo giữa kỳ môn Introduction to Machine Learning, đề tài Hồi quy và Phân loại. Câu một tự cài đặt hồi quy tuyến tính và logistic bằng Gradient Descent. Câu hai so sánh 14 bộ phân loại trên bộ dữ liệu credit-g của OpenML.

**Chốt:** Hai câu của đề là hai dạng học có giám sát: **hồi quy** (đích là số thực) và **phân loại** (đích là nhãn rời rạc).

### Slide 2 — Ba phần, ba người trình bày
**Tiến** · bắt đầu 0:22 · ~27s

> Bài gồm ba phần. Em trình bày câu một: mô hình, hàm mất mát, gradient và kết quả. Bạn Thành trình bày dữ liệu, quy trình và cách chọn mô hình ở câu hai. Bạn Tâm trình bày cách đọc kết quả, overfitting và kết luận. Câu hỏi xuyên suốt là: mô hình học được gì, và làm sao biết nó tổng quát hóa sang dữ liệu mới?

**Chốt:** Câu hỏi xuyên suốt là **tổng quát hóa**: điểm trên dữ liệu chưa từng thấy mới là thước đo thật.

### Slide 3 — Mô hình và hàm mất mát
**Tiến** · bắt đầu 0:50 · ~46s

> Hồi quy tuyến tính dự đoán một số thực bằng tổng có trọng số của các đặc trưng cộng hệ số chặn: một đặc trưng là đường thẳng, nhiều đặc trưng là siêu phẳng. Nhóm học w và b bằng cách cực tiểu trung bình bình phương sai số, nhân một phần hai. Bình phương phạt nặng sai số lớn, nên mô hình nhạy với ngoại lai. Chia cho n để mất mát không phụ thuộc cỡ mẫu. Hệ số một phần hai chỉ giúp đạo hàm gọn, không đổi điểm cực tiểu. Dữ liệu là 600 mẫu tổng hợp từ một quan hệ tuyến tính đã biết, nên kiểm tra được kết quả.

**Chốt:** Dự đoán số thực bằng tổ hợp tuyến tính $\hat y=w^\top x+b$, học bằng cách cực tiểu $\text{MSE}/2$.

### Slide 4 — Dẫn xuất gradient và vòng lặp Gradient Descent
**Tiến** · bắt đầu 1:35 · ~41s

> Theo quy tắc chuỗi, gọi e là phần dư. Gradient theo w j là trung bình của e nhân x j, theo b là trung bình của e; dạng ma trận là một phần n nhân X chuyển vị nhân phần dư. Gradient Descent đi ngược hướng gradient một bước eta, cập nhật w và b cùng lúc. Nhóm khởi tạo bằng 0, eta bằng 0.3, dừng khi chuẩn gradient dưới 10 mũ trừ 8, chỉ dựa trên dữ liệu train. Mô hình dừng sau 1175 vòng. Gradient được kiểm chứng bằng sai phân trung tâm, sai khác dưới 10 mũ trừ 6.

**Chốt:** Gradient chỉ hướng loss tăng nhanh nhất. Gradient Descent đi **ngược** hướng đó từng bước nhỏ $\eta$.

### Slide 5 — Xác suất, cross-entropy và gradient
**Tiến** · bắt đầu 2:16 · ~42s

> Logistic đưa cùng điểm tuyến tính z qua hàm sigmoid để ra xác suất từ 0 đến 1. Log odds vẫn tuyến tính, nên biên quyết định tại p bằng 0.5 là một siêu phẳng. Hàm mất mát là cross-entropy, tức âm log-likelihood Bernoulli, phạt rất nặng dự đoán tự tin mà sai. Đạo hàm sigmoid là p nhân một trừ p, triệt tiêu mẫu số của cross-entropy, nên gradient chỉ còn p trừ y, cùng dạng với hồi quy tuyến tính. Nhóm dùng eta 0.5, tối đa 5000 vòng; mô hình chạm giới hạn trước khi đạt dung sai, nên chưa hội tụ chặt.

**Chốt:** Logistic là tuyến tính cộng sigmoid để ra xác suất. Học bằng cross-entropy, và gradient vẫn gọn: $(p-y)\,x$.

### Slide 6 — Hồi quy tuyến tính: học đúng quan hệ sinh dữ liệu
**Tiến** · bắt đầu 2:58 · ~40s

> Kết quả hồi quy tuyến tính: mất mát giảm đơn điệu từ 30.9 xuống 0.126, tức tốc độ học phù hợp, không phân kỳ. Trên 120 mẫu test, các điểm bám sát đường chéo. RMSE 0.51, xấp xỉ độ lệch chuẩn của nhiễu là 0.5, nghĩa là phần sai còn lại gần như chỉ là nhiễu. R bình phương 0.995. Trọng số học được 2.99, trừ 2.01 và 1.49, rất gần giá trị thật 3, trừ 2 và 1.5. Nhưng dữ liệu sinh tuyến tính, nên đây chỉ chứng minh cài đặt đúng, chưa nói gì về dữ liệu thực.

**Chốt:** Kết quả khớp với "đáp án" đã biết, nên cài đặt là đúng.

### Slide 7 — Hồi quy logistic: biên hợp lý, nhưng còn 30 ca sai
**Tiến** · bắt đầu 3:38 · ~36s

> Với logistic, hai lớp chồng lấn nên không thể tách hoàn hảo. Cross-entropy bắt đầu ở 0.693, đúng bằng log 2 của mô hình đoán 0.5 cho mọi mẫu, rồi giảm xuống 0.45. Trên 160 mẫu test: accuracy 81.25 phần trăm, F1 lớp dương 0.85, AUC 0.86. Accuracy và F1 dùng ngưỡng 0.5, còn AUC tóm tắt mọi ngưỡng. Các vòng tròn là 30 ca sai, nằm ở vùng chồng lấn quanh biên: đó là giới hạn của dữ liệu, không phải lỗi tối ưu. Em xin mời bạn Thành.

**Chốt:** Logistic học được một biên hợp lý. 30 lỗi còn lại nằm ở vùng hai lớp chồng lấn.

### Slide 8 — OpenML credit-g: 1000 hồ sơ, 20 biến, lệch lớp
**Thành** · bắt đầu 4:14 · ~41s

> Câu hai dùng bộ credit-g, mã 31 trên OpenML: 1000 hồ sơ vay, 20 biến, gồm 7 biến số và 13 biến phân loại. Lớp dương là bad, lớp cần phát hiện. Tỷ lệ 70 trên 30 nên dữ liệu mất cân bằng: luôn đoán good đã đạt 70 phần trăm accuracy mà không bắt được hồ sơ xấu nào. Biểu đồ phải cho thấy số tiền vay lệch phải và hai lớp chồng lấn mạnh. Dữ liệu không có ô thiếu, dòng trùng hay giá trị lạ, nên giữ đủ 1000 hồ sơ; sau min–max và one-hot có 61 đặc trưng.

**Chốt:** credit-g nhỏ, nhiều biến phân loại và lệch lớp 70/30, nên accuracy không đủ tin. Cần chỉ số tính theo từng lớp.

### Slide 9 — Chống rò rỉ dữ liệu bằng thiết kế, không bằng lời hứa
**Thành** · bắt đầu 4:55 · ~37s

> Điểm nhóm chú trọng nhất là chống rò rỉ dữ liệu. Một, tách 200 hồ sơ test phân tầng ngay từ đầu. Hai, chuẩn hóa và one-hot nằm trong pipeline, nên mỗi fold chỉ học min, max và danh mục từ phần train của fold đó. Nếu chuẩn hóa trước rồi mới chia, thông tin validation đã lọt vào train và điểm sẽ đẹp giả tạo. Ba, mọi mô hình dùng chung năm fold phân tầng, chọn theo macro F1. Bốn, chốt xong mọi lựa chọn mới chạy test, đúng một lần.

**Chốt:** Mọi thứ học từ dữ liệu, kể cả min/max và danh mục one-hot, chỉ được học từ **phần train hiện tại**.

### Slide 10 — 14 mô hình và một baseline, chọn bằng cross-validation
**Thành** · bắt đầu 5:32 · ~40s

> Nhóm so sánh 14 mô hình và một baseline trên cùng bộ fold, từ mô hình tuyến tính, kNN, Naive Bayes, cây, SVM, MLP đến ensemble; ba kernel SVM chỉ là ba biến thể của một họ. MLP dẫn đầu với macro F1 0.696, Bernoulli NB 0.694. Nhưng độ lệch chuẩn giữa các fold khoảng 0.06, lớn hơn nhiều khoảng cách 0.002, nên nhóm không kết luận MLP vượt trội. kNN chọn k bằng 1 và khớp hoàn hảo trên train, một dấu hiệu overfitting. Điểm CV đã dùng để chọn tham số, nên không phải đánh giá độc lập.

**Chốt:** Chọn mô hình bằng điểm CV trung bình. Khi khoảng cách nhỏ hơn độ dao động giữa các fold, chưa thể kết luận mô hình nào hơn.

### Slide 11 — Trên 200 hồ sơ chưa từng thấy, khoảng cách rất hẹp
**Thành** · bắt đầu 6:12 · ~36s

> Đánh giá độc lập là 200 hồ sơ test. MLP đạt accuracy 0.79, macro F1 0.73, AUC 0.81. Đáng chú ý, logistic tự cài đặt từ câu một cũng đạt macro F1 0.730, gần như bằng MLP: trên một bảng dữ liệu nhỏ, mô hình phức tạp hơn không mang lại lợi ích rõ ràng. Cả 14 mô hình đều vượt baseline về macro F1, nhưng nhóm dẫn đầu chỉ chênh nhau vài phần nghìn, nên không nên đọc bảng này như bảng xếp hạng. Em xin mời bạn Tâm.

**Chốt:** Trên test, mô hình đơn giản (logistic tự cài) ngang với MLP. Phức tạp hơn không đồng nghĩa với tốt hơn.

### Slide 12 — Một con số accuracy đẹp có thể che mất lỗi quan trọng
**Tâm** · bắt đầu 6:48 · ~39s

> Đây là bài học chính của câu hai. Ma trận nhầm lẫn có hàng là nhãn thật, cột là dự đoán. MLP đúng 158 trên 200, nhưng trong 60 hồ sơ xấu, mô hình bỏ sót 28, nên recall lớp bad chỉ 0.533. Lớp đa số đã kéo accuracy lên. Gaussian NB thì ngược lại: recall bad 0.65 nhưng precision chỉ 0.51. Chọn bên nào là quyết định nghiệp vụ, tùy chi phí bỏ sót so với báo nhầm. Muốn hạ ngưỡng thì phải chọn trên validation; hạ sau khi xem test là dùng test để tinh chỉnh.

**Chốt:** Accuracy 0.79 che mất việc bỏ sót gần nửa số hồ sơ xấu. Luôn đọc chỉ số của từng lớp.

### Slide 13 — Bằng chứng: cây càng sâu, khoảng cách càng lớn
**Tâm** · bắt đầu 7:27 · ~45s

> Overfitting là khi mô hình học thuộc cả nhiễu của train, nên gặp dữ liệu mới thì kém; nhóm đo nó bằng khoảng cách train trừ validation. Ở biểu đồ trái, tăng độ sâu thì điểm train leo lên 1, còn validation chỉ tăng đến độ sâu khoảng 6 rồi giảm. Cây không giới hạn đạt 1.00 trên train nhưng 0.614 trên validation. Giới hạn độ sâu 6 và tối thiểu 5 mẫu mỗi lá, khoảng cách giảm từ 0.386 xuống 0.121. Nhưng random forest vẫn còn 0.324: ensemble giảm phương sai, không tự hết overfitting. Biện pháp chung là giới hạn độ phức tạp, chọn bằng validation và giữ test riêng.

**Chốt:** Overfitting là khoảng cách train–validation lớn. Cách chữa: giới hạn độ phức tạp và chọn tham số bằng validation.

### Slide 14 — Điều nhóm làm được, điều còn hạn chế
**Tâm** · bắt đầu 8:12 · ~40s

> Tóm lại, câu một cho thấy hai mô hình tự cài đặt học đúng: gradient khớp kiểm tra sai phân, sai số xấp xỉ mức nhiễu. Câu hai cho thấy trên dữ liệu nhỏ và mất cân bằng, mô hình phức tạp nhất không vượt trội rõ rệt, và accuracy có thể che lỗi ở lớp thiểu số. Hạn chế: một bộ dữ liệu, một lần chia test, lưới tham số nhỏ; logistic và MLP chưa hội tụ hoàn toàn; và chưa có kiểm định thống kê. Nhóm em xin cảm ơn thầy và các bạn đã lắng nghe.

**Chốt:** Ba điều cần nhớ: cài đặt đúng đã được kiểm chứng; quy trình chống rò rỉ là điều kiện để so sánh đáng tin; accuracy có thể đánh lừa trên dữ liệu lệch lớp.

## Câu hỏi dự kiến và người trả lời

| Câu hỏi | Người trả lời | Ý chính |
|---|---|---|
| Vì sao dùng ½ trong hàm mất mát? | Tiến | Triệt tiêu hệ số 2 khi đạo hàm; điểm cực tiểu không đổi. |
| Gradient đúng chưa? | Tiến | Đã so với sai phân trung tâm, sai khác < 1e−6, cho cả hai mô hình. |
| Vì sao logistic dùng cross-entropy mà không dùng MSE? | Tiến | Cross-entropy là âm log-likelihood Bernoulli; gradient gọn (p − y)x và phạt nặng dự đoán tự tin mà sai. |
| Vì sao chuẩn hóa phải nằm trong fold? | Thành | Nếu fit trước khi chia, min/max của validation đã rò rỉ vào train. |
| Vì sao chọn macro F1 thay vì accuracy? | Thành | Hai lớp trọng số ngang nhau; accuracy bị lớp good 70% chi phối. |
| MLP có thực sự tốt hơn logistic không? | Tâm | Không kết luận được: chênh 0.0004 trên test, nhỏ hơn SD giữa các fold ±0.064; chưa làm kiểm định t. |
| Sao không hạ ngưỡng để tăng recall lớp bad? | Tâm | Có thể, nhưng ngưỡng phải chọn trên validation; hạ sau khi xem test là dùng test để tinh chỉnh. |
| Vì sao không dùng deep learning (CNN/RNN)? | Thành | credit-g là bảng nhỏ 1000 dòng, không có cấu trúc ảnh hay chuỗi để CNN/RNN khai thác. |

## Ghi chú trung thực học thuật

- Mọi con số trong lời thoại lấy từ `results/`; không có kết quả nào được chạy riêng cho phần trình bày.
- Bài làm có sử dụng hỗ trợ AI trong soạn thảo và kiểm tra; nhóm đã rà lại toàn bộ.
