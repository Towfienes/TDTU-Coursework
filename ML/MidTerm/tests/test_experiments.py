"""Check preprocessing isolation and independently recompute exported test metrics."""
import sys
from pathlib import Path
import unittest
import json
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from run_experiments import ROOT, NUMERIC, load_credit, make_preprocessor, classification_metrics
from sklearn.metrics import mean_squared_error, r2_score


class ExperimentTests(unittest.TestCase):
    def test_preprocessing_fits_training_only(self):
        frame, audit = load_credit()
        train = frame.drop(columns='class').iloc[:100].copy()
        test = train.iloc[:1].copy()
        test.loc[test.index[0], 'age'] = 1000
        test.loc[test.index[0], 'checking_status'] = 'unseen_category'
        prepare = make_preprocessor(audit['categorical'])
        prepare.fit(train)
        transformed = prepare.transform(test)
        age_index = NUMERIC.index('age')
        self.assertGreater(transformed[0, age_index], 1)
        scaler = prepare.named_transformers_['numeric']
        np.testing.assert_array_equal(scaler.data_max_, train[NUMERIC].max().to_numpy())
        self.assertFalse(any('class' in name for name in prepare.get_feature_names_out()))
        encoder = prepare.named_transformers_['categorical']
        start = len(NUMERIC)
        self.assertEqual(transformed[0, start:start+len(encoder.categories_[0])].sum(), 0)

    def test_exported_results_and_split_are_consistent(self):
        results = ROOT / 'results'
        metrics = json.loads((results / 'q2_metrics.json').read_text())
        predictions = pd.read_csv(results / 'q2_test_predictions.csv')
        split = pd.read_csv(results / 'q2_split.csv')
        folds = pd.read_csv(results / 'q2_folds.csv')
        self.assertEqual(len(predictions), 200)
        self.assertEqual(predictions.row_id.nunique(), 200)
        self.assertEqual(len(folds), 800)
        self.assertEqual(folds.row_id.nunique(), 800)
        self.assertFalse(set(folds.row_id) & set(predictions.row_id))
        self.assertEqual(set(split.loc[split.split=='test', 'row_id']), set(predictions.row_id))
        self.assertTrue((folds.validation_fold.value_counts() == 160).all())
        self.assertEqual(int(predictions.actual_bad.sum()), 60)
        winner = max(metrics['models'], key=lambda row: row['cv_macro_f1'])['model']
        self.assertEqual(metrics['winner_by_cv'], winner)
        for row in metrics['models']:
            name = row['model']
            recomputed = classification_metrics(predictions.actual_bad,
                                                predictions[name+'__prediction'], predictions[name+'__score'])
            for key, value in recomputed.items():
                if key == 'confusion_matrix': self.assertEqual(row[key], value)
                else: self.assertAlmostEqual(row[key], value, places=12)
        q1 = json.loads((results/'q1_metrics.json').read_text())
        linear = np.load(results/'q1_linear_data.npz')
        self.assertAlmostEqual(q1['linear']['mse'], mean_squared_error(linear['y'][linear['test']], linear['predicted']))
        self.assertAlmostEqual(q1['linear']['r2'], r2_score(linear['y'][linear['test']], linear['predicted']))

if __name__ == '__main__': unittest.main()
