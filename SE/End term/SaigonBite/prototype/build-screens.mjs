#!/usr/bin/env node
/**
 * Render every prototype screen to PNG at 1440 x 900 with the workspace
 * Chromium build, and fail if the page makes a single non-file request.
 *
 *   node prototype/build-screens.mjs
 *
 * Output: prototype/screens/NN-name.png
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..');
const require = createRequire(path.join(repo, 'render/'));
const { chromium } = require(path.join(repo, 'render/node_modules/playwright-core'));

const CHROME = '/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';
const PAGE = 'file://' + path.join(here, 'index.html');
const OUT = path.join(here, 'screens');

const SCREENS = [
  ['01-hubs', 'hubs'],
  ['02-menu', 'menu'],
  ['03-cart', 'cart'],
  ['04-checkout', 'checkout'],
  ['05-payment', 'payment'],
  ['06-track', 'track'],
  ['07-revenue', 'revenue'],
  ['08-utilization', 'utilization'],
  ['09-dashboard', 'dashboard'],
];

fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
const page = await ctx.newPage();

const external = [];
const errors = [];
page.on('request', (r) => { if (!/^(file|data|blob):/.test(r.url())) external.push(r.url()); });
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

for (const [file, hash] of SCREENS) {
  await page.goto(`${PAGE}#${hash}`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(120);
  await page.screenshot({ path: path.join(OUT, `${file}.png`) });
  const box = await page.evaluate(() => ({
    scrollH: document.documentElement.scrollHeight,
    viewH: innerHeight,
    screen: document.body.dataset.screen || '',
  }));
  console.log(`${file}.png  1440x900  document ${box.scrollH}px tall`);
}

// one mobile shot to prove the 390 px layout, not part of the deliverable set
await page.setViewportSize({ width: 390, height: 844 });
await page.goto(`${PAGE}#menu`, { waitUntil: 'load' });
await page.waitForTimeout(120);
await page.screenshot({ path: path.join(OUT, '_mobile-390-menu.png') });
await page.setViewportSize({ width: 1440, height: 900 });

await browser.close();

console.log(`external requests: ${external.length ? external.join(', ') : 'none'}`);
console.log(`console/page errors: ${errors.length ? errors.join(' | ') : 'none'}`);
if (external.length || errors.length) process.exitCode = 1;
