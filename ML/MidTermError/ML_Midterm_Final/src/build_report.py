"""Build the English academic report exclusively from executed result files."""

from pathlib import Path
import hashlib
import json
import re
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether,
)

ROOT = Path(__file__).resolve().parents[1]
NAVY = "#111111"
TEAL = "#222222"
GRAY = "#555555"


class NumberCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("initialFontName", "Times")
        super().__init__(*args, **kwargs)
        self.states = []

    def showPage(self):
        self.states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self.states)
        for state in self.states:
            self.__dict__.update(state)
            self.setFont("Times", 7.5)
            self.setFillColor(colors.HexColor(GRAY))
            self.drawString(48, 30, "THE LEARNING CURVE  /  MACHINE LEARNING MIDTERM")
            self.drawRightString(A4[0] - 48, 30, f"{self._pageNumber} / {total}")
            if self._pageNumber > 1:
                self.setFillColor(colors.HexColor(GRAY))
                self.drawString(
                    48, A4[1] - 34, "OPTIMIZATION  /  CLASSIFICATION  /  GENERALIZATION"
                )
            super().showPage()
        super().save()


def main(root=ROOT):
    source = root / "report/report_source"
    fonts = source / "fonts"
    for alias, file in [
        ("Times", "Times.ttf"),
        ("TimesBold", "Times-Bold.ttf"),
        ("TimesItalic", "Times-Italic.ttf"),
        ("TimesBoldItalic", "Times-BoldItalic.ttf"),
        ("Serif", "Times.ttf"),
        ("SerifBold", "Times-Bold.ttf"),
        ("SerifItalic", "Times-Italic.ttf"),
        ("SerifBoldItalic", "Times-BoldItalic.ttf"),
        ("Sans", "Times.ttf"),
        ("SansBold", "Times-Bold.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(alias, str(fonts / file)))
    pdfmetrics.registerFontFamily(
        "Times",
        normal="Times",
        bold="TimesBold",
        italic="TimesItalic",
        boldItalic="TimesBoldItalic",
    )
    pdfmetrics.registerFontFamily(
        "Serif",
        normal="Times",
        bold="TimesBold",
        italic="TimesItalic",
        boldItalic="TimesBoldItalic",
    )
    pdfmetrics.registerFontFamily(
        "Sans",
        normal="Times",
        bold="TimesBold",
        italic="TimesItalic",
        boldItalic="TimesBoldItalic",
    )
    styles = {
        "body": ParagraphStyle(
            "body",
            fontName="Times",
            fontSize=10.1,
            leading=15.5,
            textColor=colors.HexColor(NAVY),
            spaceAfter=9,
        ),
        "small": ParagraphStyle(
            "small",
            fontName="Times",
            fontSize=8.1,
            leading=12,
            textColor=colors.HexColor(GRAY),
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="TimesBold",
            fontSize=20,
            leading=25,
            textColor=colors.HexColor(NAVY),
            spaceAfter=17,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="TimesBold",
            fontSize=11,
            leading=16,
            textColor=colors.HexColor(TEAL),
            spaceBefore=8,
            spaceAfter=8,
        ),
        "title": ParagraphStyle(
            "title",
            fontName="TimesBold",
            fontSize=30,
            leading=38,
            textColor=colors.HexColor(NAVY),
            spaceAfter=20,
        ),
        "sub": ParagraphStyle(
            "sub",
            fontName="Times",
            fontSize=13,
            leading=20,
            textColor=colors.HexColor(TEAL),
            spaceAfter=17,
        ),
        "cell": ParagraphStyle(
            "cell",
            fontName="Times",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor(NAVY),
        ),
        "th": ParagraphStyle(
            "th", fontName="TimesBold", fontSize=8, leading=11, textColor=colors.white
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName="TimesItalic",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor(GRAY),
            spaceBefore=5,
            spaceAfter=13,
        ),
    }
    q1 = json.loads((root / "results/q1_metrics.json").read_text())
    lin = q1["linear"]
    log = q1["logistic"]
    q2 = json.loads((root / "results/q2_summary.json").read_text())
    chosen = q2["champion_metrics"]
    provenance = json.loads((root / "data/metadata/provenance.json").read_text())
    metadata = json.loads((source / "metadata.json").read_text())
    rank = pd.read_csv(root / "results/q2_model_comparison.csv")
    description = pd.read_csv(root / "results/q2_numeric_description.csv", index_col=0)
    story = []
    manuscript = []
    figure_manifest = []
    figure_number = 0

    def p(text, style="body"):
        manuscript.append(re.sub("<[^>]+>", "", str(text)))
        return Paragraph(str(text), styles[style])

    def add(*items):
        story.extend(items)

    def section(title):
        if story:
            add(PageBreak())
        manuscript.append("\n## " + title)
        add(p(title, "h1"))

    def table(headers, rows, widths):
        manuscript.append(" | ".join(headers))
        for row in rows:
            manuscript.append(" | ".join(map(str, row)))
        data = [[Paragraph(str(v), styles["th"]) for v in headers]] + [
            [Paragraph(str(v), styles["cell"]) for v in row] for row in rows
        ]
        t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#F6F6F6")],
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        return t

    def img(name, width):
        path = root / "figures" / name
        w, h = PILImage.open(path).size
        figure_manifest.append(
            dict(
                file="figures/" + name,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            )
        )
        return Image(str(path), width=width, height=width * h / w, hAlign="CENTER")

    def figure(name, caption, width=460):
        nonlocal figure_number
        figure_number += 1
        return KeepTogether(
            [img(name, width), p(f"Figure {figure_number}. " + caption, "caption")]
        )

    def equations(name, lines):
        manuscript.append("LaTeX: " + "; ".join(lines))
        plt.rcParams["mathtext.fontset"] = "stix"
        plt.rcParams["font.family"] = "STIXGeneral"
        fig, ax = plt.subplots(figsize=(9, 0.65 * len(lines)), dpi=300)
        ax.axis("off")
        for i, line in enumerate(lines):
            ax.text(
                0.015,
                1 - (i + 0.5) / len(lines),
                "$" + line + "$",
                fontsize=16,
                color=NAVY,
                va="center",
            )
        fig.subplots_adjust(left=0.015, right=0.99, bottom=0.01, top=0.99)
        fig.savefig(root / "figures" / name, facecolor="#FFFFFF")
        plt.close(fig)
        return img(name, 480)

    def paired(left, right):
        nonlocal figure_number
        figure_number += 2
        return Table(
            [[img(left, 238), img(right, 238)]],
            colWidths=[248, 248],
            style=[
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ],
        )

    # Cover uses a genuine Q1 training curve as the visual signature.
    add(
        Spacer(1, 35),
        p("INTRODUCTION TO MACHINE LEARNING", "sub"),
        p("MIDTERM<br/>EXAMINATION", "title"),
        p(metadata["subtitle"], "sub"),
        Spacer(1, 8),
        table(
            ["Group member", "Student ID"],
            [[m["name"], m["student_id"]] for m in metadata["members"]],
            [330, 166],
        ),
        Spacer(1, 10),
        p(metadata["identity_status"], "small"),
        p(
            "Group of three | Section: "
            + metadata["section"]
            + " | "
            + metadata["date"],
            "small",
        ),
        p("THE LEARNING CURVE", "h2"),
        figure(
            "q1_linear_loss.png",
            "Actual synthetic Linear Regression training objective; source: results/q1_arrays.npz.",
            310,
        ),
        p(
            "Question 1: NumPy implementations and verified analytical gradients.<br/>Question 2: official OpenML credit-g, leakage-safe classification and measured capacity control.",
            "body",
        ),
        p(
            metadata["version"]
            + " | Dataset fingerprint: "
            + provenance["raw_sha256"][:16],
            "small",
        ),
    )

    section("1  Objectives and experimental overview")
    add(
        p(
            "This report addresses the two equally weighted questions in the original Middle Exam. Question 1 derives and trains Linear Regression and binary Logistic Regression from first principles. Question 2 studies a classification dataset downloaded from OpenML, with preparation, model comparison and overfitting analysis."
        ),
        p(
            f"On synthetic held-out data, Linear Regression achieves RMSE {lin['rmse']:.4f} and R² {lin['r2']:.4f}; Logistic Regression achieves accuracy {log['accuracy']:.4f} and F1 {log['f1']:.4f}. On German Credit, five-fold development CV selects {q2['champion_selected_by_train_cv']} from 12 predefined learning algorithms. Its independent test accuracy is {chosen['test_accuracy']:.4f} and macro-F1 is {chosen['test_macro_f1']:.4f}."
        ),
        p(
            "Results are generated by executable scripts, not transcribed from the previous submission. Analytical gradients are tested on multiple shapes and seeds, then checked against independent numerical and library references. Official raw data, metadata, checksums, split indices, fold scores and test predictions are retained."
        ),
        p("Reading map", "h2"),
        table(
            ["Topic", "Location"],
            [
                [
                    "Linear Regression theory, implementation and evidence",
                    "Sections 2-4; Q1_Linear_Regression.ipynb",
                ],
                [
                    "Logistic Regression and probability evaluation",
                    "Sections 5-7; Q1_Logistic_Regression.ipynb",
                ],
                ["OpenML source, EDA and preprocessing", "Sections 8-10; src/data.py"],
                [
                    "Classifier comparison and final evaluation",
                    "Sections 11-13; Q2_Classification.ipynb",
                ],
                ["Overfitting, mitigation and limitations", "Sections 14-16"],
                [
                    "References and reproduction",
                    "Sections 17-18; README.md; verification/",
                ],
            ],
            [265, 231],
        ),
        p("Experimental boundaries", "h2"),
        p(
            "Synthetic Q1 tasks illustrate optimization under controlled conditions. The historical credit dataset is an educational benchmark. Neither establishes deployment validity or a guaranteed grade. Model selection uses development CV only; all candidate test results are descriptive and do not change the selected procedure."
        ),
    )

    section("2  Linear Regression and its gradient")
    add(
        p(
            "Regression predicts a continuous response; classification predicts a discrete label. With m observations and d features, X is an m by d matrix, w is a d-dimensional vector, b is a scalar intercept and y is an m-dimensional response. The affine prediction can represent a nonzero response when all features are zero."
        ),
        equations(
            "linear_derivation.png",
            [
                r"\hat y_i=\mathbf{x}_i^{\mathsf{T}}\mathbf{w}+b,\quad e_i=\hat y_i-y_i",
                r"J(\mathbf{w},b)=\frac{1}{2m}\sum_{i=1}^{m}e_i^2",
                r"\frac{\partial J}{\partial w_j}=\frac{1}{2m}\sum_i 2e_i\frac{\partial e_i}{\partial w_j}=\frac{1}{m}\sum_i e_i x_{ij}",
                r"\frac{\partial J}{\partial b}=\frac{1}{2m}\sum_i 2e_i\cdot 1=\frac{1}{m}\sum_i e_i",
                r"\nabla_{\mathbf{w}}J=\frac{X^{\mathsf{T}}(X\mathbf{w}+b\mathbf{1}-\mathbf{y})}{m}",
            ],
        ),
        p(
            "The chain rule connects the squared residual to each parameter through the prediction. The factor of one half cancels the derivative of the square. It rescales the loss, but does not change the least-squares minimizer. Reported MSE is twice this training objective."
        ),
        p("Why squared error?", "h2"),
        p(
            "MSE measures average squared prediction error and penalizes large residuals. Under independent Gaussian errors with constant variance, minimizing it also maximizes the likelihood of the linear mean model. This assumption is appropriate for the synthetic data-generating process here; it is not required merely to calculate an MSE."
        ),
        p(
            "The objective is convex because its Hessian is positive semidefinite. Convexity does not make every learning rate safe: steps that are too large can diverge. Rank-deficient inputs can admit multiple least-squares solutions; this experiment has independent features."
        ),
    )

    section("3  Batch Gradient Descent and verification")
    add(
        equations(
            "gd_updates.png",
            [
                r"\mathbf{w}_{t+1}=\mathbf{w}_t-\eta\nabla_{\mathbf{w}}J(\mathbf{w}_t,b_t)",
                r"b_{t+1}=b_t-\eta\frac{\partial J(\mathbf{w}_t,b_t)}{\partial b}",
            ],
        ),
        p(
            "Both parameters are updated from gradients computed at the same current parameters. Full-batch training uses every training record in each update. The implementation initializes weights and intercept to zero, so initialization is deterministic without a random draw."
        ),
        table(
            ["Step", "Implemented operation"],
            [
                [
                    "Validate",
                    "Require finite, nonempty (m,d) features and matching (m,) or (m,1) target; require positive learning rate and integer iterations.",
                ],
                ["Initialize", "Set w=0 and b=0; record the initial loss."],
                [
                    "Iterate",
                    "Compute loss and both gradients in NumPy; reject nonfinite values; apply simultaneous gradient updates.",
                ],
                [
                    "Monitor",
                    "Record every post-update loss and the final gradient norm; use fixed training iterations.",
                ],
                ["Predict", "Validate feature count, then compute Xw+b."],
            ],
            [94, 402],
        ),
        p("Independent finite differences", "h2"),
        equations(
            "finite_difference.png",
            [
                r"g_j^{\mathrm{FD}}=\frac{J(\theta+\epsilon\mathbf{e}_j)-J(\theta-\epsilon\mathbf{e}_j)}{2\epsilon},\quad\epsilon=10^{-6}"
            ],
        ),
        p(
            "The gradient test covers four seeds and four (m,d) shapes: (1,1), (7,1), (9,3), (5,6), for both models: 32 comparisons. Every maximum absolute error must be below 10<super>-7</super>. Moderate random parameters avoid saturation and excessively ill-scaled differences. Absolute tolerance is specified rather than an unstable relative error near zero."
        ),
        p(
            "Additional checks verify an explicit one-step update, the intercept, predictions, decreasing loss, extreme logits and deterministic fits. No scikit-learn optimizer trains the submitted scratch models. Library fits appear only as separately labeled validation benchmarks.",
            "small",
        ),
    )

    section("4  Linear Regression experiment")
    add(
        p(
            "Seed 42 generates 360 standard-normal feature pairs and y=4+3x1-2x2+Gaussian noise with standard deviation 0.65. A fixed 80/20 split gives 288 training and 72 test records. StandardScaler learns its mean and variance from training features only. Gradient Descent uses learning rate 0.08 and 1,200 updates."
        ),
        table(
            ["Measurement", "Executed result"],
            [
                [
                    "Training objective, initial / final",
                    f"{lin['train_loss_first']:.6f} / {lin['train_loss_last']:.6f}",
                ],
                ["MSE / RMSE", f"{lin['mse']:.6f} / {lin['rmse']:.6f}"],
                ["MAE / R²", f"{lin['mae']:.6f} / {lin['r2']:.6f}"],
                ["Final gradient norm", f"{lin['final_gradient_norm']:.3e}"],
                [
                    "Gradient check maximum absolute difference",
                    f"{lin['grad_check_max_abs_diff']:.3e}",
                ],
                [
                    "Maximum prediction difference from least squares",
                    f"{lin['reference_prediction_max_abs_diff']:.3e}",
                ],
            ],
            [310, 186],
        ),
        paired("q1_linear_predictions.png", "q1_linear_residuals.png"),
        p(
            "Figures 2-3. Held-out predictions and residuals use the same 72 test records. The diagonal is ideal prediction; the horizontal residual line is zero.",
            "caption",
        ),
        p(
            f"RMSE {lin['rmse']:.3f} is close to the injected noise standard deviation, while residual scatter shows the unavoidable random component. R² compares squared error with the test-mean baseline; it does not measure causal explanation. The high value is expected for this deliberately linear problem."
        ),
        p(
            "The independent reference uses sklearn LinearRegression least squares. Its predictions agree within 10<super>-8</super>, supporting successful optimization of this objective. This validation does not replace the from-scratch fitting loop."
        ),
    )

    section("5  Logistic Regression and cross-entropy")
    add(
        p(
            "Binary Logistic Regression models P(y=1|x). A linear logit z is transformed to probability p by the sigmoid. The default decision predicts label 1 when p is at least 0.5. Unlike Linear Regression, the output is constrained to a probability, while the decision boundary remains linear in the transformed features."
        ),
        equations(
            "logistic_derivation.png",
            [
                r"z_i=\mathbf{x}_i^{\mathsf{T}}\mathbf{w}+b,\quad p_i=\sigma(z_i)=\frac{1}{1+e^{-z_i}}",
                r"\ell_i=-y_i\log p_i-(1-y_i)\log(1-p_i),\quad J=\frac{1}{m}\sum_i\ell_i",
                r"\frac{\partial\ell_i}{\partial p_i}=-\frac{y_i}{p_i}+\frac{1-y_i}{1-p_i}=\frac{p_i-y_i}{p_i(1-p_i)}",
                r"\frac{\partial p_i}{\partial z_i}=p_i(1-p_i),\quad\frac{\partial\ell_i}{\partial z_i}=p_i-y_i",
                r"\nabla_{\mathbf{w}}J=\frac{X^{\mathsf{T}}(\mathbf{p}-\mathbf{y})}{m},\quad\frac{\partial J}{\partial b}=\frac{1}{m}\sum_i(p_i-y_i)",
            ],
        ),
        p(
            "For finite real logits, 0&lt;p&lt;1 mathematically, so the cancellation in the chain rule is valid. The last line differentiates the average objective; the preceding lines differentiate one observation, avoiding an omitted factor of 1/m."
        ),
        p("Why binary cross-entropy?", "h2"),
        p(
            "A binary response has Bernoulli likelihood p^y(1-p)^(1-y). Taking its negative logarithm gives the loss above. Confident incorrect probabilities incur a large penalty. BCE is a probability estimation objective; neither a low BCE nor a high ROC-AUC proves calibrated probabilities on a new population."
        ),
    )

    section("6  Stable scratch implementation")
    add(
        equations(
            "stable_bce.png",
            [
                r"\ell_i=\log(1+e^{z_i})-y_i z_i",
                r"J=\mathrm{mean}\left(\mathrm{logaddexp}(0,z)-yz\right)",
            ],
        ),
        p(
            "The computation uses NumPy logaddexp rather than log of a probability that can round to zero. Sigmoid evaluates 1/(1+exp(-z)) for nonnegative logits and exp(z)/(1+exp(z)) for negative logits. Neither branch exponentiates a large positive argument."
        ),
        table(
            ["Component", "Exact behavior"],
            [
                [
                    "Parameter arrays",
                    "weights_: shape (d,); bias_: scalar; predict_proba returns shape (m,).",
                ],
                [
                    "Targets",
                    "Binary values 0/1 only; nonfinite and mismatched inputs rejected.",
                ],
                [
                    "Training",
                    "Learning rate 0.13, 2,400 full-batch updates, zero initialization.",
                ],
                [
                    "Numerical monitoring",
                    "Nonfinite loss/gradients raise errors; loss history includes initial and final updated parameters.",
                ],
                ["Threshold", "0.5 for evaluation; thresholds outside [0,1] rejected."],
                [
                    "Extreme-input test",
                    "Logits -1000, 0, +1000 produce probabilities 0, 0.5, 1 without overflow; wrong labels give finite BCE 1000.",
                ],
            ],
            [117, 379],
        ),
        p("Convergence evidence", "h2"),
        p(
            f"The final gradient norm is {log['final_gradient_norm']:.3e}. Fixed-step training approaches the optimum but is not claimed to be exactly stationary. An independent unregularized sklearn LBFGS fit reaches training loss {log['reference_training_loss']:.8f}; the scratch loss is {log['train_loss_last']:.8f}. Maximum probability disagreement is {log['reference_probability_max_abs_diff']:.6f}, below the predeclared 0.005 tolerance."
        ),
        p(
            "A reproducible synthetic dataset includes label noise and overlapping classes. Such data avoid the claim that finite coefficients must exist for every possible perfectly separable dataset. Unregularized Logistic Regression can increase coefficient magnitude without reaching a finite optimum under complete separation."
        ),
    )

    section("7  Logistic Regression experiment")
    add(
        p(
            "make_classification uses 600 samples, five features, four informative features, no redundant features, weights 0.55/0.45, class separation 1.2, label-flip probability 0.04 and seed 27. The split uses seed 42 and stratification, giving 480 training and 120 test records. Class 1 is positive. Scaling is learned only from the training records."
        ),
        table(
            ["Measurement", "Executed result"],
            [
                [
                    "Initial / final training BCE",
                    f"{log['train_loss_first']:.6f} / {log['train_loss_last']:.6f}",
                ],
                ["Test accuracy", f"{log['accuracy']:.6f}"],
                [
                    "Positive precision / recall",
                    f"{log['precision']:.6f} / {log['recall']:.6f}",
                ],
                ["Positive F1 / ROC-AUC", f"{log['f1']:.6f} / {log['roc_auc']:.6f}"],
                [
                    "Gradient check maximum absolute difference",
                    f"{log['grad_check_max_abs_diff']:.3e}",
                ],
                ["Confusion matrix [TN, FP; FN, TP]", str(log["confusion_matrix"])],
            ],
            [295, 201],
        ),
        paired("q1_logistic_loss.png", "q1_logistic_confusion.png"),
        p(
            "Figures 4-5. BCE over 2,400 updates and confusion matrix at threshold 0.5; outputs trace to q1_arrays.npz.",
            "caption",
        ),
        p(
            f"There are {log['confusion_matrix'][0][1]} false positives and {log['confusion_matrix'][1][0]} false negatives. Recall is higher than precision, so the chosen threshold captures more positive cases while accepting some false alarms. ROC-AUC uses probabilities, assessing ranking across thresholds rather than classification at 0.5."
        ),
        p(
            "MSE, RMSE and MAE are regression metrics; precision, recall, F1 and confusion matrices reflect classification decisions. Evaluation therefore matches each Q1 problem rather than applying the same metric to both."
        ),
    )

    section("8  OpenML dataset and provenance")
    add(
        p(
            "Question 2 uses credit-g, a historical German Credit risk classification dataset. Its seven numerical and thirteen categorical predictors provide a substantive setting for encoding, scaling and generalization analysis. It replaces the previous sklearn Iris mirror because official OpenML retrieval was not established for that artifact."
        ),
        table(
            ["Provenance item", "Recorded evidence"],
            [
                [
                    "Official identity",
                    f"OpenML ID {provenance['dataset_id']}, version {provenance['dataset_version']}, name credit-g [1]",
                ],
                ["Rows / predictors / target", "1,000 / 20 / class"],
                ["Label distribution", "700 good; 300 bad"],
                ["Official download", provenance["raw_download_url"]],
                ["Retrieval time UTC", provenance["retrieved_at_utc"]],
                [
                    "Retrieval method",
                    "OpenML v1 JSON API then API-provided ARFF URL via urllib.request; raw bytes retained.",
                ],
                ["MD5 matches OpenML", provenance["raw_md5"]],
                [
                    "Raw SHA-256",
                    provenance["raw_sha256"][:32]
                    + "<br/>"
                    + provenance["raw_sha256"][32:],
                ],
                ["Raw size", str(provenance["bytes"]) + " bytes"],
                [
                    "Redistribution",
                    "OpenML metadata labels Public; originating UCI dataset is CC BY 4.0, attributed to H. Hofmann (1994) [2].",
                ],
            ],
            [147, 349],
        ),
        p("Verification status: VERIFIED", "h2"),
        p(
            "The downloaded MD5 exactly matches the checksum in the official JSON response. A stronger local SHA-256 identifies the retained artifact. The parser validates dataset dimensions, target classes, numeric finiteness and nominal domains. The offline experiment reuses these exact raw bytes and verifies both recorded hashes before parsing."
        ),
        p(
            "The cached file is an official downloaded artifact, not a reconstruction from another library. Reacquisition compares bytes and rejects unexpected changes. The metadata response and acquisition log are supplied separately from the raw ARFF.",
            "small",
        ),
    )

    section("9  Exploratory analysis and cleaning")
    add(
        p(
            "Raw schema validation finds zero missing cells and zero exact duplicate records; no rows are deleted and no artificial problems are injected. The 70/30 good/bad class imbalance makes majority accuracy potentially misleading. Exploratory plots and descriptive statistics use the 800-record development partition, keeping test feature distributions out of modelling decisions."
        ),
        figure(
            "q2_numeric_distributions.png",
            "Distributions of four development predictors, with risk labels distinguished by legend and hatch. Axis units vary by predictor.",
            400,
        ),
        table(
            ["Numerical predictor", "Train mean", "Train SD", "IQR outliers"],
            [
                [
                    c.replace("_", " "),
                    f"{description.loc['mean', c]:.2f}",
                    f"{description.loc['std', c]:.2f}",
                    str(q2["eda"]["iqr_outlier_counts_training"][c]),
                ]
                for c in provenance["numerical_features"]
            ],
            [216, 88, 88, 104],
        ),
        p(
            "Credit amounts and durations have visibly uneven scales and tails. The interquartile-range rule counts potential outliers descriptively; it does not establish erroneous records. These observations are retained because removing legitimate high-credit cases would change the task. Full numerical summaries and categorical counts are saved in q2_numeric_description.csv and q2_eda.json.",
            "small",
        ),
    )

    section("10  Preprocessing without leakage")
    add(
        p(
            "A single stratified split with seed 42 is created before fitting any transform: 800 development records (560 good, 240 bad) and 200 test records (140 good, 60 bad). The identical split applies to all models. Five fixed stratified folds divide development records into 640 training and 160 validation records."
        ),
        table(
            ["Feature type", "Pipeline and rationale"],
            [
                [
                    "Seven numerical predictors",
                    "Median imputation followed by StandardScaler. Each fold learns its own training statistics. Standardization supports distance, margin and linear methods.",
                ],
                [
                    "Thirteen categorical predictors",
                    "Most-frequent imputation and dense one-hot encoding. Categories are learned only from fold training rows; unseen categories map to an all-zero block.",
                ],
                [
                    "Target",
                    "good=0 and bad=1; this fixed semantic mapping is not a learned preprocessing step.",
                ],
                [
                    "Clean-data finding",
                    "Imputers are included to define a robust pipeline but no values are actually imputed in the verified raw dataset.",
                ],
            ],
            [117, 379],
        ),
        figure(
            "q2_categorical.png",
            "Development checking-account categories and credit risk counts. Association is descriptive, not causal.",
            370,
        ),
        p(
            f"The full development transform produces {q2['transformed_training_shape'][1]} columns. Tree thresholds are insensitive to positive affine rescaling of numeric predictors, so sharing the numeric scaler does not advantage trees. Dense one-hot input is manageable at this size; Gaussian Naive Bayes remains an approximate baseline because nominal indicator variables do not satisfy its Gaussian independence assumptions.",
            "small",
        ),
    )

    section("11  Model comparison protocol")
    add(
        p(
            "Macro-F1 is chosen before viewing test results: compute each class F1 and average them equally. It gives the minority bad-credit class equal weight, unlike accuracy on a 70/30 split. Balanced accuracy and class-specific recall provide complementary views. This is an educational metric choice, not an implementation of the dataset cost matrix."
        ),
        table(
            ["Classifier", "Predefined main settings"],
            [
                [
                    "Dummy majority",
                    "Most frequent label; reported separately as baseline.",
                ],
                ["Logistic Regression", "C=1, max_iter=3000"],
                ["KNN", "k=5, uniform Euclidean neighbors"],
                ["Gaussian Naive Bayes", "Default variance smoothing"],
                ["Decision Tree", "Unrestricted depth, default leaf size"],
                ["Random Forest / Extra Trees", "150 trees each, n_jobs=1"],
                ["Linear SVM", "C=1, max_iter=20000"],
                ["RBF SVM", "C=1, gamma=scale"],
                ["Gradient Boosting", "100 stages, defaults otherwise"],
                ["HistGradientBoosting", "100 iterations, defaults otherwise"],
                ["AdaBoost", "100 estimators, learning rate 0.5"],
                ["LDA", "SVD solver; handles redundant one-hot directions"],
            ],
            [178, 318],
        ),
        p(
            "All stochastic estimators use seed 42. Complete estimator settings are serialized in q2_selection.json; unspecified settings are pinned by the recorded sklearn version. QDA is excluded because full one-hot indicators yield singular class covariance. MLP is omitted to bound runtime while retaining 12 meaningful learning algorithms."
        ),
        p(
            "Each estimator is a Pipeline containing its own ColumnTransformer. cross_validate clones and fits that entire pipeline inside each fold. Errors raise immediately and warnings remain in logs. CV uses the same folds, n_jobs=1 and five validation scores per candidate. The highest mean macro-F1 among predictive models wins, with alphabetical tie-break."
        ),
        p(
            "The selection file is written before any held-out prediction. The capacity studies also use development data only. Every predefined benchmark model is then fitted on development data and evaluated once on test data; the table does not trigger tuning.",
            "small",
        ),
    )

    section("12  Cross-validation and test comparison")
    add(
        p(
            "The table is ordered by training-only mean macro-F1. The standard deviation is the sample SD across five folds (ddof=1); it is not a confidence interval and the folds are not independent experiments."
        ),
        table(
            ["Model", "CV F1 ± SD", "Test accuracy", "Test macro-F1"],
            [
                [
                    r["model"],
                    f"{r['cv_macro_f1_mean']:.3f} ± {r['cv_macro_f1_std']:.3f}",
                    f"{r['test_accuracy']:.3f}",
                    f"{r['test_macro_f1']:.3f}",
                ]
                for _, r in rank.iterrows()
            ],
            [181, 127, 94, 94],
        ),
        figure(
            "q2_model_comparison.png",
            "Mean development CV macro-F1 with sample SD. The zero-based axis avoids magnifying small differences.",
            400,
        ),
        p(
            "Results are specific to this split, preprocessing and predefined settings. Close means relative to fold variability do not establish statistically significant differences. The majority baseline has 0.700 test accuracy but only 0.412 macro-F1, illustrating why accuracy alone can reward ignoring the minority class.",
            "small",
        ),
    )

    section("13  Selected model and generalization")
    add(
        p(
            f"The validation rule selects <b>{q2['champion_selected_by_train_cv']}</b>, with CV macro-F1 {chosen['cv_macro_f1_mean']:.4f} ± {chosen['cv_macro_f1_std']:.4f}. This estimator is selected before the test set is evaluated."
        ),
        table(
            ["Held-out measurement", "Value"],
            [
                [
                    "Accuracy / macro-F1",
                    f"{chosen['test_accuracy']:.6f} / {chosen['test_macro_f1']:.6f}",
                ],
                [
                    "Macro precision / macro recall",
                    f"{chosen['test_precision_macro']:.6f} / {chosen['test_recall_macro']:.6f}",
                ],
                [
                    "Bad-credit precision / recall",
                    f"{chosen['test_precision_bad']:.6f} / {chosen['test_recall_bad']:.6f}",
                ],
                [
                    "Balanced accuracy / ROC-AUC",
                    f"{chosen['test_balanced_accuracy']:.6f} / {chosen['test_roc_auc']:.6f}",
                ],
                [
                    "Confusion matrix [TN, FP; FN, TP]",
                    str(q2["champion_confusion_matrix"]),
                ],
            ],
            [314, 182],
        ),
        paired("q2_champion_confusion.png", "q2_roc.png"),
        p(
            f"Figures {figure_number - 1}-{figure_number}. Selected-model test confusion matrix and ROC. Bad credit is positive; ROC uses predicted scores rather than hard labels.",
            "caption",
        ),
        p(
            "Validation estimates performance during selection; test estimates performance of the resulting fixed procedure on held-out observations. Some other candidates achieve higher test metrics on this split. Replacing the chosen model after reading those results would use the test as a selection signal."
        ),
        p(
            f"The selected model has fold training macro-F1 {chosen['fold_train_macro_f1_mean']:.4f} and a train/validation gap of {chosen['fold_generalization_gap']:.4f}, so winning CV does not imply absence of overfitting. One changed prediction shifts test accuracy by 0.5 percentage points. Additional independent data would be required to validate stability."
        ),
    )

    section("14  Overfitting across model families")
    add(
        p(
            "Overfitting is diagnosed through a high training score and weaker unseen validation score. The comparison uses fold training and validation on the same fits, avoiding a misleading comparison of unrelated training sizes. A gap is evidence of limited generalization; it does not by itself prove which mechanism caused the gap."
        ),
        table(
            ["Model", "Fold train F1", "CV F1", "Mean gap"],
            [
                [
                    r["model"],
                    f"{r['fold_train_macro_f1_mean']:.3f}",
                    f"{r['cv_macro_f1_mean']:.3f}",
                    f"{r['fold_generalization_gap']:.3f}",
                ]
                for _, r in rank.iterrows()
            ],
            [209, 97, 95, 95],
        ),
        p(
            "Flexible trees attain perfect fold training scores with substantial validation gaps. The majority baseline has no gap yet underfits the minority. Both predictive quality and generalization matter."
        ),
        figure(
            "q2_knn_complexity.png",
            "KNN complexity curve on the fixed development folds. Larger k smooths local predictions; vertical bars are sample SD. Tree and SVM configurations are detailed in Section 15.",
            380,
        ),
        p(
            "All 20 settings use the identical five folds. No test score appears in capacity selection. These studies diagnose changes in complexity; they are not an exhaustive hyperparameter search.",
            "small",
        ),
    )

    section("15  Empirical mitigation and trade-offs")
    for study in q2["overfitting_studies"]:
        original = study["original"]
        best = study["selected"]
        add(
            p(study["family"], "h2"),
            table(
                ["Configuration", "Fold train F1", "CV F1", "Gap"],
                [
                    [
                        original["configuration"],
                        f"{original['fold_train_macro_f1_mean']:.4f}",
                        f"{original['cv_macro_f1_mean']:.4f}",
                        f"{original['fold_generalization_gap']:.4f}",
                    ],
                    [
                        best["configuration"],
                        f"{best['fold_train_macro_f1_mean']:.4f}",
                        f"{best['cv_macro_f1_mean']:.4f}",
                        f"{best['fold_generalization_gap']:.4f}",
                    ],
                ],
                [220, 92, 92, 92],
            ),
            p(
                f"Best tested validation change: {study['validation_change']:+.4f}; gap change: {study['gap_change']:+.4f}. Full-fit training scores and every candidate configuration are retained in q2_studies.csv.",
                "small",
            ),
        )
    add(
        p(
            "Tree pre-pruning via minimum leaf size reduces tiny partitions and increases validation macro-F1 here. It is capacity restriction during construction, not iterative early stopping. With KNN, increasing k from 1 to 5 reduces local memorization, but the small CV gain should not be overstated."
        ),
        p(
            "The deliberately extreme RBF SVM (C=100, gamma=1) generalizes poorly. A less localized kernel improves CV substantially, though the selected C=10, gamma=0.1 configuration still has a large gap. Regularization can reduce a problem without eliminating it."
        ),
        p(
            "Not every stronger restriction improves validation. Some shallow trees and very large neighbor counts lose predictive capacity. All negative or weaker candidate outcomes remain visible in the study CSV and curve, rather than reporting only the best pair."
        ),
        p(
            "The best study scores reuse folds used to select settings and can therefore be optimistic. They support descriptive comparisons, not an unbiased estimate of tuning benefit. The final preferred model remains the benchmark CV winner; study settings are not promoted after examining test results.",
            "small",
        ),
    )

    section("16  Discussion and remaining limitations")
    add(
        table(
            ["Remaining family", "Suggested control; not separately tuned here"],
            [
                [
                    "Logistic Regression / Linear SVM",
                    "Reduce C to increase regularization; compare on training CV.",
                ],
                [
                    "Random Forest / Extra Trees",
                    "Increase minimum leaf size, limit depth or features. More trees mainly reduce Monte Carlo variance, not necessarily capacity.",
                ],
                [
                    "Gradient / histogram boosting",
                    "Reduce leaf complexity, stage count or learning rate; assess validation early stopping using training data only.",
                ],
                [
                    "AdaBoost",
                    "Control weak-learner capacity and stage count; label noise can remain influential.",
                ],
                [
                    "Gaussian Naive Bayes",
                    "Consider variance smoothing and assumption mismatch; low gaps may reflect underfitting.",
                ],
                [
                    "LDA",
                    "Consider covariance shrinkage with an appropriate solver; evaluate rather than assume a gain.",
                ],
            ],
            [158, 338],
        ),
        p(
            "Q1 demonstrates correct optimization on synthetic tasks, not universal regression or classification performance. The Logistic Regression fit is close to its unregularized reference but not exactly stationary; the measured tolerance and remaining difference are explicit."
        ),
        p(
            "Q2 uses a single stratified random split and a small historical dataset. Its imbalance, redundant indicators and possible demographic associations limit interpretation. The original cost matrix penalizes a bad customer classified as good more heavily [2]; macro-F1 is not a cost-sensitive objective. Neither fairness nor probability calibration is evaluated."
        ),
        p(
            "No statistical significance, deployment readiness or causal claim follows from these scores. Nested CV would be useful for a future tuned-procedure comparison but is not claimed here. Broader family-specific advice above is theoretical; only Tree, KNN and RBF SVM controls were experimentally compared."
        ),
        p("Conclusion", "h2"),
        p(
            "Both scratch models use derived NumPy gradients and full-batch updates with independent numerical checks. Official OpenML provenance is verified, preprocessing is fitted within training folds, and validation evidence controls model selection. The capacity studies show both the usefulness and limits of stronger regularization. The companion source, executed notebooks and verification records make the reported evidence inspectable."
        ),
    )

    section("17  References")
    refs = [
        "[1] OpenML. credit-g, dataset 31, version 1. Official metadata and raw download. https://www.openml.org/api/v1/json/data/31 and https://www.openml.org/d/31. Retrieved 9 October 2026.",
        "[2] Hofmann, H. (1994). Statlog (German Credit Data). UCI Machine Learning Repository. DOI: 10.24432/C5NC77. https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data. CC BY 4.0; accessed 9 October 2026.",
        "[3] scikit-learn developers. Cross-validation: evaluating estimator performance. https://scikit-learn.org/stable/modules/cross_validation.html. Accessed 9 October 2026.",
        "[4] scikit-learn developers. Pipelines and composite estimators; ColumnTransformer for heterogeneous data. https://scikit-learn.org/stable/modules/compose.html. Accessed 9 October 2026.",
        "[5] scikit-learn developers. Linear models; Linear and Logistic Regression. https://scikit-learn.org/stable/modules/linear_model.html. Accessed 9 October 2026.",
        "[6] scikit-learn developers. Metrics and scoring: quantifying prediction quality. https://scikit-learn.org/stable/modules/model_evaluation.html. Accessed 9 October 2026.",
    ]
    for reference in refs:
        add(p(reference))
    add(
        p("Attribution and evidence", "h2"),
        p(
            "Dataset attribution identifies the original creator and originating repository, while the experiment uses the specific OpenML ARFF distribution. Source URLs and metadata are retained so the data identity can be checked independently. No equivalence claim is made between credit-g and the previous Iris CSV."
        ),
        p(
            "The loss derivations in Sections 2 and 5 are shown in full. References provide established model and workflow context; they are not substitutes for the submitted calculations or experiment execution. Figures are generated from the supplied raw data and measured optimization histories."
        ),
        p(
            "DejaVu fonts are bundled with their license to support offline PDF reconstruction. No external stock imagery or generated illustrative data appears in this report."
        ),
    )

    section("18  Reproducibility and verification appendix")
    add(
        table(
            ["Artifact", "Role"],
            [
                [
                    "src/q1_models.py",
                    "Scratch algorithms, synthetic data, independent reference checks and results.",
                ],
                ["src/data.py", "Official retrieval and raw artifact verification."],
                [
                    "src/q2_classification.py",
                    "Development EDA, fold-safe pipelines, comparison and capacity experiments.",
                ],
                ["notebooks/", "Three teaching notebooks executed from fresh kernels."],
                [
                    "data/raw and data/metadata",
                    "ARFF, official response, provenance, split indices and CV folds.",
                ],
                [
                    "results/",
                    "Metrics, per-fold scores, capacity settings, predictions and execution logs.",
                ],
                [
                    "tests/ and verification/",
                    "Mathematical, data, leakage, determinism, notebook, report and archive checks.",
                ],
                [
                    "report/report_source/",
                    "Editable metadata, generated manuscript, font licenses and numerical trace.",
                ],
            ],
            [185, 311],
        ),
        p("Reproduction order", "h2"),
        p(
            "Use Python 3.14 with the pinned requirements, from the extracted project root. Verify the cached dataset, run Q1, run Q2, execute the three notebooks, run unittest, then rebuild the PDF. Fish-compatible commands are in README.md. BLAS/OpenMP and estimator parallelism are capped at one thread."
        ),
        p("Expected evidence", "h2"),
        p(
            "Q1 tolerances are assertions in the experiment and tests. Q2 test metrics are recomputed from stored predictions; fold means, SD and gaps are recomputed from fold scores. Fold-specific imputer, scaler and category statistics are tested directly. Report numeric claims read generated JSON/CSV files; rendered PDF QA is documented separately."
        ),
        p("Every member must submit", "h2"),
        p(
            "The lecturer requires every group member to submit both the PDF and code. Confirm the student IDs on the cover, review the study guide, and understand the derivations and model-selection protocol before submission. No class section or institution has been invented."
        ),
        p(
            "Verification reports retain genuine failures and limitations. Passing finite-difference checks verifies tested code numerically, not all possible inputs. Readiness is stated in verification/requirements_traceability.md after all feasible execution gates.",
            "small",
        ),
    )

    output = root / "report/Machine_Learning_Midterm_Final.pdf"
    output.parent.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=62,
        bottomMargin=54,
        title=metadata["title"],
        author="; ".join(m["name"] for m in metadata["members"]),
        subject="NumPy Gradient Descent and verified OpenML classification",
    )
    doc.build(story, canvasmaker=NumberCanvas)
    (source / "manuscript.md").write_text(
        "# " + metadata["title"] + "\n\n" + "\n\n".join(manuscript), encoding="utf-8"
    )
    (source / "numerical_trace.json").write_text(
        json.dumps(
            dict(
                q1=q1,
                selected_q2=chosen,
                provenance=provenance,
                figures=figure_manifest,
            ),
            indent=2,
        )
    )
    print("PDF_CREATED", output, output.stat().st_size)
    return output


if __name__ == "__main__":
    main()
