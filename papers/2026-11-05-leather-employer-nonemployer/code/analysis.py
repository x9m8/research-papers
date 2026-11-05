"""Step 2. Descriptive statistics for the manuscript -> results/summary.json (every number in the text comes from here
or from the series_*.csv files)."""
import json, numpy as np, pandas as pd
from common import *

S = pd.read_csv(f'{RES}/series_aggregate.csv').set_index('year')
SG = pd.read_csv(f'{RES}/series_subindustry.csv', dtype={'naics': str})
Z = pd.read_csv(f'{RES}/size_distribution.csv').set_index('year')
G = pd.read_csv(f'{RES}/series_employer_harmonised_groups.csv')
out = {}

def pc(a, b): return 100 * (b / a - 1)

# ---- 1. changes, endpoint and CAGR
ch = {}
for tag in ['leather', 'mfg', 'all']:
    for c, lab in [('emp_est', 'employer_establishments'), ('emp_jobs', 'employer_employment'), ('emp_pay', 'employer_annual_payroll_nominal'),
                   ('ne_firms', 'nonemployer_firms'), ('ne_receipts', 'nonemployer_receipts_nominal')]:
        a, b = S.loc[2004, f'{tag}_{c}'], S.loc[2023, f'{tag}_{c}']
        ch[f'{tag}_{lab}'] = {'2004': float(a), '2023': float(b), 'pct_change': pc(a, b), 'cagr_pct': 100 * cagr(a, b, 19)}
ch['leather_nonemployer_firms_2024'] = {'2024': float(S.loc[2024, 'leather_ne_firms']), 'pct_change_2004_2024': pc(S.loc[2004, 'leather_ne_firms'], S.loc[2024, 'leather_ne_firms']),
                                         'receipts_2024': float(S.loc[2024, 'leather_ne_receipts']), 'receipts_pct_change_2004_2024': pc(S.loc[2004, 'leather_ne_receipts'], S.loc[2024, 'leather_ne_receipts'])}
for a, b in [(2004, 2009), (2009, 2019), (2019, 2023)]:
    ch[f'leather_{a}_{b}'] = {k: pc(S.loc[a, f'leather_{k}'], S.loc[b, f'leather_{k}']) for k in ['emp_est', 'emp_jobs', 'emp_pay', 'ne_firms', 'ne_receipts']}
# peak and trough
for k in ['emp_est', 'emp_jobs', 'ne_firms']:
    s = S[f'leather_{k}'].dropna()
    ch[f'leather_{k}_min'] = {'year': int(s.idxmin()), 'value': float(s.min())}; ch[f'leather_{k}_max'] = {'year': int(s.idxmax()), 'value': float(s.max())}
out['changes'] = ch

# ---- 2. productivity-like descriptives (nominal)
out['per_unit'] = {y: {'jobs_per_est': float(S.loc[y, 'leather_emp_jobs_per_est']), 'pay_per_job_usd': float(S.loc[y, 'leather_emp_pay_per_job_usd']),
                       'ne_receipts_per_firm_usd': float(S.loc[y, 'leather_ne_receipts_per_firm_usd']),
                       'mfg_ne_receipts_per_firm_usd': float(S.loc[y, 'mfg_ne_receipts_per_firm_usd']),
                       'all_ne_receipts_per_firm_usd': float(S.loc[y, 'all_ne_receipts_per_firm_usd'])} for y in [2004, 2009, 2019, 2023]}
out['ne_receipts_per_firm_ratio_to_all'] = {y: float(S.loc[y, 'leather_ne_receipts_per_firm_usd'] / S.loc[y, 'all_ne_receipts_per_firm_usd']) for y in [2004, 2012, 2023]}

