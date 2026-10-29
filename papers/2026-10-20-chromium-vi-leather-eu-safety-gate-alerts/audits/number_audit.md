# Number audit: "Fewer alerts, same allergy: hexavalent chromium in EU leather goods, 2005–2026"

Auditor: independent check (did not write the paper). Date: 2026-10-20.
Scope: manuscript.md against results/ (alerts.csv, analysis.json, sensitivity.json, build_summary.json, tables.md), code/ (common, build, analysis, sensitivity, figures, tables), raw snapshot and denominators, and lit/brief.md. Nothing in the manuscript or code was edited.

## 0. Summary

- **Reproducibility.** OK. A fresh copy rebuilt from the raw snapshot (`P4_RAW=/home/claude/p4/raw`, running build → analysis → sensitivity → figures → tables) gave byte-identical analysis.json, sensitivity.json, build_summary.json and tables.md, and an identical alerts.csv and manuscript.md.
- **Number transcription.** Nearly every number in the text, tables and captions matches the result files and is correctly rounded. The few rounding and labelling slips are listed below.
- **One major classification error, which changes several results.** All 25 Italian notifications from 2010 (1618/10–1667/10, 1733/10) are **textile garments**: jumpers, T-shirts, tracksuits, velvet trousers, a dress, and "imitation leather" trousers and jackets. They are not leather. They entered scope only because a boilerplate risk sentence says "clinical studies … indicate that, for leather goods, 50% of sensitive subjects…". They belong to one 36-notification Oeko-Tex batch; the 11 copies with a shorter text were excluded. Removing them leaves the post-2015 trend and the 13-fold figure unchanged. It does overturn the "began in 2010 with Italy" narrative, the 2010–2014 growth rate, the pre-limit composition, Germany's "unchanged" share, and part of the "concentration fall is fragile" argument (Section 4).
- **Concentration extraction.** 1 error in the random sample of 60 (1.7%, 95% CI 0.04–8.9%). A full-scope scan found one more error.
- **Classification.** In scope: 1 of 30 wrong (3.3%, 0.08–17.2%), the tip of the systematic 25/617 textile error (4.1%, 2.6–5.9%). Out of scope: 1 of 30 should be in scope (a leather necklace excluded by the JEWELLERY category rule).
- **Component counts misdescribed.** "Where the notification named the part that failed" (148 insole, 141 lining, 114 upper) counts any mention anywhere, mostly in the product description. Counted in the risk and legal text, the numbers are 83, 28 and 12.
- **Literature numbers.** All match the brief. Two discussion statements are wrong or unsupported: "five to ten years after", and "the only Danish series that spans the regulation". Alinaghi et al. (2019) is listed in the references but never cited; it reports a Danish decline in 2002–2017 that is relevant counter-evidence.

## 1. Claim-by-claim table

Verdicts: OK / WRONG / UNSUPPORTED / MINOR. "Corrected" values come from a rerun on a scratch copy with the 25 textile notifications removed, the leather necklace A12/1217/13 added, and the two extraction errors fixed (A12/0674/14 → 17.8; 1857/10 → 60).

