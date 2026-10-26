# Dataset provenance — Q2

- Registered dataset: OpenML `iris`, ID **61**, version **1**.
- OpenML page: <https://www.openml.org/d/61>
- Dataset description: 150 flower samples, 4 numeric measurements (sepal and petal dimensions), 3 Iris species labels. Cited source: R. A. Fisher, 1936.
- Packaged CSV: `iris_openml_61_offline_mirror.csv`, built with scikit-learn's `load_iris`, a bundled local copy of Fisher's Iris data. **This is an offline mirror, not proof of a completed OpenML download.**
- Data cleaning used in this submission: one exact duplicate row removed, yielding 149 rows; no missing numeric entries in the raw mirror.
- To run against the source via a real network request: `python -m src.q2_classification --use-openml-live` from the project root. A network failure produces a deliberate error; it does not silently switch the source.

The assignment asks for a classification dataset from OpenML. Fisher's Iris is registered in OpenML as ID 61; this offline execution uses the corresponding locally bundled Fisher Iris dataset and transparently records that distinction.
