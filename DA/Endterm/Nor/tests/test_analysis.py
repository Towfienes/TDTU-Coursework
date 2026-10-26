import unittest
import numpy as np
import pandas as pd
from src.analysis import COLUMNS,clean_measurements,ring_bands,holm,welch_comparison,contingency_test,metrics,regression_pipeline,FULL

class AnalysisTests(unittest.TestCase):
    def test_holm_known_example_and_order(self):
        np.testing.assert_allclose(holm([.01,.04,.03]),[.03,.06,.06])
        np.testing.assert_allclose(holm([.04,.01,.03]),[.06,.03,.06])
        with self.assertRaises(ValueError):holm([np.nan])
    def test_contingency_independence_and_sparse_fallback(self):
        r,expected=contingency_test([[10,20],[20,40]])
        self.assertAlmostEqual(r['statistic'],0);self.assertAlmostEqual(r['p'],1)
        np.testing.assert_allclose(expected,[[10,20],[20,40]])
        r,_=contingency_test([[1,0],[0,1]],n_resamples=99)
        self.assertIn('Monte Carlo',r['method']);self.assertTrue(0<r['p']<=1)
        with self.assertRaises(ValueError):contingency_test([[0,0],[1,2]])
    def test_welch_known_difference_and_symmetry(self):
        a=np.array([1,2,3,4]);b=np.array([2,3,4,5])
        r=welch_comparison(a,b);reverse=welch_comparison(b,a)
        self.assertAlmostEqual(r['difference'],-1);self.assertAlmostEqual(r['df'],6)
        self.assertAlmostEqual(r['statistic'],-1/np.sqrt(5/6))
        self.assertAlmostEqual(r['ci_low'],-reverse['ci_high'])
    def test_metric_hand_calculation_and_shapes(self):
        r=metrics([1,2,3],[1,2,4]);self.assertAlmostEqual(r['mae'],1/3)
        self.assertAlmostEqual(r['rmse'],np.sqrt(1/3));self.assertAlmostEqual(r['r2'],.5)
        with self.assertRaises(ValueError):metrics([1,2],[1])
    def test_cleaning_noncontiguous_index_and_bands(self):
        raw=pd.DataFrame([['F',.5,.4,0,.8,.3,.2,.2,8],['M',.6,.4,.1,.9,.4,.2,.2,11]],columns=COLUMNS,index=[7,19])
        clean,flags=clean_measurements(raw)
        self.assertEqual(flags,[7]);self.assertTrue(np.isnan(clean.loc[7,'height']));self.assertEqual(raw.loc[7,'height'],0)
        self.assertEqual(ring_bands(pd.Series([1,8,9,10,11,29])).astype(str).tolist(),['1–8','1–8','9–10','9–10','11+','11+'])
        with self.assertRaises(ValueError):ring_bands(pd.Series([np.inf]))
    def test_preprocessing_does_not_fit_validation(self):
        rows=[]
        for i,g in enumerate(['F','I','M']*4):rows.append([g,.1+i/100,.08+i/100,np.nan if i==0 else .1+i/100,.3+i/100,.1+i/100,.1+i/100,.1+i/100,4+i])
        df=pd.DataFrame(rows,columns=COLUMNS);p=regression_pipeline(FULL).fit(df[FULL],df.rings)
        median=p['preprocess'].named_transformers_['numeric']['impute'].statistics_.copy()
        validation=df[FULL].copy();validation.loc[:,'height']=1000
        p.predict(validation)
        np.testing.assert_array_equal(median,p['preprocess'].named_transformers_['numeric']['impute'].statistics_)
        self.assertAlmostEqual(median[2],np.nanmedian(df.height))

if __name__=='__main__':unittest.main()

class SubmissionFactsTests(unittest.TestCase):
    def test_missing_facts_and_valid_confirmed_record(self):
        from src.submission import readiness_issues
        meta={'dataset_approved':True,'youtube_url':'https://youtu.be/example','video_duration_seconds':720,'contributions_confirmed':True,'authors':[{'id':'test1','tasks':'Verified analysis','contribution_percent':100,'completion_percent':100}]}
        self.assertEqual(readiness_issues(meta),[])
        meta['authors'][0]['contribution_percent']=90
        self.assertTrue(any('sum to 100' in x for x in readiness_issues(meta)))
        meta['video_duration_seconds']=False;meta['youtube_url']='https://example.com/video'
        self.assertTrue(any('duration' in x for x in readiness_issues(meta)))
        self.assertTrue(any('YouTube' in x for x in readiness_issues(meta)))
