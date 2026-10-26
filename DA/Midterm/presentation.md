# Slide 1

Kính thưa cô và các bạn, hôm nay nhóm em xin trình bày bài báo cáo giữa kỳ môn Phân tích và Trực quan hoá Dữ liệu. 

Đề tài của nhóm xuất phát từ một tình huống kinh doanh rất thực tế: Một thương hiệu F&B vừa tung sản phẩm mới ra thị trường được đúng 7 ngày đầu tiên. Khi lên mạng xã hội theo dõi, bộ phận Marketing bắt đầu nhận về nhiều phản hồi trái chiều – có những khách hàng khen ngon, nhưng cũng có người chê giá đắt, người than phiền phục vụ chậm và phải xếp hàng lâu. 

Trước làn sóng ý kiến trái chiều đó, ban giám đốc rất lo lắng và đặt ra câu hỏi lớn: *"Chiến dịch ra mắt này có đang gặp khủng hoảng không, và tuần tới chúng ta có cần đập bỏ toàn bộ poster, chiến dịch quảng cáo để viết lại thông điệp từ đầu hay không?"* 

Hôm nay, nhóm em đứng đây để trả lời câu hỏi đó bằng dữ liệu thực nghiệm từ 1,6 triệu bài viết mạng xã hội thông qua 4 cấp độ phân tích dữ liệu chuẩn mực. Em xin phép được bắt đầu.

---

# Slide 2

Để trả lời câu hỏi của ban giám đốc một cách khoa học và bài bản, nhóm em bám sát quy trình phân tích từ Chương 1 của môn học, chia bài toán thành 4 câu hỏi nghiệp vụ rõ ràng:
* Một là **Mô tả**: Tuần ra mắt vừa qua chuyện gì đã thực sự xảy ra trên mạng xã hội?
* Hai là **Chẩn đoán**: Đâu là những nguyên nhân cốt lõi khiến khách hàng không hài lòng và chê bai?
* Ba là **Dự đoán**: Tuần tới nếu có hàng ngàn bài viết mới đổ về, liệu cỗ máy AI có thể tự động phân loại cảm xúc chính xác cho ban quản lý hay không?
* Bốn là **Đề xuất**: Ban giám đốc nên đưa ra những quyết định hành động cụ thể nào?

Đặc biệt, để đảm bảo tính liêm chính khoa học, nhóm em đã chốt cứng 4 giả thuyết nghiên cứu từ H1 đến H4 và cố định một **ngưỡng ý nghĩa thực tiễn là 5 điểm phần trăm** ngay từ trước khi chạm vào dữ liệu, tránh việc nhìn thấy số liệu rồi mới vẽ giả thuyết theo ý mình.

Tại sao nhóm lại cần ngưỡng 5 điểm phần trăm này? Cô và các bạn có thể hình dung đơn giản: Giống như khi chúng ta đem một con voi lên bàn cân, nếu có một hạt bụi rơi vào thì cái cân điện tử có nhích một chút xíu cũng chẳng làm con voi nặng hơn bao nhiêu cả. Khi làm việc với dữ liệu lớn hàng triệu bài viết, chỉ cần một sai lệch nhỏ li ti 0.1% thì công thức thống kê trên máy tính cũng tính ra $p < 0.05$ là có ý nghĩa thống kê. Nhưng trong thực tế kinh doanh, thay đổi 0.1% không đáng để doanh nghiệp phải tốn tiền sửa đổi. Do đó, nhóm quy định sự thay đổi phải lệch từ 5% trở lên thì mới thực sự có ý nghĩa đối với bài toán kinh doanh.

---

# Slide 3

Nhóm xin tóm tắt ngay câu trả lời cho ban lãnh đạo theo nguyên lý kim tự tháp: **Hãy giữ nguyên thông điệp truyền thông cốt lõi, và tập trung điều chỉnh ba điểm đau ở khâu vận hành.**

Để cô và các bạn dễ hình dung: Tình huống này giống hệt như việc khách đi uống trà sữa chê không phải vì nước trà dở, mà vì đến nơi nhân viên bảo hết trân châu hoặc bắt đứng đợi quá lâu. Vị trà ngon thì thông điệp quảng cáo cứ giữ nguyên, việc của quán là phải lo đi nhập thêm trân châu và thuê thêm nhân viên thôi ạ!

