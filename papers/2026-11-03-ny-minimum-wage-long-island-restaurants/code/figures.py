"""Figures 1-3 (300 dpi PNG + PDF) from data/raw/minwage_schedule.csv and the result files."""
import json, os
import numpy as np
from style import plt, save, BLUE, ORANGE, GREEN, YELLOW, INK, MUTED, GRID, LIGHT
from common import RES, FIG, schedule

os.makedirs(FIG, exist_ok=True)
S = schedule(); ES = json.load(open(f'{RES}/event_study.json')); E = json.load(open(f'{RES}/estimates.json'))['estimates']
SC = json.load(open(f'{RES}/scm.json')); SM = json.load(open(f'{RES}/summary.json'))
t = S.year + (S.qtr - 1) / 4.0
NAMES = {'722': 'All food services and drinking places (722)', '722511': 'Full-service restaurants (722511)', '722513': 'Limited-service restaurants (722513)'}


def covid(ax):
    ax.axvspan(2020, 2022, color=GRID, alpha=0.6, lw=0, zorder=0)


# ---------- Figure 1: the schedules and the Long Island minus rest-of-state gap ----------
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6), gridspec_kw={'width_ratios': [1.35, 1]})
ax = axes[0]
ax.step(t, S.mw_li, where='post', color=BLUE, lw=2, label='General, Long Island & Westchester')
ax.step(t, S.mw_ros, where='post', color=ORANGE, lw=2, label='General, rest of state')
ax.step(t, S.ff_outside_nyc, where='post', color=GREEN, lw=1.6, ls='--', label='Fast-food chains, outside NYC')
ax.step(t, S.tip_li, where='post', color=BLUE, lw=1.4, ls=':', label='Tipped food-service cash wage, LI')
ax.step(t, S.tip_ros, where='post', color=ORANGE, lw=1.4, ls=':', label='Tipped food-service cash wage, rest of state')
ax.step(t, S.mw_pa, where='post', color=MUTED, lw=1.4, label='Pennsylvania (federal $7.25)')
ax.set_ylabel('Dollars per hour'); ax.set_xlim(2014, 2026.25); ax.set_ylim(0, 18.5)
ax.set_title('(a) Hourly minimum rates', loc='left', fontsize=9, color=INK)
ax.legend(fontsize=6.6, loc='lower right', ncol=1)
ax = axes[1]
ax.step(t, S.mw_li - S.mw_ros, where='post', color=BLUE, lw=2, label='General minimum')
ax.step(t, (S.tip_li - S.tip_ros).fillna(0), where='post', color=ORANGE, lw=1.6, ls=':', label='Tipped cash wage')
ax.step(t, S.ff_li - S.ff_ros, where='post', color=GREEN, lw=1.6, ls='--', label='Fast-food chains (effective)')
covid(ax)
ax.set_ylabel('Long Island minus rest of state ($/hour)'); ax.set_xlim(2014, 2026.25); ax.set_ylim(-0.05, 2.0)
ax.set_title('(b) Regional gap', loc='left', fontsize=9, color=INK)
ax.legend(fontsize=6.8, loc='upper left')
fig.tight_layout(); save(fig, 'fig1_schedule', FIG)

# ---------- Figure 2: gap paths with placebo bands ----------
gmw = np.array(ES['gap_general'])
fig, axes = plt.subplots(2, 3, figsize=(10, 5.6), sharex=True)
for j, ind in enumerate(['722', '722511', '722513']):
    for i, (o, lab) in enumerate([('emp', 'Employment'), ('wage', 'Average weekly wage')]):
        ax = axes[i, j]; s = ES['series'][ind][o]
        g, lo, hi = (np.array(s[k], float) for k in ('gap', 'q025', 'q975'))
        covid(ax)
        ax.fill_between(t, lo, hi, color=LIGHT, alpha=0.6, lw=0, label='Placebo 95% range (random halves of rest of state)')
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.step(t, gmw, where='post', color=ORANGE, lw=1.3, ls='--', label='Log minimum-wage gap (LI minus rest of state)')
        ax.plot(t, g, color=BLUE, lw=1.8, marker='o', ms=2.5, label='Long Island minus rest of state')
        ax.axvline(2017, color=MUTED, lw=0.7, ls=':')
        ax.set_ylim(-0.22, 0.27) if o == 'emp' else ax.set_ylim(-0.22, 0.27)
        if i == 0:
            ax.set_title(NAMES[ind], fontsize=8.5, color=INK, loc='left')
        if j == 0:
            ax.set_ylabel(f'{lab}\nlog difference vs 2014–2016')
        if i == 1:
            ax.set_xticks([2014, 2016, 2018, 2020, 2022, 2024, 2026])
