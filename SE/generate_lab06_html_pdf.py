import os
import re
import subprocess
import markdown

SE_DIR = '/home/towfienes/TDTU/SE'
MD_FILE = os.path.join(SE_DIR, '524H0195_NgoLamTien_Lab06_Report.md')
HTML_FILE = os.path.join(SE_DIR, '524H0195_NgoLamTien_Lab06_Report.html')
PDF_FILE = os.path.join(SE_DIR, '524H0195_NgoLamTien_Lab06_Report.pdf')

with open(MD_FILE, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Replace mermaid blocks with code details
def format_mermaid(match):
    code = match.group(1).strip()
    return f"""<details style="margin: 15px 0; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px 16px;">
<summary style="cursor: pointer; font-weight: 600; color: #0284c7; user-select: none;">🔍 Xem mã nguồn định nghĩa Mermaid UML (Code Definition)</summary>
<pre style="margin-top: 10px; background: #0f172a; color: #f8fafc; padding: 14px; border-radius: 6px; overflow-x: auto; font-size: 12px; font-family: 'Fira Code', Consolas, Monaco, monospace; line-height: 1.45;"><code>{code}</code></pre>
</details>"""

pattern = r'```mermaid\s*\n(.*?)\n```'
processed_md = re.sub(pattern, format_mermaid, md_content, flags=re.DOTALL)

html_body = markdown.markdown(processed_md, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Báo cáo Bài tập Lab 06 - Kỹ thuật Phần mềm (503074) - MSSV: 524H0195</title>
<style>
    @page {{
        size: A4;
        margin: 16mm 14mm 16mm 14mm;
    }}
    * {{
        box-sizing: border-box;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.65;
        color: #1e293b;
        max-width: 920px;
        margin: 0 auto;
        padding: 40px 24px;
        background-color: #ffffff;
    }}
    h1 {{
        color: #0f172a;
        font-size: 22px;
        font-weight: 800;
        border-bottom: 3px solid #0284c7;
        padding-bottom: 8px;
        margin-top: 36px;
        margin-bottom: 18px;
    }}
    h2 {{
        color: #0369a1;
        font-size: 18px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 14px;
        border-left: 4px solid #0284c7;
        padding-left: 10px;
    }}
    h3 {{
        color: #0f766e;
        font-size: 15px;
        font-weight: 700;
        margin-top: 22px;
        margin-bottom: 10px;
    }}
    h4 {{
        color: #334155;
        font-size: 14px;
        font-weight: 600;
        margin-top: 16px;
        margin-bottom: 8px;
    }}
    p, li {{
        font-size: 13.5px;
        text-align: justify;
        color: #334155;
    }}
    ul, ol {{
        padding-left: 24px;
        margin: 10px 0;
    }}
    li {{
        margin-bottom: 6px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 12.5px;
        page-break-inside: avoid;
    }}
    th, td {{
        border: 1px solid #cbd5e1;
        padding: 8px 12px;
        text-align: left;
    }}
    th {{
        background-color: #f1f5f9;
        font-weight: 700;
        color: #0f172a;
    }}
    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}
    blockquote {{
        border-left: 4px solid #0284c7;
        margin: 16px 0;
        padding: 12px 18px;
        background-color: #f0f9ff;
        color: #0369a1;
        font-style: italic;
        border-radius: 0 8px 8px 0;
    }}
    img {{
        max-width: 100%;
        height: auto;
        display: block;
        margin: 20px auto;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
        page-break-inside: avoid;
    }}
    code {{
        background-color: #f1f5f9;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: Consolas, Monaco, monospace;
        font-size: 90%;
        color: #b91c1c;
    }}
    pre code {{
        background-color: transparent;
        padding: 0;
        color: inherit;
        font-size: 12px;
    }}
    hr {{
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 28px 0;
    }}
    a {{
        color: #0284c7;
        text-decoration: none;
    }}
    a:hover {{
        text-decoration: underline;
    }}
    @media print {{
        body {{
            max-width: 100%;
            padding: 0;
            font-size: 10.5pt;
        }}
        img {{
            max-width: 96% !important;
            max-height: 220mm !important;
            page-break-inside: avoid;
        }}
        h1, h2, h3 {{
            page-break-after: avoid;
        }}
        table {{
            page-break-inside: avoid;
        }}
        details {{
            display: none;
        }}
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"Generated HTML: {HTML_FILE} ({os.path.getsize(HTML_FILE)} bytes)")

cmd = [
    'chromium', '--no-sandbox', '--headless', '--disable-gpu',
    '--no-pdf-header-footer',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={PDF_FILE}',
    HTML_FILE
]
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(PDF_FILE):
    print(f"Generated PDF: {PDF_FILE} ({os.path.getsize(PDF_FILE)} bytes)")
else:
    print("PDF generation failed! Error:", res.stderr)
