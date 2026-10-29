# Number and methods audit: paper 17, "Food swamps and obesity revisited"

Auditor: independent AI agent (Claude), 22 Oct 2026. No package file was edited. Scratch work: `/tmp/claude-0/-home-claude/e77537ee-4bde-5960-ac22-2794b7601af1/scratchpad/p17audit` (re-run copy), `.../scratchpad/ref` (original outputs), `.../scratchpad/chk` (audit scripts).

Original article: full text read in Chrome from mdpi.com (WebFetch returned the tables only, because the body is rendered by script). Table cells were also checked against `lit/src/mdpi_flat.txt`.

## 1. Reproduction run

- Pipeline 00 → 01 → 02 → 03 → 04 → 06 → 05 → graphical_abstract → tables, run on a clean copy with the original outputs moved aside. Runtime was 25 s and every script exited 0.
- **Byte-identical**: all 8 result files (`*.json`, `robustness.csv`, `tables.md`) and all 3 derived CSVs. `tables.py` rewrote `manuscript.md`, and the result was identical to the shipped manuscript.
- Independent re-estimation with `linearmodels` IV2SLS gives identical point estimates for OLS, 2SLS and R². Clustered SEs differ by about 1% (0.2817 vs 0.2851 for the traditional IV), because linearmodels applies only G/(G−1) while `econ.py` adds (N−1)/(N−K), as Stata `regress` does. HC1 SE for natural amenities is 0.059, so the manuscript's "about three times smaller" is confirmed.
- The AR set code is correct: it inverts a quadratic, uses the same cluster variance as the 2SLS, and has the right influence weights. The (rare) `a2≈0` branch is labelled "unbounded" but is really a half-line. It is never triggered in this package.

## 2. Methods vs code

| Item | Verdict |
|---|---|
| RFEI constructions (01_build `add_rfei`) | Match Table 1 of the original and §2.3 of the manuscript. trad=(FFR+CONVS)/GROC; e1=(FFR+CONVS+SUPERC)/(GROC+FMRKT+SPECS); e2=(FFR+CONVS)/(GROC+FMRKT+SPECS+SUPERC). Zero denominators become NaN. OK |
| Controls | `CTRL` = lila, recfac, natamen, milksoda, %Black, %Hispanic, povrate, sqmi, bach_only. This matches §2.5 and the original's Table 9/A4 covariate list (confirmed). The notes to Tables 6–8 (confirmed verbatim) list fitness centres, natural amenities, %Black, %Hispanic, number of people over 65, poverty rate and county size. OK |
| Control sources/years | Atlas Feb 2014: RECFAC07, NATAMEN, MILK_SODA_PRICE10, PCT_LACCESS_LOWI10, PCT_NHBLACK10, PCT_HISP10, POVRATE10. ACS 2006–10: Gini, commute, education. 2010 boundary file: land area. Consistent with §2.2. The 2016 update mixes years (lila 2015, race 2020, poverty 2021, ACS 2014–18). §2.7 says only "updated where … offered" and should list the years |
| 2007 vs 2009 counts | Code uses 2007 counts from Feb 2014 (main) and 2009 from Nov 2012 (variant). See §3 |
| OLS, state-clustered | 49 clusters (48 states + DC) in the 3,108-county sample. OK |
| 2SLS with OSM junctions | Just-identified, cluster SE. First-stage F = (b/se)² with the cluster variance, which equals the MOP effective F with one instrument. OK |
| Population/state-FE sensitivity | Correct as coded. **But see Methods issue M1**: only *log* population kills the first stage |
| Long difference | Δobesity = PLACES 2018 age-adjusted (18+) minus Atlas/CDC 2009 age-adjusted (20+), on ΔRFEI 2016−2007, with 2010 level controls and state FE. −9999 counts become 0. Implemented as described. Caveats are in M3 |
| Density split | unh = (FFR+CONVS) and hea = GROC per 10k pop10. Supercenters, specialised stores and farmers' markets are excluded, which the text does not say. N = 3,107 |
| Interpretation arithmetic | 0.125 × median(0.01·FFR/GROC = 0.0267) = 0.0033 pp ✓. Elasticity = b·mean(FFR/GROC)/mean(obese) = 0.012 ✓. 2.604 × SD 3.533 = 9.20 ✓. 3/2.604 = 1.152 units; median outlets removed = 6.9 (≈7) ✓; median share of unhealthy outlets 21.5% ✓. **But see M2** |
| "Search over constructions" (§3.2) | **No script in the package.** I re-ran it: all 1,372 combinations of 1–4 numerator outlets (FFR, CONVS, GROC, SUPERC, SPECS, FMRKT, FSR) over 1–3 denominator outlets. (CONVS+GROC)/GROC is the unique close match: median 3.500, SD 1.860, contiguous mean 3.916. The next best has median 3.67. The claim holds, but the search script should be shipped |

