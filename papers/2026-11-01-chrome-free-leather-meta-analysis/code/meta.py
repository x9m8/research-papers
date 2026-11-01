"""Step 3: effect sizes and random-effects models.
lnRR = ln(mean_CF / mean_Cr) for tensile strength, elongation at break and tear; mean difference (CF - Cr, degC) for Ts.
Multilevel model: y = mu + u_study + w_effect + e, e ~ N(0, V), with V carrying the shared-control covariance
(Var of the chrome part of lnRR) between chrome-free arms compared with the same chrome control. REML.
Writes results/effects.csv, results/meta.json, results/ts_descriptive.csv."""
import json
import numpy as np, pandas as pd
from scipy import optimize, stats
from common import RES, EXT

ex = pd.read_csv(f'{EXT}/extraction.csv')
rp = pd.read_csv(f'{EXT}/replicates.csv')
sc = pd.read_csv(f'{EXT}/study_characteristics.csv').set_index('study_id')

# ---- replicate-level data -> arm summaries (aguilar2023: four values per arm)
rows = []
for (sid, o), g in rp.groupby(['study_id', 'outcome']):
    cr = g[g.arm == 'cr'].value
    for aid, a in g[g.arm == 'cf'].groupby('arm_id'):
        r0 = a.iloc[0]
        rows.append(dict(study_id=sid, doi=r0.doi, arm_id=aid, cf_agent=r0.cf_agent, cf_class=r0.cf_class, outcome=o, unit=r0.unit,
                         mean_cf=a.value.mean(), sd_cf=a.value.std(ddof=1), n_cf=len(a), mean_cr=cr.mean(), sd_cr=cr.std(ddof=1), n_cr=len(cr),
                         n_stated='yes', sd_stated='replicates', source=r0.source, ts_cens_cr=0, developer='yes', matched_stated='no',
                         stage='unclear', species='unclear', notes='summarised from replicate values'))
d = pd.concat([ex, pd.DataFrame(rows)], ignore_index=True)
d['n_cf_imputed'] = d.n_cf.isna(); d['n_cr_imputed'] = d.n_cr.isna()
d['has_sd'] = d.sd_cf.notna() & d.sd_cr.notna()
d['integrity_flag'] = d.study_id.map(sc.integrity_flag).fillna(0).astype(int)
d['comparator_source'] = d.study_id.map(sc.comparator_source)
d['year'] = d.study_id.map(sc.year)
# arms that share a chrome control: same study, outcome and (for direction-specific designs) same direction suffix
d['control_id'] = [f"{s}|{o}|{a.split('_')[-1] if s in ('bielak2022', 'cavali2022') else 'C'}" for s, o, a in zip(d.study_id, d.outcome, d.arm_id)]

# median coefficient of variation by outcome (rows with SD) for SD imputation in a sensitivity analysis
cv = {}
for o in ['tensile', 'elongation', 'tear']:
    s = d[(d.outcome == o) & d.has_sd]
    cv[o] = float(np.median(np.r_[s.sd_cf / s.mean_cf, s.sd_cr / s.mean_cr]))

def effects(df, n_default=3, impute_sd=False):
    df = df.copy()
    df['n_cf_u'] = df.n_cf.fillna(n_default); df['n_cr_u'] = df.n_cr.fillna(n_default)
    if impute_sd:
        for o, c in cv.items():
            m = (df.outcome == o) & ~df.has_sd
            df.loc[m & df.sd_cf.isna(), 'sd_cf'] = c * df.loc[m & df.sd_cf.isna(), 'mean_cf']
            df.loc[m & df.sd_cr.isna(), 'sd_cr'] = c * df.loc[m & df.sd_cr.isna(), 'mean_cr']
    df['yi'] = np.log(df.mean_cf / df.mean_cr)
    df['v_cf'] = df.sd_cf ** 2 / (df.n_cf_u * df.mean_cf ** 2)
    df['v_cr'] = df.sd_cr ** 2 / (df.n_cr_u * df.mean_cr ** 2)
    df['vi'] = df.v_cf + df.v_cr
    return df

def vmat(df):
    V = np.diag(df.vi.values.astype(float))
    cid = np.asarray(df.control_id, dtype=object); vcr = np.asarray(df.v_cr, dtype=float)
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if cid[i] == cid[j]: V[i, j] = V[j, i] = vcr[i]
    return V

