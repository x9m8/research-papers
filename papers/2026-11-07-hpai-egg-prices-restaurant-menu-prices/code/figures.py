"""Figures 1-3 (PNG 300 dpi + PDF)."""
import json, numpy as np, pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from style import *
from common import *
d = load_monthly(); L, n = monthly_layers()
A1 = json.load(open(f'{RES}/a1_hpai_to_prices.json')); A2 = json.load(open(f'{RES}/a2_passthrough.json'))
def dt(p): return p.to_timestamp()
# Figure 1
fig, ax = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True, gridspec_kw={'height_ratios': [1, 1.25]})
ax[0].bar(dt(L.index), L.values, width=25, color=ORANGE)
ax[0].set_ylabel('Commercial table-egg layers\nconfirmed, millions per month'); ax[0].set_title('A  HPAI detections in commercial table-egg layer flocks (APHIS)', loc='left', fontsize=9)
s = d.loc['2022-01':'2026-09']
base = {'avg_price_egg': s['avg_price_egg']['2022-01'], 'cpi_egg': s['cpi_egg']['2022-01'], 'ppi_egg_large': s['ppi_egg_large']['2022-01']}
for k, c, lab in [('ppi_egg_large', LIGHT, 'PPI, large eggs (producer)'), ('cpi_egg', BLUE, 'CPI, eggs'), ('avg_price_egg', GREEN, 'Average price, Grade A large (retail)')]:
    ax[1].plot(dt(s.index), 100 * s[k] / base[k], color=c, lw=1.6 if k != 'ppi_egg_large' else 1.1, label=lab)
ax[1].set_yscale('log'); ax[1].set_yticks([50, 100, 200, 400, 800]); ax[1].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter()); ax[1].yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax[1].set_ylim(40, 900)
ax[1].set_ylabel('Index, January 2022 = 100 (log scale)'); ax[1].legend(loc='upper left', fontsize=7.5)
ax[1].set_title('B  Egg prices', loc='left', fontsize=9)
ax[1].axvspan(pd.Timestamp('2025-10-01'), pd.Timestamp('2025-10-31'), color='#bbbbbb', alpha=0.5, lw=0); ax[1].text(pd.Timestamp('2025-10-15'), 55, 'no\nOct 2025\ndata', fontsize=6, ha='center', color=MUTED)
ax[1].xaxis.set_major_locator(mdates.YearLocator()); ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
save(fig, 'fig1_layers_and_prices', FIG)
# Figure 2
fig, ax = plt.subplots(1, 3, figsize=(7.4, 3.0), sharey=False)
for a, (y, lab, col) in zip(ax, [('ppi_egg_large', 'PPI, large eggs', LIGHT), ('avg_price_egg', 'Retail average price', GREEN), ('cpi_egg', 'CPI, eggs', BLUE)]):
    r = A1['main'][y]; h = [x['h'] for x in r]; b = np.array([100 * 10 * x['b'] for x in r]); lo = np.array([100 * 10 * x['lo'] for x in r]); hi = np.array([100 * 10 * x['hi'] for x in r])
    a.fill_between(h, lo, hi, color=col, alpha=0.3, lw=0); a.plot(h, b, color=INK if y == 'ppi_egg_large' else col, lw=1.6, marker='o', ms=3); a.axhline(0, color=MUTED, lw=0.8)
    a.set_title(lab, fontsize=8.5); a.set_xlabel('Months after detection month'); a.set_xticks(range(0, 9, 2))
ax[0].set_ylabel('Change in log price, % points,\nper 10 million layers confirmed')
save(fig, 'fig2_local_projections', FIG)
# Figure 3
fig = plt.figure(figsize=(7.4, 7.0)); gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.25], hspace=0.42, wspace=0.95)
a = fig.add_subplot(gs[0, 0]); yy = A2['yoy_series']
idx = [k for k in yy['cpi_egg'] if '2021-06' <= k <= '2026-09']
x = pd.PeriodIndex(idx, freq='M').to_timestamp()
a.plot(x, [np.nan if yy['cpi_egg'][k] is None else yy['cpi_egg'][k] for k in idx], color=BLUE, label='Eggs (CPI)')
a.set_ylabel('Eggs, 12-month change, %', color=BLUE); a.set_title('A  Egg and restaurant inflation', loc='left', fontsize=9)
a2 = a.twinx(); a2.spines['right'].set_visible(True); a2.grid(False)
a2.plot(x, [np.nan if yy['cpi_fsr'][k] is None else yy['cpi_fsr'][k] for k in idx], color=ORANGE, label='Full-service meals'); a2.plot(x, [np.nan if yy['cpi_lsr'][k] is None else yy['cpi_lsr'][k] for k in idx], color=GREEN, label='Limited-service meals')
a2.set_ylabel('Restaurants, 12-month change, %', color=ORANGE); a2.set_ylim(0, 12)
h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels(); a.legend(h1 + h2, l1 + l2, fontsize=6.5, loc='lower left'); a.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
b = fig.add_subplot(gs[0, 1])
for y, col, off in [('cpi_fsr', ORANGE, -0.1), ('cpi_lsr', GREEN, 0.1)]:
    r = A2['main'][y]['cum_by_k']; k = np.array([q['k'] for q in r]) + off
    est = np.array([10 * q['est'] for q in r]); lo = np.array([10 * q['lo'] for q in r]); hi = np.array([10 * q['hi'] for q in r])
    b.errorbar(k, est, yerr=[est - lo, hi - est], fmt='o-', color=col, ms=3, lw=1.2, capsize=2, label={'cpi_fsr': 'Full-service', 'cpi_lsr': 'Limited-service'}[y])
b.axhline(0, color=MUTED, lw=0.8); b.set_xlabel('Lags of egg price change included (months)'); b.set_ylabel('Menu-price response, % pts\nper 10% rise in egg CPI'); b.legend(fontsize=7); b.set_title('B  Cumulative pass-through', loc='left', fontsize=9)
c = fig.add_subplot(gs[1, :]); labs = list(A2['sens'].keys()); ypos = np.arange(len(labs))[::-1]
for y, col, off in [('cpi_fsr', ORANGE, 0.17), ('cpi_lsr', GREEN, -0.17)]:
    est = np.array([10 * A2['sens'][l][y]['cum'] for l in labs]); lo = np.array([10 * A2['sens'][l][y]['cum_lo'] for l in labs]); hi = np.array([10 * A2['sens'][l][y]['cum_hi'] for l in labs])
    c.errorbar(est, ypos + off, xerr=[est - lo, hi - est], fmt='o', color=col, ms=3, lw=1.1, capsize=2, label={'cpi_fsr': 'Full-service', 'cpi_lsr': 'Limited-service'}[y])
c.axvline(0, color=MUTED, lw=0.8); c.set_yticks(ypos); c.set_yticklabels(labs, fontsize=7.5); c.set_xlabel('Cumulative menu-price response, % points per 10% rise in egg price (95% CI)'); c.legend(fontsize=7, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)
c.set_title('C  Sensitivity of the cumulative response', loc='left', fontsize=9)
save(fig, 'fig3_passthrough', FIG); print('figs ok')
