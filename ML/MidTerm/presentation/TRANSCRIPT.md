# Transcript thuyết trình — Midterm ML

**Đề tài:** Hồi quy & Phân loại — Câu 1 (Gradient Descent tự cài đặt) và Câu 2 (phân loại trên OpenML credit-g)
**Thời lượng thiết kế:** 10 phút cho cả phần nói, chuyển slide và Q&A. Tổng lời thoại 1356 từ, đọc ở nhịp ~150 từ/phút ⇒ khoảng 8:53.
**Người trình bày:** Tiến (Câu 1) · Thành (Câu 2: dữ liệu và mô hình) · Tâm (kết quả, overfitting, kết luận)

## Phân chia và mốc thời gian

| Người | Slide | Số slide | Thời lượng | Số từ |
|---|---|---|---|---|
| Tiến | 1, 2, 3, 4, 5, 6, 7 | 7 | 4:13 | 643 |
| Thành | 8, 9, 10, 11 | 4 | 2:33 | 389 |
| Tâm | 12, 13, 14 | 3 | 2:07 | 324 |

Tổng lời thoại 8:53; phần còn lại để chuyển slide, nhấn mạnh và Q&A.

## Mẹo giữ nhịp 10 phút

- Mốc kiểm tra: hết slide 4 (xong lý thuyết câu 1) nên ở **2:08**, hết slide 7 ở **4:12**, hết slide 11 ở **6:45**. Trễ hơn 30 giây thì bỏ phần kiểm chứng gradient ở slide 4.
- Không đọc công thức thành lời từng ký hiệu — nói ý nghĩa, rồi chỉ tay vào hình.
- Câu chốt của mỗi phần nói chậm hơn 20%: đó là phần giảng viên ghi lại.
- Nếu bị hỏi ngoài phạm vi, người đang nói nhận câu hỏi và chuyển cho người phụ trách phần đó.

## Lời thoại theo slide

### Slide 1 — Trang bìa  
**Tiến** · bắt đầu 0:00 · ~24s

> Kính thưa thầy và các bạn. Nhóm em gồm ba thành viên xin trình bày báo cáo giữa kỳ môn Introduction to Machine Learning. Bài gồm hai câu: câu một tự cài đặt hồi quy tuyến tính và logistic bằng Gradient Descent; câu hai so sánh các bộ phân loại trên bộ credit-g của OpenML. Phần trình bày khoảng mười phút.

### Slide 2 — Ba phần, ba người trình bày  
**Tiến** · bắt đầu 0:24 · ~28s

> Bài chia ba phần. Em trình bày câu một: tự cài đặt hai mô hình hồi quy, dẫn xuất gradient và đánh giá. Bạn Thành trình bày câu hai: dữ liệu credit-g, quy trình chống rò rỉ và so sánh mười bốn mô hình cùng baseline. Bạn Tâm trình bày overfitting và kết luận. Câu hỏi xuyên suốt: mô hình học được gì, và làm sao biết nó tổng quát hóa?

### Slide 3 — Mô hình và hàm mất mát  
**Tiến** · bắt đầu 0:52 · ~36s

> Hồi quy tuyến tính dự đoán một số thực bằng tổng có trọng số của các đặc trưng cộng hệ số chặn. Vì đầu ra là số thực nên đây là bài toán hồi quy. Hàm mất mát là trung bình bình phương sai số, chia đôi. Hệ số một phần hai chỉ để khi đạo hàm, số hai triệt tiêu, không đổi nghiệm tối ưu. Chia cho n giúp mất mát là trung bình, so sánh được giữa các cỡ mẫu. Còn bình phương khiến sai số lớn bị phạt nặng.

### Slide 4 — Dẫn xuất gradient và vòng lặp Gradient Descent  
**Tiến** · bắt đầu 1:28 · ~41s

> Đạo hàm theo quy tắc chuỗi: gọi e là phần dư, đạo hàm của e theo trọng số chính là giá trị đặc trưng. Vậy gradient theo trọng số là trung bình của phần dư nhân đặc trưng, gradient theo hệ số chặn là trung bình phần dư. Viết dạng ma trận được công thức ở giữa. Thực nghiệm khởi tạo bằng không, tốc độ học không phẩy ba, dừng khi chuẩn gradient nhỏ hơn mười mũ trừ tám, sau một nghìn một trăm bảy mươi lăm vòng. Nhóm kiểm chứng lại gradient bằng sai phân trung tâm, dung sai mười mũ trừ sáu.

### Slide 5 — Xác suất, cross-entropy và gradient  
**Tiến** · bắt đầu 2:09 · ~41s

