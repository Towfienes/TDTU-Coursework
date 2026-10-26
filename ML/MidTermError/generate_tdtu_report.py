import re
from pathlib import Path

root = Path("/home/towfienes/TDTU/ML/MidTerm/ML_Midterm_Final")
code = (root / "src/build_report.py").read_text(encoding="utf-8")

# 1. Update imports
import_addition = "from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT\n"
code = code.replace("from reportlab.lib.styles import ParagraphStyle\n", "from reportlab.lib.styles import ParagraphStyle\n" + import_addition)

# 2. Canvas replacement
canvas_code = """
class TDTUTemplateCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("initialFontName", "Times")
        super().__init__(*args, **kwargs)
        self.states = []

    def showPage(self):
        self.states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        roman_map = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
        total = len(self.states)
        for idx, state in enumerate(self.states, start=1):
            self.__dict__.update(state)
            if idx <= 2:
                # Cover 1 & 2: elegant academic double border
                self.setStrokeColor(colors.HexColor("#1A1A1A"))
                self.setLineWidth(1.6)
                self.rect(36, 36, A4[0] - 72, A4[1] - 72)
                self.setLineWidth(0.6)
                self.rect(40, 40, A4[0] - 80, A4[1] - 80)
            elif 3 <= idx <= 5:
                # Front matter: Roman numerals in top-right header
                roman_idx = idx - 2
                roman_str = roman_map[roman_idx] if roman_idx < len(roman_map) else str(roman_idx)
                self.setFont("Times", 10.5)
                self.setFillColor(colors.HexColor("#111111"))
                self.drawRightString(A4[0] - 50, A4[1] - 36, roman_str)
                self.setStrokeColor(colors.HexColor("#D0D0D0"))
                self.setLineWidth(0.5)
                self.line(50, A4[1] - 42, A4[0] - 50, A4[1] - 42)
            else:
                # Main body chapters: Arabic numerals starting at page 6 -> 1
                body_num = idx - 5
                self.setFont("Times", 9.5)
                self.setFillColor(colors.HexColor("#555555"))
                self.drawString(50, A4[1] - 36, "TON DUC THANG UNIVERSITY — FACULTY OF INFORMATION TECHNOLOGY")
                self.setFillColor(colors.HexColor("#111111"))
                self.drawRightString(A4[0] - 50, A4[1] - 36, str(body_num))
                self.setStrokeColor(colors.HexColor("#888888"))
                self.setLineWidth(0.6)
                self.line(50, A4[1] - 42, A4[0] - 50, A4[1] - 42)

                # Running footer
                self.setStrokeColor(colors.HexColor("#D0D0D0"))
                self.setLineWidth(0.5)
                self.line(50, 44, A4[0] - 50, 44)
                self.setFont("Times", 8.5)
                self.setFillColor(colors.HexColor("#555555"))
                self.drawString(50, 32, "MIDTERM REPORT: INTRODUCTION TO MACHINE LEARNING")
                self.drawRightString(A4[0] - 50, 32, f"Page {body_num}")
            super().showPage()
        super().save()
"""
code = re.sub(r"class NumberCanvas\(canvas\.Canvas\):[\s\S]*?super\(\)\.save\(\)", canvas_code.strip(), code)

