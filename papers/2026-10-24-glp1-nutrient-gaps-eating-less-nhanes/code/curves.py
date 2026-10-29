"""Prevalence below EAR as a continuous function of the proportional intake reduction (2021-2023 main sample)."""
import json, numpy as np, pandas as pd
from common import RES, EAR, ageband
from usual import sample, usual, wprop, NUTS
d = sample('L'); E = d[d.eligible & d.two].copy()
U = pd.DataFrame({n: usual(E, n) for n in NUTS}, index=E.index)
rs = np.round(np.arange(0, 0.451, 0.01), 2); out = {}
for n in ['PROT', 'ZINC', 'FDFE', 'CALC', 'MAGN', 'VB12', 'VARA', 'VC', 'IRON']:
    vals = []
    for r in rs:
        X = U[n] * (1 - r)
        if n == 'PROT': y = X < 0.66 * E.refwt; m = pd.Series(True, index=E.index)
        else:
            ear = np.array([EAR[n][s][a] for s, a in zip(E.sex, E.ab)]); y = X < ear
            m = ~((E.sex == 'F') & (E.RIDAGEYR < 51)) if n == 'IRON' else pd.Series(True, index=E.index)
        vals.append(wprop(y[m], E[m])[0])
    out[n] = vals
# number of nutrients (of the 10 EAR nutrients incl. protein) below EAR per person
cnt = {}
for r in [0, 0.16, 0.24, 0.35, 0.39]:
    k = (U.PROT * (1 - r) < 0.66 * E.refwt).astype(int)
    for n in EAR:
        if n in ('VD', 'ATOC', 'IRON'): continue
        ear = np.array([EAR[n][s][a] for s, a in zip(E.sex, E.ab)]); k = k + (U[n] * (1 - r) < ear).astype(int)
    w = E.w / E.w.sum()
    cnt[str(r)] = {'mean': float(np.sum(w * k)), 'ge3': float(np.sum(w * (k >= 3))), 'ge5': float(np.sum(w * (k >= 5)))}
json.dump(dict(r=list(map(float, rs)), prev=out, counts=cnt, counts_note='protein, vitamin A, C, B12, folate, calcium, magnesium, zinc (8 nutrients; vitamins D and E and iron excluded)'), open(f'{RES}/curves.json', 'w'), indent=1)
print(json.dumps(cnt, indent=1))
