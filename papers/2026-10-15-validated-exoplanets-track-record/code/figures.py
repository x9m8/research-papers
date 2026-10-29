"""Figures (300 dpi PNG + PDF). Run after analysis.py and sensitivity.py.
Palette as in the series' earlier papers (validated for colour-vision deficiency with the dataviz validator);
identity is also carried by direct labels or marker shape."""
import json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import poisson
from common import RES, FIG
BLUE, ORANGE, GREEN, YELLOW, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#0b0b0b', '#52514e', '#e4e3df'
LIGHT = '#c9c7c0'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': GRID,
                     'grid.linewidth': 0.6, 'legend.frameon': False, 'axes.axisbelow': True})
A = json.load(open(f'{RES}/analysis.json')); S = json.load(open(f'{RES}/sensitivity.json'))
P = pd.read_csv(f'{RES}/planets.csv'); R = pd.read_csv(f'{RES}/../code/overturn_reasons.csv')
def save(fig, n): fig.savefig(f'{FIG}/{n}.png', dpi=300, bbox_inches='tight'); fig.savefig(f'{FIG}/{n}.pdf', bbox_inches='tight'); plt.close(fig)

# Fig 1: catalogue composition by discovery year (transiting planets)
L = P[P.status == 'listed'].copy()
L['cls'] = np.select([L.mass_at_disc, L.later_mass], ['disc', 'later'], 'never')
t = L.groupby(['disc_year', 'cls']).size().unstack(fill_value=0).reindex(columns=['disc', 'later', 'never'], fill_value=0)
t = t[t.index >= 2005]
fig, ax = plt.subplots(figsize=(7.2, 3.0))
x = t.index.values; b = np.zeros(len(t))
for c, col, lab in [('disc', BLUE, 'Mass measured in discovery paper'), ('later', GREEN, 'Mass measured later'), ('never', LIGHT, 'Never weighed')]:
    ax.bar(x, t[c], bottom=b, color=col, width=0.8, edgecolor='white', linewidth=0.6, label=lab); b += t[c].values
ax.set_xlabel('Year of discovery'); ax.set_ylabel('Transiting planets discovered')
ax.legend(loc='upper left', fontsize=7.5); ax.grid(axis='x', visible=False)
yy = int(t.sum(axis=1).idxmax()); ax.annotate(f"{yy}: Morton et al.\nvalidate 1,284", (yy, t.sum(axis=1).max()), xytext=(yy + 1.6, t.sum(axis=1).max() * 0.9), fontsize=7.5, color=INK,
                                         arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
save(fig, 'fig1_composition')

# Fig 2: observed vs expected overturns by validation paper
C = A['C_calibration']
papers = ['Morton et al. 2016', 'Crossfield et al. 2016', 'Livingston et al. 2018a', 'Livingston et al. 2018b', 'Mayo et al. 2018', 'Montet et al. 2015']
lab = {'Morton et al. 2016': 'Morton+2016 (Kepler)', 'Crossfield et al. 2016': 'Crossfield+2016 (K2)', 'Livingston et al. 2018a': 'Livingston+2018a (K2)',
       'Livingston et al. 2018b': 'Livingston+2018b (K2)', 'Mayo et al. 2018': 'Mayo+2018 (K2)', 'Montet et al. 2015': 'Montet+2015 (K2)'}
fig, ax = plt.subplots(figsize=(6.2, 3.0))
y = np.arange(len(papers))[::-1]
for yi, p in zip(y, papers):
    e, o, n = C[p]['expected'], C[p]['observed'], C[p]['n']
    lo, hi = poisson.ppf(0.025, e), poisson.ppf(0.975, e)
    ax.plot([0.003, max(hi, 0.0045)], [yi, yi], color=MUTED, lw=4, alpha=0.35, solid_capstyle='round')
    ax.scatter(max(e, 0.003), yi, marker='|', s=160, color=INK, zorder=3)
    ax.scatter(max(o, 0.003), yi, marker='o', s=46, color=ORANGE if o > hi else BLUE, edgecolor='white', linewidth=1, zorder=4)
    ax.text(30, yi, f'{o} observed / {e:.2f} expected   (n = {n:,})' if e >= 0.1 else f'{o} observed / {e:.2g} expected   (n = {n:,})', va='center', fontsize=7.3, color=INK)
ax.set_yticks(y); ax.set_yticklabels([lab[p] for p in papers]); ax.set_xscale('log'); ax.set_xlim(0.003, 25); ax.grid(axis='y', visible=False)
ax.set_xlabel("Validated planets later overturned (log scale; 0 plotted at axis floor)")
fig.text(0.02, -0.06, 'Black tick: expected overturns from the paper\'s own FPPs. Grey band: central 95% Poisson range (upper end 0 drawn as a stub at the floor).\nCircle: observed (orange = above range). Livingston+2018b: FPP from their table 2 (VizieR column FPP2).',
        fontsize=6.8, color=MUTED, va='top')
save(fig, 'fig2_calibration')

# Fig 3: Morton+2016 by radius
mb = C['morton_by_radius']; bins = ['<2', '2-4', '4-6', '6-10', '>10']
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.8), gridspec_kw=dict(width_ratios=[1, 1]))
n = [mb[k]['n'] for k in bins]; f = [mb[k]['later_mass'] + mb[k]['observed'] for k in bins]
ax[0].bar(range(5), n, color=LIGHT, width=0.7, label='Validated')
ax[0].bar(range(5), f, color=BLUE, width=0.7, label='Later checked (weighed or overturned)')
for i, (a, b2) in enumerate(zip(n, f)): ax[0].text(i, a * 1.15, f'{b2}/{a}', ha='center', fontsize=7.3, color=INK)
ax[0].set_yscale('log'); ax[0].set_ylim(0.7, 2.5e4); ax[0].set_xticks(range(5)); ax[0].set_xticklabels(bins); ax[0].grid(axis='x', visible=False)
ax[0].set_xlabel('Planet radius (Earth radii)'); ax[0].set_ylabel('Planets (log scale)'); ax[0].legend(fontsize=7, loc='upper right', ncol=1)
ax[0].set_title('A  Few validated planets are ever checked', loc='left', fontsize=9, color=INK)
o = [mb[k]['observed'] for k in bins]; e = [mb[k]['expected'] for k in bins]
ax[1].bar(np.arange(5) - 0.18, e, width=0.36, color=MUTED, label='Expected (sum of FPPs)')
ax[1].bar(np.arange(5) + 0.18, o, width=0.36, color=ORANGE, label='Observed overturns')
for i, (a, b2) in enumerate(zip(e, o)):
    ax[1].text(i - 0.02 if b2 else i - 0.18, a + 0.25, f'{a:.2f}', ha='right' if b2 else 'center', fontsize=6.8, color=INK); ax[1].text(i + 0.18, b2 + 0.25, str(b2), ha='center', fontsize=7.3, color=INK)
