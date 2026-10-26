"""Build TRANSCRIPT.md (and optionally the mobile study viewer) from talk_content.json.

talk_content.json is the single source of the spoken script. build_deck.js reads the
same file for the PPTX speaker notes, so notes, transcript and viewer never drift.

Usage (from presentation/):
    python3 src/build_talk.py                     # writes TRANSCRIPT.md
    python3 src/build_talk.py --viewer OUT_DIR    # also builds the study viewer into OUT_DIR

The viewer renders slide images from midterm_presentation.pdf, so rebuild the PDF first.
It needs pdftoppm (poppler) and Pillow. OUT_DIR is a build output; do not commit it.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import tempfile

SRC = os.path.dirname(os.path.abspath(__file__))
PRES = os.path.dirname(SRC)
TALK = json.load(open(os.path.join(SRC, "talk_content.json"), encoding="utf-8"))
SLIDES = TALK["slides"]
WPM = TALK["wpm"]


def mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


t = 0.0
for i, s in enumerate(SLIDES, 1):
    s["n"] = i
    s["words"] = len(s["script"].split())
    s["dur"] = s["words"] / WPM * 60
    s["start"] = t
    s["speakerFull"] = TALK["speakers"][s["speaker"]]
    t += s["dur"]
TOTAL = t
TOTAL_WORDS = sum(s["words"] for s in SLIDES)


def build_transcript():
    by = {}
    for s in SLIDES:
        by.setdefault(s["speaker"], []).append(s)
    L = [
        "# Transcript thuyết trình — Midterm ML",
        "",
        "**Đề tài:** Hồi quy & Phân loại — Câu 1 (Gradient Descent tự cài đặt) và Câu 2 (phân loại trên OpenML credit-g)  ",
        f"**Thời lượng:** tổng lời thoại {TOTAL_WORDS} từ, đọc ở nhịp ~{WPM} từ/phút ≈ **{mmss(TOTAL)}**; phần còn lại của slot 10 phút dành cho chuyển slide và hỏi đáp.  ",
        "**Người trình bày:** Tiến (Câu 1) · Thành (Câu 2: dữ liệu, quy trình, chọn mô hình) · Tâm (đọc kết quả, overfitting, kết luận)",
        "",
        "> File này được sinh từ `src/talk_content.json` bằng `python3 src/build_talk.py`; speaker notes trong `midterm_presentation.pptx` dùng cùng nguồn.",
        "> Muốn sửa lời thoại thì sửa file JSON rồi dựng lại, đừng sửa trực tiếp file này. Số liệu đã đối chiếu với `../results/*.json`.",
        "",
        "## Phân chia và mốc thời gian",
        "",
        "| Người | Slide | Bắt đầu | Thời lượng | Số từ |",
        "|---|---|---|---|---|",
    ]
    for sp, ss in by.items():
        d = sum(x["dur"] for x in ss)
        w = sum(x["words"] for x in ss)
        L.append(f"| {sp} | {ss[0]['n']}–{ss[-1]['n']} | {mmss(ss[0]['start'])} | {mmss(d)} | {w} |")
    L += [
        "",
        "## Mẹo giữ nhịp",
        "",
        f"- Mốc kiểm tra: bắt đầu slide 5 ở **{mmss(SLIDES[4]['start'])}**, slide 8 ở **{mmss(SLIDES[7]['start'])}**, slide 12 ở **{mmss(SLIDES[11]['start'])}**. Trễ hơn 30 giây thì bỏ câu kiểm chứng gradient ở slide 4 và câu về kNN ở slide 10.",
        "- Không đọc công thức từng ký hiệu: nói ý nghĩa rồi chỉ vào slide.",
        "- Nói chậm lại ở câu chốt của mỗi slide (dòng **Chốt** bên dưới).",
        "",
        "## Lời thoại theo slide",
        "",
    ]
    for s in SLIDES:
        L += [
            f"### Slide {s['n']} — {s['title']}",
            f"**{s['speaker']}** · bắt đầu {mmss(s['start'])} · ~{int(round(s['dur']))}s",
            "",
            f"> {s['script']}",
            "",
            f"**Chốt:** {s['key']}",
            "",
        ]
    L += ["## Câu hỏi dự kiến và người trả lời", "", "| Câu hỏi | Người trả lời | Ý chính |", "|---|---|---|"]
    for qa in TALK["qa"]:
        L.append(f"| {qa['q']} | {qa['who']} | {qa['a']} |")
    L += [
        "",
        "## Ghi chú trung thực học thuật",
        "",
        "- Mọi con số trong lời thoại lấy từ `results/`; không có kết quả nào được chạy riêng cho phần trình bày.",
        "- Bài làm có sử dụng hỗ trợ AI trong soạn thảo và kiểm tra; nhóm đã rà lại toàn bộ.",
        "",
    ]
    return "\n".join(L)


def build_viewer(out):
    from PIL import Image

    keys = ["n", "eyebrow", "title", "speaker", "speakerFull", "script", "key", "points", "trap", "refs"]
    data = [dict({k: s[k] for k in keys}, start=round(s["start"]), dur=round(s["dur"])) for s in SLIDES]
    tpl = open(os.path.join(SRC, "study_viewer.html"), encoding="utf-8").read()
    html = (tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
               .replace("__TOTAL__", mmss(TOTAL))
               .replace("__WORDS__", str(TOTAL_WORDS)))
    os.makedirs(os.path.join(out, "slides"), exist_ok=True)
    os.makedirs(os.path.join(out, "thumbs"), exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    shutil.copyfile(os.path.join(PRES, "figures", "tdtu-logo.png"), os.path.join(out, "tdtu-logo.png"))
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-scale-to-x", "1600", "-scale-to-y", "-1", "-png",
                        os.path.join(PRES, "midterm_presentation.pdf"), os.path.join(tmp, "s")], check=True)
        pages = sorted(glob.glob(os.path.join(tmp, "s-*.png")))
        assert len(pages) == len(SLIDES), (len(pages), len(SLIDES))
        for i, p in enumerate(pages, 1):
            im = Image.open(p).convert("RGB")
            im.save(os.path.join(out, "slides", f"s{i:02d}.webp"), "WEBP", quality=84, method=6)
            im.resize((384, 216), Image.LANCZOS).save(os.path.join(out, "thumbs", f"s{i:02d}.webp"), "WEBP", quality=75)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--viewer", metavar="OUT_DIR", help="also build the study viewer into OUT_DIR")
    a = ap.parse_args()
    open(os.path.join(PRES, "TRANSCRIPT.md"), "w", encoding="utf-8").write(build_transcript())
    if a.viewer:
        build_viewer(a.viewer)
    print(f"slides: {len(SLIDES)} | words: {TOTAL_WORDS} | runtime: {mmss(TOTAL)}")
