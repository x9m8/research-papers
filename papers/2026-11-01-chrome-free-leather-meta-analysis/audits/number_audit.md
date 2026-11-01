# Independent number audit — Paper 15, "What chrome buys"

Auditor: independent number auditor (did not write the paper). Date: 2026-10-28.
Scope: rerun of the package, extraction check against saved full texts, every number in `manuscript/manuscript.md` (abstract, social summary, text, Table 1–4, figure captions, figure PNGs, graphical abstract), and a methods review. No change was made to the manuscript, the package or WordPress. Audit-only sensitivity code: `/tmp/claude-0/-home-claude/e77537ee-4bde-5960-ac22-2794b7601af1/scratchpad/audit_sens.py` (run against `/home/claude/p15/audit_rerun`).

## Verdict

**PASS WITH REQUIRED CORRECTIONS.** The pipeline reproduces byte for byte. Every number in the abstract, text, tables and figures matches the result files. In the sampled studies no mean, SD or unit was transcribed wrongly. Two findings change how the results should be read:

1. The tensile **developer effect** (ratio of ratios 1.36) comes from two studies with non-standard chrome comparators. With in-study chrome controls only, it is 1.09 (0.86–1.37).
2. Pooling elongation and tear **departs from the protocol**, and the paper does not say so plainly.

There are also smaller issues: the extraction count of how many studies stated n is one too low, one study's arms were selected incompletely, and one table column is mislabelled.

## 1. Rerun

`pkg` was copied to `/home/claude/p15/audit_rerun` and the scripts were run in README order: screen → prisma → meta → figures → tables → graphical_abstract. All scripts ran without error. The outputs are byte-identical to the originals:

- `prescreen_counts.json`, `prisma.json`, `meta.json`, `effects.csv`, `ts_descriptive.csv`, `tables.md`, `fulltext_log.csv`, `records_dedup.csv`
- the regenerated Tables section of `manuscript.md`
- the four PNGs (pixel difference 0)

Three notes on the run:

- `tables.py` overwrites the Tables section of `manuscript.md` in place. That is by design, but it does mean the manuscript is a pipeline output.
- statsmodels emits no warnings.
- The comment in `meta.py` says the two-stage check uses DerSimonian–Laird. The code uses `method_re='iterated'`, which is Paule–Mandel, and Paule–Mandel is what the manuscript states. Only the comment needs fixing.

## 2. Extraction check

**Sample.** Eight studies drawn at random (seed 20261028): Atinafu 2026, Bielak 2022, Ferraris 2025, Hoch 2009, Jia 2022, Rosiati 2024, Valeika 2010, Valeika 2020. Added because the brief required them: Gómez-García 2026, Aguilar 2023, Chakraborty 2008. Added because they drive heterogeneity or influence: Qiao 2025 (elongation outlier), Fatama 2025 (second-largest leave-one-out shift), plus Gómez-García and Aguilar (the leave-one-out extremes). Girmay 2024 and Cavali 2022 were also checked for tensile and elongation while their tables were open. Every value was compared at the table or page stated in `source`.