# 3. Add styles for covers and front matter
styles_addition = """
        "cover_sup": ParagraphStyle(
            "cover_sup",
            fontName="Times",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_univ": ParagraphStyle(
            "cover_univ",
            fontName="TimesBold",
            fontSize=13.5,
            leading=19,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_fac": ParagraphStyle(
            "cover_fac",
            fontName="TimesBold",
            fontSize=13.5,
            leading=19,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_student": ParagraphStyle(
            "cover_student",
            fontName="TimesBold",
            fontSize=13,
            leading=19,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="TimesBold",
            fontSize=24,
            leading=30,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_course": ParagraphStyle(
            "cover_course",
            fontName="TimesBold",
            fontSize=19,
            leading=25,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName="TimesItalic",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_advise_label": ParagraphStyle(
            "cover_advise_label",
            fontName="Times",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_advise_name": ParagraphStyle(
            "cover_advise_name",
            fontName="TimesBold",
            fontSize=13.5,
            leading=19,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "cover_foot": ParagraphStyle(
            "cover_foot",
            fontName="TimesBold",
            fontSize=13,
            leading=18,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "front_title": ParagraphStyle(
            "front_title",
            fontName="TimesBold",
            fontSize=16,
            leading=22,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "front_body": ParagraphStyle(
            "front_body",
            fontName="Times",
            fontSize=12,
            leading=18,
            textColor=colors.HexColor(NAVY),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
        ),
        "front_date": ParagraphStyle(
            "front_date",
            fontName="TimesItalic",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor(NAVY),
            alignment=TA_RIGHT,
            spaceAfter=6,
        ),
        "front_role": ParagraphStyle(
            "front_role",
            fontName="TimesBold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor(NAVY),
            alignment=TA_RIGHT,
        ),
        "front_sig_note": ParagraphStyle(
            "front_sig_note",
            fontName="TimesItalic",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor(GRAY),
            alignment=TA_RIGHT,
            spaceAfter=12,
        ),
        "sig_cell": ParagraphStyle(
            "sig_cell",
            fontName="TimesBold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
        ),
        "toc_chap": ParagraphStyle(
            "toc_chap",
            fontName="TimesBold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor(NAVY),
        ),
        "toc_sec": ParagraphStyle(
            "toc_sec",
            fontName="Times",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor(NAVY),
            leftIndent=14,
        ),
        "toc_page": ParagraphStyle(
            "toc_page",
            fontName="TimesBold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor(NAVY),
            alignment=TA_RIGHT,
        ),
"""
code = code.replace('"caption": ParagraphStyle(\n            "caption",\n            fontName="TimesItalic",\n            fontSize=8.5,\n            leading=12,\n            textColor=colors.HexColor(GRAY),\n            spaceBefore=5,\n            spaceAfter=13,\n        ),\n    }', '"caption": ParagraphStyle(\n            "caption",\n            fontName="TimesItalic",\n            fontSize=8.5,\n            leading=12,\n            textColor=colors.HexColor(GRAY),\n            spaceBefore=5,\n            spaceAfter=13,\n        ),\n' + styles_addition + '    }')

