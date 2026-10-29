# Number audit, round 2: "Fewer alerts, same allergy: hexavalent chromium in EU leather goods, 2005–2026"

Auditor: independent check (did not write the paper). Date: 2026-10-20.
Scope: the revised manuscript.md against the regenerated results/ (alerts.csv, analysis.json, sensitivity.json, build_summary.json, tables.md), code/, the four PNGs in figures/, and the two earlier audits (number_audit.md, citation_audit.md). No file in the package was edited. The only file written is this report.

## 0. Summary

- **Reproducibility: OK.** I rebuilt from raw/ in a scratch copy (build → analysis → sensitivity → tables). The rebuild gave byte-identical alerts.csv, analysis.json, sensitivity.json, build_summary.json and tables.md. Tables 1–3 in the manuscript match tables.md line for line.
- **Numbers: all correct.** Every number, percentage, CI, p-value, count and date in the abstract, text, Tables 1–3 and the social summary matches the result files and is correctly rounded. The derived checks hold:
  - 39.85/3.00 = 13.3-fold.
  - −26.05% (−29.79 to −22.11) gives "26% (22–30%)".
  - Six notifications in 2005–2010 (2+0+0+1+2+1).
  - German notifications: 11 in 2011 and 63 in 2013.
  - Exclusions: 82 = 38 + 29 + (8 + 1) + 5 + 1, and 675 − 593 = 82.
- **Earlier fixes: almost all applied.** That covers the textile batch, the necklace, both extraction errors, the component counts, the Italy narrative, Germany's share, the quasi-Poisson model, the citation rewordings and the reference corrections. A few optional or minor items were not applied (Section 2).
- **New errors, all small:**
  1. The graphical abstract still says "617 notifications". The number is hard-coded in code/graphical_abstract.py.
  2. The Figure 2 caption says the points are "jittered within year", but the code plots them at the exact publication date.
  3. §2.2 says the 38 excluded textile garments "did not mention leather". 26 of them do: 25 only in the background sentence, plus a synthetic-leather bikini. Of the 25, 2 also say imitation leather in the product text.
  4. The garments regex `coat` matches "coated". As a result, A12/01220/22 "Leather belt" is classed as a garment. This changes four percentages in §3.1/§3.3 by 0.1–0.3 points.

## 1. Claim-by-claim table

Verdicts: OK / WRONG / MINOR (wording or precision; no number changes) / UNVERIFIED.

