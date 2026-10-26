import hashlib
import json
from pathlib import Path
import unittest
import nbformat
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


class TestArtifacts(unittest.TestCase):
    def test_executed_notebooks_have_real_outputs(self):
        records = json.loads(
            (ROOT / "verification/notebook_execution.json").read_text()
        )
        self.assertEqual(len(records), 3)
        for record in records:
            nb = nbformat.read(ROOT / "notebooks" / record["notebook"], as_version=4)
            cells = [c for c in nb.cells if c.cell_type == "code"]
            self.assertEqual(len(cells), record["code_cells"])
            self.assertGreaterEqual(len(cells), 7)
            images = 0
            for i, cell in enumerate(cells):
                self.assertEqual(cell.execution_count, i + 1)
                self.assertFalse(any(o.output_type == "error" for o in cell.outputs))
                images += sum("image/png" in o.get("data", {}) for o in cell.outputs)
            self.assertGreaterEqual(images, 2)
            digest = hashlib.sha256(
                "\n".join(c.source for c in cells).encode()
            ).hexdigest()
            self.assertEqual(digest, record["source_sha256"])

    def test_report_values_and_fonts(self):
        report = PdfReader(
            ROOT / "report/Machine_Learning_Midterm_Final.pdf", strict=True
        )
        self.assertGreaterEqual(len(report.pages), 15)
        self.assertLessEqual(len(report.pages), 25)
        texts = [p.extract_text() for p in report.pages]
        self.assertTrue(all(len(text) > 300 for text in texts))
        text = "\n".join(texts)
        for name in ["Ngô Lâm Tiến", "Nguyễn Công Thành", "Nguyễn Lê Nhật Tâm"]:
            self.assertIn(name, text)
        self.assertIn("524H0191", text)
        self.assertIn("FACULTY OF INFORMATION TECHNOLOGY", text)
        q1 = json.loads((ROOT / "results/q1_metrics.json").read_text())
        q2 = json.loads((ROOT / "results/q2_summary.json").read_text())
        for value in [
            q1["linear"]["r2"],
            q1["linear"]["mse"],
            q1["linear"]["rmse"],
            q1["linear"]["mae"],
            q1["logistic"]["accuracy"],
            q1["logistic"]["f1"],
            q1["logistic"]["roc_auc"],
            q2["champion_metrics"]["test_macro_f1"],
            q2["champion_metrics"]["test_accuracy"],
            q2["champion_metrics"]["test_roc_auc"],
        ]:
            self.assertIn(f"{value:.6f}", text)
        self.assertIn(q2["champion_selected_by_train_cv"], text)
        for page in report.pages:
            for ref in page["/Resources"].get("/Font", {}).values():
                font = ref.get_object()
                if font["/Subtype"] == "/TrueType":
                    self.assertIn("/FontFile2", font["/FontDescriptor"])

    def test_figure_and_numeric_trace(self):
        trace = json.loads(
            (ROOT / "report/report_source/numerical_trace.json").read_text()
        )
        self.assertEqual(
            trace["q1"], json.loads((ROOT / "results/q1_metrics.json").read_text())
        )
        self.assertEqual(
            trace["selected_q2"],
            json.loads((ROOT / "results/q2_summary.json").read_text())[
                "champion_metrics"
            ],
        )
        for fig in trace["figures"]:
            self.assertEqual(
                fig["sha256"],
                hashlib.sha256((ROOT / fig["file"]).read_bytes()).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
