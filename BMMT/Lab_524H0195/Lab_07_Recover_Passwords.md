# BÁO CÁO THỰC HÀNH CHI TIẾT - LAB RECOVER PASSWORDS
# HỌC PHẦN: NHẬP MÔN BẢO MẬT MÁY TÍNH (COMPUTER SECURITY)

---

### THÔNG TIN SINH VIÊN VÀ HỌC PHẦN
- **Trường Đại học:** Trường Đại học Tôn Đức Thắng (TDTU)
- **Khoa:** Khoa Công nghệ Thông tin
- **Học phần:** Nhập môn Bảo mật máy tính
- **Mã lớp / Hệ:** Đại học Chính quy TDTU
- **Họ và tên sinh viên:** **Ngô Lâm Tiến**
- **Mã số sinh viên (MSSV):** **524H0195**
- **Tên bài thực hành:** **Lab: Recover Passwords** (John the Ripper - Cisco CyberOps / Cybersecurity Essentials)

---

## 1. MỤC TIÊU BÀI THỰC HÀNH
1. Khảo sát cấu trúc tệp chứa thông tin tài khoản người dùng `/etc/passwd` và tệp chứa chuỗi băm mật khẩu được bảo vệ `/etc/shadow` trên Linux.
2. Sử dụng công cụ **`unshadow`** để hợp nhất hai tệp tin thành định dạng dữ liệu chuẩn phục vụ kiểm thử xâm nhập.
3. Sử dụng công cụ khôi phục mật khẩu mã nguồn mở hàng đầu **John the Ripper** để thực hiện kỹ thuật tấn công từ điển (**Dictionary Attack**) giải mã mật khẩu các tài khoản: `cisco`, `Alice`, `Bob`, `Eve`, `Eric`.
4. Đánh giá tính dễ bị tổn thương của các mật khẩu yếu, ngắn, hoặc chứa từ ngữ thông dụng.
5. Thực hành kỹ thuật **Củng cố độ mạnh mật khẩu (Password Hardening)** và kiểm chứng khả năng kháng cự của mật khẩu phức tạp trước các cuộc tấn công bẻ khóa ngoại tuyến (Offline Cracking).

---

## 2. NỀN TẢNG LÝ THUYẾT VÀ CƠ CHẾ BẢO VỆ MẬT KHẨU LINUX

### Cấu trúc tệp `/etc/shadow`
Mỗi dòng trong `/etc/shadow` có định dạng chuẩn:
`username:password_hash:last_changed:min_days:max_days:warn_days:inactive_days:expire_days:reserved`

Chuỗi `password_hash` có cấu trúc:
`$id$salt$encrypted_hash`
- `$id$`: Định danh thuật toán băm mật mã học:
  - `$1$`: MD5 (đã lỗi thời)
  - `$2a$`, `$2y$`: Blowfish / bcrypt
  - `$5$`: SHA-256
  - `$6$`: SHA-512 (tiêu chuẩn phổ biến trên Linux hiện nay)
  - `$y$`: yescrypt (tiêu chuẩn mới kháng GPU/ASIC)
- `salt`: Chuỗi ký tự ngẫu nhiên được thêm vào mật khẩu trước khi băm nhằm triệt tiêu hoàn toàn khả năng sử dụng Bảng cầu vồng (Rainbow Table).

### Cơ chế bẻ khóa mật khẩu ngoại tuyến (Offline Attack)
Thay vì thử đăng nhập trực tiếp trên hệ thống (dễ bị khóa tài khoản hoặc giới hạn tốc độ), kẻ tấn công sau khi trích xuất được tệp `/etc/shadow` sẽ mang về máy tính cá nhân hoặc dàn máy đào để bẻ khóa ngoại tuyến:
- Công cụ băm từng từ trong từ điển (Wordlist) kết hợp với Salt của nạn nhân.
- Nếu chuỗi băm tính toán trùng khớp với chuỗi băm trong shadow, mật khẩu gốc được tìm thấy.

---

