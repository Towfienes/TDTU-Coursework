# BÁO CÁO THỰC HÀNH CHI TIẾT
## Lab 6: Hệ Điều Hành và Kiểm Soát Truy Cập (Windows Access Control & Auditing)

**Học phần:** An toàn Máy tính / An ninh Hệ điều hành  
**Sinh viên thực hiện:** Ngô Lâm Tiến  
**Mã số sinh viên (MSSV):** 524H0195  
**Lớp / Khóa:** Đại học Tôn Đức Thắng (TDTU)  
**Thời gian thực hiện:** Học kỳ thực hành - Tuần 7  

---

### I. MỤC TIÊU BÀI LAB (OBJECTIVES)
1. Nắm vững khung kiến trúc kiểm soát truy cập (Access Control Framework) trên nền tảng Microsoft Windows.
2. Khảo sát và phân tích tác động của các thuộc tính tệp cơ bản: **Read-Only** (Chỉ đọc) và **Hidden** (Ẩn).
3. Tìm hiểu danh sách kiểm soát truy cập tùy ý (**DACL** - Discretionary Access Control List) của hệ thống tệp **NTFS**: phân biệt giữa quyền cơ bản (Standard Permissions) và quyền nâng cao (Advanced/Granular Permissions).
4. Phân tích nguyên tắc ưu tiên trong kiểm soát truy cập của Windows: **Deny overrides Allow** (Quyền từ chối luôn phủ quyết quyền cho phép).
5. Nghiên cứu cơ chế kiểm toán bảo mật (**Security Auditing**): cấu hình chính sách kiểm toán truy cập đối tượng (**Object Access Auditing**), giám sát Security Logs và phân tích **Event IDs** (4663, 4656, 7036).

---

### II. YÊU CẦU HỆ THỐNG VÀ MÔI TRƯỜNG (REQUIRED RESOURCES)
- Máy tính hoặc máy ảo chạy Microsoft Windows 10/11 Pro/Enterprise (hoặc Windows 7/Server).
- Tài khoản quản trị viên: `Admin` / `Administrator`.
- Các tài khoản người dùng kiểm thử được tạo theo tên sinh viên: `ngolamtien` và `ngolamtien1`.
- Thư mục thực hành trên ổ đĩa hệ thống: `C:\doctemp`.

---

### III. NỘI DUNG VÀ BÁO CÁO KẾT QUẢ TỪNG BƯỚC

#### PHẦN 1: KIỂM SOÁT TRUY CẬP (ACCESS CONTROL)

##### Bài 1: Thêm tài khoản người dùng vào hệ thống
1. Đăng nhập vào tài khoản Quản trị viên (`Admin`).
2. Vào Start > Control Panel > User Accounts > Manage Accounts > Create a new account.
3. Nhập tên tài khoản: **`ngolamtien`** (viết thường, không dấu, không khoảng trắng). Chọn loại tài khoản: **Standard User**.
4. Nhấn nút "Create Account" để hoàn tất tạo tài khoản.

---

##### Bài 2: Khảo sát tác dụng của thuộc tính Read-Only và Hidden
1. Đăng nhập tài khoản `Admin`.
2. Mở Notepad, tạo tệp văn bản và lưu tại đường dẫn: `C:\doctemp\file1_ngolamtien.txt`.
3. Mở File Explorer, điều hướng đến `C:\doctemp`, nhấp chuột phải vào `file1_ngolamtien.txt` > chọn **Properties**.
4. Tại mục **Attributes** ở thẻ General, đánh dấu chọn **Read-Only**, sau đó nhấn OK.
5. Mở lại tệp này bằng Notepad, thêm một dòng nội dung mới và nhấn `Ctrl + S` (Save).