ax[1].set_xticks(range(5)); ax[1].set_xticklabels(bins); ax[1].grid(axis='x', visible=False); ax[1].set_ylim(0, 11)
ax[1].set_xlabel('Planet radius (Earth radii)'); ax[1].set_ylabel('Planets overturned'); ax[1].legend(fontsize=7, loc='upper left')
ax[1].set_title('B  Overturns are all giant-sized', loc='left', fontsize=9, color=INK)
fig.tight_layout(); save(fig, 'fig3_morton_radius')

# Fig 4: follow-up over time (Kaplan-Meier cumulative incidence of a later mass measurement)
D = A['D_followup']
fig, ax = plt.subplots(figsize=(5.2, 3.2))
for m, col, mk in [('Kepler', BLUE, 'o'), ('K2', GREEN, 's'), ('TESS', ORANGE, '^')]:
    c = D[m]['km']; xs = [r['years'] for r in c]; ys = [100 * r['cum'] for r in c]
    ax.fill_between(xs, [100 * r['lo'] for r in c], [100 * r['hi'] for r in c], color=col, alpha=0.15, lw=0, step='post')
    ax.step(xs, ys, where='post', color=col, lw=1.8); ax.plot(xs, ys, ls='', marker=mk, ms=3.5, color=col)
    ax.text(xs[-1] + 0.3, ys[-1], m, color=INK, fontsize=8, va='center')
ax.set_xlabel('Years since announcement'); ax.set_ylabel('Weighed by then (%)'); ax.set_xlim(0, 13.8); ax.set_ylim(0, 60)
ax.text(0.3, 58, 'Planets announced without a mass. Kaplan-Meier estimate,\nunweighed planets censored at current age; bands 95%.\nCurves stop when fewer than 20 planets remain at risk.', fontsize=6.8, color=MUTED, va='top')
save(fig, 'fig4_followup')

# Fig 5: validation -> refutation timeline
vy = {'Morton': 2016, 'Crossfield': 2016, 'Livingston': 2018, 'Christiansen': 2022}
R['vy'] = R.validated_by.str.split().str[0].map(vy)
R = R.sort_values(['vy', 'refuting_year', 'pl_name']).reset_index(drop=True)
cm = {'mass above 30 MJup': ORANGE, 'stellar eclipse': BLUE, 'background or nearby eclipsing binary': GREEN}
fig, ax = plt.subplots(figsize=(6.4, 4.0))
for i, r in R.iterrows():
    ax.plot([r.vy, r.refuting_year], [i, i], color=MUTED, lw=1)
    ax.scatter(r.vy, i, marker='|', s=60, color=INK, zorder=3)
    ax.scatter(r.refuting_year, i, s=36, color=cm[r['class']], edgecolor='white', linewidth=0.8, zorder=4, marker='o' if r['class'] != 'background or nearby eclipsing binary' else 's')
ax.set_yticks(range(len(R))); ax.set_yticklabels(R.pl_name, fontsize=7); ax.invert_yaxis(); ax.grid(axis='y', visible=False)
ax.set_xlabel('Year'); ax.set_xlim(2010, 2025.5)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], marker='|', color=INK, ls='', ms=8, label='Validated'),
                   Line2D([], [], marker='o', color=ORANGE, ls='', label='Refuted: brown dwarf or low-mass star (> 30 MJup)'),
                   Line2D([], [], marker='o', color=BLUE, ls='', label='Refuted: stellar eclipse'),
                   Line2D([], [], marker='s', color=GREEN, ls='', label='Refuted: background or nearby eclipsing binary')], fontsize=7, loc='upper center', bbox_to_anchor=(0.45, -0.13), ncol=2)
save(fig, 'fig5_timeline')
print('figures written')
