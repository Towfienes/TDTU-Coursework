# End-to-end suite

Playwright tests against the running application (Tier 4 requirement).

```sh
cd tests/SaigonBite.E2ETests
npm install --cache ./.npm-cache
BASE_URL=http://localhost:5080 npx playwright test
```

`smoke.spec.mjs` covers NFR3 (responsive widths, no console errors), NFR4 (protected routes refuse
anonymous callers) and FR-S1 (language toggle). The full order journeys — one Local Customer and one
Foreign Tourist through to `Delivered` — live in `specs/journeys.spec.mjs` and are written against the
real DOM once the web tier runs.

Chromium is already installed at `~/.cache/ms-playwright`; set `PLAYWRIGHT_BROWSERS_PATH` only if it
lives elsewhere.
