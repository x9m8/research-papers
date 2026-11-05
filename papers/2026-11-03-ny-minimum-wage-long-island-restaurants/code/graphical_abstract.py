"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG

E = json.load(open(f'{RES}/estimates.json'))['estimates']; SM = json.load(open(f'{RES}/summary.json'))
BLUE, ORANGE, INK, MUTED = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
m = E['722']['emp']['main']; w = E['722']['wage']['main']
mi = lambda s: s.replace('-', '−')
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Long Island’s higher minimum wage and restaurant jobs', fontsize=18, weight='bold', color=INK)
fig.text(0.04, 0.83, 'Nassau + Suffolk vs 48 upstate New York counties, QCEW 2014–2026', fontsize=11, color=MUTED)
rows = [('Regional wage premium', '$0.30 → $1.80 → $1.00', '2017 → 2022 → 2024–26, per hour', BLUE),
        ('Restaurant jobs vs upstate', mi(f"+{100 * m['post_2024_2026']['est']:.1f}"), 'log points, 2024–26 (not slower growth)', BLUE),
        ('Weekly pay vs upstate', mi(f"{100 * w['post_2024_2026']['est']:.1f}"), 'log points, 2024–26 (levels; wage evidence inconclusive)', ORANGE)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=14 if i == 0 else 24, weight='bold', color=col); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
t = E['722']['robustness']['emp']['trend']; n = E['722']['emp']['main']['implied_elasticity_2023']
fig.text(0.04, 0.25, mi(f"No sign of job losses. But the rise is unlikely to be a wage effect: it continued when the gap narrowed in 2023"), fontsize=10.2, color=INK)
fig.text(0.04, 0.19, mi(f"(elasticity {n['est']:.2f}; 95% interval {n['lo']:.2f} to {n['hi']:.2f}) and is near zero once a trend is allowed ({t['est']:.2f}; {t['lo']:.2f} to {t['hi']:.2f})."), fontsize=10.2, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Observational · Preprint · Author operates a full-service diner in Suffolk County', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
