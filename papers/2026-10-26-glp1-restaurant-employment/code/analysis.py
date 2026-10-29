"""County long-difference and event-study estimates -> results/estimates.json, results/event_study.json,
results/descriptives.json. Run after build_panel.py."""
import json, os
import numpy as np
import pandas as pd
from common import DER, RES, YEARS_Q, BASE, END_D, END_Q, IND, ols_fe, mde, tcrit, tpval, wald

p = pd.read_csv(os.path.join(DER, 'county_panel.csv'), dtype={'fips': str, 'state': str})
p['state'] = p.fips.str[:2]
L = lambda s: np.log(s.where(s > 0))

# ---------------- sample ----------------
n0 = len(p)
p = p[(p[f'partd_{BASE}'] >= 1000) & p[f'E_{BASE}'].notna() & p[f'E_{END_D}'].notna()]
n1 = len(p)
rest = np.ones(len(p), bool)
for k in ('fsr', 'lsr'):
    for y in YEARS_Q:
        rest &= (p[f'{k}_emp_{y}'] > 0).values & (p[f'{k}_est_{y}'] > 0).values & (p[f'{k}_wag_{y}'] > 0).values
p = p[rest].copy()
for y in YEARS_Q:
    p[f'diff_emp_{y}'] = p[f'lsr_emp_{y}'] / p[f'fsr_emp_{y}']   # log of this = log LSR - log FSR
    p[f'diff_est_{y}'] = p[f'lsr_est_{y}'] / p[f'fsr_est_{y}']
    p[f'diff_wag_{y}'] = p[f'lsr_wag_{y}'] / p[f'fsr_wag_{y}']
lo, hi = p.dE.quantile([0.01, 0.99])
p['dEw'] = p.dE.clip(lo, hi)
for v in ('dE_semtir', 'dE_share'):
    a, b = p[v].quantile([0.01, 0.99]); p[v + 'w'] = p[v].clip(a, b)
sd = {v: float(p[v].std()) for v in ('dEw', 'dE', 'dE_semtirw', 'dE_sharew')}
p['c_ltot'] = L(p[f'tot_emp_{BASE}'])
p['c_lpartd'] = np.log(p[f'partd_{BASE}'])
p['c_E0'] = p[f'E_{BASE}']
p['c_tottrend'] = L(p[f'tot_emp_{BASE}']) - L(p[f'tot_emp_2015'])
CTRL = ['c_ltot', 'c_lpartd', 'c_E0', 'c_tottrend']


def ld(key, meas, x='dEw', y0=BASE, y1=END_Q, controls=True, pretrend=True, weight=False, extra=None, sub=None):
    d = p if sub is None else p[sub(p)]
    out = L(d[f'{key}_{meas}_{y1}']) - L(d[f'{key}_{meas}_{y0}'])
    cols = [x] + (CTRL if controls else []) + (extra or [])
    X = d[cols].copy()
    if pretrend:
        X['pre'] = L(d[f'{key}_{meas}_{BASE}']) - L(d[f'{key}_{meas}_2015'])
    w = d[f'{key}_{meas}_{BASE}'] if weight and key != 'diff' else (d[f'fsr_{meas}_{BASE}'] + d[f'lsr_{meas}_{BASE}'] if weight else None)
    ok = out.notna() & X.notna().all(axis=1)
    r = ols_fe(out[ok], X[ok].values, d.state[ok].values, d.state[ok].values, None if w is None else w[ok].values)
    b, se, df = float(r['b'][0]), float(r['se'][0]), r['df']
    xs = float(d.loc[ok, x].std())
    return {'b_pp': 100 * b, 'se_pp': 100 * se, 'lo_pp': 100 * (b - tcrit(df) * se), 'hi_pp': 100 * (b + tcrit(df) * se),
            'p': tpval(b / se, df), 'mde_pp': 100 * mde(se, df), 'b_sd': 100 * b * xs, 'lo_sd': 100 * (b - tcrit(df) * se) * xs,
            'hi_sd': 100 * (b + tcrit(df) * se) * xs, 'mde_sd': 100 * mde(se, df) * xs, 'sd_x': xs, 'n': r['n'], 'G': r['G'],
            'mean_dy_pct': float(100 * out[ok].mean())}

E = {}
OUTS = [('lsr', 'emp'), ('fsr', 'emp'), ('diff', 'emp'), ('lsr', 'est'), ('fsr', 'est'), ('diff', 'est'),
        ('lsr', 'wag'), ('fsr', 'wag'), ('diff', 'wag')]
