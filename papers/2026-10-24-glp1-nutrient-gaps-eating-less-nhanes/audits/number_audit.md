# Number and methods audit: "Eating less of the same: modelled nutrient gaps on GLP-1 drugs"

Auditor: independent agent, 2026-10-21. Nothing in the package was edited. All re-runs were done on a scratch copy.

## How this was checked

- I re-ran `usual.py`, `curves.py` and `tables.py` on a scratch copy. `prevalence.json`, `curves.json` and `usual_L.csv` came out byte-identical. The regenerated Tables section and `results/tables.md` are identical to the manuscript. **The pipeline reproduces.**
- I checked every number in the abstract, social summary, sections 1 to 5, Tables 1 and 2, and the figure captions against `results/prevalence.json` and `results/curves.json`, using the re-run console output.
- I wrote extra diagnostic scripts in the scratchpad, without touching the package:
  - variable coding and recall-status tables
  - variance components
  - domain-correct standard errors versus subset standard errors
  - weight totals using the MEC weight
  - an all-adult benchmark
  - a Box-Cox variant of the NRC method
  - a "shrink-then-add" supplement analysis
- I viewed all three PNG figures.

Verdict key: OK = matches; MINOR = wording or rounding issue; FIX = wrong or unsupported; METHOD = statistical issue that changes or qualifies results.

---

## A. Numbers: location | claim | correct value (source) | verdict | fix

