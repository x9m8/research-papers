"""Figures 1-3 (PNG 300 dpi + PDF)."""
import json, numpy as np, pandas as pd
from style import *
from common import RES, FIG, DER, TARGET, load
R = load('reproduction.json'); B = load('robustness.json'); U = load('update.json')
LAB = {'e1': 'Expanded #1\n(supercenters\nunhealthy)', 'e2': 'Expanded #2\n(supercenters\nhealthy)', 'trad': 'Traditional'}
Z = 1.959964

# ---------- Figure 1: published vs reproduced
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw=dict(wspace=0.32))
keys = ['trad', 'e1', 'e2']; y = np.arange(len(keys))[::-1]
a = axs[0]
series = [('Published (Table 6)', [TARGET['ols'][k][0] for k in keys], [TARGET['ols'][k][1] for k in keys], INK, 'o', 0.22),
          ('Reproduced, 2007 counts', [R['main'][k]['ols_b'] for k in keys], [R['main'][k]['ols_se_cl'] for k in keys], BLUE, 's', 0.0),
          ('Reproduced, 2009 counts', [R['counts2009'][k]['ols_b'] for k in keys], [R['counts2009'][k]['ols_se_cl'] for k in keys], ORANGE, '^', -0.22)]
for lab, b, s, c, m, off in series:
    a.errorbar(b, y + off, xerr=Z * np.array(s), fmt=m, color=c, ms=5, lw=1.2, capsize=0, label=lab)
a.axvline(0, color=MUTED, lw=0.8); a.set_yticks(y); a.set_yticklabels([LAB[k] for k in keys], fontsize=7.5)
a.set_xlabel('OLS coefficient on RFEI\n(points of obesity per unit of ratio)'); a.grid(axis='y', visible=False)
a.set_title('A  OLS', loc='left', fontsize=9, color=INK)
a.legend(fontsize=6.6, loc='lower center', bbox_to_anchor=(0.5, -0.5))
b_ = axs[1]
series = [('Published (Table 8), ESRI exits', [TARGET['iv'][k][0] for k in keys], [TARGET['iv'][k][1] for k in keys], INK, 'o', 0.15),
          ('Reproduced, OSM motorway junctions', [R['main'][k]['iv_b'] for k in keys], [R['main'][k]['iv_se_cl'] for k in keys], BLUE, 's', -0.15)]
for lab, bb, s, c, m, off in series:
    b_.errorbar(bb, y + off, xerr=Z * np.array(s), fmt=m, color=c, ms=5, lw=1.2, capsize=0, label=lab)
for k, yy in zip(keys, y):   # Anderson-Rubin set for the reproduction
    ar = R['main'][k]['ar_cl']
    if ar['lo'] is not None: b_.plot([ar['lo'], ar['hi']], [yy - 0.3] * 2, color=BLUE, lw=3, alpha=0.35, solid_capstyle='butt')
b_.plot([], [], color=BLUE, lw=3, alpha=0.35, label='Reproduced, Anderson–Rubin 95% set')
b_.axvline(0, color=MUTED, lw=0.8); b_.set_yticks(y); b_.set_yticklabels([]); b_.grid(axis='y', visible=False)
b_.set_xlabel('2SLS coefficient on RFEI\n(points of obesity per unit of ratio)'); b_.set_title('B  Instrumental variables', loc='left', fontsize=9, color=INK)
b_.legend(fontsize=6.6, loc='lower center', bbox_to_anchor=(0.5, -0.5))
save(fig, 'fig1_reproduction', FIG)

# ---------- Figure 2: the instrument is mostly county size
d = pd.read_csv(f'{DER}/county_base.csv'); S = d[d.natamen.notna() & d.obese.notna() & d.rfei_trad.notna()]
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw=dict(wspace=0.32, width_ratios=[1, 1.5]))
a = axs[0]
a.scatter(np.log10(S.pop10), np.log10(1 + S.exits_osm), s=3, color=BLUE, alpha=0.35, lw=0)
a.set_xlabel('County population, 2010 (log10)'); a.set_ylabel('OSM motorway junctions + 1 (log10)')
r = R['corr']['exits_pop10']
a.text(0.03, 0.95, f'r = {r:.2f} (raw counts)', transform=a.transAxes, fontsize=7.5, color=INK, va='top')
a.set_title('A  Exits track population', loc='left', fontsize=9, color=INK)
b_ = axs[1]
G = pd.DataFrame(B['grid']); G = G[G.group == 'trad'].set_index('label')
rows = ['Baseline (2007 counts, matched controls, clustered SE)', 'State fixed effects', 'Add people over 65 (count, as in the table notes)',
        'Add population (linear)', 'Add population (linear) + state fixed effects', 'Add log population', 'Add log and linear population', 'Add log population + state fixed effects']