CONTROLS_IND = [('pharm', 'emp'), ('acc', 'emp'), ('groc', 'emp')]
for k, m in OUTS + CONTROLS_IND:
    E[f'{k}_{m}'] = {'main': ld(k, m)}
for k, m in OUTS[:3] + CONTROLS_IND:
    e = E[f'{k}_{m}']
    e['no_controls'] = ld(k, m, controls=False, pretrend=False)
    e['weighted'] = ld(k, m, weight=True)
    e['to_2024'] = ld(k, m, y1=END_D)
    e['semtir'] = ld(k, m, x='dE_semtirw')
    e['claims_share'] = ld(k, m, x='dE_sharew')
    e['unwinsorised'] = ld(k, m, x='dE')
    e['partd_ge_5000'] = ld(k, m, sub=lambda d: d[f'partd_{BASE}'] >= 5000)
    e['excl_2019_top_decile_E0'] = ld(k, m, sub=lambda d: d.c_E0 < d.c_E0.quantile(0.9))
p['c_totgrowth'] = L(p[f'tot_emp_{END_Q}']) - L(p[f'tot_emp_{BASE}'])
for k, m in OUTS[:3]:
    E[f'{k}_{m}']['plus_total_emp_growth'] = ld(k, m, extra=['c_totgrowth'])

# ---------------- benchmark implied by household evidence ----------------
# Hristakeva et al. (2026): -8.0% limited-service spending in adopting households. If the share of households
# with a user rises by 1 percentage point per 1-point rise in Part D uptake (m = 1), aggregate LSR spending falls
# by 0.08% per point; m = 2 and m = 4 allow all-ages household uptake to rise faster than Part D uptake.
bench = {f'm{m}': -0.08 * m for m in (1, 2, 4)}

# ---------------- event study ----------------
ES = {}
ES_CTRL = ['c_ltot', 'c_lpartd', 'c_E0']
for k in ('lsr', 'fsr', 'diff', 'pharm', 'acc', 'groc'):
    ok_all = p[ES_CTRL + ['dEw']].notna().all(axis=1).to_numpy().copy()
    for y in YEARS_Q:
        ok_all &= (p[f'{k}_emp_{y}'] > 0).values
    d = p[ok_all]
    res = {}
    for y in YEARS_Q:
        if y == BASE:
            res[y] = {'b_pp': 0.0, 'lo_pp': 0.0, 'hi_pp': 0.0}; continue
        out = np.log(d[f'{k}_emp_{y}']) - np.log(d[f'{k}_emp_{BASE}'])
        r = ols_fe(out, d[['dEw'] + ES_CTRL].values, d.state.values, d.state.values)
        b, se = float(r['b'][0]), float(r['se'][0])
        res[y] = {'b_pp': 100 * b, 'se_pp': 100 * se, 'lo_pp': 100 * (b - tcrit(r['df']) * se), 'hi_pp': 100 * (b + tcrit(r['df']) * se)}
    # joint pre-trend test: stack 2015-2018, state-by-year fixed effects, controls interacted with year
    pre = [y for y in YEARS_Q if y < BASE]
    ys, Xs, fe, cl = [], [], [], []
    for j, y in enumerate(pre):
        out = np.log(d[f'{k}_emp_{y}']) - np.log(d[f'{k}_emp_{BASE}'])
        X = np.zeros((len(d), len(pre) * (1 + len(ES_CTRL))))
        X[:, j] = d.dEw.values
        for c_i, c in enumerate(ES_CTRL):
            X[:, len(pre) + j * len(ES_CTRL) + c_i] = d[c].values
        ys.append(out.values); Xs.append(X); fe.append((d.state + f'_{y}').values); cl.append(d.state.values)
    r = ols_fe(np.concatenate(ys), np.vstack(Xs), np.concatenate(fe), np.concatenate(cl))
    F, pF = wald(r['b'][:len(pre)], r['V'][:len(pre), :len(pre)], r['df'])
    ES[k] = {'coef': res, 'n': int(len(d)), 'pretrend_F': F, 'pretrend_p': pF}

