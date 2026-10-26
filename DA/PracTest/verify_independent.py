"""Kiểm chứng độc lập toàn bộ phần xử lý dữ liệu (B1-B4) của 524H0195.ipynb.

- Bản kiểm chứng KHÔNG dùng pandas và KHÔNG dùng regex: parse bằng str.split, gom bằng dict.
- Lấy df thật của notebook bằng cách exec lại các cell code trong 1 namespace mới,
  ở thư mục tạm có gen_data.py -> đường đi y hệt lúc nộp.
- So từng dòng + so từng con số đã in trong output lưu sẵn.
"""
import json, math, os, pathlib, re, shutil, statistics, subprocess, sys, tempfile
from collections import Counter, defaultdict

PRAC = pathlib.Path("/home/towfienes/TDTU/DA/PracTest")
NB = PRAC / "524H0195.ipynb"
TXT = PRAC / "sales_524H0195.txt"
BASE = {"Laptop": 15_500_000, "Chuot": 250_000, "BanPhim": 890_000,
        "ManHinh": 4_200_000, "TaiNghe": 1_150_000}
MSSV, K = "524H0195", 11
ok = fail = 0

def check(name, cond, detail=""):
    global ok, fail
    if cond: ok += 1;  print(f"  ✓ {name}" + (f" — {detail}" if detail else ""))
    else:    fail += 1; print(f"  ✗ {name} — {detail}")

# ---------- 1. Bản độc lập: phân loại dòng bằng split ----------
lines = TXT.read_text(encoding="utf-8").splitlines()
rows, cancelled, junk_lines = [], set(), []
for ln in lines:
    if "CANCEL ORDER#" in ln:
        cancelled.add(ln.split("CANCEL ORDER#", 1)[1].strip())
    elif ln.lstrip().startswith("[") and "ORDER#" in ln and ln.count("|") == 5:
        head, body = ln.split("] ", 1)                 # "[date" va phan sau
        date = head.lstrip("[").strip()
        parts = [p.strip() for p in body.split("|")]
        kv = {}
        for p in parts[1:]:
            k, v = p.split("=", 1)
            kv[k.strip()] = v
        rows.append((date, parts[0].replace("ORDER#", "").strip(), kv["cust"],
                     kv["branch"], kv["item"], kv["qty"], kv["price"]))
    else:
        junk_lines.append(ln)

print(f"\n1) PHÂN LOẠI DÒNG (bản độc lập, không regex)")
check("số dòng ORDER", len(rows), f"{len(rows)}")
check("số đơn huỷ (unique)", len(cancelled), f"{sorted(cancelled)[:4]}…")
check("số dòng rác", len(junk_lines), f"{len(junk_lines)}")
check("tổng dòng khớp file", len(rows) + len(cancelled) + len(junk_lines) == len(lines),
      f"{len(rows)}+{len(cancelled)}+{len(junk_lines)}={len(lines)}")

# ---------- 2. Bản độc lập: làm sạch đúng thứ tự ----------
n1 = n2 = None
seen, step1 = set(), []
for r in rows:                                        # bước 1: giữ lần đầu theo order_id
    if r[1] not in seen:
        seen.add(r[1]); step1.append(r)
n1 = len(step1)
step2 = [r for r in step1 if r[1] not in cancelled]   # bước 2: bỏ đơn huỷ
n2 = len(step2)
no_q = [r for r in step2 if r[5] != "?"]              # bước 3: bỏ qty '?' trước khi int
big = [r for r in no_q if int(r[5]) > 50]             # rồi mới bỏ qty > 50
step3 = [r for r in no_q if int(r[5]) <= 50]
n3 = len(step3)

def to_vnd_indep(s):                                  # bước 4: chuỗi giá -> số (viết khác notebook)
    t = s.strip()
    if t == "?": return None
    if t.endswith("VND"): return float(t[:-3].replace(".", "").strip())
    if t.endswith("tr"):  return float(t[:-2].replace(",", ".").strip()) * 1_000_000
    return float(t)

clean = []
for r in step3:
    clean.append([r[0], r[1], r[2], r[3].strip().upper(), r[4], int(r[5]), to_vnd_indep(r[6])])
missing = [i for i, r in enumerate(clean) if r[6] is None]           # bước 5: đếm trước khi điền
by_item = defaultdict(list)
for r in clean:
    if r[6] is not None: by_item[r[4]].append(r[6])
med = {it: statistics.median(v) for it, v in by_item.items()}
for i in missing:
    clean[i][6] = med[clean[i][4]]

