"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os, pandas as pd
from common import RES, ROOT
A = json.load(open(f'{RES}/analysis.json')); Y = pd.read_csv(f'{RES}/embodied_by_year.csv', index_col=0)
order = ['By-product (SWD), 2.5%', 'PEFCR, 3.5%', 'DeDuCE / SWD co-product, 5%', 'Mass (SWD), 8%', 'Mass (Laroche et al.), 10%', 'Mass, FAOSTAT weights',
         'Economic, price of the year', 'Economic, k = 0.60', 'Economic, k = 0.80', 'Economic, world beef price', 'Economic, fixed-mix beef price', 'DeDuCE 5%, unamortized']
t1 = ['**Table 1.** Deforestation embodied in EU27 imports of cattle hides and leather (HS 4101, 4104, 4107, raw-hide equivalent) under each allocation rule, and the benefit-cost ratio of keeping leather in the regulation computed with the Commission\'s own valuation (EUR 50,170 per hectare, implied by SWD Annex II) and compliance cost (EUR 16.7 million per year).', '',
      '| Allocation rule | Hectares per year, 2015–2020 mean | Hectares, 2022 | Benefit-cost, 2015–2020 | Benefit-cost, 2022 |', '|:--|--:|--:|--:|--:|']
for k in order:
    t1.append(f"| {k} | {A['mean_2015_2020'][k]:,.0f} | {A['y2022'][k]:,.0f} | {A['benefit_cost_2015_2020'][k]:.0f} | {A['benefit_cost_2022'][k]:.0f} |")
pr = A['price_ratio']; aw = A['alpha_weighted']; ab = A['brazil_alpha']; ph = A['price_hide']; pb = A['price_beef']
t2 = ['**Table 2.** EU import unit values of raw cattle hides (HS 4101, all extra-EU origins) and beef (HS 0201 + 0202, all extra-EU origins), their ratio, and the economic allocation factor for hides (EU import-weighted across deforestation origins; the same with a fixed-mix beef price holding 2005–2007 origin shares constant; and Brazil).', '',
      '| Year | Raw hides, EUR/kg | Beef, EUR/kg | Ratio | Economic factor, import-weighted, % | Same, fixed-mix beef price, % | Economic factor, Brazil, % |', '|:--|--:|--:|--:|--:|--:|--:|']
for y in [2005, 2008, 2010, 2013, 2015, 2018, 2020, 2022, 2023, 2024, 2025]:
    s = str(y)
    t2.append(f"| {y} | {ph[s]:.2f} | {pb[s]:.2f} | {pr[s]:.2f} | {100*aw[s]:.1f} |" .replace('|  |', '| – |') if s in aw else f"| {y} | {ph[s]:.2f} | {pb[s]:.2f} | {pr[s]:.2f} | – |")
    t2[-1] += (f" {100*A['alpha_weighted_fixedmix'][s]:.1f} |" if s in A['alpha_weighted_fixedmix'] else ' – |')
    t2[-1] += (f" {100*ab[s]:.1f} |" if s in ab else ' – |')
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
