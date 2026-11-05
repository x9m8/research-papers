# Number audit: Paper 20, "Regional minimum wages and restaurant employment on Long Island, New York"

Independent auditor (did not write the paper). Date: 29 October 2026.
Scope: minimum-wage schedule, independent re-fetch of the QCEW data and re-run of the shipped analysis code, every number in `manuscript/manuscript.md` (abstract, social summary, text, Tables 1–4, captions, Figures 1–3, graphical abstract), and methods.

## Verdict

**The numbers are correct and reproducible. Revise before publishing: two methods/interpretation issues need fixing, plus a few small wording fixes.**

- Re-fetching the QCEW data on 29 Oct 2026 in my own Chrome tab and rerunning the shipped code in Pyodide produced a `panel.csv` **byte-identical** to the builder's (SHA-256 b8406f75…). It also produced byte-identical `estimates.json`, `event_study.json`, `scm.json`, `panel.json`, `descriptives.json` and `break.json`. `build.json` differs only in `n_raw_rows`, because my extract left out the unused NJ and 7224/7225 rows. All balanced-county counts and 2016 employment levels match.
- `summary.py` and `tables.py`, rerun locally on the shipped JSONs, reproduce `summary.json`, `tables.md` and the manuscript's Tables section exactly.
- I checked every number in the text against the result files. None is wrong beyond rounding.
- I checked the minimum-wage schedule (all 56 rows) against NYSDOL sources. Every date and rate matches.
- Methods: the synthetic-control "ranked 4th of 49" is an artefact of a degenerate pre-period fit. The wage conclusion is applied asymmetrically: it ignores the trend-adjusted wage results and an undisclosed significant full-service wage pre-trend. Neither issue changes the main employment conclusion, but both need fixing in the text.

## 1. Minimum-wage schedule (`data/raw/minwage_schedule.csv`)

Sources read on 29 Oct 2026: dol.ny.gov/history-minimum-wage-new-york-state; forms.labor.ny.gov/WP/CR146.pdf (§146-1.2, §146-1.3(b)); forms.labor.ny.gov/WP/Part146.pdf (rev. 02/26); dol.ny.gov/minimum-wage.

| Series | Result |
|---|---|
| Statewide 8.00 / 8.75 / 9.00 (31 Dec 2013/14/15) | Matches |
| LI & Westchester 10.00…15.00 (31 Dec 2016–2021), 16.00 / 16.50 / 17.00 (1 Jan 2024/25/26) | Matches |
| Rest of state 9.70…14.20 (31 Dec 2016–2022), 15.00 / 15.50 / 16.00 | Matches |
| NYC large 11 / 13 / 15, then 16 / 16.50 / 17 | Matches |
| Fast food outside NYC 10.75 / 11.75 / 12.75 / 13.75 / 14.50, 15.00 (1 Jul 2021), 15.50 (2025), 16.00 (2026); no 2024 increase | Matches. The Part 146 summary shows fast food at LI $16.00 and rest of state $15.00 in 2024, which equals the code's effective (max) rate |
| Tipped food-service cash wage, LI: 7.50, 7.50, 8.00, 8.65, 9.35, 10.00, 10.65, 11.00, 11.35 | Matches CR146 §146-1.3(b)(2) and Part146 summary |
| Tipped cash wage, rest of state: 7.50, 7.50, 7.50, 7.85, 8.35, 8.80, 9.45, 10.00, 10.35, 10.70 | Matches (2025/26 also appear in CR146 itself, not only the summary) |
| PA $7.25 | Not re-fetched; consistent with the federal minimum since 24 Jul 2009 |
| 2027: no increase | dol.ny.gov/minimum-wage: "On January 1, 2027, New York's minimum wage will stay the same" (off-ramp met). Matches §1 |

Quarter coding (31 Dec goes to Q1 of the next year; 1 Jul 2021 goes to Q3) is implemented correctly in `effective_quarter`. The log gaps 0.030 / 0.128 / 0.055 / 0.061–0.065 and Δ = −0.073 are correct. The 31 Dec 2016 increases of 22.2% / 11.1% / 7.8% are correct.

## 2. Re-fetch and re-run

- Data: 196 QCEW industry files (NAICS 10, 722, 722511, 722513 × 2014Q1–2026Q1) fetched with `fetch()` from data.bls.gov in my own tab. 2013 and 2026Q2–Q4 return 404, which confirms the "2014Q1–2026Q1" claim.
- Code: `common.py`, `build_panel.py` and `analysis.py` were written into Pyodide 0.26.4 and checked against the package's SHA-256 hashes (all match), then run unchanged. The analysis ran in 65 s.
- **Result: every analysis JSON reproduces byte for byte.** That covers all event-study windows, elasticities, placebo intervals, single-county placebos, the 2023 narrowing, robustness rows, the SCM, the county panels, descriptives and the 2017Q1 break percentages.
- Raw-value spot check (8 county-quarter cells, compared against the QCEW *area* API slice, a different extract of the same database). All matched exactly on establishments, the 3 monthly employment levels and total wages: Nassau 722 2016Q1; Suffolk 722511 2025Q4; Erie 722513 2016Q1; Albany 722 2022Q3; Monroe total private 2019Q2; Allegheny PA 722 2018Q4; Suffolk 722 2017Q1; Nassau 722513 2026Q1. I did not read values through the interactive data-viewer screens themselves.
- Incident during re-fetch: one file (2016Q2, NAICS 10) came back with HTTP 200 but no usable rows on the first try. A retry fixed it. The shipped `fetch_browser.js` and `fetch_data.py` do not detect this case. If it had happened to the builder, total-private comparison counties would silently have dropped to 0. See fix L4.

