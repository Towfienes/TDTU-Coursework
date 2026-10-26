#!/usr/bin/env node
/**
 * Build Presentation 1 — SaigonBite Solution Pitch.
 *
 * Five slides, 16:9 (960 x 540 pt), Times New Roman, monochrome framing with a
 * coloured analytical visuals and monochrome framing. HTML is written to slides/deck.html and
 * printed to slides/Part1_Pitch.pdf by the workspace Chromium build.
 *
 *   node slides/build-deck.mjs
 *
 * Names, student IDs, tier, course and semester are read from config/team.json.
 * A member still marked TBD is rendered as TBD — never invented.
 *
 * The build refuses to report success if any slide overflows the canvas: it
 * measures every element against the content box before printing.
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..');
const tdtu = path.resolve(repo, '../../..');
const require = createRequire(path.join(repo, 'render/'));
const { chromium } = require(path.join(repo, 'render/node_modules/playwright-core'));

const CHROME = '/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';
const OUT_PDF = path.join(here, 'Part1_Pitch.pdf');
const OUT_HTML = path.join(here, 'deck.html');

const team = JSON.parse(fs.readFileSync(path.join(repo, 'config/team.json'), 'utf8'));
const logoB64 = fs
  .readFileSync(path.join(tdtu, 'docs/report-reference/tdtu-logo.png'))
  .toString('base64');

const members = team.members;
const ACCENT = '#111111';      // the monochrome framing
const GREY = '#5A5A5A';
const HAIR = '#C4C4C4';

/* ------------------------------------------------------------------ CSS -- */
const CSS = `
@page { size: 960pt 540pt; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; }
body { font-family: "Times New Roman", "Liberation Serif", serif; color: #111; }
.slide { position: relative; width: 960pt; height: 540pt; overflow: hidden;
         background: #fff; padding: 38pt 60pt 0 60pt; }
.slide + .slide { break-before: page; page-break-before: always; }

.header-logo { position: absolute; top: 34pt; left: 60pt; width: 38pt; height: 21pt; }
.kicker { padding-left: 50pt; font-size: 16pt; letter-spacing: .16em; text-transform: uppercase;
          color: ${GREY}; }
.kicker .n { color: ${ACCENT}; font-weight: 700; margin-right: 10pt; }
h1.t { font-size: 36pt; line-height: 1.14; font-weight: 700; margin: 6pt 0 0;
       letter-spacing: -.004em; }
.standfirst { font-size: 20pt; line-height: 1.34; font-style: italic; color: #2B2B2B;
              margin: 7pt 0 0; }
.hdr { border-bottom: .75pt solid #111; margin-top: 12pt; }

.footer { position: absolute; left: 60pt; right: 60pt; bottom: 20pt;
          display: flex; justify-content: space-between; align-items: baseline;
          border-top: .75pt solid ${HAIR}; padding-top: 6pt;
          font-size: 16pt; color: ${GREY}; }
.footer b { font-weight: 700; color: #111; }

/* ---- 1 · title ---- */
.cover .uni { display: flex; align-items: center; gap: 14pt; }
.cover .uni img { width: 86pt; height: 47.6pt; display: block; }
.cover .uni .inst { font-size: 16pt; line-height: 1.35; letter-spacing: .05em;
                    text-transform: uppercase; color: ${GREY}; }
.cover .uni .inst b { color: #111; }
.cover .hair { border-bottom: .75pt solid #111; margin-top: 15pt; }
.cover .eyebrow { margin-top: 30pt; font-size: 16pt; letter-spacing: .16em;
                  text-transform: uppercase; color: ${ACCENT}; font-weight: 700; }
.cover h1 { font-size: 44pt; font-weight: 700; margin: 6pt 0 0; line-height: 1.05; }
.cover .sub { font-size: 24pt; font-style: italic; margin: 5pt 0 0; color: #222; }
.cover .bar { width: 132pt; height: 3pt; background: ${ACCENT}; margin-top: 18pt; }
.cover .team { margin-top: 18pt; }
.cover .who { font-size: 24pt; line-height: 1.44; }
.cover .who .id { font-size: 20pt; color: ${GREY}; margin-left: 10pt; }
.cover .who .tbd { font-weight: 700; }
.cover .meta { margin-top: 14pt; font-size: 20pt; color: #222; }
.cover .meta span { color: ${GREY}; padding: 0 8pt; }
.cover .agenda { position: absolute; left: 60pt; right: 60pt; bottom: 66pt;
                 display: flex; gap: 30pt; font-size: 16pt; color: ${GREY};
                 letter-spacing: .12em; text-transform: uppercase; }
.cover .agenda i { font-style: normal; color: ${ACCENT}; font-weight: 700;
                   margin-right: 7pt; }

/* ---- 2 · problem ---- */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 26pt;
         margin-top: 12pt; }
.stat { border-top: 2pt solid #111; padding-top: 7pt; }
.stat .n { font-size: 36pt; font-weight: 700; color: ${ACCENT}; line-height: 1;
           letter-spacing: -.01em; }
.stat .c { font-size: 20pt; line-height: 1.25; margin-top: 4pt; }
.stat .c b { font-weight: 700; }
.stat .c span { white-space: nowrap; }

.band { margin-top: 17pt; border-top: .75pt solid ${HAIR}; padding-top: 12pt; }
.brow { display: grid; grid-template-columns: 132pt 96pt 236pt 1fr;
        align-items: center; height: 31pt; font-size: 19pt; }
.brow .lab { font-weight: 700; }
.brow .rng { color: ${GREY}; }
.brow .eff { padding-left: 14pt; }
.track { height: 13pt; background: #F1F1F1; }
.track i { display: block; height: 100%; }
.b-quiet .lab { color: ${ACCENT}; }
.b-quiet .track i { background: #347348; }
.b-mid .track i { background: #49749a; }
.b-full .track i { background: #a45232; }
.bandnote { font-size: 17pt; color: ${GREY}; margin-top: 10pt; line-height: 1.32; }
.bandnote b { color: #111; }

/* ---- 3 · solution ---- */
.pillars { display: grid; grid-template-columns: repeat(3, 1fr); gap: 26pt;
           margin-top: 18pt; }
.pillar { border-top: 2pt solid #111; padding-top: 7pt; }
.pillar .k { font-size: 16pt; letter-spacing: .14em; color: ${ACCENT};
             font-weight: 700; }
.pillar h3 { font-size: 24pt; margin: 2pt 0 4pt; line-height: 1.14; }
.pillar p { font-size: 20pt; line-height: 1.24; margin: 0; color: #1E1E1E; }
.tiers { margin-top: 17pt; }
.tier { display: grid; grid-template-columns: 132pt 1fr; align-items: center;
        border: .75pt solid #111; height: 37pt; }
.tier + .tier { margin-top: 13pt; position: relative; }
.tier .lab { font-size: 17pt; font-weight: 700; letter-spacing: .03em;
             padding-left: 10pt; border-right: .75pt solid #111; height: 100%;
             display: flex; align-items: center; }
.tier .body { font-size: 17pt; padding-left: 12pt; white-space: nowrap; }
.tier.pres .lab { background: #EFEFEF; }
.tier.biz { border-width: 2pt; }
.tier.biz .lab { background: #F4E6E4; color: ${ACCENT}; }
.tier.biz .body b { color: ${ACCENT}; }
.tier.data .lab { background: #E8EFEE; color: #23564F; }
.arrow { position: absolute; left: 0; right: 0; top: -17pt; text-align: center;
         font-size: 17pt; line-height: 1; color: ${GREY}; }
.figcap { font-size: 17pt; color: ${GREY}; margin-top: 10pt; line-height: 1.3; }

/* ---- 4 · ownership ---- */
table.own { width: 100%; border-collapse: collapse; margin-top: 12pt;
            font-size: 17pt; }
table.own th { text-align: left; font-weight: 700; font-size: 16pt;
               letter-spacing: .05em; text-transform: uppercase;
               border-bottom: 1.5pt solid #111; padding: 0 8pt 6pt 0; }
table.own td { border-bottom: .5pt solid #D2D2D2; padding: 8pt 8pt 8pt 0;
               vertical-align: top; line-height: 1.22; }
table.own td.who b { display: block; }
table.own td.who span { font-size: 16pt; color: ${GREY}; }
table.own .uc b { font-weight: 700; }
table.own .uc .sub { font-size: 16pt; color: #333; }
table.own .tag { font-size: 16pt; color: ${ACCENT}; font-weight: 700;
                 letter-spacing: .05em; }
.rule-of-ownership { margin-top: 15pt; font-size: 20pt; line-height: 1.32;
                     border-left: 3pt solid ${ACCENT}; padding-left: 12pt; }
.rule-of-ownership b { font-weight: 700; }

/* ---- 5 · de-risking ---- */
.risks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24pt;
          margin-top: 18pt; }
.risk { border-top: 2pt solid #111; padding-top: 7pt; }
.risk .n { font-size: 36pt; font-weight: 700; color: ${ACCENT}; line-height: 1; }
.risk .t { font-size: 20pt; line-height: 1.21; margin-top: 4pt; }
.risk .t b { font-weight: 700; }
.decs { display: grid; grid-template-columns: 1fr 1fr; gap: 24pt; margin-top: 17pt; }
.kitem { display: grid; grid-template-columns: 58pt 1fr; gap: 6pt;
         padding: 7pt 0; border-bottom: .5pt solid #DCDCDC; }
.kitem:last-child { border-bottom: 0; }
.kitem .n { font-size: 24pt; font-weight: 700; color: ${ACCENT}; line-height: 1.05; }
.kitem .t { font-size: 18pt; line-height: 1.3; }
.kitem .t b { font-weight: 700; }
.dec { border: .75pt solid #111; padding: 9pt 13pt; }
.dec .h { font-size: 16pt; letter-spacing: .1em; text-transform: uppercase;
          color: ${ACCENT}; font-weight: 700; }
.dec h4 { font-size: 20pt; margin: 2pt 0 4pt; line-height: 1.14; }
.dec p { font-size: 19pt; line-height: 1.26; margin: 0; }
.dec .cost { font-size: 16pt; color: ${GREY}; margin-top: 4pt; font-style: italic; }
`;

