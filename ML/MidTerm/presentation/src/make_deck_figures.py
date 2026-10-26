"""Build slide-sized figures for the midterm deck from the saved result artifacts.

Every number plotted here is read from ``results/`` (the same files the report
uses) and re-checked against the exported metrics before a figure is written.
Figures are rendered at their final on-slide size so the slide deck never
downscales them.

Run from the MidTerm folder:  python3 presentation/src/make_deck_figures.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
FIGDIR = ROOT / "presentation" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

# Restrained series palette: blue / orange / green, plus class colours used in
# the report's own figures so the deck and the report read as one document.
BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"
GOOD = "#5b8db8"
BAD = "#c0392b"
INK = "#1a1a1a"
MUTED = "#666666"

plt.rcParams.update(
    {
        "font.family": "Arial",
        "font.size": 13,
        "axes.titlesize": 14.5,
        "axes.labelsize": 13.5,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 11.5,
        "axes.edgecolor": "#444444",
        "axes.linewidth": 0.9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    }
)

CHECKS: list[tuple[str, float, float]] = []


def check(label: str, got: float, want: float, tol: float = 5e-4) -> float:
    CHECKS.append((label, got, want))
    if abs(got - want) > tol:
        raise SystemExit(f"MISMATCH {label}: computed {got} vs exported {want}")
    return got


def load_json(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def load_loss(name: str) -> tuple[np.ndarray, np.ndarray]:
    with (RESULTS / name).open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return (
        np.array([float(r["iteration"]) for r in rows]),
        np.array([float(r["loss"]) for r in rows]),
    )


# ---------------------------------------------------------------- Q1 linear
def fig_q1_linear() -> None:
    m = load_json("q1_metrics.json")["linear"]
    data = np.load(RESULTS / "q1_linear_data.npz")
    it, loss = load_loss("q1_linear_loss.csv")
    y_test = data["y"][data["test"]]
    pred = data["predicted"]

    r2 = 1 - np.sum((y_test - pred) ** 2) / np.sum((y_test - y_test.mean()) ** 2)
    rmse = float(np.sqrt(np.mean((y_test - pred) ** 2)))
    check("q1 linear R2", r2, m["r2"])
    check("q1 linear RMSE", rmse, m["rmse"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 3.9))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.93, bottom=0.13, wspace=0.28)

    ax1.semilogy(it, loss, color=BLUE, lw=1.6)
    ax1.set_title("Mất mát huấn luyện giảm đơn điệu", loc="left")
    ax1.set_xlabel("Vòng lặp GD")
    ax1.set_ylabel("J(w, b)  =  MSE / 2")
    ax1.annotate(
        f"{m['initial_loss']:.1f} → {m['final_loss']:.3f}",
        xy=(0.97, 0.9),
        xycoords="axes fraction",
        ha="right",
        va="top",
        fontsize=12.5,
        color=INK,
    )
    ax1.text(
        0.97,
        0.79,
        f"dừng sau {m['iterations']} vòng",
        transform=ax1.transAxes,
        ha="right",
        va="top",
        fontsize=11.5,
        color=MUTED,
    )

    ax2.scatter(y_test, pred, s=26, color=BLUE, alpha=0.75, edgecolor="white", linewidth=0.5)
    lo, hi = float(min(y_test.min(), pred.min())), float(max(y_test.max(), pred.max()))
    ax2.plot([lo, hi], [lo, hi], color=INK, lw=1.1, ls="--", label="Dự đoán hoàn hảo")
    ax2.set_title("Tập test: dự đoán bám sát giá trị thật", loc="left")
    ax2.set_xlabel("Giá trị thật  y")
    ax2.set_ylabel("Dự đoán  ŷ")
    ax2.legend(loc="upper left", frameon=False)
    ax2.text(
        0.97,
        0.08,
        f"R² = {r2:.4f}\nRMSE = {rmse:.4f}",
        transform=ax2.transAxes,
        ha="right",
        va="bottom",
        fontsize=12.5,
        color=INK,
        linespacing=1.4,
    )

    fig.savefig(FIGDIR / "fig_q1_linear.png", dpi=200)
    plt.close(fig)


# -------------------------------------------------------------- Q1 logistic
def fig_q1_logistic() -> None:
    m = load_json("q1_metrics.json")["logistic"]
    data = np.load(RESULTS / "q1_logistic_data.npz")
    it, loss = load_loss("q1_logistic_loss.csv")

    X, y, train, test = data["X"], data["y"], data["train"], data["test"]
    w_s, b_s = data["weights"], float(data["bias"])
    lo, rng = X[train].min(axis=0), X[train].max(axis=0) - X[train].min(axis=0)
    # Undo the training min-max scale to draw the boundary in original units.
    w_raw = w_s / rng
    b_raw = b_s - float(np.sum(w_s * lo / rng))
    check("q1 logistic raw w1", float(w_raw[0]), m["raw_weights"][0])
    check("q1 logistic raw w2", float(w_raw[1]), m["raw_weights"][1])
    check("q1 logistic raw b", b_raw, m["raw_bias"])
    pred = data["predicted"]
    acc = float(np.mean(pred == y[test]))
    check("q1 logistic accuracy", acc, m["accuracy"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 3.9))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.93, bottom=0.13, wspace=0.26)

    ax1.plot(it, loss, color=BLUE, lw=1.6)
    ax1.set_title("Cross-entropy giảm rồi bão hòa", loc="left")
    ax1.set_xlabel("Vòng lặp GD")
    ax1.set_ylabel("J(w, b)  =  BCE")
    ax1.set_ylim(0.437, 0.725)
    ax1.text(
        0.97, 0.93,
        f"{m['initial_loss']:.4f} → {m['final_loss']:.4f}\n"
        f"hết {m['iterations']} vòng, chưa đạt 1e−8",
        transform=ax1.transAxes, ha="right", va="top",
        fontsize=12, color=INK, linespacing=1.5,
    )

    # ``predicted`` already holds the 160 held-out predictions in test order.
    Xt, yt, pt = X[test], y[test], pred
    wrong = pt != yt
    for cls, colour, label in ((0, GOOD, "Lớp 0"), (1, BAD, "Lớp 1")):
        sel = yt == cls
        ax2.scatter(
            Xt[sel, 0], Xt[sel, 1], s=34, color=colour, alpha=0.8,
            edgecolor="white", linewidth=0.6, label=label, zorder=2,
        )
    ax2.scatter(
        Xt[wrong, 0], Xt[wrong, 1], s=150, facecolor="none", edgecolor=INK,
        linewidth=1.1, label="Dự đoán sai", zorder=3,
    )
    xs = np.linspace(Xt[:, 0].min() - 0.3, Xt[:, 0].max() + 0.3, 50)
    ax2.plot(xs, -(w_raw[0] * xs + b_raw) / w_raw[1], color=INK, lw=1.4, ls="--", label="Biên p = 0.5")
    ax2.set_title("Biên quyết định trên tập test", loc="left")
    ax2.set_xlabel("Đặc trưng 1")
    ax2.set_ylabel("Đặc trưng 2")
    ax2.set_xlim(Xt[:, 0].min() - 0.4, Xt[:, 0].max() + 0.4)
    ax2.set_ylim(Xt[:, 1].min() - 0.45, Xt[:, 1].max() + 1.25)
    ax2.legend(loc="upper left", frameon=False, ncol=2, handletextpad=0.4, columnspacing=1.2)
    ax2.text(
        0.985,
        0.04,
        f"Accuracy = {acc:.4f}",
        transform=ax2.transAxes,
        ha="right",
        va="bottom",
        fontsize=12.5,
        color=INK,
    )

    fig.savefig(FIGDIR / "fig_q1_logistic.png", dpi=200)
    plt.close(fig)


# --------------------------------------------------------------- Q2 dataset
def read_arff() -> tuple[list[str], list[list[str]]]:
    names: list[str] = []
    rows: list[list[str]] = []
    in_data = False
    for line in (ROOT / "data" / "credit-g.arff").read_text(encoding="utf-8").splitlines():
        low = line.strip().lower()
        if not line.strip() or low.startswith("%"):
            continue
        if low.startswith("@attribute"):
            names.append(line.split()[1].strip("'\""))
        elif low.startswith("@data"):
            in_data = True
        elif in_data:
            rows.append([v.strip().strip("'\"") for v in line.split(",")])
    return names, rows


def fig_q2_eda() -> None:
    names, rows = read_arff()
    split = {(r["row_id"]): r["split"] for r in csv.DictReader((RESULTS / "q2_split.csv").open())}
    col = {n: i for i, n in enumerate(names)}
    dev = [r for i, r in enumerate(rows) if split[str(i)] == "development"]
    counts = {0: sum(r[col["class"]] == "good" for r in dev), 1: sum(r[col["class"]] == "bad" for r in dev)}

    audit = load_json("q2_audit.json")
    check("q2 dev good", counts[0], audit["development_class_counts"]["0"], 0.5)
    check("q2 dev bad", counts[1], audit["development_class_counts"]["1"], 0.5)

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(11.0, 3.35), gridspec_kw={"width_ratios": [1, 2.25]}
    )
    fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.19, wspace=0.22)

    bars = ax1.bar(["good (0)", "bad (1)"], [counts[0], counts[1]], color=[GOOD, BAD], width=0.62)
    ax1.set_title("Mất cân bằng lớp (n = 800)", loc="left")
    ax1.set_ylabel("Số hồ sơ")
    ax1.set_ylim(0, max(counts.values()) * 1.22)
    ax1.bar_label(bars, fontsize=12.5, padding=3, color=INK)

    for cls, label, colour in (("good", "good", GOOD), ("bad", "bad", BAD)):
        vals = np.array([float(r[col["credit_amount"]]) for r in dev if r[col["class"]] == cls])
        ax2.hist(vals, bins=np.arange(0, 16000, 500), color=colour, alpha=0.62, label=label)
    ax2.set_title("Credit amount lệch phải, hai lớp chồng lấn", loc="left")
    ax2.set_xlabel("Credit amount (đơn vị gốc)")
    ax2.set_ylabel("Số hồ sơ")
    ax2.legend(frameon=False, loc="upper right")
    ax2.set_xlim(0, 15500)

    fig.savefig(FIGDIR / "fig_q2_eda.png", dpi=200)
    plt.close(fig)


# ------------------------------------------------------- Q2 cross-validation
def fig_q2_cv() -> None:
    metrics = load_json("q2_metrics.json")
    models = metrics["models"]
    winner = metrics["winner_by_cv"]
    order = sorted(models, key=lambda m: m["cv_macro_f1"])

    fig, ax = plt.subplots(figsize=(6.5, 4.55))
    fig.subplots_adjust(left=0.335, right=0.975, top=0.93, bottom=0.135)
    ypos = np.arange(len(order))
    for i, m in enumerate(order):
        base = m["model"] == "Majority baseline"
        colour = "#c8ccd2" if base else (ORANGE if m["model"] == winner else BLUE)
        ax.barh(
            i, m["cv_macro_f1"], height=0.66, color=colour, xerr=m["cv_std"],
            error_kw={"ecolor": "#555555", "elinewidth": 0.9, "capsize": 2.2},
        )
        ax.text(
            0.79, i, f"{m['cv_macro_f1']:.3f}", va="center", ha="left",
            fontsize=10.5, color=ORANGE if m["model"] == winner else INK,
            fontweight="bold" if m["model"] == winner else "normal",
        )
    ax.set_yticks(ypos, [m["model"] for m in order], fontsize=11)
    for lbl in ax.get_yticklabels():
        if lbl.get_text() == winner:
            lbl.set_fontweight("bold")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.7, len(order) - 0.3)
    ax.set_xlabel("Macro F1 trung bình 5 fold  (± độ lệch chuẩn)")
    ax.set_title("Chọn mô hình trên tập development", loc="left")
    ax.grid(axis="x", color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)

    fig.savefig(FIGDIR / "fig_q2_cv.png", dpi=200)
    plt.close(fig)


# ------------------------------------------------------------- Q2 held-out
def fig_q2_test() -> None:
    metrics = load_json("q2_metrics.json")
    by_name = {m["model"]: m for m in metrics["models"]}
    rows = list(csv.DictReader((RESULTS / "q2_test_predictions.csv").open()))
    actual = np.array([int(r["actual_bad"]) for r in rows])

    from sklearn.metrics import roc_auc_score, roc_curve

    mlp = by_name["MLP"]
    cm = mlp["confusion_matrix"]
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(11.2, 3.35), gridspec_kw={"width_ratios": [1, 1.9]}
    )
    fig.subplots_adjust(left=0.105, right=0.985, top=0.90, bottom=0.22, wspace=0.30)

    grid = np.array(cm)
    im = ax1.imshow(grid, cmap="Blues", vmin=0, vmax=grid.max() * 1.05)
    for (i, j), val in np.ndenumerate(grid):
        ax1.text(
            j, i, f"{val}", ha="center", va="center", fontsize=19,
            color="white" if val > grid.max() * 0.55 else INK,
        )
    ax1.set_xticks([0, 1], ["good", "bad"])
    ax1.set_yticks([0, 1], ["good", "bad"])
    ax1.set_xlabel("Nhãn dự đoán")
    ax1.set_ylabel("Nhãn thật")
    ax1.set_title("MLP — ma trận nhầm lẫn (n = 200)", loc="left")
    ax1.grid(False)

    for name, colour in (("MLP", BLUE), ("Polynomial SVM", GREEN), ("Bernoulli NB", ORANGE)):
        scores = np.array([float(r[f"{name}__score"]) for r in rows])
        auc = roc_auc_score(actual, scores)
        check(f"q2 AUC {name}", auc, by_name[name]["roc_auc"])
        fpr, tpr, _ = roc_curve(actual, scores)
        ax2.plot(fpr, tpr, color=colour, lw=1.7, label=f"{name}: {auc:.3f}")
    ax2.plot([0, 1], [0, 1], color="#999999", ls="--", lw=0.9)
    ax2.set_xlabel("False positive rate")
    ax2.set_ylabel("True positive rate")
    ax2.set_title("ROC trên tập test (3 mô hình dẫn đầu)", loc="left")
    ax2.legend(loc="lower right", frameon=False, fontsize=11)
    ax2.set_xlim(-0.01, 1.01)
    ax2.set_ylim(-0.01, 1.01)

    fig.savefig(FIGDIR / "fig_q2_test.png", dpi=200)
    plt.close(fig)


# ------------------------------------------------------------- overfitting
def fig_overfit() -> None:
    with (RESULTS / "q2_tree_depth.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    depth = [r["depth"] for r in rows]
    tr = [float(r["train_macro_f1"]) for r in rows]
    cv = [float(r["cv_macro_f1"]) for r in rows]

    metrics = load_json("q2_metrics.json")
    by_name = {m["model"]: m for m in metrics["models"]}
    fams = ["Decision tree", "Bagging", "Random forest", "Gradient boosting"]

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.4, 3.5), gridspec_kw={"width_ratios": [1.25, 1]}
    )
    fig.subplots_adjust(left=0.072, right=0.985, top=0.905, bottom=0.185, wspace=0.42)

    x = np.arange(len(depth))
    ax1.plot(x, tr, "-o", color=BLUE, lw=1.8, ms=6, label="Macro F1 trên fold train")
    ax1.plot(x, cv, "-s", color=ORANGE, lw=1.8, ms=6, label="Macro F1 trên fold validation")
    ax1.set_xticks(x, ["∞" if d == "unlimited" else d for d in depth])
    ax1.set_xlabel("Độ sâu tối đa của cây")
    ax1.set_ylabel("Macro F1")
    ax1.set_ylim(0.33, 1.05)
    ax1.set_title("Cây càng sâu: train tăng, validation giảm", loc="left")
    ax1.legend(frameon=False, loc="upper left", fontsize=11)
    ax1.text(
        0.97, 0.06, "ở độ sâu không giới hạn:\ntrain 1.00 · validation 0.61",
        transform=ax1.transAxes, ha="right", va="bottom",
        fontsize=10.5, color=INK, linespacing=1.5,
    )

    base_gap = [by_name[f]["default_train_macro_f1"] - by_name[f]["default_cv_macro_f1"] for f in fams]
    sel_gap = [by_name[f]["selected_train_macro_f1"] - by_name[f]["cv_macro_f1"] for f in fams]
    ypos = np.arange(len(fams))
    ax2.barh(ypos - 0.19, base_gap, height=0.34, color="#c8ccd2")
    ax2.barh(ypos + 0.19, sel_gap, height=0.34, color=BLUE)
    for i, (b, sv) in enumerate(zip(base_gap, sel_gap)):
        tail_b = f"{b:.2f}" + ("  cấu hình gốc" if i == 0 else "")
        tail_s = f"{sv:.2f}" + ("  sau khi chọn" if i == 0 else "")
        ax2.text(b + 0.009, i - 0.19, tail_b, va="center", fontsize=10, color=MUTED)
        ax2.text(sv + 0.009, i + 0.19, tail_s, va="center", fontsize=10, color=INK)
    ax2.set_yticks(ypos, ["Cây quyết định", "Bagging", "Random forest", "Gradient boosting"], fontsize=11)
    ax2.invert_yaxis()
    ax2.set_xlim(0, 0.58)
    ax2.set_xlabel("Khoảng cách train − CV (macro F1)")
    ax2.set_title("Thu hẹp khoảng cách train − CV", loc="left")
    ax2.grid(axis="x", color="#e6e6e6", lw=0.8)
    ax2.set_axisbelow(True)

    fig.savefig(FIGDIR / "fig_overfit.png", dpi=200)
    plt.close(fig)


def main() -> None:
    fig_q1_linear()
    fig_q1_logistic()
    fig_q2_eda()
    fig_q2_cv()
    fig_q2_test()
    fig_overfit()

    print(f"{'check':38s} {'drawn':>10s} {'exported':>10s}")
    for label, got, want in CHECKS:
        print(f"{label:38s} {got:10.4f} {want:10.4f}")
    print(f"\n{len(CHECKS)} artifact checks passed; figures written to {FIGDIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