| Study | Rows | Result |
|:--|--:|:--|
| Aguilar 2023 (replicates) | 24 values | All match Tables 4 and 7. Recomputed means reproduce the paper's ANOVA between-groups SS (3.7276E6). |
| Atinafu 2026 | 6 | All match Tables 1–2. Tensile was **not extracted**, although Table 2 has it (PO 12 ± 0.8; PE "18–21 ± 1.0"; chrome "20–22 ± 0.9", given as ranges). The omission is undocumented. |
| Bielak 2022 | 4 | All match Tables 1–2. This is **one** glutaraldehyde leather tested in two directions. |
| Chakraborty 2008 | 2 | Tensile 2256.3 vs 2255.80 psi matches. **n is stated**: "Each value reported is an average value of four samples" (p. 556). The extraction records n as missing and n_stated as "no". The elongation column order (44.10 vs 45.21) **cannot be verified** from the saved text, where 44.10 sits on its own line; the `source` note says only tensile was checked on the rendered PDF. |
| Fatama 2025 | 4 | All match Table V (column order confirmed). |
| Ferraris 2025 | 7 | All Ts values match Table 1. |
| Gómez-García 2026 | 2 | Values match the text and abstract (5.8 ± 1.7 vs 26.8 ± 2.7 N/mm²; Ts 77.9 ± 2.0 vs 80 ± 5.1 °C; n = 12 per vegetable system). **Only one of three vegetable arms was extracted** (mimosa, the weakest). Tara and quebracho tensile ("around 9.1–9.2 N/mm²") are in Table 2, which was not captured. The chrome n is not stated. |
| Hoch 2009 | 12 | All match Table 1. n = 10 skins per treatment is supported. |
| Jia 2022 | 8 | All match Table V, including the SD of 0.00. The methods say "average of three samples" (Ts section); n is imputed as 3 anyway, so there is no numeric effect. |
| Qiao 2025 | 9 | All match Table 2. The F-90 arm (commercial agent, 10%) was not extracted and no reason is given. The saved text does not say F-90's composition, so whether it is chrome-free could not be verified. |
| Rosiati 2024 | 3 | All match Table 4 (column order confirmed from the header: chrome, then vegetable). |
| Valeika 2010 | 6 | All match Table 3 (variant 7 is the control). Ts is shown only in a figure and was correctly not extracted. |
| Valeika 2020 | 2 | Match Table 1 (sample 5 vs sample 2). Elongation "at 10 N/mm² load" was correctly not used as elongation at break. |
| Girmay 2024 (extra) | 12 | All match Tables 6 and 9. Ts 95 ± 1.5 is trial 8, the 20% chestnut + 2% THPS recipe; the scoping brief's "96 ± 1" is trial 10, so the extraction is right. |
| Cavali 2022 (extra; tensile and elongation only) | 6 | All match Table 2. This is **one** vegetable leather tested in three directions. |

**Error rate.** The sampled studies cover 65 extraction rows: 260 numeric cells, 65 unit cells and 24 replicate values, 349 items in all. The Girmay and Cavali extra checks also matched.

- Transcription errors in means, SDs or units: **0 of 349**.
- n-field errors: Chakraborty, 2 rows (4 cells). That is **2 of 65 rows (3.1%)**, or 4 of 260 numeric cells (1.5%).
- Undocumented completeness omissions: 3 (Gómez-García arms, Atinafu tensile, Qiao F-90).
- Unverifiable item: 1 (Chakraborty elongation column order).

## 3. Manuscript numbers

All of the following were checked against `meta.json`, `prisma.json` and the rerun, and are correct:

- **PRISMA arithmetic.** 1,903 − 1,474 = 429; 429 − 244 = 185; 90 + 28 = 118; 185 − 118 = 67; 67 + 1 − 2 − 1 = 65; 34 + 4 + 2 + 1 = 41; 65 − 41 = 24. The by-source counts sum to 3,567.
- **Pooled ratios.** All pooled ratios, CIs and prediction intervals in the abstract, §3.2–3.3, Table 3 and Figures 1–2.
- **Tensile results.** τ = √0.1638 = 0.40; p = 0.11; two-stage 0.83 (0.67–1.03); leave-one-out range 0.80–0.91.
- **Tensile class, developer and small-study results.** The class estimates, the developer ratio 1.36 (0.85–2.18), non-developer 0.75 (0.54–1.04), and the small-study p = 0.70.
- **Elongation developer result.** 1.36 (1.04–1.79).
- **Flagged-study sensitivity.** 1.04 and 0.91.
- **Direction counts.** 28 of 38, 14 of 30 and 13 of 23.
- **Spot checks.** Gómez-García 5.8/26.8 = 0.22. Aguilar 3522.3/2157.1 = 1.63 and 2964.1/2157.1 = 1.37.
- **Shrinkage temperature.** 22 arms in 8 studies; 0 arms where chrome-free was higher; median −23 °C; range −39 to −2.1 °C; median of study means −21.5 °C; chrome-free 62–95 °C; chrome 80–109.2 °C; 21 of 22 censored or above 100 °C; flagged study −8 and −26 °C.
- **Study characteristics and narrative counts.** The comparator counts (19/4/1), species counts, developer count 11, years 1933–2026 with 20 from 2020 on, Table 4 rows = 13, and Nugraha "13 studies" (abstract: "tiga belas").
- **Narrative values checked against full text.** Xiao Table 3 values and Ferraris total Cr (111.73 and 53.72 mg/kg) match their full texts.

The figures were opened and match the results. Figure 3's title (22 + 2 arms, median −23 °C) and the graphical abstract values match.

### Discrepancy table

