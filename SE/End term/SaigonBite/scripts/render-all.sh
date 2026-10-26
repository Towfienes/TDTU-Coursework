#!/usr/bin/env bash
# Regenerate every document from config/team.json and the report content.
# Usage: bash scripts/render-all.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

say() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

say "Checking the toolchain"
for bin in node pdfinfo pdftotext pdfunite pdftoppm; do
  command -v "$bin" >/dev/null || { echo "missing: $bin"; exit 1; }
done
[ -d render/node_modules ] || { echo "missing render/node_modules — run: cd render && npm install playwright-core pdf-lib"; exit 1; }

say "Building Part 1 — proposal and requirements"
node render/build-part1.mjs

say "Building the Part 1 pitch deck"
if [ -f slides/build-deck.mjs ]; then
  node slides/build-deck.mjs
else
  echo "SKIPPED — slides/build-deck.mjs not present"
fi

say "Building Part 2 — design document"
if [ -f render/build-part2.mjs ]; then
  node render/build-part2.mjs
else
  echo "SKIPPED — render/build-part2.mjs not present"
fi

say "Verifying"
bash scripts/verify-pdf.sh

say "Done"
find docs slides -name '*.pdf' -printf '%p  %s bytes\n' 2>/dev/null | sort