# ---------------- descriptives ----------------
desc = {'n_joined': n0, 'n_partd_ge_1000': n1, 'n_main': int(len(p)), 'n_states': int(p.state.nunique()),
        'winsor_bounds': [float(lo), float(hi)], 'sd': sd,
        'E_base_mean': float(p[f'E_{BASE}'].mean()), 'E_end_mean': float(p[f'E_{END_D}'].mean()),
        'E_base_wmean': float(np.average(p[f'E_{BASE}'], weights=p[f'partd_{BASE}'])),
        'E_end_wmean': float(np.average(p[f'E_{END_D}'], weights=p[f'partd_{END_D}'].fillna(p[f'partd_{BASE}']))),
        'dE_mean': float(p.dE.mean()), 'dE_median': float(p.dE.median()), 'dE_p10': float(p.dE.quantile(.1)), 'dE_p90': float(p.dE.quantile(.9)),
        'dE_p90_p10': float(p.dE.quantile(.9) - p.dE.quantile(.1)),
        'share_partd_main_of_all': float(p[f'partd_{BASE}'].sum() / pd.read_csv(os.path.join(DER, 'county_panel.csv'))[f'partd_{BASE}'].sum()),
        'emp': {k: {'base_sum': float(p[f'{k}_emp_{BASE}'].sum()), 'end_sum': float(p[f'{k}_emp_{END_Q}'].sum()),
                    'median_base': float(p[f'{k}_emp_{BASE}'].median())} for k in ('fsr', 'lsr')},
        'mean_dlog_pct': {k: float(100 * (np.log(p[f'{k}_emp_{END_Q}']) - np.log(p[f'{k}_emp_{BASE}'])).mean()) for k in ('fsr', 'lsr')},
        'corr_dE_dEshare': float(p[['dEw', 'dE_sharew']].corr().iloc[0, 1]),
        'corr_dE_dEsemtir': float(p[['dEw', 'dE_semtirw']].corr().iloc[0, 1]),
        'n_ctrl': {k: E[f'{k}_emp']['main']['n'] for k in ('pharm', 'acc', 'groc')}}
# national Part D uptake from the CMS geography file, by year
B = json.load(open(os.path.join(RES, 'build.json')))
en = pd.read_csv(os.path.join(DER, 'exposure_county_year.csv'))
nat = {}
for y, c in B['coverage'].items():
    pdn = en.loc[en.year == int(y), 'partd'].sum()
    nat[y] = {'fills_national': c['fills_national'], 'E_national_approx': 100 * c['fills_national'] / 12 / pdn,
              'semtir_fills': sum(v for g, v in c['fills_by_generic_national'].items() if g in ('Semaglutide', 'Tirzepatide'))}
desc['national'] = nat
# histogram and binned scatter for figures
h, edges = np.histogram(p.dE, bins=40, range=(float(p.dE.quantile(.005)), float(p.dE.quantile(.995))))
desc['hist'] = {'counts': h.tolist(), 'edges': edges.tolist()}
# binned scatter: residualised long difference (LSR minus FSR employment) on residualised exposure, 20 bins
from common import _demean
g = np.unique(p.state, return_inverse=True)[1]
yv = (np.log(p[f'diff_emp_{END_Q}']) - np.log(p[f'diff_emp_{BASE}'])).values
Xc = np.column_stack([p[c] for c in CTRL] + [np.log(p[f'diff_emp_{BASE}']) - np.log(p['diff_emp_2015'])])
ok = ~np.isnan(Xc).any(axis=1) & ~np.isnan(yv)
def resid(v):
    vd = _demean(v[ok], g[ok], np.ones(ok.sum()))[:, 0]; Xd = _demean(Xc[ok], g[ok], np.ones(ok.sum()))
    return vd - Xd @ np.linalg.lstsq(Xd, vd, rcond=None)[0]
rx, ry = resid(p.dEw.values), resid(yv)
qs = pd.qcut(rx, 20, labels=False)
desc['binscatter_diff'] = {'x': [float(rx[qs == i].mean()) for i in range(20)], 'y_pct': [float(100 * ry[qs == i].mean()) for i in range(20)]}

def rnd(o):
    """Round floats to 6 significant digits for compact result files."""
    if isinstance(o, float):
        return float(f'{o:.6g}')
    if isinstance(o, dict):
        return {str(k): rnd(v) for k, v in o.items()}
    if isinstance(o, list):
        return [rnd(v) for v in o]
    return o


for name, obj in (('estimates', {'estimates': E, 'benchmark_pct_per_pp': bench}), ('event_study', ES), ('descriptives', desc)):
    json.dump(rnd(obj), open(os.path.join(RES, f'{name}.json'), 'w'), separators=(',', ':'))
print(json.dumps({k: {m: {kk: round(vv, 3) for kk, vv in v.items() if kk in ('b_pp', 'lo_pp', 'hi_pp', 'mde_pp', 'n', 'p')} for m, v in e.items() if m == 'main'} for k, e in E.items()}))
