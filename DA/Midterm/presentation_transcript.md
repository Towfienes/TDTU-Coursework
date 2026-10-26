# KỊCH BẢN THUYẾT TRÌNH BÁO CÁO GIỮA KỲ (PRESENTATION TRANSCRIPT)
**Đề tài:** Phân tích cảm xúc mạng xã hội cho đợt ra mắt sản phẩm F&B mới (Sentiment140)  
**Môn học:** Phân tích và Trực quan hoá Dữ liệu (Data Analysis & Visualization) – ĐH Tôn Đức Thắng  
**Nhóm:** VibeCoding_Expert (Ngô Lâm Tiến, Nguyễn Công Thành, Nguyễn Lê Nhật Tâm, Ngô Bình Minh)  
**Giảng viên hướng dẫn:** TS. Hồ Thị Linh  

---

## HƯỚNG DẪN DÀNH CHO DIỄN GIẢ (SPEAKER'S GUIDE)

> [!IMPORTANT]
> **Quy tắc vàng của một diễn giả đẳng cấp:**
> 1. **Đừng đọc slide:** Slide là để khán giả nhìn hình, còn bạn là người kể câu chuyện đằng sau những con số.
> 2. **Ký hiệu sân khấu trong kịch bản này:**
>    * `[Dừng 1-2s]`: Ngắt giọng hoàn toàn. Để số liệu thấm vào đầu người nghe trước khi nói tiếp.
>    * `[Nhấn giọng]`: Tăng âm lượng nhẹ hoặc phát âm chậm rãi, dứt khoát vào từ khóa quan trọng.
>    * `[Chỉ tay]` / `[Giao tiếp mắt]`: Hành động hình thể, hướng sự chú ý của cô và cả lớp vào đúng điểm ảnh.
>    * `[Hạ giọng]`: Chuyển sang tông trầm, chia sẻ chân thành, tạo cảm giác khiêm tốn học thuật nhưng bản lĩnh.
> 3. **Tổng thời lượng:** 12 – 14 phút (khoảng 40 – 60 giây mỗi slide).

---

## PHẦN MỞ ĐẦU: ĐẶT BÀI TOÁN & TUYÊN BỐ ĐÁP ÁN (SLIDE 1 – 3)

---

### SLIDE 1: TRANG TIÊU ĐỀ
* **Thời lượng:** 30 giây  
* **Mục tiêu:** Tạo ấn tượng tự tin, lịch thiệp, kéo người nghe vào tình huống thực tế ngay giây đầu tiên.

#### Lời thoại sân khấu:
"Kính thưa cô và các bạn. 

Mình muốn bắt đầu bài báo cáo hôm nay bằng một câu hỏi rất thực tế từ phòng họp Marketing vào sáng thứ Hai: 

`[Dừng 1s - Nhìn thẳng]` *'Chúng ta vừa ra mắt sản phẩm mới được tròn một tuần. Trên mạng bắt đầu có người khen, kẻ chê. Liệu tuần tới... chúng ta có phải đập bỏ toàn bộ chiến dịch quảng cáo để làm lại từ đầu hay không?'* 

Hôm nay, nhóm em đứng đây không phải để đoán mò. Chúng em mang đến câu trả lời rõ ràng, được đúc kết từ 1,6 triệu phản hồi thực tế trên mạng xã hội thông qua 4 cấp độ phân tích dữ liệu chuẩn mực. 

Em xin phép được bắt đầu."

---

### SLIDE 2: BÀI TOÁN KINH DOANH & 4 CẤP ĐỘ PHÂN TÍCH
* **Thời lượng:** 45 giây  
* **Mục tiêu:** Gắn chặt bài làm vào cấu trúc môn học của cô (Chương 1: 4 loại phân tích) và thể hiện tính liêm chính khoa học (Pre-registered hypotheses).

#### Lời thoại sân khấu:
"Để giải quyết áp lực thời gian của ban giám đốc, nhóm bám sát đúng quy trình phân tích từ Chương 1 của môn học. Chúng em chia bài toán lớn thành 4 câu hỏi mạch lạc:

`[Chỉ tay lần lượt 4 khối]`
* **Một - Mô tả:** Tuần vừa qua chuyện gì đã thực sự xảy ra?
* **Hai - Chẩn đoán:** Tại sao lại có những lời chê bai đó?
* **Ba - Dự đoán:** Tuần tới nếu không can thiệp, khách hàng sẽ phản ứng thế nào?
* **Và Bốn - Đề xuất:** Ban lãnh đạo nên hành động cụ thể ra sao?

