"""Small shared statistical operations; every analysis uses the saved train split."""
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm

COLUMNS = ['sex','length','diameter','height','whole_weight','shucked_weight','viscera_weight','shell_weight','rings']
NUMERIC = COLUMNS[1:]
FULL = COLUMNS[:-1]
COMPACT = ['sex','length','diameter','height','whole_weight']
GROUPS = ['F','I','M']


def clean_measurements(raw):
    if raw.columns.tolist() != COLUMNS or not raw['sex'].isin(GROUPS).all():
        raise ValueError('Unexpected schema or group code.')
    numeric=raw[NUMERIC].to_numpy(dtype=float)
    if not np.isfinite(numeric).all() or (raw['rings'] < 1).any() or (raw['rings'] % 1 != 0).any():
        raise ValueError('Invalid finite numerical values or rings.')
    if (raw[NUMERIC[:-1]] < 0).any().any():
        raise ValueError('Negative physical measurements require source review.')
    result=raw.copy()
    flagged=result['height'].eq(0)
    result.loc[flagged,'height']=np.nan
    return result, result.index[flagged].tolist()


def ring_bands(rings):
    if rings.isna().any() or not ((rings>=1)&(rings%1==0)).all():
        raise ValueError('Rings must be positive finite integers.')
    return pd.cut(rings,bins=[0,8,10,np.inf],labels=['1–8','9–10','11+'])


def holm(pvalues):
    p=np.asarray(pvalues,dtype=float)
    if p.ndim!=1 or len(p)==0 or not np.isfinite(p).all() or ((p<0)|(p>1)).any():
        raise ValueError('Expected a nonempty vector of valid p-values.')
    return multipletests(p,method='holm')[1]


def welch_comparison(a,b):
    a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
    if min(len(a),len(b))<2 or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError('Each finite group needs at least two observations.')
    test=stats.ttest_ind(a,b,equal_var=False)
    ci=test.confidence_interval(.95)
    return {'difference':float(a.mean()-b.mean()),'ci_low':float(ci.low),'ci_high':float(ci.high),
            'statistic':float(test.statistic),'df':float(test.df),'p':float(test.pvalue),'n_a':len(a),'n_b':len(b)}


def contingency_test(table,seed=42,n_resamples=9999):
    observed=np.asarray(table,dtype=float)
    if observed.ndim!=2 or min(observed.shape)<2 or (observed<0).any() or (observed%1!=0).any():
        raise ValueError('Expected a nonnegative integer contingency table.')
    if (observed.sum(axis=0)==0).any() or (observed.sum(axis=1)==0).any():
        raise ValueError('Empty margins must be removed and documented.')
    chi,p,df,expected=stats.chi2_contingency(observed,correction=False)
    method='Pearson chi-square approximation'
    if (expected<5).any():
        simulated=stats.random_table.rvs(observed.sum(axis=1).astype(int),observed.sum(axis=0).astype(int),size=n_resamples,random_state=np.random.default_rng(seed))
        scores=((simulated-expected)**2/expected).sum(axis=(1,2))
        p=(1+np.count_nonzero(scores>=chi-1e-12))/(n_resamples+1)
        method=f'Fixed-margin Monte Carlo ({n_resamples} resamples)'
    v=np.sqrt(chi/(observed.sum()*min(observed.shape[0]-1,observed.shape[1]-1)))
    return {'statistic':float(chi),'p':float(p),'df':int(df),'min_expected':float(expected.min()),'cramers_v':float(v),'method':method},expected


def regression_pipeline(features):
    numeric=[column for column in features if column!='sex']
    preprocess=ColumnTransformer([
        ('numeric',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),numeric),
        ('group',OneHotEncoder(categories=[GROUPS],drop='first',handle_unknown='error',sparse_output=False),['sex'])],verbose_feature_names_out=False)
    return Pipeline([('preprocess',preprocess),('regression',LinearRegression())])


def metrics(y,prediction):
    y,prediction=np.asarray(y,dtype=float),np.asarray(prediction,dtype=float)
    if y.shape!=prediction.shape or y.ndim!=1 or len(y)<2 or not np.isfinite(y).all() or not np.isfinite(prediction).all():
        raise ValueError('Expected aligned finite response and prediction vectors.')
    return {'mae':float(mean_absolute_error(y,prediction)), 'rmse':float(np.sqrt(mean_squared_error(y,prediction))), 'r2':float(r2_score(y,prediction))}


def cook_filter_fit(X,y,features):
    """Fit the influence screen only on the supplied training observations."""
    initial=regression_pipeline(features).fit(X,y)
    design=sm.add_constant(initial['preprocess'].transform(X),has_constant='add')
    fit=sm.OLS(np.asarray(y),design).fit()
    cooks=fit.get_influence().cooks_distance[0]
    keep=cooks<=4/len(X)
    if keep.sum()<=design.shape[1]:raise ValueError('Influence filtering left too few training rows.')
    final=regression_pipeline(features).fit(X.iloc[keep],y.iloc[keep])
    return final,keep,cooks
