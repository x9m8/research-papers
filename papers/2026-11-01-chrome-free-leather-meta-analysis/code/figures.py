"""Step 4: figures. fig1 forest plot (tensile), fig2 pooled ratios and tensile sensitivity, fig3 shrinkage temperature."""
import json
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, NullLocator
from style import BLUE, ORANGE, GREEN, INK, MUTED, GRID, LIGHT, save
from common import RES, FIG, EXT

R = json.load(open(f'{RES}/meta.json'))
E = pd.read_csv(f'{RES}/effects.csv')
sc = pd.read_csv(f'{EXT}/study_characteristics.csv').set_index('study_id')
CLS = ['vegetable', 'combination', 'aldehyde', 'synthetic', 'zeolite/silicate', 'non-chrome metal', 'other']
LAB = lambda s: f"{sc.loc[s, 'first_author']} {sc.loc[s, 'year']}" + {0: '', 1: ' †', 2: ' ‡'}[int(sc.loc[s, 'integrity_flag'])]

# ---------- Figure 1: forest plot, tensile strength
P = E[(E.outcome == 'tensile') & E.has_sd & (E.integrity_flag == 0)].copy()
P['cls_rank'] = P.cf_class.map({c: i for i, c in enumerate(CLS)})
P['lo'] = np.exp(P.yi - 1.96 * np.sqrt(P.vi)); P['hi'] = np.exp(P.yi + 1.96 * np.sqrt(P.vi)); P['rr'] = np.exp(P.yi)
P = P.sort_values(['cls_rank', 'study_id', 'yi'])
fig, ax = plt.subplots(figsize=(6.6, 8.2))
ypos, ylabels, y = [], [], 0
prev = None
for _, r in P.iterrows():
    if r.cf_class != prev:
        y += 0.6; ax.text(0.155, -y, r.cf_class.capitalize(), fontsize=8, weight='bold', color=INK, va='center', ha='left'); y += 1; prev = r.cf_class
    ax.plot([max(r.lo, 0.16), min(r.hi, 3.0)], [-y, -y], color=MUTED, lw=1)
    hollow = sc.loc[r.study_id, 'comparator_source'] != 'in-study'
    ax.plot(r.rr, -y, 's', ms=5, mfc='white' if hollow else BLUE, mec=BLUE, mew=1.2)
    ypos.append(-y); ylabels.append(f"{LAB(r.study_id)} · {r.arm_id}"); y += 1
m = R['models']['tensile']; y += 1.0
ax.fill([m['lo'], m['est'], m['hi'], m['est']], [-y, -y + 0.45, -y, -y - 0.45], color=INK)
ax.plot([m['pi_lo'], m['pi_hi']], [-y, -y], color=INK, lw=1, ls=(0, (2, 2)))
ypos.append(-y); ylabels.append(f"Pooled {m['est']:.2f} ({m['lo']:.2f}–{m['hi']:.2f})")
ax.axvline(1, color=INK, lw=0.8)
ax.set_xscale('log'); ax.xaxis.set_minor_locator(NullLocator()); ax.xaxis.set_minor_formatter(NullFormatter()); ax.set_xlim(0.15, 3.0)
ax.set_xticks([0.2, 0.33, 0.5, 0.67, 1, 1.5, 2]); ax.set_xticklabels(['0.2', '0.33', '0.5', '0.67', '1', '1.5', '2'])
ax.set_yticks(ypos); ax.set_yticklabels(ylabels, fontsize=7); ax.set_ylim(-y - 1, 0)
ax.grid(axis='y', visible=False)
ax.set_xlabel('Ratio of means, chrome-free / chrome (log scale)\n← chrome-free weaker      chrome-free stronger →')
ax.set_title('Tensile strength: within-study contrasts (filled: chrome control tanned in-study;\nopen: commercial or external chrome comparator). Bars: 95% CI (n=3 assumed where not stated).\nDiamond: pooled ratio and 95% CI; dashed line: 95% prediction interval', fontsize=8, loc='left', color=INK)
save(fig, 'fig1_forest_tensile', FIG)

# ---------- Figure 2: pooled estimates by outcome + tensile sensitivity
fig, axs = plt.subplots(1, 2, figsize=(7.2, 4.4), gridspec_kw=dict(width_ratios=[1, 1.25]))
ax = axs[0]
outs = [('tensile', 'Tensile strength\n(primary)'), ('elongation', 'Elongation at break\n(exploratory)'), ('tear', 'Tear load\n(exploratory)')]
for i, (o, l) in enumerate(outs):
    m = R['models'][o]
    ax.plot([m['pi_lo'], m['pi_hi']], [-i, -i], color=LIGHT, lw=6, solid_capstyle='butt')
    ax.plot([m['lo'], m['hi']], [-i, -i], color=BLUE, lw=2)
    ax.plot(m['est'], -i, 'o', color=BLUE, ms=7, mec='white', mew=1.5)
    ax.text(m['est'], -i + 0.28, f"{m['est']:.2f}  ({m['k_studies']} studies)", ha='center', fontsize=7.5, color=INK)
