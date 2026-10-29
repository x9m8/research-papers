# Number audit: "Validated, not confirmed"

Auditor: independent number audit (Claude, claude-opus-5-5), 15 October 2026. I did not write the paper.
Scope: every number in `manuscript/manuscript.md` checked against `results/` and `code/overturn_reasons.csv`, the Methods checked against the code, and Figures 1–5 inspected.
Reproducibility: I copied the package to a scratch folder and reran build.py → analysis.py → sensitivity.py → figures.py → tables.py. All six result files came out byte-identical to the shipped ones, and the regenerated manuscript is unchanged. The manuscript and code were not modified. Note that tables.py writes into manuscript.md, so it should only be run on a copy.
Independent recomputation: scipy Clopper–Pearson and Poisson tails for every interval and p-value, sums by radius bin, unit conversions, lags, and Ofir et al. 2025 / Howard et al. 2025 counts from raw/ps.csv.

Verdicts: OK = matches results and is correctly rounded. MINOR = right in substance but imprecise, inconsistent or unexplained. WRONG = contradicted by data or code. UNSUPPORTED = goes beyond what the data show.

## 1. Abstract and summary

| Location | Claim | Check | Verdict | Fix |
|---|---|---|---|---|
| Social summary | "Of 3,043 exoplanets validated by statistics, 21 were later overturned" | B_all n=3,043, overturned=21. The 3,043 includes 3 planets weighed at discovery (K2-38 b, c; TOI-181 b) and 7 credited to two Vanderburg et al. 2016 ApJL papers (see §3.3 row) | MINOR | "credited to 24 validation publications" |
| Social summary | "Nearly all were brown dwarfs or small stars" | 12/21 (57%) are above the 30 MJup ceiling. 4 are background EBs. Kepler-699 b and 840 b are only "non-planetary" | UNSUPPORTED | "More than half were brown dwarfs or small stars" |
| Abstract | 3,043 planets, 24 papers | B_all, 24 BATCHES keys. The 24 are author-year groups that cover 30 bibcodes (see §3.3) | MINOR | see §3.3 |
| Abstract | 21 overturned, 0.69% (0.43–1.05%) | 21/3043=0.690%; CP 0.428–1.053% | OK | – |
| Abstract | 13 vs 1.55, p=1.1×10⁻⁸ | 1.5507; poisson.sf(12,1.5507)=1.147e-8 | OK | – |
| Abstract | 20 vs 2.68 across six papers | pooled 2.6849, obs 20 | OK | – |
| Abstract | All 13 Kepler overturns >6 R⊕ | Morton radii 6.27–17.9 | OK (but see "by construction" in §3.2) | – |
| Abstract | 12 of 21 above 30 MJup | S5 by_class 12/5/4 | OK | – |
| Abstract | remove those + 3 pre-validation → 3 vs 1.55, p=0.20 | S1S2 obs 3, p=0.204 | OK | – |
| Abstract | 64% never weighed | 3074/4781=64.3% | OK | – |

## 2. Introduction and Section 3 (Methods vs code)

