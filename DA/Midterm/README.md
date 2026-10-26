# Social-Media Sentiment Analysis for a New F&B Product Launch

Midterm project, **Data Analysis and Visualization** (Ton Duc Thang University, 2026).
Group **VibeCoding_Expert**: Ngo Lam Tien (524H0195, leader), Nguyen Cong Thanh (524H0191),
Nguyen Le Nhat Tam (524H0186), Ngo Binh Minh (524H0169). Lecturer: Ho Thi Linh, Ph.D.

The marketing team of an F&B brand asks whether the campaign message should change after a launch week with
mixed reactions. We answer with descriptive, diagnostic, predictive and prescriptive analytics on the
Sentiment140 dataset (1.6 million tweets, 2009), using food-and-drink tweets as a proxy for the brand's
category conversation.

## Contents

| Path | What it is |
|---|---|
| `report/VibeCoding_Expert_Midterm_Report.docx` (+ `.pdf`) | Written report (TDTU template, 8 chapters + references) |
| `slides/VibeCoding_Expert_Midterm_Slides.pptx` (+ `.pdf`) | Presentation, 16 slides + 3 appendix slides, with speaker notes |
| `notebooks/VibeCoding_Expert_Midterm.ipynb` | Full analysis, executed, with outputs and step-by-step comments |
| `dashboard/app.py` | Interactive Streamlit dashboard |
| `data/processed/` | Scored F&B tweets (`fnb_scored.parquet`) and daily shares, used by the dashboard |
| `artifacts/` | Fitted models (`model_lr.joblib`, `model_nb.joblib`), `key_numbers.json`, result tables (CSV) |
| `figures/` | All report figures (PNG, 200 dpi) |
| `validation/` | 210-tweet review sample of the F&B dictionary (AI-assisted, single reviewer) |
| `HuongDan_GiaiThich_ChiTiet.docx` | Vietnamese study guide for the team: methods explained, Q&A preparation, presentation script |
| `archive/` | Raw data - **not included** (239 MB), see below |

## How to run

1. Install Python 3.12, then from this folder: `pip install -r requirements.txt`
2. **Dashboard** (needs only the files already in `data/processed/` and `artifacts/`):
   `python -m streamlit run dashboard/app.py`, then open http://localhost:8501
   (use `python -m` so that the same Python that has the libraries installed runs the app).
   Add `?tab=Try+the+model` to the address to open the live prediction tab directly.
3. **Notebook** (re-creates every number, figure, table and model):
   - download `training.1600000.processed.noemoticon.csv` from
     https://www.kaggle.com/datasets/kazanova/sentiment140 and place it in `archive/`;
   - open `notebooks/VibeCoding_Expert_Midterm.ipynb` and *Run All* (about 6-10 minutes with 16 GB RAM), or run
     `jupyter nbconvert --to notebook --execute --inplace notebooks/VibeCoding_Expert_Midterm.ipynb`;
   - set `FAST_MODE = True` in the setup cell for a quick test on a 10% sample (numbers will then differ slightly).

All numbers quoted in the report and slides are read from `artifacts/key_numbers.json`, which the notebook writes.

## Main results

- Data: the raw file contains a collection artifact (no positive tweets after 16 June 08:40; 275,225 negative-only
  rows removed). Clean corpus 1,274,034 tweets; F&B stream 84,632 tweets (dictionary precision 89.0%).
- Descriptive: F&B tweets are 5.1 pp less negative than all tweets; launch week looks like any other week.
- Diagnostic: availability (+45.3 pp), price (+5.6 pp) and service (+5.4 pp, +10.2 pp in the evening) go with
  negative tweets; trying and sharing go with positive ones; launch week did not change the lift (H4, p = 0.37).
- Predictive (time-based split): Logistic Regression on word and word-pair TF-IDF, AUC 0.896 on the unseen week,
  vs 0.846 for the Naive Bayes baseline (McNemar gain +4.4 pp).
- Prescriptive: keep the core message, make targeted adjustments on availability, service and price, build the
  creative around trying and sharing, and monitor daily with an alert limit of +1.5 pp.
