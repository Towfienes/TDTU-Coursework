"""Build the N4 review report from the executed notebook's exported evidence."""
from pathlib import Path
import json,sys
from copy import deepcopy
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_layout import Report
ROOT=Path(__file__).resolve().parents[1]
S=json.loads((ROOT/'results/summary.json').read_text());M=json.loads((ROOT/'project.json').read_text())
sys.path.insert(0,str(ROOT))
from src.submission import readiness_issues
READY=not readiness_issues(M)
M['submission_ready']=READY
R=Report(ROOT,M)
fmt=lambda n,d=3:f'{n:.{d}f}'
def pv(n):return f'{n:.2e}' if n<.001 else f'{n:.4f}'
def paras(*items):
    for value in items:R.para(value)
def h(s):return R.heading(s,2)
def chapter(n,s):R.heading(f'CHAPTER {n}. {s}',new_page=n>1)
def names():
    p=R.para(M['report_date'],first=False);p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    for run in p.runs:run.italic=True
    p=R.para('Authors',first=False);p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    for run in p.runs:run.italic=True
    for a in M['authors']:
        p=R.para(a['name'],first=False);p.alignment=WD_ALIGN_PARAGRAPH.RIGHT

def mr(s):
    e=OxmlElement('m:r');pr=OxmlElement('w:rPr');font=OxmlElement('w:rFonts');font.set(qn('w:ascii'),'Cambria Math');font.set(qn('w:hAnsi'),'Cambria Math');pr.append(font);e.append(pr)
    t=OxmlElement('m:t');t.text=s;e.append(t);return e

def sub(base,index):
    e=OxmlElement('m:sSub')
    for tag,text in [('e',base),('sub',index)]:x=OxmlElement('m:'+tag);x.append(mr(text));e.append(x)
    return e

def frac(a,b):
    e=OxmlElement('m:f')
    for tag,text in [('num',a),('den',b)]:x=OxmlElement('m:'+tag);x.append(mr(text));e.append(x)
    return e

def eq(*parts):
    p=R.para('',first=False);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(5)
    e=OxmlElement('m:oMath')
    for part in parts:e.append(mr(part) if isinstance(part,str) else part)
    p._p.append(e)

R.cover();R.cover(True)
R.new_numbered_section('lowerRoman',1,size=12)
R.title('ACKNOWLEDGEMENT')
paras('We thank our advisor, Ho Thi Linh, Ph.D., for the course framework in Data Analysis and Visualization. This theory endterm report connects exploratory analysis, probability distributions, hypothesis tests, correlation and multiple linear regression through one documented public dataset.',
      'We acknowledge Nash, Sellers, Talbot, Cawthorn and Ford for the original abalone study and the UCI Machine Learning Repository for making the dataset and its codebook available. The analysis uses public measurements; the group does not claim to have conducted the biological fieldwork.',
      'OpenAI Codex assisted with code and document preparation. The student authors must verify the findings, understand the statistical reasoning, and comply with the lecturer’s requirements for attribution and assistance. The separate review checklist records the checks performed and the submission information still awaiting confirmation.')
names();R.doc.add_page_break();R.title('DECLARATION OF AUTHORSHIP')
paras('This report attributes its public dataset and external methods to the cited sources. Numerical results are produced by the accompanying executed Python notebook. The original source is preserved, and all transformations, splits and reported model evaluations are traceable.',
      'We distinguish exploratory association, statistical inference and predictive evaluation. We do not interpret observational differences as causal effects. No value was changed to improve a p-value or holdout metric; potentially influential observations are retained in the primary regression and examined separately.',
      ('The group has confirmed dataset registration, the published report video and individual contribution records. No signatures have been generated on behalf of the authors.' if READY else 'This review copy does not certify a completed video or actual personal contribution percentages. Those facts must be confirmed by the group before submission. No signatures or completion records have been generated on behalf of the authors.'))
