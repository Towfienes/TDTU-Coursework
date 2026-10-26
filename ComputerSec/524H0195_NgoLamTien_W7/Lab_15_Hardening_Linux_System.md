# BÁO CÁO THỰC HÀNH CHI TIẾT
## Lab: Hardening a Linux System (Ubuntu Edition)

**Học phần:** An toàn Máy tính / Tối ưu và Làm Cứng Hệ Điều Hành  
**Sinh viên thực hiện:** Ngô Lâm Tiến  
**Mã số sinh viên (MSSV):** 524H0195  
**Lớp / Khóa:** Đại học Tôn Đức Thắng (TDTU)  
**Thời gian thực hiện:** Học kỳ thực hành - Tuần 7  

---

### I. MỤC TIÊU BÀI LAB (OBJECTIVES)
1. Thực hành sử dụng công cụ kiểm toán hệ thống an ninh **Lynis** trên hệ điều hành Ubuntu Linux.
2. Phát hiện các điểm yếu trong cấu hình mặc định (Default Weak Configurations).
3. Nghiên cứu và lựa chọn một đề xuất cải thiện an ninh (**Suggestion**) trong báo cáo Lynis để triển khai giải pháp khắc phục thực tế.

---

### II. YÊU CẦU HỆ THỐNG VÀ CÔNG CỤ (REQUIRED RESOURCES)
- Máy tính hoặc máy ảo Ubuntu 16.04/20.04 Desktop LTS trong VirtualBox/VMware.
- Tài khoản: `cisco` (mật khẩu `password`) hoặc `sv` (mật khẩu `123`).
- Bộ công cụ Lynis trong thư mục `Downloads/lynis/`.

---

### III. NỘI DUNG VÀ BÁO CÁO KẾT QUẢ TỪNG BƯỚC

#### BƯỚC 1: KHỞI CHẠY TERMINAL TRÊN UBUNTU
- Đăng nhập hệ thống Ubuntu với tài khoản được cung cấp. Mở ứng dụng Terminal.

#### BƯỚC 2: CẬP NHẬT CÔNG CỤ LYNIS
- Điều hướng vào thư mục cài đặt Lynis:
```bash
cisco@ubuntu:~$ cd Downloads/lynis/
cisco@ubuntu:~/Downloads/lynis$ sudo ./lynis update info
```
- Xác nhận phần mềm và các tệp định nghĩa kiểm tra đang ở phiên bản mới nhất.

#### BƯỚC 3: THỰC THI KIỂM TOÁN HỆ THỐNG (RUN THE TOOL)
- Chạy công cụ kiểm toán với tài khoản auditor:
```bash
cisco@ubuntu:~/Downloads/lynis$ sudo ./lynis --auditor cisco
```
- Nhấn Enter qua các giai đoạn quét để theo dõi kết quả phát hiện cấu hình yếu.
- Ghi nhận vị trí lưu trữ tệp nhật ký kiểm toán chi tiết:  
  `Report file: /var/log/lynis-report.dat`  
  `Log file: /var/log/lynis.log`

#### BƯỚC 4: ĐÁNH GIÁ KẾT QUẢ VÀ TRIỂN KHAI GIẢI PHÁP (REVIEW RESULTS)

> **CÂU HỎI BƯỚC 4.a:**  
> **How many Warnings did you receive? How many Suggestions did you receive?**  
> *(Bạn đã nhận được bao nhiêu Cảnh báo và bao nhiêu Đề xuất?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> - Số lượng Cảnh báo (Warnings): **`02 Warnings`** (`[PKGS-7392]` và `[FIRE-4512]`).  
> - Số lượng Đề xuất (Suggestions): **`49 Suggestions`**.

> **CÂU HỎI BƯỚC 4.b - CÂU 1:**  
> **Which suggestion are you addressing?**  
> *(Bạn lựa chọn giải quyết đề xuất cải thiện nào?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Lựa chọn giải quyết đề xuất: **`[BANN-7126] - Add a legal banner to /etc/issue and /etc/issue.net to warn unauthorized users`**  
> *(Thêm thông báo cảnh báo pháp lý vào tệp banner đăng nhập để cảnh báo người dùng không được ủy quyền)*.

> **CÂU HỎI BƯỚC 4.b - CÂU 2:**  
> **What is your suggested solution?**  
> *(Giải pháp khắc phục đề xuất của bạn là gì?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> **1. Bối cảnh an ninh:** Trong quản trị hệ thống và pháp lý an ninh mạng, việc không có biểu ngữ cảnh báo pháp lý (Legal Warning Banner) có thể khiến tổ chức gặp khó khăn khi truy cứu trách nhiệm kẻ xâm nhập trái phép trước pháp luật, vì kẻ tấn công có thể biện minh rằng máy chủ mở tự do.  
> 
> **2. Các bước triển khai kỹ thuật cụ thể:**  
> - **Bước 1:** Soạn thảo nội dung cảnh báo pháp lý và ghi vào tệp `/etc/issue.net` (dành cho kết nối mạng Telnet/SSH) và `/etc/issue` (dành cho console cục bộ):  
>   ```bash
>   sudo bash -c 'cat << EOF > /etc/issue.net
>   ************************************************************************
>   *                             WARNING!                                 *
>   * You must have explicit authorized permission to access this system.  *
>   * All connections and activities are monitored and recorded.           *
>   * Unauthorized access will be prosecuted to the full extent of the law.*
>   ************************************************************************
>   EOF'
>   sudo cp /etc/issue.net /etc/issue
>   ```
> - **Bước 2:** Cấu hình daemon SSH kích hoạt hiển thị banner trước khi xác thực:  
>   Mở tệp cấu hình SSH bằng nano: `sudo nano /etc/ssh/sshd_config`  
>   Tìm và sửa chỉ thị:  
>   `Banner /etc/issue.net` (bỏ dấu `#` chú thích ở đầu dòng).  
> - **Bước 3:** Khởi động lại dịch vụ SSH để áp dụng cấu hình:  
>   `sudo systemctl restart ssh` (hoặc `sudo service ssh restart`).  
> 
> **3. Xác minh kết quả:**  
> Khi người dùng hoặc kẻ tấn công kết nối từ xa vào máy chủ qua lệnh `ssh cisco@<IP>`, toàn bộ thông điệp cảnh báo pháp lý sẽ xuất hiện rõ ràng trên màn hình trước khi hiển thị yêu cầu nhập mật khẩu. Chạy lại Lynis, mục kiểm tra `[BANN-7126]` chuyển sang trạng thái tuân thủ an toàn (**PASSED**).
