"""Run the frozen Q1/Q2 design; save all results used by the report."""
from pathlib import Path
import hashlib
import json
import platform
import time
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import scipy
from scipy.io import arff
import sklearn
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_validate
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import (BaggingClassifier, RandomForestClassifier,
                              AdaBoostClassifier, GradientBoostingClassifier)
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, roc_curve,
                             mean_squared_error, mean_absolute_error, r2_score)
from models import LinearRegressionGD, LogisticRegressionGD, ScratchLogisticClassifier, sigmoid

ROOT = Path(__file__).resolve().parents[1]
RESULTS, FIGURES = ROOT / 'results', ROOT / 'results' / 'figures'
SEED = 42
NUMERIC = ['duration', 'credit_amount', 'installment_commitment', 'residence_since',
           'age', 'existing_credits', 'num_dependents']
font_manager.fontManager.addfont('/usr/share/fonts/TTF/Times.TTF') if Path('/usr/share/fonts/TTF/Times.TTF').exists() else None
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 13,
                     'axes.titlesize': 13, 'figure.dpi': 120, 'savefig.dpi': 220})


def save_json(name, value):
    (RESULTS / name).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')


def figure(name):
    plt.savefig(FIGURES / name, bbox_inches='tight', facecolor='white')
    plt.close()


def classification_metrics(y, predicted, scores):
    return {'accuracy': float(accuracy_score(y, predicted)),
            'precision_bad': float(precision_score(y, predicted, zero_division=0)),
            'recall_bad': float(recall_score(y, predicted, zero_division=0)),
            'f1_bad': float(f1_score(y, predicted, zero_division=0)),
            'macro_f1': float(f1_score(y, predicted, average='macro', zero_division=0)),
            'roc_auc': float(roc_auc_score(y, scores)),
            'confusion_matrix': confusion_matrix(y, predicted, labels=[0, 1]).tolist()}