def rma_mv(df, X=None):
    """Two-level random-effects meta-analysis (study, effect within study) by REML; returns dict."""
    y = df.yi.values.astype(float); V = vmat(df); k = len(y)
    X = np.ones((k, 1)) if X is None else X
    p = X.shape[1]
    sid = np.asarray(df.study_id, dtype=object)
    S = (sid[:, None] == sid[None, :]).astype(float)
    I = np.eye(k)
    def parts(lt):
        t2s, t2w = np.exp(lt)
        M = V + t2s * S + t2w * I
        Mi = np.linalg.inv(M)
        XtMiX = X.T @ Mi @ X
        b = np.linalg.solve(XtMiX, X.T @ Mi @ y)
        r = y - X @ b
        return M, Mi, XtMiX, b, r
    def nll(lt):
        M, Mi, XtMiX, b, r = parts(lt)
        return 0.5 * (np.linalg.slogdet(M)[1] + np.linalg.slogdet(XtMiX)[1] + r @ Mi @ r)
    best = None
    for start in [(-4, -4), (-2, -6), (-6, -2), (-1, -1), (-8, -8)]:
        res = optimize.minimize(nll, np.array(start, float), method='Nelder-Mead', options=dict(xatol=1e-8, fatol=1e-10, maxiter=20000))
        if best is None or res.fun < best.fun: best = res
    lt = np.clip(best.x, -30, 5)
    M, Mi, XtMiX, b, r = parts(lt)
    vb = np.linalg.inv(XtMiX)
    t2s, t2w = np.exp(lt)
    t2s = 0.0 if t2s < 1e-10 else t2s; t2w = 0.0 if t2w < 1e-10 else t2w
    nstud = df.study_id.nunique()
    # cluster-robust (CR1) variance by study; with an intercept-only model dominated by the study-level variance this is
    # close to the model-based SE by construction, so it is reported as a consistency check, not an independent one
    W = vb @ X.T @ Mi
    meat = np.zeros((p, p))
    for s in np.unique(sid):
        m = sid == s
        u = W[:, m] @ r[m]; meat += np.outer(u, u)
    vrob = meat * nstud / (nstud - p)
    se = np.sqrt(np.diag(vb)); se_r = np.sqrt(np.diag(vrob))
    dfree = nstud - p
    tcrit = stats.t.ppf(0.975, dfree)
    tpi = stats.t.ppf(0.975, max(nstud - 2, 1))  # prediction interval: t on k - 2 df (Riley et al. 2011)
    w = 1 / df.vi.values
    vtyp = (k - 1) * w.sum() / (w.sum() ** 2 - (w ** 2).sum())
    out = dict(k_effects=int(k), k_studies=int(nstud), b=b.tolist(), se=se.tolist(), se_robust=se_r.tolist(),
               ci_lo=(b - tcrit * se).tolist(), ci_hi=(b + tcrit * se).tolist(),
               ci_lo_robust=(b - tcrit * se_r).tolist(), ci_hi_robust=(b + tcrit * se_r).tolist(),
               p=(2 * stats.t.sf(np.abs(b / se), dfree)).tolist(), df=int(dfree), tau2_study=float(t2s), tau2_within=float(t2w),
               I2=float((t2s + t2w) / (t2s + t2w + vtyp)), I2_study=float(t2s / (t2s + t2w + vtyp)))
    if p == 1:
        sp = np.sqrt(vb[0, 0] + t2s + t2w)
        out.update(pi_lo=float(b[0] - tpi * sp), pi_hi=float(b[0] + tpi * sp))
        Q = float(r @ np.linalg.inv(V) @ r); out.update(Q=Q, Q_df=int(k - 1), Q_p=float(stats.chi2.sf(Q, k - 1)))
    return out

def summ(fit, ratio=True):
    f = (lambda x: float(np.exp(x))) if ratio else float
    return dict(est=f(fit['b'][0]), lo=f(fit['ci_lo'][0]), hi=f(fit['ci_hi'][0]), lo_rob=f(fit['ci_lo_robust'][0]), hi_rob=f(fit['ci_hi_robust'][0]),
                pi_lo=f(fit['pi_lo']), pi_hi=f(fit['pi_hi']), p=fit['p'][0], k_effects=fit['k_effects'], k_studies=fit['k_studies'],
                tau2_study=fit['tau2_study'], tau2_within=fit['tau2_within'], I2=fit['I2'], Q=fit['Q'], Q_df=fit['Q_df'], Q_p=fit['Q_p'])

R = dict(cv_median=cv, models={}, sensitivity={}, moderators={}, small_study={}, loo={}, reporting={}, two_stage={})
base = d[d.outcome.isin(['tensile', 'elongation', 'tear'])]
E = effects(base)
prim = lambda df: df[df.has_sd & (df.integrity_flag != 1)]  # flag 1 (generated-text residue) excluded; flag 2 (duplicate publication) retained

