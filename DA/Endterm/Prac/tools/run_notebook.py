"""Run all cells in a fresh kernel using this Python interpreter."""
from pathlib import Path
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]
path = ROOT/'notebooks/VibeCoding_Expert_DAV_Endterm_Analysis.ipynb'
notebook = nbformat.read(path, as_version=4)
# A temporary kernelspec keeps reproduction independent of a globally installed kernel.
with tempfile.TemporaryDirectory(prefix='dav-kernel-') as directory:
    import json
    kernel_dir = Path(directory)/'dav'
    kernel_dir.mkdir()
    (kernel_dir/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'DAV project Python','language':'python'}))
    manager = KernelManager(kernel_name='dav', kernel_spec_manager=KernelSpecManager(kernel_dirs=[directory]))
    client = NotebookClient(notebook, timeout=180, km=manager, resources={'metadata':{'path':str(ROOT)}}, allow_errors=False)
    try:
        client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
nbformat.write(notebook, path)
assert all(output.output_type != 'error' for cell in notebook.cells if cell.cell_type == 'code' for output in cell.outputs)
print(f'Executed {sum(cell.cell_type == "code" for cell in notebook.cells)} code cells without errors: {path.name}')
