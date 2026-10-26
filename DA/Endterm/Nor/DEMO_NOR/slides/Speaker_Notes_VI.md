# Kịch bản thuyết trình học thuật — Abalone, DAV Theory N4

Bản lời thoại cập nhật ngày 20/10/2026. Dùng với `VibeCoding_Expert_DAV_Theory_Endterm_Presentation_REVIEW.pptx` gồm 16 slide chính và 3 slide phụ lục. Đây là bản transcript đọc riêng; phần Notes nhúng trong PPTX vẫn là bản trước. Khi luyện nói, dùng file này và `Demo_VI.md`.

**Cách sử dụng:** đọc phần “Lời trình bày”; các dòng “Thao tác” dành cho người điều khiển màn hình, không đọc thành lời. Ngắt nhẹ sau câu hỏi nghiên cứu và sau kết quả chính. Đọc tên biến một lần bằng tiếng Anh rồi dùng nghĩa tiếng Việt. Không đọc toàn bộ bảng, số mũ của p-value hoặc mã lệnh.

**Luồng trình bày:** slide 1–14 → slide 15 giới thiệu demo → chuyển sang notebook trong khoảng 120 giây, tính cả chuyển cửa sổ → trở lại slide 16 kết luận. Slide 17–19 dành cho trao đổi thêm, không nằm trong phần nói chính. Nội dung slide 15 dưới đây và trong `Demo_VI.md` là cùng một đoạn, chỉ nói một lần.

## Phân bổ thời gian dự kiến

| Slide | Nội dung | Thời gian | Mốc kết thúc |
|---|---|---:|---:|
| 1 | Giới thiệu | 25 giây | 00:25 |
| 2 | Trang video | 10 giây | 00:35 |
| 3 | Dữ liệu và câu hỏi | 45 giây | 01:20 |
| 4 | Chất lượng và thiết kế đánh giá | 50 giây | 02:10 |
| 5 | Phân bố chiều dài | 40 giây | 02:50 |
| 6 | So sánh các nhóm | 40 giây | 03:30 |
| 7 | Kiểm tra phân phối chuẩn | 55 giây | 04:25 |
| 8 | Phân phối khối lượng | 45 giây | 05:10 |
| 9 | Thiết kế kiểm định | 60 giây | 06:10 |
| 10 | Kết quả và độ lớn khác biệt | 55 giây | 07:05 |
| 11 | Pearson và Spearman | 45 giây | 07:50 |
| 12 | Quan hệ khối lượng vỏ và số vòng | 40 giây | 08:30 |
| 13 | Hồi quy đa biến | 65 giây | 09:35 |
| 14 | Đánh giá và chẩn đoán | 65 giây | 10:40 |
| 15 | Demo notebook theo 6 phần, gồm chuyển cửa sổ | 120 giây | 12:40 |
| 16 | Kết luận | 40 giây | 13:20 |

Đây là ngân sách thời gian để tập nói, chưa phải thời lượng video đo thực tế. Quay thử và giữ tổng video dưới 15 phút; nếu cần rút ngắn, bỏ bớt chi tiết chẩn đoán ở slide 14 và chuyển sang phụ lục 18.

## Slide 1 — Data Analysis and Visualization

**Thao tác:** dừng ở trang tiêu đề, nhìn người nghe trước khi bắt đầu.

**Lời trình bày:**

Kính chào Cô và các bạn. Nhóm VibeCoding_Expert xin trình bày bài cuối kỳ môn Phân tích và Trực quan hóa Dữ liệu, lớp lý thuyết N4.

Với bộ dữ liệu Abalone, chúng em tìm hiểu mối liên hệ giữa các phép đo cơ thể bào ngư và số vòng vỏ. Bài trình bày đi từ mô tả dữ liệu, kiểm định thống kê đến đánh giá hồi quy, nhằm trả lời câu hỏi: dữ liệu cho phép chúng ta kết luận điều gì, và những kết luận đó có giới hạn nào?

