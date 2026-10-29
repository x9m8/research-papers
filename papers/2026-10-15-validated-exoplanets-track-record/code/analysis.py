"""Main analyses. Run after build.py.
A. Catalogue composition: how many listed planets rest on a discovery without a measured mass.
B. Track record by validation paper: validated, overturned, independently weighed, controversial.
C. Calibration: observed overturns vs the expected number implied by each paper's own FPPs (sum of FPPs),
   overall, by planet radius, and restricted to planets that were later followed up.
D. Follow-up over time: cumulative fraction of validation-class planets that received a later mass measurement.
E. TESS: validated TESS planets whose TOI now carries a TFOPWG false-positive disposition.
Exact Poisson tails and Clopper-Pearson intervals (scipy). Seed not needed (no randomness)."""
import json, numpy as np, pandas as pd
from scipy.stats import poisson, beta
from common import nea, RES, mission

P = pd.read_csv(f'{RES}/planets.csv')
Bt = pd.read_csv(f'{RES}/batches.csv')
comp = nea('comp')
out = {}

def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k)
    return [float(lo), float(hi)]

def cp_upper(k, n, a=0.05):  # one-sided 95% upper bound
    return float(beta.ppf(1 - a, k + 1, n - k)) if n > 0 else 1.0

# ---------------- A. composition ----------------
L = P[P.status == 'listed']
nomass_ever = L[~L.mass_at_disc & ~L.later_mass]
A = dict(n_all_planets=int(len(comp)), n_transit=int(len(L)),
         n_no_mass_at_disc=int((~L.mass_at_disc).sum()), n_no_mass_ever=int(len(nomass_ever)),
         share_all_planets_no_mass_ever=float(len(nomass_ever) / len(comp)),
         share_transit_no_mass_ever=float(len(nomass_ever) / len(L)),
         by_mission={m: dict(n=int(len(g)), no_mass_at_disc=int((~g.mass_at_disc).sum()), no_mass_ever=int((~g.mass_at_disc & ~g.later_mass).sum()))
                     for m, g in L.groupby('mission')})
yr = L.groupby('disc_year').agg(n=('pl_name', 'size'), nomass_disc=('mass_at_disc', lambda s: int((~s).sum())))
A['by_year'] = {int(k): dict(n=int(v.n), nomass_disc=int(v.nomass_disc)) for k, v in yr.iterrows()}
out['A_composition'] = A

# ---------------- B. track record by paper ----------------
BATCHES = {  # bibcode -> (label, mission, method); methods checked in audits/citation_audit.md
    '2014ApJ...784...45R': ('Rowe et al. 2014', 'Kepler', 'multiplicity'),
    '2016ApJ...822...86M': ('Morton et al. 2016', 'Kepler', 'vespa FPP'),
    '2021MNRAS.504.5327A': ('Armstrong et al. 2021', 'Kepler', 'machine learning'),
    '2022ApJ...926..120V': ('Valizadegan et al. 2022', 'Kepler', 'machine learning (ExoMiner)'),
    '2023AJ....166...28V': ('Valizadegan et al. 2023', 'Kepler', 'machine learning (ExoMiner) + multiplicity'),
    '2015ApJ...809...25M': ('Montet et al. 2015', 'K2', 'vespa FPP'),
    '2016ApJS..226....7C': ('Crossfield et al. 2016', 'K2', 'vespa FPP'),
    '2016ApJ...827...78S': ('Sinukoff et al. 2016', 'K2', 'vespa FPP'),
    '2017AJ....154..207D': ('Dressing et al. 2017', 'K2', 'vespa FPP'),
    '2018AJ....155..136M': ('Mayo et al. 2018', 'K2', 'vespa FPP'),
    '2018AJ....156...78L': ('Livingston et al. 2018a', 'K2', 'vespa FPP'),
    '2018AJ....156..277L': ('Livingston et al. 2018b', 'K2', 'vespa FPP'),
    '2018AJ....155..127H': ('Hirano et al. 2018', 'K2', 'vespa FPP'),
    '2019A&A...627A..66H': ('Heller et al. 2019', 'K2', 'vespa FPP'),
    '2020MNRAS.499.5416C': ('Castro Gonzalez et al. 2020', 'K2', 'vespa FPP'),
    '2021MNRAS.508..195D': ('de Leon et al. 2021', 'K2', 'vespa FPP'),
    '2022AJ....163..244C': ('Christiansen et al. 2022', 'K2', 'vespa FPP'),
    '2021AJ....161...24G': ('Giacalone et al. 2021', 'TESS', 'TRICERATOPS'),
    '2022AJ....163...99G': ('Giacalone et al. 2022', 'TESS', 'TRICERATOPS'),
    '2023AJ....166....9M': ('Mistry et al. 2023', 'TESS', 'VaTEST (TRICERATOPS)'),
    '2024PASA...41...30M': ('Mistry et al. 2024', 'TESS', 'VaTEST (TRICERATOPS)'),
    '2024AJ....167..233H': ('Hord et al. 2024', 'TESS', 'vespa + TRICERATOPS'),
    '2026MNRAS.548ag512L': ('Lafarga et al. 2026', 'TESS', 'machine learning (RAVEN)'),
    '2026arXiv260821560C': ('Collier et al. 2026', 'TESS', 'TRICERATOPS (automated pipeline)'),
}
# The archive credits K2-51 b, K2-67 b and K2-76 b to a candidate catalogue (Vanderburg et al. 2016, ApJS 222, 14) that
# validated nothing; Shporer et al. (2017) identify the validating paper as Crossfield et al. (2016). Credit them there.
REASSIGN = {'2016ApJS..222...14V': '2016ApJS..226....7C'}
P['val_bib'] = P.disc_bib.replace(REASSIGN)
rows = []
for bib, (paper, mis, meth) in BATCHES.items():
    g = P[(P.val_bib == bib) & (P.mission == mis) & ~P.mass_at_disc.astype(bool)]
    n = len(g); over = int(g.status.isin(['removed', 'refuted']).sum()); lm = int(g.later_mass.sum()); cv = int(g.controv.sum())
    rows.append(dict(paper=paper, bib=bib, mission=mis, method=meth, n_credited=n, overturned=over, controversial=cv, later_mass=lm,
                     followed=lm + over, frac_followed=(lm + over) / n if n else None,
                     overturn_rate=over / n if n else None, overturn_ci=cp(over, n) if n else None,
                     overturn_upper95=cp_upper(over, n) if n else None,
                     overturn_rate_followed=over / (lm + over) if (lm + over) else None,
                     overturn_followed_ci=cp(over, lm + over) if (lm + over) else None,
                     median_year=float(g.disc_year.median()) if n else None))
