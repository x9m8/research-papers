"""Analysis 1: per-transmission exact-copy probability Q and per-unit error rate mu.
Model: a transmission reproduces a text of L units exactly with probability Q(L) = exp(-mu * L).
Units: word tokens (texts) or letters (Cornish strings). Fitted by binomial maximum likelihood;
95% CIs from cluster bootstrap over seed items (trees). Seed = 20261011."""
import numpy as np, json, sys
from scipy.optimize import minimize_scalar, minimize
from data_load import gistr_chains, meylan_chains, cornish_sets, toks
rng = np.random.default_rng(20261011)

def pairs_from_chains(chains):
    rows = []  # (tree, L_parent, exact, depth); each unique parent->child transmission counted once
    seen = set()
    for c in chains:
        t = c['texts']; ids = c['ids']
        for i in range(len(t) - 1):
            if (ids[i], ids[i + 1]) in seen: continue
            seen.add((ids[i], ids[i + 1]))
            p, q = toks(t[i]), toks(t[i + 1])
            if not p: continue
            rows.append((c['tree'], len(p), int(p == q), i + 1))
    return rows

def pairs_cornish(sets):
    rows = []
    for c in sets:
        g = c['gens']
        for i in range(len(g) - 1):
            child = set(g[i + 1])
            for s in g[i]:
                rows.append((f"{c['chain']}", len(s), int(s in child), i + 1))
    return rows

def fit_mu(L, y, intercept=False):
    L = np.asarray(L, float); y = np.asarray(y, float)
    if not intercept:
        nll = lambda m: -np.sum(y * (-m * L) + (1 - y) * np.log1p(-np.exp(-m * L) + 1e-300))
        r = minimize_scalar(nll, bounds=(1e-6, 5), method='bounded'); return r.x, None
    def nll(p):
        lq0, m = p; q = np.exp(lq0 - m * L); q = np.clip(q, 1e-12, 1 - 1e-12)
        return -np.sum(y * np.log(q) + (1 - y) * np.log(1 - q))
    r = minimize(nll, [0.0, 0.05], bounds=[(-5, 0), (1e-6, 5)]); return r.x[1], np.exp(r.x[0])

def boot(rows, B=1000, intercept=False):
    trees = sorted(set(r[0] for r in rows), key=str)
    by = {t: [r for r in rows if r[0] == t] for t in trees}
    est = []
    for _ in range(B):
        samp = rng.choice(len(trees), len(trees), replace=True)
        rr = [r for i in samp for r in by[trees[i]]]
        est.append(fit_mu([r[1] for r in rr], [r[2] for r in rr], intercept)[0])
    return np.percentile(est, [2.5, 97.5])

if __name__ == '__main__':
    datasets = {f'Gistr exp {e}': pairs_from_chains(gistr_chains(e)) for e in (1, 2, 3)}
    datasets['Meylan et al. (spoken)'] = pairs_from_chains(meylan_chains())
    datasets['Cornish et al. (letter strings)'] = pairs_cornish(cornish_sets())
    out = {}
    for k, rows in datasets.items():
        L = [r[1] for r in rows]; y = [r[2] for r in rows]
        mu, _ = fit_mu(L, y)
        mu2, q0 = fit_mu(L, y, intercept=True)
        ci = boot(rows, B=400)
        out[k] = dict(n_transmissions=len(rows), n_items=len(set(r[0] for r in rows)), mean_L=float(np.mean(L)),
                      Q_obs=float(np.mean(y)), mu=float(mu), mu_ci=[float(x) for x in ci], mu_with_intercept=float(mu2), q0=float(q0),
                      Q_at_meanL=float(np.exp(-mu * np.mean(L))))
        print(k, json.dumps({a: (round(b, 4) if isinstance(b, float) else b) for a, b in out[k].items()}))
    json.dump(out, open('../results/fidelity_results.json', 'w'), indent=1)
    # binned curves for figure
    curves = {}
    for k, rows in datasets.items():
        L = np.array([r[1] for r in rows]); y = np.array([r[2] for r in rows])
        edges = np.unique(np.percentile(L, np.linspace(0, 100, 8)).round())
        cv = []
        for a, b in zip(edges[:-1], edges[1:]):
            m = (L >= a) & (L < b if b != edges[-1] else L <= b)
            if m.sum() >= 15: cv.append([float(L[m].mean()), float(y[m].mean()), int(m.sum())])
        curves[k] = cv
    json.dump(curves, open('../results/fidelity_curves.json', 'w'), indent=1)

def mu_by_depth(rows, bins=((1, 1), (2, 3), (4, 6), (7, 99))):
    out = []
    for lo, hi in bins:
        rr = [r for r in rows if lo <= r[3] <= hi]
        if len(rr) < 50: continue
        mu, _ = fit_mu([r[1] for r in rr], [r[2] for r in rr])
        ci = boot(rr, B=300)
        out.append(dict(gen=f'{lo}-{hi}' if hi < 99 else f'{lo}+', n=len(rr), mean_L=float(np.mean([r[1] for r in rr])), mu=float(mu), mu_ci=[float(x) for x in ci]))
    return out

if __name__ == '__main__':
    dep = {}
    for k in ['Gistr exp 1', 'Gistr exp 2', 'Gistr exp 3', 'Meylan et al. (spoken)']:
        dep[k] = mu_by_depth(datasets[k])
        print(k, [(d['gen'], d['n'], round(d['mean_L'], 1), round(d['mu'], 4), [round(x, 4) for x in d['mu_ci']]) for d in dep[k]])
    json.dump(dep, open('../results/fidelity_by_depth.json', 'w'), indent=1)
