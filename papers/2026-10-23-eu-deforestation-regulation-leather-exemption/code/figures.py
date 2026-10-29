import json, numpy as np, pandas as pd
from style import *
from common import RES, FIG
A = json.load(open(f'{RES}/analysis.json')); Y = pd.read_csv(f'{RES}/embodied_by_year.csv', index_col=0)
pr = pd.Series(A['price_ratio']); pr.index = pr.index.astype(int)
aw = pd.Series(A['alpha_weighted']); aw.index = aw.index.astype(int)
ab = pd.Series(A['brazil_alpha']); ab.index = ab.index.astype(int)
# Fig 1
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw=dict(wspace=0.35))
a = ax[0]; a.plot(pr.index, pr, color=ORANGE, lw=2, marker='o', ms=3)
a.set_ylabel('Raw hide price ÷ beef price\n(ratio of EU import unit values)'); a.set_ylim(0, 0.7); a.grid(axis='x', visible=False)
a.set_title('A  Hides cheapened against beef', loc='left', fontsize=9, color=INK)
b = ax[1]
for v, lab, c, ls in [(10, 'Mass, Laroche et al. 10%', MUTED, '--'), (8, 'Mass, SWD 8%', MUTED, ':'), (5, 'DeDuCE / SWD co-product 5%', INK, '-'), (3.5, 'PEFCR 3.5%', ORANGE, ':'), (2.5, 'SWD by-product 2.5%', GREEN, '--')]:
    b.axhline(v, color=c, ls=ls, lw=1); b.text(2025.6, v, lab, fontsize=6.3, va='center', color=c)
b.plot(aw.index, aw * 100, color=BLUE, lw=2, marker='o', ms=3, label='Economic, EU import-weighted')
b.plot(ab.index, ab * 100, color=BLUE, lw=1, ls='--', alpha=0.7, label='Economic, Brazil')
b.set_ylim(0, 11); b.set_xlim(2004.5, 2025); b.set_ylabel("Hide's share of cattle deforestation, %"); b.grid(axis='x', visible=False)
b.set_title('B  Allocation factors', loc='left', fontsize=9, color=INK); b.legend(fontsize=6.5, loc='lower left')
save(fig, 'fig1_prices_alpha', FIG)
# Fig 2
fig, ax = plt.subplots(figsize=(7.0, 3.3))
ax.fill_between([2015, 2020], 19504, 39005, color=YELLOW, alpha=0.35, lw=0, label='Commission estimate for 2015–2020 trade, 19,504–39,005 ha')
for col, c, ls, lw in [('Mass, FAOSTAT weights', MUTED, '-.', 1.0), ('Mass (Laroche et al.), 10%', MUTED, '--', 1.2), ('Mass (SWD), 8%', MUTED, ':', 1.2), ('DeDuCE / SWD co-product, 5%', INK, '-', 1.4), ('PEFCR, 3.5%', ORANGE, ':', 1.2),
                       ('By-product (SWD), 2.5%', GREEN, '--', 1.2), ('Economic, price of the year', BLUE, '-', 2.2)]:
    ax.plot(Y.index, Y[col], color=c, ls=ls, lw=lw, label=col)
ax.set_ylabel('Deforestation embodied in EU imports\nof hides and leather, ha per year'); ax.set_ylim(0, 145000); ax.grid(axis='x', visible=False)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f'{v:,.0f}'))
ax.legend(fontsize=6.6, ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.12)); ax.set_xlim(2004.5, 2022.5)
save(fig, 'fig2_embodied', FIG)
# Fig 3
bc15 = A['benefit_cost_2015_2020']; bc22 = A['benefit_cost_2022']
keys = ['By-product (SWD), 2.5%', 'Economic, price of the year', 'PEFCR, 3.5%', 'DeDuCE / SWD co-product, 5%', 'Mass (SWD), 8%', 'Mass (Laroche et al.), 10%', 'Mass, FAOSTAT weights']
fig, ax = plt.subplots(figsize=(7.0, 3.2)); y = np.arange(len(keys))
ax.barh(y - 0.18, [bc15[k] for k in keys], height=0.34, color=BLUE, label='2015–2020 mean')
ax.barh(y + 0.18, [bc22[k] for k in keys], height=0.34, color=ORANGE, label='2022')
ax.axvline(1, color=INK, lw=1); ax.text(1.08, -0.55, 'benefit = cost', fontsize=6.8, color=INK)
ax.set_xscale('log'); ax.set_xlim(0.5, 400); ax.set_yticks(y); ax.set_yticklabels(keys, fontsize=7.5); ax.invert_yaxis()
ax.set_xlabel("Benefit-cost ratio of keeping leather in scope (Commission's own valuation)"); ax.grid(axis='y', visible=False); ax.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f'{v:g}'))
save(fig, 'fig3_benefit_cost', FIG); print('ok')
