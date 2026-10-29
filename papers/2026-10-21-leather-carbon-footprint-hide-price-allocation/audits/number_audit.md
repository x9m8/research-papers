# Number audit: "Leather's carbon bill follows the hide price, not the cow"

Auditor: independent number check, 2026-10-20. No network was used, and the manuscript and code were not edited.

**Reproduction.** The full pipeline (hide_series, allocation, summary, carbon, crosscheck, tables) was re-run on a scratch copy of `pkg/`. Every file in `results/` came out byte-identical to the shipped files. The tables that `tables.py` regenerated were identical to Tables 1 and 2 in the manuscript.

Note: `tables.py` rewrites the `## Tables` section of `manuscript/manuscript.md` in place. Anyone re-running the package will overwrite manual edits to the tables. This should be documented, or the script should write only to `results/tables.md`.

**Verification sources.** Anchor prices were checked against `pdftotext -layout` output of the two AMS_2829 PDFs. Literature values were checked against `/home/claude/p7/lit/brief.md` and `/home/claude/p5/lit/brief.md`.

Verdicts: **OK** = matches the source. **ERROR** = wrong. **IMPRECISE** = defensible but misleading, loosely worded, or not supported as stated.

## 1. Abstract, title, social summary

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| Abstract | Monthly series June 2001 to Dec 2025 | WPU0419 runs 2001-06 to 2025-12 (295 obs); allocation_monthly runs 2001-06 to 2025-12 | OK | – |
| Abstract | Index converted with six AMS report prices | anchors.csv has 6 calibration rows | OK | – |
| Abstract | "nine published quotes not used in the scaling fall within a median 5.8%" | val_median_abs = 5.8% (n=9). Four of the nine are multi-month or annual **averages** (Peel 2013–17, 2018, H1 2019, June 2019), not quotes | IMPRECISE | Say "nine published prices or averages" |
| Abstract | 4.86% (2002–2013), 0.94% (2023–2025), 0.62% (2025) | summary.json: early 0.048586, late 0.009409, 2025 0.006208 | OK | – |
| Abstract | Fivefold, holds across six denominators (5.0–5.2-fold) | alts folds 5.00–5.16 | OK | – |
| Abstract | "Since 2013 the hide lost 76% … live steer gained 96%" | hide_pct −76.2, live_pct +96.3 (annual means, 2013 vs 2025) | OK | Could add "by 2025" |
| Abstract | Per-m² emissions "fell from 113 to 22 kg CO2e between the same periods" | carbon.json: early 113.19, late 21.92 | OK (numbers) / IMPRECISE (wording) | "the same periods" points back two sentences, and the sentence just before is about 2013→2025. Write "between 2002–2013 and 2023–2025" |
| Abstract | Mass allocation would keep them "near 112" | 111.825, constant by construction (= 21.3 × 0.63 / 0.12) | OK | – |
| Abstract | "Published allocation factors from 1% to 3.5% are snapshots of this moving ratio" | Includes Italy 2.68% (Italian prices) and LWG/UNIDO (global data, price year not stated). It is not shown that these are readings of the *US* ratio | IMPRECISE (overstatement) | "…are consistent with snapshots of a moving ratio" |
| Title | "follows the hide price, not the cow" | Log decomposition: hide 68%, live value 32% (price 27%, weight 5%) of the 2013→2025 decline | IMPRECISE (rhetorical) | Acceptable as a title only if the text keeps the 68/32 split visible. Consider "mainly the hide price" |
| Social summary | "Leather's carbon footprint fell fivefold in 20 years on paper, because hide prices crashed, not because cattle changed." | The quantity is farm-stage emissions allocated to the hide, not leather's footprint; tanning is excluded (§2.4). The fold is mean 2002–13 vs mean 2023–25 (5.2×), roughly 16 years between period midpoints; 2002→2025 is 9.3×. About 32% of the decline is from rising live value (cattle prices), so "not because cattle changed" is only half true | IMPRECISE (overstatement) | e.g. "The farm emissions charged to a US cowhide fell about fivefold on paper since the 2000s, mainly because hide prices crashed while cattle prices soared" |

