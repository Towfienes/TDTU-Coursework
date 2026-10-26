"""Check numerical evidence, leakage boundaries and native Office structures offline."""
import hashlib,json,re,sys,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import nbformat
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.analysis import COLUMNS,FULL,holm,metrics,welch_comparison,ring_bands,contingency_test
from src.submission import readiness_issues
M=json.loads((ROOT/'project.json').read_text());prefix=M['prefix'];suffix='_REVIEW' if readiness_issues(M) else ''
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=ROOT/'data/raw/abalone.data'
assert sha(raw)=='de37cdcdcaaa50c309d514f248f7c2302a5f1f88c168905eba23fe2fbc78449f'
df=pd.read_csv(raw,header=None,names=COLUMNS)
assert df.shape==(4177,9) and df.duplicated().sum()==0 and df.isna().sum().sum()==0
clean=pd.read_csv(ROOT/'data/processed/clean_measurements.csv',index_col='source_index')
assert clean.index.tolist()==df.index.tolist() and clean.height.isna().sum()==2
pd.testing.assert_frame_equal(clean.drop(columns='height').reset_index(drop=True),df.drop(columns='height'))
valid=df.height.ne(0);np.testing.assert_array_equal(clean.loc[valid,'height'],df.loc[valid,'height'])
assert clean.index[clean.height.isna()].tolist()==[1257,3996]
split=pd.read_csv(ROOT/'data/processed/split.csv').set_index('source_index')
train_idx,test_idx=train_test_split(df.index.to_numpy(),test_size=.2,random_state=42,stratify=df.sex)
assert set(split.index[split.split=='train'])==set(train_idx)
assert set(split.index[split.split=='test'])==set(test_idx)
assert len(train_idx)==3341 and len(test_idx)==836 and set(train_idx).isdisjoint(test_idx)
train=clean.loc[train_idx]
S=json.loads((ROOT/'results/summary.json').read_text())
assert S['train_n']==3341 and S['test_n']==836
assert S['invalid_height_indices']==[1257,3996]
for group in ['distribution','hypotheses']:
 r=S[group];np.testing.assert_allclose(holm([x['p'] for x in r]),[x['p_holm'] for x in r],atol=1e-14,rtol=0)
assert len(S['distribution'])==3 and all(x['n']==3341 for x in S['distribution'])
w=welch_comparison(train.loc[train.sex=='M','rings'],train.loc[train.sex=='F','rings'])
for key in ['difference','ci_low','ci_high','statistic','df','p']:assert np.isclose(w[key],S['welch'][key],atol=1e-10,rtol=0)
ct=pd.crosstab(train.sex,ring_bands(train.rings)).reindex(['F','I','M']);chi,expected=contingency_test(ct)
for key in ['statistic','p','cramers_v','min_expected']:assert np.isclose(chi[key],S['chi'][key],atol=1e-10,rtol=0)
assert expected.min()>5 and ct.to_numpy().sum()==3341
pred=pd.read_csv(ROOT/'results/tables/test_predictions.csv',index_col='source_index')
assert pred.index.tolist()==list(test_idx);np.testing.assert_array_equal(pred.rings,df.loc[test_idx,'rings'])
for r in S['test_metrics']:
 recalculated=metrics(pred.rings,pred[r['model']])
 for key,value in recalculated.items():assert np.isclose(value,r[key],atol=1e-10,rtol=0)