> Hồi quy logistic đưa cùng một điểm tuyến tính qua sigmoid để ra xác suất trong khoảng không đến một. Logit của xác suất là hàm tuyến tính nên biên vẫn là siêu phẳng. Mất mát là cross-entropy, tức âm log hợp lý Bernoulli, phạt rất nặng dự đoán tự tin mà sai. Khi đạo hàm, đạo hàm sigmoid là p nhân một trừ p, triệt tiêu mẫu số của cross-entropy, nên gradient chỉ còn p trừ y, rất gọn. Nhóm dùng tốc độ học không phẩy năm, tối đa năm nghìn vòng, và vòng lặp chạm ngân sách trước khi đạt dung sai.

### Slide 6 — Hồi quy tuyến tính: học đúng quan hệ sinh dữ liệu  
**Tiến** · bắt đầu 2:50 · ~42s

> Đây là kết quả chạy thật. Mất mát giảm từ ba mươi phẩy chín xuống không phẩy một hai sáu sau một nghìn một trăm bảy mươi lăm vòng, đơn điệu nên không phân kỳ. Trên một trăm hai mươi mẫu test, các điểm bám sát đường chéo. RMSE không phẩy năm một, đúng bằng độ lệch chuẩn của nhiễu, R bình phương không phẩy chín chín bốn bảy. Trọng số học được rất gần giá trị thật ba, trừ hai, một phẩy năm. Nhưng đây là dữ liệu tổng hợp tuyến tính, nên điểm cao là kỳ vọng, không phải bằng chứng cho dữ liệu thực.

### Slide 7 — Hồi quy logistic: biên hợp lý, nhưng còn 30 ca sai  
**Tiến** · bắt đầu 3:32 · ~41s

> Với logistic, nhãn sinh ngẫu nhiên nên hai lớp chồng lấn. Cross-entropy giảm từ không phẩy sáu chín ba một, đúng bằng log hai của mô hình đoán ngẫu nhiên, xuống không phẩy bốn năm hai. Trên tập test, mô hình đúng một trăm ba mươi trên một trăm sáu mươi, tức tám mươi mốt phẩy hai lăm phần trăm, F1 lớp dương không phẩy tám năm một, AUC không phẩy tám năm bảy. Các vòng tròn là mẫu phân loại sai, tập trung đúng ở vùng chồng lấn. Phần câu một đến đây là hết, em mời bạn Thành trình bày câu hai.

### Slide 8 — OpenML credit-g: 1000 hồ sơ, 20 biến, lệch lớp  
**Thành** · bắt đầu 4:13 · ~39s

> Dữ liệu là credit-g, mã 31 phiên bản một trên OpenML: một nghìn hồ sơ, hai mươi biến, trong đó bảy biến số và mười ba biến phân loại. Nhãn gồm bảy trăm good và ba trăm bad, nên đây là bài toán mất cân bằng. Một mô hình luôn đoán good đã đạt bảy mươi phần trăm accuracy mà không phát hiện hồ sơ xấu nào, vì vậy nhóm không dùng accuracy làm tiêu chí chính. Kiểm tra dữ liệu sạch: không ô thiếu, không dòng trùng, không giá trị lạ, nên giữ nguyên một nghìn hồ sơ.

### Slide 9 — Chống rò rỉ dữ liệu bằng thiết kế, không bằng lời hứa  
**Thành** · bắt đầu 4:52 · ~35s

> Điểm nhóm muốn nhấn mạnh là quy trình. Tập test tách ngay từ đầu và chỉ dùng một lần, sau khi mọi lựa chọn xong. Trong tám trăm hồ sơ development, nhóm chạy năm fold phân tầng, và chuẩn hóa nằm trong pipeline nên mỗi fold chỉ học min–max từ train của chính nó. Nếu chuẩn hóa trước rồi mới chia fold thì thông tin validation đã rò rỉ và điểm sẽ đẹp giả tạo. Tiêu chí chọn là macro F1 vì cho hai lớp trọng số ngang nhau.

### Slide 10 — 14 mô hình và một baseline, chọn bằng cross-validation  
**Thành** · bắt đầu 5:27 · ~39s

> Nhóm so sánh mười bốn mô hình cùng một baseline trên cùng bộ fold. Ba kernel SVM là ba biến thể của một họ, không phải ba họ thuật toán. MLP dẫn đầu với macro F1 không phẩy sáu chín sáu, Bernoulli NB bám sát không phẩy sáu chín bốn, polynomial SVM không phẩy sáu tám sáu. Nhưng độ lệch chuẩn giữa các fold khoảng không phẩy không sáu, lớn hơn khoảng cách hai mô hình đầu, nên nhóm không tuyên bố MLP vượt trội. Điểm CV đã dùng để chọn tham số nên không phải đánh giá độc lập.

### Slide 11 — Trên 200 hồ sơ chưa từng thấy, khoảng cách rất hẹp  
**Thành** · bắt đầu 6:06 · ~40s

