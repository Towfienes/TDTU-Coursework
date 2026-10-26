# OpenML dataset provenance

Official dataset: **credit-g**, OpenML ID **31**, version **1**, default target **class**, downloaded **2026-10-14**. The experiment uses the supplied labels `good` and `bad` and preserves all 1,000 records.

- Dataset page: <https://www.openml.org/d/31>
- Metadata: <https://www.openml.org/api/v1/json/data/31>
- Feature schema: <https://www.openml.org/api/v1/json/data/features/31>
- Original ARFF: <https://openml.org/data/v1/download/31/credit-g.arff>
- Creator credited by metadata: Dr. Hans Hofmann. Licence field: Public.

| Local file | SHA-256 |
|---|---|
| credit-g.arff | 768be84ef749110d5fcac109a6541f2df190e8c6987e1dc432c0a4f29d0642f5 |
| credit-g.metadata.json | 0a42592519aeb3f473eac041a5b65c9054d46cf94665c489386dbe3371348f6a |
| credit-g.features.json | e3a0b4a20bb3cd8c2e9061261a42a8950ee299c76024d823d3df246cc32fa933 |

The ARFF MD5 is **9a475053fed0c26ee95cd4525e50074c**, matching the official metadata. No locally generated replacement data or alternate labels are used for Question 2. The synthetic data for Question 1 are separate and saved in `../results/q1_*_data.npz`.

The raw dataset and the metadata are unchanged after download; cleaning checks and train-only transformations are performed by the experiment runner. Saved split row IDs are zero-based positions in the original ARFF.