Căn cứ từ dữ liệu gồm ba điểm mấu chốt:
* Thứ nhất, hội thoại về ăn uống trên mạng xã hội vốn dĩ luôn tích cực hơn mặt bằng chung: tỷ lệ tiêu cực của F&B luôn thấp hơn toàn mạng khoảng 5.1 điểm phần trăm.
* Thứ hai, kiểm định thống kê chứng minh tuần ra mắt không hề bị phản đối hay tẩy chay ($p = 0.37$). Phản ứng trái chiều vừa qua chỉ là sự pha trộn tự nhiên bình thường của thị trường ăn uống.
* Thứ ba, mô hình phân loại của nhóm đạt độ chính xác ROC-AUC 0.896 trên tuần kiểm thử độc lập, sẵn sàng bắt trọn 84% các bài viết phàn nàn mỗi ngày.

Chiến dịch truyền thông không hề thất bại, vấn đề nằm ở ba điểm nghẽn vận hành: Hết hàng, Quá tải ca tối và Giá cả.

---

# Slide 4

Về nguồn dữ liệu, nhóm làm việc trên tập Sentiment140 gồm 1,6 triệu tweet tiếng Anh năm 2009 được gán nhãn tự động bằng biểu tượng cảm xúc mặt cười và mặt mếu.

Vì đây là dữ liệu cộng đồng, không có một nhãn hàng F&B đơn lẻ nào đủ dữ liệu để phân tích độc lập (ví dụ kiểm tra thực tế chiến dịch McCafé năm đó chỉ có đúng 17 bài, còn KFC thì mất dữ liệu đúng ngày khuyến mãi), nên nhóm em đã dùng toàn bộ 84.632 bài viết về ăn uống làm môi trường hội thoại đại diện cho toàn ngành (Category Proxy).

Để lọc chuẩn xác, nhóm xây dựng từ điển regex gồm 41 thương hiệu và 5 nhóm ẩm thực, loại trừ kỹ các từ gây nhiễu như Subway (tránh nhầm với tàu điện ngầm) hay cụm từ thành ngữ Piece of cake (dễ như ăn bánh). Nhóm cũng lấy mẫu phân tầng 210 bài viết để thẩm định thủ công, đạt **độ chính xác bộ lọc là 89%** với khoảng tin cậy 95% an toàn từ 84.8% đến 93.3%. Con số 89% này nghĩa là cứ 10 bài bot cào về thì có gần 9 bài chuẩn xác là khách đang nói về trải nghiệm ăn uống thực sự, chứng minh bộ lọc hoạt động rất đáng tin cậy.

---

# Slide 5

Trong quá trình khám phá dữ liệu, nhóm em đã phát hiện một **bẫy kỹ thuật nghiêm trọng** trong tập dữ liệu gốc:

Kể từ 8 giờ 40 sáng ngày 16 tháng 6, dòng tweet tích cực hoàn toàn biến mất. Hơn 275.000 dòng dữ liệu phía sau toàn bộ 100% là bài viết tiêu cực do tác giả dừng bot tìm kiếm biểu tượng vui. 

Nó giống hệt như việc chúng ta đi khảo sát sức khỏe của người dân mà lại đứng ngay trước cổng bệnh viện để hỏi. Ai đứng ở đó mà chẳng kêu ốm! Nếu người làm dữ liệu không cẩn thận mà cứ thế đưa vào mô hình, chuỗi thời gian sẽ xuất hiện hiện tượng sụp đổ cảm xúc giả tạo và tập kiểm thử tuần tới sẽ chỉ có duy nhất một nhãn tiêu cực, làm sai lệch hoàn toàn kết quả nghiên cứu.

Nhóm em đã loại bỏ hoàn toàn 275.000 dòng lỗi này và thực hiện quy trình làm sạch 5 bước, giữ lại 1.274.034 tweet sạch. Đồng thời, theo đúng bài học Chương 3 về tỷ lệ so với số đếm, nhóm không nhìn vào số lượng bài chê tuyệt đối (vì phụ thuộc vào cách bot thu thập) mà luôn so sánh đối chứng bằng mức nâng (Lift) và tỷ số Odds Ratio giữa các nhóm với nhau.

---

# Slide 6

Ở tầng phân tích mô tả: Biểu đồ Donut bên trái cho thấy hơn một phần ba cuộc trò chuyện là về các bữa ăn hàng ngày, và **chỉ có 7.5% bài viết nhắc đích danh tên một nhãn hàng**. 

