"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
C = json.load(open(f'{RES}/composition.json')); P = json.load(open(f'{RES}/prices.json'))
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
c1 = C['C1_E2']; be = P['breakeven']['all_E2']
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Paying for protein', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, f"{C['prevalence']['E2']:,} US packaged foods with \"protein\" in the name vs other products in the same categories", fontsize=11, color=MUTED)
rows = [('Protein per 100 g (median)', f"{c1['protein']['exp_overall']:.1f} g vs {c1['protein']['cmp_overall']:.1f} g", 'protein-named vs others', BLUE),
        ('Contain a non-sugar sweetener', f"{c1['m_sweetener']['exp_overall']:.0f}% vs {c1['m_sweetener']['cmp_overall']:.0f}%", 'sucralose, stevia, polyols etc.', ORANGE),
        ('Breakeven price, median product', f"${be['median4']['serving']['median']:.2f}", 'per serving, vs median of 4 staples', GREEN)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=22, weight='bold', color=col); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.26, f"Protein-named products: less added sugar but more sodium per calorie, and more additive classes. {100*C['E3']['E2']['ge10']:.0f}% have", fontsize=10, color=INK)
fig.text(0.04, 0.20, f"at least 10 g protein per serving, yet {100*(1-C['E3']['ge10_share_named']):.0f}% of products that do are not protein-named. For the median product", fontsize=10, color=INK)
fig.text(0.04, 0.14, f"({P['breakeven']['protein_per_serving_E2']['median']:.0f} g protein per serving), eggs and beans are cheaper protein above about \\${be['median4']['serving']['median']:.2f} a serving; all four staples above \\${be['chicken_breast']['serving']['median']:.2f}.", fontsize=10, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · USDA FoodData Central 2026-04 + BLS prices · names, not front-of-pack claims · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
