---
name: tdtu-presentation
description: Create or revise formal academic presentations within the TDTU workspace using monochrome slide framing, colored charts and images, the original TDTU logo, readable evidence, Vietnamese speaking notes when requested, and rendered verification. Does not prescribe report layout or apply outside TDTU.
---

# TDTU academic presentations

Use this skill for presentations in the TDTU workspace. The current user's explicit choices override these defaults. This is a workspace skill; do not install it globally.

## References and authority

- Visual reference: [user-supplied academic slide](assets/slide-reference.png). It informs the header structure, alignment and formal tone; do not copy its dense text or colored decoration.
- Original logo: [TDTU logo](../../../docs/report-reference/tdtu-logo.png). Preserve its bytes, colors and proportions. Do not redraw it, recolor it or use a web substitute.
- Report formatting is a separate concern governed by [the shared report standard](../../../TDTU_REPORT_STYLE.md). Do not apply A4 report typography or covers directly to slides.
- Use the installed Presentations skill for the available authoring API, runtime discovery, editable objects, finalization and rendering. Read current tool instructions instead of assuming an old package version.

## Design defaults

- 16:9 canvas, white background, black text. Keep titles, body text, equations, ordinary tables, rules and layout decoration black/white/gray. Charts, plots, heatmaps, analytical diagrams and illustrations must use clear, distinguishable colors; photos and evidence images retain their original colors. This workspace-wide preference was explicitly updated by the user on 20 October 2026.
- Use a restrained palette consistently for the same group or series across slides and, when applicable, the report. Pair colors with labels, markers or line styles; do not encode meaning by color alone. Keep legends and heatmap annotations readable against their fills. Use a diverging scale centered at zero for signed correlations, with its domain and key visible. Preserve the original logo's colors and proportions.
- Use a formal header: small original logo at the upper left, clear title beside it, thin black/gray horizontal rule, consistently aligned content below. Avoid decorative cards, gradients, shadows and ornamental motion.
- At a 1280×720 canvas, a suitable starting grid is: logo near (42,20), 158×88; title near (240,45); separator at y≈126; content within x≈70–1210 and y≈170–650. Preserve image aspect ratio; adjust this grid to the actual content.
- Available Arial is a suitable default. Start at 32 pt for titles, 24 pt for body text, and 18–21 pt for chart/table labels. Code may use a verified monospace font. API coordinates and numeric font sizes may use pixels: 1 pt = 4/3 px at 96 dpi.
- Give each slide one main purpose. Replace paragraphs with a small number of short statements, a comparison, a table, a chart or a code example. Reorganize or split crowded material before reducing text size.
- Keep the same title position, content margins and page-number position. A cover may use larger typography, while retaining the same academic visual system.

## Analytical content

- Use executed results, not invented numbers. All representations of a result must read from the same saved analytical artifacts.
- Choose the minimum chart that answers the question. Include readable axis labels, units, group sizes where relevant, and a short interpretation. Show uncertainty only when its method is stated and understood.
- Keep tables and charts editable. For a chart whose native Office calculation would differ, use editable geometry from exported statistics or another documented faithful representation; do not silently change quartile or aggregation rules.
- Keep source images unchanged when they are required evidence. A logo is not an analytical figure.
- Do not imply causal effects from exploratory correlations or grouped means. Preserve dataset limitations and distinguish observed ranges from theoretical scales.
- Put full wide tables in the notebook/report or an accompanying CSV. The slide can show a clearly labelled subset while pointing to the complete evidence.
- Keep code examples short and real. Do not replace an entire analytical explanation with a screenshot of a notebook.

## Narrative and speaking support

- Confirm the actual assignment duration and required languages from the conversation. Do not infer slide language solely from the report's English default.
- Use a timed outline covering the question, source, method, evidence, conclusion and limitations. Include code-demo time in the total.
- When English slides and Vietnamese delivery are requested, keep analytical terms consistent and provide natural Vietnamese speaker notes with spaces, punctuation, transitions and concrete demo actions.
- Notes must explain interpretation, not simply translate the slide. Cite external sources in the relevant notes.
- A proposed division of speaking responsibilities is not proof of completed contributions. Never invent contribution percentages or rehearsal history.
- Provide an offline demo fallback using executed outputs. Do not claim a live demo has been rehearsed unless it actually has.

## Verification and handoff

1. Confirm the slide count, coverage, numbers and source attribution.
2. Validate the PPTX package, fonts, editable objects, chart data and geometry with the installed skill's tools. Resolve environment/precision issues without disabling the relevant checks.
3. Render every final slide and inspect each at full size. Check overflow, overlap, awkward wrapping, missing glyphs, chart labels, color contrast, consistent series colors and repeated headers. Confirm analytical visuals are colored while nonvisual slide framing and ordinary text/tables stay monochrome. A contact sheet is an overview, not the full inspection.
4. Inspect the exported PDF too, particularly native charts whose layout can change across renderers. Preserve a PPTX source and a dependable PDF projection copy.
5. Confirm speaker notes exist and the sum of planned timings fits the duration. Record whether PowerPoint/other target-app testing was available; a renderer preview is not proof of application testing.
6. Deliver the PPTX/PDF, notes and requested demo material. Keep QA images, caches and temporary builds outside the submission package.

Keep this skill independent of a particular course, group, advisor, date or dataset. Link new lasting user preferences here rather than creating competing slide guides.