def run_q1():
    rng = np.random.default_rng(SEED)
    X = rng.uniform(-3, 3, (600, 3))
    truth_w, truth_b = np.array([3., -2., 1.5]), 4.
    y = X @ truth_w + truth_b + rng.normal(0, 0.5, len(X))
    train, test = train_test_split(np.arange(len(y)), test_size=0.2, random_state=SEED)
    minimum, span = X[train].min(axis=0), np.ptp(X[train], axis=0)
    X_scaled = (X - minimum) / np.where(span == 0, 1, span)
    model = LinearRegressionGD(0.3, 4000).fit(X_scaled[train], y[train])
    predicted = model.predict(X_scaled[test])
    linear = {'train_n': len(train), 'test_n': len(test), 'learning_rate': 0.3,
              'max_epochs': 4000, 'iterations': model.n_iter_, 'gradient_norm': model.gradient_norm_,
              'initial_loss': model.loss_history_[0], 'final_loss': model.loss_history_[-1],
              'mse': float(mean_squared_error(y[test], predicted)),
              'rmse': float(np.sqrt(mean_squared_error(y[test], predicted))),
              'mae': float(mean_absolute_error(y[test], predicted)), 'r2': float(r2_score(y[test], predicted)),
              'raw_weights': (model.w_ / span).tolist(),
              'raw_bias': float(model.b_ - minimum @ (model.w_ / span)),
              'true_weights': truth_w.tolist(), 'true_bias': truth_b,
              'minimum': minimum.tolist(), 'range': span.tolist()}
    np.savez_compressed(RESULTS / 'q1_linear_data.npz', X=X, y=y, train=train, test=test,
                        predicted=predicted, weights=model.w_, bias=model.b_)
    pd.DataFrame({'iteration': np.arange(len(model.loss_history_)),
                  'loss': model.loss_history_}).to_csv(RESULTS / 'q1_linear_loss.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.4))
    axes[0].semilogy(model.loss_history_, color='#1767a8')
    axes[0].set(xlabel='GD iteration', ylabel='Training loss (MSE / 2)')
    axes[1].scatter(y[test], predicted, s=14, alpha=.65, color='#1767a8')
    lo, hi = min(y[test].min(), predicted.min()), max(y[test].max(), predicted.max())
    axes[1].plot([lo, hi], [lo, hi], 'k--', linewidth=1)
    axes[1].set(xlabel='Actual test target', ylabel='Predicted target')
    fig.tight_layout(); figure('q1_linear.png')

    rng = np.random.default_rng(SEED + 1)
    X = rng.normal(size=(800, 2))
    probability = sigmoid(0.8 + 1.6 * X[:, 0] - 1.2 * X[:, 1])
    y = (rng.random(len(X)) < probability).astype(int)
    train, test = train_test_split(np.arange(len(y)), test_size=0.2, random_state=SEED, stratify=y)
    minimum, span = X[train].min(axis=0), np.ptp(X[train], axis=0)
    X_scaled = (X - minimum) / np.where(span == 0, 1, span)
    model = LogisticRegressionGD(0.5, 5000).fit(X_scaled[train], y[train])
    predicted, scores = model.predict(X_scaled[test]), model.predict_proba(X_scaled[test])[:, 1]
    logistic = {'train_n': len(train), 'test_n': len(test), 'learning_rate': 0.5,
                'max_epochs': 5000, 'iterations': model.n_iter_, 'gradient_norm': model.gradient_norm_,
                'initial_loss': model.loss_history_[0], 'final_loss': model.loss_history_[-1],
                'train_positive': int(y[train].sum()), 'test_positive': int(y[test].sum()),
                'test_cross_entropy': model.loss_gradient(X_scaled[test], y[test], model.w_, model.b_)[0],
                'raw_weights': (model.w_ / span).tolist(),
                'raw_bias': float(model.b_ - minimum @ (model.w_ / span)),
                **{k.replace('_bad', '_positive'): v for k, v in classification_metrics(y[test], predicted, scores).items()}}
    np.savez_compressed(RESULTS / 'q1_logistic_data.npz', X=X, y=y, train=train, test=test,
                        predicted=predicted, scores=scores, weights=model.w_, bias=model.b_)
    pd.DataFrame({'iteration': np.arange(len(model.loss_history_)),
                  'loss': model.loss_history_}).to_csv(RESULTS / 'q1_logistic_loss.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.4))
    axes[0].plot(model.loss_history_, color='#1767a8')
    axes[0].set(xlabel='GD iteration', ylabel='Training binary cross entropy')
    for label, color in [(0, '#1767a8'), (1, '#c34332')]:
        mask = y[test] == label
        axes[1].scatter(X[test][mask, 0], X[test][mask, 1], s=14, alpha=.65, color=color, label=str(label))
    raw_w, raw_b = np.array(logistic['raw_weights']), logistic['raw_bias']
    line = np.array([X[test, 0].min(), X[test, 0].max()])
    axes[1].plot(line, -(raw_b + raw_w[0] * line) / raw_w[1], 'k--', label='p = 0.5')
    axes[1].set(xlabel='Feature 1', ylabel='Feature 2', ylim=(X[test, 1].min()-.2, X[test, 1].max()+.2))
    axes[1].legend(fontsize=10)
    fig.tight_layout(); figure('q1_logistic.png')
    for history in ['q1_linear_loss.csv', 'q1_logistic_loss.csv']:
        assert np.all(np.diff(pd.read_csv(RESULTS / history)['loss']) <= 1e-10), 'Unexpected loss increase'
    save_json('q1_metrics.json', {'linear': linear, 'logistic': logistic})
    print('Q1 finished.', flush=True)


def load_credit():
    path = ROOT / 'data' / 'credit-g.arff'
    content = path.read_bytes()
    if hashlib.md5(content).hexdigest() != '9a475053fed0c26ee95cd4525e50074c':
        raise ValueError('The OpenML ARFF checksum does not match the frozen source.')
    records, _ = arff.loadarff(path)
    frame = pd.DataFrame(records)
    for column in frame.select_dtypes(include='object'):
        frame[column] = frame[column].map(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
        frame[column] = frame[column].replace('?', np.nan)
    if frame.shape != (1000, 21) or not set(frame['class']) == {'good', 'bad'}:
        raise ValueError('Unexpected dataset schema or target.')
    audit = {'rows': len(frame), 'predictors': 20, 'numeric': NUMERIC,
             'categorical': [c for c in frame if c not in NUMERIC + ['class']],
             'missing_cells': int(frame.isna().sum().sum()),
             'duplicate_rows': int(frame.duplicated().sum()),
             'nonfinite_numeric': int((~np.isfinite(frame[NUMERIC].to_numpy())).sum()),
             'class_counts': frame['class'].value_counts().to_dict(),
             'arff_sha256': hashlib.sha256(content).hexdigest(),
             'arff_md5': hashlib.md5(content).hexdigest(),
             'source': 'https://www.openml.org/d/31', 'id': 31, 'version': 1}
    if audit['missing_cells'] or audit['duplicate_rows'] or audit['nonfinite_numeric']:
        raise ValueError('The frozen dataset changed: inspect the audit before running experiments.')
    return frame, audit


def make_preprocessor(categorical):
    return ColumnTransformer([('numeric', MinMaxScaler(), NUMERIC),
                              ('categorical', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical)],
                             remainder='drop')


def candidates():
    return [
        ('Majority baseline', DummyClassifier(strategy='most_frequent'), {}),
        ('Scratch logistic', ScratchLogisticClassifier(), {'model__epochs': [1500, 4000]}),
        ('Perceptron', Perceptron(tol=None, max_iter=300, random_state=SEED), {'model__eta0': [.01, .1, 1.]}),
        ('kNN', KNeighborsClassifier(), {'model__n_neighbors': [1, 5, 11, 21, 41]}),
        ('Gaussian NB', GaussianNB(), {'model__var_smoothing': [1e-9, 1e-5, 1e-2]}),
        ('Bernoulli NB', BernoulliNB(binarize=.5), {'model__alpha': [.5, 1., 2.]}),
        ('Decision tree', DecisionTreeClassifier(random_state=SEED),
         {'model__criterion': ['gini', 'entropy'], 'model__max_depth': [3, 6, None], 'model__min_samples_leaf': [1, 5]}),
        ('Linear SVM', SVC(kernel='linear'), {'model__C': [.1, 1., 10.]}),
        ('RBF SVM', SVC(kernel='rbf'), {'model__C': [.1, 1., 10.], 'model__gamma': ['scale', .1]}),
        ('Polynomial SVM', SVC(kernel='poly', degree=2), {'model__C': [.1, 1., 10.], 'model__degree': [2, 3]}),
        ('MLP', MLPClassifier(hidden_layer_sizes=(16,), activation='tanh', solver='sgd',
                              alpha=0., momentum=0., nesterovs_momentum=False,
                              max_iter=500, tol=0., n_iter_no_change=501, random_state=SEED),
         {'model__hidden_layer_sizes': [(16,), (32,)], 'model__learning_rate_init': [.01, .05]}),
        ('Bagging', BaggingClassifier(estimator=DecisionTreeClassifier(random_state=SEED),
                                      n_estimators=50, random_state=SEED, n_jobs=1),
         {'model__estimator__max_depth': [4, None], 'model__estimator__min_samples_leaf': [1, 5]}),
        ('Random forest', RandomForestClassifier(n_estimators=150, random_state=SEED, n_jobs=1),
         {'model__max_depth': [6, 10, None], 'model__min_samples_leaf': [1, 5]}),
        ('AdaBoost', AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1, random_state=SEED), random_state=SEED),
         {'model__n_estimators': [50, 150], 'model__learning_rate': [.1, 1.]}),
        ('Gradient boosting', GradientBoostingClassifier(random_state=SEED),
         {'model__n_estimators': [50, 150], 'model__learning_rate': [.05, .1], 'model__max_depth': [1, 3]}),
    ]


def exploratory_plots(X, y):
    fig, axes = plt.subplots(2, 2, figsize=(8, 6.2))
    counts = np.bincount(y, minlength=2)
    axes[0, 0].bar(['good (0)', 'bad (1)'], counts, color=['#1767a8', '#c34332'])
    axes[0, 0].set(ylabel='Development records', title='Class distribution (n = 800)')
    for label, color in [(0, '#1767a8'), (1, '#c34332')]:
        axes[0, 1].hist(X.loc[y == label, 'credit_amount'], bins=20, alpha=.5, color=color, label=['good', 'bad'][label])
        axes[1, 0].hist(X.loc[y == label, 'age'], bins=15, alpha=.5, color=color)
    axes[0, 1].set(xlabel='Credit amount (original units)', ylabel='Count', title='Right-skewed credit amounts')
    axes[0, 1].legend()
    axes[1, 0].set(xlabel='Age (years)', ylabel='Count', title='Age distributions overlap')
    table = pd.crosstab(X['checking_status'], y, normalize='index')
    table.rename(columns={0: 'good', 1: 'bad'}).plot.bar(stacked=True, ax=axes[1, 1], color=['#1767a8', '#c34332'])
    axes[1, 1].set(xlabel='Checking status', ylabel='Within-category fraction', title='Categorical predictor')
    axes[1, 1].tick_params(axis='x', rotation=25)
    axes[1, 1].legend(fontsize=10)
    fig.tight_layout(); figure('q2_eda.png')


def run_q2():
    frame, audit = load_credit()
    X, y = frame.drop(columns='class'), (frame['class'] == 'bad').astype(int)
    development, test = train_test_split(np.arange(len(y)), test_size=.2, stratify=y, random_state=SEED)
    assert not set(development) & set(test)
    assert len(set(development) | set(test)) == len(y)
    X_dev, y_dev, X_test, y_test = X.iloc[development], y.iloc[development], X.iloc[test], y.iloc[test]
    pd.DataFrame({'row_id': np.arange(len(y)), 'split': np.where(np.isin(np.arange(len(y)), test), 'test', 'development'),
                  'target_bad': y}).to_csv(RESULTS / 'q2_split.csv', index=False)
    folds = list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(X_dev, y_dev))
    fold_assignment = np.full(len(y_dev), -1)
    for number, (train, validation) in enumerate(folds):
        assert not set(train) & set(validation)
        fold_assignment[validation] = number
    pd.DataFrame({'row_id': development, 'validation_fold': fold_assignment}).to_csv(RESULTS / 'q2_folds.csv', index=False)
    exploratory_plots(X_dev, y_dev)
    audit['development_class_counts'] = y_dev.value_counts().to_dict()
    audit['test_class_counts'] = y_test.value_counts().to_dict()
    audit['numeric_summary_development'] = X_dev[NUMERIC].describe().to_dict()
    q1, q3 = X_dev[NUMERIC].quantile(.25), X_dev[NUMERIC].quantile(.75)
    iqr = q3 - q1
    audit['iqr_outlier_counts_development'] = ((X_dev[NUMERIC] < q1-1.5*iqr) | (X_dev[NUMERIC] > q3+1.5*iqr)).sum().to_dict()
    preprocessing = make_preprocessor(audit['categorical'])
    summary, selected_models, captured_warnings = [], {}, []
    cv_records = []
    design = []
    for name, estimator, grid in candidates():
        design.append({'model': name, 'base_parameters': estimator.get_params(deep=True).__repr__(), 'grid': grid})
    save_json('q2_design.json', {'selection_metric': 'macro_f1', 'seed': SEED,
                               'folds': 5, 'design': design, 'test_used_for_selection': False})
    # Finish selection for EVERY model before evaluating ANY on the test set.
    for name, estimator, grid in candidates():
        start = time.perf_counter()
        pipeline = Pipeline([('prepare', clone(preprocessing)), ('model', estimator)])
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            base = cross_validate(pipeline, X_dev, y_dev, cv=folds, scoring='f1_macro', return_train_score=True)
            search = GridSearchCV(pipeline, grid, cv=folds, scoring='f1_macro',
                                  return_train_score=True, refit=True, error_score='raise', n_jobs=1)
            search.fit(X_dev, y_dev)
        captured_warnings.extend({'model': name, 'category': w.category.__name__, 'message': str(w.message)} for w in caught)
        best = search.best_index_
        train_scores = np.array([search.cv_results_[f'split{k}_train_score'][best] for k in range(5)])
        val_scores = np.array([search.cv_results_[f'split{k}_test_score'][best] for k in range(5)])
        row = {'model': name, 'default_train_macro_f1': float(base['train_score'].mean()),
               'default_cv_macro_f1': float(base['test_score'].mean()),
               'selected_train_macro_f1': float(train_scores.mean()),
               'cv_macro_f1': float(val_scores.mean()), 'cv_std': float(val_scores.std(ddof=1)),
               'gap': float((train_scores - val_scores).mean()),
               'parameters': search.best_params_, 'selection_seconds': time.perf_counter()-start}
        summary.append(row)
        selected_models[name] = search.best_estimator_
        for candidate in range(len(search.cv_results_['params'])):
            for fold in range(5):
                cv_records.append({'model': name, 'candidate': candidate, 'fold': fold,
                                   'parameters': json.dumps(search.cv_results_['params'][candidate]),
                                   'train_macro_f1': search.cv_results_[f'split{fold}_train_score'][candidate],
                                   'validation_macro_f1': search.cv_results_[f'split{fold}_test_score'][candidate]})
        print(f'{name}: CV macro F1 {row["cv_macro_f1"]:.4f}; train {row["selected_train_macro_f1"]:.4f}', flush=True)
    winner = max((r for r in summary if r['model'] != 'Majority baseline'), key=lambda r: r['cv_macro_f1'])['model']
    save_json('q2_selection.json', {'winner_by_cv': winner, 'models': summary})
    pd.DataFrame(cv_records).to_csv(RESULTS / 'q2_cv_candidates.csv', index=False)
    chosen = selected_models[winner]
    audit['encoded_features'] = len(chosen.named_steps['prepare'].get_feature_names_out())
    save_json('q2_audit.json', audit)

    curve = []
    for depth in [1, 2, 3, 4, 6, 8, None]:
        pipeline = Pipeline([('prepare', clone(preprocessing)),
                             ('model', DecisionTreeClassifier(max_depth=depth, random_state=SEED))])
        score = cross_validate(pipeline, X_dev, y_dev, cv=folds, scoring='f1_macro', return_train_score=True)
        curve.append({'depth': 'unlimited' if depth is None else str(depth),
                      'train_macro_f1': score['train_score'].mean(), 'cv_macro_f1': score['test_score'].mean()})
    pd.DataFrame(curve).to_csv(RESULTS / 'q2_tree_depth.csv', index=False)
    fig, ax = plt.subplots(figsize=(6.8, 3.5))
    ax.plot([c['depth'] for c in curve], [c['train_macro_f1'] for c in curve], 'o-', label='Fold training')
    ax.plot([c['depth'] for c in curve], [c['cv_macro_f1'] for c in curve], 's-', label='Fold validation')
    ax.set(xlabel='Maximum tree depth', ylabel='Mean macro F1', ylim=(.3, 1.03)); ax.legend()
    fig.tight_layout(); figure('q2_overfitting.png')

    predictions = pd.DataFrame({'row_id': test, 'actual_bad': y_test.to_numpy()})
    scores_by_model = {}
    for row in summary:
        name, fitted = row['model'], selected_models[row['model']]
        predicted = fitted.predict(X_test)
        scores = fitted.predict_proba(X_test)[:, 1] if hasattr(fitted, 'predict_proba') else fitted.decision_function(X_test)
        row.update(classification_metrics(y_test, predicted, scores))
        predictions[name + '__prediction'] = predicted
        predictions[name + '__score'] = scores
        scores_by_model[name] = scores
    predictions.to_csv(RESULTS / 'q2_test_predictions.csv', index=False)
    save_json('q2_metrics.json', {'winner_by_cv': winner, 'models': summary})
    pd.DataFrame([{k: v for k, v in row.items() if k not in ['parameters', 'confusion_matrix']} for row in summary]).to_csv(RESULTS / 'q2_comparison.csv', index=False)
    save_json('warnings.json', captured_warnings)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6))
    winner_row = next(row for row in summary if row['model'] == winner)
    matrix = np.array(winner_row['confusion_matrix'])
    axes[0].imshow(matrix, cmap='Blues')
    for i in range(2):
        for j in range(2):
            axes[0].text(j, i, str(matrix[i, j]), ha='center', va='center', fontsize=17,
                         color='white' if matrix[i, j] > matrix.max()/2 else 'black')
    axes[0].set(xticks=[0, 1], yticks=[0, 1], xticklabels=['good', 'bad'], yticklabels=['good', 'bad'],
                xlabel='Predicted label', ylabel='Actual label', title=winner)
    top = sorted((r for r in summary if r['model'] != 'Majority baseline'), key=lambda r: r['cv_macro_f1'], reverse=True)[:3]
    for row in top:
        fpr, tpr, _ = roc_curve(y_test, scores_by_model[row['model']])
        axes[1].plot(fpr, tpr, label=f'{row["model"]}: {row["roc_auc"]:.3f}')
    axes[1].plot([0, 1], [0, 1], 'k--', linewidth=1)
    axes[1].set(xlabel='False positive rate', ylabel='True positive rate', xlim=(0, 1), ylim=(0, 1))
    axes[1].legend(fontsize=10, loc='lower right')
    fig.tight_layout(); figure('q2_test.png')
    fig, ax = plt.subplots(figsize=(7.3, 4.7))
    ordered = sorted(summary, key=lambda r: r['cv_macro_f1'])
    locations = np.arange(len(ordered))
    ax.barh(locations-.16, [r['cv_macro_f1'] for r in ordered], height=.3, label='5-fold CV')
    ax.barh(locations+.16, [r['macro_f1'] for r in ordered], height=.3, label='Held-out test')
    ax.set(yticks=locations, yticklabels=[r['model'] for r in ordered], xlabel='Macro F1', xlim=(0, 1))
    ax.legend(loc='lower right'); fig.tight_layout(); figure('q2_comparison.png')
    print(f'Q2 finished. CV-selected model: {winner}', flush=True)


def main():
    RESULTS.mkdir(exist_ok=True); FIGURES.mkdir(exist_ok=True)
    start = time.perf_counter()
    run_q1(); run_q2()
    save_json('environment.json', {'python': platform.python_version(), 'numpy': np.__version__,
                                  'pandas': pd.__version__, 'scipy': scipy.__version__,
                                  'scikit_learn': sklearn.__version__, 'matplotlib': matplotlib.__version__,
                                  'seed': SEED, 'elapsed_seconds': time.perf_counter()-start})

if __name__ == '__main__': main()