> **CÂU HỎI BÀI 2 - BƯỚC 6.a:**  
> **Điều gì xảy ra? Giải thích tại sao.**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - **Hiện tượng:** Notepad không cho phép lưu đè nội dung trực tiếp vào tệp cũ. Thay vào đó, hộp thoại **"Save As"** tự động bật lên yêu cầu người dùng phải lưu thành một tệp có tên khác. Nếu cố tình chọn lưu đè vào tên `file1_ngolamtien.txt`, Windows sẽ đưa ra thông báo lỗi:  
>   `"file1_ngolamtien.txt is read-only. Try saving the file with a new name."` hoặc `"Access is denied"`.  
> - **Giải thích kỹ thuật:** Thuộc tính `Read-Only` là một cờ thuộc tính hệ thống (File Attribute Flag) được quản lý ở tầng hệ thống tệp NTFS/FAT. Khi thuộc tính này được bật, hệ điều hành thiết lập cờ chỉ cho phép mở tệp dưới quyền đọc (`GENERIC_READ`). Mọi yêu cầu cấp quyền ghi (`GENERIC_WRITE`) đều bị nhân hệ điều hành từ chối ở bước kiểm tra file handle, nhằm bảo vệ tính toàn vẹn và ngăn ngừa việc vô tình sửa đổi hoặc ghi đè dữ liệu gốc.

6. Đăng xuất khỏi tài khoản `Admin` và đăng nhập vào tài khoản `ngolamtien`.
7. Mở thư mục `C:\doctemp`, nhấp chuột phải vào `file1_ngolamtien.txt` > Properties > đánh dấu chọn thuộc tính **Hidden** > nhấn OK. Đóng cửa sổ và mở lại thư mục `C:\doctemp`.

> **CÂU HỎI BÀI 2 - BƯỚC 9.a:**  
> **Bây giờ bạn có thấy file không?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> **Không thấy file.** Tệp tin `file1_ngolamtien.txt` đã biến mất khỏi giao diện hiển thị của File Explorer (với cấu hình mặc định ẩn tệp hệ thống).

> **CÂU HỎI BÀI 2 - BƯỚC 9.b:**  
> **Nếu bạn không thấy file, hãy thử tìm cách khác để hiện file ẩn.**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Các phương thức để làm xuất hiện và truy cập tệp tin ẩn:  
> 1. **Qua giao diện đồ họa File Explorer:**  
>    - Vào thanh menu `View` trên thanh Ribbon > tích chọn vào ô **Hidden items**.  
>    - Hoặc vào `View` > `Options` > `Change folder and search options` > chuyển sang thẻ `View` > tích chọn radio button **"Show hidden files, folders, and drives"** > nhấn Apply và OK.  
> 2. **Qua giao diện dòng lệnh Command Prompt (CMD):**  
>    - Sử dụng lệnh hiển thị tệp ẩn: `dir /a:h C:\doctemp`  
>    - Bỏ thuộc tính ẩn của tệp: `attrib -h C:\doctemp\file1_ngolamtien.txt`  
> 3. **Qua PowerShell:**  
>    - Sử dụng lệnh: `Get-ChildItem -Path C:\doctemp -Force`

---

##### Bài 3: Cấp quyền tường minh cho các user khác nhau đối với một file cho trước
1. Đăng nhập tài khoản `Admin`.
2. Dùng Notepad tạo tệp: `C:\doctemp\file2_ngolamtien.txt`.
3. Nhấp chuột phải vào tệp > Properties > chuyển sang thẻ **Security** > nhấn nút **Edit...**.
4. Nhấn **Add...**, nhập tên `ngolamtien`, nhấn **Check Names** để hệ thống xác thực SID tài khoản, sau đó nhấn OK.