| Location | Claim | Check | Verdict | Fix |
|---|---|---|---|---|
| Social summary | "fell 13-fold after 2015. Allergy rates did not." (92 characters) | 39.85 (2013–15) / 3.00 (2023–25) = 13.3. The base includes 2013–14. 2015 alone is 39.2, so "after 2015" is defensible | MINOR (earlier fix not applied) | Optional: "fell 13-fold from 2013–15 to 2023–25" |
| Abstract | 593 notifications, 2005–2026 | n_scope 593 | OK | – |
| Abstract | rose from 2011, peaked 2014 | Table 1: 2010 = 1, 2011 = 19; peak 2014 = 97 (42.7/1,000) | OK | – |
| Abstract | fell 26% a year, 2016–2025 (95% CI 22–30%) | −26.05 (−29.79 to −22.11) | OK | – |
| Abstract | 40 per 1,000 (2013–15) to 3 (2023–25), 13-fold | 39.85, 3.00, 13.3 | OK | – |
| Abstract | Germany sent 58% | 345/593 = 58.2% | OK | – |
| Abstract | share made in the EU doubled | 9.9% → 20.6% (×2.08) | OK | – |
| Abstract | median 14 mg/kg; one in four > 10× limit | 14.3; 148/587 = 25.2% | OK | – |
| Abstract | concentrations fell after 2015 in German notifications only | DE 21.2 → 13.5 (p = 6e-6); others 10.1 → 12.8 (p = 0.93) | OK | – |
| Abstract | surveys 23–35% → 11–13%; allergy about 2% | 23/32/35%; 13.3/10.6/12%; 2.3/1.9/2.1% | OK | – |
| §1 | 80–90% of tanneries; > 90% of production; 80 °C, UV, alkaline, fatliquors, dry storage | Citation audit #1–3 | OK | Optional: "certain fatty acids (from fatliquors)" |
| §1 | 24% (1989–94) → 46% (1995–2007); cement 13% → 3% | Citation audit #5 fix applied | OK | – |
| §1 | leather shoes most frequent exposure (Kursawe Larsen 2026) | Citation audit #6 fix applied | OK | – |
| §1 | RAC, about 80% effective (recital 7); 5,760–15,840 a year beyond the German ban; review under recital 8 | Citation audit #11, #12 fixes applied | OK | – |
| §1 | 4,830 patients, 2016–2024, 2.1%, not significantly different | Citation audit #13 | OK | – |
| §1 | Alinaghi 2019: decline 2002–2017 that began before the regulation | Citation audit, Part B | OK | – |
| §1 | notification "expected", some never notified (2019/417; Wijnhoven) | Citation audit #15 fix applied | OK | – |
| §1 | Cr(VI) one of three substance groups, 2015–2023 (EEA 2024) | Citation audit #16 | OK | – |
| §1 | "no peer-reviewed study"; Pigłowski 2023, 2026 | Citation audit #20, #37 | OK | Pigłowski (2026) title not verified by either audit; the Crossref request was rate-limited (429). Check the title against doi:10.3390/su18136875 |
| §2.1 | 2019/417 s. 3.4.3.3; ceased March 2025; GPSR from Dec 2024; pre-2015 relied on national rules | Number audit and citation audit #21 fixes applied | OK | – |
| §2.1 | 20 Oct 2026; three searches; 1,089 distinct | build_summary n_notifications 1,089 | OK | – |
| §2.2 | Cr(VI) forms; 675 | n_crvi 675 | OK | – |
| §2.2 | leather if mentioned and not described only as imitation; background sentences ignored | Code: count of "leather" > count of imitation phrases, in product text plus non-BOILER risk sentences (BOILER = clinical stud / sensitive subjects / Oeko-Tex) | OK / MINOR | Optional: state the counting rule |
| §2.2 | article rule on product name; list of article words | ARTICLE regex applied to the name (description only if there is no name), outside the excluded categories, and only if no leather mention at all. List matches | OK | – |
| §2.2 | jewellery "unless the product text named real leather" | Code tests `leather` on product text plus risk text, not product text alone. Only one Cr(VI) jewellery notification exists (A12/1217/13, "Leather necklace"), so there is no effect | MINOR | Optional: "unless the notification named real leather" |
| §2.2 | 518 name leather + 75 by product name | n_scope_leather_word 518; 593 − 518 = 75 (72 footwear, 3 gloves) | OK | – |
| §2.2 | 82 excluded = 38 textile garments that did not mention leather, 29 toys, 9 cements and other construction products (one under "other"), 5 cosmetics, 1 tattoo ink | Categories: CLOTHING_TEXTILES 38, TOYS 29, CONSTRUCTION 8 (6 cement, tile adhesive, sealing slurry) + OTHER 1 (cement), COSMETICS 5, CHEMICAL_PRODUCTS 1 (tattoo ink, SR/00211/26). Sum 82 ✓. But 26 of the 38 textiles contain "leather": the 25 Italian Oeko-Tex items (in the background sentence; 1658/10 and 1660/10 also say imitation leather in the product text) and the A12/0532/13 bikini (synthetic leather) | WRONG (wording) | "38 textile garments that were not leather (25 of them mention leather only in a generic background sentence; three describe imitation or synthetic leather)", or simply "38 textile garments not made of leather" |
| §2.2 | product types; child flag; component flags from the statement of the risk | Code: garments now checked before bags (earlier fix applied). Components come from legal provision + risk description. In 2011–2017 the risk statement is stored in the legal-provision field (risk_desc empty), so this is right in substance. New error: the garments pattern `coat` matches "coated", so A12/01220/22 "Black, coated leather belt" → garments | WRONG (1 item) | Use `\bcoats?\b`. Recount: bags 62 (10.5%), garments 50 (8.4%); after the limit bags 16.5%, garments 12.9% (before unchanged). Fig 3 labels are unchanged (16%, 13%) |
| §2.3 | extraction rules: uncertainty, ranges, mg/k, ppm, % < 1%, limit words, total/extractable chromium skipped, other-substance filter, product-text fallback, next-sentence fallback | All present in extract(), values_in(), skip() (TOTALCR) and chromium_part(). The fallback order matches (`extract(risktext) or extract(text)`; next sentence only if no chromium sentence gave a value). Not stated: values ≥ 100,000 dropped. "Statement of the risk" in code = legal + risk fields | OK / MINOR | Optional: add "values ≥ 100,000 mg/kg discarded" |
| §2.3 | 587 of 593 with a value; two g/kg, one with no other value | n_scope_with_conc 587; A12/1113/13 NaN; A12/1000/15 → 10.6 | OK | – |
| §2.3 | two extraction errors corrected | A12/0674/14 now 17.8 (10.3; 17.8); 1857/10 now 60 (total chrome 120 skipped). A rescan of all in-scope texts for a larger mg/kg value than conc_max found 6 hits; each is correctly excluded (1857/10 total chrome; DMF, azo, Disperse Orange) | OK | – |
| §2.4 | quasi-Poisson, Pearson dispersion 1.43 | trend(): Poisson SE × √max(1, χ²/df); main dispersion 1.433 | OK | – |
| §2.4 | bootstrap 10,000, fixed seed; MW; GM ratio; OLS log10 (robust); median regression | B = 10000, seed 20261020; HC1; quantreg q = 0.5 | OK | Optional: give the seed |
| §2.4 | shares compared between periods carry Clopper–Pearson intervals | Computed for all (analysis.json E), reported for some (footwear, EU, Germany) | MINOR | Optional: "selected shares are given with…" |
| §2.4 ¶2 | sensitivity list | All 11 rows in Table 3 present in sensitivity.json / analysis.json | OK | – |
| §3.1 | 12 May 2005 – 13 Aug 2026 | A.first / A.last | OK | – |
| §3.1 | footwear 307 (51.8%), gloves 171 (28.8%), bags 61 (10.3%), garments 51 (8.6%) | ptype; 3 "other" not mentioned | OK as computed / see §2.2 | After the `coat` fix: bags 62 (10.5%), garments 50 (8.4%) |
| §3.1 | bag examples (bags, wallets, belts, straps, bracelets, dog leads) | Present (5 dog leads, bracelets, a necklace, phone cases) | OK | – |
| §3.1 | children 95 (16.0%) | 95, 16.02% | OK | – |
| §3.1 | insole 83, lining 28, upper 12 | components | OK | – |
| §3.1 | 42 known countries of origin | n_origins_known 42 (Hong Kong and Taiwan counted separately) | MINOR (earlier fix applied differently) | Optional: "countries or territories" |
| §3.1 | China 271 (45.7%), India 62 (10.5%), Pakistan 47 (7.9%), EU 95 (16.0%), unknown 43 (7.3%) | origin_top, origin_eu | OK | – |
| §3.1 | 19 notifiers; Germany 345 (58.2%; 54.1–62.2); Spain 89 (15.0%); France 29; Estonia 28; Finland 27 | notifier_top; de_share_ci | OK | – |
| §3.1 | measures 320 (54.0%), 181 (30.5%), 36 (6.1%), not stated 56 (9.4%) | measures; 593 − 537 = 56 | OK | – |
| §3.2 | six notifications in six years before 2011 | 2005–2010: 2, 0, 0, 1, 2, 1 | OK | – |
| §3.2 | first full year after the German ban; Germany 11 in 2011, 63 in 2013 | Ban in force 14 Aug 2010; n_de 2011 = 11, 2013 = 63 | OK | – |
| §3.2 | +80% a year, 2010–2014 (33–144%) | before_all 80.17 (33.13–143.83); dispersion 6.5 | OK | – |
| §3.2 | peak 2014: 97, 42.7 per 1,000 | B_peak | OK | – |
| §3.2 | −26.1% (22.1–29.8); chem −32.9% (27.5–38.0); raw −20.3% (16.0–24.4) | B_trend; S5 raw | OK | – |
| §3.2 | 39.9 vs 3.0, 13-fold; 15.2% → 0.57% | B_peak3, B_recent | OK | – |
| §3.2 | 2016–2022: −24.2% (18.6–29.5) | S5 all_2016_2022 | OK | – |
| §3.2 ¶3 | Germany 29.6 → 16.0 a year; others 14.4 → 12.8 | C_other_per_year | OK | – |
| §3.2 ¶3 | both series −25 to −27% a year (Table 3) | DE only −25.1; excl. DE −27.3 | OK | – |
| §3.2 ¶3 | ten first-time notifiers after May 2015 (list) | C_first_after | OK | – |
| §3.2 ¶3 | Germany 64.9% (58.6–70.8), Dec 2010 – Apr 2015, → 52.9% (47.5–58.3) | C_notifiers; before first_day 2010-12-16 | OK | – |
| §3.3 | footwear 72.7% (66.8–78.1) → 36.2% (31.1–41.5); gloves 22.1 → 33.8; bags 2.4 → 16.2; garments 2.4 → 13.2 | E.ptype | OK as computed | After the `coat` fix: bags 2.4 → 16.5; garments 2.4 → 12.9 |
| §3.3 | China 58.1 → 36.5; South Asia 11.9 → 24.1; EU 9.9% (6.5–14.2) → 20.6% (16.4–25.3); children 18.6 → 14.1 | E.origin, E.child | OK | – |
| §3.4 | every highest value ≥ 3; six exactly 3 | below_limit 0; at_limit 6 | OK | – |
| §3.4 | median 14.3 (13.0–15.6); IQR 7.9–30.2; max 414 in ladies' gloves | D_conc; A12/0048/13 "Ladies' gloves" 414.3 | OK | – |
| §3.4 | almost five times the limit | 14.3/3 = 4.8 | OK | – |
| §3.4 | 148 (25.2%) > 10×; about one in six, 91 (15.5%) ≤ 2× | gt_10x, le_2x | OK | – |
| §3.4 ¶2 | 17.6 → 13.0, p = 0.0003; GM −26%; > 10× 35.1% → 17.9% | MW 0.000336; GM ratio 0.739; 35.06 / 17.86 | OK | – |
| §3.4 ¶2 | OLS −6.0% (−7.8 to −4.2); median regression −5.1% (−8.1 to −1.9) | trend_2010_2025 | OK | – |
| §3.4 ¶2 | lowest value 16.0 → 13.0, p = 0.007 | S2 | OK | – |
| §3.4 ¶2 | DE 21.2 → 13.5; others 10.1 → 12.8, p = 0.93 | S4 | OK | – |
| §3.4 ¶2 | count decline held in every sensitivity analysis | Every Table 3 trend CI is below 0 | OK | – |
| §3.5 | 23–35%; 467 → 13.3%; 10 of 94 samples from 74 products (10.6%), not all treated as violations; 12% of 99; factor 2–3; factor 13; Gentofte 2.3 / 1.9 / 2.1, p = 0.65 / 0.41 | Citation audit #22–26 (fixes applied) | OK | – |
| §4.1 ¶1 | "fell in most years" | 2019/20 flat, 2023 up | OK | – |
| §4.1 ¶2 | one in eight, "one to six years after" | Surveys 2016, 2018 (published 2019), 2020–21 | OK | – |
| §4.1 ¶2 | Alinaghi 2021 burden; Alinaghi 2019 earlier decline | Citation audit #27 fix applied | OK | – |
| §4.1 ¶3 | hedged explanation; Wijnhoven "between countries"; EEA "influenced by"; German enforcement from 2011; post-2022 rise from other chemical hazards; Germany more than half before and after | 64.9% / 52.9%; chemical alerts 774 → 2,496 (2022 → 2025) | OK | – |
| §4.1 ¶4 | Mathiason; Davis 2022; Hedberg 2020 | Citation audit #30–32 | OK | – |
| §4.2 | half > 14 mg/kg; a quarter about 30 or more; insole most often; EU share about 10% → 21%, "not only an import problem" | median 14.3, Q3 30.2; 83 ≫ 28 > 12; 9.9 → 20.6 | OK | – |
| §4.3 | denominator not published (Elsner & Schliemann); "the only one I found"; recital 8; Hedberg / Davis; Alinaghi on those already sensitised | Citation audit #34, #35 fixes applied | OK | – |
| §4.4 | main trend unchanged when only leather-named alerts are used; hand checks 30 + 30, one error each; batch of 25 corrected | S1 −26.8%; number audit Section 3 | OK | – |
| §5 | 13-fold fall; one in eight; "chromium allergy is as common as it was before the limit" | The allergy result is from one Danish clinic | MINOR (earlier fix not applied) | "…as common as it was before the limit in the one Danish series that spans it" |
| Table 1 | all rows and totals | B_series; totals 593/345/248/48,287/15,633; identical to tables.md | OK | – |
| Table 2 | 39.9/3.0; 15.2/0.57; 17.6 (n = 251)/13.0 (n = 336); survey and patch-test rows | analysis; citation audit | OK | – |
| Table 3 | all 12 rows | sensitivity.json, analysis.json; rounding now half-up (17.65 → 17.7, 17.45 → 17.5) | OK | – |
| Table 3 | NB row identical to plain Poisson | MoM α = −0.002, floored to 1e-8, so NB = Poisson | MINOR (earlier M7 only partly applied) | Add to the caption or row: "(dispersion estimated at 0; identical to Poisson)" |
| Fig 1 | bars and line vs Table 1; 2026 open circle; dashed line | All 22 years match (e.g. 2010 = 1, 2013 = 63 + 13, 2014 = 58 + 39). No overlaps. The legend and the "EU limit applies" label are clear of the bars | OK | Optional: caption "(A) … by notifier (Germany or other countries)" |
| Fig 2 | caption: "points jittered within year" | figures.py plots each point at its exact publication date (x = year + day/365.25); there is no jitter. The 2010 point is now 60 (1857/10), the 2005 point 299 and the maximum 414 (2013). Medians are shown for years with n ≥ 5 (2011–2026), plotted mid-year. Orange and blue points sit on the correct side of 1 May 2015. The "Limit 3 mg/kg" label starts at x = 2004.6, left of the y-axis (xlim 2005), so its first letter crosses the spine | WRONG (caption) / MINOR (overlap) | Caption: "points placed at the date of publication". Move the label to x ≥ 2005.2 |
| Fig 3 | before n = 253, after n = 340; segment labels | 73/22 → 36/34/16/13; China 58/12/10/15 → 36/24/21/10/9; legends now consistently capitalised | OK | After the `coat` fix the labels stay 16% and 13%; redraw anyway. The "12%" and "10%" labels in panel B (before) are tight but legible |
| Graphical abstract | footer "EU Safety Gate, 617 notifications 2005–2026" | Hard-coded string in graphical_abstract.py; the correct n is 593. Chart values (2010 = 0.5), "40 → 3 per 1,000", "13x fewer", "23–35% → 11–13%" and "2.3% → 2.1%" are all correct | WRONG | Change to 593 (better: read A['A']['n']) and regenerate |

