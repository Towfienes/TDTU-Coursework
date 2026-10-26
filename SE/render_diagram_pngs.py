import os
import re
import subprocess
from PIL import Image

SE_DIR = '/home/towfienes/TDTU/SE'
IMG_DIR = os.path.join(SE_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

with open('/tmp/mermaid.min.js', 'r', encoding='utf-8') as f:
    mjs = f.read()

with open(os.path.join(SE_DIR, '524H0195_NgoLamTien_Lab04_Report.md'), 'r', encoding='utf-8') as f:
    md = f.read()

blocks = re.findall(r'```mermaid\s*\n(.*?)\n```', md, flags=re.DOTALL)

img_filenames = [
    'exercise1_1_mailbox_email_class.png',
    'exercise1_2_courseware_cms_class.png',
    'exercise2_course_registration_sequence.png',
    'exercise3_atm_cash_withdrawal_activity.png'
]

for i, block in enumerate(blocks):
    escaped_block = block.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    html_page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
    margin: 0;
    padding: 30px;
    background: #ffffff;
    display: inline-block;
}}
#container {{
    display: inline-block;
    background: #ffffff;
}}
</style>
<script>{mjs}</script>
</head>
<body>
<div id="container"></div>
<script>
async function render() {{
    mermaid.initialize({{
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose'
    }});
    const res = await mermaid.render('diagram_{i}', `{escaped_block}`);
    const cont = document.getElementById('container');
    cont.innerHTML = res.svg;
    const svg = cont.querySelector('svg');
    svg.removeAttribute('style');
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    
    const vb = svg.viewBox.baseVal;
    const w = Math.ceil(vb.width);
    const h = Math.ceil(vb.height);
    
    // Store in a meta tag or title
    document.title = w + 'x' + h;
}}
render();
</script>
</body>
</html>"""

    tmp_html = f'/tmp/shot_{i}.html'
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_page)

    res = subprocess.run([
        'chromium', '--no-sandbox', '--headless', '--disable-gpu', '--virtual-time-budget=3000',
        '--dump-dom', tmp_html
    ], capture_output=True, text=True)

    m = re.search(r'<title>(\d+)x(\d+)</title>', res.stdout)
    if m:
        w_orig, h_orig = int(m.group(1)), int(m.group(2))
        win_w = w_orig + 80
        win_h = h_orig + 80
        print(f"Diagram {i} viewBox: {w_orig}x{h_orig} -> Window: {win_w}x{win_h}")
    else:
        win_w, win_h = 1200, 1600
        print(f"Diagram {i} fallback window: {win_w}x{win_h}")

    raw_png = f'/tmp/raw_diagram_{i}.png'
    subprocess.run([
        'chromium', '--no-sandbox', '--headless', '--disable-gpu',
        '--force-device-scale-factor=2',
        f'--window-size={win_w},{win_h}',
        f'--screenshot={raw_png}',
        tmp_html
    ], check=True)

    img = Image.open(raw_png)
    bbox = img.getbbox()
    if bbox:
        pad = 20
        left = max(0, bbox[0] - pad)
        top = max(0, bbox[1] - pad)
        right = min(img.width, bbox[2] + pad)
        bottom = min(img.height, bbox[3] + pad)
        cropped = img.crop((left, top, right, bottom))
    else:
        cropped = img

    out_file = os.path.join(IMG_DIR, img_filenames[i])
    cropped.save(out_file, 'PNG')
    print(f"Saved {out_file} (resolution: {cropped.size})")

print("All diagrams rendered in High-DPI Retina resolution!")
