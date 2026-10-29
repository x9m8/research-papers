"""Small econometrics helpers: OLS and just-identified 2SLS with HC1 or state-clustered standard errors,
first-stage strength (robust / cluster Wald F on the excluded instrument; with one instrument this equals the
Montiel Olea-Pflueger effective F), and Anderson-Rubin confidence sets by test inversion over a grid."""
import numpy as np, pandas as pd
from scipy import stats

def _prep(df, cols):
    return df.dropna(subset=cols).copy()

def _vcov(X, u, kind, groups=None, Xinv=None):
    n, k = X.shape
    if Xinv is None: Xinv = np.linalg.inv(X.T @ X)
    if kind == 'hc1':
        meat = (X * u[:, None] ** 2).T @ X
        return n / (n - k) * Xinv @ meat @ Xinv
    if kind == 'hc0':
        meat = (X * u[:, None] ** 2).T @ X
        return Xinv @ meat @ Xinv
    if kind == 'cluster':
        g = pd.factorize(groups)[0]; G = g.max() + 1
        S = np.zeros((G, k)); np.add.at(S, g, X * u[:, None])
        c = G / (G - 1) * (n - 1) / (n - k)
        return c * Xinv @ (S.T @ S) @ Xinv
    raise ValueError(kind)

def design(df, cols, fe=None):
    X = df[cols].astype(float).values
    names = list(cols)
    if fe is not None:
        D = pd.get_dummies(df[fe].astype(int), prefix='fe', drop_first=True, dtype=float)
        X = np.column_stack([X, D.values]); names += list(D.columns)
    X = np.column_stack([np.ones(len(df)), X]); names = ['const'] + names
    return X, names

def ols(df, y, xs, kind='hc1', cluster='stfips', fe=None, w=None):
    d = _prep(df, [y] + xs + ([w] if w else []) + ([fe] if fe else []))
    X, names = design(d, xs, fe); Y = d[y].values.astype(float)
    if w:
        sw = np.sqrt(d[w].values / d[w].values.mean()); X = X * sw[:, None]; Y = Y * sw
    Xinv = np.linalg.inv(X.T @ X); b = Xinv @ X.T @ Y; u = Y - X @ b
    V = _vcov(X, u, kind, d[cluster].values if kind == 'cluster' else None, Xinv)
    r2 = 1 - (u @ u) / ((Y - Y.mean()) @ (Y - Y.mean())) if not w else np.nan
    se = np.sqrt(np.diag(V))
    return {'b': dict(zip(names, b)), 'se': dict(zip(names, se)), 'n': len(d), 'r2': r2}