R.para('The student authors remain responsible for checking the final content and accurately reporting their work.',True);names()
R.new_numbered_section('lowerRoman',None,size=13)
R.index_placeholder('TOC','TABLE OF CONTENT');R.doc.add_page_break();R.index_placeholder('LOF','LIST OF FIGURES');R.doc.add_page_break();R.index_placeholder('LOT','LIST OF TABLES')
R.new_numbered_section('decimal',1)
chapter(1,'INTRODUCTION AND DATASET')
h('1.1 Questions and analytical scope')
paras('This project investigates how recorded physical measurements and specimen groups relate to abalone shell rings. The application is useful because determining rings directly requires cutting and examining the shell, whereas some external measurements are easier to obtain. The full dataset also includes dissected component weights; the full model is therefore not described as a completely nondestructive measurement procedure.',
      'Four questions organize the analysis: how are the measurements and rings distributed; how do the recorded groups differ; which measurements are most strongly associated with Rings; and how much predictive improvement does multiple linear regression provide over a mean baseline? The six assignment components are mapped to executable evidence in REQUIREMENTS.md.',
      ('The report includes the published video link and group-confirmed contribution records. Each student remains responsible for their own submission.' if READY else 'The report is a review copy pending the actual video link and group-confirmed contribution records. Analytical results are complete enough to review; this status does not mean that the external submission requirements have been completed.'))
h('1.2 Source and measurement dictionary')
paras('Nash et al. (1994) provide Abalone through the UCI Machine Learning Repository, DOI 10.24432/C55C7W, under CC BY 4.0. The downloaded archive contains abalone.data and abalone.names. The retained raw file has 4,177 observations and nine columns: eight original inputs and the integer response Rings. It is different from the Sentiment140 midterm data and the Student Performance practical endterm data.',
      'The source states that continuous measurements were divided by 200. We preserve the stored values and label them as scaled measurements rather than silently assigning physical millimetres or grams. Sex is the source variable name, with M (male), F (female) and I (infant); I is a developmental category, not a third biological sex. Source age is approximately Rings + 1.5 years, so that derived age must never be used as an input to predict Rings.',
      'The original field study predates the repository entry. Its rows do not include site, batch or repeated-specimen identifiers. We cannot establish independence across ecological sampling units or evaluate generalization to new sites from these columns alone. Missing examples had already been removed by the source, which can introduce selection bias.')
R.table(['Stored columns','Role and interpretation'],[
 ['sex','Nominal M/F/I; F is the regression reference'],['length, diameter, height','Scaled shell dimensions; height zero is invalid'],['whole_weight','Scaled whole-specimen weight'],['shucked_weight, viscera_weight, shell_weight','Scaled component weights; some require dissection'],['rings','Integer ring count; response, not an exact age']], '1.2.1','Variables retained from the UCI source',[6.4,9.1])
h('1.3 Reproducibility and analysis design')
paras(f"A stratified random split with seed 42 assigns {S['train_n']:,} observations to training and {S['test_n']:,} to testing. The source-row indices are saved. Detailed descriptions, distribution assessments, hypothesis tests and model development use training observations; test measurements do not guide model selection, imputation, scaling or outlier deletion. Initial source inspection was limited to schema and obvious quality issues.",
      'The notebook exports tables, figures and a hash manifest. Document builders reuse those results. The analysis runs offline in a locked environment; six numerical boundary tests, one submission-metadata test and the verifier check calculations, split separation and artifacts.')
chapter(2,'DATA QUALITY AND EXPLORATORY ANALYSIS')
h('2.1 Structural inspection and cleaning')
paras('The notebook displays the first and last rows, dtype summaries and DataFrame.info(). The raw file contains zero missing cells and zero exact duplicate rows. The two source rows with Height = 0 have zero-based indices 1257 and 3996. A zero physical thickness is treated as an invalid measurement: only those height cells become NaN; the records remain in the data.',
      'Both affected rows occur in this training split. Descriptions involving height therefore have n = 3,339; most other descriptions have n = 3,341. Descriptive and correlation calculations omit invalid heights pairwise. Regression fills missing heights with a median learned separately inside each training fold. No artificial missingness is added and no test statistic is used to define this quality rule.')
