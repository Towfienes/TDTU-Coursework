# Nhật ký thực hiện — DAV Theory N4

Ngày thực hiện/báo cáo: **20/10/2026**, Asia/Ho_Chi_Minh. Thư mục `DA/Endterm/Nor`. Người dùng duyệt kế hoạch Astra rồi yêu cầu triển khai. Giữ nguyên bài thực hành `Prac/`.

## Hồ sơ và hợp đồng

Đọc handover, AGENTS, chuẩn report/grading TDTU, skill Documents/Presentations/tdtu-presentation/JEV/Ponytail. Giữ thông tin bốn tác giả/MSSV, Cô Ho Thi Linh, Ph.D., ngôn ngữ và ngày đã cung cấp. TDTU không phải Git repo: không có commit hay `.git/info/exclude`; không tự khởi tạo repo.

Đọc ảnh đề/rubric/dataset cấm, giữ trong references. Sáu mảng thống kê, tối thiểu 500 dòng/5 biến, video 7–15 phút, link ở slide 2, từng thành viên tự nộp và bảng đóng góp thực tế được ánh xạ trong REQUIREMENTS.md.

## Nguồn và môi trường

Chọn UCI Abalone sau khi loại danh sách cấm, Sentiment140 và Student Performance. Duyệt UCI và tài liệu chính thức SciPy/statsmodels/scikit-learn; lưu raw/codebook/DOI/CC BY 4.0/SHA-256. Người dùng đã xác nhận chấp nhận dataset, metadata đã cập nhật.

Tạo .venv Python 3.12, khóa 56 dependencies; uv pip check không phát hiện xung đột. Phân tích chạy offline với raw nhỏ kèm bài. Office dùng runtime riêng đã cài. Không nén môi trường.

## Triển khai thống kê

1. Raw **4.177 × 9**, không thiếu/trùng. Height = 0 ở chỉ số gốc **1257, 3996** đổi NaN trong bản xử lý; raw và các cột khác không đổi. Không tự sửa Height lớn hoặc xóa theo IQR.
2. Split seed 42 stratify M/F/I: **3.341 train / 836 test**, không giao nhau; hai Height thiếu đều train. N mô tả Height = 3.339, biến khác thường 3.341.
3. EDA có cấu trúc, thống kê mô tả, cờ IQR và nhiều kiểu hình. Dùng stored units đúng codebook, I là infant; không dùng age suy từ Rings làm predictor.
4. Ba AD Monte Carlo 1.999/refit: p đều ở sàn **0,0005**, Holm **0,0015**. Bác bỏ ứng viên đơn giản là kết quả hợp lệ; không thử thêm đến khi có p đẹp.
5. Welch Rings M−F, Chi-square nhóm × ring band, Welch ANOVA Length: có H0/H1/df/p Holm/CI/effect size/post-hoc. Expected nhỏ nhất **334,7**, fallback mô phỏng không cần cho bảng thực tế.
6. Pearson/Spearman và pairwise n; shell weight mạnh nhất trong biến đo gốc: **r = 0,628; rho = 0,693**. Không gọi tương quan là nhân quả hay importance mô hình.
7. Baseline/compact/full cùng CV 5 fold, preprocessing chỉ fit train tương ứng. Full holdout **MAE 1,5996; RMSE 2,2509; R² 0,5259**, baseline RMSE 3,2693. Một dự đoán ngoài 1–29 được công bố, không clip/round.
8. Rank 10/10, VIF cao, BP p rất nhỏ: dùng HC3 CI, residual/Q–Q, Cook và nêu hạn chế. **212** cờ Cook trên toàn train, mô hình chính giữ lại. Sensitivity chỉ fit/screen/refit inner train, validation không đổi; so slopes ở stored units vì scaler thay đổi sau lọc.

Notebook **26 cells / 17 code**, outputs đầy đủ; **24 CSV**, summary/manifest, **10 hình PNG/SVG**. src/analysis.py chia sẻ phép tính với tests; tài liệu đọc kết quả xuất, không tạo pipeline phân tích thứ hai.

## Tài liệu và sửa lỗi

Tái sử dụng helper dàn trang Prac sau khi kiểm codebase-memory. tools bị excluded khỏi graph, đã đọc source trực tiếp theo coverage gap; không suy kết luận từ graph thiếu coverage. Pipeline thống kê Nor riêng.

Cập nhật **TDTU_REPORT_STYLE.md dùng chung**: hình/ảnh/chart report màu, chữ/bảng thường đơn sắc; quy tắc mới nhất cho slide là hình/biểu đồ có màu, nền/chữ/bảng thường trắng đen và logo gốc. Giữ nguyên hai file tham chiếu gốc.

Report Word/PDF cuối **33 trang**: hai bìa + sáu Roman + 25 Arabic, bảy chương; **9 OMML, 10 hình, 13 bảng, 54 mục tham chiếu trang**. Sửa tab TOC thành w:tab thật, heading nhiều dòng căn trái, tách heatmap để đọc rõ, rút đoạn lặp để bỏ hai trang gần trống. References hanging indent/căn trái để URL không làm giãn chữ.

Slide **19 = 16 chính + 3 phụ lục**, sáu native charts/workbooks, năm native tables, notes Việt/logo mọi trang. Script 720 giây gồm demo 60 giây, không nhận là đã quay/diễn tập. Sửa nhãn heatmap tránh chồng tiêu đề. LibreOffice bỏ density series ngắn khi số điểm các series khác nhau; lặp sáu lần từng vertex của polygon 25 bins thành 150 điểm như đường fit, giữ nguyên hình học/số liệu; kiểm PDF lại.

