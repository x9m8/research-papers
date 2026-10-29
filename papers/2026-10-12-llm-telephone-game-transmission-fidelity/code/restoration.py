"""Analysis 1: loss (e) and reconstruction (a) of seed content words along LLM chains.
Identical estimator to paper 1 (restoration.py):
  e  = P(w not in X_{t+1} | w in X_t),     w in seed content words S, t >= 1
  a  = P(w in X_{t+1}     | w not in X_t), w in S
  a0 = same as a for a matched number of control words drawn from other seed texts' content words
Attraction = a - a0. 95% CIs: cluster bootstrap over the 20 seed texts (1,000 resamples).
Also records the mean seed-retention curve over all 50 generations and its mean over generations 41-50.
Control words are drawn per chain from a generator seeded by (20261012, CRC32 of seed text + chain), so every
script that calls counts() uses the same control words for the same chain. Bootstrap seed 20261012."""
import numpy as np, json, sys, zlib
from data_load import llm_chains, content, CONDITIONS, TEMPERATURES
rng = np.random.default_rng(20261012)

def counts(chains, wordfn, pool):
    per = {}
    for c in chains:
        S = wordfn(c['texts'][0])
        if not S: continue
        others = [w for w in pool if w not in S]
        crng = np.random.default_rng([20261012, zlib.crc32((c['tree'] + '/' + c['chain']).encode())])
        C = set(crng.choice(others, size=min(len(S), len(others)), replace=False))
        X = [wordfn(t) for t in c['texts']]
        v = per.setdefault(c['tree'], np.zeros(6))
        for t in range(1, len(X) - 1):
            P = S & X[t]; A = S - X[t]
            v[1] += len(P); v[0] += len(P - X[t + 1])
            v[3] += len(A); v[2] += len(A & X[t + 1])
            CA = C - X[t]
            v[5] += len(CA); v[4] += len(CA & X[t + 1])
    return per

def rates(per, keys):
    s = sum(per[k] for k in keys)
    return s[0] / s[1], s[2] / max(s[3], 1), s[4] / max(s[5], 1)

def retention(chains, wordfn):
    R = []
    for c in chains:
        S = wordfn(c['texts'][0])
        if S: R.append([len(S & wordfn(t)) / len(S) for t in c['texts']])
    return np.array(R)

def run(name, chains, wordfn=content, B=1000):
    rng = np.random.default_rng(20261012)  # fresh per condition, so identical data give identical intervals
    pool = sorted(set().union(*[wordfn(c['texts'][0]) for c in chains]))
    per = counts(chains, wordfn, pool)
    keys = sorted(per)
    e, a, a0 = rates(per, keys)
    Bs = np.array([rates(per, [keys[i] for i in rng.choice(len(keys), len(keys))]) for _ in range(B)])
    ci = lambda x: [float(v) for v in np.percentile(x, [2.5, 97.5])]
    att = Bs[:, 1] - Bs[:, 2]
    plateau = (Bs[:, 1] - Bs[:, 2]) / (Bs[:, 0] + Bs[:, 1] - Bs[:, 2])
    R = retention(chains, wordfn)
    res = dict(n_chains=len(chains), n_items=len(keys), e=float(e), e_ci=ci(Bs[:, 0]), a=float(a), a_ci=ci(Bs[:, 1]),
               a0=float(a0), a0_ci=ci(Bs[:, 2]), attraction=float(a - a0), attraction_ci=ci(att),
               ratio_a_a0=float(a / a0) if a0 > 0 else None,
               plateau_pred=float((a - a0) / (e + a - a0)), plateau_pred_ci=ci(plateau),
               curve=[float(x) for x in R.mean(0)], retention_final=float(R.mean(0)[-1]),
               retention_late=float(R.mean(0)[41:].mean()))
    print(f"{name:28s} e={e:.3f} [{res['e_ci'][0]:.3f},{res['e_ci'][1]:.3f}] a={a:.4f} a0={a0:.4f} "
          f"ratio={res['ratio_a_a0']:.1f} plateau={res['plateau_pred']:.3f} late={res['retention_late']:.3f}", flush=True)
    return res

if __name__ == '__main__':
    out = {'rephrase': {}, 'temperature': {}, 'other_tasks': {}}
    for d, lab in CONDITIONS:
        out['rephrase'][lab] = run(lab, llm_chains(d, 'rephrase'))
    for T, d in TEMPERATURES:
        out['temperature'][str(T)] = run(f'Llama 8B T={T}', llm_chains(d, 'rephrase'))
    for task in ('inspiration', 'continue'):
        for d, lab in CONDITIONS[:5]:
            out['other_tasks'][f'{lab} | {task}'] = run(f'{lab[:18]} {task}', llm_chains(d, task), B=300)
    json.dump(out, open('../results/restoration_results.json', 'w'), indent=1)
