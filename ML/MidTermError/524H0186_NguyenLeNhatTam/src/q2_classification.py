"""Predeclared credit-g benchmark: train-only selection, one holdout evaluation."""

import json
import time
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
)
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    AdaBoostClassifier,
)
from sklearn.svm import SVC, LinearSVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from src.data import ROOT, NUMERIC, load_data

SEED = 42
PRIMARY_METRIC = "f1_macro"
plt.rcParams.update(
    {
        "font.size": 13,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelcolor": "#142A46",
        "text.color": "#142A46",
        "savefig.dpi": 190,
    }
)


def split_data(df):
    X = df.drop(columns="class")
    y = (df["class"] == "bad").astype(int)
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)


def make_pipeline(model, X):
    categorical = [c for c in X.columns if c not in NUMERIC]
    prep = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                NUMERIC,
            ),
            (
                "categorical",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        (
                            "encode",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                categorical,
            ),
        ],
        sparse_threshold=0,
    )
    return Pipeline([("preprocess", prep), ("model", model)])


def models():
    return {
        "Dummy majority": DummyClassifier(strategy="most_frequent"),
        "Logistic Regression": LogisticRegression(
            C=1.0, max_iter=3000, random_state=SEED
        ),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Gaussian Naive Bayes": GaussianNB(),
        "Decision Tree": DecisionTreeClassifier(random_state=SEED),
        "Random Forest": RandomForestClassifier(
            n_estimators=150, random_state=SEED, n_jobs=1
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=150, random_state=SEED, n_jobs=1
        ),
        "Linear SVM": LinearSVC(C=1.0, max_iter=20000, random_state=SEED),
        "RBF SVM": SVC(C=1.0, gamma="scale", random_state=SEED),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, random_state=SEED
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=100, random_state=SEED
        ),
        "AdaBoost": AdaBoostClassifier(
            n_estimators=100, learning_rate=0.5, random_state=SEED
        ),
        "LDA": LinearDiscriminantAnalysis(solver="svd"),
    }


def evaluate_cv(model, X, y, folds):
    scores = cross_validate(
        make_pipeline(clone(model), X),
        X,
        y,
        cv=folds,
        scoring=PRIMARY_METRIC,
        return_train_score=True,
        n_jobs=1,
        error_score="raise",
    )
    return dict(
        cv_macro_f1_mean=float(scores["test_score"].mean()),
        cv_macro_f1_std=float(scores["test_score"].std(ddof=1)),
        fold_train_macro_f1_mean=float(scores["train_score"].mean()),
        fold_generalization_gap=float(
            (scores["train_score"] - scores["test_score"]).mean()
        ),
    ), scores


def run_studies(X, y, folds):
    # Configurations fixed before opening holdout results; larger k reduces local flexibility.
    configs = [
        (
            "Decision Tree",
            f"depth={d},leaf={leaf}",
            DecisionTreeClassifier(
                max_depth=d, min_samples_leaf=leaf, random_state=SEED
            ),
        )
        for d, leaf in [
            (None, 1),
            (2, 1),
            (3, 1),
            (5, 1),
            (8, 1),
            (None, 5),
            (None, 15),
        ]
    ]
    configs += [
        ("KNN", f"k={k}", KNeighborsClassifier(n_neighbors=k))
        for k in [1, 3, 5, 11, 21, 41]
    ]
    configs += [
        ("RBF SVM", f"C={c},gamma={g}", SVC(C=c, gamma=g, random_state=SEED))
        for c, g in [
            (100, 1.0),
            (0.1, "scale"),
            (1.0, "scale"),
            (10.0, "scale"),
            (1.0, 0.01),
            (1.0, 0.1),
            (10.0, 0.1),
        ]
    ]
    rows, fold_rows = [], []
    for family, config, model in configs:
        metrics, scores = evaluate_cv(model, X, y, folds)
        fitted = make_pipeline(clone(model), X).fit(X, y)
        rows.append(
            dict(
                family=family,
                configuration=config,
                full_train_macro_f1=float(
                    f1_score(y, fitted.predict(X), average="macro")
                ),
                **metrics,
            )
        )
        for i, (tr, val) in enumerate(zip(scores["train_score"], scores["test_score"])):
            fold_rows.append(
                dict(
                    stage="study",
                    model=family,
                    configuration=config,
                    fold=i,
                    train_macro_f1=float(tr),
                    validation_macro_f1=float(val),
                )
            )
    return pd.DataFrame(rows), fold_rows