B = pd.DataFrame(rows)
out['B_batches'] = B.to_dict(orient='records')
tot = B.groupby('mission')[['n_credited', 'overturned', 'later_mass', 'followed', 'controversial']].sum()
out['B_by_mission'] = {m: {k: int(v) for k, v in r.items()} for m, r in tot.iterrows()}
allv = B[['n_credited', 'overturned', 'later_mass', 'followed']].sum()
out['B_all'] = {k: int(v) for k, v in allv.items()}
out['B_all']['overturn_rate'] = allv.overturned / allv.n_credited
out['B_all']['overturn_ci'] = cp(int(allv.overturned), int(allv.n_credited))
out['B_all']['overturn_rate_followed'] = allv.overturned / allv.followed
out['B_all']['overturn_followed_ci'] = cp(int(allv.overturned), int(allv.followed))

# ---------------- C. calibration against each paper's own FPPs ----------------
Bt['over'] = Bt.status.isin(['removed', 'refuted'])
Bt = Bt.merge(P[['pl_name', 'pl_rade']], on='pl_name', how='left')
C = {}
for paper, g in Bt.groupby('paper'):
    g = g[g.status.notna()]
    exp = float(g.fpp.sum()); obs = int(g.over.sum())
    gf = g[g.over | g.later_mass.fillna(False).astype(bool)]
    C[paper] = dict(n=int(len(g)), expected=exp, observed=obs, p_tail=float(poisson.sf(obs - 1, exp)) if obs > 0 else 1.0,
                    ratio=obs / exp if exp > 0 else None, median_fpp=float(g.fpp.median()), n_fpp_upper_limits=int(g.fpp_upper.sum()),
                    n_followed=int(len(gf)), expected_followed=float(gf.fpp.sum()), observed_followed=int(gf.over.sum()),
                    p_tail_followed=float(poisson.sf(int(gf.over.sum()) - 1, gf.fpp.sum())) if gf.over.sum() > 0 else 1.0,
                    overturned=sorted(g[g.over].pl_name.tolist()))
ORDER = {'Montet et al. 2015': 0, 'Morton et al. 2016': 1, 'Crossfield et al. 2016': 2, 'Mayo et al. 2018': 3, 'Livingston et al. 2018a': 4, 'Livingston et al. 2018b': 5}
pool = Bt[Bt.status.notna()].assign(o=Bt.paper.map(ORDER)).sort_values('o', kind='stable').drop_duplicates('pl_name', keep='first')   # each planet once, under the earliest paper
C['pooled_unique_planets'] = dict(n=int(len(pool)), expected=float(pool.fpp.sum()), observed=int(pool.over.sum()),
                                  p_tail=float(poisson.sf(int(pool.over.sum()) - 1, pool.fpp.sum())))
