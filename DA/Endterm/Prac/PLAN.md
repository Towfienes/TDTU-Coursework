# Kế hoạch triển khai đã chốt — Endterm DAV

Bản này thay thế kế hoạch trước phản biện Astra high. Người dùng đã yêu cầu triển khai.
Tiến độ và bằng chứng thực tế nằm trong WORKLOG.md, REQUIREMENTS.md và kết quả kiểm tra.

## Thông tin cố định
- Môn: Data Analysis and Visualization; loại bài: Endterm Report.
- Nhóm: VibeCoding_Expert.
- NGO LAM TIEN — 524H0195; NGUYEN CONG THANH — 524H0191;
  NGUYEN LE NHAT TAM — 524H0186; NGO BINH MINH — 524H0169.
- Giảng viên: Cô Ho Thi Linh, Ph.D.; tên giữ cách viết Latin trong ảnh đã cung cấp.
- Ngày báo cáo: 20/10/2026. Hạn nộp: 23:00 ngày 22/10/2026, giờ Việt Nam.
- Report và slide tiếng Anh; notes, demo và bàn giao tiếng Việt.
- Phân công chỉ là dự kiến để tập thuyết trình; không tự tạo % đóng góp.

## Phương pháp đã chốt
1. Dùng riêng UCI student-por.csv (649 dòng, 33 cột), giữ nguyên raw và checksum.
2. Không gộp hai môn, không xóa các dòng giống thuộc tính nếu chưa có căn cứ định danh.
3. Giả lập thiếu bằng seed 42, chọn không hoàn lại 32 ô absences (4,93066%).
4. Mean imputation và dropna xuất phát từ cùng corrupted và cùng mask.
5. Dùng bản gốc đã kiểm cho Phần II–IV; mô phỏng MCAR là thí nghiệm riêng.
6. Kiểm độ nhạy absences, rho với G3 và bộ lọc hai điều kiện giữa raw/imputed/dropna.
7. Tạo prior_grade_mean bằng insert ngay trước G3; grade_progress = G2−G1;
   performance_band gồm 0–9, 10–14, 15–20, là dải do bài phân tích quy ước.
8. Regex fullmatch G[123] lấy đúng các cột điểm; Series→list→lọc bằng Python.
9. Pearson matrix cho 16 biến số gốc; Spearman xếp theo |rho|, giữ dấu và n.
10. Tách G1/G2 khỏi các yếu tố hoàn cảnh; loại biến dẫn xuất khỏi xếp hạng.
11. Groupby trường tính count/mean/std/min/max của cả G1, G2, G3;
    thêm G3 theo studytime, failures và higher. Không suy nhân quả.
12. Group transform min–max trong trường; nhóm hằng trả 0, giữ index.
13. Histogram và comparative bar dùng Seaborn; box dùng Seaborn;
    pie dùng Matplotlib; scatter dùng regplot với ci=None;
    core bar dùng list/dictionary và Matplotlib.
14. comprehensive_report(df) hiển thị và trả dict có count/%/missing/thống kê điểm.
15. Top/bottom giữ đúng 10 dòng và đủ 37 cột trong notebook/CSV;
    đồng hạng giữ thứ tự dòng nguồn bằng stable sort.
16. Giữ nguyên mã failures và ghi chú điểm chưa nhất quán trong codebook.

## Trình tự và sản phẩm
1. Lưu ảnh đề, thông tin nguồn và project.json; tạo môi trường Python 3.12 riêng.
2. Chạy notebook theo đúng I–IV và các kiểm tra biên. Xuất CSV/JSON/figures/manifest.
3. Kiểm mẫu Word: đủ bốn người, hai bìa, font, OMML, Roman/Arabic và các danh mục.
4. Tạo báo cáo Word/PDF năm chương theo TDTU_REPORT_STYLE.md ở gốc TDTU.
5. Report có List of Figures và List of Tables; caption và danh mục từ nguồn thật.
6. Tạo 25 slide (22 chính, 3 phụ lục), khoảng 24,5 phút trước Q&A gồm 3 phút demo.
7. Slide trắng/đen/xám, logo gốc giữ màu; chữ, bảng, biểu đồ chỉnh sửa được.
8. Viết notes/demo/viva bằng tiếng Việt; có fallback offline dùng outputs đã chạy.
9. Tạo skill slide chỉ trong TDTU/.agents/skills/tdtu-presentation và dẫn từ AGENTS.md.
10. Chạy kiểm cuối, xem mọi trang/slide, đối chiếu số liệu, giải nén và chạy lại.
11. Đóng gói 524H0195_524H0191_524H0186_524H0169.zip, một thư mục cùng tên bên trong.

## Môi trường và hợp đồng tái lập
- Notebook: môi trường riêng, dependencies khóa trong requirements.txt.
- Word: bản sao Template_EN.docx và bundled Python/OOXML; không sửa bản gốc.
- PowerPoint: bundled Artifact Tool; native objects, workbook dữ liệu biểu đồ có thể sửa.
- Một lần chạy notebook tính các thống kê; builders chỉ trình bày artifacts này.
- TOC/SEQ/PAGEREF được giữ trong DOCX; cache số trang tạo tự động từ render
  của heading/caption thật, lặp đến khi pagination ổn định. Không lưu đè qua LO.
- Notebook chạy offline sau cài dependencies và không cần đường dẫn ngoài gói.
- Build tài liệu có hướng dẫn riêng cho bundled runtime, font và công cụ render.

## Nghiệm thu
- Input đúng 649×33, schema, miền dữ liệu, checksum và missing ban đầu.
- Missing đúng 32 ô; imputation còn 649 dòng, dropna còn 617; các ô quan sát giữ nguyên.
- Kiểm biên dải điểm 0/9/10/14/15/20; nhóm hằng; index; nhóm không có quan sát.
- Counts/% khớp; top/bottom đủ dòng/cột; toàn bộ cell chạy sạch.
- Mục lục/danh mục khớp số trang cuối; công thức native; không tràn/cắt nội dung.
- Tất cả slide được render và xem; notes tồn tại; số liệu khớp notebook.
- Gói không có .venv, caches, locks, file render QA hay đường dẫn phụ thuộc máy.
- Chạy lại từ bản giải nén cho cùng kết quả số trong sai số 1e-10.
- Không tuyên bố đã kiểm trong Microsoft PowerPoint hoặc đã tập thuyết trình nếu chưa làm.