| Location | Claim | Correct (source) | Verdict | Fix |
|---|---|---|---|---|
| Abstract | n = 2,134 | 2,134 (meta.L.n_two_day) | OK | – |
| Abstract, §3.1 | about 115 million | 114.74 M (sum of WTDR2D over the analytic sample). The same eligibility applied to all MEC-examined adults with WTMEC2YR gives 112.2 M (n = 2,918). | OK (see B4) | Optionally say "about 112–115 million" or cite the MEC-weight estimate. |
| Abstract | protein 8.3, zinc 31.6, folate 26.6, calcium 57.5 at baseline | 8.3 / 31.6 / 26.6 / 57.5 | OK | – |
| Abstract | at 24%: 27.2, 66.9, 55.9, 79.4 | same | OK | – |
| Abstract | at 35%: 46.4, 83.0, 74.5, 87.8 | same | OK | – |
| Abstract | "The average adult fell below ... 3.1 of 8 ... 4.9 at 24%" | mean count 3.120 and 4.938 (curves.json) | OK numerically, MINOR wording | "On average, eligible adults fell below the EAR for 3.1 of 8 nutrients". This is a weighted mean count, not a typical person. |
| Abstract | "only 5.6% would reach 1.2 g/kg" at 24% | 100 − 94.4 = 5.6 | OK | – |
| Abstract | "protein ... less than the requirement for their height" | Threshold is 0.66 g/kg × weight at BMI 25 for the person's height | MINOR | Say "below the EAR per kg of reference weight (BMI 25 at their height)". |
| Abstract | "Supplements ... narrowed but did not close the gaps" | Direction holds, but magnitudes are biased (B7) | OK qualitatively | Re-estimate with shrink-then-add. |
| Abstract, last sentence | "leaves most users short" | Model of eligible adults, not users. Conditional scenario. | FIX (overstatement) | "would leave most eligible adults short of several nutrients". |
| Social summary | "would leave most US users short of zinc, calcium and protein" | Protein below EAR is 18.9% at 16%, 27.2% at 24% and 46.4% at 35%, so it is never "most" in the 16–35% range (55.4% only at 39%). Zinc 53.6% at 16%. Population is eligible adults, not users. | FIX | e.g. "...would leave most eligible US adults short of zinc, calcium and magnesium, and a quarter to a half short of protein". |
| §1 | 16%, 24%, 35%, 39% reductions | Match brief §1 | OK | – |
| §1 | 127 users (Frankenfeld) | 42 + 85 = 127 (brief) | OK | – |
| §2.3 | 16% for "liraglutide 3.0 mg" | Brief: van Can abstract gives about 16% with 1.8 and 3.0 mg pooled; per-dose value not read | FIX | Say "liraglutide (1.8–3.0 mg)", or verify the per-dose figure in the full text. |
| §2.3, Table 2 | Oral semaglutide −39% | Gabe: −39.2 percentage points relative change vs placebo | MINOR | Note it is placebo-adjusted, single meal. |
| §3.1 | 87% BMI ≥ 30 | 86.55% | OK | – |
| §3.1 | 51% women | 51.47% | OK | – |
| §3.1 | mean age 51 | 51.47 | OK | – |
| §3.1 | mean BMI 35.6 | 35.64 | OK | – |
| §3.1 | 2,001 kcal, 75.3 g protein | 2,001 / 75.3. By construction this equals the weighted mean of observed two-day means, because of the rescaling. | OK | – |
| §3.2 | D 96.2, E 83.8, Mg 67.4, Ca 57.5, C 57.3, A 52.8, Zn 31.6 | all match | OK | – |
| §3.2 | "Nearly all were below ... vitamin E (83.8%)" | 83.8% | MINOR | "most" for vitamin E. |
| §3.2 | protein 8.3; 68.2 below 1.2 g/kg; K 16.0; fibre 3.2 | match | OK | – |
| §3.3 | 24%: protein 27.2, Zn 66.9, folate 55.9, Ca 79.4, Mg 93.2, A 77.6 | match | OK | – |
| §3.3 | 35%: 46.4, 83.0, 74.5, 87.8; B12 31.5; iron 15.8 | match | OK | – |
| §3.3 | 1,521 kcal / 57.2 g at 24%; 1,301 / 48.9 at 35% | match | OK | – |
| §3.3 | mean count 3.1, 4.9, 5.9 | 3.120, 4.938, 5.873 | OK | – |
| §3.3 | ≥5 of 8: 27%, 60%, 79% | 27.1, 60.5, 78.7 | OK (60.46 rounds to 60) | – |
| §3.3 | protein yardsticks at 24%: 27.2, 37.3, 67.7, 94.4, 88.1 | match | OK | – |
| §3.3 | protein-held scenario "micronutrients by construction the same" | True. Protein rows stay at baseline (8.3 etc.) by construction. The scenario adds no information and its results are not reported. | MINOR | Drop it, or report it as a single sentence. |
| §3.4 | "2017–2020 gave lower baseline shortfalls" | Food-only baseline for P: Zn 22.3, folate 21.2, Ca 48.0, Mg 61.0, protein 6.1, B12 6.5, iron 0.5 (all lower). Vitamin C 56.7 (about equal); D 97.5 and E 85.6 are higher. These food-only baselines appear nowhere in Table 2 (only food + supplement baselines). | FIX (unsupported as shown) | Add a "2017–2020, food, usual diet" column to Table 2, and qualify "lower for most nutrients". |
| §3.4 | 35%: Zn 74.1 → 50.0, Ca 84.7 → 69.3, folate 62.7 → 41.5, B12 22.8 → 11.0, Mg 96.8 → 85.2 | match P / P_supp | OK numerically, METHOD (B7) | Re-estimate. Shrink-then-add gives Zn 55.9, Ca 70.9, folate 44.5, B12 15.6, Mg 87.0. |
| §3.4 | "supplement file does not report vitamins A and E, so those results are unchanged" | Correct: P_DS1TOT and P_DS2TOT have no VARA or ATOC. Vitamin A is 82.2 in both; vitamin E is 98.4 vs 98.3 (log1p artefact). | OK / MINOR | – |
| §3.4 (not mentioned) | Iron with supplements | 8.6 (food) → 8.8 (food + supplements) at 35%, and 0.5 → 0.9 at baseline. **Adding supplements increases inadequacy.** This is a method artefact (B7). | FIX | Re-estimate. Shrink-then-add gives 7.5. |
| Table 2 | caption "at a 35% proportional cut" | Columns 4 and 5 are usual diet (r = 0) | MINOR | Fix the caption. |
| Table 2 | "99.8 (0.0)" | SE rounds to 0.0 | MINOR | Show "<0.1". In Table 1, choline at 39% prints "0.0" with no SE (inconsistent formatting). |
| Table 1 | caption says "share ... below the EAR" | Table also contains rows at or above the AI, and means | MINOR | Mention them in the caption. |
| §4.1 | "half ... short of calcium, a third short of zinc" | 57.5 / 31.6 | OK | – |
| §4.1 | "five or six of eight" | 4.9 (24%), 5.9 (35%), 6.2 (39%) | OK | – |
| §4.1 | "almost none would reach" protein targets | 5.6% reach 1.2 g/kg ref at 24%, 1.2% at 35%; 11.9% reach 80 g at 24% | OK-ish | Say "fewer than 1 in 10 (1.2 g/kg) to 1 in 8 (80 g)". |
| §4.1 | "14% less" | 1 − 1,102/1,281 = 13.97% | OK | Note it is cross-sectional (users vs non-users, app logging, n = 116), not a within-person reduction. |
| §4.1 | "the 16% curve is closer to the mark, and the shortfalls are still substantial" | At 16%: Zn 53.6, Ca 72.6, Mg 85.8, protein 18.9 | OK | – |
| §4.2 | 1/(1−r): "about a third more" at 24%, "about half again" at 35% | 1.316 (+31.6%), 1.538 (+53.8%) | OK | – |
| §4.2 | supplements "taken by some adults" | 53.2% (weighted) of the eligible 2017–2020 sample reported a 24-h supplement on at least one day | MINOR | "about half" is more informative. |
| §2.6 | "Independent AI agents checked every number" | True only after this audit's issues are resolved | MINOR | Keep only once the fixes are done. |
| Fig 2 caption | "Error bars are 95% CIs" | Coded as 1.96 × SE. Design df = 15 strata (L), so t(15) = 2.13 and the bars are about 8% too narrow. | MINOR | Use t with df = #PSU − #strata. |
| Fig 3 caption and panel A title | "four protein yardsticks" | Panel shows five thresholds (EAR × reference, adjusted and actual weight; 1.2 g/kg; 80 g) | FIX | "five protein thresholds". |
| Fig 1 | right-edge labels | "Zinc" and "Folate" labels overlap (unreadable) | FIX (cosmetic) | Offset the folate label. |
| Fig 1 caption | "shaded band spans reductions measured in trials" | Band 16–39 is correct | OK | – |

