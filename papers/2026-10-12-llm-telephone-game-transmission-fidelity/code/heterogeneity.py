"""Analysis 4: does the two-state loss/reconstruction model predict retention in held-out chains,
and do the chains reach the equilibrium a/(a+e) that the model predicts?
Same method as paper 1 (heterogeneity.py): word-specific e_w and a_w (empirical-Bayes beta-binomial
shrinkage) estimated on training chains (seed_1, seed_3, seed_5 of each seed text; first hand-off included, as in paper 1), mean retention curve
predicted for test chains (seed_2, seed_4) over all 50 generations. Three models compared by RMSE:
word-specific e and a; word-specific e with a = 0; pooled e and a.
Temperature 0 is skipped: its five chains per seed are identical, so no held-out chains exist.
Also reports per-word loss distributions estimated without the first hand-off (later_*)."""
import numpy as np, json
from scipy.special import betaln
from scipy.optimize import minimize
from data_load import llm_chains, content, CONDITIONS, TEMPERATURES

def word_rates(chains, first=True):
    """Per (seed text, word) counts [lossN, lossD, restN, restD]. With first=True the generation 0->1 hand-off is
    included in the loss counts (as in paper 1's held-out analysis); with first=False it is excluded."""
    R = {}
    for c in chains:
        S = content(c['texts'][0]); X = [content(t) for t in c['texts']]
        for w in S:
            v = R.setdefault((c['tree'], w), np.zeros(4))
            if first: v[1] += 1; v[0] += (w not in X[1])
        for t in range(1, len(X) - 1):
            for w in S:
                v = R[(c['tree'], w)]
                if w in X[t]: v[1] += 1; v[0] += (w not in X[t + 1])
                else: v[3] += 1; v[2] += (w in X[t + 1])
    return R

def fit_beta(N, D):
    N = np.asarray(N, float); D = np.asarray(D, float); m = D > 0
    nll = lambda p: -np.sum(betaln(N[m] + np.exp(p[0]), D[m] - N[m] + np.exp(p[1])) - betaln(np.exp(p[0]), np.exp(p[1])))
    return np.exp(minimize(nll, [0.0, 1.0], method='Nelder-Mead').x)

def curve(e, a, G):
    p = [1.0]
    for _ in range(G): p.append(p[-1] * (1 - e) + (1 - p[-1]) * a)
    return np.array(p)

def run(name, chains, rest):
    G = len(chains[0]['texts']) - 1
    train = [c for c in chains if c['chain'] in ('seed_1', 'seed_3', 'seed_5')]
    test = [c for c in chains if c['chain'] in ('seed_2', 'seed_4')]
    if not test: return None
    R = word_rates(train); V = np.array(list(R.values()))
    pe, pa = V[:, 0].sum() / V[:, 1].sum(), V[:, 2].sum() / V[:, 3].sum()
    be, ba = fit_beta(V[:, 0], V[:, 1]), fit_beta(V[:, 2], V[:, 3])
    obs = np.mean([[len(content(c['texts'][0]) & content(t)) / len(content(c['texts'][0])) for t in c['texts']] for c in test], 0)
    keys = sorted(set((c['tree'], w) for c in test for w in content(c['texts'][0])))
    het, noa, hom = [], [], []
    for k in keys:
        v = R.get(k)
        if v is None: continue
        e = (v[0] + be[0]) / (v[1] + be.sum()); a = (v[2] + ba[0]) / (v[3] + ba.sum())
        het.append(curve(e, a, G)); noa.append(curve(e, 0, G))
    het, noa, hom = np.mean(het, 0), np.mean(noa, 0), curve(pe, pa, G)
    rmse = lambda x: float(np.sqrt(np.mean((x - obs) ** 2)))
    es = np.array([(v[0] + be[0]) / (v[1] + be.sum()) for v in R.values()])
    R2 = word_rates(train, first=False); V2 = np.array([v for v in R2.values() if v[1] > 0])
    be2 = fit_beta(V2[:, 0], V2[:, 1]); es2 = (V2[:, 0] + be2[0]) / (V2[:, 1] + be2.sum())
    res = dict(G=G, n_test=len(test), observed=obs.tolist(), heterogeneous=het.tolist(), homogeneous=hom.tolist(),
               heterogeneous_no_restoration=noa.tolist(), rmse_het=rmse(het), rmse_hom=rmse(hom), rmse_het_noa=rmse(noa),
               word_e_quantiles=[float(x) for x in np.percentile(es, [10, 25, 50, 75, 90])],
               frac_e_below_0_05=float(np.mean(es < 0.05)), frac_e_above_0_5=float(np.mean(es > 0.5)), n_words=int(len(es)),
               later_frac_e_below_0_05=float(np.mean(es2 < 0.05)), later_frac_e_above_0_5=float(np.mean(es2 > 0.5)),
               later_word_e_quantiles=[float(x) for x in np.percentile(es2, [10, 25, 50, 75, 90])], later_n_words=int(len(es2)),
               observed_late_mean=float(obs[41:].mean()), plateau_pred=rest['plateau_pred'],
               observed_all_late=float(np.mean(rest['curve'][41:])))
    print(f"{name:24s} rmse het={res['rmse_het']:.3f} noa={res['rmse_het_noa']:.3f} hom={res['rmse_hom']:.3f} | "
          f"late obs(all)={res['observed_all_late']:.3f} pred plateau={res['plateau_pred']:.3f} | word e q10-90 {np.round(res['word_e_quantiles'],3)}", flush=True)
    return res

if __name__ == '__main__':
    rr = json.load(open('../results/restoration_results.json'))
    out = {'rephrase': {}, 'temperature': {}}
    for d, lab in CONDITIONS:
        out['rephrase'][lab] = run(lab, llm_chains(d), rr['rephrase'][lab])
    for T, d in TEMPERATURES:
        if T == 0.8: continue  # same data as Llama 3 8B Instruct above
        r = run(f'T={T}', llm_chains(d), rr['temperature'][str(T)])
        if r is None: print(f'T={T}: skipped (deterministic decoding; one distinct chain per seed, no held-out chains)'); continue
        out['temperature'][str(T)] = r
    json.dump(out, open('../results/heterogeneity_results.json', 'w'), indent=1)
