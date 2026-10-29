"""Countries whose recorded exports exceed their supply (production + imports) at each stage, mean of 2015-2020, by factor set."""
import json, numpy as np, pandas as pd
import trace as tr
from common import DER, RES, CF_SETS
names = json.load(open(f'{DER}/regions.json'))['name']
rows = []
for cfn, by in [(c, 0) for c in CF_SETS] + [('Commission SWD', 30)]:
    cf = tr.cf_set(cfn)
    for t in range(2015, 2021):
        M = tr.matrices(t, cf); h = tr.H[tr.H.t == t].set_index('region').hides.copy()
        if by: h['76'] = tr.BA[(tr.BA.t == t) & (tr.BA.brazil_yield == by)].hides.iloc[0]
        regs = sorted(set(M.index.get_level_values(1)) | set(M.index.get_level_values(2)) | set(h.index)); ix = {r: n for n, r in enumerate(regs)}; N = len(regs)
        P = np.zeros((N, N)); P[np.arange(N), np.arange(N)] = h.reindex(regs).fillna(0).values
        for s in (1, 2, 3, 4):
            m = np.zeros((N, N)); ms = M.loc[s]
            m[[ix[a] for a in ms.index.get_level_values(0)], [ix[b] for b in ms.index.get_level_values(1)]] = ms.values
            gap = m.sum(0) - (P.sum(1) + m.sum(1))
            for i in np.nonzero(gap > 0)[0]: rows.append(dict(cf=cfn + (f' (Brazil {by} kg)' if by else ''), t=t, stage=s, region=regs[i], country=names.get(regs[i], regs[i]), gap_t=gap[i]))
            R, x, exp, Tm, _ = tr.kastner(m, P)
            mix = np.where(x[:, None] > 0, R / np.where(x[:, None] > 0, x[:, None], 1), 0); P = np.clip(x - exp, 0, None)[:, None] * mix
G = pd.DataFrame(rows); G.to_csv(f'{RES}/gap_by_country.csv', index=False)
top = G.groupby(['cf', 'stage', 'country']).gap_t.sum().div(6).reset_index().sort_values('gap_t', ascending=False).groupby(['cf', 'stage']).head(3)
out = {f'{r.cf} | stage {r.stage}': [] for r in top.itertuples()}
for r in top.itertuples(): out[f'{r.cf} | stage {r.stage}'].append([r.country, round(r.gap_t / 1e3, 1)])
json.dump(out, open(f'{RES}/gap_top_countries.json', 'w'), indent=1)
for k in sorted(out): print(k, out[k])
