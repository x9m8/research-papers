"""Graphical abstract, 900 x 420 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
s = json.load(open(f'{RES}/summary.json')); c = s['changes']; sh = s['share']
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Fewer employers, more firms with no payroll', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'US leather and allied product manufacturing (NAICS 316), Census Bureau data, 2004 to 2023', fontsize=11, color=MUTED)
rows = [('Employer establishments', f"{c['leather_employer_establishments']['2004']:,.0f} → {c['leather_employer_establishments']['2023']:,.0f}", f"{c['leather_employer_establishments']['pct_change']:+.0f}%", BLUE),
        ('Employer employment', f"{c['leather_employer_employment']['2004']/1000:.1f}k → {c['leather_employer_employment']['2023']/1000:.1f}k", f"{c['leather_employer_employment']['pct_change']:+.0f}%", INK),
        ('Nonemployer firms', f"{c['leather_nonemployer_firms']['2004']:,.0f} → {c['leather_nonemployer_firms']['2023']:,.0f}", f"{c['leather_nonemployer_firms']['pct_change']:+.0f}%", ORANGE)]
for i, (k, v, p, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=20, weight='bold', color=col); fig.text(x, 0.41, p, fontsize=11, color=col)
fig.text(0.04, 0.27, f"Nonemployer share of all units: {sh['leather']['2004']:.0f}% → {sh['leather']['2023']:.0f}% in leather; {sh['mfg']['2004']:.0f}% → {sh['mfg']['2023']:.0f}% in all manufacturing.", fontsize=10.5, color=INK)
fig.text(0.04, 0.21, 'The share rose mostly by 2012, was flat to 2021, and rose again in 2022-2023.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Descriptive, County Business Patterns and Nonemployer Statistics · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
