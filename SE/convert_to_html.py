import re
import markdown

def main():
    with open('/home/towfienes/TDTU/SE/524H0195_NgoLamTien_Lab04_Report.md', 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Protect mermaid blocks from markdown mangling
    mermaid_blocks = []
    def stash_mermaid(match):
        idx = len(mermaid_blocks)
        mermaid_blocks.append(match.group(1).strip())
        return f"<!--MERMAID_PLACEHOLDER_{idx}-->"

    pattern = r"```mermaid\s*\n(.*?)\n```"
    processed_md = re.sub(pattern, stash_mermaid, md_content, flags=re.DOTALL)

    html_body = markdown.markdown(processed_md, extensions=['tables', 'fenced_code'])

    # Restore mermaid blocks as <div class="mermaid">
    for idx, block in enumerate(mermaid_blocks):
        placeholder = f"<p>&lt;!--MERMAID_PLACEHOLDER_{idx}--&gt;</p>"
        div_block = f'<div class="mermaid">\n{block}\n</div>'
        if placeholder in html_body:
            html_body = html_body.replace(placeholder, div_block)
        else:
            html_body = html_body.replace(f"<!--MERMAID_PLACEHOLDER_{idx}-->", div_block)

    with open('/tmp/mermaid.min.js', 'r', encoding='utf-8') as f:
        mermaid_js = f.read()

    html_doc = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Báo cáo Kỹ thuật Phần mềm - Week 04 - 524H0195</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #1e293b;
        max-width: 960px;
        margin: 0 auto;
        padding: 40px 20px;
        background-color: #ffffff;
    }}
    h1, h2, h3, h4 {{
        color: #0f172a;
        font-weight: 700;
    }}
    h1 {{
        border-bottom: 2px solid #0284c7;
        padding-bottom: 8px;
        margin-top: 30px;
    }}
    h2 {{
        color: #0369a1;
        margin-top: 25px;
    }}
    h3 {{
        color: #0f766e;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 14px;
    }}
    th, td {{
        border: 1px solid #cbd5e1;
        padding: 10px 14px;
        text-align: left;
    }}
    th {{
        background-color: #f1f5f9;
        font-weight: 600;
        color: #334155;
    }}
    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}
    blockquote {{
        border-left: 4px solid #0284c7;
        margin: 15px 0;
        padding: 10px 20px;
        background-color: #f0f9ff;
        color: #0369a1;
        font-style: italic;
    }}
    .mermaid {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        margin: 25px 0;
        text-align: center;
        page-break-inside: avoid;
    }}
    code {{
        background-color: #f1f5f9;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: Consolas, Monaco, monospace;
        font-size: 90%;
        color: #e11d48;
    }}
    hr {{
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 30px 0;
    }}
    @media print {{
        body {{
            max-width: 100%;
            padding: 20px;
            font-size: 11pt;
        }}
        .mermaid {{
            page-break-inside: avoid;
        }}
        h1, h2, h3 {{
            page-break-after: avoid;
        }}
    }}
</style>
<script>
{mermaid_js}
</script>
<script>
    mermaid.initialize({{
        startOnLoad: true,
        theme: 'default',
        securityLevel: 'loose',
        flowchart: {{ useMaxWidth: false, htmlLabels: true }},
        sequence: {{ useMaxWidth: false, showSequenceNumbers: true }}
    }});
</script>
</head>
<body>
{html_body}
</body>
</html>"""

    with open('/home/towfienes/TDTU/SE/524H0195_NgoLamTien_Lab04_Report.html', 'w', encoding='utf-8') as f:
        f.write(html_doc)
    print("HTML conversion successful!")

if __name__ == "__main__":
    main()
