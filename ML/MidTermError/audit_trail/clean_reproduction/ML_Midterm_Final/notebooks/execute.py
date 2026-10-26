"""Execute fresh kernels using this Python environment, from any current folder."""

from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import platform
import sys
import tempfile
import time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("notebooks", nargs="*")
    names = parser.parse_args().notebooks or [
        "Q1_Linear_Regression.ipynb",
        "Q1_Logistic_Regression.ipynb",
        "Q2_Classification.ipynb",
    ]
    results = []
    with tempfile.TemporaryDirectory() as folder:
        kernel = Path(folder) / "midterm"
        kernel.mkdir()
        (kernel / "kernel.json").write_text(
            json.dumps(
                dict(
                    argv=[
                        sys.executable,
                        "-m",
                        "ipykernel_launcher",
                        "-f",
                        "{connection_file}",
                    ],
                    display_name="Midterm current Python",
                    language="python",
                )
            )
        )
        manager = KernelSpecManager(kernel_dirs=[folder])
        for name in names:
            path = ROOT / "notebooks" / name
            if path.parent != ROOT / "notebooks" or path.suffix != ".ipynb":
                raise ValueError(
                    "Supply notebook filenames from the notebooks directory"
                )
            nb = nbformat.read(path, as_version=4)
            for cell in nb.cells:
                if cell.cell_type == "code":
                    cell.outputs = []
                    cell.execution_count = None
            digest = hashlib.sha256(
                "\n".join(c.source for c in nb.cells if c.cell_type == "code").encode()
            ).hexdigest()
            started = time.perf_counter()
            client = NotebookClient(
                nb,
                km=KernelManager(kernel_name="midterm", kernel_spec_manager=manager),
                timeout=600,
                resources={"metadata": {"path": str(ROOT)}},
            )
            client.execute(cleanup_kc=True)
            record = dict(
                notebook=name,
                status="PASS",
                code_cells=sum(c.cell_type == "code" for c in nb.cells),
                source_sha256=digest,
                executed_at_utc=datetime.now(timezone.utc).isoformat(),
                python=platform.python_version(),
                executable=sys.executable,
                elapsed_seconds=time.perf_counter() - started,
            )
            nb.metadata["execution_evidence"] = record
            nbformat.write(nb, path)
            results.append(record)
            print(json.dumps(record), flush=True)
    previous = ROOT / "verification/notebook_execution.json"
    records = (
        {r["notebook"]: r for r in json.loads(previous.read_text())}
        if previous.exists()
        else {}
    )
    records.update({r["notebook"]: r for r in results})
    previous.write_text(json.dumps(list(records.values()), indent=2))


if __name__ == "__main__":
    main()
