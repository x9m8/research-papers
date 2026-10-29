"""Analysis 6: sensitivity of loss/reconstruction estimates to two choices.
(i) Refusals: a few outputs refuse the task (pattern below; under 1.1% of outputs in every condition, concentrated
    on the five toxicity seed texts). Re-estimate e, a, a0 after dropping the five toxicity seed texts.
(ii) Word definition: all word types instead of content words (paper 1 used all words for spoken sentences).
Control words are the same per-chain draws as in restoration.py, so 'main' reproduces Table 1.
Point estimates only. Also counts refusals on toxicity seeds."""
import numpy as np, json, re
from data_load import llm_chains, content, toks, CONDITIONS
import restoration as rs
PAT = re.compile(r"\bI (cannot|can't|can not|won't|am unable|'m unable|apologi)|\bI'm sorry|as an ai", re.I)
out = {}
for d, lab in CONDITIONS:
    ch = llm_chains(d)
    nref = sum(bool(PAT.search(t[:200])) for c in ch for t in c['texts'][1:])
    nref_tox = sum(bool(PAT.search(t[:200])) for c in ch if c['tree'].startswith('Toxicity') for t in c['texts'][1:])
    def est(chains, fn):
        pool = sorted(set().union(*[fn(c['texts'][0]) for c in chains]))
        per = rs.counts(chains, fn, pool); e, a, a0 = rs.rates(per, sorted(per))
        return dict(e=float(e), a=float(a), a0=float(a0), plateau=float((a - a0) / (e + a - a0)))
    base = est(ch, content)
    notox = est([c for c in ch if not c['tree'].startswith('Toxicity')], content)
    allw = est(ch, lambda s: set(toks(s)))
    out[lab] = dict(refusal_outputs=nref, refusal_on_toxicity_seeds=nref_tox, refusal_rate=nref / sum(len(c['texts']) - 1 for c in ch), main=base, no_toxicity_seeds=notox, all_words=allw)
    print(lab, nref, {k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in out[lab].items() if isinstance(v, dict)}, flush=True)
json.dump(out, open('../results/sensitivity_results.json', 'w'), indent=1)
