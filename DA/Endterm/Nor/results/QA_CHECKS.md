# Kiểm chứng bản review — 20/10/2026

**Phạm vi:** DAV Endterm Theory N4, UCI Abalone. Đây là bản review dùng để đọc và quay video; chưa đủ dữ kiện bên ngoài để nộp chính thức.

## Dữ liệu và thống kê

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Nguồn thực tế, tối thiểu 500 dòng/5 biến | PASS: 4.177 × 9, khác danh sách cấm | `references/dataset_source.json`, ảnh đề/danh sách loại |
| Raw giữ nguyên | PASS: SHA-256 khớp giá trị cố định | `results/summary.json`, `tools/verify_project.py` |
| Missing/duplicate | 0 missing gốc, 0 duplicate; hai Height = 0 thành NaN | `tables/quality_audit.csv` |
| Không sửa cột ngoài quy tắc | PASS: chỉ hai ô Height, giữ toàn bộ dòng | Verifier so DataFrame với raw |
| Holdout | PASS: 3.341/836, stratify, seed 42, không giao nhau | `data/processed/split.csv` |
| Kiểm định phân phối | Ba AD Monte Carlo 1.999/refit; Holm đúng | `tables/distribution_tests.csv` |
| t/Chi-square/ANOVA | Có câu hỏi, H0/H1, giả định, df/p/CI/effect size | Report chương 4, notebook phần 3 |
| Holm và số học thống kê | PASS: fixtures + đối chiếu lại | `tests/test_analysis.py`, verifier |
| Pearson/Spearman | Hai ma trận và pairwise n, ties được xử lý | `tables/*matrix.csv`, `correlation_n.csv` |
| Rò rỉ dữ liệu | PASS trong pipeline đã kiểm: median/scaling/encoding chỉ fit train/fold | Test preprocessing, notebook CV/sensitivity |
| Hồi quy | Baseline/compact/full, cùng CV 5 fold, holdout cuối | `tables/cv_*`, `test_metrics.csv` |
| Dự đoán độc lập | PASS: X ở stored units × coefficient khớp CSV, atol 1e-10 | Verifier, `full_coefficients_stored_scale.csv` |
| Chẩn đoán | Rank/VIF/HC3/BP/residual/Cook; sensitivity chỉ inner train | `tables/training_diagnostics.csv`, sensitivity CSV |
| Bảy unit tests | PASS: sáu phép kiểm phân tích và một metadata | Log tái lập khi đóng gói |
| Notebook đã chạy | PASS: 26 cells, 17 code, execution 1–17, không error | Notebook có outputs và verifier |
| Tính nhất quán artifacts | PASS: raw/tables/figures được kiểm manifest | `manifest.json` |

Không áp dụng numerical gradient checking: bài dùng hồi quy OLS thư viện, không tự cài gradient descent. Thay vào đó đã kiểm phương trình dự đoán độc lập, rank và metrics.

## Tài liệu và hình thức

- **Report 33 trang:** hai bìa không số, sáu trang đầu i–vi, thân bài 1–25; số ở header giữa. A4, Times New Roman 13, line spacing 1,5, lề trái/phải/trên/dưới 3,5/2/3,5/3 cm.
- Có 7 chương, 9 phương trình OMML thật, 10 hình, 13 bảng; TOC/LOF/LOT gồm 54 mục tham chiếu. Cache cập nhật từ hai lượt render đã ổn định; bìa/references không vào TOC.
- Đã xem từng trang render cuối, kiểm font, caption, hình, bảng và ngắt trang. Các trang không đổi được đối chiếu PNG giống byte với bản đã xem; những trang thay đổi được xem lại.
- Hình report có màu, chữ và bảng thông thường đơn sắc. Hai heatmap tách riêng, miền −1 đến 1 có tâm 0. Đã cập nhật chuẩn TDTU dùng chung theo yêu cầu.
- **Slide 19 trang:** 16 chính + 3 phụ lục, 19 notes tiếng Việt, logo màu gốc mọi trang; hình/biểu đồ có màu, nền/chữ/bảng thường trắng đen; 6 native charts kèm 6 Excel workbooks, 5 native tables. Không dùng ảnh chụp công thức.
- Native finalizer: package/import/font/chart gates PASS, **0 layout warnings**. Đây là kiểm cấu trúc và renderer, không phải chứng nhận Microsoft PowerPoint thật.
- Đã xem toàn bộ slide native render và **19 trang PDF xuất qua LibreOffice**. Đã sửa nhãn heatmap chồng và density series bị bỏ khi độ dài series không bằng nhau; số liệu gốc không thay đổi.
- Script có tổng thời gian dự kiến **720 giây**, gồm demo 60 giây. Thời gian thật chưa được xác nhận.
- Hai file gốc `Template_EN.docx` và `524H0195_524H0191.pdf` giữ nguyên SHA-256; logo đúng asset gốc.