`[Hạ giọng - Nhấn mạnh]` Đặc biệt, để tránh cái bẫy 'thấy dữ liệu rồi mới bịa ra giả thuyết', nhóm em đã chốt cứng 4 giả thuyết kiểm định từ H1 đến H4, cùng một ngưỡng ý nghĩa thực tiễn tối thiểu là 5 điểm phần trăm ngay từ trước khi chạm vào dữ liệu."

---

### SLIDE 3: TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)
* **Thời lượng:** 60 giây  
* **Mục tiêu:** Cung cấp câu trả lời ngay lập tức (Pyramid Principle), làm cả phòng thi thở phào và bị cuốn hút.

#### Lời thoại sân khấu:
"Và đây là câu trả lời của nhóm em, ngắn gọn trong một câu: 

`[Nhấn giọng từng từ]` **HÃY GIỮ NGUYÊN THÔNG ĐIỆP CỐT LÕI, VÀ TẬP TRUNG SỬA BA ĐIỂM ĐAU VẬN HÀNH.**

Tại sao lại như vậy? 

* `[Chỉ vào số -5.1 pp]` Thứ nhất: Thảo luận về đồ ăn thức uống trên mạng vốn dĩ luôn ít tiêu cực hơn mặt bằng chung khoảng 5 điểm phần trăm. 
* `[Chỉ vào số p = 0.37]` Thứ hai: Kiểm định thống kê chứng minh tuần ra mắt không hề bị tẩy chay. Phản ứng trái chiều vừa qua chỉ là sự pha trộn tự nhiên của thị trường.
* `[Chỉ vào số 0.896]` Và thứ ba: Nhóm đã xây dựng thành công một mô hình phân loại tự động đạt ROC-AUC gần 0.90 trên tuần kiểm thử độc lập, sẵn sàng bắt trọn 84% phàn nàn của khách hàng mỗi ngày.

Vậy cụ thể ba điểm đau cần sửa là gì? Dữ liệu chứng minh điều đó ra sao? Em xin mời bạn Thành trình bày chi tiết về phần dữ liệu và mô tả."

---

## PHẦN 1: DỮ LIỆU & PHÂN TÍCH MÔ TẢ (SLIDE 4 – 7)

---

### SLIDE 4: TẬP DỮ LIỆU & BỘ LỌC F&B
* **Thời lượng:** 45 giây  
* **Mục tiêu:** Giải thích cách xử lý dữ liệu thông minh và minh bạch phương pháp lấy mẫu.

#### Lời thoại sân khấu:
"Cảm ơn bạn Tiến. Thưa cô, nhóm em làm việc trên tập dữ liệu Sentiment140 gồm 1,6 triệu tweet tiếng Anh năm 2009. 

Vì đây là dữ liệu cộng đồng, không có nhãn hàng F&B nào đủ lớn để phân tích độc lập `[Nói nhanh: McCafé năm đó chỉ có 17 tweet]`, nên nhóm em đã dùng toàn bộ 84.632 tweet về ăn uống làm môi trường hội thoại ngành (Category Proxy). 

`[Chỉ vào góc phải]` Để lọc chuẩn xác, nhóm em xây dựng từ điển gồm 41 thương hiệu và 5 nhóm ẩm thực, loại trừ kỹ các từ đa nghĩa như Subway hay Piece of cake. Khi lấy mẫu phân tầng 210 tweet để thẩm định, bộ lọc đạt độ chính xác **89.0%** với khoảng tin cậy 95% dao động an toàn từ 84.8% đến 93.3%."

---

### SLIDE 5: PHÁT HIỆN BẪY CHẤT LƯỢNG DỮ LIỆU (ĐIỂM NHẤN ĐẶC BIỆT)
* **Thời lượng:** 60 giây  
* **Mục tiêu:** Thể hiện con mắt sắc sảo của người làm dữ liệu, biến lỗi của dataset thành chiến công phân tích.

#### Lời thoại sân khấu:
"Thế nhưng, khi vẽ biểu đồ phân phối theo ngày `[Chỉ vào đường đứt gãy]` nhóm em phát hiện ra một cái bẫy chết người trong tập dữ liệu gốc:

