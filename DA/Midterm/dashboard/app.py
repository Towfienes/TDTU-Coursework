"""F&B Launch Social-Listening Dashboard (Streamlit).

Run from the Midterm folder:   streamlit run dashboard/app.py
Needs the files produced by notebooks/VibeCoding_Expert_Midterm.ipynb (Section 11):
  data/processed/fnb_scored.parquet, data/processed/daily_negative_share.csv,
  artifacts/model_lr.joblib, artifacts/key_numbers.json
"""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
st.set_page_config(page_title='F&B Launch Listening', page_icon=':coffee:', layout='wide')

# ---------------------------------------------------------------------------
# Colours: the same roles as in the report
# ---------------------------------------------------------------------------
POS, NEG, AQUA, GRAY, LIGHT, INK = '#2a78d6', '#eb6834', '#1baf7a', '#898781', '#c9c7bf', '#52514e'
CAT_ORDER = ['Meals & hunger', 'Coffee & tea', 'Sweets & desserts', 'Dishes', 'Drinks', 'Chains & brands']
CAT_COLORS = dict(zip(CAT_ORDER, ['#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']))
PRODUCT = ['Taste & quality', 'Price & value', 'Service & wait', 'Availability', 'Novelty & trial']
CONTEXT = ['Hunger & cravings', 'Health & diet', 'Morning caffeine', 'Social occasions']
ASPECTS = PRODUCT + CONTEXT
DAYPARTS = ['Night (0-5h)', 'Morning (6-11h)', 'Afternoon (12-17h)', 'Evening (18-23h)']
PERIODS = ['Baseline', 'Launch week', 'Next week']
DIVERGING = [[0, '#184f95'], [0.25, POS], [0.5, '#f0efec'], [0.75, NEG], [1, '#a63c12']]


def style(fig, height=360):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=50, b=10), font=dict(family='Segoe UI, sans-serif', size=12),
                      title_font=dict(size=15), plot_bgcolor='white', paper_bgcolor='white',
                      legend=dict(orientation='h', yanchor='bottom', y=1.0, xanchor='left', x=0, title=None))
    fig.update_xaxes(showgrid=True, gridcolor='#e1e0d9', linecolor='#c3c2b7')
    fig.update_yaxes(showgrid=True, gridcolor='#e1e0d9', linecolor='#c3c2b7')
    return fig


# ---------------------------------------------------------------------------
# Data and model (cached)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    f = pd.read_parquet(ROOT / 'data/processed/fnb_scored.parquet')
    f['date'] = pd.to_datetime(f['date'])
    daily = pd.read_csv(ROOT / 'data/processed/daily_negative_share.csv', parse_dates=['date'])
    key = json.loads((ROOT / 'artifacts/key_numbers.json').read_text(encoding='utf-8'))
    return f, daily, key


@st.cache_resource
def load_model():
    return joblib.load(ROOT / 'artifacts/model_lr.joblib')


fnb, daily, KEY = load_data()
bundle = load_model()
pipe, THR = bundle['pipeline'], bundle['threshold']

# ---------------------------------------------------------------------------
# Filters (one place, they scope every chart)
# ---------------------------------------------------------------------------
st.sidebar.header('Filters')
d0, d1 = fnb['date'].min().date(), fnb['date'].max().date()
dates = st.sidebar.slider('Date range (2009)', min_value=d0, max_value=d1, value=(d0, d1), format='DD MMM')
periods = st.sidebar.multiselect('Period', PERIODS, default=PERIODS)
cats = st.sidebar.multiselect('F&B category', CAT_ORDER, default=CAT_ORDER)
aspect_sel = st.sidebar.multiselect('Aspect (any of)', ASPECTS, default=[], help='Leave empty to keep all tweets')
brand_list = sorted({b for s in fnb['brands'] if s for b in s.split(', ')})
brand_sel = st.sidebar.multiselect('Brand', brand_list, default=[])
source = st.sidebar.radio('Sentiment source', ['Emoticon label (true)', 'Model prediction'],
                          help='Model prediction shows what the team would see in real time, without labels.')
st.sidebar.caption(f"Model: TF-IDF + Logistic Regression, threshold {THR:.2f}, trained on 6 Apr - 31 May 2009.")

mask = (fnb['date'].dt.date.between(*dates) & fnb['period'].isin(periods) & fnb['category'].isin(cats))
if aspect_sel:
    mask &= fnb[aspect_sel].any(axis=1)
if brand_sel:
    mask &= fnb['brands'].apply(lambda s: any(b in s.split(', ') for b in brand_sel) if s else False)
view = fnb[mask].copy()
view['is_neg'] = view['neg'] if source.startswith('Emoticon') else view['pred_neg']

