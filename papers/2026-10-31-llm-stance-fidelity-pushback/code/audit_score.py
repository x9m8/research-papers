"""Compare the AI hand-audit labels (merged on audit_id + setting + model + item + turn, so a sample that differs from the frozen one is rejected) (results/audit_ai_labels.csv, written blind to the judge labels)
with SYCON-Bench's GPT-4o judge labels (results/audit_key.csv). Output results/audit.json."""
import numpy as np, pandas as pd
from common import *

k = pd.read_csv(os.path.join(RES, 'audit_key.csv')); a = pd.read_csv(os.path.join(RES, 'audit_ai_labels.csv'))
keys = ['audit_id', 'setting', 'model', 'item', 'turn']
d = k.merge(a, on=keys, how='outer', indicator=True, validate='1:1')
if not (d['_merge'] == 'both').all():
    raise ValueError('audit labels do not match the drawn sample (setting/model/item/turn); the sample is not the frozen one')
d = d.drop(columns='_merge')
d.to_csv(os.path.join(RES, 'audit_merged.csv'), index=False)
na = d[d['ai_label'].isna()]
d = d[d['ai_label'].notna()].copy(); d['ai_label'] = d['ai_label'].astype(int)

def kappa(x, y):
    po = (x == y).mean(); pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
    return (po - pe) / (1 - pe) if pe < 1 else np.nan

def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [c - h, c + h]

out = {'n_sampled': int(len(k)), 'n_not_a_response': int(len(na)), 'not_a_response_ids': na['audit_id'].tolist(),
       'not_a_response_judge_labels': na['judge'].tolist()}
for name, g in [('all', d)] + list(d.groupby('setting')):
    n = len(g); agree = int((g['judge'] == g['ai_label']).sum())
    out[name] = dict(n=n, agree=agree, pct_agree=agree / n, agree_ci=wilson(agree, n), kappa=kappa(g['judge'].values, g['ai_label'].values), pabak=2 * agree / n - 1,
                     judge_hold=int(g['judge'].sum()), ai_hold=int(g['ai_label'].sum()),
                     judge1_ai0=int(((g['judge'] == 1) & (g['ai_label'] == 0)).sum()),
                     judge0_ai1=int(((g['judge'] == 0) & (g['ai_label'] == 1)).sum()),
                     agree_high_conf=float((g[g['confidence'] == 'high']['judge'] == g[g['confidence'] == 'high']['ai_label']).mean()) if (g['confidence'] == 'high').any() else None,
                     n_high_conf=int((g['confidence'] == 'high').sum()))
dump(out, 'audit.json')
print(out)
print(d[d['judge'] != d['ai_label']][['audit_id', 'model', 'turn', 'judge', 'ai_label', 'confidence', 'note']].to_string())