| Location | Claim | Check | Verdict | Fix |
|---|---|---|---|---|
| §1 | vespa validated 1,284 in Morton 2016 | Morton list n=1,284 | OK | – |
| §3.1 | pscomppars 6,445 planets; ps 40,336 rows | comp 6,445; ps 40,336 | OK | – |
| §3.2 | weighed at discovery = pl_bmassprov "Mass", "which excludes masses estimated from radius" | This snapshot has only Mass / Msini / Msin(i)/sin(i) / NaN, with no M–R category. What the flag actually excludes is minimum masses (Msini). 16 "never weighed" planets have an Msini row | MINOR | "(which excludes minimum masses, M sin i)" |
| §3.2 | weighed later = mass from any other publication | Code matches. Upper-limit masses cannot be checked: ps.csv has no pl_bmasselim column | OK / note | Say whether mass upper limits are counted |
| §3.2 | Kepler overturned = "named KOIs that no longer appear among the archive's planets"; "The method found 13 removed Kepler planets, all from Morton" | build.py filters the removed KOIs to those in Morton table 6 (`gone = gone[gone.kepoi_name.isin(mort.kepoi_name)]`), so "all from Morton" holds by construction. Without the filter, 14 named KOIs are absent. The extra one is Kepler-1658 b (KOI-4.01, CONFIRMED in the cumulative table, not a Morton planet), which is missing from this pscomppars snapshot. It looks like a snapshot or naming artefact rather than an overturn | WRONG (method not described) | Describe the Morton filter, or apply the stated definition and explain why Kepler-1658 b is excluded. Then reword "The method found…all from Morton" |
| §3.2 | "All 4,781 transiting planets…and all 21 overturned planets were matched without exception" | 15 of 4,781 planets have no archive solution from their discovery paper (disc_row False), including WASP-19 b, HAT-P-7 b, TrES-4 b, CoRoT-4 b and Kepler-130 c. The code treats them as "announced without a mass". The zero-unmatched count in build_summary refers to the 1,658 paper-list rows, not to the 4,781 planets | WRONG | "All 1,658 entries in the six papers' lists matched an archive planet. 15 of 4,781 transiting planets have no discovery-paper solution and are treated as announced without a mass." This affects 3,434 by at most 15 |
| §3.2 | class definitions | match overturn_reasons.csv | OK | – |
| §3.3 | "24 publications that the archive credits…announced without a mass and whose method is statistical or ML validation" | analysis.py matches the archive credit by author-year string (disc_ref), not bibcode. Six groups merge several papers: Vanderburg 2016 (3 bibcodes), Livingston 2018 (2018a+2018b, 43 planets), Hirano 2018 (2), Heller 2019 (2), Giacalone 2022 (2, incl. ApJL HD 56414 b), Mistry 2023 (2, incl. MNRAS TOI-181 b). Three credited planets had a mass at discovery (K2-38 b, c in Sinukoff 2016; TOI-181 b in Mistry 2023), and K2-38 b, c are also counted as "weighed later" | MINOR | State that the credit was grouped by author-year (30 bibcodes), or match on bibcode and drop the planets with a mass at discovery |
| §3.3 | Vanderburg 2016 credit: ten K2 planets credited to "a candidate catalogue that validated nothing" | Only the 3 overturned (K2-51/67/76) carry the ApJS catalogue bibcode (2016ApJS..222...14V, from k2pandc). The other 7 are HIP 41378 b–f (2016ApJ...827L..10V) and HD 3167 b, c (2016ApJ...829L...9V), two Vanderburg et al. 2016 Letters that did validate or confirm planets | WRONG | Rewrite: "The archive credits K2-51 b, K2-67 b and K2-76 b to the Vanderburg et al. (2016) candidate catalogue…". Split the Table 1 row, or relabel its method |
| §3.3 | Crossfield 60/3 (track record) vs 106/6 (calibration) | Explained in §3.3 (archive credit vs own list) | OK | – |
| §3.3/Table 1 | Morton 1,282 credited vs 1,284 in calibration | Kepler-560 b and Kepler-1319 b are on Morton's list but credited to Mann et al. 2017. Not explained anywhere | MINOR | Add one sentence |
| §3.3/Table 1 | Livingston 2018 = 43 credited vs 42 (2018a) and 56 (2018b) in calibration | The credit merges a and b. Only 24 of 2018a's and 19 of 2018b's list planets are credited to them. Not explained | MINOR | Explain, and label the Table 1 row "Livingston et al. 2018a, b" |
| §3.3 | rates with two-sided CP; zero-overturn batches one-sided 95% bounds | cp(), cp_upper() match | OK | – |
| §3.4 | "the planets they validated", "each paper's own list" | The VizieR lists (Disp = Planet/VP) include planets confirmed earlier by others, some weighed at discovery: Crossfield 106 (only 59 credited to it, 16 with mass at discovery), Mayo 149 (95; 15), Montet 21 (17; 2, K2-19 b, c), L18a 42 (24; 2), L18b 56 (19; 4). Counts also differ from the paper titles (Crossfield 104, Montet 17, L18a 44, L18b 60). Including them only inflates the expected count (conservative) | MINOR | "each paper's list of planets with dispositions 'planet', which includes some previously known planets" |
| §3.4 | upper-limit FPPs taken at the limit | Code strips "<". Mayo has 118 upper limits, Montet 3, Morton/Crossfield 0 (no "<" anywhere in their tables) | OK | – |
| §3.4 | Livingston 2018b FPP "of their table 2" | Column FPP2 of VizieR table23 (= paper tables 2+3) | OK | – |
| §3.4 | pooled: "each planet once, under the first paper that lists it" | drop_duplicates(keep='first') in batches.csv order: Morton, Crossfield, Mayo, L18a, L18b, Montet. This is not chronological, so planets shared with Montet 2015 are counted under Crossfield 2016 | MINOR | "under the first paper in the order of Table 1 (calibration)", or sort chronologically. Expected changes only slightly |
| §3.6 | KM, censored at current age, Greenwood 95%, stop when <20 at risk | Code matches: S·√Σd/(r(r−d)), linear ±1.96 SE, evaluated at integer years. Planets with a later mass but no pubdate are treated as censored; events dated before announcement are set to t=0 | OK | (optional) mention linear Greenwood and integer-year evaluation |
| §3.7 | matched to TOI by TIC and period within 1% | 6 of 354 matches were accepted on TIC alone (TOI period missing). 6 duplicate TOI matches were resolved by taking the first row. 1 planet has no TIC | MINOR | "within 1% where the TOI period is available" |