st.title('F&B Launch Social-Listening Dashboard')
st.caption('Proxy data: food-and-drink tweets from Sentiment140 (Apr-Jun 2009). Launch week = 1-7 Jun, next week = 14-16 Jun. '
           'Group VibeCoding_Expert, Data Analysis and Visualization midterm.')
if view.empty:
    st.warning('No tweets match the filters.')
    st.stop()

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
n, neg_share = len(view), view['is_neg'].mean()
use_true = source.startswith('Emoticon')
all_fnb_neg = fnb['neg'].mean() if use_true else fnb['pred_neg'].mean()
daily['neg_ref'] = daily['neg_all'] if use_true else daily['neg_all_pred']   # compare like with like
day_all = daily.set_index('date')['neg_ref']
lift = 100 * (neg_share - day_all.reindex(view['date']).mean())
q = view['pred_neg'].mean()
tpr, fpr = KEY['val_fnb_tpr'], KEY['val_fnb_fpr']
adj = float(np.clip((q - fpr) / (tpr - fpr), 0, 1))
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('F&B tweets', f'{n:,}', help='Tweets matching the filters')
gap = 100 * (neg_share - all_fnb_neg)
c2.metric('Negative share', f'{neg_share:.1%}', f'{gap:+.1f} pp vs all F&B' if abs(gap) >= 0.05 else None,
          delta_color='inverse', help='Share of negative tweets in the current filter')
c3.metric('Lift vs all tweets, same days', f'{lift:+.1f} pp', help='Negative share minus that of all tweets on the same days')
c4.metric('Model estimate (adjusted)', f'{adj:.1%}', help='Adjusted classify-and-count: (predicted share - FPR) / (TPR - FPR)')
c5.metric('Alert limit (daily lift)', f"{KEY['alert_ucl_pp']:+.1f} pp", help='Baseline mean + 2 SD, on days with at least 200 F&B tweets')

TAB_NAMES = ['Overview', 'Aspects', 'Brands', 'Tweet explorer', 'Try the model']
start_tab = st.query_params.get('tab', 'Overview')          # e.g. ?tab=Try+the+model opens that tab directly
tab1, tab2, tab3, tab4, tab5 = st.tabs(TAB_NAMES, default=start_tab if start_tab in TAB_NAMES else 'Overview')

# ---------------------------------------------------------------------------
# Tab 1: overview
# ---------------------------------------------------------------------------
with tab1:
    left, right = st.columns([3, 2])
    d = view.groupby('date').agg(n=('is_neg', 'size'), neg=('is_neg', 'mean')).reset_index()
    cal = pd.DataFrame({'date': pd.date_range(fnb['date'].min(), fnb['date'].max())})
    d = cal.merge(d, on='date', how='left').merge(daily[['date', 'neg_ref']], on='date', how='left')
    fig = go.Figure()
    fig.add_scatter(x=d['date'], y=100 * d['neg_ref'], name='All tweets', mode='lines+markers', line=dict(color=INK, width=2),
                    connectgaps=False, hovertemplate='%{x|%d %b}: %{y:.1f}%<extra>All tweets</extra>')
    fig.add_scatter(x=d['date'], y=100 * d['neg'], name='Filtered F&B tweets', mode='lines+markers',
                    line=dict(color=AQUA, width=2.5), connectgaps=False, customdata=d['n'],
                    hovertemplate='%{x|%d %b}: %{y:.1f}% (n=%{customdata:.0f})<extra>F&B</extra>')
    for x0, x1, label in [('2009-06-01', '2009-06-08', 'Launch week'), ('2009-06-14', '2009-06-17', 'Next week')]:
        fig.add_vrect(x0=x0, x1=x1, fillcolor=LIGHT, opacity=0.25, line_width=0, annotation_text=label,
                      annotation_position='top left')
    fig.update_layout(title='Daily negative share (gaps = days with no data)', yaxis_title='Negative tweets (%)',
                      xaxis_title='Date (2009, PDT)')
    left.plotly_chart(style(fig, 380), width='stretch')

    share = view['category'].value_counts().reindex(CAT_ORDER).dropna()
    fig = go.Figure(go.Pie(labels=share.index, values=share.values, hole=0.55, sort=False,
                           marker=dict(colors=[CAT_COLORS[c] for c in share.index], line=dict(color='white', width=2)),
                           textinfo='percent', hovertemplate='%{label}: %{value:,} tweets (%{percent})<extra></extra>'))
    fig.update_layout(title='Share of voice by F&B category')
    fig = style(fig, 380)
    fig.update_layout(legend=dict(orientation='v', yanchor='middle', y=0.5, xanchor='left', x=1.0))
    right.plotly_chart(fig, width='stretch')

    left, right = st.columns([2, 3])
    funnel = pd.DataFrame({'stage': ['F&B mentions', 'Product-directed aspect', 'Negative product talk'],
                           'n': [len(view), int(view[PRODUCT].any(axis=1).sum()),
                                 int((view[PRODUCT].any(axis=1) & (view['is_neg'] == 1)).sum())]})
    fig = go.Figure(go.Funnel(y=funnel['stage'], x=funnel['n'], textinfo='value+percent initial',
                              marker=dict(color=[LIGHT, AQUA, NEG])))
    fig.update_layout(title='Listening funnel: from mentions to product complaints')
    left.plotly_chart(style(fig, 340), width='stretch')

    dd = view.groupby(['date', 'category']).agg(n=('is_neg', 'size'), neg=('is_neg', 'mean')).reset_index()
    dd = dd[dd['n'] >= 30]
    fig = px.box(dd, x='category', y=dd['neg'] * 100, color='category', color_discrete_map=CAT_COLORS,
                 category_orders={'category': CAT_ORDER}, points='outliers')
    fig.update_layout(title='Day-to-day spread of negative share by category (days with >= 30 tweets)',
                      yaxis_title='Negative tweets per day (%)', xaxis_title='F&B category', showlegend=False)
    right.plotly_chart(style(fig, 340), width='stretch')

