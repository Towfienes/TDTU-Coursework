# Bài kiểm tra thực hành N4 — Phân tích & trực quan hoá dữ liệu (TDTU)

**MSSV trên hệ thống / tên file:** 524H0195 · **seed sinh dữ liệu:** 5240195 (bỏ chữ H)
→ **P = 5**, **K = 11**, P lẻ nên B4 là **box plot**

## Quy ước tên (quan trọng)

| Chỗ | Dùng | Lý do |
|---|---|---|
| `MSSV` trong notebook, tên `.ipynb`, `_b4.png`, `.zip` | **524H0195** | đúng MSSV trên Elearning + yêu cầu "lưu thành MSSV.ipynb / MSSV_b4.png" |
| seed trong `gen_data.py` | **5240195** | `random.Random(int(...))` chỉ nhận số; hàm `_seed()` lấy phần chữ số |

Vì vậy cell "Sinh dữ liệu" của đề **không sửa một chữ** (vẫn gọi `gen_data.py <MSSV>` và đọc `sales_<MSSV>.txt` = `sales_524H0195.txt`).

## Nộp bài — `524H0195.zip` gồm đúng 3 file theo bảng trên lớp

| File | Nguồn |
|---|---|
| `524H0195.ipynb` | `starter.ipynb` + điền hết `# TODO`, **giữ nguyên toàn bộ output** |
| `gen_data.py` | file gốc + **6 dòng `_seed()`** (lấy phần số của MSSV), không đổi gì khác |
| `524H0195_b4.png` | hình B4, 1350×780 px, dpi 150 |

`sales_524H0195.txt` **không** cần nộp — notebook tự sinh lại.

## Số liệu chạy thật (đối chiếu bằng script độc lập, khớp 100 %)

| Chỉ tiêu | Kết quả |
|---|---|
| Tổng dòng file | 382 |
| B1: dòng ORDER (kể cả lặp) / đơn huỷ / dòng rác | 346 / 12 / 24 |
| B2: sau bước 1 / bước 2 / bước 3 | 322 / 310 / 296 |
| B2: số giá thiếu trước khi điền | 21 |
| B3a: tổng doanh thu | 2.792.018.000 VND |
| B3a: xếp hạng chi nhánh | TD 1.016.714.500 > Q7 735.384.500 > Q1 620.412.500 > BT 419.506.500 |
| B3b: đơn share lớn nhất | `0258` · BT · 20,24 % |
| B3c: khách ≥ 11 đơn / số đơn còn lại | 16 khách / 216 đơn |
| B4: trung vị cao nhất | Laptop 32.887.000 VND/đơn (Chuot 515.000 → gấp ~64 lần) |

## Bẫy dữ liệu đã xử lý

- `qty=?` bỏ **trước** `astype(int)`; `qty` 99/120/999 bỏ **sau** khi đổi int.
- Giá: `1.165.000 VND`, `257000`, `4.20tr`, `0.24tr` (< 1 triệu), `?` → `to_vnd()` trả `NaN` cho `?`.
- `branch`: `Q1`, `q1`, ` Q1  ` → `strip().upper()` ở bước 4 (bước 1–3 vẫn dùng chuỗi gốc).
- Giá thiếu điền bằng trung vị **theo mặt hàng** qua `groupby("item")["price"].transform("median")`; đếm thiếu **trước** khi điền.
- `order_id` giữ chuỗi zero-pad để khớp tập `cancelled`; dòng `CANCEL` không lọt vào `rows`; 5 loại dòng rác không match pattern nào.

## Đối chiếu yêu cầu (đã kiểm bằng script, không phải đọc mắt)

| Yêu cầu | Cách làm | Bằng chứng |
|---|---|---|
| Điền MSSV, chạy cell Sinh dữ liệu | `MSSV = "524H0195"` | in `P = 5 | K = 11` |
| Notebook tự gọi `gen_data.py`, in 8 dòng đầu | cell 3 giữ nguyên 100 % | output "Da tao sales_524H0195.txt (382 dong)" + 8 dòng |
| B1: `ORDER_PATTERN` 7 nhóm, giữ chuỗi | `re.compile(ORDER_PATTERN).groups == 7`, DataFrame cột `object` | 346 / 12 / 24 |
| B1: `CANCEL_PATTERN` lấy `order_id` | `re.search` → `('0005',)` | 12 đơn huỷ |
| B1: đếm dòng rác | nhánh `else` của vòng lặp | 24 |
| B2 đúng thứ tự 1→5 | vị trí lệnh: `'?'` → `astype(int)` → `<=50`; `isna()` trước `fillna` | 322 / 310 / 296, thiếu 21 |
| B2.4 `to_vnd` | hàm xử lý 4 dạng + `NaN` | `4.068.000 VND` → 4068000 |
| B2.5 `groupby(...).transform(...)` | `transform("median")` | không còn NaN sau điền |
| B3a/b `transform` cho share | `transform("sum")` | 0258 · 20,24 % |
| B3c `groupby('cust').filter` | `lambda g: len(g) >= K` | 16 khách / 216 đơn |
| B4 chỉ matplotlib + list | `ax.boxplot`, `ax.annotate`, `.tolist()`; code **không** có `seaborn`/`df.plot`/`sns.` | grep toàn bộ code cell |
| B4 P lẻ: box plot 5 mặt hàng, y log, đánh dấu trung vị cao nhất | `set_yscale("log")`, Laptop tô cam + kim cương đỏ + nhãn | `524H0195_b4.png` |
| 1 câu nhận xét có số | "…~32,9 triệu VND/đơn, gấp khoảng 64 lần Chuot (~0,52 triệu)…" | cell markdown cuối |
| Không đổi tên biến/hàm | `n_step1..3`, `to_vnd`, `n_missing_price`, `total_revenue`, `branch_revenue`, `top_share`, `loyal`, `raw`, `df` giữ nguyên | so từng cell |
| Giữ output, đổi tên file | 9/9 cell có output, exec 1→9 | `524H0195.ipynb` |

## Chạy lại

```bash
cd <thư mục có 3 file>
python gen_data.py 524H0195      # hoặc chỉ cần chạy cell "Sinh dữ liệu"
```

Đã kiểm chứng: giải nén zip ra **thư mục trống khác** → 9/9 cell, 0 lỗi, sinh lại đúng `sales_524H0195.txt` (382 dòng) + `524H0195_b4.png`, số liệu trùng khít.

## `starter.ipynb`

Giữ nguyên bản gốc chưa sửa để đối chiếu; bản nộp là `524H0195.ipynb`.

## Kiểm chứng độc lập (không nằm trong zip)

`verify_independent.py` — chạy `python verify_independent.py`:

- Parse lại file bằng `str.split` + `dict` (**không pandas, không regex**) → so **từng dòng** `df` của notebook.
- Exec lại đúng 9 cell code của notebook trong namespace mới → so 296 dòng × 7 trường.
- So mọi con số đã in (B1/B2/B3) với bản tính độc lập; kiểm tra `revenue = qty*price`, `share` cộng = 1, giá trong ±15 % giá gốc mặt hàng.

Kết quả lần chạy cuối: **49 PASS / 0 FAIL**. File này KHÔNG có trong `524H0195.zip` (zip đúng 3 file theo bảng).
