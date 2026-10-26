// Record the demo video by driving the running application.
// Produces media/raw/*.webm, which media/render-video.sh converts to media/SaigonBite_Demo.mp4.
//
//   node media/record-demo.mjs
//
// Narration is added by the team over the recording; this script only produces the screen capture.
import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium } from '../render/node_modules/playwright-core/index.mjs';

const BASE = process.env.BASE_URL || 'http://localhost:5080';
const ROOT = path.resolve(import.meta.dirname, '..');
const RAW = path.join(ROOT, 'media', 'raw');
const EXE = '/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';
const PASS = 'Saigon@123';
const BEAT = Number(process.env.BEAT_MS || 1100);

await fs.mkdir(RAW, { recursive: true });
for (const f of await fs.readdir(RAW).catch(() => [])) {
  if (f.endsWith('.webm')) await fs.unlink(path.join(RAW, f));
}

const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
const context = await browser.newContext({
  viewport: { width: 1440, height: 900 },
  recordVideo: { dir: RAW, size: { width: 1440, height: 900 } },
});
const page = await context.newPage();

const pause = (ms = BEAT) => page.waitForTimeout(ms);
const caption = async (text) => {
  await page.evaluate((t) => {
    let el = document.getElementById('__demo_caption');
    if (!el) {
      el = document.createElement('div');
      el.id = '__demo_caption';
      el.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:2147483647;'
        + 'background:#111;color:#fff;font:600 22px/1.5 "Times New Roman",serif;'
        + 'padding:14px 24px;text-align:center;letter-spacing:.2px;';
      document.body.appendChild(el);
    }
    el.textContent = t;
  }, text).catch(() => {});
};

async function login(username) {
  await context.clearCookies();
  await page.goto(`${BASE}/account/login`, { waitUntil: 'domcontentloaded' });
  await page.locator('input[name="Username"], input[type="text"]').first().fill(username);
  await page.locator('input[name="Password"], input[type="password"]').first().fill(PASS);
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    page.locator('button[type="submit"], input[type="submit"]').first().click(),
  ]);
}


/** Submit the delivery-board form for this order and this exact transition. */
async function advanceTo(orderId, toState, ms = BEAT) {
  await page.goto(`${BASE}/deliveries`, { waitUntil: 'domcontentloaded' });
  const form = page.locator(
    `form[action*="Advance" i]`
    + `:has(input[name="id"][value="${orderId}"])`
    + `:has(input[name="to"][value="${toState}"])`).first();
  if (!(await form.count())) return false;
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    form.locator('button[type="submit"]').first().click({ timeout: 8000 }).catch(() => {}),
  ]);
  await pause(ms);
  return true;
}

/** Submit a board form by action name, scoped to the order (assign, confirm cash). */
async function boardAction(orderId, actionPattern, ms = BEAT) {
  await page.goto(`${BASE}/deliveries`, { waitUntil: 'domcontentloaded' });
  const form = page.locator(
    `form[action*="${actionPattern}" i]:has(input[name="id"][value="${orderId}"])`).first();
  if (!(await form.count())) return false;
  const select = form.locator('select').first();
  if (await select.count()) {
    const values = await select.locator('option').evaluateAll((os) => os.map((o) => o.value).filter(Boolean)).catch(() => []);
    if (values.length) await select.selectOption(values[0]).catch(() => {});
  }
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    form.locator('button[type="submit"], input[type="submit"]').first().click({ timeout: 8000 }).catch(() => {}),
  ]);
  await pause(ms);
  return true;
}

const log = [];
const note = (s) => { log.push(s); console.log('•', s); };

// ---- 1. landing
await page.goto(BASE, { waitUntil: 'domcontentloaded' });
await caption('SaigonBite — cloud-kitchen delivery hub, Ho Chi Minh City');
await pause(1600);

// ---- 2. local customer
await login('0901234567').catch(() => {});
note(`signed in as local customer → ${page.url()}`);
await caption('Local Customer signs in with a Vietnamese mobile number');
await pause();

// ---- 3. hub selection and catalogue
await page.goto(`${BASE}/brands`, { waitUntil: 'domcontentloaded' });
await caption('Choose a hub — load percentage decides the price and the admission rule');
await pause(1600);
const hubValues = await page.locator('select[name="hubId"] option')
  .evaluateAll((os) => os.map((o) => o.value).filter(Boolean)).catch(() => []);
if (hubValues.length) {
  await page.goto(`${BASE}/brands?hubId=${hubValues[0]}`, { waitUntil: 'domcontentloaded' });
  note(`hub ${hubValues[0]} selected`);
  await caption('Menu of the chosen hub — only items this hub cooks are orderable');
  await pause(1800);
}

// ---- 4. add to cart
const addForm = page.locator('form[action*="add-to-cart"], form[action*="AddToCart"]').first();
if (await addForm.count()) {
  // BR1 needs a 50,000 subtotal; one 35,000 item would be refused on camera for the wrong reason.
  const qty = addForm.locator('input[name="Quantity"]').first();
  if (await qty.count()) await qty.fill('3').catch(() => {});
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    addForm.locator('button[type="submit"]').first().click(),
  ]);
  note('item added to the cart');
  await caption('Add to basket');
  await pause();
}

