"""Step 1. Build analysis series from the extracted Census files. Writes results/series_*.csv, size_distribution.csv,
concordance.csv, flags_summary.csv."""
import numpy as np, pandas as pd, json
from common import *

cbp, nes = load_cbp(), load_nes()
years = list(range(2004, 2025))

# ---- employer series (CBP) for the three aggregates and the four 4-digit/3-digit groups
def emp_row(naics, y):
    r = cbp[(cbp.naics == naics) & (cbp.year == y)]
    return r.iloc[0] if len(r) else None

rows = []
for y in years:
    row = {'year': y, 'naics_vintage': vintage(y)}
    for k, tag in [('316', 'leather'), ('31-33', 'mfg'), ('00', 'all')]:
        r = emp_row(k, y)
        if r is not None:
            row.update({f'{tag}_emp_est': r.est, f'{tag}_emp_jobs': r.emp, f'{tag}_emp_q1pay': r.qp1, f'{tag}_emp_pay': r.ap})
        n = nes[(nes.naics == k) & (nes.year == y)]
        row.update({f'{tag}_ne_firms': n.estab.iloc[0], f'{tag}_ne_receipts': n.rcptot.iloc[0], f'{tag}_ne_source': n.source.iloc[0]})
    rows.append(row)
S = pd.DataFrame(rows)
for tag in ['leather', 'mfg', 'all']:
    S[f'{tag}_ne_share'] = S[f'{tag}_ne_firms'] / (S[f'{tag}_ne_firms'] + S[f'{tag}_emp_est'])
    S[f'{tag}_ne_share_pct'] = 100 * S[f'{tag}_ne_share']
    S[f'{tag}_ne_receipts_per_firm_usd'] = 1000 * S[f'{tag}_ne_receipts'] / S[f'{tag}_ne_firms']
    S[f'{tag}_emp_jobs_per_est'] = S[f'{tag}_emp_jobs'] / S[f'{tag}_emp_est']
    S[f'{tag}_emp_pay_per_job_usd'] = 1000 * S[f'{tag}_emp_pay'] / S[f'{tag}_emp_jobs']
    for c in ['emp_est', 'emp_jobs', 'emp_pay', 'ne_firms', 'ne_receipts']:
        base = S.loc[S.year == 2004, f'{tag}_{c}'].iloc[0]
        S[f'{tag}_{c}_idx'] = 100 * S[f'{tag}_{c}'] / base
S.to_csv(f'{RES}/series_aggregate.csv', index=False)

# ---- sub-industry groups present in both programmes (3-digit-comparable): 3161, 3162, 3169 (+ 316992 employer only)
sub = []
for y in years:
    for k, lab in [('3161', 'Leather and hide tanning and finishing'), ('3162', 'Footwear'), ('3169', 'Other leather and allied products (incl. luggage, handbags)')]:
        r = emp_row(k, y); n = nes[(nes.naics == k) & (nes.year == y)]
        if len(n) == 0: continue
        d = {'year': y, 'naics': k, 'label': lab, 'ne_firms': n.estab.iloc[0], 'ne_receipts': n.rcptot.iloc[0]}
        if r is not None: d.update({'emp_est': r.est, 'emp_jobs': r.emp, 'emp_pay': r.ap, 'emp_nf': r.emp_nf, 'empflag': r.empflag})
        sub.append(d)
SG = pd.DataFrame(sub)
SG['ne_share_pct'] = 100 * SG.ne_firms / (SG.ne_firms + SG.emp_est)
SG.to_csv(f'{RES}/series_subindustry.csv', index=False)

# ---- 6-digit employer detail with harmonised groups (concordance)
H = {'316110': 'Tanning and finishing', '316210': 'Footwear', '316211': 'Footwear', '316212': 'Footwear', '316213': 'Footwear', '316214': 'Footwear',
     '316219': 'Footwear', '316992': 'Women\'s handbags and purses', '316991': 'Other leather goods and luggage', '316993': 'Other leather goods and luggage',
     '316999': 'Other leather goods and luggage', '316998': 'Other leather goods and luggage'}
d6 = cbp[cbp.naics.isin(H)].copy(); d6['group'] = d6.naics.map(H)
G = d6.groupby(['year', 'group'], as_index=False).agg(est=('est', 'sum'), n_codes=('naics', 'nunique'))
G.to_csv(f'{RES}/series_employer_harmonised_groups.csv', index=False)
# consistency: harmonised groups must add to 3-digit totals
chk = G.groupby('year').est.sum().to_frame('sum_groups').join(S.set_index('year').leather_emp_est)
chk['diff'] = chk.sum_groups - chk.leather_emp_est
chk.to_csv(f'{RES}/check_harmonised_groups_sum.csv')

# concordance table (codes observed in the files, by vintage)
conc = []
for v, ys in [(2002, range(2004, 2008)), (2007, range(2008, 2012)), (2012, range(2012, 2017)), (2017, range(2017, 2022)), (2022, range(2022, 2024))]:
    codes = sorted(set(cbp[(cbp.year.isin(list(ys))) & cbp.naics.str.len().eq(6)].naics))
    conc.append({'cbp_years': f'{min(ys)}-{max(ys)}', 'assumed_naics_vintage': v, 'six_digit_codes_in_file': ' '.join(codes)})
pd.DataFrame(conc).to_csv(f'{RES}/concordance_observed_codes.csv', index=False)

# ---- size distribution of employer establishments (NAICS 316 total)
sz = []
for y in range(2004, 2024):
    r = emp_row('316', y)
    known = r[['n_lt5', 'n_5_9', 'n_10_19', 'n_20_49', 'n_50_99', 'n_100_249']]
    assert known.notna().all(), y
    n250 = r.est - known.sum()                         # derived: all establishments with 250+ employees
    parts = list(known.values) + [n250]
    # check derived 250+ against published cells where they are numeric
    pub = np.nansum([r.n_250_499, r.n_500_999, r.n_1000plus]); nmiss = int(pd.isna(r[['n_250_499', 'n_500_999', 'n_1000plus']]).sum())
    d = {'year': y, 'est': r.est, 'derived_250plus': n250, 'published_250plus_sum': pub, 'n_suppressed_cells_250plus': nmiss}
    d.update({f'n_{lab}': p for lab, p in zip(SIZE_LAB, parts)})
    d.update({f'sh_{lab}': 100 * p / r.est for lab, p in zip(SIZE_LAB, parts)})
    sz.append(d)
Z = pd.DataFrame(sz); Z.to_csv(f'{RES}/size_distribution.csv', index=False)

# ---- flags
fl = []
for y in range(2004, 2024):
    t = cbp[(cbp.year == y) & cbp.naics.str.len().eq(6)]
    top = emp_row('316', y)
    fl.append({'year': y, 'noise_flag_316_emp': top.emp_nf, 'noise_flag_316_payroll': top.ap_nf, 'sixdigit_cells': len(t),
               'sixdigit_emp_withheld': int((t.emp_nf == 'D').sum() + (t.emp_nf.isna() & t.empflag.notna() & (t.emp == 0)).sum()),
               'sixdigit_with_empflag': int(t.empflag.notna().sum()),
               'size_cells_N_in_316_6digit_and_4digit': int(cbp[(cbp.year == y) & cbp.naics.str.startswith('316')][SIZE].isna().sum().sum())})
pd.DataFrame(fl).to_csv(f'{RES}/flags_summary.csv', index=False)
print(S[['year', 'leather_emp_est', 'leather_emp_jobs', 'leather_ne_firms', 'leather_ne_share_pct']].to_string())
print(chk['diff'].abs().max())
