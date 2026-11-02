"""Update to 2023: NHANES body weights through 2021-2023 and FAO food supply through 2023 (new methodology from 2010)."""
import numpy as np, pandas as pd
from common import *

fa = pd.read_csv(f'{DER}/fa.csv', index_col=0); P = pd.read_csv(f'{DER}/bw_points.csv'); A, E = load_nhanes(); Dt = load_diet()
epa = load_epa(); lafa = load_lafa()
YRS = np.arange(1974, 2024)
pts = {s: list(zip(g.t, g.bw)) for s, g in P.groupby('series')}
out = {'years': YRS.tolist(), 'note_extrapolation': 'BW after 2022.5 extrapolated with the 2017.5-2022.5 slope (0.5 y)'}
FAs = {'spliced': fa.loc[YRS, 'spliced'].values,
       'fbs_from_2010': np.where(YRS >= 2010, fa.reindex(YRS)['fbs'].values, fa.reindex(YRS)['fbsh'].values)}
ser = {}
for bwname in ('nchs', 'nchs_20p'):
    r = intake(pts[bwname], YRS, NOMINAL, F0_HALL)
    for fan, FA in FAs.items():
        w = FA - r['I']; fr = w / FA
        ser[f'{bwname}|{fan}'] = {'I': r['I'], 'bw': r['bw'], 'FA': FA, 'waste': w, 'frac': 100 * fr}
def lin(y, x):
    b = np.polyfit(x, y, 1); return float(b[0])
summ = {}
for k, s in ser.items():
    idx = lambda y: list(YRS).index(y)
    d = {f'{q}_{y}': float(s[q][idx(y)]) for q in ('I', 'FA', 'waste', 'frac') for y in (1974, 2003, 2005, 2010, 2013, 2019, 2022, 2023)}
    m = (YRS >= 1974) & (YRS <= 2003); m2 = YRS >= 2003
    d['frac_slope_1974_2003_pp_per_yr'] = lin(s['frac'][m], YRS[m]); d['frac_slope_2003_2023_pp_per_yr'] = lin(s['frac'][m2], YRS[m2])
    d['waste_slope_1974_2003'] = lin(s['waste'][m], YRS[m]); d['waste_slope_2003_2023'] = lin(s['waste'][m2], YRS[m2])
    d['frac_max_year'] = int(YRS[np.argmax(s['frac'])]); d['frac_max'] = float(s['frac'].max())
    d['bw_2003'] = float(s['bw'][idx(2003)]); d['bw_2023'] = float(s['bw'][idx(2023)])
    summ[k] = d
out['summary'] = summ
out['series'] = {k: {q: np.round(v, 2) for q, v in s.items()} for k, s in ser.items()}

# Monte Carlo: change in the wasted share 2003 -> 2023 (spliced FAO, NCHS weights)
rng = np.random.default_rng(20091124); N = 100_000
D = {k: rng.normal(m, s, N) for k, (m, s) in TABLE1.items()}
bad = (D['C'] <= 0) | (D['beta'] >= 0.95)
while bad.any():
    for k in ('C', 'beta'): D[k][bad] = rng.normal(*TABLE1[k], bad.sum())
    bad = (D['C'] <= 0) | (D['beta'] >= 0.95)
