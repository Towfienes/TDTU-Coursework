"""
Software Engineering — Class Activity — User Tasks & Quality Attributes (Feb 2025)
Authors:
- 524H0195: Ngô Lâm Tiên
- 524H0191: Nguyễn Công Thành
Ton Duc Thang University (TDTU) - Faculty of Information Technology
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ─── Color Palette ────────────────────────────────────────────────────────────
DARK_NAVY   = RGBColor(0x0F, 0x1E, 0x36)   # #0F1E36 - Deep Navy
PRIMARY_BLUE= RGBColor(0x1A, 0x35, 0x5E)   # #1A355E - Brand Primary
MID_BLUE    = RGBColor(0x25, 0x63, 0xEB)   # #2563EB - Royal Blue
ACCENT_BLUE = RGBColor(0x38, 0xBD, 0xF8)   # #38BDF8 - Sky Accent
CYAN_ACCENT = RGBColor(0x06, 0xB6, 0xD4)   # #06B6D4 - Secondary Accent
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BG     = RGBColor(0xF8, 0xFA, 0xFC)   # #F8FAFC - Clean Card Slate
CARD_ALT_BG = RGBColor(0xF1, 0xF5, 0xF9)   # #F1F5F9 - Slightly deeper card
BORDER_GRAY = RGBColor(0xE2, 0xE8, 0xF0)   # #E2E8F0 - Clean Card Border
TEXT_MAIN   = RGBColor(0x0F, 0x17, 0x2A)   # #0F172A - Deep Slate Black
TEXT_MUTED  = RGBColor(0x47, 0x55, 0x69)   # #475569 - Muted Subtitle
EMERALD     = RGBColor(0x05, 0x96, 0x69)   # #059669 - Positive / Success
AMBER       = RGBColor(0xD9, 0x77, 0x06)   # #D97706 - Warning / Attention
ROSE        = RGBColor(0xDC, 0x26, 0x26)   # #DC2626 - Alert / Contrast
PURPLE      = RGBColor(0x7C, 0x3A, 0xED)   # #7C3AED - Accent Category

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def create_presentation():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def add_blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def add_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=Pt(1)):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape


def add_rounded_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=Pt(1)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape


def add_header(slide, title, category=None):
    add_rect(slide, 0, 0, SLIDE_W, Inches(1.15), fill_color=DARK_NAVY, line_color=None)
    add_rect(slide, 0, Inches(1.12), SLIDE_W, Inches(0.04), fill_color=MID_BLUE, line_color=None)
    
    txb = slide.shapes.add_textbox(Inches(0.6), Inches(0.12), Inches(12.13), Inches(0.95))
    tf = txb.text_frame
    tf.word_wrap = True
    
    if category:
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = category.upper()
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = ACCENT_BLUE
        
        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = title
        r1.font.size = Pt(22)
        r1.font.bold = True
        r1.font.color.rgb = WHITE
    else:
        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = title
        r0.font.size = Pt(24)
        r0.font.bold = True
        r0.font.color.rgb = WHITE


def add_card(slide, left, top, width, height, title=None, title_color=PRIMARY_BLUE, bg_color=CARD_BG, border_color=BORDER_GRAY):
    card_shape = add_rounded_rect(slide, left, top, width, height, fill_color=bg_color, line_color=border_color, line_width=Pt(1.2))
    if title:
        txb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.35))
        tf = txb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = title_color
    return card_shape


def add_bullet_list(slide, left, top, width, height, items, font_size=12, bullet="•", text_color=TEXT_MAIN, space_before=Pt(3)):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf = txb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.space_before = space_before
        run = p.add_run()
        if isinstance(item, tuple):
            prefix, body = item
            r_pre = run
            r_pre.text = f"{bullet} {prefix}: "
            r_pre.font.bold = True
            r_pre.font.size = Pt(font_size)
            r_pre.font.color.rgb = PRIMARY_BLUE
            
            r_bod = p.add_run()
            r_bod.text = body
            r_bod.font.size = Pt(font_size)
            r_bod.font.color.rgb = text_color
        else:
            run.text = f"{bullet}  {item}"
            run.font.size = Pt(font_size)
            run.font.color.rgb = text_color


def add_table_grid(slide, left, top, width, height, headers, rows, col_widths=None, font_size=11):
    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    tbl = table_shape.table
    
    if col_widths:
        for idx, w in enumerate(col_widths):
            tbl.columns[idx].width = w
            
    # Style Header
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        cell.text_frame.word_wrap = True
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = str(h_text)
        r.font.bold = True
        r.font.size = Pt(font_size + 1)
        r.font.color.rgb = WHITE
        
    # Style Rows
    for r_idx, row in enumerate(rows):
        bg = CARD_BG if r_idx % 2 == 0 else CARD_ALT_BG
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.text_frame.word_wrap = True
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(font_size)
            r.font.color.rgb = TEXT_MAIN


# ==============================================================================
# SLIDE BUILDERS
# ==============================================================================

def build_slide_1_cover(prs):
    slide = add_blank_slide(prs)
    # Background full navy
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill_color=DARK_NAVY, line_color=None)
    # Accent top-right and bottom-left shapes
    add_rect(slide, Inches(10), 0, Inches(3.333), Inches(0.15), fill_color=MID_BLUE, line_color=None)
    add_rect(slide, 0, Inches(7.35), Inches(5), Inches(0.15), fill_color=CYAN_ACCENT, line_color=None)
    
    # Subject badge
    add_rounded_rect(slide, Inches(1.0), Inches(1.2), Inches(5.2), Inches(0.55), fill_color=RGBColor(0x1E, 0x29, 0x3B), line_color=MID_BLUE)
    tx_sub = slide.shapes.add_textbox(Inches(1.15), Inches(1.25), Inches(5.0), Inches(0.4))
    r_sub = tx_sub.text_frame.paragraphs[0].add_run()
    r_sub.text = "TON DUC THANG UNIVERSITY • SOFTWARE ENGINEERING"
    r_sub.font.bold = True
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = ACCENT_BLUE

    # Title & Subtitle
    tx_t = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(2.2))
    tf_t = tx_t.text_frame
    tf_t.word_wrap = True
    
    p1 = tf_t.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Tutorial 1 — User Tasks & Quality Attributes"
    r1.font.bold = True
    r1.font.size = Pt(36)
    r1.font.color.rgb = WHITE
    
    p2 = tf_t.add_paragraph()
    p2.space_before = Pt(8)
    r2 = p2.add_run()
    r2.text = "Hotel Information System Requirements, Task & Support Analysis & Architectural Quality Attributes"
    r2.font.size = Pt(18)
    r2.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # Authors Card Container
    add_rounded_rect(slide, Inches(1.0), Inches(4.5), Inches(11.3), Inches(2.1), fill_color=RGBColor(0x13, 0x23, 0x3D), line_color=MID_BLUE, line_width=Pt(1.5))
    
    tx_a = slide.shapes.add_textbox(Inches(1.3), Inches(4.65), Inches(10.7), Inches(1.8))
    tf_a = tx_a.text_frame
    tf_a.word_wrap = True
    
    p_h = tf_a.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = "NHÓM THỰC HIỆN BÀI TẬP (GROUP MEMBERS):"
    r_h.font.bold = True
    r_h.font.size = Pt(13)
    r_h.font.color.rgb = CYAN_ACCENT
    
    p_m1 = tf_a.add_paragraph()
    p_m1.space_before = Pt(8)
    r_m1 = p_m1.add_run()
    r_m1.text = "1. 524H0195 — Ngô Lâm Tiên"
    r_m1.font.bold = True
    r_m1.font.size = Pt(18)
    r_m1.font.color.rgb = WHITE
    
    p_m2 = tf_a.add_paragraph()
    p_m2.space_before = Pt(4)
    r_m2 = p_m2.add_run()
    r_m2.text = "2. 524H0191 — Nguyễn Công Thành"
    r_m2.font.bold = True
    r_m2.font.size = Pt(18)
    r_m2.font.color.rgb = WHITE


def build_slide_2_agenda(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Tổng Quan Nội Dung Báo Cáo (Agenda)", "Executive Summary")
    
    # Left Card: Part 1
    add_card(slide, Inches(0.6), Inches(1.4), Inches(5.85), Inches(5.6), "PART 1: HOTEL INFORMATION SYSTEM (HIS)", PRIMARY_BLUE)
    part1_items = [
        ("Câu 1", "Mô tả tác vụ Check-Out theo phong cách Task & Support (Soren Lauesen)."),
        ("Câu 2", "Xác định 6 tác vụ điển hình của HIS và vẽ luồng công việc (End-to-End Workflow)."),
        ("Câu 3", "Định nghĩa Yêu cầu ngầm định (Tacit Requirements) và phương pháp thẩm định (Validation)."),
        ("Câu 5", "Phân tích khiếm khuyết của Domain Model mẫu & Mở rộng mô hình miền (Room Type, Overbooking)."),
        ("Câu 6", "Phân rã tác vụ Check-In: Khách đã đặt (Booked) vs Khách vãng lai (Walk-In)."),
        ("Câu 7", "Mở rộng tác vụ Check-In xử lý tình huống khẩn cấp vượt hạn mức phòng (Overbooking Crisis).")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.0), Inches(5.45), Inches(4.8), part1_items, font_size=12, bullet="🔹")

    # Right Card: Part 2
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.85), Inches(5.6), "PART 2: SOFTWARE QUALITY ATTRIBUTES", MID_BLUE)
    part2_items = [
        ("Câu 1", "Hệ thống các thuộc tính chất lượng phần mềm tổng quát (ISO/IEC 25010 & Architecture)."),
        ("Câu 2", "Các hình thức mở rộng quy mô (Scalability: Vertical, Horizontal, Structural, Geo...)."),
        ("Câu 3", "Phân tích Thông lượng (Throughput): So sánh Thông lượng trung bình vs Thông lượng đỉnh."),
        ("Câu 4", "Mối quan hệ đánh đổi giữa An ninh (Security: AuthN & AuthZ) và Tính khả dụng (Availability)."),
        ("Câu 5a-b", "Yêu cầu chất lượng cho Check-In & Check-Out: Điểm tương đồng và khác biệt cốt lõi."),
        ("Câu 5c-d", "Đặc tả yêu cầu chất lượng có thể kiểm chứng (Verifiable Scenarios) & Top 5 thuộc tính cho HIS.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(2.0), Inches(5.45), Inches(4.8), part2_items, font_size=12, bullet="🔸")


def build_slide_3_checkout_task(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 1: Tác Vụ Check-Out (Task & Support Style)", "Hotel Information System")
    
    # Top Meta Card
    add_card(slide, Inches(0.6), Inches(1.3), Inches(12.13), Inches(1.2), "TASK 1.3: CHECKOUT (TRẢ PHÒNG & QUYẾT TOÁN)", PRIMARY_BLUE)
    meta_items = [
        ("Mục đích (Purpose)", "Giải phóng phòng, thanh toán toàn bộ chi phí khách lưu trú, khóa tài khoản phòng, tiễn khách."),
        ("Kích hoạt (Trigger)", "Khách yêu cầu trả phòng tại quầy lễ tân hoặc thao tác trên Kiosk tự phục vụ."),
        ("Tần suất & Tới hạn", "Trung bình ~0.5 lượt/phòng/ngày; Cao điểm 07:00–11:00 AM (đoàn 30–50 khách trả phòng cùng lúc; cổng thanh toán thẻ bị nghẽn).")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.8), meta_items, font_size=11, bullet="📌")

    # Main Task & Support Table
    headers = ["Sub-tasks (Tác vụ con) & Vấn đề (Problems)", "Example Solution (Hệ thống máy tính hỗ trợ)"]
    rows = [
        ["1. Xác định phòng & khách hàng\n- Vấn đề: Khách quên số phòng, phát âm tên khó tìm.",
         "Hệ thống hỗ trợ quét thẻ từ phòng, tìm theo Tên khách, Số CCCD/Hộ chiếu hoặc Số điện thoại. Hiển thị tức thì thông tin đặt phòng."],
        ["2. Tổng hợp chi phí dịch vụ phát sinh\n- Vấn đề: Phí minibar, ăn sáng phút chót chưa kịp ghi sổ.",
         "Đồng bộ thời gian thực từ POS Nhà hàng, Spa. Nhân viên buồng phòng kiểm tra minibar gửi số liệu trực tiếp qua Mobile App lên PMS."],
        ["3. Xem xét hóa đơn & Xử lý khiếu nại\n- Vấn đề: Khách thắc mắc chi phí, yêu cầu tách hóa đơn công ty.",
         "Giao diện hiển thị chi tiết từng dòng; hỗ trợ Tách hóa đơn (Tiền phòng về Công ty, Chi phí cá nhân khách tự trả); áp dụng Voucher/Giảm giá."],
        ["4. Quyết toán thanh toán\n- Vấn đề: Thẻ bị từ chối, trả một phần tiền mặt một phần thẻ.",
         "Tích hợp cổng POS thanh toán đa phương thức (Thẻ, Chuyển khoản VietQR, Tiền mặt). Tự động in hóa đơn VAT điện tử & gửi email."],
        ["5. Trả phòng & Đổi trạng thái phòng\n- Vấn đề: Quên báo Buồng phòng, cấp nhầm phòng chưa dọn.",
         "Hủy kích hoạt mã thẻ từ phòng. Hệ thống tự động chuyển trạng thái phòng thành 'Trống / Cần dọn (Dirty)' và gửi lệnh dọn phòng ngay."]
    ]
    add_table_grid(slide, Inches(0.6), Inches(2.6), Inches(12.13), Inches(4.5), headers, rows, [Inches(5.0), Inches(7.13)], font_size=10)


def build_slide_4_his_tasks(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 2: Các Tác Vụ Điển Hình Của Hệ Thống Khách Sạn", "Hotel Information System")
    
    # 6 Core Tasks Grid (2 rows x 3 columns)
    tasks = [
        ("1. Đặt phòng (Book Guest)", "Quản lý giữ chỗ, kiểm tra số lượng phòng trống theo loại phòng (RoomType), lưu thông tin đặt cọc và chính sách hủy phòng.", PRIMARY_BLUE),
        ("2. Nhận phòng (Check-In)", "Đối chiếu thông tin đặt phòng, phân bổ số phòng vật lý sạch, ghi nhận giấy tờ tùy thân, ký quỹ và kích hoạt thẻ từ.", EMERALD),
        ("3. Quản lý lưu trú & Dịch vụ", "Chuyển phòng khi khách yêu cầu, ghi nhận chi phí ăn uống, giặt ủi, minibar, tổng hợp danh sách khách dùng buffet sáng.", MID_BLUE),
        ("4. Buồng phòng (Housekeeping)", "Theo dõi vòng đời phòng (Dirty → Cleaning → Inspected → Clean/Available). Quản lý phòng bảo trì, sửa chữa (Out-of-Order).", PURPLE),
        ("5. Trả phòng (Check-Out)", "Kiểm tra chi phí dịch vụ cuối cùng, giải quyết khiếu nại, quyết toán thanh toán, xuất hóa đơn tài chính và giải phóng phòng.", AMBER),
        ("6. Kiểm toán đêm (Night Audit)", "Chốt sổ doanh thu ngày, đóng giao dịch tài chính, kết chuyển dữ liệu công nợ sang Hệ thống Kế toán tổng hợp (Account System).", ROSE)
    ]
    
    card_w = Inches(3.85)
    card_h = Inches(2.6)
    xs = [Inches(0.6), Inches(4.74), Inches(8.88)]
    ys = [Inches(1.4), Inches(4.3)]
    
    for idx, (t_title, t_desc, color) in enumerate(tasks):
        gx = xs[idx % 3]
        gy = ys[idx // 3]
        add_card(slide, gx, gy, card_w, card_h, t_title, color)
        add_bullet_list(slide, gx + Inches(0.2), gy + Inches(0.6), card_w - Inches(0.4), card_h - Inches(0.7),
                        [t_desc], font_size=11, bullet="👉")


def build_slide_5_workflow(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 2: Trực Quan Hóa Luồng Công Việc (End-to-End Workflow)", "Workflow Architecture")
    
    # 5 Sequential Workflow Stages
    stages = [
        ("GIAI ĐOẠN 1: TRƯỚC LƯU TRÚ", "ĐẶT PHÒNG (RESERVATION)", 
         ["Khách gửi yêu cầu đặt phòng", "PMS kiểm tra RoomType Quota", "Ghi nhận cọc & Xác nhận Booking"], PRIMARY_BLUE),
        ("GIAI ĐOẠN 2: ĐẾN KHÁCH SẠN", "NHẬN PHÒNG (CHECK-IN)",
         ["Khách xuất trình Booking / CCCD", "Gán số phòng vật lý sạch (Clean)", "Tạo Stay, Quẹt cọc, Cấp thẻ từ"], EMERALD),
        ("GIAI ĐOẠN 3: TRONG LƯU TRÚ", "SỬ DỤNG DỊCH VỤ",
         ["Khách dùng Nhà hàng / Spa / Bar", "POS đẩy chi phí vào Tài khoản phòng", "Buồng phòng dọn dẹp định kỳ"], MID_BLUE),
        ("GIAI ĐOẠN 4: KẾT THÚC LƯU TRÚ", "TRẢ PHÒNG (CHECK-OUT)",
         ["Khách yêu cầu thanh toán hóa đơn", "Quyết toán (Thẻ/Tiền mặt) & In bill", "Thu hồi thẻ từ, Trả phòng (Dirty)"], AMBER),
        ("GIAI ĐOẠN 5: SAU TRẢ PHÒNG", "DỌN DẸP & KẾ TOÁN",
         ["Buồng phòng dọn & đổi sang Clean", "Night Audit chốt sổ doanh thu", "Đồng bộ Hệ thống Kế toán ngoài"], PURPLE)
    ]
    
    w_card = Inches(2.26)
    gap = Inches(0.20)
    for i, (stage_top, stage_name, steps, color) in enumerate(stages):
        x = Inches(0.6) + i * (w_card + gap)
        add_card(slide, x, Inches(1.4), w_card, Inches(5.6), stage_name, color)
        
        # Sub-header inside card
        txb_top = slide.shapes.add_textbox(x + Inches(0.1), Inches(1.5), w_card - Inches(0.2), Inches(0.35))
        r_top = txb_top.text_frame.paragraphs[0].add_run()
        r_top.text = stage_top
        r_top.font.bold = True
        r_top.font.size = Pt(8.5)
        r_top.font.color.rgb = color
        
        add_bullet_list(slide, x + Inches(0.12), Inches(2.4), w_card - Inches(0.24), Inches(4.3),
                        steps, font_size=10, bullet="➔")


def build_slide_6_tacit_req(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 3: Yêu Cầu Ngầm Định (Tacit Requirements) & Thẩm Định", "Requirements Engineering")
    
    # Left Card: Definition & Nature
    add_card(slide, Inches(0.6), Inches(1.4), Inches(5.85), Inches(5.6), "1. YÊU CẦU NGẦM ĐỊNH (TACIT REQUIREMENTS) LÀ GÌ?", PRIMARY_BLUE)
    p1_items = [
        ("Định nghĩa", "Là những yêu cầu, kỳ vọng mà người dùng coi là 'hiển nhiên phải có' (unstated obvious) dựa trên thói quen và kinh nghiệm làm việc, nên họ không chủ động nói ra trong các buổi phỏng vấn thu thập yêu cầu."),
        ("Bản chất", "Tồn tại dưới dạng tri thức ẩn (tacit knowledge); nếu thiếu, hệ thống vẫn 'đúng tính năng' trên giấy nhưng gây ức chế tột độ khi vận hành thực tế."),
        ("Ví dụ trong Hotel PMS", "Khi mất điện hoặc mạng chập chờn, dữ liệu nhập dở không được mất (Local Auto-save)."),
        ("Ví dụ về thời gian", "Thao tác Check-in không được mất quá 45 giây để tránh làm khách mệt mỏi sau chuyến bay dài."),
        ("Ví dụ về ca đêm", "Giao diện phải có phím tắt nhanh và cỡ chữ rõ ràng cho nhân viên trực ca đêm dễ thao tác.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.0), Inches(5.45), Inches(4.8), p1_items, font_size=11, bullet="💡")

    # Right Card: Validation Check Feasibility
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.85), Inches(5.6), "2. CÓ THỂ THẨM ĐỊNH (VALIDATION CHECK) ĐƯỢC KHÔNG?", EMERALD)
    p2_items = [
        ("Khả thi không?", "HOÀN TOÀN CÓ THỂ, nhưng KHÔNG THỂ chỉ đọc lướt tài liệu đặc tả bằng văn bản thông thường (vì vốn dĩ chúng không được ghi ra!)."),
        ("Phương pháp 1 — Quan sát thực địa (Shadowing)", "Kỹ sư phần mềm ngồi trực tiếp tại quầy lễ tân khách sạn để quan sát nhân viên xử lý khách hàng thực tế vào giờ cao điểm."),
        ("Phương pháp 2 — Làm mẫu thử (Prototyping)", "Giao bản mẫu giao diện tương tác (Interactive Mockup) cho người dùng trải nghiệm sớm; họ sẽ lập tức nhận ra thiếu sót ngầm."),
        ("Phương pháp 3 — Kịch bản đóng vai (Scenario Walkthrough)", "Diễn tập các tình huống éo le (mất mạng, khách VIP đòi đổi phòng, thẻ ngân hàng lỗi) để kích hoạt tri thức ẩn."),
        ("Phương pháp 4 — Bảng kiểm chuẩn ngành (Standard Checklists)", "Đối chiếu bộ tiêu chuẩn công nghiệp ngành khách sạn và tiêu chuẩn bảo mật thanh toán PCI-DSS quốc tế.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(2.0), Inches(5.45), Inches(4.8), p2_items, font_size=11, bullet="✅")


def build_slide_7_domain_flaws(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 5: Phân Tích Khiếm Khuyết Domain Model Mẫu", "Domain Modeling")
    
    # Left Card: Existing Model Structure
    add_card(slide, Inches(0.6), Inches(1.4), Inches(5.85), Inches(5.6), "MÔ HÌNH MIỀN CHO TRƯỚC (GIVEN MODEL)", ROSE)
    given_items = [
        ("Cấu trúc cho trước", "Guest (1) ── (1..*) Stay (1) ── (1..*) Room State (1) ── (1) Room"),
        ("Quan hệ dịch vụ", "Stay (1) ── (0..*) Service (1) ── (1) Service Type"),
        ("Ký hiệu sử dụng", "Mô hình thực thể miền phân tích (Domain Entity Model theo phong cách Soren Lauesen, ký hiệu thực thể và liên kết dạng crow's foot/UML)."),
        ("Tình trạng", "Mô hình này QUÁ SƠ SÀI VÀ THIẾU NHIỀU THỰC THỂ CỐT LÕI của một khách sạn thực tế.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.0), Inches(5.45), Inches(4.8), given_items, font_size=12, bullet="⚠️")

    # Right Card: Missing Aspects
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.85), Inches(5.6), "4 KHIẾM KHUYẾT CỐT LÕI CẦN BỔ SUNG", AMBER)
    flaws = [
        ("1. Thiếu Loại phòng (Room Type)", "Khách sạn quản lý phòng theo Loại (Single, Double, Suite, Deluxe) với đơn giá và sức chứa khác nhau, không quản lý đặt trước theo từng số phòng cụ thể."),
        ("2. Thiếu Thực thể Đặt phòng (Booking)", "Trong mô hình mẫu chỉ có 'Stay' (chỉ tồn tại khi khách ĐÃ ĐẾN). Không thể lưu trữ thông tin khách đặt phòng trước vài tháng, thông tin tiền cọc hay hủy phòng."),
        ("3. Không thể hỗ trợ Bán vượt phòng (Overbooking)", "Nếu gán trực tiếp khách vào Room vật lý, số lượng đặt phòng bị khóa cứng ở 100% sức chứa vật lý, không thể áp dụng chính sách kinh doanh Overbooking (ví dụ bán 105%)."),
        ("4. Thiếu Thực thể Hóa đơn & Thanh toán", "Chi phí bị gộp chung vào Stay mà không có Invoice/Payment để quản lý hóa đơn đỏ VAT, tách hóa đơn hay đối soát cổng thanh toán.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(2.0), Inches(5.45), Inches(4.8), flaws, font_size=11, bullet="❌")


def build_slide_8_domain_extended(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 5: Mô Hình Miền Mở Rộng (Room Type & Overbooking)", "Extended Domain Model")
    
    # Left Card: Entities Breakdown
    add_card(slide, Inches(0.6), Inches(1.4), Inches(6.85), Inches(5.6), "CÁC THỰC THỂ & QUAN HỆ TRONG MÔ HÌNH MỞ RỘNG", PRIMARY_BLUE)
    entities = [
        ("Guest (1) ── (0..*) Booking", "Một khách hàng có thể có nhiều lượt đặt phòng trong quá khứ/tương lai."),
        ("Booking (1) ── (1..*) BookingLine", "Mỗi đơn đặt phòng có thể đặt nhiều phòng theo các Loại phòng (RoomType) và khoảng thời gian khác nhau."),
        ("RoomType (1) ── (1..*) Room", "Một Loại phòng (Suite, Deluxe...) chứa nhiều phòng vật lý cụ thể (P301, P302)."),
        ("Booking (0..1) ── (0..1) Stay", "Khi khách đến Check-in, Booking chính thức kích hoạt tạo ra lượt lưu trú Stay."),
        ("Stay (1) ── (1) Room", "Tại thời điểm Check-in, khách mới được gán phòng vật lý sạch cụ thể!"),
        ("Room (1) ── (1..*) RoomState", "Ghi nhận lịch sử trạng thái phòng (Sạch, Bẩn, Đang dọn, Đang bảo trì)."),
        ("Stay (1) ── (0..*) ServiceConsumption ── (1) Service", "Lưu vết dịch vụ phát sinh theo thời gian thực."),
        ("Stay (1) ── (1) Invoice ── (1..*) Payment", "Quản lý hóa đơn quyết toán và phương thức thanh toán.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.95), Inches(6.45), Inches(4.9), entities, font_size=10.5, bullet="🔹")

    # Right Card: Overbooking Logic Explained
    add_card(slide, Inches(7.65), Inches(1.4), Inches(5.08), Inches(5.6), "CƠ CHẾ KỸ THUẬT HỖ TRỢ OVERBOOKING", EMERALD)
    ob_logic = [
        ("Bản chất tách rời (Decoupling)", "Khi đặt trước (Booking), hệ thống chỉ giữ chỗ theo Loại phòng (RoomType Quota), KHÔNG gán số phòng vật lý cụ thể."),
        ("Tham số Overbooking Rate", "Mỗi RoomType được cài đặt tỷ lệ bán vượt (ví dụ: có 100 phòng Deluxe, cho phép bán 108 chỗ = 108% dựa trên xác suất hủy phòng lịch sử 8%)."),
        ("Trạng thái Booking", "Bổ sung cờ 'IsOverbooked' hoặc 'Waitlist' để nhận diện các lượt đặt phòng nằm trong hạn mức vượt."),
        ("Khi Check-in", "Nếu khách đến đúng như dự kiến, hệ thống ưu tiên gán phòng cho khách thân thiết/VIP; nếu thiếu phòng sẽ kích hoạt quy trình điều chuyển khẩn cấp.")
    ]
    add_bullet_list(slide, Inches(7.85), Inches(2.0), Inches(4.68), Inches(4.8), ob_logic, font_size=11, bullet="⚙️")


def build_slide_9_checkin_split(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 6: Phân Rã Tác Vụ Check-In (Đã Đặt vs Vãng Lai)", "Check-In Task Analysis")
    
    # 2 Comparison Columns
    add_card(slide, Inches(0.6), Inches(1.3), Inches(5.85), Inches(3.6), "1.2a: CHECK-IN KHÁCH ĐÃ ĐẶT (BOOKED)", EMERALD)
    booked_items = [
        ("Mục đích", "Xác nhận đặt chỗ có sẵn, bàn giao phòng và cấp thẻ từ siêu tốc."),
        ("Điều kiện", "Khách đã có mã Booking trên hệ thống."),
        ("Các bước", "1. Tìm nhanh mã đặt phòng/tên khách. 2. Đối chiếu CCCD/Hộ chiếu. 3. Hệ thống tự động gợi ý phòng sạch phù hợp RoomType. 4. Ký quỹ/quẹt thẻ cọc. 5. Giao thẻ từ phòng."),
        ("Thời gian xử lý", "Cực nhanh: 30 – 45 giây/khách.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.75), Inches(5.45), Inches(3.0), booked_items, font_size=10.5, bullet="✔️")

    add_card(slide, Inches(6.88), Inches(1.3), Inches(5.85), Inches(3.6), "1.2b: CHECK-IN KHÁCH VÃNG LAI (NON-BOOKED)", AMBER)
    walkin_items = [
        ("Mục đích", "Tư vấn phòng trống, đàm phán giá, đăng ký hồ sơ mới và nhận phòng."),
        ("Điều kiện", "Khách đến đột xuất không báo trước; khách sạn còn phòng trống."),
        ("Các bước", "1. Hỏi nhu cầu (loại phòng, số đêm). 2. Kiểm tra phòng trống tức thời. 3. Đàm phán giá/chính sách. 4. Nhập đầy đủ thông tin cá nhân. 5. Thu tiền/cọc trước. 6. Cấp chìa khóa."),
        ("Thời gian xử lý", "Dài hơn: 3 – 5 phút/khách.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(1.75), Inches(5.45), Inches(3.0), walkin_items, font_size=10.5, bullet="⚠️")

    # Bottom Comparison Discussion Card
    add_card(slide, Inches(0.6), Inches(5.05), Inches(12.13), Inches(2.0), "THẢO LUẬN: GIẢI PHÁP 1 TÁC VỤ (ONE-TASK) VS 2 TÁC VỤ (TWO-TASK)", PRIMARY_BLUE)
    discuss_items = [
        ("So sánh giải pháp", "Giải pháp 1 tác vụ xem 'vãng lai' là một biến thể (Variant) của Check-In chung; Giải pháp 2 tác vụ tách thành 2 quy trình riêng biệt."),
        ("Cách tiếp cận nào phù hợp hơn?", "Tại TẦNG PHÂN TÍCH MIỀN (Domain Level), giải pháp 1 TÁC VỤ (ONE-TASK CÓ BIẾN THỂ) TỐT HƠN vì cùng chung mục tiêu nghiệp vụ ('Giao phòng cho khách'). Giúp lễ tân xử lý linh hoạt khi khách tưởng đã đặt mà thực tế bị hủy mà không cần thoát màn hình."),
        ("Tại Tầng Giao diện (UI Design)", "Nên cung cấp 2 chế độ: Chế độ 'Nhận phòng nhanh' (Fast-track) cho khách có mã đặt phòng và 'Khách vãng lai' (Walk-in Wizard) để tối ưu trải nghiệm.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(5.45), Inches(11.7), Inches(1.5), discuss_items, font_size=10.5, bullet="💡")


def build_slide_10_overbooking_crisis(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 1 — Câu 7: Xử Lý Khủng Hoảng Vượt Hạn Mức Phòng (Overbooking)", "Emergency Protocol")
    
    # Left Card: Problem Context & Trigger
    add_card(slide, Inches(0.6), Inches(1.4), Inches(5.85), Inches(5.6), "TÌNH HUỐNG KHỦNG HOẢNG & ĐIỀU KIỆN KÍCH HOẠT", ROSE)
    prob_items = [
        ("Bối cảnh Overbooking", "Khách sạn bán vượt 105% công suất phòng. Thực tế 100% khách đều đến nhận phòng dẫn đến HẾT SẠCH PHÒNG VẬT LÝ trong khi vẫn còn khách cầm đặt phòng hợp lệ."),
        ("Hậu quả nghiêm trọng", "Khách hàng bức xúc, tranh cãi gay gắt tại sảnh, tổn hại nghiêm trọng uy tín thương hiệu khách sạn nếu không có phương án ứng cứu chuyên nghiệp."),
        ("Quy tắc lựa chọn khách điều chuyển (Bumping Criteria)", 
         "TUYỆT ĐỐI KHÔNG điều chuyển khách VIP, khách thành viên thân thiết, đoàn gia đình có trẻ nhỏ/người già, hoặc khách ở dài ngày. Ưu tiên điều chuyển khách đặt qua bên thứ 3 (OTA giá rẻ), khách ở 1 đêm và đến muộn nhất.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.0), Inches(5.45), Inches(4.8), prob_items, font_size=11.5, bullet="🚨")

    # Right Card: 4-Step Emergency Protocol
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.85), Inches(5.6), "QUY TRÌNH 4 BƯỚC XỬ LÝ KHẨN CẤP (WALKING PROTOCOL)", EMERALD)
    sol_items = [
        ("Bước 1: Hệ thống phát hiện & Cảnh báo", "PMS tự động phát tín hiệu đỏ khi tỷ lệ phòng trống = 0; đề xuất danh sách ứng viên có thể điều chuyển theo thuật toán tối ưu."),
        ("Bước 2: Tìm khách sạn đối tác tương đương (Relocation)", "PMS tự động gọi API mạng lưới khách sạn liên kết/cùng tập đoàn để tìm phòng trống tiêu chuẩn tương đương hoặc cao hơn (4 sao lên 5 sao)."),
        ("Bước 3: Gói đền bù & Hỗ trợ chu đáo", "Cung cấp xe riêng đưa đón miễn phí sang khách sạn mới; Miễn phí hoàn toàn đêm đầu tiên; Tặng voucher giảm giá 50% cho lần lưu trú tiếp theo."),
        ("Bước 4: Cập nhật hệ thống & Kết chuyển chi phí", "Chuyển trạng thái Booking sang 'Walked / Relocated', tự động hạch toán chi phí phòng đền bù vào Quỹ chi phí rủi ro Overbooking của khách sạn.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(2.0), Inches(5.45), Inches(4.8), sol_items, font_size=11, bullet="✅")


def build_slide_11_quality_attributes(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 2 — Câu 1: Hệ Thống Các Thuộc Tính Chất Lượng Phần Mềm", "Software Quality Attributes")
    
    # 8 Quality Attributes Grid (2 rows x 4 cols)
    qas = [
        ("1. Maintainability (Bảo trì)", "Khả năng dễ dàng sửa lỗi, cập nhật tính năng mới hoặc thích ứng với môi trường công nghệ mới mà không gây lỗi phụ.", PRIMARY_BLUE),
        ("2. Reliability (Tin cậy)", "Khả năng hệ thống thực hiện đúng chức năng trong điều kiện vận hành xác định suốt một khoảng thời gian quy định.", EMERALD),
        ("3. Security (An toàn/Bảo mật)", "Bảo vệ thông tin dữ liệu khỏi sự truy cập, chỉnh sửa trái phép (Tam giác CIA: Bảo mật, Toàn vẹn, Khả dụng).", ROSE),
        ("4. Performance / Efficiency", "Thời gian đáp ứng (Response Time), độ trễ (Latency) và mức tiêu hao tài nguyên (CPU, RAM, Băng thông).", MID_BLUE),
        ("5. Usability (Khả dụng/Dễ dùng)", "Mức độ dễ học, dễ vận hành, giao diện trực quan và khả năng ngăn chặn sai sót cho người sử dụng.", PURPLE),
        ("6. Availability (Sẵn sàng)", "Tỷ lệ thời gian hệ thống hoạt động bình thường trên tổng thời gian (ví dụ 99.9% uptime, MTTR tối thiểu).", CYAN_ACCENT),
        ("7. Scalability (Mở rộng)", "Khả năng hệ thống xử lý khối lượng công việc tăng vọt bằng cách bổ sung thêm tài nguyên phần cứng.", AMBER),
        ("8. Testability (Kiểm thử)", "Mức độ thuận lợi để thiết kế các kịch bản kiểm thử, phát hiện và cô lập lỗi trong phần mềm.", DARK_NAVY)
    ]
    
    w_card = Inches(2.88)
    h_card = Inches(2.6)
    xs = [Inches(0.6), Inches(3.68), Inches(6.76), Inches(9.84)]
    ys = [Inches(1.4), Inches(4.3)]
    
    for idx, (q_title, q_desc, color) in enumerate(qas):
        gx = xs[idx % 4]
        gy = ys[idx // 4]
        add_card(slide, gx, gy, w_card, h_card, q_title, color)
        add_bullet_list(slide, gx + Inches(0.15), gy + Inches(0.6), w_card - Inches(0.3), h_card - Inches(0.7),
                        [q_desc], font_size=10.5, bullet="🔹")


def build_slide_12_scalability_forms(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 2 — Câu 2: Các Hình Thức Mở Rộng Quy Mô (Scalability)", "System Scalability")
    
    # 2 Main Columns: Vertical vs Horizontal + 3 Other Dimensions
    add_card(slide, Inches(0.6), Inches(1.4), Inches(5.85), Inches(3.2), "VERTICAL SCALABILITY (SCALE-UP — MỞ RỘNG DỌC)", PRIMARY_BLUE)
    vert_items = [
        ("Cơ chế hoạt động", "Nâng cấp sức mạnh phần cứng của một máy chủ duy nhất: thêm CPU Cores, tăng dung lượng RAM, lắp ổ cứng NVMe tốc độ cao hơn."),
        ("Ưu điểm", "Kiến trúc đơn giản, không cần sửa đổi mã nguồn phần mềm, không phải xử lý đồng bộ dữ liệu phân tán phức tạp."),
        ("Nhược điểm", "Chạm ngưỡng giới hạn phần cứng vật lý; Chi phí tăng theo cấp số nhân; Tồn tại điểm nghẽn đơn độc (Single Point of Failure - SPOF).")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.85), Inches(5.45), Inches(2.6), vert_items, font_size=10.5, bullet="⬆️")

    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.85), Inches(3.2), "HORIZONTAL SCALABILITY (SCALE-OUT — MỞ RỘNG NGANG)", EMERALD)
    horiz_items = [
        ("Cơ chế hoạt động", "Bổ sung thêm nhiều máy chủ tiêu chuẩn vào cụm hệ thống (Cluster), sử dụng Cân bằng tải (Load Balancer) để phân phối đều lưu lượng."),
        ("Ứng dụng", "Thiết kế Stateless Application Servers; Cơ sở dữ liệu phân tán (Sharding, Read-Replicas, Microservices)."),
        ("Ưu/Nhược điểm", "Khả năng mở rộng gần như vô hạn, độ chịu lỗi cao; tuy nhiên kiến trúc phần mềm và quản lý tính nhất quán phức tạp hơn.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(1.85), Inches(5.45), Inches(2.6), horiz_items, font_size=10.5, bullet="➡️")

    # Bottom 3 Other Scalability Forms
    add_card(slide, Inches(0.6), Inches(4.75), Inches(12.13), Inches(2.3), "CÁC HÌNH THỨC MỞ RỘNG KHÁC TRONG KỸ THUẬT PHẦN MỀM", DARK_NAVY)
    other_items = [
        ("Structural Scalability (Mở rộng cấu trúc)", "Hệ thống có thể bổ sung thêm nhiều phân hệ, tính năng hoặc microservices mà không làm suy giảm cấu trúc kiến trúc tổng thể."),
        ("Geographic Scalability (Mở rộng địa lý)", "Hệ thống có thể phục vụ người dùng phân tán toàn cầu với độ trễ thấp thông qua mạng phân phối nội dung (CDN) và cụm máy chủ đa vùng (Multi-Region Cloud)."),
        ("Administrative Scalability (Mở rộng quản trị)", "Khả năng một nền tảng phần mềm SaaS phục vụ hàng nghìn chuỗi khách sạn độc lập (Multi-tenancy) mà không làm bùng nổ chi phí vận hành quản trị.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(5.15), Inches(11.7), Inches(1.8), other_items, font_size=10.5, bullet="🌐")


def build_slide_13_throughput(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 2 — Câu 3: Phân Tích Thông Lượng (Average vs. Peak Throughput)", "Performance Engineering")
    
    # Top Definition
    add_card(slide, Inches(0.6), Inches(1.3), Inches(12.13), Inches(1.1), "KHÁI NIỆM THÔNG LƯỢNG (THROUGHPUT)", PRIMARY_BLUE)
    tp_def = [
        ("Định nghĩa", "Thông lượng là số lượng đơn vị công việc (giao dịch, yêu cầu, dữ liệu) mà hệ thống xử lý thành công trong một đơn vị thời gian (ví dụ: Transactions Per Second - TPS, Requests Per Second - RPS, Invoices Per Hour).")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.6), tp_def, font_size=11, bullet="📊")

    # Table Comparing Average vs Peak Throughput
    headers = ["Tiêu chí so sánh", "Thông lượng trung bình (Average Throughput)", "Thông lượng đỉnh (Peak Throughput)"]
    rows = [
        ["Định nghĩa & Khoảng thời gian", 
         "Mức tải trung bình tính toán trên một khoảng thời gian dài (24 giờ, 1 tuần hoặc 1 tháng).", 
         "Mức tải xử lý tối đa đo được trong các khoảng thời gian cao điểm đột biến ngắn."],
        ["Ngữ cảnh Khách sạn (HIS)", 
         "~10–15 giao dịch/giờ (khoảng thời gian buổi chiều ổn định).", 
         "~300–400 giao dịch/giờ (khung giờ vàng trả phòng 07:30–09:30 AM khi các đoàn khách cùng rời đi)."],
        ["Rủi ro thiết kế hệ thống", 
         "Nếu chỉ thiết kế máy chủ đáp ứng mức Trung bình → Hệ thống sẽ quá tải, treo đơ và sập hoàn toàn vào giờ cao điểm.", 
         "Nếu mua phần cứng cố định cho mức Đỉnh → Lãng phí 80% tài nguyên và ngân sách vào các khung giờ bình thường."],
        ["Giải pháp kiến trúc", 
         "Dùng để tính toán dung lượng cơ sở dữ liệu nền tảng và báo cáo hiệu năng định kỳ.", 
         "Áp dụng cơ chế Tự động co giãn (Auto-scaling Cloud), Bộ nhớ đệm (Redis Cache), Hàng đợi bất đồng bộ (RabbitMQ/Kafka) và Giới hạn tốc độ (Rate Limiting)."]
    ]
    add_table_grid(slide, Inches(0.6), Inches(2.5), Inches(12.13), Inches(4.6), headers, rows, [Inches(2.8), Inches(4.6), Inches(4.73)], font_size=10.5)


def build_slide_14_security_vs_availability(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 2 — Câu 4: Mối Quan Hệ Giữa Bảo Mật & Tính Sẵn Sàng", "Security vs. Availability")
    
    # Left Card: Authentication impact
    add_card(slide, Inches(0.6), Inches(1.4), Inches(5.85), Inches(3.6), "1. XÁC THỰC (AUTHENTICATION — AuthN) ẢNH HƯỞNG AVAILABILITY", ROSE)
    authn_items = [
        ("Nghẽn tài nguyên băm mật khẩu", "Các thuật toán mã hóa an toàn (Argon2, bcrypt) ngốn rất nhiều CPU. Kẻ tấn công có thể gửi hàng nghìn yêu cầu đăng nhập giả mạo (Auth DDoS) làm cạn kiệt CPU máy chủ."),
        ("Khóa tài khoản (Account Lockout)", "Chính sách bảo mật khóa tài khoản sau 5 lần nhập sai có thể bị tin tặc lợi dụng để cố ý khóa toàn bộ tài khoản lễ tân, làm tê liệt hoạt động tiếp đón khách."),
        ("Phụ thuộc dịch vụ xác thực ngoài", "Nếu cổng xác thực 2 lớp (MFA qua SMS/Email) hoặc máy chủ SSO bên thứ ba bị gián đoạn, nhân viên không thể đăng nhập vào hệ thống PMS.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.85), Inches(5.45), Inches(3.0), authn_items, font_size=10.5, bullet="🔐")

    # Right Card: Authorization impact
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.85), Inches(3.6), "2. PHÂN QUYỀN (AUTHORIZATION — AuthZ) ẢNH HƯỞNG AVAILABILITY", AMBER)
    authz_items = [
        ("Độ trễ kiểm tra quyền phức tạp", "Việc kiểm tra vai trò chi tiết (RBAC/ABAC) trên từng bản ghi cơ sở dữ liệu làm tăng thời gian phản hồi và dễ làm cạn kiệt số lượng kết nối cơ sở dữ liệu (Connection Pool)."),
        ("Cơ chế Fail-Closed", "Khi máy chủ phân quyền (Policy Decision Point) gặp sự cố, theo nguyên tắc bảo mật hệ thống sẽ từ chối truy cập (Fail-Closed) thay vì cho phép, dẫn đến mất tính sẵn sàng."),
        ("Tắc nghẽn phiên làm việc", "Việc xác thực token phân quyền liên tục qua mạng tạo nút thắt cổ chai cho toàn bộ vi dịch vụ.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(1.85), Inches(5.45), Inches(3.0), authz_items, font_size=10.5, bullet="🛡️")

    # Bottom Solution Card
    add_card(slide, Inches(0.6), Inches(5.15), Inches(12.13), Inches(1.9), "GIẢI PHÁP CÂN BẰNG KIẾN TRÚC GIỮA AN NINH VÀ SẴN SÀNG", EMERALD)
    mit_items = [
        ("Bộ nhớ đệm quyền hạn (Token Caching)", "Sử dụng mã thông báo không trạng thái có chữ ký số (Stateless JWTs) với thời hạn ngắn, lưu tạm quyền vào Redis cache để giảm tải tra cứu."),
        ("Bộ ngắt mạch & Chế độ dự phòng (Circuit Breaker)", "Khi dịch vụ bảo mật ngoài gặp sự cố, hệ thống tự động chuyển sang chế độ dự phòng cục bộ hoặc chế độ chỉ đọc (Read-only Fallback) để duy trì hoạt động cốt lõi."),
        ("Giới hạn tốc độ (Rate Limiting)", "Giới hạn số lần thử đăng nhập theo IP để ngăn chặn triệt để tấn công vét cạn mật khẩu và Auth DDoS.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.4), mit_items, font_size=10.5, bullet="✅")


def build_slide_15_hotel_qa_comparison(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 2 — Câu 5(a,b): Yêu Cầu Chất Lượng Cho Check-In & Check-Out", "Hotel Case Study")
    
    # Left Card: Similarities
    add_card(slide, Inches(0.6), Inches(1.4), Inches(5.85), Inches(5.6), "ĐIỂM TƯƠNG ĐỒNG VỀ CHẤT LƯỢNG (SIMILARITIES)", PRIMARY_BLUE)
    sim_items = [
        ("Tính sẵn sàng cao (High Availability)", "Cả hai tác vụ đều là hoạt động mặt tiền tiếp xúc trực tiếp với khách hàng; hệ thống phải hoạt động 24/7/365, tuyệt đối không được gián đoạn vào giờ cao điểm."),
        ("Hiệu năng phản hồi tức thì (Sub-second Performance)", "Thời gian tra cứu thông tin phòng và tải giao diện phải hoàn tất dưới 1–2 giây để tránh thời gian chết khó chịu giữa khách và lễ tân."),
        ("Tính nhất quán dữ liệu (Data Consistency)", "Đòi hỏi tính toàn vẹn giao dịch ACID tuyệt đối: Check-In không được cấp trùng phòng; Check-Out không được làm thất thoát bất kỳ chi phí dịch vụ nào."),
        ("Bảo mật dữ liệu cá nhân & Thẻ (Security Compliance)", "Đều tiếp xúc với dữ liệu nhạy cảm của khách (CCCD, Hộ chiếu) và thẻ tín dụng ngân hàng, bắt buộc tuân thủ nghiêm ngặt chuẩn bảo mật PCI-DSS."),
        ("Tính dễ sử dụng (Usability)", "Giao diện phải trực quan, hỗ trợ phím tắt bàn phím nhanh để giảm thao tác chuột cho nhân viên.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.0), Inches(5.45), Inches(4.8), sim_items, font_size=11, bullet="🔹")

    # Right Card: Differences
    add_card(slide, Inches(6.88), Inches(1.4), Inches(5.85), Inches(5.6), "ĐIỂM KHÁC BIỆT CỐT LÕI (DIFFERENCES)", MID_BLUE)
    diff_items = [
        ("Trọng tâm tranh chấp tài nguyên (Concurrency)", 
         "Check-In: Tập trung xử lý tranh chấp cấp phát phòng vật lý (ngăn 2 lễ tân cùng chọn phòng 302 một lúc) và tích hợp phần cứng máy ghi thẻ từ.\n"
         "Check-Out: Tập trung vào tính toán tài chính đa nguồn (hóa đơn tiền phòng + minibar + nhà hàng + giặt ủi + thuế phí)."),
        ("Xử lý yếu tố bất định (Uncertainty)", 
         "Check-In: Đối mặt với khách đến sớm (phòng chưa dọn), khách vãng lai, hoặc khủng hoảng hết phòng (Overbooking).\n"
         "Check-Out: Đối mặt với việc khách khiếu nại chi phí minibar, chia tách hóa đơn doanh nghiệp, và độ trễ phản hồi từ cổng thanh toán ngân hàng."),
        ("Tính chịu lỗi tài chính", 
         "Check-Out có tính nhạy cảm pháp lý cao hơn về hóa đơn thuế tài chính VAT, đòi hỏi độ chính xác tiền tệ 100%.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(2.0), Inches(5.45), Inches(4.8), diff_items, font_size=11, bullet="🔸")


def build_slide_16_verifiable_and_top5(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Part 2 — Câu 5(c,d): Đặc Tả Kiểm Chứng & Top 5 Thuộc Tính HIS", "Quality Specifications & Top 5")
    
    # Left Card: Verifiable Scenarios
    add_card(slide, Inches(0.6), Inches(1.4), Inches(6.85), Inches(5.6), "5(c). ĐẶC TẢ YÊU CẦU CHẤT LƯỢNG CÓ THỂ KIỂM CHỨNG", PRIMARY_BLUE)
    scenarios = [
        ("1. Hiệu năng (Performance Scenario)", 
         "Dưới tải làm việc đồng thời của 20 quầy lễ tân, thời gian tính toán và kết xuất hóa đơn Check-out phải hoàn tất trong vòng dưới 1.0 giây đối với 95% số giao dịch."),
        ("2. Dễ sử dụng (Usability Scenario)", 
         "Một nhân viên lễ tân mới sau 1 giờ đào tạo phải hoàn thành quy trình Check-in cho khách có đặt trước trong thời gian dưới 45 giây và không mắc lỗi nhập liệu."),
        ("3. Tính sẵn sàng (Availability Scenario)", 
         "Phân hệ Lễ tân phải đạt độ sẵn sàng tối thiểu 99.95% trong khung giờ từ 06:00 đến 24:00 hàng ngày; Thời gian phục hồi sau lỗi (MTTR) phải dưới 5 phút."),
        ("4. Bảo mật dữ liệu (Security Scenario)", 
         "100% dữ liệu thẻ thanh toán truyền qua mạng phải được mã hóa theo chuẩn AES-256; số thẻ trên màn hình chỉ được hiển thị 4 chữ số cuối theo chuẩn PCI-DSS Level 1."),
        ("5. Nhất quán dữ liệu (Consistency Scenario)", 
         "Hệ thống đảm bảo 0% trường hợp cấp trùng phòng (Zero Double-Booking) khi nhiều lễ tân thao tác đồng thời nhờ cơ chế giao dịch Serializable.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.95), Inches(6.45), Inches(4.9), scenarios, font_size=10, bullet="🎯")

    # Right Card: Top 5 Attributes
    add_card(slide, Inches(7.65), Inches(1.4), Inches(5.08), Inches(5.6), "5(d). TOP 5 THUỘC TÍNH CHẤT LƯỢNG CHO HIS", EMERALD)
    top5 = [
        ("🏆 1. Availability (Sẵn sàng)", "Khách sạn phục vụ 24/7/365. Hệ thống sập đồng nghĩa với sảnh khách tắc nghẽn, mất doanh thu và khủng hoảng truyền thông."),
        ("⚡ 2. Usability (Dễ dùng)", "Lễ tân làm việc dưới áp lực trực tiếp từ ánh mắt khách hàng; phần mềm phải tối ưu thao tác phím bấm, giảm tải nhận thức."),
        ("🛡️ 3. Data Integrity (Nhất quán)", "Phòng ở và hóa đơn tài chính không được phép sai sót; tránh tuyệt đối đặt trùng phòng hay mất phí dịch vụ."),
        ("🔒 4. Security (Bảo mật)", "Hệ thống lưu trữ thông tin cực kỳ nhạy cảm: thẻ ngân hàng, hộ chiếu, lịch trình di chuyển của khách VIP."),
        ("🚀 5. Performance (Hiệu năng)", "Tốc độ xử lý siêu tốc trong các đợt cao điểm sáng trả phòng và chiều các đoàn xe tour nhận phòng.")
    ]
    add_bullet_list(slide, Inches(7.85), Inches(2.0), Inches(4.68), Inches(4.8), top5, font_size=10.5, bullet="⭐")


def build_slide_17_conclusion(prs):
    slide = add_blank_slide(prs)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill_color=DARK_NAVY, line_color=None)
    add_rect(slide, 0, Inches(7.35), SLIDE_W, Inches(0.15), fill_color=MID_BLUE, line_color=None)
    
    # Title Box
    tx_t = slide.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.4))
    tf_t = tx_t.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Tổng Kết & Bài Học Rút Ra (Key Takeaways)"
    r1.font.bold = True
    r1.font.size = Pt(32)
    r1.font.color.rgb = WHITE
    
    p2 = tf_t.add_paragraph()
    p2.space_before = Pt(4)
    r2 = p2.add_run()
    r2.text = "Software Engineering Tutorial 1 — Class Activity User Tasks & Quality Attributes"
    r2.font.size = Pt(16)
    r2.font.color.rgb = ACCENT_BLUE

    # 3 Summary Cards
    cards_data = [
        ("1. Tasks & Support Approach", 
         "Chuyển dịch tư duy từ việc liệt kê chức năng máy tính rời rạc sang hỗ trợ trọn vẹn tác vụ thực tế của người dùng, giúp yêu cầu phần mềm đầy đủ và nhất quán.", 
         PRIMARY_BLUE),
        ("2. Mô hình hóa miền & Overbooking", 
         "Việc phân tách rõ ràng giữa Loại phòng (RoomType) và Phòng vật lý (Room) là chìa khóa để hiện thực hóa các bài toán kinh doanh thực tế như Đặt trước và Bán vượt phòng.", 
         EMERALD),
        ("3. Kiến trúc chất lượng phần mềm", 
         "Các thuộc tính phi chức năng (Availability, Usability, Performance, Security) là yếu tố quyết định thành bại của hệ thống trong môi trường sản xuất thực tế.", 
         MID_BLUE)
    ]
    
    w_sc = Inches(3.55)
    gap = Inches(0.34)
    for i, (stitle, sdesc, scolor) in enumerate(cards_data):
        x = Inches(1.0) + i * (w_sc + gap)
        add_rounded_rect(slide, x, Inches(2.4), w_sc, Inches(2.8), fill_color=RGBColor(0x1E, 0x29, 0x3B), line_color=scolor, line_width=Pt(1.5))
        
        tx = slide.shapes.add_textbox(x + Inches(0.2), Inches(2.55), w_sc - Inches(0.4), Inches(2.4))
        tf = tx.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        rt = pt.add_run()
        rt.text = stitle
        rt.font.bold = True
        rt.font.size = Pt(15)
        rt.font.color.rgb = WHITE
        
        pd = tf.add_paragraph()
        pd.space_before = Pt(8)
        rd = pd.add_run()
        rd.text = sdesc
        rd.font.size = Pt(12)
        rd.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Bottom Authors Signature Banner
    add_rounded_rect(slide, Inches(1.0), Inches(5.5), Inches(11.333), Inches(1.4), fill_color=RGBColor(0x13, 0x23, 0x3D), line_color=CYAN_ACCENT, line_width=Pt(1.2))
    tx_sig = slide.shapes.add_textbox(Inches(1.3), Inches(5.65), Inches(10.7), Inches(1.1))
    tf_sig = tx_sig.text_frame
    tf_sig.word_wrap = True
    
    ps1 = tf_sig.paragraphs[0]
    rs1 = ps1.add_run()
    rs1.text = "CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ THEO DÕI BÁO CÁO!"
    rs1.font.bold = True
    rs1.font.size = Pt(15)
    rs1.font.color.rgb = CYAN_ACCENT
    
    ps2 = tf_sig.add_paragraph()
    ps2.space_before = Pt(4)
    rs2 = ps2.add_run()
    rs2.text = "Nhóm thực hiện: 524H0195 — Ngô Lâm Tiên  |  524H0191 — Nguyễn Công Thành  •  Lớp Kỹ thuật Phần mềm — TDTU"
    rs2.font.size = Pt(13)
    rs2.font.color.rgb = WHITE


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    prs = create_presentation()
    print("Building slides...")
    
    build_slide_1_cover(prs)
    build_slide_2_agenda(prs)
    build_slide_3_checkout_task(prs)
    build_slide_4_his_tasks(prs)
    build_slide_5_workflow(prs)
    build_slide_6_tacit_req(prs)
    build_slide_7_domain_flaws(prs)
    build_slide_8_domain_extended(prs)
    build_slide_9_checkin_split(prs)
    build_slide_10_overbooking_crisis(prs)
    build_slide_11_quality_attributes(prs)
    build_slide_12_scalability_forms(prs)
    build_slide_13_throughput(prs)
    build_slide_14_security_vs_availability(prs)
    build_slide_15_hotel_qa_comparison(prs)
    build_slide_16_verifiable_and_top5(prs)
    build_slide_17_conclusion(prs)
    
    out_dir = "/home/towfienes/TDTU/SE"
    os.makedirs(out_dir, exist_ok=True)
    
    # Save both standard naming conventions
    fpath1 = os.path.join(out_dir, "524H0195_NgoLamTien_524H0191_NguyenCongThanh.pptx")
    fpath2 = os.path.join(out_dir, "524H0195_NgoLamTien_524H0191_NguyenCongThanh_SE_Tutorial1.pptx")
    
    prs.save(fpath1)
    prs.save(fpath2)
    print(f"✅ Successfully created 17 slides presentation:\n   -> {fpath1}\n   -> {fpath2}")


if __name__ == "__main__":
    main()
