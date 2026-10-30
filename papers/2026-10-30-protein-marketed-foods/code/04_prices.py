"""Part B: whole-food cost per gram of protein (BLS Average Prices x SR Legacy) and breakeven prices for protein-named products.
Output: results/prices.json, results/whole_food_benchmarks.csv"""
import json, gzip, io
import numpy as np, pandas as pd
from common import *

# ---- BLS average prices, US city average ----
txt = open(f'{RAW}/bls_ap_2024_2026.tsv').read().split('\n#ITEMS\n')[0]
ap = pd.read_csv(io.StringIO(txt), sep='\t', dtype=str)
ap['value'] = pd.to_numeric(ap.value, errors='coerce')
win = set(PRICE_WINDOW)
ap = ap[[(y, p) in win for y, p in zip(ap.year, ap.period)]]
# ---- SR Legacy composition ----
raw = gzip.open(f'{RAW}/sr_legacy_extract.tsv.gz', 'rt').read().split('\n#NUTRIENTS\n')
foods = pd.read_csv(io.StringIO(raw[0]), sep='\t', dtype=str).set_index('fdc_id').description
nut = pd.read_csv(io.StringIO(raw[1]), sep='\t', dtype={'fdc_id': str, 'nutrient_id': str})
prot = nut[nut.nutrient_id == '1003'].set_index('fdc_id').amount
kcal = nut[nut.nutrient_id == '1008'].set_index('fdc_id').amount

rows = []
for key, label, item, unit_g, ids, bench in WHOLE:
    s = ap[ap.series_id == f'APU0000{item}'].dropna(subset=['value'])
    p100 = float(np.mean([prot[i] for i in ids])); k100 = float(np.mean([kcal[i] for i in ids]))
    pm, pl, pmin, pmax = s.value.mean(), s.sort_values(['year', 'period']).value.iloc[-1], s.value.min(), s.value.max()
    per_g_prot = lambda price: price / unit_g / (p100 / 100)
    rows.append({'key': key, 'label': label, 'bls_series': f'APU0000{item}', 'n_months': len(s), 'price_mean12': pm, 'price_latest': pl, 'price_min': pmin, 'price_max': pmax,
                 'edible_g_per_unit': unit_g, 'sr_fdc_ids': ';'.join(ids), 'sr_descriptions': ' / '.join(foods[i] for i in ids), 'protein_g_per100g': p100, 'kcal_per100g': k100,
                 'usd_per_10g_protein': 10 * per_g_prot(pm), 'usd_per_10g_protein_min': 10 * per_g_prot(pmin), 'usd_per_10g_protein_max': 10 * per_g_prot(pmax),
                 'usd_per_100kcal': pm / unit_g / (k100 / 100) * 100, 'benchmark': bench})
W = pd.DataFrame(rows); W.to_csv(f'{RES}/whole_food_benchmarks.csv', index=False)
core = W[W.benchmark].set_index('key')
BEN = {k: core.loc[k, 'usd_per_10g_protein'] / 10 for k in core.index}       # $ per g protein
BEN['median4'] = float(np.median(list(BEN.values())))
R = {'whole_foods': W.to_dict(orient='records'), 'benchmarks_usd_per_g_protein': BEN, 'price_window': [f'{y}-{p}' for y, p in PRICE_WINDOW]}

# ---- breakeven prices for protein-named products ----
d = pd.read_pickle(f'{DER}/products.pkl')
E = d[d.E2].copy()
for b, v in BEN.items():
    E[f'be_pkg_{b}'] = E.prot_pkg * v
    E[f'be_serv_{b}'] = E.prot_serv * v
def q(x):
    x = x.dropna()
    return {'n': int(len(x)), 'median': float(x.median()), 'p25': float(x.quantile(.25)), 'p75': float(x.quantile(.75))} if len(x) else None
