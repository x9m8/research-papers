"""Part A: protein-marketed (E1/E2) products vs same-category (C1) and same-brand-line (C2) comparators; E3 eligibility.
Output: results/composition.json"""
import json, warnings
import numpy as np, pandas as pd
from scipy import stats
from common import *
warnings.filterwarnings('ignore')
rng = np.random.default_rng(SEED); B = 1000
d = pd.read_pickle(f'{DER}/products.pkl')
cats = sorted(d.branded_food_category.unique())
R = {}

OUT = [('protein', 'Protein, g per 100 g', 'med'), ('kcal', 'Energy, kcal per 100 g', 'med'), ('pct_energy_protein', 'Protein, % of energy', 'med'),
       ('kcal_per10p', 'Energy per 10 g protein, kcal', 'med'), ('asug_per10p', 'Added sugars per 10 g protein, g', 'med'),
       ('sug_per10p', 'Total sugars per 10 g protein, g', 'med'), ('na_per10p', 'Sodium per 10 g protein, mg', 'med'),
       ('sfa_per10p', 'Saturated fat per 10 g protein, g', 'med'),
       ('asug_per100k', 'Added sugars per 100 kcal, g', 'med'), ('sug_per100k', 'Total sugars per 100 kcal, g', 'med'),
       ('na_per100k', 'Sodium per 100 kcal, mg', 'med'), ('sfa_per100k', 'Saturated fat per 100 kcal, g', 'med'), ('fib_per100k', 'Fibre per 100 kcal, g', 'med'),
       ('n_ingr', 'Ingredients, n', 'med'), ('upf_classes', 'Marker classes present, n of 9', 'med'), ('upf_classes_excl_isolate', 'Marker classes excl. protein isolates, n of 8', 'med'),
       ('upf_any', 'Any marker class present, %', 'mean'), ('m_isolate', 'Protein isolate/concentrate/hydrolysate, %', 'mean'),
       ('m_sweetener', 'Non-sugar sweetener or polyol, %', 'mean'), ('m_flavour', 'Flavouring, %', 'mean'), ('m_emulsifier', 'Emulsifier, %', 'mean'),
       ('m_thickener', 'Thickener or gum, %', 'mean'), ('m_sugar_type', 'Sugar- or fibre-type substance, %', 'mean'), ('m_collagen', 'Collagen or gelatin, %', 'mean')]
LAB = {k: l for k, l, _ in OUT}; STAT = {k: s for k, _, s in OUT}
R['outcomes'] = {k: {'label': l, 'stat': s} for k, l, s in OUT}

def stat(x, s):
    x = x[~np.isnan(x)]
    if len(x) == 0: return np.nan
    return float(np.median(x)) if s == 'med' else float(100 * np.mean(x))

def boot(x, s):
    x = x[~np.isnan(x)]
    if len(x) == 0: return np.full(B, np.nan)
    idx = rng.integers(0, len(x), (B, len(x)))
    return np.median(x[idx], axis=1) if s == 'med' else 100 * x[idx].mean(axis=1)

# ---------- prevalence and validation ----------
S = json.load(open(f'{RES}/sample.json'))
v = pd.read_csv(f'{ROOT}/data/handcoded_validation.csv')
k, n = int(v.protein_marketed.sum()), len(v)
lo, hi = stats.binomtest(k, n).proportion_ci(method='wilson')
R['validation'] = {'n': n, 'positive': k, 'precision': k / n, 'ci': [lo, hi], 'false_positive_notes': v[v.protein_marketed == 0].note.tolist()}
R['prevalence'] = {'n_analysis': len(d), 'E2': int(d.E2.sum()), 'E1': int(d.E1.sum()), 'E2_share': float(d.E2.mean()), 'E1_share': float(d.E1.mean()),
                   'E2_share_of_US_release': S['us_live_protein_text'] / S['us_not_discontinued']}
top2 = d[d.E2].branded_food_category.value_counts()
R['prevalence']['top2_categories_share_of_E2'] = float(top2.iloc[:2].sum() / top2.sum())

# ---------- E3: eligibility by label protein per labelled serving ----------
e = d[d.prot_serv.notna()]
ct = pd.crosstab(np.where(e.E1, 'E1', np.where(e.E2, 'E2 only', 'Not protein-named')), e.E3)
R['E3'] = {'n_with_serving': len(e), 'crosstab': {r: {c: int(ct.loc[r, c]) for c in ct.columns} for r in ct.index}}
for grp, msk in [('E2', e.E2), ('E1', e.E1), ('nonE2', ~e.E2)]:
    x = e[msk]; R['E3'][grp] = {'n': len(x), 'ge10': float((x.prot_serv >= 9.5).mean()), '5to9': float(((x.prot_serv >= 4.5) & (x.prot_serv < 9.5)).mean()),
                                'lt5': float((x.prot_serv < 4.5).mean()), 'median_prot_serv': float(x.prot_serv.median())}
