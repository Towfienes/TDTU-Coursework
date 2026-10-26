# Midterm presentation — Hồi quy & Phân loại

Slide thuyết trình cho bài giữa kỳ môn **Introduction to Machine Learning** (TDTU), dựng từ chính
report và các artifact thực nghiệm trong `../results/`.

## Deliverables

| File | Nội dung |
|---|---|
| `midterm_presentation.pptx` | Deck chính, 14 slide, 16:9 (13.333 × 7.5 in), có speaker notes tiếng Việt cho từng slide |
| `midterm_presentation.pdf` | Bản chiếu 14 trang, khổ 960 × 540 pt (đúng 16:9), dùng khi máy trình chiếu không có PowerPoint |
| `TRANSCRIPT.md` | Lời thoại đầy đủ cho 3 người, mốc thời gian từng slide, bảng câu hỏi dự kiến |
| `figures/` | 6 hình được vẽ riêng cho slide, đọc trực tiếp từ `../results/` |
| `src/make_deck_figures.py` | Script vẽ hình + kiểm tra lại 11 con số so với `results/*.json` |
| `src/build_deck.js` | Script dựng PPTX, sinh luôn `preview.html` và `TRANSCRIPT.md` từ một nguồn duy nhất |
| `preview.html` | Bản HTML cùng hệ toạ độ với PPTX; đây là nguồn của file PDF |

## Số slide: 14 cho 10 phút

14 slide ≈ 40 giây/slide — mức thoải mái cho một bài có công thức. Cấu trúc:

| Slide | Nội dung | Người nói | Mốc |
|---|---|---|---|
| 1–2 | Bìa · nội dung ba phần | Tiến | 0:00 |
| 3–4 | Câu 1: hồi quy tuyến tính, mô hình → gradient → GD | Tiến | 0:51 |
| 5 | Câu 1: logistic, sigmoid → cross-entropy → gradient | Tiến | 2:08 |
| 6–7 | Câu 1: kết quả hai mô hình trên tập test | Tiến | 2:49 |
| 8 | Câu 2: dữ liệu credit-g, mất cân bằng lớp | Thành | 4:12 |
| 9 | Câu 2: quy trình chống rò rỉ dữ liệu | Thành | 4:51 |
| 10–11 | Câu 2: chọn mô hình bằng CV, kết quả test | Thành | 5:26 |
| 12 | Đọc kết quả: recall lớp bad | Tâm | 6:45 |
| 13 | Overfitting và biện pháp | Tâm | 7:28 |
| 14 | Kết luận, hạn chế, Q&A | Tâm | 8:12 |

Tổng lời thoại **1356 từ ≈ 8:53** khi đọc 150 từ/phút; phần còn lại của 10 phút dành cho chuyển slide và Q&A.

Nếu chỉ được **7 phút**, bỏ slide 2 (nội dung) và gộp 6–7 thành một slide chỉ giữ hình bên trái + 3 chỉ số,
hoặc bỏ slide 5 và nói logistic bằng lời ở slide 7.

## Dựng lại

```bash
# 1. Hình (đọc ../results/, tự kiểm tra 11 con số rồi mới vẽ)
python3 src/make_deck_figures.py

# 2. Deck + transcript (pptxgenjs 4.0.1)
PPTXGENJS_PATH=/path/to/node_modules/pptxgenjs node src/build_deck.js

# 3. PDF chiếu (Chromium in từ preview.html, thang 13.333 × 7.5 in)
chromium --headless=new --no-pdf-header-footer --print-to-pdf=midterm_presentation.pdf preview.html
```

`build_deck.js` đọc `q1_metrics.json`, `q2_metrics.json` và tính các khoảng cách overfitting từ đó,
nên đổi kết quả thực nghiệm rồi dựng lại là slide tự cập nhật số — không có số nào gõ tay.

## Kiểm chứng đã chạy

- `validate.py` (skill pptx): **All validations PASSED** — schema, quan hệ, content-type, bảng, hình.
- 14 slide, 14 notes, 6 hình nhúng, 1 bảng native, 5 section, logo nằm trên layout (sửa một chỗ, đổi mọi slide).
- Chỉ dùng font **Arial** trong mọi run; logo TDTU giữ nguyên byte gốc (`report/assets/tdtu-logo.png`).
- Số trang là field `slidenum` (tự cập nhật), có ở slide 2–14, không có ở bìa.
- 11 con số trên hình được tính lại từ `results/` và so với JSON xuất ra: khớp tuyệt đối.
- Đã render và xem **từng slide ở kích thước đầy đủ** (1280 × 720), không dùng contact sheet thay thế;
  sửa các lỗi chồng chữ, đường kẻ cắt qua chữ, và ký tự Arial không có (`‖`, chỉ số trên Unicode).
- PDF 14 trang, 960 × 540 pt, khớp từng pixel với preview.

## Giới hạn cần biết

- Máy này **không có PowerPoint và LibreOffice**, nên chưa mở thử bằng ứng dụng đích. PDF là bản chiếu
  dựng từ cùng hệ toạ độ (`preview.html`), không phải ảnh render của PowerPoint. Nên mở thử `.pptx`
  một lần trên máy có PowerPoint trước khi trình bày; rủi ro còn lại là font Arial và vị trí bullet.
- Bullet dùng ký tự en-dash (`–`) qua `bullet.code`; PowerPoint hiển thị đúng, nhưng nếu mở bằng
  Google Slides thì kiểm tra lại thụt lề.
- Thứ tự slide 6–7 và 10–11 cố ý tách "chọn mô hình" khỏi "kết quả test" để câu chuyện không lẫn.
