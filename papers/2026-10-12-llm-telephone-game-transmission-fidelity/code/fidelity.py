"""Analysis 2: exact copies. For each transmission (parent -> child), is the child an exact copy?
Definitions as in paper 1: 'token' = identical lowercase alphanumeric token sequence (main);
'content-set' = identical set of content words (lenient).
Where exact copies occur, fit Q(L) = exp(-mu L) and Q(L) = q0 exp(-mu L) by binomial ML (as paper 1),
with cluster-bootstrap CIs over the 20 seed texts. Where none occur, report the Clopper-Pearson 95% upper
bound on the exact-copy probability and the selective advantage it implies, s* > 1/Q_upper - 1.
The intercept fit uses multiple starting points (a single start can stop at a bound). mu is constrained >= 0.
Rows whose parent text is empty are skipped. Also: is copying 'locked in'? P(exact | parent was itself an exact copy) vs P(exact | it was not).
Seed 20261012."""
import numpy as np, json
from scipy.optimize import minimize_scalar, minimize
from scipy.stats import beta as betad
from data_load import llm_chains, toks, content, CONDITIONS, TEMPERATURES
rng = np.random.default_rng(20261012)

def rows_for(chains):
    rows = []  # tree, L_parent(words), exact_token, exact_contentset, gen, parent_was_exact
    for c in chains:
        T = [toks(t) for t in c['texts']]; C = [content(t) for t in c['texts']]
        prev = 0
        for i in range(len(T) - 1):
            if not T[i]: prev = 0; continue
            ex = int(T[i] == T[i + 1])
            rows.append((c['tree'], len(T[i]), ex, int(C[i] == C[i + 1]), i + 1, prev))
            prev = ex
    return rows

def fit_mu(L, y, intercept=False):
    L = np.asarray(L, float); y = np.asarray(y, float)
    if not intercept:
        nll = lambda m: -np.sum(y * (-m * L) + (1 - y) * np.log1p(-np.exp(-m * L) + 1e-300))
        return minimize_scalar(nll, bounds=(1e-7, 5), method='bounded').x, 1.0
    def nll(p):
        q = np.clip(np.exp(p[0] - p[1] * L), 1e-12, 1 - 1e-12)
        return -np.sum(y * np.log(q) + (1 - y) * np.log(1 - q))
    best = None
    ybar = max(y.mean(), 1e-6)
    for lq0 in (np.log(ybar), -1.0, -3.0, -6.0, -0.01):          # multistart: the surface is flat near q0 -> 0
        for m in (1e-6, 1e-3, 0.01, 0.05, 0.2):
            r = minimize(nll, [lq0, m], bounds=[(-12, 0), (0.0, 5)], method='L-BFGS-B')
            if best is None or r.fun < best.fun: best = r
    return best.x[1], float(np.exp(best.x[0]))

def boot_mu(rows, col, B=400, intercept=False):
    rng = np.random.default_rng(20261012)
    trees = sorted(set(r[0] for r in rows)); by = {t: [r for r in rows if r[0] == t] for t in trees}
    est = []
    for _ in range(B):
        rr = [r for i in rng.choice(len(trees), len(trees)) for r in by[trees[i]]]
        if sum(r[col] for r in rr) == 0: est.append(np.inf); continue
        est.append(fit_mu([r[1] for r in rr], [r[col] for r in rr], intercept)[0])
    return [float(x) for x in np.percentile(est, [2.5, 97.5])]

def summarise(name, rows):
    n = len(rows); k = sum(r[2] for r in rows); kc = sum(r[3] for r in rows)
    L = np.array([r[1] for r in rows])
    res = dict(n=n, mean_L=float(L.mean()), median_L=float(np.median(L)), exact=k, exact_rate=k / n,
               contentset_exact=kc, contentset_rate=kc / n)
    res['exact_upper95'] = float(betad.ppf(0.95, k + 1, n - k)) if k < n else 1.0  # one-sided CP upper bound
    res['s_min_from_upper'] = float(1 / res['exact_upper95'] - 1)
    if k > 0:
        mu, _ = fit_mu(L, [r[2] for r in rows]); res['mu'] = float(mu); res['mu_ci'] = boot_mu(rows, 2)
        mu1, q0 = fit_mu(L, [r[2] for r in rows], intercept=True); res['mu_int'] = float(mu1); res['q0'] = q0
        res['s_min_intercept_flat'] = float(1 / q0 - 1) if q0 > 0 else None
        for s in (0.2, 1, 9):
            res[f'Lstar_s{s}'] = float(np.log(1 + s) / mu)
            v = (np.log(1 + s) + np.log(q0)) / mu1; res[f'Lstar_int_s{s}'] = float(v) if v > 0 else None
        a = [r for r in rows if r[5] == 1]; b = [r for r in rows if r[5] == 0]
        res['p_exact_after_exact'] = float(np.mean([r[2] for r in a])) if a else None
        res['p_exact_after_nonexact'] = float(np.mean([r[2] for r in b]))
        res['n_after_exact'] = len(a)
        res['first_gen_exact_rate'] = float(np.mean([r[2] for r in rows if r[4] == 1]))
    if kc > 0:
        muc, _ = fit_mu(L, [r[3] for r in rows]); res['mu_contentset'] = float(muc)
    print(name, {k_: (round(v, 4) if isinstance(v, float) else v) for k_, v in res.items()}, flush=True)
    return res

if __name__ == '__main__':
    out = {'rephrase': {}, 'temperature': {}}
    for d, lab in CONDITIONS:
        out['rephrase'][lab] = summarise(lab, rows_for(llm_chains(d)))
    for T, d in TEMPERATURES:
        out['temperature'][str(T)] = summarise(f'T={T}', rows_for(llm_chains(d)))
    json.dump(out, open('../results/fidelity_results.json', 'w'), indent=1)
