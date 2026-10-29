"""Analysis 3: does exact copying fall with text length (as the error-threshold model assumes) or rise?
For conditions with enough exact copies (base models), fit a logistic regression of exact copy on
log2(parent length in words) with seed-text fixed effects, so the slope is estimated within seed texts.
95% CI from a cluster bootstrap over seed texts (500 resamples). Also reports exact-copy rates by length bin.
A negative slope is what independent per-word error predicts; a positive slope contradicts it.
Seed 20261012."""
import numpy as np, json, warnings
import statsmodels.api as sm
from data_load import llm_chains, CONDITIONS
from fidelity import rows_for
warnings.filterwarnings('ignore')
rng = np.random.default_rng(20261012)
BINS = [0, 50, 100, 150, 250, 100000]

def slope(rows):
    trees = sorted(set(r[0] for r in rows))
    keep = [t for t in trees if 0 < np.mean([r[2] for r in rows if r[0] == t]) < 1]  # FE needs variation
    rr = [r for r in rows if r[0] in keep]
    x = np.log2([r[1] for r in rr]); y = np.array([r[2] for r in rr])
    D = np.array([[r[0] == t for t in keep[1:]] for r in rr], float)
    X = np.column_stack([np.ones(len(rr)), x, D])
    return sm.GLM(y, X, family=sm.families.Binomial()).fit().params[1], len(keep)

if __name__ == '__main__':
    out = {}
    for d, lab in CONDITIONS:
        rows = rows_for(llm_chains(d))
        L = np.array([r[1] for r in rows]); y = np.array([r[2] for r in rows])
        binned = [dict(lo=BINS[i], hi=BINS[i + 1], n=int(((L >= BINS[i]) & (L < BINS[i + 1])).sum()),
                       rate=float(y[(L >= BINS[i]) & (L < BINS[i + 1])].mean()) if ((L >= BINS[i]) & (L < BINS[i + 1])).any() else None)
                  for i in range(len(BINS) - 1)]
        res = dict(binned=binned)
        if y.sum() >= 100:
            b, k = slope(rows)
            trees = sorted(set(r[0] for r in rows)); by = {t: [r for r in rows if r[0] == t] for t in trees}
            bs = []
            for _ in range(500):
                rr = []
                for j, i in enumerate(rng.choice(len(trees), len(trees))):
                    rr += [(f'{r[0]}#{j}',) + r[1:] for r in by[trees[i]]]
                try: bs.append(slope(rr)[0])
                except Exception: pass
            res.update(slope_log2L=float(b), slope_ci=[float(v) for v in np.percentile(bs, [2.5, 97.5])],
                       odds_ratio_per_doubling=float(np.exp(b)), n_trees_used=k, n_boot=len(bs))
        out[lab] = res
        print(lab, {k: v for k, v in res.items() if k != 'binned'}, [(x['lo'], x['n'], None if x['rate'] is None else round(x['rate'], 3)) for x in binned], flush=True)
    json.dump(out, open('../results/length_effect.json', 'w'), indent=1)
