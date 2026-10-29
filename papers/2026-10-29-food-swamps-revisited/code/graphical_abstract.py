"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, pandas as pd
from common import FIG, load
R = load('reproduction.json'); B = load('robustness.json'); U = load('update.json')
G = pd.DataFrame(B['grid']).query("group == 'trad'").set_index('label')
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Food swamps and obesity, re-run', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'A reproduction of Cooksey-Stowers, Schwartz & Brownell (2017) with public data and an open instrument', fontsize=11, color=MUTED)
m = R['main']; ld = U['long_difference']['trad|state FE']
rows = [('OLS reproduced (3 ratios)', f"{min(m[k]['ols_b'] for k in m):.2f}–{max(m[k]['ols_b'] for k in m):.2f}", 'published 0.115–0.125 per unit', BLUE),
        ('Instrument strength (F)', f"{G.loc['Baseline (2007 counts, matched controls, clustered SE)', 'fs_F']:.0f} → {G.loc['Add log population + state fixed effects', 'fs_F']:.2f}", 'after adding log population + state', ORANGE),
        ('Long difference', f"{ld['b']:.3f}", f"SE {ld['se']:.3f}; outlets 2007–16, obesity 2009–18", GREEN)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=24, weight='bold', color=col); fig.text(x, 0.41, s, fontsize=8.5, color=MUTED)
fig.text(0.04, 0.24, 'The cross-sectional association reproduces. The causal estimate rests on highway exits, which track county size;', fontsize=10.5, color=INK)
fig.text(0.04, 0.18, 'with log population and state controls it is uninformative. Changes in outlet mix did not track obesity.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · USDA Food Environment Atlas, ACS, OpenStreetMap, CDC PLACES · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
