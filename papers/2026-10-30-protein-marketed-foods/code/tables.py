"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os
import pandas as pd
from common import RES, ROOT
C = json.load(open(f'{RES}/composition.json')); P = json.load(open(f'{RES}/prices.json')); S = json.load(open(f'{RES}/sample.json'))
f0 = lambda v: f'{v:,.0f}'; f1 = lambda v: f'{v:,.1f}'; f2 = lambda v: f'{v:,.2f}'
def fmt(v, k):
    if k in ('na_per100k', 'na_per10p', 'kcal_per10p', 'kcal'): return f1(v)
    return f2(v) if abs(v) < 10 else f1(v)

# Table 1
E3 = C['E3']['crosstab']; t1 = ['**Table 1.** Label protein per labelled serving, by name tier. US products in FoodData Central Branded Foods (release 2026-04-30), latest record per GTIN, not discontinued, in the 34 categories with at least 20 protein-named products, with a gram or millilitre serving size. Protein per serving was computed from the per-100 g value and rounded to the nearest gram. Under 21 CFR 101.54(b)(1) and (c)(1) a "high" claim requires 20% of the 50 g Daily Value (10 g) and a "good source" claim 10–19% (5–9.5 g) per reference amount customarily consumed, after correction for protein quality; meal and main-dish products follow separate rules (101.54(b)(2), (c)(2)). The columns are therefore an upper bound on eligibility.', '',
      '| Name tier | Products | < 5 g | 5–9 g | ≥ 10 g |', '|:--|--:|--:|--:|--:|']
for r, lab in [('E1', 'E1: claim-like wording ("high protein", "20 g protein", "protein+")'), ('E2 only', 'E2 only: "protein" elsewhere in name, brand or sub-brand'), ('Not protein-named', 'Not protein-named')]:
    x = E3[r]; n = sum(x.values())
    t1.append(f"| {lab} | {n:,} | {x['<5 g']:,} ({100*x['<5 g']/n:.1f}%) | {x['5-9 g']:,} ({100*x['5-9 g']/n:.1f}%) | {x['>=10 g']:,} ({100*x['>=10 g']/n:.1f}%) |")

# Table 2
rows = [('protein', 'Protein, g/100 g'), ('pct_energy_protein', 'Protein, % of energy'), ('kcal', 'Energy, kcal/100 g'),
        ('asug_per100k', 'Added sugars, g/100 kcal†'), ('sug_per100k', 'Total sugars, g/100 kcal'), ('na_per100k', 'Sodium, mg/100 kcal'), ('sfa_per100k', 'Saturated fat, g/100 kcal'),
        ('fib_per100k', 'Fibre, g/100 kcal'), ('kcal_per10p', 'Energy per 10 g protein, kcal'), ('asug_per10p', 'Added sugars per 10 g protein, g†'), ('na_per10p', 'Sodium per 10 g protein, mg'),
        ('n_ingr', 'Ingredients, n'), ('upf_classes', 'Marker classes, n of 9'), ('upf_classes_excl_isolate', 'Marker classes excluding protein isolates, n of 8'),
        ('m_isolate', 'Protein isolate, concentrate or hydrolysate, %'), ('m_sweetener', 'Non-sugar sweetener or polyol, %'), ('m_flavour', 'Flavouring, %'),
        ('m_emulsifier', 'Emulsifier, %'), ('m_thickener', 'Thickener or gum, %'), ('m_sugar_type', 'Sugar- or fibre-type substance, %'), ('m_collagen', 'Collagen or gelatin, %')]
t2 = [f"**Table 2.** Composition of protein-named (E2) products compared with other products in the same category (C1) and with the same brand line's products in the same category that do not use the word (C2). Per-100 kcal outcomes exclude products under 10 kcal per 100 g; per-10 g-protein outcomes exclude products under 1 g protein per 100 g. C1: medians (or percentages) over all products, and the within-category difference averaged across categories with weights equal to the number of protein-named products (bootstrap 95% CI, 1,000 replicates). C2: {C['C2']['n_groups']} brand-line groups (brand owner × brand × category) containing both kinds of product; difference = protein-named minus other, per group; median of group differences for continuous outcomes, mean for percentages (bootstrap 95% CI over groups); Holm-adjusted Wilcoxon signed-rank P across all {sum('holm_p' in v for v in C['C2']['outcomes'].values())} C2 outcomes tested ({len(rows)} shown). † Added sugars were reported for {100*C['added_sugar_coverage']['E2']:.0f}% of protein-named and {100*C['added_sugar_coverage']['nonE2']:.0f}% of other products.", '',
      '| Outcome | Protein-named | Same category, other | C1 within-category difference (95% CI) | C2 brand-line difference (95% CI) | C2 groups | C2 Holm P |', '|:--|--:|--:|--:|--:|--:|--:|']