for o in ['tensile', 'elongation', 'tear']:
    P = prim(E[E.outcome == o])
    fit = rma_mv(P); R['models'][o] = summ(fit)
    sens = {}
    for nd in (2, 5):
        Q = prim(effects(base, n_default=nd)); sens[f'n_missing_{nd}'] = summ(rma_mv(Q[Q.outcome == o]))
    Qi = effects(base, impute_sd=True); Qi = Qi[(Qi.outcome == o) & (Qi.integrity_flag != 1) & Qi.sd_cf.notna()]
    sens['impute_sd'] = summ(rma_mv(Qi))
    Qf = E[(E.outcome == o) & E.has_sd]; sens['with_flagged'] = summ(rma_mv(Qf)) if Qf.study_id.nunique() > P.study_id.nunique() else None
    Qn = P[~P.study_id.isin(['jia2022'])]; sens['without_jia2022'] = summ(rma_mv(Qn)) if len(Qn) < len(P) else None
    Qc = P[P.comparator_source == 'in-study']; sens['in_study_comparator_only'] = summ(rma_mv(Qc)) if Qc.study_id.nunique() >= 3 else None
    Qd = P[P.study_id.map(sc.cf_developer) == 'no']; sens['non_developer_only'] = summ(rma_mv(Qd)) if Qd.study_id.nunique() >= 3 else None
    nall = P.groupby('study_id').n_stated.apply(lambda x: x.eq('yes').all())
    Qs = P[P.study_id.map(nall)]; sens['n_stated_only'] = summ(rma_mv(Qs)) if Qs.study_id.nunique() >= 3 else None
    for lab, drop in [('without_gomezgarcia2026', ['gomezgarcia2026']), ('without_aguilar2023', ['aguilar2023']), ('without_both_outliers', ['gomezgarcia2026', 'aguilar2023'])]:
        Qx = P[~P.study_id.isin(drop)]; sens[lab] = summ(rma_mv(Qx)) if len(Qx) < len(P) else None
    # simple two-stage check: average arms within study (inverse variance), then Paule-Mandel ('iterated') random effects
    st = P.groupby('study_id').apply(lambda g: pd.Series(dict(y=np.average(g.yi, weights=1 / g.vi), v=1 / (1 / g.vi).sum())), include_groups=False)
    from statsmodels.stats.meta_analysis import combine_effects
    ce = combine_effects(st.y.values, st.v.values, method_re='iterated')
    sf = ce.summary_frame()
    R['two_stage'][o] = dict(k=int(len(st)), est=float(np.exp(sf.loc['random effect', 'eff'])), lo=float(np.exp(sf.loc['random effect', 'ci_low'])),
                             hi=float(np.exp(sf.loc['random effect', 'ci_upp'])), tau2=float(ce.tau2))
    R['sensitivity'][o] = sens
    # leave-one-study-out
    loo = {}
    for s in P.study_id.unique():
        loo[s] = float(np.exp(rma_mv(P[P.study_id != s])['b'][0]))
    R['loo'][o] = dict(min=min(loo.values()), max=max(loo.values()), by_study=loo)
    # moderator: chrome-free class (cell means), and developer status
    cls = sorted(P.cf_class.unique())
    X = np.column_stack([(P.cf_class == c).astype(float) for c in cls])
    fm = rma_mv(P, X)
    R['moderators'][o] = dict(cf_class={c: dict(est=float(np.exp(fm['b'][i])), lo=float(np.exp(fm['ci_lo'][i])), hi=float(np.exp(fm['ci_hi'][i])),
                                            k_effects=int((P.cf_class == c).sum()), k_studies=int(P[P.cf_class == c].study_id.nunique())) for i, c in enumerate(cls)})
    def devmod(Pd):
        dev = (Pd.study_id.map(sc.cf_developer) == 'yes').astype(float).values
        if not (0 < dev.sum() < len(dev)): return None
        fd = rma_mv(Pd, np.column_stack([np.ones(len(Pd)), dev]))
        return dict(ratio_of_ratios=float(np.exp(fd['b'][1])), lo=float(np.exp(fd['ci_lo'][1])), hi=float(np.exp(fd['ci_hi'][1])), p=fd['p'][1],
                    k_dev_studies=int(Pd[dev == 1].study_id.nunique()), k_nondev_studies=int(Pd[dev == 0].study_id.nunique()))
    R['moderators'][o]['developer'] = devmod(P)
    R['moderators'][o]['developer_in_study_only'] = devmod(P[P.comparator_source == 'in-study'])
    R['moderators'][o]['developer_without_both_outliers'] = devmod(P[~P.study_id.isin(['gomezgarcia2026', 'aguilar2023'])])
    # small-study test: SE as moderator
    fe = rma_mv(P, np.column_stack([np.ones(len(P)), np.sqrt(P.vi.values)]))
    R['small_study'][o] = dict(slope=fe['b'][1], lo=fe['ci_lo'][1], hi=fe['ci_hi'][1], p=fe['p'][1])

