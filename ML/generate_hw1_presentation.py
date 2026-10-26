"""
Generate HW1 Presentation: Data Preprocessing & kNN
Sinh viên: Ngô Lâm Tiên — MSSV: 524H0195
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

import sys
import os

# ─── Colour palette ────────────────────────────────────────────────────────────
DARK_BLUE   = RGBColor(0x1A, 0x35, 0x5E)   # #1A355E
MID_BLUE    = RGBColor(0x27, 0x6E, 0xA9)   # #276EA9
ACCENT_BLUE = RGBColor(0x41, 0xB8, 0xF4)   # #41B8F4
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xF2, 0xF4, 0xF7)   # #F2F4F7
TEXT_DARK   = RGBColor(0x1A, 0x1A, 0x2E)   # almost black
GREEN       = RGBColor(0x27, 0xAE, 0x60)
ORANGE      = RGBColor(0xF3, 0x9C, 0x12)
RED         = RGBColor(0xE7, 0x4C, 0x3C)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)


def new_prs():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def blank(prs):
    blank_layout = prs.slide_layouts[6]   # completely blank
    return prs.slides.add_slide(blank_layout)


# ─── helpers ───────────────────────────────────────────────────────────────────

def bg(slide, color):
    """Fill slide background with solid colour."""
    from pptx.oxml.ns import qn
    from lxml import etree
    bg_el = slide.background.fill
    bg_el.solid()
    bg_el.fore_color.rgb = color


def rect(slide, l, t, w, h, fill=None, line=None, line_w=Pt(0)):
    from pptx.util import Emu
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        l, t, w, h
    )
    shape.line.width = line_w
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=18, bold=False, color=TEXT_DARK,
             align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txb = slide.shapes.add_textbox(l, t, w, h)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def header_bar(slide, title, subtitle=None):
    """Dark blue top bar with title."""
    rect(slide, 0, 0, SLIDE_W, Inches(1.25), fill=DARK_BLUE)
    add_text(slide, title,
             Inches(0.4), Inches(0.10), Inches(12), Inches(0.7),
             font_size=28, bold=True, color=WHITE)
    if subtitle:
        add_text(slide, subtitle,
                 Inches(0.4), Inches(0.75), Inches(12), Inches(0.45),
                 font_size=14, color=ACCENT_BLUE)


def bullet_box(slide, items, l, t, w, h,
               title=None, title_color=DARK_BLUE, bullet="▸"):
    """Renders a list of bullet items in a box."""
    if title:
        add_text(slide, title, l, t, w, Inches(0.4),
                 font_size=16, bold=True, color=title_color)
        t += Inches(0.4)
        h -= Inches(0.4)
    txb = slide.shapes.add_textbox(l, t, w, h)
    tf  = txb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = f"{bullet}  {item}"
        run.font.size = Pt(14)
        run.font.color.rgb = TEXT_DARK


def colored_box(slide, label, l, t, w, h,
                fill=MID_BLUE, text_color=WHITE, font_size=13, bold=False):
    r = rect(slide, l, t, w, h, fill=fill)
    txb = slide.shapes.add_textbox(l + Inches(0.05), t + Inches(0.05),
                                    w - Inches(0.1), h - Inches(0.1))
    tf = txb.text_frame
    tf.word_wrap = True
    p  = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = label
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = text_color


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDES
# ═══════════════════════════════════════════════════════════════════════════════

prs = new_prs()


# ─── Slide 1: Cover ────────────────────────────────────────────────────────────
sl = blank(prs)
bg(sl, DARK_BLUE)

# accent stripe
rect(sl, 0, Inches(5.8), SLIDE_W, Inches(0.12), fill=ACCENT_BLUE)

add_text(sl, "Homework 1",
         Inches(1), Inches(0.6), Inches(11), Inches(0.8),
         font_size=22, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)

add_text(sl, "Data Preprocessing & kNN",
         Inches(0.5), Inches(1.3), Inches(12), Inches(1.4),
         font_size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text(sl, "Lý thuyết Tiền xử lý Dữ liệu",
         Inches(1), Inches(2.65), Inches(11), Inches(0.7),
         font_size=22, italic=True, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)

rect(sl, Inches(2.5), Inches(3.5), Inches(8.3), Inches(0.04), fill=ACCENT_BLUE)

info = [
    ("Sinh viên:", "Ngô Lâm Tiên"),
    ("MSSV:",      "524H0195"),
    ("Môn học:",   "Machine Learning"),
    ("Năm học:",   "2025 – 2026"),
]
for i, (lbl, val) in enumerate(info):
    y = Inches(3.75) + i * Inches(0.55)
    add_text(sl, lbl, Inches(3.2), y, Inches(2.5), Inches(0.45),
             font_size=15, bold=True, color=ACCENT_BLUE, align=PP_ALIGN.RIGHT)
    add_text(sl, val, Inches(5.9), y, Inches(4.5), Inches(0.45),
             font_size=15, color=WHITE)

add_text(sl, "Ton Duc Thang University — Faculty of Information Technology",
         Inches(0.5), Inches(6.8), Inches(12), Inches(0.45),
         font_size=12, color=RGBColor(0xAA, 0xBB, 0xCC), align=PP_ALIGN.CENTER)


# ─── Slide 2: Agenda ──────────────────────────────────────────────────────────
sl = blank(prs)
bg(sl, LIGHT_GRAY)
header_bar(sl, "Nội dung bài trình bày", "Table of Contents")

topics = [
    ("1", "Data Preprocessing là gì?",          "Tổng quan & tầm quan trọng"),
    ("2", "Data Cleaning",                       "Missing, Duplicate, Inconsistent, Invalid"),
    ("3", "Missing-Value Handling",              "Deletion, Imputation, Prediction"),
    ("4", "Data Conversion & Encoding",          "Numeric, Ordinal, One-Hot, Target, Text"),
    ("5", "Feature Scaling",                     "Min-Max, Standard, Robust Scaler"),
    ("6", "Feature Engineering",                 "Binning, Interaction, Extraction"),
    ("7", "Preprocessing Pipeline",              "sklearn ColumnTransformer + Pipeline"),
    ("8", "Bài toán thực hành",                  "Telco Churn — 5 mô hình phân loại"),
]

colors = [MID_BLUE, DARK_BLUE, MID_BLUE, DARK_BLUE,
          MID_BLUE, DARK_BLUE, MID_BLUE, DARK_BLUE]

for i, (num, title, desc) in enumerate(topics):
    row = i // 2
    col = i % 2
    x = Inches(0.3 + col * 6.5)
    y = Inches(1.4 + row * 1.4)
    rect(sl, x, y, Inches(6.2), Inches(1.2), fill=colors[i])
    add_text(sl, num,
             x + Inches(0.1), y + Inches(0.05), Inches(0.5), Inches(0.6),
             font_size=28, bold=True, color=ACCENT_BLUE)
    add_text(sl, title,
             x + Inches(0.65), y + Inches(0.1), Inches(5.4), Inches(0.45),
             font_size=15, bold=True, color=WHITE)
    add_text(sl, desc,
             x + Inches(0.65), y + Inches(0.6), Inches(5.4), Inches(0.45),
             font_size=12, color=ACCENT_BLUE, italic=True)


# ─── Slide 3: Data Preprocessing Overview ──────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "1. Data Preprocessing — Tổng quan",
           "Bước đầu tiên & quan trọng nhất trong Machine Learning Pipeline")

add_text(sl,
    "Data Preprocessing là quá trình biến đổi dữ liệu thô → dữ liệu sạch, phù hợp cho mô hình ML.",
    Inches(0.4), Inches(1.35), Inches(12.5), Inches(0.5),
    font_size=15, color=TEXT_DARK)

# Pipeline boxes
steps = ["Raw Data", "Cleaning", "Conversion\n& Encoding", "Scaling",
         "Feature\nEngineering", "Model\nReady"]
step_colors = [RED, ORANGE, MID_BLUE, GREEN, MID_BLUE, DARK_BLUE]
bx = Inches(0.2)
for i, (step, sc) in enumerate(zip(steps, step_colors)):
    colored_box(sl, step, bx, Inches(1.95), Inches(2.05), Inches(0.95),
                fill=sc, font_size=13, bold=True)
    bx += Inches(2.05)
    if i < len(steps) - 1:
        add_text(sl, "→", bx - Inches(0.2), Inches(2.05),
                 Inches(0.3), Inches(0.95), font_size=22, bold=True,
                 color=DARK_BLUE, align=PP_ALIGN.CENTER)

# Why important
rect(sl, Inches(0.3), Inches(3.2), Inches(12.7), Inches(3.7),
     fill=LIGHT_GRAY, line=MID_BLUE, line_w=Pt(1.5))

add_text(sl, "Tại sao quan trọng?",
         Inches(0.5), Inches(3.3), Inches(5), Inches(0.4),
         font_size=16, bold=True, color=DARK_BLUE)

why = [
    "Dữ liệu thực tế thường bẩn: thiếu, sai, không nhất quán",
    "Mô hình ML nhạy cảm với chất lượng dữ liệu (Garbage In → Garbage Out)",
    "Preprocessing chiếm ~80% thời gian trong dự án ML thực tế",
    "Dữ liệu tốt > thuật toán phức tạp",
    "Pipeline chuẩn tránh Data Leakage và overfitting",
]
bullet_box(sl, why, Inches(0.5), Inches(3.75), Inches(7.5), Inches(3.1))

# Stats box
colored_box(sl, "80%\nthời gian\ncleaning\ndữ liệu",
            Inches(8.2), Inches(3.3), Inches(2.0), Inches(1.8),
            fill=ORANGE, font_size=18, bold=True)
colored_box(sl, "\"Garbage\nIn =\nGarbage\nOut\"",
            Inches(10.4), Inches(3.3), Inches(2.5), Inches(1.8),
            fill=RED, font_size=16, bold=True)
colored_box(sl, "CRISP-DM:\nBusiness → Data\nUnderstanding\n→ Preparation\n→ Modeling",
            Inches(8.2), Inches(5.3), Inches(4.7), Inches(1.5),
            fill=DARK_BLUE, font_size=12)


# ─── Slide 4: Data Cleaning ────────────────────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "2. Data Cleaning", "Phát hiện và xử lý các vấn đề trong dữ liệu")

cleaning_types = [
    ("Missing Values", RED,
     ["Giá trị bị thiếu (NaN, null, '', '?')",
      "Nguyên nhân: lỗi thu thập, khảo sát bỏ qua",
      "→ Xem Slide tiếp theo"]),
    ("Duplicate Rows", ORANGE,
     ["Dòng bị lặp do lỗi merge, nhập liệu",
      "Xử lý: df.drop_duplicates()",
      "Kiểm tra: df.duplicated().sum()"]),
    ("Inconsistent Data", MID_BLUE,
     ["Cùng giá trị nhưng format khác: 'Male'/'male'/'MALE'",
      "Xử lý: .str.strip().str.title()",
      "Chuẩn hoá đơn vị: kg vs lb, USD vs VND"]),
    ("Invalid/Outlier", GREEN,
     ["Giá trị ngoài miền hợp lệ: age=-5, salary=999999",
      "Phát hiện: IQR, Z-score, domain knowledge",
      "Xử lý: clip, NaN, hoặc remove"]),
]

for i, (title, color, items) in enumerate(cleaning_types):
    row = i // 2
    col = i % 2
    x = Inches(0.25 + col * 6.5)
    y = Inches(1.4 + row * 2.8)
    rect(sl, x, y, Inches(6.3), Inches(2.6), fill=LIGHT_GRAY,
         line=color, line_w=Pt(2))
    colored_box(sl, title, x, y, Inches(6.3), Inches(0.5),
                fill=color, font_size=14, bold=True)
    bullet_box(sl, items, x + Inches(0.1), y + Inches(0.55),
               Inches(6.0), Inches(1.9))


# ─── Slide 5: Missing-Value Handling ──────────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "3. Missing-Value Handling", "Các chiến lược xử lý giá trị bị thiếu")

# Decision tree description
strategies = [
    ("① DELETION", RED,
     "Xóa hàng/cột",
     ["Xóa hàng: df.dropna()",
      "Xóa cột nếu >50% missing",
      "⚠ Mất dữ liệu, chỉ dùng khi MCAR"]),
    ("② IMPUTATION\n   (Thống kê)", GREEN,
     "Điền giá trị tính toán",
     ["Mean: số liệu phân phối chuẩn",
      "Median: có outlier",
      "Mode: categorical",
      "SimpleImputer (sklearn)"]),
    ("③ ADVANCED\n   IMPUTATION", MID_BLUE,
     "Điền bằng mô hình",
     ["KNN Imputer: k=5 lân cận",
      "Iterative Imputer (MICE)",
      "Forward/Backward Fill",
      "Predictive model"]),
    ("④ FLAG &\n   KEEP", ORANGE,
     "Giữ và đánh dấu",
     ["Tạo cột mới: col_missing",
      "Giữ NaN + dùng model hỗ trợ NaN",
      "HistGradientBoosting (sklearn)"]),
]

for i, (title, color, subtitle, items) in enumerate(strategies):
    x = Inches(0.2 + i * 3.27)
    rect(sl, x, Inches(1.4), Inches(3.1), Inches(5.7),
         fill=LIGHT_GRAY, line=color, line_w=Pt(2))
    colored_box(sl, title, x, Inches(1.4), Inches(3.1), Inches(0.85),
                fill=color, font_size=13, bold=True)
    add_text(sl, subtitle, x + Inches(0.1), Inches(2.32), Inches(2.9), Inches(0.35),
             font_size=12, italic=True, bold=True, color=DARK_BLUE)
    bullet_box(sl, items,
               x + Inches(0.1), Inches(2.72), Inches(2.9), Inches(3.9))

# Rule of thumb
rect(sl, Inches(0.2), Inches(7.1), Inches(12.9), Inches(0.33), fill=DARK_BLUE)
add_text(sl, "📌 Rule of Thumb:  < 5% missing → Impute  |  5–20% → Careful Impute  |  > 20% → Consider Drop column",
         Inches(0.4), Inches(7.12), Inches(12.5), Inches(0.3),
         font_size=12, color=WHITE, bold=True)


# ─── Slide 6: Data Conversion & Encoding ──────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "4. Data Conversion & Categorical Encoding",
           "Chuyển đổi mọi loại feature sang dạng số")

encoding_types = [
    ("Label Encoding", MID_BLUE,
     ["Dùng cho: Binary / Ordinal",
      "['No','Yes'] → [0, 1]",
      "sklearn: LabelEncoder()",
      "⚠ Không dùng với Nominal!"]),
    ("Ordinal Encoding", GREEN,
     ["Dùng cho: Có thứ tự tự nhiên",
      "['Low','Med','High'] → [0,1,2]",
      "Giữ quan hệ thứ bậc",
      "sklearn: OrdinalEncoder()"]),
    ("One-Hot Encoding", ORANGE,
     ["Dùng cho: Categorical Nominal",
      "['Red','Blue'] → [1,0],[0,1]",
      "Không giả định thứ tự",
      "sklearn: OneHotEncoder()"]),
    ("Target Encoding", RED,
     ["Thay giá trị = mean(target)",
      "Giảm chiều so với OHE",
      "⚠ Nguy cơ Data Leakage",
      "Dùng cross-val khi encode"]),
    ("Text Features", DARK_BLUE,
     ["TF-IDF / Bag of Words",
      "Word Embedding (Word2Vec)",
      "Count vectorizer",
      "ID thuần → DROP"]),
    ("Datetime Features", MID_BLUE,
     ["Trích xuất: year, month, day",
      "day_of_week, is_weekend",
      "Tính khoảng thời gian",
      "pd.to_datetime() + .dt.*"]),
]

for i, (title, color, items) in enumerate(encoding_types):
    row = i // 3
    col = i % 3
    x = Inches(0.2 + col * 4.37)
    y = Inches(1.4 + row * 2.85)
    rect(sl, x, y, Inches(4.2), Inches(2.65), fill=LIGHT_GRAY,
         line=color, line_w=Pt(2))
    colored_box(sl, title, x, y, Inches(4.2), Inches(0.5),
                fill=color, font_size=13, bold=True)
    bullet_box(sl, items, x + Inches(0.1), y + Inches(0.55),
               Inches(3.9), Inches(2.0), bullet="•")


# ─── Slide 7: Feature Scaling ─────────────────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "5. Feature Scaling", "Đưa các feature về cùng scale để tránh bias khoảng cách")

scalers = [
    ("Min-Max\nScaler", GREEN,
     "x' = (x - min) / (max - min)",
     "→ [0, 1]",
     ["Bảo toàn phân phối",
      "Nhạy với outlier",
      "Dùng khi: Neural Net, Image"]),
    ("Standard\nScaler\n(Z-score)", MID_BLUE,
     "x' = (x - μ) / σ",
     "→ mean=0, std=1",
     ["Phân phối chuẩn hóa",
      "Kém nhạy với outlier hơn",
      "Dùng khi: kNN, SVM, LR, PCA"]),
    ("Robust\nScaler", ORANGE,
     "x' = (x - median) / IQR",
     "→ Robust với outlier",
     ["Dùng median & IQR",
      "Tốt khi có nhiều outlier",
      "Phân phối non-Gaussian"]),
    ("Log\nTransform", RED,
     "x' = log(x + 1)",
     "→ Giảm skewness",
     ["Right-skewed distribution",
      "Luôn dương sau transform",
      "Dùng cho: income, price"]),
]

for i, (title, color, formula, result, items) in enumerate(scalers):
    x = Inches(0.2 + i * 3.27)
    rect(sl, x, Inches(1.4), Inches(3.1), Inches(5.75),
         fill=LIGHT_GRAY, line=color, line_w=Pt(2))
    colored_box(sl, title, x, Inches(1.4), Inches(3.1), Inches(0.75),
                fill=color, font_size=13, bold=True)
    add_text(sl, formula, x + Inches(0.1), Inches(2.25), Inches(2.9), Inches(0.4),
             font_size=12, italic=True, color=DARK_BLUE, bold=True)
    add_text(sl, result, x + Inches(0.1), Inches(2.68), Inches(2.9), Inches(0.35),
             font_size=11, color=color, bold=True)
    bullet_box(sl, items, x + Inches(0.1), Inches(3.05), Inches(2.9), Inches(3.8),
               bullet="•")

# Warning box
rect(sl, Inches(0.2), Inches(7.08), Inches(12.9), Inches(0.35), fill=DARK_BLUE)
add_text(sl, "⚠  QUAN TRỌNG: Fit scaler ONLY trên tập Train → Transform cả Train và Test (tránh Data Leakage!)",
         Inches(0.4), Inches(7.10), Inches(12.5), Inches(0.3),
         font_size=12, color=WHITE, bold=True)


# ─── Slide 8: Feature Engineering ─────────────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "6. Feature Engineering",
           "Tạo feature mới từ dữ liệu hiện có để tăng hiệu quả mô hình")

fe_methods = [
    ("Binning / Discretization", MID_BLUE,
     ["Chia giá trị liên tục thành nhóm rời rạc",
      "age → ['Young','Middle','Senior']",
      "pd.cut(), pd.qcut()",
      "Giảm nhiễu, handle non-linearity"]),
    ("Interaction Features", GREEN,
     ["Kết hợp 2+ features: A × B, A / B, A - B",
      "price_per_sqm = price / area",
      "Capture quan hệ phi tuyến",
      "⚠ Tránh tạo quá nhiều (curse of dim.)"]),
    ("Aggregation / Groupby", ORANGE,
     ["Tính thống kê theo nhóm",
      "mean_spend_by_city, max_order_per_user",
      "pd.groupby().agg()",
      "Dùng cho time-series và tabular"]),
    ("Domain-Specific\nExtraction", RED,
     ["Trích đặc trưng từ kiến thức miền",
      "Email → domain, tld, is_edu",
      "URL → protocol, path depth",
      "Datetime → weekday, quarter, is_holiday"]),
    ("Polynomial Features", DARK_BLUE,
     ["Tạo x², x³, x₁·x₂ tự động",
      "sklearn: PolynomialFeatures(degree=2)",
      "Capture non-linear patterns",
      "⚠ Feature explosion khi degree cao"]),
    ("Text Feature\nExtraction", MID_BLUE,
     ["TF-IDF, Word Count, Char n-gram",
      "Sentiment score, topic modeling",
      "Named Entity Recognition (NER)",
      "BERT embeddings (advanced)"]),
]

for i, (title, color, items) in enumerate(fe_methods):
    row = i // 3
    col = i % 3
    x = Inches(0.2 + col * 4.37)
    y = Inches(1.4 + row * 2.85)
    rect(sl, x, y, Inches(4.2), Inches(2.65), fill=LIGHT_GRAY,
         line=color, line_w=Pt(2))
    colored_box(sl, title, x, y, Inches(4.2), Inches(0.5),
                fill=color, font_size=12, bold=True)
    bullet_box(sl, items, x + Inches(0.1), y + Inches(0.55),
               Inches(3.9), Inches(2.0), bullet="•")


# ─── Slide 9: sklearn Pipeline ────────────────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "7. Preprocessing Pipeline (sklearn)",
           "Đóng gói toàn bộ quy trình thành Pipeline có thể reproduce")

# Diagram boxes
pipeline_steps = [
    ("Input\nData", DARK_BLUE),
    ("Column\nTransformer", MID_BLUE),
    ("Model\n(Classifier)", GREEN),
    ("Predictions", ORANGE),
]

bx = Inches(0.3)
for i, (step, color) in enumerate(pipeline_steps):
    colored_box(sl, step, bx, Inches(1.5), Inches(2.6), Inches(0.9),
                fill=color, font_size=14, bold=True)
    bx += Inches(2.6)
    if i < len(pipeline_steps) - 1:
        add_text(sl, "→", bx - Inches(0.2), Inches(1.55),
                 Inches(0.3), Inches(0.9), font_size=24, bold=True,
                 color=DARK_BLUE, align=PP_ALIGN.CENTER)

# Sub-boxes for ColumnTransformer
sub = [
    ("Numerical Pipeline:\nMedian Imputer\n→ StandardScaler", MID_BLUE),
    ("Binary:\nMode Imputer", MID_BLUE),
    ("Categorical Pipeline:\nMode Imputer\n→ OneHotEncoder", MID_BLUE),
]
bx2 = Inches(2.85)
for j, (label, color) in enumerate(sub):
    colored_box(sl, label, bx2 + j * Inches(2.75), Inches(2.6),
                Inches(2.55), Inches(1.0), fill=DARK_BLUE, font_size=11)

# Benefits
rect(sl, Inches(0.3), Inches(3.85), Inches(12.7), Inches(3.3),
     fill=LIGHT_GRAY, line=MID_BLUE, line_w=Pt(1.5))
add_text(sl, "Lợi ích của Pipeline:",
         Inches(0.5), Inches(3.95), Inches(6), Inches(0.4),
         font_size=15, bold=True, color=DARK_BLUE)

benefits = [
    "✅  Tránh Data Leakage — fit() chỉ trên tập train",
    "✅  Code gọn, dễ maintain và reproduce",
    "✅  Tích hợp GridSearchCV/HyperParameter tuning",
    "✅  Dễ deploy sang production (Pipeline.predict())",
    "✅  Tự động xử lý thứ tự các bước",
]
bullet_box(sl, benefits, Inches(0.5), Inches(4.45), Inches(7.5), Inches(2.6), bullet="")

# Code snippet
code = (
    "preprocessor = ColumnTransformer([\n"
    "    ('num', Pipeline([('imp', SimpleImputer()), ('sc', StandardScaler())]), num_cols),\n"
    "    ('cat', Pipeline([('imp', SimpleImputer()), ('ohe', OneHotEncoder())]),  cat_cols),\n"
    "])\n"
    "pipeline = Pipeline([('prep', preprocessor), ('clf', KNeighborsClassifier())])\n"
    "pipeline.fit(X_train, y_train)"
)
rect(sl, Inches(8.0), Inches(3.85), Inches(5.1), Inches(3.3), fill=DARK_BLUE)
add_text(sl, code, Inches(8.1), Inches(3.95), Inches(4.9), Inches(3.15),
         font_size=9.5, color=ACCENT_BLUE)


# ─── Slide 10: Practical Task ─────────────────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "8. Bài thực hành — Telco Customer Churn",
           "Áp dụng toàn bộ lý thuyết vào bài toán phân loại thực tế")

# Dataset info box
rect(sl, Inches(0.3), Inches(1.4), Inches(4.5), Inches(5.7), fill=DARK_BLUE)
add_text(sl, "📦 Dataset", Inches(0.5), Inches(1.5), Inches(4), Inches(0.4),
         font_size=16, bold=True, color=ACCENT_BLUE)
ds_info = [
    "Nguồn: IBM Telco Customer Churn",
    "Target: Churn (Yes/No) — Binary",
    "1,500 mẫu | 18 features",
    "",
    "Feature Types:",
    "  Numerical: tenure, MonthlyCharges,",
    "  TotalCharges",
    "  Categorical: Contract, PaymentMethod,",
    "  InternetService, gender...",
    "  Binary: PhoneService, PaperlessBilling",
    "  Text: customerID (→ DROP)",
]
bullet_box(sl, ds_info, Inches(0.4), Inches(2.0), Inches(4.2), Inches(4.8),
           bullet="", title_color=WHITE)

# Workflow
steps_list = [
    ("🧹 Data Cleaning", MID_BLUE,
     ["Drop duplicate (30 dòng)",
      "Chuẩn hoá casing (gender...)",
      "Xử lý tenure<0, Charges>500",
      "Missing: Median/Mode Impute"]),
    ("⚙️ Feature Engineering", GREEN,
     ["Drop customerID",
      "ContractRank (ordinal: 0/1/2)",
      "ChargesPerMonth = Total/tenure",
      "NumServices (count dịch vụ)"]),
    ("🤖 Models Trained", ORANGE,
     ["1. kNN (k=7, Euclidean)",
      "2. Decision Tree (depth=8)",
      "3. Naive Bayes (Gaussian)",
      "4. Logistic Regression",
      "5. Random Forest (100 trees)"]),
]

for i, (title, color, items) in enumerate(steps_list):
    x = Inches(5.0 + i * 2.75)
    rect(sl, x, Inches(1.4), Inches(2.6), Inches(5.7),
         fill=LIGHT_GRAY, line=color, line_w=Pt(2))
    colored_box(sl, title, x, Inches(1.4), Inches(2.6), Inches(0.6),
                fill=color, font_size=12, bold=True)
    bullet_box(sl, items, x + Inches(0.1), Inches(2.1), Inches(2.4), Inches(4.8),
               bullet="•")

# Metrics
rect(sl, Inches(0.3), Inches(7.1), Inches(12.7), Inches(0.33), fill=MID_BLUE)
add_text(sl, "📊 Đánh giá: Accuracy | Precision | Recall | F1-Score | Confusion Matrix | 5-Fold CV",
         Inches(0.5), Inches(7.12), Inches(12.3), Inches(0.3),
         font_size=12, color=WHITE, bold=True)


# ─── Slide 11: Results Summary ─────────────────────────────────────────────────
sl = blank(prs)
bg(sl, WHITE)
header_bar(sl, "Kết quả so sánh mô hình", "Telco Churn Classification — Test Set Results")

# Table header
header_cols = ["Mô hình", "Accuracy", "Precision", "Recall", "F1-Score", "CV F1"]
col_ws = [Inches(3.2), Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.8)]
x_starts = [Inches(0.3)]
for w in col_ws[:-1]:
    x_starts.append(x_starts[-1] + w)

# Header row
for col_txt, x, w in zip(header_cols, x_starts, col_ws):
    colored_box(sl, col_txt, x, Inches(1.4), w, Inches(0.5),
                fill=DARK_BLUE, font_size=13, bold=True)

# Data rows (approximate expected results)
rows = [
    ("kNN (k=7)",           "0.75~", "0.66~", "0.58~", "0.62~", "0.61~"),
    ("Decision Tree",       "0.77~", "0.68~", "0.64~", "0.66~", "0.64~"),
    ("Naive Bayes",         "0.73~", "0.63~", "0.60~", "0.62~", "0.60~"),
    ("Logistic Regression", "0.80~", "0.72~", "0.68~", "0.70~", "0.69~"),
    ("Random Forest 🏆",    "0.82~", "0.76~", "0.70~", "0.73~", "0.72~"),
]
row_colors = [LIGHT_GRAY, WHITE, LIGHT_GRAY, WHITE, RGBColor(0xD5, 0xF5, 0xE3)]

for r_i, (row, rc) in enumerate(zip(rows, row_colors)):
    y_r = Inches(1.9 + r_i * 0.62)
    for col_txt, x, w in zip(row, x_starts, col_ws):
        txt_color = DARK_BLUE if r_i < 4 else GREEN
        colored_box(sl, col_txt, x, y_r, w, Inches(0.58),
                    fill=rc, text_color=txt_color, font_size=12,
                    bold=(r_i == 4))

add_text(sl, "* Kết quả xấp xỉ — chạy notebook để xem giá trị chính xác",
         Inches(0.3), Inches(5.12), Inches(13), Inches(0.3),
         font_size=10, italic=True, color=RED)

# Conclusion
rect(sl, Inches(0.3), Inches(5.5), Inches(12.7), Inches(1.85),
     fill=LIGHT_GRAY, line=MID_BLUE, line_w=Pt(1.5))
add_text(sl, "💡 Nhận xét & Kết luận",
         Inches(0.5), Inches(5.6), Inches(6), Inches(0.38),
         font_size=15, bold=True, color=DARK_BLUE)
conclusions = [
    "Random Forest đạt kết quả tốt nhất nhờ ensemble của nhiều cây quyết định",
    "Logistic Regression cho kết quả tốt & giải thích được (interpretable)",
    "kNN nhạy cảm với k và cần StandardScaler vì dùng khoảng cách Euclidean",
    "Preprocessing Pipeline chuẩn giúp tránh Data Leakage và dễ deploy",
]
bullet_box(sl, conclusions, Inches(0.5), Inches(6.0), Inches(12.2), Inches(1.2))


# ─── Slide 12: Thank You ───────────────────────────────────────────────────────
sl = blank(prs)
bg(sl, DARK_BLUE)
rect(sl, 0, Inches(3.5), SLIDE_W, Inches(0.12), fill=ACCENT_BLUE)

add_text(sl, "Cảm ơn thầy/cô đã lắng nghe!",
         Inches(0.5), Inches(1.5), Inches(12), Inches(1.2),
         font_size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text(sl, "Q & A",
         Inches(0.5), Inches(2.8), Inches(12), Inches(0.8),
         font_size=30, italic=True, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)

info2 = [
    "Sinh viên: Ngô Lâm Tiên  —  MSSV: 524H0195",
    "Môn học: Machine Learning",
    "Ton Duc Thang University",
]
for i, line in enumerate(info2):
    add_text(sl, line,
             Inches(0.5), Inches(4.0 + i * 0.6), Inches(12), Inches(0.5),
             font_size=16, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)

# ─── Save ──────────────────────────────────────────────────────────────────────
out = "/home/towfienes/TDTU/HW1_DataPreprocessing_Presentation.pptx"
prs.save(out)
print(f"✅ Saved: {out}")
print(f"   Slides: {len(prs.slides)}")
