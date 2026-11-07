"""Analysis 2: do egg price changes show up in restaurant menu-price inflation (US CPI, not seasonally adjusted)?
(A) Distributed-lag model, monthly log changes, 2005-2026:
    dy_t = a + sum_{k=0..K} b_k d_egg_{t-k} + sum_{k=0..3} g_k d_fah_{t-k} + sum_{k=0..3} w_k d_wage_{t-k} + sum_{k=1..3} r_k dy_{t-k} + month dummies + e
    HAC (Newey-West, 12 lags). Cumulative pass-through = sum of b_k.
(B) Reduced form: local projections of restaurant price changes on monthly HPAI layer losses, 2022-02 to 2026-09.
(C) Descriptive 12-month inflation comparisons at egg-price peaks."""
import json, numpy as np, pandas as pd, statsmodels.api as sm
from common import *
d = load_monthly(); L, n = monthly_layers()
dl_ = np.log(d).diff()           # monthly log change; NaN where a level is missing (Oct 2025 and the month after)
OUT = {'cpi_fafh': 'Food away from home (US)', 'cpi_fsr': 'Full-service meals (US)', 'cpi_lsr': 'Limited-service meals (US)', 'ny_fafh': 'Food away from home (NY-Newark-JC)'}
EGG = {'cpi_egg': 'CPI, eggs', 'avg_price_egg': 'Avg price, Grade A large', 'ppi_egg_large': 'PPI, large eggs'}
MONTH = pd.get_dummies(pd.Series(IDX.month, index=IDX), prefix='m', drop_first=True).astype(float)

def design(y, egg='cpi_egg', K=6, nF=3, nW=3, nY=3, wage='ahe_food_prod', leads=0, fah=True, start='2005-02', end='2026-09', drop=None, month=True, own=True):
    X = {}
    for k in range(-leads, K + 1):
        X[f'egg_l{k}'] = dl_[egg].shift(k)
    if fah:
        fcol = 'ny_fah' if y.startswith('ny_') else 'cpi_fah'
        for k in range(0, nF + 1): X[f'fah_l{k}'] = dl_[fcol].shift(k)
    if wage:
        for k in range(0, nW + 1): X[f'wage_l{k}'] = dl_[wage].shift(k)
    if own:
        for k in range(1, nY + 1): X[f'own_l{k}'] = dl_[y].shift(k)
    X = pd.DataFrame(X)
    if month: X = pd.concat([X, MONTH], axis=1)
    df = pd.concat([dl_[y].rename('Y'), X], axis=1).loc[start:end]
    if drop:
        for a, b in drop: df = df.drop(df.loc[a:b].index)
    return df.dropna()

def fit_dl(y, K=6, leads=0, **kw):
    df = design(y, K=K, leads=leads, **kw)
    m = sm.OLS(df['Y'], sm.add_constant(df.drop(columns='Y'))).fit(cov_type='HAC', cov_kwds={'maxlags': 12})
    names = list(m.params.index)
    def lin(cols):
        w = np.zeros(len(names)); [w.__setitem__(names.index(c), 1.0) for c in cols]
        est = float(w @ m.params.values); se = float(np.sqrt(w @ m.cov_params().values @ w)); return est, se
    lagcols = [f'egg_l{k}' for k in range(0, K + 1)]
    cum, cse = lin(lagcols)
    r = {'n': int(m.nobs), 'first': str(df.index[0]), 'last': str(df.index[-1]), 'cum': cum, 'cum_se': cse, 'cum_lo': cum - 1.96 * cse, 'cum_hi': cum + 1.96 * cse,
         'cum_p': float(2 * (1 - __import__('scipy').stats.norm.cdf(abs(cum / cse)))), 'r2': float(m.rsquared),
         'b': {c: float(m.params[c]) for c in lagcols}, 'b_se': {c: float(m.bse[c]) for c in lagcols}}
    # cumulative by horizon (for the figure)
    r['cum_by_k'] = []
    for k in range(0, K + 1):
        e, s = lin([f'egg_l{j}' for j in range(0, k + 1)]); r['cum_by_k'].append({'k': k, 'est': e, 'lo': e - 1.96 * s, 'hi': e + 1.96 * s})
    if leads:
        lc = [f'egg_l{-j}' for j in range(1, leads + 1)]; e, s = lin(lc)
        r['leads_sum'] = e; r['leads_se'] = s; r['leads_p'] = float(2 * (1 - __import__('scipy').stats.norm.cdf(abs(e / s))))
    # Wald test that the K+1 egg lags are jointly zero
    R = np.zeros((len(lagcols), len(names)))
    for i, c in enumerate(lagcols): R[i, names.index(c)] = 1
    w = m.wald_test(R, scalar=True); r['joint_p'] = float(w.pvalue)
    r['egg_sd'] = float(df['egg_l0'].std()); r['y_sd'] = float(df['Y'].std())
    return r