np.testing.assert_allclose(pred.Baseline,train.rings.mean(),atol=1e-10,rtol=0)
# Independent equation check in stored units, using only training medians.
coef=pd.read_csv(ROOT/'results/tables/full_coefficients_stored_scale.csv')
features=clean.loc[test_idx,FULL].copy();numeric=FULL[1:];values=features[numeric].fillna(train[numeric].median()).to_numpy()
design=np.column_stack([np.ones(len(features)),values,features.sex.eq('I').astype(int),features.sex.eq('M').astype(int)])
np.testing.assert_allclose(design@coef.coefficient.to_numpy(),pred.Full,atol=1e-10,rtol=0)
cv=pd.read_csv(ROOT/'results/tables/cv_fold_metrics.csv');sensitivity=pd.read_csv(ROOT/'results/tables/influence_sensitivity_cv.csv')
assert len(cv)==15 and len(sensitivity)==5
assert (cv.fit_n+cv.validation_n==3341).all()
assert (sensitivity.training_before+sensitivity.validation_n==3341).all()
assert (sensitivity.training_after+sensitivity.removed==sensitivity.training_before).all()
assert S['diagnostics']['rank']==S['diagnostics']['design_columns']==10
manifest=json.loads((ROOT/'results/manifest.json').read_text())
for name,expected in manifest['artifacts'].items():assert sha(ROOT/name)==expected,name
nb=nbformat.read(ROOT/f'notebooks/{prefix}_Analysis.ipynb',as_version=4)
code=[c for c in nb.cells if c.cell_type=='code']
assert len(code)==17 and [c.execution_count for c in code]==list(range(1,18))
assert not any(o.output_type=='error' for c in code for o in c.outputs)
assert sum('image/png' in o.get('data',{}) for c in code for o in c.outputs)>=10
for figure in (ROOT/'results/figures').glob('*.png'):
 pixels=np.asarray(Image.open(figure).convert('RGB'));spread=pixels.max(axis=2).astype(int)-pixels.min(axis=2).astype(int)
 assert (spread>40).sum()>1000,figure
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';OM='http://schemas.openxmlformats.org/officeDocument/2006/math';A='http://schemas.openxmlformats.org/drawingml/2006/main';P='http://schemas.openxmlformats.org/presentationml/2006/main'
logo=sha(ROOT/'report/assets/tdtu-logo.png')
with zipfile.ZipFile(ROOT/f'report/{prefix}_Report{suffix}.docx') as z:
 assert z.testzip() is None
 doc=ET.fromstring(z.read('word/document.xml'));text=' '.join(n.text or '' for n in doc.findall('.//{'+W+'}t'))
 assert all(a['name'] in text and a['id'] in text for a in M['authors'])
 assert not any(t in text for t in ['[[','STUDENT PERFORMANCE','MIDTERM REPORT','MERN'])
 assert len(doc.findall('.//{'+OM+'}oMath'))==9
 fields=[e.get('{'+W+'}instr','') for e in doc.findall('.//{'+W+'}fldSimple')]
 assert sum(f.startswith('PAGEREF') for f in fields)==54
 assert sum(f.startswith('SEQ ') for f in fields)==23
 assert len(doc.findall('.//{'+W+'}hyperlink/{'+W+'}r/{'+W+'}tab'))==54
 toc=[x.text for x in doc.findall('.//{'+W+'}instrText') if 'TOC ' in (x.text or '')];assert len(toc)==3
 headings=[p for p in doc.findall('.//{'+W+'}p') if p.find('{'+W+'}pPr/{'+W+'}pStyle') is not None and p.find('{'+W+'}pPr/{'+W+'}pStyle').get('{'+W+'}val') in {'Heading1','Heading2'}]
 assert all('REFERENCES' not in ''.join(e.text or '' for e in p.findall('.//{'+W+'}t')) for p in headings)
 for section in doc.findall('.//{'+W+'}sectPr'):
  margins=section.find('{'+W+'}pgMar')
  for side,value in [('left',1984),('right',1134),('top',1984),('bottom',1701)]:assert abs(int(margins.get('{'+W+'}'+side))-value)<=1
 assert any(hashlib.sha256(z.read(n)).hexdigest()==logo for n in z.namelist() if n.startswith('word/media/'))
with zipfile.ZipFile(ROOT/f'slides/{prefix}_Presentation{suffix}.pptx') as z:
 assert z.testzip() is None
 names=z.namelist();slides=sorted([n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=lambda n:int(re.search(r'(\d+)\.xml',n)[1]))
 assert len(slides)==19
 assert len([n for n in names if n.endswith('.xml') and '/charts/' in n and '/_rels/' not in n])==6
 assert len([n for n in names if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')])==6
 for i,name in enumerate(slides,1):
  s=ET.fromstring(z.read(name));assert len(s.findall('.//{'+P+'}pic'))==1
  nt=ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
  notes=' '.join(e.text or '' for e in nt.findall('.//{'+A+'}t'))
  assert 'Thời lượng dự kiến:' in notes and 'Nguồn:' in notes
 assert any(hashlib.sha256(z.read(n)).hexdigest()==logo for n in names if n.startswith('ppt/media/'))
 slide2=' '.join(e.text or '' for e in ET.fromstring(z.read(slides[1])).findall('.//{'+A+'}t'))
 assert (M['youtube_url'] in slide2) if M.get('youtube_url') else ('Video link pending' in slide2)
for rel in [f'report/{prefix}_Report{suffix}.pdf',f'slides/{prefix}_Presentation{suffix}.pdf']:assert (ROOT/rel).read_bytes().startswith(b'%PDF-')
if (ROOT/'results/office_verification.json').exists():
 for rel,expected in json.loads((ROOT/'results/office_verification.json').read_text())['sha256'].items():assert sha(ROOT/rel)==expected,rel
print('PASS: raw/schema, quality audit, disjoint saved split, Holm/tests, independent prediction equation, metrics, manifest, 17 clean code cells/10 figures, Word OMML/fields/tabs, 19 slides/notes/logo and 6 chart workbooks.')