h('2.2 Descriptive statistics and graphical choices')
rows=[]
for col in ['length','diameter','height','whole_weight','shell_weight','rings']:
 d=S['descriptive'][col];rows.append([col,int(d['count']),fmt(d['mean']),fmt(d['std']),fmt(d['25%']),fmt(d['50%']),fmt(d['75%'])])
R.table(['Variable','n','Mean','SD','Q1','Median','Q3'],rows,'2.2.1','Training descriptive statistics in stored units',[3.5,1.1,2.1,2.1,2.1,2.3,2.3])
paras('Histograms show the shape and tails without hiding the integer nature of Rings. KDE is a smooth visual aid for continuous measurements, not proof of a probability family. Boxplots compare medians and spread across groups, while group summaries retain sample sizes. Scatterplots later examine whether relationships are approximately linear. These complementary choices answer different questions rather than repeat one chart style.')
R.figure('01_eda_distributions.png','2.2.1','Training distributions of length, weight, height and rings')
paras('Length and weight are not automatically normal merely because they are physical measurements. The mixture of infant and adult specimens can create distributional asymmetry. The response is a discrete count with a right tail, and the height distribution includes unusual large observations that need influence checks rather than silent repair.')
R.figure('02_group_boxplots.png','2.2.2','Length and Rings across recorded groups with sample counts')
h('2.3 Outlier identification and treatment rationale')
paras('The 1.5×IQR rule flags values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR, using training quartiles. It is a screening rule, not a biological validity criterion. A large shell or an old specimen may be genuine. Because the source does not identify corrections, the primary model retains flagged observations; only the two impossible zero heights are treated as missing.',
      'An accompanying CSV preserves every flagged training row and the columns responsible. The regression section examines Cook’s distance, which measures influence on a fitted model rather than marginal extremeness. Comparing these concepts prevents the automatic deletion of rare but valid specimens.')
R.table(['Variable','IQR flags','Percent'],[[k,int(v['flagged_count']),fmt(v['percent'],2)+'%'] for k,v in S['iqr_counts'].items()],'2.3.1','Univariate training outlier flags without automatic deletion',[7,4,4.5])
chapter(3,'PROBABILITY DISTRIBUTIONS')
h('3.1 Candidate families and theory')
paras('A Normal distribution is symmetric about its mean μ and has scale σ. A positive random variable W is Lognormal when log(W) is Normal. The log transformation changes the shape and interpretation: normality of log weight does not imply normality of weight. We prespecify Length/Normal, Weight/Normal and Weight/Lognormal, covering two scientifically relevant measurements.',
      'A distribution family is an approximation to a measurement process. Pooling developmental groups, rounding and source selection can make a simple family inadequate. The task is to assess fit and explain discrepancies, rather than force a familiar family onto the data.')
eq('f(x) = ',frac('1','σ√(2π)'),' exp(−(x − μ)² / (2σ²))')
eq('W is Lognormal ⇔ log(W) is Normal(μ, σ²)')
h('3.2 Fitted parameters and goodness of fit')
paras('Each Anderson–Darling goodness-of-fit test uses 1,999 Monte Carlo replicates and refits unknown location and scale to every simulated sample. This accounts for parameter estimation; a plain fixed-parameter Kolmogorov–Smirnov calibration after estimating parameters from the same sample would be inappropriate. Normality of log weight provides the specified location-zero Lognormal assessment.',
      'The three distribution p-values are adjusted by Holm. With 1,999 replicates, the smallest estimable Monte Carlo p-value is 1/2,000 = 0.0005. A value at this floor does not measure how far below 0.0005 the underlying probability might be. Recorded rounding also limits an exact continuous-family interpretation.')
