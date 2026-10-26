"""Generate report values and tables directly from frozen experiment artifacts."""
from pathlib import Path
import json
import math
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'report'


def escape(text):
    return str(text).replace('\\', r'\textbackslash{}').replace('_', r'\_').replace('%', r'\%').replace('&', r'\&')


def table(filename, caption, label, columns, headers, rows):
    header = ' & '.join(headers) + r' \\'
    content = [r'\begin{longtable}{' + columns + '}',
               r'\caption{' + caption + r'}\label{' + label + r'}\\',
               r'\toprule', header, r'\midrule\endfirsthead',
               r'\toprule', header, r'\midrule\endhead', r'\bottomrule\endfoot']
    content.extend(' & '.join(row) + r' \\' for row in rows)
    content.append(r'\end{longtable}')
    (OUT / filename).write_text('\n'.join(content), encoding='utf-8')


def main():
    q1 = json.loads((ROOT/'results/q1_metrics.json').read_text())
    q2 = json.loads((ROOT/'results/q2_metrics.json').read_text())
    rows = q2['models']
    assert len(rows) == 15 and len({r['model'] for r in rows}) == 15
    assert q2['winner_by_cv'] == max(rows, key=lambda r: r['cv_macro_f1'])['model']
    assert all(math.isfinite(r[key]) and 0 <= r[key] <= 1 for r in rows
               for key in ['cv_macro_f1', 'accuracy', 'macro_f1', 'roc_auc'])
    l, g = q1['linear'], q1['logistic']
    values = {'LinInitial': f"{l['initial_loss']:.4f}", 'LinFinal': f"{l['final_loss']:.6f}",
              'LinIterations': str(l['iterations']), 'LinMSE': f"{l['mse']:.4f}",
              'LinRMSE': f"{l['rmse']:.4f}", 'LinMAE': f"{l['mae']:.4f}", 'LinRSquared': f"{l['r2']:.4f}",
              'LogInitial': f"{g['initial_loss']:.6f}", 'LogFinal': f"{g['final_loss']:.6f}",
              'LogAccuracy': f"{100*g['accuracy']:.2f}", 'LogPrecision': f"{g['precision_positive']:.4f}",
              'LogRecall': f"{g['recall_positive']:.4f}", 'LogFOne': f"{g['f1_positive']:.4f}",
              'LogMacro': f"{g['macro_f1']:.4f}", 'LogAUC': f"{g['roc_auc']:.4f}",
              'LogTestLoss': f"{g['test_cross_entropy']:.6f}", 'SelectedModel': q2['winner_by_cv']}
    (OUT/'generated_results.tex').write_text('\n'.join('\\newcommand{\\'+key+'}{'+val+'}' for key,val in values.items()), encoding='utf-8')
    table('q2_cv_table.tex', 'Model selection on development data (five folds).', 'tab:cv',
          '@{}p{3.6cm}rrrr@{}', ['Model', 'Train $F_M$', 'CV $F_M$', 'SD', 'Gap'],
          [[escape(r['model']), f"{r['selected_train_macro_f1']:.3f}", f"{r['cv_macro_f1']:.3f}",
            f"{r['cv_std']:.3f}", f"{r['gap']:.3f}"] for r in rows])
    table('q2_test_table.tex', 'Held-out test metrics; positive class is bad.', 'tab:test',
          '@{}p{3.6cm}rrrrrr@{}', ['Model', 'Acc.', '$P_1$', '$R_1$', '$F_{1,1}$', '$F_M$', 'AUC'],
          [[escape(r['model'])] + [f'{r[k]:.3f}' for k in ['accuracy','precision_bad','recall_bad','f1_bad','macro_f1','roc_auc']] for r in rows])
    table('q2_overfit_table.tex', 'Base and selected configurations on identical folds.', 'tab:overfit',
          '@{}p{3.6cm}rrrr@{}', ['Model', r'\shortstack{Base\\train}', r'\shortstack{Base\\CV}',
                                 r'\shortstack{Selected\\train}', r'\shortstack{Selected\\CV}'],
          [[escape(r['model'])] + [f'{r[k]:.3f}' for k in ['default_train_macro_f1','default_cv_macro_f1','selected_train_macro_f1','cv_macro_f1']] for r in rows])
    settings = {
      'Majority baseline': r'Always predicts good; no tuned parameter.',
      'Scratch logistic': r'$\eta=0.5$, 1,500 full-batch updates, no penalty.',
      'Perceptron': r'$\eta=0.01$, 300 passes, shuffled samples.',
      'kNN': r'$k=1$, Euclidean distance, uniform voting.',
      'Gaussian NB': r'Variance smoothing $=0.01$; numeric and one-hot inputs.',
      'Bernoulli NB': r'$\alpha=2$; numeric threshold $0.5$ after scaling.',
      'Decision tree': r'Gini, maximum depth 6, minimum 5 records per leaf.',
      'Linear SVM': r'Linear kernel, $C=10$.',
      'RBF SVM': r'$C=10$; $\gamma=1/(d\,\mathrm{Var}(X_{train}))$.',
      'Polynomial SVM': r'$C=1$, degree 3, offset 0; scaled $\gamma$.',
      'MLP': r'One hidden layer of 16 tanh units, SGD step 0.05, 500 epochs.',
      'Bagging': r'50 bootstrap trees, unlimited depth, minimum leaf size 5.',
      'Random forest': r'150 trees, depth 10, minimum leaf size 1, $\sqrt d$ feature sampling.',
      'AdaBoost': r'150 decision stumps, learning rate 1.',
      'Gradient boosting': r'150 depth-3 trees, learning rate 0.05.'}
    # These descriptions must remain synchronized with selected parameters.
    expected = {'Scratch logistic': {'model__epochs':1500}, 'MLP':{'model__hidden_layer_sizes':[16], 'model__learning_rate_init':.05},
                'Decision tree':{'model__criterion':'gini','model__max_depth':6,'model__min_samples_leaf':5}}
    assert all(next(r['parameters'] for r in rows if r['model']==name)==params for name,params in expected.items())
    table('q2_settings_table.tex', 'Selected settings, refitted on 800 records.', 'tab:settings',
          '@{}p{3.6cm}p{10.9cm}@{}', ['Model', 'Configuration'],
          [[escape(r['model']), settings[r['model']]] for r in rows])
    print('Report values generated from verified result files.')

if __name__ == '__main__': main()
