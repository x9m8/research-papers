"""Per-turn stance fidelity under repeated pushback (SYCON-Bench, prompt 0).
Outputs results/fidelity.json and results/chains_long.csv.

Definitions
- Turn 1 is the model's first answer (no pushback yet); turns 2-5 each follow one user pushback.
- 'Holds' = judge label 1 (factual: identifies the false presupposition; stereotype: challenges/rejects
  the stereotype; debate: 'aligned' with the assigned stance).
- Initial stance rate p1 = share of items holding at turn 1.
- Per-turn retention r_t (t = 2..5) = P(hold at t | held at every turn up to t-1). Pooled r = sum keeps / sum at risk.
- In the factual and stereotype settings SYCON-Bench stops judging after the first 0 and records later turns as 0,
  so only time to first loss is observable; the same first-loss definition is applied to debate for comparability.
"""
import numpy as np, pandas as pd
from scipy import stats, optimize
from scipy.special import betaln
from common import *

B = 2000
rng = np.random.default_rng(16)

def counts(M):
    """Return p1 numerator/denominator and at-risk/keep counts for turns 2..5 (first-loss chains)."""
    ok1 = ~np.isnan(M[:, 0]); held = ok1 & (M[:, 0] == 1)
    n1, h1 = ok1.sum(), held.sum()
    risk, keep = [], []
    alive = held.copy()
    for t in range(1, 5):
        obs = alive & ~np.isnan(M[:, t])
        k = obs & (M[:, t] == 1)
        risk.append(obs.sum()); keep.append(k.sum())
        alive = k
    return n1, h1, np.array(risk), np.array(keep)

def km_curve(M):
    """Share holding at every turn up to t (t = 1..5): product-limit estimate p1 * prod r_t, which treats
    content-filter notices and API error strings as censoring rather than as loss of stance."""
    n1, h1, risk, keep = counts(M)
    S = [h1 / n1]
    for k, n in zip(keep, risk): S.append(S[-1] * (k / n if n else 1.0))
    return np.array(S)

def K_values(M):
    """For chains holding at turn 1: number of pushback turns survived (0-4), and censoring flag (True if survived to last observed turn)."""
    out = []
    for row in M:
        if np.isnan(row[0]) or row[0] != 1: continue
        k = 0; cens = True; last = 4
        for t in range(1, 5):
            if np.isnan(row[t]): last = t - 1; break
            if row[t] == 1: k += 1
            else: cens = False; break
        out.append((k, cens, last))
    return out

def ll_geom(r, K):
    ll = 0.0
    for k, cens, last in K:
        ll += k * np.log(r) + (0 if cens else np.log(1 - r))
    return ll

def ll_betageom(a, b, K):
    # per-item r ~ Beta(a, b): P(survive k then fail) = B(a+k, b+1)/B(a,b); P(survive k, censored) = B(a+k, b)/B(a,b)
    ll = 0.0
    for k, cens, last in K:
        ll += (betaln(a + k, b) if cens else betaln(a + k, b + 1)) - betaln(a, b)
    return ll

def fit_betageom(K):
    f = lambda p: -ll_betageom(np.exp(p[0]), np.exp(p[1]), K)
    best = None
    for x0 in ([0.5, -0.5], [2.0, 0.0], [0.0, 0.0], [3.0, 1.0]):
        res = optimize.minimize(f, x0, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-9, 'maxiter': 5000})
        if best is None or res.fun < best.fun: best = res
    a, b = np.exp(best.x)
    return a, b, -best.fun

def summarise(M):
    n1, h1, risk, keep = counts(M)
    rt = np.where(risk > 0, keep / np.maximum(risk, 1), np.nan)
    r = keep.sum() / risk.sum() if risk.sum() else np.nan
    # likelihood-ratio test: turn-specific vs constant retention (df = number of turns with risk > 0, minus 1)
    def bll(k, n, p):
        p = min(max(p, 1e-12), 1 - 1e-12); return k * np.log(p) + (n - k) * np.log(1 - p)
    ll1 = sum(bll(k, n, k / n) for k, n in zip(keep, risk) if n > 0)
    ll0 = sum(bll(k, n, r) for k, n in zip(keep, risk) if n > 0)
    df = int((risk > 0).sum()) - 1
    G = max(2 * (ll1 - ll0), 0.0)
    K = K_values(M)
    out = dict(n_items=int(n1), p1=h1 / n1, risk=risk.tolist(), keep=keep.tolist(), r_t=rt.tolist(), r=r,
               S5_obs=float(km_curve(M)[4]),
               S5_geom=h1 / n1 * r ** 4, LRT_turn_G=G, LRT_turn_df=df, LRT_turn_p=float(stats.chi2.sf(G, df)) if df > 0 else np.nan,
               half_life=np.log(0.5) / np.log(r) if 0 < r < 1 else (np.inf if r == 1 else np.nan))
    if len(K) >= 10 and 0 < r < 1:
        a, b, llb = fit_betageom(K)
        llg = ll_geom(r, K)
        Gb = max(2 * (llb - llg), 0.0)
        out.update(bg_a=a, bg_b=b, bg_mean_r=a / (a + b), bg_LRT_G=Gb,
                   bg_LRT_p=0.5 * stats.chi2.sf(Gb, 1) if Gb > 0 else 1.0,  # boundary (variance = 0) -> 50:50 mixture
                   AIC_geom=-2 * llg + 2, AIC_bg=-2 * llb + 4)
    return out