R.table(['Candidate','μ or log μ','σ or log σ','AD','p Holm'],[[r['hypothesis'],fmt(r['mu'],4),fmt(r['sigma'],4),fmt(r['ad'],3),fmt(r['p_holm'],4)] for r in S['distribution']],'3.2.1','Distribution assessments on 3341 training observations',[5.1,2.6,2.6,2.4,2.8])
paras('All three candidate families are rejected at α = 0.05 after Holm adjustment (adjusted p = 0.0015 for each). These equal p-values result from the simulation floor, not identical discrepancies. Length/Normal has AD 29.399, Weight/Normal 16.473 and log Weight/Normal 86.506. The two variables do not follow the proposed simple families exactly; no additional families are searched to obtain a favorable result.')
h('3.3 Visual evidence and implications')
R.figure('03_length_distribution.png','3.3.1','Length histogram with fitted Normal density and Normal Q–Q plot')
paras('The Q–Q plot compares observed quantiles with theoretical Normal quantiles; systematic curvature indicates departures in shape or tails. The histogram and fitted density help interpret the departure in the original stored measurement scale. A small p-value is interpreted with this visual evidence, rather than as a practical effect size.')
R.figure('04_weight_distribution.png','3.3.2','Weight and log weight against Normal and Lognormal candidates')
paras('Log transformation does not resolve every departure for these mixed specimens. Rejection of a marginal distribution does not automatically prohibit all mean comparisons or OLS predictions: those methods have their own sampling and conditional-error assumptions. Later diagnostics address unequal group variability and nonconstant regression residual variance directly.')
chapter(4,'HYPOTHESIS TESTING')
h('4.1 Tests and assumptions')
paras('For the first question, H0 is equality of mean Rings between M and F; H1 is a nonzero difference. Welch’s two-sample t-test uses separate variance estimates and Satterthwaite degrees of freedom. It avoids assuming equal group variances but still assumes appropriately independent observations. The reported difference is M minus F, with an unadjusted 95% confidence interval.')
eq('t = ',frac('mean(M) − mean(F)','√(s²(M)/n(M) + s²(F)/n(F))'))
paras('For the second question, H0 is independence of recorded group and ring band; H1 is association. Expected counts satisfy Eij = row total × column total / n. Pearson’s chi-square statistic has (r−1)(c−1) degrees of freedom under the large-sample approximation. Cramér’s V summarizes association magnitude. The historical bands 1–8, 9–10 and 11+ appear in the retained codebook; they are not claimed to be validated biological age categories.')
eq('χ² = Σ ',frac('(observed − expected)²','expected'))
paras('For the third question, H0 is equality of mean Length across F/I/M; H1 is that at least one mean differs. Classical one-way ANOVA divides between-group mean square by within-group mean square and assumes common error variance. Welch ANOVA instead uses inverse-variance weights and adjusted degrees of freedom. We use Welch as primary and report classical ANOVA as a methodological comparison.')
eq('F classical = ',frac('MS between groups','MS within groups'))
paras('The three primary hypotheses form one family, controlled with Holm at α = 0.05. Holm compares ordered p-values to α/(m−i+1), producing adjusted p-values without assuming test independence. The distribution-fit family is separate. Very small p-values do not prove a large effect or a causal mechanism; sampling independence and representativeness remain unverified.')
h('4.2 Primary results and effect interpretation')
R.table(['Test','Statistic','df','p Holm'],[
 ['Welch t: Rings M−F',fmt(S['welch']['statistic']),fmt(S['welch']['df'],1),pv(S['hypotheses'][0]['p_holm'])],
 ['χ²: group × band',fmt(S['chi']['statistic']),'4',pv(S['hypotheses'][1]['p_holm'])],
 ['Welch F: Length',fmt(S['anova']['F']),f"2, {fmt(S['anova']['df_den'],1)}",pv(S['hypotheses'][2]['p_holm'])]],'4.2.1','Primary tests with Holm correction across three questions',[5.9,2.7,3.4,3.5])