bw, slope = bw_path(pts['nchs'], YRS); bw0 = bw[0]
a = D['C'] / F0_HALL
cdyn = (D['etaF'] + NOMINAL['rhoF'] + a * (D['etaFFM'] + NOMINAL['rhoFFM'])) / ((1 + a) * (1 - D['beta']))
csta = ((D['gF'] + a * D['gFFM']) / (1 + a) + D['delta']) / (1 - D['beta'])
Imc = D['I0'][:, None] + cdyn[:, None] * slope[None, :] / 365.25 + csta[:, None] * (bw - bw0)[None, :]
q = lambda x: [float(np.percentile(x, 2.5)), float(np.median(x)), float(np.percentile(x, 97.5))]
mc = {}
for fan, FA in FAs.items():
    W = FA[None, :] - Imc; Fr = 100 * W / FA[None, :]
    i03, i23, i74 = list(YRS).index(2003), list(YRS).index(2023), 0
    mc[fan] = {'frac_2023': q(Fr[:, i23]), 'frac_change_2003_2023_pp': q(Fr[:, i23] - Fr[:, i03]), 'P(frac_2023 > frac_2003)': float(np.mean(Fr[:, i23] > Fr[:, i03])),
               'waste_2023': q(W[:, i23]), 'waste_change_2003_2023': q(W[:, i23] - W[:, i03]), 'P(waste_2023 > waste_2003)': float(np.mean(W[:, i23] > W[:, i03])),
               'frac_change_1974_2003_pp': q(Fr[:, i03] - Fr[:, i74]),
               'band_frac': {'lo': np.percentile(Fr, 2.5, axis=0).round(2), 'hi': np.percentile(Fr, 97.5, axis=0).round(2)},
               'band_waste': {'lo': np.percentile(W, 2.5, axis=0).round(1), 'hi': np.percentile(W, 97.5, axis=0).round(1)}}
out['monte_carlo'] = mc

# per-capita (all-ages) adjustment with cycle-specific ratios from 1999-2000 onward
Er = E.set_index('cycle'); ratio_pts = []
mid = {'1999-2000': 1999.5, '2001-2002': 2001.5, '2003-2004': 2003.5, '2005-2006': 2005.5, '2007-2008': 2007.5, '2009-2010': 2009.5,
       '2011-2012': 2011.5, '2013-2014': 2013.5, '2015-2016': 2015.5, '2017-2018': 2017.5, '2021-2023': 2022.5}
for c, t in mid.items(): ratio_pts.append((t, Er.loc[c, 'eer_sed_all'] / Er.loc[c, 'eer_sed_2074']))
rt = np.interp(YRS, *zip(*ratio_pts))
s = ser['nchs|spliced']; Ipc = s['I'] * rt; wpc = s['FA'] - Ipc
out['per_capita_adjusted'] = {'ratio_by_cycle': {c: round(Er.loc[c, 'eer_sed_all'] / Er.loc[c, 'eer_sed_2074'], 4) for c in mid},
                              'frac_1974': float(100 * wpc[0] / s['FA'][0]), 'frac_2003': float(100 * wpc[29] / s['FA'][29]), 'frac_2023': float(100 * wpc[-1] / s['FA'][-1]),
                              'waste_2003': float(wpc[29]), 'waste_2023': float(wpc[-1]), 'frac_series': np.round(100 * wpc / s['FA'], 2)}

# self-reported intake (24-h recall, day 1, adults 20-74) vs model intake
sr = []
for c, t in mid.items():
    sub = Dt[Dt.cycle == c]
    m = sub[sub.sex == 1].kcal_mean.iloc[0]; w = sub[sub.sex == 2].kcal_mean.iloc[0]
    sr.append({'cycle': c, 't': t, 'men': m, 'women': w, 'pooled_pw0.525': (1 - P_W) * m + P_W * w,
               'model_I': float(np.interp(t, YRS, s['I']))})
SR = pd.DataFrame(sr); SR['ratio_selfreport_to_model'] = SR['pooled_pw0.525'] / SR['model_I']
out['self_report'] = SR.round(2).to_dict('records')
out['self_report_mmwr_1971_74'] = {'men': 2450, 'women': 1542, 'pooled_pw0.525': (1 - P_W) * 2450 + P_W * 1542, 'note': 'age-adjusted, Wright et al. (2004)'}
out['self_report_mmwr_1999_2000'] = {'men': 2618, 'women': 1877, 'pooled_pw0.525': (1 - P_W) * 2618 + P_W * 1877}

# EPA municipal food waste per capita (consistent series 1990-2017; method change in 2018)
pc = {}
for y in epa.index:
    pop = fa.loc[y, 'pop_1000'] * 1e3 if y in fa.index else np.nan
    pc[int(y)] = {'gen_1000_tons': float(epa.loc[y]), 'kg_per_cap_yr': float(epa.loc[y] * 1e3 * 907.185 / pop) if pop == pop else None}