## Kiểm chứng

Bảy tests: biên cleaning, Holm/Welch/Chi-square, preprocessing không học validation và metadata nộp bài. Verifier đối chiếu split/manifest/metrics, **công thức dự đoán độc lập** từ stored coefficients và train medians; kiểm OOXML/equations/fields/tabs/logo/notes/workbooks.

Xem từng trang report/slide render và PDF slide. Receipt ghi hash tài liệu, phân biệt renderer với Microsoft PowerPoint thật. Đóng gói theo allowlist; giải nén sang thư mục mới, tests/notebook/verifier trong kernel mới, so 24 CSV/summary ở atol 1e-10. Đã chạy PASS trong thư mục giải nén mới: bảy tests, 17 code cells, 24 CSV và summary khớp atol 1e-10. Receipt/log lưu results/package_verification.json và reproduction_log.txt.

JEV status hoạt động nhưng judge coverage trả **INSUFFICIENT_EVIDENCE**, không nhận diện rule/requirement files dù có truyền workspace. Không coi ratio 1,0 với total 0 là coverage 100%; dùng matrix/kiểm chứng native và ghi hạn chế trong QA.

## Bàn giao

Mở README/report PDF/slide PPTX để review và quay video. ZIP trong packages mang hậu tố **REVIEW**. URL/thời lượng video chờ người dùng; vai trò/tỷ lệ 30/25/25/20 là đề xuất, chưa xác nhận completion thực tế. Có dữ kiện thì cập nhật metadata/notes slide 2, build/render/verify, rồi tạo release ZIP theo MSSV.

Chưa mở PowerPoint trên máy chiếu, chưa quay/upload video hoặc nộp Elearning. Audit nội bộ bám rubric, không phải điểm giảng viên và không cam kết 10 điểm.

## Cập nhật màu slide theo yêu cầu mới

Người dùng yêu cầu cả hình/biểu đồ trong slide có màu; nền, chữ và bảng thông thường vẫn trắng đen. Đã cập nhật skill dùng chung .agents/skills/tdtu-presentation/SKILL.md, AGENTS.md và dẫn chiếu trong chuẩn report. Skill quick_validate PASS bằng môi trường uv có PyYAML; không thêm dependency vào môi trường phân tích. JEV rules check cho builder PASS (3 rules), không thay kết luận coverage trước đó.

Đã đổi màu slide 5/6/7/8/11/12/14, giữ palette nhóm/series nhất quán với report; heatmap có key miền −1 đến +1. So toàn bộ native chart numeric/category caches và formulas với bản cũ: không đổi; 19 notes không đổi. Xem từng slide thay đổi ở cả native/PDF; 12 slide còn lại PNG giống byte. Report và analytical outputs không thay đổi. Receipt mới: results/slide_color_verification.json; Office/native receipts và các review ZIP đã cập nhật. Không chạy lại toàn bộ thống kê cho thay đổi màu; lượt tái lập phân tích trước vẫn được giữ nguyên.


## Transcript học thuật và demo — 20/10/2026

Viết lại Speaker_Notes_VI.md cho 19 slide: lời nói hoàn chỉnh, thao tác màn hình riêng, giải thích lựa chọn phương pháp, độ lớn khác biệt, p-value/CI, Pearson/Spearman, R² và giới hạn HC3. Sửa mô tả màu đường phân phối cho khớp slide màu. Kế hoạch 16 slide chính là 780 giây (13 phút), gồm demo slide 15 khoảng 100 giây rồi quay lại slide 16. Phụ lục chỉ dùng khi trao đổi.

Demo_VI.md có năm đoạn lời thoại trùng chính xác slide 15, vị trí cell và execution count đối chiếu notebook, cùng hướng dẫn chống nhầm validation với test và phương án HTML offline. Đồng bộ hai file vào DEMO_NOR, cập nhật BAT_DAU_DEMO.md và packages/DEMO_NOR.zip. Kiểm tra 19 tiêu đề, tổng thời gian, năm vị trí cell, các số liệu RMSE/chia tập và các đường dẫn CSV; ZIP CRC và mọi file trong ZIP khớp thư mục.

Chỉ sửa transcript và gói demo; Notes nhúng trong PPTX vẫn bản trước, đã ghi rõ để người dùng đọc bản Markdown mới. Không chạy lại mô hình hoặc dựng lại Office vì không sửa phân tích/layout. Chưa diễn tập, đo thời lượng nói thực tế hay quay video. Các ZIP bài nộp REVIEW cũ chưa cập nhật transcript trong lượt này.


## Demo chia đúng sáu phần notebook — 21/10/2026

Theo yêu cầu mới, Demo_VI.md thay bằng sáu đoạn lời đọc theo đúng tiêu đề mục1–6 của notebook; mỗi đoạn có điểm dừng màn hình, In[n], từ khóa và thời gian. Tổng demo dự kiến120 giây; đồng bộ slide15 transcript và ngân sách toàn bài800 giây (13:20). Cập nhật DEMO_NOR, hướng dẫn bắt đầu và DEMO_NOR.zip. Đã kiểm sáu tiêu đề trùng notebook, lời thoại hai file khớp, tổng thời gian và ZIP CRC/toàn bộ bytes. Không sửa notebook, kết quả phân tích hoặc PPTX; Notes nhúng vẫn bản trước; chưa đo bằng diễn tập thực tế.