w=S['welch'];c=S['chi'];a=S['anova']
paras(f"M minus F mean Rings is {fmt(w['difference'])} rings, with 95% CI [{fmt(w['ci_low'])}, {fmt(w['ci_high'])}]. Adjusted p = {pv(S['hypotheses'][0]['p_holm'])}. This is evidence of a sample mean difference, but the magnitude is modest relative to the individual variability in rings; no sex-specific aging mechanism is identified.",
      f"The group-by-band chi-square statistic is {fmt(c['statistic'])}, with minimum expected count {fmt(c['min_expected'],1)}. All expected counts exceed five, so the standard approximation is adequate and the Monte Carlo fallback is not needed here. Cramér’s V = {fmt(c['cramers_v'])} gives the magnitude of categorical association. Infant status partly reflects development, so the association is not surprising or evidence of a new causal discovery.",
      f"Welch ANOVA gives F = {fmt(a['F'])} and adjusted p = {pv(S['hypotheses'][2]['p_holm'])}. The descriptive classical η² = {fmt(a['eta_squared_descriptive'])} expresses the share of sample Length variation between groups; it is not the Welch test statistic or a causal explained fraction. Median-based Levene p = {pv(a['levene_p'])} supports avoiding a common-variance assumption. Classical F = {fmt(a['classic_F'])} is reported for comparison, not substituted after viewing results.")
h('4.3 Group patterns and follow-up comparisons')
R.figure('05_hypothesis_groups.png','4.3.1','Ring-band shares and mean Length with unadjusted 95 percent intervals')
paras('The stacked bars show percentages within each recorded group, preventing unequal sample sizes from being mistaken for differences in composition. The mean plot includes uncertainty for each group; its confidence intervals are descriptive marginal intervals, not simultaneous post-hoc intervals.')
R.table(['Length pair','Difference','95% CI','p Holm'],[[r['comparison'],fmt(r['difference'],4),f"[{fmt(r['ci_low'],4)}, {fmt(r['ci_high'],4)}]",pv(r['p_holm'])] for r in S['posthoc']],'4.3.1','Conditional post-hoc Welch comparisons after the omnibus rejection',[3.1,3.3,5.5,3.6])
h('4.4 Scope of inference')
paras('All pairwise comparisons follow the adjusted omnibus rejection and receive a separate Holm correction; their 95% intervals are unadjusted. Missing site identifiers prevent checking ecological independence. Welch and Holm do not remove this sampling limitation; conclusions apply to this dataset pending external validation.')
chapter(5,'CORRELATION ANALYSIS')
h('5.1 Pearson and Spearman theory')
paras('Pearson correlation measures linear association using centered products. It is sensitive to extreme values and need not capture a nonlinear but monotonic relationship. Spearman correlation applies Pearson’s calculation to average ranks, which handles ties in the discrete Rings response. A shortcut rank formula without tie corrections is therefore not used.',
      'Both coefficients range from −1 to 1. Correlation is symmetric and does not estimate an intervention or a conditional regression effect. Recorded group is nominal, so M/F/I is not encoded as an ordered 0/1/2 variable for these matrices. Source indexes and outcome-derived age are excluded.')
eq('r = ',frac('Σ(x − mean x)(y − mean y)','√[Σ(x − mean x)² Σ(y − mean y)²]'))
eq('ρ = correlation(rank(X), rank(Y))')
h('5.2 Matrices and pairwise sample sizes')
R.figure('06a_pearson_heatmap.png','5.2.1','Pearson correlations among the original numerical variables',max_height=12)
R.figure('06b_spearman_heatmap.png','5.2.2','Spearman rank correlations among the original numerical variables',max_height=12)
paras('The diverging color scale is centered on zero with limits −1 to 1, so colors remain comparable across matrices. Pairwise counts are exported. Pairs involving Height use n = 3,339; other pairs use n = 3,341. Visual interpretation is supported by the tabulated values rather than the heatmap colors alone.')
R.table(['Measurement','Pearson r','Spearman ρ','n'],[[k,fmt(v['pearson']),fmt(v['spearman']),int(v['n'])] for k,v in S['correlations'].items()],'5.2.1','Original measurements associated with Rings on training data',[6.2,3.2,3.2,2.9])
h('5.3 Practical interpretation and collinearity')
R.figure('07_relationships.png','5.3.1','Shell weight and length versus Rings and shared size information')
paras('Shell weight has the largest marginal rank association with Rings among the examined original numeric measurements (ρ = 0.693, Pearson r = 0.628). That is an association ranking, not model feature importance. The stronger rank coefficient is consistent with a monotonic relationship that is not perfectly linear and includes discrete response ties.',
      'Size and weight variables overlap, making joint slopes unstable. High marginal correlations can coexist with negative or imprecise conditional slopes. Regression and VIF diagnostics assess this issue; correlation p-values do not select predictors.')
