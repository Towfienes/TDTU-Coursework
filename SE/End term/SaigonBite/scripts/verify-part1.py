"""Check the generated Part 1 documents; this does not test the application."""
import hashlib
import json
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path
import pymupdf
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'config/part1.json').read_text())
team = json.loads((ROOT / 'config/team.json').read_text())
normalise = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
report = ROOT / 'docs/part1-proposal-req/SaigonBite_Part1.pdf'
pdf = pymupdf.open(report)
text = '\n'.join(page.get_text() for page in pdf)
flat = normalise(text)
assert len(data['fr']) == 47 and len(data['nfr']) == 6 and len(data['ambiguities']) == 5
assert len({r['id'] for r in data['fr']}) == 47
assert [(r['tier'],r['cap']) for r in data['technology']['tiers']] == [('Tier 1',7.0),('Tier 1B',7.5),('Tier 2',8.5),('Tier 3',9.5),('Tier 4',10.0)]
assert team['project']['tier'] == 'Tier 4' and team['project']['tier_cap'] == 10.0
assert team['instructor']['honorific'] == 'ThS.' and not team['instructor']['title']
assert 'ThS. Phạm Thái Kỳ Trung' in text
assert 'Ph.D.' not in text and 'Dr. Phạm' not in text
for r in data['technology']['tiers']:
    assert normalise(r['stack']) in flat, ('Tier stack',r['tier'])
for r in data['technology']['acceptance']:
    assert normalise(r['plan']) in flat and normalise(r['evidence']) in flat, r['criterion']
for r in data['fr']:
    assert r['statement'].startswith('The system shall'), r['id']
    assert normalise(r['statement']) in flat, ('Report differs', r['id'])
    assert r['owner'] and r['use_case'] and r['test'] and r['source'], r['id']
for r in data['nfr']:
    assert normalise(r['target']) in flat, r['id']
    assert normalise(r['verification']) in flat, r['id']
for r in data['ambiguities']:
    assert normalise(r['assumption']) in flat, r['id']
    assert r['answer'].startswith('Not asked'), r['id']
for bad in ['Third member', 'SaigonRide', 'Sub-dong remainders are truncated', 'Verified (0.0006 ms)']:
    assert bad not in text, bad
assert not re.search(r'\bTBD\b', text)
assert set(re.findall(r'BR(\d+)\b', ' '.join(r['source'] for r in data['fr']))) == set(map(str, range(1, 19)))

# This Part1 intentionally uses the course DOCX, whose layout differs from TDTU default.
build = json.loads((ROOT / 'render/.build/course-template/build-report.json').read_text())
assert team['project']['team_id'] == 'TeamG4'
ref = ROOT.parent / 'SE_Sem01_2627_Report_Template.docx'
assert hashlib.sha256(ref.read_bytes()).hexdigest() == '46127f83a17ab4adccae2e58a5de671c11d3251323a0256faba08a5bc46066e3'
ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(ref) as original, zipfile.ZipFile(build['docx']) as filled:
    assert set(original.namelist()) == set(filled.namelist())
    editable = {'word/document.xml','word/footer1.xml','word/settings.xml','docProps/core.xml'}
    for name in original.namelist():
        if name not in editable:
            assert original.read(name) == filled.read(name), ('Template part changed',name)
    original_xml = ET.fromstring(original.read('word/document.xml'))
    final_xml = ET.fromstring(filled.read('word/document.xml'))
    assert ET.tostring(original_xml.find('w:body/w:sectPr',ns)) == ET.tostring(final_xml.find('w:body/w:sectPr',ns))
    heading_texts = [''.join(p.itertext()) for p in final_xml.findall('w:body/w:p',ns) if p.find('w:pPr/w:pStyle',ns) is not None]
    for title in ['1.1 Project Proposal','1.2 Problem Statement','1.3 Functional Requirements','1.4 Quality Attributes (Non-Functional Requirements)','1.5 Ambiguity Log']:
        assert title in heading_texts and title in build['headings'], title
    fields = [p.text or '' for p in final_xml.findall('.//w:instrText',ns)]
    assert any(f.startswith('TOC ') for f in fields) and sum('PAGEREF' in f for f in fields) == len(build['headings'])
    assert ET.fromstring(filled.read('word/settings.xml')).find('w:updateFields',ns).get('{'+ns['w']+'}val') == 'true'
for bad in ['Team02','Team XX','TeamXX','Guidance (delete','[Student','[TITLE','CHAPTER 1.','ACKNOWLEDGEMENT','DECLARATION OF AUTHORSHIP','Part 2: Software Design','Part 3: Implementation']:
    assert bad not in text, bad
