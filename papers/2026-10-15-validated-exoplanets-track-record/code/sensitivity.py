"""Sensitivity analyses for the calibration result and bounds on the true non-planet fraction.
S1  exclude overturns published before the validation paper (already known at the time)
S2  exclude overturns caused only by the archive's 30 MJup mass ceiling (brown dwarfs, low-mass stars)
S3  bounds on the non-planet fraction among Morton+2016 giants (R > 6 Earth radii):
      lower bound = overturned / all validated giants (every unchecked giant assumed a planet)
      'followed' estimate = overturned / (overturned + later weighed)  (checked giants assumed representative)
S4  upper bounds on the overturn rate for batches with no overturns, among planets later followed up
S5  time from validation to overturn."""
import json, numpy as np, pandas as pd
from scipy.stats import poisson, beta
from common import RES
from analysis import cp, cp_upper  # noqa (re-runs analysis; cheap)

Bt = pd.read_csv(f'{RES}/batches.csv'); P = pd.read_csv(f'{RES}/planets.csv')
R = pd.read_csv(f'{__import__("os").path.dirname(__file__)}/overturn_reasons.csv')
A = json.load(open(f'{RES}/analysis.json'))
Bt['over'] = Bt.status.isin(['removed', 'refuted'])
out = {}
pre = set(R[R.refuted_before_validation == 'yes'].pl_name); mass_only = set(R[R['class'] == 'mass above 30 MJup'].pl_name)
for paper in ['Morton et al. 2016', 'Crossfield et al. 2016', 'Livingston et al. 2018a']:
    g = Bt[(Bt.paper == paper) & Bt.status.notna()]
    exp = float(g.fpp.sum())
    o1 = int((g.over & ~g.pl_name.isin(pre)).sum()); o2 = int((g.over & ~g.pl_name.isin(mass_only)).sum())
    o3 = int((g.over & ~g.pl_name.isin(pre | mass_only)).sum())
    out[paper] = dict(expected=exp, observed=int(g.over.sum()),
                      S1_excl_prior=dict(observed=o1, p=float(poisson.sf(o1 - 1, exp)) if o1 else 1.0),
                      S2_excl_mass_ceiling=dict(observed=o2, p=float(poisson.sf(o2 - 1, exp)) if o2 else 1.0),
                      S1S2_both=dict(observed=o3, p=float(poisson.sf(o3 - 1, exp)) if o3 else 1.0))
# S3 giants
C = A['C_calibration']['morton_by_radius']
gi_n = C['6-10']['n'] + C['>10']['n']; gi_o = C['6-10']['observed'] + C['>10']['observed']; gi_m = C['6-10']['later_mass'] + C['>10']['later_mass']
out['S3_morton_giants'] = dict(n=gi_n, overturned=gi_o, later_weighed=gi_m, expected=C['6-10']['expected'] + C['>10']['expected'],
                               lower_bound=gi_o / gi_n, lower_ci=cp(gi_o, gi_n), followed_est=gi_o / (gi_o + gi_m), followed_ci=cp(gi_o, gi_o + gi_m))
sm_n = sum(C[b]['n'] for b in ['<2', '2-4', '4-6']); sm_m = sum(C[b]['later_mass'] for b in ['<2', '2-4', '4-6'])
out['S3_morton_small'] = dict(n=sm_n, overturned=0, later_weighed=sm_m, upper95_if_followed_representative=cp_upper(0, sm_m))
# S4 batches without overturns
B = pd.DataFrame(A['B_batches'])
z = B[B.overturned == 0]
out['S4_zero_overturn_batches'] = {r.paper: dict(n=int(r.n_credited), followed=int(r.followed), upper95_followed=cp_upper(0, int(r.followed)) if r.followed else None)
                                   for r in z.itertuples()}
grp = {'multiplicity (Rowe 2014)': ['Rowe et al. 2014'], 'machine learning (Kepler)': ['Armstrong et al. 2021', 'Valizadegan et al. 2022', 'Valizadegan et al. 2023'],
       'TESS validations': list(B[B.mission == 'TESS'].paper)}
out['S4_groups'] = {k: dict(n=int(B[B.paper.isin(v)].n_credited.sum()), followed=int(B[B.paper.isin(v)].followed.sum()), overturned=int(B[B.paper.isin(v)].overturned.sum()),
                            upper95_followed=cp_upper(int(B[B.paper.isin(v)].overturned.sum()), int(B[B.paper.isin(v)].followed.sum())))
                    for k, v in grp.items()}
# S5 time to overturn
vy = {'Morton et al. 2016': 2016, 'Crossfield et al. 2016': 2016, 'Livingston et al. 2018a': 2018, 'Christiansen et al. 2022': 2022}
R['vyear'] = R.validated_by.str.extract(r'^(\w[\w ]+? et al\. \d{4}\w?)')[0].map(vy)
R['lag'] = R.refuting_year - R.vyear
out['S5_lag'] = dict(median=float(R.lag.median()), min=int(R.lag.min()), max=int(R.lag.max()), n_before=int((R.lag < 0).sum()),
                     by_class=R['class'].value_counts().to_dict())
json.dump(out, open(f'{RES}/sensitivity.json', 'w'), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