Điều này mang lại bài học xương máu cho đội ngũ truyền thông: Khách hàng lên mạng thường chỉ nói *"hôm nay thèm trà sữa quá"* chứ ít ai réo tên thương hiệu cụ thể. Nếu nhãn hàng chỉ ngồi canh ai tag tên mình thì coi như đang bị điếc trước 90% câu chuyện mà khách hàng đang bàn tán ngoài kia.

Biểu đồ bên phải thể hiện mức nâng (Lift): Ở mọi giai đoạn, ngành ăn uống luôn ít tiêu cực hơn Twitter chung khoảng 5 điểm phần trăm. Đặc biệt, trong tuần ra mắt sản phẩm mới, mức nâng là âm 5.4 điểm phần trăm, gần như trùng khít với mức âm 5.1 điểm phần trăm của giai đoạn trước đó. Điều này chứng minh tuần ra mắt diễn ra hoàn toàn bình thường, không hề có sự sụt giảm cảm xúc nào.

---

# Slide 7

Quan sát chuỗi thời gian 39 ngày ở Slide 7: Có tới 35 trên 39 ngày đường tiêu cực của F&B nằm dưới đường trung bình của toàn mạng. 

Cô và các bạn có thể thấy một vài đỉnh nhọn nhô lên cao. Tại sao lại có những cái gai nhọn đó? Nó giống như một lớp học hôm đó chỉ có đúng 2 bạn đi học, lỡ một bạn bị điểm kém là tỷ lệ rớt môn của lớp ngày hôm đó vọt lên 50% ngay! Phân tích sâu cho thấy đó đơn giản là những ngày lượng bài viết quá ít (dưới 200 bài) khiến tỷ lệ bị nhảy vọt theo mẫu nhỏ, dải tin cậy mở rộng ra, chứ không hề có sự kiện khủng hoảng nào xảy ra. 

Về mức độ tập trung, biểu đồ Pareto chỉ ra quy luật 80/20 rất rõ nét: 20 trên 41 thương hiệu chiếm 80% thảo luận, trong đó Starbucks dẫn đầu áp đảo với hơn 20% thị phần thảo luận.

---

# Slide 8

Vậy cụ thể khách hàng chê vì cái gì? Nhóm tiến hành kiểm định 4 giả thuyết bằng kiểm định z hai tỷ lệ có hiệu chỉnh đa kiểm định Holm để tránh sai số loại I:
* Phàn nàn dịch vụ (H1) làm tăng tiêu cực 5.4 điểm phần trăm; Phàn nàn về giá (H2) làm tăng 5.6 điểm phần trăm. Cả hai đều đạt ý nghĩa thống kê và vượt ngưỡng thực tiễn 5 điểm phần trăm.
* Trải nghiệm cà phê sáng (H3) mang cảm xúc tích cực rõ rệt, giúp giảm tiêu cực 6.6 điểm phần trăm vì uống cà phê sáng giúp người ta phấn chấn hơn.
* Đặc biệt, giả thuyết H4 so sánh tuần ra mắt với các tuần bình thường (áp dụng phương pháp trừ 2 lần Diff-in-diff để loại trừ biến động nền của Twitter) chỉ chênh lệch âm 0.3 điểm phần trăm với $p = 0.37$. Giả thuyết tuần ra mắt bị phản đối chính thức bị bác bỏ.

Thủ phạm to nhất nằm ở dòng đầu tiên: **HẾT HÀNG (Availability)**. Bài viết dính chữ hết hàng có tỷ lệ chê vọt lên tới 79.6%, mức nâng tăng vọt 45.3 điểm phần trăm. Hồi quy Logistic cho thấy khách hàng gặp cảnh hết hàng có Odds tiêu cực cao gấp 7.2 lần bình thường! Tức là khách đang vui vẻ đến quán mà bị nhân viên bảo *"hết món rồi anh ơi"* là cơn giận tăng vọt gấp 7 lần. Khách chửi vì không mua được món chứ không phải chê món dở.

---

# Slide 9

