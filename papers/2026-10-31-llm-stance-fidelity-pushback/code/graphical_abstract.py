"""Graphical abstract, 900 x 420 px."""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
F = json.load(open(f'{RES}/fidelity.json')); G = json.load(open(f'{RES}/gee.json'))
BLUE, ORANGE, GREEN, INK, MUTED = '#2a78d6', '#eb6834', '#13875e', '#0b0b0b', '#52514e'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
m = {s: F['main'][s]['_mean_over_models'] for s in ['factual', 'stereotype', 'debate']}
fig = plt.figure(figsize=(9, 4.2), dpi=100)
fig.text(0.04, 0.89, 'Kept or conceded', fontsize=20, weight='bold', color=INK)
fig.text(0.04, 0.82, 'How often 11 language models keep their stance each time a user pushes back (SYCON-Bench re-analysis)', fontsize=10.5, color=MUTED)
rows = [('Factual claims\n(false presuppositions)', m['factual'], BLUE), ('Stereotype claims\n(normative)', m['stereotype'], ORANGE), ('Debate stance\n(assigned position)', m['debate'], GREEN)]
for i, (k, v, col) in enumerate(rows):
    x = 0.04 + i * 0.32
    fig.text(x, 0.64, k, fontsize=10, color=MUTED, va='center')
    fig.text(x, 0.47, f"r = {v['r']:.2f}", fontsize=24, weight='bold', color=col)
    hl = np.log(0.5) / np.log(v['r'])
    fig.text(x, 0.39, f"per pushback · half-life {hl:.1f} turns", fontsize=9, color=MUTED)
OR = G['A']['C(setting)[T.factual]']['OR']
fig.text(0.04, 0.24, f'On average, factual stances were kept longer than stereotype rejections (odds ratio {OR:.1f}), but retention was not constant', fontsize=10.2, color=INK)
fig.text(0.04, 0.18, 'from turn to turn: it tracked the wording of each pushback and differed between items.', fontsize=10.2, color=INK)
fig.text(0.04, 0.04, 'Kalafatis 2026 · x9m8.com · Secondary analysis of public benchmark data; automated labels, AI-audited · Preprint', fontsize=7.5, color=MUTED)
fig.savefig(f'{FIG}/graphical_abstract.png', dpi=100); print('ok')
