"""Official OpenML acquisition, immutable raw bytes, and offline verification."""

from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import platform
import urllib.request
import numpy as np
import pandas as pd
import scipy
import sklearn
from scipy.io import arff

ROOT = Path(__file__).resolve().parents[1]
DATA_ID, VERSION = 31, 1
API_URL = "https://www.openml.org/api/v1/json/data/31"
NUMERIC = [
    "duration",
    "credit_amount",
    "installment_commitment",
    "residence_since",
    "age",
    "existing_credits",
    "num_dependents",
]


def load_data(root=ROOT):
    raw = root / "data/raw/credit-g.arff"
    payload = raw.read_bytes()
    official = json.loads((root / "data/metadata/openml_31_response.json").read_text())[
        "data_set_description"
    ]
    if (
        int(official["id"]) != DATA_ID
        or int(official["version"]) != VERSION
        or official["name"] != "credit-g"
    ):
        raise ValueError("Unexpected official dataset identity")
    if hashlib.md5(payload).hexdigest() != official["md5_checksum"]:
        raise ValueError("Raw artifact does not match official OpenML MD5")
    if (root / "data/metadata/provenance.json").exists():
        provenance = json.loads((root / "data/metadata/provenance.json").read_text())
        if hashlib.sha256(payload).hexdigest() != provenance["raw_sha256"]:
            raise ValueError("Raw artifact does not match recorded SHA-256")
    records, schema = arff.loadarff(raw)
    df = pd.DataFrame(records)
    for col in df.select_dtypes(include=["object"]):
        df[col] = df[col].map(
            lambda value: value.decode("utf-8") if isinstance(value, bytes) else value
        )
    if df.shape != (1000, 21) or set(df["class"].unique()) != {"good", "bad"}:
        raise ValueError("Unexpected credit-g schema/target")
    if not np.isfinite(df[NUMERIC].to_numpy()).all() or df.isna().any().any():
        raise ValueError(
            "Unexpected missing or nonfinite raw values; investigate without silently cleaning"
        )
    categorical = [c for c in df.columns if c not in NUMERIC + ["class"]]
    for col in categorical + ["class"]:
        if not set(df[col]).issubset(set(schema[col][1])):
            raise ValueError(f"Invalid nominal value in {col}")
    return df


def acquire(root=ROOT):
    """Fetch official API metadata and ARFF; never silently replace a changed cache."""
    meta_bytes = urllib.request.urlopen(API_URL, timeout=45).read()
    official = json.loads(meta_bytes)["data_set_description"]
    if (int(official["id"]), int(official["version"]), official["name"]) != (
        DATA_ID,
        VERSION,
        "credit-g",
    ):
        raise ValueError("Unexpected OpenML identity")
    payload = urllib.request.urlopen(official["url"], timeout=60).read()
    if hashlib.md5(payload).hexdigest() != official["md5_checksum"]:
        raise ValueError("Downloaded ARFF fails official MD5")
    raw = root / "data/raw/credit-g.arff"
    if raw.exists() and raw.read_bytes() != payload:
        raise ValueError(
            "Official download differs from cache; preserve and investigate"
        )
    raw.parent.mkdir(parents=True, exist_ok=True)
    meta = root / "data/metadata"
    meta.mkdir(parents=True, exist_ok=True)
    raw.write_bytes(payload)
    (meta / "openml_31_response.json").write_bytes(meta_bytes)
    df = load_data(root)
    provenance = dict(
        status="VERIFIED",
        official_url="https://www.openml.org/d/31",
        api_url=API_URL,
        raw_download_url=official["url"],
        dataset_id=DATA_ID,
        dataset_version=VERSION,
        dataset_name=official["name"],
        license=official["licence"],
        rows=len(df),
        feature_count=20,
        target="class",
        class_counts={k: int(v) for k, v in df["class"].value_counts().items()},
        numerical_features=NUMERIC,
        categorical_features=[c for c in df.columns if c not in NUMERIC + ["class"]],
        retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
        retrieval_method="urllib.request.urlopen: official OpenML v1 JSON API, then API-provided ARFF URL; scipy.io.arff parser",
        raw_sha256=hashlib.sha256(payload).hexdigest(),
        raw_md5=hashlib.md5(payload).hexdigest(),
        official_md5=official["md5_checksum"],
        bytes=len(payload),
        software=dict(
            python=platform.python_version(),
            numpy=np.__version__,
            pandas=pd.__version__,
            scipy=scipy.__version__,
            sklearn=sklearn.__version__,
        ),
    )
    (meta / "provenance.json").write_text(json.dumps(provenance, indent=2))
    print(json.dumps(provenance, indent=2))
    return provenance


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    if parser.parse_args().download:
        acquire()
    else:
        df = load_data()
        print("VERIFIED cached official OpenML artifact:", df.shape)