Sự bực mình của khách hàng không chỉ nằm ở bản thân món ăn mà phụ thuộc rất lớn vào thời điểm và hoàn cảnh:
* Heatmap ma trận giờ cho thấy phàn nàn về dịch vụ tăng vọt vào **buổi tối từ 18h đến 23h** (tăng thêm 10.2 điểm phần trăm) do các cửa hàng quá tải khách giờ tan tầm, nhân viên phục vụ không kịp khiến khách phải chờ lâu.
* Mô hình chủ đề NMF (đã gạn lọc hết từ khóa đồ ăn để tìm ngữ cảnh) phát hiện: Các cuộc trò chuyện ăn uống gắn liền với 'Công việc và giờ giải lao' làm tăng tiêu cực tới 13.7 điểm phần trăm do khách hàng vừa ăn vừa chịu áp lực deadline. Ngược lại, ăn uống quây quần cùng gia đình hay nấu nướng tại nhà lại tràn ngập niềm vui.

Nói một cách dễ hiểu: Khách hàng vừa ăn vừa lo công việc thì ăn sơn hào hải vị cũng thấy quạu. Còn đi ăn với người yêu, gia đình thì ăn mì tôm cũng thấy vui. Khách quạu một phần vì hoàn cảnh của họ, nhãn hàng cần hiểu tâm lý này để làm nội dung quảng cáo cho khéo léo. Nhóm cũng lưu ý theo đúng bài học Chương 1: đây là các mối liên hệ tương quan quan sát được, làm cơ sở định hướng truyền thông chứ chưa phải quan hệ nhân quả tuyệt đối.

---

# Slide 10

Để theo dõi cảm xúc tuần tới mà không cần nhân sự đọc thủ công từng bài, nhóm xây dựng mô hình tự động phân loại. 

Về phương pháp chia dữ liệu, nhóm chủ động chọn **chia theo dòng thời gian** thay vì chia ngẫu nhiên: Huấn luyện trên tháng 4 và 5 (hơn 650.000 tweet), tinh chỉnh tham số trên tuần ra mắt, và đánh giá duy nhất một lần trên tuần tới (hơn 150.000 tweet). 

Tại sao nhóm lại không chia ngẫu nhiên? Giống như việc bạn cho học sinh biết trước đề thi ngày mai thì điểm đứa nào chẳng được 10! Dữ liệu Twitter các bài cùng ngày thường bàn về cùng một tin tức thời sự; nếu chia ngẫu nhiên, mô hình sẽ 'học lỏm' sự kiện của ngày mai và cho điểm cao ảo tưởng (AUC vọt lên 0.903). Chia theo thời gian bắt máy dùng quá khứ đoán tương lai, kết quả mới là năng lực thật và kiểm tra được độ trôi ngôn ngữ theo thời gian.

Nhóm so sánh mô hình chuẩn Naive Bayes (Bag-of-words) với mô hình nâng cao Logistic Regression sử dụng TF-IDF cả từ đơn và cặp từ với 300.000 đặc trưng, tối ưu ngưỡng quyết định ở mức 0.44.

---

# Slide 11

Trên tập kiểm thử tuần tới, Logistic Regression vượt trội toàn diện:
* Chỉ số ROC-AUC đạt 0.896 so với 0.846 của Naive Bayes – nghĩa là nếu chọn ngẫu nhiên 1 câu chê và 1 câu khen, có tới gần 90% khả năng mô hình sẽ xếp câu chê điểm cao hơn.
* Độ chính xác đạt 81.0% và bắt trọn 84.3% các bài viết tiêu cực (Recall). 

Tại sao nhóm lại chỉnh ngưỡng quyết định xuống 0.44 thay vì để mặc định 0.5? Giống như cổng an ninh sân bay, thà máy kêu nhầm cái thắt lưng kim loại để nhân viên kiểm tra lại, còn hơn là để lọt một cây kéo nguy hiểm. Trong kinh doanh, thà báo nhầm một khách khen để vào chăm sóc, còn hơn là bỏ sót một khách hàng đang tức giận mà không kịp xin lỗi.

Kiểm định McNemar cho mẫu ghép cặp chứng minh Logistic Regression giúp giảm chính xác 440 lỗi gán nhãn sai trên mỗi 10.000 bài viết ($p < 0.001$). Các kiểm tra độ vững ở Phụ lục B cũng khẳng định mô hình hoạt động ổn định trên cả người dùng mới lẫn người dùng cũ.

---

# Slide 12