| Location | Claim | Check | Verdict | Fix |
|---|---|---|---|---|
| Social summary | "fell 13-fold after 2015" | 39.69/3.00 = 13.2 (2013–2015 vs 2023–2025); base includes pre-limit years | MINOR | "fell 13-fold between 2013–15 and 2023–25" |
| Abstract | 617 notifications, 2005–2026 | n_scope 617 | OK (but see A1) | 593 after the textile correction |
| Abstract | "Notifications rose from 2010" | 2010 = 26 only because of 25 textile items; true 2010 count = 1 | WRONG | "rose from 2011" |
| Abstract | "peaked in 2014 at 43 per 1,000" | 42.71 | OK | – |
| Abstract | "fallen by 26% a year (95% CI 23–29%)" | −26.05 (−29.19 to −22.77) | OK | Optional: NB dispersion collapsed to 0 (see M7) |
| Abstract | "to 3.0 per 1,000 in 2023–2025, a 13-fold drop" | 3.00; 13.2-fold is vs 2013–2015 (39.7), not vs the 2014 peak of 43 just named (that ratio is 14.3) | MINOR | Name the base: "from 39.7 in 2013–2015" |
| Abstract | "Germany sent 56%" | 344/617 = 55.75% | OK | 58.2% (345/593) after correction |
| Abstract | "share made in the EU doubled" | 9.0% → 20.6% | OK | Corrected 9.9% → 20.6%, still roughly doubled |
| Abstract | "median of 14 mg/kg" | 14.3 | OK | – |
| Abstract | "one in four exceeded ten times the limit" | 147/611 = 24.1% | OK | Corrected 148/587 = 25.2% |
| Abstract | "a fall in concentrations after 2015 was not robust" | Holds for the excluding-Germany check; the min-value check becomes significant after correction | MINOR | Reword after the rerun (Section 4) |
| Abstract | surveys 23–35% → 11–13% | Brief: 23, 32, 35%; 13.3, 10.6, 12% | OK | – |
| Abstract | Danish allergy "about 2%" | Larsen 2026: 2.3, 1.9, 2.1% | OK | – |
| Intro ¶1 | 80–90% of tanneries (Black 2013); >90% of production (Hedberg 2015) | Brief 3.5 | OK | – |
| Intro ¶1 | 80 °C, UV, alkaline, fatliquors, dry storage; humidity suppresses | Brief 3.1/3.2 (fatliquor point is from Annex XV / Palop, not Hedberg or Mathiason) | MINOR | Fine as is, or cite Danish EPA 2012 for fatliquors |
| Intro ¶2 | leather share 24% → 46%, 1985–2007 (Thyssen 2009) | 24.1 → 45.5 | OK | – |
| Intro ¶2 | foot/hand dermatitis, sick leave, QoL (Bregnbak 2014; Alinaghi 2021) | Brief 2.4, 2.7 | OK | – |
| Intro ¶3 | German ban Aug 2010; Reg. 301/2014; 3 mg/kg = EN ISO 17075 limit; 80% (recital 7) | Brief 1.1, 1.3 | OK | – |
| Intro ¶3 | RAC: "roughly 5,800–15,800 cases a year" | 5,760–15,840 net of the German rule | OK | – |
| Intro ¶4 | 4,830 patients, 2016–2024, 2.1%, no lower than before | Brief 2.8 | OK | – |
| Intro ¶4 | "about one article in eight" | 13.3, 10.6, 12% | OK | – |
| Intro ¶4 | Cr(VI) among three most-alerted substances (EEA) | Brief 4.8 (phthalates, Cr(VI), cadmium; restricted chemicals, human health) | OK | – |
| 2.1 | Decision 2019/417 s. 3.4.3.3 | Brief 6.1; that Decision is no longer in force from 26.3.2025 (GPSR) | MINOR | Note that the rules changed under the GPSR (Dec 2024 / Mar 2025) |
| 2.1 | "records of limit exceedances" | Pre-2015 notifications had no EU limit; the 2010 Italian batch used a self-set 5 mg/kg | MINOR | Qualify for pre-2015 |
| 2.1 | 20 Oct 2026; three searches; 1,089 distinct | snapshot queries = [chromium, hexavalent, leather]; 1,089 ids | OK | – |
| 2.1 | denominators from the same service | denominators json: totalElements for {year} and {year, riskType: CHEMICAL} | OK | – |
| 2.2 | Cr(VI) forms incl. misspellings; 675 | CRVI regex; n_crvi 675 | OK | – |
| 2.2 | leather unless "only" imitation | Code: count of "leather" mentions > count of imitation phrases | MINOR | Describe the counting rule; note that leather in boilerplate text triggers it (cause of the textile error) |
| 2.2 | Article list "shoes, boots, … watch straps" | Code also has footwear, moccasin, clog, sneaker, trainer, loafer, mitten, purse | MINOR | Complete the list |
| 2.2 | Exclusion categories "cement, toys, cosmetics, jewellery and chemical products" | Code excludes CONSTRUCTION_PRODUCTS (cement, tile adhesive, sealing slurry), TOYS, COSMETICS, JEWELLERY, CHEMICAL_PRODUCTS | MINOR | "construction products (mainly cement)" |
| 2.2 | "542 that name leather and 75 by product type" | 542; 617−542 = 75 | OK | 518 + 75 after correction |
| 2.2 | 58 excluded = 29 toys, 13 textile garments, 8 cement, 5 cosmetics, 3 others | category counts 29/13/8/5/1/1/1. The "3 others" are 1 cement (category OTHER), 1 **leather necklace** (A12/1217/13, 62.5 mg/kg), 1 tattoo ink. The 8 "cement" are 6 cement, 1 tile adhesive, 1 sealing slurry. Of the 13 textiles, 1 mentions (synthetic) leather (a bikini) and 11 are the excluded half of the Italian Oeko-Tex batch | WRONG (necklace should be in scope) / MINOR (labels) | Bring the necklace into scope (leather article under entry 47); list as 9 construction products incl. 7 cement, 1 tattoo ink |
| 2.2 | 617 in study set | 25 are non-leather textiles (Section 3) | WRONG | Exclude the 25; n = 593 |
| 2.2 ¶2 | product types, child flag, component flags | Bag regex is checked before garments and matches "collar", "pouch", "strap", "belt", "watching": about 10 of 73 "bags" are garments (4 textiles, a leather jacket, 4 lederhosen, a leather bra, a jockstrap, adult novelty items) | MINOR | Check garments before bags, or use word boundaries; recount |
| 2.2 ¶2 | Origin groups | Code as stated | OK | – |
| 2.3 | uncertainties dropped; ranges/lists; % < 1% converted; limit values skipped; other-substance filter | Code matches. Not stated: fallback to the product description and to the next sentence; "mg/k" read as mg/kg; ppm = mg/kg; values ≥ 100,000 dropped | MINOR | Add the unstated rules |
| 2.3 | 611 of 617 with value | 611 | OK | 587/593 after correction |
| 2.3 | two g/kg reports, not converted; one had no other value | A12/1113/13 (15 g/kg only, no value), A12/1000/15 ("11.6 g/kg and 10.6 mg/kg" → 10.6) | OK | – |
| 2.4 | before/after split at 1 May 2015 by publication date | `pub_date >= '2015-05-01'` | OK | – |
| 2.4 | NB with log(all alerts) offset; MoM dispersion | Code does this, but for the main model α hit the 1e-8 floor, so the model is Poisson (Table 3 Poisson row identical). Pearson χ²/df = 1.43; quasi-Poisson CI is −29.8 to −22.1 | MINOR | State that α was estimated at 0, or use a Pearson-based α / quasi-Poisson; CI widens slightly |
| 2.4 | 2016–2025 main; 2010–2014 before | Code | OK | – |
| 2.4 | bootstrap 10,000, fixed seed | B = 10000, seed 20261020 | OK | Give the seed |
| 2.4 | Mann–Whitney, GM ratio, OLS log10 with robust SE, median regression | HC1 OLS, quantreg q = 0.5 | OK | – |
| 2.4 | "Proportions carry exact (Clopper–Pearson) intervals" | Only Germany's share has a CI; other percentages have none | MINOR | "Germany's share carries…", or add CIs |
| 2.4 ¶2 | sensitivity list | S1–S7 plus chem offset from analysis.py all present | OK | – |
| 3.1 | 12 May 2005 – 13 Aug 2026 | A.first/last | OK | – |
| 3.1 | Footwear 307 (49.8%), gloves 171 (27.7%), bags 73 (11.8%), garments 63 (10.2%) | analysis A.ptype | OK as computed | Corrected: 307 (51.8%), 171 (28.8%), 69 (11.6%), 42 (7.1%), other 4. Fix the bag/garment regex too |
| 3.1 | Children 96 (15.6%) | 96 | OK | 95 (16.0%) after correction |
| 3.1 | "Where the notification named the part that failed … insole 148, lining 141, upper 114" | Flags search all text including the product description (e.g. "leather upper, cream leather insole"). In legal + risk text: insole 83, lining 28, upper 12 | WRONG | Recount on risk/legal text only, or drop "the part that failed" |
| 3.1 | "43 countries of origin" | 43 values include "Unknown" → 42 countries (Hong Kong and Taiwan counted separately) | WRONG (minor) | "42 countries or territories" |
| 3.1 | China 272 (44.1%), India 62 (10.0%), Pakistan 47 (7.6%), EU 95 (15.4%), unknown 66 (10.7%) | analysis | OK | Corrected: China 271 (45.7%), India 62 (10.5%), Pakistan 47 (7.9%), EU 95 (16.0%), unknown 43 (7.3%) |
| 3.1 | 19 notifying countries; Germany 344 (55.8%), Spain 89 (14.4%), Italy 33, France 29, Estonia 28, Finland 27 | analysis | OK | Corrected: Germany 345 (58.2%), Spain 89 (15.0%), **Italy 8**, France 29, Estonia 28, Finland 27 |
| 3.1 | Measures 319 (51.7%), 206 (33.4%), 36 (5.8%), 56 (9.1%) | analysis; 56 = blank | OK | Corrected: 320 (54.0%), 181 (30.5%), 36 (6.1%), 56 (9.4%) |
| 3.2 | "five notifications in five years before 2010" | 2+0+0+1+2 | OK | – |
| 3.2 | "began in earnest in 2010, when Italy sent 25 of the year's 26" | The 25 Italian items are textile garments; the true 2010 count is 1 (France, 1857/10) | WRONG | Rewrite: notifications began in earnest in 2011 with German enforcement |
| 3.2 | "grew by 44% a year … 2010–2014 (95% CI 27–62%)" | Matches the file (43.6; 27.4–61.8) but is driven by the spurious 2010 = 26 | WRONG | Corrected: +95% a year (63–132%) |
| 3.2 | "German … only four in 2005–2009, resumed in 2011 … reached 62 in 2013" | DE: 2005 2, 2009 2; first after 2009 on 2011-02-16; 2013 = 62 | OK | 2013 = 63 if the necklace is added |
| 3.2 | peak 2014: 97, 42.7 per 1,000 | B_peak | OK | – |
| 3.2 | "fallen almost every year" | 2019/20 flat, 2023 up | OK | – |
| 3.2 | −26.1% (22.8–29.2); chem −33.5% (29.6–37.2); raw −20.3% (16.6–23.8) | B_trend, S5 | OK | Unchanged by the correction |
| 3.2 | 39.7 vs 3.0; 13-fold; 15.1% → 0.57% | B_peak3, B_recent | OK | Corrected 39.9; 15.2%; fold 13.3 |
| 3.2 | 2016–2022: −24.2% (19.0–29.2) | S5 | OK | – |
| 3.2 ¶2 | Germany 29.4 → 16.0 a year; others 19.4 → 12.8 | C_other_per_year | OK as computed | Corrected: others 14.4 → 12.8; DE 29.6 → 16.0 |
| 3.2 ¶2 | both declined ~25–27% a year | −25.1, −26.9 | OK | – |
| 3.2 ¶2 | ten first-time notifiers after May 2015 (list) | C_first_after | OK | – |
| 3.2 ¶2 | "The EU limit widened participation" | Causal reading of a timing coincidence | UNSUPPORTED (minor) | "After the limit, ten countries notified for the first time" |
| 3.2 ¶2 | Germany 58.8% (52.7–64.7) vs 52.9% (47.5–58.3), "barely changed" | Correct as computed. Corrected before-share is 64.9% (58.6–70.8); the CIs no longer overlap | WRONG after correction | Report a ~12-point fall in Germany's share |
| 3.3 | footwear 66 → 36, gloves 20 → 34, bags 4 → 19 | E.ptype 66.4/36.2, 20.2/33.8, 3.6/18.5 | OK | Corrected before: 73/22/2, garments 2% |
| 3.3 | China 53 → 36, South Asia 11 → 24, EU 9 → 21 "more than doubled" | 53.4/36.5, 10.8/24.1, 9.0/20.6 | OK | Corrected before: 58/12/10 → "roughly doubled" |
| 3.3 | children 17 → 14 | 17.3/14.1 | OK | Corrected 18.6 → 14.1 |
| 3.4 | "Every notified value was at or above 3; six exactly 3" | Highest values all ≥ 3; six = 3 (all six verified as genuinely reported 3 mg/kg). Some reported lower range bounds are below 3 (e.g. 2.4, 1.6 in the textile batch) | MINOR | "Every highest value…" |
| 3.4 | median 14.3 (13.8–15.4), IQR 8.0–28.8, max 414 in gloves | D_conc; max 414.3 = A12/0048/13 ladies' gloves (verified) | OK | Corrected median 14.3 (13.0–15.6), IQR 7.9–30.2 |
| 3.4 | "almost five times the limit" | 4.8× | OK | – |
| 3.4 | 147 (24.1%) > 10×; 91 (14.9%) ≤ 2× | D_conc | OK | Corrected 148 (25.2%), 91 (15.5%) |
| 3.4 ¶2 | 17.5 → 13.0, p = 0.0002, GM −25%, >10× 31.6 → 17.9% | D_conc | OK | Corrected 17.6 → 13.0, p = 0.0003, GM −26%, 35.1 → 17.9% |
| 3.4 ¶2 | OLS −5.4% (−7.0 to −3.8); median reg −4.3% (−6.9 to −1.6) | D_conc.trend | OK | Corrected −6.0 (−7.8 to −4.2); −5.1 (−8.1 to −1.9) |
| 3.4 ¶2 | German 20.9 → 13.5; others 14.1 → 12.8, p = 0.52 | S4: 20.95 → 13.5; 14.1 → 12.8, p = 0.523 | MINOR (20.95 rounds to 21.0) | Corrected: DE 21.2 → 13.5; others 10.1 → 12.8, p = 0.93 |
| 3.4 ¶2 | "It also disappears if the lowest … (14.4 to 13.0; p = 0.55)" | Correct as computed; after correction 16.0 → 13.0, p = 0.005, so it does not disappear | WRONG after correction | Drop this leg of the fragility argument; keep the Germany-excluded result |
| 3.4 ¶2 | count decline held in every sensitivity analysis | All Table 3 trends negative, CIs exclude 0 | OK | – |
| 3.5 | 23–35% (Danish EPA 2012); 467 → 13.3% (ECHA 2018); 94 → 10.6%; 12% of 99 (Köhler) | Brief 5 | OK | – |
| 3.5 | "fell by roughly a factor of two to three" | 23–35 vs 10.6–13.3 → 1.7–3.3 | OK | – |
| 3.5 | Gentofte 2.3 / 1.9 / 2.1% | Brief 2.8 | OK | – |
| 4.1 ¶1 | "fell year after year" | 2023 rose (11 → 20); 2019–20 flat | MINOR | "fell in most years" |
| 4.1 ¶2 | "one in eight still exceeded the limit **five to ten years** after it took effect" | Surveys are from 2016, 2019 and 2020–21, i.e. 1–6 years after | WRONG | "one to six years after" |
| 4.1 ¶3 | "The likeliest explanation is … fewer checks" | No data on testing volume; plausible but untested | UNSUPPORTED | Hedge: "A plausible explanation…"; say that test counts are not published |
| 4.1 ¶3 | "Notifications began in a burst from Italy in 2010" | That burst was textiles | WRONG | Delete; begin with German enforcement from 2011 |
| 4.1 ¶3 | Germany's share "hardly changed" | See 3.2 ¶2 | WRONG after correction | Revise |
| 4.1 ¶3 | other chemical hazards drove the post-2022 rise (Table 1) | All alerts +2,522 and chemical +1,722, 2022 → 2025 | OK | – |
| 4.1 ¶4 | Mathiason; Davis; Hedberg 2020 | Brief 3.2, 1.2, 3.3 | OK | – |
| 4.2 | "half contain more than 14 mg/kg …, a quarter about 29 mg/kg or more" | median 14.3; Q3 28.75 | OK | Corrected Q3 30.2 |
| 4.2 | "parts that fail are mainly insoles and linings" | Holds in the risk text (insole 83 ≫ lining 28 > upper 12), but the numbers in 3.1 are wrong | OK (direction) | Use the risk-text counts |
| 4.2 | EU share 9 → 21% "is a reminder that Cr(VI) is a matter of tanning chemistry and storage, not of where an article was assembled" | Origin share says nothing about chemistry; could reflect where surveillance looks | UNSUPPORTED | Soften or remove |
| 4.3 | no denominator published (Elsner & Schliemann) | Brief 4.5 | OK | – |
| 4.3 | "The Danish series is the only one that spans the regulation" | The brief does not establish this (no exhaustive search) | UNSUPPORTED (minor) | "the only one I found" |
| 4.4 | "a sample was checked by hand in the number audit" | Now done: extraction 1/60; classification found the systematic error | OK once reported | Report the error rates and the 2010 correction |
| 5 | "chromium allergy is as common as it was" | One Danish clinic | MINOR | "in the one Danish series" |
| References | Alinaghi et al. (2019) listed | Never cited in the text; finds a decline 2002–2017 that began before 2015 | MINOR / omission | Cite it (as counter-evidence) or remove it |
| Table 1 | all rows and totals | B_series; totals 617/344/273/48,287/15,633 | OK as computed | Corrected 2010 row: 1, 0, 1, 1, 0.5, 0.23; 2013: 76/63; totals 593/345/248 |
| Table 2 | Safety Gate rows 39.7/3.0; 15.1/0.57; 17.5 (n = 275)/13.0 (n = 336); survey and patch-test rows | analysis, brief | OK | Corrected 39.9; 15.2; 17.6 (n = 251) |
| Table 3 | all rows | sensitivity.json | OK | MINOR rounding: "17.6" for 17.65 and "20.9" for 20.95 (half-up would give 17.7, 21.0); regenerate after the correction |
| Table 3 | Poisson row identical to main | NB α = 0 for the main model | MINOR | Explain (M7) |
| Fig 1 | bars and line vs Table 1 | Values match; no overlaps; 2026 open circle labelled | OK / WRONG content | The 2010 orange bar (26) is the textile batch; redraw. The dashed line at 1 May 2015 cuts through the 2015 bar (whole-year bar, mixed period); acceptable |
| Fig 2 | points, medians ≥ 5, 3 mg/kg line | Matches code and caption. Two horizontal clusters in 2010 (13 × 19.2, 12 × 14.1) are the duplicated textile batch; the 2010 median (19.2) rests on them; the 1857/10 point (120) should be 60. Jitter puts some 2015 "after" (blue) points left of the 1 May line | WRONG content / MINOR | Redraw after the correction; optionally jitter 2015 by date |
| Fig 3 | before/after shares | Matches E. Before n = 277 includes the textiles; garments-before 9% → 2% after correction; labels fit; legend capitalisation differs between panels | WRONG content / MINOR | Redraw; capitalise legend labels consistently |

