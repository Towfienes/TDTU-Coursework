from pathlib import Path
import json, pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether,HRFlowable,CondPageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_CENTER,TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

root=Path(__file__).resolve().parents[1]
metrics=json.loads((root/'results/q1_metrics.json').read_text())
q2=json.loads((root/'results/q2_summary.json').read_text())
rank=pd.read_csv(root/'results/q2_model_comparison.csv')
depth=pd.read_csv(root/'results/q2_tree_depth_study.csv',keep_default_na=False)
output=root/'report/Machine_Learning_Midterm_Report.pdf'
C_NAVY=colors.HexColor('#142A46');C_BLUE=colors.HexColor('#0E7490');C_MUTED=colors.HexColor('#536478');C_PALE=colors.HexColor('#E9F4F7');C_LINE=colors.HexColor('#CBD5DF');C_SOFT=colors.HexColor('#F2F6FA')
def find_font(*candidates):
    for filename in candidates:
        for directory in ['/usr/share/fonts/truetype/lato','/usr/share/fonts/TTF',
                          '/usr/share/fonts/truetype/dejavu','/usr/local/share/fonts']:
            p=Path(directory)/filename
            if p.is_file():return str(p)
        for p in Path('/usr/share/fonts').rglob(filename):
            if p.is_file():return str(p)
    raise FileNotFoundError('Install ttf-lato or ttf-dejavu on Linux to regenerate the PDF')