# ---------------------------------------------------------------------------
# Tab 2: aspects
# ---------------------------------------------------------------------------
with tab2:
    rows = []
    for a in ASPECTS:
        m = view[a]
        if m.sum() < 30:
            continue
        p = view.loc[m, 'is_neg'].mean()
        se = np.sqrt(p * (1 - p) / m.sum())
        rows.append({'aspect': a, 'group': 'Product-directed' if a in PRODUCT else 'Context', 'n': int(m.sum()),
                     'neg': 100 * p, 'err': 196 * se, 'lift': 100 * (p - view.loc[~m, 'is_neg'].mean())})
    asp = pd.DataFrame(rows)
    left, right = st.columns(2)
    if not asp.empty:
        asp = asp.sort_values('neg')
        fig = px.scatter(asp, x='neg', y='aspect', error_x='err', color='group',
                         color_discrete_map={'Product-directed': AQUA, 'Context': GRAY},
                         hover_data={'n': ':,', 'lift': ':+.1f', 'err': False})
        fig.add_vline(x=100 * view['is_neg'].mean(), line_color=INK, line_width=1)
        fig.update_traces(marker=dict(size=11))
        fig.update_layout(title='Negative share by aspect (95% CI)', xaxis_title='Negative tweets (%)', yaxis_title='Aspect')
        left.plotly_chart(style(fig, 420), width='stretch')

        flows = []
        for a in asp['aspect']:
            m = view[a]
            flows += [(a, 'Negative', int((m & (view['is_neg'] == 1)).sum())), (a, 'Positive', int((m & (view['is_neg'] == 0)).sum()))]
        labels = list(asp['aspect']) + ['Negative', 'Positive']
        idx = {l: i for i, l in enumerate(labels)}
        node_colors = [AQUA if l in PRODUCT else GRAY for l in asp['aspect']] + [NEG, POS]
        fig = go.Figure(go.Sankey(node=dict(label=labels, color=node_colors, pad=12, thickness=14),
                                  link=dict(source=[idx[s] for s, _, _ in flows], target=[idx[t] for _, t, _ in flows],
                                            value=[v for _, _, v in flows],
                                            color=['rgba(235,104,52,0.35)' if t == 'Negative' else 'rgba(42,120,214,0.25)'
                                                   for _, t, _ in flows])))
        fig.update_layout(title='Where each aspect flows: negative vs positive tweets')
        right.plotly_chart(style(fig, 420), width='stretch')

    base = view.groupby('daypart')['is_neg'].mean()
    heat = pd.DataFrame(index=ASPECTS, columns=DAYPARTS, dtype=float)
    for a in ASPECTS:
        g = view[view[a]].groupby('daypart')['is_neg'].agg(['mean', 'size'])
        for dp in DAYPARTS:
            if dp in g.index and g.loc[dp, 'size'] >= 50:
                heat.loc[a, dp] = 100 * (g.loc[dp, 'mean'] - base[dp])
    lim = np.nanmax(np.abs(heat.to_numpy())) if heat.notna().any().any() else 1
    fig = px.imshow(heat, color_continuous_scale=DIVERGING, zmin=-lim, zmax=lim, text_auto='+.1f', aspect='auto')
    fig.update_layout(title='Negative lift by aspect and time of day (pp vs all filtered tweets in the same daypart; blank = n < 50)',
                      xaxis_title='Time of day (PDT)', yaxis_title='Aspect', coloraxis_colorbar=dict(title='pp'))
    st.plotly_chart(style(fig, 420), width='stretch')