| # | Location | Stated | Correct / finding | Source | Severity | Fix |
|:--|:--|:--|:--|:--|:--|:--|
| 1 | §3.2 ¶4; §4.1 ¶3 ("tensile ratios about a third higher"); Table 3 last row | Developers' tensile ratios 1.36× those of others (0.85–2.18); non-developer pool 0.75 | The ratio is confounded with comparator source. It is driven by Aguilar (developer, commercial chrome, ratios 1.37/1.63) and Gómez-García (non-developer, external benchmark, 0.22). In-study comparators only: **1.09 (0.86–1.37), p = 0.43** (4 vs 8 studies). Without those two studies: **1.07 (0.86–1.33)**. Elongation holds up: 1.41 (1.00–1.97) in-study only; 1.37 (1.02–1.86) without the two. | audit_sens.py | **Major** (interpretation) | Report the in-study-only developer estimate. Drop "about a third higher" for tensile, or call it fragile. Keep the elongation statement, labelled exploratory. Note that the non-developer 0.75 includes Gómez-García. |
| 2 | §2.1, §3.3, Abstract, Table 3 | Elongation and tear pooled as "exploratory" | The protocol (brief l.391) says outcomes with fewer than about 15 studies are **downgraded to descriptive**. Pooling them is a deviation. The brief's other pre-specified moderators (species, stage, post-tanning matched) and its risk-of-bias checklist and contour funnel plots were not done. §2.6 lists only class and developer as pre-specified. | lit/brief.md l.152–168, 391 | **Major** (reporting) | Add a "Deviations from protocol" paragraph covering the elongation/tear pooling and the unanalysed moderators and checks. Consider moving elongation and tear out of the abstract's headline or marking them as a deviation. |
| 3 | §3.2, Table 3 (primary k) | 15 studies meet the threshold | Tensile meets the "about 15" threshold only with Gómez-García, whose chrome comparator is an external benchmark, whose chrome n is not stated, and which contributes 1 of 3 arms. Without it: **0.91 (0.81–1.03), 14 studies**. This is already in the leave-one-out range (0.91), but the threshold point is not discussed. | audit_sens.py; meta.json loo | Moderate | Say in §3.2 or §4.4 that the threshold is met by one study with an external comparator, and give the estimate without it. |
| 4 | data/extraction (gomezgarcia2026); §3.2 ¶2; Fig. 1 | One mimosa arm, 0.22 | Tara and quebracho arms (≈9.1–9.2 N/mm², SDs in uncaptured Table 2) were omitted. Illustration with an assumed SD of 1.7: pooled tensile **0.85 (0.70–1.03)**. True values unverified. | tandf_2724460.txt l.233, 333–337 | Moderate | Retrieve Table 2 and extract all three arms, or disclose that only the mimosa arm was readable. |
| 5 | Abstract; §3.1; §4.2; Table 2 (Chakraborty "no"); graphical abstract ("n stated for every arm in 8") | Eight studies stated n for every arm | Chakraborty states n = 4 ("average value of four samples"), so the count is **9** (or more; the other 9 unsampled studies were not checked for this). | bjsir_2246.txt p. 556 | Moderate | Set n_cf = n_cr = 4 and n_stated = yes for Chakraborty, and rerun. No effect on pooled estimates, because Chakraborty has no SDs. |
| 6 | Table 2, "Chrome-free arms" column (also meta.json classes_arms, n_arms_total = 56) | Bielak "2 aldehyde"; Cavali "3 vegetable" | One leather each, tested in 2 and 3 directions | lfj_22_1_1.txt Tables 1–2; Cavali Table 2 | Minor | Count agents, not direction rows, or footnote the directions. |
| 7 | §3.2 ("cluster-robust interval was the same to two decimals"); §2.6 | Robust check presented as confirmation | With REML, an intercept-only model and study-level variance dominating, CR1 equals the model SE almost by construction (tensile SE 0.10701 vs 0.10700). CR1 was used, not the CR2/clubSandwich check the protocol named. | audit_sens.py | Minor | Use CR2 with small-sample df, or present this as not an independent check. |
| 8 | Prediction intervals (Table 3, Abstract) | df = k − 1 | Riley et al. use k − 2. Tensile 0.33–2.08 vs the stated 0.34–2.07. Negligible. | audit_sens.py | Minor | State the df used, or switch to k − 2. |
| 9 | extraction.csv (atinafu2026, qiao2025) | Tensile not extracted (Atinafu); F-90 arm not extracted (Qiao) | Undocumented omissions. Atinafu's chrome tensile is a range; F-90's composition is not stated. | zenodo_19131211.txt Table 2; s42825_025_00190_0 Table 2 | Minor | Add notes to `fulltext_screening.csv`/`extraction.csv` giving the reasons. |
| 10 | Chakraborty elongation (44.10 CF vs 45.21 Cr) | As extracted | Column order not verifiable from saved text | bjsir_2246.txt l.258–260 | Minor (unverified) | Check against the rendered PDF, as was done for tensile. |
| 11 | Table 3, "Studies stating n only" (9 studies) | Label says n stated | Includes Gómez-García, coded "partial", with chrome n imputed | effects / sc | Minor | Relabel as "stating n for at least one arm", or exclude it. |
| 12 | §4.1, §5 ("about 20 °C") vs Abstract and social summary ("23 °C") | Mixed figures | Arm median −23; study median −21.5 | meta.json ts | Minor | Use one figure, or say "a median of 21.5–23 °C". |
| 13 | §3.5 / Table 4 (Ferraris total Cr) | Chrome-free leathers 111.73 and 53.72 mg/kg Cr | Values correct. However, the same source table gives the wet-blue chrome leather only 2.965 mg/kg total Cr, which is implausible (likely a unit or reporting error in the source). | Ferraris Table 1 | Minor | Add a caveat that the source table's chromium values look internally inconsistent. |
| 14 | References | Zuriaga-Agustí et al. 2015 listed | Not cited anywhere in the text or tables | manuscript.md l.260 | Minor | Cite it or remove it. |
| 15 | code/meta.py comment | "DerSimonian-Laird" | The code uses Paule–Mandel ('iterated'), as the manuscript says | meta.py | Trivial | Fix the comment. |
| 16 | code/screen.py docstring | `screening_manual.csv` | The file is `screening_ta_manual.csv` | screen.py | Trivial | Fix the docstring. |