R['E3']['nonE2_ge10_n'] = int(((~e.E2) & (e.prot_serv >= 9.5)).sum())
R['E3']['ge10_share_named'] = float(e[e.prot_serv >= 9.5].E2.mean())
R['E3']['E2_lt5_by_category'] = {c: {'n': int(len(g)), 'lt5': float((g.prot_serv < 4.5).mean())} for c, g in e[e.E2].groupby('branded_food_category') if len(g) >= 20}
R['E3']['nonE2_ge10_by_category'] = e[(~e.E2) & (e.prot_serv >= 9.5)].branded_food_category.value_counts().head(8).to_dict()

# ---------- C1: within-category contrasts ----------
def c1(expo, data, label, outcomes=None):
    res = {}
    for k in (outcomes or LAB):
        s = STAT[k]; diffs, ws, bs, per = [], [], [], {}
        for c, g in data.groupby('branded_food_category'):
            a = g.loc[g[expo], k].to_numpy(float); b = g.loc[~g.E2, k].to_numpy(float)
            na, nb = np.sum(~np.isnan(a)), np.sum(~np.isnan(b))
            if na < 5 or nb < 5: continue
            dd = stat(a, s) - stat(b, s); diffs.append(dd); ws.append(na); bs.append(boot(a, s) - boot(b, s))
            per[c] = {'exp': stat(a, s), 'cmp': stat(b, s), 'n_exp': int(na), 'n_cmp': int(nb)}
        if not diffs: continue
        w = np.array(ws) / np.sum(ws); bsa = np.array(bs)
        pooled = float(np.dot(w, diffs)); pb = np.nansum(bsa * w[:, None], axis=0)
        res[k] = {'pooled_diff': pooled, 'ci': [float(np.nanpercentile(pb, 2.5)), float(np.nanpercentile(pb, 97.5))], 'n_categories': len(diffs),
                  'n_exp': int(np.sum(ws)), 'share_categories_positive': float(np.mean(np.array(diffs) > 0)),
                  'exp_overall': stat(data.loc[data[expo], k].to_numpy(float), s), 'cmp_overall': stat(data.loc[~data.E2, k].to_numpy(float), s), 'per_category': per}
    return res
R['C1_E2'] = c1('E2', d, 'E2')
R['C1_E1'] = c1('E1', d, 'E1')
dd = d[d.post2023]
R['C1_E2_post2023'] = c1('E2', dd, 'E2', ['asug_per10p', 'asug_per100k', 'sug_per100k', 'na_per100k', 'protein', 'upf_classes'])
# coarsened exact matching sensitivity: strata = category x within-category energy-density quintile
d['kq'] = d.groupby('branded_food_category').kcal.transform(lambda x: pd.qcut(x.rank(method='first'), 5, labels=False))
d['stratum'] = d.branded_food_category + ' #' + d.kq.astype(str)
cem = d.rename(columns={'branded_food_category': 'cat0', 'stratum': 'branded_food_category'})
R['C1_E2_CEM'] = {k: {kk: vv for kk, vv in v.items() if kk != 'per_category'} for k, v in
                  c1('E2', cem, 'E2', ['protein', 'asug_per100k', 'sug_per100k', 'na_per100k', 'sfa_per100k', 'asug_per10p', 'na_per10p', 'upf_classes', 'm_sweetener']).items()}

# added-sugar coverage
R['added_sugar_coverage'] = {'E2': float(d[d.E2].added_sugar.notna().mean()), 'nonE2': float(d[~d.E2].added_sugar.notna().mean()),
                             'E2_post2023': float(d[d.E2 & d.post2023].added_sugar.notna().mean()), 'nonE2_post2023': float(d[~d.E2 & d.post2023].added_sugar.notna().mean()),
                             'share_post2023_E2': float(d[d.E2].post2023.mean()), 'share_post2023_nonE2': float(d[~d.E2].post2023.mean())}

# ---------- C2: brand-line twins ----------
grp = d.groupby('twin_key')
tw = d[d.twin_key.isin([g for g, x in grp if x.E2.any() and (~x.E2).any()])]
R['C2'] = {'n_groups': int(tw.twin_key.nunique()), 'n_E2_products': int(tw.E2.sum()), 'n_twin_products': int((~tw.E2).sum()),
           'n_brand_owners': int(tw.brand_owner.str.upper().nunique()), 'outcomes': {}}
