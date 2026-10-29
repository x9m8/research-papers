"""Sensitivity analyses. Run after analysis.py. Writes results/sensitivity.json.
S1  strict scope: alerts whose text names leather (drops shoes/gloves identified by product type only)
S2  per-alert concentration = lowest reported value instead of highest
S3  periods and years by notification creation date instead of publication date
S4  Germany excluded / Germany only
S5  trend in raw counts (no offset) and with offset, 2016-2022 only (before the 2023 rise in total alerts)
S6  plain Poisson and negative binomial (NB2, method-of-moments) instead of quasi-Poisson
S7  values at exactly the 3 mg/kg limit excluded from concentration summaries
"""
import json, os
import numpy as np, pandas as pd
import statsmodels.api as sm, statsmodels.formula.api as smf
from scipy.stats import mannwhitneyu
from common import RES, RAW

A = pd.read_csv(f'{RES}/alerts.csv')
D = json.load(open(os.path.join(RAW, 'denominators_20261020.json')))
ALL = {int(k): v for k, v in D['all_alerts'].items()}; CHEM = {int(k): v for k, v in D['chemical_alerts'].items()}
out = {}


def yearly(S, datecol='pub_date'):
    yr = S[datecol].str[:4].astype(int)
    Y = pd.DataFrame(dict(year=range(2005, 2027)))
    Y['n'] = Y.year.map(yr.value_counts()).fillna(0).astype(int)
    Y['all'] = Y.year.map(ALL); Y['chem'] = Y.year.map(CHEM); Y['one'] = 1
    return Y


def trend(Y, y0, y1, offset='all', family='quasi'):
    from scipy.stats import norm
    d = Y[Y.year.between(y0, y1)].copy(); d['t'] = d.year - y0
    off = np.log(d[offset])
    pois = smf.glm('n ~ t', d, family=sm.families.Poisson(), offset=off).fit()
    disp = float(pois.pearson_chi2 / pois.df_resid)
    if family == 'nb':
        mu = pois.mu; alpha = max(1e-8, float(((d.n - mu) ** 2 - mu).sum() / (mu ** 2).sum()))
        fit = smf.glm('n ~ t', d, family=sm.families.NegativeBinomial(alpha=alpha), offset=off).fit()
        b, se, p = fit.params['t'], fit.bse['t'], float(fit.pvalues['t'])
    else:
        b, se = pois.params['t'], pois.bse['t']
        if family == 'quasi': se = se * np.sqrt(max(1.0, disp))
        p = float(2 * norm.sf(abs(b / se)))
    return dict(pct_per_year=float(100 * (np.exp(b) - 1)), ci=[float(100 * (np.exp(b - 1.96 * se) - 1)), float(100 * (np.exp(b + 1.96 * se) - 1))],
                p=p, n=int(d.n.sum()), dispersion=disp)


def conc(S, col='conc_max', datecol='pub_date'):
    c = S[S[col].notna()]; after = c[datecol] >= '2015-05-01'
    return dict(n=len(c), median_before=float(c[~after][col].median()), median_after=float(c[after][col].median()),
                gm_ratio=float(np.exp(np.log(c[after][col]).mean() - np.log(c[~after][col]).mean())),
                p=float(mannwhitneyu(c[~after][col], c[after][col]).pvalue))


def peak_vs_recent(Y):
    a = Y[Y.year.between(2013, 2015)]; b = Y[Y.year.between(2023, 2025)]
    r1, r2 = 1000 * a.n.sum() / a['all'].sum(), 1000 * b.n.sum() / b['all'].sum()
    return dict(per1000_2013_2015=float(r1), per1000_2023_2025=float(r2), fold=float(r1 / r2) if r2 else None)


S = A[A.scope]
base = yearly(S)
out['base'] = dict(trend=trend(base, 2016, 2025), conc=conc(S), peak_vs_recent=peak_vs_recent(base))
s1 = S[S.leather]
out['S1_strict_leather_word'] = dict(n=len(s1), trend=trend(yearly(s1), 2016, 2025), conc=conc(s1), peak_vs_recent=peak_vs_recent(yearly(s1)))
s2 = S.copy()
out['S2_min_value'] = dict(conc=conc(s2, 'conc_min'))
s3 = S[S.created.notna() & (S.created.str.len() == 10)]
y3 = yearly(s3, 'created')
out['S3_creation_date'] = dict(n=len(s3), trend=trend(y3, 2016, 2025), conc=conc(s3, datecol='created'), peak_year=int(y3.loc[y3.n.idxmax(), 'year']),
                               median_lag_days=float((pd.to_datetime(s3.pub_date) - pd.to_datetime(s3.created)).dt.days.median()))
de, nde = S[S.notifier == 'Germany'], S[S.notifier != 'Germany']
out['S4_germany'] = dict(excl_germany=dict(n=len(nde), trend=trend(yearly(nde), 2016, 2025), conc=conc(nde)),
                         germany_only=dict(n=len(de), trend=trend(yearly(de), 2016, 2025), conc=conc(de)))
out['S5_offsets'] = dict(raw_counts_2016_2025=trend(base, 2016, 2025, 'one'), all_2016_2022=trend(base, 2016, 2022, 'all'),
                         raw_counts_2016_2022=trend(base, 2016, 2022, 'one'), chem_2016_2022=trend(base, 2016, 2022, 'chem'))
out['S6_models'] = dict(poisson=trend(base, 2016, 2025, 'all', 'poisson'), nb=trend(base, 2016, 2025, 'all', 'nb'),
                       nb_chem=trend(base, 2016, 2025, 'chem', 'nb'))
s7 = S[S.conc_max != 3.0]
out['S7_excl_at_limit'] = dict(conc=conc(s7))
json.dump(out, open(f'{RES}/sensitivity.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
