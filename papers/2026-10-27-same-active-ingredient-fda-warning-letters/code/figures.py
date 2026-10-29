"""Figures 1-3 (PNG 300 dpi + PDF)."""
import json
import numpy as np, pandas as pd
import matplotlib.dates as mdates
from style import plt, save, INK, MUTED, GRID, LIGHT
from common import RES, FIG, CODE_LABEL

CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#6250d6']  # validated categorical order (light mode)
ORDER = ['Telehealth platform', 'Clinic / med spa', 'Online pharmacy / marketplace', 'Research-chemical seller',
         'Compounder (503A/503B)', 'API supplier / other manufacturer']
T = json.load(open(f'{RES}/timeline.json')); R = json.load(open(f'{RES}/recalls.json'))

# ---------- Figure 1: timeline ----------
months = pd.period_range('2023-10', '2026-09', freq='M')
M = pd.DataFrame(T['by_month_group']).T.reindex(months.astype(str), fill_value=0)[ORDER]
fig, (a, b) = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True, gridspec_kw=dict(height_ratios=[2.2, 1], hspace=0.12))
x = months.to_timestamp() + pd.Timedelta(days=14)
bottom = np.zeros(len(M))
for g, col in zip(ORDER, CAT):
    a.bar(x, M[g].values, bottom=bottom, width=24, color=col, label=g, edgecolor='white', linewidth=0.6)
    bottom += M[g].values
for d, lab in T['events']:
    for ax in (a, b):
        ax.axvline(pd.Timestamp(d), color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=0)
for k, (d, lab) in enumerate(T['events'], 1):
    if k == 3: continue
    a.text(pd.Timestamp(d), 59, '3,4' if k == 4 else str(k), fontsize=6.5, color=MUTED, ha='center', va='top', bbox=dict(fc='white', ec='none', pad=0.6))
a.set_ylabel('Warning letters per month'); a.set_ylim(0, 60)
a.legend(fontsize=7, ncol=1, loc='upper left', bbox_to_anchor=(0.0, 0.88), frameon=True, facecolor='white', edgecolor='none', framealpha=1)
a.text(0, 1.02, 'A  Warning letters by issue month and seller type (n = 154)', transform=a.transAxes, fontsize=8.5, color=INK, weight='bold')
q = pd.period_range('2023Q4', '2026Q3', freq='Q')
tot = pd.Series(R['by_quarter']).reindex(q.astype(str), fill_value=0)
ste = pd.Series(R['by_quarter_sterility']).reindex(q.astype(str), fill_value=0)
xq = q.to_timestamp() + pd.Timedelta(days=45)
b.bar(xq, ste.values, width=70, color=CAT[0], label='Lack of sterility assurance', edgecolor='white', linewidth=0.6)
b.bar(xq, (tot - ste).values, bottom=ste.values, width=70, color=LIGHT, label='Other reason', edgecolor='white', linewidth=0.6)
b.set_ylabel('Recall records\nper quarter'); b.legend(fontsize=7, loc='upper left', frameon=True, facecolor='white', edgecolor='none', framealpha=1)
b.text(0, 1.04, 'B  openFDA recall records naming semaglutide, tirzepatide or retatrutide', transform=b.transAxes, fontsize=8.5, color=INK, weight='bold')
b.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); b.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
b.set_xlim(pd.Timestamp('2023-09-15'), pd.Timestamp('2026-10-15'))
save(fig, 'fig1_timeline', FIG)

# ---------- Figure 2: heat map seller group x code ----------
B = pd.read_csv(f'{RES}/prevalence_by_seller.csv')
codes = ['V_unapproved', 'V_misbrand_502f1', 'V_rx_503b1', 'V_misbrand_502a', 'V_misbrand_502bb', 'V_cgmp', 'V_sterility', 'V_503A_conditions', 'V_503B_conditions',
         'V_other_peptide', 'C_sameness', 'C_generic', 'C_fda_approved', 'C_firm_branded', 'C_brand_names', 'C_research_disguise', 'C_no_rx']
P = B.pivot(index='code', columns='group', values='pct').loc[codes, ORDER]
Nn = B.groupby('group').N.first().reindex(ORDER)
K = B.pivot(index='code', columns='group', values='n').loc[codes, ORDER]
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('blue', ['#f7f9fc', '#cde2fb', '#86b6ef', '#3987e5', '#1c5cab', '#0d366b'])
fig, ax = plt.subplots(figsize=(7.2, 6.2))
ax.imshow(P.values, cmap=cmap, vmin=0, vmax=1, aspect='auto')
for i in range(P.shape[0]):
    for j in range(P.shape[1]):
        v = P.values[i, j]
        ax.text(j, i, f'{100*v:.0f}', ha='center', va='center', fontsize=7.2, color='white' if v > 0.55 else INK)
