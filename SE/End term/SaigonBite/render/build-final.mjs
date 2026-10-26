// Build the consolidated final report: Parts 1, 2 and 3 in one bookmarked PDF.
// Front matter is numbered in roman, the body restarts at 1, and the bookmark tree comes
// from Chromium's outline generation so it survives as a real, navigable PDF outline.
import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import { CSS, htmlToPdf, pdfText, CHROME, GEOM } from './lib.mjs';
import { markdownToHtml } from './md.mjs';
import { renderBlocks, sectionHeadings, sectionHeadingHtml } from './blocks.mjs';
import { part1 } from './content-part1.mjs';
import * as fm from './frontmatter.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const OUT = path.join(ROOT, 'docs', 'final', 'SAIGONBITE_FULL_REPORT.pdf');
const TMP = path.join(HERE, '.build');

const EXTRA_CSS = `
.toc-entry.lvl3 { font-weight: normal; padding-left: 2.4cm; font-size: 12pt; }
.toc-entry.lvl2 .t, .toc-entry.lvl3 .t { white-space: normal; }
pre { font-family: "Courier New", monospace; font-size: 9pt; line-height: 1.25;
      background: #f6f6f6; border: 0.5pt solid #999; padding: 6pt; margin: 6pt 0;
      white-space: pre-wrap; text-align: left; }
blockquote { margin: 6pt 0 6pt 1.27cm; padding-left: 8pt; border-left: 2pt solid #888; font-style: italic; }
code { font-family: "Courier New", monospace; font-size: 10pt; }
a { color: #000; text-decoration: none; }
`;

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '');

// ---------------------------------------------------------------- assemble content
const sections = part1.body.map((fn) => fn());
const isBack = (s) => s.kind === 'appendix' || s.kind === 'references';
const front = sections.filter((s) => !isBack(s));
const back = sections.filter(isBack);

// diagrams for the Part 2 markdown
const images = {};
try {
  for (const f of await fs.readdir(path.join(ROOT, 'docs', 'part2-design', 'diagrams'))) {
    if (f.endsWith('.svg')) {
      images[f] = await fs.readFile(
        path.join(ROOT, 'docs', 'part2-design', 'diagrams', f), 'utf8');
    }
  }
} catch { /* no diagrams */ }

const part2md = await fs.readFile(path.join(ROOT, 'docs', 'part2-design', 'part2.md'), 'utf8');
const part3md = await fs.readFile(path.join(ROOT, 'docs', 'part3-qa', 'part3.md'), 'utf8');

const p2 = markdownToHtml(`# PART 2. SOFTWARE DESIGN, ARCHITECTURE AND UI/UX\n\n${part2md}`, { images });
const p3 = markdownToHtml(`# PART 3. IMPLEMENTATION, TESTING AND PRODUCT DEMO\n\n${part3md}`, { images });

// ---- headings and figures, in document order
const toc = [];
const figures = [];
for (const s of front) {
  for (const h of sectionHeadings(s)) {
    if (h.figure) figures.push({ caption: h.caption, key: h.key });
    else toc.push({ level: h.level, label: h.label, key: h.key });
  }
}
toc.push({ level: 1, label: 'PART 2. SOFTWARE DESIGN, ARCHITECTURE AND UI/UX',
  key: 'PART 2. SOFTWARE DESIGN, ARCHITECTURE AND UI/UX' });
for (const h of p2.headings.slice(1)) toc.push({ ...h, key: h.label });   // part divider already added
for (const f of p2.figures) figures.push({ caption: f.caption, key: f.caption });
toc.push({ level: 1, label: 'PART 3. IMPLEMENTATION, TESTING AND PRODUCT DEMO',
  key: 'PART 3. IMPLEMENTATION, TESTING AND PRODUCT DEMO' });
for (const h of p3.headings.slice(1)) toc.push({ ...h, key: h.label });
for (const f of sections.filter(isBack)) {
  for (const h of sectionHeadings(f)) {
    if (h.figure) figures.push({ caption: h.caption, key: h.key });
    else toc.push({ level: h.level, label: h.label, key: h.key });
  }
}

// ---- body HTML in the required order
const bodyHtml = [
  ...front.map((s) => sectionHeadingHtml(s) + '\n' + renderBlocks(s.blocks)),
  p2.html,
  p3.html,
  ...back.map((s) => sectionHeadingHtml(s) + '\n' + renderBlocks(s.blocks)),
].join('\n');

// ---------------------------------------------------------------- two-pass render
const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });

const tocHtml = (numbers) => toc.map((h, i) => {
  const lvl = Math.min(h.level, 3);
  return `<div class="toc-entry lvl${lvl}"><span class="t">${h.label}</span>`
    + `<span class="dots"></span><span class="pg">${numbers[i] ?? 1}</span></div>`;
}).join('\n');