/* --------------------------------------------------------------- helpers -- */
const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const isTbd = (v) => !v || String(v).trim().toUpperCase() === 'TBD';
const nameOf = (m) => (isTbd(m.full_name) ? '<span class="tbd">TBD</span>' : esc(m.full_name));
const idOf = (m) => (isTbd(m.student_id) ? 'TBD' : esc(m.student_id));

const m1 = members[0]; // 524H0195 — D, pricing, payment
const m2 = members[1]; // 524H0191 — A, R1
const m3 = members[2]; // third member — B, R2 (may be TBD)

const footer = (n) => `<div class="footer">
  <span><b>SaigonBite</b> — Cloud-Kitchen Food Delivery Hub</span>
  <span>${n} / 5</span></div>`;

const header = (num, kicker, title, standfirst) => `<img class="header-logo" src="data:image/png;base64,${logoB64}" alt="TDTU"><div class="kicker">
    <span class="n">${num}</span>${esc(kicker)}</div>
  <h1 class="t">${title}</h1>
  ${standfirst ? `<div class="standfirst">${standfirst}</div>` : ''}
  <div class="hdr"></div>`;

/* ---------------------------------------------------------------- slides -- */
const cover = `
<section class="slide cover">
  <div class="uni">
    <img src="data:image/png;base64,${logoB64}" alt="Ton Duc Thang University">
    <div class="inst"><b>Ton Duc Thang University</b><br>Faculty of Information Technology</div>
  </div>
  <div class="hair"></div>

  <div class="eyebrow">${esc(team.project.team_id)} · Presentation 1 · The Solution Pitch</div>
  <h1>SaigonBite</h1>
  <div class="sub">Cloud-Kitchen Food Delivery Hub for Ho Chi Minh City</div>
  <div class="bar"></div>

  <div class="team">
    <div class="who">${nameOf(m1)}<span class="id">${idOf(m1)}</span></div>
    <div class="who">${nameOf(m2)}<span class="id">${idOf(m2)}</span></div>
    <div class="who">${nameOf(m3)}<span class="id">${idOf(m3)}</span></div>
  </div>

  <div class="meta">
    ${esc(team.project.course)} (${esc(team.project.course_code)})<span>·</span>${esc(team.project.semester_label)}<span>·</span>${esc(team.project.semester)}<span>·</span>${esc(team.project.tier)}
  </div>

  <div class="agenda">
    <span><i>01</i>The problem</span><span><i>02</i>Our solution</span>
    <span><i>03</i>Ownership</span><span><i>04</i>De-risking</span>
  </div>
  ${footer(1)}
</section>`;

