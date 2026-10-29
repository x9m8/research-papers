"""Graphical abstract, 900 x 420 px."""
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
S = json.load(open(f'{RES}/summary.json')); T = json.load(open(f'{RES}/timeline.json'))
P = pd.read_csv(f'{RES}/prevalence.csv').set_index('code')
N = S['N_included']
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.9, '"Same active ingredient"', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.83, f'What FDA alleged in {N} warning letters on compounded and unapproved semaglutide and tirzepatide, 2023–2026', fontsize=10.5, color=MUTED)
rows = [('Letters issued on three days', f"{100*T['top3_share']:.0f}%", '9 Sep 2025, 20 Feb & 8 Jun 2026', BLUE),
        ('Cited a sameness claim', f"{100*P.loc['C_sameness','pct']:.0f}%", f"{int(P.loc['C_sameness','n'])} of {N} letters", ORANGE),
        ('Cited seller-as-compounder labels', f"{100*P.loc['C_firm_branded','pct']:.0f}%", 'all from 2026 batches', GREEN)]
for i, (k, v, s, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.62, k, fontsize=10.5, color=MUTED); fig.text(x, 0.48, v, fontsize=26, weight='bold', color=col); fig.text(x, 0.41, s, fontsize=9, color=MUTED)
fig.text(0.04, 0.24, f"Telehealth platforms and clinics drew {S['telehealth_like_n']} letters, all citing false or misleading advertising of compounded drugs;", fontsize=10.5, color=INK)
fig.text(0.04, 0.18, 'peptide sellers, online pharmacies and compounders drew unapproved-drug, Rx and CGMP charges.', fontsize=10.5, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Letters are FDA allegations and measure enforcement choices, not market behaviour · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