# Morton by radius
m = Bt[(Bt.paper == 'Morton et al. 2016') & Bt.status.notna()].copy()
mr = vizier_r = None
from common import vizier
mt = vizier('J/ApJ/822/86/table6'); mt = mt[mt.Kepler != '']
mt['pl_name'] = 'Kepler-' + mt.Kepler.str.replace(r'([a-z])$', r' \1', regex=True); mt['Rp_m'] = pd.to_numeric(mt.Rp, errors='coerce')
m = m.merge(mt[['pl_name', 'Rp_m']], on='pl_name', how='left')
bins = [0, 2, 4, 6, 10, 1e3]; labels = ['<2', '2-4', '4-6', '6-10', '>10']
m['rbin'] = pd.cut(m.Rp_m, bins, labels=labels, right=False)
C['morton_by_radius'] = {str(b): dict(n=int(len(g)), expected=float(g.fpp.sum()), observed=int(g.over.sum()), later_mass=int(g.later_mass.fillna(False).astype(bool).sum()),
                                      p_tail=float(poisson.sf(int(g.over.sum()) - 1, g.fpp.sum())) if g.over.sum() > 0 else 1.0)
                         for b, g in m.groupby('rbin', observed=False)}
C['morton_overturned_radii'] = sorted([round(x, 2) for x in m[m.over].Rp_m.tolist()])
out['C_calibration'] = C

# ---------------- D. follow-up over time ----------------
V = L[~L.mass_at_disc & L.mission.isin(['Kepler', 'K2', 'TESS'])].copy()
V['t0'] = pd.to_datetime(V.disc_pubdate, errors='coerce'); V['t1'] = pd.to_datetime(V.later_mass_date, errors='coerce')
V['dt'] = (V.t1 - V.t0).dt.days / 365.25
end = pd.Timestamp('2026-10-15')
V['age'] = (end - V.t0).dt.days / 365.25
D = {}
for mis, g in V.groupby('mission'):
    curve = []
    for yrs in range(0, 13):
        at_risk = g[g.age >= yrs]
        if len(at_risk) < 20: break
        curve.append(dict(years=yrs, n=int(len(at_risk)), frac=float(((at_risk.dt <= yrs) & at_risk.later_mass).mean())))
    # Kaplan-Meier cumulative incidence of a mass measurement; planets not yet weighed are censored at their age.
    ev = g.later_mass.astype(bool) & g.dt.notna()
    tt = np.where(ev, g.dt.clip(lower=0), g.age).astype(float); ok = ~np.isnan(tt); tt, evv = tt[ok], ev.values[ok]
    km = []; times = np.sort(np.unique(tt[evv]))
    def km_at(t_):
        s, v = 1.0, 0.0
        for u in times[times <= t_]:
            d = int(((tt == u) & evv).sum()); r = int((tt >= u).sum())
            if r > d: s *= 1 - d / r; v += d / (r * (r - d))
        return s, v
    for yrs in range(0, 14):
        r = int((tt >= yrs).sum())
        if r < 20: break
        s, v = km_at(yrs); se = s * np.sqrt(v)
        km.append(dict(years=yrs, at_risk=r, cum=float(1 - s), lo=float(max(0, 1 - s - 1.96 * se)), hi=float(min(1, 1 - s + 1.96 * se))))
    D[mis] = dict(n=int(len(g)), ever=int(g.later_mass.sum()), frac_ever=float(g.later_mass.mean()), median_age=float(g.age.median()), curve=curve, km=km)
out['D_followup'] = D

# ---------------- E. TESS validated planets vs TOI dispositions ----------------
cid = nea('cid'); toi = nea('toi2')
T = L[(L.mission == 'TESS') & ~L.mass_at_disc].merge(cid[['pl_name', 'tic_id']], on='pl_name', how='left')
T['tid'] = pd.to_numeric(T.tic_id.astype(str).str.replace('TIC ', ''), errors='coerce')
toi['tid'] = pd.to_numeric(toi.tid, errors='coerce')
mm = T.merge(toi[['tid', 'toi', 'tfopwg_disp', 'pl_orbper']].rename(columns={'pl_orbper': 'toi_per'}), on='tid', how='left')
mm = mm[(mm.toi_per.isna()) | (abs(mm.toi_per / mm.pl_orbper - 1) < 0.01)]
best = mm.dropna(subset=['toi']).drop_duplicates('pl_name')
E = dict(n_tess_validated_class=int(len(T)), matched_toi=int(len(best)), disp_counts=best.tfopwg_disp.value_counts(dropna=False).to_dict(),
         fp_like=best[best.tfopwg_disp.isin(['FP', 'FA'])][['pl_name', 'toi', 'tfopwg_disp', 'disc_ref']].to_dict(orient='records'))
out['E_tess'] = E

json.dump(out, open(f'{RES}/analysis.json', 'w'), indent=1, default=lambda o: o if not isinstance(o, (np.integer, np.floating)) else o.item())
print(json.dumps({k: (v if k not in ('B_batches', 'A_composition') else '...') for k, v in out.items()}, indent=1, default=str)[:6000])
print(B[['paper', 'mission', 'method', 'n_credited', 'overturned', 'later_mass', 'controversial', 'frac_followed']].to_string())
