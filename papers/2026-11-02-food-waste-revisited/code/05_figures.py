"""Figures 1-3 (PNG 300 dpi + PDF)."""
import numpy as np, pandas as pd
from common import *
from style import *

R = load('reproduction.json'); B = load('robustness.json'); U = load('update.json')
P = pd.read_csv(f'{DER}/bw_points.csv'); dig = load_digitized(); lafa = load_lafa(); fa = pd.read_csv(f'{DER}/fa.csv', index_col=0)
Y = np.array(R['years']); YU = np.array(U['years'])

# ---------- Figure 1: reproduction 1974-2003 ----------
fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.4))
a = ax[0]
for s, col, mk, lab in (('hall_digitized', ORANGE, '^', 'Original Fig. 1A (digitized)'), ('nchs', BLUE, 'o', 'NCHS public data (this study)')):
    g = P[(P.series == s) & (P.t <= 2004)]
    a.plot(g.t, g.bw, color=col, lw=1.6, marker=mk, ms=6, mfc='white', mew=1.6, label=lab)
a.set_title('A  Mean adult body weight', loc='left', fontsize=9.5, weight='bold'); a.set_ylabel('kg'); a.legend(fontsize=7.5, loc='upper left')
a = ax[1]
m = R['main']['nchs']['series']; band = R['monte_carlo']['nchs']['band_I']
a.plot(Y, m['FA'], color=INK, lw=1.6, label='FAO food supply (FBSH, current release)')
a.fill_between(Y, band['lo'], band['hi'], color=BLUE, alpha=0.15, lw=0)
a.plot(Y, m['I'], color=BLUE, lw=2, label='Model intake, reproduced (95% MC band)')
a.plot(lafa.loc[1974:2003].index, lafa.loc[1974:2003].values, color=GREEN, lw=1.4, ls='--', label='USDA loss-adjusted availability')
d = dig[dig.panel == 'B']; a.plot(d.year, d.value, ls='none', marker='^', ms=6, mfc='white', mec=ORANGE, mew=1.6, label='Original intake curve (digitized)')
a.set_title('B  Supply and intake', loc='left', fontsize=9.5, weight='bold'); a.set_ylabel('kcal per person per day'); a.legend(fontsize=6.8, loc='upper left', ncol=1)
a.set_ylim(1800, 5000)
a = ax[2]
bw = R['monte_carlo']['nchs']['band_waste']
a.fill_between(Y, bw['lo'], bw['hi'], color=BLUE, alpha=0.15, lw=0)
a.plot(Y, m['waste'], color=BLUE, lw=2, label='Reproduced (NCHS weights)')
a.plot(Y, R['main']['hall_digitized']['series']['waste'], color=BLUE, lw=1.2, ls=':', label='Reproduced (digitized weights)')
d = dig[dig.panel == 'C']; a.plot(d.year, d.value, ls='none', marker='^', ms=6, mfc='white', mec=ORANGE, mew=1.6, label='Original Fig. 1C (digitized)')
a.set_title('C  Food waste = supply − intake', loc='left', fontsize=9.5, weight='bold'); a.set_ylabel('kcal per person per day'); a.legend(fontsize=7.5, loc='upper left')
for x in ax: x.set_xlim(1972, 2005)
fig.tight_layout(); save(fig, 'fig1_reproduction', FIG)

# ---------- Figure 2: robustness (share of supply wasted, 1974 and 2003) ----------
G = pd.DataFrame(B['grid'])
short = ['Baseline (NCHS weights, current FAO)', 'Weights digitized from original', 'γF = 3.6 (Table 1)', 'F0 re-derived (19.6 kg)', 'Weights: adults 20+, all',
         'Weights: survey female share', 'Survey points at end years', 'I0 = IOM sedentary (2,133)', 'I0 = IOM low-active (2,361)', 'I0 = self-reported (1,973)',
         'Activity coefficient −10% by 2003', 'Activity coefficient +10% by 2003', 'Per-capita intake (children)', 'IOM requirement, sedentary', 'IOM requirement, low-active',
         'Per-capita + low-active I0']
