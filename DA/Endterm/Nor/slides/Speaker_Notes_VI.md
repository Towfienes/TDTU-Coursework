# Lời thoại và notes tiếng Việt

16 slide chính dự kiến 720 giây = 12 phút; 3 phụ lục không tính trong video. Chưa có xác nhận đã diễn tập.

## Slide 1 — Data Analysis and Visualization

Thời lượng dự kiến: 25 giây.
Kính chào Cô và các bạn. Nhóm VibeCoding_Expert trình bày bài cuối kỳ lý thuyết lớp N4, môn Phân tích và Trực quan hóa Dữ liệu. Đề tài là phân tích các phép đo bào ngư và số vòng vỏ. Chúng em sử dụng một bộ dữ liệu công khai xuyên suốt các phần: khám phá dữ liệu, phân phối xác suất, kiểm định, tương quan và hồi quy đa biến. Mục tiêu là hiểu dữ liệu và đánh giá dự đoán, đồng thời chỉ ra giới hạn của phương pháp.
Nguồn: Executed notebook and results/summary.json.

## Slide 2 — Report video

Thời lượng dự kiến: 15 giây.
Đây là liên kết video báo cáo chính thức của nhóm trên YouTube theo đúng quy định của đề bài: https://youtu.be/D-H3yQ4IDro?si=VZ5VouVBJcCDhlBc. Thời lượng video đáp ứng chuẩn từ 7 đến 15 phút theo yêu cầu của Khoa; các slide phụ lục dùng để hỗ trợ phần phản biện vấn đáp.
Nguồn: Executed notebook and results/summary.json.

## Slide 3 — Dataset and research questions

Thời lượng dự kiến: 40 giây.
Dữ liệu Abalone được Nash và cộng sự công bố, hiện lưu trên UCI. Có 4.177 quan sát, tám biến đầu vào và biến mục tiêu Rings. Ba nhóm M, F, I lần lượt biểu thị đực, cái và cá thể non; vì thế I không phải một giới tính thứ ba. Nguồn cho biết các phép đo liên tục đã được chia tỷ lệ. Chúng em giữ nguyên giá trị lưu trữ và ghi rõ trên trục, không tự đổi thành đơn vị vật lý. Từ một nguồn này, chúng em hỏi phân bố có hình dạng gì, các nhóm khác nhau thế nào, phép đo nào liên hệ với số vòng và mô hình tuyến tính dự đoán được đến đâu.
Nguồn: Nash et al.(1994), https://doi.org/10.24432/C55C7W; retained abalone.names.

## Slide 4 — Quality checks and holdout design

Thời lượng dự kiến: 45 giây.
Đầu tiên, chúng em đọc file không có header và kiểm đủ chín cột. Dữ liệu gốc không thiếu và không trùng toàn dòng, nhưng hai giá trị chiều cao bằng không không thể hiện một độ dày vỏ hợp lệ. Chúng em lưu chỉ số dòng và chuyển riêng hai ô đó thành thiếu; không sửa dữ liệu gốc. Dữ liệu được chia 80 phần trăm huấn luyện và 20 phần trăm kiểm tra, phân tầng theo nhóm với seed 42. Cụ thể có 3.341 dòng train và 836 dòng test. Các bước điền median, chuẩn hóa và kiểm ảnh hưởng chỉ học trong train hoặc từng fold; test được giữ để đánh giá cuối.
Nguồn: Executed notebook and results/summary.json.

## Slide 5 — Distribution of recorded length

Thời lượng dự kiến: 45 giây.
Histogram này cho thấy hình dạng phân bố chiều dài trong tập train. Trung bình khoảng 0,524 và độ lệch chuẩn khoảng 0,120 theo thang lưu trữ. Biểu đồ giúp nhìn lệch, đuôi và vùng tập trung; nó không tự chứng minh dữ liệu chuẩn. Trong notebook, chúng em còn dùng histogram và KDE cho khối lượng, chiều cao và số vòng. KDE chỉ là đường làm trơn cho biến liên tục; Rings là biến đếm nên giữ các mức nguyên. Đây là lý do không dùng duy nhất một loại biểu đồ cho mọi câu hỏi.
Nguồn: Notebook1; exported length histogram, 25 equal-width bins.

