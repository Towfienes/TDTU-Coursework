# Kịch bản thuyết trình tiếng Việt

Thời lượng dự kiến khoảng 24,5 phút trước Q&A; chưa xác nhận đã diễn tập thực tế.

## Slide 1 — Data Analysis and Visualization

Thời lượng dự kiến: 45 giây.
Giới thiệu nhóm bốn người và Cô Ho Thi Linh. Nêu đề tài phân tích thành tích học sinh từ dữ liệu công khai; báo cáo cuối kỳ ngày 20/10/2026. Không gọi đây là dữ liệu sinh viên TDTU.
Nguồn: Executed notebook and results/summary.json.

## Slide 2 — Objectives and analytical questions

Thời lượng dự kiến: 1 phút.
Trình bày bốn câu hỏi tương ứng bốn phần đề. Điểm nhấn là phân tích mô tả có thể chạy lại, có nguồn gốc dữ liệu và có giới hạn rõ ràng. Chuyển sang dataset trước khi giải thích kỹ thuật.
Nguồn: Executed notebook and results/summary.json.

## Slide 3 — Dataset and provenance

Thời lượng dự kiến: 1 phút 15 giây.
Nguồn UCI Student Performance, chỉ file student-por.csv. Có 649 bản ghi, 33 cột, không thiếu ở nguồn. GP có 423 và MS có 226 bản ghi. Không gộp môn Toán vì có học sinh trùng giữa hai file. Nêu thang lý thuyết 0–20 khác miền quan sát 0–19.
Nguồn: Cortez (2008), https://doi.org/10.24432/C5TG7T; references/student.txt.

## Slide 4 — Inspect before transforming

Thời lượng dự kiến: 1 phút.
Mở notebook mục I.1 và I.2. Giải thích delimiter chấm phẩy, kiểm checksum, shape, dtypes và info. Hiển thị cả đầu và cuối dữ liệu giúp phát hiện parse sai. Integer storage không có nghĩa studytime là số giờ thực.
Nguồn: Executed notebook and results/summary.json.

## Slide 5 — A controlled missingness experiment

Thời lượng dự kiến: 1 phút.
Giải thích 5%×649=32,45; lấy 32 ô nên tỷ lệ là 4,93%. Che duy nhất absences, cùng mask cho hai nhánh. Seed 42 tái lập; MCAR chỉ là giả lập. Tất cả kết luận chính dùng raw đã kiểm.
Nguồn: Executed notebook and results/summary.json.

## Slide 6 — Imputation and deletion change the data

Thời lượng dự kiến: 1 phút 15 giây.
Bảng này lấy từ output chạy thật. Mean imputation dùng mean của 617 giá trị chưa bị che: 3,623987. Giữ 649 dòng nhưng giảm phân tán và tạo số lần vắng lẻ. Dropna còn 617. Cả hai bắt đầu từ cùng corrupted, không drop sau fillna.
Nguồn: Executed notebook and results/summary.json.

## Slide 7 — Python structures and regex

Thời lượng dự kiến: 45 giây.
Chứng minh Series→list→lọc bằng Python. Có 549 điểm ≥ 10 theo quy ước bài phân tích. Regex fullmatch lấy đúng G1/G2/G3, loại G12 và G3_extra. Không cần bịa ID cá nhân hoặc dữ liệu bẩn.
Nguồn: Executed notebook and results/summary.json.

## Slide 8 — Indexing and a two-condition filter

Thời lượng dự kiến: 1 phút.
Giải thích loc theo nhãn có bao gồm cận cuối 9, iloc theo vị trí. Bộ lọc studytime ≥ 2 và absences ≤ 5 cho 334/649 = 51,46%. Nhấn mạnh ngưỡng minh họa, không phải quy tắc can thiệp.
Nguồn: Executed notebook and results/summary.json.

## Slide 9 — Three engineered features

Thời lượng dự kiến: 1 phút 15 giây.
Giải thích từng cột và thao tác insert ngay trước G3. prior_grade_mean không chứa G3; grade_progress là chênh lệch giữa hai kỳ, không tự nó chứng minh tiến bộ do can thiệp. performance_band gồm 0–9, 10–14, 15–20 là nhóm tự quy ước. Vì chứa outcome, cột này không được xếp hạng như một yếu tố giải thích.
Nguồn: Executed notebook and results/summary.json.

