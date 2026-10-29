"""Figures 1-3 from the result files (results/*.json)."""
import json
import numpy as np
from style import *
from common import RES, FIG

B = json.load(open(f'{RES}/build.json')); D = json.load(open(f'{RES}/descriptives.json'))
ES = json.load(open(f'{RES}/event_study.json')); EST = json.load(open(f'{RES}/estimates.json'))
PURPLE = '#8a63d2'

# ---- Figure 1: national uptake and the county distribution of the change ----
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw={'width_ratios': [1.1, 1]})
yrs = sorted(B['coverage'], key=int); x = [int(y) for y in yrs]
gen = lambda y, g: B['coverage'][y]['fills_by_generic_national'].get(g, 0) / 1e6
series = [('Semaglutide', BLUE), ('Tirzepatide', ORANGE), ('Dulaglutide', GREEN)]
other = [sum(v for g, v in B['coverage'][y]['fills_by_generic_national'].items() if g not in ('Semaglutide', 'Tirzepatide', 'Dulaglutide')) / 1e6 for y in yrs]
ends = {}
for g, c in series:
    v = [gen(y, g) for y in yrs]; a1.plot(x, v, color=c, lw=1.8, marker='o', ms=3); ends[g] = v[-1]
if abs(ends['Tirzepatide'] - ends['Dulaglutide']) < 1.0:   # keep the two end labels apart
    hi_, lo_ = sorted(['Tirzepatide', 'Dulaglutide'], key=ends.get, reverse=True)
    ends[hi_] += 0.5; ends[lo_] -= 0.5
for g, c in series:
    a1.text(x[-1] + 0.15, ends[g], g, color=c, fontsize=7, va='center')
a1.plot(x, other, color=MUTED, lw=1.4, marker='o', ms=3); a1.text(x[-1] + 0.15, other[-1], 'Other GLP-1', color=MUTED, fontsize=7, va='center')
a1.set_xlim(2018.7, 2025.9); a1.set_xticks(x); a1.set_ylabel('30-day fills, millions'); a1.set_title('a  Medicare Part D GLP-1 fills, United States', fontsize=8.5, loc='left')
e = D['hist']['edges']; c = D['hist']['counts']
a2.bar(e[:-1], c, width=np.diff(e), align='edge', color=BLUE, alpha=0.85, lw=0)
a2.axvline(D['dE_median'], color=INK, lw=0.8, ls='--'); a2.text(D['dE_median'], max(c) * 1.02, f"median {D['dE_median']:.1f}", fontsize=7, ha='center')
a2.set_xlabel('Change in GLP-1 users per 100 Part D enrollees,\n2019 to 2024 (full-year equivalents)'); a2.set_ylabel('Counties')
a2.set_title('b  County change in uptake', fontsize=8.5, loc='left'); a2.grid(axis='x', visible=False)
fig.tight_layout(); save(fig, 'fig1_exposure', FIG)

# ---- Figure 2: event studies ----
panels = [('lsr', 'Limited-service restaurants', ORANGE), ('fsr', 'Full-service restaurants', BLUE), ('diff', 'Limited minus full service', INK),
          ('pharm', 'Pharmacies (positive control)', GREEN), ('acc', 'Accommodation (placebo)', MUTED), ('groc', 'Grocery stores', PURPLE)]
fig, axs = plt.subplots(2, 3, figsize=(7.0, 4.4), sharex=True)
lim = max(max(abs(v.get('lo_pp', 0)), abs(v.get('hi_pp', 0))) for k, _, _ in panels for v in ES[k]['coef'].values())
for ax, (k, t, col) in zip(axs.flat, panels):
    co = ES[k]['coef']; yy = sorted(co, key=int); xv = [int(y) for y in yy]
    b = [co[y]['b_pp'] for y in yy]; lo = [co[y]['lo_pp'] for y in yy]; hi = [co[y]['hi_pp'] for y in yy]
    ax.axhline(0, color=INK, lw=0.6); ax.axvline(2019, color=LIGHT, lw=0.8, ls=':')
    ax.fill_between(xv, lo, hi, color=col, alpha=0.18, lw=0); ax.plot(xv, b, color=col, lw=1.6, marker='o', ms=2.5)
    ax.set_title(t, fontsize=8, loc='left'); ax.set_ylim(-lim * 1.05, lim * 1.05)
    ax.text(0.02, 0.04, f"n = {ES[k]['n']:,}; pre-2019 F-test p = {ES[k]['pretrend_p']:.2f}", transform=ax.transAxes, fontsize=6.3, color=MUTED)
for ax in axs[1]: ax.set_xticks([2015, 2017, 2019, 2021, 2023, 2025]); ax.tick_params(axis='x', labelsize=7)
for ax in axs[:, 0]: ax.set_ylabel('% change in employment\nper 1-point rise in uptake', fontsize=7.5)
fig.tight_layout(); save(fig, 'fig2_event_study', FIG)

# ---- Figure 3: long differences against the household benchmark ----
E = EST['estimates']; bm = EST['benchmark_pct_per_pp']
rows = [('lsr_emp', 'Limited-service: employment'), ('lsr_est', 'Limited-service: establishments'), ('lsr_wag', 'Limited-service: wages'),
        ('fsr_emp', 'Full-service: employment'), ('fsr_est', 'Full-service: establishments'), ('fsr_wag', 'Full-service: wages'),
        ('diff_emp', 'Limited minus full: employment'), ('diff_est', 'Limited minus full: establishments'), ('diff_wag', 'Limited minus full: wages'),
        ('pharm_emp', 'Pharmacies: employment'), ('acc_emp', 'Accommodation: employment'), ('groc_emp', 'Grocery: employment')]
cols = [ORANGE] * 3 + [BLUE] * 3 + [INK] * 3 + [GREEN, MUTED, PURPLE]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.9), gridspec_kw={'width_ratios': [1.35, 1]})
yv = np.arange(len(rows))[::-1]
a1.axvspan(min(bm.values()), max(bm.values()), color=YELLOW, alpha=0.25, lw=0)
a1.axvline(0, color=INK, lw=0.6)
for y, (k, lab), c in zip(yv, rows, cols):
    m = E[k]['main']; a1.plot([m['lo_pp'], m['hi_pp']], [y, y], color=c, lw=1.4); a1.plot(m['b_pp'], y, 'o', color=c, ms=4)
a1.set_yticks(yv); a1.set_yticklabels([r[1] for r in rows], fontsize=7); a1.grid(axis='y', visible=False)
a1.set_xlabel('% change, 2019–2025, per 1-point rise in uptake'); a1.set_title('a  Long-difference estimates (95% CI)', fontsize=8.5, loc='left')
a1.set_ylim(-0.7, len(rows) + 0.2)
a1.text(0.1, len(rows) - 0.25, '← household-panel benchmark (shaded)', fontsize=6.3, color=MUTED, ha='left', va='center')
bs = D['binscatter_diff']
a2.axhline(0, color=INK, lw=0.6); a2.plot(bs['x'], bs['y_pct'], 'o', color=INK, ms=3.5)
bb = E['diff_emp']['main']['b_pp']; xx = np.array([min(bs['x']), max(bs['x'])]); a2.plot(xx, bb * xx, color=ORANGE, lw=1.2)
a2.set_xlabel('Change in uptake (residualised), points'); a2.set_ylabel('Δ log LSR − Δ log FSR employment, %\n(residualised)', fontsize=7.5)
a2.set_title('b  Binned scatter, 20 bins', fontsize=8.5, loc='left')
fig.tight_layout(); save(fig, 'fig3_long_differences', FIG)
print('ok')
