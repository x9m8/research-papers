"""Validation of the usual-intake method against official NCI-method estimates: USDA ARS, WWEIA NHANES 2017-March 2020, 'Total usual nutrient intake
from food, beverages, and dietary supplements, among non-Hispanic White individuals', Tables TB 5, 8, 9, 13, 15, 17, 19 (% below EAR, 19+ by sex).
Same population (non-Hispanic White, 19+, not pregnant, two reliable recalls), same method as the main analysis (usual.usual with supp=True)."""
import json, numpy as np, pandas as pd
from common import RES, EAR, ageband
from usual import sample, usual, wprop
d = sample('P'); B = d[(d.RIDAGEYR >= 19) & (d.RIDEXPRG.fillna(2) != 1) & d.two & (d.RIDRETH3 == 3)].copy()
ARS = {'FDFE': (7, 20), 'VB12': ('<3', 7), 'VC': (39, 34), 'VD': (60, 55), 'CALC': (21, 42), 'MAGN': (48, 43), 'ZINC': (15, 14)}
rows = []
for n, (am, af) in ARS.items():
    U = usual(B, n, 0.0, True)
    for s, a in (('M', am), ('F', af)):
        g = B[B.sex == s]; ear = np.array([EAR[n][s][ageband(x)] for x in g.RIDAGEYR]); p, se = wprop(U[g.index] < ear, g)
        rows.append(dict(nutrient=n, sex=s, this_method=round(100 * p, 1), se=round(100 * se, 1), ars_nci=a))
V = pd.DataFrame(rows); V.to_csv(f'{RES}/validation_ars.csv', index=False); print(V.to_string(), len(B))
num = V[V.ars_nci.apply(lambda x: isinstance(x, (int, float)))]
print('mean abs diff', (num.this_method - num.ars_nci.astype(float)).abs().mean(), 'max', (num.this_method - num.ars_nci.astype(float)).abs().max())