ax.set_xticks(range(len(ORDER))); SHORT = {'Telehealth platform': 'Telehealth\nplatform', 'Clinic / med spa': 'Clinic /\nmed spa', 'Online pharmacy / marketplace': 'Online\npharmacy', 'Research-chemical seller': 'Research-\nchemical', 'Compounder (503A/503B)': 'Compounder\n503A/503B', 'API supplier / other manufacturer': 'API / other\nmanufacturer'}
ax.set_xticklabels([f'{SHORT[g]}\n(n = {Nn[g]})' for g in ORDER], fontsize=7, rotation=0)
ax.set_yticks(range(len(codes))); ax.set_yticklabels([CODE_LABEL[c] for c in codes], fontsize=7.2)
ax.tick_params(axis='x', labeltop=True, labelbottom=False, length=0); ax.tick_params(axis='y', length=0)
ax.grid(False)
for s in ax.spines.values(): s.set_visible(False)
ax.axhline(9.5, color=INK, lw=0.8)
ax.set_xticks(np.arange(-.5, len(ORDER)), minor=True); ax.set_yticks(np.arange(-.5, len(codes)), minor=True)
ax.grid(which='minor', color='white', lw=1.2); ax.tick_params(which='minor', length=0)
plt.setp(ax.get_xticklabels(), ha='center')
fig.text(0.01, 0.04, 'Cells: % of letters to each seller type in which FDA cited the violation (top block) or the claim/feature (bottom block).', fontsize=7, color=MUTED)
save(fig, 'fig2_heatmap', FIG)

# ---------- Figure 3: waves + agreement ----------
W = pd.read_csv(f'{RES}/waves.csv'); A = pd.read_csv(f'{RES}/agreement.csv')
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 4.6), gridspec_kw=dict(width_ratios=[0.9, 1], wspace=1.05))
wc = ['C_sameness', 'C_brand_names', 'C_generic', 'C_fda_approved', 'C_firm_branded']
waves = ['Sep 2025', 'Feb 2026', 'Jun 2026']
y = np.arange(len(wc))
for k, (w, col) in enumerate(zip(waves, CAT[:3])):
    s = W[W.wave == w].set_index('code').loc[wc]
    a.barh(y + (k - 1) * 0.26, 100 * s.pct, height=0.24, color=col, label=f"{w} (n = {int(s.N.iloc[0])})", edgecolor='white', linewidth=0.5)
a.set_yticks(y); a.set_yticklabels([CODE_LABEL[c].replace(' claim', '') for c in wc], fontsize=7.2); a.invert_yaxis()
a.set_xlim(0, 100); a.set_xlabel('% of letters in batch'); a.legend(fontsize=6.8, loc='upper center', bbox_to_anchor=(0.4, -0.13), ncol=1)
fig.text(0.01, 0.97, 'A  Claims FDA cited, by letter batch', fontsize=8.5, weight='bold', color=INK)
a.set_title('')
ac = A[~A.variable.isin(['eligible', 'seller_type'])].copy()
ac = pd.concat([A[A.variable.isin(['eligible', 'seller_type'])], ac])
ac['lab'] = ac.variable.map(lambda v: {'eligible': 'Eligibility', 'seller_type': 'Seller type'}.get(v, CODE_LABEL.get(v, v)))
ac['k'] = ac.kappa.fillna(np.nan)
ac = ac.iloc[::-1]
yy = np.arange(len(ac))
b.hlines(yy, 0, ac.k.fillna(0), color=GRID, lw=1)
b.plot(ac.k, yy, 'o', ms=4.5, color=CAT[0], label="Cohen's κ")
b.plot(ac.pct_agree, yy, 'D', ms=3.6, color=CAT[1], label='% agreement / 100')
b.set_yticks(yy); b.set_yticklabels(ac.lab.str.replace('False/misleading compounded-drug advertising', 'Compounded-drug advertising').str.replace('"Research use" / not for human consumption', '"Research use" labelling'), fontsize=6.3); b.set_xlim(-0.02, 1.05); b.axvline(0.8, color=MUTED, lw=0.6, ls=':')
b.set_xlabel('Agreement, rules vs reader (before adjudication)'); b.legend(fontsize=6.8, loc='upper center', bbox_to_anchor=(0.5, -0.13), ncol=2)
fig.text(0.47, 0.97, 'B  Inter-pass agreement (rules vs reader)', fontsize=8.5, weight='bold', color=INK)
save(fig, 'fig3_waves_agreement', FIG)
print('ok')
