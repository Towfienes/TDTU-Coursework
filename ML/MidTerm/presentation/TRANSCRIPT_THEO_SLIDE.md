# Nói theo slide — bản ngắn

Mỗi slide có 2–5 bước. Mỗi bước bắt đầu bằng **vùng cần chỉ trên slide**, sau đó là câu để nói. Tổng 1026 từ, đọc ở ~150 từ/phút ≈ **6:50**.

Cách dùng: nhìn slide, chỉ vào vùng in đậm, nói câu bên cạnh. Bản đầy đủ có giải thích "vì sao" nằm ở `TRANSCRIPT.md`.
Lời thoại không gắn tên người nói; khi cả nhóm chia phần, thêm câu chuyển lời ở slide 7 và 11.

> File này được sinh từ `src/talk_content.json` (trường `guide`) bằng `python3 src/build_talk.py`.

## 1. Hồi quy & Phân loại
Bắt đầu 0:00 · ~16s

1. **Tiêu đề** — Kính thưa thầy và các bạn, nhóm em trình bày đề tài Hồi quy và Phân loại.
2. **Dòng phụ** — Câu một tự cài Gradient Descent cho hồi quy tuyến tính và logistic; câu hai so sánh 14 bộ phân loại trên OpenML.

## 2. Ba phần, ba người trình bày
Bắt đầu 0:16 · ~25s

1. **Mục 01** — Câu một: tự cài hai mô hình hồi quy, từ hàm mất mát, gradient đến kết quả.
2. **Mục 02** — Câu hai: dữ liệu credit-g, quy trình chống rò rỉ và cách chọn mô hình.
3. **Mục 03** — Phần cuối: đọc kết quả, overfitting và kết luận.
4. **Câu hỏi dưới cùng** — Cả bài trả lời một câu: mô hình học được gì, và có tổng quát hóa sang dữ liệu mới không?

## 3. Mô hình và hàm mất mát
Bắt đầu 0:41 · ~35s

1. **Trái · dự đoán** — Công thức trên: ŷ bằng tổng có trọng số của đặc trưng cộng b. Đầu ra là số thực nên đây là hồi quy.
2. **Trái · mất mát** — Bên dưới là hàm mất mát: trung bình bình phương sai số, nhân một phần hai.
3. **Phải · giải thích** — Bên phải giải thích từng chi tiết: bình phương phạt nặng sai số lớn, chia n để lấy trung bình, ½ chỉ cho đạo hàm gọn.
4. **Dòng dữ liệu** — Dòng cuối: 600 mẫu tổng hợp sinh từ công thức đã biết, nên kiểm tra được mô hình học đúng hay sai.

## 4. Dẫn xuất gradient và vòng lặp Gradient Descent
Bắt đầu 1:16 · ~35s

1. **Trái · đạo hàm** — Gọi e là phần dư. Theo quy tắc chuỗi, gradient là trung bình e nhân x, viết gọn thành một phần n Xᵀ nhân phần dư.
2. **Trái · cập nhật** — Dòng cập nhật: đi ngược gradient một bước η, cập nhật w và b cùng lúc.
3. **Phải · thông số** — Bên phải là thông số chạy: khởi tạo 0, η bằng 0.3, dừng khi gradient nhỏ hơn 10⁻⁸, hội tụ sau 1175 vòng, gradient đã kiểm bằng sai phân.
4. **Ghi chú dưới** — Ghi chú dưới: mỗi vòng dùng cả tập train, và không dùng test để quyết định dừng.

## 5. Xác suất, cross-entropy và gradient
Bắt đầu 1:51 · ~36s

1. **Trái · mô hình** — Điểm z tuyến tính đi qua sigmoid thành xác suất p. Log-odds vẫn tuyến tính nên biên quyết định là đường thẳng.
2. **Trái · mất mát** — Hàm mất mát là cross-entropy: dự đoán càng tự tin mà sai thì phạt càng nặng.
3. **Phải · gradient** — Bên phải: đạo hàm sigmoid triệt tiêu mẫu số, gradient chỉ còn p trừ y, nên công thức cập nhật giống hồi quy tuyến tính.
4. **Ba dòng dưới** — Ba dòng dưới: η bằng 0.5, tối đa 5000 vòng, chạm giới hạn trước khi hội tụ chặt; tính toán được viết ổn định số học.

## 6. Hồi quy tuyến tính: học đúng quan hệ sinh dữ liệu
Bắt đầu 2:27 · ~28s

1. **Trái · đường loss** — Biểu đồ trái: mất mát giảm đều từ 30.9 xuống 0.126, không dao động, nên tốc độ học hợp lý.
2. **Phải · dự đoán vs thật** — Biểu đồ phải: trên 120 mẫu test, các điểm nằm sát đường chéo, tức dự đoán gần đúng giá trị thật.
3. **Ba số dưới** — Ba số dưới: RMSE 0.51, gần bằng nhiễu 0.5; R² 0.995; trọng số học được gần như trùng giá trị thật 3, −2, 1.5. Kết luận: cài đặt đúng.

## 7. Hồi quy logistic: biên hợp lý, nhưng còn 30 ca sai
Bắt đầu 2:55 · ~25s

1. **Trái · đường loss** — Biểu đồ trái: cross-entropy bắt đầu ở 0.693, bằng log 2, tức đoán 0.5 cho mọi mẫu, rồi giảm còn 0.45.
2. **Phải · biên quyết định** — Biểu đồ phải: đường chéo là biên p bằng 0.5. Các vòng tròn là 30 ca sai, nằm đúng vùng hai lớp chồng lấn.
3. **Bốn số dưới** — Bốn số dưới: accuracy 81.25%, F1 0.85, AUC 0.86, và ma trận nhầm lẫn 44, 18, 12, 86.