names = ['Baseline\n(matched\ncontrols)', 'State\nFE', '+ people\nover 65\n(count)', '+ pop.\n(linear)', '+ pop.\n(linear)\n+ state FE', '+ log\npop.', '+ log and\nlinear\npop.', '+ log\npop.\n+ state FE']
F = [G.loc[x, 'fs_F'] for x in rows]
b_.bar(range(len(rows)), F, color=[BLUE] * 5 + [ORANGE] * 3, width=0.62)
b_.axhline(10, color=MUTED, lw=0.8, ls='--'); b_.text(len(rows) - 0.55, 10.8, 'F = 10', fontsize=7, color=MUTED, ha='right')
b_.set_yscale('log'); b_.set_ylim(0.01, 200); b_.set_xticks(range(len(rows))); b_.set_xticklabels(names, fontsize=6)
b_.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f'{v:g}'))
for i, f in enumerate(F): b_.text(i, f * 1.25, f'{f:.2g}' if f < 1 else f'{f:.0f}' if f >= 10 else f'{f:.1f}', ha='center', fontsize=6.5, color=INK)
b_.set_ylabel('First-stage F (state-clustered)'); b_.grid(axis='x', visible=False)
b_.set_title('B  Instrument strength, traditional RFEI', loc='left', fontsize=9, color=INK)
save(fig, 'fig2_instrument', FIG)

# ---------- Figure 3: specification curve, traditional RFEI, IV with AR sets, plus update and long difference
G = pd.DataFrame(B['grid']); G = G[G.group == 'trad'].copy()
G['lab'] = G.label; G = G[~G.label.str.startswith('Log of')]   # log units are not comparable with the ratio scale
upd = U['cross_section_2016']
extra = [('Update: 2016 counts, BRFSS 2018 (PLACES)', upd['trad|all']), ('Update + state fixed effects', upd['trad|state FE'])]
rows = [(r.lab, r.iv_b, r.iv_se, r.ar_lo, r.ar_hi, r.ar_type) for r in G.itertuples()]
rows += [(l, v['iv_b'], v['iv_se'], v['ar']['lo'], v['ar']['hi'], v['ar']['type']) for l, v in extra]
rows = sorted(rows, key=lambda t: t[1])
fig, ax = plt.subplots(figsize=(7.2, 5.4))
for i, (l, b, s, lo, hi, typ) in enumerate(rows):
    c = ORANGE if l.startswith('Update') else BLUE
    if lo is not None and not (isinstance(lo, float) and np.isnan(lo)):
        ax.plot([lo, min(hi, 8.5)], [i, i], color=c, lw=2.4, alpha=0.35, solid_capstyle='butt')
        if hi > 8.5: ax.text(8.45, i + 0.32, f'AR upper bound {hi:.1f} →', fontsize=6, color=MUTED, ha='right', va='center')
    else:
        ax.plot([-1, 6], [i, i], color=c, lw=2.4, alpha=0.15, ls=(0, (2, 1)))
        ax.text(6.05, i, 'AR set unbounded', fontsize=6.3, color=MUTED, va='center')
    if b > 8.3:
        ax.annotate(f'{b:.1f} →', (8.35, i), fontsize=6.5, color=c, va='center', ha='right')
    else:
        ax.plot(b, i, 'o' if not l.startswith('Update') else 'D', color=c, ms=4.5)
ax.axvline(TARGET['iv']['trad'][0], color=INK, lw=0.9, ls='--'); ax.text(TARGET['iv']['trad'][0] + 0.05, len(rows) - 0.3, 'Published IV, 2.604', fontsize=7, color=INK)
ld = U['long_difference']['trad|state FE']
ax.axvline(0, color=MUTED, lw=0.8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=6.6)
ax.set_xlim(-1, 8.5); ax.set_xlabel('2SLS coefficient on the traditional RFEI (points of obesity per unit of ratio)')
ax.grid(axis='y', visible=False)
ax.text(8.45, -0.9, f"Long difference, counts 2007→2016, obesity 2009→2018 (OLS, state FE): {ld['b']:.3f} (SE {ld['se']:.3f})", fontsize=7, color=INK, ha='right', bbox=dict(facecolor='white', edgecolor='none', pad=1.5))
ax.set_ylim(-1.4, len(rows) - 0.2)
save(fig, 'fig3_speccurve', FIG); print('ok')
