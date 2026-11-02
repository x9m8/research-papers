# Number audit: Paper 19, "US food waste revisited: a reproduction with public data"

Independent audit, 29 Oct 2026. Auditor did not write the paper. Manuscript, code and results were not modified; the rerun was done in a copy (`/home/claude/p19/audit_rerun`).

## Verdict

**Pass with minor corrections.** The pipeline reruns cleanly and bit-for-bit: every result file, derived file and the regenerated Tables section is byte-identical to the package. The model code matches Hall et al.'s published equations 10 and 13–14 exactly, and the printed coefficients (9,100 and 22) are reproduced from first principles. Every input value I spot-checked against the live public source matched: Ogden et al. (2004) Tables 7, 9 and 10; FAOSTAT FBSH and FBS; and ERS LAFA. Every number in the abstract, text, tables, captions and graphical abstract agrees with the results files, to the stated rounding. The direct quotations from Hall et al. are accurate.

There are no high-severity errors. The main issues are in framing, not arithmetic:

1. The 2003→2023 "95% interval" covers only parameter uncertainty, and the result depends on which end year is chosen.
2. The abstract's "fell to 35.7% by 2013" hides the true trough, 35.2% in 2017.
3. A few small wording and attribution slips.

## 1. Rerun

- Copied pkg to `audit_rerun` and ran `01_inputs` → `02_reproduce` → `03_robustness` → `04_update` → `05_figures` → `graphical_abstract` → `tables` (Python 3.13.16). All exited 0.
- `results/*.json|csv|md`, `data/derived/*.csv` and `manuscript.md` (rewritten by `tables.py`) are byte-identical to the originals. The figures regenerated and match the package PNGs visually.
- I did not rerun `00_nhanes_aggregate.js`, which needs a browser on cdc.gov and the microdata. The NHANES aggregates are therefore taken as given; see §3 for the external cross-checks.
- I did not run `build_docs.sh`, and I did not audit the `out/` .docx/.pdf against the .md.

## 2. Model against the original (read from PMC2775916, equation images inspected)

| Item | Original | Code | Status |
|---|---|---|---|
| Eq. 13, full form (incl. δ(t) term) | ΔI = [ (ηF+ρF+α(ηFFM+ρFFM))/(1+α) · dBW/dt + (γF+αγFFM)/(1+α)·(BW−BW0) + δBW − δ0BW0 ] / (1−β) | `coefs()`, `intake()` incl. `delta_path` | Match |
| Eq. 14 (displayed as a second "(13)" in the article) | 9,100 kcal/kg × dBW/dt + 22 kcal/kg/d × (BW−BW0) | 9,103.0 and 22.14 at nominal values (α = 10.4/19.1) | Match |
| Eq. 10, Jackson fat mass; F0 = pW·FW + (1−pW)·FM = 19.1 kg; pW = 0.525 | as printed | `jackson_fat`, `F0_HALL = 19.1`, `P_W = 0.525` | Match |
| Text parameters γFFM 22, γF 3.2, β 0.24, ρF 9,400, ρFFM 1,800, ηF 180, ηFFM 230, C 10.4, α 0.54, I0 2,100 | as stated | `NOMINAL` | Match |
| Table 1 (MC) 22±4, 3.6±2, 7±4, 0.24±0.1, 230±100, 180±20, 10.4±5, 2100±100 | as printed | `TABLE1` | Match. The redraw truncation (C ≤ 0, β ≥ 0.95) is not in the original; it is disclosed in the README but not in the manuscript. The original reports MC means; the paper uses medians. |
| Waste = FA − I | eq. "(14)" | `FA - I` | Match |
| Oil: 3 kcal fossil per kcal food | stated | `FOSSIL_PER_FOOD=3`; 0.252 kcal/Btu; 5.8e6 Btu/bbl | The arithmetic is correct. **The original does not state 5.8 million Btu/bbl**, but §2.3 lists it among "the original's conversion assumptions". |
| Freshwater: agriculture ≈70% | stated | 0.70 × wasted share | Match (0.70 × 38.64 = 27.0%) |
| MSW energy density 1.9 kcal/g | stated | 1.9 | Match. The EPA 2003 figure is interpolated between 2000 and 2005. |

