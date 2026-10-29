"""Sensitivity of mu to the definition of an 'exact copy'.
raw: identical string after whitespace normalisation (case and punctuation count);
token: identical lowercase alphanumeric token sequence (main analysis);
content_set: identical set of content words (order, function words, inflection-free tokens ignored) - lenient.
L is always the parent's token length so mu stays per word."""
import json, re, numpy as np
from data_load import gistr_chains, meylan_chains, toks, content
from fidelity import fit_mu, boot
def rows(chains, same):
    out, seen = [], set()
    for c in chains:
        t, ids = c['texts'], c['ids']
        for i in range(len(t) - 1):
            if (ids[i], ids[i+1]) in seen: continue
            seen.add((ids[i], ids[i+1])); L = len(toks(t[i]))
            if L: out.append((c['tree'], L, int(same(t[i], t[i+1])), i+1))
    return out
norm = lambda s: re.sub(r'\s+', ' ', str(s)).strip()
defs = {'raw': lambda a, b: norm(a) == norm(b), 'token': lambda a, b: toks(a) == toks(b), 'content_set': lambda a, b: content(a) == content(b)}
data = {f'Gistr exp {e}': gistr_chains(e) for e in (1, 2, 3)}; data['Meylan et al. (spoken)'] = meylan_chains()
out = {}
for k, ch in data.items():
    out[k] = {}
    for d, f in defs.items():
        r = rows(ch, f); mu = fit_mu([x[1] for x in r], [x[2] for x in r])[0]; ci = boot(r, B=200)
        out[k][d] = dict(mu=float(mu), ci=[float(x) for x in ci], Q_obs=float(np.mean([x[2] for x in r])), Lstar_s02=float(np.log(1.2)/mu))
    print(k, {d: (round(v['mu'], 4), round(v['Q_obs'], 3), round(v['Lstar_s02'], 1)) for d, v in out[k].items()})
json.dump(out, open('../results/sensitivity_results.json', 'w'), indent=1)
