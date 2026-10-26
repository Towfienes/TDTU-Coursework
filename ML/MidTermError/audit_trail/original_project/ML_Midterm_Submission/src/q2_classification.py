"""Q2: Leakage-safe multi-class benchmark for Iris, OpenML dataset ID 61.

The bundled CSV is an offline mirror of Fisher's Iris data from scikit-learn.
OpenML live re-fetch is optional; do not confuse offline mirror with a
successful network download. This program measures actual held-out results.
"""
from pathlib import Path
import json, warnings, argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris,fetch_openml
from sklearn.model_selection import train_test_split,StratifiedKFold,cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score,precision_score,recall_score,f1_score,
 classification_report, confusion_matrix,ConfusionMatrixDisplay)
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC,LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier,ExtraTreesClassifier,
 GradientBoostingClassifier,AdaBoostClassifier)
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis,QuadraticDiscriminantAnalysis

FEATURES=['sepallength','sepalwidth','petallength','petalwidth']
LABELS=['setosa','versicolor','virginica']
SEED=42

def create_offline_openml_mirror(root):
    """Bundle the corresponding original Fisher Iris observations locally."""
    path=root/'data/iris_openml_61_offline_mirror.csv'
    if not path.exists():
        raw=load_iris(as_frame=True)
        df=pd.DataFrame(raw.data.to_numpy(),columns=FEATURES)
        df['class']=[LABELS[i] for i in raw.target]
        df.to_csv(path,index=False,float_format='%.1f')
    return path

def get_data(root,use_openml_live=False):
    local=create_offline_openml_mirror(root)
    if use_openml_live:
        try:
            bunch=fetch_openml(data_id=61,as_frame=True,parser='auto')
            df=bunch.frame.copy()
            keys=list(df.columns)
            rename={keys[i]:FEATURES[i] for i in range(4)}
            rename[keys[4]]='class'
            df=df.rename(columns=rename)
            df['class']=df['class'].astype(str).str.lower().str.replace('iris-','',regex=False)
            df=df[FEATURES+['class']]
            if len(df)!=150 or set(df['class'])!=set(LABELS):
                raise ValueError('unexpected OpenML dataset schema')
            return df,'Live OpenML data ID 61, version 1'
        except Exception as exc:
            raise RuntimeError('Requested live OpenML fetch failed; rerun without --use-openml-live to use explicit offline mirror.') from exc
    return pd.read_csv(local),'Bundled offline mirror (scikit-learn Fisher Iris); OpenML dataset 61'

def make_pipeline(model):
    prep=ColumnTransformer([
     ('numeric',Pipeline([('impute',SimpleImputer(strategy='median')),
                 ('scale',StandardScaler())]),FEATURES)],remainder='drop')
    return Pipeline([('preprocess',prep),('model',model)])

def models():
    return {
     'Dummy (majority)':DummyClassifier(strategy='most_frequent'),
     'Logistic Regression':LogisticRegression(max_iter=2000,random_state=SEED),
     'KNN (k=5)':KNeighborsClassifier(n_neighbors=5),
     'SVM (RBF)':SVC(kernel='rbf',C=1.,gamma='scale',random_state=SEED),
     'Linear SVM':LinearSVC(max_iter=20000,random_state=SEED),
     'Decision Tree':DecisionTreeClassifier(random_state=SEED),
     'Random Forest':RandomForestClassifier(n_estimators=150,random_state=SEED,n_jobs=1),
     'Extra Trees':ExtraTreesClassifier(n_estimators=150,random_state=SEED,n_jobs=1),
     'Gradient Boosting':GradientBoostingClassifier(random_state=SEED),
     'AdaBoost':AdaBoostClassifier(random_state=SEED),
     'Gaussian Naive Bayes':GaussianNB(),
     'LDA':LinearDiscriminantAnalysis(),
     'QDA':QuadraticDiscriminantAnalysis(),
    }

