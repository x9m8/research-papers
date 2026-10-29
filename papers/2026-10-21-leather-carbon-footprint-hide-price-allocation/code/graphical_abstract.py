"""Graphical abstract, 900 px wide."""
import json, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
Y = pd.read_csv(f'{RES}/allocation_annual.csv'); S = json.load(open(f'{RES}/summary.json')); K = json.load(open(f'{RES}/carbon.json'))
BLUE, ORANGE, GREEN, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, "Leather's carbon bill follows the hide price", fontsize=19, weight='bold', color=INK)
fig.text(0.04, 0.83, "Economic allocation of US cattle emissions to the hide, 2001–2025", fontsize=11, color=MUTED)
ax = fig.add_axes([0.06, 0.17, 0.48, 0.52])
ax.plot(Y.year, Y.share * 100, color=BLUE, lw=2.4, marker='o', ms=3.5)
ax.axhline(3.5, color=ORANGE, ls=':', lw=1.4); ax.text(2001.5, 3.62, 'EU PEFCR fixed 3.5%', fontsize=8, color=ORANGE)
ax.set_title("Hide's share of a US steer's value, %", loc='left', fontsize=10, color=INK); ax.set_ylim(0, 6.5)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', color=GRID); ax.set_axisbelow(True); ax.set_xticks([2005, 2010, 2015, 2020, 2025])
rows = [('Hide share of steer value', f"{100 * S['early']:.1f}% → {100 * S['late']:.1f}%", '2002–13 vs 2023–25', BLUE),
        ('Farm CO₂e carried by 1 m² leather', f"{K['kg_m2_econ_early']:.0f} → {K['kg_m2_econ_late']:.0f} kg", 'same animal, prices only', ORANGE),
        ('Since 2013', f"hide −{-S['decomp_2013_2025']['hide_pct']:.0f}%, steer +{S['decomp_2013_2025']['live_pct']:.0f}%", 'dollar value per head', GREEN)]
for i, (k, v, s, c) in enumerate(rows):
    yy = 0.62 - i * 0.18
    fig.text(0.6, yy + 0.045, k, fontsize=10, color=MUTED); fig.text(0.6, yy - 0.015, v, fontsize=15, weight='bold', color=c); fig.text(0.6, yy - 0.06, s, fontsize=8.5, color=MUTED)
fig.text(0.04, 0.03, 'Kalafatis 2026 · x9m8.com · BLS PPI WPU0419 scaled to USDA AMS hide prices; USDA ERS steer prices and weights; Rotz et al. 2019', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
