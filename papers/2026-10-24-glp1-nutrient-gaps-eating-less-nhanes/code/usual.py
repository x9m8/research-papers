"""Usual intake by the NRC (1986) variance-adjustment method on the log scale, by sex, then scenario scaling and prevalence below the EAR
(cut-point). Survey-weighted with the dietary two-day weight; Taylor-linearised SEs from strata and PSUs."""
import json, numpy as np, pandas as pd
from common import RAW, RES, EAR, AI, NUTS, SCEN, LABEL, ageband
CYCLE = {'L': dict(demo='DEMO_L', bmx='BMX_L', d1='DR1TOT_L', d2='DR2TOT_L', diq='DIQ_L', bpq='BPQ_L', w2='WTDR2D', w1='WTDRD1'),
         'P': dict(demo='P_DEMO', bmx='P_BMX', d1='P_DR1TOT', d2='P_DR2TOT', diq='P_DIQ', bpq='P_BPQ', w2='WTDR2DPP', w1='WTDRD1PP')}
def rd(n): return pd.read_sas(f'{RAW}/{n}.xpt', format='xport')
def sample(c):
    C = CYCLE[c]; d = rd(C['demo']).merge(rd(C['bmx'])[['SEQN', 'BMXWT', 'BMXHT', 'BMXBMI']], on='SEQN', how='left')
    d1 = rd(C['d1']); d2 = rd(C['d2'])
    keep1 = ['SEQN', C['w1'], C['w2'], 'DR1DRSTZ'] + [f'DR1T{n}' for n in NUTS]; keep2 = ['SEQN', 'DR2DRSTZ'] + [f'DR2T{n}' for n in NUTS]
    d = d.merge(d1[keep1], on='SEQN', how='left').merge(d2[keep2], on='SEQN', how='left')
    diq = rd(C['diq'])[['SEQN', 'DIQ010']]; bpq = rd(C['bpq'])
    bp = 'BPQ020' if 'BPQ020' in bpq else None
    d = d.merge(diq, on='SEQN', how='left').merge(bpq[['SEQN', bp]] if bp else bpq[['SEQN']], on='SEQN', how='left')
    if c == 'P':
        for k, f in (('1', 'P_DS1TOT'), ('2', 'P_DS2TOT')):
            ds = rd(f); cols = [x for x in ds.columns if x.startswith(f'DS{k}T')]
            d = d.merge(ds[['SEQN'] + cols], on='SEQN', how='left')
    d['adult'] = (d.RIDAGEYR >= 20) & (d.RIDEXPRG.fillna(2) != 1)
    d['comorb'] = (d.DIQ010 == 1) | ((d[bp] == 1) if bp else False)
    d['eligible'] = d.adult & ((d.BMXBMI >= 30) | ((d.BMXBMI >= 27) & d.comorb))
    d['two'] = (d.DR1DRSTZ == 1) & (d.DR2DRSTZ == 1) & (d[C['w2']] > 1e-6)
    d['w'] = d[C['w2']]; d['sex'] = np.where(d.RIAGENDR == 1, 'M', 'F'); d['ab'] = d.RIDAGEYR.map(ageband)
    d['refwt'] = 25 * (d.BMXHT / 100) ** 2          # weight at BMI 25 for measured height
    d['ibw'] = 22 * (d.BMXHT / 100) ** 2; d['adjwt'] = d.ibw + 0.4 * (d.BMXWT - d.ibw)
    return d
def usual(df, n, r=0.0, supp=False):
    """NRC shrinkage on log(x + 1) by sex, with day 1 as the reference (day-2 recalls rescaled to the day-1 weighted mean, as the NCI method
    treats the day-2 sequence effect), back-transformed and rescaled to the weighted mean of observed 2-day means. Scenario r scales food intake;
    supplements (supp=True) are added after shrinkage as each person's mean of the two supplement recalls ("shrink then add")."""
    out = pd.Series(np.nan, index=df.index)
    for s, g in df.groupby('sex'):
        w = g.w / g.w.sum()
        x1 = g[f'DR1T{n}'].astype(float); x2 = g[f'DR2T{n}'].astype(float)
        x2 = x2 * np.sum(w * x1) / np.sum(w * x2)
        a = np.log1p(x1); b = np.log1p(x2); m = (a + b) / 2; mu = np.sum(w * m)
        dd = a - b; s2w = np.sum(w * (dd - np.sum(w * dd)) ** 2) / 2   # within-person variance (per day), centred
        s2m = np.sum(w * (m - mu) ** 2)                                 # variance of 2-day means
        s2b = max(s2m - s2w / 2, 1e-9)
        f = np.sqrt(s2b / (s2b + s2w / 2))
        u = np.expm1(mu + (m - mu) * f)
        obs = (x1 + x2) / 2
        u = u * np.sum(w * obs) / np.sum(w * u)
        u = u * (1 - r)
        if supp and f'DS1T{n}' in g:
            u = u + (g[f'DS1T{n}'].fillna(0) + g[f'DS2T{n}'].fillna(0)) / 2
        out.loc[g.index] = u
    return out