## 3. Store-count vintage (checked independently)

Published Table 3 (confirmed): FFR 15.0 (228.60); GROC 6.0 (76.80); SUPERC 0.0 (2.64); CONVS 16.0 (87.50); SPECS 1.0 (37.95). The separate row "Number of fast food retailers" is 15.0 (228.58).

| Release / year | FFR | GROC | SUPERC | CONVS | SPECS |
|---|---|---|---|---|---|
| Feb 2014, 2007 | 15 (228.58) | 6 (76.81) | 0 (2.64) | 16 (87.54) | 1 (37.95) |
| Nov 2012, 2007 | 15 (228.48) | 6 (76.77) | 0 (2.64) | 16 (87.51) | 1 (37.93) |
| Nov 2012, 2009 | **14** (230.52) | 6 (79.70) | **1** (3.36) | **15** (87.80) | 1 (31.67) |
| Aug 2015, 2007 | 15 (228.58) | 6 (76.75) | 0 (2.64) | **20 (255.72)** | 1 (37.92) |

What this shows:
- 2009 counts clearly do not match, and 2007 counts do.
- Feb 2014 fits best overall. Its FFR SD equals the published "Number of fast food retailers" SD (228.58) exactly. The manuscript could cite that row; it is stronger evidence than 228.60.
- The Aug 2015 2007 convenience-store counts differ (20, 255.72), which rules that release out. The manuscript could add this.
- The Ns 3,055/3,069 (2007) vs 3,054/3,064/3,065 (2009) are confirmed.
- The evidence for the 2007 choice is sound.

## 4. Number check (abstract, text, tables, captions, figures)

Everything not listed was checked against `results/*` and is correct. Only problems and borderline items are tabled.

