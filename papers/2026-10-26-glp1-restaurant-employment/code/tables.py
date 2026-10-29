"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os
from common import RES, ROOT

E = json.load(open(f'{RES}/estimates.json'))['estimates']; D = json.load(open(f'{RES}/descriptives.json'))
ES = json.load(open(f'{RES}/event_study.json'))
f2 = lambda v: ('0.00' if v == 0 else f'{v:.3f}' if abs(v) < 0.005 else f'{v:.2f}').replace('-', '−')   # keep sign of tiny values
pv = lambda p: '<0.001' if p < 0.001 else f'{p:.3f}'.replace('-', '−')
ci = lambda m: f"{f2(m['b_pp'])} ({f2(m['lo_pp'])} to {f2(m['hi_pp'])})"

t1 = ['**Table 1.** Analysis sample. Counties with at least 1,000 Medicare Part D enrollees in 2019 and with employment, establishments and wages disclosed by the QCEW for both limited-service (NAICS 722513) and full-service (722511) restaurants in every year 2015–2025. Uptake is GLP-1 receptor agonist 30-day fills written by prescribers located in the county, divided by 12 and by the county\'s Part D enrollees, per 100 enrollees.', '',
      '| Quantity | Value |', '|:--|--:|',
      f"| Counties joined (exposure and QCEW) | {D['n_joined']:,} |",
      f"| … with ≥1,000 Part D enrollees in 2019 | {D['n_partd_ge_1000']:,} |",
      f"| … and restaurant data disclosed in all years (analysis sample) | {D['n_main']:,} |",
      f"| States (clusters) | {D['n_states']} |",
      f"| Share of Part D enrollees (2019) in joined counties covered by the sample | {100 * D['share_partd_main_of_all']:.1f}% |",
      f"| GLP-1 uptake 2019, mean across counties (enrollee-weighted) | {D['E_base_mean']:.2f} ({D['E_base_wmean']:.2f}) |",
      f"| GLP-1 uptake 2024, mean across counties (enrollee-weighted) | {D['E_end_mean']:.2f} ({D['E_end_wmean']:.2f}) |",
      f"| Change 2019–2024: median (10th–90th percentile) | {D['dE_median']:.2f} ({D['dE_p10']:.2f} to {D['dE_p90']:.2f}) |",
      f"| Change 2019–2024: SD after winsorising at 1st/99th percentiles | {D['sd']['dEw']:.2f} |",
      f"| Limited-service employment in sample, 2019 → 2025 | {D['emp']['lsr']['base_sum']/1e6:.2f} m → {D['emp']['lsr']['end_sum']/1e6:.2f} m |",
      f"| Full-service employment in sample, 2019 → 2025 | {D['emp']['fsr']['base_sum']/1e6:.2f} m → {D['emp']['fsr']['end_sum']/1e6:.2f} m |",
      f"| Mean county change in log employment 2019–2025, limited / full service | {f2(D['mean_dlog_pct']['lsr'])}% / {f2(D['mean_dlog_pct']['fsr'])}% |"]

rows = [('lsr_emp', 'Limited-service, employment'), ('lsr_est', 'Limited-service, establishments'), ('lsr_wag', 'Limited-service, total wages'),
        ('fsr_emp', 'Full-service, employment'), ('fsr_est', 'Full-service, establishments'), ('fsr_wag', 'Full-service, total wages'),
        ('diff_emp', 'Limited minus full, employment'), ('diff_est', 'Limited minus full, establishments'), ('diff_wag', 'Limited minus full, total wages'),
        ('pharm_emp', 'Pharmacies, employment (positive control)'), ('acc_emp', 'Accommodation, employment (placebo)'), ('groc_emp', 'Grocery, employment')]
t2 = ['**Table 2.** Long differences, 2019–2025. Coefficient on the 2019–2024 change in GLP-1 uptake (users per 100 Part D enrollees), expressed as the percentage change in the outcome per 1-point rise in uptake, and per standard deviation (SD) of the change. All models include state fixed effects, the outcome\'s own 2015–2019 change, log private employment (2019), log Part D enrollees (2019), uptake in 2019 and the 2015–2019 change in log private employment; standard errors clustered by state. MDE: minimum detectable effect at 80% power, two-sided 5% test.', '',
      '| Outcome | % per point (95% CI) | p | MDE per point | % per SD (95% CI) | n |', '|:--|--:|--:|--:|--:|--:|']
for k, l in rows:
    m = E[k]['main']
    t2.append(f"| {l} | {ci(m)} | {pv(m['p'])} | {f2(m['mde_pp'])} | {f2(m['b_sd'])} ({f2(m['lo_sd'])} to {f2(m['hi_sd'])}) | {m['n']:,} |")

specs = [('main', 'Main specification'), ('no_controls', 'State fixed effects only'), ('weighted', 'Weighted by 2019 employment'),
         ('to_2024', 'Outcome 2019–2024'), ('semtir', 'Exposure: semaglutide and tirzepatide only'), ('claims_share', 'Exposure: GLP-1 share of all Part D claims (per 1,000)'),
         ('unwinsorised', 'Exposure not winsorised'), ('partd_ge_5000', 'Counties with ≥5,000 Part D enrollees'),
         ('excl_2019_top_decile_E0', 'Excluding top decile of 2019 uptake'), ('plus_total_emp_growth', 'Adding 2019–2025 private employment growth')]
t3 = [f'**Table 3.** Robustness of the employment estimates. Percentage change per 1-point rise in uptake (95% CI); for the claims-share exposure the unit is one GLP-1 claim per 1,000 Part D claims (SD {E["lsr_emp"]["claims_share"]["sd_x"]:.2f}). n in brackets. The pre-trend row tests the four 2015–2018 event-study coefficients jointly (state-clustered F test).', '',
      '| Specification | Limited-service | Full-service | Limited minus full | Pharmacies | Accommodation |', '|:--|--:|--:|--:|--:|--:|']
for s, l in specs:
    cells = []
    for k in ('lsr_emp', 'fsr_emp', 'diff_emp', 'pharm_emp', 'acc_emp'):
        m = E[k].get(s)
        cells.append(f"{ci(m)} [{m['n']:,}]" if m else '—')
    t3.append(f'| {l} | ' + ' | '.join(cells) + ' |')
t3.append('| *Per SD of exposure, main specification* | ' + ' | '.join(f"{f2(E[k]['main']['b_sd'])} ({f2(E[k]['main']['lo_sd'])} to {f2(E[k]['main']['hi_sd'])})" for k in ('lsr_emp', 'fsr_emp', 'diff_emp', 'pharm_emp', 'acc_emp')) + ' |')
t3.append('| *Pre-2019 event-study coefficients, joint F-test p* | ' + ' | '.join(pv(ES[k]['pretrend_p']) for k in ('lsr', 'fsr', 'diff', 'pharm', 'acc')) + ' |')

tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables[:1500])
