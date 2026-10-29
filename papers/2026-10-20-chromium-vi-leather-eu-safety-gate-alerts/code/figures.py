"""Figures (300 dpi PNG + PDF). Run after analysis.py. Palette as in the series' earlier papers; identity is also
carried by direct labels or legends."""
import json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import RES, FIG
BLUE, ORANGE, GREEN, YELLOW, INK, MUTED, GRID, LIGHT = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#0b0b0b', '#52514e', '#e4e3df', '#c9c7c0'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': GRID,
                     'grid.linewidth': 0.6, 'legend.frameon': False, 'axes.axisbelow': True})
An = json.load(open(f'{RES}/analysis.json'))
A = pd.read_csv(f'{RES}/alerts.csv'); S = A[A.scope].copy(); S['after'] = S.pub_date >= '2015-05-01'
Y = pd.DataFrame(An['B_series'])
EU = 2015 + 4 / 12  # 1 May 2015


def save(fig, n): fig.savefig(f'{FIG}/{n}.png', dpi=300, bbox_inches='tight'); fig.savefig(f'{FIG}/{n}.pdf', bbox_inches='tight'); plt.close(fig)


def eu_line(ax, y, label=True, x=EU):
    ax.axvline(x, color=MUTED, lw=0.9, ls='--')
    if label: ax.text(x + 0.2, y, 'EU limit applies\n(1 May 2015)', fontsize=7, color=MUTED, va='top')


# Fig 1: notifications per year (A) and per 1,000 Safety Gate alerts (B)
Yp = Y[Y.year.between(2005, 2026)]
fig, ax = plt.subplots(2, 1, figsize=(7.0, 4.6), sharex=True, gridspec_kw=dict(hspace=0.18))
ax[0].bar(Yp.year, Yp.n_de, color=BLUE, width=0.78, label='Notified by Germany', edgecolor='white', linewidth=0.6)
ax[0].bar(Yp.year, Yp.n_other, bottom=Yp.n_de, color=ORANGE, width=0.78, label='Notified by other countries', edgecolor='white', linewidth=0.6)
ax[0].set_ylabel('Notifications'); ax[0].legend(loc='upper right', fontsize=7.5); ax[0].grid(axis='x', visible=False)
ax[0].set_title('A  Hexavalent chromium in leather articles, EU Safety Gate', loc='left', fontsize=9, color=INK)
eu_line(ax[0], ax[0].get_ylim()[1] * 0.98, x=EU - 0.5)
full = Yp[Yp.year <= 2025]
ax[1].plot(full.year, full.per1000_all, color=INK, lw=1.8, marker='o', ms=4)
p26 = Yp[Yp.year == 2026]
ax[1].plot(p26.year, p26.per1000_all, ls='', marker='o', ms=4, mfc='white', mec=INK)
ax[1].set_ylabel('Per 1,000 alerts'); ax[1].grid(axis='x', visible=False)
ax[1].set_title('B  Share of all Safety Gate alerts', loc='left', fontsize=9, color=INK)
ax[1].text(2026.25, p26.per1000_all.iloc[0], '2026\n(to 20 Oct)', fontsize=6.8, color=MUTED, va='center')
eu_line(ax[1], 0, label=False, x=EU - 0.5)
ax[1].set_xlim(2004.4, 2027.3); ax[1].set_xticks(range(2005, 2027, 3))
save(fig, 'fig1_alerts_per_year')

# Fig 2: measured concentrations
C = S[S.conc_max.notna()].copy()
rng = np.random.default_rng(1)
fig, ax = plt.subplots(figsize=(7.0, 3.4))
d = pd.to_datetime(C.pub_date); x = d.dt.year + (d.dt.dayofyear - 1) / 365.25  # exact publication date, so points sit on the correct side of 1 May 2015
ax.scatter(x, C.conc_max, s=10, color=np.where(C.after, BLUE, ORANGE), alpha=0.55, linewidths=0)
med = C[C.year >= 2010].groupby('year').conc_max.agg(['median', 'size'])
med = med[med['size'] >= 5]
ax.plot(med.index + 0.5, med['median'], color=INK, lw=1.8, marker='s', ms=4, label='Yearly median (years with 5 or more values)')
ax.axhline(3, color=INK, lw=1, ls=':')
ax.text(2005.2, 3.25, 'Limit 3 mg/kg', fontsize=7, color=INK)
ax.set_yscale('log'); ax.set_ylim(2, 600); ax.set_yticks([3, 10, 30, 100, 300]); ax.set_yticklabels(['3', '10', '30', '100', '300'])
ax.set_ylabel('Highest reported Cr(VI), mg/kg (log scale)'); ax.set_xlim(2005, 2027); ax.set_xticks(range(2005, 2028, 3))
ax.grid(axis='x', visible=False); eu_line(ax, 520)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], marker='o', ls='', color=ORANGE, alpha=0.7, label='Notified before 1 May 2015'),
                   Line2D([], [], marker='o', ls='', color=BLUE, alpha=0.7, label='Notified after'),
                   Line2D([], [], marker='s', color=INK, label='Yearly median (5+ values), plotted mid-year')], fontsize=7, loc='upper left', ncol=3,
          bbox_to_anchor=(0, 1.13))
save(fig, 'fig2_concentrations')

# Fig 3: what and where from, before vs after
E = An['E']
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.5), gridspec_kw=dict(wspace=0.45))
def hstack(a, d, order, colors, title):
    for j, per in enumerate(['before', 'after']):
        left = 0
        for k, c in zip(order, colors):
            v = d[per].get(k.lower() if k.lower() in d[per] else k, {}).get('pct', 0)
            a.barh(j, v, left=left, color=c, height=0.62, edgecolor='white', linewidth=1)
            if v >= 7: a.text(left + v / 2, j, f'{v:.0f}%', ha='center', va='center', fontsize=7, color='white' if c not in (LIGHT, YELLOW) else INK)
            left += v
    a.set_yticks([0, 1]); a.set_yticklabels([f"Before\n(n = {d['before']['_n']})", f"After\n(n = {d['after']['_n']})"])
    a.invert_yaxis(); a.set_xlim(0, 100); a.set_xlabel('% of notifications'); a.grid(axis='y', visible=False)
    a.set_title(title, loc='left', fontsize=9, color=INK)
    a.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in colors], labels=order, fontsize=6.8, loc='upper center',
             bbox_to_anchor=(0.45, -0.32), ncol=3, handlelength=1, columnspacing=0.8)
hstack(ax[0], E['ptype'], ['Footwear', 'Gloves', 'Bags and small leather goods', 'Garments', 'Other'], [BLUE, ORANGE, GREEN, YELLOW, LIGHT], 'A  Product')
hstack(ax[1], E['origin'], ['China', 'South Asia', 'EU', 'Other', 'Unknown'], [BLUE, ORANGE, GREEN, YELLOW, LIGHT], 'B  Country of origin')
save(fig, 'fig3_composition')
print('figures written')