## Slide 2 — Report video

**Thao tác:** chuyển nhanh qua trang liên kết. Chỉ cập nhật URL sau khi có video thật; không đọc URL minh họa hay tuyên bố đã đăng video.

**Lời trình bày:**

Trang này dành cho liên kết video theo yêu cầu của bài nộp. Sau đây, chúng em trình bày nguồn dữ liệu và các câu hỏi nghiên cứu.

## Slide 3 — Dataset and research questions

**Thao tác:** chỉ số quan sát, biến mục tiêu và ba nhãn M, F, I.

**Lời trình bày:**

Abalone được lưu trữ trên UCI, gồm 4.177 quan sát, tám biến đầu vào và biến mục tiêu Rings, tức số vòng vỏ. Bộ dữ liệu có cả biến định lượng và biến phân nhóm, phù hợp để triển khai xuyên suốt các yêu cầu của đề.

Ba nhãn M, F và I tương ứng với cá thể đực, cái và cá thể non. Vì vậy, I thể hiện giai đoạn phát triển, không phải một giới tính thứ ba. Các phép đo liên tục được giữ theo thang dữ liệu nguồn.

Chúng em đặt ba câu hỏi: phân bố và khác biệt giữa các nhóm như thế nào; phép đo nào liên hệ rõ với số vòng; và khi kết hợp nhiều phép đo, mô hình dự đoán tốt đến đâu trên dữ liệu chưa dùng để huấn luyện?

**Nguồn để đối chiếu:** `references/abalone.names`; Nash và cộng sự (1994), DOI 10.24432/C55C7W; `results/summary.json`.

## Slide 4 — Quality checks and holdout design

**Thao tác:** chỉ hai giá trị Height bằng 0 và sơ đồ chia tập.

**Lời trình bày:**

Trước khi phân tích, chúng em kiểm tra cấu trúc, dữ liệu thiếu và bản ghi trùng. File hiện có không thiếu ô và không trùng toàn dòng, nhưng phát hiện hai giá trị chiều cao bằng không. Theo quy tắc chiều cao phải dương, hai ô này được đánh dấu thiếu trong bản xử lý; dữ liệu gốc vẫn được giữ nguyên.

Tiếp theo, chúng em chia dữ liệu thành 3.341 quan sát huấn luyện và 836 quan sát kiểm tra, có phân tầng theo nhóm. Phân tích khám phá và phát triển mô hình thực hiện trên tập huấn luyện.

Các tham số điền thiếu và chuẩn hóa chỉ được học từ phần dữ liệu dùng để huấn luyện ở từng lần fit. Cách tổ chức này hạn chế rò rỉ thông tin và giúp kết quả trên tập kiểm tra phản ánh khả năng dự đoán trên các quan sát được giữ lại.

## Slide 5 — Distribution of recorded length

**Thao tác:** chỉ vùng tập trung và phần đuôi trên histogram.

**Lời trình bày:**

Histogram cho thấy chiều dài tập trung chủ yếu ở vùng giữa, với trung bình khoảng 0,524 và độ lệch chuẩn khoảng 0,120 theo thang lưu trữ.

Chúng em chọn histogram vì biểu đồ này thể hiện được hình dạng phân bố, độ lệch và vùng giá trị ít xuất hiện. Một giá trị trung bình riêng lẻ không thể cung cấp những thông tin đó.

Các điểm ở đuôi được xem xét thêm bằng boxplot và quy tắc IQR trong notebook. Tuy nhiên, một quan sát nằm ngoài ngưỡng IQR chưa đủ để xác định đó là lỗi đo; nhóm không tự động xóa các quan sát này. Từ mô tả trực quan, chúng em chuyển sang kiểm tra phân phối bằng phương pháp thống kê.

## Slide 6 — Length differs across recorded groups

**Thao tác:** lần lượt chỉ nhóm I, F và M; không đọc từng chữ số của bảng.

