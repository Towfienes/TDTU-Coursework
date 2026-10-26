# PDF quality assurance

Final artifact: `report/Machine_Learning_Midterm_Final.pdf`, 19 A4 portrait pages, PDF 1.4, unencrypted. Inspected 9 October 2026.

The PDF skill was located at `/home/towfienes/.codex/plugins/cache/openai-primary-runtime/pdf/26.1007.11041/skills/pdf/SKILL.md`; its complete workflow was read and applied. Authoring uses ReportLab and bundled licensed DejaVu fonts. Mathematical expressions use high-resolution Matplotlib mathtext with LaTeX syntax; no terminal TeX dependency is needed.

## Render and visual inspection — PASS

Every page was rendered by Poppler at 160 DPI (1323 × 1871 pixels) and inspected individually at original resolution. The final revision changed pages 1, 10 and 14; these were individually reinspected. Pixel comparisons confirmed that the remaining 16 pages were identical to the individually reviewed revision. Rendered review images and intermediate diagnostics are preserved outside the submission ZIP in the workspace `audit_trail/`.

Checks included mathematical subscripts and symbols, complete tables, chart axes and legends, caption association, header/footer separation, page numbering, references and Vietnamese member names. Early layout defects produced three nearly empty continuation pages; those were removed before finalization. Figure labels were enlarged for A4 reading. The final corrections reduced crowded loss-axis labels, used common bins across class histograms and moved a short ROC legend into unused chart space. No clipping, orphan captions, overlapping body text or missing visible glyphs remained in the reviewed pages.

## Programmatic preflight — PASS

- `pdfinfo`: 19 pages, A4 595.276 × 841.89 points, no encryption, no JavaScript or forms.
- Strict `pypdf` parsing and text extraction: all 19 pages have meaningful text; confirmed names and IDs are present.
- Automated artifact tests match ten key report metrics to generated JSON at six decimal places and verify the selected classifier name.
- `numerical_trace.json` reproduces the source metrics and records SHA-256 for every figure used by the report.
- `pdffonts`: all five DejaVu TrueType fonts used for visible text are embedded, subsetted and have Unicode mappings. A nonembedded standard Helvetica resource is initialized by ReportLab, but examination of text-showing operators confirms it draws no visible text.
- Equations are 300-DPI image assets and remain legible in inspected renders. Body text is searchable; equation glyphs are not searchable text.

## Limits

veraPDF is **UNAVAILABLE** in this environment. Formal PDF/A and PDF/UA conformance was not requested and is not asserted. The PDF is not tagged for accessibility. No physical-printer proof was performed; visual QA used A4 page renders. The reproducible builder and licensed font assets are included.
