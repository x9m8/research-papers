import json, numpy as np, pandas as pd
from style import plt, save, BLUE, ORANGE, GREEN, YELLOW, INK, MUTED, GRID, LIGHT
from common import RES, FIG, CORE_CF, CORE_RULE, CF_SETS
o = json.load(open(f'{RES}/analysis.json'))
Y = pd.read_csv(f'{RES}/eu_embodied_by_year.csv')
base = Y[(Y.china == 1) & (~Y.extra3) & (Y.bovine == 1)]
core = base[(base.cf == CORE_CF) & (base.balance == 'clip')]
P = core.pivot(index='t', columns='method', values=CORE_RULE); Q = core.pivot(index='t', columns='method', values='rhe') / 1e3

# Figure 1: annual series
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0))
sw = base[base.method == 'Stage-wise tracing'].groupby('t')[CORE_RULE].agg(['min', 'max'])
ax[0].fill_between(sw.index, sw['min'] / 1e3, sw['max'] / 1e3, color=BLUE, alpha=0.15, lw=0)
lines = [('Exporter: all direct imports', ORANGE, 'Direct imports,\nall stages'), ('Exporter: hides and leather', YELLOW, 'Direct imports,\nhides and leather'),
         ('Pooled tracing (Laroche)', GREEN, 'Pooled tracing'), ('Stage-wise tracing', BLUE, 'Stage-wise tracing')]
for m, c, lab in lines:
    ax[0].plot(P.index, P[m] / 1e3, color=c, lw=2 if m == 'Stage-wise tracing' else 1.4, label=lab.replace('\n', ' '))
ax[0].set_ylabel('Embodied deforestation (thousand ha/yr)'); ax[0].set_ylim(0, None); ax[0].set_xlim(2005, 2023)
ax[0].set_title('A  Deforestation, 5% allocation', loc='left', fontsize=9, color=INK)
ax[0].legend(fontsize=7, loc='upper right')
for m, c, lab in [('Exporter: hides and leather', YELLOW, 'Direct imports: hides and leather'), ('Exporter: articles', MUTED, 'Direct imports: articles'), ('Stage-wise tracing', BLUE, 'EU use (stage-wise)')]:
    ax[1].plot(Q.index, Q[m], color=c, lw=2 if m == 'Stage-wise tracing' else 1.4, label=lab)
ax[1].set_ylabel('Raw-hide equivalent (thousand t/yr)'); ax[1].set_ylim(0, None); ax[1].set_xlim(2005, 2023)
ax[1].set_title('B  Hide equivalents', loc='left', fontsize=9, color=INK); ax[1].legend(fontsize=7, loc='lower left')
for a in ax: a.set_xticks([2005, 2010, 2015, 2020])
fig.tight_layout(); save(fig, 'fig1_series', FIG)

# Figure 2: bridge from exporter attribution to stage-wise consumption, 2015-2020
b = o['bridge_2015_2020_ha']
steps = [('Direct imports,\nhides & leather\n(exporter)', b['Exporter attribution, hides and leather'], 'total'),
         ('Re-attributed\nto cattle\norigin', b['Re-attribution of hides and leather imports to cattle origin'], 'step'),
         ('Imported\narticles', b['Articles imported, traced to cattle origin'], 'step'),
         ('EU-produced\nhides', b['EU-produced hides'], 'step'),
         ('EU exports,\nall stages', b['Minus EU exports (all stages), traced'], 'step'),
         ('EU use\n(stage-wise)', b['Stage-wise tracing (model)'], 'total')]
fig, ax = plt.subplots(figsize=(7.2, 3.2)); run = 0
for n, (lab, v, kind) in enumerate(steps):
    if kind == 'total': bot, h, c = 0, v, (YELLOW if n == 0 else BLUE); run = v
    else: bot, h, c = (run, v, GREEN) if v >= 0 else (run + v, -v, ORANGE); run += v
    ax.bar(n, h / 1e3, bottom=bot / 1e3, color=c, width=0.62)
    ax.text(n, (bot + h) / 1e3 + 0.4, (f'{v:+,.0f}' if kind == 'step' else f'{v:,.0f}'), ha='center', fontsize=7.5, color=INK)
ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps], fontsize=7.5)
ax.set_ylabel('Thousand ha/yr, 5% allocation'); ax.grid(axis='x', visible=False); ax.set_ylim(0, 36)
fig.tight_layout(); save(fig, 'fig2_bridge', FIG)

# Figure 3: entry routes
r = pd.read_csv(f'{RES}/routes_ha_by_year.csv', index_col=0)
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1.4, 1]))
bot = np.zeros(len(r))
for col, c, lab in [('Direct from origin', YELLOW, 'Entered direct from origin'), ('Via third country', BLUE, 'Entered via a third country')]:
    ax[0].bar(r.index, r[col] / 1e3, bottom=bot, color=c, width=0.8, label=lab, edgecolor='white', linewidth=0.5); bot += r[col].values / 1e3
ax[0].set_ylabel('Thousand ha/yr, 5% allocation'); ax[0].legend(fontsize=7, loc='upper right'); ax[0].grid(axis='x', visible=False)
ax[0].set_title('A  EU use by entry route', loc='left', fontsize=9, color=INK)
e = o['indirect_ha_entry_countries_share']; ks = list(e)[:7][::-1]
ax[1].barh(range(len(ks)), [100 * e[k] for k in ks], color=BLUE, height=0.6)
ax[1].set_yticks(range(len(ks))); ax[1].set_yticklabels(ks, fontsize=7.5); ax[1].grid(axis='y', visible=False)
for n, k in enumerate(ks): ax[1].text(100 * e[k] + 0.6, n, f'{100 * e[k]:.0f}%', va='center', fontsize=7.5, color=INK)
ax[1].set_xlabel('Share of indirect hectares, 2015–2020 (%)'); ax[1].set_xlim(0, 38)
ax[1].set_title('B  Recorded exporting country', loc='left', fontsize=9, color=INK)
fig.tight_layout(); save(fig, 'fig3_routes', FIG)
print('ok')
