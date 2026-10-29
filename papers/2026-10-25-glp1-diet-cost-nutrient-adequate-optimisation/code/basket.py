"""Observed diet of US adults eligible for GLP-1 obesity treatment, NHANES 2017-March 2020 (food-level recalls), priced with ERS PP-NAP 2017/2018.
Eligibility and weights as in the companion paper (adults 20+, not pregnant, BMI >=30 or >=27 with diabetes or hypertension; two reliable recalls; WTDR2DPP).
Basket x0 = survey-weighted mean grams/day of each food code (mean of the two days), by sex."""
import json, numpy as np, pandas as pd
from common import *
E = pd.read_csv(f'{ROOT}/data/eligible_P.csv')
f1 = pd.read_csv(f'{RAW}/p_dr1iff.csv'); f2 = pd.read_csv(f'{RAW}/p_dr2iff.csv')[['SEQN', 'code', 'g']]
F = pd.concat([f1.assign(day=1), f2.assign(day=2)]); F = F[F.SEQN.isin(E.SEQN)]
P = F.groupby(['SEQN', 'code']).g.sum().div(2).reset_index()            # mean g/day over two days
P = P.merge(E[['SEQN', 'sex', 'w']], on='SEQN')
W = E.groupby('sex').w.sum()
B = P.groupby(['sex', 'code']).apply(lambda g: np.sum(g.g * g.w)).unstack(0).fillna(0) / W   # g/day per person, by sex
B.columns = [f'x0_{s}' for s in B.columns]; B = B.reset_index().rename(columns={'code': 'Food code'})
# share of eligible adults eating each food (weighted)
eat = P.groupby(['sex', 'code']).w.sum().unstack(0).fillna(0) / W; eat.columns = [f'eat_{s}' for s in eat.columns]
B = B.merge(eat.reset_index().rename(columns={'code': 'Food code'}), on='Food code')
# nutrients: FNDDS 2017-2018, else 2021-2023 for codes not in 2017-2018
n17 = pd.read_excel(f'{RAW}/FNDDS1718_nutrients.xlsx', header=1); n21 = pd.read_excel(f'{RAW}/FNDDS2123_nutrients.xlsx', header=1)
n21 = n21[~n21['Food code'].isin(n17['Food code'])]
N = pd.concat([n17.assign(fndds='2017-2018'), n21.assign(fndds='2021-2023')], ignore_index=True)
pr = pd.read_csv(f'{RES}/foods_priced.csv')[['Food code', 'price_100gm', 'price_100g_2026', 'method_description']]
B = B.merge(N, on='Food code', how='left').merge(pr, on='Food code', how='left')
# impute missing prices by WWEIA category median (2026 dollars), flagged
med = pr.merge(n17[['Food code', 'WWEIA Category number']], on='Food code').groupby('WWEIA Category number').price_100g_2026.median()
B['price_imputed'] = B.price_100g_2026.isna() & B['WWEIA Category number'].notna()
gmed = pr.merge(n17[['Food code', 'WWEIA Category number']], on='Food code').assign(gr=lambda d: d['WWEIA Category number'] // 100).groupby('gr').price_100g_2026.median()
cat = B.loc[B.price_imputed, 'WWEIA Category number']
B.loc[B.price_imputed, 'price_100g_2026'] = cat.map(med).fillna((cat // 100).map(gmed))   # category median, else median of the category group
B.to_csv(f'{RES}/basket.csv', index=False)
out = {}
for s in 'MF':
    x = B[f'x0_{s}']; ok = B.price_100g_2026.notna()
    out[s] = dict(n_people=int((E.sex == s).sum()), kcal=float((x * B['Energy (kcal)'].fillna(0) / 100).sum()), protein=float((x * B['Protein (g)'].fillna(0) / 100).sum()),
                  grams=float(x.sum()), cost_day=float((x * B.price_100g_2026 / 100)[ok].sum()),
                  grams_priced_share=float(x[ok & ~B.price_imputed].sum() / x.sum()), grams_imputed_share=float(x[B.price_imputed].sum() / x.sum()),
                  grams_no_nutrients=float(x[B['Energy (kcal)'].isna()].sum() / x.sum()), n_foods=int((x > 0).sum()))
json.dump(out, open(f'{RES}/basket.json', 'w'), indent=1); print(json.dumps(out, indent=1))
