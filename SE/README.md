# 📚 Software Engineering — Tutorial 1 (Week 3)
## User Tasks, Domain Modeling & Software Quality Attributes

**Khoa:** Công nghệ Thông tin — Đại học Tôn Đức Thắng (TDTU)  
**Thời gian:** Tháng 02/2025  

### 👥 Nhóm sinh viên thực hiện:
- **524H0195 — Ngô Lâm Tiên**
- **524H0191 — Nguyễn Công Thành**

---

## 📁 Danh sách tệp nộp bài:

| Tên File | Định dạng | Mục đích sử dụng |
|---|---|---|
| [`524H0195_NgoLamTien_524H0191_NguyenCongThanh.pptx`](524H0195_NgoLamTien_524H0191_NguyenCongThanh.pptx) | PowerPoint (16:9) | **File chính nộp trên eLearning** (17 slides thiết kế trực quan, chuyên nghiệp). |
| [`524H0195_NgoLamTien_524H0191_NguyenCongThanh_SE_Tutorial1.pptx`](524H0195_NgoLamTien_524H0191_NguyenCongThanh_SE_Tutorial1.pptx) | PowerPoint (16:9) | Bản sao phụ có tên môn học chi tiết. |
| [`524H0195_NgoLamTien_524H0191_NguyenCongThanh_Report.md`](524H0195_NgoLamTien_524H0191_NguyenCongThanh_Report.md) | Markdown Báo cáo | Báo cáo chi tiết toàn văn lời giải, bảng biểu và sơ đồ workflow. |
| [`generate_se_presentation.py`](generate_se_presentation.py) | Python Script | Mã nguồn sinh file thuyết trình bằng `python-pptx`. |

---

## 🎯 Nội dung đã giải quyết:
- **Part 1 — Hotel Information System (HIS):**
  - Câu 1: Bảng Task & Support cho tác vụ **1.3 Check-Out**.
  - Câu 2: Xác định 6 tác vụ cốt lõi và vẽ sơ đồ quy trình hoạt động (End-to-End Workflow).
  - Câu 3: Phân tích bản chất **Yêu cầu ngầm định (Tacit Requirements)** và 4 phương pháp thẩm định.
  - Câu 5: Phân tích khiếm khuyết của Domain Model mẫu & xây dựng **Mô hình miền mở rộng** hỗ trợ **Loại phòng (Room Type)** và **Bán vượt phòng (Overbooking)**.
  - Câu 6: Phân rã tác vụ Check-In (**Khách đã đặt vs Khách vãng lai**); Thảo luận so sánh One-Task vs Two-Task.
  - Câu 7: Xử lý tình huống khẩn cấp vượt hạn mức phòng (**Overbooking Crisis / Walking Protocol**).
- **Part 2 — Essential Software Products Quality Attributes:**
  - Câu 1: Hệ thống phân loại các thuộc tính chất lượng (ISO/IEC 25010).
  - Câu 2: Các hình thức mở rộng quy mô (**Vertical, Horizontal, Structural, Geographic, Administrative Scalability**).
  - Câu 3: Khái niệm Thông lượng (**Throughput**); So sánh Thông lượng trung bình vs Thông lượng đỉnh.
  - Câu 4: Mối quan hệ đánh đổi kiến trúc giữa **An ninh (Security: AuthN & AuthZ)** và **Tính sẵn sàng (Availability)**.
  - Câu 5: Yêu cầu chất lượng cho Check-In & Check-Out; Điểm tương đồng và khác biệt; 5 kịch bản kiểm chứng được (**Verifiable Quality Scenarios**) và **Top 5 thuộc tính chất lượng cho HIS**.