def savefig(root, name):
    plt.tight_layout()
    plt.savefig(root / "figures" / name)
    plt.close()


def exploratory(root, df, Xtr, ytr):
    categorical = [c for c in Xtr if c not in NUMERIC]
    iqr = Xtr[NUMERIC].quantile(0.75) - Xtr[NUMERIC].quantile(0.25)
    low = Xtr[NUMERIC].quantile(0.25) - 1.5 * iqr
    high = Xtr[NUMERIC].quantile(0.75) + 1.5 * iqr
    eda = dict(
        raw_rows=len(df),
        raw_columns=len(df.columns),
        missing_cells=int(df.isna().sum().sum()),
        exact_duplicate_rows=int(df.duplicated().sum()),
        numeric_count=len(NUMERIC),
        categorical_count=len(categorical),
        cleaning="No records removed: valid schema, no missing values, no exact duplicates. Outliers retained as plausible observations.",
        iqr_outlier_counts_training={
            c: int(v)
            for c, v in ((Xtr[NUMERIC] < low) | (Xtr[NUMERIC] > high)).sum().items()
        },
        categorical_counts_training={
            c: {str(k): int(v) for k, v in Xtr[c].value_counts().items()}
            for c in categorical
        },
        categorical_cardinality_training={
            c: int(Xtr[c].nunique()) for c in categorical
        },
    )
    if eda["exact_duplicate_rows"]:
        raise ValueError(
            "Unexpected duplicate records: investigate before defining split"
        )
    Xtr[NUMERIC].describe().to_csv(root / "results/q2_numeric_description.csv")
    (root / "results/q2_eda.json").write_text(json.dumps(eda, indent=2))
    plt.figure(figsize=(6, 3.6))
    bars = plt.bar(
        ["Good (0)", "Bad (1)"],
        [(ytr == 0).sum(), (ytr == 1).sum()],
        color=["#142A46", "#0E7490"],
    )
    plt.bar_label(bars, padding=3)
    plt.ylim(0, len(ytr) * 0.8)
    plt.ylabel("Training records")
    plt.title("Credit risk labels in development partition")
    savefig(root, "q2_class_balance.png")
    fig, axs = plt.subplots(2, 2, figsize=(8.5, 5.8))
    for ax, c in zip(
        axs.ravel(), ["duration", "credit_amount", "age", "existing_credits"]
    ):
        edges = np.histogram_bin_edges(Xtr[c], bins=14)
        for label, color, hatch in [(0, "#142A46", ""), (1, "#0E7490", "//")]:
            ax.hist(
                Xtr.loc[ytr == label, c],
                bins=edges,
                alpha=0.55,
                color=color,
                hatch=hatch,
                label=["Good", "Bad"][label],
            )
        ax.set_xlabel(c.replace("_", " "))
        ax.set_ylabel("Records")
    axs[0, 0].legend()
    fig.suptitle("Training feature distributions by credit risk")
    savefig(root, "q2_numeric_distributions.png")
    counts = pd.crosstab(Xtr["checking_status"], ytr).rename(
        columns={0: "Good", 1: "Bad"}
    )
    counts.plot.bar(stacked=True, color=["#142A46", "#0E7490"], figsize=(7, 4), rot=0)
    plt.ylabel("Training records")
    plt.xlabel("Checking account status")
    plt.title("A categorical predictor and credit risk")
    savefig(root, "q2_categorical.png")
    return eda


