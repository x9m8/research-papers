"""Graphical abstract (900 px wide PNG): wording vs gist, people vs language models."""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HUM, CHAT, BASE, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#1baf7a', '#0b0b0b', '#52514e', '#e4e3df'
C = json.load(open('../results/compare_results.json'))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': MUTED, 'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.grid': True, 'grid.color': GRID,
                     'axes.axisbelow': True})
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), dpi=100)
groups = [('People', [v['exact_rate'] for v in C['human'].values()], HUM),
          ('Chat models', [C['models'][k]['exact_rate'] for k in list(C['models'])[:5]], CHAT),
          ('Base models', [C['models'][k]['exact_rate'] for k in list(C['models'])[5:]], BASE)]
for i, (lab, v, c) in enumerate(groups):
    ax[0].bar(i, np.mean(v), color=c, width=0.6)
    ax[0].plot([i, i], [min(v), max(v)], color=INK, lw=1.5)
    ax[0].text(i, max(v) + 0.03, f'{min(v):.0%}–{max(v):.0%}' if max(v) > 0.01 else '≈0%', ha='center', fontsize=10, color=INK)
ax[0].set_xticks(range(3)); ax[0].set_xticklabels([g[0] for g in groups]); ax[0].grid(axis='x', visible=False)
ax[0].set_ylim(0, 0.8); ax[0].set_ylabel('Exact copies per hand-off')
ax[0].set_title('Wording: models rephrase, not copy', loc='left', fontsize=11, color=INK)
groups2 = [('People', [v['plateau'] for v in C['human'].values()], HUM),
           ('Chat models', [C['models'][k]['plateau'] for k in list(C['models'])[:5]], CHAT),
           ('Base models', [C['models'][k]['plateau'] for k in list(C['models'])[5:]], BASE)]
for i, (lab, v, c) in enumerate(groups2):
    ax[1].bar(i, np.mean(v), color=c, width=0.6)
    ax[1].plot([i, i], [min(v), max(v)], color=INK, lw=1.5)
    ax[1].text(i, max(v) + 0.015, f'{min(v):.2f}–{max(v):.2f}', ha='center', fontsize=10, color=INK)
ax[1].set_xticks(range(3)); ax[1].set_xticklabels([g[0] for g in groups2]); ax[1].grid(axis='x', visible=False)
ax[1].set_ylim(0, 0.45); ax[1].set_ylabel('Long-run share of original words')
ax[1].set_title('Gist: similar for people and models', loc='left', fontsize=11, color=INK)
fig.text(0.01, 0.005, 'Bars: mean across datasets or models; lines: range. Rephrase chains (Perez et al., 2025) vs human recall (Kalafatis, 2026).',
         fontsize=7.5, color=MUTED)
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig('../figures/graphical_abstract.png', dpi=100)
print('graphical abstract written')