# ---- 3. nonemployer share
sh = {}
for tag in ['leather', 'mfg', 'all']:
    s = S[f'{tag}_ne_share_pct'].dropna()
    sh[tag] = {'2004': float(s[2004]), '2008': float(s[2008]), '2012': float(s[2012]), '2019': float(s[2019]), '2021': float(s[2021]), '2023': float(s[2023]), 'change_pp_2004_2023': float(s[2023] - s[2004]),
               'change_pp_2004_2012': float(s[2012] - s[2004]), 'change_pp_2012_2021': float(s[2021] - s[2012]), 'change_pp_2021_2023': float(s[2023] - s[2021]),
               'max_year': int(s.idxmax()), 'max': float(s.max())}
# counterfactual decomposition for the leather share, 2004 -> 2023
n0, e0, n1, e1 = S.loc[2004, 'leather_ne_firms'], S.loc[2004, 'leather_emp_est'], S.loc[2023, 'leather_ne_firms'], S.loc[2023, 'leather_emp_est']
share = lambda n, e: 100 * n / (n + e)
sh['decomposition_pp'] = {'observed_change': share(n1, e1) - share(n0, e0),
                          'only_employer_changes (NE held at 2004)': share(n0, e1) - share(n0, e0),
                          'only_nonemployer_changes (employer held at 2004)': share(n1, e0) - share(n0, e0)}
# sensitivity: the 2007 value is derived (two states withheld); share change excluding it is unaffected because endpoints are 2004 and 2023
# year-to-year increases in share
d = S.leather_ne_share_pct.dropna().diff().dropna()
sh['leather_years_share_rose'] = int((d > 0).sum()); sh['leather_years_share_fell'] = int((d < 0).sum()); sh['leather_yoy_n'] = int(len(d))
# is the leather change larger than manufacturing / all industries?
sh['leather_minus_mfg_pp'] = sh['leather']['change_pp_2004_2023'] - sh['mfg']['change_pp_2004_2023']
sh['leather_minus_all_pp'] = sh['leather']['change_pp_2004_2023'] - sh['all']['change_pp_2004_2023']
out['share'] = sh

# subindustry share
sub = {}
for k in ['3161', '3162', '3169']:
    t = SG[(SG.naics == k)].set_index('year')
    sub[k] = {'label': t.label.iloc[0]}
    for y in [2004, 2012, 2023]:
        sub[k][str(y)] = {'emp_est': float(t.loc[y, 'emp_est']), 'ne_firms': float(t.loc[y, 'ne_firms']), 'share_pct': float(t.loc[y, 'ne_share_pct'])}
    sub[k]['emp_est_pct_change'] = pc(t.loc[2004, 'emp_est'], t.loc[2023, 'emp_est']); sub[k]['ne_pct_change'] = pc(t.loc[2004, 'ne_firms'], t.loc[2023, 'ne_firms'])
    sub[k]['emp_jobs_pct_change'] = pc(t.loc[2004, 'emp_jobs'], t.loc[2023, 'emp_jobs'])
    sub[k]['share_change_pp'] = float(t.loc[2023, 'ne_share_pct'] - t.loc[2004, 'ne_share_pct'])
out['subindustry'] = sub
# harmonised six-digit groups employer establishments
hg = {}
for g, t in G.groupby('group'):
    t = t.set_index('year'); hg[g] = {'2004': float(t.loc[2004, 'est']), '2011': float(t.loc[2011, 'est']), '2012': float(t.loc[2012, 'est']), '2023': float(t.loc[2023, 'est'])}
out['harmonised_groups'] = hg
# handbag detail vs other
C = load_cbp(); hb = C[C.naics == '316992'].set_index('year')
out['handbags_316992'] = {str(y): float(hb.loc[y, 'est']) for y in [2004, 2011, 2012, 2023]}

