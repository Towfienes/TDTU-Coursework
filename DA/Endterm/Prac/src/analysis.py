"""Small shared operations; the notebook shows the assignment's Pandas steps."""
import json

import numpy as np
import pandas as pd

BANDS = ["0–9", "10–14", "15–20"]
RAW_COLUMNS = "school sex age address famsize Pstatus Medu Fedu Mjob Fjob reason guardian traveltime studytime failures schoolsup famsup paid activities nursery higher internet romantic famrel freetime goout Dalc Walc health absences G1 G2 G3".split()
NUMERIC_COLUMNS = "age Medu Fedu traveltime studytime failures famrel freetime goout Dalc Walc health absences G1 G2 G3".split()


def performance_bands(grades):
    """Analyst-defined bands, not an official grading policy."""
    if grades.isna().any() or not grades.between(0, 20).all():
        raise ValueError("Grades must be complete and lie in [0, 20].")
    return pd.cut(grades, [-1, 9, 14, 20], labels=BANDS, ordered=True)


def normalize_within_group(frame, group="school", column="G3"):
    """Relative group scale; a constant group is assigned zero."""
    if frame[[group, column]].isna().any().any():
        raise ValueError("Group normalization requires complete group/value columns.")
    if not np.isfinite(frame[column]).all():
        raise ValueError("Normalization values must be finite.")
    grouped = frame.groupby(group, observed=True)[column]
    low = grouped.transform("min")
    span = grouped.transform("max") - low
    return (frame[column] - low).div(span.where(span.ne(0), 1))


def comprehensive_report(frame):
    """Display and return a JSON-safe summary without reading files/global data."""
    required = {"G1", "G2", "G3", "performance_band"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing required columns: {sorted(required - set(frame.columns))}")
    total = len(frame)
    counts = frame["performance_band"].value_counts().reindex(BANDS, fill_value=0)
    distribution = {
        band: {"count": int(count), "percent": float(100 * count / total) if total else 0.0}
        for band, count in counts.items()
    }
    summary = {
        "total_records": total,
        "total_columns": len(frame.columns),
        "missing_by_column": {name: int(value) for name, value in frame.isna().sum().items()},
        "grade_statistics": json.loads(frame[["G1", "G2", "G3"]].agg(["count", "mean", "std", "min", "median", "max"]).to_json()),
        "performance_distribution": distribution,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False))
    return summary