## 2. Were the earlier fixes applied?

### 2a. Number audit (number_audit.md)

| # | Earlier fix | Status | Note |
|---|---|---|---|
| A1 | Exclude the 25 Italian textile notifications (n = 593) | Applied | BOILER sentences are ignored for the leather test; 0 Italian 2010 items are in scope |
| A2 | Bring the leather necklace A12/1217/13 into scope | Applied | JEWELLERY in scope if `leather` |
| A3 | Extraction: A12/0674/14 → 17.8 | Applied | The sentence splitter now splits only after "." |
| A4 | Extraction: 1857/10 → 60 | Applied | TOTALCR skip rule |
| A5 | Bag regex matched garments | Applied differently | Garments are now checked first. New side effect: `coat` matches "coated" (1 belt) |
| A6 | Component counts from the risk text (83/28/12) | Applied | – |
| A7 | 42 countries (not 43) | Applied differently | "42 known countries of origin"; "countries or territories" not used |
| A8 | Social summary: name the base years | Not applied | Minor; "after 2015" is defensible |
| A9 | Abstract: name the base of the 13-fold drop | Applied | – |
| A10 | "rose from 2011" | Applied | – |
| A11 | Reword "a fall in concentrations not robust" | Applied | "fell after 2015 in German notifications only" |
| A12 | §2.1: GPSR note; qualify pre-2015 | Applied | – |
| A13 | §2.2: describe the leather counting rule | Not applied (minor) | The boilerplate trigger is now handled in code and described |
| A14 | §2.2: complete the article list | Applied | – |
| A15 | §2.2: "construction products (mainly cement)"; exclusion breakdown | Applied | But the textile wording is wrong (Section 1) |
| A16 | §2.3: state the unstated extraction rules | Mostly applied | Product-text fallback, next sentence, mg/k and ppm are stated; the ≥ 100,000 drop is not |
| A17 | §2.4: NB α = 0 → state it or use quasi-Poisson | Applied differently | The main model is now quasi-Poisson; the NB row in Table 3 is still unexplained |
| A18 | §2.4: give the bootstrap seed | Not applied | Optional |
| A19 | §2.4: Clopper–Pearson statement | Partly applied | CIs are given for selected shares |
| A20 | §3.1 corrected counts and percentages | Applied | – |
| A21 | §3.2: delete "began in 2010 with Italy"; recompute 2010–2014 growth | Applied | +80% (33–144%), quasi-Poisson |
| A22 | §3.2: "the EU limit widened participation" (causal) | Applied | Now a statement of timing |
| A23 | §3.2/§4.1: Germany's share fell about 12 points | Applied | – |
| A24 | §3.3 corrected shares; "roughly doubled" | Applied | "doubled" (×2.08) is fine |
| A25 | §3.4: "Every highest value…" | Applied | – |
| A26 | §3.4: drop the lowest-value leg of the fragility argument | Applied | – |
| A27 | §4.1: "fell in most years" | Applied | – |
| A28 | §4.1: "one to six years after" | Applied | – |
| A29 | §4.1: hedge "likeliest explanation" | Applied | – |
| A30 | §4.2: Q3 30; soften the EU-origin chemistry claim | Applied | – |
| A31 | §4.3: "the only one I found" | Applied | – |
| A32 | §4.4: report the hand-check error rates | Applied | – |
| A33 | §5: "in the one Danish series" | Not applied | Minor |
| A34 | Cite Alinaghi 2019 or remove it | Applied (cited) | – |
| A35 | Table 1 corrected 2010 row and totals | Applied | – |
| A36 | Table 3 rounding (half-up) | Applied | – |
| A37 | Figures 1–3 redrawn after the correction | Applied | Fig 1: 2010 = 1; Fig 2: no 2010 textile clusters, 1857/10 at 60, 2015 points by date; Fig 3: garments before 2%, consistent legends. The graphical abstract footer was not updated |
| A38 | Intro fatliquor citation | Not applied | Optional |

