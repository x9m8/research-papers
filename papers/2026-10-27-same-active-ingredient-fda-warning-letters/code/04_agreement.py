"""Agreement between pass 1 (rules) and pass 2 (reader) before adjudication.
Output: results/agreement.csv, results/agreement.json, data/coding/disagreements.csv"""
import json
import numpy as np, pandas as pd
from sklearn.metrics import cohen_kappa_score
from common import RES, CODING, CODES, CODE_LABEL

p1 = pd.read_csv(f'{CODING}/pass1_rules.csv').set_index('slug')
p2 = pd.read_csv(f'{CODING}/pass2_reader.csv').set_index('slug').loc[p1.index]

def kappa(a, b):
    if len(set(a)) == 1 and len(set(b)) == 1:
        return None  # undefined: both constant
    return float(cohen_kappa_score(a, b))

rows = []
for var in ['eligible', 'seller_type'] + CODES:
    a, b = p1[var].values, p2[var].values
    rows.append(dict(variable=var, label=CODE_LABEL.get(var, var), n=len(a), agree=int((a == b).sum()),
                     pct_agree=float((a == b).mean()), kappa=kappa(a, b),
                     n_pass1=int((a == 1).sum()) if var not in ('seller_type',) else None,
                     n_pass2=int((b == 1).sum()) if var not in ('seller_type',) else None))
ag = pd.DataFrame(rows)
ag.to_csv(f'{RES}/agreement.csv', index=False)
codes_only = ag[ag.variable.isin(CODES)]
summ = dict(n_letters=len(p1), median_kappa_codes=float(codes_only.kappa.dropna().median()),
            min_kappa_codes=float(codes_only.kappa.dropna().min()), max_kappa_codes=float(codes_only.kappa.dropna().max()),
            mean_pct_agree_codes=float(codes_only.pct_agree.mean()),
            n_codes_kappa_ge_0_8=int((codes_only.kappa >= 0.8).sum()), n_codes_kappa_lt_0_6=int((codes_only.kappa < 0.6).sum()),
            n_codes=len(codes_only), total_cell_disagreements=int((len(p1) - codes_only.agree).sum()),
            seller_type=ag[ag.variable == 'seller_type'].iloc[0].to_dict(), eligible=ag[ag.variable == 'eligible'].iloc[0].to_dict())
json.dump(summ, open(f'{RES}/agreement.json', 'w'), indent=1, default=str)
# disagreement list for adjudication
d = []
for var in ['eligible', 'seller_type'] + CODES:
    for s in p1.index[p1[var] != p2[var]]:
        d.append(dict(slug=s, variable=var, pass1=p1.at[s, var], pass2=p2.at[s, var]))
pd.DataFrame(d).to_csv(f'{CODING}/disagreements.csv', index=False)
print(ag[['variable', 'n_pass1', 'n_pass2', 'pct_agree', 'kappa']].to_string()); print(json.dumps(summ, indent=1, default=str)[:600]); print(len(d), 'disagreements')