ax.axvline(1, color=INK, lw=0.8); ax.set_xscale('log'); ax.xaxis.set_minor_locator(NullLocator()); ax.xaxis.set_minor_formatter(NullFormatter()); ax.set_xlim(0.3, 2.3)
ax.set_xticks([0.33, 0.5, 0.67, 1, 1.5, 2]); ax.set_xticklabels(['0.33', '0.5', '0.67', '1', '1.5', '2'])
ax.set_yticks([-i for i in range(3)]); ax.set_yticklabels([l for _, l in outs], fontsize=7.5); ax.set_ylim(-2.6, 0.6); ax.grid(axis='y', visible=False)
ax.set_xlabel('Pooled ratio, chrome-free / chrome'); ax.set_title('a  Pooled ratios: 95% CI (blue),\n    95% prediction interval (grey)', fontsize=8, loc='left')
ax = axs[1]
S = R['sensitivity']['tensile']; base = R['models']['tensile']
items = [('Primary analysis', base), ('Missing n set to 2', S['n_missing_2']), ('Missing n set to 5', S['n_missing_5']),
         ('Imputed SDs added', S['impute_sd']), ('Without SD = 0 study', S['without_jia2022']),
         ('Without Gómez-García 2026', S['without_gomezgarcia2026']), ('Without Aguilar 2023', S['without_aguilar2023']),
         ('Without both', S['without_both_outliers']),
         ('In-study chrome control only', S['in_study_comparator_only']), ('Non-developer studies only', S['non_developer_only']),
         ('n stated for every arm', S['n_stated_only'])]
for i, (l, m) in enumerate(items):
    c = INK if i == 0 else BLUE
    ax.plot([m['lo'], m['hi']], [-i, -i], color=c, lw=1.6)
    ax.plot(m['est'], -i, 'o', color=c, ms=5.5, mec='white', mew=1)
    ax.text(2.2, -i, f"{m['est']:.2f} · {m['k_studies']}", va='center', ha='right', fontsize=7, color=MUTED)
ax.axvline(1, color=INK, lw=0.8); ax.set_xscale('log'); ax.xaxis.set_minor_locator(NullLocator()); ax.xaxis.set_minor_formatter(NullFormatter()); ax.set_xlim(0.45, 2.3)
ax.set_xticks([0.5, 0.67, 1, 1.5]); ax.set_xticklabels(['0.5', '0.67', '1', '1.5'])
ax.set_yticks([-i for i in range(len(items))]); ax.set_yticklabels([l for l, _ in items], fontsize=7.5); ax.grid(axis='y', visible=False)
ax.set_xlabel('Pooled tensile ratio (95% CI)'); ax.set_title('b  Tensile strength: sensitivity analyses\n    (estimate · number of studies)', fontsize=8, loc='left')
fig.tight_layout(); save(fig, 'fig2_pooled_sensitivity', FIG)

# ---------- Figure 3: shrinkage temperature, chrome-free arm vs chrome control
T = pd.read_csv(f'{RES}/ts_descriptive.csv')
T['lab'] = [f"{LAB(s)} · {a}" for s, a in zip(T.study_id, T.arm_id)]
T = T.sort_values(['study_id', 'mean_cf'])
fig, ax = plt.subplots(figsize=(6.6, 6.2))
ax.axvspan(100, 112, color=GRID, alpha=0.6, lw=0); ax.text(100.5, 0.6, 'above ISO 3380\nrange (>100 °C)', fontsize=6.5, color=MUTED, va='bottom')
for i, (_, r) in enumerate(T.iterrows()):
    yy = -i
    ax.plot([r.mean_cf, r.mean_cr], [yy, yy], color=LIGHT, lw=1.5, zorder=1)
    flag = r.integrity_flag == 1
    ax.plot(r.mean_cf, yy, 'o', ms=6, color=GREEN, mfc='white' if flag else GREEN, mec=GREEN, zorder=3)
    if r.ts_cens_cr == 2:
        ax.annotate('', xy=(r.mean_cr + 2.5, yy), xytext=(r.mean_cr, yy), arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2))
    ax.plot(r.mean_cr, yy, 'D', ms=5, color=ORANGE, mfc='white' if flag else ORANGE, mec=ORANGE, zorder=3)
ax.set_yticks([-i for i in range(len(T))]); ax.set_yticklabels(T.lab, fontsize=6.8); ax.grid(axis='y', visible=False)
ax.set_xlim(55, 112); ax.set_ylim(-len(T) + 0.3, 1.6)
ax.set_xlabel('Shrinkage temperature (°C)')
ax.plot([], [], 'o', color=GREEN, label='Chrome-free arm'); ax.plot([], [], 'D', color=ORANGE, label='Chrome control')
ax.plot([], [], 'o', mfc='white', mec=MUTED, color=MUTED, label='Open: study with integrity flag')
ax.annotate('', xy=(0, 0), xytext=(0, 0)); ax.plot([], [], color=ORANGE, marker=r'$\rightarrow$', ls='', ms=10, label='Arrow: reported as ">95 °C"')
ax.legend(loc='lower left', fontsize=7, frameon=True, facecolor='white', edgecolor=GRID)
ax.set_title(f"Shrinkage temperature: every chrome-free arm below its chrome control\n({R['ts']['n_arms']} arms in {R['ts']['n_studies']} studies, plus {len(R['ts']['flagged_study_md'])} arms from a flagged study; median difference {R['ts']['md_median_arm']:.0f} °C)", fontsize=8, loc='left')
save(fig, 'fig3_shrinkage', FIG)
print('figures ok')
