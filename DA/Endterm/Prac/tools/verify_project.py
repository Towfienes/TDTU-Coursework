"""Verify persisted evidence and editable Office structures; no network required."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

import nbformat
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
meta=json.loads((ROOT/'project.json').read_text())
prefix=meta['prefix']
source=ROOT/'data/raw/student-por.csv'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='a7594a11d7771c0efe1a740824e0e833da9c4cad07c39a9766a874575563fb3f'
raw=pd.read_csv(source,sep=';')
assert raw.shape==(649,33) and raw.isna().sum().sum()==0
mask=pd.read_csv(ROOT/'data/processed/missing_mask.csv')['source_index']
assert len(mask)==32 and mask.nunique()==32
imputed=pd.read_csv(ROOT/'data/processed/mean_imputed.csv')
dropped=pd.read_csv(ROOT/'data/processed/drop_missing.csv')
assert imputed.shape==(649,33) and dropped.shape==(617,33)
assert imputed.isna().sum().sum()==dropped.isna().sum().sum()==0
unmasked=raw.index.difference(mask)
np.testing.assert_allclose(imputed.loc[mask,'absences'],raw.loc[unmasked,'absences'].mean(),atol=1e-10,rtol=0)
np.testing.assert_array_equal(imputed.loc[unmasked,'absences'],raw.loc[unmasked,'absences'])
pd.testing.assert_frame_equal(imputed.drop(columns='absences'),raw.drop(columns='absences'))
expected_drop=raw.loc[unmasked].reset_index(drop=True)
expected_drop['absences']=expected_drop['absences'].astype(float)
pd.testing.assert_frame_equal(dropped.reset_index(drop=True),expected_drop)
features=pd.read_csv(ROOT/'data/processed/analysis_features.csv',index_col='source_index')
assert features.shape==(649,37)
assert set(raw.columns).issubset(features.columns)
for name,ascending in [('top',False),('bottom',True)]:
    output=pd.read_csv(ROOT/f'results/tables/{name}_10_all_columns.csv',index_col='source_index')
    expected=features.sort_values('G3',ascending=ascending,kind='stable').head(10)
    pd.testing.assert_frame_equal(output,expected,check_exact=False,atol=1e-10,rtol=0)
summary=json.loads((ROOT/'results/summary.json').read_text())
assert summary['total_records']==649 and summary['total_columns']==37
assert sum(r['count'] for r in summary['performance_distribution'].values())==649
assert np.isclose(sum(r['percent'] for r in summary['performance_distribution'].values()),100)
manifest=json.loads((ROOT/'results/manifest.json').read_text())
for relative,checksum in manifest['artifacts'].items():
    assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==checksum, relative
notebook=nbformat.read(ROOT/f'notebooks/{prefix}_Analysis.ipynb',as_version=4)
code=[cell for cell in notebook.cells if cell.cell_type=='code']
assert len(code)==20
assert [cell.execution_count for cell in code]==list(range(1,21))
assert not any(output.output_type=='error' for cell in code for output in cell.outputs)
assert sum('image/png' in output.get('data',{}) for cell in code for output in cell.outputs)>=6

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
logo_hash=hashlib.sha256((ROOT/'report/assets/tdtu-logo.png').read_bytes()).hexdigest()
with zipfile.ZipFile(ROOT/f'report/{prefix}_Report.docx') as archive:
    assert archive.testzip() is None
    document=ET.fromstring(archive.read('word/document.xml'))
    assert len(document.findall('.//{'+M+'}oMath'))==3
    sections=document.findall('.//{'+W+'}sectPr')
    assert len(sections)==4
    for section in sections:
        margin=section.find('{'+W+'}pgMar')
        for side,expected in [('left',1984),('right',1134),('top',1984),('bottom',1701)]:
            assert abs(int(margin.get('{'+W+'}'+side))-expected)<=1,(side,margin.attrib)
    fmt=[s.find('{'+W+'}pgNumType') for s in sections]
    assert fmt[0] is None and [x.get('{'+W+'}fmt') for x in fmt[1:]]==['lowerRoman','lowerRoman','decimal']
    simple=[el.get('{'+W+'}instr','') for el in document.findall('.//{'+W+'}fldSimple')]
    assert sum(x.startswith('PAGEREF') for x in simple)==48
    assert sum(x.startswith('SEQ ') for x in simple)==18
    instructions=[el.text or '' for el in document.findall('.//{'+W+'}instrText')]
    assert sum('TOC ' in x for x in instructions)==3
    fulltext=' '.join(el.text or '' for el in document.findall('.//{'+W+'}t'))
    assert all(author['name'] in fulltext and author['id'] in fulltext for author in meta['authors'])
    assert not any(token in fulltext for token in ['[[','MIDTERM REPORT','MERN','Pham Kim'])
    assert any(hashlib.sha256(archive.read(name)).hexdigest()==logo_hash for name in archive.namelist() if name.startswith('word/media/'))

with zipfile.ZipFile(ROOT/f'slides/{prefix}_Presentation.pptx') as archive:
    assert archive.testzip() is None
    names=archive.namelist()
    slides=sorted([name for name in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',name)],key=lambda name:int(re.search(r'(\d+)\.xml',name)[1]))
    assert len(slides)==25
    charts=[name for name in names if name.endswith('.xml') and '/charts/' in name and '/_rels/' not in name]
    assert len(charts)==5
    assert len([name for name in names if name.startswith('ppt/embeddings/') and name.endswith('.xlsx')])==5
    assert any(hashlib.sha256(archive.read(name)).hexdigest()==logo_hash for name in names if name.startswith('ppt/media/'))
    for slide_number,name in enumerate(slides,1):
        slide=ET.fromstring(archive.read(name))
        assert len(slide.findall('.//{'+P+'}pic'))==1
        image=slide.find('.//{'+A+'}blip')
        assert image is not None and image.get('{'+REL+'}embed')
        note=ET.fromstring(archive.read(f'ppt/notesSlides/notesSlide{slide_number}.xml'))
        note_text=' '.join(el.text or '' for el in note.findall('.//{'+A+'}t'))
        assert 'Thời lượng dự kiến' in note_text and 'Nguồn:' in note_text
for relative in [f'report/{prefix}_Report.pdf',f'slides/{prefix}_Presentation.pdf']:
    assert (ROOT/relative).read_bytes().startswith(b'%PDF-')
print('PASS: source, mask, treatments, all-column rankings, manifest, 20 executed cells, 6 figures, native Word fields/equations, 25 slides with embedded original logo, notes and 5 editable chart workbooks.')