> **CÂU HỎI BÀI 3 - BƯỚC 6:**  
> **Quyền mặc định (default permissions) cho user này là gì? Trong khi vẫn xem các option của tab Security cho file này, hãy xem các quyền được chỉ định cho nhóm Users. Các quyền mặc định cho nhóm này có khác với quyền của người dùng bạn đã thêm để có quyền truy cập vào file không?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - **Quyền mặc định khi thêm user `ngolamtien`:** Hệ thống tự động gán các quyền cơ bản: **Read & execute** và **Read**.  
> - **Quyền được chỉ định cho nhóm `Users`:** Mặc định nhóm `Users` kế thừa từ thư mục cha bao gồm: **Read & execute** và **Read** (và đối với thư mục có thêm `List folder contents`).  
> - **So sánh và Phân tích khác biệt:**  
>   Về mặt quyền hạn cụ thể (Read, Read & Execute), hai nhóm này nhìn bên ngoài có vẻ tương đương. Tuy nhiên, về mặt bản chất cấu trúc bảng DACL:  
>   1. Nhóm `Users` nhận quyền thông qua cơ chế **Kế thừa (Inherited Permissions)** từ thư mục gốc ổ đĩa `C:\`.  
>   2. User `ngolamtien` nhận quyền thông qua **Cấp quyền tường minh (Explicit Permission)** trực tiếp trên tệp `file2_ngolamtien.txt`.  
>   3. Trong thuật toán đánh giá DACL của Windows, **Explicit ACE luôn có độ ưu tiên cao hơn Inherited ACE**. Điều này đảm bảo rằng các tinh chỉnh bảo mật trực tiếp trên tệp sẽ luôn được ưu tiên áp dụng trước quyền kế thừa từ nhóm.

5. Nhấp nút **Advanced** trong thẻ Security > chọn user `ngolamtien` > nhấn nút **Edit** để mở cửa sổ phân quyền chuyên sâu.

> **CÂU HỎI BÀI 3 - BƯỚC 8:**  
> **Bạn thấy gì? Nó khác với các quyền trong tab security cha như thế nào? Có mối liên hệ nào không?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - **Những gì quan sát được:** Cửa sổ **Permission Entry for file2_ngolamtien.txt** hiển thị danh sách 14 quyền chi tiết dạng vi mô (Granular / Advanced Permissions):  
>   - *Traverse folder / execute file*  
>   - *List folder / read data*  
>   - *Read attributes*  
>   - *Read extended attributes*  
>   - *Create files / write data*  
>   - *Create folders / append data*  
>   - *Write attributes*  
>   - *Write extended attributes*  
>   - *Delete subfolders and files*  
>   - *Delete*  
>   - *Read permissions*  
>   - *Change permissions (Write DAC)*  
>   - *Take ownership (Write Owner)*  
>   - *Synchronize*  
> - **Sự khác biệt và Mối liên hệ:**  
>   - Thẻ Security cha chỉ là giao diện tóm tắt (High-level / Standard Permissions: Full control, Modify, Read & execute, Read, Write) nhằm phục vụ thao tác nhanh của người dùng phổ thông.  
>   - Mỗi quyền ở tab Security cha thực chất là một tập hợp (macro mapping) của các quyền chi tiết trong cửa sổ Advanced. Ví dụ:  
>     - Quyền **Read** ở tab cha thực chất bao gồm 4 quyền nâng cao: *List folder / read data*, *Read attributes*, *Read extended attributes*, và *Read permissions*.  
>     - Quyền **Write** ở tab cha bao gồm: *Create files / write data*, *Create folders / append data*, *Write attributes*, *Write extended attributes*.  
>     - Quyền **Full Control** là sự kết hợp của toàn bộ 14 quyền nâng cao.

---

##### Bài 4: Hiểu cơ chế kiểm soát truy cập của MS Windows (Deny overrides Allow)
1. Đăng nhập tài khoản `Admin`.
2. Tạo thêm một người dùng Standard mới có tên: **`ngolamtien1`**.
3. Tạo thư mục: `C:\doctemp\folderngolamtien`.
4. Mở Properties thư mục > thẻ Security > Edit > Add user `ngolamtien1`.

> **CÂU HỎI BÀI 4 - BƯỚC 7:**  
> **Chọn user ngolamtien1 trong cửa sổ Permissions. Quyền gì hiện được gán cho user này?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> User `ngolamtien1` được gán các quyền mặc định: **Read & execute**, **List folder contents**, và **Read**.

5. Đánh dấu chọn quyền **List folder contents** tại cột **Deny**. Nhấn OK (Windows hiển thị thông báo cảnh báo về việc thiết lập Deny entry), nhấn Yes để chấp nhận.
6. Đăng nhập vào user `ngolamtien`.
7. Dùng Notepad tạo tệp `file3_ngolamtien.txt` lưu vào trong thư mục `C:\doctemp\folderngolamtien`. Mở ra đọc bình thường.
8. Đăng xuất khỏi `ngolamtien`, đăng nhập vào tài khoản `ngolamtien1`.
9. Thử mở thư mục `C:\doctemp\folderngolamtien`.

> **CÂU HỎI BÀI 4 - BƯỚC 14:**  
> **Mở thư mục C:\doctemp\folderngolamtien. Điều gì sẽ xảy ra khi bạn truy cập vào thư mục và tại sao?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - **Hiện tượng:** Khi tài khoản `ngolamtien1` nhấp đúp vào thư mục `folderngolamtien`, Windows lập tức chặn lại và hiển thị hộp thoại:  
>   `"You don't currently have permission to access this folder. Click Continue to permanently get access to this folder."`  
>   Nếu người dùng nhấn Continue, hệ thống sẽ bật thông báo lỗi:  
>   `"You have been denied permission to access this folder."` và hoàn toàn không cho phép mở hay xem bất kỳ tệp nào bên trong.  
> - **Giải thích cơ chế bảo mật chuyên sâu của Windows:**  
>   1. **Nguyên tắc Deny overrides Allow:** Thuật toán duyệt DACL của Windows Security Reference Monitor (SRM) hoạt động theo thứ tự: Duyệt qua các Explicit Deny ACE trước. Ngay khi tìm thấy một ACE có cờ Deny khớp với SID của người dùng hoặc SID của nhóm mà người dùng là thành viên, hệ điều hành lập tức chấm dứt kiểm tra và đưa ra phán quyết **Từ chối (Access Denied)**, bất kể tài khoản đó có được cấp phép (Allow) ở các nhóm khác hay không.  
>   2. **Ý nghĩa của quyền List folder contents:** Quyền này điều khiển khả năng đọc cấu trúc thư mục (liệt kê danh sách tệp). Khi bị Deny quyền này, hàm API truy vấn hệ thống tệp `ZwQueryDirectoryFile` / `FindFirstFile` bị chặn hoàn toàn, khiến Windows Explorer không thể hiển thị nội dung bên trong thư mục.

---

#### PHẦN 2: AUDITING TRONG WINDOWS (KIỂM TOÁN HỆ THỐNG)

##### Bài 5: Audit Log Review (Xem xét nhật ký kiểm toán)
1. Đăng nhập tài khoản `Admin`. Mở công cụ **Event Viewer** (`eventvwr.msc`).
2. Điều hướng đến **Windows Logs**, quan sát các mục: **Security**, **Application**, và **System**.
3. Đăng xuất `Admin`, đăng nhập tài khoản Standard `ngolamtien`. Mở lại Event Viewer và nhấp vào mục **Security**.

> **CÂU HỎI BÀI 5 - CÂU 1:**  
> **Bạn có thể xem security logs khi là người dùng thường không? Người dùng thường có nên được xem security logs không? Tại sao?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - **Khả năng truy cập:** Người dùng thường (`ngolamtien`) **KHÔNG THỂ xem được Security logs**. Khi mở mục Security trong Event Viewer, hệ thống báo lỗi:  
>   `"Event Viewer cannot open the event log or custom view... Access is denied (5)"`.  
> - **Đánh giá an ninh:** Người dùng thông thường **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP xem Security logs**.  
> - **Giải thích lý do:**  
>   1. **Tính bảo mật của thông tin kiểm toán (Confidentiality):** Security Log chứa các dữ liệu an ninh cực kỳ nhạy cảm: danh sách tài khoản, địa chỉ IP mạng nội bộ, tiến trình khởi chạy, tài nguyên được truy cập, và các nỗ lực đăng nhập thất bại. Nếu người dùng thường (hoặc một tài khoản bị chiếm đoạt) đọc được nhật ký này, kẻ tấn công có thể thám sát toàn diện cấu trúc phòng thủ của hệ thống để lập kế hoạch tấn công tiếp theo.  
>   2. **Ngăn chặn việc né tránh giám sát (Evasion):** Kẻ tấn công nội bộ có thể nghiên cứu quy tắc kiểm toán để tìm cách thực hiện các hành vi phá hoại mà không để lại dấu vết.  
>   3. **Đặc quyền Windows:** Theo thiết kế bảo mật, chỉ các tài khoản sở hữu đặc quyền người dùng `SeSecurityPrivilege` (*Manage auditing and security log*) — mặc định chỉ cấp cho Administrators — mới có quyền đọc hoặc xóa Security log.

> **CÂU HỎI BÀI 5 - CÂU 2:**  
> **Sự khác biệt giữa security logs và system logs là gì?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> 
> | Tiêu chí so sánh | Security Logs (Nhật ký An ninh) | System Logs (Nhật ký Hệ thống) |
> |---|---|---|
> | **Mục đích chính** | Theo dõi, kiểm toán các sự kiện liên quan đến an ninh và tuân thủ chính sách bảo mật. | Ghi nhận trạng thái vận hành của hệ điều hành, trình điều khiển (drivers) và dịch vụ hệ thống. |
> | **Nội dung ghi nhận** | Đăng nhập/đăng xuất (Logon/Logoff), truy cập file/thư mục, thay đổi quyền người dùng, thay đổi chính sách bảo mật. | Khởi động/tắt máy, lỗi phần cứng, crash dịch vụ, cập nhật driver, sự cố mạng. |
> | **Cơ chế kích hoạt** | Mặc định bị tắt; phải được quản trị viên chủ động kích hoạt qua Local Security Policy. | Tự động kích hoạt mặc định bởi hệ điều hành Windows ngay sau khi cài đặt. |
> | **Phân quyền truy cập** | Cực kỳ nghiêm ngặt: Chỉ nhóm Administrators (có đặc quyền `SeSecurityPrivilege`) mới được xem. | Mở rộng: Mọi người dùng thông thường đều có quyền đọc để hỗ trợ chẩn đoán sự cố ứng dụng. |

---

##### Bài 6: Object Access Auditing (Kiểm toán truy cập đối tượng)
- Đăng nhập tài khoản `Admin`. Mở **Local Security Policy** (`secpol.msc`).
- Điều hướng đến: **Security Settings** > **Local Policies** > **Audit Policy**.
- Nhấp đúp vào chính sách **Audit object access** > tích chọn cả hai ô: **Success** và **Failure** > nhấn OK.

> **CÂU HỎI BÀI 6:**  
> **Tại sao các chính sách audit mặc định là disable?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Việc Microsoft để các chính sách audit mặc định ở trạng thái Disabled xuất phát từ 3 lý do kỹ thuật quan trọng:  
> 1. **Suy giảm hiệu năng hệ thống (System Performance Overhead):** Trong một hệ điều hành hiện đại, có hàng trăm ngàn thao tác truy cập đối tượng (mở tệp tin, truy vấn registry, gọi IPC) diễn ra mỗi giây. Nếu ghi log mọi thao tác, CPU và đặc biệt là hệ thống ổ đĩa I/O sẽ bị quá tải nghiêm trọng.  
> 2. **Tràn dung lượng lưu trữ tệp nhật ký (Storage Exhaustion / Log Flooding):** Kích thước tệp nhật ký sẽ tăng vọt chỉ trong vài giờ. Khi file log đạt dung lượng tối đa, hệ thống buộc phải ghi đè các bản ghi cũ (làm mất dấu vết quan trọng) hoặc ngừng hoạt động nếu được cấu hình chính sách bảo vệ nghiêm ngặt.  
> 3. **Tỷ lệ tín hiệu trên nhiễu quá thấp (Signal-to-Noise Ratio):** Lượng bản ghi khổng lồ từ các hoạt động bình thường sẽ "nhấn chìm" các sự kiện an ninh thực sự nguy hiểm, gây ra hội chứng mệt mỏi cảnh báo (Alert Fatigue) cho chuyên viên an ninh mạng. Do đó, hệ điều hành yêu cầu quản trị viên phải chủ động cấu hình audit có mục tiêu cụ thể.

---

##### Bài 7: Audit Collection (Thu thập và phân tích nhật ký kiểm toán)
1. Đăng nhập tài khoản `Admin`. Tạo thư mục: `C:\doctemp\folder2_ngolamtien`.
2. Mở Properties thư mục > thẻ Security > Advanced > chuyển sang thẻ **Auditing** > nhấn **Continue**.
3. Nhấn **Add**, chọn Principal là `ngolamtien1`.

> **CÂU HỎI BÀI 7 - BƯỚC 7:**  
> **Bạn sẽ quan tâm đến sự kiện nào? Giải thích lý do của mình cho ít nhất 3 sự kiện (với tiêu chí tránh tạo log file quá lớn).**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Để tối ưu hóa hiệu năng và chất lượng kiểm toán an ninh, 3 sự kiện quan trọng nhất cần được kích hoạt là:  
> 1. **`Create files / write data` (Ghi / Tạo tệp):**  
>    *Lý do:* Theo dõi các hành vi thêm mới tệp tin hoặc sửa đổi dữ liệu quan trọng. Cực kỳ cần thiết để phát hiện mã độc tải mã độc phụ (Dropper/Downloader), tin tặc tải webshell/backdoor lên hệ thống, hoặc mã độc tống tiền (Ransomware) bắt đầu quá trình mã hóa ghi đè tệp.  
> 2. **`Delete` / `Delete subfolders and files` (Xóa tệp / thư mục con):**  
>    *Lý do:* Giám sát hành vi xóa dữ liệu trái phép hoặc phá hoại cơ sở dữ liệu của tổ chức. Đồng thời phát hiện kỹ thuật xóa dấu vết (Anti-forensics / Defense Evasion) của kẻ xâm nhập sau khi thực hiện hành vi tấn công.  
> 3. **`Change permissions` (Write DAC - Thay đổi quyền bảo mật):**  
>    *Lý do:* Phát hiện các hành vi leo thang đặc quyền (Privilege Escalation) hoặc cố tình chiếm quyền kiểm soát đối tượng dữ liệu nhạy cảm bằng cách tự cấp quyền cho tài khoản khác.

4. Cấu hình kiểm toán: Tích chọn **List folder / read data** và **Create files / write data** ở cột **Success**. Nhấn OK.
5. Đăng xuất `Admin`, đăng nhập tài khoản `ngolamtien1`.
6. Mở Notepad, tạo tệp `file5_ngolamtien.txt` và lưu vào thư mục `C:\doctemp\folder2_ngolamtien`.
7. Đăng xuất `ngolamtien1`, đăng nhập trở lại tài khoản `Admin`.
8. Mở **Event Viewer** > chọn **Windows Logs** > **Security**.
9. Sử dụng tính năng **Find...** tìm kiếm tên tài khoản `ngolamtien1` và lọc các sự kiện File System Access.

> **CÂU HỎI BÀI 7 - BƯỚC 16:**  
> **ID sự kiện đã đăng ký cho các entries này là gì?**  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Mã định danh sự kiện (Event ID) được ghi nhận trong Windows Security Log là:  
> - **`Event ID 4663`**: *"An attempt was made to access an object"* (Ghi nhận nỗ lực truy cập đối tượng thành công, hiển thị chi tiết tên tệp `file5_ngolamtien.txt`, tiến trình `notepad.exe`, loại quyền truy cập `Accesses: WriteData/AddFile`, và tài khoản thực hiện `ngolamtien1`).  
> - Đi kèm với nó là **`Event ID 4656`**: *"A handle to an object was requested"* (Ghi nhận yêu cầu xin cấp con trỏ handle đến đối tượng tệp tin trong hệ thống tệp).

10. **Khôi phục hệ thống:** Sau khi hoàn tất thực hành, tắt chính sách Object Access Auditing trong Local Security Policy và xóa các tài khoản thử nghiệm (`ngolamtien`, `ngolamtien1`) để đảm bảo an toàn hệ thống.

---

### IV. BÀI HỌC VÀ KẾT LUẬN (CONCLUSION)
- **Kiểm soát truy cập:** Hệ thống phân quyền NTFS kết hợp giữa Explicit Permissions và Inherited Permissions, cùng nguyên tắc "Deny overrides Allow", tạo nên một bức tường phòng thủ vững chắc cho tài nguyên trên hệ điều hành Windows.
- **Kiểm toán an ninh:** Object Access Auditing kết hợp cùng Event ID 4663 và 4656 là công cụ giám sát cốt lõi trong các hệ thống SIEM (Security Information and Event Management) hiện đại, cho phép truy vết chính xác "Ai, Làm gì, Khi nào, Trên đối tượng nào".