const lofHtml = (numbers) => figures.map((f, i) =>
  `<div class="lof-entry"><span class="t">${f.caption}</span>`
  + `<span class="dots"></span><span class="pg">${numbers[i] ?? 1}</span></div>`).join('\n');

const docHtml = (tocNums, lofNums) => `<!doctype html><html><head><meta charset="utf-8">
<style>${CSS}${EXTRA_CSS}</style></head><body>
${fm.coverOuter('Consolidated Final Report — Parts 1, 2 and 3')}
${fm.coverInner('Consolidated Final Report — Parts 1, 2 and 3')}
${fm.acknowledgement('Parts 1 to 3 of the final report')}
${fm.declaration()}
<h1 class="centered">TABLE OF CONTENT</h1>
${tocHtml(tocNums)}
<h1 class="centered">LIST OF FIGURES</h1>
${lofHtml(lofNums)}
${bodyHtml}
</body></html>`;

async function render(tocNums, lofNums) {
  const page = await browser.newPage();
  await page.setContent(docHtml(tocNums, lofNums), { waitUntil: 'load' });
  const buf = await page.pdf({
    format: 'A4', printBackground: true, outline: true, tagged: true,
    margin: { top: '35mm', bottom: '30mm', left: '35mm', right: '20mm' },
  });
  await page.close();
  return buf;
}

// pass A: placeholder numbers, only to learn pagination
const probe = await render([], []);
const probePages = pdfText(probe, TMP, 'final-probe.pdf').split('\f');
// The chapter title also appears in the table of contents, so the body is located by a
// sentence that only exists in the body itself.
const BODY_MARKER = 'SaigonBite is a planned network of cloud kitchens';
const bodyStart = probePages.findIndex((p) => norm(p).includes(norm(BODY_MARKER)));
if (bodyStart < 0) throw new Error('could not locate the first body page');

const pageOf = (key) => {
  const n = norm(key);
  for (let i = bodyStart; i < probePages.length; i++) {
    if (norm(probePages[i]).includes(n)) return i - bodyStart + 1;
  }
  return null;
};
const tocNums = toc.map((h) => pageOf(h.key));
const lofNums = figures.map((f) => pageOf(f.caption));
const missing = toc.filter((_, i) => tocNums[i] === null).map((h) => h.label)
  .concat(figures.filter((_, i) => lofNums[i] === null).map((f) => f.caption));
if (missing.length) console.warn('anchors not found:', missing.slice(0, 5));

// pass B: real numbers
const finalPdf = await render(tocNums, lofNums);

// ---------------------------------------------------------------- page numbering
const doc = await PDFDocument.load(finalPdf);
const font = await doc.embedFont(StandardFonts.TimesRoman);
const roman = (n) => {
  const map = [[1000, 'm'], [900, 'cm'], [500, 'd'], [400, 'cd'], [100, 'c'], [90, 'xc'],
    [50, 'l'], [40, 'xl'], [10, 'x'], [9, 'ix'], [5, 'v'], [4, 'iv'], [1, 'i']];
  let out = '', v = n;
  for (const [k, s] of map) while (v >= k) { out += s; v -= k; }
  return out;
};
doc.getPages().forEach((pg, i) => {
  if (i < 2) return;                                   // covers carry no number
  const inFront = i < bodyStart;
  const label = inFront ? roman(i - 1) : String(i - bodyStart + 1);
  const size = (inFront && i - 1 <= 2) ? 12 : 13;
  const w = font.widthOfTextAtSize(label, size);
  pg.drawText(label, {
    x: GEOM.axisX - w / 2, y: GEOM.pageH - GEOM.numTopY, size, font, color: rgb(0, 0, 0),
  });
});
const bytes = Buffer.from(await doc.save());
await fs.mkdir(path.dirname(OUT), { recursive: true });
await fs.writeFile(OUT, bytes);
await browser.close();

// ---------------------------------------------------------------- verify
const pages = doc.getPageCount();
const finalText = pdfText(bytes, TMP, 'final-check.pdf').split('\f');
const problems = [];
for (let i = 0; i < toc.length; i++) {
  const want = tocNums[i];
  const idx = finalText.findIndex((p, j) => j >= bodyStart && norm(p).includes(norm(toc[i].key)));
  const actual = idx < 0 ? null : idx - bodyStart + 1;
  if (want === null || actual !== want) {
    problems.push(`TOC ${toc[i].label}: printed ${want}, actual ${actual}`);
  }
}
const cents = execFileSync('pdfinfo', [OUT]).toString().match(/Pages:\s+(\d+)/);
console.log(JSON.stringify({
  file: OUT,
  pages, bodyStartPage: bodyStart + 1,
  bodyPages: pages - bodyStart,
  tocEntries: toc.length, figures: figures.length,
  declaredPages: Number(cents[1]),
  problems: problems.slice(0, 8), problemCount: problems.length,
}, null, 2));
if (problems.length) process.exitCode = 1;
