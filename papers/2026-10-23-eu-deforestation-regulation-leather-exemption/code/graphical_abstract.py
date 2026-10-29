"""Graphical abstract, 900 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
A = json.load(open(f'{RES}/analysis.json'))
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Lower economic value, same forest', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, "The EU's leather exemption from its deforestation rules, tested against trade and price data", fontsize=11, color=MUTED)
m = A['mean_2015_2020']; bc = A['benefit_cost_2015_2020']
rows = [('Hide price ÷ beef price', f"{A['price_ratio']['2005']:.2f} → {A['price_ratio']['2025']:.2f}", 'EU import prices, 2005 → 2025', ORANGE),
        ('Deforestation in EU imports', f"{m['By-product (SWD), 2.5%']/1000:.0f}k–{m['Mass, FAOSTAT weights']/1000:.0f}k ha", 'per year, 2015–2020, seven allocation rules', BLUE),
        ('Benefit ÷ cost', f"{min(A['benefit_cost_2022'].values()):.0f}–{max(bc.values()):.0f}×", "Commission's gross valuation, 2015–2022", GREEN)]
for i, (k, v, s, c) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=22, weight='bold', color=c); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.24, "DeDuCE's 5% leather share is a fixed constant. A price-based share fell from about 7% (2005) to about 3% (2022):", fontsize=10.5, color=INK)
fig.text(0.04, 0.18, 'cheaper hides shrink the hectares charged to leather, not the forest cleared for cattle.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Eurostat Comext, FAOSTAT, DeDuCE v2.0; Commission SWD(2026) 194', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