### 2b. Citation audit (citation_audit.md)

| # | Earlier fix | Status | Note |
|---|---|---|---|
| 3 | "fatty acids (from fatliquors)" | Not applied | Optional |
| 5 | Thyssen: 24% (1989–94) → 46% (1995–2007); cement 13% → 3% | Applied | – |
| 6 | Shoes: cite Kursawe Larsen 2026 | Applied | – |
| 7 | Split Bregnbak / Alinaghi findings | Not applied | Optional |
| 8 | "not merely temporary" contact | Not applied | Optional |
| 10 | "determination limit" | Not applied | Optional ("quantification limit" kept) |
| 11 | 80% attributed to the RAC opinion, recital 7; recital 8 | Applied | The dossier-submitter expert-judgement note was not added (optional) |
| 12 | 5,760–15,840, net of the German ban | Applied | The mean of 10,800 was not added (optional) |
| 13 | Kursawe Larsen; adults | Applied (name) | "Adults" not added (optional) |
| 15 | "expected to notify"; cite 2019/417 and Wijnhoven | Applied | – |
| 16 | "substance groups", 2015–2023 | Applied | – |
| 20 | Add Pigłowski 2026 | Applied | Title not verified |
| 21 | 2019/417 no longer in force; GPSR | Applied | – |
| 23 | Danish 2019: 10 of 94 samples from 74 products, uncertainty; Table 2 label | Applied differently | Table 2 says "Denmark, 2019 report" rather than "2018, published 2019"; acceptable |
| 24 | ECHA 468 / 13.2% footnote | Not applied | Optional |
| 26 | "did not fall significantly" | Applied | – |
| 27 | Alinaghi 2021 measures burden, not prevalence | Applied | – |
| 28 | Drop "and over time" | Applied | – |
| 29 | EEA "influenced by" | Applied | – |
| 35 | Alinaghi: revision for those already sensitised; recital 8 | Applied | – |
| 36 | "11–13%" vs "10–13%" | Kept "11–13%" | Acceptable (counts exceedances, not violations) |
| 37 | "no peer-reviewed study" | Applied | Note on trade tallies not added (optional) |
| Ref | Alinaghi 2019 cited | Applied | – |
| Ref | Bedarfsgegenständeverordnung issue date | Applied | – |
| Ref | Danish EPA 2012 URL | Applied | – |
| Ref | Danish EPA 2019 subtitle, editors, ISBN, URL | Partly applied | URL only |
| Ref | Davis year 2022 | Applied | In text and in the reference |
| Ref | ECHA 2018 URL | Applied | – |
| Ref | EEA (2024) and correct title | Applied | – |
| Ref | Elsner & Schliemann title | Applied | – |
| Ref | Hedberg 2020 journal and article number | Applied | – |
| Ref | Köhler title | Applied | – |
| Ref | Kursawe Larsen surname | Applied | In all in-text uses and Table 2 |
| Ref | RAC/SEAC date and URL | Applied | – |
| Ref | Wijnhoven URL | Applied | – |
| Ref | Kawakami "(in Japanese)", PMID | Not applied | Optional |

