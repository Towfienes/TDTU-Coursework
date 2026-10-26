# Kế hoạch đã triển khai — Endterm DAV Theory N4

Kế hoạch Astra đã được người dùng duyệt và yêu cầu triển khai tại `Nor/`. Đây là bài lớp lý thuyết, tách biệt với `Prac/`. Ngày báo cáo: **20/10/2026**. Report/slide tiếng Anh; notes, demo và nhật ký tiếng Việt.

## Yêu cầu và dữ liệu

- Bám rubric: EDA 15%, phân phối 15%, kiểm định 15%, tương quan 15%, hồi quy 20%, code 20%.
- Một nguồn UCI Abalone: **4.177 dòng, 9 cột**, vượt 500 dòng/5 biến. Dữ liệu thực tế công khai, nhóm tự tìm; không nhận là tự đo.
- Khác toàn bộ dataset trong hai danh sách cấm, Sentiment140 giữa kỳ và Student Performance thực hành. Người dùng đã xác nhận chấp nhận dataset.
- Giữ raw/codebook, URL, DOI, giấy phép và SHA-256. M/F/I là male/female/infant; dùng stored units đúng nguồn.

## Thiết kế phân tích

1. Audit schema, thiếu/trùng. Chỉ đổi hai Height = 0 thành NaN trong bản xử lý; giữ dòng, không mô phỏng missingness.
2. Split 80/20 stratify nhóm, seed 42; lưu chỉ số gốc. EDA chi tiết, suy luận và phát triển mô hình dùng 3.341 train; 836 test dành cho đánh giá cuối.
3. EDA có mean, median, SD, quartiles; histogram/KDE, boxplot, bar, scatter và lý do chọn. IQR chỉ gắn cờ, không tự xóa dữ liệu hợp lệ.
4. Phân phối: Length/Normal; Whole weight/Normal và Lognormal. AD Monte Carlo 1.999, refit tham số, Holm ba kiểm tra; histogram/density và Q–Q. Báo đúng sàn p, không thử đến khi có p mong muốn.
5. Ba giả thuyết chính ở alpha 0,05: Welch Rings M/F, Chi-square nhóm × ring band, Welch ANOVA Length F/I/M. Nêu H0/H1, giả định, statistic/df/p, CI/effect size. Holm chính; post-hoc Welch có Holm riêng sau omnibus. Chi-square có fallback mô phỏng giữ biên khi expected nhỏ.
6. Pearson/Spearman biến số gốc, ties và pairwise n. Hai heatmap/scatter; phân biệt tương quan với hệ số có điều kiện và nhân quả.
7. Hồi quy Rings: baseline trung bình, compact, full 8 đầu vào gốc. Median/scaling/dummies nằm trong từng fold. Cùng 5 fold, MAE/RMSE/R² CV và test. Không dùng age = Rings + 1,5 làm X; không round/clip dự đoán.
8. Chẩn đoán rank/VIF, HC3 CI, phần dư/Q–Q, BP và Cook. Sensitivity fit/screen/refit chỉ inner train, validation không đổi; không chọn lại theo test.

## Sản phẩm và nghiệm thu

- Notebook chạy sẵn, src/tests, dữ liệu, CSV/JSON, PNG/SVG và manifest. Notebook xuất một nguồn số liệu cho tài liệu.
- Word/PDF chuẩn TDTU: hai bìa → acknowledgement → declaration → TOC/LOF/LOT → bảy chương → references. A4/TNR 13/lề 3,5–2–3,5–3 cm; Roman rồi Arabic ở header giữa; OMML thật. Bìa/references không vào TOC theo đề.
- Report hình màu, chữ/caption/bảng thường đơn sắc; cập nhật chuẩn chung `TDTU_REPORT_STYLE.md`. Slide nền/chữ/bảng thường trắng đen; hình và biểu đồ có màu, logo màu gốc.
- Slide 16 chính + 3 phụ lục, sáu native charts/workbooks; notes Việt 12 phút gồm demo 1 phút, năm câu hỏi vấn đáp.
- README ba bước, REQUIREMENTS mapping, WORKLOG quá trình, QA và audit rubric.
- Bảy tests, notebook kernel mới, verifier số liệu và Office; kiểm công thức dự đoán độc lập ở stored units.
- Render/xem từng trang report/slide; kiểm thêm PDF slide vì native charts có thể khác giữa renderer.
- Giải nén candidate sang thư mục mới; tests/notebook/verifier; so toàn bộ 24 CSV và summary với atol 1e-10. Loại môi trường/cache/QA renders khỏi ZIP. Có bản tổng và bốn review ZIP theo MSSV.

## Dữ kiện còn chờ

Video **7–15 phút**, nộp trước hết **21/10/2026**; URL thật ở slide 2. Report/code **23:55 ngày 22/10/2026 giờ Việt Nam**; mỗi sinh viên tự nộp ZIP theo MSSV.

Người dùng chưa có URL/thời lượng video. Tỷ lệ **đề xuất** theo yêu cầu: 30%–25%–25%–20%; việc làm/mức hoàn thành thực tế cần nhóm xác nhận. Không tạo chữ ký hay lịch sử hoàn thành. Có dữ kiện thì cập nhật project.json/notes slide 2, build/render/verify lại, cập nhật receipt và chạy `package_submission.py --release`.

Trạng thái và bằng chứng cuối: WORKLOG.md và results/QA_CHECKS.md. Kế hoạch không thay thế kết quả kiểm thử.
