"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG

E = json.load(open(f'{RES}/estimates.json'))['estimates']; D = json.load(open(f'{RES}/descriptives.json')); Bd = json.load(open(f'{RES}/bounds.json'))
BLUE, ORANGE, INK, MUTED = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
l, f = E['lsr_emp']['main'], E['fsr_emp']['main']
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Drive-thru dose–response', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'GLP-1 uptake in Medicare Part D and restaurant employment, 1,275 US counties, 2019–2025', fontsize=11, color=MUTED)
rows = [('Part D uptake, 2019 → 2024', f"{Bd['national_E_2019']:.1f} → {Bd['national_E_2024']:.1f}", 'users per 100 enrollees, US', BLUE),
        ('Limited-service jobs', f"{l['b_pp']:+.1f}%".replace('-', '−'), f"per point; 95% CI {l['lo_pp']:.2f} to {l['hi_pp']:+.2f}".replace('-', '−'), ORANGE),
        ('Full-service jobs', f"{f['b_pp']:+.1f}%".replace('-', '−').replace('+0.0', '0.0'), f"per point; 95% CI {f['lo_pp']:.2f} to {f['hi_pp']:+.2f}".replace('-', '−'), BLUE)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=24, weight='bold', color=col); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.24, 'Neither estimate is statistically distinguishable from zero. The household-panel evidence implies about −0.1% to', fontsize=10.5, color=INK)
fig.text(0.04, 0.18, '−0.3% per point, far inside the confidence interval: public county data cannot yet detect an effect that size.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Observational, not causal · Preprint · Author operates a full-service diner', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