# 4. Replace cover page with 5 front matter pages
front_matter_code = """
    logo_path = source / "tdtu_logo.png"

    # 1. OUTER COVER PAGE
    add(
        Spacer(1, 20),
        p("VIETNAM GENERAL CONFEDERATION OF LABOR", "cover_sup"),
        Spacer(1, 3),
        p("TON DUC THANG UNIVERSITY", "cover_univ"),
        Spacer(1, 3),
        p("FACULTY OF INFORMATION TECHNOLOGY", "cover_fac"),
        Spacer(1, 28),
        Image(str(logo_path), width=135, height=75, hAlign="CENTER"),
        Spacer(1, 38),
        p("NGÔ LÂM TIẾN — 524H0195", "cover_student"),
        Spacer(1, 3),
        p("NGUYỄN CÔNG THÀNH — 524H0191", "cover_student"),
        Spacer(1, 3),
        p("NGUYỄN LÊ NHẬT TÂM — 524H0186", "cover_student"),
        Spacer(1, 45),
        p("MIDTERM REPORT", "cover_title"),
        Spacer(1, 10),
        p("INTRODUCTION TO MACHINE LEARNING", "cover_course"),
        Spacer(1, 10),
        p("Optimization, Classification and Generalization", "cover_sub"),
        Spacer(1, 95),
        p("HO CHI MINH CITY, 2026", "cover_foot"),
        PageBreak(),
    )

    # 2. INNER COVER PAGE
    add(
        Spacer(1, 20),
        p("VIETNAM GENERAL CONFEDERATION OF LABOR", "cover_sup"),
        Spacer(1, 3),
        p("TON DUC THANG UNIVERSITY", "cover_univ"),
        Spacer(1, 3),
        p("FACULTY OF INFORMATION TECHNOLOGY", "cover_fac"),
        Spacer(1, 28),
        Image(str(logo_path), width=135, height=75, hAlign="CENTER"),
        Spacer(1, 38),
        p("NGÔ LÂM TIẾN — 524H0195", "cover_student"),
        Spacer(1, 3),
        p("NGUYỄN CÔNG THÀNH — 524H0191", "cover_student"),
        Spacer(1, 3),
        p("NGUYỄN LÊ NHẬT TÂM — 524H0186", "cover_student"),
        Spacer(1, 42),
        p("MIDTERM REPORT", "cover_title"),
        Spacer(1, 10),
        p("INTRODUCTION TO MACHINE LEARNING", "cover_course"),
        Spacer(1, 28),
        p("Advised by", "cover_advise_label"),
        Spacer(1, 4),
        p("Faculty of Information Technology", "cover_advise_name"),
        Spacer(1, 80),
        p("HO CHI MINH CITY, 2026", "cover_foot"),
        PageBreak(),
    )

    # 3. ACKNOWLEDGEMENT
    add(
        Spacer(1, 15),
        p("ACKNOWLEDGEMENT", "front_title"),
        p(
            "We would like to express our sincere gratitude to our instructor and the Faculty of Information Technology at Ton Duc Thang University for their dedicated instruction, insightful feedback, and continuous guidance throughout the Introduction to Machine Learning course and this midterm project. Through this assignment, we have developed a rigorous understanding of optimization foundations from first principles, sound empirical benchmarking protocols, and essential principles for preventing data leakage and controlling model capacity.",
            "front_body",
        ),
        p(
            "We also extend our appreciation to our fellow students and academic peers for constructive discussions and collaborative sharing of machine learning insights. We are deeply honored and privileged to conduct this research under the academic standards of Ton Duc Thang University.",
            "front_body",
        ),
        Spacer(1, 25),
        p("Ho Chi Minh city, October 2026.", "front_date"),
        p("Authors", "front_role"),
        p("(Signature and full name)", "front_sig_note"),
        Spacer(1, 40),
        Table(
            [
                [
                    Paragraph("Ngô Lâm Tiến", styles["sig_cell"]),
                    Paragraph("Nguyễn Công Thành", styles["sig_cell"]),
                    Paragraph("Nguyễn Lê Nhật Tâm", styles["sig_cell"]),
                ]
            ],
            colWidths=[166, 166, 166],
            style=[("ALIGN", (0, 0), (-1, -1), "CENTER")],
        ),
        PageBreak(),
    )

    # 4. DECLARATION OF AUTHORSHIP
    add(
        Spacer(1, 15),
        p("DECLARATION OF AUTHORSHIP", "front_title"),
        p(
            "We hereby declare that this is our own project and is guided by our instructor; The research derivations, algorithmic implementations, and empirical results contained herein are our original work and have not been published in any form before. The data in the tables for analysis, comments and evaluation are collected and processed by our group from documented sources, which are clearly stated in the reference section.",
            "front_body",
        ),
        p(
            "In addition, the project also uses comments, assessments as well as standard algorithms and baseline data of other authors and organizations with clear citations and annotated sources.",
            "front_body",
        ),
        p(
            "If any violation occurs, we will take full responsibility for the content of our project. Ton Duc Thang University is not responsible for any copyright or intellectual property infringements during our implementation process (if any).",
            "front_body",
        ),
        Spacer(1, 20),
        p("Ho Chi Minh city, October 2026", "front_date"),
        p("Authors", "front_role"),
        p("(Signature and full name)", "front_sig_note"),
        Spacer(1, 40),
        Table(
            [
                [
                    Paragraph("Ngô Lâm Tiến", styles["sig_cell"]),
                    Paragraph("Nguyễn Công Thành", styles["sig_cell"]),
                    Paragraph("Nguyễn Lê Nhật Tâm", styles["sig_cell"]),
                ]
            ],
            colWidths=[166, 166, 166],
            style=[("ALIGN", (0, 0), (-1, -1), "CENTER")],
        ),
        PageBreak(),
    )

    # 5. TABLE OF CONTENT
    toc_data = [
        ("CHAPTER 1. INTRODUCTION", 1, True),
        ("1.1 Objectives and experimental overview", 1, False),
        ("1.2 Reading map and experimental boundaries", 1, False),
        ("CHAPTER 2. THEORETICAL BASIS", 2, True),
        ("2.1 Linear Regression and its gradient", 2, False),
        ("2.2 Batch Gradient Descent and verification", 3, False),
        ("2.3 Linear Regression experiment", 4, False),
        ("2.4 Logistic Regression and cross-entropy", 5, False),
        ("2.5 Stable scratch implementation", 6, False),
        ("2.6 Logistic Regression experiment", 7, False),
        ("CHAPTER 3. DESIGNING AND IMPLEMENTING", 8, True),
        ("3.1 OpenML dataset and provenance", 8, False),
        ("3.2 Exploratory analysis and cleaning", 9, False),
        ("3.3 Preprocessing without leakage", 10, False),
        ("3.4 Model comparison protocol", 11, False),
        ("3.5 Cross-validation and test comparison", 12, False),
        ("3.6 Selected model and generalization", 13, False),
        ("CHAPTER 4. OVERFITTING ANALYSIS AND MITIGATION", 14, True),
        ("4.1 Overfitting across model families", 14, False),
        ("4.2 Empirical mitigation and trade-offs", 15, False),
        ("4.3 Discussion and remaining limitations", 16, False),
        ("REFERENCES", 17, True),
        ("APPENDIX. REPRODUCIBILITY AND VERIFICATION", 18, True),
    ]

    toc_rows = []
    for t_title, t_pg, is_chap in toc_data:
        st_title = "toc_chap" if is_chap else "toc_sec"
        toc_rows.append(
            [
                Paragraph(t_title, styles[st_title]),
                Paragraph(str(t_pg), styles["toc_page"]),
            ]
        )

    t_toc = Table(toc_rows, colWidths=[450, 48])
    t_toc.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    add(
        Spacer(1, 15),
        p("TABLE OF CONTENT", "front_title"),
        t_toc,
    )
"""

