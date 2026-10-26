# SaigonBite — Presentation 1: Vietnamese speaking notes

English deck: `Part1_Pitch.pdf` (5 slides). Planned duration: **6:15**; permitted range: **5–7 minutes**. This is a timing budget, not a claim that rehearsal has been completed.

| Slide | Speaker | Planned slot | Purpose |
|---|---|---|---|
| 1 | Ngô Lâm Tiến | 0:00–0:40 | Product, team and proposed tier |
| 2 | Nguyễn Công Thành | 0:40–1:55 | Client needs and load thresholds |
| 3 | Ngô Lâm Tiến | 1:55–3:15 | Solution and quality attributes |
| 4 | Tiến → Thành → Phú | 3:15–4:50 | Each member claims a complete CRUD use case |
| 5 | Nguyễn Trọng Phú | 4:50–6:15 | Acceptance plan, tier risks and assumptions |

## Slide 1 — Ngô Lâm Tiến — 0:40

Kính chào thầy và các bạn. Nhóm em trình bày Part 1 của SaigonBite, nền tảng đặt món cho hệ thống bếp trung tâm tại Thành phố Hồ Chí Minh. Nhóm gồm em là Ngô Lâm Tiến, MSSV 524H0195; Nguyễn Công Thành, 524H0191; và Nguyễn Trọng Phú, 524H0179.

Nhóm đề xuất Tier 4, gồm nền tảng MVC, tích hợp sandbox thanh toán, dashboard quản trị và kiểm thử tự động. Đây là mục tiêu cần được chứng minh ở các phần sau và được thầy xác nhận. Hôm nay nhóm trình bày bài toán, giải pháp dự kiến, phân công và kế hoạch nghiệm thu yêu cầu.

## Slide 2 — Nguyễn Công Thành — 1:15

Khách hàng của SaigonBite có hai nhóm. Khách địa phương đăng ký bằng số điện thoại Việt Nam và dùng MoMo, VNPay hoặc tiền mặt. Khách du lịch đăng ký bằng hộ chiếu, quốc tịch và email; họ dùng Apple Pay, PayPal hoặc tiền mặt. Hai nhóm cùng dùng một nền tảng và một schema, nhưng khác điều kiện đăng ký và lựa chọn thanh toán.

Vấn đề thứ hai là tải bếp không đều. Theo BR7, tải dưới 30% được giảm 10% tiền món. Từ 30% đến dưới 90% không có giảm Quiet Kitchen. Từ 90% trở lên, hệ thống từ chối đơn mới và đề nghị chọn hub khác.

Điểm cần chú ý là tải có thể là số lẻ: 29,5% vẫn được giảm, 89,5% chưa bị từ chối. Tải được tính từ số đơn Confirmed và Preparing chia cho capacity; không tính đơn mới. Những quy tắc này giúp điều tiết nhu cầu mà khách vẫn thấy rõ lý do giá thay đổi.

## Slide 3 — Ngô Lâm Tiến — 1:20

Nhóm đề xuất ba phần nghiệp vụ. Thứ nhất là tính giá: áp dụng đúng thứ tự chín bước, giữ phần lẻ ở các bước trung gian và chỉ làm tròn tổng cuối một lần. Ví dụ trong report cho thấy cắt phần lẻ sớm có thể làm tổng lệch một nghìn đồng. Việc kiểm món còn bán hay thuộc hub nào nằm ở business service, trước khi gọi hàm tính giá.

Thứ hai là Strategy cho thanh toán. Mỗi phương thức có một lớp, được chọn theo loại khách. Mục tiêu bảo trì là thêm một phương thức bằng một lớp mới và một đăng ký, không sửa các lớp thanh toán cũ.

