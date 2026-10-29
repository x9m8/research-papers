"""Graphical abstract, 900 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
R = json.load(open(f'{RES}/results.json')); G = R['grid']
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
f0, m0 = G['F|0.0|0.8']['cost_scaled'], G['M|0.0|0.8']['cost_scaled']; f24, m24 = G['F|0.24|0.8'], G['M|0.24|0.8']
sv = lambda c0, c: 100 * (1 - c / c0)
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Eating less, eating differently', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'What a nutritionally adequate diet costs US adults eligible for GLP-1 drugs, at a 24% cut in calories', fontsize=11, color=MUTED)
rows = [('Grocery saving, same food', '24%', 'eating less of the current diet', MUTED),
        ('Grocery saving, adequate diet', f"{sv(f0, f24['adequate']['cost']):.0f}–{sv(m0, m24['adequate']['cost']):.0f}%", 'closest diet meeting requirements*', BLUE),
        ('Calories moved to other foods', f"{100*f24['adequate']['realloc']:.0f}–{100*m24['adequate']['realloc']:.0f}%", 'eggs, nuts, legumes, milk, cereal up', ORANGE)]
for i, (k, v, s, c) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=24, weight='bold', color=c); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.24, 'The cheapest adequate diets cost less than the Thrifty Food Plan. The barrier is how much people change', fontsize=10.5, color=INK)
fig.text(0.04, 0.18, 'what they eat, not money. *All requirements in the food database except vitamins D and E.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · NHANES 2017–2020 food records, USDA prices in 2026 dollars · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
