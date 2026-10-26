# Năm câu hỏi vấn đáp và ý trả lời

## 1. Đề yêu cầu 5%, vì sao chỉ che 32 dòng? Có được ghi đúng 5% không?

Không có số dòng nguyên bằng 5% của 649 vì kết quả là 32,45. Làm tròn về 32 cho tỷ lệ 4,93066%, gần 5% nhất. Ghi “xấp xỉ 5%” và công bố cả số lượng lẫn tỷ lệ thực tế. Chọn không hoàn lại để có đúng 32 ô khác nhau, lưu mask và seed để kiểm chứng.

Câu hỏi tiếp: seed có làm phương pháp tốt hơn không? Không. Seed giúp tái lập một mô phỏng; nó không chứng minh độ bền vững trước mọi missing pattern.

## 2. Mean imputation giữ nguyên số dòng, vì sao vẫn có thể làm sai phân tích?

Nó tạo một cụm giá trị bằng mean và không phản ánh biến động của những giá trị thực sự chưa biết. Với absences, còn tạo giá trị lẻ cho biến đếm. Trong thí nghiệm này SD đổi từ khoảng 4,6408 của raw thành 4,4940 sau imputation; count thỏa bộ lọc đổi từ 334 thành 339. Vì raw đầy đủ đã biết, kết luận chính dùng raw; hai nhánh là minh họa riêng.

Câu hỏi tiếp: mean tính ở đâu? Trên các giá trị còn quan sát sau khi che. Không dùng các giá trị gốc đã che để tính mean thay thế.

## 3. G2 tương quan mạnh nhất với G3. Có thể nói G2 “gây ra” G3 hoặc failures là nguyên nhân lớn nhất không?

Không. G2/G3 là những kỳ đánh giá liên quan nhau, cùng phản ánh năng lực và nhiều yếu tố khác. Spearman khoảng 0,9445 mô tả thứ hạng cùng biến thiên. failures có rho khoảng −0,4484, lớn nhất về trị tuyệt đối trong các biến hoàn cảnh dạng số/thứ bậc gốc đã xét. Chưa có điều chỉnh đa biến hay thiết kế thực nghiệm, nên không kết luận nhân quả hoặc xếp hạng tất cả nguyên nhân.

Câu hỏi tiếp: vì sao không xếp performance_band vào? Nó được tạo từ G3 nên dùng nó giải thích G3 là quan hệ vòng. Các biến dẫn xuất khác cũng bị loại khỏi bảng xếp hạng “yếu tố gốc” để không tạo lợi thế do cách xây biến.

## 4. Hai học sinh có cùng G3_minmax_school có nhất thiết cùng điểm G3 không? Nhóm toàn một giá trị xử lý thế nào?

Không nhất thiết. Min–max dùng mức min/max riêng từng trường, nên cùng vị trí tương đối không đảm bảo cùng điểm tuyệt đối nếu hai khoảng khác nhau. Với dataset hiện tại hai trường cùng miền G3 0–19, phép biến đổi tình cờ dùng cùng khoảng; điều này không thay đổi giới hạn của phương pháp nói chung. Nếu nhóm hằng, mẫu số bằng 0; quy ước trả 0 và kiểm không NaN/inf, giữ đúng index.

Câu hỏi tiếp: score chuẩn hóa có dùng làm biến giải thích G3 không? Không, nó là biến đổi trực tiếp của outcome.

## 5. Top ten có nhiều người đồng hạng. Chọn mười dòng có tùy tiện không, và làm sao kiểm đủ cột?

Tiêu chí đã chốt trước: sắp theo G3, stable sort giữ thứ tự nguồn khi bằng điểm, lấy đúng mười dòng. Đây là quy tắc chọn để tái lập, không phải căn cứ học thuật phân biệt những người đồng điểm. Notebook và CSV giữ đủ 37 cột; slide/báo cáo dùng bảng trích lược có ghi rõ. Source index zero-based cho phép truy lại dòng gốc.

Câu hỏi tiếp: nếu muốn hiển thị tất cả người đồng điểm ở ngưỡng? Khi đó có thể nhiều hơn mười dòng. Bài này giữ đúng mười theo yêu cầu và công bố cách phá đồng hạng.
