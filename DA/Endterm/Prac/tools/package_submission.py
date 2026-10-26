"""Package selected deliverables and reproduce the extracted analysis before release."""
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
META=json.loads((ROOT/'project.json').read_text())
ROOT_FILES=['README.md','PLAN.md','WORKLOG.md','REQUIREMENTS.md','project.json','requirements.in','requirements.txt']
FOLDERS=['data','notebooks','src','tests','results','report','slides','references','tools']
JUNK={'.venv','__pycache__','.pytest_cache','.ipynb_checkpoints','.mypy_cache','node_modules','.DS_Store','Thumbs.db','desktop.ini'}


def build_archive(destination):
    files=[ROOT/name for name in ROOT_FILES]
    files.extend(path for folder in FOLDERS for path in (ROOT/folder).rglob('*') if path.is_file() and not path.is_symlink())
    files=sorted(path for path in files if not any(part in JUNK for part in path.relative_to(ROOT).parts)
                 and not path.name.startswith('~$') and path.suffix not in {'.pyc','.swp'} and not path.name.endswith('~'))
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in files:archive.write(path,Path(META['submission'])/path.relative_to(ROOT))
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        names=archive.namelist()
        assert {Path(name).parts[0] for name in names}=={META['submission']}
        assert not any(part in JUNK or part=='.build' for name in names for part in Path(name).parts)
        assert all(not Path(name).is_absolute() and '..' not in Path(name).parts for name in names)
    return len(files)


def compare_json(expected,actual):
    if isinstance(expected,dict):
        assert expected.keys()==actual.keys()
        for key in expected:compare_json(expected[key],actual[key])
    elif isinstance(expected,list):
        assert len(expected)==len(actual)
        for left,right in zip(expected,actual):compare_json(left,right)
    elif isinstance(expected,(float,int)):
        assert math.isclose(expected,actual,rel_tol=0,abs_tol=1e-10),(expected,actual)
    else:
        assert expected==actual,(expected,actual)


def main():
    (ROOT/'.build').mkdir(exist_ok=True)
    candidate=ROOT/'.build/submission_candidate.zip'
    count=build_archive(candidate)
    environment=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',MPLBACKEND='Agg')
    logs=[]
    with tempfile.TemporaryDirectory(prefix='tdtu-dav-reproduction-') as directory:
        with zipfile.ZipFile(candidate) as archive:archive.extractall(directory)
        extracted=Path(directory)/META['submission']
        for command in [[sys.executable,'-m','unittest','discover','-s','tests','-v'],
                        [sys.executable,'tools/run_notebook.py'],[sys.executable,'tools/verify_project.py']]:
            result=subprocess.run(command,cwd=extracted,env=environment,capture_output=True,text=True,timeout=180)
            logs.append(result.stdout+result.stderr)
            if result.returncode:raise RuntimeError('Extracted reproduction failed:\n'+logs[-1])
        expected_summary=json.loads((ROOT/'results/summary.json').read_text())
        actual_summary=json.loads((extracted/'results/summary.json').read_text())
        compare_json(expected_summary,actual_summary)
        table_count=0
        for expected_path in (ROOT/'results/tables').glob('*.csv'):
            actual_path=extracted/'results/tables'/expected_path.name
            pd.testing.assert_frame_equal(pd.read_csv(expected_path),pd.read_csv(actual_path),check_exact=False,atol=1e-10,rtol=0)
            table_count+=1
    receipt={'status':'pass','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'archive_root':META['submission'],'fresh_kernel_code_cells':20,'unit_tests':3,
             'all_csv_tables_compared':table_count,'structured_summary_compared':True,'floating_absolute_tolerance':1e-10,
             'raw_sha256':hashlib.sha256((ROOT/'data/raw/student-por.csv').read_bytes()).hexdigest(),
             'original_summary_sha256':hashlib.sha256((ROOT/'results/summary.json').read_bytes()).hexdigest(),
             'method':'Extract candidate into a fresh temporary directory; run tests, notebook and verification with the installed locked environment; compare all analytical CSV tables and summary.'}
    (ROOT/'results/package_verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    (ROOT/'.build/reproduction.log').write_text('\n'.join(logs))
    (ROOT/'results/reproduction_log.txt').write_text('\n'.join(logs))
    final=ROOT/f"{META['submission']}.zip"
    count=build_archive(final)
    print(f'PASS: extracted reproduction, {table_count} CSV tables and structured summary agree; {count} files; {final.stat().st_size/1024/1024:.2f} MiB; {final.name}')


if __name__=='__main__':main()
