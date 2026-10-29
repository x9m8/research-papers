"""Tables -> results/tables.md and the '## Tables' section of manuscript/manuscript.md (overwrites that section)."""
import os, numpy as np, pandas as pd
from common import RES, ROOT, TARGET, load
R = load('reproduction.json'); B = load('robustness.json'); U = load('update.json')
f2 = lambda v: f'{v:.2f}'; f3 = lambda v: f'{v:.3f}'
def ar(a):
    if a['type'] == 'bounded interval': return f"[{a['lo']:.2f}, {a['hi']:.2f}]"
    if a['type'].startswith('union'): return f"(−∞, {a['pieces'][0][1]:.2f}] ∪ [{a['pieces'][1][0]:.2f}, ∞)"
    return a['type']
lab = {'trad': 'Traditional', 'e1': 'Expanded #1 (supercenters unhealthy)', 'e2': 'Expanded #2 (supercenters healthy)'}

t1 = ['**Table 1.** Published and reproduced estimates of the food-swamp coefficient (percentage points of adult obesity per one-unit change in the RFEI ratio). Reproduction: 2007 store counts, 2009 obesity, contiguous US counties, controls for % low income and low access, recreation and fitness facilities, natural amenities, milk:soda price ratio, % bachelor\'s degree, % Black, % Hispanic, poverty rate and land area; standard errors clustered by state. Instrument: published, ESRI StreetMap highway exits; reproduced, OpenStreetMap motorway junctions (2026). Published labels "Modified v1/v2" are placed against the Table 1 definitions; see §3.2 for the label ambiguity.', '',
      '| RFEI | Published OLS (SE) | Reproduced OLS (SE) | N pub. / rep. | R² pub. / rep. | Published IV (SE) | Reproduced IV (SE) | First-stage F pub. / rep. | Reproduced AR 95% set |', '|:--|--:|--:|--:|--:|--:|--:|--:|--:|']
for k in ('trad', 'e1', 'e2'):
    p, m = TARGET['ols'][k], R['main'][k]; pi = TARGET['iv'][k]
    t1.append(f"| {lab[k]} | {p[0]:.3f} ({p[1]:.4f}) | {m['ols_b']:.3f} ({m['ols_se_cl']:.4f}) | {p[2]:,} / {m['ols_n']:,} | {p[3]:.3f} / {m['ols_r2']:.3f} | {pi[0]:.3f} ({pi[1]:.3f}) | {m['iv_b']:.3f} ({m['iv_se_cl']:.3f}) | {TARGET['fs_F'][k]:.2f} / {m['fs_F_cl']:.1f} | {ar(m['ar_cl'])} |")
a = R['main_alt']['alt']
t1.append(f"| (CONVS + GROC)/GROC, see §3.2 | — | {a['ols_b']:.3f} ({a['ols_se_cl']:.4f}) | — / {a['ols_n']:,} | — / {a['ols_r2']:.3f} | — | {a['iv_b']:.3f} ({a['iv_se_cl']:.3f}) | — / {a['fs_F_cl']:.1f} | {ar(a['ar_cl'])} |")

G = pd.DataFrame(B['grid'])
order = ['Baseline (2007 counts, matched controls, clustered SE)', '2009 store counts', 'State fixed effects', 'Add people over 65 (count, as in the table notes)', 'Add population (linear)',
         'Add population (linear) + state fixed effects', 'Add log population', 'Add log and linear population', 'Add log population + state fixed effects',
         'Population-weighted', 'Zero denominators kept: (num+1)/(den+1)', 'Drop counties with denominator < 3', 'Drop top 1% of RFEI', 'Log of (num+1)/(den+1)',
         'Instrument: any exit (0/1)', 'Instrument: log(1 + exits)', 'Instrument: exits per 1,000 sq mi', 'Instrument: distinct exit refs', 'Counties with at least one exit']
t2 = ['**Table 2.** Sensitivity of the traditional-RFEI estimates. OLS and 2SLS coefficients (state-clustered SE), first-stage F on the excluded instrument (state-clustered; with one instrument this equals the Montiel Olea–Pflueger effective F) and Anderson–Rubin 95% confidence sets. The log specification is in log units and not comparable in size with the others.', '',
      '| Specification | N | OLS (SE) | 2SLS (SE) | First-stage F | AR 95% set |', '|:--|--:|--:|--:|--:|--:|']
for o in order:
    r = G[(G.label == o) & (G.group == 'trad')].iloc[0]
    a_ = {'type': r.ar_type, 'lo': r.ar_lo, 'hi': r.ar_hi}
    if r.ar_type.startswith('union'):
        aset = 'unbounded (two rays)'
    else:
        aset = f'[{r.ar_lo:.2f}, {r.ar_hi:.2f}]'
    t2.append(f"| {o} | {int(r.n):,} | {r.ols_b:.3f} ({r.ols_se:.3f}) | {r.iv_b:.2f} ({r.iv_se:.2f}) | {r.fs_F:.2f} | {aset} |")

cs = U['cross_section_2016']; ld = U['long_difference']
t3 = ['**Table 3.** Update with newer data. Cross-section: 2016 store counts (Food Environment Atlas, July 2025 release; −9999 codes treated as zero) and model-based adult obesity for 2018 (CDC PLACES, 2020 release), contiguous US counties, controls updated where available (food desert 2015, recreation facilities 2016, % Black, % Hispanic and people over 65 2020, poverty 2021, education ACS 2014–2018), OSM instrument. "No −9999" restricts to the 1,500 counties without any −9999-coded count. Long difference: change in obesity 2009→2018 regressed on change in the RFEI 2007→2016, with 2010 baseline controls and state fixed effects. State-clustered SE.', '',
      '| RFEI | Cross-section OLS (SE) | Cross-section 2SLS (SE) | First-stage F | 2SLS + state FE (SE) | First-stage F, FE | 2SLS, no −9999 (SE) | First-stage F, no −9999 | Long difference (SE) | N (long difference) |', '|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|']
