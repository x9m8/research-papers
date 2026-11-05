"""Paths, constants and the minimum-wage schedule shared by all scripts."""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'data', 'raw')
DER = os.path.join(ROOT, 'data', 'derived')
RES = os.path.join(ROOT, 'results')
FIG = os.path.join(ROOT, 'figures')
QCEW_FILE = 'qcew_ny_nj_pa_quarterly.csv'

NYC = {'36005', '36047', '36061', '36081', '36085'}    # Bronx, Kings, New York, Queens, Richmond
LI = {'36059', '36103'}                                # Nassau, Suffolk
WESTCHESTER = {'36119'}
FIRST_Q, LAST_Q = (2014, 1), (2026, 1)
BASE_YEARS = (2014, 2015, 2016)                        # seasonal baseline (before the regional split of 31 Dec 2016)
COVID = (2020, 2021)                                   # years excluded from estimation
INDUSTRIES = {'722': 'Food services and drinking places', '722511': 'Full-service restaurants',
              '722513': 'Limited-service restaurants', '10': 'Total private'}
SEED = 20261028


def qindex(y, q):
    return int(y) * 4 + int(q) - 1


QUARTERS = [(y, q) for y in range(FIRST_Q[0], LAST_Q[0] + 1) for q in range(1, 5) if qindex(y, q) <= qindex(*LAST_Q)]


def effective_quarter(date):
    """Quarter in which a rate applies for the whole quarter. A rate effective 31 Dec applies from Q1 of the next year."""
    d = pd.Timestamp(date)
    if d.month == 12 and d.day == 31:
        return qindex(d.year + 1, 1)
    return qindex(d.year, (d.month - 1) // 3 + 1) if d.day == 1 and d.month in (1, 4, 7, 10) else qindex(d.year, (d.month - 1) // 3 + 1) + 1


def schedule():
    """Quarterly table of the rates used in the analysis (from data/raw/minwage_schedule.csv, coded from official sources)."""
    s = pd.read_csv(os.path.join(RAW, 'minwage_schedule.csv'))
    s['qi'] = s.effective_date.map(effective_quarter)
    out = pd.DataFrame({'qi': [qindex(y, q) for y, q in QUARTERS], 'year': [y for y, q in QUARTERS], 'qtr': [q for y, q in QUARTERS]})

    def path(region, rtype, fallback=None):
        r = s[(s.region == region) & (s.rate_type == rtype)].sort_values('qi')
        vals = []
        for qi in out.qi:
            prior = r[r.qi <= qi]
            vals.append(prior.hourly_rate.iloc[-1] if len(prior) else np.nan)
        v = pd.Series(vals, index=out.index, dtype=float)
        if fallback is not None:
            v = v.fillna(fallback)
        return v

    allny = path('NY_ALL', 'general')
    out['mw_li'] = path('NY_LIW', 'general').fillna(allny)
    out['mw_ros'] = path('NY_ROS', 'general').fillna(allny)
    out['mw_pa'] = path('PA', 'general')
    out['ff_outside_nyc'] = path('NY_OUTSIDE_NYC', 'fast_food')
    # fast-food chains pay the higher of the fast-food rate and the general rate
    out['ff_li'] = np.fmax(out.ff_outside_nyc.fillna(0), out.mw_li)
    out['ff_ros'] = np.fmax(out.ff_outside_nyc.fillna(0), out.mw_ros)
    # tipped food-service cash wage: regional only from 31 Dec 2016; before that the rate was statewide (gap zero)
    out['tip_li'] = path('NY_LIW', 'tipped_food_cash')
    out['tip_ros'] = path('NY_ROS', 'tipped_food_cash')
    out['gap_general'] = np.log(out.mw_li) - np.log(out.mw_ros)
    out['gap_ff'] = np.log(out.ff_li) - np.log(out.ff_ros)
    out['gap_tip'] = (np.log(out.tip_li) - np.log(out.tip_ros)).fillna(0.0)
    return out


def region_of(fips):
    if fips.startswith('42'):
        return 'PA'
    if fips.startswith('34'):
        return 'NJ'
    if fips in NYC:
        return 'NYC'
    if fips in LI:
        return 'LI'
    if fips in WESTCHESTER:
        return 'WES'
    return 'ROS'


def ols(y, X):
    """OLS with classical and HC1 standard errors. Returns coefficients, se_hc1."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    XtX = np.linalg.pinv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
    n, k = X.shape
    V = XtX @ (X.T * e ** 2) @ X @ XtX * n / max(n - k, 1)
    return b, np.sqrt(np.diag(V)), e


def newey_west_se(y, X, lags=4):
    X = np.asarray(X, float); y = np.asarray(y, float)
    XtX = np.linalg.pinv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = u[L:].T @ u[:-L]; S += w * (G + G.T)
    V = XtX @ S @ XtX
    return b, np.sqrt(np.diag(V))
