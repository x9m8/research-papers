"""Long Island vs rest of New York State: gap paths, window differences, minimum-wage elasticities,
placebo inference, synthetic control, and a secondary NY/PA county panel.
Writes results/estimates.json, event_study.json, scm.json, panel.json, descriptives.json, break.json."""
import os, json
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from common import DER, RES, BASE_YEARS, COVID, SEED, INDUSTRIES, newey_west_se, ols

N_SPLITS = 2000
OUTCOMES = ['emp', 'estabs', 'wage']          # log employment, log establishments, log average weekly wage
R5 = lambda v: None if v is None or not np.isfinite(v) else round(float(v), 5)


def load():
    P = pd.read_csv(os.path.join(DER, 'panel.csv'), dtype={'area_fips': str, 'industry_code': str})
    S = pd.read_csv(os.path.join(DER, 'schedule_quarterly.csv'))
    return P, S


def mats(P, ind, counties, qis):
    """County x quarter arrays of employment, establishments, wages for the given counties (all must be disclosed)."""
    x = P[(P.industry_code == ind) & P.area_fips.isin(counties)]
    out = []
    for v in ['emp', 'estabs', 'wages']:
        m = x.pivot(index='area_fips', columns='qi', values=v).reindex(index=counties, columns=qis)
        out.append(m.to_numpy(float))
    return out


def agg_logs(E, N, W, w):
    """Aggregate rows with weight matrix w (k x counties) and return dict of log series (k x T)."""
    e, n, wa = w @ E, w @ N, w @ W
    return {'emp': np.log(e), 'estabs': np.log(n), 'wage': np.log(wa / e / 13.0)}


class Design:
    def __init__(self, S, base_years=BASE_YEARS):
        self.S = S.reset_index(drop=True)
        self.year = S.year.to_numpy(); self.qtr = S.qtr.to_numpy(); self.T = len(S)
        self.base = np.isin(self.year, base_years)
        self.est = ~np.isin(self.year, list(range(COVID[0], COVID[1] + 1)))   # quarters used for estimation

    def dev(self, L):
        """Subtract the same-quarter mean over the baseline years (removes level and seasonality)."""
        L = np.atleast_2d(L).copy()
        for q in range(1, 5):
            m = (self.qtr == q)
            L[:, m] -= L[:, m & self.base].mean(axis=1, keepdims=True)
        return L

    def windows(self):
        y = self.year
        return {'pre_2014_2015': (y <= 2015), 'post_2017_2019': (y >= 2017) & (y <= 2019), 'covid_2020_2021': (y >= 2020) & (y <= 2021),
                'y2022': y == 2022, 'y2023': y == 2023, 'post_2024_2026': y >= 2024}

    def elasticity(self, G, x, trend=False, sample=None, shift=False):
        """Regress each row of G (k x T) on x with an intercept over estimation quarters. Returns k slopes and NW se of row 0.
        trend: add a linear time trend; shift: add a step dummy for 2017Q1 onward (absorbs a one-off level break)."""
        m = self.est if sample is None else (self.est & sample)
        cols = [np.ones(m.sum()), x[m]]
        if trend:
            cols.append(np.arange(self.T)[m] / 4.0)
        if shift:
            cols.append((self.year[m] >= 2017).astype(float))
        X = np.column_stack(cols)
        B = np.linalg.lstsq(X, np.atleast_2d(G)[:, m].T, rcond=None)[0]
        b0, se0 = newey_west_se(np.atleast_2d(G)[0, m], X, lags=4)
        return B[1], se0[1]


