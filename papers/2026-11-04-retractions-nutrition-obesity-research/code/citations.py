"""Step 3c: post-retraction citation counts from OpenAlex counts_by_year (citing works by their publication year, 2012-2025).
Reads data/derived/citation_dois.json and openalex.json; writes results/citations.json.
Post-retraction citations = citing works published in calendar years Y+1 to 2025, Y = retraction year (the retraction year itself
is excluded because citing works published that year may predate the notice)."""
import os, json
import numpy as np, pandas as pd
from common import *

LAST = 2025
recs = pd.DataFrame(json.load(open(os.path.join(DER, 'citation_dois.json'))))
oa = json.load(open(os.path.join(DER, 'openalex.json')))
W = oa['works']
rng = np.random.default_rng(SEED + 1)
rows = []
for d, g, y, p in recs[['doi', 'group', 'ret_year', 'pub_year']].itertuples(index=False):
    w = W.get(d)
    if w is None:
        rows.append({'group': g, 'ret_year': y, 'found': False}); continue
    cby = {int(k): v for k, v in w['counts_by_year'].items()}
    post = sum(v for k, v in cby.items() if y < k <= LAST)
    upto = sum(v for k, v in cby.items() if 2012 <= k <= y)
    yrs = LAST - y
    rows.append({'group': g, 'ret_year': y, 'pub_year': p, 'found': True, 'retracted_flag': bool(w['is_retracted']),
                 'total': w['cited_by_count'], 'post': post, 'upto': upto, 'post_years': yrs, 'rate': post / yrs,
                 'complete': (p is not None and not pd.isna(p) and p >= 2012)})
t = pd.DataFrame(rows)
f = t[t['found']]


def summ(x):
    return {'n': int(len(x)), 'retracted_flag': float(x['retracted_flag'].mean()), 'any_post': float((x['post'] > 0).mean()),
            'post_ge5': float((x['post'] >= 5).mean()), 'post_sum': int(x['post'].sum()), 'post_median': float(x['post'].median()),
            'post_mean': float(x['post'].mean()), 'rate_mean': float(x['rate'].mean()), 'rate_median': float(x['rate'].median()),
            'total_median': float(x['total'].median()),
            'post_share_complete': (float(x.loc[x['complete'], 'post'].sum() / (x.loc[x['complete'], 'post'].sum() + x.loc[x['complete'], 'upto'].sum()))
                                    if x['complete'].any() else None),
            'n_complete': int(x['complete'].sum())}


def boot(a, b, fn, B=2000):
    est = fn(a) - fn(b); d = np.empty(B)
    for i in range(B):
        d[i] = fn(a.iloc[rng.integers(0, len(a), len(a))]) - fn(b.iloc[rng.integers(0, len(b), len(b))])
    return {'diff': float(est), 'lo': float(np.percentile(d, 2.5)), 'hi': float(np.percentile(d, 97.5))}


def ratio_boot(a, b, B=2000):
    est = a['rate'].mean() / b['rate'].mean(); d = np.empty(B)
    for i in range(B):
        d[i] = a['rate'].iloc[rng.integers(0, len(a), len(a))].mean() / b['rate'].iloc[rng.integers(0, len(b), len(b))].mean()
    return {'ratio': float(est), 'lo': float(np.percentile(d, 2.5)), 'hi': float(np.percentile(d, 97.5))}


A, Bc = f[f['group'] == 'field'], f[f['group'] == 'comparison']
res = {'n_requested': {g: int((t['group'] == g).sum()) for g in ['field', 'comparison']},
       'n_found': {g: int((f['group'] == g).sum()) for g in ['field', 'comparison']},
       'skipped_bad_doi': oa['skipped'], 'failed': len(oa['failed']), 'retrieved': oa['retrieved'], 'last_year': LAST,
       'field': summ(A), 'comparison': summ(Bc),
       'diff_any_post': boot(A, Bc, lambda x: (x['post'] > 0).mean()),
       'rate_ratio': ratio_boot(A, Bc),
       'diff_retracted_flag': boot(A, Bc, lambda x: x['retracted_flag'].mean())}
res['by_period'] = {}
for nm, (lo, hi) in {'2012_2017': (2012, 2017), '2018_2023': (2018, 2023)}.items():
    a, b = A[A['ret_year'].between(lo, hi)], Bc[Bc['ret_year'].between(lo, hi)]
    res['by_period'][nm] = {'field': summ(a), 'comparison': summ(b), 'rate_ratio': ratio_boot(a, b)}
# citations per year by years since retraction (field and comparison), for the figure
k = {}
for g in ['field', 'comparison']:
    acc = {}
    for d, gg, y in recs[['doi', 'group', 'ret_year']].itertuples(index=False):
        if gg != g or d not in W: continue
        cby = {int(a): v for a, v in W[d]['counts_by_year'].items()}
        for yr in range(max(2012, y - 5), LAST + 1):
            s = yr - y
            acc.setdefault(s, []).append(cby.get(yr, 0))
    k[g] = {str(s): {'n': len(v), 'mean': float(np.mean(v))} for s, v in sorted(acc.items())}
res['mean_by_years_since'] = k
dump(res, 'citations.json')
print('citations', res['n_found'])
