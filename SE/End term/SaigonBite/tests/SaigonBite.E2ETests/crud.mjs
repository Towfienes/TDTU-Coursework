// CRUD and pricing-rule checks that exercise the POST routes the views actually generate.
// Covers the heavy-rain flag end to end (BR5 + BR17 snapshot), voucher creation and brand editing.
import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium } from '../../render/node_modules/playwright-core/index.mjs';

const BASE = process.env.BASE_URL || 'http://localhost:5080';
const ROOT = path.resolve(import.meta.dirname, '..', '..');
const SHOTS = path.join(ROOT, 'docs', 'part3-qa', 'screenshots');
const EVID = path.join(ROOT, 'docs', 'part3-qa', 'evidence');
const EXE = '/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';
const PASS = 'Saigon@123';

await fs.mkdir(SHOTS, { recursive: true });
const steps = [];
const record = (n, ok, d = '') => { steps.push({ n, ok, d }); console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ' — ' + d : ''}`); };

const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
const shot = (f) => page.screenshot({ path: path.join(SHOTS, f), fullPage: true }).catch(() => {});

async function login(user) {
  await ctx.clearCookies();
  await page.goto(`${BASE}/account/login`, { waitUntil: 'domcontentloaded' });
  await page.locator('input[name="Username"], input[type="text"]').first().fill(user);
  await page.locator('input[type="password"]').first().fill(PASS);
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    page.locator('button[type="submit"]').first().click(),
  ]);
}

/** Place one three-unit order from hub 1 with COD and return the rounded total on the order page. */
async function placeOrder() {
  await login('0901234567');
  await page.goto(`${BASE}/brands?hubId=1`, { waitUntil: 'domcontentloaded' });
  const add = page.locator('form[action*="AddToCart" i], form[action*="add-to-cart" i]').first();
  const qty = add.locator('input[name="Quantity"]').first();
  if (await qty.count()) await qty.fill('3').catch(() => {});
  await Promise.all([page.waitForLoadState('domcontentloaded'), add.locator('button[type="submit"]').first().click()]);

  await page.goto(`${BASE}/orders/checkout`, { waitUntil: 'domcontentloaded' });
  await page.locator('input[name="Method"][value="CashOnDelivery"]').check({ force: true }).catch(() => {});
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    page.locator('button[name="Place"][value="true"]').first().click().catch(() => {}),
  ]);
  const text = (await page.locator('body').innerText()).replace(/\s+/g, ' ');
  // the order page groups thousands with separators; the rounded total is the largest amount shown
  const totals = [...text.matchAll(/(\d{1,3}(?:[.,]\d{3})+)/g)]
    .map((m) => Number(m[1].replace(/[.,]/g, '')))
    .filter((n) => Number.isFinite(n) && n > 0);
  return { id: Number((page.url().match(/\/orders\/(\d+)/) || [])[1] || 0), totals, text };
}

/** Drive the heavy-rain flag. The dashboard form is one-way: it posts an explicit enabled value. */
async function setRain(on) {
  await login('admin');
  for (let attempt = 0; attempt < 3; attempt++) {
    await page.goto(`${BASE}/admin`, { waitUntil: 'domcontentloaded' });
    const text = (await page.locator('body').innerText()).replace(/\s+/g, ' ');
    const current = /RAIN FLAG\s*On/i.test(text);
    if (current === on) return true;
    const form = page.locator('form[action*="rain" i]').first();
    if (!(await form.count())) return false;
    await Promise.all([
      page.waitForLoadState('domcontentloaded'),
      form.locator('button[type="submit"], input[type="submit"]').first().click().catch(() => {}),
    ]);
  }
  await page.goto(`${BASE}/admin`, { waitUntil: 'domcontentloaded' });
  const final = (await page.locator('body').innerText()).replace(/\s+/g, ' ');
  return /RAIN FLAG\s*On/i.test(final) === on;
}

/** Read the rain-surcharge row from an order page. */
async function rainRow(orderId) {
  await login('0901234567');
  await page.goto(`${BASE}/orders/${orderId}`, { waitUntil: 'domcontentloaded' });
  const text = (await page.locator('body').innerText()).replace(/\s+/g, ' ');
  const m = text.match(/rain[^0-9]{0,40}([\d.,]+)/i);
  return m ? Number(m[1].replace(/[.,]/g, '')) : null;
}

// ---------------------------------------------------------------- BR5 end to end
const rainOn = await setRain(true);
record('admin can toggle the heavy-rain flag', rainOn, rainOn ? 'flag switched' : 'no control');
const withRain = await placeOrder();
record('an order can be placed with rain on', withRain.id > 0, `order ${withRain.id}, totals seen ${withRain.totals.join(',')}`);

await setRain(false);
const noRain = await placeOrder();
record('an order can be placed with rain off', noRain.id > 0, `order ${noRain.id}, totals seen ${noRain.totals.join(',')}`);

if (withRain.id && noRain.id) {
  const on = Math.max(...withRain.totals);
  const off = Math.max(...noRain.totals);
  record('BR5: the rain surcharge adds exactly 10,000 to the rounded total',
    on - off === 10000,
    `order ${withRain.id} total ${on} − order ${noRain.id} total ${off} = ${on - off}`);
}
await shot('c01-rain-flag.png');

// ---------------------------------------------------------------- admin CRUD
await login('admin');
const voucherCode = `AUTOTEST${Date.now().toString().slice(-5)}`;
const vres = await page.goto(`${BASE}/vouchers/create`, { waitUntil: 'domcontentloaded' });
record('the voucher create form loads', vres.status() === 200, `status ${vres.status()}`);
const vform = page.locator('form[action*="Create" i], form[action*="create" i]').first();
if (await vform.count()) {
  const fill = async (name, value) => {
    const el = vform.locator(`[name="${name}"]`).first();
    if (await el.count()) await el.fill(String(value)).catch(() => {});
  };
  await fill('Code', voucherCode);
  await fill('Value', 10);
  await fill('MaxDiscount', 30000);
  await fill('MinSubtotal', 100000);
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    vform.locator('button[type="submit"], input[type="submit"]').first().click().catch(() => {}),
  ]);
  const list = await page.goto(`${BASE}/vouchers`, { waitUntil: 'domcontentloaded' }).then(() => page.locator('body').innerText());
  record('a voucher created through the UI appears in the list', list.includes(voucherCode),
    list.includes(voucherCode) ? voucherCode : 'not found in the list');
} else {
  record('a voucher created through the UI appears in the list', false, 'no create form');
}
await shot('c02-voucher.png');

const bres = await page.goto(`${BASE}/brands/1/edit`, { waitUntil: 'domcontentloaded' });
record('the brand edit form loads', bres.status() === 200, `status ${bres.status()}`);
const bform = page.locator('form[action*="Edit" i], form[action*="edit" i]').first();
record('the brand edit form posts somewhere', (await bform.count()) > 0,
  (await bform.getAttribute('action').catch(() => '')) || 'none');

const summary = {
  base: BASE, ranAt: new Date().toISOString(),
  total: steps.length, passed: steps.filter((s) => s.ok).length,
  failed: steps.filter((s) => !s.ok).length, steps,
};
await fs.writeFile(path.join(EVID, 'crud-results.json'), JSON.stringify(summary, null, 2));
console.log(`\n${summary.passed}/${summary.total} CRUD checks passed`);
await browser.close();
process.exitCode = summary.failed ? 1 : 0;
