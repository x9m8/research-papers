"""Main analyses of Safety Gate notifications for hexavalent chromium in leather and leather-type articles.
Run after build.py. Writes results/analysis.json.

Periods (by publication date)
  before   2005-01-01 .. 2015-04-30   (no EU-wide limit)
  after    2015-05-01 .. snapshot     (Regulation (EU) No 301/2014: Cr(VI) < 3 mg/kg in leather in contact with skin)
Full calendar years are used for trend models; 2026 is partial (to the snapshot date) and is excluded from them.
"""
import json, os
import numpy as np, pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import mannwhitneyu, beta
from common import RES, RAW

rng = np.random.default_rng(20261020)
A = pd.read_csv(f'{RES}/alerts.csv')
D = json.load(open(os.path.join(RAW, 'denominators_20261020.json')))
S = A[A.scope].copy()
S['after'] = S.pub_date >= '2015-05-01'
S['period'] = np.where(S.after, 'after', 'before')
LIMIT = 3.0
out = {}


def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k)
    return [float(lo), float(hi)]


def boot_median(x, B=10000):
    x = np.asarray(x); m = np.median(rng.choice(x, (B, len(x)), replace=True), axis=1)
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


# ---------- A. composition ----------
def share(col, g=S):
    vc = g[col].value_counts()
    return {str(k): dict(n=int(v), pct=float(100 * v / len(g))) for k, v in vc.items()}

out['A'] = dict(n=len(S), first=S.pub_date.min(), last=S.pub_date.max(),
                n_with_conc=int(S.conc_max.notna().sum()), n_leather_word=int(S.leather.sum()),
                ptype=share('ptype'), child=dict(n=int(S.child.sum()), pct=float(100 * S.child.mean())),
                components=dict(insole=int(S.comp_insole.sum()), lining=int(S.comp_lining.sum()), upper=int(S.comp_upper.sum()),
                                any=int((S.comp_insole | S.comp_lining | S.comp_upper).sum())),
                origin_top=dict(list(share('origin').items())[:12]),
                notifier_top=dict(list(share('notifier').items())[:12]), n_notifiers=int(S.notifier.nunique()), n_origins_known=int(S[S.origin != 'Unknown'].origin.nunique()),
                de_share_ci=[100 * x for x in cp(int((S.notifier == 'Germany').sum()), len(S))],
                origin_eu=dict(n=int(S.origin_eu.sum()), pct=float(100 * S.origin_eu.mean())),
                measures=share('measures'), risk_types=share('risk_types'),
                other_crvi_excluded=A[A.crvi & ~A.scope].category.value_counts().to_dict())

# ---------- B. annual series and trends ----------
yrs = range(2005, 2027)
Y = pd.DataFrame(dict(year=list(yrs)))
Y['n'] = Y.year.map(S.groupby('year').size()).fillna(0).astype(int)
Y['n_de'] = Y.year.map(S[S.notifier == 'Germany'].groupby('year').size()).fillna(0).astype(int)
Y['n_other'] = Y.n - Y.n_de
Y['all'] = Y.year.map({int(k): v for k, v in D['all_alerts'].items()})
Y['chem'] = Y.year.map({int(k): v for k, v in D['chemical_alerts'].items()})
Y['per1000_all'] = 1000 * Y.n / Y['all']
Y['per100_chem'] = 100 * Y.n / Y.chem
Y['notifiers'] = Y.year.map(S.groupby('year').notifier.nunique()).fillna(0).astype(int)
out['B_series'] = Y.to_dict(orient='records')
pk = Y.loc[Y.per1000_all.idxmax()]
out['B_peak'] = dict(year=int(pk.year), n=int(pk.n), per1000_all=float(pk.per1000_all))
last3 = Y[Y.year.between(2023, 2025)]
out['B_recent'] = dict(years='2023-2025', n=int(last3.n.sum()), all=int(last3['all'].sum()), chem=int(last3.chem.sum()),
                       per1000_all=float(1000 * last3.n.sum() / last3['all'].sum()),
                       per100_chem=float(100 * last3.n.sum() / last3.chem.sum()))
