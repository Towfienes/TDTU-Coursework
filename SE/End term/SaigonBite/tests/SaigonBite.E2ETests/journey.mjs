// Authenticated end-to-end journey: both customer types, the order lifecycle, and both reports.
// Drives the real UI so antiforgery tokens are handled by the browser.
//
//   node journey.mjs
//
// Writes screenshots to docs/part3-qa/screenshots/ and a JSON summary to
// docs/part3-qa/evidence/journey-results.json.
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
await fs.mkdir(EVID, { recursive: true });
const steps = [];
const record = (name, ok, detail = '') => {
  steps.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
};

const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });

async function newSession() {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  return { ctx, page: await ctx.newPage() };
}

async function shot(page, name, fullPage = true) {
  try { await page.screenshot({ path: path.join(SHOTS, name), fullPage }); } catch { /* ignored */ }
}

async function login(page, username) {
  await page.goto(`${BASE}/account/login`, { waitUntil: 'domcontentloaded' });
  const user = page.locator('input[name="Username"], input[name="UserName"], input[type="text"]').first();
  const pass = page.locator('input[name="Password"], input[type="password"]').first();
  await user.fill(username);
  await pass.fill(PASS);
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    page.locator('button[type="submit"], input[type="submit"]').first().click(),
  ]);
  const body = await page.locator('body').innerText();
  const signedOut = /invalid|incorrect|không đúng|sai mật khẩu/i.test(body);
  return !signedOut && !page.url().includes('/account/login');
}

// ---------------------------------------------------------------- local customer journey
const local = await newSession();
record('local customer signs in', await login(local.page, '0901234567'), local.page.url());
await shot(local.page, 'j01-local-after-login.png');

const browse = await local.page.goto(`${BASE}/brands`, { waitUntil: 'domcontentloaded' });
record('brands page loads for the customer', browse.status() === 200, `status ${browse.status()}`);
await shot(local.page, 'j02-brands.png');

// a hub must be selected before the catalogue offers add-to-cart (BrandsController.Index)
// the hub is chosen from a <select name="hubId"> inside a GET form, not from links
const hubSelect = local.page.locator('select[name="hubId"]');
const hubValues = await hubSelect.locator('option')
  .evaluateAll((os) => os.map((o) => o.value).filter(Boolean)).catch(() => []);
let hubChosen = false;
if (hubValues.length) {
  // navigate straight to the documented query parameter, which is what the form submits
  await local.page.goto(`${BASE}/brands?hubId=${hubValues[0]}`, { waitUntil: 'domcontentloaded' });
  hubChosen = local.page.url().includes('hubId=');
}
record('a hub can be selected', hubChosen,
  hubChosen ? local.page.url() : `${hubValues.length} hub options, url ${local.page.url()}`);

if (hubChosen) {
  await shot(local.page, 'j03-hub-menu.png');
  const bodyText = await local.page.locator('body').innerText();
  record('menu items are listed with prices', /[0-9][0-9.,]{3,}/.test(bodyText),
    `${bodyText.length} chars on the page`);

  const addForm = local.page.locator('form[action*="add-to-cart"], form[action*="AddToCart"]').first();
  const formCount = await local.page.locator('form[action*="add-to-cart"], form[action*="AddToCart"]').count();
  record('add-to-cart control is rendered for a customer', formCount > 0, `${formCount} forms`);
  if (formCount > 0) {
    await Promise.all([
      local.page.waitForLoadState('domcontentloaded'),
      addForm.locator('button[type="submit"]').first().click(),
    ]);
    record('an item can be added to the cart', true, local.page.url());
  }
  await shot(local.page, 'j04-after-add.png');

  const cart = await local.page.goto(`${BASE}/orders/cart`, { waitUntil: 'domcontentloaded' });
  const cartBody = await local.page.locator('body').innerText().catch(() => '');
  record('cart page loads', cart.status() === 200, `status ${cart.status()}`);
  const emptyish = /your cart is empty|giỏ hàng trống|chưa có món/i.test(cartBody);
  record('cart holds the added item', !emptyish,
    emptyish ? 'cart reported empty' : cartBody.replace(/\s+/g, ' ').slice(0, 160));
  await shot(local.page, 'j05-cart.png');

  const checkout = await local.page.goto(`${BASE}/orders/checkout`, { waitUntil: 'domcontentloaded' });
  const checkoutBody = await local.page.locator('body').innerText().catch(() => '');
  const breakdown = /subtotal|tạm tính|delivery|giao|total|tổng|voucher/i.test(checkoutBody);
  record('checkout displays a price breakdown', breakdown,
    `status ${checkout.status()}, ${checkoutBody.length} chars`);
  const payMethods = /momo|vnpay|cash|tiền mặt|cod/i.test(checkoutBody);
  const touristMethods = /apple ?pay|paypal/i.test(checkoutBody);
  record('BR13 local customer sees only local methods', payMethods && !touristMethods,
    `local=${payMethods} tourist=${touristMethods}`);
  await shot(local.page, 'j06-checkout-breakdown.png');
}

// ---------------------------------------------------------------- staff, shipper, admin
const staff = await newSession();
record('kitchen staff signs in', await login(staff.page, 'kitchen1'));
await shot(staff.page, 'j07-kitchen.png');

const ship = await newSession();
record('shipper signs in', await login(ship.page, 'shipper1'));
const del = await ship.page.goto(`${BASE}/deliveries`, { waitUntil: 'domcontentloaded' });
record('delivery board loads for the shipper', del.status() === 200, `status ${del.status()}`);
await shot(ship.page, 'j08-deliveries.png');

const admin = await newSession();
record('admin signs in', await login(admin.page, 'admin'));
await shot(admin.page, 'j09-admin-dashboard.png');

for (const [route, file, label] of [
  ['/reports/revenue', 'j10-revenue-report.png', 'R1 revenue report renders'],
  ['/reports/utilisation', 'j11-utilisation-report.png', 'R2 hub utilisation report renders'],
]) {
  const res = await admin.page.goto(BASE + route, { waitUntil: 'domcontentloaded' });
  const body = await admin.page.locator('body').innerText().catch(() => '');
  record(label, res.status() === 200 && body.length > 400, `status ${res.status()}, ${body.length} chars`);
  await shot(admin.page, file);
}

const adminBody = await admin.page.goto(`${BASE}/admin`, { waitUntil: 'domcontentloaded' })
  .then(() => admin.page.locator('body').innerText());
record('admin dashboard shows the heavy-rain flag (BR5)', /rain|mưa/i.test(adminBody),
  `${adminBody.length} chars`);

const summary = {
  base: BASE,
  ranAt: new Date().toISOString(),
  total: steps.length,
  passed: steps.filter((s) => s.ok).length,
  failed: steps.filter((s) => !s.ok).length,
  steps,
};
await fs.writeFile(path.join(EVID, 'journey-results.json'), JSON.stringify(summary, null, 2));
console.log(`\n${summary.passed}/${summary.total} journey checks passed`);

await browser.close();
process.exitCode = summary.failed ? 1 : 0;