const problem = `
<section class="slide">
  ${header('01', 'The problem',
    'Customers and kitchen load',
    'Clear prices and controlled delivery for local customers and foreign tourists.')}

  <div class="stats">
    <div class="stat"><div class="n">2</div><div class="c">
      <b>customer groups</b>, one lifecycle: a ten-digit mobile, or a passport and a
      hotel room.</div></div>

    <div class="stat"><div class="n">5</div><div class="c">
      <b>payment methods</b>, three per group; only cash on delivery appears in both
      lists (BR13).</div></div>

    <div class="stat"><div class="n">18</div><div class="c">
      <b>business rules</b> define pricing, payment, lifecycle and registration (BR1–BR18).</div></div>
  </div>

  <div class="band">
    <div class="brow b-quiet"><span class="lab">Quiet Kitchen</span>
      <span class="rng">&lt; 30 %</span>
      <span class="track"><i style="width:30%"></i></span>
      <span class="eff">10 % off the food subtotal (BR7)</span></div>
    <div class="brow b-mid"><span class="lab">Normal</span>
      <span class="rng">30–&lt;90 %</span>
      <span class="track"><i style="width:60%"></i></span>
      <span class="eff">no Quiet Kitchen discount</span></div>
    <div class="brow b-full"><span class="lab">Refused</span>
      <span class="rng">≥ 90 %</span>
      <span class="track"><i style="width:10%"></i></span>
      <span class="eff">new orders refused (BR8)</span></div>
    <div class="bandnote">Load uses Confirmed + Preparing orders / capacity. <b>29.5 % qualifies</b> for the discount; <b>90 % refuses</b> a new order (BR7, BR8).</div>
  </div>
  ${footer(2)}
</section>`;