`[Hạ giọng - Kể chuyện]` Kể từ 8 giờ 40 sáng ngày 16 tháng 6, dòng tweet tích cực hoàn toàn biến mất. **Hơn 275.000 dòng dữ liệu phía sau... 100% là tweet tiêu cực!** Nguyên nhân là do người thu thập dữ liệu ngày hôm đó đã tắt bot tìm kiếm biểu tượng vui. 

`[Nhấn giọng]` Nếu một người phân tích non tay cứ thế ném dữ liệu vào mô hình, họ sẽ kết luận là chiến dịch sụp đổ hoàn toàn. Nhóm em đã mạnh dạn cắt bỏ 275.000 dòng lỗi này và thực hiện quy trình làm sạch 5 bước nghiêm ngặt. 

Đồng thời, áp dụng đúng bài học Chương 3: Nhóm tuyệt đối không dùng tỷ lệ tiêu cực tuyệt đối, mà luôn đo lường mức nâng (Lift) khi so sánh giữa các nhóm đối chứng."

---

### SLIDE 6: DESCRIPTIVE – BỮA ĂN THƯỜNG NHẬT & MỨC NÂNG
* **Thời lượng:** 45 giây  
* **Mục tiêu:** Rút ra bài học kinh doanh từ biểu đồ Donut và Lift tổng thể.

#### Lời thoại sân khấu:
"Nhìn vào bức tranh mô tả ở Slide 6:

`[Chỉ biểu đồ Donut bên trái]` Hơn một phần ba câu chuyện của khách hàng là về những bữa ăn hàng ngày. Đáng chú ý: **chỉ có 7.5% tweet nhắc đích danh một thương hiệu**. Điều này mang lại bài học xương máu cho đội truyền thông: nếu bạn chỉ lắng nghe những bài viết có tag tên mình, bạn đã bỏ lỡ hơn 90% câu chuyện mà khách hàng đang bàn tán ngoài kia.

`[Chỉ biểu đồ bên phải]` Ở biểu đồ mức nâng: Trong suốt các giai đoạn, F&B luôn ít tiêu cực hơn Twitter chung khoảng 5 điểm phần trăm. Ngay cả trong tuần ra mắt `[chỉ cột giữa]`, mức nâng vẫn là âm 5.4 điểm phần trăm, hoàn toàn bình thường."

---

### SLIDE 7: DESCRIPTIVE – XU HƯỚNG THEO NGÀY & QUY LUẬT PARETO
* **Thời lượng:** 45 giây  
* **Mục tiêu:** Đọc hiểu biểu đồ chuỗi thời gian, giải thích hiện tượng nhiễu mẫu nhỏ.

#### Lời thoại sân khấu:
"Đi sâu vào chuỗi thời gian 39 ngày: Có tới **35 ngày** đường tiêu cực của F&B nằm dưới mức trung bình của Twitter. 

`[Chỉ vào các đỉnh nhô lên]` Cô và các bạn có thể thấy một vài đỉnh nhô cao bất thường. Nhưng khi nhìn vào dải tin cậy 95%, ta thấy dải này phình rất to. Đó đơn giản là những ngày lượng tweet quá ít (dưới 200 tweet), chứ không hề có sự kiện khủng hoảng nào xảy ra. 

Về thương hiệu: Quy luật Pareto 80/20 thể hiện rõ khi 20 trên 41 thương hiệu chiếm 80% lượt thảo luận, riêng Starbucks chiếm hơn 20%.

Tiếp theo, bạn Tâm sẽ giúp chúng ta trả lời câu hỏi: *Vậy người ta chê vì cái gì?*"

---

## PHẦN 2: PHÂN TÍCH CHẨN ĐOÁN (SLIDE 8 – 9)

---

### SLIDE 8: CHẨN ĐOÁN – BỐN GIẢ THUYẾT & Ổ PHÀN NÀN LỚN NHẤT
* **Thời lượng:** 60 giây  
* **Mục tiêu:** Báo cáo kiểm định giả thuyết chặt chẽ và chỉ ra nguyên nhân cốt lõi (Availability).

#### Lời thoại sân khấu:
"Cảm ơn bạn Thành. Thưa cô và các bạn, nhóm em tiến hành kiểm định 4 giả thuyết bằng kiểm định z-test hai tỷ lệ, có hiệu chỉnh đa kiểm định bằng phương pháp Holm từ Chương 5:

