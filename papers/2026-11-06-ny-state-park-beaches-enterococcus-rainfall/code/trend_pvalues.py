"""Adds two-sided Wald p-values for the by-waterbody year trends in results/trends.json,
computed from the coefficient and standard error already stored there (asymptotic normal
approximation, consistent with the clustered/model SEs statsmodels reports elsewhere in
this package). Run locally (no browser/Pyodide needed); idempotent.
"""
import json
from scipy.stats import norm
from common import RESULTS

path = f'{RESULTS}/trends.json'
t = json.load(open(path))
for wb, row in t['by_waterbody'].items():
    z = row['year_coef'] / row['year_se']
    row['year_z'] = z
    row['year_p'] = float(2 * (1 - norm.cdf(abs(z))))
json.dump(t, open(path, 'w'), indent=2, default=float)
print('updated', path)