Mô hình của nhóm hoàn toàn minh bạch và có khả năng giải thích chứ không phải một chiếc hộp đen bí ẩn:
* Về toàn cục: Hệ số hồi quy thể hiện rõ các từ mang trọng số âm kéo về tích cực như *can't wait* hay *not bad*, và các từ mang trọng số dương đẩy về tiêu cực như *sad, sick, sucks*.
* Về cục bộ: Biểu đồ phân rã Waterfall – phiên bản tuyến tính của SHAP – chứng minh mô hình xử lý rất thông minh ngữ cảnh phủ định. 

Ví dụ thực tế với câu: *"that's not bad at all"* (món này không tệ chút nào). Nếu là thuật toán đếm từ đơn giản, nhìn thấy chữ *bad* là nó phán ngay khách đang chê bai. Nhưng nhờ có cặp từ, cụm **'not bad'** mang lực kéo tích cực rất mạnh, đè bẹp chữ *bad* đứng riêng và đưa xác suất tiêu cực xuống chỉ còn 0.06. 

Điều này chứng minh cỗ máy AI thực sự hiểu được cách diễn đạt tự nhiên nói giảm nói tránh của con người.

---

# Slide 13

Quay trở lại bài toán ra quyết định theo đúng quy tắc nhóm đã cam kết từ đầu: 
Chúng ta chỉ viết lại thông điệp nếu tuần ra mắt xấu hơn bình thường có ý nghĩa thống kê từ 5 điểm phần trăm trở lên. Điều kiện này không xảy ra (H4 chỉ chênh lệch âm 0.3 pp, $p = 0.37$).

Giống như bác sĩ hội chẩn cho bệnh nhân: Bệnh nhân chỉ bị cảm nhẹ chứ không hề gãy chân, thì kê thuốc cảm thôi chứ đừng đè người ta ra bó bột! 

Vì vậy, nhóm đưa ra kết luận dứt khoát: **Không cần viết lại thông điệp truyền thông làm gì cho tốn kém tiền bạc.** Thay vào đó, nhóm kích hoạt nhánh điều chỉnh có mục tiêu vào ba điểm đau thực sự gây phàn nàn có mức chênh lệch vượt ngưỡng 5 điểm phần trăm đã được kiểm chứng: Tình trạng hàng, Dịch vụ ca tối và Giá cả.

---

# Slide 14

Từ kết quả phân tích, nhóm đúc kết thành 6 đề xuất hành động thực tế cho ban lãnh đạo, mỗi đề xuất đều có đủ 3 con số từ 3 tầng dữ liệu trước bảo chứng:
* **R1. Giữ nguyên thông điệp cốt lõi:** Dựa vào Lift tuần ra mắt âm 5.4 pp (Mô tả), kiểm định H4 $p = 0.37$ (Chẩn đoán), và mô hình dự báo tuần tới tiêu cực chỉ quanh mức 38% (Dự đoán).
* **R2. Bổ sung thông tin điểm bán và tồn kho:** Nhắm vào khía cạnh chiếm 1% thảo luận nhưng có Odds tiêu cực gấp 7.2 lần, giúp dập tắt nguồn cơn của 108 phàn nàn trên 10.000 bài viết. Đăng thông báo rõ quán nào còn hàng kẻo khách đến bị hụt hẫng.
* **R3. Tăng cường nhân sự phục vụ vào ca tối:** Khắc phục mức tăng tiêu cực 10.2 điểm phần trăm trong khung giờ từ 18h đến 23h, giảm khoảng 129 bài chê trên 10.000 bài viết.
* **R4. Định vị lại giá bằng combo dùng thử:** Đưa ra voucher quà tặng hoặc combo giảm giá để giải tỏa cảm giác đắt đỏ (Odds Ratio 1.21), giảm 87 bài chê trên 10.000 bài viết.
* **R5. Quảng cáo xoay quanh việc rủ bạn bè trải nghiệm cái mới:** Tận dụng tâm lý thích thử món mới (giúp giảm tiêu cực 7.2 pp) và đi cùng bạn bè (giảm 8.6 pp), tuyệt đối tránh mang tâm lý áp lực công việc vào thông điệp.
* **R6. Vận hành hệ thống giám sát thời gian thực:** Đưa toàn bộ vào cỗ máy AI để theo dõi mỗi ngày.

---

# Slide 15