def placebo_masks(nD, rng, n=N_SPLITS):
    M = np.zeros((n, nD))
    for i in range(n):
        M[i, rng.permutation(nD)[: nD // 2]] = 1.0
    return M


def summarise(est, plac):
    """Placebo-based inference: two-sided p, 95% interval (estimate minus placebo quantiles), SD and MDE (2.8 SD)."""
    plac = np.asarray(plac); plac = plac[np.isfinite(plac)]
    p = (1 + np.sum(np.abs(plac) >= abs(est))) / (1 + len(plac))
    lo, hi = est - np.quantile(plac, 0.975), est - np.quantile(plac, 0.025)
    return {'est': R5(est), 'lo': R5(lo), 'hi': R5(hi), 'p': R5(p), 'sd_placebo': R5(np.std(plac, ddof=1)),
            'mde': R5(2.8 * np.std(plac, ddof=1)), 'n_placebo': int(len(plac))}


def gap_and_placebos(D, P, ind, treated, donors, relative_to_total=False):
    qis = D.S.qi.tolist()
    Et, Nt, Wt = mats(P, ind, treated, qis); Ed, Nd, Wd = mats(P, ind, donors, qis)
    T = agg_logs(Et, Nt, Wt, np.ones((1, len(treated)))); C = agg_logs(Ed, Nd, Wd, np.ones((1, len(donors))))
    rng = np.random.default_rng(SEED)
    M = placebo_masks(len(donors), rng)
    PT = agg_logs(Ed, Nd, Wd, M); PC = agg_logs(Ed, Nd, Wd, 1 - M)
    single = np.eye(len(donors)); ST = agg_logs(Ed, Nd, Wd, single); SC = agg_logs(Ed, Nd, Wd, 1 - single)
    if relative_to_total:
        Et0, _, _ = mats(P, '10', treated, qis); Ed0, _, _ = mats(P, '10', donors, qis)
        T['emp'] = T['emp'] - np.log(Et0.sum(0, keepdims=True)); C['emp'] = C['emp'] - np.log(Ed0.sum(0, keepdims=True))
        PT['emp'] = PT['emp'] - np.log(M @ Ed0); PC['emp'] = PC['emp'] - np.log((1 - M) @ Ed0)
        ST['emp'] = ST['emp'] - np.log(Ed0); SC['emp'] = SC['emp'] - np.log((1 - single) @ Ed0)
    out = {}
    for o in OUTCOMES:
        out[o] = {'gap': D.dev(T[o])[0] - D.dev(C[o])[0], 'split': D.dev(PT[o]) - D.dev(PC[o]), 'single': D.dev(ST[o]) - D.dev(SC[o])}
    return out


def estimate_block(D, G, x, trend=False, sample=None, single_ok=None, shift=False):
    b, se = D.elasticity(G['gap'][None, :], x, trend, sample, shift)
    bs, _ = D.elasticity(G['split'], x, trend, sample, shift); b1, _ = D.elasticity(G['single'], x, trend, sample, shift)
    if single_ok is not None:
        b1 = b1[single_ok]
    r = {'elasticity': summarise(b[0], bs), 'elasticity_single_county_placebo': summarise(b[0], b1), 'elasticity_nw_se': R5(se)}
    r['elasticity']['nw_lo'] = R5(b[0] - 1.96 * se); r['elasticity']['nw_hi'] = R5(b[0] + 1.96 * se)
    for k, m in D.windows().items():
        r[k] = summarise(G['gap'][m].mean(), G['split'][:, m].mean(1))
    # 2023 narrowing of the regional gap: change in the outcome gap from 2022 to 2023, and the implied elasticity
    a, c = D.year == 2022, D.year == 2023
    dx = x[c].mean() - x[a].mean()
    d, ds = G['gap'][c].mean() - G['gap'][a].mean(), G['split'][:, c].mean(1) - G['split'][:, a].mean(1)
    r['chg_2022_to_2023'] = summarise(d, ds); r['chg_2022_to_2023']['d_log_mw_gap'] = R5(dx)
    if abs(dx) > 1e-9:
        r['implied_elasticity_2023'] = summarise(d / dx, ds / dx)
    return r


def scm(D, P, ind, treated, donors, x):
    """Synthetic control on the baseline-demeaned log series (pre-period = baseline years), with in-space placebos.
    Because the series are demeaned on the same quarters used for fitting, the pre-period fit is (near) exact by construction,
    so the post/pre RMSPE ratio is not informative; post_rmspe_rank ranks units by post-period RMSPE alone."""
    qis = D.S.qi.tolist()
    Et, Nt, Wt = mats(P, ind, treated, qis); Ed, Nd, Wd = mats(P, ind, donors, qis)
    T = agg_logs(Et, Nt, Wt, np.ones((1, len(treated)))); U = agg_logs(Ed, Nd, Wd, np.eye(len(donors)))
    res = {}
    for o in ['emp', 'wage']:
        y1 = D.dev(T[o])[0]; Y0 = D.dev(U[o])
        pre = D.base

        def fit(y, Y):
            k = Y.shape[0]; Yp, yp = Y[:, pre], y[pre]
            r = minimize(lambda w: np.sum((yp - w @ Yp) ** 2), np.full(k, 1.0 / k), jac=lambda w: -2 * Yp @ (yp - w @ Yp), method='SLSQP',
                         bounds=[(0, 1)] * k, constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1, 'jac': lambda w: np.ones(k)}],
                         options={'maxiter': 500, 'ftol': 1e-12})
            return np.clip(r.x, 0, None) / np.clip(r.x, 0, None).sum()

        w = fit(y1, Y0); g = y1 - w @ Y0
        post = D.est & (D.year >= 2017)
        rmspe = lambda gg, m: float(np.sqrt(np.mean(gg[m] ** 2)))
        ratio = rmspe(g, post) / max(rmspe(g, pre), 1e-9)
        pr, pb, pp, pq = [], [], [], []
        for j in range(len(donors)):
            idx = [k for k in range(len(donors)) if k != j]
            wj = fit(Y0[j], Y0[idx]); gj = Y0[j] - wj @ Y0[idx]
            pr.append(rmspe(gj, post) / max(rmspe(gj, pre), 1e-9)); pb.append(D.elasticity(gj[None, :], x)[0][0]); pp.append(rmspe(gj, post)); pq.append(rmspe(gj, pre))
        b, se = D.elasticity(g[None, :], x)
        top = np.argsort(-w)[:5]
        res[o] = {'gap': [R5(v) for v in g], 'weights_top': {donors[k]: R5(w[k]) for k in top if w[k] > 1e-4},
                  'n_donors_weight_gt_0.01': int(np.sum(w > 0.01)), 'pre_rmspe': R5(rmspe(g, pre)), 'post_rmspe': R5(rmspe(g, post)),
                  'rmspe_ratio_rank': int(1 + np.sum(np.array(pr) >= ratio)), 'post_rmspe_rank': int(1 + np.sum(np.array(pp) >= rmspe(g, post))),
                  'n_units_pre_rmspe_below_1e-6': int(np.sum(np.array([rmspe(g, pre)] + pq) < 1e-6)), 'n_units': len(donors) + 1,
                  'elasticity': summarise(b[0], pb), 'elasticity_nw_se': R5(se),
                  'mean_gap_2017_2019': R5(g[(D.year >= 2017) & (D.year <= 2019)].mean()), 'mean_gap_2022': R5(g[D.year == 2022].mean()),
                  'mean_gap_2024_2026': R5(g[D.year >= 2024].mean())}
    return res


