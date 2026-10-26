import json
import hashlib
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from src.data import ROOT, NUMERIC, load_data
from src.q2_classification import split_data, make_pipeline, models, evaluate_cv


class TestCredit(unittest.TestCase):
    def test_provenance_and_schema(self):
        df = load_data()
        self.assertEqual(df.shape, (1000, 21))
        self.assertEqual(
            df["class"].value_counts().to_dict(), {"good": 700, "bad": 300}
        )
        self.assertFalse(df.isna().any().any())
        self.assertEqual(int(df.duplicated().sum()), 0)
        p = json.loads((ROOT / "data/metadata/provenance.json").read_text())
        payload = (ROOT / "data/raw/credit-g.arff").read_bytes()
        self.assertEqual(p["raw_sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(p["raw_md5"], p["official_md5"])
        self.assertEqual((p["dataset_id"], p["dataset_version"]), (31, 1))
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "data/raw").mkdir(parents=True)
            (root / "data/metadata").mkdir()
            (root / "data/raw/credit-g.arff").write_bytes(payload + b"corrupted")
            (root / "data/metadata/openml_31_response.json").write_bytes(
                (ROOT / "data/metadata/openml_31_response.json").read_bytes()
            )
            with self.assertRaises(ValueError):
                load_data(root)

    def test_split_and_folds(self):
        Xtr, Xte, ytr, yte = split_data(load_data())
        split = json.loads((ROOT / "data/metadata/split.json").read_text())
        self.assertEqual((len(Xtr), len(Xte)), (800, 200))
        self.assertEqual(ytr.value_counts().to_dict(), {0: 560, 1: 240})
        self.assertEqual(yte.value_counts().to_dict(), {0: 140, 1: 60})
        self.assertFalse(set(Xtr.index) & set(Xte.index))
        self.assertEqual(split["train_indices"], Xtr.index.tolist())
        seen = []
        for f in json.loads((ROOT / "data/metadata/folds.json").read_text()):
            self.assertFalse(set(f["train"]) & set(f["validation"]))
            self.assertEqual(len(f["train"]), 640)
            self.assertEqual(len(f["validation"]), 160)
            seen += f["validation"]
        self.assertEqual(sorted(seen), list(range(800)))

    def test_fold_specific_preprocessing_and_unknown_categories(self):
        Xtr, Xte, ytr, yte = split_data(load_data())
        for f in json.loads((ROOT / "data/metadata/folds.json").read_text()):
            train = Xtr.iloc[f["train"]]
            target = ytr.iloc[f["train"]]
            pipe = make_pipeline(LogisticRegression(max_iter=2000), Xtr).fit(
                train, target
            )
            prep = pipe.named_steps["preprocess"]
            numeric = prep.named_transformers_["numeric"]
            np.testing.assert_allclose(
                numeric.named_steps["impute"].statistics_, train[NUMERIC].median()
            )
            np.testing.assert_allclose(
                numeric.named_steps["scale"].mean_, train[NUMERIC].mean(), atol=1e-10
            )
            self.assertEqual(int(numeric.named_steps["scale"].n_samples_seen_), 640)
            transformed = prep.transform(Xtr.iloc[f["validation"]])
            self.assertTrue(np.isfinite(transformed).all())
            self.assertEqual(transformed.shape[0], 160)
            encode = prep.named_transformers_["categorical"].named_steps["encode"]
            categorical = [c for c in Xtr if c not in NUMERIC]
            for col, categories in zip(categorical, encode.categories_):
                self.assertEqual(set(categories), set(train[col]))
        pipe = make_pipeline(LogisticRegression(max_iter=2000), Xtr).fit(Xtr, ytr)
        sentinel = Xte.iloc[:1].copy()
        sentinel["checking_status"] = "UNSEEN_CATEGORY"
        self.assertTrue(
            np.isfinite(pipe.named_steps["preprocess"].transform(sentinel)).all()
        )
        self.assertEqual(pipe.predict(sentinel).shape, (1,))

    def test_metrics_recomputed_from_predictions(self):
        comparison = pd.read_csv(ROOT / "results/q2_model_comparison.csv")
        pred = pd.read_csv(ROOT / "results/q2_predictions.csv")
        self.assertEqual(len(comparison), 13)
        self.assertEqual(set(comparison.model), set(models()))
        for _, r in comparison.iterrows():
            p = pred[r.model + "__prediction"]
            s = pred[r.model + "__score"]
            y = pred.y_true
            self.assertAlmostEqual(r.test_accuracy, accuracy_score(y, p), places=12)
            self.assertAlmostEqual(
                r.test_macro_f1, f1_score(y, p, average="macro"), places=12
            )
            self.assertAlmostEqual(r.test_roc_auc, roc_auc_score(y, s), places=12)

    def test_training_only_selection_and_studies(self):
        comparison = pd.read_csv(ROOT / "results/q2_model_comparison.csv")
        selection = json.loads((ROOT / "results/q2_selection.json").read_text())
        expected = (
            comparison[comparison.model != "Dummy majority"]
            .sort_values(["cv_macro_f1_mean", "model"], ascending=[False, True])
            .iloc[0]
            .model
        )
        self.assertEqual(selection["champion"], expected)
        self.assertTrue(selection["selected_before_test"])
        folds = pd.read_csv(ROOT / "results/q2_fold_scores.csv")
        for _, r in comparison.iterrows():
            scores = folds[(folds.stage == "benchmark") & (folds.model == r.model)]
            self.assertEqual(len(scores), 5)
            self.assertAlmostEqual(
                r.cv_macro_f1_mean, scores.validation_macro_f1.mean(), places=12
            )
            self.assertAlmostEqual(
                r.cv_macro_f1_std, scores.validation_macro_f1.std(ddof=1), places=12
            )
            self.assertAlmostEqual(
                r.fold_generalization_gap,
                (scores.train_macro_f1 - scores.validation_macro_f1).mean(),
                places=12,
            )
        studies = pd.read_csv(ROOT / "results/q2_studies.csv")
        self.assertEqual(set(studies.family), {"Decision Tree", "KNN", "RBF SVM"})
        for _, r in studies.iterrows():
            scores = folds[
                (folds.stage == "study")
                & (folds.model == r.family)
                & (folds.configuration == r.configuration)
            ]
            self.assertEqual(len(scores), 5)
            self.assertAlmostEqual(
                r.cv_macro_f1_mean, scores.validation_macro_f1.mean(), places=12
            )

    def test_cv_determinism(self):
        Xtr, _, ytr, _ = split_data(load_data())
        folds = [
            (np.asarray(f["train"]), np.asarray(f["validation"]))
            for f in json.loads((ROOT / "data/metadata/folds.json").read_text())
        ]
        a, sa = evaluate_cv(models()["Logistic Regression"], Xtr, ytr, folds)
        b, sb = evaluate_cv(models()["Logistic Regression"], Xtr, ytr, folds)
        np.testing.assert_array_equal(sa["test_score"], sb["test_score"])


if __name__ == "__main__":
    unittest.main()