## 2. Concentration extraction validation

**Random sample.** 60 in-scope notifications (`alerts[alerts.scope].sample(60, random_state=7)`). Each was read in full (legal + risk_desc) and checked for whether conc_max is the highest Cr(VI) value in mg/kg.

- Correct: 59/60.
- **Error 1: A12/0674/14 (girls' sandals).** The text reads "measured values: Model 1/: 10.3 mg/kg; Model 2/: 17.8 mg/kg". conc_max = 10.3; the correct value is 17.8. Cause: `sentences()` splits at "; " followed by a capital letter ("Model 2"), and the new fragment has no chromium word, so it is skipped.
- **Error rate: 1/60 = 1.7% (95% CI 0.04–8.9%).**

**Full-scope scans (beyond the sample).**
- *Missed higher value.* Every in-scope notification whose legal/risk text holds a larger mg/kg number than conc_max was reviewed. Of 6 hits, only A12/0674/14 is a real error. The other 5 are correctly excluded values for other substances (azo amines, DMF, Disperse Orange 37, a 30 mg/kg limit).
- *All 59 multi-value notifications reviewed.* **Error 2: 1857/10 (men's Oxford shoes, France, 2010).** The text reads "high levels of extractible chrome (120 mg/kg) and in particular of chrome VI (60 mg/kg)". conc_max = 120 is total extractable chromium; the correct value is 60. Range and list cases (e.g. "17.5 – 35.9 – 29.3") give the correct maximum; some drop the first number, which affects conc_min only.
- **conc_max ≥ 150 (6 notifications): all correct.** 0513/05: 299 (179; 255; 299 listed, limit 3 skipped). A12/1829/12: 225. A12/0048/13: 414.3, ladies' gloves (the reported maximum). A12/0855/13: 170. A12/1865/17: 270. A12/1597/18: 285.
- **conc_max == 3 (6 notifications): all correct.** Each reports a measured value of 3 or 3.0 mg/kg: A12/0383/15, A12/1240/15, A12/1669/19, A12/1943/19, A12/01853/21, A12/01320/23.
- **Percent conversions (2): correct.** A12/01372/23: 0.00109% → 10.9. SR/02248/26: 0.013% → 130.
- **g/kg (2): handled as described.** A12/1113/13 has no value; A12/1000/15 → 10.6.

**Overall in-scope extraction errors found: 2 of 611 values (0.3%).** Neither changes any reported median, IQR or rounded percentage materially.

## 3. Classification validation

**In-scope sample.** 30 notifications (`sample(30, random_state=11)`). 29 are genuine Cr(VI) findings in leather or leather-type articles. That includes the 4 identified by product type only (IN7 A12/0573/16, IN15 A12/0592/14, IN20 A12/0586/14, IN25 A12/0656/15), which are shoes whose insole or lining is plausibly leather.
- **Wrong: IN9 1658/10**, "Black imitation leather jacket" from the Italian Oeko-Tex textile batch.
- **Error rate: 1/30 = 3.3% (95% CI 0.08–17.2%).**

**Systematic error found from that case.** 36 Italian notifications from 2010 share one Oeko-Tex risk text, written for textile clothing. 25 copies carry a longer version that mentions "for leather goods", and that alone puts them in scope. The products are jumpers, T-shirts, tracksuits, velvet trousers, a blouse, dresses, children's suits, and two imitation-leather items. None is a leather article.
- **False positives: 25/617 = 4.1% (2.6–5.9%).**
- Refs: 1618–1630/10, 1656–1667/10 (excluding 1665/10), 1733/10.
- All other in-scope items whose leather word appears only in the risk/legal text were reviewed. None is a false positive besides this batch (A12/0489/13 says Cr(VI) is in the leather lining and insole).

**Out-of-scope Cr(VI) sample.** 30 notifications (crvi True, scope False; `sample(30, random_state=11)`), mostly toys, costumes, cosmetics, cement and the remaining Italian textiles.
- **Should be in scope: OUT20 A12/1217/13 (Germany, 2013)**, "Leather necklace", 62.5 mg/kg Cr(VI) "in the leather component". It was excluded only because its category is JEWELLERY, yet it is a leather article in skin contact under REACH entry 47. A check of all 58 excluded notifications found it is the only one.
- **Error rate: 1/30 = 3.3% (0.08–17.2%); 1/58 of all exclusions.**

**Leather-mentioning, chromium_any True, crvi False (all 4).**
- 0333/09 is total "chrome" (74/54 mg/kg) plus DMF in shoes, not Cr(VI). Correctly out.
- A11/0069/17, A12/03377/24 and SR/03349/25 are chairs with chrome frames and (artificial) leather. Correctly out.
- None should be in scope.

**Other classification notes.**
- Product type: about 10 of 73 "bags and small leather goods" are garments or body-worn items, because the bag regex runs first and matches "collar", "pouch", "strap", "belt" and "watch(ing)". Examples: A12/0659/13 leather jacket; lederhosen A12/1366/16, A12/0281/19, A12/1811/19, A12/1943/19; A12/00076/21 leather bra; A12/01295/21 jockstrap; 4 of the textile batch.
- The children flag was checked; matched words are children/baby/babies/girls/boys only. OK.
- Component flags: see 3.1 in the table (description text, not the part that failed).

## 4. Effect of the corrections (rerun on a scratch copy)

The rerun removed the 25 textiles, added A12/1217/13, and fixed the two extraction errors.

| Result | Paper | Corrected |
|---|---|---|
| n (with value) | 617 (611) | 593 (587) |
| Trend 2016–2025 per 1,000 alerts | −26.1% (−29.2 to −22.8) | unchanged |
| 2013–15 vs 2023–25 per 1,000 | 39.7 vs 3.0, 13-fold | 39.9 vs 3.0, 13.3-fold |
| 2010 notifications | 26 (Italy 25) | 1 (France) |
| Trend 2010–2014 | +44% (27–62%) | +95% (63–132%) |
| Germany share before / after | 58.8% (52.7–64.7) / 52.9% | 64.9% (58.6–70.8) / 52.9% (47.5–58.3) |
| Other countries per year 2010–14 → 2016–25 | 19.4 → 12.8 | 14.4 → 12.8 |
| Footwear / garments before | 66% / 9% | 73% / 2% |
| China / EU origin before | 53% / 9% | 58% / 10% |
| Median conc before → after, p | 17.5 → 13.0, 0.0002 | 17.6 → 13.0, 0.0003 |
| > 10× limit, all / before | 24.1% / 31.6% | 25.2% / 35.1% |
| OLS trend in concentration | −5.4%/yr | −6.0%/yr (−7.8 to −4.2) |
| Lowest-value sensitivity | 14.4 → 13.0, p = 0.55 | 16.0 → 13.0, p = 0.005 |
| Germany excluded, concentration | 14.1 → 12.8, p = 0.52 | 10.1 → 12.8, p = 0.93 |
| Measures (vol / comp / both / none) | 51.7 / 33.4 / 5.8 / 9.1% | 54.0 / 30.5 / 6.1 / 9.4% |

The paper's main conclusion still holds: a large post-2015 fall in notifications against survey and allergy data that did not fall much. The concentration decline now depends only on Germany, not on the choice of highest or lowest value.