chapter(6,'MULTIPLE LINEAR REGRESSION')
h('6.1 Model theory and feature definitions')
paras('Multiple linear regression models the conditional mean of Rings as an intercept plus a sum of feature contributions. Ordinary least squares minimizes the sum of squared residuals. Numeric predictors are median-imputed and standardized using the training sample only. Dummy variables for I and M use F as reference; the infant coefficient remains an adjusted association, not a causal sex effect.')
eq(sub('Rings','i'),' = β₀ + Σ ',sub('β','j'),sub('x','ij'),' + ',sub('ε','i'))
eq('OLS objective = min β Σ (observed rings − predicted rings)²')
paras('The compact model uses group, length, diameter, height and whole weight. The full model adds shucked, viscera and shell weights, using all eight original inputs. The baseline predicts the mean Rings of the training sample. The feature sets and fivefold design were fixed before holdout evaluation; the goal is to quantify the cost and predictive value of additional measurements.',
      'Linearity concerns the conditional mean given predictors, not the marginal normality of each predictor. Normal residual assumptions support some classical inferential statements, while prediction can still be evaluated empirically under departures. HC3 standard errors allow heteroskedasticity in the coefficient covariance calculation; they do not cure nonlinear mean structure, influential errors or unobserved clustering.')
h('6.2 Leakage control and cross validation')
paras('Every fold fits imputation, scaling, dummy encoding and regression on its inner-training observations. The validation fold is transformed using that fitted preprocessing. The five folds are identical for baseline, compact and full models. CV mean/SD describes variability across these folds; it is not a confidence interval based on independent repeated experiments.')
rows=[]
for name in ['Baseline','Compact','Full']:
 vals=[r for r in S['cv'] if r['model']==name]
 import statistics
 rows.append([name,*[f"{fmt(statistics.mean(r[k] for r in vals))} ± {fmt(statistics.stdev(r[k] for r in vals))}" for k in ['mae','rmse','r2']]])
R.table(['Model','MAE mean ± SD','RMSE mean ± SD','R² mean ± SD'],rows,'6.2.1','Fivefold training cross validation with shared folds',[3.1,4.1,4.2,4.1])
h('6.3 Final holdout evaluation')
R.table(['Model','MAE','RMSE','R²','Outside 1–29'],[[r['model'],fmt(r['mae']),fmt(r['rmse']),fmt(r['r2']),r['outside_1_29']] for r in S['test_metrics']],'6.3.1','Final evaluation of prespecified models on 836 held out records',[3.2,2.7,2.7,2.7,4.2])
baseline,compact,full=S['test_metrics'];improvement=(baseline['rmse']-full['rmse'])/baseline['rmse']*100
paras(f"Full-model test RMSE is {fmt(full['rmse'])} rings compared with {fmt(baseline['rmse'])} for the mean baseline, a reduction of {fmt(improvement,1)}%. Test MAE is {fmt(full['mae'])} rings, and R² = {fmt(full['r2'])}. Additional component weights improve this prespecified comparison over the compact model, but they also change the measurement effort required.",
      'Predictions remain continuous when metrics are computed. The full model has one prediction outside the observed Rings range 1–29; values are neither rounded nor clipped to improve scores. The ideal-line scatter exposes systematic error and large misses, and R² below one confirms that these measurements do not determine Rings exactly.')