## 3. Results

| Location | Claim | Check | Verdict | Fix |
|---|---|---|---|---|
| §4.1 | 4,781; 3,434; 360; 3,074; 64.3%; 47.7% of 6,445 | 3434−3074=360; 0.6430; 0.4770 | OK | – |
| §4.1 | Kepler 2,341/2,762; K2 401/549; TESS 327/1,004 | by_mission | OK | – |
| §4.2 | 3,043 / 21 / 0.69% (0.43–1.05) / 202 weighed / 223 followed / 9.4% (5.9–14.0) | B_all; CP recomputed | OK | – |
| §4.2 | Kepler 2,418/13; K2 391/8; TESS 234/0 | B_by_mission | OK | – |
| §4.2 | "Every Kepler overturn comes from one paper" | True in the output, but guaranteed by the Morton filter in build.py (see §3.2) | MINOR | Tie to the corrected method description |
| §4.2 | K2: Crossfield 3, Vanderburg 3, Livingston 2018a 1, Christiansen 2022 1 | B_batches. Table 1 says "Livingston et al. 2018" (merged credit) | OK / MINOR | Label consistently |
| §4.2 | Rowe 716, 119 weighed, 0 overturned, upper bound 2.5% | cp_upper(0,119)=2.49% | OK | – |
| §4.2 | Rowe "best follow-up of any large batch", "because many are in resonant chains" | 16.6% followed. Crossfield (60 planets) has 16.7%. Rowe's later masses are mostly TTV (Hadden 2014: 56, Ofir 2025: 28, Hadden & Lithwick 2017: 7, Mills 2016: 4). "Resonant chains" is not shown by the data | MINOR | "of any batch of hundreds"; "many are in near-resonant multi-planet systems with measurable TTVs" |
| §4.2 | ML 420 planets, 4 followed, bound 53% | 50+301+69=420; 0+3+1=4; 52.7% | OK | – |
| §4.3 | Morton 1,284, 1.55, 13, 1.1×10⁻⁸ | C_calibration | OK | – |
| §4.3 | Crossfield "validated 106" K2 planets, 1.08, 6, p=0.0009 | Numbers OK, but the title of the cited paper says 104 validated (see §3.4) | MINOR | "Crossfield et al. (2016) list 106 K2 planets…" |
| §4.3 | Livingston 2018a "validated 42", 0.0099, 1, p=0.0098 | 0.009876; p=0.00983. The title says 44 | MINOR | "list 42 matched planets" |
| §4.3 | others expected 0.02–0.05 | 0.0206, 0.0258, 0.0470 | OK | – |
| §4.3 | pooled 1,563, 20 vs 2.68, p=1.2×10⁻¹¹ | 1.217e-11 | OK | – |
| §4.3 | Morton and Crossfield report no upper-limit FPPs | 0 "<" in either VizieR table | OK | – |
| §4.4 | <6 R⊕: 1,209 planets, 1.47 expected, 0 overturned | 600+560+49=1209; 0.6895+0.7273+0.0553=1.472 | OK | – |
| §4.4 | >6 R⊕: 75, 0.079, 13; radii 6.27–17.9 | 45+30; 0.0786 | OK | – |
| §4.4 | lower bound 17.3% (9.6–27.8) | CP(13,75) | OK | – |
| §4.4 | 20 of 75 followed; 65% (41–85) | 13+7; CP(13,20)=40.8–84.6 | OK | – |
| §4.4 | own expectation ~0.1%; "two orders of magnitude" | 0.0786/75=0.105%. 17.3/0.105=165×, 65/0.105=620× | OK | – |
| §4.4 | "Seven were stars between about 78 and 103 MJup" | Kepler-486 (78), 503 (79), 807 (78), 628 (92), 706 (93), 470 (103), plus K2-76 b 0.094 M☉ × 1047.6 = 98.5 MJup → 7 | OK | (optional) name K2-76 b |
| §4.4 | two brown dwarfs ~37 and 40 MJup | Kepler-494, 492 | OK | – |
| §4.4 | K2-51 b and K2-67 b ~0.15 and 0.16 M☉; Kepler-854 b | 0.146→0.15 (153 MJup); 0.161→0.16 (169 MJup). 7+2+3=12 | OK | – |
| §4.4 | five stellar eclipses: hierarchical triples, a self-luminous companion, two radius-too-large | Kepler-469, K2-399 (triples/hierarchical), Kepler-488, Kepler-699, Kepler-840 = 5 | OK | – |
| §4.4 | four background/nearby EBs | K2-78, 82, 92, 256 | OK | – |
| §4.4 | KOI-126 = Kepler-469 b; Díaz 2013, 2014 KOIs | cum: K00126.01 = Kepler-469 b; K00205.01 = Kepler-492 b; K00189.01 = Kepler-486 b | OK | – |
| §4.4 | S1: Morton 10 vs 1.55, "p = 5 × 10⁻⁶" | 5.46e-6. Table 3 prints 5.5 × 10⁻⁶ | MINOR | Use 5.5 × 10⁻⁶ in text |
| §4.4 | S2: 4 (p=0.072); both 3 (p=0.20); Crossfield 3 vs 1.08 p=0.096 | sensitivity.json | OK | – |
| §4.5 | KM at 5 yr: Kepler 5.6% (4.7–6.5), K2 10.3% (7.5–13.1), TESS 46.3% (35.9–56.7) | D_followup km[5]. TESS at-risk is 24, ≥20 | OK | – |
| §4.5 | Kepler step from Ofir et al. 2025, "masses for 38 of these planets about eleven years after validation" | From ps.csv: Ofir 2025 gives the first measured mass for 43 Kepler planets announced without a mass (90 have some Ofir mass). 28 of the 43 (all Rowe 2014) have lag ≈10.9 yr and make up 28 of the 30 events in the 10–11 yr KM interval. 37 have lag ≥10 yr. 38 cannot be reproduced. Several of the 43 were not validations (Swift 2013, Muirhead 2012, Steffen 2013, Fabrycky 2012) | WRONG | "…which gave the first measured masses for 43 of these planets, 28 of them Rowe et al. (2014) validations about eleven years after announcement" |
| §4.5 | K2 step "mostly from Howard et al. 2025" | 9 of 12 events in the 8–9 yr interval are Howard 2025 (11 first masses in total) | OK | – |
| §4.5 | lag median 2 yr, range −5 to 8 | S5; recomputed list (calendar-year differences) | OK | (optional) say "calendar years" |
| §4.6 | 405 TESS; 354 matched; 264 CP, 86 PC, 2 APC, 2 KP; no FP/FA | E_tess | OK | – |
| §4.6 | 23 followed TESS validations, bound 12% | S4_groups 12.2% | OK | – |

