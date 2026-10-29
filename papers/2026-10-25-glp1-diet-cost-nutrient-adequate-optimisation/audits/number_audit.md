# Number and methods audit: "Less food, nearly the same bill"

Auditor: independent number/methods check, 2026-10-21. No package file was edited. All re-runs were done on a scratch copy (`/tmp/claude-0/-home-claude/e77537ee-4bde-5960-ac22-2794b7601af1/scratchpad/p10audit`). Audit scripts are in its `audit/` folder (s1–s6.py).

## 1. Reproduction

I ran build.py, basket.py, categories.py, results.py and tables.py in sequence on a clean copy, with `__pycache__` removed. The full run takes about 12 s.

- `results.json`, `diets_by_category.csv`, `tables.md`, `categories.csv`, `basket.csv`, `basket.json`, `build.json` and `foods_priced.csv` are **byte-identical** to the package.
- After tables.py runs, the manuscript's Tables section is byte-identical too.
- **Verdict: the pipeline reproduces exactly.**
- Minor: `results.py` has no `if __name__ == '__main__'` guard. Importing it (for example to reuse `realloc`) re-runs the whole analysis and overwrites the results.

## 2. Number check (text, abstract, tables, figures vs results files)

| Location | Claim | Correct value (source) | Verdict | Fix |
|---|---|---|---|---|
| Abstract, §2.1 | 3,448 adults (1,853 F, 1,595 M); ~117 million | 3,448; 116.6 M (sum of w) | OK | – |
| Abstract | $9.12→$5.92 (F), $11.69→$7.60 (M) at 35% | 9.115→5.925; 11.694→7.601 | OK | – |
| Abstract | Adequate at 24% $7.77 / $9.84 = 85% / 84% of current | 7.772/9.115 = 85.3%; 9.842/11.694 = 84.2% | OK | – |
| Abstract | "required moving two-thirds of calories" | 65.5% F, 72.3% M | IMPRECISE | "two-thirds to nearly three-quarters" |
| Abstract, §3.3 | Frontier beyond 32% (F) and 28% (M) | 32.01%, 28.50% (rounds to 28; the label in Fig. 2 also reads 28) | OK, but see §4: driven by the P95 choice | – |
| Abstract | At 35% best achievable costs 91–93% of current | 93.3% F, 91.0% M | OK | – |
| Abstract | "cheapest adequate diets cost $4.50 to $7.60, below the TFP" | 4.54–5.15 F and 6.52–7.59 M, **only at cuts ≤24%**; none exists at 35/39% | IMPRECISE | "$4.54–$7.59 at cuts up to 24%; none at 35%" |
| Abstract | "meets every RDA or AI except vitamins D and E" | Fibre is applied as 14 g/1,000 kcal (e.g. 15.7 g for F at −35%), not the AI of 25/38 g | IMPRECISE | Say "fibre scaled to energy" |
| Abstract | "Appetite suppression saves money only if people keep eating badly." | The closest adequate diet costs less than the current diet at every cut (8.99–8.28 vs 9.12 F; 10.65–9.84 vs 11.69 M). The cheapest adequate diet costs half as much. | ERROR (contradicted by own results) | Delete or rephrase: "saves less if people also eat better" |
| Social summary | "Eating a third less and staying well-nourished saves less than a tenth." | At 35% there is **no** adequate diet. The best achievable diet (still short) saves 6.7% F / 9.0% M. At 24% the adequate diet saves 15–16%. | ERROR | e.g. "A quarter less and adequate saves ~15%" |
| §1 | Grocery prices +31% 2017/18→2025 | factor 1.3115 | OK | – |
| §2.1 | 3,833 / 3,653 food codes | basket.json n_foods | OK | – |
| §2.2 | 3% of grams imputed | 3.17% F, 3.05% M | OK | – |
| §2.2 | CPI factors 1.312 → 1.343; Sept-2026 forecast 2.4% (1.8–3.0) | 1.3115, 1.3430; raw file row month 9 matches | OK | – |
| §2.2 | TFP $58.50/$73.50 wk = $8.36/$10.50 day | arithmetic correct. I did not check the source values. | OK (arith.) | Verify against the FNS June 2026 PDF. TFP 2021 ref URL has typo "fna.usda.gov" → "fns.usda.gov" |
| §2.3 | 155 / 154 categories | 160−5, 159−5 | OK | – |
| §3.1 | 1,724 / 2,227 kcal excl. alcohol | 1,723.9 / 2,227.4 (basket incl. alcohol 1,775 / 2,360) | OK | – |
| §3.1 | "about 10% above the TFP" | 9.0% F, 11.4% M (vs ages 20–50 TFP) | IMPRECISE | "9% and 11%". Note that the sample's mean age is 50.5, and the 51–70 TFP is lower, so the gap is understated |
| §3.1 | Shortfalls (A, C, choline, Ca, Mg, K, fibre both; Fe F; vit K M); excess Na, fat, sat fat | scaled_unmet at r=0 matches | OK | – |
| §3.1 | Vit D 3.9–4.5 µg; vit E 8.0–9.2 mg | 3.87/4.49; 7.96/9.22 (recomputed, not in results files) | OK | Add to results.json |
| §3.2 | At current energy, moved "about half"; $8.99 / $10.65 | 46% / 52%; 8.99 / 10.65 | OK | – |
| §3.2 | 24%: 12% and 11% more than eating less of the same | 12.2%, 10.7% | OK | – |
| §3.2 | Moved 66% and 72% | 65.5%, 72.3% | OK | – |
| §3.2 / Fig 3 | Increases: eggs, nuts/seeds, legumes, reduced-fat milk, oatmeal, cereals; men also chips | Matches. Omitted: bananas (+99 kcal, M) and coffee rising to its P95 (907 g/day, +30 kcal, F; outside the top 7) | IMPRECISE (minor) | Add bananas |
| §3.2 / Fig 3 | Decreases: soft drinks, pizza, cakes, cookies, pasta, chicken; M burgers, burritos | Women also cheese (−31 kcal). For men, "cakes" is not in the top 7 (that slot is egg sandwiches) | IMPRECISE (minor) | Say "cakes (women)"; add cheese |
| §3.2 | Cheapest within habitual $4.54–5.15 F, $6.52–7.59 M at cuts ≤24%; floor $1.65–2.43; 12–18 foods; dry milk, legumes, millet, powdered drink | matches (floor_n 12–18; composition confirmed) | OK | – |
| §3.3, Table 1 | 35%: Mg 91%, LA 98% (F); Mg 90%, LA 88% (M); $8.51 / $10.64 = 93% / 91% | 91.4, 98.5, 89.7, 87.8; 93.3%, 91.0% | OK | – |
| §3.3 | 39%: choline and (F) calcium also short | matches | OK | – |
| §3.3 | With D and E: F <1%, M 9% | 0.54%, 8.8% | OK (Fig. 2 bar label reads "1") | Label "<1" |
| §3.3, Table 2 | "best achievable intake" of D at 24% = 87%; E 82–84%; 35%: 84–85%, 68–74% | Values match `de`, but they come from a **joint minimum of summed relative shortfalls**, not per-nutrient maxima. Vitamin D alone can reach **95.5% F / 93.7% M** at 24% with all other requirements met (E 87.1% / 92.3%). | ERROR (mislabelled) | Call it "intake in the diet with the smallest total shortfall", or report per-nutrient maxima |
| Table 2 ‡ footnote | Other shortfalls (at −35%) "are shown in Table 1" | The de-run shortfalls differ from Table 1: F Mg 90.9 / LA 79.4 vs 91 / 98; M Mg 80.2 / LA 84.7 vs 90 / 88. At **M −24%**, magnesium is also short (97.9%), and that is not mentioned. | ERROR | Report them in Table 2 or correct the footnote |
| §3.4 | 1.2 g/kg adds 87c F, 97c M at 24% | 0.871, 0.969 | OK | – |
| §3.4 | 1.5×P95: F feasible at 35%, $7.76; 2×: M at $11.58 | 7.757; 11.576 (M at 1.5× still short: Mg 96, LA 98) | OK | – |
| §3.4 | 51–70: costs change <25c; at 35% calcium joins women's shortfalls | As coded: Δ −0.01, +0.20, −0.03, −0.05. For women, choline (99.7%) also joins and linoleic acid **drops out**; for men, LA drops out too. **The coded spec is wrong; see §3.** Corrected F35 = $9.65† (+$1.14). | ERROR | Fix the age-51 spec and re-report |
| §3.4 | CPI interval moves costs <0.6% | ±0.586% | OK | – |
| §4.1 | 84–85% at 24%; >90% at 35% | matches | OK | – |
| §4.1 | Cheapest adequate always below TFP | true wherever feasible (max 7.59 vs 10.50; 5.15 vs 8.36; 1.2 g/kg 8.89 vs 10.50) | OK | – |
| Fig 1 legend | "Best achievable, still short of magnesium and linoleic acid" | At 39%, choline (both) and calcium (F) are also short | IMPRECISE | "...short of magnesium, linoleic acid and others" |
| Fig 1 | Points and TFP lines | match the grid | OK | – |
| Fig 2 | Bars | match the frontier (32.0 / 28.5 etc.) | OK | – |
| Fig 3 caption | – | matches diets_by_category | OK | – |