Extra diagnostics I computed in the same run:
- Wage-outlier donors dropped: 722 = Columbia (36031) and Schuyler (36097); 722511 = 36017, 36031, 36043, 36097; 722513 = Erie (36029) and Wyoming (36121).
- Erie 722513 average weekly wage: 2016Q1 $465 against $338–378 in the other 2015–2016 quarters. This confirms the "Erie spike in early 2016" statement.
- SCM (722 employment): Long Island pre-RMSPE = 1.9×10⁻⁷, i.e. a perfect fit. The pre-period matrix has rank 11, and 48 donors can fit it exactly. 7 of the 48 placebo counties also have pre-RMSPE < 10⁻⁶. Ranked by post-period RMSPE alone, Long Island is **18th of 49**, not 4th.

## 3. Discrepancy table

| # | Location | Stated | Correct / issue | Source | Severity | Fix |
|---|---|---|---|---|---|---|
| 1 | §3.3, last sentence of "other checks" paragraph | "Long Island ranked 4th of 49 units on the ratio of post- to pre-period fit" | The number is computed correctly but means nothing. Pre-RMSPE ≈ 0 (1.9e-7) because the outcomes are demeaned on the same 2014–2016 quarters that form the pre-period (8 free values, 48 donors). The ratio is post/≈0, so the rank is set by numerical noise in degenerate placebo fits (7 placebos < 1e-6). Ranked by post-RMSPE alone: 18th of 49 | scm.json `pre_rmspe` 0.0; auditor rerun | **High** (misleading inferential claim) | Delete the rank, or report the post-RMSPE rank (18/49). Better: fit the SCM on undemeaned log levels or add a hold-out pre-period. Say in §2.3 that the pre-period fit is exact by construction |
| 2 | Abstract ("Average weekly restaurant wages rose no faster…"), §3.2 wage paragraph, §4.1 third finding ("no sign in the QCEW wage data…"), §5 | Wage gap read as showing no relative rise | Inconsistent with the paper's own treatment of trends. Employment conclusions favour the trend-adjusted estimate. For wages, the trend-adjusted full-service elasticity is **+0.30 (0.16 to 0.44)** and the step-dummy version is +0.26 (0.10 to 0.42), both positive and excluding zero. The full-service wage series had a significant pre-trend of −0.94 log points a year (**placebo p = 0.0005**, not reported); total private wages had one too (p = 0.005; lead −0.6, −1.1 to −0.1). The "−3.6 in 2024–2026" largely continues that pre-trend | estimates.json robustness.wage.trend/step_2017; event_study.json pretrend_slope_* | **Medium-high** (interpretation) | Report the wage pre-trends in §3.3 next to the employment ones. Soften "no sign" to "no relative rise in levels; trend-adjusted full-service estimates are positive, so the wage evidence is inconclusive". Adjust the abstract and §5 to match |
| 3 | §2.1, para 2 | Fast-food rate "until 2023, above both regions' general minimum" | In 2022 (and 2023) the fast-food rate ($15.00) *equalled* the LI general rate ($15.00); it was above the LI rate only through 2021 | Table 1; NYSDOL | Low | "at or above both regions' general minimum until 2024 (equal to the Long Island rate in 2022–2023)" |
| 4 | Table 1, 2021 fast-food columns | 15.00, labelled "in force for most of each year" | $14.50 Jan–Jun and $15.00 Jul–Dec, i.e. exactly half the year (the table takes the Q4 value) | CR146 §146-1.2 | Low | Footnote: "2021: $14.50 until 30 June, $15.00 from 1 July" |
| 5 | Table 3, total private wage, 2023 | "−3.9 (−7.9 to 0.0)" | Upper bound is −0.02 log points; the interval narrowly excludes zero, but "0.0" reads as including it | estimates.json `10.wage.main.y2023.hi` = −0.0002 | Low | Print "−0.0", or add a note |
| 6 | Table 3 caption | "(×100, approximately per cent)" | At the reported sizes the approximation is loose: 13.6 log points = 14.5%, 16.6 = 18.0% | summary.json `*_windows_pct` | Low | "log points (×100); e.g. 13.6 log points ≈ 14.5%" |
| 7 | §2.4 | "the p-value is the share of placebo estimates at least as large in absolute value" | The code uses (1 + count)/(1 + 2000), so the minimum is 0.0005. That is consistent with "<0.001", but the description is inexact | analysis.py `summarise` | Low | "(1 + number at least as large)/(1 + number of placebos)" |
| 8 | §4.1 | "These intervals sit within the range that most of the literature reports, from roughly zero … to modest negative values" | The intervals reach +0.13 and +0.31, above that range | text vs Table 4 | Low | "These intervals are consistent with the near-zero estimates …; they exclude large negative values" |
| 9 | §3.3 | "dropping two comparison counties with outlying wage movements" | Correct for 722 and 722513 (2 each), but full-service dropped 4, and Table 4 includes the full-service row | estimates.json n_dropped | Low | "dropping two to four comparison counties (four for full-service)" |

