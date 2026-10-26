# Năm câu hỏi phản biện và ý trả lời

## 1. Có 4.177 dòng mà phần kiểm định chỉ dùng 3.341, có làm sai yêu cầu dữ liệu không?

Dataset gốc vẫn có 4.177 dòng/chín biến, vượt tối thiểu 500/5. Chúng em lưu holdout 836 dòng để kiểm tra dự đoán độc lập. EDA chi tiết/inference dùng train, công bố n của từng phép tính; giữ test khỏi phát triển mô hình. Đây là lựa chọn thiết kế, không phải bỏ bớt dữ liệu để tìm p-value. Với Height, n giảm thêm hai do giá trị 0 không hợp lệ. Nguồn đã loại missing từ trước nên cũng phải nêu selection bias.

## 2. Cả ba phân phối bị bác bỏ thì t-test và hồi quy còn dùng được không?

Phân phối cận biên của predictor khác phân phối phần dư có điều kiện. Welch kiểm trung bình với sai số chuẩn cho phương sai khác nhau; cỡ nhóm lớn hỗ trợ xấp xỉ, nhưng không chữa phụ thuộc cụm hay selection bias. OLS vẫn ước lượng xấp xỉ tuyến tính và dự đoán được đánh giá trực tiếp. Cần xem phần dư, phương sai thay đổi và influence, dùng HC3 cho CI; không nhận rằng mọi giả định được thỏa. P Monte Carlo 0,0005 là sàn 1/2.000, không phải 0.

## 3. Vì sao không đưa Rings+1,5 vào dự đoán Rings và không mã nhóm M/F/I thành 0/1/2?

Age được tạo trực tiếp từ đáp án nên gây rò rỉ hoàn toàn. M/F/I là nhãn danh nghĩa, I là infant; gán thứ tự số tạo khoảng cách không có căn cứ. Hồi quy dùng hai dummy I/M với F tham chiếu. Correlation chỉ dùng biến số gốc. Group association không chứng minh tác động của giới tính vì infant là giai đoạn phát triển.

## 4. Shell weight tương quan dương mạnh mà một hệ số khối lượng có thể âm, có lỗi code không?

Tương quan là liên hệ cận biên; slope đa biến giữ các predictor khác cố định. Các khối lượng/kích thước chồng thông tin, VIF cao làm slope nhạy. Kiểm rank, prediction identity giữa sklearn/OLS và hệ số stored units để loại lỗi triển khai. HC3 không chữa đa cộng tuyến. Không gọi conditional slope là nguyên nhân sinh học hay importance tuyệt đối.

## 5. Tại sao không xóa 212 dòng Cook rồi báo metric tốt nhất, hoặc round/clip dự đoán?

Cook phụ thuộc mô hình, không chứng minh quan sát sai. Primary model giữ dữ liệu; sensitivity định trước chỉ fit/screen/refit inner train, giữ validation nguyên. Nếu dùng toàn train để chọn dòng trước CV sẽ lộ thông tin validation. Không chọn lại theo test. RMSE/MAE tính trên dự đoán liên tục gốc; clipping/rounding sẽ là phương pháp mới cần thiết kế/đánh giá riêng. Full có một dự đoán ngoài miền quan sát và phải công bố.

Câu hỏi tiếp: Holm cho gia đình nào? Ba kiểm định chính một gia đình; ba distribution tests một gia đình khác; post-hoc được làm sau omnibus và có Holm riêng. CI 95% được báo riêng lẻ, không tự nhận simultaneous CI.
