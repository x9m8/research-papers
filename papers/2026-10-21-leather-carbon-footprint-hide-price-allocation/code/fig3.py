import json, pandas as pd
from style import *
from common import RES, FIG, DATA
Y = pd.read_csv(f'{RES}/allocation_annual.csv'); C = pd.read_csv(f'{RES}/carbon_annual.csv'); P = json.load(open(f'{DATA}/params.json'))
fig, ax = plt.subplots(1, 2, figsize=(7.6, 3.1), gridspec_kw=dict(wspace=0.5))
a = ax[0]
a.plot(Y.year, Y.share * 100, color=BLUE, lw=1.8, label='US, this study (economic)')
for p in P['published']:
    m = 'o' if p['kind'] == 'economic' else 's'
    a.scatter(p['year'], p['value'] * 100, marker=m, s=28, facecolor=ORANGE if p['kind'] == 'economic' else 'white', edgecolor=ORANGE, lw=1.3, zorder=3)
lab = {'Roncevich et al. global weighted': (2025.2, 8.1, 'Roncevich et al.', 'right'), 'PEFCR Leather default (EU)': (2018.9, 3.5, 'PEFCR 3.5%'), 'Leather Working Group LCA': (2024.3, 2.05, 'LWG'), 'UNIDO guidelines': (2026.9, 1.5, 'UNIDO'),
       'US economic value (L&HCA-funded LCA)': (2026.0, 0.55, 'US LCA'), 'Italy, 2023 prices (Lunesu et al.)': (2021.0, 3.05, 'Italy 2023'),
       'Mekonnen & Hoekstra value fraction': (2010.0, 5.6, 'Mekonnen & Hoekstra', 'center'), 'US hide mass fraction': (2024.1, 4.8, 'US mass', 'right'), 'Italy mass (Lunesu et al.)': (2024.1, 5.88, 'Italy mass', 'right'),
       'Canada, 2006 US prices (Desjardins et al.)': (2007.0, 6.8, 'Canada 2006'), 'Canada mass (Desjardins et al.)': (2007.0, 6.2, 'Canada mass')}
for p in P['published']:
    x, y, t, *h = lab[p['label']]; a.text(x, y, t, fontsize=6.3, color=MUTED, va='center', ha=h[0] if h else 'left')
a.scatter([], [], marker='o', color=ORANGE, label='Published, economic'); a.scatter([], [], marker='s', facecolor='white', edgecolor=ORANGE, label='Published, mass')
a.set_ylim(0, 8.8); a.set_xlim(2001, 2031); a.set_xticks(range(2005, 2030, 5)); a.set_ylabel("Hide's share of emissions, %"); a.grid(axis='x', visible=False)
a.set_title('A  Published factors against the US series', loc='left', fontsize=9, color=INK); a.legend(fontsize=6.5, loc='lower left')
b = ax[1]
b.plot(C.year, C.kg_m2_mass, color=MUTED, lw=1.4, ls='--'); b.text(2016.3, C.kg_m2_mass.iloc[0] + 4, 'Mass, 4.8%', fontsize=6.8, color=MUTED)
b.plot(C.year, C.kg_m2_pefcr, color=ORANGE, lw=1.4, ls=':'); b.text(2017.3, C.kg_m2_pefcr.iloc[0] + 4, 'PEFCR 3.5%', fontsize=6.8, color=ORANGE)
b.plot(C.year, C.kg_m2_econ, color=BLUE, lw=2, marker='o', ms=3); b.text(2003, 40, 'Economic allocation,\nprice of the year', fontsize=6.8, color=BLUE)
b.set_ylim(0, 150); b.set_xlim(2001, 2025.5); b.set_ylabel('kg CO$_2$e per m$^2$ of leather\n(farm and feedlot share only)'); b.grid(axis='x', visible=False)
b.set_title('B  Same hide, different carbon bill', loc='left', fontsize=9, color=INK)
save(fig, 'fig3_factors_carbon', FIG); print('ok')
