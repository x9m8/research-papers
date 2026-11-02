"""Reproduce Hall et al. (2009): intake underlying the rise in adult body weight, food waste = FAO supply - intake, 1974-2003,
with the published nominal parameters and a Monte Carlo over Table 1. Two body-weight inputs: the values digitized from the
original Figure 1A, and public NCHS values (Ogden et al. 2004 for NHANES I-III; NHANES continuous microdata thereafter)."""
import numpy as np, pandas as pd
from common import *

fa = pd.read_csv(f'{DER}/fa.csv', index_col=0); P = pd.read_csv(f'{DER}/bw_points.csv')
lafa = load_lafa(); epa = load_epa(); eia = load_eia(); dig = load_digitized()
YRS = np.arange(1974, 2004)
pts = {s: list(zip(g.t, g.bw)) for s, g in P.groupby('series')}
out = {'years': YRS.tolist()}


def run(series, p=NOMINAL, F0=F0_HALL, fa_col='fbsh', years=YRS, base=1974.0):
    r = intake(pts[series], years, p, F0, base_year=base)
    FA = fa.loc[years, fa_col].values
    w = FA - r['I']
    return dict(I=r['I'], dI=r['dI'], dyn=r['dyn'], sta=r['sta'], bw=r['bw'], bw0=r['bw0'], slope=r['slope'], FA=FA, waste=w, frac=w / FA)


def headline(R, years=YRS, y0=1974, y1=2003, pop_col='pop_1000'):
    i0, i1 = list(years).index(y0), list(years).index(y1)
    pop = fa.loc[y1, 'pop_1000'] * 1e3
    tot = R['waste'][i1] * 365.25 * pop
    bbl = tot * FOSSIL_PER_FOOD / (KCAL_PER_BTU * BTU_PER_BBL)
    oil = eia.loc[y1] * 1e3 * 365.25 if y1 in eia.index else np.nan
    return {'bw_1974': R['bw'][i0], 'bw_2003': R['bw'][i1], 'dBW': R['bw'][i1] - R['bw0'], 'mean_slope_kg_per_day': (R['bw'][i1] - R['bw0']) / ((y1 - y0) * 365.25),
            'slope_2003_kg_per_day': R['slope'][i1] / 365.25, 'dyn_term_2003': R['dyn'][i1], 'static_term_2003': R['sta'][i1],
            'I_1974': R['I'][i0], 'I_2003': R['I'][i1], 'FA_1974': R['FA'][i0], 'FA_2003': R['FA'][i1],
            'waste_1974': R['waste'][i0], 'waste_2003': R['waste'][i1], 'waste_increase_pct': 100 * (R['waste'][i1] / R['waste'][i0] - 1),
            'frac_1974': 100 * R['frac'][i0], 'frac_2003': 100 * R['frac'][i1],
            'waste_peak_year': int(years[np.argmax(R['waste'])]), 'waste_peak': R['waste'].max(), 'frac_peak': 100 * R['frac'].max(),
            'total_waste_trillion_kcal_per_yr': tot / 1e12, 'oil_million_bbl': bbl / 1e6, 'oil_share_pct': 100 * bbl / oil,
            'freshwater_share_pct': 100 * AG_SHARE_WATER * R['frac'][i1]}


main = {}
for s in ('hall_digitized', 'nchs'):
    R = run(s); main[s] = {'headline': headline(R), 'series': {k: np.round(v, 2) for k, v in R.items() if isinstance(v, np.ndarray)}}
out['main'] = main

# comparison with digitized published curves
dI = dig[dig.panel == 'B'].set_index('year').value; dW = dig[dig.panel == 'C'].set_index('year').value
comp = []
for s in ('hall_digitized', 'nchs'):
    ser = main[s]['series']
    for y, v in dI.items(): comp.append({'bw_input': s, 'quantity': 'intake', 'year': int(y), 'published_digitized': v, 'reproduced': ser['I'][list(YRS).index(int(y))]})
    for y, v in dW.items(): comp.append({'bw_input': s, 'quantity': 'waste', 'year': int(y), 'published_digitized': v, 'reproduced': ser['waste'][list(YRS).index(int(y))]})
C = pd.DataFrame(comp); C['diff'] = C.reproduced - C.published_digitized
out['curve_comparison'] = C.round(1).to_dict('records')
out['curve_comparison_summary'] = C.groupby(['bw_input', 'quantity'])['diff'].agg(['mean', 'min', 'max']).round(1).reset_index().to_dict('records')