---

## B. Code and statistical checks

**B1. NHANES variables and coding: correct.**

- **RIDEXPRG.** 1 = pregnant is excluded. 3 (cannot ascertain) and NaN are kept. Among adults 20+ in L: 41 pregnant.
- **DIQ010 == 1.** Borderline (3) is not counted. That is defensible but should be stated.
- **BPQ020 == 1.** The variable exists in both BPQ_L and P_BPQ, so the `if 'BPQ020' in bpq` fallback is never used. That fallback would silently drop hypertension if the variable were renamed, so an assert is preferable.
- **Recall status.** DR1DRSTZ and DR2DRSTZ == 1 means reliable. Weights are WTDR2D (L) and WTDR2DPP (P). Design variables are SDMVSTRA and SDMVPSU.
- **Body measures and age.** BMXBMI is measured BMI. Age is RIDAGEYR ≥ 20. Age bands (<31, <51, <71) map correctly to the DRI groups 19–30, 31–50, 51–70 and 71+ (top code 80).
- **Missing values.** The analytic sample has no missing height, weight or nutrient values.
- **Zero weights.** pandas reads XPT zeros as about 5.4e-79, so the `w > 0` test does nothing. 845 L records with day 2 "not done" have WTDR2D > 0 by this test. The recall-status filter excludes them anyway, so there is no impact. Use `> 1e-6`.

**B2. EAR and AI values: match brief Table J-1 exactly.**

- Vitamin A 625/500; C 75/60; D 10; E 12; B12 2.0; folate 320.
- Calcium 800/800/800/1000 (men) and 800/800/1000/1000 (women).
- Iron 6 (men) and 8.1/8.1/5/5 (women).
- Magnesium 330/350 (men) and 255/265 (women). Zinc 9.4/6.8. Protein 0.66 g/kg.
- AIs: K 3,400/2,600; fibre 38/30 and 25/21; choline 550/425; vitamin K 120/90.
- Using age 20+ instead of 19+ is fine.
- Iron excludes women under 51, which matches the text. Ideally the probability approach would be applied to them rather than excluding them.

**B3. NRC shrinkage: algebra correct.**

