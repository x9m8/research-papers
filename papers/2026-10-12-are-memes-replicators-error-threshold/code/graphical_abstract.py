import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
fid = json.load(open('../results/fidelity_results.json'))
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': MUTED})
fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
s = np.logspace(-1.3, 1, 200)
lo, hi = fid['Meylan et al. (spoken)']['mu'], fid['Gistr exp 2']['mu']
ax.fill_between(s, 0.5, np.log(1 + s) / lo, color='#2a78d6', alpha=0.18, lw=0)
ax.fill_between(s, np.log(1 + s) / lo, np.log(1 + s) / hi, color='#2a78d6', alpha=0.38, lw=0)
ax.plot(s, np.log(1 + s) / hi, color='#2a78d6', lw=2); ax.plot(s, np.log(1 + s) / lo, color='#2a78d6', lw=2)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_ylim(0.5, 150); ax.set_xlim(0.05, 10)
ax.axvline(0.2, color=MUTED, ls='--', lw=1)
ax.text(0.215, 0.56, 's ≈ 0.2 (online diffusion)', fontsize=9, color=MUTED, va='bottom', ha='left')
ax.text(0.3, 45, 'Above the band: no exact copy survives.\nContent persists as gist, rebuilt by\nreconstruction (attraction).', fontsize=11, color=INK)
ax.text(2.2, 0.75, 'Below: selection can\nkeep the exact form\n(a replicator)', fontsize=11, color='#1d5ea8', ha='center')
ax.text(4.5, 30, 'measured\nerror rates\n0.03–0.12/word', fontsize=9, color='#1d5ea8', ha='center', va='center')
from matplotlib.ticker import FuncFormatter
fmt=FuncFormatter(lambda v,p: f'{v:g}'); ax.xaxis.set_major_formatter(fmt); ax.yaxis.set_major_formatter(fmt)
ax.set_xlabel('Selective advantage of the intact item, s'); ax.set_ylabel('Longest item kept word-perfect (words)')
ax.set_title('Human memory loses 3–12% of words per retelling', loc='left', fontsize=13, color=INK)
fig.tight_layout(); fig.savefig('../figures/graphical_abstract.png', dpi=100)
print(fig.get_size_inches()*100)
