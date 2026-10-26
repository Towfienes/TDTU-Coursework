# BÁO CÁO THỰC HÀNH TỔNG HỢP - LAB 08
# HỌC PHẦN: NHẬP MÔN BẢO MẬT MÁY TÍNH (COMPUTER SECURITY)

---

### THÔNG TIN SINH VIÊN VÀ HỌC PHẦN
- **Trường Đại học:** Trường Đại học Tôn Đức Thắng (TDTU)
- **Khoa:** Khoa Công nghệ Thông tin
- **Bộ môn:** An toàn Thông tin & Mạng máy tính
- **Học phần:** Nhập môn Bảo mật máy tính (Computer Security)
- **Họ và tên sinh viên:** **Ngô Lâm Tiến**
- **Mã số sinh viên (MSSV):** **524H0195**
- **Lớp / Khóa:** Đại học Chính quy TDTU
- **Nội dung thực hiện:** Toàn bộ 7 bài tập thực hành chi tiết trong gói Lab 08
- **Tên tệp lưu trữ nộp bài:** `Lab_524H0195.zip`

---

## 1. MỤC LỤC TỔNG QUAN VÀ DANH MỤC CÁC BÀI THỰC HÀNH

Bộ tài liệu hoàn chỉnh bao gồm **7 bài thực hành chuyên sâu**, được phân chia khoa học thành 3 nhóm chuyên đề an ninh trọng tâm:

### NHÓM CHUYÊN ĐỀ 1: GIÁM SÁT MẠNG, PHÁT HIỆN VÀ PHÒNG THỦ XÂM NHẬP (SOC & IDS/IPS)
1. **[Lab 11.1.7]** `11.1.7_Lab_Snort_and_Firewall_Rules_524H0195`  
   *Cấu hình hệ thống phát hiện xâm nhập Snort IDS trên Router R1, mô phỏng tải mã độc Nimda qua HTTP cổng 6666, phân tích cấu trúc cảnh báo an ninh, trích xuất dữ liệu điều tra số từ tệp PCAP (tcpdump) và thiết lập quy tắc tường lửa `iptables` (chuỗi FORWARD) để ngăn chặn cuộc tấn công.*
2. **[Lab 11.2.6]** `11.2.6_Lab_Classify_Alerts_524H0195`  
   *Tra cứu chuyên sâu 10 mã định danh lỗ hổng bảo mật và chữ ký Snort (SIDs & CVEs, điểm CVSS v3.x), phân loại chính xác các cảnh báo an ninh thành True Positive (Dương tính thật), False Positive (Dương tính giả) và Cần thêm thông tin cho hai môi trường mạng đặc thù: Windows và Linux.*

### NHÓM CHUYÊN ĐỀ 2: QUẢN TRỊ HỆ THỐNG, KIỂM SOÁT TRUY CẬP VÀ NHẬT KÝ HỆ ĐIỀU HÀNH
3. **[Lab 3.1.17]** `3.1.17_Lab_Configure_Authentication_and_Authorization_in_Linux_524H0195`  
   *Quản trị người dùng và nhóm bảo mật (`groupadd`, `adduser`, `usermod`), phân tích tệp `/etc/passwd` và `/etc/shadow`, thực thi cơ chế phân quyền kiểm soát truy cập tùy ý (DAC) theo chế độ ký hiệu (Symbolic Mode - `chmod o-x`) và chế độ bát phân tuyệt đối (Absolute Octal Mode - `chmod 750`), bảo đảm nguyên tắc đặc quyền tối thiểu.*
4. **[Lab 4.2.9]** `4.2.9_Lab_Reading_Server_Logs_524H0195`  
   *Định vị và phân tích tệp nhật ký trong `/var/log`, so sánh ưu nhược điểm của các công cụ `cat`, `more`, `less`, `tail` và theo dõi thời gian thực `tail -f`, lý giải sự cần thiết của phân quyền quản trị root trên tệp log, tầm quan trọng của đồng bộ thời gian NTP trong điều tra số, và so sánh đối chiếu toàn diện giữa Syslog truyền thống và Journald (`systemd`).*

