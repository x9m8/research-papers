"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import json, os
from common import RES, ROOT

E = json.load(open(f'{RES}/estimates.json'))['estimates']; B = json.load(open(f'{RES}/build.json'))
SM = json.load(open(f'{RES}/summary.json')); SC = json.load(open(f'{RES}/scm.json')); PN = json.load(open(f'{RES}/panel.json'))
mi = lambda s: s.replace('-', '−')
f2 = lambda v: mi(f'{v:.2f}') if abs(v) >= 0.005 or v == 0 else mi(f'{v:.3f}')
pv = lambda p: '<0.001' if p < 0.001 else f'{p:.3f}'
ci = lambda m: f"{f2(m['est'])} ({f2(m['lo'])} to {f2(m['hi'])})"
o1 = lambda v: ('−0.0' if -0.0005 < v < 0 else mi(f'{100 * v:.1f}').replace('−0.0', '0.0'))   # keep the sign of tiny negative bounds
lp = lambda m: f"{o1(m['est'])} ({o1(m['lo'])} to {o1(m['hi'])})"   # log points x 100
NAME = {'722': 'All food services and drinking places (722)', '722511': 'Full-service restaurants (722511)',
        '722513': 'Limited-service restaurants (722513)', '10': 'Total private employment (all industries)'}
SHORT = {'722': '722 all', '722511': '722511 full-service', '722513': '722513 limited-service', '10': 'Total private'}
OUTS = {'emp': 'Jobs', 'estabs': 'Estab.', 'wage': 'Wage'}
OUT = {'emp': 'Employment', 'estabs': 'Establishments', 'wage': 'Average weekly wage'}

S = B['schedule_by_year_q4']
t1 = ['**Table 1.** Minimum hourly rates in force for most of each year (dollars). General rates, fast-food rates and tipped food-service cash wages from the New York State Department of Labor, 12 NYCRR Part 146 and NYSDOB (2022); increases dated 31 December apply from the following year. Fast-food rate: chains of 30 or more establishments nationally (§146-3.13(b)), outside New York City; the effective rate is the higher of the fast-food and general rates. The log gap is ln(Long Island rate) − ln(rest-of-state rate). 2026: first quarter only in the data. Pennsylvania: $7.25 throughout.', '',
      '| Year | LI & Westchester | Rest of state | Gap ($) | Log gap | Tipped cash wage, LI | Tipped cash wage, rest of state | Fast food, LI (effective) | Fast food, rest of state |',
      '|:--|--:|--:|--:|--:|--:|--:|--:|--:|']
for y in sorted(S):
    v = S[y]; tip = lambda x: '—' if x is None else f'{x:.2f}'
    t1.append(f"| {y} | {v['mw_li']:.2f} | {v['mw_ros']:.2f} | {v['mw_li'] - v['mw_ros']:.2f} | {v['gap_general']:.3f} | {tip(v['tip_li'])} | {tip(v['tip_ros'])} | {v['ff_li']:.2f} | {v['ff_ros']:.2f} |")
t1.append('')
t1.append('— Tipped food-service cash wage before 31 December 2016 not tabulated; it was the same statewide, so the regional gap was zero. Fast food 2016: $9.75 outside New York City from 31 December 2015 (NYSDOB, 2022, Table 1). Fast food 2021: $14.50 until 30 June, $15.00 from 1 July (the table shows the later rate).')

t2 = ['**Table 2.** Analysis sample. Long Island = Nassau and Suffolk counties. Comparison = counties outside New York City, Long Island and Westchester with employment, establishments and wages disclosed by the QCEW in all 49 quarters, 2014Q1–2026Q1. Annual averages of quarterly values; average weekly wage = total wages / employment / 13.', '',
      '| Industry | Comparison counties | Employment 2016, LI / comparison | Employment change 2016–2025, LI / comparison | Average weekly wage 2016, LI / comparison | Average weekly wage 2025, LI / comparison |',
      '|:--|--:|--:|--:|--:|--:|']
for ind in ['722', '722511', '722513', '10']:
    s = SM[ind]
    t2.append(f"| {NAME[ind]} | {E[ind]['n_donors']} | {s['emp_2016']['LI']:,} / {s['emp_2016']['ROS']:,} | {mi(f'{s['emp_change_2016_2025_pct']['LI']:+.1f}')}% / {mi(f'{s['emp_change_2016_2025_pct']['ROS']:+.1f}')}% | ${s['aww_2016']['LI']:,.0f} / ${s['aww_2016']['ROS']:,.0f} | ${s['aww_2025']['LI']:,.0f} / ${s['aww_2025']['ROS']:,.0f} |")

