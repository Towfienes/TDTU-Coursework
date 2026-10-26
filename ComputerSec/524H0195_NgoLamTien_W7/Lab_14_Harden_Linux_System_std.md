# BÁO CÁO THỰC HÀNH CHI TIẾT
## Lab: Harden a Linux System (Standard Edition)

**Học phần:** An toàn Máy tính / Làm Cứng Hệ Thống (System Hardening)  
**Sinh viên thực hiện:** Ngô Lâm Tiến  
**Mã số sinh viên (MSSV):** 524H0195  
**Lớp / Khóa:** Đại học Tôn Đức Thắng (TDTU)  
**Thời gian thực hiện:** Học kỳ thực hành - Tuần 7  

---

### I. MỤC TIÊU BÀI LAB (OBJECTIVES)
1. Sử dụng công cụ kiểm toán an ninh nguồn mở chuyên nghiệp **Lynis** để quét và đánh giá toàn diện mức độ an toàn của hệ thống Linux.
2. Phân tích báo cáo kiểm toán: định danh các điểm yếu cấu hình, phân loại các cảnh báo (**Warnings**) và đề xuất khắc phục (**Suggestions**).
3. Triển khai giải pháp kỹ thuật cụ thể để khắc phục cảnh báo và làm cứng hệ thống (**System Hardening**).
4. Thực hiện tái kiểm toán để xác minh hiệu quả của giải pháp và nâng cao chỉ số an ninh **Hardening Index**.

---

### II. YÊU CẦU HỆ THỐNG VÀ CÔNG CỤ (REQUIRED RESOURCES)
- Máy ảo CSE-LABVM (Ubuntu Linux trong VirtualBox).
- Tài khoản: `cisco` (mật khẩu: `password`).
- Công cụ kiểm toán an ninh: `lynis` (phiên bản 3.0.6 từ CISOfy).

---

### III. NỘI DUNG VÀ BÁO CÁO KẾT QUẢ TỪNG BƯỚC

#### PHẦN 1 & 2: XÁC MINH VÀ CẬP NHẬT LYNIS (INSTALL & EXAMINE LYNIS)
- Kiểm tra phiên bản cài đặt qua policy: `sudo apt-cache policy lynis`.
- Kiểm tra trạng thái cơ sở dữ liệu luật kiểm toán:
```bash
cisco@labvm:~$ sudo lynis update info
== Lynis ==
  Version       : 3.0.6
  Status        : Up-to-date
  Release date  : 2021-07-22
  Project page  : https://cisofy.com/lynis/
```

#### PHẦN 3: THỰC THI QUÉT HỆ THỐNG BẰNG LYNIS (RUN LYNIS TOOL)
- Chạy kiểm toán toàn diện hệ thống với định danh auditor:
```bash
cisco@labvm:~$ sudo lynis --auditor cisco
```
- Công cụ tự động quét qua hơn 300 hạng mục kiểm tra an ninh: Boot loader, Kernel hardening, Memory processes, Users & Authentication, Shells, File systems, USB storage, Name services, Ports & Packages, Networking, Firewall, SSH, Logging và Banners.

#### PHẦN 4: ĐÁNH GIÁ KẾT QUẢ VÀ KHẮC PHỤC LỖ HỔNG (REVIEW RESULTS & ADDRESS WARNINGS)

- Trích đoạn phần kết quả tổng kết (Lynis 3.0.6 Results):
```text
================================================================================
-[ Lynis 3.0.6 Results ]Warnings (2):
---------------------------
  ! Found one or more vulnerable packages. [PKGS-7392]
      https://cisofy.com/lynis/controls/PKGS-7392/
  ! iptables module(s) loaded, but no rules active [FIRE-4512]
      https://cisofy.com/lynis/controls/FIRE-4512/

Suggestions (49):
---------------------------
  * Set a password on GRUB boot loader to prevent altering boot configuration [BOOT-5122]
  * Add a legal banner to /etc/issue, to warn unauthorized users [BANN-7126]
...
```

