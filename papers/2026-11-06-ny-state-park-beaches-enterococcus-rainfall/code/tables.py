"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md."""
import json
import os
from common import RESULTS, ROOT

desc = json.load(open(f'{RESULTS}/descriptives.json'))
trends = json.load(open(f'{RESULTS}/trends.json'))
rainfall = json.load(open(f'{RESULTS}/rainfall.json'))
closures = json.load(open(f'{RESULTS}/closures.json'))

t1 = [
    '**Table 1.** Enterococcus single-sample exceedances (≥104 CFU/100 mL) by waterbody, '
    'and the year trend from a beach-fixed-effects logistic regression within each waterbody '
    '(standard errors clustered by beach station). NY State Park beaches, Long Island, 2015–2025.',
    '',
    '| Waterbody | Beach stations | Samples | Exceedances | Rate (%) | Odds ratio per year | SE (log-odds) |',
    '|:--|--:|--:|--:|--:|--:|--:|',
]
wb_order = ['Great South Bay', 'Long Island Sound', 'Atlantic Ocean']
for wb in wb_order:
    row = trends['by_waterbody'][wb]
    t1.append(f"| {wb} | {row['n_beach_stations']} | {row['n']:,} | {row['n_exceeded']} | "
              f"{100 * row['rate']:.1f} | {row['year_odds_ratio_per_year']:.3f} | {row['year_se']:.3f} |")
pf = trends['pooled_fe']
t1.append(f"| **All Long Island (pooled, beach FE)** | {pf['n_clusters']} | {pf['n']:,} | "
          f"{desc['n_exceeded']} | {100 * desc['exceedance_rate']:.1f} | "
          f"{pf['year_odds_ratio_per_year']:.3f} | {pf['year_se_cluster']:.3f} (clustered) |")

t2 = [
    '',
    '**Table 2.** Closure and advisory days by beach station, 2015–2025 (forward-filled from '
    'consecutive reported status changes; seasonal/administrative closures excluded, see Methods). '
    'Ranked by total days.',
    '',
    '| Beach station | Waterbody | Closure days | Advisory days | Total days | % of all closure days |',
    '|:--|:--|--:|--:|--:|--:|',
]
for r in closures['by_beach']:
    t2.append(f"| {r['state_park_beach']} | {r['waterbody']} | {int(r['closure_days'])} | "
              f"{int(r['advisory_days'])} | {int(r['total_days'])} | {r['pct_of_total_closure_days']:.1f} |")
t2.append(f"| **Total** | | {int(closures['total_closure_days'])} | {int(closures['total_advisory_days'])} | "
          f"{int(closures['total_closure_days'] + closures['total_advisory_days'])} | 100.0 |")

t3 = [
    '',
    '**Table 3.** Rainfall and the odds of an Enterococcus exceedance: logistic regression with beach '
    'fixed effects and a linear year term, standard errors clustered by beach station (n = 15 '
    'clusters). Rainfall is measured at the beach’s assigned station (JFK or Islip-LI MacArthur '
    'Airport; see Methods); odds ratios are per 1 cm of rain.',
    '',
    '| Rainfall measure | n | Odds ratio per cm | 95% CI | p |',
    '|:--|--:|--:|--:|--:|',
]
specs = [
    ('main_48h', 'Prior 48 hours (main specification)'),
    ('robustness_sameday', 'Same day as sampling'),
    ('robustness_72h', 'Prior 72 hours'),
    ('robustness_48h_no_fe', 'Prior 48 hours, no beach fixed effects'),
]
for key, label in specs:
    r = rainfall[key]
    t3.append(f"| {label} | {r['n']:,} | {r['odds_ratio_per_unit']:.2f} | "
              f"{r['or_ci95_cluster'][0]:.2f}–{r['or_ci95_cluster'][1]:.2f} | {r['p_cluster']:.1e} |")

tables = '\n'.join(t1) + '\n' + '\n'.join(t2) + '\n' + '\n'.join(t3) + '\n'
open(f'{RESULTS}/tables.md', 'w').write(tables)

ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read()
    i = s.index('## Tables')
    j = s.index('## Figures')
    open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])

print(tables)