## 4. Discussion and conclusions

| Location | Claim | Check | Verdict | Fix |
|---|---|---|---|---|
| §5.1 | small planets: no overturns beyond prediction | Morton <6 R⊕: 0 vs 1.47 | OK | – |
| §5.1 | "at least one in six…was a brown dwarf or star" | 13/75=17.3% counts Kepler-699 b and Kepler-840 b, which are only "non-planetary" (radius too large). Brown dwarf or star established for 11/75 = 14.7% (about one in seven) | WRONG (wording) | "at least one in six…was not a planet, most of them brown dwarfs or stars" |
| §5.1 | "plausibly more than half of those followed" | 65% (41–85%) | OK | – |
| §5.1 | Santerne 34.8±6.5%, 54.6±6.5%; Fressin 9.4%, 17.7% | Not in the result files; belongs to the citation audit | n/a | – |
| §5.3 | 64% never weighed; 13 overturns in the largest batch are giants | OK | OK | – |
| §5.4 | 9 of 1,209 small Morton planets weighed; upper bound 28% | 3+5+1=9; cp_upper(0,9)=28.3% | OK | – |
| §5.4 | bulk validation of giants accounts for most overturns | 13 Morton giants + K2-51/67/76 warm Jupiters ≥16/21 | OK | – |
| §5.5 | Kepler-452 b controversial; Kepler-747 b still listed | Both controv=1 and listed (Kepler-747 b is the Morton "controversial" 1) | OK | (optional) note that Kepler-747 b is also flagged controversial |
| §5.5 | six papers, 1,563 planets | OK | OK | – |
| §6 | "roughly two orders of magnitude" | 165–620× | OK | – |