| Location | Claim | Correct value | Verdict | Fix |
|---|---|---|---|---|
| §3.4 | "The expanded estimates fall within the range of the published 1.277 and 1.510" | 1.544 and 1.811, both **above** 1.510 | **Wrong** | "are close to or somewhat above the published 1.510 and 1.277" |
| §3.1 | "the demographic medians … also match the published descriptive statistics to the reported precision" | %Black, %Hispanic, median income and poverty match. Population median 25,849 vs 25,970 (SD 312,950 vs 313,819); bachelor's 11.7 vs 12.2; drove alone 79.2 vs 80.2; Gini 0.43 vs "0.4"; land area 604 vs 624; 65+ 3,975 vs 4,000 | **Overstated** | Name the variables that match and those that do not |
| §2.5 | Bachelor's-only 11.7% and drove alone 79.2% "match" the published 12.2 / 80.2 | Closer than the alternatives (bachelor's or higher 16.9; any car 90.9), but not a match | Overstated | "are closer to" |
| §3.7 | Low-commuting AR set "unbounded above ([0.75, ∞))" | (−∞, −621.8] ∪ [0.75, ∞), a union of two rays | **Incomplete** | Give both pieces, or "unbounded (two rays)" |
| §3.2 / Table 4 | (CONVS+GROC)/GROC "mean 3.90" vs published Table 4 mean 3.89 | 3.90 is the all-county mean. Table 4 is N = 3,108, where the contiguous mean is 3.92 | Minor | State the sample, or give 3.92 |
| §3.2 | Alt construction "matches all three published values" | True for median, SD and mean. But Table 4 count >3.89: published 1,419, alt 1,244 (Table 1 formula 2,176). Expanded counts don't match either (1,527 vs 1,470; 1,215 vs 1,425), and neither does food desert (1,065 vs 1,193) | Incomplete | Disclose that Table 4 counts are not reproduced by any construction |
| §3.2 | Expanded label swap "fits the Table 3 note" | Coefficients support the swap. Published SDs (2.14 / 2.38) vs reproduced e2 2.17 and e1 2.41, and Table 4 means, also point to a swap. R² slightly favours no swap. Published expanded medians and SDs are **not** reproduced by either Table 1 construction (e1 median 3.76 vs 3.4) | Incomplete | Say that the expanded descriptive statistics also don't match exactly. Add the SD evidence |
| §3.8 | "Excluding counties with any suppressed count … 2.27 (SE 1.12) on a weak first stage (F 4.1)" | Correct for traditional. The same subsample gives **strong-F** expanded IV estimates of 2.11 (0.71; F 11.7) and 2.24 (0.68; F 17.0), near the published IV | **Selective** | Report them |
| §3.8, §4.4 vs §2.7 | "suppressed count" | §2.7 and the code say −9999 = absent from CBP (2016 has no zeros), not suppression | Inconsistent | Use "−9999-coded" throughout |
| §2.4 | "For 17 states" (Overpass cross-check) | 16 states + DC (the list includes DC, AK, HI) | Minor | "16 states and DC" |
| §1 | "The publisher's page listed 549 citations" | 549 is the Google Scholar count shown on the MDPI page (Scopus 228, PMC 473, WoS 464 on the same page) | Imprecise | "549 citations (Google Scholar count shown on the publisher's page)" |
| §3.9 / §4.3 | "one SD (3.53) shifts obesity by 9.2 points … more than twice the SD"; "effects larger than the whole spread of county obesity" | 3.53 is the SD of the Table 1 construction. With the published SD (1.86), which the paper argues was the variable actually used, 2.604 × 1.86 = 4.84 points, about 1.16 SD of obesity | **Internally inconsistent / overstated** | Give both, e.g. "4.8 points with the published SD of 1.86 (9.2 with the Table 1 construction)". Soften "whole spread" |
| §3.9 / §5 | Zoning "about three percentage points" | The original says "about three percent". Reading it as pp is an interpretation; 3% of a 30.5% rate is about 0.9 pp | Unflagged assumption | Say it is read as pp, or show both |
| §3.9 | 0.0033 pp per 1% FFR; elasticity 0.012 | Arithmetic correct, but it presumes the Table 1 construction. Under the hypothesised (CONVS+GROC)/GROC, FFR is not in the index at all | Caveat missing | One sentence |
| §4.3 | "The original's reading … as an elasticity overstated…" | The original's own §4.3 says OLS implies lowering obesity "by about 0.003 to 0.12 percent" | Fairness | Acknowledge the original's 0.003 figure |
| Abstract | "first-stage F 28 to 35" | 27.5, 30.7, 35.0 | OK (27.5 rounds to 28) | – |
| Fig. 1 caption | Doesn't mention panel A's orange triangles (2009 counts) | – | Caption omission | Add "and with 2009 counts (triangles)" |
| Fig. 2B | First bar labelled "Published specification" | It is the reproduction's baseline (matched controls, OSM instrument), not the published model | **Misleading label** | "Baseline (matched controls)" |
| Fig. 3 | "Add log population" AR bar runs off the axis at 8.5 (true upper bound 16.47) with no marker | – | Minor | Add "→16.5" like the 15.6 marker |
| Fig. 3 / graphical abstract | "Long difference 2007→2016" | Counts 2007→2016, obesity 2009→2018 | Minor | "(counts 2007→2016, obesity 2009→2018)" |
| §2.8 | "Independent AI agents checked every number…" | True only once this and the citation audit are resolved | Conditional | Keep only after fixes |