Hand checks: Cdyn = (180+9,400+0.5445·2,030)/(1.5445·0.76) = 9,103. Cstat = ((3.2+0.5445·22)/1.5445+7)/0.76 = 22.14. IOM EER I0 (men 2,456.8, women 1,840.8 at the 1999–2000 mean ages) pools to 2,133.4. Total waste 1,459.45 × 365.25 × 292.883 M = 156.1 trillion kcal. Oil: ×3/(0.252×5.8e6) = 320.5 M bbl, which against EIA 2003 (20,034 kbd × 365.25) is 4.38%.

## 3. Data inputs: spot-checks against the public sources

| Input | Checked against | Result |
|---|---|---|
| Ogden 2004 AD347 Table 7, weights 20–74, all five surveys, both sexes, with SEs; 20+ for NHANES III and 1999–2002; Tables 9 and 10 height and BMI for NHANES I and III | cdc.gov/nchs/data/ad/ad347.pdf (read 29 Oct 2026) | All match. "Pregnant females were excluded" is confirmed. |
| FAOSTAT FBSH Grand Total 1974, 2000, 2003, 2005, 2010–2013; Sugar & Sweeteners and Animal Products 2005 and 2011; population 1974–2005 | FAOSTAT API via fao.org (29 Oct 2026) | All match (3,031; 3,755; 3,777; 3,828; 3,650; 3,649; 3,687; 3,682; sugar 656→589; animal 1,052→980) |
| FAOSTAT FBS Grand Total 2010–2013, 2019, 2022, 2023; population | same | All match (3,730.68; 3,724.24; 3,759.04; 3,745.33; 3,819.76; 3,937; 3,947.33) |
| FBS − FBSH overlap 80.68, 75.24, 72.04, 63.33; mean 72.82 | recomputed from the verified values | Match |
| ERS LAFA calories total 1974, 2000, 2003, 2010 | ers.usda.gov/media/5381/calories.csv | Match (2,028; 2,561; 2,566; 2,501) |
| NHANES microdata aggregates | Internal: pooled 1999–2002 gives 86.84/74.61 kg against Ogden's 86.8/74.7 | Consistent. The microdata were not re-parsed (not verifiable here). |
| EIA MTTUPUS2 2003 = 20,034 kbd; EPA food generation 2000/2005 = 30,700/32,930 thousand tons | not re-fetched | Unverified live; plausible |
| OpenAlex citation count "747 on 28 Oct 2026" | api.openalex.org (29 Oct 2026) | Now **753**. The 28 Oct value cannot be verified. |

FAO splice: the method (subtract the 2010–2013 mean difference from FBS from 2014 on) is implemented as described. Population switches to the FBS series from 2014; this affects only totals, which are not reported after 2003. On sensitivity, using the 2013-only offset (63.3) or the 2010-only offset (80.7) moves the 2003→2023 change from +0.01 to +0.16 or −0.12 pp.

## 4. Manuscript numbers

All of the following were checked against the results files and the rerun and are **correct to the stated rounding**:

