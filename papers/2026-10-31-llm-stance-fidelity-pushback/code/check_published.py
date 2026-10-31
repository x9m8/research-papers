"""Check: API error strings in the released Claude 3.7 Sonnet debate outputs and their effect on Turn of Flip (ToF).
Hong et al. (2025, Table 2) report ToF 4.47 and NoF 0.25 for Claude-3.7-Sonnet in the debate setting -> results/published_check.json"""
import numpy as np
from common import *

d = pd.read_csv(label_path('debate', 'claude'))
F = filtered_mask('debate', 'claude')
L = d[[f'Response_{t}' for t in TURNS]].to_numpy()
judged0_on_error = int(((L == 0) & F).sum())
clean = ~F.any(1)
def tof(row):
    k = 0
    for x in row:
        if x == 1: k += 1
        else: break
    return k
out = dict(released_mean_ToF=float(d['ToF'].mean()), released_mean_NoF=float(d['NoF'].mean()),
           n_error_responses=int(F.sum()), n_items_with_error=int(F.any(1).sum()), n_error_responses_labelled_0=judged0_on_error,
           first_turn_of_error=pd.Series(F.argmax(1)[F.any(1)] + 1).value_counts().sort_index().to_dict(),
           mean_ToF_items_without_errors=float(np.mean([tof(r) for r in L[clean]])), n_items_without_errors=int(clean.sum()))
dump(out, 'published_check.json'); print(out)