p13 = Y[Y.year.between(2013, 2015)]
out['B_peak3'] = dict(years='2013-2015', n=int(p13.n.sum()), per1000_all=float(1000 * p13.n.sum() / p13['all'].sum()),
                      per100_chem=float(100 * p13.n.sum() / p13.chem.sum()))


def trend(df, offset, family='quasi'):
    """Yearly counts on year with log offset. Main: quasi-Poisson (Poisson point estimate, standard errors scaled by
    the Pearson dispersion when it exceeds 1). Alternatives: 'poisson', 'nb' (NB2, method-of-moments alpha)."""
    d = df.copy(); d['t'] = d.year - d.year.min()
    pois = smf.glm('n ~ t', d, family=sm.families.Poisson(), offset=np.log(d[offset])).fit()
    disp = float(pois.pearson_chi2 / pois.df_resid)
    if family == 'nb':
        mu = pois.mu; alpha = max(1e-8, float(((d.n - mu) ** 2 - mu).sum() / (mu ** 2).sum()))
        fit = smf.glm('n ~ t', d, family=sm.families.NegativeBinomial(alpha=alpha), offset=np.log(d[offset])).fit()
        b, se, p = fit.params['t'], fit.bse['t'], float(fit.pvalues['t'])
    else:
        b, se = pois.params['t'], pois.bse['t']
        if family == 'quasi': se = se * np.sqrt(max(1.0, disp))
        from scipy.stats import norm
        p = float(2 * norm.sf(abs(b / se)))
    return dict(years=f'{d.year.min()}-{d.year.max()}', model=family, pct_per_year=float(100 * (np.exp(b) - 1)),
                ci=[float(100 * (np.exp(b - 1.96 * se) - 1)), float(100 * (np.exp(b + 1.96 * se) - 1))],
                p=p, dispersion=disp, n_alerts=int(d.n.sum()))

post = Y[Y.year.between(2016, 2025)]
pre = Y[Y.year.between(2010, 2014)]
out['B_trend'] = dict(after_all=trend(post, 'all'), after_chem=trend(post, 'chem'),
                      before_all=trend(pre, 'all'), before_chem=trend(pre, 'chem'))

# ---------- C. who notifies ----------
B = S[S.pub_date >= '2010-01-01']
C = {}
for per, g in B.groupby('period'):
    C[per] = dict(n=len(g), de=int((g.notifier == 'Germany').sum()), de_pct=float(100 * (g.notifier == 'Germany').mean()),
                  de_ci=[100 * v for v in cp(int((g.notifier == 'Germany').sum()), len(g))],
                  notifiers=int(g.notifier.nunique()), first_day=g.pub_date.min(), last_day=g.pub_date.max())
out['C_notifiers'] = C
# yearly non-German notifications: 2010-2014 vs 2016-2025 (full years)
nb_pre = Y[Y.year.between(2010, 2014)].n_other; nb_post = Y[Y.year.between(2016, 2025)].n_other
out['C_other_per_year'] = dict(before_2010_2014=float(nb_pre.mean()), after_2016_2025=float(nb_post.mean()),
                               de_before=float(Y[Y.year.between(2010, 2014)].n_de.mean()),
                               de_after=float(Y[Y.year.between(2016, 2025)].n_de.mean()))
# first-time notifiers after the EU limit
first = S.groupby('notifier').pub_date.min()
out['C_first_after'] = sorted(first[first >= '2015-05-01'].index.tolist())

