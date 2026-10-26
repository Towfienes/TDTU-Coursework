# Video Demo — shot list and narration

Weight: 10 % of the final mark. The specification requires an end-to-end walkthrough of the working
product including **one order for each customer type** and **both reports**.

Target length: 6–8 minutes. Record at 1440×900, 1080p, with a clean database seeded with the demo
data. Record the audio separately and mux it; do not narrate while clicking.

## Pre-flight checklist

- [ ] `docker compose up -d db` healthy
- [ ] `dotnet run --project src/SaigonBite.Web` serving on port 5080
- [ ] Database reset to the seed: 5 hubs, 3 brands each, ~60 items, 5 vouchers
- [ ] One hub deliberately below 30 % load (for the Quiet Kitchen discount) and one at 90 % (for the
      protection rule)
- [ ] Heavy-rain flag **off** at the start, so its effect can be shown live
- [ ] Two accounts ready: one Local Customer, one Foreign Tourist
- [ ] Screens already open in tabs; notifications silenced; zoom at 100 %
- [ ] Backup recording of each segment exists before uploading

## Shots

| # | Time | Screen | What must be visible | Narration beat |
|---|---|---|---|---|
| 1 | 0:00–0:25 | Landing page | Product name, language toggle, both entry points | What SaigonBite is; the two customer groups |
| 2 | 0:25–0:50 | Hubs list | Load percentage per hub; one hub shown as near-full | The uneven-load problem and why the platform prices it |
| 3 | 0:50–1:35 | Brand and menu browsing | Items with availability; prices in VND | Use case A: menu and availability |
| 4 | 1:35–2:20 | Cart → checkout | **Full price breakdown:** subtotal, Quiet Kitchen discount, voucher, food total, delivery fee, rush surcharge, rain surcharge, rounded total | BR10's nine steps, in order, and that rounding happens once |
| 5 | 2:20–2:50 | Payment step, **Local Customer** | MoMo, VNPay, Cash on Delivery only | BR13: the actor decides the methods |
| 6 | 2:50–3:20 | Place the order | Price snapshot stored; order in `Placed` | BR17: the price is reproducible |
| 7 | 3:20–4:00 | Kitchen staff view | Confirm → Preparing → Ready; each step appends to status history | BR15: only legal transitions, and every one is audited |
| 8 | 4:00–4:35 | Shipper view | Assign shipper, Out for Delivery, cash confirmation, Delivered | BR14: cash must be confirmed before delivery |
| 9 | 4:35–5:05 | Reject two illegal attempts | e.g. `Placed → Preparing`, and cancelling in `Preparing` | The business layer refuses even though the UI never offers it |
| 10 | 5:05–5:30 | Heavy-rain flag toggle, new order | Rain surcharge appears at 10,000; existing order unchanged | BR5 and the snapshot |
| 11 | 5:30–6:05 | **Foreign Tourist** order | Passport registration, hotel room address, Apple Pay/PayPal/COD only | BR18 and BR13 for the tourist path |
| 12 | 6:05–6:35 | Hub at 90 % load | Order refused, prompt to choose another hub | BR8 protection |
| 13 | 6:35–7:10 | **Revenue report** | Revenue by brand category and by payment method, cancelled and failed excluded | Report R1 |
| 14 | 7:10–7:45 | **Hub Utilization report** | Orders handled, average Confirmed→Ready, current load, Quiet Kitchen count | Report R2 |
| 15 | 7:45–8:10 | Dashboard | Both reports as charts; the rain flag | Tier 4 interactive dashboard |
| 16 | 8:10–8:30 | Test run | `dotnet test` summary line, 131 passed | The QA evidence, on screen |

## Narration script (Vietnamese, ~8 minutes)

Ghi âm từng đoạn rời rồi ghép, để khớp hình mà không phải nói dài.

**1 — Giới thiệu.** "SaigonBite là nền tảng đặt món từ mạng bếp trung tâm tại Thành phố Hồ Chí Minh.
Hệ thống phục vụ hai nhóm khách khác nhau về định danh và phương thức thanh toán: khách địa phương
dùng số điện thoại, khách nước ngoài dùng hộ chiếu và email. Đây là bản demo chạy thật, không phải
mockup."

**2 — Vấn đề tải bếp.** "Mỗi hub có sức chứa cố định. Vào giờ cao điểm, hub này quá tải trong khi hub
khác rảnh. Hệ thống hiển thị phần trăm tải theo thời gian thực, và dùng chính con số đó để định giá."

**3 — Menu.** "Khách chọn hub, xem thương hiệu và món. Món hết hàng bị chặn ngay ở tầng nghiệp vụ, không
chỉ ẩn nút trên giao diện."

**4 — Bảng giá.** "Đây là phần quan trọng nhất. Giá đi qua đúng chín bước theo quy tắc BR10: tạm tính,
giảm giá bếp vắng, voucher, tổng tiền món, phí giao theo quãng đường, phụ phí giờ cao điểm, phụ phí mưa,
rồi mới làm tròn một lần duy nhất ở bước cuối. Làm tròn sớm sẽ sai."

**5–6 — Thanh toán và đặt đơn.** "Khách địa phương chỉ thấy MoMo, VNPay và tiền mặt. Danh sách phương
thức do loại khách quyết định, và tầng nghiệp vụ kiểm tra lại lần nữa. Khi đặt, hệ thống lưu ảnh chụp
giá: thời điểm, tải bếp, cờ mưa — để giá luôn tái lập được."

**7–9 — Vòng đời đơn.** "Bếp xác nhận, chuẩn bị, báo sẵn sàng. Mỗi bước ghi một dòng lịch sử. Giờ tôi
thử hai chuyển trạng thái sai: nhảy từ Đã đặt sang Đang chuẩn bị, và huỷ khi đang chuẩn bị. Cả hai bị
từ chối ở tầng nghiệp vụ — đây là điểm khác biệt giữa ẩn nút và chặn thật."

**10 — Cờ mưa.** "Bật cờ mưa, đơn mới cộng 10.000. Đơn cũ không đổi vì đã chụp ảnh cờ tại lúc đặt."

**11–12 — Khách nước ngoài.** "Khách nước ngoài đăng ký bằng hộ chiếu, quốc tịch và email, giao tới
khách sạn. Phương thức chỉ còn Apple Pay, PayPal và tiền mặt. Và đây là hub đã chạm 90% tải: hệ thống
từ chối nhận đơn mới và đề nghị chọn hub khác."

**13–15 — Báo cáo.** "Báo cáo doanh thu theo nhóm thương hiệu và phương thức thanh toán, loại bỏ đơn
huỷ và đơn thất bại. Báo cáo hiệu suất hub cho biết số đơn, thời gian chuẩn bị trung bình từ xác nhận
đến sẵn sàng, tải hiện tại và số lần giảm giá bếp vắng. Dashboard vẽ cả hai bằng biểu đồ."

**16 — Kiểm thử.** "Toàn bộ logic giá và máy trạng thái được kiểm thử tự động: 131 ca, trong đó 74 ca
giá trị biên và 6 ca chuyển trạng thái sai. Tất cả đều xanh."

## Post-production

```sh
ffmpeg -i screen.mp4 -i voice.wav -c:v copy -c:a aac -b:a 192k -shortest SaigonBite_Demo.mp4
```

Export H.264, 1080p, audio 192 kbps. Upload as an unlisted YouTube link as well as the .mp4, because
the specification warns that hosting may expire.
