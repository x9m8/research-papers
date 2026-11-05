"""Figures 1-3 (PNG 300 dpi + PDF) from results/*.csv."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from style import *
from common import *

S = pd.read_csv(f'{RES}/series_aggregate.csv').set_index('year')
SG = pd.read_csv(f'{RES}/series_subindustry.csv', dtype={'naics': str})
Z = pd.read_csv(f'{RES}/size_distribution.csv').set_index('year')

def vlines(ax, lab=False):
    for b in BREAK_YEARS:
        ax.axvline(b - 0.5, color=LIGHT, lw=0.8, ls=(0, (3, 3)), zorder=0)

# ---- Figure 1: indexed series
fig, ax = plt.subplots(figsize=(6.6, 3.9))
vlines(ax)
for col, lab, c, ls in [('leather_emp_est_idx', 'Employer establishments (CBP)', BLUE, '-'), ('leather_emp_jobs_idx', 'Employer employment (CBP)', INK, '-'),
                        ('leather_ne_firms_idx', 'Nonemployer firms (NES)', ORANGE, '-'), ('leather_ne_receipts_idx', 'Nonemployer receipts, nominal (NES)', ORANGE, (0, (4, 2)))]:
    s = S[col].dropna(); ax.plot(s.index, s.values, color=c, ls=ls, lw=1.8, label=lab)
ax.plot([2007], [S.loc[2007, 'leather_ne_firms_idx']], 'o', mfc='white', mec=ORANGE, ms=5, zorder=5)
ax.axhline(100, color=MUTED, lw=0.6)
ax.set_ylabel('Index, 2004 = 100'); ax.set_xticks(range(2004, 2025, 2)); ax.set_ylim(30, 175)
for b, v in zip(BREAK_YEARS, [2007, 2012, 2017, 2022]):
    ax.text(b - 0.45, 31, f'NAICS {v}', fontsize=6.5, color=MUTED, rotation=90, va='bottom')
ax.legend(loc='upper left', fontsize=7.5, ncol=1)
fig.text(0.01, -0.02, 'Employer series end in 2023, nonemployer series in 2024. Hollow marker: 2007 nonemployer value summed from state files (two states withheld).\nDashed verticals: first year of a new NAICS vintage (2007, 2012, 2017, 2022 vintages assumed to start in the same reference year).', fontsize=6.5, color=MUTED, va='top')
save(fig, 'fig1_indexed_series', FIG)

# ---- Figure 2: nonemployer share
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.5), sharey=False)
ax = axs[0]; vlines(ax)
for tag, lab, c in [('leather', 'Leather and allied (316)', ORANGE), ('mfg', 'All manufacturing (31-33)', BLUE), ('all', 'All industries', MUTED)]:
    s = S[f'{tag}_ne_share_pct'].dropna(); ax.plot(s.index, s.values, color=c, lw=1.8, label=lab)
ax.plot([2007], [S.loc[2007, 'leather_ne_share_pct']], 'o', mfc='white', mec=ORANGE, ms=5, zorder=5)
ax.set_ylabel('Nonemployer firms, % of nonemployer firms\nplus employer establishments'); ax.set_xticks(range(2004, 2024, 4)); ax.set_ylim(40, 90); ax.legend(fontsize=7, loc='center right')
ax.set_title('A  By sector', loc='left', fontsize=9, weight='bold')
ax = axs[1]; vlines(ax)
for k, lab, c in [('3161', 'Tanning and finishing (3161)', GREEN), ('3162', 'Footwear (3162)', BLUE), ('3169', 'Other leather goods, luggage, handbags (3169)', ORANGE)]:
    t = SG[SG.naics == k].dropna(subset=['emp_est']); ax.plot(t.year, t.ne_share_pct, color=c, lw=1.8, label=lab)
ax.set_xticks(range(2004, 2024, 4)); ax.set_ylim(40, 95); ax.legend(fontsize=7, loc='lower right'); ax.set_title('B  Within NAICS 316', loc='left', fontsize=9, weight='bold')
fig.tight_layout(); save(fig, 'fig2_nonemployer_share', FIG)

# ---- Figure 3: size distribution
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.5))
ax = axs[0]; yrs = [2004, 2013, 2023]; cols = [LIGHT, BLUE, ORANGE]; w = 0.26; x = np.arange(len(SIZE_LAB))
for i, (y, c) in enumerate(zip(yrs, cols)):
    ax.bar(x + (i - 1) * w, [Z.loc[y, f'sh_{l}'] for l in SIZE_LAB], w, color=c, label=str(y))
ax.set_xticks(x); ax.set_xticklabels(SIZE_LAB, fontsize=7.5); ax.set_xlabel('Employees at the establishment'); ax.set_ylabel('% of employer establishments'); ax.legend(fontsize=7.5)
ax.set_title('A  Share by size class', loc='left', fontsize=9, weight='bold')
ax = axs[1]; ch = [Z.loc[2023, f'n_{l}'] - Z.loc[2004, f'n_{l}'] for l in SIZE_LAB]
ax.bar(x, ch, color=[ORANGE if v < 0 else BLUE for v in ch]); ax.axhline(0, color=MUTED, lw=0.6)
ax.set_xticks(x); ax.set_xticklabels(SIZE_LAB, fontsize=7.5); ax.set_xlabel('Employees at the establishment'); ax.set_ylabel('Change in establishments, 2004 to 2023')
for xi, v in zip(x, ch): ax.text(xi, v - 6, f'{v:+.0f}', ha='center', va='top', fontsize=7, color=INK)
ax.set_ylim(min(ch) - 40, 10); ax.set_title('B  Net change in counts', loc='left', fontsize=9, weight='bold')
fig.text(0.01, -0.02, '*1-4 in 2004-2016 files; "under 5" from 2017 files (including establishments reporting no March employment). 250+ derived as total minus smaller classes.', fontsize=6.5, color=MUTED)
fig.tight_layout(); save(fig, 'fig3_size_distribution', FIG)
print('figs ok')
