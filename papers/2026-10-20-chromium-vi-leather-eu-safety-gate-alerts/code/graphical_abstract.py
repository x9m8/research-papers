"""Graphical abstract, 900 px wide."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from common import RES, FIG
A = json.load(open(f'{RES}/analysis.json')); Y = pd.DataFrame(A['B_series'])
BLUE, ORANGE, GREEN, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Fewer alerts, same allergy', fontsize=19, weight='bold', color=INK)
fig.text(0.04, 0.83, 'Hexavalent chromium in EU leather goods, before and after the 2015 limit', fontsize=11, color=MUTED)
ax = fig.add_axes([0.06, 0.17, 0.48, 0.52])
y = Y[Y.year.between(2005, 2025)]
ax.plot(y.year, y.per1000_all, color=INK, lw=2.2, marker='o', ms=3.5)
ax.axvline(2015.33, color=MUTED, ls='--', lw=1); ax.text(2015.6, 41, 'EU limit\nMay 2015', fontsize=8, color=MUTED, va='top')
ax.set_title('Cr(VI)-in-leather notifications per 1,000 Safety Gate alerts', loc='left', fontsize=10, color=INK)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', color=GRID); ax.set_axisbelow(True); ax.set_xticks([2005, 2010, 2015, 2020, 2025])
b, r = A['B_peak3']['per1000_all'], A['B_recent']['per1000_all']
rows = [('Alerts', f'{b:.0f} → {r:.0f} per 1,000', f'{b / r:.0f}x fewer', BLUE),
        ('Leather failing the limit', '23–35% → 11–13%', 'surveys', ORANGE),
        ('Chromium allergy', '2.3% → 2.1%', 'Danish patients', GREEN)]
for i, (k, v, s, c) in enumerate(rows):
    yy = 0.62 - i * 0.18
    fig.text(0.6, yy + 0.045, k, fontsize=10, color=MUTED)
    fig.text(0.6, yy - 0.015, v, fontsize=15, weight='bold', color=c)
    fig.text(0.6, yy - 0.06, s, fontsize=8.5, color=MUTED)
fig.text(0.04, 0.03, 'Kalafatis 2026 · x9m8.com · EU Safety Gate, ' + f"{A['A']['n']:,}" + ' notifications 2005–2026; surveys and patch tests from published sources',
         fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100)
print('ok')
