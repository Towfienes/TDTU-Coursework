"""Author the six-part theory notebook; calculations run only during execution."""
from pathlib import Path
import nbformat as nbf
ROOT=Path(__file__).resolve().parents[1]
cells=[]
def md(s):cells.append(nbf.v4.new_markdown_cell(s.strip()))
def code(s):cells.append(nbf.v4.new_code_cell(s.strip()))
md('''# Abalone measurements and shell rings
## Endterm — Data Analysis and Visualization, Theory N4
**VibeCoding_Expert** · NGO LAM TIEN (524H0195) · NGUYEN CONG THANH (524H0191) · NGUYEN LE NHAT TAM (524H0186) · NGO BINH MINH (524H0169)  
Advisor: Ho Thi Linh, Ph.D. · Report date20October2026.

This notebook answers one coherent question: how do scaled physical measurements and M/F/I groups relate to shell rings, and how well does multiple linear regression predict Rings? It follows all six assignment sections. Public source: [UCI Abalone](https://doi.org/10.24432/C55C7W), Nash et al. (1994), CC BY4.0. The group did not collect these biological measurements. The user has confirmed dataset selection. The video link and actual contribution/completion records remain pending.

**Design fixed before inference:** stratified80/20 split, seed42; detailed EDA/inference and model development on train; untouched test for one final comparison of prespecified models. The preliminary source check established schema and obvious measurement issues. No predictive or causal performance is promised. I means infant, not a third biological sex. Measurements are retained as stored (the source states division by200); axes explicitly identify scaled values.''')
code('''from pathlib import Path
import hashlib, json, sys, importlib.metadata
import numpy as np
import pandas as pd
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib','inline')
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.oneway import anova_oneway
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split, KFold
from sklearn.dummy import DummyRegressor
ROOT=Path.cwd().resolve()
if not (ROOT/'data/raw/abalone.data').exists():ROOT=ROOT.parent
assert (ROOT/'data/raw/abalone.data').exists()
sys.path.insert(0,str(ROOT))
from src.analysis import *
SEED=42
T=ROOT/'results/tables';F=ROOT/'results/figures'
T.mkdir(parents=True,exist_ok=True);F.mkdir(parents=True,exist_ok=True)
pd.set_option('display.max_columns',None)
sns.set_theme(style='whitegrid',font='DejaVu Sans',font_scale=1.05)
COLORS={'F':'#CC6677','I':'#228833','M':'#4477AA'}
plt.rcParams.update({'figure.dpi':100,'savefig.dpi':180,'axes.titleweight':'bold','svg.hashsalt':'tdtu-nor'})
def save_table(frame,name,index=False):frame.to_csv(T/f'{name}.csv',index=index)
def save_figure(fig,name):
    fig.tight_layout();fig.savefig(F/f'{name}.png',bbox_inches='tight',facecolor='white')
    fig.savefig(F/f'{name}.svg',bbox_inches='tight',facecolor='white',metadata={'Date':None})
    plt.show()
def dump(path,value):path.write_text(json.dumps(value,indent=2,allow_nan=False,default=lambda x:x.item() if isinstance(x,np.generic) else x.tolist())+'\\n')
''')
md('''## 1. Exploratory data analysis
### 1.1 Source and structural validation
The CSV has no header. UCI supplies8features plus Rings, the target:9columns total. The source had already removed examples with missing values, so the absence of missing cells is not proof that the original field study was complete. The current source has no site or batch identifiers, which limits independence assumptions and validation across locations.''')
code('''source=json.loads((ROOT/'references/dataset_source.json').read_text())
raw_path=ROOT/'data/raw/abalone.data'
raw_hash=hashlib.sha256(raw_path.read_bytes()).hexdigest()
assert raw_hash==source['raw_sha256']
raw=pd.read_csv(raw_path,header=None,names=COLUMNS)
raw.index.name='source_index'
assert raw.shape==(4177,9) and raw.isna().sum().sum()==0 and raw.duplicated().sum()==0
print('Original shape:',raw.shape,'SHA256:',raw_hash)
display(raw.head());display(raw.tail());raw.info()
display(raw.dtypes.astype(str).rename('dtype').to_frame())
''')
md('''### 1.2 Quality rules and saved holdout
Height=0 cannot represent a positive shell thickness: flag and replace only these two cells with NaN. Other extremes are not silently edited. The cleaning rule is domain-based and fixed before splitting. The source observations remain unchanged. Univariate descriptions omit the invalid heights, reporting their n; model median imputation is fit only within training folds.''')
code('''clean,invalid_height=clean_measurements(raw)
assert len(invalid_height)==2
train_idx,test_idx=train_test_split(clean.index.to_numpy(),test_size=.2,random_state=SEED,stratify=clean.sex)
assert len(set(train_idx)&set(test_idx))==0 and set(train_idx)|set(test_idx)==set(raw.index)
train=clean.loc[train_idx].copy();test=clean.loc[test_idx].copy()
split=pd.DataFrame({'source_index':raw.index,'split':np.where(raw.index.isin(train_idx),'train','test')})
split.to_csv(ROOT/'data/processed/split.csv',index=False)
clean.to_csv(ROOT/'data/processed/clean_measurements.csv')
audit=pd.DataFrame({'source_index':invalid_height,'column':'height','raw_value':0,'action':'set to NaN; training-only median imputation in regression'})
save_table(audit,'quality_audit')
display(audit);print('Train:',len(train),'Test:',len(test))
display(pd.crosstab(split['split'],raw.sex.to_numpy()))
''')
code('''descriptive=train[NUMERIC].describe().T
save_table(descriptive,'descriptive_train',index=True)
group_stats=train.groupby('sex',observed=True)[['length','rings']].agg(['count','mean','std','median','min','max'])
save_table(group_stats,'group_statistics',index=True)
print('All following detailed descriptions and tests use train only: n =',len(train))
display(descriptive);display(group_stats)
fig,axes=plt.subplots(2,2,figsize=(10,7))
for ax,col,color in zip(axes.flat,['length','whole_weight','height','rings'],['#4477AA','#EE7733','#228833','#AA3377']):
    sns.histplot(data=train,x=col,kde=col!='rings',discrete=col=='rings',color=color,ax=ax)
    ax.set_xlabel('Rings (count)' if col=='rings' else f'{col} (scaled, as stored)');ax.set_ylabel('Training records')
fig.suptitle('Training distributions retain skewness, tails and integer rings',y=1.02)
save_figure(fig,'01_eda_distributions')
''')
code('''fig,axes=plt.subplots(1,2,figsize=(10,4.5))
for ax,col in zip(axes,['length','rings']):
    sns.boxplot(data=train,x='sex',y=col,hue='sex',order=GROUPS,hue_order=GROUPS,palette=COLORS,legend=False,ax=ax)
    ax.set_xlabel('Recorded group (I = infant)');ax.set_ylabel('Rings (count)' if col=='rings' else 'Length (scaled, as stored)')
    for i,g in enumerate(GROUPS):ax.text(i,.98,f'n={sum(train.sex==g)}',transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=10)
save_figure(fig,'02_group_boxplots')
q1=train[NUMERIC].quantile(.25);q3=train[NUMERIC].quantile(.75);iqr=q3-q1
flags=(train[NUMERIC].lt(q1-1.5*iqr)|train[NUMERIC].gt(q3+1.5*iqr))
outlier_counts=flags.sum().rename('flagged_count').to_frame();outlier_counts['percent']=outlier_counts.flagged_count/len(train)*100
save_table(outlier_counts,'iqr_counts',True)
flagged=train.loc[flags.any(axis=1)].copy();flagged['flagged_columns']=flags.loc[flags.any(axis=1)].apply(lambda row:', '.join(row.index[row]),axis=1)
save_table(flagged,'iqr_flagged_training_rows',True)
display(outlier_counts);print('IQR flags identify unusual records, not confirmed measurement errors. No IQR-based deletion.')
''')
md('''## 2. Probability distributions
A normal distribution has density proportional to exp(−(x−μ)²/(2σ²)); a positive variable is lognormal when its logarithm is normal. These are candidate families, not assertions. We compare Length with Normal and Whole_weight with Normal and Lognormal. AD statistics emphasize tail discrepancies.

`goodness_of_fit` refits unknown μ and σ for every Monte Carlo sample. A plain KS p-value after fitting parameters to the same observations is not used. For a lognormal family with location0, the normality check is performed on log(weight). There are1999resamples per test and three Holm-adjusted distribution tests. P-values cannot be below1/2000; rounded observations and large sample size limit an exact continuous-distribution interpretation.''')
code('''distribution_rows=[]
for offset,(label,column,logged) in enumerate([('Length / Normal','length',False),('Weight / Normal','whole_weight',False),('Weight / Lognormal','whole_weight',True)]):
    values=train[column].dropna().to_numpy()
    if logged:values=np.log(values)
    result=stats.goodness_of_fit(stats.norm,values,statistic='ad',n_mc_samples=1999,rng=np.random.default_rng(SEED+offset))
    distribution_rows.append({'hypothesis':label,'n':len(values),'ad':float(result.statistic),'p':float(result.pvalue),
                              'mu':float(values.mean()),'sigma':float(values.std(ddof=1)),'seed':SEED+offset})
distribution=pd.DataFrame(distribution_rows);distribution['p_holm']=holm(distribution.p)
distribution['reject_05']=distribution.p_holm<.05
save_table(distribution,'distribution_tests');display(distribution)
''')
code('''fig,axes=plt.subplots(1,2,figsize=(10,4.2))
x=train.length.to_numpy();grid=np.linspace(x.min(),x.max(),150);mu=x.mean();sd=x.std(ddof=1)
sns.histplot(x=x,stat='density',bins=30,color='#4477AA',alpha=.5,ax=axes[0],label='Observed')
axes[0].plot(grid,stats.norm.pdf(grid,mu,sd),color='#CC3311',label='Fitted Normal');axes[0].legend()
axes[0].set(xlabel='Length (scaled, as stored)',ylabel='Density')
stats.probplot(x,dist='norm',plot=axes[1]);axes[1].get_lines()[0].set(color='#4477AA',marker='.',markersize=3);axes[1].get_lines()[1].set_color('#CC3311')
axes[1].set_title('Length: Normal Q–Q plot')
save_figure(fig,'03_length_distribution')
''')
code('''fig,axes=plt.subplots(2,2,figsize=(10,7))
w=train.whole_weight.to_numpy();grid_w=np.linspace(w.min(),w.max(),150)
mu_w=w.mean();sd_w=w.std(ddof=1);logmu=np.log(w).mean();logsd=np.log(w).std(ddof=1)
sns.histplot(x=w,stat='density',bins=35,color='#EE7733',alpha=.45,ax=axes[0,0],label='Observed')
axes[0,0].plot(grid_w,stats.norm.pdf(grid_w,mu_w,sd_w),color='#4477AA',label='Normal')
axes[0,0].plot(grid_w,stats.lognorm.pdf(grid_w,logsd,scale=np.exp(logmu)),color='#228833',label='Lognormal')
axes[0,0].legend();axes[0,0].set(xlabel='Whole weight (scaled, as stored)',ylabel='Density')
sns.histplot(x=np.log(w),stat='density',kde=True,color='#228833',ax=axes[0,1]);axes[0,1].set_xlabel('log(whole_weight)')
for ax,values,title in [(axes[1,0],w,'Weight / Normal'),(axes[1,1],np.log(w),'log Weight / Normal')]:
    stats.probplot(values,dist='norm',plot=ax);ax.get_lines()[0].set(color='#4477AA',marker='.',markersize=3);ax.get_lines()[1].set_color('#CC3311');ax.set_title(title)
save_figure(fig,'04_weight_distribution')
''')
md('''## 3. Hypothesis testing
**Welch t-test:** H0: mean Rings(M)=mean Rings(F), two-sided. It compares independent means allowing unequal variances, with Satterthwaite degrees of freedom. Report the mean difference M−F and its95%CI.

**Chi-square independence:** H0: recorded group and ring band are independent. Bands1–8/9–10/11+ follow a historical coding described in the retained codebook; they are not validated biological age classes. Use Pearson χ² with df=(r−1)(c−1), check expected counts; sparse tables use fixed-margin Monte Carlo.

**One-way ANOVA:** classical ANOVA compares between-group and within-group variability under common variance. Welch ANOVA instead weights unequal group variances and adjusts degrees of freedom. Primary H0: mean Length(F)=mean Length(I)=mean Length(M). Independence remains an assumption, because site/batch IDs are absent. Welch methods tolerate unequal variances but do not remove confounding, selection bias or clustered sampling.

Alpha=.05; Holm correction applies to the three primary tests as one family. Follow-up pairwise Length comparisons form a separate Holm family only if the omnibus adjusted result rejects. Failure to reject is not proof of equality, and statistical significance does not measure practical importance.''')
code('''welch=welch_comparison(train.loc[train.sex=='M','rings'],train.loc[train.sex=='F','rings'])
contingency=pd.crosstab(train.sex,ring_bands(train.rings)).reindex(GROUPS)
chi,expected=contingency_test(contingency)
length_groups=[train.loc[train.sex==g,'length'].to_numpy() for g in GROUPS]
anova=anova_oneway(length_groups,use_var='unequal',welch_correction=True)
classic=stats.f_oneway(*length_groups)
levene=stats.levene(*length_groups,center='median')
overall_mean=train.length.mean()
ss_between=sum(len(a)*(a.mean()-overall_mean)**2 for a in length_groups)
eta_sq=float(ss_between/np.sum((train.length-overall_mean)**2))
hypotheses=pd.DataFrame([
 {'test':'Welch t: Rings M−F','statistic':welch['statistic'],'df1':welch['df'],'df2':np.nan,'p':welch['p']},
 {'test':'Chi-square: group × ring band','statistic':chi['statistic'],'df1':chi['df'],'df2':np.nan,'p':chi['p']},
 {'test':'Welch ANOVA: Length groups','statistic':float(anova.statistic),'df1':float(anova.df_num),'df2':float(anova.df_denom),'p':float(anova.pvalue)}])
hypotheses['p_holm']=holm(hypotheses.p);hypotheses['reject_05']=hypotheses.p_holm<.05
save_table(hypotheses,'hypothesis_tests');save_table(contingency,'contingency_observed',True)
save_table(pd.DataFrame(expected,index=GROUPS,columns=contingency.columns),'contingency_expected',True)
display(hypotheses);print('Welch difference and CI:',welch);print('Chi-square diagnostics:',chi)
print('Classical ANOVA reference:',classic,'Median-based Levene:',levene,'Descriptive eta-squared:',eta_sq)
''')
code('''posthoc=[]
if hypotheses.loc[2,'reject_05']:
    for a,b in [('F','I'),('F','M'),('I','M')]:posthoc.append({'comparison':a+'−'+b,**welch_comparison(train.loc[train.sex==a,'length'],train.loc[train.sex==b,'length'])})
    pairwise=pd.DataFrame(posthoc);pairwise['p_holm']=holm(pairwise.p);save_table(pairwise,'anova_posthoc');display(pairwise)
print('Pairwise CIs are unadjusted95% descriptive intervals; only p-values have Holm familywise adjustment.')
fig,axes=plt.subplots(1,2,figsize=(10,4.6))
percent=contingency.div(contingency.sum(axis=1),axis=0)*100
percent.plot.bar(stacked=True,color=['#4477AA','#EE7733','#228833'],ax=axes[0],rot=0)
axes[0].set(xlabel='Recorded group (I = infant)',ylabel='Percent within group',ylim=(0,100));axes[0].legend(title='Rings',fontsize=9)
length_summary=train.groupby('sex').length.agg(['count','mean','std']).reindex(GROUPS)
length_summary['ci95']=stats.t.ppf(.975,length_summary['count']-1)*length_summary['std']/np.sqrt(length_summary['count'])
axes[1].bar(GROUPS,length_summary['mean'],yerr=length_summary.ci95,color=[COLORS[g] for g in GROUPS],capsize=5)
axes[1].set(xlabel='Recorded group (I = infant)',ylabel='Mean length (scaled, as stored)',ylim=(0,.7))
axes[1].set_title('Means with unadjusted95%CI')
save_figure(fig,'05_hypothesis_groups')
''')
md('''## 4. Pearson and Spearman correlation
Pearson r measures linear association using centered products. Spearman ρ applies Pearson correlation to ranks, using average ranks for ties. Their values are not causal effects and cannot by themselves measure independent predictor importance. Group is nominal and is not assigned an arbitrary numeric order. Pairwise n is exported because invalid heights are omitted from relevant pairs. Matrices exclude source indexes and outcome-derived variables.''')
code('''pearson=train[NUMERIC].corr(method='pearson');spearman=train[NUMERIC].corr(method='spearman')
pair_n=train[NUMERIC].notna().astype(int).T.dot(train[NUMERIC].notna().astype(int))
save_table(pearson,'pearson_matrix',True);save_table(spearman,'spearman_matrix',True);save_table(pair_n,'correlation_n',True)
correlations=pd.DataFrame({'pearson':pearson['rings'].drop('rings'),'spearman':spearman['rings'].drop('rings'),'n':pair_n['rings'].drop('rings')})
correlations['abs_spearman']=correlations.spearman.abs();correlations=correlations.sort_values('abs_spearman',ascending=False)
save_table(correlations,'rings_correlations',True);display(correlations)
labels=['Length','Diameter','Height','Whole wt','Shucked wt','Viscera wt','Shell wt','Rings']
for matrix,title,name in [(pearson,'Pearson r','06a_pearson_heatmap'),(spearman,'Spearman ρ','06b_spearman_heatmap')]:
    fig,ax=plt.subplots(figsize=(7.5,6))
    sns.heatmap(matrix,annot=True,fmt='.2f',cmap='vlag',vmin=-1,vmax=1,center=0,ax=ax,cbar=True,annot_kws={'fontsize':12},xticklabels=labels,yticklabels=labels,cbar_kws={'shrink':.8})
    ax.set_xticklabels(labels,rotation=45,ha='right',fontsize=12);ax.set_yticklabels(labels,rotation=0,fontsize=12);ax.set_title(title)
    save_figure(fig,name)
''')
code('''fig,axes=plt.subplots(1,3,figsize=(12,4))
for ax,a,b in [(axes[0],'shell_weight','rings'),(axes[1],'length','rings'),(axes[2],'length','diameter')]:
    sns.regplot(data=train,x=a,y=b,ci=None,scatter_kws={'alpha':.2,'s':8,'color':'#4477AA'},line_kws={'color':'#CC3311'},ax=ax)
    ax.set_xlabel(a+' (scaled)');ax.set_ylabel('Rings (count)' if b=='rings' else b+' (scaled)')
save_figure(fig,'07_relationships')
''')
md('''## 5. Multiple linear regression
OLS fits Rings=β0+ΣβjXj+ε by minimizing squared residuals. Multiple predictors allow conditional associations, but coefficients do not identify causal effects. A dummy for I and one for M use F as reference. Numeric coefficients below correspond to one training SD after median imputation; original-scale coefficients are exported separately.

Three prespecified methods: training-mean baseline; compact measurements (group, length, diameter, height, whole weight); full8original inputs. Component weights may require dissection: do not describe the full model as wholly nondestructive. An80/20holdout estimates performance on similarly sampled records, not new locations or cohorts. FivefoldCV on train estimates development variability. Every fold fits its own median and scaling; the test is not used to select or tune models.''')
code('''folds=list(KFold(n_splits=5,shuffle=True,random_state=SEED).split(train))
models={'Baseline':None,'Compact':COMPACT,'Full':FULL}
cv_rows=[]
for name,features in models.items():
    for fold,(inner,valid) in enumerate(folds,1):
        a,b=train.iloc[inner],train.iloc[valid]
        if features is None:
            fitted=DummyRegressor(strategy='mean').fit(a[['length']],a.rings);prediction=fitted.predict(b[['length']])
        else:
            fitted=regression_pipeline(features).fit(a[features],a.rings);prediction=fitted.predict(b[features])
        cv_rows.append({'model':name,'fold':fold,**metrics(b.rings,prediction),'fit_n':len(a),'validation_n':len(b)})
cv=pd.DataFrame(cv_rows);save_table(cv,'cv_fold_metrics')
cv_summary=cv.groupby('model')[['mae','rmse','r2']].agg(['mean','std'])
save_table(cv_summary,'cv_summary',True);display(cv_summary)
''')
code('''# One final holdout evaluation of all prespecified methods; no tuning follows.
fitted_models={};test_rows=[]
predictions=test[['sex','rings']].copy()
for name,features in models.items():
    model=DummyRegressor(strategy='mean').fit(train[['length']],train.rings) if features is None else regression_pipeline(features).fit(train[features],train.rings)
    prediction=model.predict(test[['length']] if features is None else test[features])
    fitted_models[name]=model;predictions[name]=prediction
    test_rows.append({'model':name,**metrics(test.rings,prediction),'outside_1_29':int(((prediction<1)|(prediction>29)).sum())})
test_metrics=pd.DataFrame(test_rows);save_table(test_metrics,'test_metrics');save_table(predictions,'test_predictions',True)
display(test_metrics)
full=fitted_models['Full'];Z=full['preprocess'].transform(train[FULL]);design=sm.add_constant(Z,has_constant='add')
assert np.linalg.matrix_rank(design)==design.shape[1]
ols=sm.OLS(train.rings.to_numpy(),design).fit();robust=ols.get_robustcov_results(cov_type='HC3')
np.testing.assert_allclose(ols.predict(design),full.predict(train[FULL]),atol=1e-10,rtol=0)
feature_names=['Intercept',*full['preprocess'].get_feature_names_out()]
interval=robust.conf_int()
coefficients=pd.DataFrame({'term':feature_names,'coefficient':robust.params,'HC3_SE':robust.bse,'ci_low':interval[:,0],'ci_high':interval[:,1]})
save_table(coefficients,'full_coefficients_HC3');display(coefficients)
# Convert numeric slopes and intercept back to stored-measurement units.
original=full['regression'].coef_.copy();scaler=full['preprocess'].named_transformers_['numeric']['scale'];original[:7]/=scaler.scale_
original_intercept=full['regression'].intercept_-np.dot(original[:7],scaler.mean_)
original_coefficients=pd.DataFrame({'term':feature_names,'coefficient':[original_intercept,*original]})
save_table(original_coefficients,'full_coefficients_stored_scale')
np.testing.assert_allclose(np.column_stack([np.ones(len(train)),full['preprocess'].named_transformers_['numeric']['impute'].transform(train[NUMERIC[:-1]]),Z[:,7:]])@original_coefficients.coefficient,full.predict(train[FULL]),atol=1e-10,rtol=0)
''')
code('''vif=pd.DataFrame({'term':feature_names[1:],'VIF':[variance_inflation_factor(design,i) for i in range(1,design.shape[1])]})
save_table(vif,'vif');display(vif)
bp=het_breuschpagan(ols.resid,design)
cooks=ols.get_influence().cooks_distance[0]
influence=pd.DataFrame({'source_index':train.index,'observed':train.rings,'fitted':ols.fittedvalues,'residual':ols.resid,'cooks_distance':cooks})
save_table(influence,'training_diagnostics')
print('Design rank:',np.linalg.matrix_rank(design),'of',design.shape[1]);print('Breusch–Pagan LM / p:',bp[:2]);print('Cook flags:',int((cooks>4/len(train)).sum()))
fig,axes=plt.subplots(2,2,figsize=(10,7))
axes[0,0].scatter(ols.fittedvalues,ols.resid,s=8,alpha=.25,color='#4477AA');axes[0,0].axhline(0,color='#CC3311');axes[0,0].set(xlabel='Training fitted rings',ylabel='Residual')
stats.probplot(ols.resid,dist='norm',plot=axes[0,1]);axes[0,1].get_lines()[0].set(color='#4477AA',marker='.',markersize=3);axes[0,1].get_lines()[1].set_color('#CC3311');axes[0,1].set_title('Training residual Q–Q')
axes[1,0].scatter(np.arange(len(train)),cooks,s=7,color='#228833',alpha=.5);axes[1,0].axhline(4/len(train),color='#CC3311',label='4/n');axes[1,0].set(xlabel='Training position',ylabel="Cook's distance");axes[1,0].legend()
sns.histplot(ols.resid,kde=True,color='#EE7733',ax=axes[1,1]);axes[1,1].set_xlabel('Training residual (rings)')
save_figure(fig,'08_regression_diagnostics')
fig,axes=plt.subplots(1,2,figsize=(10,4.4))
axes[0].scatter(test.rings,predictions.Full,s=10,alpha=.35,color='#4477AA');axes[0].plot([1,29],[1,29],color='#CC3311');axes[0].set(xlabel='Observed test rings',ylabel='Full-model prediction',xlim=(0,30))
test_metrics.plot.bar(x='model',y=['mae','rmse'],color=['#4477AA','#EE7733'],ax=axes[1],rot=0);axes[1].set(xlabel='',ylabel='Test error (rings)')
save_figure(fig,'09_holdout_evaluation')
''')
md('''### 5.6 Influence sensitivity — training only
A Cook flag is not proof of an error. The primary full model retains every training record. As a sensitivity check only, fit a provisional full model within each inner-training fold, compute its Cook distances, remove observations above4/n inside that same training fold, refit preprocessing and OLS, then evaluate the unchanged validation fold. This prevents validation information from influencing deletion. Coefficient changes on the full training set are reported separately; no sensitivity method is tuned or evaluated on the holdout.''')
code('''sensitivity_rows=[]
for fold,(inner,valid) in enumerate(folds,1):
    a,b=train.iloc[inner],train.iloc[valid]
    sensitive,keep,_=cook_filter_fit(a[FULL],a.rings,FULL)
    sensitivity_rows.append({'fold':fold,'training_before':len(a),'training_after':int(keep.sum()),'removed':int((~keep).sum()),'validation_n':len(b),**metrics(b.rings,sensitive.predict(b[FULL]))})
sensitivity=pd.DataFrame(sensitivity_rows);save_table(sensitivity,'influence_sensitivity_cv');display(sensitivity)
sensitive,keep,_=cook_filter_fit(train[FULL],train.rings,FULL)
coef_change=pd.DataFrame({'term':feature_names,'primary_scaled':[full['regression'].intercept_,*full['regression'].coef_],'filtered_scaled':[sensitive['regression'].intercept_,*sensitive['regression'].coef_]})
# Different scalers after filtering: compare slopes in the original stored units instead.
filtered_coef=sensitive['regression'].coef_.copy();filtered_scaler=sensitive['preprocess'].named_transformers_['numeric']['scale'];filtered_coef[:7]/=filtered_scaler.scale_
filtered_intercept=sensitive['regression'].intercept_-np.dot(filtered_coef[:7],filtered_scaler.mean_)
coef_change['primary_stored']=original_coefficients.coefficient;coef_change['filtered_stored']=[filtered_intercept,*filtered_coef]
save_table(coef_change,'influence_coefficient_sensitivity');display(coef_change[['term','primary_stored','filtered_stored']])
''')
md('''## 6. Synthesis and reproducible exports
Read the outputs together: distribution rejection need not invalidate large-sample mean comparisons, but dependence and sampling bias remain. Association is not causation. Strong collinearity can destabilize conditional coefficients even when predictions improve. Evaluate improvement relative to baseline in ring units, with CV variability and holdout performance. Source Rings+1.5 is an approximate age relation, not additional independent information or a predictor.

The report and slides consume this execution's exported summary, tables and figures. Their builders do not recompute statistical analyses. Personal contribution percentages and video publication are separate external facts and are not generated from code.''')
code('''# Portable chart snapshots are exported from this same execution.
length_hist,edges=np.histogram(train.length,bins=25,density=True)
weight_hist,w_edges=np.histogram(train.whole_weight,bins=25,density=True)
qq_probs=np.linspace(.005,.995,100)
chart_data={'length_density':{'hist_x':((edges[1:]+edges[:-1])/2).tolist(),'hist_y':length_hist.tolist(),'x':grid.tolist(),'normal':stats.norm.pdf(grid,mu,sd).tolist()},
 'weight_density':{'x':grid_w.tolist(),'normal':stats.norm.pdf(grid_w,mu_w,sd_w).tolist(),'lognormal':stats.lognorm.pdf(grid_w,logsd,scale=np.exp(logmu)).tolist(),'hist_x':((w_edges[1:]+w_edges[:-1])/2).tolist(),'hist_y':weight_hist.tolist()},
 'qq_length':{'x':stats.norm.ppf(qq_probs).tolist(),'y':np.quantile(train.length,qq_probs).tolist()},
 'shell_scatter':{'x':train.shell_weight.tolist(),'y':train.rings.tolist()},
 'holdout':{'x':test.rings.tolist(),'y':predictions.Full.tolist()},
 'residuals':{'x':ols.fittedvalues.tolist(),'y':ols.resid.tolist()},
 'length_group':length_summary.reset_index().to_dict('records'),'contingency_percent':percent.to_dict('index')}
summary={'raw_shape':list(raw.shape),'raw_sha256':raw_hash,'original_missing':int(raw.isna().sum().sum()),'duplicates':int(raw.duplicated().sum()),
 'invalid_height_indices':invalid_height,'train_n':len(train),'test_n':len(test),'train_group_counts':train.sex.value_counts().to_dict(),'raw_group_counts':raw.sex.value_counts().to_dict(),
 'descriptive':descriptive.to_dict('index'),'iqr_counts':outlier_counts.to_dict('index'),'distribution':distribution.to_dict('records'),
 'hypotheses':hypotheses.drop(columns='df2').to_dict('records'),'welch':welch,'chi':chi,'anova':{'F':float(anova.statistic),'df_num':float(anova.df_num),'df_den':float(anova.df_denom),'p':float(anova.pvalue),'classic_F':float(classic.statistic),'classic_p':float(classic.pvalue),'levene_stat':float(levene.statistic),'levene_p':float(levene.pvalue),'eta_squared_descriptive':eta_sq},
 'posthoc':pairwise.to_dict('records') if posthoc else [],'contingency':contingency.to_dict('index'),'correlations':correlations.to_dict('index'),
 'pearson':pearson.to_dict('index'),'spearman':spearman.to_dict('index'),'test_metrics':test_metrics.to_dict('records'),
 'cv':cv.to_dict('records'),'coefficients':coefficients.to_dict('records'),'coefficients_stored':original_coefficients.to_dict('records'),'vif':vif.to_dict('records'),
 'diagnostics':{'rank':int(np.linalg.matrix_rank(design)),'design_columns':int(design.shape[1]),'bp_lm':float(bp[0]),'bp_p':float(bp[1]),'cook_flagged':int((cooks>4/len(train)).sum())},
 'sensitivity':sensitivity.to_dict('records'),'sensitivity_removed_total_train':int((~keep).sum()),'coefficient_sensitivity':coef_change[['term','primary_stored','filtered_stored']].to_dict('records'),'chart_data':chart_data}
dump(ROOT/'results/summary.json',summary)
versions={name:importlib.metadata.version(name) for name in ['numpy','pandas','scipy','seaborn','matplotlib','scikit-learn','statsmodels','nbformat','nbclient','ipykernel']}
artifacts=sorted([*T.glob('*.csv'),*F.glob('*.png'),*F.glob('*.svg'),*(ROOT/'data/processed').glob('*.csv'),ROOT/'results/summary.json'])
dump(ROOT/'results/manifest.json',{'raw_sha256':raw_hash,'split_seed':42,'versions':versions,'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts}})
print('Completed all six theory sections. Summary and all artifacts exported; no test-driven tuning was performed.')
''')
nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3 (DAV Theory)','language':'python','name':'python3'}})
nbf.write(nb,ROOT/'notebooks/VibeCoding_Expert_DAV_Theory_Endterm_Analysis.ipynb')
print('Authored',len(cells),'cells;',sum(c.cell_type=='code' for c in cells),'code cells.')