## 3. Code vs Methods

**DRI values (31–50).** All MIN values are correct:

- Vitamins: A 900/700 RAE, C 90/75, D 15, E 15, K 120/90 (AI, correct sex), thiamin 1.2/1.1, riboflavin 1.3/1.1, niacin 16/14, B6 1.3, folate 400 DFE, B12 2.4, choline 550/425 (correct sex).
- Minerals: Ca 1000, P 700, Mg 420/320, Fe 8/18, Zn 11/8, Cu 0.9, Se 55, K 3400/2600 (2019).
- Fatty acids: LA 17/12, ALA 1.6/1.1.

ULs are correct: retinol (preformed) 3000, Ca 2500, Fe 45, Zn 40, Cu 10 mg, Se 400, folic acid 1000, vitamin C 2000, P 4000. Sodium uses the CDRR of 2300. The supplement-only ULs (Mg, niacin, vitamin E) are correctly not applied. Folate as DFE (minimum) with the UL on folic acid is correct. Vitamin A as RAE (minimum) with the UL on retinol is correct.

**Protein.** 0.8 × 70 = 56 g and 0.8 × 57 = 45.6 g, which is correct. The AMDRs (10–35 / 20–35 / 45–65), saturated fat <10%, LA ≥5%, ALA ≥0.6% and fibre 14 g/1,000 kcal are all as stated.