def wage_outliers(P, ind, c):
    """Returns {c} if the county's average weekly wage in this industry moves by more than 25 log points between consecutive quarters
    outside 2020-2021, else an empty set."""
    x = P[(P.industry_code == ind) & (P.area_fips == c)].sort_values('qi')
    lw = np.log(x.wages / x.emp / 13.0).to_numpy(); yr = x.year.to_numpy()
    d = np.abs(np.diff(lw)); ok = ~np.isin(yr[1:], [2020, 2021]) & ~np.isin(yr[:-1], [2020, 2021])
    return {c} if np.any(d[ok] > 0.25) else set()


def break_check(P):
    """Fourth-to-first-quarter change in summed establishments and employment by region and year (balanced counties)."""
    out = {}
    for ind in INDUSTRIES:
        x = P[(P.industry_code == ind) & P.balanced]
        for rg in ['LI', 'WES', 'NYC', 'ROS', 'PA']:
            r = x[x.region == rg].groupby(['year', 'qtr'])[['estabs', 'emp']].sum()
            if not len(r):
                continue
            o = {}
            for y in range(2015, 2027):
                if (y - 1, 4) in r.index and (y, 1) in r.index:
                    o[y] = {'estabs': R5(r.loc[(y, 1), 'estabs'] / r.loc[(y - 1, 4), 'estabs'] - 1), 'emp': R5(r.loc[(y, 1), 'emp'] / r.loc[(y - 1, 4), 'emp'] - 1)}
            out[f'{ind}_{rg}'] = o
    return out


