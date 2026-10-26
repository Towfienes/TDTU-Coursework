"""Workspace-only archive verification; never included in the submission."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import time
import zipfile
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
archive = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2]).resolve()
target.mkdir(parents=True, exist_ok=False)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for name in z.namelist():
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        assert not any(part in {'.venv', '__pycache__', '.ruff_cache'} for part in Path(name).parts)
    z.extractall(target)
root = target / 'ML_Midterm_Final'
for line in (root/'requirements.txt').read_text().splitlines():
    name, version = line.split('==')
    assert importlib.metadata.version(name) == version
checksum = root/'verification/checksums.sha256'
if checksum.exists():
    for line in checksum.read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, name
env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', MPLBACKEND='Agg')
commands = [
    ('data', ['-m','src.data']),
    ('tests_before', ['-m','unittest','discover','-s','tests','-v']),
    ('notebooks', ['notebooks/execute.py']),
    ('q1', ['-m','src.q1_models']),
    ('q2', ['-m','src.q2_classification']),
    ('report', ['-m','src.build_report']),
    ('tests_after', ['-m','unittest','discover','-s','tests','-v']),
    ('lint', ['-m','ruff','check','src','tests','notebooks/execute.py']),
    ('syntax', ['-m','compileall','-q','src','tests','notebooks/execute.py']),
]
records=[]
for label, args in commands:
    started=time.perf_counter()
    with (target/(label+'.log')).open('w') as log:
        result=subprocess.run([sys.executable,*args],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
    record=dict(check=label,command=[sys.executable,*args],returncode=result.returncode,elapsed_seconds=time.perf_counter()-started)
    records.append(record)
    print(json.dumps(record),flush=True)
    assert result.returncode==0, label
reference=BASE/'ML_Midterm_Final'
for name in ['q1_metrics.json','q2_selection.json']:
    assert json.loads((root/'results'/name).read_text())==json.loads((reference/'results'/name).read_text()),name
for name in ['q2_model_comparison.csv','q2_studies.csv','q2_fold_scores.csv','q2_predictions.csv']:
    pd.testing.assert_frame_equal(pd.read_csv(root/'results'/name),pd.read_csv(reference/'results'/name),rtol=1e-12,atol=1e-12)
a=json.loads((root/'results/q2_summary.json').read_text());b=json.loads((reference/'results/q2_summary.json').read_text())
a.pop('elapsed_seconds');b.pop('elapsed_seconds');assert a==b
with np.load(root/'results/q1_arrays.npz') as a,np.load(reference/'results/q1_arrays.npz') as b:
    assert set(a.files)==set(b.files)
    for key in a.files:np.testing.assert_allclose(a[key],b[key],rtol=1e-12,atol=1e-12)
for p in (reference/'figures').glob('*.png'):
    assert (root/'figures'/p.name).read_bytes()==p.read_bytes(),p.name
from pypdf import PdfReader
a=PdfReader(root/'report/Machine_Learning_Midterm_Final.pdf');b=PdfReader(reference/'report/Machine_Learning_Midterm_Final.pdf')
assert len(a.pages)==len(b.pages)==19
assert [p.extract_text() for p in a.pages]==[p.extract_text() for p in b.pages]
summary=dict(status='PASS',archive=str(archive),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),extraction=str(target),verified_at_utc=datetime.now(timezone.utc).isoformat(),environment='All direct pinned dependencies verified in independently installed clean venv',commands=records,numerical_comparison='Q1 JSON/NPZ, Q2 selection/summary and four CSVs match; floating CSV/array tolerance 1e-12; experiment figures byte-identical; 19 PDF page texts identical')
(target/'reproduction_summary.json').write_text(json.dumps(summary,indent=2))
print('PASS: clean extraction, environment, all executions and numerical comparisons',flush=True)