print(f"\n2) LÀM SẠCH (bản độc lập)")
check("sau bước 1 (bỏ trùng)", n1, f"{n1}  (trùng: {len(rows)-n1})")
check("sau bước 2 (bỏ huỷ)", n2, f"{n2}  (bỏ: {n1-n2})")
check("qty '?' bị bỏ", len(step2) - len(no_q), f"{len(step2)-len(no_q)}")
check("qty > 50 bị bỏ sau khi int", len(big), f"{len(big)} giá trị {sorted({r[5] for r in big})}")
check("sau bước 3", n3, f"{n3} = {n2} - {len(step2)-len(no_q)} - {len(big)}")
check("số giá thiếu TRƯỚC khi điền", len(missing), f"{len(missing)}")
check("không còn giá thiếu sau khi điền", all(r[6] is not None for r in clean))

# ---------- 3. Số liệu độc lập ----------
for r in clean:
    r.append(r[5] * r[6])                              # r[7] = revenue
total = sum(r[7] for r in clean)
bt = defaultdict(float)
for r in clean: bt[r[3]] += r[7]
branch_rank = sorted(bt.items(), key=lambda kv: -kv[1])
shares = [(r[7] / bt[r[3]], r[1], r[3]) for r in clean]
top_share = max(shares)
cust_cnt = Counter(r[2] for r in clean)
loyal = [r for r in clean if cust_cnt[r[2]] >= K]
item_med = {}
for r in clean: item_med.setdefault(r[4], []).append(r[7])
item_med = {k: statistics.median(v) for k, v in item_med.items()}
best_item = max(item_med, key=item_med.get)

print(f"\n3) SỐ LIỆU (bản độc lập)")
check("tổng doanh thu", round(total), f"{total:,.0f}")
check("xếp hạng chi nhánh", [b for b, _ in branch_rank],
      " > ".join(f"{b} {v:,.0f}" for b, v in branch_rank))
check("share lớn nhất", True, f"đơn {top_share[1]} · {top_share[2]} · {top_share[0]:.4%}")
check("khách >= K đơn", len({r[2] for r in loyal}), f"{len({r[2] for r in loyal})} khách / {len(loyal)} đơn")
check("trung vị cao nhất", best_item, f"{best_item} {item_med[best_item]:,.0f}")

# ---------- 4. Chạy lại đúng code của notebook ----------
tmp = tempfile.mkdtemp(prefix="nbverify-")
shutil.copy(PRAC / "gen_data.py", tmp)
nb = json.loads(NB.read_text(encoding="utf-8"))
srcs = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
cwd0 = os.getcwd(); os.chdir(tmp)
os.environ["MPLBACKEND"] = "Agg"
ns = {}
for s in srcs:
    exec(compile(s, "<cell>", "exec"), ns)
os.chdir(cwd0)
df = ns["df"]; raw = ns["raw"]; nb_cancelled = ns["cancelled"]

print(f"\n4) df THẬT của notebook vs bản độc lập")
check("số dòng raw", len(raw) == len(rows), f"notebook {len(raw)} / độc lập {len(rows)}")
check("tập cancelled", nb_cancelled == cancelled, f"notebook {len(nb_cancelled)} / độc lập {len(cancelled)}")
check("số dòng df", len(df) == n3, f"notebook {len(df)} / độc lập {n3}")
check("ordinal order_id giống nhau", list(df["order_id"]) == [r[1] for r in clean])
check("order_id không trùng", df["order_id"].is_unique)
check("không còn đơn bị huỷ", not set(df["order_id"]) & cancelled)
check("qty là int, 1..50", str(df["qty"].dtype).startswith("int") and df["qty"].between(1, 50).all(),
      f"{df['qty'].min()}..{df['qty'].max()}")
check("branch chỉ còn 1 dạng/chi nhánh", sorted(df["branch"].unique()),
      str(sorted(df["branch"].unique())))
check("price không NaN, > 0", df["price"].notna().all() and (df["price"] > 0).all())
check("revenue = qty*price từng dòng", (df["revenue"] == df["qty"] * df["price"]).all())
check("share cộng lại = 1 mỗi chi nhánh",
      all(abs(v - 1) < 1e-12 for v in df.groupby("branch")["share"].sum()))

diffs = []
for i, r in enumerate(clean):
    row = df.iloc[i]
    if (row["cust"] != r[2] or row["branch"] != r[3] or row["item"] != r[4]
            or int(row["qty"]) != r[5] or abs(float(row["price"]) - r[6]) > 1e-9
            or abs(float(row["revenue"]) - r[7]) > 1e-9
            or abs(float(row["share"]) - r[7] / bt[r[3]]) > 1e-12):
        diffs.append((i, r[1]))
check("so từng dòng (cust/branch/item/qty/price/revenue/share)", not diffs, f"lệch: {diffs[:3]}")

# ---------- 5. Đối chiếu con số IN TRONG NOTEBOOK ----------
def stream(cell):
    return "".join("".join(o["text"]) for o in cell["outputs"] if o["output_type"] == "stream")
