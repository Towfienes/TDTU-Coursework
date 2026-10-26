import pw from '/home/towfienes/TDTU/SE/End term/SaigonBite/render/node_modules/playwright-core/index.js';
const { chromium } = pw;
import path from 'node:path';
const files = process.argv.slice(2);
const root = '/home/towfienes/TDTU/SE/End term/SaigonBite/docs/part2-design/diagrams';
const browser = await chromium.launch({
  executablePath: '/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome',
  args: ['--no-sandbox'],
});
for (const f of files) {
  const full = path.join(root, f);
  const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: 1600, height: 1200 } });
  await page.goto('file://' + encodeURI(full));
  const svg = await page.$('svg');
  const box = await svg.boundingBox();
  await page.setViewportSize({ width: Math.ceil(box.width) + 8, height: Math.ceil(box.height) + 8 });
  const out = path.join('/home/towfienes/TDTU/SE/End term/SaigonBite/docs/part2-design/.verify', f.replace(/\.svg$/, '.png'));
  await svg.screenshot({ path: out });
  console.log(f, '->', Math.ceil(box.width) + 'x' + Math.ceil(box.height));
  await page.close();
}
await browser.close();