def wprop(y, df):
    """Weighted proportion and Taylor-linearised SE (with-replacement PSUs within strata)."""
    w = df.w.values; y = y.values.astype(float); p = np.sum(w * y) / np.sum(w)
    z = w * (y - p) / np.sum(w); t = pd.DataFrame({'h': df.SDMVSTRA.values, 'i': df.SDMVPSU.values, 'z': z}).groupby(['h', 'i']).z.sum().reset_index()
    v = 0.0
    for h, g in t.groupby('h'):
        nh = len(g)
        if nh > 1: v += nh / (nh - 1) * np.sum((g.z - g.z.mean()) ** 2)
    return p, np.sqrt(v)
def run(c, protect_protein=False, supp=False):
    d = sample(c); E = d[d.eligible & d.two].copy()
    U = pd.DataFrame({n: usual(E, n) for n in NUTS}, index=E.index)
    res = {}
    for sc, r in SCEN.items():
        X = U * (1 - r) if not supp else pd.DataFrame({n: usual(E, n, r, True) for n in NUTS}, index=E.index)
        if protect_protein: X['PROT'] = U.PROT
        row = {}
        for n in EAR:
            ear = np.array([EAR[n][s][a] for s, a in zip(E.sex, E.ab)])
            mask = pd.Series(True, index=E.index)
            if n == 'IRON': mask = ~((E.sex == 'F') & (E.RIDAGEYR < 51))   # cut-point invalid for menstruating women
            p, se = wprop((X[n] < ear)[mask], E[mask]); row[n] = (p, se)
        p, se = wprop(X.PROT < 0.66 * E.refwt, E); row['PROT_ear_refwt'] = (p, se)
        p, se = wprop(X.PROT < 0.66 * E.BMXWT, E); row['PROT_ear_actualwt'] = (p, se)
        p, se = wprop(X.PROT < 0.66 * E.adjwt, E); row['PROT_ear_adjwt'] = (p, se)
        p, se = wprop(X.PROT < 1.2 * E.refwt, E); row['PROT_below_1.2_refwt'] = (p, se)
        p, se = wprop(X.PROT < 80, E); row['PROT_below_80g'] = (p, se)
        for n in AI:
            ai = np.array([(AI[n][s][a] if isinstance(AI[n][s], list) else AI[n][s]) for s, a in zip(E.sex, E.ab)])
            p, se = wprop(X[n] >= ai, E); row[f'{n}_above_AI'] = (p, se)
        ww = E.w / E.w.sum()
        row['mean_kcal'] = (float(np.sum(ww * X.KCAL)), None); row['mean_prot'] = (float(np.sum(ww * X.PROT)), None)
        row['mean_fibre_density'] = (float(np.sum(ww * (X.FIBE / X.KCAL * 1000))), None)
        res[sc] = row
    meta = dict(n_two_day=int(len(E)), n_eligible_any=int(d.eligible.sum()), wsum=float(E.w.sum()), share_female=float(np.sum(E.w * (E.sex == 'F')) / E.w.sum()),
                mean_age=float(np.sum(E.w * E.RIDAGEYR) / E.w.sum()), mean_bmi=float(np.sum(E.w * E.BMXBMI) / E.w.sum()),
                share_bmi30=float(np.sum(E.w * (E.BMXBMI >= 30)) / E.w.sum()), n_strata=int(E.SDMVSTRA.nunique()), n_psu=int(E.groupby(['SDMVSTRA', 'SDMVPSU']).ngroups))
    return res, meta, E.assign(**{f'U_{n}': U[n] for n in NUTS})
if __name__ == '__main__':
    out = {}
    for c in ('L', 'P'):
        for prot, supp in ((False, False), (True, False)) + (((False, True),) if c == 'P' else ()):
            res, meta, E = run(c, prot, supp)
            out[f'{c}{"_protect" if prot else ""}{"_supp" if supp else ""}'] = dict(meta=meta, res={k: {kk: [vv[0], vv[1]] for kk, vv in v.items()} for k, v in res.items()})
            if c == 'L' and not prot: E[['SEQN', 'sex', 'RIDAGEYR', 'BMXBMI', 'BMXWT', 'refwt', 'w'] + [f'U_{n}' for n in NUTS]].to_csv(f'{RES}/usual_L.csv', index=False)
    json.dump(out, open(f'{RES}/prevalence.json', 'w'), indent=1)
    for k, v in out.items():
        print(k, v['meta'])
        df = pd.DataFrame({sc: {n: round(100 * x[0], 1) for n, x in r.items() if not n.startswith('mean')} for sc, r in v['res'].items()}); print(df.to_string())
        print({sc: (round(r['mean_kcal'][0]), round(r['mean_prot'][0], 1)) for sc, r in v['res'].items()})
