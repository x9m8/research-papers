"""Manuscript tables from the result files; inserted between '## Tables' and '## Figures' in the manuscript."""
import json, os, pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from common import RES, ROOT
def f(x, d=1): return str(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))
Y = pd.read_csv(f'{RES}/allocation_annual.csv'); C = pd.read_csv(f'{RES}/carbon_annual.csv'); d = Y.merge(C, on='year')
S = json.load(open(f'{RES}/summary.json')); K = json.load(open(f'{RES}/carbon.json'))
t1 = ['**Table 1.** Hide value, live steer value and the hide\'s economic allocation factor, United States, annual means of monthly values. '
      'Hide: butt-branded steer hide, $ per piece (PPI scaled to AMS prices). Live value: Nebraska fed-steer price times steer live weight. '
      'Emissions carried by the hide use 21.3 kg CO~2~e per kg carcass weight (Rotz et al., 2019) for every year, so only prices move them. 2001 covers June to December.', '',
      '| Year | Hide, $/piece | Steer price, $/cwt live | Live weight, lb | Live value, $/head | Hide share, % | Hide share, output-value basis, % | kg CO~2~e per hide | kg CO~2~e per m^2^ |',
      '|:--|--:|--:|--:|--:|--:|--:|--:|--:|']
for r in d.itertuples():
    t1.append(f'| {r.year} | {f(r.hide, 2)} | {f(r.ne, 2)} | {r.steer_lw:,.0f} | {r.live_value:,.0f} | {f(100 * r.share, 2)} | {f(100 * r.share_output, 2)} | {r.kg_hide_econ:,.0f} | {f(r.kg_m2_econ)} |')
a = S['alts']
nm = {'share': 'Main: Nebraska price, steer dressed weight / 0.63', 'share_cattle_lw': 'All-cattle commercial live weight', 'share_tx': 'Texas/Oklahoma/New Mexico steer price',
      'share_dress62': 'Dressing percentage 62%', 'share_dress64': 'Dressing percentage 64%', 'share_output': 'Output value: Choice cutout × carcass weight + hide'}
t2 = ['**Table 2.** Sensitivity of the hide\'s economic allocation factor to the denominator, the dollar scaling and the price-averaging rule. Early: mean of 2002–2013; late: mean of 2023–2025.', '',
      '| Analysis | Early, % | Late, % | 2025, % | Early ÷ late |', '|:--|--:|--:|--:|--:|']
for k, v in a.items(): t2.append(f"| {nm[k]} | {f(100 * v['early'], 2)} | {f(100 * v['late'], 2)} | {f(100 * v['y2025'], 2)} | {f(v['fold'])} |")
t2.append(f"| Dollar scaling at the lowest single-report ratio | {f(100 * S['early_kmin'], 2)} | {f(100 * S['late_kmin'], 2)} | {f(100 * S['share_2025'] * S['k_min'] / S['k'], 2)} | {f(S['fold'])} |")
t2.append(f"| Dollar scaling at the highest single-report ratio | {f(100 * S['early_kmax'], 2)} | {f(100 * S['late_kmax'], 2)} | {f(100 * S['share_2025'] * S['k_max'] / S['k'], 2)} | {f(S['fold'])} |")
t2.append(f"| Prices averaged over 2023–2025 (three-year window) | – | – | {f(100 * S['roll3_2025'], 2)} | – |")
t2.append(f"| Prices averaged over 2021–2025 (five-year window) | – | – | {f(100 * S['roll5_2025'], 2)} | – |")
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