## 3. Methods text vs code

- **build.py classification.**
  - Matches §2.2: the Cr(VI) regex, the BOILER exclusion of background sentences for the leather test, the imitation-leather count rule, ARTICLE on the product name, the excluded categories, and the JEWELLERY rule.
  - Small wording gap: the jewellery rule uses product and risk text, not product text alone. It has no effect.
  - Component flags come from the legal-provision and risk-description fields. For 2011–2017 the risk statement lives in the legal-provision field, so "statement of the risk" is right in substance.
- **Extraction.**
  - Matches §2.3, including the uncertainty strip, ranges and lists, mg/k, ppm, conversion of percentages below 1%, the limit-word skip, the total/extractable chromium skip (TOTALCR), the other-substance filter, the product-text fallback and the next-sentence fallback.
  - Not stated: values ≥ 100,000 are dropped.
- **analysis.py.**
  - Quasi-Poisson: Poisson point estimate, SE × √(Pearson χ²/df) when > 1; main dispersion 1.43. Matches §2.4.
  - Periods split at 2015-05-01 by publication date; trend windows 2016–2025 and 2010–2014; bootstrap B = 10,000 with seed 20261020; Mann–Whitney; GM ratio; OLS with HC1; median regression. All match.
- **sensitivity.py.** NB uses the MoM α, which is negative (−0.002) and floored, so the NB row equals Poisson. This is not explained.