Everything else I checked is correct, including:
- Abstract: 4.1 (1.4–6.8), 13.6 (5.1–21.6), 1.03 (0.35–1.66), −0.05 (−0.24–0.13), 0.09 (−0.14–0.31), 8.2% and 3.5%, 42–48 counties, 2,000 splits.
- §1 and §2 rates and gaps; §2.2 county counts; §2.4: 225,439, 92,837, 2.4×, MDE 2.8 SD.
- §3.1: 29.2%, +9.4/−4.6, +2.9/−13.0, $483/$368, $729/$572, +4.0/+1.2.
- §3.2: all window values, the lead bound 0.7, wage windows.
- §3.3: elasticities, MDEs 1.00/0.33/0.26, the 2023 changes and implied elasticities, trend, step, the 0.84–1.44 range, 0.83, 0.70, single-county −0.76 to 2.11, SCM gaps 3.9/12.7 and elasticity 0.90 (−0.48–2.24), outlier-dropped wage values, pre-trend 0.5 lp/yr p = 0.22, full-service establishments p = 0.008.
- Break percentages 12.0/8.2/5.9/3.5/0.2, medians −0.4 to 0.3, employment differences 1.5 and 0.8 points.
- §3.4 panels; §4.1 the 31% premium, the $0.50–$1.20 cash-wage gap and 1.43 (0.72–2.21).
- Tables 2–4 cell by cell, via regeneration.
- Figures 1–3 match the data and captions: Fig 3b points at 8.2/5.9/3.5/12.0/0.2 against 11.1/11.1/7.8/22.2/0.
- Graphical abstract ($0.30→$1.80→$1.00, +13.6, −1.2, −0.05 (−0.24–0.13), 0.09 (−0.14–0.31), "48 upstate counties" for NAICS 722) and the social summary.

## 4. Methods review

- **Random half-split placebo.** Implemented as described (24 vs 24 counties, seed 20261028; the interval is the estimate minus the placebo 97.5/2.5 percentiles). It is valid only if Long Island's region-specific shocks are exchangeable with the difference between two random mixes of upstate counties. Long Island is a contiguous downstate suburban economy, and the random halves average out geographic shocks, so these intervals likely understate uncertainty. The single-county placebo intervals all include zero. The manuscript says the single-county version is "wider than the truth" but does not acknowledge that the half-split may be too narrow. Suggest adding one sentence to §4.3, so that "all intervals exclude zero" is not read as strong evidence (Medium; does not change the null-effect conclusion).
- **Comparison-county selection and suppression.** The code requires disclosure (code ≠ N and emp, estabs, wages > 0) in all 49 quarters, as stated. This conditions on future disclosure, which is mild and disclosed in §4.3. Nassau and Suffolk are disclosed throughout (verified).
- **COVID exclusion.** 2020–2021 are dropped from all regressions and panels, as stated. Windows for 2020–2021 are computed but not reported, which is fine.
- **Trend specification.** A linear trend over the estimation quarters, fitted jointly with the gap; with a rising gap in 2017–2022 the two are partly collinear (MDE 0.33). This is appropriate as a sensitivity check. See issue 2 for the asymmetric use of trends between employment and wages.
- **Synthetic control.** See issue 1. The weights spread over 31 donors with weight > 0.01, which is close to an equal-weight average, so the SCM adds little over the main comparison. The in-space placebo elasticity intervals are fine to report.
- **Clustered SEs in the PA panel.** Clustered by county with a G/(G−1)·(n−1)/(n−k) correction. Treatment varies at the level of 3 regions (LI, rest of state, PA), so the SEs are too small. The text says so (§2.3, §3.4); that is adequate.
- **2017Q1 break.** Reproduced exactly. The step dummy halves the 722 elasticity; that is reported.
- Nothing above overturns the paper's main conclusion (no evidence of LI restaurant job losses; the positive naive elasticity is not causal).

## 5. Process notes

- `data/transfer_media_ids.txt` records an *attempted* upload to the WordPress media library that was blocked. Nothing was uploaded, but Peter may want to know an upload was tried.
- `fetch_browser.js` and `fetch_data.py` should treat a 200 response with zero matching rows as a failure and retry (see §2).

## Not verified

- The Pennsylvania $7.25 history was not re-fetched from dol.gov; I relied on general knowledge.
- I did not check figure-rendering code line by line; I checked figures visually against the result files.
- Literature claims and references were outside scope.