**Niacin.** FNDDS gives preformed niacin, while the RDA is in niacin equivalents (NE). That makes the constraint conservative. I added tryptophan-derived NE (protein × 11/60) and nothing changed, because niacin never binds. OK.

**Issues found:**

1. **Age 51–70 sensitivity is mis-specified (ERROR).** It changes B6, Ca and LA but leaves women's **iron RDA at 18 mg**; for women 51+ it is 8 mg. It also leaves the **calcium UL at 2500**; it is 2000 at 51+. Iron is a binding constraint for women: its dual value at 24% is 21.5, the second largest. Corrected results:

   | | Women −24% | Women −35% | Women frontier | Men |
   |---|---|---|---|---|
   | Coded | $7.76 | $8.71† (choline 99.7, Ca 88.5, Mg 92.8) | 29.6% | unchanged |
   | Corrected | $7.99 | $9.65† (Ca 90.5, Mg 95.2) | 30.2% | unchanged |

   The age-51 men's frontier, not reported, is 32.5%, higher than the main analysis because of the lower LA AI. Related point: the main analysis applies the premenopausal iron RDA of 18 mg to a sample with a weighted mean age of 50.5, so roughly half of the women are 51 or older. This should at least be stated.
2. **The "best achievable % of RDA" for vitamins D and E is mislabelled (ERROR).** The `elastic()` function minimises Σ s_k/req_k jointly over all minima, so the vitamin D and E percentages it reports are a by-product of that trade-off. See the §2 table for the per-nutrient maxima.
3. **The P95 bound includes non-consumers (material and undisclosed).** The `wq()` function is a correct lower weighted quantile. But because non-consumers are included, **47 of 155 (F) and 53 of 154 (M) categories have P95 = 0**, so they are capped at their current mean and can only shrink. These are categories eaten by fewer than 5% of adults on the recall days, including Greek and regular yogurt, cottage cheese and bean dishes (men), and nonfat milk. The P95 is also taken over a 2-day mean rather than usual intake, which widens it for frequently eaten categories and zeroes it for rarely eaten ones.
4. **Fibre scaled to energy (modelling choice; drives results).** With the absolute AI (25/38 g), the men's −24% diet is infeasible (fibre 94%) and the men's frontier falls from 28.5% to 19.8%; the women's frontier falls to 30.5%. The Methods disclose the 14 g/1,000 kcal rule, but the abstract's "every RDA or AI" does not.
5. **Inconsistent exclusions (minor).** The category model keeps nutritional beverages (7208), protein powders (9802), enhanced water (7804) and "not in a category" (9999). The floor LP excludes them, and the adequate diets push 7208 and 9802 to their bounds. Dropping them from the category model moves the frontier to 31.3% / 27.7% and the costs at 24% to $7.73 / $10.03. The Methods say only alcohol and water were excluded from "all diets"; the floor additionally excludes nutrition bars and flavored waters.
6. **CPI (OK).** Inputs match the raw ERS file (2017 −0.2 … 2025 2.3). The factor is idx2025 / mean(idx2017, idx2018) = 1.3115, and × 1.024 = 1.3430, which is correct. The forecast row selected is the September 2026 forecast for 2026.
7. **Composites (OK).** Nutrients and prices are gram-weighted means of the foods eaten in each category; the price uses priced foods only. **Imputation (OK):** unweighted category median of 2026 prices, with a group-median fallback, as described.
8. **QP (OK).** The objective is Σ((y−t)/t)², as the Methods state. The module docstrings in catmodel.py and model.py still describe an L1 objective, and the `elastic()` docstring says cost is minimised in closest mode. Stale; fix.
9. **Elastic (OK).** It matches the text: maxima, AMDR %, LA 5%, ALA 0.6% and energy are hard. The closest diet is then found subject to total shortfall ≤ best × (1+1e-6). The LA shortfall reported is against the gram AI.
10. **Bisection (OK and robust).** 18 iterations on [0, 0.6] give a resolution of 2e-6. The minimum total shortfall rises monotonically in r: F is 0 up to 0.32, then 0.06 at 0.34; M is 0 up to 0.28, then 0.044 at 0.30. HiGHS feasibility status is identical at tolerances 1e-9, 1e-7 and 1e-5 at ±0.2 pp around each frontier. **The frontier is not a solver-tolerance artifact.** Relaxing every minimum by 0.1% / 1% / 2% moves it to 32.1 / 32.8 / 33.6 (F) and 28.6 / 29.4 / 30.2 (M).
11. **Energy moved (OK).** Half of Σ|Δkcal_c| divided by total kcal, as defined. **Floor (OK):** 150/300 g food caps and 400/600 g group caps; 12–18 foods; composition as described (it includes raw egg yolk, coffee and cocoa).

