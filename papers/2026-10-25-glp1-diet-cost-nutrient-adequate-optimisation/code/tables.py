"""Tables -> results/tables.md and the '## Tables' section of the manuscript."""
import json, os
from common import RES, ROOT, TFP_DAY_SINGLE
R = json.load(open(f'{RES}/results.json')); G = R['grid']; RS = [0.0, 0.16, 0.24, 0.35, 0.39]
SEX = {'F': 'Women', 'M': 'Men'}; LAB = {0.0: 'Current energy', 0.16: '−16%', 0.24: '−24%', 0.35: '−35%', 0.39: '−39%'}
NN = {'Magnesium (mg)': 'magnesium', '18:2\n(g)': 'linoleic acid', 'Calcium (mg)': 'calcium', 'Choline, total (mg)': 'choline', 'protein target': 'protein', 'fibre': 'fibre'}
def short(d): return '; '.join(f'{NN.get(k, k)} ' + (f'{v:.1f}%' if v >= 99.5 else f'{v:.0f}%') for k, v in d.items())
def cell(a, with_short=True):
    if a is None or a.get('cost') is None: return 'none exists'
    if a.get('feasible', True): return f"{a['cost']:.2f}"
    return f"{a['cost']:.2f}†" + (f" ({short(a['short'])})" if with_short and a.get('short') else '')
t1 = [f"**Table 1.** Daily food cost per person (US$, 2026 prices) of diets for US adults eligible for GLP-1 obesity treatment, at current energy intake and after the cuts measured in GLP-1 trials. NHANES 2017–March 2020 food records priced with ERS national average prices for 2017–2018. Adequate diets meet the RDA or AI for adults aged 31–50 for every nutrient with a value in FNDDS except vitamins D and E (fibre scaled to energy), stay within upper limits, the sodium CDRR and the AMDRs, keep the observed mix of foods within each food category and limit each category to the 95th percentile (P95) of current individual intake (P99 in the wider-limits column). Protein ≥0.8 g/kg reference weight. For a one-person household, the USDA Thrifty Food Plan for June 2026 is ${TFP_DAY_SINGLE['F'][0]:.2f} to ${TFP_DAY_SINGLE['F'][1]:.2f} a day for women and ${TFP_DAY_SINGLE['M'][0]:.2f} to ${TFP_DAY_SINGLE['M'][1]:.2f} for men (ages 51–70 to 20–50).", '',
      '| Sex and scenario | Energy, kcal/day | Eating less of the same | Closest adequate diet | Energy moved between categories, % | Closest adequate diet, P99 limits | Cheapest adequate diet | Least-cost diet from any foods |',
      '|:--|--:|--:|--:|--:|--:|--:|--:|']
for s in 'FM':
    t1.append(f'| ***{SEX[s]}*** | | | | | | | |')
    for r in RS:
        g = G[f'{s}|{r}|0.8']; a = g['adequate']
        t1.append(f"| {LAB[r]} | {g['kcal']:,.0f} | {g['cost_scaled']:.2f} | {cell(a)} | {100*a['realloc']:.0f} | {cell(g['p99'])} | {cell(g['cheapest'] if g['cheapest']['feasible'] else None)} | {g['floor']['cost']:.2f} |")
t1 += ['', '†No fully adequate diet exists within the P95 limits; the figure is the cost of the diet with the smallest total shortfall that is closest to current eating, with the share of each requirement met in brackets.']
t2 = ['**Table 2.** Sensitivity analyses at 24% and 35% cuts in energy intake: daily cost (US$) of the closest adequate diet, or the best achievable† where none exists; and the highest intake of vitamins D and E achievable from food with every other requirement met, as a percentage of the RDA.', '',
      '| Analysis | Women, −24% | Women, −35% | Men, −24% | Men, −35% |', '|:--|--:|--:|--:|--:|']
row = lambda lab, f: t2.append(f'| {lab} | ' + ' | '.join(f(s, r) for s in 'FM' for r in (0.24, 0.35)) + ' |')
row('Main analysis', lambda s, r: cell(G[f'{s}|{r}|0.8']['adequate']))
row('Protein ≥1.2 g/kg reference weight', lambda s, r: cell(G[f'{s}|{r}|1.2']['adequate']))
row('Category limits at P99', lambda s, r: cell(G[f'{s}|{r}|0.8']['p99']))
row('Foods chosen freely within categories, each food ≤5× its current mean (cheapest diet)', lambda s, r: f"{G[f'{s}|{r}|0.8']['food5_cheapest']:.2f}" if G[f'{s}|{r}|0.8']['food5_cheapest'] else 'none exists')
row('Sum of absolute (not squared) relative deviations', lambda s, r: f"{R['sens'][f'{s}|{r}|l1']['cost']:.2f}" if R['sens'][f'{s}|{r}|l1']['feasible'] else 'none exists')
row('Fibre at the absolute AI (25 g women, 38 g men)', lambda s, r: cell(R['sens'][f'{s}|{r}|fibre_abs']))
row('Requirements for ages 51–70', lambda s, r: cell(R['sens'][f'{s}|{r}|age51']))
fmt = lambda v: '–' if v is None else f'{v:.0f}%'
row('Vitamin D from food, highest % of RDA (P95; P99)', lambda s, r: f"{fmt(R['de'][f'{s}|{r}']['D'])}; {fmt(R['de'][f'{s}|{r}']['D_p99'])}")
row('Vitamin E from food, highest % of RDA (P95; P99)', lambda s, r: f"{fmt(R['de'][f'{s}|{r}']['E'])}; {fmt(R['de'][f'{s}|{r}']['E_p99'])}")
t2 += ['', '– Not computable because the other requirements cannot all be met within the P95 limits.']
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