for k, lab in rows:
    a = C['C1_E2'][k]; b = C['C2']['outcomes'][k]
    mean = C['outcomes'][k]['stat'] == 'mean'
    bd, bci = (b['mean_group_diff'], b['mean_ci']) if mean else (b['median_group_diff'], b['ci'])
    p = b.get('holm_p'); ps = '<0.001' if p < 0.001 else f'{p:.3f}'
    t2.append(f"| {lab} | {fmt(a['exp_overall'], k)} | {fmt(a['cmp_overall'], k)} | {fmt(a['pooled_diff'], k)} ({fmt(a['ci'][0], k)} to {fmt(a['ci'][1], k)}) | {fmt(bd, k)} ({fmt(bci[0], k)} to {fmt(bci[1], k)}) | {b['n_groups']} | {ps} |")

# Table 3
lab = {'eggs': 'Eggs, grade A large', 'milk_whole': 'Milk, whole', 'beans_dry': 'Beans, dried', 'chicken_breast': 'Chicken breast, boneless', 'milk_lowfat': 'Milk, low-fat, reduced-fat or skim',
       'ground_beef': 'Ground beef, 100% beef', 'ground_beef_lean': 'Ground beef, lean and extra lean', 'cheddar': 'Cheddar cheese', 'yogurt': 'Yogurt', 'bread_white': 'Bread, white pan', 'rice_white': 'Rice, white, long grain, uncooked'}
unit = {'eggs': 'dozen', 'milk_whole': 'gallon', 'milk_lowfat': 'gallon', 'yogurt': '8 oz'}
W = pd.DataFrame(P['whole_foods']).sort_values('usd_per_10g_protein')
t3 = [f"**Table 3.** Whole-food cost of protein, US city average. Prices are the mean of the BLS Average Price series over October 2025 to September 2026 (no value was published for October 2025, so {int(W.n_months.iloc[0])} months); composition from SR Legacy (SR item averaged where several are listed in the code). Range: lowest and highest monthly price. Bold rows are the four benchmarks used for breakeven prices; their median is US${10*P['benchmarks_usd_per_g_protein']['median4']:.3f} per 10 g protein.", '',
      '| Food (BLS series) | Mean price, US$ per unit | Protein, g/100 g | US$ per 10 g protein (range) | US$ per 100 kcal |', '|:--|--:|--:|--:|--:|']
for _, r in W.iterrows():
    nm = f"{lab[r.key]} ({r.bls_series})"; nm = f'**{nm}**' if r.benchmark else nm
    t3.append(f"| {nm} | {r.price_mean12:.2f} per {unit.get(r.key, 'lb')} | {r.protein_g_per100g:.2f} | {r.usd_per_10g_protein:.3f} ({r.usd_per_10g_protein_min:.3f}–{r.usd_per_10g_protein_max:.3f}) | {r.usd_per_100kcal:.3f} |")

# Table 4
B = P['breakeven_by_category']; cs = sorted(B, key=lambda c: -B[c]['n_pkg'])[:14]
t4 = ['**Table 4.** Breakeven prices for protein-named products: the price at which the product would supply protein as cheaply as each whole-food benchmark (Table 3). Per serving: label protein per labelled serving × benchmark cost per gram. Per package: protein per 100 g × parsed package weight × benchmark cost per gram, against the median of the four benchmarks; package weight in FDC may refer to a single unit or a multipack, so per-package values are less reliable. Medians (interquartile range) in US$. Categories shown are the 14 with the most protein-named products that have a parsed package weight. These are thresholds, not observed prices.', '',
      '| Category | Products with serving size (with package weight) | Protein per serving, g | Eggs | Whole milk | Dry beans | Chicken breast | Per package, median of four |', '|:--|--:|--:|--:|--:|--:|--:|--:|']
q = lambda x, dp=2: f"{x['median']:.{dp}f} ({x['p25']:.{dp}f}–{x['p75']:.{dp}f})"
for c in cs:
    b = B[c]
    t4.append(f"| {c} | {b['n_serv']:,} ({b['n_pkg']:,}) | {q(b['prot_serv'], 0)} | {q(b['serv_eggs'])} | {q(b['serv_milk_whole'])} | {q(b['serv_beans_dry'])} | {q(b['serv_chicken_breast'])} | {q(b['pkg_median4'])} |")
a = P['breakeven']['all_E2']
t4.append(f"| All protein-named products | {a['median4']['serving']['n']:,} ({a['median4']['package']['n']:,}) | {q(P['breakeven']['protein_per_serving_E2'], 0)} | {q(a['eggs']['serving'])} | {q(a['milk_whole']['serving'])} | {q(a['beans_dry']['serving'])} | {q(a['chicken_breast']['serving'])} | {q(a['median4']['package'])} |")

tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n\n' + '\n'.join(t4) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