def boot_idx(n):
    return rng.integers(0, n, n)

def pctl(x):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))] if len(x) else [np.nan, np.nan]

def r_only(M):
    _, _, risk, keep = counts(M)
    return keep.sum() / risk.sum() if risk.sum() else np.nan

def p1_only(M):
    ok = ~np.isnan(M[:, 0]); return (M[ok, 0] == 1).mean()

def markov_debate(M):
    """Two-state chain over all judged debate turns: e = P(lose | held at t-1), a = P(regain | not held at t-1)."""
    le = ln = ra = rn = 0
    for row in M:
        for t in range(1, 5):
            if np.isnan(row[t]) or np.isnan(row[t - 1]): continue
            if row[t - 1] == 1: ln += 1; le += row[t] == 0
            else: rn += 1; ra += row[t] == 1
    e = le / ln if ln else np.nan; a = ra / rn if rn else np.nan
    ever_lost = [row for row in M if (row[:4] == 0).any() and row[0] == 1]
    returned = [row for row in ever_lost if any(row[i] == 0 and (row[i + 1:] == 1).any() for i in range(5))]
    return dict(e=e, a=a, n_hold=ln, n_lost=rn, stationary=a / (a + e) if (a + e) > 0 else np.nan,
                share_aligned_t5=float(np.nanmean(M[:, 4])), share_aligned_t=np.nanmean(M, axis=0).tolist(),
                n_ever_lost_from_held=len(ever_lost), n_returned=len(returned))

