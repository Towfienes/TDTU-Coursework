// Render the same signing block as the report, with 1–5 illustrative authors.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { chromium } from 'playwright-core';
import { PDFDocument } from 'pdf-lib';
import { CSS, CHROME } from './lib.mjs';
import { part1 } from './content-part1.mjs';
import { signatureBlock, SIGNATURE_CSS } from './signatures.mjs';

const out = new URL('../docs/part1-proposal-req/previews/', import.meta.url);
await fs.mkdir(out, { recursive: true });
const names = [...part1.team.members.map(m => m.full_name), 'Nguyễn Lê Nhật Tâm', 'Ngô Bình Minh'];
for (const count of [0, 6]) {
  assert.throws(() => signatureBlock(Array(count).fill('Author'), ''), RangeError);
}
assert.match(signatureBlock(['A & B'], '<date>'), /A &amp; B/);
const intro = part1.front[0].html().split('<div class="signoff"')[0];
const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
const pdf = await PDFDocument.create();
const measurements = [];
try {
  for (let count = 1; count <= 5; count++) {
    const page = await browser.newPage({ viewport: { width: 700, height: 1000 } });
    await page.setContent(`<html><head><meta charset="utf-8"><style>${CSS}${SIGNATURE_CSS}
      body { width: 155mm; } .preview-number { position: fixed; top: -20mm; width: 155mm; text-align: center; }
      </style></head><body><div class="preview-number">i</div>${intro}${signatureBlock(names.slice(0, count), part1.team.project.report_date)}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    const geometry = await page.evaluate(() => {
      const boxes = [...document.querySelectorAll('.signature-name')].map(el => {
        const r = el.getBoundingClientRect();
        return { left: r.left, right: r.right, top: r.top, height: r.height, font: getComputedStyle(el).fontSize };
      });
      return { width: document.body.getBoundingClientRect().width, boxes };
    });
    assert.equal(geometry.boxes.length, count);
    const gaps = geometry.boxes.slice(1).map((box, i) => box.left - geometry.boxes[i].right);
    assert(geometry.boxes.every(box => box.left >= 0 && box.right <= geometry.width + 0.1));
    assert(geometry.boxes.every(box => Math.abs(box.top - geometry.boxes[0].top) < 0.1));
    assert(gaps.every(gap => gap > 0));
    if (gaps.length) assert(Math.max(...gaps) - Math.min(...gaps) < 0.1);
    const bytes = await page.pdf({ format: 'A4', printBackground: true });
    const sample = await PDFDocument.load(bytes);
    assert.equal(sample.getPageCount(), 1, `${count} authors must fit one page`);
    pdf.addPage((await pdf.copyPages(sample, [0]))[0]);
    measurements.push({ count, ...geometry, gaps });
    await page.close();
  }
} finally {
  await browser.close();
}
await fs.writeFile(new URL('signatures-1-to-5.pdf', out), await pdf.save());
await fs.writeFile(new URL('signatures-1-to-5-geometry.json', out), JSON.stringify(measurements, null, 2) + '\n');
console.log('PASS: 1–5 authors, one row, equal positive gaps, within margins, one page each; invalid counts rejected.');