R.figure('09_holdout_evaluation.png','6.3.1','Observed and predicted test rings and comparison with the mean baseline')
h('6.4 Coefficients and model diagnostics')
R.table(['Term','Scaled slope','HC3 95% CI'],[[r['term'],fmt(r['coefficient']),f"[{fmt(r['ci_low'])}, {fmt(r['ci_high'])}]" ] for r in S['coefficients']],'6.4.1','Full model coefficients with heteroskedasticity robust intervals',[5.8,3.3,6.4])
paras('Numeric coefficients represent a one-training-SD increase in the imputed measurement, with other predictors held fixed. Dummy coefficients represent shifts relative to F, and the intercept refers to F at the training means of the numeric variables. The stored-unit coefficient table and numerical prediction identity are exported, so the formula can be checked without confusing standardized and original scales.',
      'Large VIF values identify redundant information; they do not by themselves invalidate predictions. Conditional coefficient signs can differ from marginal correlations because overlapping dimensions and component weights compete to explain the same variation. These intervals are model-based, were not corrected for simultaneous coefficient comparisons and should not be interpreted as evidence of independent causal mechanisms.')
R.table(['Term','VIF'],[[r['term'],fmt(r['VIF'],2)] for r in S['vif']],'6.4.2','Variance inflation factors from the training design',[9.5,6])
R.figure('08_regression_diagnostics.png','6.4.1','Training residual patterns and Cook influence diagnostics')
d=S['diagnostics']
paras(f"The full design has rank {d['rank']} of {d['design_columns']}, so it is not exactly singular. Breusch–Pagan LM = {fmt(d['bp_lm'])}, p = {pv(d['bp_p'])}, indicating nonconstant residual variance under the test assumptions. Q–Q and residual plots also reveal where Normal-error or linear-mean approximations are limited. HC3 covariance is used for reported coefficient intervals, while test prediction metrics remain direct empirical summaries.")
h('6.5 Influence sensitivity and limits')
paras(f"Cook’s distance above 4/n flags {d['cook_flagged']} training observations. The primary model retains them. For sensitivity only, each inner-training fold fits an initial model, screens its own influence, refits preprocessing and regression on retained inner-training rows, and predicts the unchanged validation fold. The validation and test observations never participate in deciding which training records to remove.")
R.table(['Fold','Train before','Removed','Validation n','RMSE'],[[r['fold'],r['training_before'],r['removed'],r['validation_n'],fmt(r['rmse'])] for r in S['sensitivity']],'6.5.1','Training only influence sensitivity with unchanged validation folds',[1.5,3.5,3,3.8,3.7])
paras('The coefficient-sensitivity CSV compares slopes in stored units, because standardization changes after deleting observations. Comparing standardized slopes without accounting for different scalers would be misleading. Sensitivity results are reported as a stability check, not used to replace the primary model after viewing holdout errors.',
      'A random holdout from the same source does not measure temporal or geographic transportability. More measurements, nonlinear structure or site-aware validation could improve future studies, but those extensions are outside the present linear-regression assignment. Neither a good RMSE nor a small p-value demonstrates a biological cause.')
chapter(7,'CONCLUSIONS AND CONTRIBUTIONS')
h('7.1 Answers to the research questions')
paras('The training measurements show asymmetric distributions and differences between developmental groups. The proposed Normal and Lognormal families are rejected under the stated Monte Carlo checks. This is a substantive distributional result, not a failure to execute the assignment.',
      'Recorded groups differ in mean Rings and Length, and their ring-band composition is associated. The M−F mean difference is about −0.355 rings, which should be considered alongside its interval and individual variation. Infant status and historical sampling qualify interpretation.',
      f"Shell weight has the strongest examined marginal rank association with Rings, while related size and weight variables are collinear. The full linear model improves test RMSE by {fmt(improvement,1)}% relative to the mean baseline, with MAE about {fmt(full['mae'],2)} rings. Residual diagnostics, coefficient sensitivity and an out-of-range prediction limit how confidently it should be used for individual specimens.")