## 2. Methods vs code

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| §2.1 | Series WPU0419, June 2001 = 100, monthly, from FRED 20 Oct 2026 | fred_20261020.json: WPU0419 = 100.0 at 2001-06; identical to WPU04190108 | OK | – |
| §2.1 | "The index starts in June 2001, which sets the start of the study" | WPU0419 / WPU041 has a constant ratio of 0.4578 (sd 0.0002) over all 295 months. WPU0419 is WPU041 rebased, and WPU041 (in the same json) runs from 1926 | IMPRECISE | Either drop the causal claim, or explain why WPU041 was not used to extend back (e.g. ERS coverage, no early anchors) |
| §2.1 | *k* is the geometric mean of the price/index ratio over six reports | hide_series.py: k = exp(mean(log(price/ppi))) = 0.62678 | OK | – |
| §2.1 | Anchors 28 Apr 2015 $95.75; 27 Oct 2017 $56.00; 8 Nov 2019 $36.00–36.50 (midpoint); 23 May 2025 $15.25; 26 Aug 2025 $19.25; 30 Sep 2025 $19.00 | anchors.csv matches. The AMS PDFs confirm "Steer Hides, Branded (Butt) … Wtd Avg Price 19.25" (26 Aug) and "19.00" (30 Sep), stated per piece (19.25/1,400 lb × 100 = 1.375 ≈ $1.38/cwt). The other four match brief p5 (AMS overview, NW_LS441 2017, NW_LS448 2019, AMS_2830 2025) | OK | – |
| §2.1 | All anchors presented as "AMS report price[s]" alongside a description of the Drop Value report | Two of the six (8 Nov 2019 NW_LS448; 23 May 2025 AMS_2830) come from the **Major Packer Hide Report**, as quotes for specific weight classes (62–66 lb; **60–62 lb only** in May 2025). The other four are drop-value weighted averages. The 29% miss on 23 May 2025 may partly reflect this difference in specification | IMPRECISE | State the report and weight class of each anchor, and note the May 2025 spec difference |
| §2.1 | Nine figures not used in the fit: Peel 2013–17, 2018, H1 2019, June 2019; Brester & Swanser start 2020 and Apr 2020; Kay 2020, leatherbiz 2020b, Peck 2025 | anchors.csv has 9 non-calibration rows with these values (74.36, 47.93, 34.46, 27.60, 36.50, 18.00, 30.00, 33.00, 25.04), matching brief p5. Averages are compared with the matching window means in code | OK | – |
| §2.2 | Formula s = H / (P × W / 100) | allocation.py `share = hide / (ne*steer_lw/100)` | OK | – |
| §2.2 | P = Nebraska 65–80% Choice steers; W = FI steer dressed weight / 0.63 | Code uses 'Steers 65-80 percent Choice', Nebraska; 'Federally inspected average dressed weight' (Steers) / 0.63 | OK | – |
| §2.2 | 0.63 is "the dressing percentage used in the AMS drop-value report" | AMS PDFs: "Dressed Equivalent Basis (63.0%)" (steer) | OK | Note: AMS's own reference animal is a 1,400 lb steer (2025) or 1,375 lb (2015). The model's W is about 1,500–1,530 lb in Aug–Sep 2025 (see §3.3 row) |
| §2.2 | Annual values are means of monthly values | groupby year mean (live value = mean of monthly products) | OK | – |
| §2.2 | Output-value denominator = Choice cutout ($/cwt) × carcass weight + hide | Code: `cut*steer_dw/100 + hide`. Cutout series is 'Boxed beef cutout Choice 1-3, 600-900 pounds' | OK | Name the cutout series (Choice 1–3, 600–900 lb) |
| §2.3 (b) | "the Texas/Oklahoma/New Mexico steer price" | Code uses TX/OK/NM **Steers 35–65 percent Choice**, a lower grade than the Nebraska 65–80% series | IMPRECISE | Give the grade |
| §2.3 (a),(c),(d),(e) | Commercial all-cattle live weight; 62% and 64%; output value; k at min/max single ratio | Matches code (share_cattle_lw, share_dress62/64, share_output, k_range) | OK | – |
| §2.3 (f) / §3.3 / §4.2 | "three- and five-year trailing means"; §3.3: "**Averaging prices** over the **previous** three or five years gave 0.94% or 1.39% for 2025" | summary.py: `Y.share.rolling(w).mean()`. This is the mean of the annual **shares**, and the window **includes 2025** (2023–25, 2021–25). The 3-year value is identical to the "late" mean by definition. Averaging prices (ratio of mean hide price to mean live value, FAO-style) gives **0.91%** (3 yr) and **1.25%** (5 yr) | ERROR | Either say "mean of the annual shares for 2023–2025 / 2021–2025", or switch the code to price averaging (0.91% / 1.25%) and update §3.3, §4.2 and Table 2 |
| §2.3 | Cross-check against AMS $/cwt hide value ÷ that month's steer price | crosscheck.py: 1.38/NE Aug 2025, 1.36/NE Sep 2025 | OK | See §3.3 caveat |
| §2.3 | Log decomposition Δln s = Δln H − Δln P − Δln W, 2013→2025 | summary.py on annual means; Δln live used as P × W | OK | – |
| §2.4 | 21.3 kg CO2e/kg carcass (Rotz 2019) | params.json; brief C1 | OK | – |
| §2.4 | Hide 4.80 lb per 100 lb live (cured and fleshed; AMS 2015) | brief D1. The 2025 AMS PDFs use 4.70 and 4.77 | OK | – |
| §2.4 | 0.12 m² per kg **raw** hide (Lunesu) applied to AMS **cured and fleshed** weight | Basis mismatch: cured/fleshed weight is not raw (green) weight | IMPRECISE | Acknowledge the weight-basis mismatch |
| §2.4 | "The resulting 4.0 m² per hide" | 2025 only: 3.96 m². Range 3.3 m² (2003) to 4.0 m² (2025) | IMPRECISE | "about 3.4–4.0 m² per hide (4.0 in 2025)" |
| §2.4 | "matches the 4 m² per hide assumed in UNIDO's mass balance" | UNIDO (brief G4): 4 m² is the **raw hide area** of a 25.6 kg wet-salted hide. Finished output is about 3.5 m² grain leather per hide (5.1 m² including split). The model's hide is 33 kg | IMPRECISE (overstated agreement) | "is close to the 4 m² hide area in UNIDO's mass balance, though that refers to a lighter (25.6 kg) wet-salted hide" |
| §2.4 | Comparison at PEFCR 3.5% and 4.8% mass | params.json mass_alloc_us 0.048, pefcr 0.035 | OK | – |
| §2.4 / §3.5 | Implicit: per-m² result depends on the animal | Algebraically kg/m² = s × 21.3 × 0.63 / (0.048 × 0.12) = s × 2,330. Weights cancel exactly, so the per-m² series is the share series rescaled | IMPRECISE | State this. It also explains why mass allocation gives a flat 111.8 by construction, not because "hide weight and carcass weight grow together" empirically |