pdfmetrics.registerFont(TTFont('Lato',find_font('Lato-Regular.ttf','DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('LatoBold',find_font('Lato-Bold.ttf','DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('LatoItalic',find_font('Lato-Italic.ttf','DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='LatoBold',italic='LatoItalic',boldItalic='LatoBold')
S={
 'title':ParagraphStyle('title',fontName='LatoBold',fontSize=31,leading=37,textColor=C_NAVY,spaceAfter=16),
 'subtitle':ParagraphStyle('subtitle',fontName='Lato',fontSize=15,leading=21,textColor=C_BLUE,spaceAfter=18),
 'h1':ParagraphStyle('h1',fontName='LatoBold',fontSize=18,leading=24,textColor=C_NAVY,spaceBefore=13,spaceAfter=12),
 'h2':ParagraphStyle('h2',fontName='LatoBold',fontSize=11.6,leading=16,textColor=C_BLUE,spaceBefore=11,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='Lato',fontSize=9.4,leading=14.5,textColor=C_NAVY,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='Lato',fontSize=8,leading=12,textColor=C_MUTED,spaceAfter=6),
 'bullet':ParagraphStyle('bullet',fontName='Lato',fontSize=9.2,leading=13.6,leftIndent=15,firstLineIndent=-10,spaceAfter=5,textColor=C_NAVY),
 'code':ParagraphStyle('code',fontName='Lato',fontSize=8.8,leading=13,textColor=C_NAVY,leftIndent=10,spaceAfter=5),
 'caption':ParagraphStyle('caption',fontName='LatoItalic',fontSize=8.2,leading=12,textColor=C_MUTED,spaceAfter=9,alignment=TA_CENTER),
 'th':ParagraphStyle('th',fontName='LatoBold',fontSize=8,leading=10.5,textColor=colors.white),
 'cell':ParagraphStyle('cell',fontName='Lato',fontSize=7.7,leading=10.7,textColor=C_NAVY),
 'metric':ParagraphStyle('metric',fontName='LatoBold',fontSize=14.5,leading=20,textColor=C_BLUE,alignment=TA_CENTER),
 'metlabel':ParagraphStyle('metlabel',fontName='Lato',fontSize=8,leading=11,textColor=C_MUTED,alignment=TA_CENTER),
}

def P(text,style='body'):return Paragraph(str(text),S[style])
def bullet(text):return P('&#8226;  '+text,'bullet')
def heading(t): return P(t,'h1')
def sub(t):return P(t,'h2')
def tbl(rows, widths=None, header=True, small=False, numeric=None):
 data=[]
 for r,row in enumerate(rows):
    rr=[]
    for entry in row:
      text=str(entry)
      rr.append(P(text,'th' if header and r==0 else 'cell'))
    data.append(rr)
 table=Table(data,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
 styling=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
          ('LINEBELOW',(0,-1),(-1,-1),.5,C_LINE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,C_SOFT])]
 if header:styling.extend([('BACKGROUND',(0,0),(-1,0),C_NAVY),('TOPPADDING',(0,0),(-1,0),8),('BOTTOMPADDING',(0,0),(-1,0),8)])
 else:styling.append(('BOX',(0,0),(-1,-1),.5,C_LINE))
 table.setStyle(TableStyle(styling));return table

def fig(file,width=485):
 from PIL import Image as PILImage
 path=root/'figures'/file
 w,h=PILImage.open(path).size
 return Image(str(path),width=width,height=width*h/w,hAlign='CENTER')

def paired(left,right,width=240):
 return Table([[fig(left,width),fig(right,width)]],colWidths=[246,246],style=TableStyle([
 ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4)]))

def equation(name,lines):
 path=root/'figures'/name
 figu,ax=plt.subplots(figsize=(9,0.58*len(lines)+.12),dpi=195)
 ax.set_axis_off()
 for i,line in enumerate(lines):
  ax.text(.025,1-(i+.5)/len(lines),line,size=14.5,ha='left',va='center',color='#142A46',transform=ax.transAxes)
 figu.subplots_adjust(left=.02,right=.99,top=.99,bottom=.01)
 figu.savefig(path,facecolor='#F1F7F9');plt.close(figu)
 return fig(name,485)

linear_eq=equation('linear_equations.png',[
 r'$\hat{y}_i=\mathbf{x}_i^\top\mathbf{w}+b$',
 r'$J(\mathbf{w},b)=\frac{1}{2m}\sum_{i=1}^{m}(\hat{y}_i-y_i)^2$',
 r'$\nabla_{\mathbf{w}}J=\frac{1}{m}X^\top(\hat{\mathbf{y}}-\mathbf{y})$',
 r'$\frac{\partial J}{\partial b}=\frac{1}{m}\sum_{i=1}^{m}(\hat{y}_i-y_i)$',
])
logistic_eq=equation('logistic_equations.png',[
 r'$z_i=\mathbf{x}_i^\top\mathbf{w}+b\qquad p_i=\sigma(z_i)=\frac{1}{1+e^{-z_i}}$',
 r'$J(\mathbf{w},b)=-\frac{1}{m}\sum_i[y_i\log(p_i)+(1-y_i)\log(1-p_i)]$',
 r'$\frac{\partial J}{\partial z_i}=p_i-y_i$',
 r'$\nabla_{\mathbf{w}}J=\frac{1}{m}X^\top(\mathbf{p}-\mathbf{y}),\quad\frac{\partial J}{\partial b}=\frac{1}{m}\sum_i(p_i-y_i)$',
])
W=509
story=[]
def add(*things): story.extend(things)
# COVER
add(Spacer(1,40),P('INTRODUCTION TO MACHINE LEARNING','subtitle'),
  P('MIDTERM<br/>PROJECT REPORT','title'),HRFlowable(width='100%',thickness=4,color=C_BLUE),Spacer(1,28),
  P('Question 1: Linear &amp; Logistic Regression from Scratch<br/>Question 2: OpenML Classification Benchmark','subtitle'),
  Spacer(1,12),
  tbl([['REPORT INFORMATION','DETAILS'],['Course','Introduction to Machine Learning'],
       ['Assessment','Middle Exam — 10 points total'],['Student name / ID','_______________________________'],
       ['Group / section','_______________________________'],
       ['Execution','Python 3 | NumPy | scikit-learn | Matplotlib'],
       ['Prepared on','8 October 2026']],widths=[145,344]),
  Spacer(1,24),P('EXPERIMENT SNAPSHOT','h2'))
metrics_box=tbl([['Q1: Linear Regression','Q1: Logistic Regression','Q2: Classifier comparison'],
 [f"R² {metrics['linear']['r2']:.3f} / RMSE {metrics['linear']['rmse']:.3f}",
  f"Accuracy {metrics['logistic']['accuracy']:.1%}",
  f"13 methods / selected {q2['champion_test_accuracy']:.1%} accuracy"]],widths=[166,166,167])
add(metrics_box,Spacer(1,15),P('Reproducibility note: The experiments below were actually executed and saved. Q2 uses a bundled offline copy of Fisher\'s Iris dataset registered at OpenML ID 61. The live OpenML endpoint could not be reached in the execution environment; this distinction is documented throughout.','small'))
add(PageBreak())
# TABLE OF CONTENTS / overview
add(heading('Executive Summary &amp; Submission Map'),
 P('This report addresses every rubric item in the uploaded assignment: mathematical description, appropriate losses and gradients, Gradient Descent training, from-scratch implementations with evaluation for Question 1, followed by data preparation, multi-model comparison and overfitting mitigation for Question 2.'),
 sub('Deliverables and where to find them'),
 tbl([['Deliverable','Contents'],['This PDF','Theory, derivations, methodology, experimental measurements, analysis and citations'],
 ['Q1_Linear_Regression.ipynb','Self-contained NumPy class code, dataset creation, training curves and test metrics'],
 ['Q1_Logistic_Regression.ipynb','Stable sigmoid/BCE implementation, optimization, confusion matrix and metrics'],
 ['Q2_Classification.ipynb','Dataset EDA, train-only preprocessing, 13 methods, comparative results, complexity study'],
 ['src/*.py and results/*','Reusable programs and numerical output CSV/JSON files'],
 ['data/* and figures/*','Bundled offline Iris data and publication-ready experimental plots']],widths=[176,313]),
 sub('Scientific protocol'),
 bullet('Use deterministic random seeds and make separate training/test splits.'),
 bullet('Fit feature scaling only on the training data; for Q2, scale/impute inside cross-validation folds.'),
 bullet('Report held-out test performance, with model selection in Q2 based only on cross-validation within the training split.'),
 bullet('Check Q1 analytical gradients against finite-difference numerical derivatives.'),
 bullet('Show an explicit overfitting demonstration and a pre-pruning mitigation experiment.'),
 sub('Important limits'),
 P('Q1 uses synthetic datasets as expressly permitted by the task. Q2 uses the Iris dataset registered at OpenML (ID 61, version 1); to ensure offline reproducibility, the observations were loaded from the local Fisher Iris copy distributed with scikit-learn. This execution did not verify a live download from OpenML. The report makes no claims about real-world decision-making reliability.'))
add(PageBreak())
# q1 linear theory
add(heading('1. Linear Regression — Model &amp; Theory'),
 P('<b>Problem:</b> supervised regression. Given a feature vector with d numeric inputs, estimate a continuous target (e.g., house price). For a dataset of m observations, the model predicts an affine function of the features.'),
 linear_eq,
 sub('1.1 Derivation of the mean squared error gradient'),
 P('Define each residual r<sub>i</sub> = x<sub>i</sub><super>T</super>w + b - y<sub>i</sub>. The cost is J = (1 / 2m) sum r<sub>i</sub><super>2</super>. By the chain rule, the derivative of r<sub>i</sub><super>2</super> / 2 with respect to w<sub>j</sub> is r<sub>i</sub> x<sub>ij</sub>. The derivative with respect to b is r<sub>i</sub> because the intercept has coefficient one.'),
 P('Therefore, dJ/dw<sub>j</sub> = (1/m) sum r<sub>i</sub>x<sub>ij</sub>, and dJ/db = (1/m) sum r<sub>i</sub>. Stacking all d derivatives gives the compact matrix expression in the formula box.'),
 sub('1.2 Batch Gradient Descent algorithm'),
 bullet('<b>Step 1.</b> Initialize w as a zero vector, b = 0, choose learning rate eta = 0.08.'),
 bullet('<b>Step 2.</b> In each epoch, compute all predictions and the loss on training observations.'),
 bullet('<b>Step 3.</b> Compute gradient_w = X<super>T</super>(pred - y)/m and gradient_b = mean(pred - y).'),
 bullet('<b>Step 4.</b> Update w := w - eta * gradient_w; b := b - eta * gradient_b.'),
 bullet('<b>Step 5.</b> Repeat for 1200 epochs; never use the test set to update model parameters.'),
 sub('1.3 Implementation details'),
 P('The LinearRegressionGD class in src/q1_models.py implements both the loss/gradient and update loop directly in NumPy; no scikit-learn estimator is involved in fitting. The factor of 1/2 in the loss simplifies its derivative but does not change the optimum.'))
add(PageBreak())
lin=metrics['linear']
add(heading('2. Linear Regression — Experiment &amp; Results'),
 P('Dataset: 360 artificial observations with two independent standard-normal features and y = 4 + 3x1 - 2x2 + Gaussian noise (standard deviation 0.65). The random seed is 42. An 80/20 split produces 288 training and 72 held-out test rows. StandardScaler is fitted on the training features only.'),
 tbl([['Metric','Observed result'],['Learning rate / epochs','0.08 / 1200'],
 ['Training loss, first -> last',f"{lin['train_loss_first']:.4f} -> {lin['train_loss_last']:.4f}"],
 ['Held-out MSE',f"{lin['mse']:.4f}"],['Held-out RMSE',f"{lin['rmse']:.4f}"],
 ['Held-out MAE',f"{lin['mae']:.4f}"],['Held-out R²',f"{lin['r2']:.4f}"],
 ['Maximum gradient-check error',f"{lin['grad_check_max_abs_diff']:.2e}"]],widths=[240,249]),
 Spacer(1,8),paired('q1_linear_loss.png','q1_linear_predictions.png',241),
 P('Figures 1–2. The training objective decreases, and test predictions cluster around the ideal prediction diagonal.','caption'),
 sub('Interpretation'),
 P(f"The model explains approximately {lin['r2']*100:.2f}% of variance on the held-out test data for this deliberately linear synthetic experiment. Its RMSE of {lin['rmse']:.3f} is consistent with the injected random noise scale. The numerical gradient difference of {lin['grad_check_max_abs_diff']:.2e} supports the correctness of the analytical gradient implementation."),
 P('This is an illustrative result under a known data-generating process. It is not evidence that linear regression will be equally accurate for nonlinear or out-of-distribution data.','small'))
add(PageBreak())
# logistic theory
add(heading('3. Logistic Regression — Model &amp; Theory'),
 P('<b>Problem:</b> binary classification. The score z is transformed with the sigmoid function into the estimated probability P(y=1|x). The default decision rule predicts positive class 1 when p is at least 0.5.'),
 logistic_eq,
 sub('3.1 Why cross-entropy?'),
 P('Squared error is suitable for continuous targets; for a Bernoulli outcome, the negative log-likelihood (binary cross-entropy) is the appropriate objective. It heavily penalizes confident but incorrect predicted probabilities. We implement it stably as mean(logaddexp(0, z) - y*z), avoiding log(0) and numerical overflow.'),
 sub('3.2 Gradient derivation: the chain rule'),
 bullet('For one observation, J<sub>i</sub> = -y<sub>i</sub> log(p<sub>i</sub>) - (1-y<sub>i</sub>) log(1-p<sub>i</sub>).'),
 bullet('Differentiate with respect to p: dJ<sub>i</sub>/dp = (p<sub>i</sub>-y<sub>i</sub>) / [p<sub>i</sub>(1-p<sub>i</sub>)].'),
 bullet('The sigmoid derivative is dp/dz = p(1-p), so these factors cancel: dJ<sub>i</sub>/dz = p<sub>i</sub> - y<sub>i</sub>.'),
 bullet('Because dz/dw<sub>j</sub> = x<sub>ij</sub> and dz/db = 1, the model gradients are X<super>T</super>(p-y)/m and mean(p-y).'),
 sub('3.3 Gradient Descent implementation'),
 P('Initialize w = 0 and b = 0. At every epoch: form logits, apply a numerically stable sigmoid, calculate cross-entropy, derive residuals (p-y), and update parameters by subtracting 0.13 times the gradients. Train for 2400 epochs. The class includes a probability predictor and a configurable decision threshold.'),
 P('Implementation: src/q1_models.py, class LogisticRegressionGD. The optimization algorithm is from scratch; scikit-learn is used only for generating data, preprocessing, splitting, and measuring results.'))
add(PageBreak())
log=metrics['logistic']
add(heading('4. Logistic Regression — Experiment &amp; Results'),
 P('Dataset: 600 artificial examples, five features (four informative), binary labels, moderate imbalance (55/45), 4% label flipping, class separation 1.2. Dataset seed 27 and split seed 42. The stratified 80/20 split contains 480 training rows and 120 test rows. Only training statistics determine the scaler.'),
 tbl([['Metric','Observed result'],['Training loss, first -> last',f"{log['train_loss_first']:.4f} -> {log['train_loss_last']:.4f}"],
 ['Held-out accuracy',f"{log['accuracy']*100:.2f}%"],['Precision / recall',f"{log['precision']:.4f} / {log['recall']:.4f}"],
 ['F1 score',f"{log['f1']:.4f}"],['ROC-AUC',f"{log['roc_auc']:.4f}"],
 ['Maximum gradient-check error',f"{log['grad_check_max_abs_diff']:.2e}"],
 ['Confusion matrix [TN,FP;FN,TP]',str(log['confusion_matrix'])]],widths=[245,244]),
 Spacer(1,8),paired('q1_logistic_loss.png','q1_logistic_confusion.png',238),
 P('Figures 3–4. Cross-entropy decreases during training; the confusion matrix summarizes positive/negative test decisions.','caption'),
 sub('Interpretation'),
 P(f"Accuracy is {log['accuracy']:.1%}, while class-1 F1 = {log['f1']:.3f}. Recall = {log['recall']:.3f} captures the model's ability to find positive observations, and ROC-AUC = {log['roc_auc']:.3f} measures ranking across thresholds. The confusion matrix includes 4 false negatives and 10 false positives."),
 P('Accuracy alone may obscure trade-offs under class imbalance. Unlike linear regression, Logistic Regression predicts probabilities and minimizes a Bernoulli likelihood-based loss.','small'))
add(PageBreak())
# q2 data
add(heading('5. OpenML Classification — Dataset &amp; Data Preparation'),
 P('<b>Task:</b> predict the species of a flower from four continuous measurements. The Iris dataset is listed as <b>OpenML ID 61, version 1</b>; the listing reports 150 rows, four explanatory numeric variables, one categorical target and three classes. Source: https://www.openml.org/d/61 [1].'),
 P('<b>Actual execution source:</b> the submission ships a local CSV generated from scikit-learn\'s Fisher Iris copy, matching the OpenML-listed problem definition. Live HTTP download was unavailable in the execution environment. Use the <i>--use-openml-live</i> option to fetch OpenML ID 61 directly when internet access is available. The local copy is not falsely presented as a live OpenML fetch.'),
 tbl([['Data property','Value'],['Raw rows / cleaned rows',f"{q2['original_rows']} / {q2['cleaned_rows']}"],
 ['Exact duplicate rows removed',str(q2['duplicates_removed'])],['Missing raw entries',str(q2['missing_values_original'])],
 ['Numeric features',', '.join(q2['features'])],['Target / categories','class: setosa, versicolor, virginica'],
 ['Training / test rows',f"{q2['train_rows']} / {q2['test_rows']}"],
 ['Train/test rule','70/30 stratified, random_state = 42']],widths=[200,289]),
 sub('5.1 Cleaning and transformations'),
 bullet('Inspect dtypes, class distribution, missing values and exact duplicate rows; remove one fully duplicated observation.'),
 bullet('Convert numeric columns using pandas.to_numeric, replacing invalid or infinite entries with missing values.'),
 bullet('Use a numeric median imputer and StandardScaler inside a Pipeline so each cross-validation fold fits its own transformations.'),
 bullet('The target has three classes. The numeric features need no one-hot encoding; the labels remain categorical strings.'),
 bullet('Original data contain no missing values, so imputation is preventative. Do not claim missing-value imputation materially changed this dataset.'),
 sub('5.2 Exploratory data analysis'),
 paired('q2_class_balance.png','q2_feature_scatter.png',240),
 P('Figures 5–6. Flower classes are approximately balanced. Petal length and width offer visibly useful class separation.','caption'))
add(PageBreak())
# pipeline and descriptive
add(heading('6. Experimental Design &amp; Data Exploration'),
 paired('q2_correlation.png','q2_feature_distributions.png',240),
 P('Figures 7–8. Correlations and raw feature distributions help identify relationships and scale differences. EDA is descriptive and does not fit the predictive pipeline.','caption'),
 sub('6.1 Model training and selection protocol'),
 bullet('After cleaning, stratify a 70% development/30% held-out split. Keep test labels inaccessible for training or CV selection.'),
 bullet('For each model, run 5-fold StratifiedKFold cross-validation on the training partition only, with shuffling and seed 42.'),
 bullet('Inside each CV fold, fit median imputation and standard scaling using only that fold\'s training portion; then fit the estimator.'),
 bullet('Rank classifiers by training-fold mean macro-F1. Ties are resolved by a reproducible alphabetic secondary order.'),
 bullet('Refit models on the full development split; summarize accuracy, macro precision/recall/F1 and the gap between train and held-out test accuracy.'),
 bullet('The final champion is identified using CV, not by reading which model had the highest held-out test accuracy.'),
 sub('6.2 Evaluation metric definitions'),
 P('<b>Accuracy</b> = correct / total predictions. <b>Precision</b> = TP/(TP+FP), <b>Recall</b> = TP/(TP+FN), and <b>F1</b> is the harmonic mean of precision and recall. Macro scores average the per-class scores equally, rather than weighting them by class frequency. CV reports fold mean and standard deviation.'),
 sub('6.3 Methods compared'),
 P('Dummy majority-class predictor; Logistic Regression; k-Nearest Neighbors; SVM (RBF and linear); Decision Tree; Random Forest; Extra Trees; Gradient Boosting; AdaBoost; Gaussian Naive Bayes; Linear Discriminant Analysis; Quadratic Discriminant Analysis (13 methods total). Hyperparameters are deterministic fixed baselines for a broad comparison, not exhaustive model tuning.'))
add(PageBreak())
# comparison
add(heading('7. Classification Benchmark — Measured Results'),
 P('The table below reports actual training-only 5-fold cross-validation macro-F1 and held-out test metrics. Ranking is computed using training CV macro-F1, not test metrics. Scores are rounded to three decimals for readability.'),
 tbl([['Method','CV macro-F1','Test accuracy','Test macro-F1']]+[
   [r['model'],f"{r['cv_macro_f1_mean']:.3f} ± {r['cv_macro_f1_std']:.3f}",
    f"{r['test_accuracy']:.3f}",f"{r['test_f1_macro']:.3f}"] for _,r in rank.iterrows()],
    widths=[178,119,95,97]),
 Spacer(1,12),fig('q2_model_comparison.png',width=390),
 P('Figure 9. Mean training-fold macro-F1 scores with one standard-deviation error bars.','caption'))
add(PageBreak())
add(heading('8. Final Selection &amp; Hold-Out Evaluation'),
 P(f"By the prespecified CV criterion, the selected model is <b>{q2['champion_selected_by_train_cv']}</b>. Its held-out accuracy is <b>{q2['champion_test_accuracy']:.4f}</b> and macro-F1 is <b>{q2['champion_test_macro_f1']:.4f}</b>. The held-out sample contains {q2['test_rows']} observations."),
 fig('q2_champion_confusion.png',width=360),
 P('Figure 10. Confusion matrix for the CV-selected classifier; rows are actual classes, columns are predictions.','caption'),
 sub('Why the highest test score is not automatically the selected model'),
 P('A few candidates (e.g., LDA and QDA in this particular split) show higher measured test scores than the selected model. Choosing a replacement based on those same test outcomes would turn the test set into a tuning signal. This report therefore respects the prespecified training-only cross-validation criterion and uses the test split only as an independent performance estimate.'),
 sub('Statistical caution'),
 P('The sample size is modest; the test set contains only 45 records. A difference of one correctly classified flower changes test accuracy by about 2.22 percentage points. Single-split rankings can therefore be unstable. A more comprehensive study would repeat nested cross-validation and quantify uncertainty, using a larger independent test collection where possible.'),
 P('The experiment demonstrates standard classification workflows, not deployable flower-identification software.'))
add(PageBreak())
# overfit
mit=q2['overfitting_mitigation']
add(heading('9. Overfitting — Diagnosis &amp; Mitigation'),
 P('<b>Overfitting</b> happens when a model fits the development set so closely that its performance on new data is weaker. A highly flexible Decision Tree can isolate individual training examples and achieve near-perfect in-sample performance, even when the boundary is unnecessarily complex.'),
 fig('q2_overfitting.png',width=467),
 P('Figure 11. Train-vs-cross-validation macro-F1 across maximum tree depths; the shaded area marks CV fold variation.','caption'),
 sub('9.1 Observed generalization gap'),
 P(f"The unrestricted tree achieves train macro-F1 = <b>{mit['unpruned_train_macro_f1']:.4f}</b> but hold-out macro-F1 = <b>{mit['unpruned_test_macro_f1']:.4f}</b>, consistent with an overfitting gap. Cross-validation scores plateau while training fit increases at greater depth."),
 sub('9.2 Demonstration: early stopping via tree pre-pruning'),
 P(f"Select max_depth from the candidates [1, 2, 3, 4, 5, 7, unrestricted] using mean 5-fold macro-F1 on training data only, with simpler trees favored in a tie. The chosen depth is <b>{mit['selected_max_depth_using_cv']}</b>. The resulting train macro-F1 is <b>{mit['pruned_train_macro_f1']:.4f}</b> and hold-out macro-F1 is <b>{mit['pruned_test_macro_f1']:.4f}</b>."),
 tbl([['Model','Train macro-F1','Test macro-F1'],
 ['Unrestricted Decision Tree',f"{mit['unpruned_train_macro_f1']:.4f}",f"{mit['unpruned_test_macro_f1']:.4f}"],
 [f"Pre-pruned tree (depth {mit['selected_max_depth_using_cv']})",f"{mit['pruned_train_macro_f1']:.4f}",f"{mit['pruned_test_macro_f1']:.4f}"]],widths=[237,126,126]),
 P('The reported improvement is empirical for this one split; it is not a guarantee that tree pruning always improves held-out accuracy.','small'))
add(PageBreak())
add(heading('10. Overfitting Remedies by Algorithm &amp; Conclusions'),
 sub('10.1 Model-specific prevention strategies'),
 tbl([['Method family','Practical overfitting controls'],
 ['Logistic Regression / linear SVM','Increase regularization (reduce C), select relevant features, tune on CV'],
 ['kNN','Increase k when k=1 is noisy, scale inputs, tune k inside CV'],
 ['RBF SVM','Tune C and gamma using training folds; avoid unnecessarily complex boundaries'],
 ['Decision Tree','Limit max_depth, min_samples_leaf, min_samples_split, use cost-complexity pruning'],
 ['Random Forest / Extra Trees','Control maximum depth and leaf size; consider max_features and cross-validation'],
 ['Boosting','Lower learning rate, fewer stages, shallower weak learners, early stopping'],
 ['Naive Bayes / LDA / QDA','Inspect assumptions, regularize covariance estimates where appropriate']],
 widths=[169,320]),
 sub('10.2 Synthesis of the two exam questions'),
 P('Question 1 demonstrates analytic gradients, correct batch Gradient Descent implementation and finite-difference verification. Regression predicts numeric targets with squared-error loss; binary Logistic Regression predicts probabilities using cross-entropy. Their performance was measured on untouched held-out sets.'),
 P('Question 2 demonstrates reproducible data analysis and leakage-safe classification. Thirteen algorithms were evaluated under the same split and CV protocol. The Decision Tree complexity experiment shows why training performance alone is not a sufficient quality measure. Pre-pruning a tree by a training-only CV selection rule improved the observed held-out macro-F1 in this run.'),
 sub('10.3 Limitations and ethical considerations'),
 bullet('Both Q1 datasets are synthetic, so their success may not transfer to noisy real-world tasks.'),
 bullet('The Iris dataset is small and nearly separable; a 45-row held-out split yields high variability.'),
 bullet('The offline Iris copy was not fetched from OpenML live at execution; the corresponding OpenML ID is cited and the optional live-fetch path is supplied.'),
 bullet('Tree depth was tuned on training CV, but comparing many test scores in a report may invite post-hoc selection; use an independent final evaluation for deployment decisions.'),
 bullet('Data preprocessing and evaluated models should be tailored to data context; performance differences on Iris are not universal model rankings.'))
add(PageBreak())
add(heading('11. Reproducibility, Files &amp; References'),
 sub('11.1 Suggested procedure (from extracted project directory)'),
 P('1. Create a Python virtual environment and install required packages with <b>pip install -r requirements.txt</b>.'),
 P('2. Run <b>python -m src.q1_models</b> to regenerate both from-scratch optimizations, four plots and results/q1_metrics.json.'),
 P('3. Run <b>python -m src.q2_classification</b> to regenerate EDA, classifier benchmark, tree depth study, results tables, and JSON summary.'),
 P('4. Open the three Jupyter notebooks in the notebooks/ folder, or use <b>jupyter lab</b> from the project root. Notebook outputs have been precomputed and saved.'),
 P('5. For a direct OpenML download where the network is available, execute <b>python -m src.q2_classification --use-openml-live</b>. This flag intentionally errors if the download fails instead of silently claiming online provenance.'),
 sub('11.2 Saved data and evidence'),
 tbl([['Path','Contents'],['data/iris_openml_61_offline_mirror.csv','150-row offline Fisher Iris mirror; one exact duplicate removed during cleaning'],
 ['results/q1_metrics.json','Actual held-out metrics, learning curves summary and numerical gradient checks'],
 ['results/q2_model_comparison.csv','13-model CV and held-out comparison'],
 ['results/q2_tree_depth_study.csv','Depth-versus-training/CV macro-F1 experiment'],
 ['results/q2_summary.json','Cleaning, champion, confusion matrix and mitigation metadata'],
 ['figures/*.png','Saved visual evidence corresponding to plots in this PDF'],
 ['src/*.py','Runnable training programs without hidden external dependencies']],widths=[210,279]),
 sub('11.3 References'),
 P('[1] OpenML, <i>iris</i> (dataset ID 61, version 1), https://www.openml.org/d/61. Accessed October 2026.','small'),
 P('[2] OpenML Documentation, <i>Datasets / Download a dataset</i>, https://docs.openml.org/examples/20_basic/simple_datasets_tutorial/.','small'),
 P('[3] R. A. Fisher (1936), <i>The Use of Multiple Measurements in Taxonomic Problems</i>, Annals of Eugenics 7(2), 179-188.','small'),
 P('[4] scikit-learn documentation, <i>Dataset loading / load_iris; Pipeline and cross-validation</i>, https://scikit-learn.org/stable/.','small'),
 P('Implementation details, seeds, metric definitions, source code, and saved numerical results are supplied in the companion ZIP archive.','small'))

class NumberCanvas(canvas.Canvas):
 def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self._state=[]
 def showPage(self):self._state.append(dict(self.__dict__));self._startPage()
 def save(self):
  n=len(self._state)
  for state in self._state:
   self.__dict__.update(state);self.draw_page_num(n);super().showPage()
  super().save()
 def draw_page_num(self,n):
  self.setStrokeColor(C_LINE); self.setLineWidth(.7)
  self.line(44,45,A4[0]-44,45)
  self.setFont('Lato',8);self.setFillColor(C_MUTED)
  self.drawString(44,32,'INTRODUCTION TO MACHINE LEARNING  |  MIDTERM PROJECT')
  self.drawRightString(A4[0]-44,32,f'{self._pageNumber} / {n}')
  if self._pageNumber>1:
   self.setFont('LatoBold',8);self.setFillColor(C_BLUE)
   self.drawString(44,A4[1]-35,'MACHINE LEARNING / EXPERIMENTAL REPORT')

output.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=58,bottomMargin=58,title='Machine Learning Midterm - Models, Derivations, Experiments',author='Course Project Submission',subject='Q1 Regression from scratch; Q2 OpenML Iris Classification')
doc.build(story,canvasmaker=NumberCanvas)
print('PDF_CREATED',output,output.stat().st_size)
