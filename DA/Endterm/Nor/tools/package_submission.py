"""Build clean archives only after an extracted, fresh-kernel reproduction."""
import argparse
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.submission import readiness_issues

META = json.loads((ROOT / 'project.json').read_text())
ROOT_FILES = ['README.md', 'PLAN.md', 'WORKLOG.md', 'REQUIREMENTS.md',
              'project.json', 'requirements.in', 'requirements.txt']
FOLDERS = ['data', 'notebooks', 'src', 'tests', 'results', 'report', 'slides', 'references', 'tools']
JUNK = {'.build', '.venv', 'env', '__pycache__', '.pytest_cache', '.ipynb_checkpoints',
        '.mypy_cache', 'node_modules', '.DS_Store', 'Thumbs.db', 'desktop.ini', 'ehthumbs.db'}
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


def build_archive(destination, archive_root, release=False):
    files = [ROOT / name for name in ROOT_FILES]
    files += [p for folder in FOLDERS for p in (ROOT / folder).rglob('*') if p.is_file()]
    files = sorted(p for p in files if not p.is_symlink()
                   and not any(part in JUNK for part in p.relative_to(ROOT).parts)
                   and not p.name.startswith('~$') and p.suffix not in {'.pyc', '.swp'}
                   and not p.name.endswith('~') and not (release and '_REVIEW' in p.name))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, Path(archive_root) / path.relative_to(ROOT))
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(files) == len(set(archive.namelist()))
        for name, source in zip(archive.namelist(), files):
            parts = Path(name).parts
            assert parts[0] == archive_root and '..' not in parts and not Path(name).is_absolute()
            assert not any(part in JUNK for part in parts)
            assert hashlib.sha256(archive.read(name)).hexdigest() == sha(source)
    return len(files)


def compare_json(expected, actual):
    if isinstance(expected, dict):
        assert expected.keys() == actual.keys()
        for key in expected:
            compare_json(expected[key], actual[key])
    elif isinstance(expected, list):
        assert len(expected) == len(actual)
        for left, right in zip(expected, actual):
            compare_json(left, right)
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        assert math.isclose(expected, actual, rel_tol=0, abs_tol=1e-10), (expected, actual)
    else:
        assert expected == actual, (expected, actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', action='store_true', help='Require real video/contribution records.')
    args = parser.parse_args()
    if args.release:
        issues = readiness_issues(META)
        if issues:
            parser.error('Release facts incomplete: ' + '; '.join(issues))
    office = json.loads((ROOT / 'results/office_verification.json').read_text())
    assert office['project_sha256'] == sha(ROOT / 'project.json'), 'Rebuild and reverify edited metadata.'
    assert office['all_report_pages_visually_reviewed'] and office['all_slide_pages_visually_reviewed']
    for name, expected in office['sha256'].items():
        assert sha(ROOT / name) == expected, name
    suffix = '' if args.release else '_REVIEW'
    candidate = ROOT / '.build/submission_candidate.zip'
    count = build_archive(candidate, META['group'], args.release)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg',
                       OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    logs = []
    with tempfile.TemporaryDirectory(prefix='tdtu-nor-reproduction-') as directory:
        with zipfile.ZipFile(candidate) as archive:
            archive.extractall(directory)
        extracted = Path(directory) / META['group']
        commands = [[sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                    [sys.executable, 'tools/run_notebook.py'],
                    [sys.executable, 'tools/verify_project.py']]
        try:
            for command in commands:
                result = subprocess.run(command, cwd=extracted, env=environment,
                                        capture_output=True, text=True, timeout=600)
                logs.append('$ ' + ' '.join(command[1:]) + '\n' + result.stdout + result.stderr)
                if result.returncode:
                    raise RuntimeError('Extracted reproduction failed:\n' + logs[-1])
            compare_json(json.loads((ROOT / 'results/summary.json').read_text()),
                         json.loads((extracted / 'results/summary.json').read_text()))
            tables = sorted((ROOT / 'results/tables').glob('*.csv'))
            assert {p.name for p in tables} == {p.name for p in (extracted / 'results/tables').glob('*.csv')}
            for expected in tables:
                pd.testing.assert_frame_equal(pd.read_csv(expected),
                    pd.read_csv(extracted / 'results/tables' / expected.name),
                    check_exact=False, atol=1e-10, rtol=0)
        finally:
            (ROOT / '.build/reproduction.log').write_text('\n'.join(logs))
    receipt = {'status': 'pass', 'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'mode': 'release' if args.release else 'review', 'fresh_kernel_code_cells': 17,
               'unit_tests': 7, 'all_csv_tables_compared': len(tables),
               'structured_summary_compared': True, 'floating_absolute_tolerance': 1e-10,
               'raw_sha256': sha(ROOT / 'data/raw/abalone.data'),
               'original_summary_sha256': sha(ROOT / 'results/summary.json'),
               'environment': 'Existing exact locked Python environment; fresh directory and kernel.',
               'method': 'Extract candidate; run tests, full notebook and verifier; compare every analytical CSV and summary.'}
    (ROOT / 'results/package_verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    (ROOT / 'results/reproduction_log.txt').write_text('\n'.join(logs))
    destinations = [(f"{META['prefix']}{suffix}.zip", META['group'])]
    destinations += [(a['id'] + suffix + '.zip', a['id']) for a in META['authors']]
    for name, archive_root in destinations:
        destination = ROOT / 'packages' / name
        count = build_archive(destination, archive_root, args.release)
        print(f'PASS: {name}; {count} files; {destination.stat().st_size / 1024**2:.2f} MiB')
    print(f'Extracted reproduction: 7 tests, 17 code cells, {len(tables)} CSV tables and structured summary agree.')


if __name__ == '__main__':
    main()
