import json
import re

with open('/home/towfienes/TDTU/ML/MidTerm/presentation/slides_data.json', 'r', encoding='utf-8') as f:
    slides = json.load(f)

html_template = '''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>TDTU Machine Learning — Mobile Slide Viewer</title>
  <script src="qrcode.min.js"></script>
  <style>
    :root {
      --bg: #090d16;
      --card-bg: rgba(22, 27, 40, 0.85);
      --border: rgba(255, 255, 255, 0.1);
      --accent: #2563eb;
      --accent-glow: rgba(37, 99, 235, 0.35);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      min-height: 100dvh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* Top Bar */
    header {
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand img { height: 28px; width: auto; }
    .brand-title {
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.5px;
      line-height: 1.2;
    }
    .brand-sub {
      font-size: 11px;
      color: var(--text-muted);
    }
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .btn-action {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .btn-action:hover, .btn-action.active {
      background: var(--accent);
      border-color: var(--accent);
      box-shadow: 0 0 12px var(--accent-glow);
    }

    /* Main Container */
    main {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      position: relative;
    }

    /* iPhone Frame (on Desktop) */
    .device-wrapper {
      position: relative;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      width: 100%;
      max-width: 420px;
    }
    .device-wrapper.landscape {
      max-width: 860px;
    }
    .device-wrapper.full-desktop {
      max-width: 1100px;
    }
    .device-wrapper.full-desktop .phone-frame {
      border: none;
      border-radius: 12px;
      padding: 0;
      box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    }
    .device-wrapper.full-desktop .dynamic-island,
    .device-wrapper.full-desktop .status-bar {
      display: none;
    }

    .phone-frame {
      background: #000;
      border: 10px solid #27272a;
      border-radius: 54px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), 0 0 0 2px rgba(255, 255, 255, 0.1);
      overflow: hidden;
      position: relative;
      display: flex;
      flex-direction: column;
      aspect-ratio: 9 / 19.5;
    }
    .device-wrapper.landscape .phone-frame {
      aspect-ratio: 19.5 / 9;
      border-radius: 40px;
    }

    /* Status Bar */
    .status-bar {
      height: 44px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      font-size: 13px;
      font-weight: 600;
      z-index: 20;
      color: #fff;
      background: #000;
      user-select: none;
    }
    .dynamic-island {
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      width: 110px;
      height: 28px;
      background: #000;
      border-radius: 20px;
      z-index: 30;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 8px;
    }
    .camera-lens {
      width: 10px;
      height: 10px;
      background: #111;
      border-radius: 50%;
      border: 1px solid #222;
      box-shadow: inset 0 0 2px #0a192f;
    }
    .sensor {
      width: 10px;
      height: 10px;
      background: #050b14;
      border-radius: 50%;
    }

    /* Slide Stage inside Device */
    .screen-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: #111;
      position: relative;
      overflow: hidden;
    }
    .viewport-box {
      width: 100%;
      aspect-ratio: 16 / 9;
      background: #fff;
      position: relative;
      overflow: hidden;
      user-select: none;
    }
    .slide-render {
      position: absolute;
      top: 0;
      left: 0;
      width: 1279.97px;
      height: 720.00px;
      transform-origin: top left;
      display: none;
      background: #fff;
    }
    .slide-render.active {
      display: block;
    }

    /* Touch Tap Zones */
    .tap-zone {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 25%;
      z-index: 15;
      cursor: pointer;
    }
    .tap-left { left: 0; }
    .tap-right { right: 0; }

    /* Progress bar */
    .progress-bar-container {
      height: 3px;
      background: rgba(255, 255, 255, 0.1);
      width: 100%;
    }
    .progress-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #3b82f6, #60a5fa);
      width: 7.14%;
      transition: width 0.3s ease;
    }

    /* Control Bar under slide */
    .deck-controls {
      background: #18181b;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      z-index: 20;
    }
    .ctrl-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #fff;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
    }
    .ctrl-btn:hover {
      background: var(--accent);
    }
    .slide-indicator {
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Notes Drawer (Bottom Sheet) */
    .notes-drawer {
      flex: 1;
      background: #12141a;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 14px 16px;
    }
    .speaker-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    .speaker-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .badge-tien { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #3b82f6; }
    .badge-thanh { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
    .badge-tam { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid #a855f7; }
    
    .time-badge {
      font-size: 11px;
      color: var(--text-muted);
      font-variant-numeric: tabular-nums;
    }
    .slide-title-label {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
    }
    .speech-box {
      background: rgba(255, 255, 255, 0.03);
      border-left: 3px solid #3b82f6;
      padding: 10px 12px;
      border-radius: 0 8px 8px 0;
      font-size: 13px;
      line-height: 1.6;
      color: #cbd5e1;
      margin-bottom: 12px;
    }
    .tts-btn {
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid #3b82f6;
      color: #60a5fa;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      align-self: flex-start;
    }

    /* Modal QR Code */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 100;
      padding: 20px;
    }
    .modal-overlay.open { display: flex; }
    .modal-card {
      background: #18181b;
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 24px;
      max-width: 360px;
      width: 100%;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8);
      position: relative;
    }
    .modal-close {
      position: absolute;
      top: 14px;
      right: 14px;
      background: none;
      border: none;
      color: #94a3b8;
      font-size: 20px;
      cursor: pointer;
    }
    .qr-container {
      background: #fff;
      padding: 14px;
      border-radius: 12px;
      display: inline-block;
      margin: 16px 0;
    }
    .qr-container img, .qr-container canvas {
      display: block;
      width: 180px;
      height: 180px;
    }
    .url-chip {
      background: rgba(255, 255, 255, 0.08);
      padding: 8px 12px;
      border-radius: 8px;
      font-family: monospace;
      font-size: 12px;
      color: #38bdf8;
      word-break: break-all;
    }

    /* NATIVE MOBILE OVERRIDES (on actual phone) */
    @media (max-width: 768px) {
      body { background: #000; }
      header { padding: 8px 12px; }
      .brand-title { font-size: 12px; }
      .brand-sub { display: none; }
      .btn-mode, .btn-rotate { display: none; }
      main { padding: 0; align-items: stretch; }
      .device-wrapper {
        max-width: 100% !important;
        height: 100%;
        display: flex;
        flex-direction: column;
      }
      .phone-frame {
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        aspect-ratio: auto !important;
        flex: 1;
      }
      .status-bar, .dynamic-island { display: none !important; }
    }
  </style>
</head>
<body>

  <!-- Top Header -->
  <header>
    <div class="brand">
      <img src="figures/tdtu-logo.png" alt="TDTU">
      <div>
        <div class="brand-title">TDTU · MACHINE LEARNING</div>
        <div class="brand-sub">Báo cáo Giữa kỳ · Slide & Lời thoại Thuyết trình</div>
      </div>
    </div>
    <div class="nav-actions">
      <button class="btn-action btn-mode" id="btnMode" onclick="toggleMode()">
        <span>💻</span> Màn hình rộng
      </button>
      <button class="btn-action btn-rotate" id="btnRotate" onclick="toggleRotate()">
        <span>🔄</span> Xoay ngang
      </button>
      <button class="btn-action" style="background:#0284c7;border-color:#0284c7;" onclick="openQR()">
        <span>📲</span> Mở trên điện thoại
      </button>
    </div>
  </header>

  <!-- Main View -->
  <main>
    <div class="device-wrapper" id="deviceWrapper">
      <div class="phone-frame">
        <!-- Status Bar -->
        <div class="status-bar">
          <span id="liveClock">09:41</span>
          <div style="display:flex;gap:6px;align-items:center;">
            <span>5G</span>
            <span>100%</span>
          </div>
        </div>
        <div class="dynamic-island">
          <div class="sensor"></div>
          <div class="camera-lens"></div>
        </div>

        <!-- Phone Screen Content -->
        <div class="screen-content">
          
          <!-- Slide Stage -->
          <div class="viewport-box" id="viewportBox">
            <div class="tap-zone tap-left" onclick="prevSlide()"></div>
            <div class="tap-zone tap-right" onclick="nextSlide()"></div>
'''

