"""Paths and shared estimation helpers (NumPy only, so the scripts also run under Pyodide)."""
import os
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) if '__file__' in globals() else '/pkg'
RAW, DER, RES, FIG = (os.path.join(ROOT, d) for d in ('data/raw', 'data/derived', 'results', 'figures'))
for d in (DER, RES, FIG):
    os.makedirs(d, exist_ok=True)

YEARS_Q = list(range(2015, 2026))   # QCEW annual averages
YEARS_D = list(range(2019, 2025))   # Part D data years
BASE, END_D, END_Q = 2019, 2024, 2025
DROP_STATES = {'02', '09'}          # Alaska and Connecticut: county definitions changed during the period
IND = {'fsr': 'Full-service restaurants (722511)', 'lsr': 'Limited-service restaurants (722513)',
       'pharm': 'Pharmacies (446110/456110)', 'acc': 'Accommodation (721)', 'groc': 'Supermarkets and grocery (445110)',
       'tot': 'All private industries'}


def _demean(a, g, w):
    """Weighted within-group demeaning of the columns of a (n x k) by integer group codes g."""
    a = np.asarray(a, float)
    if a.ndim == 1:
        a = a[:, None]
    sw = np.bincount(g, weights=w)
    out = np.empty_like(a)
    for j in range(a.shape[1]):
        m = np.bincount(g, weights=w * a[:, j]) / sw
        out[:, j] = a[:, j] - m[g]
    return out


def ols_fe(y, X, fe, cl, w=None, names=None):
    """OLS (or WLS) of y on X with one set of absorbed fixed effects 'fe' (integer codes) and
    cluster-robust standard errors by 'cl'. Fixed effects are nested within clusters in every use here,
    so the small-sample factor counts only the slope coefficients. Returns dict with b, se, V, n, G, df."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    n = len(y)
    w = np.ones(n) if w is None else np.asarray(w, float)
    fe = np.unique(fe, return_inverse=True)[1]
    yd = _demean(y, fe, w)[:, 0]; Xd = _demean(X, fe, w)
    sw = np.sqrt(w)
    Xs, ys = Xd * sw[:, None], yd * sw
    XtX_inv = np.linalg.pinv(Xs.T @ Xs)
    b = XtX_inv @ Xs.T @ ys
    u = ys - Xs @ b
    clu = np.unique(cl, return_inverse=True)[1]
    G = clu.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, clu, Xs * u[:, None])
    k = X.shape[1]
    c = G / (G - 1) * (n - 1) / (n - k)
    V = c * XtX_inv @ (S.T @ S) @ XtX_inv
    r2w = 1 - (u @ u) / (ys @ ys) if ys @ ys > 0 else np.nan
    return {'b': b, 'se': np.sqrt(np.diag(V)), 'V': V, 'n': int(n), 'G': int(G), 'df': int(G - 1),
            'names': names, 'r2_within': float(r2w)}


def tcrit(df, a=0.05):
    from scipy import stats
    return float(stats.t.ppf(1 - a / 2, df))


def tpval(t, df):
    from scipy import stats
    return float(2 * stats.t.sf(abs(t), df))


def mde(se, df, power=0.8, a=0.05):
    """Minimum detectable effect for a two-sided test at level a with the given power."""
    from scipy import stats
    return float((stats.t.ppf(1 - a / 2, df) + stats.t.ppf(power, df)) * se)


def wald(b, V, df):
    """Joint F test that all elements of b are zero (cluster-robust V), F(q, df)."""
    from scipy import stats
    q = len(b)
    F = float(b @ np.linalg.pinv(V) @ b / q)
    return F, float(stats.f.sf(F, q, df))