# ---- 4. NAICS-break diagnostic: year-on-year log change at vintage boundaries vs all other years.
# "Other years" is restricted to 2005-2023 for every series so the nonemployer series (which runs to 2024) is
# compared over the same window as the employer series (which ends in 2023), not given one extra data point.
bd = {}
for name, col in [('employer_establishments', 'leather_emp_est'), ('employer_employment', 'leather_emp_jobs'), ('nonemployer_firms', 'leather_ne_firms'),
                  ('nonemployer_receipts', 'leather_ne_receipts')]:
    s = S[col].dropna(); dl = np.log(s).diff().dropna() * 100
    dl = dl[dl.index <= 2023]
    isb = dl.index.isin(BREAK_YEARS)
    bd[name] = {'boundary_years': {str(y): float(dl.loc[y]) for y in BREAK_YEARS if y in dl.index},
                'median_abs_other_years': float(dl[~isb].abs().median()), 'max_abs_other_years': float(dl[~isb].abs().max()),
                'other_years_max_year': int(dl[~isb].abs().idxmax()), 'window': '2005-2023'}
out['break_diagnostic'] = bd
# NE all-industry and manufacturing jump at 2022
out['ne_2021_2022'] = {tag: pc(S.loc[2021, f'{tag}_ne_firms'], S.loc[2022, f'{tag}_ne_firms']) for tag in ['leather', 'mfg', 'all']}
out['ne_2021_2022_receipts'] = {tag: pc(S.loc[2021, f'{tag}_ne_receipts'], S.loc[2022, f'{tag}_ne_receipts']) for tag in ['leather', 'mfg', 'all']}
out['emp_2022_2023'] = {tag: pc(S.loc[2022, f'{tag}_emp_est'], S.loc[2023, f'{tag}_emp_est']) for tag in ['leather', 'mfg', 'all']}

# ---- 5. size distribution
sz = {}
for y in [2004, 2008, 2012, 2019, 2023]:
    r = Z.loc[y]; sz[str(y)] = {lab: {'n': float(r[f'n_{lab}']), 'pct': float(r[f'sh_{lab}'])} for lab in SIZE_LAB}
    sz[str(y)]['est'] = float(r.est)
    sz[str(y)]['pct_20plus'] = float(r['sh_20-49'] + r['sh_50-99'] + r['sh_100-249'] + r['sh_250+']); sz[str(y)]['pct_under10'] = float(r['sh_1-4*'] + r['sh_5-9'])
    sz[str(y)]['pct_100plus'] = float(r['sh_100-249'] + r['sh_250+'])
sz['change_n_2004_2023'] = {lab: {'abs': float(Z.loc[2023, f'n_{lab}'] - Z.loc[2004, f'n_{lab}']), 'pct': pc(Z.loc[2004, f'n_{lab}'], Z.loc[2023, f'n_{lab}'])} for lab in SIZE_LAB}
sz['total_change_n_2004_2023'] = float(Z.loc[2023, 'est'] - Z.loc[2004, 'est'])
# share of the total establishment loss by class
tot = sz['total_change_n_2004_2023']
sz['share_of_net_loss_pct'] = {lab: 100 * sz['change_n_2004_2023'][lab]['abs'] / tot for lab in SIZE_LAB}
sz['by_year_pct_under10'] = {int(y): float(Z.loc[y, 'sh_1-4*'] + Z.loc[y, 'sh_5-9']) for y in Z.index}
sz['by_year_pct_20plus'] = {int(y): float(Z.loc[y, 'sh_20-49'] + Z.loc[y, 'sh_50-99'] + Z.loc[y, 'sh_100-249'] + Z.loc[y, 'sh_250+']) for y in Z.index}
sz['n_250plus_by_year'] = {int(y): float(Z.loc[y, 'n_250+']) for y in Z.index}
# the 1-4 class relative to manufacturing and all industries
sz['mfg_pct_under10'] = {str(y): float(100 * (C[(C.naics == '31-33') & (C.year == y)][['n_lt5', 'n_5_9']].sum(axis=1).iloc[0]) / C[(C.naics == '31-33') & (C.year == y)].est.iloc[0]) for y in [2004, 2023]}
sz['all_pct_under10'] = {str(y): float(100 * (C[(C.naics == '00') & (C.year == y)][['n_lt5', 'n_5_9']].sum(axis=1).iloc[0]) / C[(C.naics == '00') & (C.year == y)].est.iloc[0]) for y in [2004, 2023]}
out['size'] = sz
# mean employment per establishment, excluding the under-5 class is not possible (no employment by class extracted)