*Chỉ khi chia phần:* “Em xin mời bạn Thành trình bày câu hai.”

## 8. OpenML credit-g: 1000 hồ sơ, 20 biến, lệch lớp
Bắt đầu 3:20 · ~25s

1. **Trái · số lớp** — Biểu đồ trái: 560 good so với 240 bad, lệch 70/30. Luôn đoán good đã được 70% accuracy.
2. **Phải · credit amount** — Biểu đồ phải: số tiền vay lệch phải và hai lớp chồng lên nhau, không biến nào tự tách được.
3. **Bốn số dưới** — Bốn số dưới: bộ OpenML mã 31; không thiếu, không trùng; chia 800 và 200 phân tầng; 61 đặc trưng sau min–max và one-hot.

## 9. Chống rò rỉ dữ liệu bằng thiết kế, không bằng lời hứa
Bắt đầu 3:45 · ~30s

1. **Ô 01** — Bước một: tách 200 hồ sơ test ngay từ đầu và khóa lại.
2. **Ô 02** — Bước hai: chuẩn hóa nằm trong từng fold, chỉ học từ phần train của fold đó.
3. **Ô 03** — Bước ba: cùng 5 fold phân tầng cho mọi mô hình, chọn theo macro F1.
4. **Ô 04** — Bước bốn: chốt hết lựa chọn rồi mới chạy test, đúng một lần.
5. **Bốn dòng dưới** — Bốn dòng dưới tóm lại: so sánh công bằng, giữ ngoại lai hợp lệ, và baseline 0.412 làm mốc.

## 10. 14 mô hình và một baseline, chọn bằng cross-validation
Bắt đầu 4:15 · ~31s

1. **Biểu đồ cột** — Biểu đồ: macro F1 trung bình 5 fold của 14 mô hình và baseline. MLP màu cam đứng đầu.
2. **Hai thanh đầu** — Nhìn hai thanh đầu: MLP 0.696, Bernoulli NB 0.694. Thanh lỗi ±0.06 rộng hơn khoảng cách, nên chưa nói được ai hơn.
3. **Phải · ghi chú** — Bên phải: ba kernel SVM chỉ là một họ; kNN chọn k bằng 1, một dấu hiệu overfitting.
4. **Ghi chú dưới** — Ghi chú dưới: điểm CV đã dùng để chọn, nên cần tập test để đánh giá độc lập.

## 11. Trên 200 hồ sơ chưa từng thấy, khoảng cách rất hẹp
Bắt đầu 4:46 · ~26s

1. **Bảng · baseline** — Hàng đầu bảng là baseline: accuracy 0.70 nhưng macro F1 chỉ 0.41.
2. **Bảng · MLP** — Hàng cuối là MLP được chọn: accuracy 0.79, macro F1 0.73, AUC 0.81.
3. **Bảng · logistic tự cài** — So với hàng logistic tự cài: macro F1 cũng 0.730. Mô hình phức tạp hơn không hơn rõ.
4. **Phải · ghi chú** — Bên phải: cả 14 mô hình vượt baseline, nhưng chỉ chênh vài phần nghìn, nên đừng đọc như bảng xếp hạng.

*Chỉ khi chia phần:* “Em xin mời bạn Tâm trình bày phần đọc kết quả và overfitting.”

## 12. Một con số accuracy đẹp có thể che mất lỗi quan trọng
Bắt đầu 5:12 · ~30s

1. **Ma trận nhầm lẫn** — Ma trận của MLP: hàng là nhãn thật, cột là dự đoán. Đường chéo 126 cộng 32 là 158 trên 200 đúng.
2. **Hàng bad** — Nhưng nhìn hàng bad: 28 hồ sơ xấu bị bỏ sót, recall lớp bad chỉ 0.533.
3. **Phải · ROC** — Đường ROC: ba mô hình đầu gần như chồng nhau, AUC từ 0.78 đến 0.81.
4. **Dòng dưới** — Dòng dưới: Gaussian NB bắt được nhiều bad hơn nhưng báo nhầm nhiều hơn. Chọn bên nào là quyết định nghiệp vụ.

## 13. Bằng chứng: cây càng sâu, khoảng cách càng lớn
Bắt đầu 5:42 · ~36s

1. **Trái · độ sâu cây** — Biểu đồ trái: tăng độ sâu, đường train màu xanh leo lên 1, đường validation màu cam đạt đỉnh ở độ sâu 6 rồi giảm. Đó là overfitting.
2. **Phải · khoảng cách** — Biểu đồ phải: thanh xám là khoảng cách train–CV ban đầu, thanh xanh là sau khi chọn tham số. Cây giảm từ 0.39 xuống 0.12.
3. **Ba số dưới** — Ba số dưới: cây không giới hạn đạt 1.00 trên train mà chỉ 0.614 trên validation; random forest vẫn còn 0.324.
4. **Dòng cuối** — Dòng cuối là cách chữa: giới hạn độ phức tạp, chọn bằng validation, giữ test riêng.

## 14. Điều nhóm làm được, điều còn hạn chế
Bắt đầu 6:18 · ~33s

1. **Cột 1 · kết quả** — Cột một: hai mô hình tự cài học đúng; MLP được chọn với macro F1 0.73; accuracy 0.79 vẫn bỏ sót 28 hồ sơ xấu.
2. **Cột 2 · bài học** — Cột hai: chuẩn hóa trong fold là điều kiện để so sánh đáng tin; chênh nhỏ hơn dao động fold thì chưa kết luận.
3. **Cột 3 · hạn chế** — Cột ba: một bộ dữ liệu, một lần chia test, chưa hội tụ hoàn toàn, chưa có kiểm định thống kê.
4. **Lời cảm ơn** — Nhóm em xin cảm ơn thầy và các bạn đã lắng nghe.
