# TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG — KHOA CÔNG NGHỆ THÔNG TIN

**PHIẾU THẨM ĐỊNH NỘI BỘ — KHÔNG PHẢI ĐIỂM GIẢNG VIÊN**  
Học phần: Data Analysis and Visualization, Theory N4, Endterm.  
Đề tài: Abalone Measurements and Shell Rings.  
Giảng viên: Cô Ho Thi Linh, Ph.D.  
Nhóm: VibeCoding_Expert — NGO LAM TIEN 524H0195; NGUYEN CONG THANH 524H0191; NGUYEN LE NHAT TAM 524H0186; NGO BINH MINH 524H0169.  
Ngày review: 20/10/2026. Chuẩn kiểm: rubric trong ảnh đề và TDTU_GRADING_STANDARD.md.

## Bảng điểm tham khảo phần kỹ thuật

Điểm dưới là ước lượng thận trọng để chuẩn bị bảo vệ, dựa trên sản phẩm/code đã kiểm. Không thay rubric của cô, không tính như đã hoàn thành video và không bảo đảm điểm cuối kỳ. Điểm chính thức **chưa có**.

| Tiêu chí đúng trọng số đề | Tối đa /10 | Ước lượng nội bộ | Bằng chứng và phần còn phải bảo vệ |
|---|---:|---:|---|
| Mô tả và trực quan hóa | 1,50 | 1,40 | Schema, missing/trùng, mô tả, IQR, nhiều loại hình và lý do; một số panel phải đọc lớn, Height/Cook có cực trị làm nén vùng trung tâm |
| Phân phối xác suất | 1,50 | 1,45 | Hai biến, ba ứng viên, tham số/refit/AD/Holm, histogram/KDE/Q–Q; 1.999 mô phỏng chỉ xác định được sàn p = 0,0005 |
| Kiểm định giả thuyết | 1,50 | 1,45 | t/Chi-square/ANOVA, H0/H1/df/CI/effect size/post-hoc; nguồn thiếu site ID nên giả định độc lập chỉ có thể nêu, không xác nhận |
| Tương quan | 1,50 | 1,45 | Pearson/Spearman/ties/pairwise n, hai heatmap/scatter; chưa lượng hóa khoảng bất định của correlation, diễn giải giữ ở mức khám phá |
| Hồi quy đa biến | 2,00 | 1,85 | Lý thuyết, 3 mô hình, CV/test, HC3/VIF/BP/Cook; có nonconstant variance và một dự đoán ngoài miền, chưa có external validation |
| Code, tái lập và tổ chức dự án | 2,00 | 1,90 | 7 tests, 17 code cells, manifest, phương trình dự đoán độc lập, runbook/lockfile/allowlist ZIP; kiểm thực thi trong một môi trường Linux, không giả là đã thử máy cô |
| **Tổng phần kỹ thuật tham khảo** | **10,00** | **9,50** | **Mức Giỏi/Xuất sắc dự kiến về kỹ thuật; điều kiện nộp còn chờ** |

Một số giới hạn trên là giới hạn dữ liệu/phạm vi kiểm chứng, không phải kết luận triển khai sai. Việc cô có trừ điểm hoặc yêu cầu thêm phụ thuộc cách chấm và phần giải thích của nhóm.

## Tổ chức thư mục và tái lập

`report/`, `slides/`, `notebooks/`, `src/`, `tests/`, `data/`, `results/`, `references/`, `tools/` tách vai trò rõ; README cài/chạy trong ba bước, 56 dependencies khóa phiên bản. Raw nhỏ có thể giữ kèm để offline. `.venv`, `.build`, QA renders/cache và ZIP khác không thuộc allowlist gói. Script kiểm CRC/tên/path/hash mỗi gói, giải nén và chạy lại phân tích.

Xem kết quả thực ở `QA_CHECKS.md`, `package_verification.json`, `reproduction_log.txt`. Không lấy JEV ratio 1,0/total 0 làm bằng chứng coverage; công cụ trả insufficient evidence.

## Số liệu và liêm chính học thuật

- Raw 4.177 × 9, không tạo/sửa dữ liệu để cải thiện p hoặc metric. Chỉ hai ô Height không hợp lệ đổi NaN, có chỉ số nguồn.
- Tách train/test trước phát triển; median/scaling nằm trong CV. Age suy từ Rings không vào X. Cook sensitivity giữ nguyên validation. Verifier tính lại metric và kiểm Xβ ở stored units độc lập với pipeline dự đoán.
- Full test RMSE **2,2509**, MAE **1,5996**, R² **0,5259**; baseline RMSE **3,2693**. Không gọi đó là độ chính xác phần trăm hay causal effect.
- Report ghi nguồn dataset/phương pháp và việc hỗ trợ soạn/code. Không nhận là nhóm tự thu thập hiện trường; không tạo chữ ký, video hoặc completion records.

## Thể thức và thuyết trình

Đã kiểm report 33 trang, hai bìa, front matter Roman liên tục, header giữa, A4/lề/TNR theo chuẩn, 9 OMML thật, 10 hình màu/13 bảng, TOC/LOF/LOT 54 mục. References/bìa không nằm TOC đúng yêu cầu riêng của đề. Hai file tham chiếu gốc không đổi.

Slide hình/biểu đồ màu, nền/chữ/bảng thông thường trắng đen và logo gốc, 19 trang, 6 native charts/workbooks, 5 tables, notes Việt; native finalizer pass và 0 cảnh báo layout. Đã xem native render/PDF; không nhận là đã chạy PowerPoint thật. Kịch bản 12 phút có demo 1 phút và phụ lục dự phòng; năng lực trình bày/vấn đáp của nhóm chưa được đánh giá.

## Năm câu hỏi phản biện

1. Vì sao chỉ 3.341 mẫu vào kiểm định khi raw có 4.177? Thiết kế holdout bảo vệ điều gì và không bảo vệ điều gì?
2. Cả ba ứng viên phân phối bị bác bỏ thì Welch/OLS có vô hiệu không? Phân biệt predictor cận biên và residual có điều kiện.
3. Vì sao age = Rings + 1,5 gây leakage? Vì sao M/F/I không thể gán ordinal 0/1/2?
4. Tương quan khối lượng dương mà conditional slope âm có nhất thiết là bug? VIF/HC3 giải quyết được phần nào?
5. Vì sao không xóa hết 212 cờ Cook hoặc clip/round để cải thiện metric? Validation phải nằm ở đâu khi screen ảnh hưởng?

Ý trả lời cụ thể: `slides/Viva_VI.md`. Nhóm phải hiểu và tự giải thích, không chỉ đọc thuộc.

## Quyết định review

Phần phân tích và tài liệu đủ để nhóm đọc, kiểm và quay video. **Chưa công nhận sẵn sàng nộp cuối**: thiếu URL/thời lượng video thật và xác nhận phần việc/tỷ lệ/completion thực tế. Dataset đã được người dùng xác nhận. Bảng 30/25/25/20 là đề xuất theo yêu cầu; chưa tự nhận hoàn thành 100%.

Sau khi cập nhật dữ kiện, build/render/verify lại và tạo bốn release ZIP đúng MSSV; từng sinh viên tự nộp. Không có điểm chính thức hoặc bảo đảm 10/10 trong biên bản này.