old_cover_pattern = r"# Cover uses a genuine Q1 training curve as the visual signature\.[\s\S]*?section\(\"1  Objectives and experimental overview\"\)"
code = re.sub(old_cover_pattern, front_matter_code.strip() + '\n\n    section("CHAPTER 1. INTRODUCTION<br/><br/>1.1  Objectives and experimental overview")', code)

# 5. Update chapter headers
code = code.replace('section("2  Linear Regression and its gradient")', 'section("CHAPTER 2. THEORETICAL BASIS<br/><br/>2.1  Linear Regression and its gradient")')
code = code.replace('section("3  Batch Gradient Descent and verification")', 'section("2.2  Batch Gradient Descent and verification")')
code = code.replace('section("4  Linear Regression experiment")', 'section("2.3  Linear Regression experiment")')
code = code.replace('section("5  Logistic Regression and cross-entropy")', 'section("2.4  Logistic Regression and cross-entropy")')
code = code.replace('section("6  Stable scratch implementation")', 'section("2.5  Stable scratch implementation")')
code = code.replace('section("7  Logistic Regression experiment")', 'section("2.6  Logistic Regression experiment")')

code = code.replace('section("8  OpenML dataset and provenance")', 'section("CHAPTER 3. DESIGNING AND IMPLEMENTING<br/><br/>3.1  OpenML dataset and provenance")')
code = code.replace('section("9  Exploratory analysis and cleaning")', 'section("3.2  Exploratory analysis and cleaning")')
code = code.replace('section("10  Preprocessing without leakage")', 'section("3.3  Preprocessing without leakage")')
code = code.replace('section("11  Model comparison protocol")', 'section("3.4  Model comparison protocol")')
code = code.replace('section("12  Cross-validation and test comparison")', 'section("3.5  Cross-validation and test comparison")')
code = code.replace('section("13  Selected model and generalization")', 'section("3.6  Selected model and generalization")')

code = code.replace('section("14  Overfitting across model families")', 'section("CHAPTER 4. OVERFITTING ANALYSIS AND MITIGATION<br/><br/>4.1  Overfitting across model families")')
code = code.replace('section("15  Empirical mitigation and trade-offs")', 'section("4.2  Empirical mitigation and trade-offs")')
code = code.replace('section("16  Discussion and remaining limitations")', 'section("4.3  Discussion and remaining limitations")')

code = code.replace('section("17  References")', 'section("REFERENCES")')
code = code.replace('section("18  Reproducibility and verification appendix")', 'section("APPENDIX. REPRODUCIBILITY AND VERIFICATION")')

# 6. Change canvasmaker to TDTUTemplateCanvas and update output file path
code = code.replace("canvasmaker=NumberCanvas", "canvasmaker=TDTUTemplateCanvas")
code = code.replace('output = root / "report/Machine_Learning_Midterm_Final.pdf"', 'output = root / "report/Machine_Learning_Midterm_TDTU_Template.pdf"')

(root / "src/build_template_report.py").write_text(code, encoding="utf-8")
print("build_template_report.py generated successfully!")
