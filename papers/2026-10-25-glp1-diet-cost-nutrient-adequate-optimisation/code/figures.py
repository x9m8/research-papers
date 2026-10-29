import json, numpy as np, pandas as pd
from style import *
from common import RES, FIG, TFP_DAY_SINGLE
R = json.load(open(f'{RES}/results.json')); G = R['grid']; RS = [0.0, 0.16, 0.24, 0.35, 0.39]
SEX = {'F': 'Women', 'M': 'Men'}
# Fig 1 cost
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.3), sharey=True, gridspec_kw=dict(wspace=0.08))
for a, s in zip(ax, 'FM'):
    x = np.array(RS) * 100; g = [G[f'{s}|{r}|0.8'] for r in RS]
    a.plot(x, [v['cost_scaled'] for v in g], color=MUTED, lw=1.6, marker='o', ms=3, label='Eating less of the same')
    ad = [v['adequate']['cost'] if v['adequate']['feasible'] else np.nan for v in g]
    be = [v['adequate']['cost'] if not v['adequate']['feasible'] else np.nan for v in g]
    last = max(i for i, v in enumerate(ad) if not np.isnan(v)); be[last] = ad[last]
    a.plot(x, ad, color=BLUE, lw=2.2, marker='o', ms=3, label='Closest adequate diet*')
    a.plot(x, be, color=BLUE, lw=1.4, ls='--', marker='o', ms=3, mfc='white', label='Best achievable (not fully adequate)')
    a.plot(x, [v['p99']['cost'] for v in g], color=BLUE, lw=1.2, ls=':', marker='s', ms=2.5, alpha=0.8, label='Closest adequate diet*, wider limits (P99)')
    a.plot(x, [v['cheapest']['cost'] if v['cheapest']['feasible'] else np.nan for v in g], color=GREEN, lw=1.6, marker='o', ms=3, label='Cheapest adequate diet*')
    a.plot(x, [v['floor']['cost'] for v in g], color=ORANGE, lw=1.2, ls=':', marker='o', ms=2.5, label='Least-cost diet from any foods*')
    lo, hi = TFP_DAY_SINGLE[s]; a.axhspan(lo, hi, color=INK, alpha=0.10, lw=0, label='Thrifty Food Plan, June 2026, one-person household, ages 51–70 to 20–50')
    a.axvspan(16, 39, color=YELLOW, alpha=0.12, lw=0)
    a.set_title(f'{"A" if s == "F" else "B"}  {SEX[s]}', loc='left', fontsize=9, color=INK); a.set_xlabel('Cut in energy intake, %'); a.set_xlim(-1.5, 41); a.set_ylim(0, 13.5); a.grid(axis='x', visible=False)
ax[0].set_ylabel('Food cost, US$ per person per day (2026)'); ax[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f'${v:.0f}'))
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=3, fontsize=6.8)
save(fig, 'fig1_cost', FIG)
# Fig 2 frontier by specification
F = R['frontier']; specs = [('cat_p95', 'Fixed mix,\nP95 (main)'), ('cat_p99', 'Fixed mix,\nP99'), ('food5', 'Free mix,\n≤5× per food'), ('food_free', 'Free mix,\nno food limit')]
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1), sharey=True, gridspec_kw=dict(wspace=0.08)); w = 0.38
for a, s in zip(ax, 'FM'):
    for j, (lab, c, nm) in enumerate([('no_D_E', BLUE, 'Vitamins D and E set aside'), ('all', ORANGE, 'All nutrients')]):
        v = [100 * (F[f'{s}|{k}|{lab}'] or 0) for k, _ in specs]
        bars = a.bar(np.arange(4) + (j - 0.5) * w, v, w, color=c, zorder=2, label=nm)
        for bb, vv, (k, _) in zip(bars, v, specs):
            t = '≥60' if vv >= 59.9 else ('<1' if vv < 1 else f'{vv:.0f}')
            a.text(bb.get_x() + bb.get_width() / 2, vv + 0.8, t, ha='center', fontsize=6.3, color=MUTED)
    a.axhspan(16, 39, color=YELLOW, alpha=0.15, lw=0, zorder=0); 
    a.set_xticks(range(4)); a.set_xticklabels([l for _, l in specs], fontsize=6.5); a.set_ylim(0, 68); a.grid(axis='x', visible=False)
    a.set_title(f'{"A" if s == "F" else "B"}  {SEX[s]}', loc='left', fontsize=9, color=INK)
ax[0].set_ylabel('Largest cut in energy intake at which\nan adequate diet exists, %')
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=6.8)
save(fig, 'fig2_frontier', FIG)
# Fig 3 category changes at 24%
SHORT = {'Ready-to-eat cereal, higher sugar (>21.2g/100g)': 'Breakfast cereal, higher sugar', 'Ready-to-eat cereal, lower sugar (=<21.2g/100g)': 'Breakfast cereal, lower sugar', 'Pasta mixed dishes, excludes macaroni and cheese': 'Pasta mixed dishes', 'Burgers (single code)': 'Burgers'}
D = pd.read_csv(f'{RES}/diets_by_category.csv'); D = D[D.r == 0.24]
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.6), gridspec_kw=dict(wspace=0.9))
for a, s in zip(ax, 'FM'):
    p = D[D.sex == s].pivot_table(index='desc', columns='diet', values='kcal').fillna(0); p['chg'] = p.adequate - p.scaled
    p = pd.concat([p.sort_values('chg').head(7), p.sort_values('chg').tail(7)])
    a.barh(range(len(p)), p.chg, color=[ORANGE if v < 0 else BLUE for v in p.chg]); a.set_yticks(range(len(p))); a.set_yticklabels([SHORT.get(d, d) for d in p.index], fontsize=6.5)
    a.axvline(0, color=INK, lw=0.8); a.set_xlabel('Change in kcal per day'); a.grid(axis='y', visible=False)
    a.set_title(f'{"A" if s == "F" else "B"}  {SEX[s]}, 24% cut', loc='left', fontsize=9, color=INK)
save(fig, 'fig3_changes', FIG); print('ok')
