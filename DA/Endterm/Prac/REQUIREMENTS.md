# Đối chiếu yêu cầu và bằng chứng

Đề gốc được giữ tại `references/assignment_part_I.png` đến `assignment_part_IV.png`.
Notebook: `notebooks/VibeCoding_Expert_DAV_Endterm_Analysis.ipynb`.
Mọi mục dưới đây được kiểm bằng output thực, không chỉ dựa vào việc có tên hàm trong source.

| Yêu cầu | Mục notebook | Bằng chứng/đầu ra | Mục report | Slide |
|---|---|---|---|---|
| Tải dữ liệu, đọc Pandas | I.1 | CSV gốc, checksum, metadata nguồn | 1.2, 2.1 | 3–4 |
| 5 dòng đầu/cuối | I.2 | Hai bảng head/tail đủ 5 dòng | 2.1 | 4 |
| shape, dtypes, info | I.2 | 649×33, bảng dtype, output info | 2.1 | 4 |
| Giả lập 5% một cột số | I.3 | 32 ô absences, seed 42, mask CSV | 2.2 | 5 |
| isnull().sum mỗi cột | I.3 | Missing trước/sau và hai nhánh | 2.2–2.3 | 6 |
| Mean imputation | I.3 | mean_imputed.csv, còn 649 dòng | 2.3 | 6 |
| dropna, so sánh shape | I.3 | drop_missing.csv, còn 617 dòng, missing_comparison.csv | 2.3 | 6 |
| Series → list, lọc Python | I.4 | List comprehension, count 549, đối chiếu mask | 2.4 | 7 |
| Regular expression | I.4 | fullmatch G[123], kiểm cả tên không hợp lệ | 2.4 | 7 |
| loc lấy 10 dòng đầu | II.1 | loc[:9], output và assert số dòng | 3.1 | 8 |
| iloc lấy tập cột | II.1 | Vị trí school/age/G1/G2/G3, output | 3.1 | 8 |
| Lọc điều kiện hai cột | II.1 | 334 dòng, 51,46%, two_condition_filter.csv | 3.1 | 8 |
| Tạo ít nhất 3 cột | II.2 | Mean điểm trước, progress, performance_band | 3.2 | 9 |
| Dùng insert | II.2 | prior_grade_mean ngay trước G3, có assert vị trí | 3.2 | 9 |
| Ma trận corr | II.3 | Pearson 16×16, pearson_matrix.csv | 3.3 | 11, notes |
| Group count/mean/std/min/max điểm | II.3 | Cả G1/G2/G3 theo trường, school_grade_statistics.csv | 3.4 | 10 |
| Grouping/aggregation quan hệ biến | II.3 | G3 theo studytime/failures/higher, CSV từng nhóm | 3.4 | 10, 14 |
| Chuẩn hóa trong nhóm | II.4 | groupby/transform, index và [0,1], fixture hằng | 3.5 | 10 |
| Histogram Seaborn/Pandas | III.1a | sns.histplot; Figure 01 | 4.1 | 12 |
| Box plot Seaborn | III.1b | sns.boxplot; Figure 02 | 4.2 | 13 |
| Bar plot Seaborn/Pandas | III.2a | sns.barplot, mean và n; Figure 03 | 4.3 | 14 |
| Pie của cột tạo ở II | III.2b | performance_band; Figure 04, count/% | 4.4 | 15 |
| Scatter, regression nếu Seaborn | III.3 | sns.regplot ci=None; Figure 05 | 4.5 | 16 |
| Core Matplotlib từ list/dict | III.4 | List/dict 5 dòng; plt.bar; Figure 06 | 4.6 | 17 |
| comprehensive_report | IV.1 | Hàm input df, in output, trả dict; summary.json | 5.1 | 18 |
| Top/bottom 10 đủ cột | IV.2a | Hai bảng đủ 37 cột và hai CSV đầy đủ | 5.2 | 18, 23–24 |
| Kết luận có thống kê và biểu đồ | IV.2b | Spearman tách prior/context, nhóm và hình | 5.3–5.4 | 20 |

## Điều kiện bổ sung đã chốt

- Báo cáo Word và PDF theo chuẩn TDTU; hai bìa, Roman/Arabic, công thức OMML, mục lục và danh mục hình/bảng.
- PowerPoint và PDF: 25 slide tổng, ngôn ngữ Anh, notes Việt, logo gốc giữ màu, thiết kế đơn sắc.
- Thuyết trình dự kiến 24,5 phút trước Q&A, gồm 3 phút demo; chưa coi lịch dự kiến là bằng chứng đã diễn tập.
- Đóng gói đúng chuỗi bốn MSSV, có code/dữ liệu nhỏ/hướng dẫn và không có môi trường ảo/cache.
- Phân công dự kiến không phải bằng chứng đóng góp thực tế; không gán phần trăm.
- Các kiểm tra, giới hạn và trạng thái cuối được ghi tại `results/QA_CHECKS.md` và `WORKLOG.md`.