## 4. Plausibility and alternative specifications

**Energy and cost.** 1,724 / 2,227 kcal excluding alcohol is plausible for NHANES adults with obesity; it is slightly below the all-adult WWEIA means, consistent with known under-reporting. Cost works out to about $5.3 per 1,000 kcal at grocery prices, which is plausible. But food away from home is valued at grocery prices, so real spending is substantially higher.

**Comparison with the Thrifty Food Plan.** The current diet is 9% (F) and 11% (M) above the ages 20–50 TFP. Because the sample's mean age is 50.5 and the 51–70 TFP is lower, the true gap is larger. I could not verify the June 2026 TFP values.

**Alternative specifications** (main analysis without D and E, protein 0.8 g/kg):

| Spec | F 0% | F −24% | F −35% | M 0% | M −24% | M −35% | Frontier F / M (no D, E) | Frontier F / M (all incl. D, E) |
|---|---|---|---|---|---|---|---|---|
| Main (P95, QP) | 8.99 | 7.77 (mv 66) | 8.51† | 10.65 | 9.84 (72) | 10.64† | 32.0 / 28.5 | 0.5 / 8.8 |
| **P99 bounds** | 9.10 | 8.00 (62) | **7.87 feasible** (78) | 10.17 | 9.88 (63) | **9.58 feasible** (77) | **47.4 / 46.7** | **40.0 / 41.9** |
| L1 objective (P95) | 9.46 (mv 36) | 7.36 (58) | – | 11.43 (43) | 9.95 (70) | – | same (cost LP) | same |
| Fibre = AI 25/38 g | – | 8.52 | 8.86† (+fibre 92%) | – | 10.86† (fibre 94%) | 10.93† (fibre 74%) | 30.5 / 19.8 | – |
| Age 51–70 corrected | – | 7.99 | 9.65† | – | 9.81 | 10.60† | 30.2 / 32.5 | – |
| Drop 7208/9802/7804 | – | 7.73 | 8.49† | – | 10.03 | 10.66† | 31.3 / 27.7 | – |
| **Food-level choice within P95 category totals** | – | feasible $2.19 | **feasible $2.23** | – | feasible $2.88 | **feasible $2.97** | >45% / >45%, even including D and E | – |
| Food-level, each food ≤5× its current mean | – | feasible | feasible | – | feasible | feasible | 39% infeasible | – |

**What these show:**

