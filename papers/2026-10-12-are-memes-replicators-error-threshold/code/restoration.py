"""Analysis 2: loss (e) and restoration (a) of seed content words along chains.
For each chain with texts X_0 (seed), X_1, ..., and seed content-word set S:
  e = P(w not in X_{t+1} | w in X_t),  w in S
  a = P(w in X_{t+1}  | w not in X_t), w in S  (word absent from the text the participant saw)
Control for chance re-entry: a0 = same quantity for 'pseudo-seed' words taken from the seed of a
different item in the same experiment, matched in number (these were never in the chain).
Attraction (reconstruction) rate = a - a0.  CIs: cluster bootstrap over seed items.
Also fits r(t) = p + (1-p) * (1-e-a)^t, p = a/(e+a), to the seed-retention curve as a consistency check."""
import numpy as np, json
from scipy.optimize import curve_fit
from data_load import gistr_chains, meylan_chains, content, toks
rng = np.random.default_rng(20261011)

def counts(chains, wordfn, control_pool):
    """Return per-tree counts: [lossN, lossD, restN, restD, ctrlN, ctrlD]."""
    per = {}
    trees = sorted(set(c['tree'] for c in chains), key=str)
    for c in chains:
        S = wordfn(c['texts'][0])
        if not S: continue
        others = [w for w in control_pool if w not in S]
        C = set(rng.choice(others, size=min(len(S), len(others)), replace=False)) if others else set()
        X = [wordfn(t) for t in c['texts']]
        v = per.setdefault(c['tree'], np.zeros(6))
        for t in range(1, len(X) - 1):
            for w in S:
                if w in X[t]:
                    v[1] += 1; v[0] += (w not in X[t + 1])
                else:
                    v[3] += 1; v[2] += (w in X[t + 1])
            for w in C:
                if w not in X[t]:
                    v[5] += 1; v[4] += (w in X[t + 1])
    return per

def rates(per, keys):
    s = sum(per[k] for k in keys)
    return s[0] / s[1], s[2] / s[3], s[4] / max(s[5], 1)

def retention_curve(chains, wordfn, G):
    R = []
    for c in chains:
        if len(c['texts']) <= G: continue
        S = wordfn(c['texts'][0])
        if not S: continue
        R.append([len(S & wordfn(c['texts'][t])) / len(S) for t in range(G + 1)])
    return np.array(R)

def model(t, e, a):
    p = a / (e + a); return p + (1 - p) * (1 - e - a) ** t

def run(name, chains, wordfn, G):
    pool = sorted(set().union(*[wordfn(c['texts'][0]) for c in chains]))
    per = counts(chains, wordfn, pool)
    keys = list(per)
    e, a, a0 = rates(per, keys)
    B = []
    for _ in range(1000):
        ks = [keys[i] for i in rng.choice(len(keys), len(keys))]
        B.append(rates(per, ks))
    B = np.array(B)
    ci = lambda j: [float(x) for x in np.percentile(B[:, j], [2.5, 97.5])]
    att = B[:, 1] - B[:, 2]
    R = retention_curve(chains, wordfn, G)
    t = np.arange(G + 1); m = R.mean(0)
    (ef, af), cov = curve_fit(model, t, m, p0=[0.1, 0.02], bounds=([1e-6, 0], [1, 1]))
    res = dict(n_chains=len(chains), n_items=len(keys), e=float(e), e_ci=ci(0), a=float(a), a_ci=ci(1), a0=float(a0), a0_ci=ci(2),
               attraction=float(a - a0), attraction_ci=[float(x) for x in np.percentile(att, [2.5, 97.5])],
               plateau_pred_direct=float((a - a0) / (e + a - a0)),
               curve_G=G, curve_n=int(len(R)), curve=[float(x) for x in m], curve_fit_e=float(ef), curve_fit_a=float(af),
               curve_fit_plateau=float(af / (ef + af)))
    print(name, json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items() if k != 'curve'}))
    return res

if __name__ == '__main__':
    out = {}
    for e, G in [(1, 7), (2, 6), (3, 10)]:
        ch = gistr_chains(e)
        out[f'Gistr exp {e} (content words)'] = run(f'Gistr {e}', ch, content, G)
    mc = meylan_chains()
    out['Meylan et al. (all words)'] = run('Meylan', mc, lambda s: set(toks(s)), 20)
    json.dump(out, open('../results/restoration_results.json', 'w'), indent=1)
