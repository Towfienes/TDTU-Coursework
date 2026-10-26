"""Sinh du lieu ca nhan hoa cho bai kiem tra. Chay: python gen_data.py <MSSV>"""
import random, sys
from datetime import datetime, timedelta

def _seed(mssv):
    """MSSV tren Elearning co chu (vd 524H0195) -> chi lay phan so (5240195) lam seed.

    Voi MSSV toan so, int(mssv) va ham nay cho cung mot seed nen du lieu khong doi.
    """
    digits = "".join(ch for ch in str(mssv) if ch.isdigit())
    return int(digits) if digits else mssv


def generate(mssv):
    rnd = random.Random(_seed(mssv))
    branches = rnd.sample(["Q1", "Q3", "Q7", "TD", "BT", "GV"], 4)
    items = {"Laptop": 15_500_000, "Chuot": 250_000, "BanPhim": 890_000,
             "ManHinh": 4_200_000, "TaiNghe": 1_150_000}
    customers = sorted({f"KH{rnd.randint(100, 999)}" for _ in range(25)})
    junk = ["# SYSTEM: backup completed", "WARN: printer offline",
            "----------------------------------------", "INFO: sync with server OK",
            "ERROR: timeout while reading POS"]
    start = datetime(2025, 1, 1)
    lines, n = [], rnd.randint(280, 340)
    for oid in range(1, n + 1):
        t = start + timedelta(days=rnd.randint(0, 89), minutes=rnd.randint(480, 1260))
        item = rnd.choice(list(items))
        price = int(items[item] * rnd.uniform(0.9, 1.1)) // 1000 * 1000
        qty = rnd.choices([1, 2, 3, 4, 5], [40, 25, 15, 10, 10])[0]
        br = rnd.choice(branches)
        r = rnd.random()
        br_s = br.lower() if r < 0.25 else (f" {br} " if r < 0.35 else br)
        r = rnd.random()
        if r < 0.5:   price_s = f"{price:,}".replace(",", ".") + " VND"
        elif r < 0.8: price_s = str(price)
        elif r < 0.93: price_s = f"{price / 1e6:.2f}tr"
        else:         price_s = "?"
        r = rnd.random()
        qty_s = "?" if r < 0.04 else (str(rnd.choice([99, 120, 999])) if r < 0.06 else str(qty))
        line = (f"[{t:%Y-%m-%d %H:%M}] ORDER#{oid:04d} | cust={rnd.choice(customers)} | "
                f"branch={br_s} | item={item} | qty={qty_s} | price={price_s}")
        lines.append(line)
        if rnd.random() < 0.05: lines.append(line)                 # dong trung lap
        if rnd.random() < 0.04:                                     # don bi huy
            lines.append(f"[{t + timedelta(hours=2):%Y-%m-%d %H:%M}] CANCEL ORDER#{oid:04d}")
        if rnd.random() < 0.07: lines.append(rnd.choice(junk))     # dong rac
    with open(f"sales_{mssv}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Da tao sales_{mssv}.txt ({len(lines)} dong)")

if __name__ == "__main__":
    generate(sys.argv[1])