t3 = ['**Table 3.** Long Island minus rest of state: mean log difference relative to the 2014–2016 same-quarter baseline, in log points (×100; for example, 13.6 log points ≈ 14.5%), by period, and the elasticity of the outcome with respect to the minimum wage. 95% intervals in parentheses from 2,000 random half-splits of the comparison counties (placebo distribution); p = (1 + placebos at least as large in absolute value)/(1 + 2,000). Elasticity: regression of the quarterly Long Island minus rest-of-state log difference on the log minimum-wage gap, 2014Q1–2026Q1 excluding 2020–2021. 2023 narrowing: change in the outcome difference from 2022 to 2023 divided by the change in the log wage gap (−0.073). Jobs = employment; Estab. = establishments; Wage = average weekly wage.', '',
      '| Industry | Outcome | 2014–2015 (lead) | 2017–2019 | 2022 | 2023 | 2024–2026Q1 | Elasticity | p | Elasticity from 2023 narrowing |',
      '|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|']
for ind in ['722', '722511', '722513', '10']:
    for o in ['emp', 'estabs', 'wage']:
        m = E[ind][o]['main']
        t3.append(f"| {SHORT[ind] if o == 'emp' else ''} | {OUTS[o]} | {lp(m['pre_2014_2015'])} | {lp(m['post_2017_2019'])} | {lp(m['y2022'])} | {lp(m['y2023'])} | {lp(m['post_2024_2026'])} | {ci(m['elasticity'])} | {pv(m['elasticity']['p'])} | {ci(m['implied_elasticity_2023'])} |")

R = lambda ind, o, k: E[ind]['robustness'][o].get(k)
rows = [('Main specification', lambda ind, o: E[ind][o]['main']['elasticity']),
        ('Single-county placebos (conservative)', lambda ind, o: E[ind][o]['main']['elasticity_single_county_placebo']),
        ('Pre-COVID quarters only (2014–2019)', lambda ind, o: R(ind, o, 'pre_covid_only')),
        ('Step dummy from 2017Q1', lambda ind, o: R(ind, o, 'step_2017')),
        ('Linear time trend', lambda ind, o: R(ind, o, 'trend')),
        ('Baseline 2016 only', lambda ind, o: R(ind, o, 'baseline_2016_only')),
        ('Westchester added to treated region', lambda ind, o: R(ind, o, 'with_westchester')),
        ('Comparison counties with ≥1,000 jobs in 2016', lambda ind, o: R(ind, o, 'donors_ge1000')),
        ('Industry-specific gap (tipped cash wage; effective fast-food rate)', lambda ind, o: R(ind, o, 'tipped_cash_wage_gap') or R(ind, o, 'fast_food_effective_gap')),
        ('Employment relative to total private employment', lambda ind, o: R(ind, o, 'relative_to_total_private')),
        ('Comparison counties with wage outliers dropped', lambda ind, o: R(ind, o, 'drop_wage_outlier_donors')),
        ('Synthetic control (in-space placebos)', lambda ind, o: SC[ind][o]['elasticity'] if o in SC[ind] else None)]
t4 = ['**Table 4.** Robustness of the minimum-wage elasticities for employment and average weekly wages. Estimate (95% placebo interval). Last rows: county panels with county-by-season and quarter fixed effects, log minimum wage as regressor, standard errors clustered by county (normal-approximation intervals; these understate uncertainty because the wage varies only by region). — not applicable.', '',
      '| Specification | 722 employment | 722511 employment | 722513 employment | 722 wage | 722511 wage | 722513 wage |', '|:--|--:|--:|--:|--:|--:|--:|']
for lab, f in rows:
    cells = []
    for o in ['emp', 'wage']:
        for ind in ['722', '722511', '722513']:
            m = f(ind, o)
            if lab.startswith('Industry-specific') and ind == '722':
                m = None
            cells.append(ci(m) if m else '—')
    t4.append(f'| {lab} | ' + ' | '.join(cells) + ' |')
for lab, k in [('County panel, Long Island and rest of state', 'ny_li_ros'), ('County panel, New York (ex. NYC, Westchester) and Pennsylvania', 'ny_pa'),
               ('… weighted by 2016 employment', 'ny_pa_weighted'), ('… 2014–2019 only', 'ny_pa_pre_covid')]:
    cells = [f"{f2(PN[ind][k]['b'])} ({f2(PN[ind][k]['lo'])} to {f2(PN[ind][k]['hi'])})" for ind in ['722', '722511', '722513']]
    t4.append(f'| {lab} | ' + ' | '.join(cells) + ' | — | — | — |')

tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n\n' + '\n'.join(t4) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