## 5. Tables

| Location | Claim | Check | Verdict | Fix |
|---|---|---|---|---|
| Table 1 | all rows | identical to tables.md and analysis.json; upper bounds = cp_upper(0, followed) | OK | – |
| Table 1 | Vanderburg 2016 method "archive credit to a candidate catalogue; validated elsewhere" | True for only 3 of 10 planets (see §3.3) | WRONG | Split or relabel |
| Table 1 | "Livingston et al. 2018" | merged a+b credit | MINOR | "2018a, b" |
| Table 1 calib. | Livingston 2018b median FPP "6.5e-06" | value 6.55e-06 (float rounding to 6.5) | MINOR | 6.6e-06 or 6.55e-06 |
| Table 1 calib. | other entries | match | OK | – |
| Table 2 | 21 rows, classes, years | match overturn_reasons.csv | OK | – |
| Table 3 | all values | match sensitivity.json | OK | – |
| Table 3 note | 75, 13, 7, 0.079; 17.3% (9.6–27.8); 65.0% (40.8–84.6) | match | OK | – |

## 6. Figures (PNG inspected)

| Figure | Check | Verdict | Fix |
|---|---|---|---|
| Fig 1 | Stacked bars match by_year (2014 = 810, 2016 = 1,432). Colours match the caption. The annotation "Morton et al. validate 1,284" points at the 2016 total bar (1,432). 2002 and 2004 (6 planets) are dropped by the ≥2005 cut. No overlaps | OK / MINOR | Optional: mention the axis starts in 2005 |
| Fig 2 | Ticks, bands and circles match C_calibration. Text labels match the table. Orange for Morton, Crossfield, L18a. Caption matches | OK | – |
| Fig 3 | Panel A labels 3/600, 5/560, 1/49, 7/45, 13/30 match (later_mass + observed). Panel B 0.69/0.73/0.06/0.05/0.03 and 0/0/0/4/9 match. The "0.05" and "0.03" value labels touch or overlap the adjacent orange bars. Bins are [6,10) and ≥10, consistent with ">6 R⊕" | MINOR | Move small expected labels up or left |
| Fig 4 | KM points match D_followup.km. Ends: Kepler 12 yr, K2 10 yr, TESS 5 yr. The x-axis reads "Years since validation" but the population is all planets announced without a mass, and the caption says "since announcement" | MINOR | Relabel the axis "Years since announcement" |
| Fig 5 | 21 rows; validation and refutation years match overturn_reasons.csv; colours and shapes match the classes; legend clear of the axis | OK | – |

## Required fixes

