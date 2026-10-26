// Generic report builder: Markdown -> HTML -> Chromium PDF -> stamped and merged to the TDTU layout.
// Used by Part 2, Part 3 and the consolidated final report.
import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { chromium } from 'playwright-core';
import { CSS, esc, htmlToPdf, stampNumbers, merge, pdfText, CHROME } from './lib.mjs';
import { markdownToHtml } from './md.mjs';
import * as fm from './frontmatter.mjs';

const EXTRA_CSS = `
.toc-entry.lvl3 { font-weight: normal; padding-left: 2.4cm; font-size: 12pt; }
.toc-entry.lvl2 .t, .toc-entry.lvl3 .t { white-space: normal; }
pre { font-family: "Courier New", monospace; font-size: 9pt; line-height: 1.25;
      background: #f6f6f6; border: 0.5pt solid #999; padding: 6pt; margin: 6pt 0;
      white-space: pre-wrap; text-align: left; }
blockquote { margin: 6pt 0 6pt 1.27cm; padding-left: 8pt; border-left: 2pt solid #888;
             font-style: italic; }
code { font-family: "Courier New", monospace; font-size: 10pt; }
a { color: #000; text-decoration: none; }
`;

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '');

/**
 * Build one report PDF.
 * @param {object} opt
 * @param {string} opt.mdPath        Markdown source of the body
 * @param {string} opt.diagramsDir   directory holding the referenced SVG files
 * @param {string} opt.outFile       destination PDF
 * @param {string} opt.partLabel     text printed on the covers
 * @param {string[]} [opt.appendix]  extra Markdown files appended as appendices
 */
export async function buildReport({ mdPath, diagramsDir, outFile, partLabel, appendix = [] }) {
  const tmp = await fs.mkdtemp(path.join(path.dirname(outFile), '.build-'));
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });

  // ---- gather svg images
  const images = {};
  try {
    for (const f of await fs.readdir(diagramsDir)) {
      if (f.endsWith('.svg')) images[f] = await fs.readFile(path.join(diagramsDir, f), 'utf8');
    }
  } catch { /* no diagrams directory */ }

  // ---- body
  let md = await fs.readFile(mdPath, 'utf8');
  for (const a of appendix) {
    md += `\n\n${await fs.readFile(a, 'utf8')}`;
  }
  const { html: bodyHtml, headings, figures } = markdownToHtml(md, { images });

  const doc = (inner, extra = '') =>
    `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}${EXTRA_CSS}${extra}</style></head><body>${inner}</body></html>`;

  const bodyPdf = await htmlToPdf(browser, doc(bodyHtml));
  const bodyPages = pdfText(bodyPdf, tmp, 'body.pdf').split('\f').filter((p) => p.trim());

  const locate = (key) => {
    const n = norm(key);
    for (let i = 0; i < bodyPages.length; i++) if (norm(bodyPages[i]).includes(n)) return i + 1;
    return null;
  };

  // ---- covers and front matter
  const coversPdf = await htmlToPdf(browser, doc(fm.coverOuter(partLabel) + fm.coverInner(partLabel)));
  const ackDecPdf = await htmlToPdf(browser, doc(fm.acknowledgement(partLabel) + fm.declaration()));
  const ackDecPages = pdfText(ackDecPdf, tmp, 'ack.pdf').split('\f').filter((p) => p.trim()).length;

  const tocEntry = (h) => {
    const page = locate(h.label);
    if (page === null) throw new Error(`TOC anchor not found: ${h.label}`);
    const lvl = Math.min(h.level, 3);
    return `<div class="toc-entry lvl${lvl}"><span class="t">${esc(h.label)}</span>`
      + `<span class="dots"></span><span class="pg">${page}</span></div>`;
  };
  const lofEntry = (f) => {
    const page = locate(f.caption);
    if (page === null) throw new Error(`LOF anchor not found: ${f.caption}`);
    return `<div class="lof-entry"><span class="t">${esc(f.caption)}</span>`
      + `<span class="dots"></span><span class="pg">${page}</span></div>`;
  };

  const tocPdf = await htmlToPdf(browser,
    doc(`<h1 class="centered" style="break-before:auto;page-break-before:auto;">TABLE OF CONTENT</h1>`
      + headings.map(tocEntry).join('\n')));
  const tocPages = pdfText(tocPdf, tmp, 'toc.pdf').split('\f').filter((p) => p.trim()).length;

  const lofPdf = await htmlToPdf(browser,
    doc(`<h1 class="centered" style="break-before:auto;page-break-before:auto;">LIST OF FIGURES</h1>`
      + (figures.length ? figures.map(lofEntry).join('\n')
        : '<p class="noindent">This part contains no figures.</p>')));
  const lofPages = pdfText(lofPdf, tmp, 'lof.pdf').split('\f').filter((p) => p.trim()).length;

  // ---- numbering and merge
  const romanToc = ackDecPages + 1;
  const romanLof = ackDecPages + tocPages + 1;
  const finalPdf = await merge([
    coversPdf,
    await stampNumbers(ackDecPdf, 'roman', 1),
    await stampNumbers(tocPdf, 'roman', romanToc),
    await stampNumbers(lofPdf, 'roman', romanLof),
    await stampNumbers(bodyPdf, 'arabic', 1),
  ]);
  await fs.writeFile(outFile, finalPdf);
  await browser.close();

  // ---- verify
  const info = execFileSync('pdfinfo', [outFile]).toString();
  const pages = Number(info.match(/Pages:\s+(\d+)/)[1]);
  const finalPages = pdfText(finalPdf, tmp, 'final.pdf').split('\f');
  const offset = 2 + ackDecPages + tocPages + lofPages + 1;
  const problems = [];

  const expected = offset - 1 + bodyPages.length;
  if (pages !== expected) problems.push(`page count ${pages} != expected ${expected}`);

  for (const h of headings) {
    const claimed = locate(h.label);
    const idx = finalPages.findIndex((p, i) => i >= offset - 1 && norm(p).includes(norm(h.label)));
    if (claimed === null || idx === -1) { problems.push(`TOC anchor missing: ${h.label}`); continue; }
    const actual = idx + 1 - offset + 1;
    if (actual !== claimed) {
      problems.push(`TOC page mismatch for ${h.label}: says ${claimed}, actual ${actual}`);
    }
  }
  for (const f of figures) {
    if (locate(f.caption) === null) problems.push(`LOF anchor missing: ${f.caption}`);
  }

  // Remove the per-build scratch directory so no temporary PDFs are left under docs/.
  await fs.rm(tmp, { recursive: true, force: true }).catch(() => {});

  const fonts = execFileSync('pdffonts', [outFile]).toString();
  const report = {
    file: outFile, pages, bodyPages: bodyPages.length,
    tocEntries: headings.length, figures: figures.length,
    ackDecPages, tocPages, lofPages,
    timesEmbedded: /TimesNewRoman|Times-Roman|LiberationSerif/i.test(fonts),
    problems,
  };
  return report;
}