## 3. Results

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| §3.1 | k = 0.627; ratios 0.487–0.704 | 0.62678; 0.48651–0.70404 | OK | – |
| §3.1 | "Fitted prices were within 11% of **four** of the six AMS prices" | Errors −10.97, −3.86, −6.11, +28.83, −1.39, −2.05%. **Five** of six are within 11% | ERROR | "five of the six" |
| §3.1 | 23 May 2025: AMS $15.25, fitted $19.65 (29% high); LOO miss 36% | 19.65, +28.83%, LOO +35.53% | OK | – |
| §3.1 | Validation median abs error 5.8%, mean 11.5% | 5.8 / 11.5 | OK | – |
| §3.1 | April 2020: $26.83 vs "just over $18" (49% high); June 2019 21% high | 26.83, +49.0%; +21.3% | OK | – |
| §3.1 | Hide about $51 in 2002, peak annual mean $93.71 in 2014, $20.85 in 2025 | 50.75; 93.71 (max annual); 20.85 | OK | – |
| §3.2 | 5.81% in 2002; mean 4.86% 2002–13; dip 3.20% in 2009 | 5.81; 4.86; 3.20 (2008 4.50, 2010 5.11) | OK | – |
| §3.2 | 3.52% 2015, 1.98% 2020, 0.62% 2025 | OK | OK | – |
| §3.2 | 2023–25 mean 0.94%, one-fifth (5.2-fold) | 0.941%, 5.16 | OK | – |
| §3.2 | Monthly max 6.77% June 2001; min 0.51% Sept 2025 | 0.06767 at 2001-06; 0.005072 at 2025-09 | OK | – |
| §3.2 | 2013→2025: hide −76%, live value +96%, price +78%, weight +11% | −76.2, +96.3, +77.6 (224.05/126.19), +10.6 (1516.1/1370.6) | OK | – |
| §3.2 | Hide fall = 68% of log decline, live value 32% | hide_part_of_change 0.680 | OK | – |
| §3.3 | Fivefold held in every variant; early 4.47–5.05, late 0.89–0.99, 5.0–5.2-fold | summary alts | OK | – |
| §3.3 | k-scaling: early 3.77 / 5.46, late 0.73 / 1.06 | 3.771 / 5.458; 0.730 / 1.057 | OK | – |
| §3.3 | 3- and 5-year "averaging prices" 0.94% / 1.39% | Numbers are right for mean of shares, but the description is wrong (see §2.3 row) | ERROR (description) | See §2.3 fix |
| §3.3 | AMS Aug/Sep 2025 hide $1.38 / $1.36 per cwt live | PDFs: 1.38 (Aug 26) and 1.36 (Sep 30), Steer Hides Branded (Butt) | OK | – |
| §3.3 | Direct shares 0.56% / 0.57%; model 0.51% both | 0.562 / 0.567; 0.514 / 0.507 | OK | – |
| §3.3 | "The checks that bypass the price index agreed in direction and roughly in size" | (i) The Aug/Sep 2025 AMS hide prices are themselves calibration anchors, so this check is not independent of the scaling. (ii) The model–direct gap does not come from the hide price (model $18.98 / $18.61 vs AMS $19.25 / $19.00, −1 to −2%). It comes from live weight: model W = 1,503 / 1,529 lb vs AMS typical steer 1,400 lb. (iii) "Direction" has no meaning for single-month level comparisons. (iv) April 2020: model 1.81% vs about 1% (+81%), which is not "roughly in size" | IMPRECISE (overstatement) | Report as level comparisons. Say the 2025 gap reflects the AMS 1,400 lb reference weight vs the model's about 1,500 lb, and that April 2020 disagrees substantially |
| §3.3 | Peel 1 March 2024: 6.4% × 18.4% = 1.18%; model 1.01% for March 2024 | 1.1776%; 1.0118% | OK | – |
| §3.3 | April 2020 model 1.81% | 1.807% | OK | – |
| §3.4 | Mekonnen & Hoekstra 5% matches US 2000s | US 2002–08: 4.50–5.81% | OK | The price period of M&H is unknown (brief B4: Appendix V not read), and Fig 3A plots it at 2010 |
| §3.4 | Desjardins 6.8% (2006 US prices) vs US 2006 5.02% | 5.02 | OK | – |
| §3.4 | PEFCR 3.5% matches US 2015–2017 | 3.52, 3.61, 3.46 | OK | – |
| §3.4 | Italian 2.68% above US 2023 1.23%, "consistent with the higher Italian hide-to-meat price ratio" | 1.23 OK. No Italian vs US hide-to-meat price ratio is computed or cited. Lunesu gives Italian ratios only (0.70 in 2015, 0.19 in 2023) | IMPRECISE (unsupported) | Drop the clause, or cite a comparison |
| §3.4 | LWG 1.8%, UNIDO 1.5% and US 1% "bracket US values for **2020–2024**" | US 2020 1.98, **2021 2.49**, 2022 1.65, 2023 1.23, 2024 0.97. 2020–21 lie above 1.8%; 2024 is just below 1% | ERROR | "match US values for about 2022–2024" |
| §3.4 | Mass-based 4.8% and 5.88% near US 2000s share | OK (Fig 3A also shows Desjardins mass 6.2%) | OK | – |
| §3.5 | 2025 steer carries about 9,230 kg CO2e; hide about 33 kg; 4.0 m² | 9,228; 33.0 kg; 3.96 m² | OK | – |
| §3.5 | 135 (2002), 113 (2002–13 mean), 22 (2023–25), 14.5 (2025) kg CO2e/m² | 135.4; 113.2; 21.9; 14.46 | OK | – |
| §3.5 | "Nothing about the animal changed in this calculation" | Weights do vary by year in the inputs (carcass 365–433 kg) but cancel exactly in kg/m² | IMPRECISE | "Because carcass and hide weight cancel, only the price ratio moves this figure" |
| §3.5 | PEFCR 82; mass 112 "because hide weight and carcass weight grow together" | 81.54; 111.83. Both are constant because hide weight is modelled as proportional to dressed weight (4.8% × dw / 0.63); this is a modelling identity, not an empirical finding | IMPRECISE | Say "by construction" |
| §3.5 | Mass gave 7.7× economic in 2025 | 7.73 | OK | – |