- Abstract: 9,103; 22.1; 929→1,459; 57%; 30.7→38.6%; 22–37%; 39.0% (2002, 2005); 38.6% (2023); +0.0 (−1.2 to +1.0).
- §2.2: 86.84/74.61 against 86.8/74.7; 63–81 (mean 72.8).
- §2.4: 0.915.
- §2.5: 0.915–0.929.
- §3.1: 22.5; 19.6 (19.2); α 0.53/0.54; 2,133 (2,109–2,158); 0.2–1.5 kg; 71.2/71.9; 80.3/81.4; 8.9/9.4 kg; 8.4/8.9 × 10⁻⁴; within 16 kcal; within 30 kcal except 2000–01 (54–99); 3,755; 2,102→2,318 (2,311); 208; 9.9; 13.7; 929, 1,459, 57%, 30.7, 38.6; digitized 929, 1,466, 58%, 30.6, 38.8; 156; 320; 4.4%; 27%; MC 733–1,123 and 1,214–1,687; 99.95%; +8.0 (+3.8 to +11.4); USDA +8%/−17%; EPA 99 kg and 35%.
- §3.2: +6.0 to +10.4 pp; 49–79%; ≤0.4 pp; 2,361; 22.0/31.7; 1,973; 34.8/42.0; 36.6/43.9; 40.6/36.7; 125–140 against ≈215; 40.7–41.1; δ 1.3.
- §3.3: 81.3, 84.8, 84.5 kg; 2,318, 2,382, 2,377; 3,828, 3,649, −67, −72, 3,731, 3,947; shares 38.6/39.0/36.1/35.7/36.4/38.6; −0.06 against +0.26; 50%; +38 (−12 to +80); 73 kcal; 39.8%; 1.1 (0.0 to 2.1); +0.01; 36.6/43.6/43.0; 97%/86%; 2,255→2,050.
- §4–5: ≈750 against ≈215; ≈60 and ≈100 kcal; 32–44%; 31→39%.
- Tables 1–3 and 3 (continued): all cells match.
- Figures 1–3 and the graphical abstract: plotted values and labels agree with the results. The Figure 2 labels match Table 2.
- Quotations from Hall et al. (abstract sentence; "progressively increased from about 30%…"; "within 5%…∼25% too low"; "push effect"; "unless the uncertainties…later dates"; dashed MC curves in Fig. 1) were checked verbatim against PMC2775916. They are accurate.

### Discrepancy table

| # | Location | Stated | Correct / issue | Source | Severity | Fix |
|---|---|---|---|---|---|---|
| 1 | Abstract; §3.3; Table 3; graphical abstract ("95% interval −1.2 to +1.0") | Presented as the 95% interval for the 2003→2023 change | The interval propagates **model-parameter uncertainty only**. It omits sampling error in the mean weights, the splice offset (±0.15 pp across the 2010–2013 range), the extrapolation to 2023 and FAO noise. A ±0.35 kg error in the 2021–23 mean weight alone moves the change by ∓0.27 pp. | rerun sensitivity (audit script) | Medium | Say "95% parameter-uncertainty interval" wherever it is cited. Add one sentence that sampling, splice and extrapolation uncertainty are excluded and would widen it. Soften §4.4's "small next to the parameter uncertainty" for the change, where parameter uncertainty largely cancels. |
| 2 | Abstract; §4.2; conclusion ("the share has not risen further"; trend −0.06 pp/yr) | End-to-end change +0.0 pp; trend −0.06 | Both rest on the choice of 2023 as the end year. 2022 against 2003 is −0.19 pp. The series fell to 35.19% in 2017, then rose 3.5 pp in 2017–2023 as FAO supply jumped. A naive OLS SE on the 2003–2023 slope is 0.048 pp/yr (understated, given autocorrelation), so the slope is not distinguishable from 0. No interval is reported for either trend. | update.json series; rerun | Medium (inference) | Report the trend without implying a sign. Mention the 2017 trough and the late rise. Avoid implying a significance test the paper did not run. "Did not continue the 1974–2003 climb" is supported; "stopped" is fine only if it is not read as a decline. |
| 3 | Abstract | "fell to 35.7% by 2013 and returned to 38.6% in 2023" | The minimum was **35.2% in 2017** (2014–2017 all 35.2–35.3%). 35.7% in 2013 is true but not the trough. | update.json `nchs|spliced` frac series | Low–Medium | "fell to about 35% in 2014–2017 (35.2% in 2017) and returned to 38.6% in 2023" |
| 4 | §3.2 | "β and C moved it by 0.5–0.8 points" | β +1 SD moves the 2003 share by **0.87** (−1 SD: 0.67); C: 0.55 and 0.77 | robustness.json `oat` | Low | "0.5–0.9 points" |
| 5 | §4.2 | "a small rise of about one point remains, most of it the break itself" | The spliced change is +0.0, so essentially **all** of the unspliced +1.1 pp is the break (73 kcal at about 2,377/3,947² gives about 1.1 pp) | update.json | Low | "…remains, essentially all of it the break itself" |
| 6 | §2.3 | 5.8 million Btu per barrel listed among "the original's conversion assumptions" | Hall et al. do not state a Btu/barrel factor. 5.8 MMBtu/bbl is the EIA crude heat content chosen here. | PMC2775916 full text | Low | Attribute 5.8 MMBtu/bbl to EIA, not to the original |
| 7 | §1 | "OpenAlex listed 747 works citing the paper on 28 October 2026" | OpenAlex returns 753 on 29 Oct 2026. The 28 Oct value cannot be verified. | api.openalex.org/works/doi:10.1371/journal.pone.0007940 | Low | Re-check at publication and update the count and date |
| 8 | §3.1 | "EPA's current series puts municipal solid food waste at 99 kg per person in 2003" | EPA has no 2003 value. 99.2 kg is linearly interpolated between 2000 and 2005. | code 02, epa_food_msw.txt | Low | Add "(interpolated between 2000 and 2005)" |
| 9 | §2.1 / Methods | MC "from normal distributions (their Table 1)" | The code redraws C ≤ 0 and β ≥ 0.95 (not in the original) and reports medians (the original reports means) | code 02/04; README; PMC2775916 | Low | Add one clause to §2.1 or the Table 1 caption |
| 10 | §2.1 | "they obtain their equation 13 … reduces to their equation 14" | In the article the simplified equation is printed with a second label "(13)" and the waste equation is "(14)". The text calls the simplified one "equation 14". | PMC2775916 equation images | Low (clarity) | Footnote or parenthesis: "(printed as a second eq. 13; the text calls it eq. 14)" |
| 11 | §3.2 | "a one-SD change in I0 moved the 2003 share by 2.6–2.7 points" | Both directions are 2.65 pp | robustness.json | Trivial | "by 2.6 points" or "about 2.65" |
| 12 | Model detail (no text claim) | I(1974) = 2,102, not I0 = 2,100 | The dynamic term is nonzero at the base year (slope of the 1974–1978.5 segment), slightly inconsistent with the assumption of energy balance in 1974. The effect is 2 kcal. | common.py `intake()` | Trivial | Optionally note it, or set the dyn term to 0 at the base year |
| 13 | README | "P_ files for 2017–March 2020" | The body-weight and diet series use the 2017–2018 `_J` files. The P_ aggregates are computed but unused. | 00_nhanes_aggregate.js, 01_inputs.py | Trivial | Clarify in the README |
| 14 | Graphical abstract | "(95% -1.2 to +1.0)" | Hyphen instead of minus sign; same caveat as #1 | graphical_abstract.png | Trivial | Use "−" and "parameter 95% interval" |