R['breakeven'] = {'all_E2': {b: {'package': q(E[f'be_pkg_{b}']), 'serving': q(E[f'be_serv_{b}'])} for b in BEN},
                  'all_E1': {b: {'package': q(E[E.E1][f'be_pkg_{b}']), 'serving': q(E[E.E1][f'be_serv_{b}'])} for b in BEN},
                  'E2_excl_kind_mismatch': {b: q(E[~E.pkg_kind_mismatch][f'be_pkg_{b}']) for b in BEN},
                  'protein_per_package_E2': q(E.prot_pkg), 'protein_per_serving_E2': q(E.prot_serv)}
R['breakeven_by_category'] = {}
for c, g in E.groupby('branded_food_category'):
    if g.prot_pkg.notna().sum() < 20: continue
    R['breakeven_by_category'][c] = {'n_pkg': int(g.prot_pkg.notna().sum()), 'n_serv': int(g.prot_serv.notna().sum()), 'prot_pkg': q(g.prot_pkg), 'prot_serv': q(g.prot_serv),
                                     **{f'pkg_{b}': q(g[f'be_pkg_{b}']) for b in BEN}, **{f'serv_{b}': q(g[f'be_serv_{b}']) for b in BEN}}
# breakeven per 100 g / 100 ml of product, used for comparisons that do not depend on package size
E['be_100g_median4'] = E.protein * BEN['median4']
R['breakeven']['per100_median4_E2'] = q(E.be_100g_median4)
E[['fdc_id', 'branded_food_category', 'E1', 'protein', 'prot_serv', 'pkg_amount', 'pkg_kind', 'basis', 'prot_pkg'] + [f'be_pkg_{b}' for b in BEN] + [f'be_serv_{b}' for b in BEN]].to_csv(f'{RES}/breakeven_products.csv.gz', index=False)

# ---- B3: brand-line twins, breakeven premium per 100 g ----
T = pd.read_csv(f'{RES}/twin_groups.csv')
T = T[(T.p_twin > 0) & T.p_exp.notna()].copy()
T['ratio'] = T.p_exp / T.p_twin; T['p_star'] = T.ratio - 1
R['B3'] = {'n_groups': len(T), 'median_ratio': float(T.ratio.median()), 'p25_ratio': float(T.ratio.quantile(.25)), 'p75_ratio': float(T.ratio.quantile(.75)),
           'share_ratio_le1': float((T.ratio <= 1).mean()),
           'share_pstar_ge': {name: float((T.p_star >= p).mean()) for name, p in PREMIUM_SCENARIOS.items()},
           'median_protein_per_dollar_ratio_at': {name: float((T.ratio / (1 + p)).median()) for name, p in PREMIUM_SCENARIOS.items()},
           'by_category': {c: {'n': int(len(g)), 'median_ratio': float(g.ratio.median()), 'share_pstar_ge_0.50': float((g.p_star >= .5).mean())}
                           for c, g in T.groupby('category') if len(g) >= 8}}
T.to_csv(f'{RES}/twin_groups_ratio.csv', index=False)
json.dump(R, open(f'{RES}/prices.json', 'w'), indent=1, default=float)
print(W[['key', 'price_mean12', 'price_latest', 'protein_g_per100g', 'usd_per_10g_protein', 'usd_per_10g_protein_min', 'usd_per_10g_protein_max']].round(3).to_string())
print(json.dumps(BEN, indent=1)); print(json.dumps(R['breakeven']['all_E2']['median4'])); print(json.dumps({k: v for k, v in R['B3'].items() if k != 'by_category'}, indent=1))
for c, v in R['breakeven_by_category'].items(): print(f"{c[:40]:40s} n={v['n_pkg']} protpkg={v['prot_pkg']['median']:.0f} pkg_eggs={v['pkg_eggs']['median']:.2f} pkg_beans={v['pkg_beans_dry']['median']:.2f} serv_eggs={v['serv_eggs']['median'] if v['serv_eggs'] else None}")