const solution = `
<section class="slide">
  ${header('02', 'Our solution', 'A layered, testable solution')}

  <div class="pillars">
    <div class="pillar">
      <div class="k">Pillar 01</div>
      <h3>Load-aware pricing</h3>
      <p>Nine calculation steps; round once at the end. Business services check item availability and hub membership.</p>
    </div>
    <div class="pillar">
      <div class="k">Pillar 02</div>
      <h3>A payment Strategy</h3>
      <p>One interface, one class per method and one registration; existing payment classes stay unchanged (NFR2).</p>
    </div>
    <div class="pillar">
      <div class="k">Pillar 03</div>
      <h3>An enforced lifecycle</h3>
      <p>Eight states, eight transitions, named actors. The business layer rejects
         the rest (BR15).</p>
    </div>
  </div>

  <div class="tiers">
    <div class="tier pres"><div class="lab">Presentation</div>
      <div class="body">Razor views · Bootstrap 5 · Chart.js · English / Vietnamese resources</div></div>
    <div class="tier biz"><div class="arrow">↓</div><div class="lab">Business</div>
      <div class="body"><b>PricingEngine</b> + validation · <b>OrderStateMachine</b> BR15–BR16 ·
        <b>IPaymentStrategy</b> + resolver</div></div>
    <div class="tier data"><div class="arrow">↓</div><div class="lab">Data</div>
      <div class="body">EF Core 8 Code-First · SQL Server 2022 · soft-delete filters · price snapshot</div></div>
  </div>
  <div class="figcap">Planned isolation: pricing and state rules can be unit-tested without a database or browser. Verify in Part 3.</div>
  ${footer(3)}
</section>`;

const ownership = `
<section class="slide">
  ${header('03', 'Ownership', 'Three owners, complete CRUD scopes')}

  <table class="own">
    <thead><tr>
      <th style="width:21%">Member</th>
      <th style="width:40%">Main use case — complete CRUD</th>
      <th style="width:22%">Secondary scope</th>
      <th style="width:17%">Report owned</th>
    </tr></thead>
    <tbody>
      <tr>
        <td class="who"><b>${nameOf(m1)}</b><span>${idOf(m1)}</span></td>
        <td class="uc"><b>D — Place and Manage Orders</b>
          <div class="sub"><span class="tag">MANDATORY</span> · pricing and payment Strategy</div></td>
        <td>C — Manage Vouchers</td>
        <td>—</td>
      </tr>
      <tr>
        <td class="who"><b>${nameOf(m2)}</b><span>${idOf(m2)}</span></td>
        <td class="uc"><b>A — Manage Menu &amp; Brands</b>
          <div class="sub">brands, items, availability, soft delete</div></td>
        <td>E — Manage User Accounts</td>
        <td>R1 — Revenue</td>
      </tr>
      <tr>
        <td class="who"><b>${nameOf(m3)}</b><span>${idOf(m3)}</span></td>
        <td class="uc"><b>B — Manage Hubs &amp; Capacity</b>
          <div class="sub">hubs, capacity, derived load</div></td>
        <td>F — Manage Deliveries<br>Change-request note</td>
        <td>R2 — Hub Utilization</td>
      </tr>
    </tbody>
  </table>

  <div class="rule-of-ownership">
    <b>Each member owns one main use case with complete CRUD.</b> R1 aggregates brand category
    and payment method, so it sits with A. R2 aggregates load and preparation time, so it sits
    with B. D carries the pricing engine and both customer types, so its owner takes no report.
  </div>
  ${footer(4)}
</section>`;