res = {'labels': {'out': dict(OUT), 'egg': EGG}}
# main specification, all four outcomes
res['main'] = {y: fit_dl(y) for y in OUT}
# leads falsification (3 leads)
res['leads'] = {y: fit_dl(y, leads=3) for y in OUT}
# sensitivity
SENS = {
 'baseline (K=6)': {},
 'K=3': {'K': 3}, 'K=12': {'K': 12},
 'no FAH control': {'fah': False}, 'no wage control': {'wage': None},
 'wage = all private AHE (from 2006-03)': {'wage': 'ahe_private', 'start': '2006-04'},
 'excl. 2020-03 to 2021-12': {'drop': [('2020-03', '2021-12')]},
 'from 2015-01': {'start': '2015-01'},
 'from 2019-01': {'start': '2019-01'},
 'egg = avg price, Grade A large': {'egg': 'avg_price_egg'},
 'egg = PPI large eggs': {'egg': 'ppi_egg_large'},
 'no month dummies': {'month': False},
 'no own lags': {'own': False},
}
res['sens'] = {lab: {y: fit_dl(y, **kw) for y in ['cpi_fsr', 'cpi_lsr', 'cpi_fafh', 'ny_fafh']} for lab, kw in SENS.items()}
# parsimonious model on the HPAI period only (2022-02 on)
res['hpai_period'] = {y: fit_dl(y, K=3, nF=1, nW=1, nY=2, month=False, start='2022-02') for y in OUT}

# (B) reduced-form local projections on layers affected
def lp_rf(y, H=12):
    ly = np.log(d[y]); full = pd.period_range('2021-10', '2026-09', freq='M'); Lf = L.reindex(full, fill_value=0.0); rows = []
    dy = ly.diff().reindex(full); wg = np.log(d['ahe_food_prod']).diff().reindex(full)
    for h in range(0, H + 1):
        X = pd.DataFrame({'L0': Lf, 'L1': Lf.shift(1), 'L2': Lf.shift(2), 'dy1': dy.shift(1), 'dy2': dy.shift(2), 'w1': wg.shift(1)})
        Y = (ly.shift(-h) - ly.shift(1)).reindex(full)
        df = pd.concat([Y.rename('Y'), X], axis=1).loc['2022-02':'2026-09'].dropna()
        m = sm.OLS(df['Y'], sm.add_constant(df.drop(columns='Y'))).fit(cov_type='HAC', cov_kwds={'maxlags': h + 3})
        b, se = m.params['L0'], m.bse['L0']
        rows.append({'h': h, 'b': float(b), 'se': float(se), 'lo': float(b - 1.96 * se), 'hi': float(b + 1.96 * se), 'p': float(m.pvalues['L0']), 'n': int(m.nobs)})
    return rows
res['rf_lp'] = {y: lp_rf(y) for y in OUT}
# placebo: same LP for all-items CPI less nothing available -> use food at home as comparison outcome
res['rf_lp']['cpi_fah'] = lp_rf('cpi_fah'); res['labels']['out']['cpi_fah'] = 'Food at home (US)'  # comparison outcome only

