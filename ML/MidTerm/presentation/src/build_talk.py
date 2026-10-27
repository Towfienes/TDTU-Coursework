"""Build TRANSCRIPT.md, TRANSCRIPT_THEO_SLIDE.md (and optionally the mobile study viewer)
from talk_content.json.

talk_content.json is the single source of the spoken script. build_deck.js reads the
same file for the PPTX speaker notes, so notes, transcript and viewer never drift.

Usage (from presentation/):
    python3 src/build_talk.py                     # writes TRANSCRIPT.md and TRANSCRIPT_THEO_SLIDE.md
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

# short, slide-anchored version ("guide")
t = 0.0
for s in SLIDES:
    s["gwords"] = sum(len(g["say"].split()) for g in s["guide"])
    s["gdur"] = s["gwords"] / WPM * 60
    s["gstart"] = t
    t += s["gdur"]
GTOTAL = t
GWORDS = sum(s["gwords"] for s in SLIDES)


def build_transcript():
    by = {}
    for s in SLIDES:
        by.setdefault(s["speaker"], []).append(s)
    L = [
        "# Transcript thuyết trình — Midterm ML",
        "",
        "**Đề tài:** Hồi quy & Phân loại — Câu 1 (Gradient Descent tự cài đặt) và Câu 2 (phân loại trên OpenML credit-g)  ",
        f"**Thời lượng:** tổng lời thoại {TOTAL_WORDS} từ, đọc ở nhịp ~{WPM} từ/phút ≈ **{mmss(TOTAL)}**; phần còn lại của slot 10 phút dành cho chuyển slide và hỏi đáp.  ",
        "**Cách trình bày:** lời thoại không gắn tên người nói, nên dùng nguyên văn được cho cả hai trường hợp: **một người trình bày cả 14 slide**, hoặc **cả nhóm chia phần** theo gợi ý bên dưới (khi đó thêm câu chuyển lời ở slide 7 và 11).",
        "",
        f"> Cần bản ngắn hơn, nói theo từng vùng trên slide? Xem `TRANSCRIPT_THEO_SLIDE.md` ({GWORDS} từ ≈ {mmss(GTOTAL)}).",
        "> File này được sinh từ `src/talk_content.json` bằng `python3 src/build_talk.py`; speaker notes trong `midterm_presentation.pptx` dùng cùng nguồn.",
        "> Muốn sửa lời thoại thì sửa file JSON rồi dựng lại, đừng sửa trực tiếp file này. Số liệu đã đối chiếu với `../results/*.json`.",
        "",
        "## Nếu cả nhóm chia phần",
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
        "- Thầy có thể gọi một người bất kỳ lên trình bày cả bài, nên **mỗi thành viên tập đủ 14 slide**, không chỉ phần của mình.",
        "- Slide 2 có ghi tên người phụ trách từng phần; khi nói chỉ cần nêu nội dung ba phần, không đọc tên.",
        "",
        "## Lời thoại theo slide",
        "",
    ]
    for s in SLIDES:
        L += [
            f"### Slide {s['n']} — {s['title']}",
            f"Bắt đầu {mmss(s['start'])} · ~{int(round(s['dur']))}s · nếu chia phần: **{s['speaker']}**",
            "",
            f"> {s['script']}",
            "",
            *([f"*Chỉ khi chia phần, thêm câu chuyển lời:* “{s['handoff']}”", ""] if s.get("handoff") else []),
            f"**Chốt:** {s['key']}",
            "",
        ]
    L += ["## Câu hỏi dự kiến", "", "Khi trình bày một mình, người trình bày trả lời tất cả; cột cuối chỉ là gợi ý khi cả nhóm cùng đứng lên.", "",
          "| Câu hỏi | Ý chính | Phụ trách (nếu chia phần) |", "|---|---|---|"]
    for qa in TALK["qa"]:
        L.append(f"| {qa['q']} | {qa['a']} | {qa['who']} |")
    L += [
        "",
        "## Ghi chú trung thực học thuật",
        "",
        "- Mọi con số trong lời thoại lấy từ `results/`; không có kết quả nào được chạy riêng cho phần trình bày.",
        "- Bài làm có sử dụng hỗ trợ AI trong soạn thảo và kiểm tra; nhóm đã rà lại toàn bộ.",
        "",
    ]
    return "\n".join(L)


def build_guide():
    L = [
        "# Nói theo slide — bản ngắn",
        "",
        f"Mỗi slide có 2–5 bước. Mỗi bước bắt đầu bằng **vùng cần chỉ trên slide**, sau đó là câu để nói. Tổng {GWORDS} từ, đọc ở ~{WPM} từ/phút ≈ **{mmss(GTOTAL)}**.",
        "",
        "Cách dùng: nhìn slide, chỉ vào vùng in đậm, nói câu bên cạnh. Bản đầy đủ có giải thích \"vì sao\" nằm ở `TRANSCRIPT.md`.",
        "Lời thoại không gắn tên người nói; khi cả nhóm chia phần, thêm câu chuyển lời ở slide 7 và 11.",
        "",
        "> File này được sinh từ `src/talk_content.json` (trường `guide`) bằng `python3 src/build_talk.py`.",
        "",
    ]
    for s in SLIDES:
        L += [f"## {s['n']}. {s['title']}", f"Bắt đầu {mmss(s['gstart'])} · ~{int(round(s['gdur']))}s", ""]
        for i, g in enumerate(s["guide"], 1):
            L.append(f"{i}. **{g['at']}** — {g['say']}")
        if s.get("handoff"):
            L += ["", f"*Chỉ khi chia phần:* “{s['handoff']}”"]
        L.append("")
    return "\n".join(L)


def build_viewer(out):
    from PIL import Image

    keys = ["n", "eyebrow", "title", "speaker", "speakerFull", "script", "key", "de", "points", "more", "trap", "refs"]
    data = [dict({k: s[k] for k in keys}, guide=s["guide"], handoff=s.get("handoff", ""),
                 start=round(s["start"]), dur=round(s["dur"]), gstart=round(s["gstart"]), gdur=round(s["gdur"]))
            for s in SLIDES]
    tpl = open(os.path.join(SRC, "study_viewer.html"), encoding="utf-8").read()
    html = (tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
               .replace("__TOTAL__", mmss(TOTAL))
               .replace("__WORDS__", str(TOTAL_WORDS))
               .replace("__GTOTAL__", mmss(GTOTAL))
               .replace("__GWORDS__", str(GWORDS)))
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
    open(os.path.join(PRES, "TRANSCRIPT_THEO_SLIDE.md"), "w", encoding="utf-8").write(build_guide())
    if a.viewer:
        build_viewer(a.viewer)
    print(f"slides: {len(SLIDES)} | full: {TOTAL_WORDS} words, {mmss(TOTAL)} | theo slide: {GWORDS} words, {mmss(GTOTAL)}")