## 4. Discussion, limitations, conclusion

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| §4.1 | "fell about fivefold **in a decade**" | The 5.2× is between 2002–13 and 2023–25 means. 2013→2023 is 4.1×; 2013→2025 is 8.2× in 12 years | IMPRECISE | "about fivefold between the 2000s and 2023–2025" |
| §4.1 | Hides lost three-quarters, live value doubled | −76%, +96% (2013→2025) | OK | – |
| §4.1 | "a shrinking US cattle herd and record beef prices" | No source cited for herd size. Record fed-cattle prices are shown by ERS data (2025 mean $224/cwt) | IMPRECISE | Add a citation for herd contraction |
| §4.1 | LHCA: about 15% of US hides wasted in 2024 (leatherbiz 2024) | p5 brief: "closer to 15%" in 2024; 7% in 2023 | OK | – |
| §4.1 | PEFCR gives 0% to hides that are legally waste | brief A1 | OK | – |
| §4.2 | Ratio moved "by a factor of two within the five years from 2019 to 2024" | 2.26 / 0.97 = 2.32 | IMPRECISE (minor) | "more than twofold" |
| §4.2 | 2005 vs 2025 prices differ "about eightfold" | 4.83 / 0.62 = 7.8; 112.6 / 14.5 = 7.8 | OK | – |
| §4.2 | Roncevich weights 6.8 / 8 / 14 for Italy / India / North America, 2022 exports, US = Canada assumption | brief G1 | OK | – |
| §4.2 | 14% above every US monthly value since mid-2001 (max 6.77%); US 2022 1.65% | OK | OK | – |
| §4.2 | Five-year mean for 2025 = 1.39%, "still about one-third of the 2002–2013 level" | 1.39 / 4.86 = 0.29. With FAO-style price averaging it is 1.25% (0.26) | IMPRECISE | "under a third (about 29%)", or about a quarter if price averaging is adopted |
| §4.2 / §1 | Physical/mass allocation gives "5% to 6%" | Sources in the briefs: US 4.8%, Italy 5.88%, Canada 6.2%. LHCA critique (brief A3) also lists PEFCR 7%, UNIDO 7.33%, LWG 7.8% by mass | IMPRECISE | "about 5% to 8%", or restrict explicitly to the three studies cited |
| §4.2 | Physical basis about eight times today's economic value | 4.8–6% / 0.62% = 7.7–9.7× | OK | – |
| §4.3 | "two of the scaling points come from a single quarter of 2025" | True (Aug and Sep). But **three of six** anchors are from 2025 and **none is earlier than April 2015** | IMPRECISE | State "half the anchors are from 2025; none predates 2015" |
| §4.3 | Scaling gives "roughly ±20%" uncertainty in level | k_min/k = 0.776 (−22%), k_max/k = 1.123 (+12%) | IMPRECISE | "−22% to +12%" |
| §4.3 | "although the fivefold decline does not depend on it" | True only under the assumption that the index is proportional to the butt-branded steer price throughout. The 2002–2013 level has no anchor and only one validation point (Peel 2013–17 average) | IMPRECISE (overstatement) | "does not depend on the choice of k, but does assume that the PPI tracks butt-branded steer hides back to 2002, which no pre-2013 price checks" |
| §4.3 | Output-value variant "gave nearly identical results" | Folds 5.0 vs 5.2, but levels differ: early 4.47 vs 4.86 (−8%), 2019 1.85 vs 2.26, 2021 1.71 vs 2.49 | IMPRECISE | "gave a similar decline (5.0-fold) at a slightly lower level" |
| §5 | "from about 5% in the 2000s to about 0.6% in 2025, under every denominator tested" | Early 4.47–5.05; 2025 0.61–0.66 | OK | – |
| §5 | "Most of the drop came from hide prices, and the rest from cattle prices" | Log shares: hide 68%, cattle price 27%, live weight 5% | IMPRECISE | "…the rest from higher cattle prices and heavier cattle" |
| §1 | Hide share of by-product value "two-thirds in 2000 to under a fifth by 2020" (LHCA, as reported in leatherbiz, 2020) | brief D3: 67% in 2000; "now" 15–20% (June 2020) | OK (numbers) / IMPRECISE (cite) | The citation should be "leatherbiz, 2020a"; the reference list has only 2020a/2020b |
| §1 | PEFCR 3.5%, 92.9%, "no change … allowed"; Lunesu 2.68%; LWG 1.8%, US 1%, UNIDO 1.5%; Desjardins 6.8% (2006); Roncevich 8.1%; Desjardins "roughly halved 2006–2009"; Roncevich quote | All match briefs A1, A3, B1, G1, G2 | OK | – |