def county_panel(P, S, ind, counties, regions, weight=False, years=None):
    """ln Y = county x season FE + quarter FE + b ln MW; county-clustered SE."""
    x = P[(P.industry_code == ind) & P.area_fips.isin(counties)].merge(S[['qi', 'mw_li', 'mw_ros', 'mw_pa']], on='qi')
    x = x[~x.year.between(*COVID)]
    if years is not None:
        x = x[x.year.between(*years)]
    x['lmw'] = np.log(np.where(x.area_fips.map(regions) == 'LI', x.mw_li, np.where(x.area_fips.map(regions) == 'PA', x.mw_pa, x.mw_ros)))
    x['y'] = np.log(x.emp)
    w16 = x[x.year == 2016].groupby('area_fips').emp.mean()
    fe1 = pd.get_dummies(x.area_fips + '_' + x.qtr.astype(str), drop_first=False).to_numpy(float)
    fe2 = pd.get_dummies(x.qi, drop_first=True).to_numpy(float)
    X = np.column_stack([x.lmw.to_numpy(), fe1, fe2]); y = x.y.to_numpy()
    wt = x.area_fips.map(w16).to_numpy() if weight else np.ones(len(x))
    sw = np.sqrt(wt); Xw, yw = X * sw[:, None], y * sw
    XtX = np.linalg.pinv(Xw.T @ Xw); b = XtX @ Xw.T @ yw; e = yw - Xw @ b
    cl = x.area_fips.to_numpy(); meat = np.zeros((X.shape[1], X.shape[1]))
    for c in np.unique(cl):
        s = Xw[cl == c].T @ e[cl == c]; meat += np.outer(s, s)
    G = len(np.unique(cl)); n, k = X.shape
    V = XtX @ meat @ XtX * G / (G - 1) * (n - 1) / (n - k)
    se = float(np.sqrt(V[0, 0]))
    return {'b': R5(b[0]), 'se': R5(se), 'lo': R5(b[0] - 1.96 * se), 'hi': R5(b[0] + 1.96 * se), 'n_obs': int(n), 'n_counties': int(G)}


