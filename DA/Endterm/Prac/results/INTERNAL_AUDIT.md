# Tự thẩm định nội bộ theo chuẩn TDTU

**TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG — KHOA CÔNG NGHỆ THÔNG TIN**  
Học phần: Data Analysis and Visualization. Đề tài: Student Performance.  
Nhóm: VibeCoding_Expert; bốn tác giả/MSSV và giảng viên Cô Ho Thi Linh, Ph.D. được ghi tại `project.json`. Ngày kiểm: 20/10/2026.

Khung điểm dưới đây do dự án tự thiết lập từ bốn phần đề và chuẩn workspace; **không phải rubric hay điểm chính thức của giảng viên**. Điểm phản ánh bằng chứng của sản phẩm hiện tại, không xác nhận kiến thức hoặc đóng góp của từng thành viên.

| Tiêu chí | Tối đa | Tự kiểm | Bằng chứng và nhận định |
|---|---:|---:|---|
| I — Thu thập, head/tail, schema, info | 0,6 | 0,6 | Raw 649×33, checksum, đủ output cấu trúc, codebook và nguồn UCI |
| I — Missing cùng mask, mean/dropna, so sánh | 0,8 | 0,8 | 32 ô/4,93%; 649/617 dòng; ô không che giữ nguyên; sensitivity có số thực |
| I — Series/list/Python và regex | 0,4 | 0,4 | Lọc ra 549 điểm; fullmatch G[123] và negative examples |
| II — loc/iloc, hai điều kiện | 0,4 | 0,4 | 10 dòng đầu, chọn cột theo vị trí, 334 dòng qua bộ lọc |
| II — Ba feature và insert | 0,5 | 0,5 | Công thức và vị trí cột có assert; feature dẫn xuất không được xếp là yếu tố gốc |
| II — corr, grouping và aggregation | 0,8 | 0,8 | Pearson 16×16, Spearman có dấu/n; count/mean/std/min/max G1/G2/G3 theo trường |
| II — transform trong nhóm | 0,5 | 0,5 | Min–max đúng index/[0,1]; nhóm hằng có test, không NaN/inf |
| III — Sáu biểu đồ và diễn giải | 1,8 | 1,8 | Histogram, box, bar, pie, regplot, Matplotlib core; nhãn/đơn vị/n/giới hạn, outputs chạy thật |
| IV — Hàm tổng hợp, count/% | 0,5 | 0,5 | Input df, print và return dict; tổng 649/100%; kiểm cả frame rỗng |
| IV — Top/bottom đủ 10 dòng và mọi cột | 0,4 | 0,4 | Notebook/CSV đủ 37 cột; ổn định đồng hạng; slide/report ghi rõ trích cột |
| IV — Kết luận có cơ sở và giới hạn | 0,6 | 0,6 | Tách prior/context; G2 rho 0,9445, failures −0,4484; không gọi là nhân quả |
| Tổ chức thư mục và tái lập | 1,0 | 1,0 | 3 bước chạy, dependency lock, 3 test, fresh-kernel/extracted rerun, ZIP sạch và nhỏ |
| Báo cáo theo chuẩn TDTU | 1,0 | 1,0 | Hai bìa, Roman/Arabic, lề/font, OMML3, LOF/LOT; 31 trang đã xem |
| Slide, notes, demo và readiness | 0,7 | 0,4 | 25 slide, 5 editable chart workbooks, notes/demo/viva; giữ lại 0,3 vì chưa thử Microsoft PowerPoint và chưa diễn tập đo giờ |
| **Tổng tự kiểm** | **10,0** | **9,7** | **Đạt kiểm tra sản phẩm nội bộ; còn bước trình chiếu/diễn tập thực tế** |

## Nhận xét chuyên môn và liêm chính

Số liệu đến từ notebook đã chạy; builders đọc artifacts, không có pipeline thống kê thứ hai. Tái lập từ thư mục giải nén đối chiếu toàn bộ 14 bảng CSV và summary với sai số tuyệt đối 1e-10. Mean được tính trên giá trị còn quan sát sau khi che, không dùng các giá trị gốc đã che để điền. Hai treatment xuất phát từ cùng corrupted frame.

Đề mang tính phân tích mô tả: không yêu cầu mô hình dự đoán, dashboard, chia train/test hoặc gradient checking. Không trừ điểm vì thiếu các sản phẩm ngoài đề. Việc min–max dùng toàn bộ dữ liệu trong trường được trình bày là mô tả, không được tuyên bố là preprocessing cho đánh giá dự đoán ngoài mẫu.

Điểm yếu khoa học cần bảo vệ: dữ liệu chỉ hai trường/một môn; association chưa điều chỉnh yếu tố gây nhiễu; biến thứ bậc không phải số giờ liên tục; các nhóm studytime có cỡ mẫu khác nhau; chỉ một mô phỏng MCAR. Phần failures giữ nguyên mã và ghi rõ codebook chưa nhất quán. Không sửa số hoặc tạo định danh học sinh giả.

Các bảng rộng đầy đủ ở notebook/CSV; report/slide chỉ trích cột có ghi rõ. Chuẩn báo cáo được ưu tiên theo PDF tham chiếu và lựa chọn người dùng. Phân công dự kiến không đủ căn cứ để tạo tỷ lệ đóng góp, nên không tự điền tỷ lệ dù mẫu chấm chung có gợi ý trường này.

## Năm câu hỏi bảo vệ cần trả lời được

1. Vì sao 32/649 là xấp xỉ 5%, và một seed không chứng minh tính bền vững của phương pháp?
2. Vì sao mean imputation giữ số dòng nhưng giảm SD và đổi count qua bộ lọc? Mean được tính trên những ô nào?
3. Vì sao rho của G2 cao không chứng minh nhân quả, và performance_band không được dùng giải thích G3?
4. Min–max trong từng trường giữ thông tin gì, mất thông tin gì; nhóm hằng và index không liên tiếp xử lý thế nào?
5. Khi top ten đồng điểm, quy tắc stable sort mang ý nghĩa gì; kiểm được đủ 37 cột ở đâu?

Ý trả lời và câu hỏi tiếp nằm tại `slides/Viva_VI.md`. Nhóm cần tự diễn tập ba phút demo và toàn bài; điểm tự kiểm không bảo đảm điểm bảo vệ.
