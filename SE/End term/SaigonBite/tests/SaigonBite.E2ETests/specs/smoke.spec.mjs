// End-to-end smoke coverage. These assertions hold regardless of the exact view markup,
// so they are safe to run before the full order flow is written against the real DOM.
import { test, expect } from '@playwright/test';

const PUBLIC_ROUTES = [
  { path: '/', name: 'landing' },
  { path: '/account/login', name: 'login' },
  { path: '/account/register', name: 'register' },
];

test.describe('NFR3 — the application serves its public routes', () => {
  for (const route of PUBLIC_ROUTES) {
    test(`GET ${route.path} responds without a server error`, async ({ page }) => {
      const response = await page.goto(route.path, { waitUntil: 'domcontentloaded' });
      expect(response, `no response for ${route.path}`).not.toBeNull();
      expect(response.status(), `${route.path} status`).toBeLessThan(400);
      await expect(page.locator('body')).toBeVisible();
    });
  }
});

test.describe('NFR3 — responsive from 390 px to 1440 px', () => {
  for (const width of [390, 768, 1440]) {
    test(`no horizontal scrolling at ${width} px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow, `horizontal overflow at ${width} px`).toBeLessThanOrEqual(1);
    });
  }
});

test.describe('NFR4 — access is refused to anonymous callers', () => {
  const PROTECTED = ['/orders', '/admin', '/reports/revenue', '/deliveries'];
  for (const path of PROTECTED) {
    test(`${path} redirects an anonymous visitor away`, async ({ page }) => {
      const response = await page.goto(path, { waitUntil: 'domcontentloaded' });
      // Either a redirect to the login page or an explicit refusal; not a rendered admin screen.
      const url = page.url();
      const landedOnLogin = /account\/login|\/login/i.test(url);
      const refused = response === null || response.status() >= 300;
      expect(landedOnLogin || refused, `${path} was served to an anonymous visitor`).toBeTruthy();
    });
  }
});

test.describe('FR-S1 — the interface offers a language toggle', () => {
  test('a Vietnamese/English switch exists on the landing page', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    const toggle = page.locator(
      'a[href*="lang"], a[href*="language"], a[href*="culture"], button:has-text("VI"),'
      + ' button:has-text("EN"), a:has-text("Tiếng Việt"), a:has-text("English")').first();
    await expect(toggle).toBeVisible();
  });
});

test.describe('no console errors on the landing page', () => {
  test('the browser console stays clean', async ({ page }) => {
    const errors = [];
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto('/', { waitUntil: 'networkidle' });
    expect(errors, `console errors:\n${errors.join('\n')}`).toHaveLength(0);
  });
});