pv = {}
for k in LAB:
    s = STAT[k]; rows = []
    for g, x in tw.groupby('twin_key'):
        a = x.loc[x.E2, k].to_numpy(float); b = x.loc[~x.E2, k].to_numpy(float)
        if np.sum(~np.isnan(a)) and np.sum(~np.isnan(b)): rows.append((g, stat(a, s) - stat(b, s), stat(a, s), stat(b, s)))
    if len(rows) < 10: continue
    df = np.array([r[1] for r in rows]); ex = np.array([r[2] for r in rows]); cm = np.array([r[3] for r in rows])
    bi = rng.integers(0, len(df), (B, len(df))); bm = np.median(df[bi], axis=1)
    nz = df[df != 0]
    p = float(stats.wilcoxon(nz).pvalue) if len(nz) >= 10 else np.nan
    pv[k] = p
    bmean = df[bi].mean(axis=1)
    R['C2']['outcomes'][k] = {'n_groups': len(df), 'median_group_diff': float(np.median(df)), 'mean_group_diff': float(np.mean(df)), 'mean_ci': [float(np.percentile(bmean, 2.5)), float(np.percentile(bmean, 97.5))], 'ci': [float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))],
                              'share_positive': float(np.mean(df > 0)), 'share_negative': float(np.mean(df < 0)), 'wilcoxon_p': p,
                              'median_exp': float(np.median(ex)), 'median_twin': float(np.median(cm))}
ks = [k for k in pv if not np.isnan(pv[k])]; order = np.argsort([pv[k] for k in ks]); m = len(ks); adj = {}; run = 0
for r, i in enumerate(order):
    run = max(run, min(1, (m - r) * pv[ks[i]])); adj[ks[i]] = run
for k in adj: R['C2']['outcomes'][k]['holm_p'] = adj[k]
# protein ratio within twin groups (for Part B)
rat = tw.groupby('twin_key').apply(lambda x: pd.Series({'p_exp': x.loc[x.E2, 'protein'].median(), 'p_twin': x.loc[~x.E2, 'protein'].median(),
                                                         'category': x.branded_food_category.iloc[0], 'brand': x.brand_key.iloc[0], 'n_exp': int(x.E2.sum()), 'n_twin': int((~x.E2).sum())}), include_groups=False)
rat.to_csv(f'{RES}/twin_groups.csv')
# a few illustrative named pairs (largest twin groups in selected categories)
ex = rat.sort_values('n_exp', ascending=False)
R['C2']['examples'] = [{'brand_line': b.split(' || ')[1], 'category': r['category'], 'protein_exp': float(r.p_exp), 'protein_twin': float(r.p_twin), 'n_exp': int(r.n_exp), 'n_twin': int(r.n_twin)}
                       for b, r in ex.iterrows() if r['category'] in ('Cereal', 'Snack, Energy & Granola Bars', 'Yogurt', 'Milk', 'Pasta by Shape & Type', 'Frozen Dinners & Entrees')][:12]

# ---------- category table ----------
R['category_table'] = {}
for c, g in d.groupby('branded_food_category'):
    a, b = g[g.E2], g[~g.E2]
    R['category_table'][c] = {'n': len(g), 'n_E2': len(a), 'prot_E2': float(a.protein.median()), 'prot_cmp': float(b.protein.median()),
                              'asug100k_E2': float(a.asug_per100k.median()), 'asug100k_cmp': float(b.asug_per100k.median()),
                              'na100k_E2': float(a.na_per100k.median()), 'na100k_cmp': float(b.na_per100k.median()),
                              'upf_E2': float(a.upf_classes.median()), 'upf_cmp': float(b.upf_classes.median()),
                              'sweet_E2': float(100 * a.m_sweetener.mean()), 'sweet_cmp': float(100 * b.m_sweetener.mean())}
json.dump(R, open(f'{RES}/composition.json', 'w'), indent=1, default=float)
for k in ['protein', 'asug_per100k', 'na_per100k', 'sfa_per100k', 'asug_per10p', 'na_per10p', 'kcal_per10p', 'upf_classes', 'm_sweetener', 'm_isolate']:
    a = R['C1_E2'][k]; b = R['C2']['outcomes'].get(k, {})
    print(f"{LAB[k]:50s} C1 {a['exp_overall']:.2f} vs {a['cmp_overall']:.2f} diff {a['pooled_diff']:.2f} [{a['ci'][0]:.2f},{a['ci'][1]:.2f}] | C2 {b.get('median_group_diff', np.nan):.2f} n={b.get('n_groups')} p={b.get('holm_p', np.nan):.2g}")
print(json.dumps(R['validation']), json.dumps(R['prevalence']), json.dumps({k: v for k, v in R['E3'].items() if 'category' not in k}, default=float), json.dumps(R['added_sugar_coverage']), sep='\n')
print({k: R['C2'][k] for k in ['n_groups', 'n_E2_products', 'n_twin_products', 'n_brand_owners']})
