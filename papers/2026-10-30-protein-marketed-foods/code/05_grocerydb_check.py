"""External check on the breakeven thresholds with observed 2021 shelf prices from GroceryDB (Ravandi et al., 2025).
Input: data/external/GroceryDB_foods.csv, downloaded from
  https://raw.githubusercontent.com/Barabasi-Lab/GroceryDB/a8d541c1ac6f25bee94cf37a493c01528005a6aa/data/GroceryDB_foods.csv
  (MIT licence; sha256 8181e3a2c94dabe449528e05ebd27f1c151b8ce75a04baa7b327600496326772; not redistributed in this package).
A product's observed price is above its breakeven price exactly when its observed cost per 10 g of protein exceeds the benchmark's.
Output: results/grocerydb_check.json"""
import re, html, json
import numpy as np, pandas as pd
from common import ROOT, RES

g = pd.read_csv(f'{ROOT}/data/external/GroceryDB_foods.csv')
R = {'rows': len(g), 'stores': g.store.value_counts().to_dict()}
g['name'] = g.name.fillna('').map(html.unescape)
U = {'oz': 28.3495, 'lb': 453.592, 'lbs': 453.592, 'g': 1, 'kg': 1000, 'fl oz': 29.5735, 'floz': 29.5735, 'ml': 1, 'l': 1000, 'gal': 3785.41, 'gallon': 3785.41}
def name_weight(s):
    """Package size stated in the product name (count x unit size where given), in g or ml."""
    s = s.lower()
    m = re.search(r'(\d+)\s*(?:ct|pk|pack|count)\s*/\s*(\d+(?:\.\d+)?)\s*(fl oz|floz|oz|g|ml)\b', s)
    if m: return int(m.group(1)) * float(m.group(2)) * U[m.group(3)]
    m = re.search(r'(\d+(?:\.\d+)?)\s*(fl\.? oz|floz|oz|lbs|lb|kg|g|ml|l|gallon|gal)\b', s)
    if m: return float(m.group(1)) * U[m.group(2).replace('.', '')]
    return np.nan
g['w_name'] = g.name.map(name_weight)
# quality rule: the package weight field agrees within 15% with the size stated in the name (the field has evident errors otherwise)
g['w_ok'] = (g.w_name / g.package_weight).between(0.85, 1.15)
g = g[g.Protein.between(0, 100, inclusive='right') & (g.price > 0) & (g.package_weight > 0)].copy()
g['usd10'] = 10 * g.price / (g.Protein * g.package_weight / 100)
n = g.name.str.lower(); cat = g['harmonized single category']
P = g[n.str.contains('protein') & ~n.str.contains(r'\bno protein|low protein|protein free')]
Q = P[P.w_ok]
B = json.load(open(f'{RES}/prices.json'))['benchmarks_usd_per_g_protein']
q = lambda x: {'n': int(len(x)), 'median': float(x.median()), 'p25': float(x.quantile(.25)), 'p75': float(x.quantile(.75))}
R['protein_named'] = {'all_with_protein': int(len(P)), 'weight_checked': int(len(Q)), 'usd_per_10g': q(Q.usd10), 'usd_per_10g_unchecked': q(P.usd10),
                      'share_above_benchmark': {k: float((Q.usd10 > 10 * v).mean()) for k, v in B.items()},
                      'share_above_benchmark_unchecked': {k: float((P.usd10 > 10 * v).mean()) for k, v in B.items()},
                      'by_store': {s: q(x.usd10) for s, x in Q.groupby('store')},
                      'by_category': {c: q(x.usd10) for c, x in Q.groupby('harmonized single category') if len(x) >= 8}}
# same stores, same year: staples priced in GroceryDB itself
eggs = g[(cat == 'eggs-wf') & n.str.contains('egg') & n.str.contains(r'\d+\s*ct') & ~n.str.contains('white|liquid|hard|bite')]
chick = g[n.str.contains('chicken breast') & n.str.contains('boneless') & g.w_ok &
          ~n.str.contains('breaded|nugget|tender|fried|strip|cooked|grilled|sandwich|seasoned|marinated|meal|bowl|garlic|jerk|lemon|asada|herb|bbq|teriyaki|italian|rotisserie')]
R['grocerydb_staples'] = {'eggs_dozen_counts': q(eggs.usd10), 'chicken_breast_plain': q(chick.usd10)}
json.dump(R, open(f'{RES}/grocerydb_check.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in R['protein_named'].items() if k != 'by_category'}, indent=1)); print(json.dumps(R['grocerydb_staples'], indent=1))
for c, v in R['protein_named']['by_category'].items(): print(c, v)
