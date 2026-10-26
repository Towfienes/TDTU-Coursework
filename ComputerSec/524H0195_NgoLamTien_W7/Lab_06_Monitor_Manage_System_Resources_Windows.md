# BÁO CÁO THỰC HÀNH CHI TIẾT
## Lab: Monitor and Manage System Resources in Windows

**Học phần:** An toàn Máy tính / Quản trị Hệ thống  
**Sinh viên thực hiện:** Ngô Lâm Tiến  
**Mã số sinh viên (MSSV):** 524H0195  
**Lớp / Khóa:** Đại học Tôn Đức Thắng (TDTU)  
**Thời gian thực hiện:** Học kỳ thực hành - Tuần 7  

---

### I. MỤC TIÊU BÀI LAB (OBJECTIVES)
1. Sử dụng các công cụ quản trị nâng cao (**Administrative Tools**) trong Windows để giám sát và phân tích tài nguyên phần cứng thời gian thực.
2. Khảo sát chu trình hoạt động (Start/Stop/Disable) của dịch vụ hệ thống thông qua dịch vụ **Routing and Remote Access (RRAS)**.
3. Sử dụng công cụ **Performance Monitor** (`perfmon.exe`) để theo dõi các bộ đếm hiệu năng (Performance Counters).
4. Phân tích nhật ký sự kiện hệ thống trong **Computer Management** (`compmgmt.msc` / Event Viewer).
5. Thiết lập bộ thu thập dữ liệu tự động (**Data Collector Sets**) để trích xuất tệp nhật ký hiệu năng bộ nhớ định dạng CSV và phân tích dữ liệu.

---

### II. YÊU CẦU HỆ THỐNG VÀ CÔNG CỤ (REQUIRED RESOURCES)
- 01 Máy tính hoặc máy ảo chạy Microsoft Windows 10/11 có kết nối mạng.
- Quyền Quản trị viên (Administrator).
- Các tiện ích Windows: Services (`services.msc`), Performance Monitor (`perfmon.exe`), Computer Management (`compmgmt.msc`).

---

### III. NỘI DUNG VÀ BÁO CÁO KẾT QUẢ TỪNG BƯỚC

#### PHẦN 1: KHỞI ĐỘNG VÀ DỪNG DỊCH VỤ ROUTING AND REMOTE ACCESS (RRAS)

- Vào Control Panel > Administrative Tools > mở tiện ích **Services**.
- Tìm dịch vụ **Routing and Remote Access**. Nhấp đúp mở Properties > chuyển Startup type thành **Manual** > nhấn Apply.
- Mở song song công cụ **Performance Monitor** (`perfmon.exe`) và cửa sổ **Network Connections** (`ncpa.cpl`).
- Trong Performance Monitor, nhấp vào biểu tượng **Unfreeze Display** để bắt đầu ghi biểu đồ.
- Quay lại cửa sổ dịch vụ RRAS, nhấn nút **Start** để khởi chạy dịch vụ.
- Chuyển sang cửa sổ Network Connections, nhấn phím **F5** để làm mới.

