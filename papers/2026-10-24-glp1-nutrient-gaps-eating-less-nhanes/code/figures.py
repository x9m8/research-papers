import json, numpy as np, pandas as pd
from style import *
from common import RES, FIG, LABEL
C = json.load(open(f'{RES}/curves.json')); P = json.load(open(f'{RES}/prevalence.json'))
r = np.array(C['r']) * 100
fig, ax = plt.subplots(figsize=(7.0, 3.6))
ax.axvspan(16, 39, color=YELLOW, alpha=0.15, lw=0); ax.text(16.5, 103, 'Reductions measured in GLP-1 trials (16–39%)', fontsize=7, color=MUTED, va='bottom')
cols = {'MAGN': MUTED, 'CALC': ORANGE, 'ZINC': BLUE, 'FDFE': GREEN, 'PROT': INK, 'VB12': YELLOW, 'IRON': '#8a63d2'}
ends = {}
for n, c in cols.items():
    y = np.array(C['prev'][n]) * 100; ax.plot(r, y, color=c, lw=2.2 if n == 'PROT' else 1.6); ends[n] = y[-1]
pos = {}; last = -99
for n in sorted(ends, key=ends.get):                     # spread end labels at least 4.2 points apart
    pos[n] = max(ends[n], last + 4.2); last = pos[n]
for n, c in cols.items():
    lab = LABEL[n] + (' (per kg reference weight)' if n == 'PROT' else ' (men; women 51+)' if n == 'IRON' else '')
    ax.text(45.6, pos[n], lab, fontsize=6.8, color=c, va='center')
ax.set_xlim(0, 45); ax.set_ylim(0, max(108, max(pos.values()) + 3)); ax.set_xlabel('Proportional cut in everything eaten, %'); ax.set_ylabel('Share below the EAR, %'); ax.grid(axis='x', visible=False)
save(fig, 'fig1_curves', FIG)
from scipy.stats import t as tdist
M = P['L']['meta']; DF = M['n_psu'] - M['n_strata']; TC = tdist.ppf(0.975, DF)
L = P['L']['res']; keys = ['PROT_ear_refwt', 'ZINC', 'FDFE', 'CALC', 'MAGN', 'VARA', 'VC', 'VB12', 'IRON']
labs = ['Protein', 'Zinc', 'Folate', 'Calcium', 'Magnesium', 'Vit. A', 'Vit. C', 'Vit. B12', 'Iron*']
sc = [('Baseline', LIGHT), ('Semaglutide 1 mg, −24%', BLUE), ('Semaglutide 2.4 mg, −35%', ORANGE)]
fig, ax = plt.subplots(figsize=(7.0, 3.3)); x = np.arange(len(keys)); wdt = 0.27
for i, (s, c) in enumerate(sc):
    v = [100 * L[s][k][0] for k in keys]; e = [100 * TC * L[s][k][1] for k in keys]
    ax.bar(x + (i - 1) * wdt, v, wdt, color=c, label=s.replace('Baseline', 'Usual diet'), yerr=e, error_kw=dict(lw=0.6, capsize=1.5, ecolor=MUTED))
ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=7.5); ax.set_ylabel('Share below the EAR, %'); ax.set_ylim(0, 105); ax.grid(axis='x', visible=False)
ax.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3)
save(fig, 'fig2_scenarios', FIG)
keys3 = [('PROT_ear_refwt', 'EAR,\nreference\nweight'), ('PROT_ear_adjwt', 'EAR,\nadjusted\nweight'), ('PROT_ear_actualwt', 'EAR,\nactual\nweight'),
         ('PROT_below_1.2_refwt', '1.2 g/kg,\nreference\nweight'), ('PROT_below_80g', '80 g\nper day')]
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(wspace=0.3, width_ratios=[1.3, 1]))
a = ax[0]; x = np.arange(len(keys3))
for i, (s, c) in enumerate(sc):
    a.bar(x + (i - 1) * wdt, [100 * L[s][k][0] for k, _ in keys3], wdt, color=c)
a.set_xticks(x); a.set_xticklabels([l for _, l in keys3], fontsize=6.3); a.set_ylabel('Share below threshold, %'); a.set_ylim(0, 105); a.grid(axis='x', visible=False)
a.set_title('A  Protein, five yardsticks (2021–2023)', loc='left', fontsize=8.5, color=INK)
b = ax[1]; k2 = ['VB12', 'FDFE', 'CALC', 'MAGN', 'ZINC']; l2 = ['B12', 'Folate', 'Calcium', 'Magnesium', 'Zinc']; x = np.arange(len(k2))
b.bar(x - 0.2, [100 * P['P']['res']['Semaglutide 2.4 mg, −35%'][k][0] for k in k2], 0.38, color=ORANGE, label='Food only')
b.bar(x + 0.2, [100 * P['P_supp']['res']['Semaglutide 2.4 mg, −35%'][k][0] for k in k2], 0.38, color=GREEN, label='Food + supplements')
b.set_xticks(x); b.set_xticklabels(l2, fontsize=6.8, rotation=30, ha='right'); b.set_ylim(0, 105); b.grid(axis='x', visible=False); b.legend(fontsize=6.8, loc='upper left')
b.set_title('B  −35%, 2017–2020, supplements', loc='left', fontsize=8.5, color=INK)
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=c, label=s.replace('Baseline', 'Usual diet')) for s, c in sc], loc='lower center', ncol=3, fontsize=7, bbox_to_anchor=(0.35, -0.14))
save(fig, 'fig3_sensitivity', FIG); print('ok')