## 5. Tables

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| Table 1 | All 25 rows × 8 columns | Regenerated by tables.py from reproduced results; identical to the manuscript. Spot-checked against allocation.py and carbon.py printouts | OK | – |
| Table 1 caption | "2001 covers June to December" | n = 7 | OK | – |
| Table 2 | All rows | Identical to regenerated table. k-row 2025 values 0.48 and 0.70 = 0.621% × k_min/k and × k_max/k | OK | – |
| Table 2 | "Three-/Five-year trailing mean of the main series" | Correct label for what code does (mean of annual shares, window ends in 2025). Inconsistent with §3.3 "averaging prices" | OK (table) | Align §3.3 / §4.2 text with the table, or change the method |
| Table 2 | "Choice cutout x carcass weight" | Uses letter x | IMPRECISE (cosmetic) | Use × |

## 6. Figures

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| Fig 1 | Line, six filled orange anchors, open blue "published quotes" | fig12.py plots only **6 of the 9** validation figures. The three multi-month averages (2013–17, 2018, H1 2019) are omitted, and June 2019 is a monthly average, not a quote | IMPRECISE | Caption: "Open blue circles: six published single-month prices not used in the scaling (three multi-month averages not shown)" |
| Fig 1 | Visual | No clipping or overlap. The 2015 anchor ($95.75) sits visibly above the line (fitted $85.24, −11%) | OK | – |
| Fig 2A | Band spans five alternative denominators | fig12.py: min/max of 5 alternatives, clipped to include the main series | OK | – |
| Fig 2B | Indexed 2002 = 100, log scale | Uses `iloc[1]` = 2002. Live value ends at about 388, hide at about 41 | OK | – |
| Fig 3A | Published factors at price year or publication year | PEFCR 2018, LWG 2024, UNIDO 2026, US LCA 2025, Italy 2023, Canada 2006, M&H 2010 (publication; text compares it to the "2000s"), masses 2006 / 2025 | OK | – |
| Fig 3A | Labels | "Mekonnen & Hoekstra" label is at x≈2004, y=5.55, about 6 years left of its marker (2010, 5.0), which reads ambiguously. "Canada 2006", "PEFCR 3.5%" and "UNIDO" labels touch or overlap their markers. Roncevich 8.1% is not plotted (y-limit 7) although it is central to §4.2 | IMPRECISE (layout) | Move the labels and add leader lines. Optionally extend ylim and plot 8.1%, or say in the caption it is off-scale |
| Fig 3B | Blue economic, orange PEFCR, grey mass | Mass line is dark grey dashed, as described | OK | – |
| Fig 3B | Labels | "PEFCR fixed factor (3.5%)" text extends beyond the right end of the axes (past 2025.5); it survives only because of bbox_inches='tight' | IMPRECISE (cosmetic) | Move the label left |
| Fig 3B | y-label "farm and feedlot share only" | Consistent with Rotz cradle-to-farm-gate | OK | – |