assert 'TeamG4' in pdf[0].get_text()
for i,page in enumerate(pdf):
    assert abs(page.rect.width-612) < 1 and abs(page.rect.height-792) < 1
    spans = [s for b in page.get_text('dict')['blocks'] for line in b.get('lines',[]) for s in line['spans'] if s['text'].strip()]
    footers = [s for s in spans if s['bbox'][1]>740]
    assert len(footers)==1 and footers[0]['text'].endswith(f'Page {i+1}'), (i+1,footers)
    assert 'TeamG4' in footers[0]['text'] and 'Calibri' in footers[0]['font']
    for span in spans:
        if span['text']=='@PTKT': continue  # Source header part is byte-identical.
        assert 'Calibri' in span['font'], (i+1,span['font'])
        assert span['size'] >= 8.4, ('Below template minimum',i+1,span)
        if span['bbox'][1]<740:
            assert span['bbox'][1]>=58 and span['bbox'][3]<=729, ('Vertical overflow',i+1,span['text'])
    # Justified trailing spaces can extend past the final visible glyph.
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                for char in span['chars']:
                    x0,y0,x1,y1=char['bbox']
                    if 58<=y0<740 and char['c'].strip():
                        assert x0>=70 and x1<=542, ('Horizontal glyph overflow',i+1,char)
toc_page = pdf[build['headings']['Table of Contents']-1]
links = toc_page.get_links()
assert len(links)==len(build['headings'])
for link in links:
    printed = re.findall(r'\d+',toc_page.get_textbox(link['from']))
    assert printed and link['page']==int(printed[-1])-1, link
for title,page_number in build['headings'].items():
    assert normalise(title) in normalise(pdf[page_number-1].get_text()),title
print(f'PASS course report: {len(pdf)} Letter pages, 47 FR + 6 NFR + 5 assumptions, {len(links)} TOC links, native headings/bookmarks, original package/style/geometry preserved; TeamG4/ThS.')

subprocess.run([sys.executable, str(ROOT / 'scripts/verify-workbook.py')], check=True)
subprocess.run([sys.executable, str(ROOT / 'scripts/verify-marking-sheet.py')], check=True)

slide_pdf = pymupdf.open(ROOT / 'slides/Part1_Pitch.pdf')
assert len(slide_pdf) == 5
assert normalise('TeamG4') in normalise(slide_pdf[0].get_text())
assert normalise('29.5 % qualifies') in normalise(slide_pdf[1].get_text())
assert 'never the tier' not in ''.join(p.get_text() for p in slide_pdf)
assert normalise('10.0/10') in normalise(slide_pdf[4].get_text())
assert normalise('Core MVC variant pending') in normalise(slide_pdf[4].get_text())
with zipfile.ZipFile(ROOT / 'slides/Part1_Pitch.pptx') as z:
    assert z.testzip() is None
    slides = [n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)]
    notes = [n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)]
    assert len(slides) == len(notes) == 5
    assert all(b'<a:t>' in z.read(n) for n in slides + notes)
assert 40 + 75 + 80 + 95 + 85 == 375
print('PASS pitch: 5 PDF slides, fractional-load example, 5 editable PPTX slides and 5 notes pages; planned budget 6:15')

s = Decimal(61111)
q = s * Decimal('.1')
v = (s - q) * Decimal('.1')
round_total = lambda n: (n / 1000).quantize(Decimal(1), rounding=ROUND_HALF_UP) * 1000
assert round_total(s - q - v + 15000) == 64000
q_bad = q.to_integral_value(rounding=ROUND_FLOOR)
v_bad = ((s - q_bad) * Decimal('.1')).to_integral_value(rounding=ROUND_FLOOR)
assert round_total(s - q_bad - v_bad + 15000) == 65000
assert Decimal(59) / 200 * 100 < 30 and Decimal(179) / 200 * 100 < 90
print('PASS independent acceptance calculations: final-only rounding and fractional-load boundaries (not application tests)')

immutable = {'SE_FinalProject_Requirements_SaigonBite_Sem01_2627.pdf':'5b2841734be141ad', 'SE_FP_SaigonBite_CaseStudy_Sem01_2627.pdf':'9c3b6c3e3f1f9971', 'SE_FP_SaigonBite_StudentSurvivalGuide_Sem01_2627.pdf':'09eee8c07f3476e3', 'SE_Sem01_2627_Team_Workbook_Template.xlsx':'e6efb91f2a497825'}
for name, digest in immutable.items():
    assert hashlib.sha256((ROOT.parent / name).read_bytes()).hexdigest().startswith(digest), name
for name in ['524H0195_524H0191_SaigonBite_Part1.pdf', '524H0195_524H0191_524H0179_SaigonBite_Part1.pdf', f"{team['project']['team_id']}_SE_Final_Report_SaigonBite.pdf", 'docs/part1-proposal-req/SaigonBite_Part1.pdf']:
    assert (ROOT.parent / name).read_bytes() == report.read_bytes(), ('Stale report copy', name)
spec = (ROOT / 'specs/001-saigonbite-platform/spec.md').read_text()
assert all(r['statement'] in spec for r in data['fr'])
print('PASS sources unchanged, all report copies current and readable spec aligned')

subprocess.run(['node', '--input-type=module', '-e', "import assert from 'node:assert/strict'; import {part1} from './render/content-part1.mjs'; import {renderBlocks} from './render/blocks.mjs'; const html=part1.body.map(fn=>renderBlocks(fn().blocks)).join(''); assert(html.includes('FR-D10') && html.includes('NFR6') && html.includes('TC-NFR-6'));"], cwd=ROOT, check=True)
print('PASS shared-renderer compatibility for future consolidated builds')