## 4. Methods review

- **Effect measure.** The lnRR and its variance SD²/(n·x̄²) for each arm follow Hedges et al. (1999) and are coded correctly. Nasr's SD = pooled SEM × √5 is correct, and gives both arms the same SD. One soft spot: some arms have small n and a CV over 30% (Fatama elongation, CV 37%, n imputed 3), where the delta-method variance is less accurate. This does not change the conclusions.
- **Model.** Two-level REML with random effects for study and contrast. Arms sharing a chrome control get the chrome variance as their covariance, and the per-direction controls in Bielak and Cavali are handled correctly. CIs use t with k − 1 df, which is reasonable. The two-stage Paule–Mandel check agrees with the main model.
- **Dependence.** Shared controls are modelled. Arms that are the same leather tested in different directions (Bielak, Cavali) are treated as separate contrasts, with within-study correlation absorbed by the contrast-level random effect. That is acceptable.
- **SD of 0.00.** Jia's SD of 0.00 gives a variance of almost zero. The sensitivity analysis without Jia shows no effect on tensile; for tear, the estimate moves from 0.93 to 0.98.
- **Missing n.** Missing n is imputed as 3, with sensitivity at 2 and 5. The results do not depend on it (0.8327 and 0.8318 vs 0.8322).
- **Pooling threshold.** See items 2 and 3.
- **Developer moderator.** See item 1. It is the only finding that would change a stated conclusion: the claim of a tensile developer effect in §4.1. The headline pooled and in-study tensile estimates, the elongation developer effect and all shrinkage-temperature results stand.
- **Small-study test.** The Egger-type test has little power. The paper says so.

## 5. Not verified

- Table 4 rows that rest on abstracts or publisher pages: Daddi, Oliveira, Blas García, Inbasekar, Dhayalan, Pourrasoul Sardroudi, Ciurli and Tariq. Their full texts were not among the saved files checked.
- Navarro et al. 2020 ("39 LCA papers of four types").
- The Hedberg et al. 2014 citation for the EU Cr(VI) restriction.
- The "Italian tanneries" description of both LCAs.
- The extraction values of the unsampled studies: Uddin, Huang, Anggriyani, Tian, Jiang, Zhu, Nasr, Yorgancioglu, Evans, Cavali tear and Girmay elongation-direction notes. Whether these studies stated n was also not checked, so the corrected n-stated count is "at least 9".
- The true tara and quebracho SDs in Gómez-García (Table 2 was not captured).
- The Chakraborty elongation column order.
- Whether Qiao's F-90 agent is chrome-free.