h('7.2 Limitations and responsible use')
paras('The public source had already excluded missing examples; observations are historical and lack site/batch IDs. Measurements were scaled, and two invalid heights required a documented rule. Distribution tests assume continuous families despite rounded values. Group comparisons are unadjusted, multiple outcomes share measurements, and ecological dependence cannot be checked.',
      'The predictive objective is ring count, not a validated determination of exact age. Extrapolation to other species, measurement protocols or regions requires new data. A practical use would report prediction uncertainty and cost of additional measurements rather than present the fitted equation as a definitive age instrument.')
h('7.3 Contribution and submission confirmation')
paras('The lecturer requires actual tasks, contribution percentages and completion levels for every student, as well as a real video link on slide 2. These records cannot be inferred from authorship order or automatically assigned. '+('The following records have been confirmed by the group.' if READY else 'The user requested a proposed allocation of roles and shares. The table labels these as proposed; completion and actual work still require group verification.'))
R.table(['Student','ID','Task / contribution / completion'],[[a['name'],a['id'],f"{a['tasks']}; contribution {a['contribution_percent']}%; completion {a['completion_percent']}%" if READY else f"{a['proposed_tasks']}; proposed {a['proposed_contribution_percent']}%; completion pending"] for a in M['authors']],'7.3.1','Contribution records confirmed by the group' if READY else 'Proposed roles and shares pending verification of actual work',[5.5,2.6,7.4])
if READY:R.para('Published report video: '+M['youtube_url'],first=False)
paras('The video script targets 12 minutes within the required 7–15 minutes. Dataset acceptance has been confirmed by the user. The group must record and publish the video, provide the actual YouTube URL and finalize contributions. Video submission is due by the end of 21 October 2026; report/code are due at 23:55 on 22 October 2026, Vietnam time. Each member submits a ZIP named with their own student ID.')
R.doc.add_page_break();R.title('REFERENCES')
for text in [
 'Nash, W., Sellers, T., Talbot, S., Cawthorn, A., & Ford, W. (1994). Abalone [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55C7W. CC BY 4.0. Original codebook retained with the project.',
 'SciPy developers. (2025). SciPy 1.15.3 documentation: goodness_of_fit, ttest_ind and chi2_contingency. https://docs.scipy.org/doc/scipy-1.15.3/reference/stats.html. Accessed 20 October 2026.',
 'Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference. https://www.statsmodels.org/. Documentation consulted for Welch ANOVA, HC3 covariance, influence and VIF.',
 'Scikit-learn developers. (2025). Scikit-learn 1.6 documentation: pipelines, preprocessing, cross validation and common pitfalls. https://scikit-learn.org/1.6/common_pitfalls.html. Accessed 20 October 2026.',
 'Matplotlib and Seaborn developers. Documentation for histogram, boxplot, regression plot and heatmap visualization. https://matplotlib.org/stable/ and https://seaborn.pydata.org/. Accessed 20 October 2026.'
]:
 p=R.para(text,first=False);p.alignment=WD_ALIGN_PARAGRAPH.LEFT;p.paragraph_format.left_indent=__import__('docx').shared.Cm(1.27);p.paragraph_format.first_line_indent=__import__('docx').shared.Cm(-1.27);p.paragraph_format.space_after=Pt(8)
R.finalize_indexes()
(ROOT/'.build').mkdir(exist_ok=True)
R.doc.save(ROOT/'.build/report_draft.docx')
(ROOT/'.build/report_index.json').write_text(json.dumps(R.entries+R.figures+R.tables,indent=2)+'\n')
print('Built review report:',len(R.figures),'figures;',len(R.tables),'tables;',len(R.entries),'TOC headings. References excluded.')