### NHÓM CHUYÊN ĐỀ 3: MẬT MÃ HỌC ỨNG DỤNG, HẠ TẦNG KHÓA CÔNG KHAI (PKI) VÀ BẺ KHÓA MẬT KHẨU
5. **[Lab 8.5.5]** `8.5.5_Lab_Generate_and_Use_a_Digital_Signature_524H0195`  
   *Sử dụng bộ công cụ OpenSSL sinh cặp khóa RSA 2048-bit, thực hiện ký số điện tử (Digital Signature) trên tài liệu hợp đồng bằng hàm băm SHA-256 kết hợp khóa bí mật, xác thực chữ ký bằng khóa công khai (`Verified OK`), mô phỏng kẻ tấn công sửa đổi nội dung và kiểm chứng khả năng phát hiện gian lận tự động (`Verification Failure`).*
6. **[Lab 8.6.8]** `8.6.8_Lab_Certificate_Authority_Stores_524H0195`  
   *Khảo sát kho chứng chỉ số gốc đáng tin cậy (Root CA Stores) trong trình duyệt Chrome/Firefox, phân tích ý nghĩa an ninh của Dấu vân tay chứng chỉ (Certificate Fingerprints / Thumbprints SHA-1 vs SHA-256), dùng OpenSSL tính toán và đối chiếu vân tay, phân tích các rủi ro thỏa hiệp CA và kiến trúc vận hành của HTTPS Deep Packet Inspection Proxy.*
7. **[Lab Password Recovery]** `Lab_Recover_Passwords_std_524H0195`  
   *Khảo sát cấu trúc băm mật khẩu và Salt trong `/etc/shadow`, sử dụng công cụ `unshadow` hợp nhất dữ liệu tài khoản, vận hành công cụ John the Ripper thực hiện tấn công từ điển bẻ khóa 5 tài khoản yếu, thực hiện củng cố độ mạnh mật khẩu (Password Hardening) kháng cự thành công bẻ khóa ngoại tuyến, và đề xuất giải pháp phòng thủ đa tầng (PAM, Argon2id, MFA).*

---

## 2. MA TRẬN TỔNG HỢP KẾT QUẢ VÀ CÔNG CỤ THỰC HIỆN

| STT | Mã bài Lab | Tên bài thực hành | Công cụ & Môi trường | Kết quả đạt được | Trạng thái giải quyết |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | **Lab 11.1.7** | Snort and Firewall Rules | Mininet, Snort IDS, iptables, tcpdump, wget | Bắt gói mã độc Nimda, phân tích cảnh báo Snort, thiết lập iptables FORWARD drop cổng 6666 thành công. | **Hoàn thành 100% (12/12 câu hỏi)** |
| **2** | **Lab 11.2.6** | Classify Alerts | NVD, MITRE CVE, Snort SIDs, CVSS v3.x | Tra cứu 10 CVE/SID, chấm điểm CVSS, phân loại chính xác 20 trường hợp Windows và Linux. | **Hoàn thành 100% (30/30 câu hỏi)** |
| **3** | **Lab 3.1.17** | Configure Auth & Authz in Linux | Linux CLI, groupadd, adduser, usermod, chmod | Tạo nhóm HR, tạo tài khoản jenny & joe, áp dụng chmod o-x và 750, cô lập thư mục thành công. | **Hoàn thành 100% (Thực nghiệm & Phân tích DAC)** |
| **4** | **Lab 4.2.9** | Reading Server Logs | Linux CLI, cat, more, less, tail, journald, NTP | Phân tích ưu nhược điểm các công cụ xem log, vai trò NTP, bảo vệ /var/log, so sánh Syslog vs Journald. | **Hoàn thành 100% (6/6 câu hỏi)** |
| **5** | **Lab 8.5.5** | Generate & Use Digital Signature | OpenSSL, RSA 2048, SHA-256, gedit | Sinh khóa RSA, ký số văn bản contract.txt, kiểm tra hợp lệ Verified OK, phát hiện can thiệp Verification Failure. | **Hoàn thành 100% (Thực nghiệm & Mô hình toán học)** |
| **6** | **Lab 8.6.8** | Certificate Authority Stores | Web Browsers, OpenSSL x509, PKI Stores | Khảo sát Root CA Stores, tính fingerprint SHA-256, phân tích HTTPS Proxy MITM inspection. | **Hoàn thành 100% (8/8 câu hỏi)** |
| **7** | **Lab Passwords**| Recover Passwords | John the Ripper, unshadow, /etc/shadow | Bẻ khóa 5 mật khẩu yếu, củng cố mật khẩu Eric với độ hỗn loạn entropy cao, chặn đứng tấn công từ điển. | **Hoàn thành 100% (Thực nghiệm & Khuyến nghị PAM/MFA)** |

