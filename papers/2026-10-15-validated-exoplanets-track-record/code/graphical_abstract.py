"""Graphical abstract, 900 px wide."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
A = json.load(open(f'{RES}/analysis.json')); C = A['C_calibration']['morton_by_radius']; B = A['B_all']
BLUE, ORANGE, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Validated, not confirmed', fontsize=19, weight='bold', color=INK)
fig.text(0.04, 0.82, 'How statistically validated exoplanets have held up', fontsize=11.5, color=MUTED)
fig.text(0.04, 0.6, f"{B['n_credited']:,}", fontsize=34, weight='bold', color=BLUE)
fig.text(0.04, 0.53, 'planets validated by statistics\n(Kepler, K2, TESS; 24 papers)', fontsize=10, color=INK, va='top')
fig.text(0.04, 0.3, f"{B['overturned']}", fontsize=34, weight='bold', color=ORANGE)
fig.text(0.04, 0.23, 'later overturned. 12 were brown dwarfs\nor small stars of planetary size', fontsize=10, color=INK, va='top')
ax = fig.add_axes([0.5, 0.2, 0.46, 0.52])
bins = ['<2', '2-4', '4-6', '6-10', '>10']; x = range(5)
ax.bar([i - 0.18 for i in x], [C[b]['expected'] for b in bins], 0.36, color=MUTED, label="Expected from the paper's own odds")
ax.bar([i + 0.18 for i in x], [C[b]['observed'] for b in bins], 0.36, color=ORANGE, label='Actually overturned')
ax.set_xticks(list(x)); ax.set_xticklabels(bins); ax.set_xlabel('Planet radius (Earth radii)', fontsize=9.5)
ax.set_ylim(0, 10.5); ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', color=GRID); ax.set_axisbelow(True)
ax.legend(fontsize=8.5, frameon=False, loc='upper left')
ax.set_title('Morton et al. 2016: 1,284 Kepler validations', fontsize=10, loc='left', color=INK)
fig.text(0.04, 0.03, 'Kalafatis 2026 · x9m8.com · NASA Exoplanet Archive, 15 Oct 2026', fontsize=8, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100)
print('ok')