## 3. TIẾN TRÌNH THỰC HIỆN VÀ PHÂN TÍCH KẾT QUẢ

### PHẦN 1: HỢP NHẤT DỮ LIỆU TÀI KHOẢN VỚI LỆNH `UNSHADOW`
1. Di chuyển vào thư mục cài đặt công cụ John the Ripper:
   ```bash
   cisco@labvm:~$ cd Downloads/john/run
   cisco@labvm:~/Downloads/john/run$
   ```
2. Thực thi lệnh `unshadow` kết hợp `/etc/passwd` và `/etc/shadow` thành tệp `mypasswd`:
   ```bash
   cisco@labvm:~/Downloads/john/run$ sudo ./unshadow /etc/passwd /etc/shadow > mypasswd
   [sudo] password for cisco: password
   ```
   *Mục đích của unshadow:* Trích xuất tên người dùng, UID, GID từ `/etc/passwd` và gắn kèm chuỗi băm tương ứng từ `/etc/shadow` thành một tệp duy nhất để John the Ripper có đầy đủ ngữ cảnh nhận diện.

---

### PHẦN 2: THỰC THI BẺ KHÓA VỚI JOHN THE RIPPER
1. Kiểm tra trạng thái mật khẩu ban đầu:
   ```bash
   cisco@labvm:~/Downloads/john/run$ ./john --show mypasswd
   Created directory: /home/cisco/.john
   0 password hashes cracked, 5 left
   ```
   *Nhận xét:* Ban đầu hệ thống ghi nhận có 5 chuỗi băm cần được xử lý, chưa có chuỗi băm nào được bẻ khóa.

2. Khởi chạy John the Ripper kết hợp từ điển `password.lst` và các quy tắc biến đổi chuỗi (`--rules`):
   ```bash
   cisco@labvm:~/Downloads/john/run$ ./john --wordlist=password.lst --rules mypasswd --format=crypt
   Loaded 5 password hashes with 5 different salts (crypt, generic crypt(3) [?/64])
   Press 'q' or Ctrl-C to abort, almost any other key for status
   password1        (Eric)
   password         (cisco)
   password         (Eve)
   12345            (Bob)
   123456           (Alice)
   5g 0:00:00:00 100% 6.097g/s 117.0p/s 585.3c/s 585.3C/s
   Session completed
   ```

3. Xem lại toàn bộ mật khẩu đã được giải mã thành công:
   ```bash
   cisco@labvm:~/Downloads/john/run$ ./john --show mypasswd
   cisco:password:900:900:Cybersecurity Analyst,,,:/home/cisco:/bin/bash
   Alice:123456:1000:1000::/home/Alice:/bin/bash
   Bob:12345:1001:1001::/home/Bob:/bin/bash
   Eve:password:1002:1002::/home/Eve:/bin/bash
   Eric:password1:1003:1003::/home/Eric:/bin/bash
   5 password hashes cracked, 0 left
   ```

#### Bảng tổng hợp kết quả giải mã 5 tài khoản:
| Tài khoản (Username) | Mật khẩu gốc (Cleartext Password) | Đánh giá mức độ an toàn | Điểm yếu chí tử |
| :--- | :--- | :---: | :--- |
| **cisco** | `password` | Cực kỳ yếu | Sử dụng từ điển thông dụng nhất thế giới. |
| **Alice** | `123456` | Cực kỳ yếu | Dãy số thứ tự đơn giản, nằm ở top 1 danh sách rò rỉ. |
| **Bob** | `12345` | Cực kỳ yếu | Dãy số quá ngắn (5 ký tự). |
| **Eve** | `password` | Cực kỳ yếu | Trùng mật khẩu với tài khoản quản trị `cisco`. |
| **Eric** | `password1` | Cực kỳ yếu | Từ điển thông dụng kèm theo số `1` ở đuôi. |

---

