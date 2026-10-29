**Table 1.** Published and reproduced estimates of the food-swamp coefficient (percentage points of adult obesity per one-unit change in the RFEI ratio). Reproduction: 2007 store counts, 2009 obesity, contiguous US counties, controls for % low income and low access, recreation and fitness facilities, natural amenities, milk:soda price ratio, % bachelor's degree, % Black, % Hispanic, poverty rate and land area; standard errors clustered by state. Instrument: published, ESRI StreetMap highway exits; reproduced, OpenStreetMap motorway junctions (2026). Published labels "Modified v1/v2" are placed against the Table 1 definitions; see §3.2 for the label ambiguity.

| RFEI | Published OLS (SE) | Reproduced OLS (SE) | N pub. / rep. | R² pub. / rep. | Published IV (SE) | Reproduced IV (SE) | First-stage F pub. / rep. | Reproduced AR 95% set |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Traditional | 0.125 (0.0443) | 0.086 (0.0247) | 3,055 / 3,055 | 0.560 / 0.560 | 2.604 (1.076) | 1.023 (0.285) | 15.66 / 30.7 | [0.58, 1.82] |
| Expanded #1 (supercenters unhealthy) | 0.120 (0.0579) | 0.117 (0.0447) | 3,069 / 3,069 | 0.559 / 0.559 | 1.510 (0.434) | 1.544 (0.449) | 7.87 / 27.5 | [0.86, 2.85] |
| Expanded #2 (supercenters healthy) | 0.115 (0.0499) | 0.120 (0.0515) | 3,069 / 3,069 | 0.560 / 0.558 | 1.277 (0.383) | 1.811 (0.491) | 7.44 / 35.0 | [1.03, 3.14] |
| (CONVS + GROC)/GROC, see §3.2 | — | 0.132 (0.0454) | — / 3,055 | — / 0.558 | — | 3.257 (1.539) | — / 6.9 | [1.45, 14.66] |

**Table 2.** Sensitivity of the traditional-RFEI estimates. OLS and 2SLS coefficients (state-clustered SE), first-stage F on the excluded instrument (state-clustered; with one instrument this equals the Montiel Olea–Pflueger effective F) and Anderson–Rubin 95% confidence sets. The log specification is in log units and not comparable in size with the others.

| Specification | N | OLS (SE) | 2SLS (SE) | First-stage F | AR 95% set |
|:--|--:|--:|--:|--:|--:|
| Baseline (2007 counts, matched controls, clustered SE) | 3,055 | 0.086 (0.025) | 1.02 (0.29) | 30.71 | [0.58, 1.82] |
| 2009 store counts | 3,054 | 0.077 (0.025) | 1.01 (0.31) | 21.14 | [0.55, 1.99] |
| State fixed effects | 3,055 | 0.063 (0.017) | 0.77 (0.18) | 41.91 | [0.46, 1.21] |
| Add people over 65 (count, as in the table notes) | 3,054 | 0.085 (0.025) | 0.93 (0.23) | 35.44 | [0.56, 1.54] |
| Add population (linear) | 3,055 | 0.083 (0.025) | 0.73 (0.25) | 19.30 | [0.33, 1.46] |
| Add population (linear) + state fixed effects | 3,055 | 0.062 (0.017) | 0.53 (0.17) | 33.62 | [0.21, 0.92] |
| Add log population | 3,055 | 0.066 (0.024) | 1.76 (0.87) | 4.83 | [0.79, 16.47] |
| Add log and linear population | 3,055 | 0.065 (0.025) | 1.17 (0.61) | 3.98 | [0.43, 57.10] |
| Add log population + state fixed effects | 3,055 | 0.043 (0.018) | 15.58 (92.13) | 0.03 | unbounded (two rays) |
| Population-weighted | 3,054 | 0.228 (0.049) | 1.34 (0.28) | 105.93 | [0.83, 1.95] |
| Zero denominators kept: (num+1)/(den+1) | 3,108 | 0.130 (0.039) | 0.97 (0.26) | 35.18 | [0.55, 1.69] |
| Drop counties with denominator < 3 | 2,492 | 0.137 (0.030) | 1.00 (0.28) | 32.63 | [0.57, 1.77] |
| Drop top 1% of RFEI | 3,024 | 0.104 (0.028) | 1.10 (0.34) | 25.33 | [0.60, 2.11] |
| Log of (num+1)/(den+1) | 3,108 | 0.527 (0.186) | 5.02 (1.17) | 49.08 | [3.03, 7.92] |
| Instrument: any exit (0/1) | 3,055 | 0.086 (0.025) | 0.28 (0.14) | 67.07 | [0.04, 0.60] |
| Instrument: log(1 + exits) | 3,055 | 0.086 (0.025) | 0.34 (0.14) | 44.16 | [0.09, 0.68] |
| Instrument: exits per 1,000 sq mi | 3,055 | 0.086 (0.025) | 1.80 (1.01) | 1.82 | unbounded (two rays) |
| Instrument: distinct exit refs | 3,055 | 0.086 (0.025) | 1.07 (0.43) | 6.87 | [0.51, 4.00] |
| Counties with at least one exit | 1,954 | 0.108 (0.026) | 1.28 (0.40) | 15.15 | [0.72, 2.74] |