const derisk = `
<section class="slide">
  ${header('04', 'De-risking', 'Acceptance targets and open decisions')}

  <div class="risks">
    <div class="risk"><div class="n">4</div>
      <div class="t"><b>Tier 4 · cap ${team.project.tier_cap.toFixed(1)}/10:</b> Tier 3 + live sandbox API + interactive Admin dashboard + automated tests. Core MVC variant pending confirmation.</div></div>
    <div class="risk"><div class="n">20+</div>
      <div class="t"><b>Planned EP/BVA cases:</b> BR1–BR12 and BR14, plus at least five forbidden-transition tests.</div></div>
    <div class="risk"><div class="n">1</div>
      <div class="t"><b>New payment class</b> + one registration (NFR2). Assess other change requests separately.</div></div>
  </div>

  <div class="decs">
    <div class="dec">
      <div class="h">Ambiguity A1</div>
      <h4>Who assigns the shipper?</h4>
      <p>An Admin assigns an available shipper to a Ready order; store the shipper and assignment time. No automatic dispatch.</p>
      <div class="cost">Working assumption; instructor review pending.</div>
    </div>
    <div class="dec">
      <div class="h">Ambiguity A2</div>
      <h4>What is refunded after a failed delivery?</h4>
      <p>Refund online payments in full (simulated); COD collects nothing. Failed is terminal and excluded from revenue.</p>
      <div class="cost">Working assumption; instructor review pending.</div>
    </div>
  </div>
  ${footer(5)}
</section>`;

/* ----------------------------------------------------------------- build -- */
const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SaigonBite — Presentation 1 — The Solution Pitch</title>
<style>${CSS}</style>
</head>
<body>
${cover}
${problem}
${solution}
${ownership}
${derisk}
</body>
</html>`;

fs.writeFileSync(OUT_HTML, html, 'utf8');

const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto('file://' + OUT_HTML, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);

// Geometry gate: nothing may sit below the footer rule or outside the margins.
const report = await page.evaluate(() => {
  const LIMIT_BOTTOM_PT = 540 - 56;   // footer rule sits at 540 - 20 - text
  const LIMIT_RIGHT_PT = 960 - 60;
  return [...document.querySelectorAll('.slide')].map((s, i) => {
    const sr = s.getBoundingClientRect();
    const k = 960 / sr.width;         // px -> pt (1pt = 4/3px)
    const bad = [];
    for (const el of s.querySelectorAll('*')) {
      if (el.closest('.footer')) continue;
      const r = el.getBoundingClientRect();
      const bottom = (r.bottom - sr.top) * k;
      const right = (r.right - sr.left) * k;
      if (r.height > 0 && (bottom > LIMIT_BOTTOM_PT || right > LIMIT_RIGHT_PT + 1)) {
        bad.push(`${el.tagName.toLowerCase()}.${el.className || '-'} bottom=${bottom.toFixed(1)}pt right=${right.toFixed(1)}pt`);
      }
    }
    const worst = [...s.querySelectorAll('*')]
      .filter((el) => !el.closest('.footer'))
      .reduce((m, el) => Math.max(m, (el.getBoundingClientRect().bottom - sr.top) * k), 0);
    return { slide: i + 1, worst: worst.toFixed(1), overflow: bad.slice(0, 3) };
  });
});

const pdf = await page.pdf({
  preferCSSPageSize: true, printBackground: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
});
fs.writeFileSync(OUT_PDF, pdf);
await browser.close();

console.log(`wrote ${path.relative(repo, OUT_HTML)} (${html.length} bytes)`);
console.log(`wrote ${path.relative(repo, OUT_PDF)} (${pdf.length} bytes)`);
let bad = 0;
for (const r of report) {
  if (r.overflow.length) { bad++; console.log(`slide ${r.slide}: OVERFLOW (lowest element ${r.worst}pt of 484)`); for (const o of r.overflow) console.log("   ", o); } else { console.log(`slide ${r.slide}: ok (lowest element ${r.worst}pt of 484)`); }
}
console.log(bad ? `geometry: ${bad} slide(s) overflow` : 'geometry: all 5 slides inside the content box');
if (bad) process.exitCode = 1;
