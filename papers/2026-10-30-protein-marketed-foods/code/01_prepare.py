"""Build the analysis frame from the FDC Branded Foods extract.
Input: data/raw/fdc_branded_extract_main.tsv.gz, fdc_branded_extract_ingredients.tsv.gz, fdc_branded_summary_counts.tsv.gz
Output: data/derived/products.pkl, results/sample.json"""
import json
import numpy as np, pandas as pd
from common import *

rd = lambda f: pd.read_csv(f'{RAW}/{f}', sep='\t', dtype=str, quoting=3, keep_default_na=False)
m = rd('fdc_branded_extract_main.tsv.gz'); ing = rd('fdc_branded_extract_ingredients.tsv.gz'); sm = rd('fdc_branded_summary_counts.tsv.gz')
S = {'extract_rows': len(m)}

# ---- whole-release counts (latest record per GTIN, computed in the browser pass; see 00_browser_extract.js) ----
sm['n'] = sm.n.astype(int)
S['release_latest_gtins'] = int(sm.n.sum())
S['release_by_country'] = sm.groupby('market_country').n.sum().sort_values(ascending=False).to_dict()
us_all = sm[sm.market_country.isin(US)]
us_live = us_all[us_all.discontinued == '0']
S['us_latest_gtins'] = int(us_all.n.sum()); S['us_not_discontinued'] = int(us_live.n.sum())
S['us_live_protein_text'] = int(us_live[us_live.protein_text == '1'].n.sum())
S['us_live_added_sugar_cov'] = float(us_live[us_live.has_added_sugar == '1'].n.sum() / us_live.n.sum())
cov = us_live.groupby('avail_year').apply(lambda d: pd.Series({'n': d.n.sum(), 'cov': d[d.has_added_sugar == '1'].n.sum() / d.n.sum()}), include_groups=False)
S['us_live_added_sugar_cov_by_year'] = {k: {'n': int(v.n), 'cov': float(v['cov'])} for k, v in cov.iterrows()}

# ---- US, not discontinued ----
m = m[m.market_country.isin(US) & (m.discontinued_date == '')].copy()
m['name'] = (m.description + ' | ' + m.brand_name + ' | ' + m.subbrand_name)
m['E2'] = m.name.str.contains(E2_RE); m['E1'] = m.name.str.contains(E1_RE) & m.E2
S['us_live_E2_check'] = int(m.E2.sum()); S['us_live_E1'] = int(m.E1.sum())
S['us_live_E1_in_description_only'] = int(m.description.str.contains(E1_RE).sum())
cnt = m[m.E2].groupby('branded_food_category').size()
cats = sorted(cnt[cnt >= MIN_E2_PER_CATEGORY].index)
S['n_categories'] = len(cats)
S['E2_outside_categories'] = int(m[m.E2 & ~m.branded_food_category.isin(cats)].shape[0])
d = m[m.branded_food_category.isin(cats)].copy()
assert set(d.in_scope) == {'1'}, 'category rule mismatch with extract'
S['category_rows_before_dedup'] = len(d)

# ---- GTIN check: the extract keeps the max fdc_id per raw gtin_upc; also collapse leading-zero variants ----
d['gtin_norm'] = d.gtin_upc.str.lstrip('0')
d['fdc_int'] = d.fdc_id.astype(int)
d = d.sort_values('fdc_int')
dup = d.duplicated('gtin_norm', keep='last')
S['dropped_leading_zero_gtin_duplicates'] = int(dup.sum())
d = d[~dup]

# ---- nutrients ----
for c in ['protein', 'fat', 'carb', 'kcal', 'sodium', 'added_sugar', 'sugars', 'satfat', 'fiber', 'serving_size']:
    d[c] = pd.to_numeric(d[c].replace('', np.nan), errors='coerce')
bad = (d.protein.isna() | d.kcal.isna() | (d.protein < 0) | (d.protein > 100) | (d.kcal < 0) | (d.kcal > 950)
       | (d[['protein', 'fat', 'carb']].fillna(0).sum(axis=1) > 105) | (d.sodium > 40000) | (d.added_sugar > 100) | (d.satfat > 100))
S['dropped_missing_or_implausible'] = int(bad.sum())
d = d[~bad].copy()
S['n_analysis'] = len(d); S['n_E2'] = int(d.E2.sum()); S['n_E1'] = int(d.E1.sum())