- **Within-person variance.** Var(a − b) = 2σ²w, so `s2w = Σw(a−b)²/2` is the correct per-day estimator if the day-1/day-2 mean difference is zero. The code uses the uncentred mean square. In L the mean log differences are ≤0.06 and the effect is negligible. In P (day 1 in person, day 2 by phone) they are 0.03–0.11 (about 10% lower energy on day 2), which inflates s2w by up to about 4% (e.g. KCAL F 0.142 vs 0.137 centred). Centre the differences, or adjust for the sequence effect.
- **Between-person variance.** `s2m − s2w/2` is correct.
- **Shrink factor.** `f = sqrt(s2b/(s2b + s2w/2)) = sqrt(s2b/s2m)` is correct. Every person has n_i = 2, so a single factor is consistent.
- **Other choices.** Shrinkage is by sex only, with no age, weekend or sequence covariates (the NCI method uses them). Weighting is applied to the variance components, which is fine.
- **Transformation.** The log1p transform is not the problem. A Box-Cox variant (λ chosen per nutrient and sex, 0.15–0.55) changes prevalences by ≤2.4 points at baseline, 24% and 35% for every nutrient (e.g. eligible L baseline: zinc 31.6 → 33.0, folate 26.6 → 27.5, vitamin A 52.8 → 55.2, protein 8.3 → 8.3).

**B4. Mean rescaling.**

- The multiplicative rescale to the weighted mean of observed two-day means corrects back-transformation bias. It is acceptable and described accurately.
- Scaling U × (1 − r) after shrinkage, rather than scaling the recalls and refitting as the brief recommends, is near-equivalent under log1p.

**B5. Taylor SE: formula correct.**

- The formula is the standard with-replacement linearisation of a ratio mean: z = w(y − p)/Σw, summed to PSU totals, with Σ_h n_h/(n_h−1) Σ(z_hi − z̄_h)².
- The analysis subsets to the domain rather than using full-sample domain estimation. All L strata have 2 PSUs in the domain (one P stratum has 3), so the domain-correct SEs are **identical** (checked: zinc, calcium, protein).
- **Limitation.** The SEs treat the shrunken usual intakes as known. The variance components and the shrink factor are estimated from the same data and are not propagated, so the SEs are understated. Use BRR, Fay or jackknife replication that refits `usual()` in each replicate, as NCI practice does. This plus the z-vs-t issue (Fig 2) means the CIs are too narrow. Say so in the limitations.

**B6. "n nutrients below EAR": correct.**

- The count covers protein (reference weight) plus A, C, B12, folate, Ca, Mg and Zn, which is 8 nutrients and matches §2.5.
- The `curves.py` comment says "of the 10 EAR nutrients", which is cosmetic.
- These are per-person counts of cut-point classifications. Treating the cut-point as an individual classification is a known misuse: the cut-point is valid only for prevalence. Present the count as a descriptive index with that caveat.

**B7. Supplement sensitivity: variable names fine, method biased (main methods problem).**

- **Variables and merging.**
  - The DS1T*/DS2T* names exist (DS1TZINC, DS1TFDFE, DS1TCALC, DS1TMAGN, DS1TVB12, DS1TVC, DS1TVD, DS1TIRON, DS1TPROT and so on). VARA and ATOC are absent, as the text says.
  - The merge on SEQN is fine. Non-users have NaN (DS1DS = 2, 100% NaN). Users without that nutrient also have NaN (70% of DS1DS = 1 for iron). `fillna(0)` is correct for both.
  - 11 eligible records have no DS record and are treated as non-users, which is trivial.
- **The problem.** The code adds supplement amounts to each day's food *before* the log-scale shrinkage. Supplement intake is bimodal (53% users) and adds huge between-person variance. That raises the shrink factor for everyone, so **non-users' food intakes are shrunk less**, and the multiplicative mean rescale is driven by high-dose users.
- **Evidence of the bias, among non-users only (who take nothing):**

  | Non-users, 2017–2020 | Food only | Add-then-shrink |
  |---|---|---|
  | Zinc below EAR, 35% cut | 76.3% | 67.1% |
  | Vitamin D below EAR, 35% cut | 99.9% | 97.4% |
  | Iron, baseline | 0.5% | 1.0% |

  Iron prevalence *rises* overall with supplements (8.6 → 8.8 at 35%; 0.5 → 0.9 at baseline).
