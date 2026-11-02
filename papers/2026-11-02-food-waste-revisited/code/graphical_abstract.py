"""Graphical abstract, 900 x 420 px."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import FIG, load
R = load('reproduction.json'); U = load('update.json')
h = R['main']['nchs']['headline']; s = U['summary']['nchs|spliced']; mc = U['monte_carlo']['spliced']
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.89, 'US food waste revisited', fontsize=21, weight='bold', color=INK)
fig.text(0.04, 0.82, 'A reproduction of Hall, Guo, Dore & Chow (2009) with public data, updated to 2023', fontsize=11, color=MUTED)
rows = [('Wasted share, 1974 → 2003', f"{h['frac_1974']:.1f}% → {h['frac_2003']:.1f}%", 'reproduced; original: about 30% → almost 40%', BLUE),
        ('Waste per person, 1974 → 2003', f"+{h['waste_increase_pct']:.0f}%", f"{h['waste_1974']:,.0f} → {h['waste_2003']:,.0f} kcal/day", ORANGE),
        ('Wasted share, 2003 → 2023', f"{s['frac_2003']:.1f}% → {s['frac_2023']:.1f}%", f"change {mc['frac_change_2003_2023_pp'][1]:+.1f} pp (parameter 95%: {mc['frac_change_2003_2023_pp'][0]:+.1f} to {mc['frac_change_2003_2023_pp'][2]:+.1f})".replace('-', '−'), GREEN)]
for i, (k, v, sub, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.63, k, fontsize=10.5, color=MUTED); fig.text(x, 0.49, v, fontsize=22, weight='bold', color=col); fig.text(x, 0.42, sub, fontsize=8.3, color=MUTED)
fig.text(0.04, 0.25, 'The published calculation reproduces from public data. The rise to 2003 survives every input check, but the level of', fontsize=10.2, color=INK)
fig.text(0.04, 0.19, 'waste depends on the assumed baseline intake, and after 2003 the climb in the wasted share did not continue.', fontsize=10.2, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · FAOSTAT, NHANES (CDC/NCHS), USDA ERS, EPA · Preprint, not peer reviewed', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