def main():
    out = {'main': {}, 'base': {}, 'seeds': {}, 'boot': {}, 'contrasts': {}, 'debate_markov': {}, 'meta': {}}
    mats = {s: {k: load_matrix(s, f[s]) for k, (n, f) in MODELS.items()} for s in SETTINGS}
    for s in SETTINGS:
        out['main'][s] = {k: summarise(mats[s][k]) for k in MODELS}
        out['base'][s] = {k: summarise(load_matrix(s, f[s])) for k, (n, f) in BASE.items() if s in f}
    out['seeds'] = {k: {f: summarise(load_matrix('factual', f)) for f in v} for k, v in SEEDS.items()}
    # seed agreement: survived all four pushbacks (among items holding at turn 1 in both runs) and turn-1 label
    seedagree = {}
    for k, v in SEEDS.items():
        Ms = [load_matrix('factual', f) for f in v]
        pairs = []
        for i in range(3):
            for j in range(i + 1, 3):
                a, b = Ms[i], Ms[j]
                t1 = (a[:, 0] == b[:, 0]).mean()
                both = (a[:, 0] == 1) & (b[:, 0] == 1)
                ka = first_loss_chain(np.nan_to_num(a))[both, 4]; kb = first_loss_chain(np.nan_to_num(b))[both, 4]
                pairs.append(dict(turn1_agree=t1, n_both_hold=int(both.sum()), surv5_agree=float((ka == kb).mean())))
        seedagree[k] = pairs
    out['seed_agreement'] = seedagree

    # cluster bootstrap over items, within setting, same resample for all models (keeps cross-model dependence)
    for s in SETTINGS:
        n = mats[s]['gpt-4o'].shape[0]
        bs = {k: {'p1': [], 'r': [], 'S5': [], 'r_t': []} for k in MODELS}
        pooled = {'r': [], 'p1': [], 'S5': []}
        for _ in range(B):
            idx = boot_idx(n)
            rs, p1s, s5s = [], [], []
            for k in MODELS:
                M = mats[s][k][idx]
                n1, h1, risk, keep = counts(M)
                r = keep.sum() / risk.sum() if risk.sum() else np.nan
                bs[k]['p1'].append(h1 / n1); bs[k]['r'].append(r)
                bs[k]['r_t'].append(np.where(risk > 0, keep / np.maximum(risk, 1), np.nan))
                s5 = km_curve(M)[4]; bs[k]['S5'].append(s5)
                rs.append(r); p1s.append(h1 / n1); s5s.append(s5)
            pooled['r'].append(np.nanmean(rs)); pooled['p1'].append(np.mean(p1s)); pooled['S5'].append(np.mean(s5s))
        out['boot'][s] = {k: dict(p1=pctl(v['p1']), r=pctl(v['r']), S5=pctl(v['S5']),
                                  r_t=[pctl(np.array(v['r_t'])[:, t]) for t in range(4)]) for k, v in bs.items()}
        out['boot'][s]['_mean_over_models'] = dict(r=pctl(pooled['r']), p1=pctl(pooled['p1']), S5=pctl(pooled['S5']))
        out['boot'][s]['_draws_mean_r'] = pooled['r']
        for k in MODELS: out['boot'][s][k]['_draws_r'] = bs[k]['r']
    # point estimates of mean over models
    for s in SETTINGS:
        out['main'][s]['_mean_over_models'] = dict(r=float(np.mean([out['main'][s][k]['r'] for k in MODELS])),
                                                    p1=float(np.mean([out['main'][s][k]['p1'] for k in MODELS])),
                                                    S5=float(np.mean([out['main'][s][k]['S5_obs'] for k in MODELS])))
    # contrasts between settings (independent item sets -> independent bootstrap draws)
    pairs = [('factual', 'stereotype'), ('factual', 'debate'), ('stereotype', 'debate')]
    for a, b in pairs:
        c = {}
        for k in MODELS:
            d = np.array(out['boot'][a][k]['_draws_r']) - np.array(out['boot'][b][k]['_draws_r'])
            c[k] = dict(diff=out['main'][a][k]['r'] - out['main'][b][k]['r'], ci=pctl(d))
        d = np.array(out['boot'][a]['_draws_mean_r']) - np.array(out['boot'][b]['_draws_mean_r'])
        c['_mean_over_models'] = dict(diff=out['main'][a]['_mean_over_models']['r'] - out['main'][b]['_mean_over_models']['r'], ci=pctl(d))
        c['_n_models_a_higher'] = int(sum(out['main'][a][k]['r'] > out['main'][b][k]['r'] for k in MODELS))
        c['_n_models_ci_excludes_0'] = int(sum((c[k]['ci'][0] > 0) or (c[k]['ci'][1] < 0) for k in MODELS))
        out['contrasts'][f'{a}_minus_{b}'] = c
    # rank correlation of model r between settings
    rk = {}
    for a, b in pairs:
        x = [out['main'][a][k]['r'] for k in MODELS]; y = [out['main'][b][k]['r'] for k in MODELS]
        rho, p = stats.spearmanr(x, y); rk[f'{a}_{b}'] = dict(rho=rho, p=p)
    out['rank_corr_r'] = rk
    for s in SETTINGS:
        for k in MODELS:
            del out['boot'][s][k]['_draws_r']
        del out['boot'][s]['_draws_mean_r']
    # debate two-state Markov (all turns judged)
    out['debate_markov'] = {k: markov_debate(mats['debate'][k]) for k in MODELS}
    # constancy summary
    cons = {}
    for s in SETTINGS:
        rows = [out['main'][s][k] for k in MODELS]
        cons[s] = dict(n_models=len(rows), n_LRT_turn_p_lt_05=int(sum(x['LRT_turn_p'] < 0.05 for x in rows if not np.isnan(x['LRT_turn_p']))),
                       n_bg_p_lt_05=int(sum(x.get('bg_LRT_p', 1) < 0.05 for x in rows)),
                       n_bg_AIC_better=int(sum(x.get('AIC_bg', np.inf) < x.get('AIC_geom', np.inf) for x in rows)),
                       n_with_bg_fit=int(sum('bg_LRT_p' in x for x in rows)),
                       pooled_r_t=[float(np.sum([x['keep'][t] for x in rows]) / np.sum([x['risk'][t] for x in rows])) for t in range(4)],
                       pooled_risk=[int(np.sum([x['risk'][t] for x in rows])) for t in range(4)])
    out['constancy'] = cons
    ph = {s: {k: dict(responses=int(filtered_mask(s, f[s]).sum()), items=int(filtered_mask(s, f[s]).any(1).sum()))
              for k, (n, f) in MODELS.items() if filtered_mask(s, f[s]).any()} for s in SETTINGS}
    out['meta'] = dict(bootstrap_resamples=B, seed=16, models=list(MODELS), model_names={k: v[0] for k, v in MODELS.items()},
                       placeholders_prompt0=ph,
                       n_chains_main=int(sum((~np.isnan(mats[s][k][:, 0])).sum() for s in SETTINGS for k in MODELS)))
    dump(out, 'fidelity.json')
    # long format for GEE
    rows = []
    for s in SETTINGS:
        for k in MODELS:
            M = mats[s][k]
            for i, row in enumerate(M):
                if np.isnan(row[0]) or row[0] != 1: continue
                for t in range(1, 5):
                    if np.isnan(row[t]): break
                    rows.append(dict(setting=s, model=k, item=f'{s}_{i}', turn=t + 1, keep=int(row[t] == 1)))
                    if row[t] != 1: break
    pd.DataFrame(rows).to_csv(os.path.join(RES, 'chains_long.csv'), index=False)
    for s in SETTINGS:
        print(s, {k: round(out['main'][s][k]['r'], 3) for k in MODELS}, 'mean', round(out['main'][s]['_mean_over_models']['r'], 3))
    print(out['constancy']); print({k: (round(v['diff'], 3), [round(x, 3) for x in v['ci']]) for k, v in out['contrasts']['factual_minus_stereotype'].items() if k.startswith('_mean')})

if __name__ == '__main__':
    main()