### Not verified / outside scope

- NHANES microdata aggregates: not re-derived (needs a browser run on cdc.gov). Consistency with Ogden's 1999–2002 values is the only external check.
- EIA and EPA raw values were not re-fetched. The digitized Figure 1 values were not re-digitized.
- Hall et al. (2011) "about 0.9 MJ (about 215 kcal) per day" and "I found no published reproduction" were not checked.
- The causal claim in §3.1/§4.1 that the USDA and EPA mismatches are "because both series have been revised" is plausible but untested (the original's vintages were not retrieved).
- The out/ .docx/.pdf were not compared with manuscript.md.

## 5. Methods notes

- **Monte Carlo:** implemented as in the original Table 1, with a fixed seed. 2.5–97.5 percentiles are reported. The same parameter draws are reused for the update, which is appropriate.
- **Robustness:** the variants are implemented as described. The δ(t) path uses the full eq. 13 term (δ·BW − δ0·BW0)/(1−β), which is correct. The OAT for γF is centred on 3.6 (Table 1), not on the baseline 3.2, so it is asymmetric around the baseline. This is not stated, but it is immaterial.
- **Children adjustment:** the ratio of mean IOM sedentary EER for all ages to that for adults 20–74 (0.915 in 1999–2000) is applied to the whole modelled intake. Table 2 holds it at 0.915 for all years; the update interpolates by cycle and holds it constant before 1999.5. The 1974 correction is probably understated, as §4.4 says. The update's 2003 per-capita share (43.6%) differs from Table 2's (43.9%) because of the cycle-specific ratio. Both are reported consistently.
- **2003–2023 inference:** see discrepancies #1–2. The splice-offset and weight-sampling sensitivities are each about 0.15–0.3 pp. They do not overturn "no further rise", but they belong in the stated uncertainty.