**Lời trình bày:**

Khi phân nhóm, chiều dài trung bình của cá thể non thấp hơn hai nhóm còn lại. Đây là một đặc điểm cần tính đến khi diễn giải toàn bộ dữ liệu, vì mẫu đang kết hợp các cá thể ở những giai đoạn phát triển khác nhau.

Biểu đồ cột trên slide giúp so sánh trung bình. Boxplot và khoảng tin cậy trong báo cáo bổ sung thông tin về phân tán và mức bất định của ước lượng.

Chênh lệch nhìn thấy trên hình mới là bằng chứng mô tả. Để đánh giá bằng chứng thống kê, chúng em sẽ dùng kiểm định phù hợp; đồng thời không quy sự khác biệt này hoàn toàn cho giới tính.

## Slide 7 — Length against a Normal candidate

**Thao tác:** chỉ đường quan sát màu xanh và đường chuẩn ứng viên màu đỏ; sau đó chỉ kết quả AD.

**Lời trình bày:**

Với chiều dài, chúng em kiểm tra phân phối chuẩn như một mô hình ứng viên. Đường màu xanh mô tả mật độ quan sát; đường màu đỏ là mật độ chuẩn được ước lượng từ tập huấn luyện. Sự khác biệt giữa hai đường được xem xét thêm bằng Q–Q plot trong báo cáo.

Nhóm sử dụng kiểm định Anderson–Darling, với 1.999 mẫu mô phỏng và ước lượng lại tham số trong mỗi mẫu. Việc ước lượng lại giúp phản ánh đúng trường hợp trung bình và độ lệch chuẩn chưa được biết trước.

P-value sau điều chỉnh Holm bằng 0,0015, nên bác bỏ giả thuyết phân phối chuẩn ở mức 5%. Kết luận này cho thấy mô hình chuẩn chưa phù hợp hoàn toàn với dữ liệu; không có nghĩa mọi phương pháp tiếp theo đều mất hiệu lực. Cần xét riêng giả định của từng phương pháp.

## Slide 8 — Weight and candidate distributions

**Thao tác:** chỉ mật độ quan sát màu cam, đường Normal màu xanh và Lognormal màu xanh lá.

**Lời trình bày:**

Với khối lượng toàn phần, chúng em kiểm tra hai ứng viên: phân phối chuẩn và phân phối lognormal. Lognormal là một lựa chọn có cơ sở vì khối lượng dương và có thể lệch phải, nhưng vẫn cần kiểm tra bằng dữ liệu.

Cả hai ứng viên đều bị bác bỏ sau điều chỉnh. Như vậy, lấy log không tự động bảo đảm rằng phân phối trở nên phù hợp.

Các p-value mô phỏng cùng chạm mức nhỏ nhất có thể báo cáo, là 0,0005 trước điều chỉnh. Điều đó không có nghĩa mức sai khác của các mô hình giống nhau. Chúng em đọc kết quả cùng biểu đồ và thống kê kiểm định, thay vì chỉ dựa vào p-value. Sự pha trộn giữa các nhóm là một khả năng giải thích, chưa phải nguyên nhân đã được chứng minh.

## Slide 9 — Three prespecified hypothesis tests

**Thao tác:** chỉ lần lượt ba câu hỏi; nhấn tên phép kiểm gắn với loại dữ liệu.

**Lời trình bày:**

Chúng em xác định ba câu hỏi kiểm định.

Thứ nhất, số vòng trung bình có khác nhau giữa M và F hay không? Nhóm dùng Welch t-test hai phía để so sánh hai trung bình, cho phép phương sai khác nhau.

Thứ hai, nhóm M, F, I có độc lập với dải số vòng hay không? Câu hỏi giữa hai biến phân loại được kiểm tra bằng Chi-square. Các dải số vòng theo cách mã hóa lịch sử trong codebook, không được xem là ngưỡng tuổi sinh học đã xác nhận.

