import os
from PIL import Image

IMG_DIR = '/home/towfienes/TDTU/SE/images'
os.makedirs(IMG_DIR, exist_ok=True)

files = [
    ('/tmp/test_render0.png', os.path.join(IMG_DIR, 'exercise1_1_mailbox_email_class.png')),
    ('/tmp/test_render1.png', os.path.join(IMG_DIR, 'exercise1_2_courseware_cms_class.png')),
    ('/tmp/test_render2.png', os.path.join(IMG_DIR, 'exercise2_course_registration_sequence.png')),
    ('/tmp/test_render3.png', os.path.join(IMG_DIR, 'exercise3_atm_cash_withdrawal_activity.png')),
]

for src, dst in files:
    img = Image.open(src)
    # Autocrop white borders
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
    cropped.save(dst, 'PNG', optimize=True)
    print(f"Processed {dst}: {cropped.size}")

print("All 4 images processed and saved!")