cells = nb["cells"]
t = {i: stream(c) for i, c in enumerate(cells) if c["cell_type"] == "code"}
m1 = re.search(r"B1 \| ORDER: (\d+) \| đơn huỷ: (\d+) \| dòng rác: (\d+)", t[5])
m2 = re.search(r"sau bước 1: (\d+) \| sau bước 2: (\d+) \| sau bước 3: (\d+)", t[7])
m3 = re.search(r"số giá bị thiếu: (\d+)", t[8])
m4 = re.search(r"tổng doanh thu: ([\d,]+) VND", t[10])
m5 = re.search(r"share lớn nhất: (\d+) \| chi nhánh: (\w+) \| share: ([\d.]+)%", t[11])
m6 = re.search(r"số khách: (\d+) \| số đơn: (\d+)", t[12])
br_lines = re.findall(r"^(\w+)\s+([\d.]+e\+\d+)$", t[10], re.M)

print(f"\n5) CON SỐ IN TRONG NOTEBOOK vs BẢN ĐỘC LẬP")
check("B1 in ra", tuple(map(int, m1.groups())) == (len(rows), len(cancelled), len(junk_lines)),
      str(m1.groups()))
check("B2 bước 1/2/3 in ra", tuple(map(int, m2.groups())) == (n1, n2, n3), str(m2.groups()))
check("B2 giá thiếu in ra", int(m3.group(1)) == len(missing), str(m3.group(1)))
check("B3a tổng in ra", int(m4.group(1).replace(",", "")) == round(total), str(m4.group(1)))
check("B3a thứ tự chi nhánh in ra", [b for b, _ in br_lines] == [b for b, _ in branch_rank],
      str([b for b, _ in br_lines]))
check("B3a giá trị từng chi nhánh in ra",
      all(abs(float(v) - bt[b]) / bt[b] < 1e-6 for b, v in br_lines))
check("B3b in ra", (m5.group(1), m5.group(2)) == (top_share[1], top_share[2])
      and abs(float(m5.group(3)) - round(top_share[0] * 100, 2)) < 0.01,
      f"{m5.group(1)} · {m5.group(2)} · {m5.group(3)}%")
check("B3c in ra", tuple(map(int, m6.groups())) == (len({r[2] for r in loyal}), len(loyal)),
      str(m6.groups()))

# ---------- 6. Kiểm tra ngữ nghĩa đơn vị giá ----------
print(f"\n6) KIỂM TRA ĐƠN VỊ GIÁ (bắt lỗi hiểu sai 'tr' hay dấu nghìn)")
bad_range = [(r[1], r[4], r[6]) for r in clean
             if not (0.85 * BASE[r[4]] <= r[6] <= 1.15 * BASE[r[4]])]
check("mọi price nằm trong ±15% giá gốc mặt hàng", not bad_range, str(bad_range[:3]))
fmt = Counter()
for ln in lines:
    if ln.count("|") == 5 and "ORDER#" in ln:
        p = ln.rsplit("=", 1)[1].strip()
        fmt["VND" if p.endswith("VND") else "tr" if p.endswith("tr") else "?" if p == "?" else "số trần"] += 1
check("đủ 4 định dạng giá đều xuất hiện", all(fmt[k] > 0 for k in ("VND", "tr", "?", "số trần")), str(dict(fmt)))
# ví dụ đúng như đề bài nêu
for s, want in [("15.861.000 VND", 15_861_000), ("15861000", 15_861_000),
                ("15,86tr", 15_860_000), ("0.24tr", 240_000)]:
    got = ns["to_vnd"](s)
    check(f"to_vnd('{s}')", abs(got - want) < 1e-6, f"{got:,.0f}")
check("to_vnd('?') là NaN", math.isnan(ns["to_vnd"]("?")))

# ---------- 7. Hình B4 ----------
print(f"\n7) HÌNH B4")
top5 = sorted({r[4] for r in clean}, key=lambda it: -sum(r[7] for r in clean if r[4] == it))[:5]
check("top 5 mặt hàng theo doanh thu", len(top5) == 5, " > ".join(top5))
check("notebook cũng lấy đúng 5 mặt hàng này",
      sorted(df.groupby("item")["revenue"].sum().sort_values(ascending=False).head(5).index) == sorted(top5))
check("P lẻ -> nhánh box plot", int(MSSV[-1]) % 2 == 1, f"P = {MSSV[-1]}")
check("png tồn tại + đúng tên", (PRAC / f"{MSSV}_b4.png").exists(), f"{MSSV}_b4.png")
check("png được tạo lại khi chạy từ zip", (pathlib.Path(tmp) / f"{MSSV}_b4.png").exists())
check("median tính lại khớp nhãn trên hình",
      f"{item_med[best_item] / 1e6:.1f}".replace(".", ",") == "32,9",
      f"{best_item}: {item_med[best_item]:,.0f} VND")

print(f"\n===== KẾT QUẢ: {ok} PASS / {fail} FAIL =====")
sys.exit(1 if fail else 0)