## Slide 6 — Length differs across recorded groups

Thời lượng dự kiến: 45 giây.
Biểu đồ cột so sánh chiều dài trung bình và ghi cỡ mẫu của từng nhóm. Nhóm I có nghĩa là cá thể non, nên sự khác biệt với hai nhóm còn lại có thể phản ánh giai đoạn phát triển. Chúng em dùng thêm boxplot trong report để nhìn trung vị, độ phân tán và các điểm cực trị, còn hình mean có khoảng tin cậy để thể hiện mức bất định. Những cách nhìn này bổ sung nhau. Không thể từ hình này kết luận giới tính gây ra kích thước khác nhau, vì nhóm tuổi và cách lấy mẫu còn liên quan.
Nguồn: Executed notebook and results/summary.json.

## Slide 7 — Length against a Normal candidate

Thời lượng dự kiến: 50 giây.
Với Length, chúng em đặt trước ứng viên Normal. Đường xám nối mật độ quan sát tại các tâm bin; đường đen là mật độ chuẩn với tham số ước lượng từ train. Ngoài hình này, report có Q–Q plot để xem độ lệch ở các phân vị. Kiểm định Anderson–Darling dùng 1.999 mẫu mô phỏng, ước lượng lại trung bình và độ lệch chuẩn trong mỗi mẫu. Cách này tính đến việc tham số chưa biết trước. Kết quả AD khoảng 29,40, p sau Holm là 0,0015, nên bác bỏ ứng viên ở mức 5 phần trăm. P gốc nằm ở sàn độ phân giải 0,0005; không được viết bằng không.
Nguồn: Notebook2; SciPy1.15.3 goodness_of_fit documentation.

## Slide 8 — Weight and candidate distributions

Thời lượng dự kiến: 45 giây.
Biến quan trọng thứ hai là whole weight, luôn dương. Chúng em so sánh hai ứng viên Normal và Lognormal, trong đó Lognormal tương đương kiểm tính chuẩn của log trọng lượng khi location được cố định bằng không. Cả hai đều bị bác bỏ sau điều chỉnh Holm. Việc log biến không tự động làm phân phối phù hợp. Ba p-value bằng nhau trong bảng do đều chạm sàn Monte Carlo, không có nghĩa ba mức sai khác như nhau. Kết luận đúng là các mô hình phân phối đơn giản này chưa mô tả đầy đủ dữ liệu trộn nhiều nhóm; chúng em không tiếp tục tìm đến khi có p đẹp.
Nguồn: Notebook2; exported fitted densities and observed bin densities.

## Slide 9 — Three prespecified hypothesis tests

Thời lượng dự kiến: 65 giây.
Tiếp theo là ba câu hỏi kiểm định đã định trước. Thứ nhất, Welch t-test hai phía kiểm trung bình Rings giữa M và F, cho phép phương sai khác nhau. Thứ hai, Chi-square kiểm độc lập giữa nhóm và dải Rings 1 đến 8, 9 đến 10, từ 11 trở lên; các dải này xuất hiện trong codebook, không được nhận là ngưỡng tuổi sinh học chính thức. Thứ ba, Welch ANOVA kiểm trung bình Length của cả ba nhóm. ANOVA cổ điển dùng tỷ số mean square giữa nhóm và trong nhóm với giả định phương sai chung; Welch điều chỉnh khi phương sai khác nhau. Chúng em đặt alpha bằng 0,05 và dùng Holm cho ba câu hỏi chính. Mọi phương pháp vẫn cần giả định độc lập; dữ liệu thiếu site và batch ID nên giới hạn này còn tồn tại.
Nguồn: Notebook3; SciPy Welch t-test, statsmodels anova_oneway.

## Slide 10 — Results and effect magnitude

