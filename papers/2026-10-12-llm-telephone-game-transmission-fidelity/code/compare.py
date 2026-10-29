"""Analysis 5: summaries used in the paper.
(a) Side-by-side table of human rates (paper 1 results JSONs, shipped in ../paper1_results/) and model rates.
(b) Equilibrium: correlation across the 11 model conditions between the pooled-rate plateau
    (a - a0)/(e + a - a0) and observed mean retention over generations 41-50 (both from restoration_results.json).
(c) Seed-length check: per-seed-text loss rate e vs number of seed content words (Spearman, 20 texts),
    to see whether longer seeds (model seeds are 91-760 words; human seeds 10-66) are lost faster.
(d) Temperature: Spearman correlation of e, a and plateau with temperature (5 levels)."""
import numpy as np, json
from scipy.stats import spearmanr, pearsonr
from data_load import llm_chains, content, CONDITIONS, TEMPERATURES
from restoration import counts

R = json.load(open('../results/restoration_results.json'))
F = json.load(open('../results/fidelity_results.json'))
H = json.load(open('../results/heterogeneity_results.json'))
P1R = json.load(open('../paper1_results/restoration_results.json'))
P1F = json.load(open('../paper1_results/fidelity_results.json'))
out = {}

# (a)
human = {}
for k_r, k_f, lab in [('Gistr exp 1 (content words)', 'Gistr exp 1', 'Gistr 1 (written)'),
                      ('Gistr exp 2 (content words)', 'Gistr exp 2', 'Gistr 2 (written)'),
                      ('Gistr exp 3 (content words)', 'Gistr exp 3', 'Gistr 3 (written)'),
                      ('Meylan et al. (all words)', 'Meylan et al. (spoken)', 'Meylan et al. (spoken)')]:
    r, f = P1R[k_r], P1F[k_f]
    human[lab] = dict(e=r['e'], a=r['a'], a0=r['a0'], ratio=r['a'] / r['a0'], plateau=r['plateau_pred_direct'],
                      exact_rate=f['Q_obs'], mean_L=f['mean_L'], mu=f['mu'])
out['human'] = human
out['human_ranges'] = {k: [min(v[k] for v in human.values()), max(v[k] for v in human.values())] for k in ('e', 'a', 'a0', 'ratio', 'plateau', 'exact_rate')}
mods = {lab: dict(e=R['rephrase'][lab]['e'], a=R['rephrase'][lab]['a'], a0=R['rephrase'][lab]['a0'],
                  ratio=R['rephrase'][lab]['ratio_a_a0'], plateau=R['rephrase'][lab]['plateau_pred'],
                  exact_rate=F['rephrase'][lab]['exact_rate'], mean_L=F['rephrase'][lab]['mean_L']) for _, lab in CONDITIONS}
out['models'] = mods
inst = [lab for _, lab in CONDITIONS[:5]]
out['instruct_ranges'] = {k: [min(mods[l][k] for l in inst), max(mods[l][k] for l in inst)] for k in ('e', 'a', 'a0', 'ratio', 'plateau', 'exact_rate')}

# (b)
pred, obs, names = [], [], []
for _, lab in CONDITIONS:
    pred.append(R['rephrase'][lab]['plateau_pred']); obs.append(R['rephrase'][lab]['retention_late']); names.append(lab)
for T, _ in TEMPERATURES:
    if T == 0.8: continue  # identical data to Llama 3 8B Instruct
    pred.append(R['temperature'][str(T)]['plateau_pred']); obs.append(R['temperature'][str(T)]['retention_late']); names.append(f'Llama 8B T={T}')
pred, obs = np.array(pred), np.array(obs)
out['equilibrium'] = dict(names=names, pred=pred.tolist(), obs=obs.tolist(), pearson_r=float(pearsonr(pred, obs)[0]),
                          pearson_p=float(pearsonr(pred, obs)[1]), mean_obs_minus_pred=float(np.mean(obs - pred)),
                          range_obs_minus_pred=[float(np.min(obs - pred)), float(np.max(obs - pred))], n=len(names))
print('equilibrium', {k: v for k, v in out['equilibrium'].items() if k not in ('names', 'pred', 'obs')})

# (c)
lenchk = {}
for d, lab in CONDITIONS:
    ch = llm_chains(d)
    pool = sorted(set().union(*[content(c['texts'][0]) for c in ch]))
    per = counts(ch, content, pool)
    sizes = {c['tree']: len(content(c['texts'][0])) for c in ch}
    trees = sorted(per)
    e_t = [per[t][0] / per[t][1] for t in trees]; n_t = [sizes[t] for t in trees]
    rho, p = spearmanr(n_t, e_t)
    lenchk[lab] = dict(rho=float(rho), p=float(p), seed_content_words=[min(n_t), max(n_t)])
    print('length', lab, round(rho, 2), round(p, 3))
out['seed_length_vs_e'] = lenchk

# (d)
Ts = [T for T, _ in TEMPERATURES]
tem = {k: [R['temperature'][str(T)][k] for T in Ts] for k in ('e', 'a', 'a0', 'plateau_pred', 'retention_late')}
tem['exact_rate'] = [F['temperature'][str(T)]['exact_rate'] for T in Ts]
tem['spearman_e'] = float(spearmanr(Ts, tem['e'])[0]); tem['spearman_a'] = float(spearmanr(Ts, tem['a'])[0])
tem['e_ratio_1.6_vs_0'] = tem['e'][-1] / tem['e'][0]
tem['T'] = Ts
out['temperature'] = tem
print('temperature', {k: (np.round(v, 4).tolist() if isinstance(v, list) else round(v, 3)) for k, v in tem.items()})
json.dump(out, open('../results/compare_results.json', 'w'), indent=1)

# (e) First hand-off: share of seed content words kept after one transmission, and its link to seed length.
first = {}
for d, lab in CONDITIONS:
    ch = llm_chains(d)
    by = {}
    for c in ch:
        S = content(c['texts'][0]); by.setdefault(c['tree'], []).append(len(S & content(c['texts'][1])) / len(S))
    sizes = {c['tree']: len(content(c['texts'][0])) for c in ch}
    trees = sorted(by); r1 = [np.mean(by[t]) for t in trees]
    rho, p = spearmanr([sizes[t] for t in trees], r1)
    first[lab] = dict(retention_gen1=float(R['rephrase'][lab]['curve'][1]), rho_with_seed_length=float(rho), p=float(p),
                      per_seed_range=[float(min(r1)), float(max(r1))])
    print('first', lab, {k: (round(v, 3) if isinstance(v, float) else [round(x, 3) for x in v]) for k, v in first[lab].items()})
out['first_handoff'] = first
out['human_first_handoff'] = {k: float(v['curve'][1]) for k, v in P1R.items()}
json.dump(out, open('../results/compare_results.json', 'w'), indent=1)
