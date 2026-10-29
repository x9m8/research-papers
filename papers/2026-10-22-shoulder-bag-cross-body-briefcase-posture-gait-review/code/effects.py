"""Within-study standardised differences (carry vs no-load) for adult studies. Not pooled.
d_av = (mean_carry - mean_noload) / sqrt((SD_carry^2 + SD_noload^2)/2), Hedges small-sample correction J = 1 - 3/(4(n-1)-1).
SE converted to SD by SE*sqrt(n). Rows without a usable SD on both sides are kept with percent difference only.
Approximate 95% CI for a within-subject design assumes a correlation r between conditions (main 0.5; 0.2 and 0.8 sensitivity):
var(d) = (1/n + d^2/(2n)) * 2(1-r) (Borenstein et al., 2009)."""
import json, re, numpy as np, pandas as pd
from common import DATA, RES
e = pd.read_csv(f'{DATA}/extraction.csv')
e['n_an'] = pd.to_numeric(e.n_analysed.astype(str).str.extract(r'^(\d+)')[0])
noload = e.comparison.str.contains(r'\bno\b|none|unloaded|empty|without|no load|control', case=False, regex=True) & ~e.comparison.str.contains('backpack|rucksack', case=False) | e.comparison.str.contains(r'^no backpack', case=False)
e['vs_noload'] = noload
def sd(v, kind, n):
    try: v = float(v)
    except Exception: return np.nan
    if kind == 'SE': return v * np.sqrt(n)
    if kind == 'SD': return v
    return np.nan
e['sd_c'] = [sd(v, k, n) for v, k, n in zip(e.carry_sd, e.carry_dispersion, e.n_an)]
e['sd_0'] = [sd(v, k, n) for v, k, n in zip(e.comparison_sd, e.comparison_dispersion, e.n_an)]
e['diff'] = e.carry_mean - e.comparison_mean
e['pct'] = 100 * e['diff'] / e.comparison_mean.abs()
sdav = np.sqrt((e.sd_c ** 2 + e.sd_0 ** 2) / 2)
J = 1 - 3 / (4 * (e.n_an - 1) - 1)
e['g'] = J * e['diff'] / sdav
for r in (0.2, 0.5, 0.8):  # variance form of Borenstein et al. (2009)
    se = np.sqrt((1 / e.n_an + e.g ** 2 / (2 * e.n_an)) * 2 * (1 - r)); e[f'lo_{r}'] = e.g - 1.96 * se; e[f'hi_{r}'] = e.g + 1.96 * se
e['adult'] = e.age_group.str.contains('adult', case=False) & ~e.age_group.str.contains('ADOLESCENT')
dom = {'EMG': 'Muscle activity (EMG)'}
def domain(r):
    d = str(r.outcome_domain).lower(); o = str(r.outcome_name).lower()
    if 'emg' in d: return 'Muscle activity'
    if any(k in o for k in ('heart', 'rpe', 'borg')): return 'Effort'
    if any(k in d for k in ('posture', 'kinematic')) or any(k in o for k in ('tilt', 'rotation', 'lean', 'obliquity', 'flexion', 'asymmetry', 'plumb')): return 'Posture and pelvis'
    return 'Gait'
e['domain'] = e.apply(domain, axis=1)
e['bag_side'] = e.outcome_name.str.contains('bag side|strap side|load side|loaded side', case=False)
e.to_csv(f'{RES}/effects_all.csv', index=False)
A = e[e.adult & e.vs_noload].copy()
G = A[A.g.notna()]
summ = dict(n_rows_adult_noload=int(len(A)), n_with_g=int(len(G)), n_studies_with_g=int(G.study_id.nunique()), studies_with_g=sorted(G.study_id.unique()),
            by_domain={d: dict(n=int(len(x)), studies=int(x.study_id.nunique()), median_g=float(x.g.median()), n_abs_ge_0_5=int((x.g.abs() >= 0.5).sum()),
                                n_ci_excl0=int(((x['lo_0.5'] > 0) | (x['hi_0.5'] < 0)).sum())) for d, x in G.groupby('domain')})
bs = G[G.bag_side & (G.domain == 'Muscle activity')]
summ['bag_side_emg'] = bs[['study_id', 'outcome_name', 'load_pct_bm', 'carry_mean', 'comparison_mean', 'g', 'lo_0.5', 'hi_0.5']].to_dict('records')
json.dump(summ, open(f'{RES}/effects_summary.json', 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in summ.items() if k != 'bag_side_emg'}, indent=1, default=float))
print(bs[['study_id', 'outcome_name', 'load_pct_bm', 'carry_mean', 'comparison_mean', 'g', 'lo_0.5', 'hi_0.5']].round(2).to_string())