Thứ ba là vòng đời đơn với tám trạng thái và tám chuyển tiếp hợp lệ. Tầng nghiệp vụ kiểm cả vai trò lẫn điều kiện, không chỉ ẩn nút. Các NFR còn yêu cầu tính giá dưới 1,5 giây cho 30 dòng, giao diện song ngữ responsive, phân quyền phía server và audit cho mỗi thay đổi trạng thái hoặc lần thanh toán. Đây là tiêu chí nghiệm thu dự kiến, chưa phải kết quả chạy ứng dụng trong Part 1.

## Slide 4 — Cả ba thành viên — 1:35

**Ngô Lâm Tiến — khoảng 0:35:**

Em là Ngô Lâm Tiến, phụ trách use case D — Place and Manage Orders. CRUD gồm tạo đơn, xem và theo dõi, sửa món khi Placed, và hủy khi Placed hoặc Confirmed. Hủy là thao tác nghiệp vụ thay cho xóa lịch sử. Em chịu trách nhiệm chung cho pricing engine, lựa chọn thanh toán và kiêm quản lý voucher.

**Nguyễn Công Thành — khoảng 0:30:**

Em là Nguyễn Công Thành, phụ trách use case A — Manage Menu and Brands. Em quản lý tạo, xem, sửa và xóa mềm thương hiệu lẫn món ăn, cùng trạng thái availability. Em kiêm use case E về tài khoản và báo cáo R1: doanh thu theo nhóm món và phương thức thanh toán, loại đơn Cancelled và Failed.

**Nguyễn Trọng Phú — khoảng 0:30:**

Em là Nguyễn Trọng Phú, phụ trách use case B — Manage Hubs and Capacity. CRUD gồm tạo hub, xem tải, sửa thông tin và capacity, xóa mềm hub. Em kiêm giao nhận và báo cáo R2 gồm số đơn, thời gian Confirmed đến Ready, tải hiện tại và số lần giảm Quiet Kitchen.

## Slide 5 — Nguyễn Trọng Phú — 1:25

Để nghiệm thu, nhóm lên kế hoạch ít nhất 20 ca EP/BVA bao phủ các ngưỡng số trong BR1 đến BR12 và BR14, cùng ít nhất năm ca chuyển trạng thái không hợp lệ. RTM đã có 46 FR và sáu NFR, gắn nguồn, use case, người phụ trách và phép kiểm dự kiến. Verdict hiện tại là Planned; kết quả thực thi sẽ bổ sung ở Part 3.

Tier 4 cần đủ sandbox thật, dashboard và kiểm thử workflow. Nếu chưa đủ thì phải xét lại theo rubric và stack thực tế; 9,5 chỉ là trần Tier 3 khi đáp ứng Tier 3, không phải điểm chắc chắn. Với change request, một lớp cộng một đăng ký chỉ áp dụng cho việc thêm phương thức thanh toán; thay đổi khác cần phân tích riêng.

Hai giả định còn chờ thầy góp ý: A1, Admin gán shipper đang sẵn sàng cho đơn Ready và lưu thời gian gán. A2, giao thất bại vẫn là trạng thái Failed: thanh toán online hoàn toàn bộ theo sổ cái mô phỏng, COD không thu tiền, và không ghi doanh thu. Nhóm sẽ cập nhật cả report, workbook và test nếu giả định thay đổi. Nhóm em cảm ơn thầy và các bạn.

## Rehearsal and Q&A

- Rehearse all three members with a real timer. Shorten examples first if exceeding 7:00; keep every ownership claim. Do not call this budget a measured duration.
- Sources: course Specification sections 2–4, Case Study section 4, Survival Guide Part 1; exact versions appear in report REFERENCES.
- Be ready to explain: 29.5% load; free delivery with rain/rush; why Failed differs from Cancelled; final-only rounding; the role/condition for each transition.
- If asked whether tests or sandbox passed: show actual later-phase evidence if available; Part 1 makes no such PASS claim.
- The six mandatory/defined NFRs and assumptions A1–A5 must match `config/part1.json` and the workbook. No signature or instructor approval is inferred.