# ---- 6. data quality
fl = pd.read_csv(f'{RES}/flags_summary.csv')
out['quality'] = {'withheld_sixdigit_cells_total': int(fl.sixdigit_emp_withheld.sum()), 'sixdigit_cells_total': int(fl.sixdigit_cells.sum()),
                  'years_with_withheld_cell': fl[fl.sixdigit_emp_withheld > 0].year.tolist(),
                  'N_size_cells_2017_2023_range': [int(fl[fl.year >= 2017].size_cells_N_in_316_6digit_and_4digit.min()), int(fl[fl.year >= 2017].size_cells_N_in_316_6digit_and_4digit.max())],
                  'noise_flags_316_emp': fl.noise_flag_316_emp.fillna('none').value_counts().to_dict(),
                  'size_sum_gap_max_for_316_pre2017': 0,
                  'ne_2007_derived': {'estab': float(S.loc[2007, 'leather_ne_firms']), 'states_flagged': 2}}
# NE 2007 sensitivity: interpolate between 2006 and 2008
interp = (S.loc[2006, 'leather_ne_firms'] + S.loc[2008, 'leather_ne_firms']) / 2
out['quality']['ne_2007_vs_mean_2006_2008'] = {'derived': float(S.loc[2007, 'leather_ne_firms']), 'mean_neighbours': float(interp)}
# check: 6-digit concordance sums
chk = pd.read_csv(f'{RES}/check_harmonised_groups_sum.csv'); out['quality']['harmonised_group_sum_max_abs_diff'] = float(chk['diff'].abs().max())
# employer: noise-sensitive series -> how much would +-5% noise on employment change the 2004-2023 decline? (bounds, not an estimate)
e0, e1 = S.loc[2004, 'leather_emp_jobs'], S.loc[2023, 'leather_emp_jobs']
out['quality']['employment_change_if_2023_noise_up_to_2pct'] = {'low': pc(e0, e1 * 0.98), 'high': pc(e0, e1 * 1.02)}
# cross-check against the Census 'America Counts' story (all industries, 2012-2023 and 2021, 2022 growth)
out['crosscheck_all'] = {'ne_cagr_2012_2023_pct': 100 * cagr(S.loc[2012, 'all_ne_firms'], S.loc[2023, 'all_ne_firms'], 11),
                         'employer_est_cagr_2012_2023_pct': 100 * cagr(S.loc[2012, 'all_emp_est'], S.loc[2023, 'all_emp_est'], 11),
                         'ne_growth_2021_pct': pc(S.loc[2020, 'all_ne_firms'], S.loc[2021, 'all_ne_firms']), 'ne_growth_2022_pct': pc(S.loc[2021, 'all_ne_firms'], S.loc[2022, 'all_ne_firms']),
                         'leather_ne_cagr_2012_2023_pct': 100 * cagr(S.loc[2012, 'leather_ne_firms'], S.loc[2023, 'leather_ne_firms'], 11),
                         'leather_emp_est_cagr_2012_2023_pct': 100 * cagr(S.loc[2012, 'leather_emp_est'], S.loc[2023, 'leather_emp_est'], 11)}
json.dump(out, open(f'{RES}/summary.json', 'w'), indent=1, default=float)
print(json.dumps(out['changes']['leather_employer_establishments']), json.dumps(out['share']['leather']), json.dumps(out['share']['decomposition_pp']))
print(json.dumps(out['break_diagnostic'], indent=0)[:1800])