// ---- 5. cart and breakdown
await page.goto(`${BASE}/orders/cart`, { waitUntil: 'domcontentloaded' });
await caption('Basket — one hub per basket, priced line by line');
await pause(1800);

// ---- 6. checkout
await page.goto(`${BASE}/orders/checkout`, { waitUntil: 'domcontentloaded' });
await caption('Checkout — the full BR10 breakdown: subtotal, Quiet Kitchen, voucher, fees, rounded total');
await pause(2400);
await caption('BR13 — a Local Customer is offered MoMo, VNPay and cash only');
await pause(2000);

// ---- 7. place the order
// Two submit buttons exist: name="Place" value="true" places, value="false" re-prices.
await page.locator('input[name="Method"][value="CashOnDelivery"]').check({ force: true }).catch(() => {});
await pause(600);
const placed = page.locator('button[name="Place"][value="true"]').first();
if (await placed.count()) {
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    placed.click({ timeout: 8000 }).catch(() => {}),
  ]);
  await pause(1200);
  note(`order submitted → ${page.url()}`);
  await caption('Order placed — timestamp, hub load and rain flag are stored with it (BR17)');
  await pause(1600);
}

const orderId = Number((page.url().match(/\/orders\/(\d+)/) || [])[1] || 0);
note(`order id ${orderId || 'none'}`);

// ---- 8. kitchen, admin, shipper, reports
if (orderId) {
  await login('kitchen1');
  note('signed in as kitchen1');
  for (const to of ['Confirmed', 'Preparing', 'Ready']) {
    await caption(`Kitchen Staff — ${to} (BR15, hub-scoped)`);
    await advanceTo(orderId, to, 1500);
  }

  await login('admin');
  note('signed in as admin');
  await caption('Admin assigns a shipper to the ready order');
  await boardAction(orderId, 'assign', 1400);
  await caption('Both mandatory reports — R1 revenue, R2 hub utilisation');
  for (const r of ['/reports/revenue', '/reports/utilisation']) {
    await page.goto(BASE + r, { waitUntil: 'domcontentloaded' }).catch(() => {});
    await pause(2400);
  }

  await login('shipper1');
  note('signed in as shipper1');
  await caption('Shipper — out for delivery, then cash confirmed before Delivered (BR14)');
  await advanceTo(orderId, 'OutForDelivery', 1600);
  await caption('Cash must be confirmed before the order can be delivered');
  await boardAction(orderId, 'confirm', 1300);
  await advanceTo(orderId, 'Delivered', 1600);
  await caption(`Order ${orderId} is Delivered — five transitions, every one audited`);
  await pause(1400);
}

// ---- 9. the second customer type
await login('emma.wilson@example.com');
note('signed in as the Foreign Tourist');
await caption('Foreign Tourist — passport identity, hotel room address, Apple Pay or PayPal only');
await page.goto(`${BASE}/brands?hubId=1`, { waitUntil: 'domcontentloaded' });
const tAdd = page.locator('form[action*="AddToCart" i], form[action*="add-to-cart" i]').first();
const tQty = tAdd.locator('input[name="Quantity"]').first();
if (await tQty.count()) await tQty.fill('3').catch(() => {});
await Promise.all([
  page.waitForLoadState('domcontentloaded'),
  tAdd.locator('button[type="submit"]').first().click().catch(() => {}),
]);
await pause(1000);
await page.goto(`${BASE}/orders/checkout`, { waitUntil: 'domcontentloaded' });
await caption('Checkout — hotel and room instead of a street address, and only international methods');
await pause(1800);
await page.locator('[name="HotelName"]').first().fill('Rex Hotel').catch(() => {});
await page.locator('[name="RoomNumber"]').first().fill('512').catch(() => {});
await pause(900);
const paypal = page.locator('input[name="Method"][value="PayPal"]').first();
if (await paypal.count()) await paypal.check({ force: true }).catch(() => {});
await pause(700);
await Promise.all([
  page.waitForLoadState('domcontentloaded'),
  page.locator('button[name="Place"][value="true"]').first().click().catch(() => {}),
]);
await pause(1500);
const touristOrder = Number((page.url().match(/\/orders\/(\d+)/) || [])[1] || 0);
note(`tourist order ${touristOrder || 'none'} → ${page.url()}`);
await caption(`Tourist order ${touristOrder} placed — both customer types now ordered end to end`);
await pause(1700);

await caption('Admin dashboard — both reports as charts, and the heavy-rain flag');
await page.goto(`${BASE}/admin`, { waitUntil: 'domcontentloaded' }).catch(() => {});
await caption('End of demo — SaigonBite');
await pause(1400);

await context.close();
await browser.close();

const files = (await fs.readdir(RAW)).filter((f) => f.endsWith('.webm'));
await fs.writeFile(path.join(ROOT, 'media', 'raw', 'recording-log.json'),
  JSON.stringify({ base: BASE, steps: log, videos: files }, null, 2));
console.log('\nrecorded:', files.join(', ') || 'none');
if (!files.length) process.exitCode = 1;