Thứ ba, chiều dài trung bình có bằng nhau giữa cả ba nhóm hay không? Nhóm dùng Welch ANOVA; khi bác bỏ giả thuyết chung, mới tiếp tục so sánh từng cặp.

Mức ý nghĩa là 5%. Ba kiểm định chính được điều chỉnh Holm để kiểm soát nguy cơ có ít nhất một kết luận dương tính giả trong nhóm kiểm định này. Giả định độc lập giữa các quan sát vẫn cần được lưu ý.

## Slide 10 — Results and effect magnitude

**Thao tác:** chỉ chênh lệch M−F, khoảng tin cậy và Cramér V.

**Lời trình bày:**

Cả ba kiểm định chính đều bác bỏ giả thuyết không sau điều chỉnh. Tuy nhiên, ý nghĩa thống kê cần được đọc cùng độ lớn khác biệt.

Ví dụ, chênh lệch số vòng trung bình M trừ F khoảng âm 0,355 vòng. Khoảng tin cậy 95% từ âm 0,606 đến âm 0,103 cho thấy hướng chênh lệch nhất quán, nhưng mức chênh lệch tuyệt đối vẫn tương đối nhỏ. Đây là khoảng tin cậy riêng cho phép so sánh; nhóm chỉ điều chỉnh p-value, không gọi đó là khoảng tin cậy đồng thời.

Với Chi-square, Cramér V khoảng 0,372 bổ sung thông tin về mức liên hệ. Tần số kỳ vọng nhỏ nhất khoảng 334,7, nên bảng không gặp vấn đề ô quá thưa.

Những kết quả này cung cấp bằng chứng về khác biệt và liên hệ trong mẫu. P-value không phải xác suất giả thuyết không đúng, và cũng không đo tầm quan trọng thực tiễn của kết quả.

## Slide 11 — Pearson and Spearman associations

**Thao tác:** chỉ ô Shell weight–Rings trên heatmap; phân biệt tương quan giữa đầu vào và tương quan với mục tiêu.

**Lời trình bày:**

Chúng em sử dụng hai hệ số tương quan để nhìn mối liên hệ từ hai góc độ. Pearson đo mức liên hệ tuyến tính giữa các giá trị; Spearman đo mức liên hệ đơn điệu thông qua thứ hạng.

Trong các phép đo được xét, khối lượng vỏ có tương quan với số vòng nổi bật nhất: Pearson khoảng 0,628 và Spearman khoảng 0,693. Spearman cao hơn gợi ý xu hướng tăng theo thứ hạng thể hiện rõ hơn mức phù hợp với một đường thẳng.

Tuy nhiên, đây là liên hệ giữa từng cặp biến. Kết quả này chưa cho biết đóng góp riêng của khối lượng vỏ khi các phép đo khác đã có trong mô hình, và không đủ để kết luận quan hệ nhân quả.

## Slide 12 — Shell weight and Rings

**Thao tác:** chỉ xu hướng chung rồi chỉ độ phân tán theo chiều dọc.

**Lời trình bày:**

Biểu đồ phân tán giúp kiểm tra ý nghĩa thực tế của hệ số tương quan. Khi khối lượng vỏ tăng, số vòng nhìn chung cũng tăng. Nhưng tại những mức khối lượng gần nhau, số vòng vẫn phân tán đáng kể.

Vì vậy, một phép đo đơn lẻ chưa mô tả đầy đủ khác biệt giữa các cá thể. Đây là cơ sở để chuyển sang mô hình hồi quy sử dụng nhiều biến.

Mặt khác, các phép đo kích thước liên hệ chặt với nhau, nên việc bổ sung biến có thể làm tăng thông tin trùng lặp. Chúng em sẽ xem xét cả khả năng dự đoán lẫn đa cộng tuyến, thay vì mặc định rằng thêm biến luôn tốt hơn.

## Slide 13 — Multiple linear regression design

**Thao tác:** chỉ ba phương án, bước tiền xử lý và cơ chế đánh giá.