- **Standard fix.** Use NCI-style "shrink-then-add": estimate usual food intake, scale it, then add each person's mean supplement amount over the two days. The table below compares the three methods (eligible, 2017–2020, 35% cut, % below EAR).

  | Nutrient | Food | Manuscript | Shrink-then-add |
  |---|---|---|---|
  | Zinc | 74.1 | 50.0 | 55.9 |
  | Folate | 62.7 | 41.5 | 44.5 |
  | Calcium | 84.7 | 69.3 | 70.9 |
  | Magnesium | 96.8 | 85.2 | 87.0 |
  | Vitamin B12 | 22.8 | 11.0 | 15.6 |
  | Vitamin C | 77.9 | 53.2 | 56.0 |
  | Vitamin D | 99.8 | 62.7 | 62.0 |
  | Iron | 8.6 | 8.8 | 7.5 |

  Baseline under shrink-then-add: Zn 17.8, folate 15.7, Ca 36.6, Mg 54.1, B12 4.8, C 42.0, D 60.1, iron 0.5.
- **Effect on conclusions.** The qualitative claim "narrowed but did not close" survives. The manuscript overstates the narrowing for zinc, B12 and folate, and shows an impossible iron increase.

**B8. Other code notes.**

- `protect_protein` runs are computed but unused.
- The `P_supp` run recomputes usual intake per scenario with `r` applied before log1p, which explains the tiny vitamin A and E changes.
- **Eligibility via BPQ020.** BPQ020 is "ever told high blood pressure", which is fine. It includes people whose hypertension has since resolved, which is fine for an approximation.

---

## C. Plausibility of baseline estimates

I ran the same method on **all non-pregnant adults 20+** for comparison with national NCI-method (WWEIA) estimates (% below EAR, food only).

| Nutrient | 2017–2020, this method | 2021–2023, this method | Approx. published NCI/WWEIA, adults (from memory; verify against the ARS table cited in brief §3 item 6) |
|---|---|---|---|
| Vitamin A | 46.8 | 49.6 | ~45 |
| Vitamin C | 53.2 | 51.9 | ~45–46 |
| Vitamin D | 96.7 | 94.2 | ~95 |
| Vitamin E | 81.9 | 78.7 | ~85–88 |
| Calcium | 48.3 | 53.6 | ~40–45 |
| Magnesium | 56.9 | 59.5 | ~50–52 |
| Zinc | 22.3 | 28.9 | ~12–15 |
| Folate (DFE) | 18.9 | 23.5 | ~8–12 |
| Vitamin B12 | 7.6 | 9.1 | ~3–5 |
| Protein (EAR) | 5.6 (ref wt) | 7.2 | low single digits |

**Assessment.**

- Vitamins A and D and calcium are in the plausible range. Magnesium and vitamin C are somewhat high, and vitamin E is somewhat low.
- **Zinc, folate and B12 look high (about 1.5–2× published values).** These are the nutrients with large day-to-day variance (folate s2w/s2b ≈ 2.4–3.5 on the log scale). Changing the transformation does not fix it (B3).
- Likely contributors:
  - no weekend or day-sequence adjustment, so between-day structure leaks into between-person variance;
  - shrinkage pooled across ages within sex;
  - the simpler NRC method generally.
- My reference values are from memory, not read in this session. **This must be validated against the ARS WWEIA usual-intake PDF** before publication, as the brief itself recommends. Until then, zinc and folate baselines (31.6%, 26.6%) and their scenario values should be treated as possibly overstated.
- **Cycle difference.** The 2021–2023 all-adult numbers run 3–7 points above 2017–2020 for zinc, folate and calcium. That is consistent with telephone-only recalls but not explained in the text. Iron in L (3.0%) is six times P (0.5%), which should be commented on.
- **Eligible vs all adults.** Eligible adults differ from all adults by only about 2–4 points at baseline (L zinc 31.6 vs 28.9; folate 26.6 vs 23.5). The conclusion "Most US adults who qualify ... already eat too little of several nutrients" is true of US adults generally. Say so, to avoid implying it is specific to this group.

---

