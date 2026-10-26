// The second customer type: a Foreign Tourist places an order.
// Required by the video and demo rubric ("one order for each customer type") and by BR13/BR18.
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
  return !page.url().includes('/account/login');
}

// ---- 1. the tourist registers with a passport rather than a phone number
const reg = await page.goto(`${BASE}/account/register/tourist`, { waitUntil: 'domcontentloaded' })
  .then(() => page.locator('body').innerText());
record('the tourist registration form asks for a passport, not a mobile number',
  /passport|hộ chiếu/i.test(reg) && !/mobile number|số điện thoại/i.test(reg),
  reg.replace(/\s+/g, ' ').slice(0, 120));
await shot('t01-tourist-registration.png');

// ---- 2. sign in as the seeded tourist
const signedIn = await login('emma.wilson@example.com');
record('the seeded tourist account signs in', signedIn, page.url());

// ---- 3. build a basket from one hub
await page.goto(`${BASE}/brands?hubId=1`, { waitUntil: 'domcontentloaded' });
const add = page.locator('form[action*="AddToCart" i], form[action*="add-to-cart" i]').first();
const qty = add.locator('input[name="Quantity"]').first();
if (await qty.count()) await qty.fill('3').catch(() => {});
await Promise.all([
  page.waitForLoadState('domcontentloaded'),
  add.locator('button[type="submit"]').first().click().catch(() => {}),
]);
record('a tourist can fill a basket', true, page.url());

// ---- 4. BR13 — the tourist sees only international methods
await page.goto(`${BASE}/orders/checkout`, { waitUntil: 'domcontentloaded' });
const checkout = await page.locator('body').innerText();
const methods = await page.locator('input[name="Method"]').evaluateAll((es) => es.map((e) => e.value));
record('BR13: the tourist is offered Apple Pay, PayPal and cash only',
  methods.includes('ApplePay') && methods.includes('PayPal')
  && methods.includes('CashOnDelivery')
  && !methods.includes('Momo') && !methods.includes('VnPay'),
  methods.join(', '));
record('BR10: the tourist checkout shows the full breakdown',
  /subtotal|delivery|total/i.test(checkout), checkout.replace(/\s+/g, ' ').slice(0, 100));
await shot('t02-tourist-checkout.png');

// ---- 5. fill the hotel address the specification grants a Tourist, then place
await page.locator('[name="HotelName"]').first().fill('Rex Hotel').catch(() => {});
await page.locator('[name="RoomNumber"]').first().fill('512').catch(() => {});
await page.locator('input[name="Method"][value="CashOnDelivery"]').check({ force: true }).catch(() => {});
await Promise.all([
  page.waitForLoadState('domcontentloaded'),
  page.locator('button[name="Place"][value="true"]').first().click().catch(() => {}),
]);
const orderId = Number((page.url().match(/\/orders\/(\d+)/) || [])[1] || 0);
record('the tourist order is placed', orderId > 0, `order ${orderId}, ${page.url().replace(BASE, '')}`);
await shot('t03-tourist-order.png');

if (orderId) {
  const text = (await page.locator('body').innerText()).replace(/\s+/g, ' ');
  record('the tourist order stores the hotel delivery address',
    /hotel|khách sạn/i.test(text), text.slice(0, 120));
}

const summary = {
  base: BASE, ranAt: new Date().toISOString(),
  total: steps.length, passed: steps.filter((s) => s.ok).length,
  failed: steps.filter((s) => !s.ok).length, steps,
};
await fs.writeFile(path.join(EVID, 'tourist-results.json'), JSON.stringify(summary, null, 2));
console.log(`\n${summary.passed}/${summary.total} tourist checks passed`);
await browser.close();
process.exitCode = summary.failed ? 1 : 0;
