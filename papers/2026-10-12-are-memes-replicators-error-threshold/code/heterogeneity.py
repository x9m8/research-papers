"""Analysis 3: are retention plateaus attraction or heterogeneous loss?
For each seed item (tree) and each seed word w, estimate its own loss probability e_w
(pooled over all chains of that item, transitions where w present). Restoration a_w likewise.
Then predict the mean seed-retention curve by iterating each word's 2-state Markov chain
p_{t+1} = p_t (1-e_w) + (1-p_t) a_w, p_0 = 1, averaged over words and items, and compare with
(i) the observed curve and (ii) a homogeneous model using pooled e and a.
Leave-chain-out is not needed for the descriptive comparison, but to avoid circularity we
estimate e_w, a_w on odd-numbered chains and evaluate the curve on even-numbered chains."""
import numpy as np, json
from data_load import gistr_chains, meylan_chains, content, toks

def word_rates(chains, wordfn):
    R = {}  # (tree,w) -> [lossN, lossD, restN, restD]
    for c in chains:
        S = wordfn(c['texts'][0]); X = [wordfn(t) for t in c['texts']]
        for t in range(1, len(X) - 1):
            for w in S:
                v = R.setdefault((c['tree'], w), np.zeros(4))
                if w in X[t]: v[1] += 1; v[0] += (w not in X[t + 1])
                else: v[3] += 1; v[2] += (w in X[t + 1])
        # include generation-0 -> 1 transition for loss (seed always present)
        for w in S:
            v = R.setdefault((c['tree'], w), np.zeros(4)); v[1] += 1; v[0] += (w not in X[1])
    return R

from scipy.special import betaln
from scipy.optimize import minimize
def fit_beta(N, D):
    """Empirical-Bayes beta-binomial fit of per-word rates; returns alpha, beta."""
    N = np.asarray(N, float); D = np.asarray(D, float); m = D > 0
    nll = lambda p: -np.sum(betaln(N[m] + np.exp(p[0]), D[m] - N[m] + np.exp(p[1])) - betaln(np.exp(p[0]), np.exp(p[1])))
    r = minimize(nll, [0.0, 1.0], method='Nelder-Mead'); return np.exp(r.x)
PRIOR = {}
def predict(R, trees_words, G, pooled=None, prior=(1, 1)):
    curves = []
    for key in trees_words:
        v = R.get(key)
        if v is None: continue
        if pooled: e, a = pooled
        else:
            ae, be = PRIOR['e']; aa, ba = PRIOR['a']
            e = (v[0] + ae) / (v[1] + ae + be)       # empirical-Bayes posterior mean
            a = (v[2] + aa) / (v[3] + aa + ba)
        p = [1.0]
        for _ in range(G): p.append(p[-1] * (1 - e) + (1 - p[-1]) * a)
        curves.append(p)
    return np.mean(curves, 0)

def observed(chains, wordfn, G):
    R = []
    for c in chains:
        if len(c['texts']) <= G: continue
        S = wordfn(c['texts'][0])
        if S: R.append([len(S & wordfn(c['texts'][t])) / len(S) for t in range(G + 1)])
    return np.mean(R, 0), len(R)

out = {}
for name, chains, fn, G in [('Gistr exp 1', gistr_chains(1), content, 7), ('Gistr exp 2', gistr_chains(2), content, 6),
                            ('Gistr exp 3', gistr_chains(3), content, 10), ('Meylan et al.', meylan_chains(), lambda s: set(toks(s)), 20)]:
    full = [c for c in chains if len(c['texts']) > G]
    train = [c for i, c in enumerate(full) if i % 2 == 1]; test = [c for i, c in enumerate(full) if i % 2 == 0]
    R = word_rates(train, fn)
    tot = sum(R.values()); pooled_e = tot[0] / tot[1]; pooled_a = tot[2] / tot[3]
    V = np.array(list(R.values()))
    PRIOR['e'] = fit_beta(V[:, 0], V[:, 1]); PRIOR['a'] = fit_beta(V[:, 2], V[:, 3])
    obs, n = observed(test, fn, G)
    keys = sorted(set((c['tree'], w) for c in test if len(c['texts']) > G for w in fn(c['texts'][0])), key=str)
    het = predict(R, keys, G)
    hom = predict(R, keys, G, pooled=(pooled_e, pooled_a))
    noa = []
    for key in keys:
        v = R.get(key)
        if v is None: continue
        ae, be = PRIOR['e']; e = (v[0] + ae) / (v[1] + ae + be); noa.append([(1 - e) ** t for t in range(G + 1)])
    noa = np.mean(noa, 0)
    ae, be = PRIOR['e']; es = np.array([(v[0] + ae) / (v[1] + ae + be) for v in R.values() if v[1] >= 3])
    rmse = lambda x: float(np.sqrt(np.mean((x - obs) ** 2)))
    out[name] = dict(G=G, n_test_chains=n, observed=obs.tolist(), heterogeneous=het.tolist(), homogeneous=hom.tolist(),
                     heterogeneous_no_restoration=noa.tolist(), rmse_het=rmse(het), rmse_hom=rmse(hom), rmse_het_noa=rmse(noa),
                     pooled_e=float(pooled_e), pooled_a=float(pooled_a), beta_e=[float(x) for x in PRIOR['e']], beta_a=[float(x) for x in PRIOR['a']],
                     word_e_quantiles=[float(x) for x in np.percentile(es, [10, 25, 50, 75, 90])],
                     frac_words_e_below_0_05=float(np.mean(es < 0.05)), n_words=int(len(es)))
    print(name, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out[name].items() if not isinstance(v, list) or k in ('word_e_quantiles','beta_e','beta_a')})
    print('   obs',np.round(obs,3).tolist()); print('   het',np.round(het,3).tolist()); print('   hom',np.round(hom,3).tolist()); print('   noa',np.round(noa,3).tolist())
json.dump(out, open('../results/heterogeneity_results.json', 'w'), indent=1)