- **The feasibility headline ("no adequate diet beyond 32% / 28%") is robust to solver tolerance but not to the acceptability bound.** Moving from P95 to P99, which still caps every category at what at least 1% of eligible adults actually eat, makes the 35% cut feasible for both sexes, at 86% (F) and 82% (M) of current cost. With P99 bounds, even vitamins D and E become attainable from food up to about a 40% cut.
- **The infeasibility comes from the fixed within-category composites.** If people can choose among foods they already eat within each category, with category totals still at P95, adequate diets that include vitamins D and E exist beyond a 45% cut. They still exist at 35% when each food is capped at 5× its current population mean.
- **The cost of the closest adequate diet depends on the distance norm by $0.1–0.8.** At 24%, as a share of current cost it is 81% vs 85% (F) and 85% vs 84% (M). At current energy, L1 gives 98% of current cost for men vs 91% with the QP.

## 5. Overstatements in the prose

1. **Abstract last sentence and §5, "saves money only if people keep eating badly".** Contradicted by Table 1: adequate diets are cheaper than the current diet at every cut, and the cheapest adequate diet costs half as much.
2. **Social summary, "staying well-nourished saves less than a tenth".** No adequate diet exists at 35% in the main specification; at 24% the saving is 15–16%.
3. **§4.1, "no diet built from foods in the amounts eligible adults now eat meets every requirement"**, and **§5, "beyond a cut of about 30% no such diet can be built from foods ... without supplements or unusually large servings"**. The finding holds only for fixed category composites under P95 bounds that include non-consumers. Food-level choice within the same category totals, or P99 bounds, make it feasible. It should be framed as conditional on the composite and P95 assumptions; the Limitations section mentions this only briefly.
4. **§4.1, "Meeting them takes ... larger amounts of nutrient-dense foods than almost anyone now eats".** P99 bounds, which by construction at least 1% of people already eat, suffice. Better: "more than 95% of people eat".
5. **§3.3 and Table 2, vitamin D/E "best achievable".** Understated by 6–9 points at 24% (see §3, issue 2).
6. **Title, "nearly the same bill".** At 24% the adequate diet is 84–85% of current cost, and 81% with the L1 norm. "Nearly the same" is a stretch; "most of the bill" is more accurate.
7. **"Meets every RDA or AI".** Fibre is energy-scaled, and the iron RDA of 18 mg is applied to a sample in which about half the women are 51 or older.
8. **§2.6, "Independent AI agents checked every number"** should be accurate after this audit's fixes are applied.

## 6. Prioritised fix list

1. **Reframe the feasibility conclusions** (abstract, §4.1, §5, social summary) as conditional on the fixed within-category composites and P95 bounds. Report the P99 result (frontier ~47%; 35% feasible at $7.87 / $9.58) and the food-level-within-category result in §3.4 / Table 2. Disclose that 47 (F) and 53 (M) categories are frozen at their mean because P95 = 0.
2. **Fix the age 51–70 specification** (women's iron 8 mg; calcium UL 2000) and update Table 2 and §3.4: F24 $7.99; F35 $9.65† (Ca 90.5%, Mg 95.2%). The "<25 cents" claim becomes false: +$1.14 for F35. Consider also flagging the main analysis's 18 mg iron for older women.
3. **Correct the vitamin D/E reporting.** Either relabel the numbers as intakes in the minimum-total-shortfall diet, or report per-nutrient maxima (D: 95.5% / 93.7% at 24% with other requirements met). Fix the ‡ footnote, whose figures do not match Table 1, and report the men's −24% magnesium shortfall of 97.9% in that run.
4. **Remove or rewrite** "saves money only if people keep eating badly" and the social summary.
5. **Abstract fixes.** "$4.54–$7.59, at cuts up to 24%"; "two-thirds to nearly three-quarters of calories"; "fibre scaled to energy".
6. **Add sensitivity rows** for the L1 objective and for the absolute fibre AI (men's frontier 19.8%; men −24% infeasible).
7. **TFP comparison.** "9% and 11%"; note the age mismatch (51–70 TFP); verify the June 2026 TFP values; fix the "fna.usda.gov" typo.
8. **Figure 1 legend.** Do not limit the shortfalls to Mg and LA (at 39%: choline, calcium). Figure 2: label 0.5% as "<1".
9. **Figure 3 prose.** Add bananas (M) and cheese (F); "cakes" applies to women only.
10. **Housekeeping.** Exclude 7208/9802/7804/9999 consistently, or say so (effect ≤0.8 pp on the frontier). Fix the stale L1 and "cost minimised" docstrings. Add a `__main__` guard to results.py. Write current-diet vitamin D/E intakes to results.json.