# ---------- D. concentrations ----------
Cn = S[S.conc_max.notna()].copy()
Cn['mult'] = Cn.conc_max / LIMIT
Dd = dict(n=len(Cn), median=float(Cn.conc_max.median()), median_ci=boot_median(Cn.conc_max),
          iqr=[float(Cn.conc_max.quantile(.25)), float(Cn.conc_max.quantile(.75))], max=float(Cn.conc_max.max()),
          gm=float(np.exp(np.log(Cn.conc_max).mean())),
          le_2x=dict(n=int((Cn.mult <= 2).sum()), pct=float(100 * (Cn.mult <= 2).mean())),
          gt_10x=dict(n=int((Cn.mult > 10).sum()), pct=float(100 * (Cn.mult > 10).mean())),
          below_limit=int((Cn.conc_max < LIMIT).sum()), at_limit=int((Cn.conc_max == LIMIT).sum()))
for per, g in Cn.groupby('period'):
    Dd[per] = dict(n=len(g), median=float(g.conc_max.median()), median_ci=boot_median(g.conc_max),
                   iqr=[float(g.conc_max.quantile(.25)), float(g.conc_max.quantile(.75))],
                   gm=float(np.exp(np.log(g.conc_max).mean())),
                   gt_10x_pct=float(100 * (g.mult > 10).mean()), le_2x_pct=float(100 * (g.mult <= 2).mean()))
Dd['mannwhitney_p'] = float(mannwhitneyu(Cn[~Cn.after].conc_max, Cn[Cn.after].conc_max).pvalue)
Dd['gm_ratio_after_before'] = Dd['after']['gm'] / Dd['before']['gm']
# log-linear trend in concentration 2010-2025 (OLS on log10, and median regression)
T = Cn[Cn.year.between(2010, 2025)].copy(); T['t'] = T.year - 2010; T['l'] = np.log10(T.conc_max)
ols = smf.ols('l ~ t', T).fit(cov_type='HC1'); qr = smf.quantreg('l ~ t', T).fit(q=0.5)
Dd['trend_2010_2025'] = dict(n=len(T), ols_pct_per_year=float(100 * (10 ** ols.params['t'] - 1)),
                             ols_ci=[float(100 * (10 ** v - 1)) for v in ols.conf_int().loc['t']], ols_p=float(ols.pvalues['t']),
                             median_pct_per_year=float(100 * (10 ** qr.params['t'] - 1)),
                             median_ci=[float(100 * (10 ** v - 1)) for v in qr.conf_int().loc['t']], median_p=float(qr.pvalues['t']))
Dd['by_type'] = {k: dict(n=len(g), median=float(g.conc_max.median())) for k, g in Cn.groupby('ptype')}
Dd['by_year'] = {int(k): dict(n=len(g), median=float(g.conc_max.median())) for k, g in Cn.groupby('year')}
out['D_conc'] = Dd

# ---------- E. composition by period ----------
def by_period(col, top=None):
    o = {}
    for per, g in S.groupby('period'):
        vc = g[col].value_counts()
        o[per] = {str(k): dict(n=int(v), pct=float(100 * v / len(g)), ci=[100 * x for x in cp(int(v), len(g))]) for k, v in (vc.head(top) if top else vc).items()}
        o[per]['_n'] = len(g)
    return o

S['origin_grp'] = np.select([S.origin.str.contains('China'), S.origin.isin(['India', 'Pakistan', 'Bangladesh']),
                             S.origin_eu, S.origin.eq('Unknown')], ['China', 'South Asia', 'EU', 'Unknown'], 'Other')
out['E'] = dict(ptype=by_period('ptype'), origin=by_period('origin_grp'), child={p: float(100 * g.child.mean()) for p, g in S.groupby('period')},
                gloves_ppe={p: int(((g.ptype == 'gloves') & (g.category == 'PROTECTIVE_EQUIPMENT')).sum()) for p, g in S.groupby('period')})
json.dump(out, open(f'{RES}/analysis.json', 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps({k: out[k] for k in ['B_peak', 'B_recent', 'B_peak3', 'B_trend', 'C_notifiers', 'C_other_per_year']}, indent=1))
print(json.dumps({k: v for k, v in Dd.items() if k not in ('by_year',)}, indent=1))
