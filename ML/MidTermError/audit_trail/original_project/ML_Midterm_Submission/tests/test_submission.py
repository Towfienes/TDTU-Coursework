"""Offline regression tests for the prepared midterm project.
Run: python -m unittest discover -s tests -v
"""
import unittest, json
from pathlib import Path
import numpy as np
import pandas as pd
import nbformat
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from src.q1_models import LinearRegressionGD,LogisticRegressionGD,gradient_check
from src.q2_classification import create_offline_openml_mirror,make_pipeline,FEATURES,models
ROOT=Path(__file__).resolve().parents[1]

class TestSubmission(unittest.TestCase):
    def test_linear_finite_difference(self):
        rng=np.random.default_rng(6);X=rng.normal(size=(25,3));y=rng.normal(size=25)
        self.assertLess(gradient_check(LinearRegressionGD(),X,y),1e-7)
    def test_logistic_finite_difference(self):
        rng=np.random.default_rng(6);X=rng.normal(size=(25,4));y=rng.integers(0,2,size=25)
        self.assertLess(gradient_check(LogisticRegressionGD(),X,y),1e-7)
    def test_stable_sigmoid_and_loss(self):
        vals=LogisticRegressionGD.sigmoid(np.array([-1000.,0.,1000.]))
        np.testing.assert_allclose(vals,np.array([0.,.5,1.]),atol=1e-12)
        rng=np.random.default_rng(3);X=rng.normal(size=(80,3));y=(X[:,0]-X[:,1]>.0).astype(int)
        model=LogisticRegressionGD(epochs=400).fit(X,y)
        self.assertLess(model.loss_history_[-1],model.loss_history_[0])
        self.assertTrue(np.isfinite(model.loss_history_).all())
    def test_linear_converges(self):
        rng=np.random.default_rng(3);X=rng.normal(size=(80,2));y=1+2*X[:,0]-3*X[:,1]
        model=LinearRegressionGD(epochs=1000).fit(X,y)
        np.testing.assert_allclose(model.weights_,[2,-3],atol=1e-6)
        self.assertAlmostEqual(model.bias_,1,places=6)
    def test_openml_mirror_schema_and_models(self):
        df=pd.read_csv(create_offline_openml_mirror(ROOT))
        self.assertEqual(df.shape,(150,5))
        self.assertEqual(set(df['class']),{'setosa','versicolor','virginica'})
        self.assertEqual(set(df['class'].value_counts()),{50})
        self.assertEqual(len(models()),13)
    def test_preprocessor_training_only(self):
        df=pd.read_csv(create_offline_openml_mirror(ROOT)).drop_duplicates()
        Xtr,Xte,ytr,yte=train_test_split(df[FEATURES],df['class'],stratify=df['class'],test_size=.3,random_state=42)
        pipe=make_pipeline(LogisticRegression(max_iter=2000)).fit(Xtr,ytr)
        scaler=pipe.named_steps['preprocess'].named_transformers_['numeric'].named_steps['scale']
        imputer=pipe.named_steps['preprocess'].named_transformers_['numeric'].named_steps['impute']
        Xtr_imp=imputer.transform(Xtr)
        np.testing.assert_allclose(scaler.mean_,Xtr_imp.mean(axis=0),atol=1e-12)
    def test_saved_results_and_notebook_executions(self):
        q1=json.loads((ROOT/'results/q1_metrics.json').read_text())
        q2=json.loads((ROOT/'results/q2_summary.json').read_text())
        results=pd.read_csv(ROOT/'results/q2_model_comparison.csv')
        self.assertLess(q1['linear']['grad_check_max_abs_diff'],1e-6)
        self.assertLess(q1['logistic']['grad_check_max_abs_diff'],1e-6)
        self.assertEqual(q2['cleaned_rows'],149)
        self.assertEqual(q2['train_rows']+q2['test_rows'],149)
        self.assertEqual(len(results),13)
        self.assertEqual(q2['champion_selected_by_train_cv'],results.loc[results.cv_macro_f1_mean.idxmax(),'model'])
        for name in ['Q1_Linear_Regression.ipynb','Q1_Logistic_Regression.ipynb','Q2_Classification.ipynb']:
            nb=nbformat.read(ROOT/'notebooks'/name,as_version=4)
            for cell in nb.cells:
                if cell.cell_type=='code':
                    self.assertIsNotNone(cell.execution_count)
                    self.assertFalse(any(o.output_type=='error' for o in cell.outputs))

if __name__=='__main__':unittest.main()
