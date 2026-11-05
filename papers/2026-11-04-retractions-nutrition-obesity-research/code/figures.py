"""Figures 1-3 (300 dpi PNG + PDF) from results/*.json."""
import json, os
import numpy as np
from style import *
from common import RES, FIG, GROUP_LABELS

os.makedirs(FIG, exist_ok=True)
T = json.load(open(f'{RES}/trends.json')); C = json.load(open(f'{RES}/comparison.json')); Z = json.load(open(f'{RES}/citations.json'))
yrs = T['years']; i0 = yrs.index(2000); Y = np.array(yrs[i0:])

# ---- Figure 1: counts and share by retraction year -------------------------------------------------------------------
P = np.array(T['primary'][i0:]); B = np.array(T['primary_bulk'][i0:]); Br = np.array(T['broad'][i0:])
A = np.array(T['all'][i0:]); Bm = np.array(T['biomed'][i0:])
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={'wspace': 0.32})
ax[0].bar(Y, P - B, color=BLUE, width=0.8, label='Primary definition: other reasons')
ax[0].bar(Y, B, bottom=P - B, color=ORANGE, width=0.8, label='Primary: paper mill, peer-review\nmanipulation or computer-generated')
ax[0].plot(Y, Br, color=INK, lw=1.2, marker='o', ms=2.5, label='Broad definition (adds title keywords)')
ax[0].set_ylabel('Retractions per year'); ax[0].set_title('a  Nutrition and obesity retractions', loc='left', fontsize=9)
ax[0].legend(fontsize=6.5, loc='upper left')
k8 = Y >= 2008
ax[1].plot(Y[k8], 100 * P[k8] / A[k8], color=BLUE, lw=1.5, marker='o', ms=2.5, label='Share of all retractions')
ax[1].plot(Y[k8], 100 * P[k8] / Bm[k8], color=GREEN, lw=1.5, marker='s', ms=2.5, label='Share of biomedical retractions')
ax[1].set_ylabel('Per cent'); ax[1].set_ylim(0, 6.2); ax[1].set_title('b  Primary definition as a share', loc='left', fontsize=9)
ax[1].legend(fontsize=6.5, loc='upper left')
for a in ax: a.set_xlabel('Year of retraction notice')
ax[0].set_xlim(1999.3, 2026.7); ax[1].set_xlim(2007.3, 2026.7); ax[0].set_ylim(0, 215)
save(fig, 'fig1_trends', FIG)

# ---- Figure 2: reasons, field vs rest ----------------------------------------------------------------------------------
order = ['misconduct', 'peer_review', 'paper_mill', 'computer_generated', 'image', 'plagiarism', 'duplication', 'fabrication',
         'authorship_dispute', 'ethics_consent', 'error_only', 'limited_info']
R, Rb = C['primary_vs_rest']['reasons'], C['primary_vs_biomed_rest']['reasons']
fig, ax = plt.subplots(figsize=(6.6, 4.2))
RJ0 = C['journal_only_vs_rest']['reasons']
yy = np.arange(len(order))[::-1]
for j, g in enumerate(order):
    from math import sqrt
    p = R[g]['p']; n = R[g]['n']
    ax.plot([min(100 * p, 100 * R[g]['p_comp'], 100 * RJ0[g]['p_comp']), max(100 * p, 100 * R[g]['p_comp'], 100 * RJ0[g]['p_comp'])], [yy[j]] * 2, color=GRID, lw=2, zorder=1)
ax.scatter([100 * R[g]['p_comp'] for g in order], yy, marker='s', s=26, color=MUTED, label='Rest of database, all (n = %s)' % f"{C['primary_vs_rest']['n_comp']:,}", zorder=2)
RJ = C['journal_only_vs_rest']['reasons']
ax.scatter([100 * RJ[g]['p_comp'] for g in order], yy, marker='D', s=22, color=ORANGE, label='Rest of database, journal articles only (n = %s)' % f"{C['journal_only_vs_rest']['n_comp']:,}", zorder=2)
ax.scatter([100 * Rb[g]['p_comp'] for g in order], yy, marker='^', s=26, color=GREEN, label='Rest of biomedical subjects (n = %s)' % f"{C['primary_vs_biomed_rest']['n_comp']:,}", zorder=2)
ax.scatter([100 * R[g]['p'] for g in order], yy, marker='o', s=34, color=BLUE, edgecolor='white', linewidth=0.8,
           label=f"Nutrition and obesity, primary (n = {C['primary_vs_rest']['n']})", zorder=3)
ax.set_yticks(yy); ax.set_yticklabels([GROUP_LABELS[g] for g in order], fontsize=7.5)
ax.set_xlabel('Share of retractions with the reason (%; reasons overlap)'); ax.legend(fontsize=6.8, loc='lower right')
ax.grid(axis='y', visible=False)
save(fig, 'fig2_reasons', FIG)

# ---- Figure 3: time to retraction by reason; citations by years since retraction --------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={'wspace': 0.55, 'width_ratios': [1.05, 1]})
og = ['fabrication', 'duplication', 'plagiarism', 'misconduct', 'paper_mill', 'peer_review', 'error_only']
lab = {'fabrication': 'Fabrication etc.', 'duplication': 'Duplication', 'plagiarism': 'Plagiarism', 'misconduct': 'Any misconduct',
       'paper_mill': 'Paper mill', 'peer_review': 'Peer review', 'error_only': 'Error only'}
yy = np.arange(len(og))[::-1]
for k, (src, col, off, mk, nm) in enumerate([(C['ttr_by_reason_primary'], BLUE, 0.15, 'o', 'Nutrition and obesity'),
                                              (C['ttr_by_reason_rest'], MUTED, -0.15, 's', 'Rest of database')]):
    for j, g in enumerate(og):
        s = src[g]
        ax[0].plot([s['q1'], s['q3']], [yy[j] + off] * 2, color=col, lw=1.4, alpha=0.8)
    ax[0].scatter([src[g]['median'] for g in og], yy + off, color=col, marker=mk, s=22, zorder=3, label=nm)
ax[0].set_yticks(yy); ax[0].set_yticklabels([lab[g] for g in og], fontsize=7.5)
ax[0].set_xlabel('Years from publication to retraction\n(median and interquartile range)'); ax[0].grid(axis='y', visible=False)
ax[0].legend(fontsize=6.5, loc='lower right'); ax[0].set_title('a  Time to retraction', loc='left', fontsize=9)
M = Z['mean_by_years_since']
for g, col, mk, nm in [('field', BLUE, 'o', 'Nutrition and obesity'), ('comparison', MUTED, 's', 'Matched biomedical sample')]:
    ks = sorted((int(s) for s in M[g] if M[g][s]['n'] >= 100))
    ax[1].plot(ks, [M[g][str(s)]['mean'] for s in ks], color=col, marker=mk, ms=3, lw=1.5, label=nm)
ax[1].axvline(0.5, color=ORANGE, lw=1, ls='--'); ax[1].text(1.6, 5.3, 'right of the line: citing years\nafter the retraction year', fontsize=6.3, color=MUTED, va='top')
ax[1].set_xlabel('Years since retraction (citing year minus retraction year)'); ax[1].set_ylabel('Mean citing works per paper per year')
ax[1].set_ylim(0, 6.6); ax[1].legend(fontsize=6.5, loc='upper right'); ax[1].set_title('b  Citations before and after retraction', loc='left', fontsize=9)
save(fig, 'fig3_time_citations', FIG)
print('figures ok')