for s in slides:
    active_cls = ' active' if s['index'] == 1 else ''
    html_template += f'''            <div class="slide-render{active_cls}" id="slide-{s['index']}">
{s['html']}
            </div>\n'''

html_template += '''          </div>

          <!-- Progress bar -->
          <div class="progress-bar-container">
            <div class="progress-bar-fill" id="progressBar"></div>
          </div>

          <!-- Slide Controls Bar -->
          <div class="deck-controls">
            <button class="ctrl-btn" onclick="prevSlide()" title="Slide trước">◀</button>
            <div class="slide-indicator">
              <span id="slideNum">Slide 1</span>
              <span style="color:#64748b;">/ 14</span>
            </div>
            <button class="ctrl-btn" onclick="nextSlide()" title="Slide sau">▶</button>
          </div>

          <!-- Notes & Speech Drawer -->
          <div class="notes-drawer" id="notesDrawer">
            <div class="speaker-meta">
              <div class="speaker-badge badge-tien" id="speakerBadge">🔵 Ngô Lâm Tiến</div>
              <div class="time-badge" id="timeBadge">⏱️ 0:00 (~24s)</div>
            </div>
            <div class="slide-title-label" id="slideTitleLabel">Trang bìa</div>
            <div class="speech-box" id="speechBox">
              Kính thưa thầy và các bạn. Nhóm em gồm ba thành viên xin trình bày báo cáo giữa kỳ môn Introduction to Machine Learning...
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              <button class="tts-btn" onclick="speakCurrentSlide()">
                <span>🔊</span> Đọc lời thoại (Speech)
              </button>
              <a href="../output/pdf/midterm_report.pdf" target="_blank" class="tts-btn" style="background:rgba(16,185,129,0.15);border-color:#10b981;color:#34d399;text-decoration:none;">
                <span>📄</span> Mở PDF Báo cáo
              </a>
              <a href="midterm_presentation.pptx" download class="tts-btn" style="background:rgba(245,158,11,0.15);border-color:#f59e0b;color:#fbbf24;text-decoration:none;">
                <span>📊</span> Tải PPTX
              </a>
            </div>
          </div>

        </div>
      </div>
    </div>
  </main>

  <!-- QR Code Modal -->
  <div class="modal-overlay" id="qrModal" onclick="closeQR(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeQR()">&times;</button>
      <h3 style="font-size:16px;margin-bottom:6px;">Quét mã mở trên Điện thoại</h3>
      <p style="font-size:12px;color:var(--text-muted);">Kết nối chung Wi-Fi và mở máy ảnh điện thoại quét mã QR bên dưới:</p>
      <div class="qr-container">
        <img src="figures/qr_code.png" alt="QR Code">
      </div>
      <div class="url-chip">http://192.168.1.29:8888/</div>
      <p style="font-size:11px;color:#64748b;margin-top:10px;">Vuốt tay trái/phải để chuyển slide · Có sẵn kịch bản nói tiếng Việt</p>
    </div>
  </div>

  <script>
    const slidesData = ''' + json.dumps(slides, ensure_ascii=False) + ''';
    let currentSlide = 1;
    const totalSlides = slidesData.length;

    // Responsive Scale Calculation
    function updateSlideScale() {
      const box = document.getElementById('viewportBox');
      if (!box) return;
      const w = box.clientWidth;
      const scale = w / 1279.97;
      document.querySelectorAll('.slide-render').forEach(el => {
        el.style.transform = 'scale(' + scale + ')';
      });
    }

    window.addEventListener('resize', updateSlideScale);
    window.addEventListener('DOMContentLoaded', updateSlideScale);

    function showSlide(index) {
      if (index < 1 || index > totalSlides) return;
      currentSlide = index;

      document.querySelectorAll('.slide-render').forEach((el, idx) => {
        el.classList.toggle('active', (idx + 1) === currentSlide);
      });

      document.getElementById('slideNum').textContent = 'Slide ' + currentSlide;
      document.getElementById('progressBar').style.width = ((currentSlide / totalSlides) * 100) + '%';

      const data = slidesData[currentSlide - 1];
      document.getElementById('slideTitleLabel').textContent = data.title;
      document.getElementById('speechBox').textContent = data.script;
      document.getElementById('timeBadge').textContent = '⏱️ ' + data.start + ' (~' + data.duration + ')';

      const badge = document.getElementById('speakerBadge');
      badge.textContent = '🎤 ' + data.speaker;
      badge.className = 'speaker-badge ' + (
        data.speaker.includes('Tiến') ? 'badge-tien' :
        data.speaker.includes('Thành') ? 'badge-thanh' : 'badge-tam'
      );

      updateSlideScale();
    }

    function nextSlide() {
      if (currentSlide < totalSlides) showSlide(currentSlide + 1);
    }
    function prevSlide() {
      if (currentSlide > 1) showSlide(currentSlide - 1);
    }

    // Touch Swipe Support
    let touchStartX = 0;
    let touchEndX = 0;
    const viewportBox = document.getElementById('viewportBox');

    viewportBox.addEventListener('touchstart', e => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    viewportBox.addEventListener('touchend', e => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });

    function handleSwipe() {
      const diff = touchEndX - touchStartX;
      if (Math.abs(diff) > 40) {
        if (diff < 0) nextSlide();
        else prevSlide();
      }
    }

    // Keyboard navigation
    window.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      }
    });

    // View Modes
    let isLandscape = false;
    let isFullDesktop = false;

    function toggleRotate() {
      const wrapper = document.getElementById('deviceWrapper');
      isLandscape = !isLandscape;
      wrapper.classList.toggle('landscape', isLandscape);
      document.getElementById('btnRotate').classList.toggle('active', isLandscape);
      setTimeout(updateSlideScale, 300);
    }

    function toggleMode() {
      const wrapper = document.getElementById('deviceWrapper');
      isFullDesktop = !isFullDesktop;
      wrapper.classList.toggle('full-desktop', isFullDesktop);
      document.getElementById('btnMode').classList.toggle('active', isFullDesktop);
      document.getElementById('btnMode').innerHTML = isFullDesktop ? 
        '<span>📱</span> Khung điện thoại' : '<span>💻</span> Màn hình rộng';
      setTimeout(updateSlideScale, 300);
    }

    // QR Modal
    function openQR() {
      document.getElementById('qrModal').classList.add('open');
    }
    function closeQR() {
      document.getElementById('qrModal').classList.remove('open');
    }

    // Live Clock
    function updateClock() {
      const now = new Date();
      const hrs = String(now.getHours()).padStart(2, '0');
      const mins = String(now.getMinutes()).padStart(2, '0');
      document.getElementById('liveClock').textContent = hrs + ':' + mins;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Text to Speech
    function speakCurrentSlide() {
      if (!('speechSynthesis' in window)) {
        alert('Trình duyệt không hỗ trợ Text-to-Speech.');
        return;
      }
      window.speechSynthesis.cancel();
      const text = document.getElementById('speechBox').textContent;
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'vi-VN';
      utterance.rate = 1.0;
      window.speechSynthesis.speak(utterance);
    }

    // Init
    showSlide(1);
    setTimeout(updateSlideScale, 100);
  </script>
</body>
</html>
'''

with open('/home/towfienes/TDTU/ML/MidTerm/presentation/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Successfully built presentation/index.html!')