1. **Social summary.** "Nearly all were brown dwarfs or small stars" is unsupported (12 of 21). Change it to "More than half…".
2. **§3.2, Kepler overturns.** Describe the filter that keeps only removed KOIs on Morton et al.'s list. Without it the stated definition gives 14, including Kepler-1658 b (KOI-4.01, absent from this pscomppars snapshot, likely an artefact). Explain that exclusion. Then reword "The method found 13…all from Morton" and §4.2's "Every Kepler overturn comes from one paper", which currently hold by construction.
3. **§3.2, "matched without exception".** Correct the sentence. All 1,658 paper-list entries matched, but 15 of the 4,781 transiting planets have no discovery-paper solution and are treated as announced without a mass (e.g. WASP-19 b, HAT-P-7 b). Either fix that classification or state it.
4. **§3.2, mass definition.** The "Mass" flag excludes minimum masses (M sin i), not radius-based estimates.
5. **§3.3 and Table 1, Vanderburg et al. 2016.** Only K2-51 b, K2-67 b and K2-76 b are credited to the candidate catalogue. The other 7 credited planets (HIP 41378 b–f, HD 3167 b, c) come from two Vanderburg et al. 2016 Letters that did validate or confirm planets. Rewrite the sentence and split or relabel the Table 1 row.
6. **§3.3, batch definition.** Say that archive credit was grouped by author-year: the 24 groups cover 30 bibcodes (Livingston 2018 a+b, Hirano 2018, Heller 2019, Giacalone 2022, Mistry 2023, Vanderburg 2016). Either note or remove the three credited planets with a mass at discovery (K2-38 b, c; TOI-181 b).
7. **Track-record vs calibration counts.** Explain Morton 1,282 vs 1,284 (Kepler-560 b and Kepler-1319 b are credited to Mann et al. 2017) and Livingston 43 vs 42/56 (merged credit). Crossfield 60 vs 106 is already explained.
8. **§3.4 and §4.3, calibration lists.** The lists include planets validated or confirmed earlier by others, some weighed at discovery. Replace "validated 106" (Crossfield; title says 104) and "validated 42" (Livingston 2018a; title says 44) with "list". Note that Montet's list has 21 planets against 17 validated.
9. **§3.4, pooled analysis.** "First paper that lists it" is file order (Morton, Crossfield, Mayo, L18a, L18b, Montet), not chronological. Say so, or sort by date.
10. **§4.5, Ofir et al. 2025.** "38 of these planets" cannot be reproduced. Ofir 2025 gives the first mass for 43 Kepler planets announced without a mass. 28 of them (all Rowe 2014, about 10.9 yr after announcement) make the step. Correct the number and say "announcement", since several of the 43 were not validations.
11. **§5.1.** "At least one in six…was a brown dwarf or star" counts Kepler-699 b and 840 b, which are only "non-planetary" (11 of 75 = 14.7% are established brown dwarfs or stars). Reword to "was not a planet, most of them brown dwarfs or stars".
12. **§4.4.** Give the S1 p-value as 5.5 × 10⁻⁶, consistent with Table 3.
13. **Table 1 calibration.** The Livingston 2018b median FPP should read 6.6e-06 (or 6.55e-06), not 6.5e-06.
14. **§4.2.** Qualify "best follow-up of any large batch" (Crossfield, 60 planets, is at 16.7% vs Rowe 16.6%). Change "resonant chains" to "near-resonant multi-planet systems with TTVs" (the later masses are mostly from TTV papers).
15. **§3.7.** Add "where the TOI period is available": 6 of the 354 matches rest on TIC alone.
16. **Figure 4.** Change the x-axis label to "Years since announcement", to match the caption and method.
17. **Figure 3B.** Move the "0.05" and "0.03" expected-value labels so they don't overlap the orange bars.
18. **Table 1.** Label the merged row "Livingston et al. 2018a, b".

## Resolution (15 Oct 2026)
All 18 fixes applied. Track record re-keyed by bibcode (24 publications whose method was confirmed in the citation audit); K2-51 b, K2-67 b, K2-76 b credited to Crossfield et al. 2016; planets weighed in the credited paper excluded (track record now 3,028 planets, 21 overturned, 192 weighed later). Pooled calibration now orders papers by date (expected 2.69, p = 1.3e-11). Kepler overturn filter and the Kepler-1658 b exclusion described in Section 3.2; Ofir et al. 2025 claim corrected to 43 planets (28 Rowe 2014); Figure 3B labels and Figure 4 axis fixed.
