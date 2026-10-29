"""Write manuscript tables (markdown) from the result files and insert them into the manuscript under '## Tables'."""
import json, os
import pandas as pd
from common import RES
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(f'{RES}/analysis.json')); S = json.load(open(f'{RES}/sensitivity.json'))
Y = pd.DataFrame(A['B_series'])


from decimal import Decimal, ROUND_HALF_UP
def f(x, d=1): return str(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))
def pct_ci(t): return f"{f(t['pct_per_year'])}% ({f(t['ci'][0])} to {f(t['ci'][1])})"


t1 = ['**Table 1.** Safety Gate notifications for hexavalent chromium in leather and leather-type articles, by year of publication. '
      'All alerts and chemical-risk alerts are the totals in the Safety Gate search for each year. 2026 runs to the snapshot date (20 October).', '',
      '| Year | Notifications | By Germany | By other countries | Notifying countries | All alerts | Per 1,000 alerts | Chemical-risk alerts | Per 100 chemical alerts |',
      '|:-----|-----:|-----:|-----:|-----:|-------:|------:|-------:|------:|']
for r in Y.itertuples():
    t1.append(f'| {r.year} | {r.n} | {r.n_de} | {r.n_other} | {r.notifiers} | {r.all:,} | {f(r.per1000_all)} | {r.chem:,} | {f(r.per100_chem, 2)} |')
t1.append(f"| **2005–2026** | **{int(Y.n.sum())}** | **{int(Y.n_de.sum())}** | **{int(Y.n_other.sum())}** | | **{int(Y['all'].sum()):,}** | | **{int(Y.chem.sum()):,}** | |")

c = A['D_conc']
t2 = ['**Table 2.** Three measures of the same problem before and after the EU limit. Safety Gate rows are computed here; the others are taken from the cited sources.', '',
      '| Measure | Before the limit | After the limit | Source |', '|:------|:------|:------|:------|',
      f"| Safety Gate notifications per 1,000 alerts | {f(A['B_peak3']['per1000_all'])} (2013–2015) | {f(A['B_recent']['per1000_all'])} (2023–2025) | This study |",
      f"| Safety Gate notifications per 100 chemical-risk alerts | {f(A['B_peak3']['per100_chem'])} (2013–2015) | {f(A['B_recent']['per100_chem'], 2)} (2023–2025) | This study |",
      f"| Median highest Cr(VI) in a notified article, mg/kg | {f(c['before']['median'])} (n = {c['before']['n']}) | {f(c['after']['median'])} (n = {c['after']['n']}) | This study |",
      '| Leather articles above 3 mg/kg in market surveys | 23% of 588 (Germany 2008); 32% of 504 (Germany 2009); 35% of 43 (Denmark 2002) | 13.3% of 467 (EU enforcement project, 2016 checks); 10.6% of 94 samples (Denmark, 2019 report); 12% of 99 (Stuttgart 2020–2021) | Danish EPA (2012); ECHA (2018); Danish EPA (2019); Köhler (2022) |',
      '| Chromium allergy among patch-tested dermatitis patients, Gentofte (Denmark) | 2.3% (2006–2009); 1.9% (2010–2013) | 2.1% (2016–2024, n = 4,830), stable | Kursawe Larsen et al. (2026) |']

b = S['base']; t3 = ['**Table 3.** Sensitivity of the two main results. Trend: annual change in notifications per 1,000 alerts, 2016–2025 (quasi-Poisson; 95% CI) unless stated. '
                     'Concentration: median highest value before and after 1 May 2015, ratio of geometric means (after/before) and Mann–Whitney p.', '',
                     '| Analysis | n | Annual change | Median before → after (mg/kg) | Geometric-mean ratio | p |', '|:------|-----:|:------|:------|-----:|-----:|']
def row(name, n, tr, cc):
    t3.append(f"| {name} | {n} | {pct_ci(tr) if tr else '–'} | {f(cc['median_before'])} → {f(cc['median_after'])} | {cc['gm_ratio']:.2f} | {cc['p']:.2g} |" if cc else
              f"| {name} | {n} | {pct_ci(tr)} | – | – | – |")
row('Main analysis', A['A']['n'], b['trend'], b['conc'])
row("Only alerts that name leather", S['S1_strict_leather_word']['n'], S['S1_strict_leather_word']['trend'], S['S1_strict_leather_word']['conc'])
t3.append(f"| Lowest instead of highest value per alert | {S['S2_min_value']['conc']['n']} | – | {f(S['S2_min_value']['conc']['median_before'])} → {f(S['S2_min_value']['conc']['median_after'])} | {S['S2_min_value']['conc']['gm_ratio']:.2f} | {S['S2_min_value']['conc']['p']:.2g} |")
row('Creation date instead of publication date', S['S3_creation_date']['n'], S['S3_creation_date']['trend'], S['S3_creation_date']['conc'])
row('Germany excluded', S['S4_germany']['excl_germany']['n'], S['S4_germany']['excl_germany']['trend'], S['S4_germany']['excl_germany']['conc'])
row('Germany only', S['S4_germany']['germany_only']['n'], S['S4_germany']['germany_only']['trend'], S['S4_germany']['germany_only']['conc'])
s5 = S['S5_offsets']
t3.append(f"| Raw counts, no denominator, 2016–2025 | {s5['raw_counts_2016_2025']['n']} | {pct_ci(s5['raw_counts_2016_2025'])} | – | – | – |")
t3.append(f"| Per 1,000 alerts, 2016–2022 only | {s5['all_2016_2022']['n']} | {pct_ci(s5['all_2016_2022'])} | – | – | – |")
t3.append(f"| Per 100 chemical-risk alerts, 2016–2025 | {A['B_trend']['after_chem']['n_alerts']} | {pct_ci(A['B_trend']['after_chem'])} | – | – | – |")
t3.append(f"| Plain Poisson instead of quasi-Poisson | {S['S6_models']['poisson']['n']} | {pct_ci(S['S6_models']['poisson'])} | – | – | – |")
t3.append(f"| Negative binomial (method-of-moments dispersion estimated at zero, so equal to Poisson) | {S['S6_models']['nb']['n']} | {pct_ci(S['S6_models']['nb'])} | – | – | – |")
s7 = S['S7_excl_at_limit']['conc']
t3.append(f"| Values of exactly 3 mg/kg excluded | {s7['n']} | – | {f(s7['median_before'])} → {f(s7['median_after'])} | {s7['gm_ratio']:.2f} | {s7['p']:.2g} |")

tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(HERE, '..', 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures')
    open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