Hai con số cuối cùng giúp ban giám đốc giữ được cái đầu lạnh và kỳ vọng thực tế:
* Phân tích What-if chỉ ra: Kể cả khi quán có giải quyết triệt để 100% phàn nàn ở cả 3 khuyết điểm trên, tiêu cực toàn ngành cũng chỉ giảm khoảng 0.7 điểm phần trăm do mỗi khía cạnh chiếm tỷ trọng nhỏ. Giống như bạn dọn sạch rác ở một góc công viên thì cả thành phố cũng không thể hết bụi được. Vì vậy, sếp hãy đo KPI riêng cho từng khâu vận hành chứ đừng mơ mộng cả cõi mạng biến mất hoàn toàn ý kiến trái chiều.
* Nhóm thiết lập ngưỡng cảnh báo sớm: **dương 1.5 điểm phần trăm** (dựa trên nguyên tắc trung bình cộng hai lần độ lệch chuẩn từ Chương 4). Vạch này đóng vai trò như chuông báo cháy: nó chỉ báo nhầm đúng 1 lần trong 23 ngày thường, và hoàn toàn yên tĩnh trong tuần ra mắt.

Toàn bộ hệ thống giám sát này đã được nhóm hiện thực hóa thành một Dashboard trực quan bằng Streamlit để theo dõi hàng ngày. 

*(Nếu cô yêu cầu demo: Bật tab Dashboard, trỏ vào KPI −5.1 pp, bấm lọc khía cạnh Availability thấy cột chê nhảy vọt lên gần 80%, và gõ câu tweet mẫu `the new drink is not bad but the line was so long` vào tab Try the model để xem máy phân tích lực kéo từng từ).*

---

# Slide 16

Để kết luận lại toàn bộ bài báo cáo: 
Chiến dịch ra mắt không hề thất bại. Khách hàng chửi là vì đến quán bị hết hàng và phải đứng đợi lâu lúc đông khách. Nhãn hàng hãy tự tin giữ vững thông điệp cốt lõi, điều chỉnh ba điểm đau vận hành và để cỗ máy AI giám sát thị trường mỗi ngày.

Nhóm em cũng nghiêm túc ghi nhận các hạn chế học thuật: Dữ liệu là proxy từ năm 2009, nhãn tự động chưa có lớp trung tính, và kết quả là mối liên hệ tương quan quan sát được. Khi doanh nghiệp áp dụng các điều chỉnh mới, bước đi khoa học tiếp theo bắt buộc phải là một thử nghiệm A/B Testing đối chứng ngoài thực tế.

Thay mặt nhóm VibeCoding_Expert, em xin chân thành cảm ơn cô Linh và các bạn đã chú ý lắng nghe. Nhóm em rất sẵn sàng nhận các câu hỏi phản biện ạ!

---

# Phụ lục: Trả lời nhanh khi bị hỏi xoáy (Slides 17 – 19)

* **Slide 17 (Nếu cô hỏi về công thức z-test H1–H4):**  
  *"Dạ thưa cô, ở Slide 17 nhóm áp dụng đúng kiểm định z hai tỷ lệ gộp từ Chương 5. Vì thực hiện đồng thời 4 kiểm định nên nhóm dùng hiệu chỉnh Holm để kiểm soát sai số gia đình dưới mức 5%, và tính đầy đủ khoảng tin cậy 95% kèm độ lớn hiệu ứng Cohen's h ạ."*

* **Slide 18 (Nếu cô hỏi sao không train riêng trên tập F&B):**  
  *"Dạ thưa cô, dòng cuối cùng của Slide 18 cho thấy khi train riêng trên 84 nghìn bài F&B, ROC-AUC chỉ đạt 0.862, kém xa mức 0.896 khi học trên toàn bộ 1,2 triệu bài. Lý do là ngôn ngữ ẩm thực cần vốn từ vựng cảm xúc phong phú của toàn bộ mạng xã hội thì máy mới học phân loại tốt được ạ."*

* **Slide 19 (Nếu cô hỏi 1,6 triệu bài ban đầu lọc đi đâu):**  
  *"Dạ thưa cô, bảng ở Slide 19 ghi lại chi tiết 5 bước làm sạch theo đúng chuẩn Chương 1: loại bỏ 3.370 dòng mâu thuẫn nhãn, cắt 275.225 dòng lỗi thu thập sau ngày 16/6, dọn dẹp các bài rỗng sau chuẩn hóa và lọc bỏ các bài viết spam bị lặp lại từ bot ạ."*
