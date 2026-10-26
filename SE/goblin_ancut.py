import os
import re
import subprocess
import markdown

SE_DIR = '/home/towfienes/TDTU/SE'
IMG_DIR = os.path.join(SE_DIR, 'images')

with open(os.path.join(SE_DIR, '524H0195_NgoLamTien_Report.md'), 'r', encoding='utf-8') as f:
    md_content = f.read()

def format_mermaid(match):
    code = match.group(1).strip()
    return f"""<details style="margin: 15px 0; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 15px;">
<summary style="cursor: pointer; font-weight: 600; color: #0284c7;">🔍 Xem mã nguồn định nghĩa Mermaid UML (Code Definition)</summary>
<pre style="margin-top: 10px; background: #ffffff; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 12px;"><code>{code}</code></pre>
</details>"""

pattern = r'```mermaid\s*\n(.*?)\n```'
processed_md = re.sub(pattern, format_mermaid, md_content, flags=re.DOTALL)

html_body = markdown.markdown(processed_md, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Báo cáo Bài tập Lab 4 - Lab 5 - Lab 6 - Kỹ thuật Phần mềm (503074) - 524H0195</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 14mm 18mm 14mm;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.6;
        color: #1e293b;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px;
        background-color: #ffffff;
    }}
    h1 {{
        color: #0f172a;
        font-size: 22px;
        font-weight: 800;
        border-bottom: 3px solid #0284c7;
        padding-bottom: 8px;
        margin-top: 35px;
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
    p, li {{
        font-size: 13.5px;
        text-align: justify;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 18px 0;
        font-size: 12.5px;
        page-break-inside: avoid;
    }}
    th, td {{
        border: 1px solid #cbd5e1;
        padding: 8px 10px;
        text-align: left;
    }}
    th {{
        background-color: #f1f5f9;
        font-weight: 600;
        color: #1e293b;
    }}
    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}
    blockquote {{
        border-left: 4px solid #0284c7;
        margin: 15px 0;
        padding: 10px 16px;
        background-color: #f0f9ff;
        color: #0369a1;
        font-style: italic;
        border-radius: 0 6px 6px 0;
    }}
    img {{
        max-width: 100%;
        height: auto;
        display: block;
        margin: 18px auto;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.06);
        page-break-inside: avoid;
    }}
    code {{
        background-color: #f1f5f9;
        padding: 2px 5px;
        border-radius: 4px;
        font-family: Consolas, Monaco, monospace;
        font-size: 88%;
        color: #dc2626;
    }}
    hr {{
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 25px 0;
    }}
    @media print {{
        body {{
            max-width: 100%;
            padding: 0;
            font-size: 10.5pt;
        }}
        img {{
            max-width: 95% !important;
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

html_out = os.path.join(SE_DIR, '524H0195_NgoLamTien_Report.html')
with open(html_out, 'w', encoding='utf-8') as f:
    f.write(full_html)

pdf_out = os.path.join(SE_DIR, '524H0195_NgoLamTien_Report.pdf')
cmd = [
    'chromium', '--headless', '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_out}',
    html_out
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("PDF output size:", os.path.getsize(pdf_out), "bytes")