for k in ('trad', 'e1', 'e2'):
    a0, a1, a2, l = cs[f'{k}|all'], cs[f'{k}|state FE'], cs[f'{k}|no -9999 counts'], ld[f'{k}|state FE']
    t3.append(f"| {lab[k]} | {a0['ols_b']:.3f} ({a0['ols_se']:.3f}) | {a0['iv_b']:.2f} ({a0['iv_se']:.2f}) | {a0['fs_F']:.1f} | {a1['iv_b']:.2f} ({a1['iv_se']:.2f}) | {a1['fs_F']:.1f} | {a2['iv_b']:.2f} ({a2['iv_se']:.2f}) | {a2['fs_F']:.1f} | {l['b']:.3f} ({l['se']:.3f}) | {l['n']:,} |")

T = R['table3']; c4 = R['table4_cutoffs']
t4 = ['**Table 4.** Points where the published description and the public data diverge, with the evidence from this reproduction.', '',
      '| Item | Published | What the data show |', '|:--|:--|:--|',
      f"| Year of store counts | \"2009 data\" (§2.1) | Table 3 medians (SD) match the 2007 counts in the February 2014 release to within 0.05: fast food {T['ffr']['median']:.0f} ({T['ffr']['sd']:.2f}; Table 3's row \"Number of fast food retailers\" gives 228.58 exactly), grocery {T['groc']['median']:.0f} ({T['groc']['sd']:.2f}), specialised {T['specs']['median']:.0f} ({T['specs']['sd']:.2f}), recreation {T['recfac']['median']:.0f} ({T['recfac']['sd']:.2f}); the analytic Ns 3,055 and 3,069 arise with 2007 counts ({R['ns']['rfei_trad']:,}, {R['ns']['rfei_e1']:,}) but not 2009 counts ({R['ns']['rfei_trad_09']:,}, {R['ns']['rfei_e1_09']:,}); the August 2015 release's 2007 convenience-store counts differ (median 20, SD 255.72) |",
      f"| Traditional RFEI | (FFR + CONVS)/GROC (Table 1) | That ratio has median {T['rfei_trad']['median']:.2f}, SD {T['rfei_trad']['sd']:.2f}; the published 3.5 (1.86) and Table 4 mean 3.89 are matched by (CONVS + GROC)/GROC, the closest of 1,372 constructions searched: median {T['rfei_alt']['median']:.2f}, SD {T['rfei_alt']['sd']:.2f}, mean {c4['rfei_alt']['mean_contig']:.2f} (contiguous counties). The Table 4 count above 3.89 (1,419) is not reproduced ({c4['rfei_alt']['n_above_pub_cut']:,}) |",
      "| Supercenter placement | Table 1, §2.2.2 and Table 4: #1 numerator, #2 denominator; Table 3 note and §2.4.1: the reverse; §3.3 calls #1 \"supercenters categorized as healthy\" | Reproduced OLS for the Table 1 #2 definition is closest to the published v1 coefficient, and vice versa; the published expanded-index medians, SDs and Table 4 counts are not reproduced exactly by either definition |",
      f"| Control set, Tables 6–8 | Notes list % Black, % Hispanic, people over 65, poverty, county size | The note set gives R² {R['note_controls']['trad']['ols_r2']:.3f}; replacing people over 65 with % bachelor's (as in Tables 9 and A4) gives R² {R['main']['trad']['ols_r2']:.3f} (published 0.560) and matches the published control coefficients |",
      "| Standard errors (clarification, not a discrepancy) | Table notes: \"robust\"; §3.3: \"robust standard errors clustered by state\" | Consistent: published SEs for the controls match state-clustered SEs (e.g. natural amenities 0.196 vs 0.198 reproduced) |",
      f"| Food-desert spread | Table 3: 6.2 (8.37) | 8.37 is the mean ({T['lila']['mean']:.2f}); the SD is {T['lila']['sd']:.2f} |",
      f"| Milk:soda price ratio | Table 3: 30.2 (62.10) | The Atlas ratio has median {T['milksoda']['median']:.3f} and SD {T['milksoda']['sd']:.3f} |",
      f"| Abstract vs Table 9 | Abstract: effect \"stronger in counties with greater income inequality (p < 0.05)\" and where residents are less mobile \"(p < 0.01)\" | Table 9 gives 2.737 for Gini < 0.41 and 1.564 for Gini > 0.41 (larger where inequality is lower), and the original's §3.4 text agrees with Table 9; the low-mobility estimate is marked p < 0.05. With the ACS 2006–2010 Gini, {R['strat']['gini<0.41|rfei_trad']['n']:,} of {R['main']['trad']['iv_n']:,} counties are below 0.41; a split with 2,442 below would need a cut-off near {R['strat_gini_cut_for_2442']:.2f} |"]
tables = '\n'.join(t1) + '\n\n' + '\n'.join(t2) + '\n\n' + '\n'.join(t3) + '\n\n' + '\n'.join(t4) + '\n'
open(f'{RES}/tables.md', 'w').write(tables)
ms = os.path.join(ROOT, 'manuscript', 'manuscript.md')
if os.path.exists(ms):
    s = open(ms).read(); i = s.index('## Tables'); j = s.index('## Figures'); open(ms, 'w').write(s[:i] + '## Tables\n\n' + tables + '\n' + s[j:])
print(tables)
