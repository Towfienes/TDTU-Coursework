"""
Generate Chap 5 System Modelling Presentation:
Mentcare Psychiatric Patient Management System
Group Members:
- Ngô Lâm Tiến (524H0195) - Người đại diện
- Ngô Bình Minh (524H0169)
- Lê Xuân Khánh (524H0055)
- Nguyễn Công Thành (524H0191)
Faculty of Information Technology - Ton Duc Thang University (TDTU)
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ─── Color Palette ────────────────────────────────────────────────────────────
DARK_NAVY   = RGBColor(0x0A, 0x19, 0x2F)   # #0A192F - Deep Slate Navy
PRIMARY_BLUE= RGBColor(0x1E, 0x3A, 0x5F)   # #1E3A5F - Professional Navy
MID_BLUE    = RGBColor(0x25, 0x63, 0xEB)   # #2563EB - Tech Blue
ACCENT_BLUE = RGBColor(0x38, 0xBD, 0xF8)   # #38BDF8 - Sky Accent
CYAN_ACCENT = RGBColor(0x06, 0xB6, 0xD4)   # #06B6D4 - Secondary Accent
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BG     = RGBColor(0xF8, 0xFA, 0xFC)   # #F8FAFC - Light Slate Card
CARD_ALT_BG = RGBColor(0xF1, 0xF5, 0xF9)   # #F1F5F9 - Alternate Card
BORDER_GRAY = RGBColor(0xCB, 0xD5, 0xE1)   # #CBD5E1 - Border Gray
TEXT_MAIN   = RGBColor(0x0F, 0x17, 0x2A)   # #0F172A - Main Text
TEXT_MUTED  = RGBColor(0x47, 0x55, 0x69)   # #475569 - Muted Text
EMERALD     = RGBColor(0x05, 0x96, 0x69)   # #059669 - Green Success
AMBER       = RGBColor(0xD9, 0x77, 0x06)   # #D97706 - Amber Warning
ROSE        = RGBColor(0xDC, 0x26, 0x26)   # #DC2626 - Rose Danger
PURPLE      = RGBColor(0x7C, 0x3A, 0xED)   # #7C3AED - Purple Accent

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
# SLIDE BUILDERS FOR CHAP 5 - SYSTEM MODELLING
# ==============================================================================

def build_slide_1_cover(prs):
    slide = add_blank_slide(prs)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill_color=DARK_NAVY, line_color=None)
    add_rect(slide, Inches(9), 0, Inches(4.333), Inches(0.15), fill_color=MID_BLUE, line_color=None)
    add_rect(slide, 0, Inches(7.35), Inches(5), Inches(0.15), fill_color=CYAN_ACCENT, line_color=None)
    
    # Subject badge
    add_rounded_rect(slide, Inches(1.0), Inches(0.8), Inches(6.0), Inches(0.5), fill_color=RGBColor(0x1E, 0x29, 0x3B), line_color=MID_BLUE)
    tx_sub = slide.shapes.add_textbox(Inches(1.15), Inches(0.85), Inches(5.8), Inches(0.4))
    r_sub = tx_sub.text_frame.paragraphs[0].add_run()
    r_sub.text = "TDTU • SOFTWARE ENGINEERING • CHAPTER 5 ACTIVITY"
    r_sub.font.bold = True
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = ACCENT_BLUE

    # Title & Subtitle
    tx_t = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(2.2))
    tf_t = tx_t.text_frame
    tf_t.word_wrap = True
    
    p1 = tf_t.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "System Modelling — Mentcare Case Study"
    r1.font.bold = True
    r1.font.size = Pt(36)
    r1.font.color.rgb = WHITE
    
    p2 = tf_t.add_paragraph()
    p2.space_before = Pt(8)
    r2 = p2.add_run()
    r2.text = "Day in the Life of a Systems Analyst & DevOps Engineer (5 Phases of System Modelling)"
    r2.font.size = Pt(18)
    r2.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # Authors Card Container (4 Students)
    add_rounded_rect(slide, Inches(1.0), Inches(3.9), Inches(11.3), Inches(3.1), fill_color=RGBColor(0x13, 0x23, 0x3D), line_color=MID_BLUE, line_width=Pt(1.5))
    
    tx_a = slide.shapes.add_textbox(Inches(1.3), Inches(4.05), Inches(10.7), Inches(2.8))
    tf_a = tx_a.text_frame
    tf_a.word_wrap = True
    
    p_h = tf_a.paragraphs[0]
    r_h = p_h.add_run()
    r_h.text = "DANH SÁCH THÀNH VIÊN NHÓM (GROUP MEMBERS — 4 STUDENTS):"
    r_h.font.bold = True
    r_h.font.size = Pt(13)
    r_h.font.color.rgb = CYAN_ACCENT
    
    members = [
        ("1. Ngô Lâm Tiến", "524H0195 (Người đại diện nộp bài — Lead Submitter)"),
        ("2. Ngô Bình Minh", "524H0169"),
        ("3. Lê Xuân Khánh", "524H0055"),
        ("4. Nguyễn Công Thành", "524H0191")
    ]
    for m_name, m_id in members:
        p_m = tf_a.add_paragraph()
        p_m.space_before = Pt(4)
        r_name = p_m.add_run()
        r_name.text = f"{m_name} "
        r_name.font.bold = True
        r_name.font.size = Pt(16)
        r_name.font.color.rgb = WHITE
        
        r_id = p_m.add_run()
        r_id.text = f"— MSSV: {m_id}"
        r_id.font.size = Pt(15)
        r_id.font.color.rgb = ACCENT_BLUE


def build_slide_2_phase1(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Phase 1: Context & System Boundaries", "Lead Systems Analyst Role")
    
    # Card 1: System Boundary Definition
    add_card(slide, Inches(0.6), Inches(1.35), Inches(5.85), Inches(5.65), "1. MENTCARE SYSTEM BOUNDARY DEFINITION", PRIMARY_BLUE)
    p1_items = [
        ("Phạm vi kiểm soát nội bộ (INSIDE Boundary)", 
         "Các phân hệ thuộc quyền quản lý trực tiếp của Mentcare:\n"
         "• Cơ sở dữ liệu hồ sơ bệnh án tâm thần (Consultation Notes, Risk Assessments, Mental Health Treatment Plans).\n"
         "• Phân hệ lịch hẹn nội bộ (Internal Clinic Scheduling) & Ghi nhận phiên điều trị.\n"
         "• Module phân quyền bác sĩ, giám sát cảnh báo hành vi nguy cơ bệnh nhân và nhật ký bảo mật (Security Audit Logs)."),
        ("Hệ thống độc lập bên ngoài (OUTSIDE Boundary)", 
         "Các hệ thống dùng chung của toàn bệnh viện kết nối qua API/HL7:\n"
         "• Patient Record System (PRS): Hệ thống hồ sơ thông tin hành chính & bệnh sử tổng quát dùng chung.\n"
         "• Admissions System: Quản lý giường bệnh và tiếp nhận bệnh nhân nội trú/ngoại trú toàn viện.\n"
         "• Prescription System: Quản lý kho dược, xuất thuốc, kiểm tra tương tác thuốc và quy định dược lý.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.9), Inches(5.45), Inches(4.9), p1_items, font_size=10.5, bullet="🏛️")

    # Card 2: Context Model & Billing Gateway
    add_card(slide, Inches(6.88), Inches(1.35), Inches(5.85), Inches(5.65), "2. CONTEXT MODEL & BILLING GATEWAY ANALYSIS", MID_BLUE)
    p2_items = [
        ("Mô hình bối cảnh (Context Model)", 
         "Hệ thống Mentcare nằm ở vị trí trung tâm, tương tác với 3 thực thể ngoài:\n"
         "  [Central PRS] <──(HL7/FHIR: Tra cứu hồ sơ/Đồng bộ)──> [ MENTCARE ]\n"
         "  [Admissions]  <──(REST API: Báo nhập viện/Giường)────> [ MENTCARE ]\n"
         "  [Prescription]<──(e-Prescription Order)───────────────> [ MENTCARE ]"),
        ("Câu hỏi 3: Cổng Thanh toán (Billing Gateway) nằm TRONG hay NGOÀI?", 
         "👉 Cổng thanh toán BẮT BUỘC NẰM NGOÀI (OUTSIDE) ranh giới hệ thống Mentcare."),
        ("Lý do 1: Tách biệt trách nhiệm (Separation of Concerns)", 
         "Mentcare là hệ thống quản lý lâm sàng tâm thần. Các nghiệp vụ tài chính, kết nối cổng ngân hàng, đối soát thẻ tín dụng là nghiệp vụ chuyên biệt của khối tài chính bệnh viện."),
        ("Lý do 2: Tiêu chuẩn bảo mật (PCI-DSS Compliance)", 
         "Tách riêng Billing Gateway giúp cách ly dữ liệu thẻ thanh toán, giảm phạm vi kiểm toán bảo mật khắt khe cho Mentcare."),
        ("Lý do 3: Tái sử dụng viện phí (Reusability)", 
         "Bệnh viện sử dụng một cổng thanh toán chung cho tất cả các khoa (Tim mạch, Ung bướu, Tâm thần), Mentcare chỉ gọi API tích hợp.")
    ]
    add_bullet_list(slide, Inches(7.08), Inches(1.9), Inches(5.45), Inches(4.9), p2_items, font_size=10, bullet="🌐")


def build_slide_3_phase2(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Phase 2: Interaction Modeling (Use Cases)", "IT Business Analyst Role")
    
    # Top Card: 3 Distinct Use Cases
    add_card(slide, Inches(0.6), Inches(1.3), Inches(12.13), Inches(1.7), "1. THREE DISTINCT USE CASES INITIATED BY MEDICAL RECEPTIONIST", PRIMARY_BLUE)
    uc_items = [
        ("UC-01: Đăng ký hồ sơ bệnh nhân mới (Register New Patient Profile)", 
         "Tiếp nhận thông tin hành chính ban đầu của bệnh nhân, xác thực định danh và liên kết đồng bộ sang Central Patient Record System."),
        ("UC-02: Tiếp đón & Điểm danh bệnh nhân đến khám (Check-in Arriving Patient)", 
         "Xác nhận sự có mặt của bệnh nhân cho ca hẹn, đưa vào hàng đợi phòng khám (Queue) và kích hoạt thông báo cho Bác sĩ điều trị."),
        ("UC-03: Đặt lịch hẹn tái khám (Schedule Follow-up Appointment)", 
         "Tìm kiếm khung giờ trống của Bác sĩ chuyên khoa, đặt phòng tư vấn và phát hành giấy hẹn tái khám / gửi SMS nhắc hẹn.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.75), Inches(11.7), Inches(1.15), uc_items, font_size=10.5, bullet="📋")

    # Bottom Table: Tabular Description for "Schedule Follow-up Appointment"
    headers = ["Thuộc tính (Element)", "Đặc tả chi tiết (Specification for 'Schedule Follow-up Appointment')"]
    rows = [
        ["Tác nhân (Actors)", "Nhân viên Lễ tân y tế (Medical Receptionist - Primary Initiator), Bệnh nhân (Patient), Bác sĩ tâm thần (Attending Doctor)."],
        ["Mô tả (Description)", "Xếp lịch hẹn tái khám chuyên khoa tâm thần theo chỉ định sau phiên khám của bác sĩ hoặc theo yêu cầu bệnh nhân, đảm bảo lịch trống và không trùng phòng."],
        ["Dữ liệu (Data)", "Mã bệnh nhân (Patient ID), Mã bác sĩ (Doctor ID), Khoảng thời gian yêu cầu (Date & Time slot), Loại hình khám (Tái khám định kỳ, Đánh giá thuốc, Khẩn cấp), Mã phòng tư vấn."],
        ["Kích hoạt (Stimulus)", "Lễ tân nhấp chọn chức năng 'Lập lịch tái khám' trên Mentcare sau khi bệnh nhân hoàn tất ca khám hiện tại hoặc gọi điện đặt lịch."],
        ["Phản hồi (Response)", "Hệ thống hiển thị lịch trống thời gian thực; sau khi xác nhận, Mentcare khóa lịch khám, gửi lời mời lịch đến Bác sĩ và tự động gửi tin nhắn SMS/Email nhắc lịch cho Bệnh nhân."],
        ["Ghi chú an ninh (Security)", "Quyền hạn RBAC nghiêm ngặt: Lễ tân CHỈ ĐƯỢC XEM thông tin hành chính & lịch rảnh của bác sĩ, TUYỆT ĐỐI KHÔNG ĐƯỢC XEM bệnh án tâm thần, chẩn đoán hay ghi chú lâm sàng nhạy cảm của bệnh nhân."]
    ]
    add_table_grid(slide, Inches(0.6), Inches(3.15), Inches(12.13), Inches(3.9), headers, rows, [Inches(3.2), Inches(8.93)], font_size=10)


def build_slide_4_phase3(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Phase 3: Structural Modeling (Class & Generalization)", "System Architect Role")
    
    # Left Card: Class Hierarchy Structure & Attributes
    add_card(slide, Inches(0.6), Inches(1.35), Inches(6.3), Inches(5.65), "1. GENERALIZATION HIERARCHY FOR 'DOCTOR'", PRIMARY_BLUE)
    class_items = [
        ("Lớp cha (Superclass): Doctor", 
         "Chứa các thuộc tính và hành vi cốt lõi của mọi bác sĩ trong hệ thống:\n"
         "• Thuộc tính 1: doctorId: String (Mã định danh duy nhất của bác sĩ)\n"
         "• Thuộc tính 2: fullName: String (Họ và tên bác sĩ)\n"
         "• Thuộc tính bổ sung: licenseNumber: String, phone: String, email: String\n"
         "• Phương thức chung: scheduleAppointment(), viewSchedule(), getContactInfo()"),
        ("Lớp con 1 (Subclass): HospitalDoctor (Bác sĩ nội viện)", 
         "Kế thừa toàn bộ thuộc tính từ Doctor và có thuộc tính đặc thù:\n"
         "• Thuộc tính riêng: departmentId: String (Khoa/Phòng nội trú phụ trách)\n"
         "• Thuộc tính riêng: onCallShift: String, pagerNumber: String (Số máy nhắn tin cấp cứu)\n"
         "• Phương thức riêng: admitPatientToWard(), emergencyConsultation()"),
        ("Lớp con 2 (Subclass): GeneralPractitioner (Bác sĩ đa khoa / Cộng đồng)", 
         "Kế thừa từ Doctor và phục vụ mạng lưới chăm sóc ngoại viện:\n"
         "• Thuộc tính riêng: clinicAddress: String (Địa chỉ phòng khám gia đình tư nhân)\n"
         "• Thuộc tính riêng: practiceRegistrationNumber: String, referralNetworkId: String\n"
         "• Phương thức riêng: issueMentalHealthReferral(), shareCommunityCarePlan()")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.9), Inches(5.9), Inches(4.9), class_items, font_size=10.5, bullet="🏛️")

    # Right Card: Generalization Rationale Question 4
    add_card(slide, Inches(7.1), Inches(1.35), Inches(5.63), Inches(5.65), "2. TẠI SAO DÙNG KẾ THỪA (GENERALIZATION)?", EMERALD)
    why_items = [
        ("Câu hỏi 4", "Tại sao dùng Kế thừa (Generalization) thay vì định nghĩa các lớp riêng biệt từ đầu?"),
        ("1. Tái sử dụng mã nguồn & Nguyên lý DRY (Don't Repeat Yourself)", 
         "Các thông tin cơ bản (ID, Tên, Số chứng chỉ hành nghề, SĐT, Email) chỉ cần định nghĩa duy nhất tại lớp Doctor, tránh lặp lại mã nguồn nhiều lần."),
        ("2. Tính Đa hình (Polymorphism) & Mở rộng linh hoạt", 
         "Phân hệ Lập lịch hẹn của Mentcare chỉ cần làm việc với giao diện tổng quát `Doctor` (ví dụ `appointment.assignDoctor(Doctor doc)`). Hệ thống có thể tiếp nhận cả HospitalDoctor hoặc GP một cách đồng nhất mà không cần viết lại mã nguồn."),
        ("3. Bảo trì tập trung & Tính nhất quán dữ liệu (Data Integrity)", 
         "Khi bệnh viện bổ sung quy định mới về định danh y tế (ví dụ thêm trường `nationalProviderIdentifier`), ta chỉ cần sửa đúng 1 nơi tại lớp cha `Doctor`, toàn bộ các lớp con lập tức được cập nhật đồng bộ."),
        ("4. Ánh xạ cơ sở dữ liệu tối ưu (ORM Mapping)", 
         "Hỗ trợ ánh xạ cơ sở dữ liệu trực quan theo mô hình Single Table Inheritance hoặc Joined Table Inheritance, tối ưu hóa truy vấn bảng quan hệ.")
    ]
    add_bullet_list(slide, Inches(7.3), Inches(1.9), Inches(5.23), Inches(4.9), why_items, font_size=10, bullet="💡")


def build_slide_5_phase4(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Phase 4: Behavioral Modeling (State Machine)", "DevOps / Integration Engineer Role")
    
    # Top Card: Context & 4 Mandatory States
    add_card(slide, Inches(0.6), Inches(1.3), Inches(12.13), Inches(1.8), "SMART HARDWARE PHARMACY DOOR LOCK — 4 TRẠNG THÁI BẮT BUỘC", PRIMARY_BLUE)
    state_items = [
        ("1. Locked (Khóa an toàn — Default)", "Chốt khóa cơ điện đang đóng chặt, đèn LED hiển thị màu đỏ; hệ thống ở trạng thái chờ thẻ nhân viên quẹt."),
        ("2. Authenticating (Đang xác thực quyền)", "Thẻ nhân viên vừa được quét; đầu đọc gửi mã RFID qua Mentcare để kiểm tra danh tính, quyền hạn và ca trực."),
        ("3. Unlocked (Đã mở khóa an toàn)", "Xác thực thành công, chốt điện từ thụt lại, đèn LED chuyển xanh; cho phép nhân viên đẩy cửa bước vào kho thuốc."),
        ("4. Alarm / Disabled (Báo động / Khóa khẩn cấp)", "Phát hiện cố tình cạy cửa (Door Forced) hoặc cửa mở quá lâu (Door Ajar Timeout); còi báo động hú, gửi tín hiệu khẩn cấp về Phòng An ninh.")
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.75), Inches(11.7), Inches(1.25), state_items, font_size=10.5, bullet="🔒")

    # Bottom Table: State Transitions & Events (Stimuli)
    headers = ["Trạng thái bắt đầu (From)", "Sự kiện kích hoạt (Event / Stimulus) & Điều kiện (Guard)", "Trạng thái đích (To)", "Hành động thực hiện (Action)"]
    rows = [
        ["Locked", "Badge Scanned (Nhân viên quẹt thẻ vào đầu đọc RFID)", "Authenticating", "Đọc mã RFID thẻ, bật đèn LED vàng nhấp nháy."],
        ["Authenticating", "Auth Success [Role ∈ {Pharmacist, HeadDoctor} & OnDuty]", "Unlocked", "Kích hoạt nam châm điện nhả chốt, bật LED xanh, kích hoạt bộ đếm thời gian 10s."],
        ["Authenticating", "Auth Failure [Sai thẻ / Không có quyền / Không trong ca]", "Locked", "Phát 3 tiếng bip cảnh báo, ghi log bảo mật thất bại, giữ nguyên chốt khóa."],
        ["Authenticating", "Timeout [Mạng nội bộ chậm > 3s]", "Locked", "Ghi log timeout, chuyển về trạng thái Locked để đảm bảo an toàn."],
        ["Unlocked", "Door Closed & Latched [Cảm biến từ nhận diện đóng cửa]", "Locked", "Đóng chốt điện từ, đổi LED đỏ, tắt timer."],
        ["Unlocked", "Timeout [Cửa bị giữ mở > 30s]", "Alarm / Disabled", "Hú còi báo động tại chỗ, gửi cảnh báo vi phạm về trung tâm bảo vệ."],
        ["Locked", "Door Forced [Cảm biến phát hiện cửa bị cạy phá trái phép]", "Alarm / Disabled", "Bật còi hú công suất lớn, kích hoạt chốt khóa vật lý khẩn cấp, gọi Cảnh sát viện."],
        ["Alarm / Disabled", "Security Reset [Quản lý dùng Master Key + Nhập PIN an ninh]", "Locked", "Tắt còi báo động, lưu báo cáo sự cố an ninh, đưa khóa về hoạt động bình thường."]
    ]
    add_table_grid(slide, Inches(0.6), Inches(3.25), Inches(12.13), Inches(3.8), headers, rows, [Inches(2.0), Inches(4.5), Inches(2.2), Inches(3.43)], font_size=9.5)


def build_slide_6_phase5(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Phase 5: GenAI Workflow Integration", "Forward-Thinking Developer Role")
    
    # Left Card: Technical Prompt
    add_card(slide, Inches(0.6), Inches(1.35), Inches(6.3), Inches(5.65), "1. KỸ THUẬT THIẾT KẾ PROMPT CHUYỂN UML THÀNH MÃ NGUỒN", PRIMARY_BLUE)
    tx_p = slide.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.9), Inches(5.0))
    tf_p = tx_p.text_frame
    tf_p.word_wrap = True
    
    p_code = tf_p.paragraphs[0]
    r_code = p_code.add_run()
    r_code.text = (
        "PROMPT MẪU CHUẨN KỸ THUẬT CHO LLM:\n\n"
        "\"Act as a Senior Python/Java Software Architect. Based on the following UML Class Diagram specification for the Mentcare Medical Staff system:\n\n"
        "1. Superclass: Doctor (ABC)\n"
        "   - Attributes: doctor_id: str, full_name: str, license_number: str, email: str, phone: str\n"
        "   - Abstract/Common Methods: schedule_appointment(patient_id: str, slot: datetime) -> bool, get_profile() -> dict\n\n"
        "2. Subclass: HospitalDoctor (inherits Doctor)\n"
        "   - Unique Attributes: department_id: str, on_call_shift: str, pager_number: str\n"
        "   - Specific Methods: admit_patient(patient_id: str, ward_id: str) -> None\n\n"
        "3. Subclass: GeneralPractitioner (inherits Doctor)\n"
        "   - Unique Attributes: clinic_address: str, practice_reg_num: str, referral_network_id: str\n"
        "   - Specific Methods: issue_referral(patient_id: str, specialist_id: str) -> dict\n\n"
        "Task: Generate a production-ready Python 3.12 implementation using dataclasses, complete Type Hints, full Google-style docstrings, strict input validation in __post_init__, and unit tests with pytest demonstrating polymorphic usage.\""
    )
    r_code.font.size = Pt(9.5)
    r_code.font.color.rgb = TEXT_MAIN

    # Right Card: Why UML > Plain English
    add_card(slide, Inches(7.1), Inches(1.35), Inches(5.63), Inches(5.65), "2. TẠI SAO CẤU TRÚC UML AN TOÀN & CHÍNH XÁC HƠN VĂN BẢN?", EMERALD)
    why_items = [
        ("1. Triệt tiêu tính mơ hồ (Elimination of Ambiguity)", 
         "Văn bản tự nhiên tiếng Anh/tiếng Việt chứa đầy từ đa nghĩa và cấu trúc câu lỏng lẻo. UML cung cấp cú pháp hình thức toán học rõ ràng (tên lớp, kiểu dữ liệu, quan hệ `is-a`, tầm vực `+`/`-`), giúp LLM hiểu chính xác 100% mà không phải phỏng đoán."),
        ("2. Ngăn chặn hiện tượng 'Ảo giác' (Hallucination Control)", 
         "Khi cung cấp cấu trúc thực thể tường minh, không gian tìm kiếm xác suất của LLM bị thu hẹp vào các lớp đã định nghĩa. AI sẽ không tự ý bịa ra các thuộc tính tùy tiện hay tạo thêm các hàm không mong muốn."),
        ("3. Đảm bảo an toàn kiểu dữ liệu (Strict Type Safety)", 
         "UML chỉ rõ kiểu dữ liệu (`String`, `DateTime`, `Boolean`) và quan hệ bao hàm (Inheritance, Multiplicity), đảm bảo mã nguồn sinh ra có Type Hinting chuẩn, giảm thiểu tối đa lỗi Runtime Type Errors trong y tế."),
        ("4. Nhất quán kiến trúc doanh nghiệp (Architectural Invariants)", 
         "UML đóng vai trò là bản hợp đồng thiết kế (Design Contract). Mã nguồn do AI sinh ra bắt buộc phải tuân thủ đúng kiến trúc do Kiến trúc sư trưởng vạch ra.")
    ]
    add_bullet_list(slide, Inches(7.3), Inches(1.9), Inches(5.23), Inches(4.9), why_items, font_size=10, bullet="🛡️")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    prs = create_presentation()
    print("Building Chap 5 System Modelling presentation slides...")
    
    build_slide_1_cover(prs)
    build_slide_2_phase1(prs)
    build_slide_3_phase2(prs)
    build_slide_4_phase3(prs)
    build_slide_5_phase4(prs)
    build_slide_6_phase5(prs)
    
    out_dir = "/home/towfienes/TDTU/SE"
    os.makedirs(out_dir, exist_ok=True)
    
    # Save filenames
    fpath1 = os.path.join(out_dir, "524H0195_NgoLamTien_Chap5_SystemModelling.pptx")
    fpath2 = os.path.join(out_dir, "524H0195_524H0169_524H0055_524H0191_Chap5_SystemModelling.pptx")
    
    prs.save(fpath1)
    prs.save(fpath2)
    print(f"✅ Successfully created 6 slides presentation:\n   -> {fpath1}\n   -> {fpath2}")


if __name__ == "__main__":
    main()