`[Chỉ vào bảng giả thuyết]`
* **H1 - Dịch vụ và thời gian chờ:** làm tăng tiêu cực 5.4 điểm phần trăm.
* **H2 - Giá cả và cảm nhận giá trị:** làm tăng 5.6 điểm phần trăm. Cả hai đều được ủng hộ mạnh mẽ.
* **H3 - Cà phê sáng:** lại mang cảm xúc rất tích cực, giảm tiêu cực 6.6 điểm phần trăm.
* **Và H4:** Tuần ra mắt so với tuần thường chỉ chênh lệch âm 0.3 điểm phần trăm, với giá trị $p = 0.37$. Giả thuyết tuần ra mắt bị phản đối đã chính thức bị bác bỏ.

`[Dừng 1s - Nhấn giọng mạnh]` Nhưng con số gây sốc nhất nằm ở dòng đầu tiên: **Khía cạnh Tình trạng hàng (Availability).** 
Những bài viết than phiền vì hết hàng có tỷ lệ tiêu cực lên tới **79.6%**, mức nâng tăng vọt 45.3 điểm phần trăm! Hồi quy Logistic khẳng định: Khách hàng gặp cảnh hết món có Odds tiêu cực gấp **7.2 lần** người bình thường."

---

### SLIDE 9: CHẨN ĐOÁN – THỜI ĐIỂM & BỐI CẢNH (HEATMAP & NMF TOPICS)
* **Thời lượng:** 45 giây  
* **Mục tiêu:** Chứng minh cảm xúc phụ thuộc vào khoảnh khắc chứ không riêng gì sản phẩm.

#### Lời thoại sân khấu:
"Sự bực mình của khách hàng không chỉ nằm ở bản thân món ăn, mà nằm ở thời điểm và hoàn cảnh:

`[Chỉ vào Heatmap]` Heatmap cho thấy phàn nàn về dịch vụ tăng vọt vào **buổi tối** (+10.2 pp). Lúc này khách tan làm, quán đông, nhân viên quá tải dẫn đến chờ lâu. 

`[Chỉ vào biểu đồ bên phải]` Khi chạy mô hình trích xuất chủ đề NMF (đã gạn lọc hết từ khóa đồ ăn), một sự thật thú vị xuất hiện: Chủ đề *Công việc và giờ giải lao* khiến tỷ lệ tiêu cực tăng tới 13.7 điểm phần trăm. Ngược lại, ăn uống quây quần bên gia đình hay nấu nướng tại nhà lại tràn ngập niềm vui.

`[Hạ giọng lịch thiệp]` Tất nhiên, theo bài học Chương 1, đây là dữ liệu quan sát thể hiện mối liên hệ tương quan chứ chưa thể khẳng định nhân quả. 

Vậy làm sao để tuần tới ta tự động bắt được những cảm xúc này? Bạn Minh sẽ trình bày cỗ máy dự đoán."

---

## PHẦN 3: PHÂN TÍCH DỰ ĐOÁN & DIỄN GIẢI (SLIDE 10 – 12)

---

### SLIDE 10: DỰ ĐOÁN – CHIẾN LƯỢC CHIA TẬP THEO THỜI GIAN
* **Thời lượng:** 45 giây  
* **Mục tiêu:** Khẳng định tính chuẩn mực trong thiết kế Machine Learning (Time-based split, không rò rỉ dữ liệu).

#### Lời thoại sân khấu:
"Cảm ơn bạn Tâm. Thưa cô và các bạn, bài toán của nhóm em là: Tuần tới có hàng ngàn tweet đổ về, làm sao để hệ thống tự động gắn nhãn tiêu cực mà không cần con người đọc từng câu?

`[Chỉ vào trục thời gian]` Điểm mấu chốt ở đây: Nhóm em **chia tập train/test theo đúng dòng thời gian thực**:
* Huấn luyện trên tháng 4 và tháng 5 (hơn 650.000 tweet).
* Tinh chỉnh tham số trên tuần ra mắt.
* Và đánh giá duy nhất một lần trên tuần tới (hơn 150.000 tweet).

Tại sao không chia ngẫu nhiên 80/20 như các bài tập thông thường? 
Bởi vì trong thực tế, bạn không thể dùng dữ liệu của tương lai để dự đoán quá khứ. Chia theo thời gian giúp ngăn chặn hoàn toàn rò rỉ dữ liệu giữa các ngày có chung dòng thời sự, và phản ánh đúng sự biến thiên ngôn ngữ theo thời gian."

