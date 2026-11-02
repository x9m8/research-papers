"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import os, pandas as pd
from common import RES, ROOT, load
R = load('reproduction.json'); B = load('robustness.json'); U = load('update.json'); I = load('inputs.json')
d, n = R['main']['hall_digitized']['headline'], R['main']['nchs']['headline']; mc = R['monte_carlo']['nchs']
us = R['usda']; ms = R['msw']['2003']
f0 = lambda v: f'{v:,.0f}'; f1 = lambda v: f'{v:,.1f}'
ci = lambda k, f=f0: f"{f(mc[k][0])} to {f(mc[k][2])}"
t1 = ['**Table 1.** Published statements and reproduced values. "Digitized weights" uses mean adult body weights read from the original Figure 1A; "NCHS weights" uses published NCHS means for NHANES I–III (Ogden et al., 2004) and NHANES microdata from 1999–2000 (adults 20–74, pregnant women excluded, women weighted 0.525). Both use the current FAOSTAT old-methodology food balance sheets (FBSH) and the original nominal parameters. Intervals: 2.5th–97.5th percentiles of 100,000 Monte Carlo draws over the original Table 1 parameter distributions (NCHS weights; draws with C ≤ 0 or β ≥ 0.95 redrawn); they reflect parameter uncertainty only. Original values are from the text of Hall et al. (2009) or, where marked, digitized from its Figure 1.', '',
      '| Quantity | Original | Reproduced, digitized weights | Reproduced, NCHS weights | 95% interval |', '|:--|:--|--:|--:|--:|',
      f"| Coefficient on dBW/dt (kcal/kg) | 9,100 | {f0(I['coefficients']['C_dyn_nominal'])} | same | {ci('C_dyn')} |",
      f"| Coefficient on BW − BW0 (kcal/kg/d) | 22 | {I['coefficients']['C_static_nominal']:.1f} | same | {ci('C_static', f1)} |",
      f"| Initial mean fat mass F0 (kg) | 19.1 | — | {I['F0']['nhanes1_calibrated']:.1f} (approximated from NHANES I means) | — |",
      f"| Baseline intake I0, 1974 (kcal/d) | 2,100 (IOM equations, sedentary) | — | {f0(I['I0_iom']['sedentary|age+0'])} (IOM, sedentary; {f0(I['I0_iom']['sedentary|age+3'])}–{f0(I['I0_iom']['sedentary|age-3'])} for mean age ±3 y) | — |",
      f"| Change in mean adult weight, 1974–2003 (kg) | ~10 | {d['dBW']:.1f} | {n['dBW']:.1f} | — |",
      f"| Rate of weight change (kg/d) | ~9.5 × 10⁻⁴ | {d['mean_slope_kg_per_day']*1e4:.1f} × 10⁻⁴ (mean) | {n['mean_slope_kg_per_day']*1e4:.1f} × 10⁻⁴ (mean) | — |",
      f"| First term of eq. 14 in 2003 (kcal/d) | <10 | {d['dyn_term_2003']:.1f} | {n['dyn_term_2003']:.1f} | — |",
      f"| Second term of eq. 14 in 2003 (kcal/d) | ~220 | {d['static_term_2003']:.0f} | {n['static_term_2003']:.0f} | — |",
      f"| Model intake 2003 (kcal/d) | ~2,300 (Fig. 1B, digitized 2,302) | {f0(d['I_2003'])} | {f0(n['I_2003'])} | {ci('I_2003')} |",
      f"| Food waste 1974 (kcal/person/d) | ~900 (Fig. 1C, digitized 911) | {f0(d['waste_1974'])} | {f0(n['waste_1974'])} | {ci('waste_1974')} |",
      f"| Food waste 2003 (kcal/person/d) | ~1,400; more than 1,400 in the abstract (Fig. 1C, digitized 1,455) | {f0(d['waste_2003'])} | {f0(n['waste_2003'])} | {ci('waste_2003')} |",
      f"| Increase in waste per person, 1974–2003 | ~50% | {d['waste_increase_pct']:.0f}% | {n['waste_increase_pct']:.0f}% | {ci('waste_increase_pct')}% |",
      f"| Share of supply wasted, 1974 → 2003 | about 30% → almost 40% | {d['frac_1974']:.1f}% → {d['frac_2003']:.1f}% | {n['frac_1974']:.1f}% → {n['frac_2003']:.1f}% | {ci('frac_1974', f1)}% → {ci('frac_2003', f1)}% |",
      f"| Total waste, 2003 (trillion kcal/yr) | ~150 | {d['total_waste_trillion_kcal_per_yr']:.0f} | {n['total_waste_trillion_kcal_per_yr']:.0f} | — |",
      f"| Oil embodied (million barrels/yr; 3 kcal fossil per kcal food) | ~300 | {d['oil_million_bbl']:.0f} | {n['oil_million_bbl']:.0f} | — |",
      f"| Share of US oil consumption, 2003 | ~4% | {d['oil_share_pct']:.1f}% | {n['oil_share_pct']:.1f}% | — |",
      f"| Share of freshwater use (70% × wasted share) | more than one quarter | {d['freshwater_share_pct']:.0f}% | {n['freshwater_share_pct']:.0f}% | — |",
      f"| USDA-implied waste (FAO supply − USDA loss-adjusted availability) vs model, 1974 | within 5% | {us['1974']['usda_vs_model_dig_pct']:+.0f}% | {us['1974']['usda_vs_model_nchs_pct']:+.0f}% | — |",
      f"| USDA-implied waste vs model, 2003 | ~25% too low | {us['2003']['usda_vs_model_dig_pct']:+.0f}% | {us['2003']['usda_vs_model_nchs_pct']:+.0f}% | — |",
      f"| Municipal solid food waste as share of wasted energy, 2003 (1.9 kcal/g; EPA 2003 value interpolated) | ~30% (EPA 2007 source) | — | {ms['share_of_model_waste_nchs_pct']:.0f}% | — |"]