---

## 3. CẤU TRÚC GÓI NỘP BÀI (SUBMISSION MANIFEST)

Gói nộp bài hoàn chỉnh được lưu trữ tại tệp nén: **`/home/towfienes/TDTU/BMMT/Lab_524H0195.zip`**, bao gồm:
```text
Lab_524H0195/
├── 00_BAO_CAO_TONG_HOP_LAB08_524H0195.html                 (Báo cáo tổng hợp giao diện web đẹp mắt)
├── 00_BAO_CAO_TONG_HOP_LAB08_524H0195.md                   (Báo cáo tổng hợp định dạng Markdown chuẩn)
│
├── DOCX_REPORTS/ (Các tệp Word gốc đã điền đầy đủ câu trả lời và chèn khung sinh viên TDTU)
│   ├── 11.1.7 Lab - Snort and Firewall Rules.docx
│   ├── 11.2.6 Lab - Classify Alerts.docx
│   ├── 3.1.17 Lab - Configure Authentication and Authorization in Linux.docx
│   ├── 4.2.9 Lab - Reading Server Logs.docx
│   ├── 8.5.5 Lab - Generate and Use a Digital Signature.docx
│   ├── 8.6.8 Lab - Certificate Authority Stores.docx
│   └── Lab - Recover Passwords - std.docx
│
├── MARKDOWN_REPORTS/ (Báo cáo thực hành kỹ thuật chi tiết định dạng Markdown)
│   ├── Lab_01_11.1.7_Snort_and_Firewall_Rules.md
│   ├── Lab_02_11.2.6_Classify_Alerts.md
│   ├── Lab_03_3.1.17_Configure_Authentication_and_Authorization_in_Linux.md
│   ├── Lab_04_4.2.9_Reading_Server_Logs.md
│   ├── Lab_05_8.5.5_Generate_and_Use_a_Digital_Signature.md
│   ├── Lab_06_8.6.8_Certificate_Authority_Stores.md
│   └── Lab_07_Recover_Passwords.md
│
└── HTML_REPORTS/ (Báo cáo trình bày giao diện HTML responsive theo phong cách TDTU tiêu chuẩn)
    ├── Lab_01_11.1.7_Snort_and_Firewall_Rules.html
    ├── Lab_02_11.2.6_Classify_Alerts.html
    ├── Lab_03_3.1.17_Configure_Authentication_and_Authorization_in_Linux.html
    ├── Lab_04_4.2.9_Reading_Server_Logs.html
    ├── Lab_05_8.5.5_Generate_and_Use_a_Digital_Signature.html
    ├── Lab_06_8.6.8_Certificate_Authority_Stores.html
    └── Lab_07_Recover_Passwords.html
```

---

## 4. KẾT LUẬN CHUNG VÀ CAM ĐOAN HỌC THUẬT
- Toàn bộ 7 bài lab đã được nghiên cứu, giải quyết và phân tích với tinh thần học thuật nghiêm túc, bám sát tài liệu chuẩn Cisco CyberOps và các tiêu chuẩn an toàn máy tính hiện đại của Trường Đại học Tôn Đức Thắng (TDTU).
- Dữ liệu câu trả lời phản ánh chính xác bản chất kỹ thuật, lệnh thực thi thực tế, phân tích nguyên nhân - hậu quả và đề xuất giải pháp phòng thủ chuyên sâu.
- Sinh viên **Ngô Lâm Tiến - MSSV: 524H0195** xin cam đoan các nội dung trong báo cáo được hoàn thành đầy đủ, trung thực và sẵn sàng bảo vệ trong các buổi vấn đáp chuyên đề.