**Table 3.** Update with newer data. Cross-section: 2016 store counts (Food Environment Atlas, July 2025 release; −9999 codes treated as zero) and model-based adult obesity for 2018 (CDC PLACES, 2020 release), contiguous US counties, controls updated where available (food desert 2015, recreation facilities 2016, % Black, % Hispanic and people over 65 2020, poverty 2021, education ACS 2014–2018), OSM instrument. "No −9999" restricts to the 1,500 counties without any −9999-coded count. Long difference: change in obesity 2009→2018 regressed on change in the RFEI 2007→2016, with 2010 baseline controls and state fixed effects. State-clustered SE.

| RFEI | Cross-section OLS (SE) | Cross-section 2SLS (SE) | First-stage F | 2SLS + state FE (SE) | First-stage F, FE | 2SLS, no −9999 (SE) | First-stage F, no −9999 | Long difference (SE) | N (long difference) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Traditional | 0.056 (0.030) | 0.87 (0.26) | 21.4 | 0.46 (0.20) | 15.3 | 2.27 (1.12) | 4.1 | -0.010 (0.012) | 3,011 |
| Expanded #1 (supercenters unhealthy) | 0.096 (0.059) | 1.37 (0.43) | 24.8 | 0.76 (0.35) | 11.9 | 2.11 (0.71) | 11.7 | -0.012 (0.015) | 3,034 |
| Expanded #2 (supercenters healthy) | 0.105 (0.075) | 1.70 (0.55) | 27.8 | 0.95 (0.46) | 9.7 | 2.24 (0.68) | 17.0 | 0.002 (0.020) | 3,035 |

**Table 4.** Points where the published description and the public data diverge, with the evidence from this reproduction.

| Item | Published | What the data show |
|:--|:--|:--|
| Year of store counts | "2009 data" (§2.1) | Table 3 medians (SD) match the 2007 counts in the February 2014 release to within 0.05: fast food 15 (228.58; Table 3's row "Number of fast food retailers" gives 228.58 exactly), grocery 6 (76.81), specialised 1 (37.95), recreation 2 (30.31); the analytic Ns 3,055 and 3,069 arise with 2007 counts (3,055, 3,069) but not 2009 counts (3,054, 3,064); the August 2015 release's 2007 convenience-store counts differ (median 20, SD 255.72) |
| Traditional RFEI | (FFR + CONVS)/GROC (Table 1) | That ratio has median 5.33, SD 3.54; the published 3.5 (1.86) and Table 4 mean 3.89 are matched by (CONVS + GROC)/GROC, the closest of 1,372 constructions searched: median 3.50, SD 1.86, mean 3.92 (contiguous counties). The Table 4 count above 3.89 (1,419) is not reproduced (1,244) |
| Supercenter placement | Table 1, §2.2.2 and Table 4: #1 numerator, #2 denominator; Table 3 note and §2.4.1: the reverse; §3.3 calls #1 "supercenters categorized as healthy" | Reproduced OLS for the Table 1 #2 definition is closest to the published v1 coefficient, and vice versa; the published expanded-index medians, SDs and Table 4 counts are not reproduced exactly by either definition |
| Control set, Tables 6–8 | Notes list % Black, % Hispanic, people over 65, poverty, county size | The note set gives R² 0.474; replacing people over 65 with % bachelor's (as in Tables 9 and A4) gives R² 0.560 (published 0.560) and matches the published control coefficients |
| Standard errors (clarification, not a discrepancy) | Table notes: "robust"; §3.3: "robust standard errors clustered by state" | Consistent: published SEs for the controls match state-clustered SEs (e.g. natural amenities 0.196 vs 0.198 reproduced) |
| Food-desert spread | Table 3: 6.2 (8.37) | 8.37 is the mean (8.37); the SD is 8.21 |
| Milk:soda price ratio | Table 3: 30.2 (62.10) | The Atlas ratio has median 0.845 and SD 0.126 |
| Abstract vs Table 9 | Abstract: effect "stronger in counties with greater income inequality (p < 0.05)" and where residents are less mobile "(p < 0.01)" | Table 9 gives 2.737 for Gini < 0.41 and 1.564 for Gini > 0.41 (larger where inequality is lower), and the original's §3.4 text agrees with Table 9; the low-mobility estimate is marked p < 0.05. With the ACS 2006–2010 Gini, 847 of 3,055 counties are below 0.41; a split with 2,442 below would need a cut-off near 0.46 |
