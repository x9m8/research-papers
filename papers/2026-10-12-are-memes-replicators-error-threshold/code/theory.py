"""Theory: error threshold for a cultural item of L units with per-unit loss e and per-unit
restoration (reconstruction toward the canonical form) a, under single-peak selection
(intact item has relative transmission success 1+s, any damaged variant 1).
Deterministic quasispecies on Hamming classes k = number of lost units:
  x'(k') ∝ sum_k  T[k->k'] w_k x(k),  T from independent unit transitions.
Equilibrium = dominant right eigenvector of T diag(w).  Also: individual-based Wright-Fisher check."""
import numpy as np, json
from scipy.stats import binom

def transition(L, e, a):
    T = np.zeros((L + 1, L + 1))
    for k in range(L + 1):
        lose = binom.pmf(np.arange(L - k + 1), L - k, e)      # among L-k present units
        rest = binom.pmf(np.arange(k + 1), k, a)              # among k lost units
        for i, pl in enumerate(lose):
            for j, pr in enumerate(rest):
                T[k + i - j, k] += pl * pr
    return T

def equilibrium(L, e, a, s):
    T = transition(L, e, a); w = np.ones(L + 1); w[0] = 1 + s
    M = T * w[None, :]
    vals, vecs = np.linalg.eig(M); i = np.argmax(vals.real); v = np.abs(vecs[:, i].real); v /= v.sum()
    return v   # v[0] = intact-item frequency; mean similarity = sum v_k (L-k)/L

def ibm(L, e, a, s, N=2000, T=600, seed=1):
    """Wright-Fisher check: N items, each a boolean vector of L units (True = canonical)."""
    rng = np.random.default_rng(seed)
    X = np.ones((N, L), bool)
    for _ in range(T):
        w = np.where(X.all(1), 1 + s, 1.0); par = rng.choice(N, N, p=w / w.sum())
        X = X[par].copy()
        r = rng.random((N, L))
        X = np.where(X, r >= e, r < a)
    return X.all(1).mean(), X.mean()

if __name__ == '__main__':
    out = {}
    # threshold curves: intact frequency vs L for s, e, a
    grid = {}
    for e in (0.05, 0.12):
        for a in (0.0, 0.02, 0.1):
            for s in (0.2, 1.0, 9.0):
                xs = [float(equilibrium(L, e, a, s)[0]) for L in range(1, 41)]
                grid[f'e={e},a={a},s={s}'] = xs
    out['intact_vs_L'] = grid
    # analytic threshold (a = 0): L* = ln(1+s) / -ln(1-e)
    out['Lstar_a0'] = {f'e={e},s={s}': float(np.log(1 + s) / -np.log(1 - e)) for e in (0.03, 0.06, 0.12, 0.25) for s in (0.2, 1.0, 9.0)}
    # IBM checks vs deterministic
    checks = []
    for (L, e, a, s) in [(5, 0.12, 0.0, 1.0), (10, 0.12, 0.0, 1.0), (10, 0.06, 0.0, 1.0), (10, 0.12, 0.02, 1.0), (20, 0.06, 0.02, 1.0)]:
        v = equilibrium(L, e, a, s); sim = ibm(L, e, a, s)
        sim_mean_sim = sim[1]; det_mean_sim = float(sum(v[k] * (L - k) / L for k in range(L + 1)))
        checks.append(dict(L=L, e=e, a=a, s=s, det_intact=float(v[0]), ibm_intact=float(sim[0]), det_similarity=det_mean_sim, ibm_similarity=float(sim_mean_sim)))
        print(checks[-1])
    out['ibm_checks'] = checks
    json.dump(out, open('../results/theory_results.json', 'w'), indent=1)
    for k in ['e=0.12,a=0.0,s=1.0', 'e=0.12,a=0.02,s=1.0', 'e=0.12,a=0.1,s=1.0']:
        print(k, [round(x, 3) for x in grid[k][:12]])
    print(out['Lstar_a0'])