def main(root=None,use_openml_live=False):
    root=Path(root or Path(__file__).resolve().parents[1]);(root/'figures').mkdir(exist_ok=True)
    (root/'results').mkdir(exist_ok=True);(root/'data').mkdir(exist_ok=True)
    data,origin=get_data(root,use_openml_live)
    original_rows=len(data); missing_before=int(data.isna().sum().sum()); duplicate_count=int(data.duplicated().sum())
    # Remove literal invalid numeric cells, and duplicate rows. Imputation FITS on train only.
    data=data.replace([np.inf,-np.inf],np.nan).drop_duplicates().copy()
    for col in FEATURES:data[col]=pd.to_numeric(data[col],errors='coerce')
    data['class']=data['class'].astype(str).str.strip().str.lower()
    data=data[data['class'].isin(LABELS)].dropna(subset=['class'])
    assert data[FEATURES].shape[1]==4 and data['class'].nunique()==3
    numeric_missing_after=int(data[FEATURES].isna().sum().sum())
    X,y=data[FEATURES],data['class']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.30,stratify=y,random_state=SEED)
    cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=SEED)
    # EDA (descriptive only). Model and imputation/scaling FIT training folds only.
    fig,ax=plt.subplots(figsize=(7,4.4));counts=y.value_counts().reindex(LABELS)
    bars=ax.bar(counts.index,counts.values,color=['#0891B2','#7C3AED','#F59E0B'])
    ax.bar_label(bars,padding=3);ax.set_ylim(0,max(counts)*1.17)
    ax.set_title('Q2 - Iris Class Distribution');ax.set_ylabel('Observations');fig.tight_layout()
    fig.savefig(root/'figures/q2_class_balance.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.4,5.1))
    for i,label in enumerate(LABELS):
        sub=data[data['class']==label]
        ax.scatter(sub['petallength'],sub['petalwidth'],s=34,alpha=.8,label=label,
                   color=['#0891B2','#7C3AED','#F59E0B'][i])
    ax.set_xlabel('Petal length (cm)');ax.set_ylabel('Petal width (cm)');ax.legend(frameon=False)
    ax.set_title('Q2 - Petal Dimensions by Species');fig.tight_layout()
    fig.savefig(root/'figures/q2_feature_scatter.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(6.8,5.2))
    sns.heatmap(data[FEATURES].corr(),annot=True,fmt='.2f',cmap='RdBu_r',vmin=-1,vmax=1,ax=ax)
    ax.set_title('Q2 - Correlation between Raw Numeric Features');fig.tight_layout()
    fig.savefig(root/'figures/q2_correlation.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.7))
    sns.boxplot(data=data.melt(id_vars='class',value_vars=FEATURES),x='variable',y='value',ax=ax,color='#B6DDEA')
    ax.tick_params(axis='x',labelrotation=12);ax.set_xlabel('Feature');ax.set_ylabel('Value (cm)')
    ax.set_title('Q2 - Feature Distributions');fig.tight_layout()
    fig.savefig(root/'figures/q2_feature_distributions.png',dpi=170);plt.close(fig)
    rows=[]; predictions={}; all_models=models()
    for name,model in all_models.items():
        pipe=make_pipeline(model)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',category=UserWarning)
            scores=cross_val_score(pipe,X_train,y_train,scoring='f1_macro',cv=cv,n_jobs=1)
            pipe.fit(X_train,y_train)
        train_pred=pipe.predict(X_train);test_pred=pipe.predict(X_test)
        rows.append(dict(model=name,cv_macro_f1_mean=float(scores.mean()),cv_macro_f1_std=float(scores.std()),
          train_accuracy=float(accuracy_score(y_train,train_pred)),
          test_accuracy=float(accuracy_score(y_test,test_pred)),
          test_precision_macro=float(precision_score(y_test,test_pred,average='macro',zero_division=0)),
          test_recall_macro=float(recall_score(y_test,test_pred,average='macro',zero_division=0)),
          test_f1_macro=float(f1_score(y_test,test_pred,average='macro',zero_division=0)),
          train_test_accuracy_gap=float(accuracy_score(y_train,train_pred)-accuracy_score(y_test,test_pred))))
        predictions[name]=pipe
    comparison=pd.DataFrame(rows).sort_values(by=['cv_macro_f1_mean','model'],ascending=[False,True]).reset_index(drop=True)
    comparison.to_csv(root/'results/q2_model_comparison.csv',index=False,float_format='%.6f')
    # Select using 5-fold train-only CV, not observed test performance.
    champion_name=comparison.iloc[0]['model'];champion=predictions[champion_name]
    champion_pred=champion.predict(X_test)
    cm=confusion_matrix(y_test,champion_pred,labels=LABELS)
    fig,ax=plt.subplots(figsize=(6.6,5.1));ConfusionMatrixDisplay(cm,display_labels=LABELS).plot(ax=ax,cmap='Blues',colorbar=False)
    ax.set_title('Q2 - CV-Selected Model: '+champion_name);fig.tight_layout()
    fig.savefig(root/'figures/q2_champion_confusion.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5.9));view=comparison.sort_values('cv_macro_f1_mean')
    ax.barh(view['model'],view['cv_macro_f1_mean'],color='#0E7490',alpha=.88)
    ax.errorbar(view['cv_macro_f1_mean'],np.arange(len(view)),xerr=view['cv_macro_f1_std'],fmt='none',ecolor='#27334C',capsize=3)
    ax.set_xlim(0,1.06);ax.set_xlabel('5-fold CV macro-F1 (training split only)')
    ax.set_title('Q2 - Classifier Comparison (mean +/- 1 fold SD)');fig.tight_layout()
    fig.savefig(root/'figures/q2_model_comparison.png',dpi=170);plt.close(fig)
    # Train-only complexity experiment for a single decision tree.
    complexity=[]
    for depth in [1,2,3,4,5,7,None]:
        pipe=make_pipeline(DecisionTreeClassifier(max_depth=depth,random_state=SEED))
        cv_scores=cross_val_score(pipe,X_train,y_train,cv=cv,scoring='f1_macro',n_jobs=1)
        pipe.fit(X_train,y_train)
        complexity.append({'max_depth':'None' if depth is None else str(depth),
           'train_macro_f1':float(f1_score(y_train,pipe.predict(X_train),average='macro')),
           'cv_macro_f1':float(cv_scores.mean()),'cv_std':float(cv_scores.std())})
    depth_df=pd.DataFrame(complexity)
    depth_df.to_csv(root/'results/q2_tree_depth_study.csv',index=False,float_format='%.6f')
    fig,ax=plt.subplots(figsize=(8.6,4.8))
    xs=np.arange(len(depth_df))
    ax.plot(xs,depth_df.train_macro_f1,'o-',lw=2,color='#DC2626',label='Training macro-F1')
    ax.plot(xs,depth_df.cv_macro_f1,'s-',lw=2,color='#0E7490',label='5-fold CV macro-F1')
    ax.fill_between(xs,(depth_df.cv_macro_f1-depth_df.cv_std).to_numpy(),
        (depth_df.cv_macro_f1+depth_df.cv_std).to_numpy(),color='#0E7490',alpha=.15)
    ax.set_xticks(xs,depth_df.max_depth);ax.set_xlabel('Tree maximum depth (None = unrestricted)')
    ax.set_ylabel('Macro-F1');ax.set_ylim(.45,1.04);ax.grid(alpha=.16);ax.legend()
    ax.set_title('Q2 - Overfitting: Model Complexity vs Generalization');fig.tight_layout()
    fig.savefig(root/'figures/q2_overfitting.png',dpi=170);plt.close(fig)
    # Mitigation: choose depth via CV ONLY and evaluate that depth on the held-out test.
    depth_df=depth_df.sort_values(by=['cv_macro_f1','train_macro_f1'],ascending=[False,True])
    best_depth_str=depth_df.iloc[0]['max_depth'];best_depth=None if best_depth_str=='None' else int(best_depth_str)
    tuned=make_pipeline(DecisionTreeClassifier(max_depth=best_depth,random_state=SEED)).fit(X_train,y_train)
    unpruned=make_pipeline(DecisionTreeClassifier(random_state=SEED)).fit(X_train,y_train)
    mitigation={
      'selected_max_depth_using_cv':best_depth_str,
      'unpruned_train_macro_f1':float(f1_score(y_train,unpruned.predict(X_train),average='macro')),
      'unpruned_test_macro_f1':float(f1_score(y_test,unpruned.predict(X_test),average='macro')),
      'pruned_train_macro_f1':float(f1_score(y_train,tuned.predict(X_train),average='macro')),
      'pruned_test_macro_f1':float(f1_score(y_test,tuned.predict(X_test),average='macro')),
      'important_note':'Depth selected with training CV only; both held-out test scores reported after selection.'}
    summary={'openml_dataset_id':61,'openml_dataset_url':'https://www.openml.org/d/61',
      'data_origin':origin,'original_rows':original_rows,'duplicates_removed':duplicate_count,
      'missing_values_original':missing_before,'missing_numeric_after_cleaning':numeric_missing_after,
      'cleaned_rows':len(data),'train_rows':len(y_train),'test_rows':len(y_test),
      'train_class_counts':{k:int(v) for k,v in y_train.value_counts().items()},
      'test_class_counts':{k:int(v) for k,v in y_test.value_counts().items()},
      'class_counts_cleaned':{k:int(v) for k,v in data['class'].value_counts().items()},
      'features':FEATURES,'target':'class','cv_folds':5,'random_state':SEED,
      'champion_selected_by_train_cv':champion_name,
      'champion_test_accuracy':float(accuracy_score(y_test,champion_pred)),
      'champion_test_macro_f1':float(f1_score(y_test,champion_pred,average='macro')),
      'champion_confusion_matrix_label_order':LABELS,
      'champion_confusion_matrix':cm.tolist(),
      'classification_report':classification_report(y_test,champion_pred,labels=LABELS,output_dict=True,zero_division=0),
      'overfitting_mitigation':mitigation}
    (root/'results/q2_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print('Q2 successful: train-only stratified CV, final held-out test evaluation.')
    print(comparison.to_string(index=False,float_format=lambda x:f'{x:.3f}'))
    print(json.dumps(summary,indent=2))
    return summary,comparison

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--use-openml-live',action='store_true');args=p.parse_args()
    main(use_openml_live=args.use_openml_live)
