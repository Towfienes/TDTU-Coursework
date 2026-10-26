# Kiểm tra cuối — Endterm DAV

Ngày kiểm: 20/10/2026. Đây là bằng chứng kiểm tra nội bộ, không phải kết quả chấm của giảng viên.

| Phạm vi | Kết quả đã kiểm | Bằng chứng |
|---|---|---|
| Nguồn | UCI student-por.csv, 649×33, 0 ô thiếu, SHA-256 đúng | `references/dataset_source.json`, `manifest.json` |
| Missing | 32 ô absences khác nhau, seed 42; hai nhánh dùng cùng mask | Notebook I.3, `data/processed/missing_mask.csv` |
| Treatments | Mean: 649 dòng; dropna: 617; không còn missing; ô quan sát giữ nguyên | `tools/verify_project.py`, `tables/missing_comparison.csv` |
| Kiểm thử biên | 3 test qua: dải điểm và dữ liệu sai, index/nhóm hằng, summary rỗng/nhóm zero-count | `tests/test_analysis.py`, `reproduction_log.txt` |
| Notebook | 41 cell tổng, 20 cell code có execution count 1–20, không error, đủ 6 hình trong outputs | Notebook đã thực thi, `tools/verify_project.py` |
| Phần II–IV | Dùng raw đã kiểm; feature frame 649×37; top/bottom đúng 10 dòng, đủ 37 cột và stable ties | `data/processed/analysis_features.csv`, hai CSV top/bottom |
| Số liệu | Count/% đúng tổng; manifest khớp; tất cả 14 bảng CSV và structured summary khớp sau chạy lại | `package_verification.json` |
| Word/PDF | 31 trang: 2 bìa, 6 trang Roman, 23 trang Arabic; A4 và lề chuẩn; 3 OMML, 6 hình, 12 bảng | `office_verification.json`, `tools/verify_project.py` |
| Danh mục | TOC/LOF/LOT có 48 heading/caption, native PAGEREF/SEQ; mapping số trang ổn định sau 2 lượt | `office_verification.json`; công cụ `tools/update_fields.py` |
| PowerPoint | 25 slide, 25 notes Việt, logo gốc nhúng ở từng slide, 9 bảng native, 5 chart/workbook chỉnh sửa được | `office_verification.json`, native package/chart validators |
| Bố cục slide | Finalizer không có lỗi hoặc cảnh báo hình học; font Arial/DejaVu Sans Mono đúng chính sách | `office_verification.json` |
| Kiểm trực quan | Đã xem từng trang report và từng slide, cả render PPTX và PDF; sửa logo, bảng phụ lục, nhãn pie và tương phản scatter | Private renders trong `.build/qa/`, không nộp các ảnh QA |
| Tái lập sau giải nén | Tests → kernel mới → verifier đều qua trong thư mục tạm độc lập; sai số tuyệt đối tối đa 1e-10 cho đối chiếu số | `package_verification.json`, `reproduction_log.txt` |
| Môi trường | Python 3.12, 50 dependency đã khóa; `uv pip check` qua | `requirements.txt`, `manifest.json` |
| Gói nộp | Một folder theo bốn MSSV; CRC và đường dẫn ZIP được kiểm; không có venv/cache/Office lock/private build | `tools/package_submission.py` |
| Tài liệu gốc | Template và PDF chuẩn ở gốc TDTU giữ nguyên checksum | `office_verification.json` |

## Phạm vi của kiểm tra trực quan

Report cuối được render bằng công cụ Documents và xem đủ 31 trang. PPTX được import/render bằng Artifact Tool; bản PDF xuất bằng LibreOffice được xem đủ 25 trang. Khi chỉ sửa slide 15–16, render lại cả deck: các trang còn lại giống byte PNG đã kiểm; hai slide thay đổi được xem lại ở cả hai renderer. Không dùng contact sheet hoặc text extraction làm bằng chứng duy nhất.

Scatter trên PDF lúc đầu mất tương phản do marker trong suốt; bản cuối dùng marker xám đặc. Lần chạy lại với backend Agg lúc đầu không nhúng hình trong notebook; đã bật inline backend rõ ràng trong cell setup và kiểm lại thành công trong cùng điều kiện. Sáu PNG phân tích và toàn bộ bảng/summary không đổi; byte SVG có thể đổi vì metadata/ID do Matplotlib sinh.

## Giới hạn và việc nhóm cần làm

- Tái lập dùng thư mục giải nén và kernel mới với môi trường dependency đã cài đúng lock; chưa thử cài mới trên một hệ điều hành khác. Cài dependency cần mạng hoặc package cache; chạy phân tích dùng dữ liệu cục bộ.
- Chưa mở bằng ứng dụng Microsoft PowerPoint. Native package/import checks và hai renderer không thay thế việc thử trên máy trình chiếu thực tế; có PDF dự phòng.
- Thời lượng khoảng 24,5 phút là lịch dự kiến, chưa đo từ buổi tập của nhóm. Chưa xác nhận khả năng bảo vệ của từng thành viên.
- Kết luận là liên hệ quan sát chưa điều chỉnh đa biến; không phải tác động nhân quả. Chỉ một mask MCAR được mô phỏng. Ambiguity của failures được công bố và giữ nguyên dữ liệu.
- Không có mô hình dự đoán hay thuật toán tối ưu tự viết: train/test, cross-validation và gradient checking không áp dụng cho phạm vi đề này.
- Phân công là đề xuất; không có phần trăm đóng góp hoặc chữ ký tự tạo. Gói chưa được nộp lên Elearning.