Checked and correct (sample):
- Abstract: all numbers.
- §3.1: all store medians and SDs, the Ns, the zero-denominator counts (53, 39).
- §3.2: R², all four control coefficients and SEs, R² 0.474.
- §3.3: 77,175 nodes; 1,142 zero-exit counties; all six correlations.
- §3.4: all IV coefficients, F statistics and AR sets.
- §3.5: r 0.90; 0.36 (0.04); F 4.8 / 0.03 / 0.41 / 0.48 / 41.9; 0.77 (0.18).
- §3.5 para 2: 0.28, 0.34, 1.07 / 6.9, 1.8, 1,954 / 1.28; the range 0.28–1.34.
- §3.6: all values.
- §3.7: 1,510; 847; 0.46; 1.43 / 3.8; 0.98 / 10.9; 1.8; 0.98 / 31.3.
- §3.8: cross-section and long difference (4.9, 3.1; −0.010 / 0.012 / 3,011; −0.012; 0.002; −0.027).
- Tables 1–3: every cell. Table 4: every number.
- Figs 1–3 and the graphical abstract: values agree with the results files.

## 5. Claimed discrepancies in the original (verified against the article text)

| Claim | Original text | Verdict | Fairness |
|---|---|---|---|
| "2009 data" vs 2007 counts | §2.1: "This paper used 2009 data from the … Food Environment Atlas"; Atlas accessed 1 June 2015 (ref 45) | Confirmed. Data evidence is strong (§3 above) | Neutral |
| Traditional RFEI = (CONVS+GROC)/GROC? | Table 1 and §2.2.2 give (FFR+CONVS)/GROC. Table 3 gives 3.5 (1.86); Table 4 gives 3.89 | Descriptive match confirmed and unique among 1,372 candidates. Coefficient close (0.132 vs 0.125). Table 4 count not matched (see above) | Hedged ("consistent with", "cannot confirm"). Fine. Ship the search code |
| Supercenter placement | §2.2.2: "superstores in the numerator (unhealthy) in RFEI #1 and the denominator (healthy) in RFEI #2". Table 3 note: "in the denominator and numerator, respectively". §3.3: "expanded RFEI 1 with supercenters categorized as healthy" | Confirmed. §2.4.1 also lists "(2) Expanded RFEI with supercenters categorized as 'healthy' and (3) Expanded RFEI 2 … 'unhealthy'", which could be cited. Table 4 labels follow Table 1 | Fair |
| Control set | Table 6/8 notes: "number of fitness centers, natural amenities, % Black, % Hispanic, number of people over 65, poverty rate and county size". Table 9 and A4 show % bachelor's and no 65+ | Confirmed | Fair |
| SE type | Table notes: "Robust standard errors"; §3.3: "robust standard errors clustered by state" | Confirmed. This is not really a contradiction ("robust clustered" is normal Stata wording); the data show clustered | **Soften**: listing it in Table 4 as a "discrepancy" overstates it. Call it a clarification |
| Table 3 lila "(8.37)" = mean; milk:soda 30.2 (62.10) | Confirmed. The Atlas milk:soda ratio median is 0.845, SD 0.126 | "0.84" should read 0.85 (or 0.845) | Fair |
| Inequality direction | Abstract: "stronger in counties with greater income inequality (p < 0.05)". Table 9: 2.737 (Gini<0.41) vs 1.564. §3.4: "remained statistically significant in areas with lower income inequality". §4.4: stratifying "did not diminish the food swamp effect" | Confirmed | Add that the original's own §3.4 agrees with Table 9, so only the abstract diverges. Also, the abstract's "less mobile (p < 0.01)" vs Table 9's 2.452** (p<0.05) is a further unlisted inconsistency |
| Stata 14 vs 15 | §2.4: "STATA/SE version 14"; §2.4.2: "'ivregress' command in Stata (version 15.0)" | Confirmed | Trivial. Consider dropping it from Table 4 so the list doesn't look like nitpicking |

Overall tone:
- Neutral and non-accusatory. §4.2 says "None of these is unusual … some may be typographical" and frames code sharing generally.
- §1, "the IV result has not been checked", should be "could not be independently checked" or "to my knowledge has not been checked".
- §1, "often read as settling the question in favour of supply-side zoning", is unsupported. Cite a source or cut it.

## 6. Methods issues and overstatements