**Lời trình bày:**

Hồi quy tuyến tính đa biến biểu diễn số vòng dự đoán bằng một hệ số chặn và tổng các biến đầu vào nhân với hệ số tương ứng. Phương pháp bình phương tối thiểu lựa chọn hệ số để giảm tổng bình phương phần dư trên dữ liệu huấn luyện.

Chúng em so sánh ba phương án đã xác định: baseline dự đoán trung bình tập huấn luyện; mô hình gọn dùng nhóm, kích thước và khối lượng toàn phần; mô hình đầy đủ dùng tám biến đầu vào gốc.

Biến nhóm được mã hóa bằng hai biến giả, lấy F làm tham chiếu. Điền thiếu, chuẩn hóa và hồi quy được tổ chức trong cùng quy trình. Với kiểm định chéo năm phần, mỗi lần huấn luyện đều học lại tham số tiền xử lý từ phần huấn luyện tương ứng.

Tuổi suy ra từ Rings cộng 1,5 không được đưa vào đầu vào, vì chứa trực tiếp thông tin của biến mục tiêu. Tập kiểm tra được giữ riêng, không dùng để điều chỉnh mô hình.

## Slide 14 — Holdout performance and model limits

**Thao tác:** chỉ ba cột RMSE rồi chỉ các giới hạn mô hình.

**Lời trình bày:**

Trên 836 quan sát kiểm tra, RMSE giảm từ khoảng 3,27 vòng ở baseline xuống 2,58 ở mô hình gọn và 2,25 ở mô hình đầy đủ. Mức giảm so với baseline khoảng 31,1%. MAE của mô hình đầy đủ khoảng 1,60 vòng, tức sai lệch tuyệt đối trung bình khoảng một phẩy sáu vòng.

R bình phương khoảng 0,526 phản ánh mức giảm tổng bình phương sai số so với dự đoán trung bình của tập kiểm tra; không phải mô hình dự đoán đúng 52,6% cá thể. Baseline trong bài dùng trung bình tập huấn luyện, nên khác nhẹ với mốc dùng trong công thức R bình phương.

Chẩn đoán cho thấy đa cộng tuyến và phương sai phần dư không đồng nhất. Nhóm dùng HC3 để điều chỉnh sai số chuẩn của hệ số; HC3 không cải thiện trực tiếp dự đoán hay sửa quan hệ phi tuyến. Các điểm có ảnh hưởng được kiểm tra độ nhạy, nhưng vẫn giữ trong mô hình chính. Vì vậy, kết quả dự đoán có cải thiện, song cần diễn giải trong những giới hạn này.

## Slide 15 — Reproducible code demonstration

**Thao tác:** chuyển sang notebook/HTML đã mở sẵn. Kéo lần lượt qua sáu phần, dừng ở vị trí ghi trong `Demo_VI.md`. Tổng dự kiến 120 giây, gồm chuyển cửa sổ.

**Lời trình bày:**

Để minh họa quy trình phân tích, em xin chuyển sang notebook và lần lượt giới thiệu sáu phần chính.

Ở phần một, chúng em đọc dữ liệu và kiểm tra cấu trúc, dữ liệu thiếu, trùng lặp và giá trị bất thường. Bộ dữ liệu có 4.177 quan sát và chín cột. Hai giá trị chiều cao bằng không được đánh dấu thiếu. Sau đó, chúng em giữ riêng 836 quan sát kiểm tra; thống kê mô tả và biểu đồ trên tập huấn luyện giúp nhận diện phân bố và các điểm cần xem xét.

Ở phần hai, chúng em kiểm tra phân phối chuẩn cho chiều dài, cùng phân phối chuẩn và lognormal cho khối lượng. Kiểm định Anderson–Darling dùng mô phỏng và ước lượng lại tham số. Cả ba giả thuyết đều bị bác bỏ sau điều chỉnh Holm. Vì vậy, các phân phối ứng viên này chưa mô tả đầy đủ dữ liệu.