def main(root=ROOT):
    started = time.perf_counter()
    for folder in ["results", "figures", "data/metadata"]:
        (root / folder).mkdir(parents=True, exist_ok=True)
    data = load_data(root)
    Xtr, Xte, ytr, yte = split_data(data)
    folds = list(
        StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED).split(Xtr, ytr)
    )
    split = dict(
        seed=SEED,
        train_indices=Xtr.index.tolist(),
        test_indices=Xte.index.tolist(),
        train_class_counts={str(k): int(v) for k, v in ytr.value_counts().items()},
        test_class_counts={str(k): int(v) for k, v in yte.value_counts().items()},
    )
    (root / "data/metadata/split.json").write_text(json.dumps(split, indent=2))
    (root / "data/metadata/folds.json").write_text(
        json.dumps([dict(train=a.tolist(), validation=b.tolist()) for a, b in folds])
    )
    eda = exploratory(root, data, Xtr, ytr)
    all_models = models()
    rows = []
    fold_rows = []
    # No Xte/yte passed into CV or capacity studies.
    for name, model in all_models.items():
        print("CV:", name, flush=True)
        metrics, scores = evaluate_cv(model, Xtr, ytr, folds)
        rows.append(dict(model=name, **metrics))
        for i, (tr, val) in enumerate(zip(scores["train_score"], scores["test_score"])):
            fold_rows.append(
                dict(
                    stage="benchmark",
                    model=name,
                    configuration="predeclared",
                    fold=i,
                    train_macro_f1=float(tr),
                    validation_macro_f1=float(val),
                )
            )
    comparison = (
        pd.DataFrame(rows)
        .sort_values(["cv_macro_f1_mean", "model"], ascending=[False, True])
        .reset_index(drop=True)
    )
    champion_name = comparison.loc[comparison.model != "Dummy majority", "model"].iloc[
        0
    ]
    studies, study_folds = run_studies(Xtr, ytr, folds)
    fold_rows += study_folds
    studies.to_csv(root / "results/q2_studies.csv", index=False)
    study_summary = []
    for family in ["Decision Tree", "KNN", "RBF SVM"]:
        group = studies[studies.family == family]
        original = group.iloc[0]
        best = group.sort_values(
            ["cv_macro_f1_mean", "fold_generalization_gap"], ascending=[False, True]
        ).iloc[0]
        study_summary.append(
            dict(
                family=family,
                original=original.to_dict(),
                selected=best.to_dict(),
                validation_change=float(
                    best.cv_macro_f1_mean - original.cv_macro_f1_mean
                ),
                gap_change=float(
                    best.fold_generalization_gap - original.fold_generalization_gap
                ),
            )
        )
    selection = dict(
        primary_metric=PRIMARY_METRIC,
        champion=champion_name,
        rule="Maximum training-only CV mean macro-F1; alphabetical tie-break; baseline excluded",
        selected_before_test=True,
        capacity_studies=study_summary,
        candidate_parameters={
            name: {k: str(v) for k, v in m.get_params().items()}
            for name, m in all_models.items()
        },
    )
    # Save the decision before any held-out predictions are computed.
    (root / "results/q2_selection.json").write_text(json.dumps(selection, indent=2))
    predictions = pd.DataFrame({"row_index": Xte.index, "y_true": yte.to_numpy()})
    for i, row in comparison.iterrows():
        name = row["model"]
        pipe = make_pipeline(clone(all_models[name]), Xtr).fit(Xtr, ytr)
        pred = pipe.predict(Xte)
        train_pred = pipe.predict(Xtr)
        score = (
            pipe.predict_proba(Xte)[:, 1]
            if hasattr(pipe, "predict_proba")
            else pipe.decision_function(Xte)
        )
        comparison.loc[i, "full_train_macro_f1"] = f1_score(
            ytr, train_pred, average="macro"
        )
        for key, value in dict(
            test_accuracy=accuracy_score(yte, pred),
            test_precision_bad=precision_score(yte, pred, zero_division=0),
            test_recall_bad=recall_score(yte, pred, zero_division=0),
            test_precision_macro=precision_score(
                yte, pred, average="macro", zero_division=0
            ),
            test_recall_macro=recall_score(yte, pred, average="macro", zero_division=0),
            test_macro_f1=f1_score(yte, pred, average="macro"),
            test_balanced_accuracy=balanced_accuracy_score(yte, pred),
            test_roc_auc=roc_auc_score(yte, score),
        ).items():
            comparison.loc[i, key] = value
        predictions[name + "__prediction"] = pred
        predictions[name + "__score"] = score
        if name == champion_name:
            champion_cm = confusion_matrix(yte, pred, labels=[0, 1])
            transformed = pipe.named_steps["preprocess"].transform(Xtr)
            encoded_features = (
                pipe.named_steps["preprocess"].get_feature_names_out().tolist()
            )
            fig, ax = plt.subplots(figsize=(5.5, 4.4))
            ConfusionMatrixDisplay(champion_cm, display_labels=["Good", "Bad"]).plot(
                ax=ax, cmap="Blues", colorbar=False
            )
            ax.set_title("CV-selected model: " + name)
            savefig(root, "q2_champion_confusion.png")
            fig, ax = plt.subplots(figsize=(5.5, 4.3))
            RocCurveDisplay.from_predictions(yte, score, ax=ax, name="Selected model")
            ax.plot([0, 1], [0, 1], "--", color="#777")
            ax.set_xlabel("False positive rate")
            ax.set_ylabel("True positive rate")
            ax.set_title("Test ROC (bad credit = 1)")
            ax.legend(loc="lower right", fontsize=12)
            savefig(root, "q2_roc.png")
    comparison.to_csv(root / "results/q2_model_comparison.csv", index=False)
    predictions.to_csv(root / "results/q2_predictions.csv", index=False)
    pd.DataFrame(fold_rows).to_csv(root / "results/q2_fold_scores.csv", index=False)
    view = comparison.sort_values("cv_macro_f1_mean")
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.barh(view.model, view.cv_macro_f1_mean, color="#0E7490")
    ax.errorbar(
        view.cv_macro_f1_mean,
        np.arange(len(view)),
        xerr=view.cv_macro_f1_std,
        fmt="none",
        ecolor="#142A46",
        capsize=3,
    )
    ax.set_xlim(0, 1)
    ax.set_xlabel("Training-only 5-fold macro-F1 (mean +/- sample SD)")
    ax.set_title("Predeclared classifier comparison")
    savefig(root, "q2_model_comparison.png")
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.2))
    for ax, family in zip(axs, ["Decision Tree", "KNN", "RBF SVM"]):
        view = studies[studies.family == family]
        xs = np.arange(len(view))
        ax.plot(
            xs,
            view.fold_train_macro_f1_mean,
            "o-",
            label="Fold training",
            color="#142A46",
        )
        ax.errorbar(
            xs,
            view.cv_macro_f1_mean,
            yerr=view.cv_macro_f1_std,
            fmt="s--",
            capsize=2,
            label="Fold validation",
            color="#0E7490",
        )
        ax.set_xticks(xs, view.configuration, rotation=65, ha="right", fontsize=7)
        ax.set_ylim(0, 1.05)
        ax.set_title(family)
        ax.set_ylabel("Macro-F1")
    axs[0].legend(fontsize=8)
    savefig(root, "q2_overfitting.png")
    view = studies[studies.family == "KNN"]
    ks = [int(s.split("=")[1]) for s in view.configuration]
    fig, ax = plt.subplots(figsize=(7.5, 3.5))
    ax.plot(
        ks, view.fold_train_macro_f1_mean, "o-", label="Fold training", color="#142A46"
    )
    ax.errorbar(
        ks,
        view.cv_macro_f1_mean,
        yerr=view.cv_macro_f1_std,
        fmt="s--",
        capsize=3,
        label="Fold validation",
        color="#0E7490",
    )
    ax.set_xticks(ks)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Neighbor count k")
    ax.set_ylabel("Macro-F1")
    ax.legend(fontsize=10)
    savefig(root, "q2_knn_complexity.png")
    selected = comparison.loc[comparison.model == champion_name].iloc[0].to_dict()
    summary = dict(
        dataset_id=31,
        dataset_version=1,
        dataset_name="credit-g",
        train_rows=len(ytr),
        test_rows=len(yte),
        seed=SEED,
        cv_folds=5,
        primary_metric=PRIMARY_METRIC,
        baseline="Dummy majority",
        predictive_algorithms=12,
        champion_selected_by_train_cv=champion_name,
        champion_metrics=selected,
        champion_confusion_matrix=champion_cm.tolist(),
        label_order=["good (0)", "bad (1)"],
        transformed_training_shape=list(transformed.shape),
        encoded_features=encoded_features,
        eda=eda,
        overfitting_studies=study_summary,
        exclusions={
            "MLP": "Omitted to bound CPU cost; 12 learning algorithms cover the principal families.",
            "QDA": "Full one-hot indicators introduce singular within-class covariance; LDA with SVD is included.",
        },
        warning_policy="Warnings preserved in execution logs; CV errors raise immediately.",
        parallelism="n_jobs=1; BLAS/OpenMP capped by documented environment variables",
        elapsed_seconds=time.perf_counter() - started,
    )
    (root / "results/q2_summary.json").write_text(json.dumps(summary, indent=2))
    print(comparison.to_string(index=False))
    print(json.dumps(summary, indent=2))
    return summary, comparison


if __name__ == "__main__":
    main()