G['short'] = short
fig, a = plt.subplots(figsize=(7.2, 5.2))
yy = np.arange(len(G))[::-1]
for y, (_, r) in zip(yy, G.iterrows()):
    a.plot([r.frac_1974, r.frac_2003], [y, y], color=LIGHT, lw=2.5, zorder=1)
a.scatter(G.frac_1974, yy, s=42, color=MUTED, zorder=2, label='1974', edgecolor='white', linewidth=1)
a.scatter(G.frac_2003, yy, s=42, color=BLUE, zorder=3, label='2003', edgecolor='white', linewidth=1)
for y, (_, r) in zip(yy, G.iterrows()):
    a.text(r.frac_2003 + 0.6, y, f'+{r.change_pp:.1f} pp', va='center', fontsize=7.2, color=MUTED)
a.axvspan(30, 40, color=ORANGE, alpha=0.06, lw=0); a.text(30.2, len(G) - 0.45, 'original: ~30% → almost 40%', fontsize=7.5, color=ORANGE)
a.set_yticks(yy); a.set_yticklabels(G.short, fontsize=7.8); a.set_xlabel('Share of FAO food supply wasted (%)')
a.set_xlim(20, 48); a.set_ylim(-0.7, len(G) + 0.4); a.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), fontsize=8); a.grid(axis='y', visible=False)
fig.tight_layout(); save(fig, 'fig2_robustness', FIG)

# ---------- Figure 3: update to 2023 ----------
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
a = ax[0]; s = U['series']['nchs|spliced']; s2 = U['series']['nchs|fbs_from_2010']
a.plot(YU, fa.loc[YU, 'fbsh'], color=INK, lw=1.6, label='FAO supply, old methodology (to 2013)')
a.plot(YU[YU >= 2010], fa.loc[2010:2023, 'fbs'], color=INK, lw=1.2, ls='--', label='FAO supply, new methodology (2010–)')
a.plot(YU, s['I'], color=BLUE, lw=2, label='Model intake (NCHS weights)')
SR = pd.DataFrame(U['self_report'])
a.plot(SR.t, SR['pooled_pw0.525'], color=GREEN, marker='o', ms=5, lw=1.2, mfc='white', mew=1.4, label='Self-reported intake, NHANES 24-h recall')
a.set_ylim(1800, 4100); a.set_ylabel('kcal per person per day'); a.legend(fontsize=7, loc='center left', bbox_to_anchor=(0, 0.40))
a.set_title('A  Supply, modelled and reported intake', loc='left', fontsize=9.5, weight='bold')
a = ax[1]; bd = U['monte_carlo']['spliced']['band_frac']
a.fill_between(YU, bd['lo'], bd['hi'], color=BLUE, alpha=0.13, lw=0)
a.plot(YU, s['frac'], color=BLUE, lw=2, label='Spliced FAO series (95% parameter MC band)')
a.plot(YU, s2['frac'], color=BLUE, lw=1.2, ls='--', label='New FAO methodology from 2010, unspliced')
a.plot(YU, U['per_capita_adjusted']['frac_series'], color=ORANGE, lw=1.4, label='Per-capita intake (children adjusted)')
uf = U['usda_frac']; a.plot([int(k) for k in uf], list(uf.values()), color=GREEN, lw=1.2, ls=':', label='USDA LAFA-implied share (to 2010)')
a.axvline(2003, color=MUTED, lw=0.8, ls=':'); a.text(2003.5, 22.5, 'end of original series', fontsize=7, color=MUTED)
a.set_ylabel('Share of supply wasted (%)'); a.set_ylim(20, 56); a.legend(fontsize=6.8, loc='upper left', ncol=2)
a.set_title('B  Share of food supply wasted, 1974–2023', loc='left', fontsize=9.5, weight='bold')
for x in ax: x.set_xlim(1972, 2025)
fig.tight_layout(); save(fig, 'fig3_update', FIG)
print('figures done')