# Monte Carlo over Table 1 (seeded), both BW inputs
rng = np.random.default_rng(20091124)
N = 100_000
def draws(n):
    d = {k: rng.normal(m, s, n) for k, (m, s) in TABLE1.items()}
    bad = (d['C'] <= 0) | (d['beta'] >= 0.95)
    while bad.any():
        for k in ('C', 'beta'):
            m, s = TABLE1[k]; d[k][bad] = rng.normal(m, s, bad.sum())
        bad = (d['C'] <= 0) | (d['beta'] >= 0.95)
    d['rhoF'] = np.full(n, NOMINAL['rhoF']); d['rhoFFM'] = np.full(n, NOMINAL['rhoFFM'])
    return d
mc = {}
D = draws(N)
for s in ('hall_digitized', 'nchs'):
    bw, slope = bw_path(pts[s], YRS); bw0 = float(np.interp(1974.0, *zip(*pts[s])))
    a = D['C'] / F0_HALL
    cdyn = (D['etaF'] + D['rhoF'] + a * (D['etaFFM'] + D['rhoFFM'])) / ((1 + a) * (1 - D['beta']))
    csta = ((D['gF'] + a * D['gFFM']) / (1 + a) + D['delta']) / (1 - D['beta'])
    I = D['I0'][:, None] + cdyn[:, None] * slope[None, :] / 365.25 + csta[:, None] * (bw - bw0)[None, :]
    FA = fa.loc[YRS, 'fbsh'].values[None, :]
    W = FA - I; Fr = W / FA
    q = lambda x: [float(np.percentile(x, 2.5)), float(np.median(x)), float(np.percentile(x, 97.5))]
    i3 = list(YRS).index(2003)
    mc[s] = {'I_2003': q(I[:, i3]), 'dI_2003': q(I[:, i3] - D['I0']), 'waste_1974': q(W[:, 0]), 'waste_2003': q(W[:, i3]),
             'frac_1974': q(100 * Fr[:, 0]), 'frac_2003': q(100 * Fr[:, i3]), 'waste_change_kcal': q(W[:, i3] - W[:, 0]),
             'waste_increase_pct': q(100 * (W[:, i3] / W[:, 0] - 1)), 'frac_change_pp': q(100 * (Fr[:, i3] - Fr[:, 0])),
             'P(waste rose)': float(np.mean(W[:, i3] > W[:, 0])), 'P(frac rose)': float(np.mean(Fr[:, i3] > Fr[:, 0])),
             'C_static': q(csta), 'C_dyn': q(cdyn),
             'band_I': {'lo': np.percentile(I, 2.5, axis=0).round(1), 'hi': np.percentile(I, 97.5, axis=0).round(1)},
             'band_waste': {'lo': np.percentile(W, 2.5, axis=0).round(1), 'hi': np.percentile(W, 97.5, axis=0).round(1)}}
out['monte_carlo'] = {'n': N, 'seed': 20091124, 'truncation': 'C > 0 and beta < 0.95 (redrawn)', 'gF_mean': TABLE1['gF'][0], **mc}

# USDA comparison (LAFA, current vintage) and municipal solid food waste (EPA)
us = {}
for y in (1974, 2003):
    fav = fa.loc[y, 'fbsh']; la = lafa.loc[y]; usda_w = fav - la
    us[str(y)] = {'lafa': la, 'usda_waste': usda_w, 'usda_frac_pct': 100 * usda_w / fav,
                  'model_waste_nchs': main['nchs']['series']['waste'][list(YRS).index(y)],
                  'model_waste_dig': main['hall_digitized']['series']['waste'][list(YRS).index(y)]}
    for k in ('nchs', 'dig'):
        us[str(y)][f'usda_vs_model_{k}_pct'] = 100 * (usda_w / us[str(y)][f'model_waste_{k}'] - 1)
out['usda'] = us
out['usda_series'] = {int(y): float(v) for y, v in lafa.loc[1974:2010].items()}
msw = {}
for y in (2000, 2003, 2005):
    gen = np.interp(y, epa.index, epa.values) * 1e3 * 907.185   # short tons -> kg
    pc = gen / (fa.loc[y, 'pop_1000'] * 1e3)
    kcal_d = pc * 1000 * 1.9 / 365.25
    msw[str(y)] = {'kg_per_cap_yr': pc, 'kcal_per_cap_day_at_1.9': kcal_d,
                   'share_of_model_waste_nchs_pct': 100 * kcal_d / main['nchs']['series']['waste'][list(YRS).index(y)] if y <= 2003 else None}
out['msw'] = msw
dump(out, 'reproduction.json')
for s in main: print(s, {k: round(v, 3) for k, v in main[s]['headline'].items()})
print(pd.DataFrame(out['curve_comparison_summary']))
for s in mc: print(s, {k: [round(x, 1) for x in v] for k, v in mc[s].items() if isinstance(v, list)}, mc[s]['P(waste rose)'], mc[s]['P(frac rose)'])
print(us); print(msw)