> Đây là kết quả trên hai trăm hồ sơ test chưa từng dùng để chọn mô hình. MLP có accuracy không phẩy bảy chín, macro F1 không phẩy bảy ba không, AUC không phẩy tám một ba. Đáng chú ý: hồi quy logistic tự cài đặt ở câu một đạt macro F1 không phẩy bảy ba không một, gần như bằng MLP. Trong bài toán nhỏ này, mô hình phức tạp hơn không mang lại lợi ích rõ rệt. Mọi mô hình học đều vượt baseline, nhưng chênh lệch chỉ vài phần nghìn. Em mời bạn Tâm trình bày phần overfitting.

### Slide 12 — Một con số accuracy đẹp có thể che mất lỗi quan trọng  
**Tâm** · bắt đầu 6:46 · ~43s

> Bức tranh này là bài học chính của câu hai. MLP đúng một trăm năm mươi tám trên hai trăm, nghe rất tốt. Nhưng trong sáu mươi hồ sơ thực sự xấu, mô hình bỏ sót hai mươi tám, tức recall lớp bad chỉ không phẩy năm ba ba. Đây là cái bẫy của dữ liệu mất cân bằng: lớp đa số kéo accuracy lên trong khi lớp cần phát hiện bị bỏ qua. Nếu là bài toán tín dụng thật, bỏ sót hồ sơ xấu thường tốn kém hơn báo nhầm. Nhóm không hạ ngưỡng sau khi xem test, vì làm vậy là dùng test để tinh chỉnh.

### Slide 13 — Bằng chứng: cây càng sâu, khoảng cách càng lớn  
**Tâm** · bắt đầu 7:29 · ~44s

> Biểu đồ bên trái tách riêng ảnh hưởng của độ sâu cây: độ sâu tăng thì điểm train leo lên một, nhưng validation chỉ tăng đến khoảng độ sâu sáu rồi giảm. Cây không giới hạn đạt một phẩy không trên train nhưng chỉ không phẩy sáu một bốn trên validation. Giới hạn độ sâu sáu và tối thiểu năm mẫu mỗi lá, khoảng cách thu hẹp từ không phẩy ba tám sáu xuống không phẩy một hai một, điểm validation tăng. Nhưng random forest sau khi chọn tham số vẫn còn khoảng cách không phẩy ba hai bốn. Ensemble giảm phương sai nhưng không miễn nhiễm với việc ghi nhớ dữ liệu.

### Slide 14 — Điều nhóm làm được, điều còn hạn chế  
**Tâm** · bắt đầu 8:13 · ~40s

> Tóm lại, câu một cho thấy hai mô hình tự cài đặt học đúng: gradient khớp kiểm tra sai phân, sai số xấp xỉ mức nhiễu. Câu hai cho thấy trên dữ liệu nhỏ và mất cân bằng, mô hình phức tạp nhất không vượt trội rõ rệt, và accuracy có thể che mất lỗi ở lớp thiểu số. Hạn chế: một bộ dữ liệu, một lần chia test, lưới tham số nhỏ; logistic và MLP đều chạm ngân sách vòng lặp nên chưa hội tụ; không có kiểm định thống kê. Em xin kết thúc và cảm ơn thầy, các bạn.

## Câu hỏi dự kiến và người trả lời

| Câu hỏi | Người trả lời | Ý chính |
|---|---|---|
| Vì sao dùng ½ trong hàm mất mát? | Tiến | Triệt tiêu hệ số 2 khi đạo hàm; nghiệm tối ưu không đổi. |
| Vì sao chuẩn hóa phải nằm trong fold? | Thành | Nếu fit trước khi chia fold, min/max của validation đã rò rỉ vào train. |
| Vì sao chọn macro F1 thay vì accuracy? | Thành | Hai lớp trọng số ngang nhau; accuracy bị lớp good 70% chi phối. |
| MLP có thực sự tốt hơn logistic không? | Tâm | Không kết luận được: chênh 0.0004, nhỏ hơn SD giữa các fold ±0.064. |
| Sao không hạ ngưỡng để tăng recall lớp bad? | Tâm | Có thể, nhưng phải chọn ngưỡng trên validation; hạ sau khi xem test là dùng test để tinh chỉnh. |
| Gradient đúng chưa? | Tiến | Đã kiểm chứng bằng sai phân trung tâm, dung sai 1e−6, cả hai mô hình. |
| Vì sao chỉ 14 mô hình mà không phải deep learning? | Thành | credit-g là bảng nhỏ 1000 dòng, không có biểu diễn ảnh/chuỗi; CNN/RNN sẽ áp một biểu diễn tùy ý. |

## Ghi chú trung thực học thuật

- Mọi con số trong slide lấy từ `results/` và được script `presentation/src/make_deck_figures.py` kiểm tra lại trước khi vẽ.
- Không có kết quả nào được chạy riêng cho slide.
- Bài làm có sử dụng hỗ trợ AI trong soạn thảo và kiểm tra; nhóm đã rà lại toàn bộ.
