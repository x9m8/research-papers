"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md."""
import json, os, pandas as pd
from common import *
S = pd.read_csv(f'{RES}/series_aggregate.csv').set_index('year'); J = json.load(open(f'{RES}/summary.json'))
SG = pd.read_csv(f'{RES}/series_subindustry.csv', dtype={'naics': str}); Z = pd.read_csv(f'{RES}/size_distribution.csv').set_index('year')
C = pd.read_csv(f'{RES}/concordance_observed_codes.csv')
n = lambda v: f'{v:,.0f}'
t1 = ['**Table 1.** US leather and allied product manufacturing (NAICS 316): employer establishments, employment and payroll (County Business Patterns, CBP) and nonemployer firms and receipts (Nonemployer Statistics, NES), selected years. Dollar values are nominal. The nonemployer share is nonemployer firms divided by nonemployer firms plus employer establishments. NES 2024 values: ' + f"{n(S.loc[2024,'leather_ne_firms'])} firms, ${S.loc[2024,'leather_ne_receipts']/1000:,.1f} million in receipts.", '',
      '| Year | Employer establishments | Employment (March) | Annual payroll ($ million) | Nonemployer firms | Nonemployer receipts ($ million) | Nonemployer share (%) |', '|:--|--:|--:|--:|--:|--:|--:|']
for y in [2004, 2008, 2012, 2016, 2020, 2023]:
    r = S.loc[y]; t1.append(f"| {y} | {n(r.leather_emp_est)} | {n(r.leather_emp_jobs)} | {r.leather_emp_pay/1000:,.1f} | {n(r.leather_ne_firms)} | {r.leather_ne_receipts/1000:,.1f} | {r.leather_ne_share_pct:.1f} |")
t2 = ['**Table 2.** Change from 2004 to 2023 in leather and allied products, all manufacturing and all industries (percent; nonemployer share in percentage points). Dollar values are nominal.', '',
      '| Measure | Leather (316) | Manufacturing (31-33) | All industries |', '|:--|--:|--:|--:|']
for lab, k in [('Employer establishments', 'employer_establishments'), ('Employer employment', 'employer_employment'), ('Employer annual payroll', 'employer_annual_payroll_nominal'),
               ('Nonemployer firms', 'nonemployer_firms'), ('Nonemployer receipts', 'nonemployer_receipts_nominal')]:
    t2.append(f"| {lab} | " + ' | '.join(f"{J['changes'][f'{t}_{k}']['pct_change']:+.1f}" for t in ['leather', 'mfg', 'all']) + ' |')
t2.append('| Nonemployer share, 2004 (%) | ' + ' | '.join(f"{J['share'][t]['2004']:.1f}" for t in ['leather', 'mfg', 'all']) + ' |')
t2.append('| Nonemployer share, 2023 (%) | ' + ' | '.join(f"{J['share'][t]['2023']:.1f}" for t in ['leather', 'mfg', 'all']) + ' |')
t2.append('| Change in share (pp) | ' + ' | '.join(f"{J['share'][t]['change_pp_2004_2023']:+.1f}" for t in ['leather', 'mfg', 'all']) + ' |')
t3 = ['**Table 3.** Employer establishments, nonemployer firms and nonemployer share by industry group within NAICS 316, 2004, 2012 and 2023. The groups are the 4-digit codes published in both programmes (both programmes publish the same 4-digit codes in every year).', '',
      '| Group | 2004: employer / nonemployer / share % | 2012: employer / nonemployer / share % | 2023: employer / nonemployer / share % |', '|:--|--:|--:|--:|']
for k, v in J['subindustry'].items():
    t3.append(f"| {k} {v['label']} | " + ' | '.join(f"{n(v[y]['emp_est'])} / {n(v[y]['ne_firms'])} / {v[y]['share_pct']:.1f}" for y in ['2004', '2012', '2023']) + ' |')
t4 = ['**Table 4.** Employer establishments in NAICS 316 by employment-size class (employees in the pay period including 12 March), CBP. Counts and percent of establishments. *1-4 in the 2004-2016 files, "under 5" in later files; in every year the classes sum to the establishment total. 250+ is the total minus the smaller classes.', '',
      '| Size class | 2004 n | 2004 % | 2013 n | 2013 % | 2023 n | 2023 % | Change in n, 2004-2023 | % change |', '|:--|--:|--:|--:|--:|--:|--:|--:|--:|']
for l in SIZE_LAB:
    ch = J['size']['change_n_2004_2023'][l]
    t4.append(f"| {l} | {n(Z.loc[2004,f'n_{l}'])} | {Z.loc[2004,f'sh_{l}']:.1f} | {n(Z.loc[2013,f'n_{l}'])} | {Z.loc[2013,f'sh_{l}']:.1f} | {n(Z.loc[2023,f'n_{l}'])} | {Z.loc[2023,f'sh_{l}']:.1f} | {ch['abs']:+.0f} | {ch['pct']:+.1f} |")
t4.append(f"| All | {n(Z.loc[2004,'est'])} | 100 | {n(Z.loc[2013,'est'])} | 100 | {n(Z.loc[2023,'est'])} | 100 | {J['size']['total_change_n_2004_2023']:+.0f} | {J['changes']['leather_employer_establishments']['pct_change']:+.1f} |")
t5 = ['**Table 5.** Six-digit NAICS codes present in the CBP files for NAICS 316, by reference-year block, and the harmonised groups used here.', '',
      '| CBP reference years | Assumed NAICS vintage | Six-digit codes in the file |', '|:--|--:|:--|']
for _, r in C.iterrows(): t5.append(f"| {r.cbp_years} | {r.assumed_naics_vintage} | {r.six_digit_codes_in_file} |")
t5.append('| Harmonised group | | Codes |'); 
t5 += ['| Tanning and finishing | | 316110 (all years) |', '| Footwear | | 316211, 316212, 316213, 316214, 316219 (to 2011); 316210 (from 2012) |', "| Women's handbags and purses | | 316992 (all years) |",
       '| Other leather goods and luggage | | 316991, 316993, 316999 (to 2011); 316998 (from 2012) |']
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n\n' + '\n'.join(t4) + '\n\n' + '\n'.join(t5) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