def iv(df, y, x, z, ctrls, kind='hc1', cluster='stfips', fe=None, w=None, ar=True, grid=None):
    """Just-identified 2SLS of y on x instrumented by z, with exogenous controls."""
    d = _prep(df, [y, x, z] + ctrls + ([w] if w else []) + ([fe] if fe else []))
    C, cn = design(d, ctrls, fe)
    Y = d[y].values.astype(float); Xe = d[x].values.astype(float); Z = d[z].values.astype(float)
    if w:
        sw = np.sqrt(d[w].values / d[w].values.mean()); C = C * sw[:, None]; Y = Y * sw; Xe = Xe * sw; Z = Z * sw
    g = d[cluster].values
    # first stage
    F1 = np.column_stack([Z, C]); F1inv = np.linalg.inv(F1.T @ F1); p = F1inv @ F1.T @ Xe; v = Xe - F1 @ p
    Vp = _vcov(F1, v, kind, g if kind == 'cluster' else None, F1inv)
    fs_b, fs_se = p[0], np.sqrt(Vp[0, 0]); fs_F = (fs_b / fs_se) ** 2
    fs_F_homo = fs_b ** 2 / (F1inv[0, 0] * (v @ v) / (len(d) - F1.shape[1]))
    # second stage
    Xh = np.column_stack([F1 @ p, C]); X = np.column_stack([Xe, C]); W = F1
    A = np.linalg.inv(Xh.T @ X); b = A @ Xh.T @ Y; u = Y - X @ b
    n, k = X.shape
    if kind == 'cluster':
        gg = pd.factorize(g)[0]; G = gg.max() + 1; S = np.zeros((G, k)); np.add.at(S, gg, Xh * u[:, None])
        V = G / (G - 1) * (n - 1) / (n - k) * A @ (S.T @ S) @ A.T
    else:
        meat = (Xh * u[:, None] ** 2).T @ Xh; V = (n / (n - k) if kind == 'hc1' else 1.0) * A @ meat @ A.T
    se = np.sqrt(V[0, 0])
    # reduced form
    r = F1inv @ F1.T @ Y; ur = Y - F1 @ r; Vr = _vcov(F1, ur, kind, g if kind == 'cluster' else None, F1inv)
    out = {'b': b[0], 'se': se, 'n': n, 'fs_b': fs_b, 'fs_se': fs_se, 'fs_F': fs_F, 'fs_F_homo': fs_F_homo,
           'rf_b': r[0], 'rf_se': np.sqrt(Vr[0, 0]), 'p': 2 * stats.norm.sf(abs(b[0] / se)),
           'ctrl_b': dict(zip(cn, b[1:])), 'ctrl_se': dict(zip(cn, np.sqrt(np.diag(V))[1:]))}
    if ar:
        out['ar'] = ar_set(Y, Xe, F1, F1inv, kind, g, grid)
    return out

def ar_set(Y, Xe, F1, F1inv, kind, g, grid=None, crit=stats.chi2.ppf(0.95, 1)):
    """Anderson-Rubin 95% confidence set, solved exactly. For a candidate beta, regress Y - beta*X on (Z, controls) and
    test the Z coefficient with the same robust/cluster variance; the coefficient is ry - beta*rx and its variance is a
    quadratic in beta, so the acceptance region {t^2 < crit} is the solution set of a quadratic inequality."""
    n, k = F1.shape
    ry = F1inv @ F1.T @ Y; rx = F1inv @ F1.T @ Xe
    uy = Y - F1 @ ry; ux = Xe - F1 @ rx
    h = F1 @ F1inv[0]                                  # influence weights for the Z coefficient
    if kind == 'cluster':
        gg = pd.factorize(g)[0]; G = gg.max() + 1
        sy = np.zeros(G); sx = np.zeros(G); np.add.at(sy, gg, h * uy); np.add.at(sx, gg, h * ux)
        c = G / (G - 1) * (n - 1) / (n - k)
    else:
        sy, sx = h * uy, h * ux; c = n / (n - k) if kind == 'hc1' else 1.0
    A, B, C = c * (sy @ sy), c * (sy @ sx), c * (sx @ sx)
    # (ry0 - b rx0)^2 - crit (A - 2 B b + C b^2) < 0  <=>  a2 b^2 + a1 b + a0 < 0
    a2 = rx[0] ** 2 - crit * C; a1 = -2 * (ry[0] * rx[0] - crit * B); a0 = ry[0] ** 2 - crit * A
    disc = a1 ** 2 - 4 * a2 * a0
    if abs(a2) < 1e-15:
        return {'type': 'unbounded', 'lo': None, 'hi': None, 'pieces': []}
    if disc < 0:
        return ({'type': 'empty', 'lo': None, 'hi': None, 'pieces': []} if a2 > 0 else
                {'type': 'unbounded (whole real line)', 'lo': None, 'hi': None, 'pieces': [[-np.inf, np.inf]]})
    r1, r2 = sorted([(-a1 - np.sqrt(disc)) / (2 * a2), (-a1 + np.sqrt(disc)) / (2 * a2)])
    if a2 > 0:
        return {'type': 'bounded interval', 'lo': float(r1), 'hi': float(r2), 'pieces': [[float(r1), float(r2)]]}
    return {'type': 'union of two unbounded rays', 'lo': None, 'hi': None, 'pieces': [[-np.inf, float(r1)], [float(r2), np.inf]]}