### PHẦN 3: CỦNG CỐ ĐỘ MẠNH MẬT KHẨU (PASSWORD HARDENING)
1. Sử dụng tài khoản quản trị để đổi mật khẩu cho tài khoản `Eric` sang một mật khẩu phức tạp có độ dài và độ hỗn loạn cao (ví dụ: `Tr0ng$ecUr1ty!2026#TDTU`):
   ```bash
   cisco@labvm:~/Downloads/john/run$ sudo passwd Eric
   [sudo] password for cisco: password
   New password: <your_new_strong_password>
   Retype new password: <your_new_strong_password>
   passwd: password updated successfully
   ```

2. Cập nhật lại tệp `mypasswd` bằng lệnh `unshadow`:
   ```bash
   cisco@labvm:~/Downloads/john/run$ sudo ./unshadow /etc/passwd /etc/shadow > mypasswd
   ```

3. Chạy lại John the Ripper kiểm thử khả năng bẻ khóa:
   ```bash
   cisco@labvm:~/Downloads/john/run$ ./john --wordlist=password.lst --rules mypasswd --format=crypt
   Loaded 5 password hashes with 5 different salts (crypt, generic crypt(3) [?/64])
   Remaining 1 password hash
   Press 'q' or Ctrl-C to abort, almost any other key for status
   0g 0:00:00:17 7% 0g/s 599.6p/s 599.6c/s 599.6C/s reddog1..mark1
   Session aborted
   ```
   *Hiện tượng:* John the Ripper đã bẻ khóa xong 4 tài khoản cũ trong cơ sở dữ liệu cache (`.john.pot`), nhưng tài khoản Eric còn lại duy nhất (`Remaining 1 password hash`) liên tục được quét qua hàng nghìn biến thể mà không thể tìm ra mật khẩu.

4. Kiểm tra lại trạng thái:
   ```bash
   cisco@labvm:~/Downloads/john/run$ ./john --show mypasswd
   cisco:password:900:900:Cybersecurity Analyst,,,:/home/cisco:/bin/bash
   Alice:123456:1000:1000::/home/Alice:/bin/bash
   Bob:12345:1001:1001::/home/Bob:/bin/bash
   Eve:password:1002:1002::/home/Eve:/bin/bash
   4 password hashes cracked, 1 left
   ```
   *Kết luận:* Mật khẩu mới của Eric đã hoàn toàn vô hiệu hóa kỹ thuật tấn công từ điển của John the Ripper.

---

## 4. CHIẾN LƯỢC BẢO VỆ MẬT KHẨU TOÀN DIỆN CHO TỔ CHỨC
1. **Thiết lập chính sách độ phức tạp mật khẩu bằng Linux PAM:**
   - Cấu hình mô-đun `pam_pwquality` (hoặc `pam_cracklib`) trong `/etc/security/pwquality.conf`:
     - Độ dài tối thiểu ít nhất 12 - 16 ký tự (`minlen = 14`).
     - Yêu cầu ít nhất 1 chữ hoa (`ucredit = -1`), 1 chữ thường (`lcredit = -1`), 1 chữ số (`dcredit = -1`) và 1 ký tự đặc biệt (`ocredit = -1`).
     - Ngăn chặn việc tái sử dụng mật khẩu cũ thông qua `pam_pwhistory` (`remember = 5`).
2. **Sử dụng các thuật toán băm hiện đại (Slow Hashing Functions):**
   - Thay thế các thuật toán băm nhanh dễ bị giải mã bằng GPU (như MD5, SHA-1, SHA-256 thuần) bằng các giải thuật điều chỉnh được hệ số tiêu tốn thời gian và bộ nhớ như **Argon2id**, **bcrypt**, hoặc **yescrypt**.
3. **Triển khai Xác thực Đa Yếu tố (MFA / 2FA):**
   - Kể cả khi kẻ tấn công đánh cắp được chuỗi băm và bẻ khóa thành công mật khẩu tĩnh, việc bắt buộc phải có yếu tố thứ hai (TOTP, Hardware Token FIDO2/YubiKey) sẽ ngăn chặn hoàn toàn việc đăng nhập trái phép vào máy chủ doanh nghiệp.