# (C) descriptive 12-month changes
yoy = (d[['cpi_egg', 'cpi_fah', 'cpi_fafh', 'cpi_fsr', 'cpi_lsr', 'ny_fafh', 'ahe_food_prod', 'avg_price_egg']] / d[['cpi_egg', 'cpi_fah', 'cpi_fafh', 'cpi_fsr', 'cpi_lsr', 'ny_fafh', 'ahe_food_prod', 'avg_price_egg']].shift(12) - 1) * 100
desc = {}
for lab, a, b in [('wave1', '2022-06', '2023-06'), ('wave2', '2024-10', '2025-09')]:
    sub = yoy.loc[a:b]; pk = sub['cpi_egg'].idxmax(); desc[lab] = {'peak_month': str(pk), **{k: float(yoy.loc[pk, k]) for k in yoy.columns}}
    # restaurant inflation 12 months later vs 12 months before peak
    desc[lab]['fsr_12m_before'] = float(yoy.loc[pk - 12, 'cpi_fsr']) if (pk - 12) in yoy.index else None
    desc[lab]['lsr_12m_before'] = float(yoy.loc[pk - 12, 'cpi_lsr']) if (pk - 12) in yoy.index else None
    for k in ['cpi_fsr', 'cpi_lsr']:
        later = yoy.loc[pk + 6: pk + 12, k].dropna() if (pk + 6) in yoy.index else pd.Series(dtype=float)
        desc[lab][k + '_next6to12'] = float(later.mean()) if len(later) else None
desc['egg_yoy_2022_12'] = float(yoy.loc['2022-12', 'cpi_egg']); desc['egg_yoy_2023_01'] = float(yoy.loc['2023-01', 'cpi_egg'])
desc['summary_sd_monthly'] = {k: float(dl_[k]['2005-02':'2026-09'].std()) for k in ['cpi_egg', 'cpi_fafh', 'cpi_fsr', 'cpi_lsr', 'cpi_fah', 'ny_fafh', 'ahe_food_prod']}
desc['cumulative_2019_12_to_2026_09'] = {k: float(100 * (d[k]['2026-09'] / d[k]['2019-12'] - 1)) for k in ['cpi_egg', 'cpi_fah', 'cpi_fafh', 'cpi_fsr', 'cpi_lsr', 'ny_fafh', 'cpi_all', 'ny_all']}
desc['cumulative_2021_12_to_2026_09'] = {k: float(100 * (d[k]['2026-09'] / d[k]['2021-12'] - 1)) for k in ['cpi_egg', 'cpi_fah', 'cpi_fafh', 'cpi_fsr', 'cpi_lsr', 'ny_fafh']}
desc['wage_cum_2021_12_to_2026_08'] = float(100 * (d['ahe_food_prod']['2026-08'] / d['ahe_food_prod']['2021-12'] - 1))
res['desc'] = desc
res['yoy_series'] = {k: {str(i): (None if np.isnan(v) else float(v)) for i, v in yoy[k].items()} for k in ['cpi_egg', 'cpi_fsr', 'cpi_lsr', 'cpi_fafh', 'ny_fafh', 'cpi_fah', 'ahe_food_prod']}
json.dump(res, open(f'{RES}/a2_passthrough.json', 'w'), indent=1)
for y in OUT:
    r = res['main'][y]; print(y, f"n={r['n']} cum={r['cum']:.4f} se={r['cum_se']:.4f} CI=({r['cum_lo']:.4f},{r['cum_hi']:.4f}) joint_p={r['joint_p']:.3f}  leads={res['leads'][y]['leads_sum']:.4f} p={res['leads'][y]['leads_p']:.3f}")
for lab in SENS:
    print(lab, {y: (round(res['sens'][lab][y]['cum'], 4), round(res['sens'][lab][y]['cum_se'], 4), res['sens'][lab][y]['n']) for y in ['cpi_fsr', 'cpi_lsr']})
print('hpai-period', {y: (round(res['hpai_period'][y]['cum'], 4), round(res['hpai_period'][y]['cum_se'], 4), res['hpai_period'][y]['n']) for y in OUT})
print(json.dumps(desc, indent=0)[:2500])
for y in ['cpi_fsr', 'cpi_lsr', 'cpi_fafh', 'cpi_fah']:
    print(y, [(r['h'], round(100 * r['b'] * 10, 3), round(r['p'], 2)) for r in res['rf_lp'][y]])
