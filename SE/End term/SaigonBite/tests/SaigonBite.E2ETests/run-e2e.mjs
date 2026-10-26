// End-to-end verification against the running application.
// Uses playwright-core with an explicit Chromium, so it does not depend on the
// @playwright/test runner being installable in this environment.
//
//   node run-e2e.mjs            # BASE_URL defaults to http://localhost:5080
//
// Writes docs/part3-qa/evidence/e2e-results.json and screenshots into
// docs/part3-qa/screenshots/. Exits non-zero if any check fails.
import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium } from '../../render/node_modules/playwright-core/index.mjs';

const BASE = process.env.BASE_URL || 'http://localhost:5080';
const ROOT = path.resolve(import.meta.dirname, '..', '..');
const SHOTS = path.join(ROOT, 'docs', 'part3-qa', 'screenshots');
const EVID = path.join(ROOT, 'docs', 'part3-qa', 'evidence');
const EXE = '/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';

await fs.mkdir(SHOTS, { recursive: true });
await fs.mkdir(EVID, { recursive: true });

const results = [];
const record = (name, ok, detail = '') => {
  results.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
};

const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();

const consoleErrors = [];
page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('pageerror', (e) => consoleErrors.push(String(e)));

// ---- 1. public routes
const PUBLIC = ['/', '/account/login', '/account/register/local', '/account/register/tourist'];
for (const route of PUBLIC) {
  try {
    let res;
  try { res = await page.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 20000 }); }
  catch { record(`NFR4 ${route} refuses anonymous access`, false, 'unreachable'); continue; }
    const status = res ? res.status() : 0;
    record(`NFR3 GET ${route} responds`, status > 0 && status < 400, `status ${status}`);
    const body = await page.locator('body').innerText();
    record(`NFR3 GET ${route} has content`, body.trim().length > 40, `${body.trim().length} chars`);
  } catch (e) {
    record(`NFR3 GET ${route} responds`, false, String(e).slice(0, 120));
  }
}

try {
  await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.screenshot({ path: path.join(SHOTS, 'e2e-01-landing-1440.png'), fullPage: true });
} catch (e) {
  record('NFR3 landing screenshot captured', false, String(e).slice(0, 100));
}

// ---- 2. responsive
for (const width of [390, 768, 1440]) {
  await page.setViewportSize({ width, height: 900 });
  try { await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 20000 }); }
  catch (e) { record(`NFR3 no horizontal scroll at ${width}px`, false, 'page unreachable'); continue; }
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  record(`NFR3 no horizontal scroll at ${width}px`, overflow <= 1, `overflow ${overflow}px`);
  if (width === 390) await page.screenshot({ path: path.join(SHOTS, 'e2e-02-landing-390.png'), fullPage: true });
}
await page.setViewportSize({ width: 1440, height: 900 });

// ---- 3. protected routes
for (const route of ['/orders', '/admin', '/reports/revenue', '/deliveries']) {
  let res;
  try { res = await page.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 20000 }); }
  catch { record(`NFR4 ${route} refuses anonymous access`, false, 'unreachable'); continue; }
  const url = page.url();
  const redirected = /login|account/i.test(url);
  const refused = !res || res.status() >= 400;
  record(`NFR4 ${route} refuses anonymous access`, redirected || refused,
    redirected ? 'redirected to login' : `status ${res ? res.status() : 0}`);
}

// ---- 4. language toggle
try { await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 20000 }); } catch { /* handled below */ }
// The toggle is the /account/language link; matching on visible text alone false-positives
// on any word containing "en" ("Skip to content" was matched in the first run).
const toggle = page.locator('a[href*="/account/language"]').first();
record('FR-S1 language toggle present', await toggle.count() > 0,
  await toggle.count() ? (await toggle.innerText()).trim() : 'not found');

// ---- 5. console cleanliness, measured on the landing page only
consoleErrors.length = 0;
try { await page.goto(BASE + '/', { waitUntil: 'networkidle', timeout: 20000 }); }
catch { /* unreachable is already recorded above */ }
const realErrors = consoleErrors.filter((e) => !/favicon\.ico/i.test(e));
record('NFR3 landing page console is clean', realErrors.length === 0,
  realErrors.slice(0, 2).join(' | '));
if (consoleErrors.length !== realErrors.length) {
  record('known gap: no favicon served (404)', false, 'add a favicon to remove this console 404');
}

// ---- 6. both reports reachable once authenticated is out of scope here
const summary = {
  base: BASE,
  ranAt: new Date().toISOString(),
  total: results.length,
  passed: results.filter((r) => r.ok).length,
  failed: results.filter((r) => !r.ok).length,
  screenshotDir: SHOTS,
  results,
};
await fs.writeFile(path.join(EVID, 'e2e-results.json'), JSON.stringify(summary, null, 2));
console.log(`\n${summary.passed}/${summary.total} checks passed`);

await browser.close();
process.exitCode = summary.failed ? 1 : 0;
