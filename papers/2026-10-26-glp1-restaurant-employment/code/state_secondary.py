"""Secondary, exploratory: state card spending on accommodation and food services (Opportunity Insights /
Affinity Solutions, spend_acf) against the change in Medicare Part D GLP-1 uptake, 2022-2025.
-> results/state_secondary.json"""
import json, os
import numpy as np
import pandas as pd
from common import RAW, RES, ols_fe, tcrit, tpval, mde

a = pd.read_csv(os.path.join(RAW, 'affinity_state_monthly.csv'), na_values=['.'])
a['spend_acf'] = pd.to_numeric(a.spend_acf, errors='coerce')
ann = a[a.year.isin([2022, 2025])].groupby(['statefips', 'year']).spend_acf.agg(['mean', 'count']).unstack()
ann = ann[(ann[('count', 2022)] == 12) & (ann[('count', 2025)] == 12)]
dy = (np.log1p(ann[('mean', 2025)]) - np.log1p(ann[('mean', 2022)])).rename('dy')
dy.index = dy.index.astype(int).map(lambda s: f'{s:02d}')

en = pd.read_csv(os.path.join(RAW, 'medicare_enrollment_county.csv'), dtype=str)
en['partd'] = pd.to_numeric(en.PRSCRPTN_DRUG_TOT_BENES.str.replace(',', ''), errors='coerce')
en['st'] = en.BENE_FIPS_CD.str.zfill(5).str[:2]
E = {}
for y in (2019, 2022, 2024):
    g = pd.read_csv(os.path.join(RAW, f'partd_geo_glp1_{y}.csv'), dtype=str)
    g = g[g.Prscrbr_Geo_Lvl == 'State'].assign(f=lambda d: pd.to_numeric(d.Tot_30day_Fills, errors='coerce'))
    f = g.groupby('Prscrbr_Geo_Cd').f.sum()
    d = en[en.YEAR == str(y)].groupby('st').partd.sum()
    E[y] = 100 * f / 12 / d
s = pd.DataFrame({'dE_22_24': E[2024] - E[2022], 'dE_19_24': E[2024] - E[2019], 'E_2022': E[2022]}).join(dy, how='inner').dropna()
s = s[s.index <= '56']
out = {'n_states': int(len(s)), 'mean_dy_pct': float(100 * s.dy.mean())}
for x in ('dE_22_24', 'dE_19_24'):
    r = ols_fe(s.dy.values, s[[x, 'E_2022']].values, np.zeros(len(s), int), np.arange(len(s)))
    b, se = float(r['b'][0]), float(r['se'][0])
    out[x] = {'b_pp': 100 * b, 'se_pp': 100 * se, 'lo_pp': 100 * (b - tcrit(r['df']) * se), 'hi_pp': 100 * (b + tcrit(r['df']) * se),
              'p': tpval(b / se, r['df']), 'mde_pp': 100 * mde(se, r['df']), 'sd_x': float(s[x].std()), 'mean_x': float(s[x].mean())}
json.dump(out, open(os.path.join(RES, 'state_secondary.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