## Summary of required fixes

1. **§3.1:** "within 11% of four of the six AMS prices" should say **five** of six. Only 23 May 2025 misses.
2. **§3.3, §2.3(f), §4.2:** the trailing means are means of annual **shares**, with windows that include 2025, not "averaging prices over the previous" years. Either reword, or switch to price averaging, which gives **0.91% (3-yr) and 1.25% (5-yr)**. In that case also fix "about one-third" in §4.2 (it is 0.29 now, 0.26 with price averaging).
3. **§3.4:** LWG / UNIDO / US 1% do not bracket 2020–2024 (2020 1.98%, 2021 2.49%). Say about **2022–2024**.
4. **§3.3 cross-checks:** the Aug/Sep 2025 AMS points are calibration anchors (not independent). The 0.51% vs 0.56–0.57% gap comes from live weight (model about 1,500 lb vs AMS 1,400 lb reference steer), not hide price. April 2020 is off by +81%. Remove "agreed in direction and roughly in size".
5. **§4.3:** level uncertainty from k is **−22% / +12%**, not ±20%. The claim that the "fivefold decline does not depend on it" needs the caveat that no anchor predates 2015 and the 2002–2013 level rests on PPI proportionality.
6. **§2.1:** say that two anchors (2019, May 2025) are Major Packer Hide Report weight-class quotes (May 2025: 60–62 lb only). Also the start-date rationale: WPU0419 is WPU041 rebased, and WPU041 extends to 1926.
7. **§2.3(b):** the TX/OK/NM price is the **35–65% Choice** grade.
8. **§2.4 / §3.5:** "4.0 m² per hide" applies to 2025 only (3.3–4.0 over the period). The UNIDO 4 m² is raw area of a 25.6 kg salted hide, so it is not a match. Note the raw vs cured/fleshed weight basis. Say that weights cancel, so kg/m² = share × 2,330, and mass/PEFCR lines are flat by construction.
9. **Overstatements to soften:**
   - Social summary ("carbon footprint", "20 years", "not because cattle changed").
   - Abstract last sentence ("are snapshots of this moving ratio").
   - Abstract "nine published quotes" (four are averages).
   - §4.1 "fivefold in a decade".
   - §4.3 output variant "nearly identical".
   - §5 "rest from cattle prices" (5% is weight).
   - §3.4 Italian "hide-to-meat ratio" clause (unsupported).
   - "5% to 6%" mass range (other mass values of 7–7.8% are reported).
   - "factor of two" (2.3) for 2019–2024.
   - §4.1 herd-shrinking claim needs a citation.
10. **Abstract:** replace "between the same periods" with the explicit periods.
11. **Figures:**
    - Fig 1 caption: only 6 of the 9 checks are plotted.
    - Fig 3A: label placement (M&H label far from its marker; labels overlapping markers); consider showing or noting Roncevich 8.1%.
    - Fig 3B: PEFCR label runs past the axis.
12. **Citation and housekeeping:**
    - §1 "leatherbiz, 2020" should be 2020a.
    - Table 2: use × instead of x.
    - `tables.py` overwrites the manuscript's tables section when run; document this.

All other numbers in the abstract, text, Tables 1–2 and captions reproduce exactly from the result files. The four anchor prices verifiable against local sources ($19.25, $19.00 in the PDFs; the others in brief p5) are correct, as is the 63.0% dressing basis.