E.to_csv(f'{RES}/effects.csv', index=False)

# ---- shrinkage temperature: descriptive mean differences
T = d[d.outcome == 'ts'].copy()
T['md'] = T.mean_cf - T.mean_cr
T['cens_label'] = T.ts_cens_cr.map({0: 'exact, within ISO 3380 range', 1: 'exact but above 100 C', 2: 'reported as lower bound (>95 C)'})
T[['study_id', 'arm_id', 'cf_agent', 'cf_class', 'mean_cf', 'sd_cf', 'mean_cr', 'sd_cr', 'md', 'ts_cens_cr', 'cens_label', 'integrity_flag', 'source']].to_csv(f'{RES}/ts_descriptive.csv', index=False)
Tp = T[T.integrity_flag != 1]
st_md = Tp.groupby('study_id').md.mean()
R['ts'] = dict(n_arms=int(len(Tp)), n_studies=int(Tp.study_id.nunique()), n_arms_cf_higher=int((Tp.md > 0).sum()),
               md_median_arm=float(Tp.md.median()), md_min=float(Tp.md.min()), md_max=float(Tp.md.max()),
               md_median_study=float(st_md.median()), n_arms_censored_or_above100=int((Tp.ts_cens_cr > 0).sum()),
               n_studies_with_sd=int(Tp[Tp.sd_cf.notna() & Tp.sd_cr.notna()].study_id.nunique()),
               cr_ts_values=sorted(Tp.drop_duplicates('study_id').mean_cr.tolist()),
               cf_ts_min=float(Tp.mean_cf.min()), cf_ts_max=float(Tp.mean_cf.max()),
               md_median_excl_censored=float(Tp[Tp.ts_cens_cr != 2].md.median()),
               flagged_study_md=T[T.integrity_flag == 1].md.tolist())

# ---- reporting characteristics (study level, all 24 included studies)
studies = sc.index.tolist()
ds = d.groupby('study_id')
R['reporting'] = dict(
    n_studies=len(studies),
    n_stated_all_arms=int(sum(ds.get_group(s).n_stated.eq('yes').all() for s in studies)),
    n_stated_any=int(sum(ds.get_group(s).n_stated.isin(['yes', 'partial']).any() for s in studies)),
    sd_any=int(sum(ds.get_group(s).has_sd.any() for s in studies)),
    matched_stated=int(sum(ds.get_group(s).matched_stated.eq('yes').any() for s in studies)),
    developer=int((sc.cf_developer == 'yes').sum()),
    comparator_in_study=int((sc.comparator_source == 'in-study').sum()),
    comparator_other=int((sc.comparator_source != 'in-study').sum()),
    integrity_flag_generated_text=int((sc.integrity_flag == 1).sum()), integrity_flag_duplicate=int((sc.integrity_flag == 2).sum()),
    species=sc.species.value_counts().to_dict(),
    classes_arms=d[d.outcome.isin(['tensile', 'elongation', 'tear', 'ts'])].drop_duplicates(['study_id', 'arm_id']).cf_class.value_counts().to_dict(),
    years=dict(min=int(sc.year.min()), max=int(sc.year.max()), n_2020_on=int((sc.year >= 2020).sum())),
    n_arms_total=int(d.drop_duplicates(['study_id', 'arm_id']).shape[0]))

# descriptive direction counts on all arms with means (incl. those without SD), by outcome
dd = d[d.integrity_flag != 1]
R['direction'] = {o: dict(n_arms=int((dd.outcome == o).sum()), n_cf_lower=int(((dd.outcome == o) & (dd.mean_cf < dd.mean_cr)).sum()),
                          n_studies=int(dd[dd.outcome == o].study_id.nunique())) for o in ['tensile', 'elongation', 'tear', 'ts']}
json.dump(R, open(f'{RES}/meta.json', 'w'), indent=1, default=float)
for o in ['tensile', 'elongation', 'tear']:
    m = R['models'][o]; print(o, {k: round(v, 3) if isinstance(v, float) else v for k, v in m.items()})
    print('   two-stage', R['two_stage'][o]); print('   sens', {k: (round(v['est'], 3) if v else None) for k, v in R['sensitivity'][o].items()})
    print('   loo', round(R['loo'][o]['min'], 3), round(R['loo'][o]['max'], 3), ' small-study', R['small_study'][o])
    print('   classes', {c: (round(v['est'], 3), v['k_studies']) for c, v in R['moderators'][o]['cf_class'].items()}, R['moderators'][o].get('developer'))
print('ts', R['ts']); print('reporting', R['reporting']); print('direction', R['direction'])
