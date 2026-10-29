# Paper 11: independent audit of numbers and methods

Paper: *Drive-thru dose–response: GLP-1 uptake and US restaurant employment*
Package audited: /home/claude/p11/pkg. Audited 22 October 2026. No package file was edited.

## 0. Bottom line

- **Numbers.** I checked every number in the abstract, text, tables, captions, figures and graphical abstract against results/*.json. All of them match after rounding, with one display issue (A1). I found no transcription errors.
- **Reproduction.** Re-running bounds.py, figures.py, tables.py and graphical_abstract.py on a scratch copy gave byte-identical output for:
  - bounds.json and tables.md;
  - manuscript.md (tables.py rewrites its Tables section);
  - all four PNGs.
  
  The three PDFs differ only in the `/CreationDate` string. Once that string is removed they are byte-identical, and the file sizes are the same. The SHA-256 values of the result JSONs and code files match provenance.md.
- **Code against Methods.** The code does what the Methods describe, with four omissions or loose wordings (M1–M4). None of them changes a number.
- **Interpretation.** The text describes the pharmacy event study the wrong way round (B1). This also undermines the explanation offered in §4.1. A few other statements overreach (B2–B6).

## 1. Code checked against Methods

| Item | Code | Verdict |
|---|---|---|
| GLP-1 rows | 10 generic names, filtered by `Gnrc_Name` (fetch_browser.js / fetch_data.py) | OK |
| ZIP via NPI | `Prscrbr_Zip5` taken from the same-year by-Provider file, mapped on `Prscrbr_NPI` | OK |
| ZIP→county | 2020 ZCTA–county file. Kept the county with the largest `AREALAND_PART`, using sort + drop_duplicates (33,791 ZCTAs) | OK |
| Denominator | `PRSCRPTN_DRUG_TOT_BENES`, Monthly Enrollment, `BENE_GEO_LVL=County`, `MONTH=Year`, same year | OK |
| E | 100 × fills / 12 / Part D enrollees. Main exposure is ΔE 2019–2024, winsorised at p1/p99 within the analysis sample | OK |
| Alternative exposures | Semaglutide+tirzepatide uptake; 1000 × GLP-1 claims / all Part D claims by prescriber county | OK. Both are also winsorised, which Methods does not say (M1) |
| QCEW | County rows, `own_code==5`, `area_fips` with 5 digits and not ending 000. Cells with `disclosure_code=='N'` are set to NaN. Pharmacies use 446110 for ≤2021 and 456110 for ≥2022. Rows ending 999 are dropped, as are AK and CT | OK |
| Main sample | partd_2019 ≥ 1000, E is non-missing in both 2019 and 2024, and LSR and FSR have emp/est/wages > 0 in all 11 years | OK (3,046 → 2,703 → 1,275) |
| Comparison-industry samples | The long-difference (LD) model needs the industry disclosed only in 2015, 2019 and 2025 (and 2024 for the to-2024 spec). The event study (ES) needs every year | Partly matches. §2.2 says "where it was disclosed", which is fine. The Fig 2 caption correctly says "every year". This explains why the n values differ: pharmacies 985 (LD) vs 956 (ES); accommodation 1,169 vs 1,118; grocery 630 vs 574 |
| LD specification | Δlog y 2019–2025 regressed on dEw. Controls: own pre-trend 2015–19, log total private employment 2019, Δlog total private employment 2015–19, log Part D 2019, E_2019. State FE | OK |
| Clustering and inference | CR1 clustered by state, t with G−1 df. The small-sample factor excludes the absorbed FE, which is valid because the FE are nested in the clusters | OK. G = 48, or 47 for accommodation and grocery ("most outcomes" is correct) |
| Weighting | Weights are the industry's own 2019 level (for employment, own-industry employment). For the contrast, the weight is LSR + FSR | Matches Table 3. Methods never describes the weighted spec, and the abstract calls it "county size" (M2) |
| Event study | Year-by-year regressions of log(emp_t / emp_2019) on dEw plus 3 baseline controls, with state FE. The joint pre-trend test stacks 2015–18 with state×year FE and year-specific controls, clustered by state, Wald F(4, G−1) | OK |
| MDE | (t_.975 + t_.80) × SE, df = G−1 | OK |
| Multiplicity | Not computed in code. Text says the LSR-wage CI (p = 0.037) would not survive correction | Claim is correct: Bonferroni/Holm threshold for 12 tests is 0.0042. Suggest stating the threshold (M3) |
| Benchmark | −0.08 × m for m = 1, 2, 4. Ratios in bounds.py are lo/bench and MDE/|bench| | OK |
| State secondary | Δlog(1 + spend_acf), 2022 vs 2025 means (12 months required). Regressed on ΔE 2022–24 + E_2022, n = 51 | Mostly OK. "Heteroskedasticity-robust" is implemented as CR1 with one cluster per state, factor (51/50)(50/49) = 1.041 against HC1's 51/48 = 1.063, and df = 50. The difference is negligible but should be described accurately (M4) |
| Coverage checks | npi/national fills; share matched; correlation of state sums with the CMS state file | OK. build.json also has `state_ratio_median`, 0.70 (2019) to 0.87 (2024), which the text does not report (B5) |

## 2. Every number checked against results/*.json

All numbers below are correct. Each row lists the claim with its source value (field) in brackets.

| Location | Claims checked (source value) | Verdict |
|---|---|---|
| Abstract | 8.0% (literature, not checked); 1,275; 1.3→4.6 (1.285→4.639); median 2.9 (2.943); −0.72 (−1.49, 0.05); 0.01 (−1.08, 1.10); gap −0.73 (−1.94, 0.47); weighted 0.02; benchmark −0.08 to −0.32; MDE 3–14× (3.43–13.70, LSR emp) | Correct. Wording issues: B3, B4, M2 |
| §2.1 | 72.9% / 88.5%; 99.0–99.2% (0.98973–0.99160); r ≥ 0.998 (0.99846) | Correct. "Reproduced closely" overstates: B5 |
| §3.1 | 3,046 / 2,703 / 1,275 / 48; 86.6% (0.8655); 4.2-fold (4.233); 10.3% / 76.1%; means 0.96→4.20; median 2.94, p10–p90 1.54–5.28; SD 1.53 (1.5257); LSR 4.06m→4.16m; FSR 5.05m→4.91m; 2.44% / −1.47% | Correct |
| §3.2 | All Table 2 values quoted; p = 0.066, 0.037, 0.227; per SD −1.10 (−2.28, 0.08); MDE 1.10 / 1.71 / 1.55 | Correct |
| §3.3 | LSR pre-period 0.05–0.30, p = 0.19; 2020 −0.33, 2023 −0.60, 2024 −0.92 (−1.65, −0.20), 2025 −0.92 (−1.75, −0.08); FSR within ±0.6 (max abs 0.56), p = 0.58; contrast p = 0.42; pharmacies p = 0.012, LD −1.04 (−2.44, 0.37); grocery p = 0.068, 0.00 (−1.68, 1.67); accommodation 1.27 (−0.33, 2.88), p = 0.87 | Numbers correct. **The pharmacy pre-trend description is wrong: B1.** "Flat" accommodation pre-trends: B4 |
| §3.4 | 0.02 (−0.62, 0.66); −0.65 (−1.30, −0.00); −0.79 (−1.46, −0.12); −0.76 (−1.64, 0.11); −0.56 (−1.35, 0.22); −0.82 (−1.68, 0.04); −0.71 (−1.66, 0.24); claims-share SD 2.84; −0.15 (−0.49, 0.19); FSR 0.57 (0.07, 1.06); contrast −0.72 (−1.30, −0.14); r = 0.42 (0.415) | Correct. Display issue A1 |
| §3.5 | n = 51; mean 5.3% (5.335); 0.54 (−2.55, 3.64); p = 0.73; MDE 4.4 | Correct |
| §4.1 | −1.49 to 0.05; −1.94 to 0.47; MDE 1.10 = 3.4–13.7× (3.426–13.702); "more negative than about −1.5" = 4.7–18.6× (4.662–18.648); national ΔE 3.4 (3.353); 0.3–1.1% (0.268–1.073) | Correct |
| §4.3 | 72.9 → 88.5%; "more than half" of counties removed by suppression (1,428 / 2,703 = 52.8%) | Correct |
| Table 1 | All rows | Correct (regenerated byte-identically from JSON) |
| Table 2 | All 12 rows × 6 columns | Correct (regenerated byte-identically) |
| Table 3 | All cells, n values, per-SD row, pre-trend p row (0.194, 0.585, 0.421, 0.012, 0.870) | Correct. Display issue A1 |
| Fig 1 | (a) semaglutide 16.6M, tirzepatide 6.09M, dulaglutide 5.75M in 2024; "Other" = remaining generics including exenatide ER. (b) median label 2.9 | Correct. Caption issue A2 |
| Fig 2 | n = 1,275 / 1,275 / 1,275 / 956 / 1,118 / 574; p = 0.19 / 0.58 / 0.42 / 0.01 / 0.87 / 0.07; coefficients and bands match event_study.json | Correct |
| Fig 3 | (a) 12 estimates and CIs; band −0.32 to −0.08. (b) 20 bins, slope −0.732 | Correct |
| Graphical abstract | 1.3→4.6; −0.7% (CI −1.5 to +0.05); 0.0% (−1.1 to +1.1); "about −0.1% to −0.3%" | Correct. Cosmetic: the LSR CI mixes 1 and 2 decimals |

### Display issues

| ID | Location | Claim | Correct value | Verdict | Fix |
|---|---|---|---|---|---|
| A1 | §3.4 text; Table 3, "State FE only", LSR | Text: "(−1.30 to −0.00)". Table: "(−1.30 to 0.00)" | hi = −0.0014, p = 0.0495 | Text and table disagree, and the table looks as if the interval includes zero when it does not | Write "−0.65% (−1.30 to −0.001; p = 0.050)". In tables.py's `f2`, keep the sign for small negative values, or show 3 decimals in this case |
| A2 | Fig 1b caption | "the axis is cut at the 0.5th and 99.5th percentiles" | np.histogram range drops values outside it, so the histogram shows 1,261 of 1,275 counties | Imprecise | "14 counties outside the 0.5th–99.5th percentiles are not shown" |

## 3. Do the conclusions follow?

### B1 (major): the pharmacy pre-trend is described backwards

§3.3 says pharmacy employment showed "declining relative employment before 2019 as well as after". §4.1 says it "fell in high-uptake counties before 2019 as well as after".

The ES coefficients are log(emp_t) − log(emp_2019). The pharmacy values for 2015–18 are −0.25, −0.34, −0.85 and −0.50, all negative. A negative pre-period coefficient means employment in those years was lower than in 2019 in high-uptake counties. So relative pharmacy employment **rose** into 2019 and then fell: −1.08 in 2022 and −1.35 in 2025. That is a hump or reversal, not a continuing decline, and Fig 2 shows it plainly.

This matters for the argument:
- The pre-trend test still rejects (p = 0.012), so "the positive control failed" stands.
- But "these counties share [declining] trends" and the pharmacy-closures conjecture are not supported in the form stated.

Fix: "Relative pharmacy employment rose in high-uptake counties before 2019 and fell after it; the pre-trend test rejected (p = 0.012). This pattern of a rise then a fall suggests county-specific shocks or mean reversion that the controls do not capture." Either remove the pharmacy-closures sentence or reword it as a reversal.

The grocery description ("steady downward relative trend") is correct: coefficients run from +1.92 in 2015 to −0.96 in 2025.

### B2 (moderate): the LSR event study does not show a gap that only opens after 2019

The LSR pre-period coefficients are all positive (0.30 in 2015, 0.05, 0.20, 0.12). That means a mild relative decline in high-uptake counties already from 2015 to 2019, at about −0.075%/pt per year. The post-2019 slope is about −0.15%/pt per year. The LD models control for the outcome's own pre-trend, so the main estimate deals with this. But the narrative claims in §3.3 ("after 2019 the coefficients turned negative") and §4.1 ("the gap opening after 2019") overstate the break.

Fix: "The 2015–18 coefficients were small and positive, consistent with a mild pre-existing relative decline. The decline steepened after 2019."

### B3 (moderate): "rule out" depends on the design being valid

Both the abstract ("The data rule out large effects only") and §4.1 ("can rule out effects more negative than about −1.5%") read the CI as a bound on the true effect. That reading holds only if the design is unbiased, and the paper's own failed positive control and weighting sensitivity call this into question. The bounding statement is the paper's main contribution, so it should carry the qualification.

Fix: "Under the design's assumptions, effects more negative than about −1.5% per point are inconsistent with the data. Given the failed positive control, even this bound should be read cautiously."

Also, "That lies inside every interval" (abstract) is true for Table 2. It is not true for every interval in the paper: the LSR to-2024 CI (−1.46, −0.12) excludes −0.08. The −8% benchmark also applies to limited-service spending, not to full-service employment. Suggest: "That range lies inside the limited-service and contrast intervals."

### B4 (moderate): the robustness picture in the abstract and conclusion is selective

The abstract and conclusion stress the weighting result (0.02). They do not mention that every nominal rejection for limited-service restaurants has the same negative sign:
- LSR wages, p = 0.037;
- outcome measured to 2024, p = 0.022;
- no controls, p = 0.0495;
- ES 2024 and 2025 CIs exclude zero;
- the claims-share exposure gives a significant negative contrast, −0.72 (p = 0.017), with FSR at +0.57 (p = 0.026).

"No clear association" (§5) is defensible. A fair summary would add one clause: "Estimates for limited-service restaurants were consistently negative across most specifications but sensitive to weighting." The abstract should also mention that the alternative prescriber-based exposure yields a significant negative contrast.

Accommodation "flat pre-trends (p = 0.87)" is also an overstatement. The coefficients rise steadily from −0.87 to 0, and the test fails to reject only because the CIs are wide. Say "the pre-trend test did not reject."

### B5 (minor to moderate): exposure validation and measurement error

§2.1 says county sums "reproduced the CMS state totals closely: the correlation was at least 0.998". The correlation is driven by state size. In levels, the median county-sum/CMS-state ratio was only 0.70 in 2019 and 0.87 in 2024 (build.json `state_ratio_median`). Report this.

Because suppression coverage rose over the period, the measured ΔE partly reflects coverage change. That change probably depends on prescriber size, and so on rural versus urban county type. The error is therefore not classical, and could bias the estimate in either direction, not just toward zero. §4.3 ("could add measurement error") should say so.

There is a related scale mismatch:
- The national 1.3→4.6 and the 3.35-point ΔE in the §4.1 national calculation use unsuppressed national fills.
- The county regressors use the suppressed extract: sample mean 0.96→4.20, mean ΔE 3.24.

One sentence noting this would do.

### B6 (minor): the pharmacy positive control was weak by design

GLP-1 fills are a small share of pharmacy volume. The expected effect on pharmacy employment per point is probably far below the pharmacy MDE (2.00). The control could therefore not "pass" on its sign, and only its pre-trend is informative. §2.2 or §4.3 should say this, so that the failure is read as a pre-trend failure (B1), not a sign failure ("opposite sign to the expectation" with p = 0.145 is just noise).

### Weighting sensitivity

It is correctly reported. However, the weights are own-industry 2019 employment, not "county size" (abstract) (see M2). Note also that the weighted estimate (0.02, CI −0.62 to 0.66) still includes the benchmark range, so it does not overturn the bounding conclusion.

### Methods wording

- **M1:** say the alternative exposures were also winsorised at p1/p99.
- **M2:** add one Methods sentence on the weighted specification: weights are 2019 own-industry employment, and LSR + FSR for the contrast. Change "county size" to "2019 employment" in the abstract.
- **M3:** state the Bonferroni/Holm threshold (0.05/12 = 0.0042) next to the multiplicity claim.
- **M4:** §2.6: "heteroskedasticity-robust (HC1-type, t with 50 df)", or leave as is. The numerical difference is negligible.

## 4. Prioritised fixes

1. **B1.** Correct the pharmacy pre-trend direction in §3.3 and §4.1, and revise or drop the pharmacy-closures conjecture.
2. **B3.** Make the "rule out" statements (abstract, §4.1) conditional on design validity. Narrow "inside every interval" to the LSR and contrast intervals.
3. **B4.** In the abstract and conclusion, add that LSR estimates were consistently negative, and that the prescriber-based exposure gave a significant negative contrast (−0.72, p = 0.017). Change "flat" accommodation pre-trends to "test did not reject".
4. **B2.** Soften "gap opening after 2019" and mention the small positive LSR pre-period coefficients.
5. **B5.** Report the 0.70–0.87 level ratio alongside r ≥ 0.998. Describe the coverage-driven error as possibly non-classical. Note the scale difference between suppressed and national measures.
6. **A1.** Fix the "−0.00" / "0.00" display and add p = 0.050 (tables.py `f2`).
7. **M2, M1, M3, M4.** Methods wording; "county size" → "2019 employment".
8. **B6, A2.** Note the weak power of the positive control. Correct the Fig 1b caption (14 counties not shown).

## 5. Reproduction log

- Scratch copy: /tmp/claude-0/-home-claude/e77537ee-4bde-5960-ac22-2794b7601af1/scratchpad/p11audit. Outputs were deleted before re-running.
- Environment: Python 3.13.16, pandas 3.0.5, NumPy 2.5.3, matplotlib 3.11.2.
- Scripts run: bounds.py, figures.py, tables.py, graphical_abstract.py.
- Byte-identical: bounds.json, tables.md, manuscript.md, fig1/fig2/fig3/graphical_abstract PNGs.
- PDFs: identical after removing `/CreationDate`.
- build_panel.py, analysis.py and state_secondary.py could not be re-run because the raw data are not available locally. They were checked by reading the code only.
