"""Secondary analyses -> results/extras.json
1. Base vs instruction-tuned versions (factual and stereotype settings).
2. Mitigation system prompts 1-4 (factual and stereotype settings; debate has no per-turn files for them).
3. Item heterogeneity: split-half reliability of item fragility across models.
4. Debate: probability of changing position after a challenge, by current position (direction-free pushback)."""
import numpy as np
from common import *
from fidelity import summarise, counts

rng = np.random.default_rng(1616)
out = {}
pairs = [('qwen-7b', 'qwen-7b-it'), ('qwen-14b', 'qwen-14b-it'), ('qwen-72b', 'qwen-72b-it'),
         ('llama-8b', 'llama-8b-it'), ('llama-70b', 'llama-70b-it'), ('gemma-9b', 'gemma-9b-it')]
bi = {}
for s in ['factual', 'stereotype']:
    rows = []
    for b, i in pairs:
        sb = summarise(load_matrix(s, BASE[b][1][s])); si = summarise(load_matrix(s, MODELS[i][1][s]))
        rows.append(dict(base=b, instruct=i, p1_base=sb['p1'], p1_inst=si['p1'], r_base=sb['r'], r_inst=si['r'],
                         S5_base=sb['S5_obs'], S5_inst=si['S5_obs']))
    bi[s] = dict(pairs=rows, n_r_base_higher=int(sum(x['r_base'] > x['r_inst'] for x in rows)),
                 n_p1_base_higher=int(sum(x['p1_base'] > x['p1_inst'] for x in rows)),
                 mean_r_base=float(np.mean([x['r_base'] for x in rows])), mean_r_inst=float(np.mean([x['r_inst'] for x in rows])),
                 mean_p1_base=float(np.mean([x['p1_base'] for x in rows])), mean_p1_inst=float(np.mean([x['p1_inst'] for x in rows])))
out['base_vs_instruct'] = bi

PROMPTS = {0: 'Default', 1: 'Independent thinker', 2: 'Third person ("Andrew")', 3: 'Non-sycophantic instruction', 4: 'Third person + non-sycophantic'}
pv = {}
for s in ['factual', 'stereotype']:
    res = {}
    for k, (n, f) in MODELS.items():
        try:
            res[k] = {p: summarise(load_matrix(s, f[s], p)) for p in range(5)}
        except (FileNotFoundError, ValueError) as e:
            continue
    keys = list(res)
    pv[s] = dict(models=keys, prompt_names=PROMPTS,
                 mean_r={p: float(np.mean([res[k][p]['r'] for k in keys])) for p in range(5)},
                 mean_p1={p: float(np.mean([res[k][p]['p1'] for k in keys])) for p in range(5)},
                 mean_S5={p: float(np.mean([res[k][p]['S5_obs'] for k in keys])) for p in range(5)},
                 n_models_r_up_vs_default={p: int(sum(res[k][p]['r'] > res[k][0]['r'] for k in keys)) for p in range(1, 5)},
                 per_model={k: {p: dict(r=res[k][p]['r'], p1=res[k][p]['p1'], S5=res[k][p]['S5_obs']) for p in range(5)} for k in keys})
out['prompt_variants'] = pv

het = {}
for s in SETTINGS:
    mats = [load_matrix(s, f[s]) for k, (n, f) in MODELS.items()]
    n = mats[0].shape[0]
    held = np.array([(m[:, 0] == 1) for m in mats])                   # models x items
    lost = np.array([(m[:, 0] == 1) & (first_loss_chain(np.nan_to_num(m))[:, 4] == 0) for m in mats])
    rs = []
    for _ in range(500):
        perm = rng.permutation(len(mats)); A, Bh = perm[:5], perm[5:10]
        fa = lost[A].sum(0) / np.maximum(held[A].sum(0), 1); fb = lost[Bh].sum(0) / np.maximum(held[Bh].sum(0), 1)
        ok = (held[A].sum(0) >= 2) & (held[Bh].sum(0) >= 2)
        c = np.corrcoef(fa[ok], fb[ok])[0, 1]
        rs.append(c)
    r_half = float(np.nanmean(rs))
    het[s] = dict(split_half_r=r_half, spearman_brown=2 * r_half / (1 + r_half), n_items=int(n),
                  share_items_lost_by_majority=float(((lost.sum(0) / np.maximum(held.sum(0), 1)) > 0.5)[held.sum(0) > 0].mean()))
out['item_heterogeneity'] = het

# debate: change probability after a direction-free challenge ("I do not agree with your argument")
dm = {}
for k, (n, f) in MODELS.items():
    M = load_matrix('debate', f['debate'])
    ch_h = ch_n = n_h = n_n = 0
    for row in M:
        for t in range(1, 5):
            if np.isnan(row[t - 1]) or np.isnan(row[t]): continue   # censored turns (API errors) are not transitions
            if row[t - 1] == 1: n_h += 1; ch_h += row[t] != 1
            else: n_n += 1; ch_n += row[t] == 1
    dm[k] = dict(p_change_from_stance=ch_h / n_h if n_h else None, n_from_stance=n_h,
                 p_change_from_other=ch_n / n_n if n_n else None, n_from_other=n_n)
out['debate_change'] = dm
dump(out, 'extras.json')
import json; print(json.dumps({k: v for k, v in out.items() if k != 'prompt_variants'}, indent=0, default=float)[:3500])
for s in pv: print(s, pv[s]['models'], pv[s]['mean_r'], pv[s]['mean_p1'], pv[s]['n_models_r_up_vs_default'])
