# 📦 GÓI NỘP BÀI THỰC HÀNH LAB 06 — KỸ THUẬT PHẦN MỀM (503074)
## TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG (TDTU) — KHOA CÔNG NGHỆ THÔNG TIN

- **Sinh viên thực hiện:** Ngô Lâm Tiến
- **Mã số sinh viên (MSSV):** 524H0195
- **Giảng viên hướng dẫn:** ThS. Mai Văn Mạnh
- **Tài liệu tham chiếu:** `Lab04_6Class_Sequence.pdf`
- **Tên gói nén:** `524H0195_lab06.zip`

---

## 📁 CẤU TRÚC DANH MỤC TỆP BÀN GIAO:

| Tên Tệp / Thư mục | Định dạng | Mô tả nội dung kỹ thuật |
|---|---|---|
| [`524H0195_NgoLamTien_Lab06_Report.pdf`](524H0195_NgoLamTien_Lab06_Report.pdf) | PDF (26 trang) | **Báo cáo chính thức** nộp trên Elearning. Trình bày chuẩn học thuật TDTU, tích hợp toàn bộ biểu đồ UML độ phân giải cao và bảng đặc tả chi tiết. |
| [`524H0195_NgoLamTien_Lab06_Report.html`](524H0195_NgoLamTien_Lab06_Report.html) | HTML5 | Bản báo cáo xem trực tiếp trên trình duyệt web với giao diện hiện đại, responsive và hỗ trợ in ấn (Print CSS). |
| [`524H0195_NgoLamTien_Lab06_Report.md`](524H0195_NgoLamTien_Lab06_Report.md) | Markdown | Toàn văn mã nguồn báo cáo với đầy đủ mã nguồn Mermaid UML và bảng dữ liệu. |
| [`atm_simulation.py`](atm_simulation.py) | Python 3 | Mã nguồn mô phỏng kiểm chứng máy trạng thái và quy trình xử lý dữ liệu rút tiền ATM (**Exercise 3 - Trọng tâm Lab 06**), bao gồm 4 test cases: rút tiền chuẩn, nuốt thẻ khi sai PIN 3 lần, kiểm tra bội số 50k, và timeout tự động đảo nợ/hoàn tiền (Auto-Reversal). |
| [`course_registration_simulation.py`](course_registration_simulation.py) | Python 3 | Mã nguồn mô phỏng quy trình đăng ký học phần đại học (**Exercise 2**), kiểm tra môn tiên quyết và sĩ số còn chỗ kèm danh sách chờ (Waitlist). |
| [`email_mailbox_model.py`](email_mailbox_model.py) | Python 3 | Mã nguồn mô hình hướng đối tượng Hộp thư & Thư điện tử theo chuẩn RFC 5322 (**Exercise 1.1**). |
| [`cms_model.py`](cms_model.py) | Python 3 | Mã nguồn mô hình hệ thống Quản lý Khóa học CMS (**Exercise 1.2**). |
| `images/` | Thư mục | Chứa 10 tệp hình ảnh biểu đồ UML chất lượng cao (5 PNG Retina + 5 SVG vector):<br>• `exercise1_1_mailbox_email_class.png/.svg`<br>• `exercise1_2_courseware_cms_class.png/.svg`<br>• `exercise2_course_registration_sequence.png/.svg`<br>• `exercise3_atm_cash_withdrawal_activity.png/.svg` (Sơ đồ tổng quan)<br>• `exercise3_atm_cash_withdrawal_swimlane.png/.svg` (Sơ đồ phân làn Swimlane 4 đối tượng). |

---

## 🚀 HƯỚNG DẪN THỰC THI KIỂM CHỨNG CÁC SCRIPT MÔ PHỎNG:

```bash
# 1. Chạy mô phỏng máy trạng thái rút tiền ATM (Lab 06 - Exercise 3)
python3 atm_simulation.py

# 2. Chạy mô phỏng tiến trình đăng ký học phần (Exercise 2)
python3 course_registration_simulation.py

# 3. Chạy kiểm thử mô hình lớp Mailbox & Email (Exercise 1.1)
python3 email_mailbox_model.py

# 4. Chạy kiểm thử mô hình hệ thống CMS (Exercise 1.2)
python3 cms_model.py
```