d['basis'] = np.where(d.serving_size_unit.str.lower().isin(['ml', 'mlt']), 'volume', 'mass')
okserv = d.serving_size_unit.str.lower().isin(['g', 'grm', 'gm', 'ml', 'mlt']) & (d.serving_size > 0) & (d.serving_size < 2000)
d['serving'] = np.where(okserv, d.serving_size, np.nan)
d['prot_serv'] = (d.protein * d.serving / 100).round(0)  # label protein is declared to the nearest gram
d['E3'] = pd.cut(d.prot_serv, [-1, 4.5, 9.5, 1e9], labels=['<5 g', '5-9 g', '>=10 g'])
d['pct_energy_protein'] = np.where(d.kcal > 0, 100 * 4 * d.protein / d.kcal, np.nan)
P = d.protein.where(d.protein >= 1)        # per-protein outcomes only where protein >= 1 g per 100 g
for c, o in [('kcal', 'kcal_per10p'), ('added_sugar', 'asug_per10p'), ('sugars', 'sug_per10p'), ('sodium', 'na_per10p'), ('satfat', 'sfa_per10p'), ('fiber', 'fib_per10p')]:
    d[o] = 10 * d[c] / P
K = d.kcal.where(d.kcal >= 10)
for c, o in [('added_sugar', 'asug_per100k'), ('sugars', 'sug_per100k'), ('sodium', 'na_per100k'), ('satfat', 'sfa_per100k'), ('fiber', 'fib_per100k'), ('protein', 'prot_per100k')]:
    d[o] = 100 * d[c] / K
d['year'] = pd.to_numeric(d.available_date.str[:4], errors='coerce')
d['post2023'] = d.year >= 2023

# ---- package ----
pk = d.package_weight.apply(parse_package)
d['pkg_amount'] = [a for a, k in pk]; d['pkg_kind'] = [k for a, k in pk]
d.loc[(d.pkg_amount < 5) | (d.pkg_amount > 20000), 'pkg_amount'] = np.nan
d['pkg_kind_mismatch'] = d.pkg_amount.notna() & (d.pkg_kind != d.basis)
d['prot_pkg'] = d.protein * d.pkg_amount / 100     # assumes 1 g = 1 ml when package and nutrient basis differ (flagged)
S['pkg_parsed_share'] = float(d.pkg_amount.notna().mean()); S['pkg_parsed_share_E2'] = float(d[d.E2].pkg_amount.notna().mean())
S['pkg_kind_mismatch_share_of_parsed'] = float(d.pkg_kind_mismatch.sum() / d.pkg_amount.notna().sum())

# ---- ingredients ----
ing = ing.set_index('fdc_id').ingredients
d['ingredients'] = d.fdc_id.map(ing).fillna('')
has = d.ingredients.str.strip() != ''
for k, rx in MARK_RE.items():
    d[f'm_{k}'] = np.where(has, d.ingredients.str.contains(rx).astype(float), np.nan)
d['m_collagen'] = np.where(has, d.ingredients.str.contains(COLLAGEN_RE).astype(float), np.nan)
d['upf_classes'] = d[[f'm_{k}' for k in UPF_CLASSES]].sum(axis=1, min_count=1)
d['upf_classes_excl_isolate'] = d[[f'm_{k}' for k in UPF_CLASSES if k != 'isolate']].sum(axis=1, min_count=1)
d['upf_any'] = (d.upf_classes > 0).astype(float).where(has)
d['n_ingr'] = d.ingredients.apply(n_ingredients)
S['ingredients_present_share'] = float(has.mean())

# ---- brand-line key for twins ----
norm = lambda s: s.str.upper().str.replace(r'[^A-Z0-9 ]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()
d['brand_key'] = norm(d.brand_owner) + ' || ' + np.where(norm(d.brand_name) != '', norm(d.brand_name), norm(d.brand_owner))
d['twin_key'] = d.brand_key + ' || ' + d.branded_food_category
d.drop(columns=['ingredients']).to_pickle(f'{DER}/products.pkl')
d[['fdc_id', 'ingredients']].to_pickle(f'{DER}/ingredients.pkl')

S['categories'] = {c: {'n': int((d.branded_food_category == c).sum()), 'E2': int(((d.branded_food_category == c) & d.E2).sum()),
                       'E1': int(((d.branded_food_category == c) & d.E1).sum())} for c in cats}
json.dump(S, open(f'{RES}/sample.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in S.items() if k not in ('categories', 'release_by_country')}, indent=1))