---

### SLIDE 11: SO SÁNH HAI MÔ HÌNH & KIỂM ĐỊNH MCNEMAR
* **Thời lượng:** 50 giây  
* **Mục tiêu:** Báo cáo kết quả vượt trội của Logistic Regression bằng kiểm định ghép cặp chuẩn xác.

#### Lời thoại sân khấu:
"Nhóm em đặt lên bàn cân hai mô hình: Multinomial Naive Bayes truyền thống và Logistic Regression nâng cao với 300.000 đặc trưng từ đơn và cặp từ.

`[Chỉ vào ROC Curve]` Kết quả trên tuần kiểm thử độc lập:
* Logistic Regression chiến thắng áp đảo với **ROC-AUC đạt 0.896** so với 0.846 của Naive Bayes.
* Độ chính xác đạt 81.0%, và quan trọng nhất: nó tóm gọn **84.3%** các bài viết tiêu cực.

`[Nhấn giọng]` Vì hai mô hình cùng chấm điểm trên một tập tweet, nhóm em áp dụng đúng kiểm định phi tham số **McNemar** từ Chương 5. Kết quả cho thấy Logistic Regression giúp giảm chính xác 440 lỗi gán nhãn sai trên mỗi 10.000 tweet ($p < 0.001$). 

Các kiểm tra độ vững ở Phụ lục B cũng khẳng định mô hình khái quát cực tốt trên cả người dùng mới lẫn người dùng cũ."

---

### SLIDE 12: DIỄN GIẢI MÔ HÌNH – MÔ HÌNH BIẾT ĐỌC HIỂU PHỦ ĐỊNH
* **Thời lượng:** 60 giây  
* **Mục tiêu:** Biến Machine Learning từ "hộp đen" thành công cụ trực quan, minh bạch tuyệt đối.

#### Lời thoại sân khấu:
"Nhiều người e ngại Machine Learning là một 'hộp đen bí ẩn'. Nhưng mô hình của nhóm em hoàn toàn đọc được như một bảng chỉ số:

`[Chỉ biểu đồ Waterfall bên phải - Điểm ăn tiền]` Hãy nhìn vào ví dụ thực tế này: Một khách hàng viết: *'that's not bad at all...'* (món này không tệ chút nào).
* Nếu là thuật toán đếm từ đơn giản, nhìn thấy chữ *'bad'* nó sẽ phán ngay đây là lời chê.
* Nhưng mô hình của nhóm em có cặp từ (bigram). Cụm từ **'not bad'** mang một hệ số âm cực lớn, kéo phăng xác suất tiêu cực xuống chỉ còn 0.06!

Ở biểu đồ Waterfall, từng thanh màu thể hiện chính xác lực đẩy của từng từ: từ nào kéo về giận dữ, từ nào kéo về hài lòng. Đây chính là phiên bản tuyến tính của SHAP, minh bạch 100% trước ban lãnh đạo."

---

## PHẦN 4: ĐỀ XUẤT, GIÁM SÁT & KẾT LUẬN (SLIDE 13 – 16)

---

### SLIDE 13: QUY TẮC QUYẾT ĐỊNH (PRE-REGISTERED DECISION RULE)
* **Thời lượng:** 40 giây  
* **Mục tiêu:** Chuyển giao mượt mà sang Tầng 4, khẳng định tính nhất quán khoa học của nhóm.

#### Lời thoại sân khấu:
"Quay trở lại với bạn Tiến để chốt lại bài toán kinh doanh.

Cảm ơn bạn Minh. Thưa cô và các bạn, nhóm em xin nhắc lại quy tắc quyết định đã được thiết lập từ đầu:
* Chúng ta chỉ viết lại thông điệp nếu tuần ra mắt xấu hơn bình thường có ý nghĩa thống kê và tệ hơn từ 5% trở lên. Điều kiện này **không xảy ra** (H4 âm 0.3 pp, $p = 0.37$).
* Do đó, quyết định tối ưu là: **KÍCH HOẠT ĐIỀU CHỈNH CÓ MỤC TIÊU** vào đúng ba điểm đau đã vượt ngưỡng 5 pp: Tình trạng hàng, Dịch vụ và Giá cả."

---