# ---------------------------------------------------------------------------
# Tab 3: brands
# ---------------------------------------------------------------------------
with tab3:
    b = view[view['brands'] != ''].assign(brand=lambda x: x['brands'].str.split(', ')).explode('brand')
    if b.empty:
        st.info('No brand mentions in the current filter.')
    else:
        bs = b.groupby('brand').agg(mentions=('is_neg', 'size'), neg=('is_neg', 'mean')).reset_index()
        left, right = st.columns(2)
        top = bs.sort_values('mentions', ascending=False).head(15)
        top['err'] = 196 * np.sqrt(top['neg'] * (1 - top['neg']) / top['mentions'])
        top = top.sort_values('neg')
        fig = px.scatter(top, x=top['neg'] * 100, y='brand', error_x='err', size='mentions', size_max=22,
                         hover_data={'mentions': ':,'})
        fig.update_traces(marker=dict(color=AQUA, line=dict(color='white', width=1.5)))
        fig.add_vline(x=100 * view['is_neg'].mean(), line_color=INK, line_width=1)
        fig.update_layout(title='Negative share of the 15 most-mentioned brands (95% CI, size = mentions)',
                          xaxis_title='Negative tweets (%)', yaxis_title='Brand')
        left.plotly_chart(style(fig, 460), width='stretch')

        cat_of = b.groupby('brand')['category'].agg(lambda s: s.mode().iloc[0])
        bs['category'] = bs['brand'].map(cat_of)
        fig = px.treemap(bs, path=[px.Constant('Brand mentions'), 'category', 'brand'], values='mentions',
                         color=bs['neg'] * 100, color_continuous_scale=DIVERGING,
                         range_color=[100 * view['is_neg'].mean() - 25, 100 * view['is_neg'].mean() + 25])
        fig.update_traces(hovertemplate='%{label}: %{value:,} mentions, %{color:.1f}% negative<extra></extra>')
        fig.update_layout(title='Brand mentions by category (colour = negative share, %)', coloraxis_colorbar=dict(title='% neg'))
        right.plotly_chart(style(fig, 460), width='stretch')

# ---------------------------------------------------------------------------
# Tab 4: tweet explorer
# ---------------------------------------------------------------------------
with tab4:
    query = st.text_input('Search the tweets (case-insensitive)', '')
    t = view if not query else view[view['text_disp'].str.contains(query, case=False, regex=False)]
    st.caption(f'{len(t):,} tweets; showing the 300 most recent.')
    st.dataframe(t.sort_values('dt', ascending=False).head(300)[['dt', 'category', 'brands', 'label', 'proba_neg', 'text_disp']]
                 .rename(columns={'dt': 'Time', 'category': 'Category', 'brands': 'Brands', 'label': 'Emoticon label',
                                  'proba_neg': 'P(negative)', 'text_disp': 'Tweet'}),
                 hide_index=True, width='stretch',
                 column_config={'P(negative)': st.column_config.ProgressColumn(min_value=0, max_value=1, format='%.2f')})

# ---------------------------------------------------------------------------
# Tab 5: live prediction with an explanation
# ---------------------------------------------------------------------------
with tab5:
    st.write('Type a tweet. The model returns the probability that it is negative and shows which words drove the score '
             '(coefficient x TF-IDF weight, in log-odds).')
    text = st.text_area('Tweet', "the new iced latte is not bad but the line was so long and they ran out of cups")
    if text.strip():
        import html as _html
        import re as _re
        t = _html.unescape(text)
        t = _re.sub(r'https?://\S+|www\.\S+', ' _url_ ', t)
        t = _re.sub(r'@\w+', ' _user_ ', t).lower()
        t = _re.sub(r'([a-z])\1{2,}', r'\1\1', t)
        t = _re.sub(r'\s+', ' ', t).strip()
        tf, clf = pipe.named_steps['tfidf'], pipe.named_steps['clf']
        x = tf.transform([t])
        p = float(clf.predict_proba(x)[0, 1])
        label = 'Negative' if p >= THR else 'Not negative'
        a, b_ = st.columns([1, 2])
        a.metric('P(negative)', f'{p:.2f}')
        a.metric('Label at threshold', label)
        vocab = tf.get_feature_names_out()
        contrib = pd.DataFrame({'term': vocab[x.indices], 'contribution': x.data * clf.coef_[0][x.indices]})
        contrib = contrib.reindex(contrib['contribution'].abs().sort_values(ascending=False).index).head(12)
        contrib = contrib.sort_values('contribution')
        fig = go.Figure(go.Bar(x=contrib['contribution'], y=contrib['term'], orientation='h',
                               marker_color=[NEG if v > 0 else POS for v in contrib['contribution']]))
        fig.update_layout(title='Term contributions (right = towards negative)', xaxis_title='Log-odds contribution',
                          yaxis_title='Term')
        b_.plotly_chart(style(fig, 380), width='stretch')