Thời lượng dự kiến: 50 giây.
Cả ba kiểm định chính đều bác bỏ giả thuyết không sau Holm, nhưng cần đọc cả độ lớn. Chênh lệch Rings trung bình M trừ F khoảng âm 0,355 vòng; khoảng tin cậy 95 phần trăm từ âm 0,606 đến âm 0,103. Chênh lệch này nhỏ hơn nhiều độ biến động giữa từng cá thể. Chi-square có Cramér V khoảng 0,372, và tần số kỳ vọng nhỏ nhất khoảng 334,7 nên không gặp bảng thưa. Welch ANOVA cho thấy Length khác nhóm; report tiếp tục so từng cặp với Holm riêng sau phép kiểm tổng thể. Những p rất nhỏ là bằng chứng thống kê trong mẫu, không phải xác suất giả thuyết không đúng và không chứng minh nguyên nhân.
Nguồn: Executed notebook and results/summary.json.

## Slide 11 — Pearson and Spearman associations

Thời lượng dự kiến: 45 giây.
Pearson đo liên hệ tuyến tính, còn Spearman đo liên hệ thứ hạng đơn điệu. Rings có nhiều giá trị bằng nhau nên Spearman dùng hạng trung bình cho ties. Chúng em tính hai ma trận trên biến số gốc và không mã hóa M, F, I thành thứ tự giả. Trên slide là Spearman; report có cả hai heatmap màu, số cụ thể và cỡ mẫu theo cặp. Shell weight có liên hệ thứ hạng với Rings khoảng 0,693, còn Pearson khoảng 0,628. Đây là tương quan cận biên, không phải độ quan trọng độc lập trong mô hình nhiều biến.
Nguồn: Executed notebook and results/summary.json.

## Slide 12 — Shell weight and Rings

Thời lượng dự kiến: 40 giây.
Scatter này giúp đọc ý nghĩa của hệ số tương quan. Shell weight tăng thường đi cùng số vòng tăng, nhưng nhiều cá thể có cùng trọng lượng gần nhau vẫn có Rings khác nhau. Các điểm chồng vì Rings là số nguyên; notebook có độ trong suốt và đường fit mô tả. Mối liên hệ có thể đơn điệu hơn là tuyến tính hoàn hảo, phù hợp với việc Spearman cao hơn Pearson. Chúng em cũng thấy chiều dài và đường kính chia sẻ thông tin kích thước, gợi ý đa cộng tuyến. Shell weight là phép đo thành phần; không nên mô tả toàn bộ quy trình là không phá hủy mẫu.
Nguồn: Executed notebook and results/summary.json.

## Slide 13 — Multiple linear regression design

Thời lượng dự kiến: 60 giây.
Mô hình hồi quy tuyến tính đa biến mô tả Rings bằng intercept và tổng các đóng góp beta nhân predictor. Baseline chỉ dự đoán trung bình train. Mô hình gọn dùng nhóm, ba kích thước và trọng lượng toàn phần; mô hình đầy đủ dùng tám đầu vào gốc. Nhóm được mã hóa bằng hai dummy, lấy F làm tham chiếu. Median và scaler đều được fit mới trong mỗi fold. Chúng em dùng năm fold giống nhau cho các phương án, rồi đánh giá các mô hình đã định trên test. Biến tuổi tính từ Rings cộng 1,5 bị loại khỏi đầu vào vì chứa trực tiếp đáp án. Hệ số được diễn giải trên thang chuẩn hóa, còn CSV có thêm hệ số theo thang lưu trữ để kiểm phương trình.
Nguồn: Notebook5; scikit-learn1.6 common pitfalls and pipeline documentation.

## Slide 14 — Holdout performance and model limits

Thời lượng dự kiến: 65 giây.
Trên 836 dòng test, baseline có RMSE khoảng 3,27 vòng, compact khoảng 2,58 và full khoảng 2,25. Như vậy full giảm RMSE khoảng 31,1 phần trăm so baseline, với MAE khoảng 1,60 vòng và R bình phương khoảng 0,526. Chúng em tính bằng dự đoán liên tục gốc, không làm tròn hay cắt miền để cải thiện metric. Có một dự đoán ngoài miền Rings quan sát. Chẩn đoán trên train cho thấy VIF cao và phương sai phần dư không hằng; vì vậy dùng HC3 cho khoảng tin cậy hệ số, nhưng HC3 không sửa quan hệ phi tuyến. Có 212 dòng vượt ngưỡng Cook 4 trên n. Phân tích độ nhạy chỉ lọc inner train và giữ validation, còn mô hình chính giữ các dòng này.
Nguồn: Executed notebook and results/summary.json.