## 4. Figures (PNG inspected)

- **fig1_alerts_per_year.png:** values correct; no overlaps.
- **fig2_concentrations.png:** values correct. The caption wrongly says "jittered", and the limit label crosses the y-axis.
- **fig3_composition.png:** values correct; labels legible.
- **graphical_abstract.png:** footer says 617 (wrong); everything else correct.

## 5. Required fixes remaining

1. **Graphical abstract:** "617 notifications" → "593". In code/graphical_abstract.py, use `A['A']['n']`, then regenerate.
2. **Figure 2 caption:** replace "points jittered within year" with "points placed at the date of publication". Optional in the same pass: move the "Limit 3 mg/kg" label right of the y-axis.
3. **§2.2:** "38 textile garments that did not mention leather" is inaccurate. 26 of them contain the word: 25 in a background sentence, plus a synthetic-leather bikini. Of the 25, 2 also say imitation leather in the product text. Reword, e.g. "38 textile garments not made of leather".
4. **build.py garments pattern:** `coat` → `\bcoats?\b`. This fixes A12/01220/22 (leather belt). Then update:
   - §3.1: bags 61 (10.3%) → 62 (10.5%); garments 51 (8.6%) → 50 (8.4%).
   - §3.3 (after the limit): bags 16.2% → 16.5%; garments 13.2% → 12.9%.
   - Regenerate Fig 3 (labels unchanged).
   - No other number changes: concentrations, trends and Tables 1–3 do not depend on product type.

Recommended (minor; earlier-audit items not applied or new wording points):
- §5: qualify the allergy claim ("in the one Danish series").
- Table 3: note that the NB dispersion was estimated at 0, so the NB row equals Poisson.
- §2.3: say that values ≥ 100,000 mg/kg are discarded.
- §2.4: give the bootstrap seed.
- §3.1: "countries or territories".
- Social summary: name the base years.
- Verify the Pigłowski (2026) title.

## Resolution (20 Oct 2026)
All four required fixes applied (graphical-abstract count read from analysis.json; Figure 2 caption; Section 2.2 wording; `\bcoats?\b` in build.py with Sections 3.1/3.3 and Figure 3 updated). Minor items applied: Section 5 qualified; negative-binomial row labelled; 100,000 mg/kg rule and bootstrap seed stated; "countries or territories"; social summary base years; Figure 2 label position; Figure 1 caption. Pigłowski (2026) title verified against Crossref (doi:10.3390/su18136875) in the browser.
