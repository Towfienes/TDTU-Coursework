# MỞ FILE NÀY TRƯỚC — DEMO NOR

Gói demo để mang sang máy khác. Giải nén cả thư mục, không chuyển riêng notebook vì code cần data/src/references đi kèm.

## Đọc và thuyết trình ngay, không cần cài Python

1. Mở `slides/` → PowerPoint để thuyết trình; dùng PDF nếu máy không có PowerPoint. Đây là bản màu REVIEW đã kiểm tra.
2. Mở `NOTEBOOK_DOC_OFFLINE.html` bằng Chrome/Edge/Firefox: có code, bảng và biểu đồ đã chạy, không cần mạng.
3. Mở `slides/Speaker_Notes_VI.md` để đọc lời thoại; `Demo_VI.md` có lời đọc chia đúng 6 phần của notebook, khoảng 120 giây; `Viva_VI.md` có câu hỏi phản biện. File .md có thể đọc bằng Notepad/VS Code.
4. Báo cáo Word/PDF nằm trong `report/`.

Transcript mới dự kiến 13 phút 20 giây: slide 1–14 → slide 15 chuyển sang notebook khoảng 120 giây → trở lại slide 16 kết luận. Slide 17–19 là phụ lục. Dùng lời thoại trong hai file Markdown; Notes nhúng trong PPTX vẫn là bản trước. Thời lượng cần được đo lại khi nhóm luyện nói.

## Nếu muốn chạy code trên máy mới

Cần Python 3.12 và mạng để cài thư viện lần đầu. Mở terminal tại thư mục DEMO_NOR:

```
python -m venv .venv
```

Windows:
```
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python tools/run_notebook.py
```

Linux/macOS:
```
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/run_notebook.py
```

Lệnh trên chạy toàn bộ notebook và cập nhật output/tables/figures. Để bấm chạy từng cell, mở notebook trong VS Code có extension Python/Jupyter và chọn interpreter .venv vừa tạo. Có thể chỉ đọc HTML khi không cài được môi trường.

## Cấu trúc

- `slides/`: slide màu, lời thoại, demo, câu hỏi.
- `report/`: báo cáo để đọc.
- `notebooks/`: notebook gốc có output.
- `data/`: dữ liệu thô và split/bản xử lý.
- `src/`: hàm phân tích notebook sử dụng.
- `references/`: codebook và nguồn UCI.
- `results/`: số liệu CSV/JSON và biểu đồ PNG để mở riêng.
- `tools/run_notebook.py`: chạy notebook trong kernel mới.

Dataset: https://archive.ics.uci.edu/dataset/1/abalone

Đây là gói DEMO phục vụ trình chiếu. Slide và Báo cáo đã được gắn link YouTube chính thức: https://youtu.be/D-H3yQ4IDro?si=VZ5VouVBJcCDhlBc (thời lượng 12 phút, đáp ứng khung 7–15 phút).
