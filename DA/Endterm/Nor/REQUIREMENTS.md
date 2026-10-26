# Yêu cầu → bằng chứng — Endterm Theory N4

Rubric chính thức: EDA15%, phân phối15%, kiểm định15%, tương quan15%, hồi quy20%, code20%. Không dùng điểm tự đặt thay rubric này.

| Yêu cầu | Notebook | Bằng chứng | Report | Slide |
|---|---|---|---|---|
| Một dataset thực tế, khác giữa kỳ/danh sách cấm | 1.1 | raw4177×9, codebook, dataset_source | 1.2 | 3 |
| ≥500 dòng, ≥5 biến | 1.1 | shape, schema assertions | 1.2 | 3 |
| Kiểu dữ liệu, thiếu và trùng | 1.1–1.2 | info/dtype, quality_audit | 2.1 | 4 |
| Mean, median, SD, quartiles | 1 | descriptive_train.csv | 2.2 | 5 |
| ≥3 loại biểu đồ và lý do chọn | 1 | histogram/KDE, box, bar, scatter | 2.2–2.3 | 5–6 |
| Ngoại lai và cách xử lý | 1, 5.6 | IQR rows/counts, Cook sensitivity | 2.3, 6.5 | 4, 14 |
| ≥2 biến phân phối | 2 | Length và Whole_weight | 3 | 7–8 |
| Kiểm tra phân phối đúng tham số ước lượng | 2 | AD MonteCarlo1999/refit/Holm | 3.2 | 7–8 |
| Lý thuyết t-test | 3 | Welch formula + assumptions | 4.1 | 9 |
| Lý thuyết Chi-square | 3 | independence/expected counts | 4.1 | 9 |
| Lý thuyết ANOVA | 3 | classic vsWelch | 4.1 | 9 |
| Câu hỏi, H0/H1, áp dụng và diễn giải | 3 | hypothesis_tests, WelchCI, posthoc | 4.2–4.4 | 9–10 |
| Pearson/Spearman lý thuyết | 4 | formulas, ties/ordinal discussion | 5.1 | 11 |
| Pearson/Spearman tính và hình | 4 | matrices, pairn, heatmaps/scatter | 5.2 | 11–12 |
| Ý nghĩa thực tiễn tương quan | 4, 6 | ranking, multicollinearity caveats | 5.3 | 12 |
| Lý thuyết hồi quy đa biến | 5 | OLS objective, dummies, assumptions | 6.1 | 13 |
| Xây dựng và đánh giá | 5 | baseline/compact/full, CV5/test | 6.2–6.4 | 13–14 |
| Giải thích và chẩn đoán mô hình | 5 | HC3/VIF/BP/Cook/residuals | 6.4–6.5 | 14, appendix |
| Python chạy được/chú thích/tái lập | all | fresh kernel, tests, CSV comparisons | 1.3 | 15 |
| Báo cáo Word/PDF rõ từng bước | all | report.docx/.pdf, native equations | all | — |
| Slide báo cáo và code | all | PPTX/PDF +notebook/src | — | all |
| Video7–15min, trước hết21/10 | — | Script12min; video thật chờ nhóm | 7.3 | 2 |
| URL video ở slide2 | — | project.json youtube_url; pending | — | 2 |
| Từng thành viên tự nộp | — | fourMSSVZIP sau xácnhận | README | notes |
| Phần việc/%đónggóp/%hoàn thành thật | — | project.json; proposed shares, actual completion pending | 7.3 | notes |
| Không bìa/References trongTOC | — | OOXML fields và PDFpageindex | front matter | — |
| Report hình màu, còn lại đơn sắc | — | standard TDTU updated, colorPNGs | all | slides: color visuals, monochrome framing |
| Gói nộp22/10/2026 lúc23:55VN | — | metadata, readiness check | README | notes |

Mức hoàn thành thực tế được ghi trong QA_CHECKS và WORKLOG. Dataset đã được người dùng xác nhận. URL/thời lượng video và đóng góp thực tế còn chờ; không tự tạo để vượt readiness gate.