h, l = axes[0, 0].get_legend_handles_labels()
fig.legend(h, l, loc='lower center', ncol=3, fontsize=7.5, bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(rect=(0, 0.05, 1, 1)); save(fig, 'fig2_gap_paths', FIG)

# ---------- Figure 3: (a) employment elasticities across designs, (b) the 2017Q1 break in establishment counts ----------
fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), gridspec_kw={'width_ratios': [1.45, 1]})
ax = axes[0]
rows = [('Main (random-halves placebo)', lambda ind: E[ind]['emp']['main']['elasticity']),
        ('Main (single-county placebo)', lambda ind: E[ind]['emp']['main']['elasticity_single_county_placebo']),
        ('Pre-COVID only, 2014–2019', lambda ind: E[ind]['robustness']['emp']['pre_covid_only']),
        ('Step at 2017Q1 added', lambda ind: E[ind]['robustness']['emp']['step_2017']),
        ('Linear trend added', lambda ind: E[ind]['robustness']['emp']['trend']),
        ('2023 narrowing only (2022→2023)', lambda ind: E[ind]['emp']['main']['implied_elasticity_2023']),
        ('Synthetic control', lambda ind: SC[ind]['emp']['elasticity'])]
cols = {'722': BLUE, '722511': ORANGE, '722513': GREEN}
off = {'722': -0.22, '722511': 0.0, '722513': 0.22}
mk = {'722': 'o', '722511': 's', '722513': 'D'}
for r, (lab, f) in enumerate(rows):
    for ind in ['722', '722511', '722513']:
        m = f(ind); y = r + off[ind]
        ax.plot([m['lo'], m['hi']], [y, y], color=cols[ind], lw=1.6)
        ax.plot(m['est'], y, marker=mk[ind], color=cols[ind], ms=5, mec='white', mew=0.6,
                label={'722': 'All 722', '722511': 'Full-service', '722513': 'Limited-service'}[ind] if r == 0 else None)
ax.axvline(0, color=MUTED, lw=0.8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=7.5); ax.invert_yaxis()
ax.set_xlabel('Employment elasticity with respect to the minimum wage (95% placebo interval)')
ax.set_xlim(-2.6, 4.7)
ax.set_title('(a) Long Island vs rest of state, employment', loc='left', fontsize=9, color=INK)
ax.legend(fontsize=7.5, loc='upper center', bbox_to_anchor=(0.45, -0.14), ncol=3)
ax = axes[1]
B = SM['break_2017Q1']; inc = SM['mw_increase_2017Q1_pct']
pts = [('NYC', '722_NYC', inc['NYC_large']), ('Long Island', '722_LI', inc['LI_WES']), ('Westchester', '722_WES', inc['LI_WES']),
       ('Rest of state', '722_ROS', inc['ROS']), ('Pennsylvania', '722_PA', inc['PA'])]
for name, k, x in pts:
    y = 100 * B[k]['estabs_2017']; y0 = 100 * B[k]['estabs_median_other_years']
    ax.plot([x, x], [y0, y], color=LIGHT, lw=1.2)
    ax.plot(x, y, 'o', color=BLUE, ms=7, mec='white', mew=0.8)
    ax.plot(x, y0, 'o', color=MUTED, ms=5, mfc='white')
    dy = -1.3 if name == 'Westchester' else 0.6
    ax.annotate(name, (x, y), xytext=(5, 6 if name != 'Westchester' else -11), textcoords='offset points', fontsize=7.5, color=INK)
ax.plot([], [], 'o', color=BLUE, label='Q4 2016 → Q1 2017'); ax.plot([], [], 'o', color=MUTED, mfc='white', label='Median Q4 → Q1, other years')
ax.axhline(0, color=MUTED, lw=0.8)
ax.set_xlabel('Increase in general minimum wage, 31 Dec 2016 (%)'); ax.set_ylabel('Change in restaurant establishments (%)')
ax.set_xlim(-2, 26); ax.set_ylim(-3, 15)
ax.set_title('(b) Establishment counts, NAICS 722', loc='left', fontsize=9, color=INK)
ax.legend(fontsize=7.2, loc='upper left')
fig.tight_layout(); save(fig, 'fig3_elasticities_break', FIG)
print('ok')