### SLIDE 14: SÁU ĐỀ XUẤT HÀNH ĐỘNG GẮN CHẶT VỚI CON SỐ
* **Thời lượng:** 60 giây  
* **Mục tiêu:** Trình bày 6 đề xuất sắc bén, mỗi đề xuất đều có đủ 3 con số (Mô tả, Chẩn đoán, Dự đoán).

#### Lời thoại sân khấu:
"Nhóm em đúc kết thành 6 đề xuất hành động thực chiến, mỗi đề xuất đều có bảo chứng từ ba tầng dữ liệu trước:

`[Nói nhanh, dứt khoát từng đề xuất]`
* **R1:** Giữ nguyên thông điệp quảng cáo cốt lõi. Tuần tới mô hình dự báo tỷ lệ tiêu cực chỉ quanh mức 38%, không có khủng hoảng.
* **R2:** Bổ sung ngay thông tin điểm bán và tình trạng tồn kho trên Fanpage. Cắt đứt nguồn cơn của 108 phàn nàn trên mỗi 10.000 bài viết.
* **R3:** Tăng cường nhân sự phục vụ vào ca tối (từ 18h đến 23h), nơi phàn nàn tăng thêm 10.2 điểm phần trăm.
* **R4:** Định vị lại giá bằng combo dùng thử hoặc voucher quà tặng để giải tỏa áp lực đắt đỏ.
* **R5:** Thiết kế nội dung quảng bá xoay quanh việc *'rủ bạn bè trải nghiệm cái mới'* (giảm tiêu cực tới 8.6 pp), tuyệt đối tránh mang tâm lý áp lực công việc vào thông điệp.
* **Và R6:** Đưa toàn bộ vào hệ thống giám sát thời gian thực mỗi ngày."

---

### SLIDE 15: PHÂN TÍCH WHAT-IF, NGƯỠNG CẢNH BÁO & DASHBOARD
* **Thời lượng:** 60 giây (Kèm thao tác chuyển tab sang Streamlit)  
* **Mục tiêu:** Quản trị kỳ vọng thực tế, giới thiệu ngưỡng kiểm soát chất lượng và mở Dashboard.

#### Lời thoại sân khấu:
"Hai con số cuối cùng giúp ban giám đốc giữ được cái đầu lạnh:
* Phân tích What-if chỉ ra: Kể cả ta xóa sạch 100% phàn nàn ở cả ba khía cạnh trên, tiêu cực toàn ngành cũng chỉ giảm khoảng 0.7 điểm phần trăm, vì mỗi khía cạnh chỉ chiếm một góc nhỏ. Do đó, KPI phải đặt riêng cho từng khía cạnh chứ không đặt chung chung.
* Nhóm em thiết lập vạch cảnh báo chất lượng: **+1.5 điểm phần trăm** (dựa trên nguyên tắc trung bình cộng hai lần độ lệch chuẩn từ Chương 4). Vạch này chỉ báo nhầm đúng 1 lần trong 23 ngày thường, và hoàn toàn yên tĩnh trong tuần ra mắt.

`[Chuyển màn hình sang Dashboard]` Và toàn bộ quy trình này đã được nhóm hiện thực hóa thành một công cụ Dashboard tương tác trực tiếp bằng Streamlit."

---

### KỊCH BẢN THAO TÁC DASHBOARD (60 GIÂY VÀNG)
*(Minh hoặc Tiến vừa cầm chuột click vừa nói)*:

1. **Giây 0 – 15:** *"Trên màn hình Overview, thẻ KPI cập nhật tự động mức nâng âm 5.1 pp và đường xu hướng tuần ra mắt hoàn toàn êm ả."*
2. **Giây 15 – 30:** *(Click sang tab Aspects, chọn Availability)*: *"Khi lọc riêng khía cạnh Availability, cô có thể thấy cột tiêu cực lập tức vọt lên chạm mức 80%, khoanh vùng chính xác điểm nóng vận hành."*
3. **Giây 30 – 50:** *(Click sang tab 'Try the model', gõ câu tweet mẫu)*: 
   `"the new drink is not bad but the wait was too long and they ran out of ice"`
   *"Bấm dự đoán: Mô hình lập tức trả về xác suất tiêu cực. Biểu đồ Waterfall bên dưới bóc tách rõ: cụm 'not bad' màu xanh kéo về khen, nhưng 'ran out' và 'too long' màu đỏ đẩy mạnh về chê."*
