"""Early layout proof using real names, sections, equations and native index fields."""
import json
from pathlib import Path
from report_layout import Report

root=Path(__file__).resolve().parents[1]
(root/'.build/qa').mkdir(parents=True,exist_ok=True)
report=Report(root,json.loads((root/'project.json').read_text()))
report.cover();report.cover(inner=True)
report.new_numbered_section('lowerRoman',1,size=12)
report.title('ACKNOWLEDGEMENT')
report.para('We thank Ho Thi Linh, Ph.D., for the course instruction and assignment requirements. This layout sample verifies the retained template before the full report is typeset.')
report.doc.add_page_break();report.title('DECLARATION OF AUTHORSHIP')
report.para('The public data source and generated analysis will be documented. This is a layout feasibility sample, not the final declaration.')
report.new_numbered_section('lowerRoman',None,size=13)
report.index_placeholder('TOC','TABLE OF CONTENT');report.doc.add_page_break()
report.index_placeholder('LOF','LIST OF FIGURES');report.doc.add_page_break()
report.index_placeholder('LOT','LIST OF TABLES')
report.new_numbered_section('decimal',1)
report.heading('CHAPTER 1. INTRODUCTION')
report.heading('1.1 Layout verification',2)
report.para('The report uses an editable Word equation, numbered captions, automatic heading/caption lists and centred header page numbers. The score is normalized within its school.')
report.equation('z','G3 − min(G3 within school)','max(G3 within school) − min(G3 within school)')
report.table(['Check','Expected'],[['Font','Times New Roman, 13 pt'],['Header','Page number centred']], '1.1.1','Layout check')
report.figure('01_grade_histogram.png','1.1.1','Sample histogram for layout verification')
report.finalize_indexes()
destination=root/'.build/qa/layout_sample.docx';report.doc.save(destination)
(root/'.build/qa/layout_index.json').write_text(json.dumps(report.entries+report.figures+report.tables,ensure_ascii=False,indent=2))
print(destination)