> **CÂU HỎI PHẦN 1 - BƯỚC m:**  
> **Những thay đổi nào xuất hiện trong cửa sổ sau khi khởi động dịch vụ Routing and Remote Access?**  
> *(What changes appear in the window after starting the Routing and Remote Access service?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Trong cửa sổ Network Connections, xuất hiện thêm một biểu tượng kết nối mạng mới có tên là **"Incoming Connections"** (Kết nối đến) hoặc các adapter giao tiếp ảo liên quan đến tính năng định tuyến và truy cập từ xa (VPN/NAT Routing).

- Quay lại cửa sổ Properties của RRAS, nhấn nút **Stop** để dừng dịch vụ.
- Chuyển sang cửa sổ Network Connections và kiểm tra.

> **CÂU HỎI PHẦN 1 - BƯỚC o:**  
> **Những thay đổi nào xuất hiện trong ngăn bên phải sau khi ngừng dịch vụ Routing and Remote Access?**  
> *(What changes appear in the right pane after stopping the Routing and Remote Access service?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Biểu tượng **"Incoming Connections"** biến mất khỏi danh sách các kết nối mạng (hoặc chuyển sang trạng thái ngắt kết nối/vô hiệu hóa hoàn toàn).

- Quay lại cửa sổ Performance Monitor, nhấn nút **Freeze Display** để dừng ghi nhận đồ thị.

> **CÂU HỎI PHẦN 1 - BƯỚC p:**  
> **Bộ đếm (Counter) nào đang được ghi lại nhiều nhất trong biểu đồ (gợi ý: hãy nhìn vào màu biểu đồ và màu Counter)?**  
> *(Which counter is being recorded the most in the graph?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Bộ đếm **`% Processor Time`** (Thời gian xử lý của CPU, thường được biểu diễn bằng đường màu xanh lá cây hoặc đỏ tùy theo theme mặc định) hoặc bộ đếm **`Pages/sec`** của bộ nhớ Memory có biên độ dao động mạnh nhất tại thời điểm dịch vụ khởi động và giải phóng tài nguyên.

- Nhấp vào menu đổ xuống **Change graph type** > chọn chế độ xem **Report**.

> **CÂU HỎI PHẦN 1 - BƯỚC q-r:**  
> **Những giá trị nào được hiển thị bởi counter?**  
> *(What values are displayed by the counter?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Chế độ Report hiển thị các số liệu thống kê chi tiết bao gồm:  
> - **Last:** Giá trị tức thời tại thời điểm dừng đo.  
> - **Average:** Giá trị trung bình của toàn bộ chu kỳ ghi nhận.  
> - **Minimum:** Giá trị nhỏ nhất ghi nhận được.  
> - **Maximum:** Giá trị đỉnh cao nhất trong chu kỳ kiểm thử.

- Trong cửa sổ Properties của RRAS, chuyển Startup type sang **Disabled** và nhấn OK.
- Kiểm tra lại cửa sổ Services.

> **CÂU HỎI PHẦN 1 - BƯỚC t:**  
> **Status và Startup Type cho Routing and Remote Access là gì?**  
> *(What are the Status and Startup Type for Routing and Remote Access?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - Cột **Status**: Trống (Blank / Stopped - dịch vụ đã dừng hoạt động hoàn toàn).  
> - Cột **Startup Type**: **Disabled** (Bị vô hiệu hóa, không thể tự khởi động cùng Windows).

---

#### PHẦN 2: LÀM VIỆC VỚI COMPUTER MANAGEMENT (EVENT VIEWER)

- Mở tiện ích: Control Panel > Administrative Tools > **Computer Management** (`compmgmt.msc`).
- Điều hướng đến: **System Tools** > **Event Viewer** > **Windows Logs** > **System**.
- Tìm các bản ghi sự kiện có Source là **Service Control Manager** liên quan đến dịch vụ Routing and Remote Access.

> **CÂU HỎI PHẦN 2 - BƯỚC d:**  
> **Mô tả gì cho từng sự kiện trong số bốn sự kiện?**  
> *(What is the description for each of the four events?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Bốn sự kiện liên tiếp của dịch vụ (mã **Event ID 7036**) mô tả chính xác quy trình vòng đời của dịch vụ:  
> 1. **Sự kiện 1 (Bắt đầu khởi động):**  
>    `The Routing and Remote Access service entered the start type / running state.` (Dịch vụ chuyển sang trạng thái bắt đầu hoạt động).  
> 2. **Sự kiện 2 (Khởi chạy thành công):**  
>    Thông báo dịch vụ Routing and Remote Access đã khởi chạy thành công và các tiến trình phụ thuộc liên quan đã sẵn sàng phục vụ.  
> 3. **Sự kiện 3 (Bắt đầu dừng):**  
>    `The Routing and Remote Access service entered the stop pending state.` (Hệ thống gửi tín hiệu yêu cầu dịch vụ chuẩn bị dừng và giải phóng socket).  
> 4. **Sự kiện 4 (Dừng hoàn toàn):**  
>    `The Routing and Remote Access service entered the stopped state.` (Dịch vụ đã dừng hoạt động hoàn toàn và tài nguyên được thu hồi).

---

#### PHẦN 3: CẤU HÌNH DATA COLLECTOR SETS TRONG ADMINISTRATIVE TOOLS

- Trong Performance Monitor, mở rộng mục **Data Collector Sets** > nhấp chuột phải vào **User Defined** > chọn **New** > **Data Collector Set**.
- Đặt tên bộ thu thập: **`Memory Logs`**. Chọn tùy chọn **Create manually (Advanced)** > Next.
- Tích chọn loại dữ liệu: **Performance counter** > Next.
- Nhấn **Add...** để chọn bộ đếm: Tìm đến nhóm **Memory** > chọn **Available MBytes** > nhấn **Add>>** > nhấn OK.
- Đặt khoảng thời gian lấy mẫu (**Sample interval**): **`4 seconds`** > Next.
- Vị trí lưu trữ dữ liệu (**Where would you like the data to be saved?**): Chọn đường dẫn thư mục `C:\PerfLogs` > Next > Finish.
- Mở rộng mục User Defined > chọn `Memory Logs`. Nhấp chuột phải vào `DataCollector01` > chọn **Properties**.
- Tại mục **Log format**, chuyển sang định dạng **Comma Separated** (tệp CSV).
- Chuyển sang thẻ **File** để kiểm tra đường dẫn.

> **CÂU HỎI PHẦN 3 - BƯỚC n:**  
> **Tên đường dẫn đầy đủ đến file ví dụ là gì?**  
> *(What is the full path name to the example file?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Tên đường dẫn đầy đủ của tệp log hiệu năng là:  
> **`C:\PerfLogs\Memory Logs\DataCollector01.csv`**  
> *(hoặc có dạng cấu trúc gắn nhãn thời gian: `C:\PerfLogs\<ComputerName>_YYYYMMDD-000001\DataCollector01.csv`)*.

- Chọn `Memory Logs` ở khung bên trái, nhấn biểu tượng **mũi tên màu xanh lá cây** (Play) để bắt đầu thu thập dữ liệu.
- Mở và đóng trình duyệt web vài lần để tạo tải tiêu thụ RAM.
- Nhấn biểu tượng **ô vuông màu đen** (Stop) để dừng thu thập dữ liệu.

> **CÂU HỎI PHẦN 3 - BƯỚC q:**  
> **Bạn nhận thấy có sự thay đổi nào đối với biểu tượng Memory Logs?**  
> *(What change do you notice to the Memory Logs icon?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - Khi đang chạy (Running/Recording): Biểu tượng có thêm một dấu tròn nhỏ chứa mũi tên xanh Play (thể hiện tiến trình thu thập đang hoạt động).  
> - Khi nhấn dừng (Stopped): Biểu tượng quay trở lại trạng thái tĩnh bình thường, không còn biểu tượng Play.

- Vào `C:\PerfLogs`, mở thư mục vừa tạo và mở tệp `DataCollector01.csv` bằng Notepad hoặc Excel.

> **CÂU HỎI PHẦN 3 - BƯỚC r:**  
> **Cột xa nhất bên phải hiển thị thông tin gì?**  
> *(What information is displayed in the farthest right column?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Cột ngoài cùng bên phải hiển thị giá trị số đo thực tế của bộ đếm hiệu năng đã chọn: **Dung lượng bộ nhớ RAM còn trống khả dụng tính theo Megabyte (`\\<PC-NAME>\Memory\Available MBytes`)** tại từng mốc thời gian lấy mẫu cách nhau 4 giây.

- Dọn dẹp hệ thống: Xóa Data Collector Set `Memory Logs` trong Performance Monitor và xóa thư mục dữ liệu đã tạo trong `C:\PerfLogs`.

---

### IV. BÀI HỌC VÀ KẾT LUẬN (CONCLUSION)
- **Quản trị dịch vụ an toàn:** Các dịch vụ mạng không cần thiết (như Routing and Remote Access) nếu để ở trạng thái tự động khởi động sẽ mở rộng bề mặt tấn công. Cần tắt (Disabled) các dịch vụ này theo chuẩn Hardening.
- **Tự động hóa giám sát:** Data Collector Sets trong Performance Monitor là công cụ đắc lực giúp xây dựng đường cơ sở hiệu năng (Performance Baseline), phát hiện sớm các hiện tượng rò rỉ bộ nhớ (Memory Leak) hoặc phát hiện các tiến trình độc hại tiêu thụ tài nguyên ngầm.