Hash bốn tài liệu cuối và số lượng cấu trúc: `office_verification.json`. Biên bản native: `presentation_validation.json`; pagination: `report_pagination.json`. Ảnh QA riêng nằm `.build/qa/`, không nén vào bài.

## Tái lập và vệ sinh gói

Trạng thái chạy giải nén cuối: **PASS**: 7 tests, 17 code cells, 24 CSV và structured summary khớp sau giải nén; xem receipt/log bên dưới.

`tools/package_submission.py` chỉ chọn README/PLAN/WORKLOG/REQUIREMENTS, metadata/requirements và các thư mục sản phẩm cần thiết. Candidate được giải nén vào thư mục tạm mới; chạy bảy tests, toàn bộ notebook trong kernel mới, verifier và so **24 CSV + structured summary** với atol 1e-10. Môi trường dependencies dùng bản locked đang cài; không nhận là đã thử hệ điều hành khác.

ZIP có một thư mục gốc, kiểm CRC, đường dẫn, tên trùng, byte nội dung với source; loại `.venv`, `.build`, cache, pyc, file khóa Office và rác hệ điều hành. Raw chỉ khoảng 187 KiB, phù hợp giữ kèm để chạy offline. Không nén archive lồng nhau.

Kết quả thực của lượt giải nén lưu `package_verification.json` và `reproduction_log.txt`; chỉ coi PASS khi receipt có status pass.

## Giới hạn công cụ và điều kiện nộp

JEV 2.0.0 local configured, nhưng `judge coverage` trả `INSUFFICIENT_EVIDENCE` với total 0, không nhận diện requirement/rule files. Không coi ratio 1,0 là coverage 100%. Việc đối chiếu yêu cầu dựa trên `REQUIREMENTS.md`, mã thực thi và kiểm tra tài liệu ở trên.

Dataset đã được người dùng xác nhận. Còn chờ **URL YouTube, thời lượng thật và xác nhận phần việc/tỷ lệ/mức hoàn thành thực tế**. Vai trò và tỷ lệ 30/25/25/20 trong report hiện là đề xuất theo yêu cầu người dùng. Không biến chúng thành bằng chứng đã hoàn thành.

Chưa kiểm trên Microsoft PowerPoint/máy chiếu, chưa diễn tập thực, quay/upload video hoặc nộp Elearning. Hạn video hết 21/10/2026; report/code 23:55 ngày 22/10/2026 giờ Việt Nam. Mỗi sinh viên tự nộp bản ZIP mang MSSV của mình sau khi cập nhật thông tin thật.

## Kiểm tra bổ sung sau cập nhật màu slide

- Skill TDTU: hình/biểu đồ/heatmap/sơ đồ có màu, ảnh/logo giữ màu gốc; phần nền/chữ/công thức/bảng thông thường đơn sắc. Validator skill PASS; JEV rules check builder PASS.
- Bảy slide hình/biểu đồ 5, 6, 7, 8, 11, 12, 14 có màu ở native và PDF render, đã xem từng trang thay đổi. Mười hai slide còn lại giống byte với PNG đã review.
- Dữ liệu/cache/formula của sáu chart và 19 notes giữ nguyên; report hashes không đổi. Native finalizer PASS, 0 layout warnings. Bằng chứng: slide_color_verification.json và presentation_validation.json.
- ZIP review được làm mới từ source hiện tại. Không chạy lại thống kê vì chỉ đổi style; receipt tái lập phân tích trước vẫn áp dụng cho cùng dữ liệu/mã phân tích.
