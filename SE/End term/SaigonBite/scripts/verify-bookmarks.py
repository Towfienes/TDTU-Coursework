#!/usr/bin/env python3
"""Verify the PDF bookmark tree of the consolidated report.

Usage:  UV_CACHE_DIR=render/.uv-cache uv run --quiet --with pypdf \\
          python3 scripts/verify-bookmarks.py docs/final/SAIGONBITE_FULL_REPORT.pdf

Exits non-zero when the report has no bookmarks, when a required part is missing
from the tree, or when the nesting is flat.
"""
import sys
from pypdf import PdfReader

REQUIRED = ["ACKNOWLEDGEMENT", "TABLE OF CONTENT", "LIST OF FIGURES", "REFERENCES"]


def walk(outline, depth=0, rows=None):
    rows = [] if rows is None else rows
    for item in outline:
        if isinstance(item, list):
            walk(item, depth + 1, rows)
        else:
            rows.append((depth, item.title.strip()))
    return rows


def main(path):
    reader = PdfReader(path)
    rows = walk(reader.outline)
    print(f"pages: {len(reader.pages)}")
    print(f"bookmarks: {len(rows)}")
    for depth, title in rows[:60]:
        print("  " * depth + f"- {title}")

    problems = []
    if not rows:
        problems.append("no bookmarks at all")
    if rows and max(r[0] for r in rows) == 0:
        problems.append("bookmark tree is flat — no nesting")
    titles = {t.upper() for _, t in rows}
    for req in REQUIRED:
        if not any(req in t for t in titles):
            problems.append(f"missing required bookmark: {req}")
    chapters = [t for d, t in rows if d == 0]
    if len(chapters) < 6:
        problems.append(f"only {len(chapters)} top-level entries; a full report needs at least 6")

    print()
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1
    print("PASS bookmark tree is present, nested and complete")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
