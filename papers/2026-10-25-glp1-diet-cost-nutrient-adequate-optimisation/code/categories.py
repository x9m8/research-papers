"""Collapse the observed basket into WWEIA food categories (TFP-style composites): composite nutrients and price per 100 g, weighted by the grams
eaten by eligible adults of each sex; acceptability bounds = survey-weighted 95th percentile of each person's two-day mean intake of the category."""
import json, numpy as np, pandas as pd
from common import *
B = pd.read_csv(f'{RES}/basket.csv'); E = pd.read_csv(f'{ROOT}/data/eligible_P.csv')
f1 = pd.read_csv(f'{RAW}/p_dr1iff.csv'); f2 = pd.read_csv(f'{RAW}/p_dr2iff.csv')[['SEQN', 'code', 'g']]
F = pd.concat([f1, f2]); F = F[F.SEQN.isin(E.SEQN)].rename(columns={'code': 'Food code'})
F = F.merge(B[['Food code', 'WWEIA Category number', 'WWEIA Category description']], on='Food code', how='left')
NUT = [c for c in B.columns if pd.api.types.is_numeric_dtype(B[c]) and c not in ('Food code', 'WWEIA Category number', 'x0_M', 'x0_F', 'eat_M', 'eat_F', 'price_100gm', 'price_100g_2026', 'price_imputed')]
def wq(x, w, q):
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w) / w.sum(); return float(x[np.searchsorted(c, q)])
rows = []
for s in 'MF':
    Es = E[E.sex == s]; W = Es.w.sum()
    pc = F[F.SEQN.isin(Es.SEQN)].groupby(['SEQN', 'WWEIA Category number']).g.sum().div(2).unstack(fill_value=0)
    pc = pc.reindex(Es.SEQN, fill_value=0); ww = Es.set_index('SEQN').w.reindex(pc.index).values
    for cat, g in B[B[f'x0_{s}'] > 0].groupby('WWEIA Category number'):
        x = g[f'x0_{s}'].values; tot = x.sum()
        row = dict(sex=s, cat=int(cat), desc=g['WWEIA Category description'].iloc[0], t=tot, p95=wq(pc[cat].values, ww, 0.95) if cat in pc else 0.0,
                   p99=wq(pc[cat].values, ww, 0.99) if cat in pc else 0.0, n_foods=len(g),
                   eat=float(np.sum(ww * (pc[cat].values > 0)) / ww.sum()) if cat in pc else 0.0)
        ok = g.price_100g_2026.notna().values
        row['price_100g'] = float(np.sum(x[ok] * g.price_100g_2026.values[ok]) / x[ok].sum()) if ok.any() else np.nan
        for c in NUT: row[c] = float(np.sum(x * g[c].fillna(0).values) / tot)
        rows.append(row)
C = pd.DataFrame(rows); C.to_csv(f'{RES}/categories.csv', index=False)
print(C.groupby('sex').size(), C[C.sex == 'F'].sort_values('t', ascending=False)[['desc', 't', 'p95', 'eat', 'price_100g', 'Energy (kcal)']].head(15).round(2).to_string())