- **M1 (important). The county-size conclusion depends on the functional form.**
  - With *linear* population (per 10k) added, the traditional first stage stays strong: F 19.3, 2SLS 0.73 (0.25), AR [0.33, 1.46].
  - With the original's own "number of people over 65" control (r = 0.98 with population), it also stays strong: F 35.4, 2SLS 0.93. The note-controls variant gives F 40.8.
  - Only *log* population (with or without state FE) removes it.
  - So "the instrument works because exits count county size", "Highway exits mostly measure how big a county is" and "it has no predictive power" need qualifying:
    - Report the linear-population and 65+ count results.
    - Explain why log population is the right size control (the scatter in Fig. 2A is log-linear).
    - Note that the original's 65+ count would not have removed the first stage in the reproduction.
- **M2. The interpretation arithmetic mixes constructions.** The paper argues the published RFEI had SD 1.86 but evaluates the published IV coefficient with the Table 1 SD (3.53). See the table in §4 of this audit.
- **M3. The long difference** ("These estimates exclude … 0.086 … 1.02") is numerically correct. But:
  - (a) RFEI 2007 and 2016 correlate only 0.65, so the change carries a lot of measurement noise. The −9999 recoding and the different CBP vintage add to it, attenuating the slope toward zero.
  - (b) The outcome change mixes two estimation methods: CDC 2009 small-area estimates vs PLACES MRP, which uses county demographics. State FE do not remove county-specific model differences.
  - (c) An effect could take more than about 9 years to appear.
  - §2.7 calls it "a check on direction", which is appropriate. But the abstract's "do not survive", §3.8's "tells a different story" and §5's "do not survive … a long difference" should mention attenuation.
  - With the −9999 subset, e1/e2 give −0.082 (0.047) and −0.062 (0.052), which supports the null-or-negative reading.
- **M4. Density split** (§3.6): "The positive RFEI coefficient comes from the grocery-store denominator, not from more fast food per person" is a decomposition claim that no model tests. The unhealthy density coefficient is marginal (p≈0.08). Say "appears to be driven mainly by". Note that the densities exclude supercenters, specialised stores and farmers' markets.
- **M5. Selective reporting**: the expanded-RFEI 2016 IV in the no-−9999 subsample is strong-F and large (2.11, 2.24). See §4.
- **M6.** Undocumented `CTRL` choice: selected to match the published R². The paper says so in §2.5/§4.4, which is acceptable.
- **M7.** The SE small-sample convention (Stata `regress` style) should be stated in §2.5. Stata `ivregress` defaults may differ slightly.

## 7. Prioritised fix list

1. Fix the §3.4 sentence "fall within the range of the published 1.277 and 1.510" (it is false).
2. Qualify the county-size conclusion (M1). Add the linear-population and 65+ count results to Table 2 and §3.5. Soften the abstract, §4.1 and §5 wording ("mostly measure how big a county is").
3. Make §3.9/§4.3 consistent with the paper's own construction argument: 4.8 points at SD 1.86, alongside 9.2 at 3.53. State that "three percent" is being read as pp, and acknowledge the original's §4.3 "0.003".
4. Report the expanded-RFEI no-−9999 2016 IV results. Replace "suppressed" with "−9999-coded".
5. Add attenuation and measurement caveats to the long-difference conclusions in the abstract, §3.8 and §5.
6. Correct §3.1's "demographic medians match". Change "match" in §2.5 to "closer to".
7. In §3.2/Table 4, disclose the unmatched Table 4 counts and expanded descriptive statistics. Add the "Number of fast food retailers 228.58" evidence. Ship the construction-search script (1,372 candidates).
8. Fix the §3.7 AR set description. Fix the Fig. 2B bar label, the Fig. 1 caption and the Fig. 3 axis truncation marker.
9. Fairness edits: SE "discrepancy" → clarification; drop or demote Stata 14/15; add the original's §3.4 sentence on lower inequality and the abstract's p<0.01 mobility mismatch; soften the §1 "has not been checked" and "often read as settling" (or cite a source for the latter).
10. Minor: "16 states and DC"; the 549 citations source; milk:soda median 0.85; the long-difference years in Fig. 3 and the graphical abstract; list the years of the 2016 controls; the §2.8 "every number checked" claim, only after fixes.