## Slide 15 — Reproducible code demonstration

Thời lượng dự kiến: 60 giây.
Trong một phút demo, trước hết em mở notebook mục một để chỉ checksum nguồn và bảng chỉ số train, test đã lưu. Tiếp theo ở mục ba, em chỉ bảng kiểm định, p Holm và khoảng tin cậy chênh lệch M trừ F. Điều này cho thấy kết luận không chỉ lấy từ một p-value. Ở mục năm, em mở pipeline gồm imputer, scaler và hồi quy bên trong vòng lặp cross validation, rồi chỉ CSV dự đoán test. Cuối cùng, em mở summary để chứng minh report và slide cùng đọc kết quả đã xuất, không tính lại theo một cách khác. Nếu chạy trực tiếp gặp lỗi, nhóm dùng ngay output đã lưu; không cài thư viện hoặc tải nguồn trong lúc quay.
Nguồn: Executed notebook and results/summary.json.

## Slide 16 — Conclusions and limitations

Thời lượng dự kiến: 25 giây.
Ba kết luận chính là: các phân phối ứng viên bị bác bỏ; nhóm và phép đo có liên hệ với Rings; hồi quy đầy đủ cải thiện dự đoán nhưng còn sai số đáng kể. Lấy mẫu lịch sử, thiếu site ID, đa cộng tuyến và hình dạng phần dư hạn chế việc khái quát. Chúng em không suy từ liên hệ và hiệu quả dự đoán sang nguyên nhân sinh học.
Nguồn: Executed notebook and results/summary.json.

## Slide 17 — Appendix: definitions and inference

Thời lượng dự kiến: phụ lục dự phòng.
Phụ lục dùng khi vấn đáp. Giải thích Welch t là chênh lệch trung bình chia sai số chuẩn cho phép hai phương sai khác nhau; Chi-square cộng (O−E) bình phương trên E; ANOVA cổ điển là mean square giữa chia trong nhóm. Holm kiểm soát ba giả thuyết chính. Khoảng tin cậy Welch trong bảng là 95 phần trăm riêng lẻ; chỉ p-value được điều chỉnh gia đình. P-value không phải xác suất H0 đúng.
Nguồn: Executed notebook and results/summary.json.

## Slide 18 — Appendix: regression diagnostics

Thời lượng dự kiến: phụ lục dự phòng.
Phụ lục chẩn đoán. Rank 10 trên 10 nghĩa thiết kế không suy biến chính xác, nhưng VIF cao vẫn phản ánh đa cộng tuyến. Breusch–Pagan có p khoảng 1,44 nhân 10 mũ âm 78. HC3 xử lý covariance dưới phương sai thay đổi, không sửa phụ thuộc cụm hay quan hệ phi tuyến. Cook là ảnh hưởng phụ thuộc mô hình, không phải chứng minh một quan sát sai. So hệ số sau sensitivity bằng thang gốc vì scaler đã thay đổi.
Nguồn: Executed notebook and results/summary.json.

## Slide 19 — References

Thời lượng dự kiến: phụ lục dự phòng.
Nguồn chính gồm bộ dữ liệu Nash và cộng sự trên UCI, codebook giữ nguyên, SciPy cho kiểm định và goodness of fit, statsmodels cho Welch ANOVA, HC3 và influence, scikit-learn cho pipeline và đánh giá. Phiên bản thực tế được khóa trong requirements và manifest. Nhóm cần dẫn nguồn, hiểu phương pháp và xác nhận đóng góp thực tế trước khi nộp.
Nguồn: Primary sources listed on this slide and in report References.