## Slide 10 — Grouped statistics and transformation

Thời lượng dự kiến: 1 phút 30 giây.
Notebook và báo cáo có đủ count, mean, std, min, max cho cả G1, G2, G3 theo trường. Slide trích G3 và cỡ mẫu để đọc được. GP có 423 bản ghi, MS có 226; trung bình và độ phân tán khác nhau nhưng chưa điều chỉnh yếu tố khác. Chuẩn hóa min–max dùng transform trong từng trường và giữ đúng index; nhóm hằng trả 0. Đây là thang tương đối trong nhóm.
Nguồn: Executed notebook and results/summary.json.

## Slide 11 — Association ranking: two distinct families

Thời lượng dự kiến: 1 phút 15 giây.
Có ma trận Pearson cho 16 biến số gốc và bảng Spearman bổ sung. G2 có rho khoảng 0,94445 và là điểm kỳ trước; không trình bày như một phát hiện mới về hoàn cảnh. failures có rho khoảng −0,44836, lớn nhất về trị tuyệt đối trong nhóm biến hoàn cảnh dạng số/thứ bậc đã xét. Đây không phải feature importance của mô hình đa biến. Không so mean difference của biến định tính trực tiếp với rho.
Nguồn: Executed notebook and results/summary.json.

## Slide 12 — Final-grade distribution

Thời lượng dự kiến: 1 phút.
Histogram trong notebook dùng sns.histplot với bin một điểm. Slide dùng cùng bảng tần số đã xuất ở dạng chart chỉnh sửa được. Mean khoảng 11,906; median 12; sample SD khoảng 3,231. Giữ điểm 0 như một kết quả quan sát. Trục giữ toàn thang lý thuyết 0–20, kể cả bin rỗng.
Nguồn: Executed notebook and results/summary.json.

## Slide 13 — Final grades by school

Thời lượng dự kiến: 1 phút.
Box plot trong notebook dùng Seaborn. Q1, median, Q3, whiskers và outliers được xuất theo cùng quy tắc 1,5 IQR. Slide dùng các đối tượng chỉnh sửa được dựng từ thống kê này để tránh khác biệt quy tắc quartile của Office. Median GP là 13, MS là 11. Khác biệt nhóm chưa điều chỉnh không chứng minh tác động của trường.
Nguồn: Executed notebook and results/summary.json.

## Slide 14 — Final grade by study-time category

Thời lượng dự kiến: 1 phút.
So sánh mean G3 theo studytime 1–4. Bảng gốc có count và SD; các cỡ nhóm lần lượt là 212, 305, 97, 35. Nhãn trên slide giữ cả khoảng giờ và n. Nhóm trên 10 giờ nhỏ nhất. Không suy ra rằng một người học thêm giờ sẽ đạt đúng chênh lệch trung bình quan sát này.
Nguồn: Executed notebook and results/summary.json.

## Slide 15 — Performance-band proportions

Thời lượng dự kiến: 1 phút.
Pie chart sử dụng đúng cột tạo ở Phần II. Nhóm 0–9 có 100 bản ghi, 15,41%; 10–14 có 418, 64,41%; 15–20 có 131, 20,18%. Đây là dải điểm do nhóm quy ước để mô tả, không phải hệ thống xếp loại chính thức. Tổng count là 649 và phần trăm tổng 100 trước làm tròn.
Nguồn: Executed notebook and results/summary.json.

## Slide 16 — Earlier and final grades

Thời lượng dự kiến: 1 phút.
Notebook dùng sns.regplot, ci=None, và độ trong suốt để thấy các tọa độ chồng nhau. Tọa độ đường fit được xuất từ lần chạy Seaborn và dùng lại trên slide. Rho khoảng 0,9445 là liên hệ, không phải nhân quả. G2 và G3 là các kỳ đánh giá liên quan nhau về thời gian và nội dung.
Nguồn: Executed notebook and results/summary.json.

## Slide 17 — Matplotlib core from Python structures

Thời lượng dự kiến: 1 phút.
Chỉ rõ cell III.4: dữ liệu chuyển thành list/dictionary, rồi dùng Matplotlib bar và bar_label. Giá trị là mean G1/G2 của năm bản ghi đầu, không chứa G3. Nhãn 1–5 là vị trí dòng nguồn, không phải mã hay tên cá nhân. Ví dụ nhỏ này minh họa thao tác Python và vẽ, không đại diện cho toàn bộ dataset.
Nguồn: Executed notebook and results/summary.json.