def main():
    P, S = load()
    D = Design(S)
    xg, xt, xf = S.gap_general.to_numpy(), S.gap_tip.to_numpy(), S.gap_ff.to_numpy()
    bal = P[P.balanced].groupby('industry_code').area_fips.apply(lambda s: sorted(set(s)))
    reg = P.drop_duplicates('area_fips').set_index('area_fips').region
    LIc = sorted(reg[reg == 'LI'].index); WES = sorted(reg[reg == 'WES'].index)
    est, es, sc, pan, desc = {}, {}, {}, {}, {}
    for ind in INDUSTRIES:
        donors = [c for c in bal[ind] if reg[c] == 'ROS']
        G = gap_and_placebos(D, P, ind, LIc, donors)
        qis = S.qi.tolist(); Ed, _, _ = mats(P, ind, donors, qis); size16 = Ed[:, D.year == 2016].mean(1)
        big = size16 >= 1000
        est[ind] = {'n_donors': len(donors), 'n_donors_ge1000': int(big.sum())}
        for o in OUTCOMES:
            est[ind][o] = {'main': estimate_block(D, {k: G[o][k] for k in G[o]}, xg)}
        es[ind] = {o: {'gap': [R5(v) for v in G[o]['gap']], 'q025': [R5(v) for v in np.quantile(G[o]['split'], 0.025, axis=0)],
                       'q975': [R5(v) for v in np.quantile(G[o]['split'], 0.975, axis=0)],
                       'pretrend_slope_per_year': R5(np.polyfit(np.arange(12) / 4.0, G[o]['gap'][D.base], 1)[0]),
                       'pretrend_slope_placebo_p': R5((1 + np.sum(np.abs([np.polyfit(np.arange(12) / 4.0, r[D.base], 1)[0] for r in G[o]['split']]) >=
                                                              abs(np.polyfit(np.arange(12) / 4.0, G[o]['gap'][D.base], 1)[0]))) / (1 + N_SPLITS))}
                   for o in OUTCOMES}
        if ind == '10':
            continue
        # robustness for employment and wages
        rob = {}
        for o in OUTCOMES:
            g = {k: G[o][k] for k in G[o]}
            r = {'trend': estimate_block(D, g, xg, trend=True)['elasticity'],
                 'step_2017': estimate_block(D, g, xg, shift=True)['elasticity'],
                 'pre_covid_only': estimate_block(D, g, xg, sample=(D.year <= 2019))['elasticity'],
                 'single_county_placebo': est[ind][o]['main']['elasticity_single_county_placebo'],
                 'single_county_placebo_ge1000': estimate_block(D, g, xg, single_ok=big)['elasticity_single_county_placebo']}
            if ind == '722511':
                r['tipped_cash_wage_gap'] = estimate_block(D, g, xt)['elasticity']
            if ind == '722513':
                r['fast_food_effective_gap'] = estimate_block(D, g, xf)['elasticity']
            Gw = gap_and_placebos(D, P, ind, LIc + WES, donors)
            r['with_westchester'] = estimate_block(D, {k: Gw[o][k] for k in Gw[o]}, xg)['elasticity']
            Gl = gap_and_placebos(D, P, ind, LIc, [c for c, b_ in zip(donors, big) if b_])
            r['donors_ge1000'] = estimate_block(D, {k: Gl[o][k] for k in Gl[o]}, xg)['elasticity']
            D16 = Design(S, base_years=(2016,)); G16 = gap_and_placebos(D16, P, ind, LIc, donors)
            r['baseline_2016_only'] = estimate_block(D16, {k: G16[o][k] for k in G16[o]}, xg)['elasticity']
            if o == 'emp':
                Gr = gap_and_placebos(D, P, ind, LIc, [c for c in donors if c in bal['10']], relative_to_total=True)
                r['relative_to_total_private'] = estimate_block(D, {k: Gr[o][k] for k in Gr[o]}, xg)['elasticity']
            if o == 'wage':
                clean = [c for c in donors if c not in wage_outliers(P, ind, c)]
                Gc = gap_and_placebos(D, P, ind, LIc, clean)
                r['drop_wage_outlier_donors'] = estimate_block(D, {k: Gc[o][k] for k in Gc[o]}, xg)['elasticity']
                r['drop_wage_outlier_donors']['n_dropped'] = len(donors) - len(clean)
            rob[o] = r
        est[ind]['robustness'] = rob
        sc[ind] = scm(D, P, ind, LIc, donors, xg)
        # secondary county panel: within NY (LI vs ROS) and NY + PA
        pa = [c for c in bal[ind] if reg[c] == 'PA']
        pan[ind] = {'ny_li_ros': county_panel(P, S, ind, LIc + donors, reg),
                    'ny_li_ros_weighted': county_panel(P, S, ind, LIc + donors, reg, weight=True),
                    'ny_pa': county_panel(P, S, ind, LIc + donors + pa, reg),
                    'ny_pa_weighted': county_panel(P, S, ind, LIc + donors + pa, reg, weight=True),
                    'ny_pa_pre_covid': county_panel(P, S, ind, LIc + donors + pa, reg, years=(2014, 2019)),
                    'n_pa_counties': len(pa)}
    # descriptives: levels for LI and the ROS donor aggregate
    for ind in INDUSTRIES:
        donors = [c for c in bal[ind] if reg[c] == 'ROS']
        dd = {}
        for name, cs in [('LI', LIc), ('ROS_donors', donors)]:
            x = P[(P.industry_code == ind) & P.area_fips.isin(cs)]
            yr = x.groupby(['year', 'qi'])[['emp', 'estabs', 'wages']].sum().groupby('year').mean()
            yr['aww'] = yr.wages / yr.emp / 13.0
            dd[name] = {int(y): {'emp': R5(r.emp), 'estabs': R5(r.estabs), 'aww': R5(r.aww)} for y, r in yr.iterrows()}
        desc[ind] = dd
    desc['li_counties'] = LIc
    json.dump({'note': 'elasticities: d log(outcome) / d log(minimum wage), LI minus ROS; windows: mean log gap vs 2014-2016 seasonal baseline',
               'n_splits': N_SPLITS, 'seed': SEED, 'estimates': est}, open(os.path.join(RES, 'estimates.json'), 'w'), separators=(',', ':'))
    json.dump({'qi': S.qi.tolist(), 'label': [f'{y}Q{q}' for y, q in zip(S.year, S.qtr)], 'gap_general': [R5(v) for v in xg],
               'gap_tip': [R5(v) for v in xt], 'gap_ff': [R5(v) for v in xf], 'series': es}, open(os.path.join(RES, 'event_study.json'), 'w'), separators=(',', ':'))
    json.dump(sc, open(os.path.join(RES, 'scm.json'), 'w'), separators=(',', ':'))
    json.dump(pan, open(os.path.join(RES, 'panel.json'), 'w'), separators=(',', ':'))
    json.dump(desc, open(os.path.join(RES, 'descriptives.json'), 'w'), separators=(',', ':'))
    json.dump(break_check(P), open(os.path.join(RES, 'break.json'), 'w'), separators=(',', ':'))
    for ind in ['722', '722511', '722513']:
        print(ind, est[ind]['n_donors'], {o: est[ind][o]['main']['elasticity'] for o in OUTCOMES})


if __name__ == '__main__':
    main()
