import json, pandas as pd, numpy as np
from style import *
import matplotlib.ticker
from common import RES, FIG
M = pd.read_csv(f'{RES}/allocation_monthly.csv', index_col=0); t = pd.PeriodIndex(M.index, freq='M'); x = t.year + (t.month - 0.5) / 12
C = json.load(open(f'{RES}/hide_calibration.json'))
def dx(s): d = pd.Timestamp(s); return d.year + (d.dayofyear - 0.5) / 365.25
fig, ax = plt.subplots(figsize=(7.0, 3.2))
ax.plot(x, M.hide, color=INK, lw=1.4, label='PPI for hides and skins scaled to dollars')
ax.scatter([dx(r['date']) for r in C['cal']], [r['price'] for r in C['cal']], s=26, color=ORANGE, zorder=3, label='USDA AMS report price (used to scale)')
pt = [r for r in C['val'] if not any(k in r['kind'] for k in ('2018 average', 'Jan-Jun', '2013-2017'))]
ax.scatter([dx(r['date']) for r in pt], [r['price'] for r in pt], s=26, facecolor='white', edgecolor=BLUE, lw=1.3, zorder=3, label='Published quote (check, not used to scale)')
ax.set_ylabel('US butt-branded steer hide, $ per piece'); ax.set_xlim(2001, 2026.3); ax.set_ylim(0, 110); ax.grid(axis='x', visible=False)
ax.legend(fontsize=7, loc='upper left')
save(fig, 'fig1_hide_price', FIG)

Y = pd.read_csv(f'{RES}/allocation_annual.csv')
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw=dict(wspace=0.35, width_ratios=[1.45, 1]))
a = ax[0]
alts = Y[['share_cattle_lw', 'share_tx', 'share_dress62', 'share_dress64', 'share_output']] * 100
a.fill_between(Y.year, alts.min(axis=1).clip(upper=Y.share * 100), alts.max(axis=1).clip(lower=Y.share * 100), color=BLUE, alpha=0.18, lw=0, label='Range across five alternative denominators')
a.plot(Y.year, Y.share * 100, color=BLUE, lw=2, marker='o', ms=3.5, label='Main estimate')
a.set_ylabel("Hide's share of the steer's value, %"); a.set_ylim(0, 6.6); a.set_xlim(2001, 2025.5); a.grid(axis='x', visible=False)
a.set_title('A  Economic allocation factor for the hide', loc='left', fontsize=9, color=INK); a.legend(fontsize=6.8, loc='lower left')
b = ax[1]
b.plot(Y.year, Y.hide / Y.hide.iloc[1] * 100, color=ORANGE, lw=1.8, label='Hide, $ per piece')
b.plot(Y.year, Y.live_value / Y.live_value.iloc[1] * 100, color=INK, lw=1.8, label='Live steer, $ per head')
b.axhline(100, color=MUTED, lw=0.6); b.set_yscale('log'); b.set_yticks([25, 50, 100, 200, 400]); b.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); b.set_yticklabels(['25', '50', '100', '200', '400'])
b.set_ylabel('Index, 2002 = 100 (log)'); b.set_xlim(2001, 2025.5); b.grid(axis='x', visible=False)
b.set_title('B  Two prices pulling apart', loc='left', fontsize=9, color=INK); b.legend(fontsize=6.8, loc='upper left')
save(fig, 'fig2_allocation', FIG)
print('ok')
