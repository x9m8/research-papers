"""Write manuscript tables (markdown) from results/*.json and overturn_reasons.csv, and insert them into the manuscript."""
import json, os, pandas as pd
from common import RES
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(f'{RES}/analysis.json')); S = json.load(open(f'{RES}/sensitivity.json'))
R = pd.read_csv(f'{HERE}/overturn_reasons.csv')

def pct(x): return f'{100 * x:.1f}'
def pv(p):
    if p >= 0.01: return f'{p:.2f}'
    if p >= 0.001: return f'{p:.4f}'
    m, e = f'{p:.1e}'.split('e'); return f'{m} × 10^{int(e)}^'

t1 = ['**Table 1.** Track record of 24 validation publications (archive discovery credit by bibcode; K2-51 b, K2-67 b and K2-76 b credited to Crossfield et al. 2016, which validated them; planets weighed in the credited paper excluded) and, for the six with machine-readable per-planet FPPs, calibration against each paper\'s list of validated planets. Followed = overturned or later weighed. Upper bound: one-sided 95% Clopper–Pearson bound on the overturn rate among followed planets when none were overturned.', '',
      '| Publication | Mission | Method | Planets | Over-turned | Weighed later | Followed | Upper bound |', '|:----------------------|:--------|:------------------|---------:|---------:|---------:|---------:|---------:|']
from scipy.stats import beta
for r in A['B_batches']:
    ub = f"{pct(beta.ppf(0.95, 1, r['followed']))}%" if r['overturned'] == 0 and r['followed'] else ('–' if r['overturned'] == 0 else '')
    t1.append(f"| {r['paper']} | {r['mission']} | {r['method']} | {r['n_credited']:,} | {r['overturned']} | {r['later_mass']} | {r['followed']} | {ub} |")
b = A['B_all']
t1.append(f"| **All** | | | **{b['n_credited']:,}** | **{b['overturned']}** | **{b['later_mass']}** | **{b['followed']}** | |")
t1 += ['', '*Calibration (each paper\'s own validated list and FPPs; p = Poisson P(X ≥ observed)).*', '',
       '| Validation paper | Planets | Median FPP | Expected | Observed | p |', '|:--------------------------|-------:|---------:|---------:|-------:|-----------:|']
C = A['C_calibration']
for p in ['Morton et al. 2016', 'Crossfield et al. 2016', 'Livingston et al. 2018a', 'Livingston et al. 2018b', 'Mayo et al. 2018', 'Montet et al. 2015']:
    c = C[p]; t1.append(f"| {p} | {c['n']:,} | {c['median_fpp'] * (1 + 1e-9):.1e} | {c['expected']:.3g} | {c['observed']} | {pv(c['p_tail']) if c['observed'] else '–'} |")
c = C['pooled_unique_planets']; t1.append(f"| Pooled, distinct planets | {c['n']:,} | | {c['expected']:.3g} | {c['observed']} | {pv(c['p_tail'])} |")

t2 = ['**Table 2.** The 21 overturned planets: what they turned out to be and who showed it. *The archive credits discovery to Vanderburg et al. (2016), a candidate catalogue. Before? = refuted before the validation paper appeared.', '',
      '| Planet | Validated by | What it was | Class | Shown by | Before? |', '|:-----------|:-----------------|:------------------------|:--------------|:-------------|:-----|']
for r in R.sort_values(['refuting_year', 'pl_name']).itertuples():
    t2.append(f"| {r.pl_name} | {r.validated_by.replace(' (discovery credited to Vanderburg et al. 2016)', '*')} | {r.what_it_was} | {r._4} | {r.refuting_paper} | {r.refuted_before_validation} |")

t3 = ['**Table 3.** Sensitivity of the calibration result. S1 drops overturns published before the validation paper; S2 drops overturns resting only on a mass above 30 Jupiter masses.', '',
      '| Paper | Expected | Observed | S1: observed (p) | S2: observed (p) | S1 + S2: observed (p) |', '|:--------------------------|-------:|-------:|------------:|------------:|------------:|']
for p in ['Morton et al. 2016', 'Crossfield et al. 2016', 'Livingston et al. 2018a']:
    s = S[p]; f = lambda k: f"{s[k]['observed']} ({pv(s[k]['p'])})"
    t3.append(f"| {p} | {s['expected']:.3g} | {s['observed']} | {f('S1_excl_prior')} | {f('S2_excl_mass_ceiling')} | {f('S1S2_both')} |")
g = S['S3_morton_giants']
t3 += ['', f"Morton et al. (2016) planets larger than 6 Earth radii: {g['n']} validated, {g['overturned']} overturned, {g['later_weighed']} weighed later, {g['expected']:.3f} expected. "
       f"Lower bound on non-planet fraction {pct(g['lower_bound'])}% (95% CI {pct(g['lower_ci'][0])}–{pct(g['lower_ci'][1])}%); among followed giants {pct(g['followed_est'])}% ({pct(g['followed_ci'][0])}–{pct(g['followed_ci'][1])}%)."]

tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = f'{HERE}/../manuscript/manuscript.md'; s = open(ms).read()
if 'TABLES_PLACEHOLDER' in s: s = s.replace('TABLES_PLACEHOLDER', tables)
else: s = s[:s.index('## Tables') + len('## Tables\n\n')] + tables + '\n' + s[s.index('## Figures'):]
open(ms, 'w').write(s); print(tables)
