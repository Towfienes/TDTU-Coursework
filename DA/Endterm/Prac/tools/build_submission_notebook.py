"""Build and execute the clean, self-contained submission notebook."""
import copy
from pathlib import Path
import json
import nbformat as nbf
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

# Read the original authored notebook structure
with open(ROOT / 'tools/build_notebook.py', 'r', encoding='utf-8') as f:
    source_code = f.read()

# Replace the dependencies and hardcoded paths in the code string
cell1_old = """from pathlib import Path
import hashlib
import json
import re
import sys
import importlib.metadata
import numpy as np
import pandas as pd
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib.cbook import boxplot_stats
import seaborn as sns
from IPython.display import display

ROOT = Path.cwd().resolve()
if not (ROOT / 'data/raw/student-por.csv').exists():
    ROOT = ROOT.parent
assert (ROOT / 'data/raw/student-por.csv').exists(), 'Run from the project root or notebooks directory.'
sys.path.insert(0, str(ROOT))
from src.analysis import BANDS, RAW_COLUMNS, NUMERIC_COLUMNS, performance_bands, normalize_within_group, comprehensive_report

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 220)
sns.set_theme(style='whitegrid', palette='deep', font='DejaVu Sans', font_scale=1.05)
plt.rcParams.update({'figure.dpi': 110, 'savefig.dpi': 200, 'axes.titleweight': 'bold'})
TABLES = ROOT / 'results/tables'
FIGURES = ROOT / 'results/figures'
TABLES.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

def save_table(frame, name, index=True):
    frame.to_csv(TABLES / f'{name}.csv', index=index)

def save_figure(fig, name):
    fig.tight_layout()
    fig.savefig(FIGURES / f'{name}.png', bbox_inches='tight', facecolor='white')
    fig.savefig(FIGURES / f'{name}.svg', bbox_inches='tight', facecolor='white')
    plt.show()"""

cell1_new = """from pathlib import Path
import hashlib
import json
import re
import sys
import importlib.metadata
import numpy as np
import pandas as pd
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib.cbook import boxplot_stats
import seaborn as sns
from IPython.display import display

ROOT = Path.cwd().resolve()

# Find the dataset in current folder or standard subfolders
candidates = [
    Path('student-por.csv'),
    ROOT / 'student-por.csv',
    ROOT / 'data/raw/student-por.csv',
    ROOT.parent / 'data/raw/student-por.csv',
]
raw_path = next((p for p in candidates if p.exists()), None)
assert raw_path is not None, 'student-por.csv not found in current folder or data/raw/'

# Domain definitions embedded directly (no external module dependency)
BANDS = ['0–9', '10–14', '15–20']
RAW_COLUMNS = 'school sex age address famsize Pstatus Medu Fedu Mjob Fjob reason guardian traveltime studytime failures schoolsup famsup paid activities nursery higher internet romantic famrel freetime goout Dalc Walc health absences G1 G2 G3'.split()
NUMERIC_COLUMNS = 'age Medu Fedu traveltime studytime failures famrel freetime goout Dalc Walc health absences G1 G2 G3'.split()

def performance_bands(grades):
    '''Analyst-defined bands, not an official grading policy.'''
    if grades.isna().any() or not grades.between(0, 20).all():
        raise ValueError('Grades must be complete and lie in [0, 20].')
    return pd.cut(grades, [-1, 9, 14, 20], labels=BANDS, ordered=True)

def normalize_within_group(frame, group='school', column='G3'):
    '''Relative group scale; a constant group is assigned zero.'''
    if frame[[group, column]].isna().any().any():
        raise ValueError('Group normalization requires complete group/value columns.')
    if not np.isfinite(frame[column]).all():
        raise ValueError('Normalization values must be finite.')
    grouped = frame.groupby(group, observed=True)[column]
    low = grouped.transform('min')
    span = grouped.transform('max') - low
    return (frame[column] - low).div(span.where(span.ne(0), 1))

def comprehensive_report(frame):
    '''Display and return a JSON-safe summary without reading files/global data.'''
    required = {'G1', 'G2', 'G3', 'performance_band'}
    if not required.issubset(frame.columns):
        raise ValueError(f'Missing required columns: {sorted(required - set(frame.columns))}')
    total = len(frame)
    counts = frame['performance_band'].value_counts().reindex(BANDS, fill_value=0)
    distribution = {
        band: {'count': int(count), 'percent': float(100 * count / total) if total else 0.0}
        for band, count in counts.items()
    }
    summary = {
        'total_records': total,
        'total_columns': len(frame.columns),
        'missing_by_column': {name: int(value) for name, value in frame.isna().sum().items()},
        'grade_statistics': json.loads(frame[['G1', 'G2', 'G3']].agg(['count', 'mean', 'std', 'min', 'median', 'max']).to_json()),
        'performance_distribution': distribution,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False))
    return summary

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 220)
sns.set_theme(style='whitegrid', palette='deep', font='DejaVu Sans', font_scale=1.05)
plt.rcParams.update({'figure.dpi': 110, 'savefig.dpi': 200, 'axes.titleweight': 'bold'})
TABLES = ROOT / 'results/tables'
FIGURES = ROOT / 'results/figures'
PROCESSED = ROOT / 'data/processed'
TABLES.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

def save_table(frame, name, index=True):
    frame.to_csv(TABLES / f'{name}.csv', index=index)

def save_figure(fig, name):
    fig.tight_layout()
    fig.savefig(FIGURES / f'{name}.png', bbox_inches='tight', facecolor='white')
    fig.savefig(FIGURES / f'{name}.svg', bbox_inches='tight', facecolor='white')
    plt.show()"""

cell3_old = """raw_path = ROOT / 'data/raw/student-por.csv'
raw_hash = hashlib.sha256(raw_path.read_bytes()).hexdigest()"""

cell3_new = """raw_hash = hashlib.sha256(raw_path.read_bytes()).hexdigest()"""

modified_source = source_code.replace(cell1_old, cell1_new).replace(cell3_old, cell3_new)
target_path = ROOT / 'notebooks/Notebook_524H0195_524H0191_524H0186_524H0169.ipynb'
modified_source = modified_source.replace(
    "nbf.write(nb, ROOT/'notebooks/VibeCoding_Expert_DAV_Endterm_Analysis.ipynb')",
    f"nbf.write(nb, '{target_path}')"
)

exec(modified_source, {'__file__': str(ROOT / 'tools/build_submission_notebook.py')})

# Now execute the generated notebook using nbclient
print('Executing submission notebook...')
notebook = nbf.read(target_path, as_version=4)

with tempfile.TemporaryDirectory(prefix='dav-sub-kernel-') as directory:
    kernel_dir = Path(directory) / 'dav'
    kernel_dir.mkdir()
    (kernel_dir / 'kernel.json').write_text(json.dumps({
        'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'display_name': 'DAV Python',
        'language': 'python'
    }))
    manager = KernelManager(kernel_name='dav', kernel_spec_manager=KernelSpecManager(kernel_dirs=[directory]))
    client = NotebookClient(notebook, timeout=180, km=manager, resources={'metadata': {'path': str(ROOT)}}, allow_errors=False)
    try:
        client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)

nbf.write(notebook, target_path)
print(f'Successfully generated and executed: {target_path}')