Phần ba áp dụng Welch t-test, Chi-square và Welch ANOVA cho ba câu hỏi nghiên cứu. Kết quả được điều chỉnh Holm và đọc cùng độ lớn khác biệt. Chẳng hạn, số vòng trung bình của M thấp hơn F khoảng 0,355 vòng. Có bằng chứng thống kê về chênh lệch, nhưng không thể từ đó kết luận nguyên nhân sinh học.

Ở phần bốn, Pearson đo liên hệ tuyến tính, còn Spearman đo liên hệ theo thứ hạng. Khối lượng vỏ có tương quan nổi bật với số vòng: lần lượt khoảng 0,628 và 0,693. Đây là liên hệ giữa từng cặp biến, chưa phải đóng góp riêng trong mô hình đa biến.

Phần năm so sánh baseline, mô hình gọn và mô hình đầy đủ. Trong kiểm định chéo năm phần, quy trình điền thiếu và chuẩn hóa được học lại trên phần huấn luyện của từng vòng, nhằm hạn chế rò rỉ dữ liệu. Trên tập test giữ riêng, mô hình đầy đủ đạt RMSE khoảng 2,25 vòng, so với 3,27 của baseline. Chúng em cũng kiểm tra phần dư, đa cộng tuyến và độ nhạy với các quan sát có ảnh hưởng.

Cuối cùng, notebook xuất các bảng, hình và số liệu tổng hợp để truy vết kết quả trong báo cáo. Mô hình cải thiện dự đoán, nhưng vẫn có sai số và giới hạn khái quát. Em xin trở lại slide kết luận.

## Slide 16 — Conclusions and limitations

**Thao tác:** quay lại slide 16, dừng cuộn notebook; nhìn người nghe khi kết thúc.

**Lời trình bày:**

Từ phân tích, chúng em rút ra ba kết luận. Các phân phối ứng viên đơn giản chưa mô tả đầy đủ dữ liệu. Nhóm và các phép đo có liên hệ với số vòng, nhưng mức liên hệ cần được đọc cùng độ lớn và giới hạn thống kê. Hồi quy đầy đủ cải thiện dự đoán so với baseline, song sai số vẫn đáng kể.

Dữ liệu lịch sử và việc thiếu thông tin địa điểm lấy mẫu hạn chế khả năng khái quát sang quần thể mới. Nghiên cứu này cung cấp bằng chứng mô tả và dự đoán, chưa xác lập nguyên nhân sinh học.

Nhóm xin cảm ơn Cô và các bạn đã lắng nghe, và sẵn sàng trao đổi thêm về phương pháp cũng như kết quả.

## Slide 17 — Appendix: definitions and inference

**Chỉ dùng khi được hỏi; không đọc trong phần trình bày chính.**

Welch t-test chuẩn hóa chênh lệch hai trung bình bằng sai số chuẩn cho phép hai phương sai khác nhau. ANOVA cổ điển so sánh biến thiên giữa nhóm với biến thiên trong nhóm dưới giả định phương sai chung; Welch ANOVA điều chỉnh trọng số và bậc tự do khi phương sai khác nhau. Dùng Welch không loại bỏ giả định độc lập hay sai lệch chọn mẫu.

Trong Chi-square, mỗi ô đóng góp bình phương chênh lệch giữa tần số quan sát và kỳ vọng, chia cho tần số kỳ vọng. Kiểm định này đánh giá độc lập giữa biến phân loại, không kiểm tra chênh lệch trung bình.

Holm kiểm soát xác suất có ít nhất một bác bỏ sai trong một họ giả thuyết, dưới các điều kiện của các p-value đầu vào. Bài có họ riêng cho ba kiểm định phân phối, ba câu hỏi chính và các so sánh cặp sau ANOVA. Không được mô tả là đã điều chỉnh chung mọi phân tích trong nghiên cứu.

## Slide 18 — Appendix: regression diagnostics

