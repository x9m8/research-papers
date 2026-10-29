"""Graphical abstract, 900 px."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
P = json.load(open(f'{RES}/prevalence.json'))['L']['res']; C = json.load(open(f'{RES}/curves.json'))['counts']
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
b, c = P['Baseline'], P['Semaglutide 2.4 mg, −35%']
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, 'Eating less of the same', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, 'Modelled nutrient gaps if US adults eligible for GLP-1 drugs eat a third less of their usual diet', fontsize=11, color=MUTED)
rows = [('Below the EAR for zinc', f"{100*b['ZINC'][0]:.0f}% → {100*c['ZINC'][0]:.0f}%", 'usual diet → 35% cut', BLUE),
        ('Below the EAR for protein*', f"{100*b['PROT_ear_refwt'][0]:.0f}% → {100*c['PROT_ear_refwt'][0]:.0f}%", '*per kg of reference weight', ORANGE),
        ('Short on 5+ of 8 nutrients', f"{100*C['0']['ge5']:.0f}% → {100*C['0.35']['ge5']:.0f}%", 'usual diet → 35% cut', GREEN)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=24, weight='bold', color=col); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.24, 'NHANES 2021–2023, n = 2,134 (about 115 million adults); usual intake cut by 16–39%, the reductions measured', fontsize=10.5, color=INK)
fig.text(0.04, 0.18, 'in GLP-1 trials. Keeping nutrients level means eating differently, not just less.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Simulation, not a study of users · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