G = pd.DataFrame(B['grid'])
t2 = ['**Table 2.** Robustness of the 1974–2003 result. Each row changes one input or assumption relative to the baseline (NCHS weights, current FAOSTAT FBSH, nominal parameters), except the last, which combines two. Intake is the modelled mean intake; waste is FAO supply minus intake.', '',
      '| Variant | Intake 2003 (kcal/d) | Waste 1974 (kcal/d) | Waste 2003 (kcal/d) | Increase in waste | Wasted share 1974 | Wasted share 2003 | Change (pp) |', '|:--|--:|--:|--:|--:|--:|--:|--:|']
for _, r in G.iterrows():
    t2.append(f"| {r.label} | {r.I_2003:,.0f} | {r.waste_1974:,.0f} | {r.waste_2003:,.0f} | {r.increase_pct:.0f}% | {r.frac_1974:.1f}% | {r.frac_2003:.1f}% | {r.change_pp:+.1f} |")

S = U['summary']; m1 = U['monte_carlo']['spliced']; m2 = U['monte_carlo']['fbs_from_2010']
t3 = ['**Table 3.** Update to 2023. Model intake from NCHS adult body weights through NHANES 2021–2023 (body weight after mid-2022 extrapolated half a year). FAO supply: "spliced" uses the old-methodology series to 2013 and the new-methodology series from 2014, lowered by the 2010–2013 mean difference between the two (' + f"{I['fao_overlap_2010_2013']['mean']:.1f}" + ' kcal); "unspliced" switches to the new series in 2010. Slopes are least-squares trends in the wasted share. Intervals: Monte Carlo over the original parameter distributions; parameter uncertainty only (they omit sampling error in mean weights, the splice offset and the half-year extrapolation; see §3.3).', '',
      '| Year or statistic | Intake (kcal/d) | Supply, spliced | Waste, spliced | Wasted share, spliced | Supply, unspliced | Wasted share, unspliced |', '|:--|--:|--:|--:|--:|--:|--:|']
a, b = S['nchs|spliced'], S['nchs|fbs_from_2010']
for y in (1974, 2003, 2005, 2010, 2013, 2019, 2023):
    t3.append(f"| {y} | {a[f'I_{y}']:,.0f} | {a[f'FA_{y}']:,.0f} | {a[f'waste_{y}']:,.0f} | {a[f'frac_{y}']:.1f}% | {b[f'FA_{y}']:,.0f} | {b[f'frac_{y}']:.1f}% |")
t3.append(f"| Trend in wasted share, 1974–2003 (pp/yr) | | | | {a['frac_slope_1974_2003_pp_per_yr']:+.2f} | | {b['frac_slope_1974_2003_pp_per_yr']:+.2f} |")
t3.append(f"| Trend in wasted share, 2003–2023 (pp/yr) | | | | {a['frac_slope_2003_2023_pp_per_yr']:+.2f} | | {b['frac_slope_2003_2023_pp_per_yr']:+.2f} |")
se = U['sensitivity_2003_2023']
t3.append(f"| Lowest share after 2003 (spliced) | | | | {se['frac_min_after_2003']:.1f}% ({se['frac_min_year']}) | | |")
t3.append(f"| Change in wasted share 2003→2022, pp (end-year sensitivity) | | | | {se['change_2003_2022_pp']:+.2f} | | |")
fmt = lambda v: f"{v[1]:+.1f} ({v[0]:+.1f} to {v[2]:+.1f})"
t3.append(f"| Change in wasted share 2003→2023, pp (95% parameter-uncertainty interval) | | | | {fmt(m1['frac_change_2003_2023_pp'])} | | {fmt(m2['frac_change_2003_2023_pp'])} |")
t3.append(f"| Change in waste 2003→2023, kcal/d (95% parameter-uncertainty interval) | | | {m1['waste_change_2003_2023'][1]:+.0f} ({m1['waste_change_2003_2023'][0]:+.0f} to {m1['waste_change_2003_2023'][2]:+.0f}) | | | |")
SR = pd.DataFrame(U['self_report'])
t3b = ['', '**Table 3 (continued).** Self-reported energy intake (first-day 24-hour recall, adults 20–74, reliable recalls, women weighted 0.525) against the modelled intake at the same dates.', '',
       '| NHANES cycle | Men (kcal/d) | Women (kcal/d) | Pooled | Model intake | Reported / model |', '|:--|--:|--:|--:|--:|--:|']
for _, r in SR.iterrows():
    t3b.append(f"| {r.cycle} | {r.men:,.0f} | {r.women:,.0f} | {r['pooled_pw0.525']:,.0f} | {r.model_I:,.0f} | {r.ratio_selfreport_to_model:.2f} |")
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n' + '\n'.join(t3b) + '\n'
import re
tables = re.sub(r'(?<![\w/])-(?=\d)', '−', tables)
open(f'{RES}/tables.md', 'w').write(tables)
ms_ = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms_):
    s = open(ms_).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms_, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