> **CÂU HỎI BƯỚC 4.a - CÂU 1:**  
> **How many Warnings did you receive?**  
> *(Bạn đã nhận được bao nhiêu Cảnh báo - Warnings?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Hệ thống ghi nhận **`02 Cảnh báo (Warnings)`**:  
> 1. `[PKGS-7392]`: Phát hiện một hoặc nhiều gói phần mềm trên hệ thống tồn tại lỗ hổng bảo mật đã được công bố.  
> 2. `[FIRE-4512]`: Các module hạt nhân của iptables đã được nạp vào kernel nhưng chưa có bất kỳ quy tắc tường lửa (rules) nào được kích hoạt bảo vệ.

> **CÂU HỎI BƯỚC 4.a - CÂU 2:**  
> **How many Suggestions did you receive?**  
> *(Bạn đã nhận được bao nhiêu Đề xuất cải thiện - Suggestions?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Hệ thống ghi nhận **`49 Đề xuất (Suggestions)`** nhằm nâng cao độ an toàn của hệ điều hành.

> **CÂU HỎI BƯỚC 4.b - CÂU 1:**  
> **Which warning are you addressing?**  
> *(Bạn lựa chọn giải quyết cảnh báo nào?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Lựa chọn giải quyết cảnh báo: **`[FIRE-4512] - iptables module(s) loaded, but no rules active`**  
> *(Tường lửa iptables chưa kích hoạt quy tắc bảo vệ)*.

> **CÂU HỎI BƯỚC 4.b - CÂU 2:**  
> **What is your solution?**  
> *(Giải pháp khắc phục kỹ thuật của bạn là gì?)*  
>  
> **TRẢ LỜI CHI TIẾT:**  
> Để khắc phục cảnh báo `[FIRE-4512]`, ta triển khai bộ quy tắc tường lửa cơ bản và lưu trữ cố định vào hệ thống:  
> 
> **Cách 1: Sử dụng công cụ UFW (Uncomplicated Firewall - Khuyến nghị cho Ubuntu):**  
> ```bash
> sudo ufw default deny incoming       # Chặn toàn bộ kết nối đi vào mặc định
> sudo ufw default allow outgoing      # Cho phép kết nối đi ra ngoài
> sudo ufw allow 22/tcp                # Mở cổng 22 cho SSH quản trị
> sudo ufw enable                      # Kích hoạt tường lửa
> sudo ufw status verbose              # Kiểm tra trạng thái
> ```
> 
> **Cách 2: Cấu hình trực tiếp bằng IPTables thuần:**  
> ```bash
> # 1. Cho phép các kết nối đã thiết lập và kết nối liên quan
> sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
> # 2. Cho phép giao tiếp nội bộ qua loopback
> sudo iptables -A INPUT -i lo -j ACCEPT
> # 3. Cho phép SSH cổng 22
> sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
> # 4. Thiết lập chính sách mặc định: DROP toàn bộ gói tin lạ đi vào
> sudo iptables -P INPUT DROP
> # 5. Cài đặt iptables-persistent để lưu cấu hình sau khi reboot
> sudo apt install iptables-persistent -y
> sudo netfilter-persistent save
> ```

##### Bước 4.c: Xác minh kết quả tái kiểm toán
- Chạy lại lệnh kiểm toán: `sudo lynis --auditor cisco`.
- **Kết quả:** Cảnh báo `[FIRE-4512]` đã hoàn toàn biến mất khỏi danh sách Warnings. Mục kiểm tra Firewall chuyển sang trạng thái:  
  `[+] Security configurations: Active firewall [ FOUND ]`.  
- Chỉ số **Hardening Index** của hệ thống tăng từ `62` lên `68`. Hệ thống đã được tăng cường phòng thủ vững chắc.
