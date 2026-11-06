"""Graphical abstract, 900x420 px."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RESULTS, FIG

desc = json.load(open(f'{RESULTS}/descriptives.json'))
rain = json.load(open(f'{RESULTS}/rainfall.json'))
closures = json.load(open(f'{RESULTS}/closures.json'))
trends = json.load(open(f'{RESULTS}/trends.json'))

BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})

fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Rain, not the calendar, moves the needle', fontsize=19, weight='bold', color=INK)
fig.text(0.04, 0.83, 'Enterococcus exceedances at 15 NY State Park beaches on Long Island, 2015–2025',
          fontsize=10.5, color=MUTED)

rows = [
    ('Exceedance rate', f"{100*desc['exceedance_rate']:.1f}%",
     f"{desc['n_samples']:,} samples, no year trend (p={trends['pooled_fe']['year_p_cluster']:.2f})", BLUE),
    ('Odds per cm of rain\n(48h before sampling)', f"×{rain['main_48h']['odds_ratio_per_unit']:.2f}",
     f"p={rain['main_48h']['p_cluster']:.1e}, beach fixed effects", ORANGE),
    ('Closure days, 11 seasons', f"{int(closures['total_closure_days'])}",
     "top 5 beaches = 66% of them (Jones Beach's Zach's Bay alone, 27%)", GREEN),
]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.64, k, fontsize=10, color=MUTED)
    fig.text(x, 0.47, v, fontsize=26, weight='bold', color=col)
    fig.text(x, 0.38, s, fontsize=8.3, color=MUTED, wrap=True)

fig.text(0.04, 0.2, "Great South Bay (7.4%) and Long Island Sound (5.4%) exceeded more often than the open",
          fontsize=10.5, color=INK)
fig.text(0.04, 0.14, "Atlantic (3.8%). Covers NY State Park beaches only — not county- or town-run beaches.",
          fontsize=10.5, color=INK)
fig.text(0.04, 0.03, "Kalafatis 2026 · x9m8.com · Open Data NY + NOAA NCEI · Preprint, not peer reviewed",
          fontsize=7.5, color=MUTED)

fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100)
print('ok')
