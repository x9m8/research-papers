"""Headline numbers for the allocation factor: period means, decomposition, smoothing, monthly volatility."""
import json, numpy as np, pandas as pd
from common import RES
Y = pd.read_csv(f'{RES}/allocation_annual.csv').set_index('year'); M = pd.read_csv(f'{RES}/allocation_monthly.csv', index_col=0)
M['year'] = M.index.str[:4].astype(int)
def pm(a, b, c='share'): return float(Y.loc[a:b, c].mean())
early, late = (2002, 2013), (2023, 2025)
o = dict(early=pm(*early), late=pm(*late), share_2025=float(Y.loc[2025, 'share']), share_2002=float(Y.loc[2002, 'share']))
o['fold'] = o['early'] / o['late']
alts = ['share', 'share_cattle_lw', 'share_tx', 'share_dress62', 'share_dress64', 'share_output']
o['alts'] = {c: dict(early=pm(*early, c), late=pm(*late, c), y2025=float(Y.loc[2025, c]), fold=pm(*early, c) / pm(*late, c)) for c in alts}
# decomposition of the log change 2013 -> 2025 (annual means)
a, b = 2013, 2025
dh = np.log(Y.loc[b, 'hide'] / Y.loc[a, 'hide']); dl = np.log(Y.loc[b, 'live_value'] / Y.loc[a, 'live_value'])
dp = np.log(Y.loc[b, 'ne'] / Y.loc[a, 'ne']); dw = np.log(Y.loc[b, 'steer_lw'] / Y.loc[a, 'steer_lw'])
o['decomp_2013_2025'] = dict(dlog_share=float(dh - dl), dlog_hide=float(dh), dlog_live=float(dl), dlog_price=float(dp), dlog_weight=float(dw),
                             hide_pct=float(100 * (Y.loc[b, 'hide'] / Y.loc[a, 'hide'] - 1)), live_pct=float(100 * (Y.loc[b, 'live_value'] / Y.loc[a, 'live_value'] - 1)),
                             hide_part_of_change=float(dh / (dh - dl)))
# 3- and 5-year trailing means (price-averaging rules)
# trailing averages of PRICES (hide value and live value averaged over the window, then divided), windows ending in 2025
for w in (3, 5): o[f'roll{w}_2025'] = float(Y.hide.rolling(w).mean().loc[2025] / Y.live_value.rolling(w).mean().loc[2025])
# within-year monthly range
r = M.groupby('year').share.agg(['min', 'max']); o['max_within_year_range_pp'] = float(100 * (r['max'] - r['min']).max()); o['max_within_year_range_year'] = int((r['max'] - r['min']).idxmax())
o['roll5_frac_of_early'] = o['roll5_2025'] / o['early']
o['output_vs_main_early'] = o['alts']['share_output']['early'] / o['early']
o['hide_2002'] = float(Y.loc[2002, 'hide']); o['hide_2014'] = float(Y.loc[2014, 'hide']); o['hide_2025'] = float(Y.loc[2025, 'hide'])
o['live_2002'] = float(Y.loc[2002, 'live_value']); o['live_2025'] = float(Y.loc[2025, 'live_value'])
o['lw_2002'] = float(Y.loc[2002, 'steer_lw']); o['lw_2025'] = float(Y.loc[2025, 'steer_lw'])
json.dump(o, open(f'{RES}/summary.json', 'w'), indent=1); print(json.dumps(o, indent=1))
# level uncertainty from the dollar scaling: share is proportional to k, so use the smallest and largest single-anchor ratios
C = json.load(open(f'{RES}/hide_calibration.json')); kmin, kmax = C['k_range']; k = C['k']
o['k'] = k; o['k_min'] = kmin; o['k_max'] = kmax
o['late_kmin'] = o['late'] * kmin / k; o['late_kmax'] = o['late'] * kmax / k; o['early_kmin'] = o['early'] * kmin / k; o['early_kmax'] = o['early'] * kmax / k
json.dump(o, open(f'{RES}/summary.json', 'w'), indent=1)
print({x: round(o[x], 4) for x in ['k', 'k_min', 'k_max', 'early_kmin', 'early_kmax', 'late_kmin', 'late_kmax']})
