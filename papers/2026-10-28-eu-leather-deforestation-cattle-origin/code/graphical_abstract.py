"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
o = json.load(open(f'{RES}/analysis.json')); b = o['bridge_2015_2020_ha']
BLUE, ORANGE, GREEN, YELLOW, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Where the cattle were raised', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'Deforestation in EU leather use, hides traced through tanning and manufacturing countries (2015–2020, 5% rule)', fontsize=10.5, color=MUTED)
rows = [('Direct imports of hides\nand leather, by exporter', f"{b['Exporter attribution, hides and leather']:,} ha", YELLOW),
        ('Added by imported\nleather goods', f"+{b['Articles imported, traced to cattle origin']:,}", GREEN),
        ('Other terms*', f"+{b['Re-attribution of hides and leather imports to cattle origin'] + b['EU-produced hides']:,}", MUTED),
        ('Removed by EU exports\nof leather and goods', f"−{-b['Minus EU exports (all stages), traced']:,}", ORANGE),
        ('EU use, traced\nto cattle origin', f"{b['Stage-wise tracing (model)']:,} ha", BLUE)]
for i, (k, v, col) in enumerate(rows):
    x = 0.03 + i * 0.185
    fig.text(x, 0.6, k, fontsize=8.5, color=MUTED, va='bottom'); fig.text(x, 0.45, v, fontsize=18, weight='bold', color=col)
sh = o['all_indirect_share_ha_2015_2020']; br = o['origin_share_ha_2015_2020']['Stage-wise tracing']['Brazil']
fig.text(0.04, 0.26, f'{100 * sh:.0f}% of the traced hectares reach the EU through a third country, mostly as goods, led by China and Viet Nam;', fontsize=10.5, color=INK)
fig.text(0.04, 0.2, f'{100 * br:.0f}% trace back to Brazil. Imported goods add hectares, but EU exports remove more.', fontsize=10.5, color=INK)
fig.text(0.04, 0.1, '*Re-attribution of direct imports to cattle origin and EU-produced hides. Direct imports attributed to the exporting country, as in the companion paper.', fontsize=7.5, color=MUTED)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · BACI, FAOSTAT, DeDuCE v2.1 · Preprint, not peer reviewed', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