out['epa_msw'] = pc
# USDA LAFA implied waste share (FAO old methodology minus LAFA), 1974-2010
us = {int(y): float(100 * (fa.loc[y, 'fbsh'] - lafa.loc[y]) / fa.loc[y, 'fbsh']) for y in range(1974, 2011)}
out['usda_frac'] = us
# sensitivities of the 2003->2023 change that the parameter Monte Carlo omits
sp = ser['nchs|spliced']; i03, i22, i23 = list(YRS).index(2003), list(YRS).index(2022), list(YRS).index(2023)
imin = int(np.argmin(sp['frac'][i03:])) + i03
sens = {'frac_min_after_2003': float(sp['frac'][imin]), 'frac_min_year': int(YRS[imin]),
        'change_2003_2022_pp': float(sp['frac'][i22] - sp['frac'][i03]), 'change_2003_2023_pp': float(sp['frac'][i23] - sp['frac'][i03]),
        'rise_min_to_2023_pp': float(sp['frac'][i23] - sp['frac'][imin])}
ovv = (fa['fbs'] - fa['fbsh']).dropna()
for lab, off in (('offset_2010_only', ovv.loc[2010]), ('offset_2013_only', ovv.loc[2013])):
    FAx = FAs['spliced'].copy(); FAx[YRS >= 2014] = fa.loc[YRS[YRS >= 2014], 'fbs'].values - off
    fr = 100 * (FAx - sp['I']) / FAx; sens[f'change_2003_2023_pp|{lab}'] = float(fr[i23] - fr[i03])
for dw in (-0.35, 0.35):
    p2 = [(t, b + (dw if t == 2022.5 else 0.0)) for t, b in pts['nchs']]
    Ix = intake(p2, YRS, NOMINAL, F0_HALL)['I']; fr = 100 * (FAs['spliced'] - Ix) / FAs['spliced']
    sens[f'change_2003_2023_pp|bw2021_23{dw:+.2f}kg'] = float(fr[i23] - fr[i03])
p3 = [(t, b) for t, b in pts['nchs']]
Ix = intake(p3, YRS, NOMINAL, F0_HALL)['I']; Ix2 = Ix.copy(); Ix2[i23] = float(np.interp(2022.5, YRS, Ix))
fr = 100 * (FAs['spliced'] - Ix2) / FAs['spliced']; sens['change_2003_2023_pp|no_extrapolation'] = float(fr[i23] - fr[i03])
X = YRS[YRS >= 2003]; yv = sp['frac'][YRS >= 2003]; b = np.polyfit(X, yv, 1); res = yv - np.polyval(b, X)
sens['trend_2003_2023_ols_se_naive'] = float(np.sqrt(res.var(ddof=2) / ((X - X.mean()) ** 2).sum()))
out['sensitivity_2003_2023'] = sens
fao = load_fao()['FBSH']
names = {'2901': 'Grand total', '2909': 'Sugar & sweeteners', '2941': 'Animal products', '2914': 'Vegetable oils', '2905': 'Cereals', '2924': 'Alcoholic beverages'}
out['fbsh_2005_2011'] = {v: {'2005': float(fao.loc[2005, k]), '2011': float(fao.loc[2011, k]), 'change': float(fao.loc[2011, k] - fao.loc[2005, k])} for k, v in names.items()}
dump(out, 'update.json')
pd.set_option('display.width', 250)
print(pd.DataFrame(summ).T.round(2).to_string())
for k, v in mc.items(): print(k, {kk: vv for kk, vv in v.items() if not kk.startswith('band')})
print(out['per_capita_adjusted']['frac_1974'], out['per_capita_adjusted']['frac_2003'], out['per_capita_adjusted']['frac_2023'], out['per_capita_adjusted']['ratio_by_cycle'])
print(SR.round(1).to_string()); print(pc)
