"""Report missing external submission facts; --json is consumed by document builders."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.submission import readiness_issues
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--json',action='store_true');args=parser.parse_args()
    issues=readiness_issues(json.loads((ROOT/'project.json').read_text()))
    if args.json:print(json.dumps({'ready':not issues,'issues':issues}));sys.exit(0)
    print('READY' if not issues else 'REVIEW ONLY — missing external facts:')
    for issue in issues:print('- '+issue)
    sys.exit(2 if issues else 0)
