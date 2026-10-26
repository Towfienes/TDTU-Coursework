// Build the TDTU-standard report PDFs from structured content.
// Pipeline: content -> HTML -> Chromium PDF -> paginate -> TOC/LOF -> stamp -> merge -> verify.
import { chromium } from 'playwright-core';
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const CHROME = process.env.CHROME_BIN ||
  '/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';

// Measured page geometry (TDTU_REPORT_STYLE.md §3, §5–§6)
export const GEOM = {
  pageW: 595.28, pageH: 841.89,          // A4 in pt
  mTop: 99.21, mBottom: 85.04,           // 3.5 cm / 3 cm
  mLeft: 99.21, mRight: 56.69,           // 3.5 cm / 2 cm
  contentW: 439.38,                      // 155 mm
  axisX: 318.90,                         // centre of the content area, not of the paper
  numTopY: 44.0,                         // page number near y = 43.75–44.08 pt
};

const CSS = `
@page { size: A4; margin: 35mm 20mm 30mm 35mm; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Times New Roman", "Liberation Serif", serif;
  font-size: 13pt; line-height: 1.5; color: #000;
  text-align: justify; hyphens: manual;
}
p { margin: 0 0 0 0; text-indent: 1.27cm; }
p.noindent { text-indent: 0; }
h1.chapter {
  font-size: 16pt; font-weight: bold; text-transform: uppercase;
  text-align: left; margin: 0 0 14pt 0; line-height: 1.5;
  break-before: page; page-break-before: always; break-after: avoid;
}
h1.chapter:first-child { break-before: auto; page-break-before: auto; }
h1.centered {
  font-size: 16pt; font-weight: bold; text-transform: uppercase;
  text-align: center; margin: 0 0 18pt 0; line-height: 1.5;
  break-before: page; page-break-before: always; break-after: avoid;
}
h2 { font-size: 14pt; font-weight: bold; text-align: left;
     margin: 12pt 0 4pt 0; line-height: 1.5; break-after: avoid; }
h3 { font-size: 14pt; font-weight: bold; font-style: italic; text-align: left;
     margin: 10pt 0 2pt 0; line-height: 1.5; break-after: avoid; }
ul, ol { margin: 4pt 0 4pt 0; padding-left: 1.27cm; }
li { margin: 0 0 2pt 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; font-size: 10pt;
        margin: 6pt 0 12pt 0; line-height: 1.25; text-align: left; }
th, td { border: 0.5pt solid #000; padding: 3pt 4pt; vertical-align: top; }
th { font-weight: bold; background: #f2f2f2; }
td.num, th.num { text-align: right; white-space: nowrap; }
td.ctr, th.ctr { text-align: center; }
.figure { text-align: center; margin: 10pt 0 6pt 0; break-inside: avoid; }
.figure svg { max-width: 100%; height: auto; }
.caption { font-size: 13pt; text-align: center; margin: 4pt 0 12pt 0;
           text-indent: 0; break-after: avoid; }
.eq { text-align: center; margin: 8pt 0; text-indent: 0;
      font-style: italic; font-size: 13pt; }
.ref { font-size: 13pt; text-indent: 0; padding-left: 1.27cm;
       text-indent: -1.27cm; margin-bottom: 6pt; text-align: left; }
.toc-entry, .lof-entry { display: flex; align-items: baseline;
  font-size: 13pt; text-indent: 0; margin: 0 0 3pt 0; line-height: 1.5; }
.toc-entry .t { white-space: nowrap; }
.toc-entry .dots, .lof-entry .dots {
  flex: 1 1 auto; border-bottom: 1px dotted #000; margin: 0 4pt;
  transform: translateY(-3pt); min-width: 12pt; }
.toc-entry .pg, .lof-entry .pg { white-space: nowrap; }
.toc-entry.lvl1 { font-weight: bold; text-transform: uppercase; }
.toc-entry.lvl2 { font-weight: normal; padding-left: 1.27cm; }
.lof-entry { font-weight: normal; }
.tbd { font-weight: bold; }
.cover { page-break-after: always; position: relative; height: 232mm; }
.cover .blk { position: absolute; left: 0; width: 155mm; text-align: center; }
`;

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Render one HTML document to a PDF buffer. */
async function htmlToPdf(browser, html, { footer = false } = {}) {
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  const buf = await page.pdf({
    format: 'A4', printBackground: true,
    margin: { top: '35mm', bottom: '30mm', left: '35mm', right: '20mm' },
    displayHeaderFooter: footer,
    headerTemplate: '<div></div>',
    footerTemplate: '<div></div>',
  });
  await page.close();
  return buf;
}

/** Number of pages in a PDF buffer, via pdf-lib. */
async function countPages(buf) {
  return (await PDFDocument.load(buf)).getPageCount();
}

/** Which 1-based page of `buf` contains `needle`, using pdftotext. */
function locatePage(buf, needle, tmpdir) {
  const f = path.join(tmpdir, 'probe.pdf');
  execFileSync('sh', ['-c', `cat > ${JSON.stringify(f)}`], { input: buf });
  const total = Number(execFileSync('pdfinfo', [f]).toString()
    .match(/Pages:\s+(\d+)/)[1]);
  const squash = (s) => s.replace(/\s+/g, ' ').trim();
  const target = squash(needle);
  for (let p = 1; p <= total; p++) {
    const txt = execFileSync('pdftotext', ['-f', String(p), '-l', String(p), '-layout', f, '-'])
      .toString();
    if (squash(txt).includes(target)) return p;
  }
  return null;
}

/**
 * Stamp page numbers.
 * @param buf       PDF buffer
 * @param style     'none' | 'roman' | 'arabic'
 * @param startAt   first number (1-based) for arabic; roman starts at 'i'
 */
async function stampNumbers(buf, style, startAt = 1) {
  if (style === 'none') return buf;
  const doc = await PDFDocument.load(buf);
  const font = await doc.embedFont(StandardFonts.TimesRoman);
  const roman = (n) => {
    const map = [[1000,'m'],[900,'cm'],[500,'d'],[400,'cd'],[100,'c'],[90,'xc'],
      [50,'l'],[40,'xl'],[10,'x'],[9,'ix'],[5,'v'],[4,'iv'],[1,'i']];
    let out = '', v = n;
    for (const [k, s] of map) while (v >= k) { out += s; v -= k; }
    return out;
  };
  doc.getPages().forEach((pg, i) => {
    const label = style === 'roman' ? roman(startAt + i) : String(startAt + i);
    const size = (style === 'roman' && startAt + i <= 2) ? 12 : 13;
    const w = font.widthOfTextAtSize(label, size);
    pg.drawText(label, {
      x: GEOM.axisX - w / 2,
      y: GEOM.pageH - GEOM.numTopY,
      size, font, color: rgb(0, 0, 0),
    });
  });
  return Buffer.from(await doc.save());
}

async function merge(buffers) {
  const out = await PDFDocument.create();
  for (const b of buffers) {
    const src = await PDFDocument.load(b);
    const pages = await out.copyPages(src, src.getPageIndices());
    pages.forEach((p) => out.addPage(p));
  }
  return Buffer.from(await out.save());
}

/** Extract text of a buffer for verification. */
function pdfText(buf, tmpdir, name = 'verify.pdf') {
  const f = path.join(tmpdir, name);
  execFileSync('sh', ['-c', `cat > ${JSON.stringify(f)}`], { input: buf });
  return execFileSync('pdftotext', ['-layout', f, '-']).toString();
}

export {
  CSS, esc, htmlToPdf, countPages, locatePage, stampNumbers, merge, pdfText, CHROME,
};
