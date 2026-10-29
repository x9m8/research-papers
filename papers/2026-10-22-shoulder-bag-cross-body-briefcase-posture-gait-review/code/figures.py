import json, numpy as np, pandas as pd
from style import *
from common import RES, FIG
import matplotlib.patches as mp
# Fig 1 flow
fig, ax = plt.subplots(figsize=(6.6, 5.2)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
def box(x, y, w, h, t, c='white'):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.12', fc=c, ec=MUTED, lw=0.9)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=7.6, color=INK, wrap=True)
def arr(x1, y1, x2, y2): ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9))
box(0.2, 8.6, 4.4, 1.1, 'Europe PMC, 12 queries\n936 hits, 789 unique records'); box(5.4, 8.6, 4.4, 1.1, 'Other sources (web, proceedings,\ntheses, registries): 9 records')
arr(2.4, 8.6, 3.6, 7.7); arr(7.6, 8.6, 6.4, 7.7)
box(2.3, 6.6, 5.4, 1.1, 'Records screened on title and abstract\nn = 798'); box(8.0, 6.6, 1.9, 1.1, 'Excluded\nn = 733', '#f4f3f0')
arr(7.7, 7.15, 8.0, 7.15); arr(5.0, 6.6, 5.0, 5.7)
box(2.3, 4.6, 5.4, 1.1, 'Reports assessed in detail\nn = 65'); arr(5.0, 4.6, 3.3, 3.7); arr(5.0, 4.6, 6.7, 3.7)
box(0.2, 2.5, 4.5, 1.2, 'Assessed for eligibility\nn = 24 (18 in full text)', BLUE + '22'); box(5.3, 2.5, 4.5, 1.2, 'Full text not obtained: n = 41\n(40 charted in the evidence map;\n1 duplicate)', YELLOW + '33')
arr(2.45, 2.5, 1.5, 1.6); arr(2.45, 2.5, 3.6, 1.6)
box(0.15, 0.3, 2.6, 1.3, 'Included\nn = 13\n(8 adult with SDs,\n2 adolescent)', BLUE + '44'); box(2.9, 0.3, 2.3, 1.3, 'Excluded\nn = 11', '#f4f3f0')
save(fig, 'fig1_flow', FIG)

# Fig 2 evidence map
L = pd.read_csv(f'{RES}/map_long.csv')
bags = ['shoulder same-side', 'cross-body', 'hand-carried', 'non-bag load']; bl = ['One-shoulder bag', 'Cross-body bag', 'Hand-carried bag', 'Other or unspecified\nside load']
outs = ['gait', 'posture', 'kinematics', 'kinetics', 'EMG', 'balance', 'physiological', 'coordination', 'pressure', 'comfort', 'pain']
ol = ['Gait', 'Posture', 'Joint/pelvis\nangles', 'Forces', 'Muscle\nactivity', 'Balance', 'Effort,\nheart rate', 'Coordi-\nnation', 'Strap\npressure', 'Comfort', 'Pain']
fig, ax = plt.subplots(figsize=(7.2, 3.0))
for i, b in enumerate(bags):
    for j, o in enumerate(outs):
        x = L[(L.bag == b) & (L.outcome == o)]; ft = x[x.evidence == 'Full text, included'].id.nunique(); tot = x.id.nunique()
        if tot: ax.scatter(j, i, s=60 + 70 * tot, color=YELLOW, alpha=0.35, lw=0)
        if ft: ax.scatter(j, i, s=60 + 70 * ft, color=BLUE, alpha=0.9, lw=0)
        ax.text(j, i, str(tot) if tot else '0', ha='center', va='center', fontsize=7, color=INK if tot else '#b8b6af')
ax.set_xticks(range(len(outs))); ax.set_xticklabels(ol, fontsize=6.8); ax.set_yticks(range(len(bags))); ax.set_yticklabels(bl)
ax.set_xlim(-0.6, len(outs) - 0.4); ax.set_ylim(len(bags) - 0.4, -0.6); ax.grid(False); ax.spines[['left', 'bottom']].set_visible(False); ax.tick_params(length=0)
ax.scatter([], [], s=90, color=BLUE, label='Included, full text'); ax.scatter([], [], s=90, color=YELLOW, alpha=0.5, label='All records assessed (number shown)')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=2, fontsize=7)
save(fig, 'fig2_evidence_map', FIG)

# Fig 3 effects vs no load (adults)
E = pd.read_csv(f'{RES}/effects_all.csv'); A = E[E.adult & E.vs_noload & E.g.notna()].copy()
lab = lambda s: s.split(';')[0].replace(' (frontal plane)', '').replace('Trapezius', 'Upper trapezius') if 'Upper' not in s else s.split(';')[0]
bagc = lambda b: ORANGE if 'cross' in b.lower() else (GREEN if 'hand' in b.lower() or 'barbell' in b.lower() else BLUE)
doms = ['Muscle activity', 'Posture and pelvis', 'Gait']
fig, axs = plt.subplots(1, 3, figsize=(7.4, 3.9), sharey=False, gridspec_kw=dict(wspace=0.08))
for a, d in zip(axs, doms):
    x = A[A.domain == d].sort_values('g'); y = np.arange(len(x))
    a.hlines(y, x['lo_0.5'], x['hi_0.5'], color=GRID, lw=1.2)
    a.scatter(x.g, y, s=[22 if bs else 10 for bs in x.bag_side], c=[bagc(b) for b in x.bag_type], zorder=3, edgecolors=[INK if bs else 'none' for bs in x.bag_side], linewidths=0.6)
    a.axvline(0, color=MUTED, lw=0.8); a.set_yticks([]); a.set_title(f'{d}\n({x.study_id.nunique()} studies, {len(x)} outcomes)', fontsize=8, color=INK, loc='left')
    a.set_xlim(-3.2, 3.2)
    for xx, yy in zip(x.g, y):
        if xx > 3.2: a.annotate(f'g = {xx:.1f} →', (3.15, yy + 0.9), ha='right', va='bottom', fontsize=6, color=MUTED)
    a.grid(axis='y', visible=False)
from matplotlib.lines import Line2D
axs[0].legend(handles=[Line2D([], [], marker='o', ls='', color=BLUE, label='One-shoulder bag'), Line2D([], [], marker='o', ls='', color=ORANGE, label='Cross-body bag'),
                       Line2D([], [], marker='o', ls='', color=GREEN, label='Hand-carried / side load'), Line2D([], [], marker='o', ls='', mfc='white', mec=INK, label='Strap- or load-side measure')],
              fontsize=6.8, loc='upper center', bbox_to_anchor=(0.5, 0.02), ncol=4, bbox_transform=fig.transFigure)
fig.text(0.5, 0.07, 'Standardised difference from walking or standing without the load (Hedges g; bars: approximate 95% CI, r = 0.5)', ha='center', fontsize=7.5, color=INK)
fig.subplots_adjust(bottom=0.2)
save(fig, 'fig3_effects', FIG); print('ok')
