# Part 1 course-template exception

The student explicitly requested this template for this assignment only on24 October2026. It overrides the shared TDTU report layout for Part1; it does not change the shared standard, slides or later reports.

Original: `../SE_Sem01_2627_Report_Template.docx` relative to the repository root, found in Downloads and copied byte-for-byte. SHA256: `46127f83a17ab4adccae2e58a5de671c11d3251323a0256faba08a5bc46066e3`.

The course template uses Letter215.9×279.4mm, Calibri11, navy headings, pale-blue tables and footer page numbers. One section; margins top1200/bottom1300/left-right1440twip, header/footer708twip. Instruction pages and future Part2/3 placeholders are removed as the template directs for a separate submission. The title/IP/TOC/Feedback/Part1 structure and section1.1–1.5 headings are retained. Appendix A is Contribution Statement, B is Generative AI Usage Log; unused full-size diagram placeholder is replaced by the required seeded RTM in Appendix C. Advisor metadata is filled using the same centered author pattern. No logo, acknowledgement/declaration or generic A4/TNR style was added.

The builder patches only document.xml, footer1.xml, settings.xml and core.xml. All other package parts, styles, theme, numbering, headers and relationships remain byte-identical; section geometry also matches. TOC/PAGEREF/PAGE fields remain native. Cached TOC pages are materialized from real PDF bookmark destinations; updateFields=true requests Word refresh on opening. The DOCX is never saved through LibreOffice; the bundled renderer only exports it. Microsoft Word was not available for its own field/layout test.

Builder: `render/build-part1.py` through the existing Node entry point. The full measured contract, package inventory, render evidence and build report are under ignored `render/.build/course-template/`. The original DOCX is immutable.
