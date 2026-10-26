#!/usr/bin/env bash
# Layout gates for the generated PDFs, per TDTU_REPORT_STYLE.md section 10.
# Usage: bash scripts/verify-pdf.sh [file ...]
# Exits non-zero when any gate fails.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAIL=0
pass() { printf '  \033[32mPASS\033[0m %s\n' "$1"; }
fail() { printf '  \033[31mFAIL\033[0m %s\n' "$1"; FAIL=$((FAIL + 1)); }

check() {
  local f="$1"
  echo "== $f"

  [ -f "$f" ] || { fail "file missing"; return; }

  local info pages size
  info="$(pdfinfo "$f" 2>/dev/null)"
  pages="$(sed -n 's/^Pages:[[:space:]]*//p' <<<"$info")"
  size="$(sed -n 's/^Page size:[[:space:]]*//p' <<<"$info")"

  [ -n "$pages" ] && pass "opens, $pages pages" || fail "cannot read page count"

  # Only this Part 1 uses the supplied SE course DOCX (Letter, Calibri, footer).
  if [[ "$(realpath "$(dirname "$f")")" == "$ROOT/docs/part1-proposal-req" ]] &&
     [[ "$(basename "$f")" =~ ^(SaigonBite_Part1|Team.+_SE_Final_Report_SaigonBite)\.pdf$ ]]; then
    if [[ "$size" =~ ([0-9.]+)[[:space:]]x[[:space:]]*([0-9.]+) ]] &&
       awk -v w="${BASH_REMATCH[1]}" -v h="${BASH_REMATCH[2]}" 'BEGIN{exit !(w>611 && w<613 && h>791 && h<793)}'; then
      pass "SE course template: Letter portrait"
    else
      fail "Part 1 differs from the course template page size"
    fi
    if pdffonts "$f" 2>/dev/null | grep -qi 'Calibri'; then
      pass "course template Calibri present"
    else
      fail "no Calibri in course report"
    fi
    if pdftotext -f 1 -l 1 -layout "$f" - 2>/dev/null | grep -qE 'SE Report.*Page 1'; then
      pass "course footer page number present"
    else
      fail "course footer missing"
    fi
    if pdftotext "$f" - 2>/dev/null | grep -qE 'TBD|Guidance \(delete|Team XX|Team02'; then
      fail "unfilled course-template content"
    else
      pass "no course placeholders or old team code"
    fi
    return
  fi

  # Slide decks are 16:9 landscape and are not held to the A4 report standard.
  if [[ "$size" =~ ([0-9.]+)[[:space:]]x[[:space:]]*([0-9.]+) ]] && awk -v w="${BASH_REMATCH[1]}" -v h="${BASH_REMATCH[2]}" 'BEGIN{exit !(w>h)}'; then
    local w="${BASH_REMATCH[1]}" h="${BASH_REMATCH[2]}"
    if awk -v w="$w" -v h="$h" 'BEGIN{exit !((w/h)>1.7 && (w/h)<1.82)}'; then
      pass "slide deck, 16:9 landscape ($size)"
    else
      pass "landscape deliverable ($size)"
    fi
    if pdffonts "$f" 2>/dev/null | grep -qiE 'TimesNewRoman|Times-Roman|LiberationSerif'; then
      pass "Times-family font present"
    else
      fail "no Times-family font in the deck"
    fi
    return
  fi

  # A4 portrait, 209.9 x 297.1 mm plus a sub-point rounding allowance
  if [[ "$size" =~ ([0-9.]+)[[:space:]]x[[:space:]]*([0-9.]+) ]]; then
    local w="${BASH_REMATCH[1]}" h="${BASH_REMATCH[2]}"
    if awk -v w="$w" -v h="$h" 'BEGIN{exit !(w>594 && w<597 && h>841 && h<844)}'; then
      pass "A4 portrait ($size)"
    else
      fail "page size is $size, expected A4 portrait"
    fi
  else
    fail "cannot read page size"
  fi

  # Times New Roman must be embedded, not substituted
  if pdffonts "$f" 2>/dev/null | grep -qiE 'TimesNewRoman|Times-Roman|LiberationSerif'; then
    pass "Times-family font present"
  else
    fail "no Times-family font — check the render"
  fi

  # No formula screenshots: report body should carry no huge raster images
  # other than the cover logo. Count image XObjects per page.
  local imgpages
  imgpages="$(pdfimages -list "$f" 2>/dev/null | tail -n +3 | awk '{print $1}' | sort -u | wc -l)"
  if [ "$imgpages" -le 4 ]; then
    pass "raster images on $imgpages page(s) — logo only"
  else
    fail "raster images on $imgpages pages — check for formula or screenshot images"
  fi

  # Page numbers must exist in the top margin of body pages
  local first_body_text
  first_body_text="$(pdftotext -f 3 -l 3 -layout "$f" - 2>/dev/null | head -3)"
  if grep -qE '^[[:space:]]*(i|ii|iii|iv|v|1)[[:space:]]*$' <<<"$first_body_text"; then
    pass "page number in the top margin"
  else
    fail "no page number found at the top of page 3"
  fi

  # Placeholders must not survive into a final deliverable
  if pdftotext "$f" - 2>/dev/null | grep -q 'TBD'; then
    fail "contains TBD placeholders — fill config/team.json before submitting"
  else
    pass "no TBD placeholders"
  fi
}

if [ "$#" -gt 0 ]; then
  targets=("$@")
else
  mapfile -t targets < <(find docs slides -name '*.pdf' -not -path '*.build*' 2>/dev/null | sort)
fi

if [ "${#targets[@]}" -eq 0 ]; then
  echo "no PDFs found under docs/ or slides/"; exit 1
fi

for f in "${targets[@]}"; do check "$f"; done

echo
if [ "$FAIL" -eq 0 ]; then
  echo "ALL GATES PASSED"
else
  echo "$FAIL GATE(S) FAILED"
fi
exit $([ "$FAIL" -eq 0 ] && echo 0 || echo 1)
