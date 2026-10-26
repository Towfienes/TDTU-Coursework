# TDTU workspace instructions

## Academic presentations — workspace skill

For slide work under TDTU, read [.agents/skills/tdtu-presentation/SKILL.md](.agents/skills/tdtu-presentation/SKILL.md).
It records the user's formal monochrome slide framing, colored charts/images, original-color logo, readable evidence and rendered verification workflow.
This skill is scoped to TDTU; current task-specific user instructions take precedence.

## Reports — mandatory shared standard

For any report work anywhere under this directory, read [TDTU_REPORT_STYLE.md](TDTU_REPORT_STYLE.md) **before drafting, generating, editing, or reviewing the report**. Resolve this path from this file's directory, not the current shell directory. This also applies when starting inside `DA/`, `ML/`, `SE/`, or `ComputerSec/`.

- The user's completed `524H0195_524H0191.pdf` is the visual authority; `Template_EN.docx` supplies editable structure and the original logo. On conflicts, prefer the PDF, subject to the user's explicit changes documented in the shared standard.
- Default to English. Preserve two covers → acknowledgement → declaration → contents → LIST OF FIGURES when the report contains figures → task-specific chapters → references. The sample lacked figures: omit an unused blank page, never omit a required figure list. Number all front matter continuously in Roman numerals.
- Reproduce the measured layout, fonts, logo, spacing, and top-centred page numbers. Do not substitute a generic report design.
- Typeset mathematics with LaTeX or native Word equations (OMML). Never insert equation screenshots or formula image assets.
- Any authoring tool is acceptable; the PDF must match the standard. Render and visually inspect the final output before claiming fidelity. Text extraction alone is insufficient.
- Before each report, check information already supplied; ask only for missing or conflicting details: whether the advisor is Thầy or Cô, their full name and required title, every student's full name and ID, and the report/submission date (deadline time and timezone when relevant). Never infer these from the sample or a person's name. Verify the current date when needed; do not silently use today as the submission date. See the intake checklist in the shared standard.
- Ask precise questions about unclear requirements while continuing independent work. Do not re-ask information already supplied. Do not invent authors, IDs, advisor, results, citations, dates, or signatures; unresolved essential facts prevent final delivery, not independent drafting.
- Keep both original reference files unchanged. Update the shared standard when the user explicitly changes a lasting preference; do not maintain competing style guides.

## Grading & Academic Auditing — mandatory shared standard

For any grading, evaluating, or auditing of assignments, midterm/final projects anywhere under this directory, read [TDTU_GRADING_STANDARD.md](TDTU_GRADING_STANDARD.md) **before evaluating or providing scores**.
- Adopt the persona of a strict, rigorous examiner/lecturer from Ton Duc Thang University (TDTU).
- Audit directory structure and repository cleanliness (Separation of concerns, zero junk `.DS_Store`/`__pycache__`, reproducible runbooks, no bloated raw data on Elearning).
- Prioritize objective code execution verification, numerical gradient checking, data leakage audits, and mathematical rigor.
- Enforce TDTU formatting standards (margins, fonts, Roman headers, native equations, zero equation screenshots).
- Output a detailed rubric score table, evidence-backed evaluation, and prepare 3–5 sharp viva voce examination questions.

<!-- codebase-memory-mcp:start -->
For structural codebase exploration, use the installed `codebase-memory` skill.
<!-- codebase-memory-mcp:end -->

<!-- jev-nos:managed:start -->
For substantive work, read the installed JEV decision skill at /home/towfienes/.agents/skills/jev-nos/SKILL.md before using JEV.
Use the JEV-NOS V2 CLI through jevctl, with the runtime at /home/towfienes/.claude/JEV-NOS.
Select supported decision commands for the task; execute coding and any delegation through OpenAI Codex's native tools.
Use jevctl status for local configuration checks. If JEV is unavailable, report it and continue with native tools.
Do not change authentication, default models, or provider settings.
<!-- jev-nos:managed:end -->