## Slide 18 — Comprehensive report and extreme records

Thời lượng dự kiến: 1 phút 30 giây.
Hàm comprehensive_report(df) vừa in nội dung dễ đọc vừa trả dictionary để dùng lại đúng số liệu. Có 37 cột: 33 cột gốc và 4 cột dẫn xuất. Top/bottom giữ đúng 10 dòng; stable sort giữ thứ tự nguồn khi đồng hạng. Tất cả 37 cột có trong notebook và CSV; slide chỉ trích các cột có thể đọc được.
Nguồn: Executed notebook and results/summary.json.

## Slide 19 — Code demonstration

Thời lượng dự kiến: 3 phút.
Demo trong 3 phút: (1) mở I.3, chỉ mask 32 ô và hai kết quả mean/dropna 649/617; (2) mở II.2 và II.4, chỉ insert và transform; (3) mở IV.1 và IV.2, gọi comprehensive_report rồi xem bảng đủ cột. Chạy toàn bộ từ kernel sạch trước buổi báo cáo để kiểm tái lập. Nếu demo gặp lỗi, dùng outputs đã lưu, không chờ tải dữ liệu. Xem Demo_VI.md để có lời dẫn và mốc thời gian.
Nguồn: Executed notebook and results/summary.json.

## Slide 20 — Conclusions and limitations

Thời lượng dự kiến: 1 phút 30 giây.
Chốt phân bố điểm, liên hệ với G2 và failure categories. Nhắc giới hạn: hai trường ở Bồ Đào Nha, không đại diện TDTU; chưa điều chỉnh đa biến; không chứng minh nhân quả; chỉ một mô phỏng MCAR. Gợi ý nghiên cứu hỗ trợ học sinh là một hướng cần kiểm chứng, chưa có effect size hay mức lợi ích dự kiến.
Nguồn: Executed notebook and results/summary.json.

## Slide 21 — References

Thời lượng dự kiến: 30 giây.
Nêu dataset và tài liệu chính thức của các thư viện. Codebook, mã nguồn và manifest có trong gói nộp. Biểu đồ phân tích sinh từ notebook; logo giữ nguồn chuẩn của trường. Trích dẫn dữ liệu theo CC BY 4.0 và chuyển sang hỏi đáp.
Nguồn: URLs displayed on this slide.

## Slide 22 — Questions and discussion

Thời lượng dự kiến: Theo giảng viên.
Mời giảng viên hỏi. Chuẩn bị giải thích vì sao 32 ô chỉ là 4,93%; mean imputation thay đổi độ phân tán; tương quan G2 không chứng minh nhân quả; normalization trong nhóm không tạo thang điểm tuyệt đối; stable top ten xử lý đồng hạng ra sao. Xem Viva_VI.md.
Nguồn: Executed notebook and results/summary.json.

## Slide 23 — Appendix: highest ten records

Thời lượng dự kiến: Dự phòng.
Bảng trên slide chọn một số cột để đọc được. Tất cả 37 cột nằm trong notebook và CSV. Source index dùng zero-based. Đồng hạng giữ thứ tự dòng nguồn; bản ghi đồng điểm bị loại không kém hơn hay tốt hơn về G3.
Nguồn: Executed notebook and results/summary.json.

## Slide 24 — Appendix: lowest ten records

Thời lượng dự kiến: Dự phòng.
Bảng trên slide chọn một số cột để đọc được. Tất cả 37 cột nằm trong notebook và CSV. Source index dùng zero-based. Đồng hạng giữ thứ tự dòng nguồn; bản ghi đồng điểm bị loại không kém hơn hay tốt hơn về G3.
Nguồn: Executed notebook and results/summary.json.

## Slide 25 — Appendix: sensitivity and method checks

Thời lượng dự kiến: Dự phòng.
Bảng độ nhạy hiển thị sample SD của absences, rho với G3 và số dòng thỏa bộ lọc. Dùng cùng mask cho mọi phương pháp. Denominator raw là 649, dropna là 617. Fixture nhóm hằng trả 0; kiểm ngưỡng band tại 0, 9, 10, 14, 15, 20. Giữ nguyên mã failures và ghi chú sự mơ hồ trong codebook, không sửa ngầm.
Nguồn: Executed notebook and results/summary.json.