4. **Giây 50 – 60:** *"Người quản lý cũng có thể đổi nguồn dữ liệu sang nhãn dự báo của AI để theo dõi tức thời các luồng thảo luận mới đổ về."*

---

### SLIDE 16: KẾT LUẬN & HẠN CHẾ HỌC THUẬT
* **Thời lượng:** 40 giây  
* **Mục tiêu:** Khép lại bài thuyết trình trang trọng, khiêm tốn nhưng đĩnh đạc.

#### Lời thoại sân khấu:
"Để khép lại bài thuyết trình: 
Thông điệp ra mắt không có lỗi. Lỗi nằm ở khâu vận hành lúc đông khách và hết hàng. Hãy giữ vững thông điệp, điều chỉnh ba điểm đau và để cỗ máy AI giám sát thị trường mỗi ngày.

Nhóm cũng nghiêm túc ghi nhận các hạn chế: dữ liệu proxy từ năm 2009, nhãn tự động chưa có lớp trung tính, và đây là nghiên cứu quan sát. Khi nhãn hàng triển khai thông điệp mới, bước đi khoa học tiếp theo bắt buộc phải là một thử nghiệm A/B Testing đối chứng.

Thay mặt nhóm VibeCoding_Expert, em xin chân thành cảm ơn cô Linh và các bạn đã chú ý lắng nghe. Nhóm em rất sẵn sàng nhận các câu hỏi phản biện ạ!"

---

## PHẦN PHỤ LỤC: PHẢN XẠ NHANH KHI BỊ CHẤM HỎI (SLIDE 17 – 19)

---

### SLIDE 17 (APPENDIX A): CÁC BẢNG KIỂM ĐỊNH H1 – H4
* **Bật khi giảng viên hỏi:** *"Công thức kiểm định giả thuyết của em tính thế nào? Có hiệu chỉnh sai số gia đình không?"*
* **Lời đáp nhanh:** 
  > *"Dạ thưa cô, ở Slide 17, nhóm áp dụng đúng kiểm định z-test hai tỷ lệ gộp từ Chương 5. Vì thực hiện đồng thời 4 kiểm định nên nhóm dùng hiệu chỉnh Holm để kiểm soát Family-wise Error Rate dưới mức $\alpha = 0.05$. Độ lớn hiệu ứng Cohen's h đều được tính kèm khoảng tin cậy 95% tương ứng ạ."*

---

### SLIDE 18 (APPENDIX B): ĐỘ VỮNG CỦA LOGISTIC REGRESSION
* **Bật khi giảng viên hỏi:** *"Tại sao em không huấn luyện mô hình riêng trên 84 nghìn tweet F&B mà phải train trên toàn bộ 1,2 triệu tweet?"*
* **Lời đáp nhanh:** 
  > *"Dạ thưa cô, xin mời cô nhìn vào dòng cuối cùng của Slide 18: Nhóm đã thực nghiệm huấn luyện riêng trên tập F&B, nhưng kết quả AUC chỉ đạt 0.862, kém xa mức 0.896 khi học trên toàn bộ dữ liệu. Lý do là ngôn ngữ ẩm thực cần vốn từ vựng phong phú về mặt cảm xúc của toàn bộ 1,2 triệu tweet thì mới nhận diện được các cách diễn đạt phức tạp ạ."*

---

### SLIDE 19 (APPENDIX C): NHẬT KÝ LÀM SẠCH DỮ LIỆU (CLEANING LOG)
* **Bật khi giảng viên hỏi:** *"Tại sao từ 1,6 triệu tweet ban đầu lại ra được 1,27 triệu tweet sạch? Bỏ những gì?"*
* **Lời đáp nhanh:** 
  > *"Dạ thưa cô, bảng ở Slide 19 ghi lại chi tiết 5 bước làm sạch theo đúng quy chuẩn 'Document all changes' của Chương 1: loại bỏ 3.370 dòng mâu thuẫn nhãn, cắt bỏ 275.225 dòng lỗi thu thập sau ngày 16/6, dọn dẹp các tweet rỗng sau chuẩn hóa và loại bỏ các bài viết spam bị lặp lại từ bot ạ."*

---
*Kịch bản hoàn tất – Chúc nhóm VibeCoding_Expert tự tin làm chủ sân khấu và đạt kết quả xuất sắc nhất!*