## D. Population-total claim ("about 115 million")

- The two-day dietary weight is calibrated so that the two-day sample represents the whole population. In L, ΣWTDR2D over all two-day-reliable records is 324.7 M, and over adults 20+ it is 242.1 M.
- A domain sum of WTDR2D is therefore a valid estimate of the eligible population size (114.7 M).
- An independent estimate with the MEC weight over all examined adults with BMI (n = 2,918) gives 112.2 M of 239.8 M. The figures are consistent, so the claim stands.
- Add a CI if it is a headline number, and make clear it is August 2021–August 2023.

---

## E. Overstatements and framing

1. **Social summary.** "most US users short of ... protein" is false under the paper's own primary protein measure (27% at 24%, 46% at 35%). It is also about eligible adults, not users. **Fix (high priority).**
2. **Abstract final sentence, and conclusion "as early evidence suggests users do".** The "eating less of the same" premise rests on a single conference app study reported by news (no abstract located). Hedge: "as one early app-based study suggests".
3. **§4.1 "At the intake reductions seen with current obesity doses".** These are lab ad libitum, mostly single-meal reductions. Bring the caveat into the same sentence.
4. **Cut-point used as a per-person classification** (counts of nutrients, "the average adult"). Add a caveat.
5. **Precision.** The SEs and CIs ignore variance-component estimation and use z rather than t. Say they are approximate.
6. **"Nearly all ... vitamin E (83.8%)".** Overstated.
7. **Supplement magnitudes.** Biased as described in B7.

---

## Prioritised fix list

1. **Supplement sensitivity (B7).** Replace add-then-shrink with shrink-then-add, using each person's two-day mean supplement amount added to scaled usual food intake. Then regenerate Table 2, Fig 3B and the §3.4 numbers. The current version raises iron inadequacy when supplements are added and overstates the narrowing for zinc and B12 by about 5 points.
2. **Validate the baseline against the published NCI/WWEIA usual-intake tables** (all adults, 2017–2020; ARS PDF in brief). Zinc, folate and B12 appear 1.5–2× too high. If confirmed, add day-of-week and sequence adjustment (or move to the NCI method or the SIMPLE macro), or at minimum state the discrepancy in the Limitations.
3. **Social summary and abstract last sentence.** Remove "most ... short of protein" and change "users" to "eligible adults" in conditional form.
4. **§3.4 "lower baseline shortfalls".** Add a 2017–2020 food-only usual-diet column to Table 2 (values: protein 6.1, Zn 22.3, folate 21.2, Ca 48.0, Mg 61.0, A 48.0, C 56.7, D 97.5, E 85.6, B12 6.5, iron 0.5), qualify the claim ("for most nutrients; not D, E"), and fix the Table 2 caption, which says 35% for the usual-diet columns.
5. **§2.3 / Table 1 header.** "liraglutide 3.0 mg" for −16% is not supported (doses pooled in the source). Relabel or verify.
6. **Standard errors.** Use replicate-based variance that refits the shrinkage, and t(df) for 95% CIs (Fig 2). At minimum, state in §2.5 or §4.3 that the SEs are conditional and approximate.
7. **Fig 3.** "four yardsticks" should be five, in both the caption and the panel A title. **Fig 1:** fix the overlapping Zinc/Folate labels.
8. Centre day differences when estimating s2w. This matters for P, where day-1 intake is about 10% higher than day-2.
9. **Wording.**
   - "average adult" should be "on average".
   - "Nearly all ... vitamin E" should be "most".
   - Note the cut-point caveat for per-person counts.
   - State that DIQ010 = 3 (borderline) is not counted.
   - Note that eligible-adult baselines are close to those of all US adults.
10. **Cosmetic code fixes.**
    - Weight test `w > 0` should be `w > 1e-6` (pandas XPT zero issue).
    - Assert that BPQ020 exists instead of silently falling back.
    - Fix the `curves.py` comment ("10" should be "8").
    - Show "<0.1" instead of "(0.0)" SEs.
    - Drop or report the unused protein-held scenario.

Scratch diagnostics (not part of the package): /tmp/claude-0/-home-claude/e77537ee-4bde-5960-ac22-2794b7601af1/scratchpad/chk1.py to chk5.py.