**Chỉ dùng khi được hỏi.**

Ma trận thiết kế có hạng đầy đủ không đồng nghĩa với không có đa cộng tuyến: vẫn có thể tồn tại các cột gần phụ thuộc tuyến tính, khiến hệ số nhạy với thay đổi dữ liệu. Do đó, hiệu quả dự đoán tốt hơn không bảo đảm mỗi hệ số riêng lẻ ổn định hoặc có ý nghĩa nhân quả.

HC3 điều chỉnh ước lượng ma trận hiệp phương sai để hỗ trợ suy luận khi phương sai sai số thay đổi. Nó không thay thế việc xem xét dạng hàm, sự độc lập hoặc dữ liệu bị thiếu biến quan trọng.

Có 212 quan sát vượt ngưỡng Cook 4/n trên train. Đây là dấu hiệu ảnh hưởng trong mô hình, không phải xác nhận dữ liệu sai. Phân tích độ nhạy chỉ lọc trong phần huấn luyện của từng fold và giữ nguyên phần validation; mô hình chính giữ các quan sát đó. Một dự đoán test nằm ngoài miền Rings quan sát cũng cho thấy giới hạn của hồi quy tuyến tính với mục tiêu đếm.

## Slide 19 — References

**Chỉ dùng khi cần giới thiệu hoặc đối chiếu nguồn.**

Nguồn dữ liệu là Abalone của Nash và cộng sự trên UCI; codebook được lưu cùng dự án. Các phương pháp được đối chiếu với tài liệu gốc của SciPy, statsmodels và scikit-learn được dẫn trong báo cáo. Số liệu trình bày được truy vết qua notebook, các bảng CSV và `results/summary.json`.

## Những cách diễn đạt cần giữ chính xác

| Tránh nói | Nên nói |
|---|---|
| “P-value là xác suất H0 đúng.” | “P-value đánh giá mức cực đoan của dữ liệu dưới H0 và các giả định của phép kiểm.” |
| “Khác biệt có ý nghĩa nên ảnh hưởng rất lớn.” | “Có bằng chứng thống kê; độ lớn cần đọc qua chênh lệch, khoảng tin cậy và thước đo liên hệ.” |
| “R² bằng 0,526 nghĩa là đúng 52,6%.” | “R² đánh giá mức giảm tổng bình phương sai số so với mốc trung bình của tập đánh giá.” |
| “Shell weight quyết định số vòng.” | “Shell weight có liên hệ với số vòng trong dữ liệu quan sát.” |
| “HC3 sửa mô hình để dự đoán tốt hơn.” | “HC3 điều chỉnh sai số chuẩn và khoảng tin cậy của hệ số.” |
| “Điểm ngoại lai là dữ liệu sai.” | “Điểm được gắn cờ cần xem xét; chưa đủ căn cứ để tự động loại bỏ.” |
| “Demo này đang chạy lại toàn bộ phân tích.” | “Em trình bày quy trình và kết quả đã chạy, được lưu trong notebook.” |

## Bằng chứng để người trình bày tự đối chiếu

- Dữ liệu, chia tập, số liệu tổng hợp: `results/summary.json`.
- Phân phối: `results/tables/distribution_tests.csv`.
- Kiểm định: `results/tables/hypothesis_tests.csv`, `contingency_expected.csv`.
- Tương quan: `results/tables/rings_correlations.csv`.
- Hồi quy: `results/tables/test_metrics.csv`, `test_predictions.csv`, `cv_fold_metrics.csv`.
- Demo: `Demo_VI.md`; notebook tại `../notebooks/VibeCoding_Expert_DAV_Theory_Endterm_Analysis.ipynb`.

Các đường dẫn results ở trên tính từ thư mục gốc Nor hoặc DEMO_NOR. Mốc thời gian là kế hoạch; nhóm cần tự luyện, kiểm tra âm thanh và đo thời lượng thật trước khi nộp video.
