# Number audit: "Lower economic value, same forest" (manuscript/manuscript.md)

Auditor: independent agent, 2026-10-21. Nothing in the package was edited. The pipeline was re-run on a scratch copy (build.py, analysis.py). `analysis.json` and `embodied_by_year.csv` reproduce byte-for-byte. The manuscript's Tables section is identical to `results/tables.md`.

Verdicts: OK = matches results/code. MINOR = right in substance but imprecise. WRONG = does not match. FLAG = analytical or interpretive problem.

## A. Abstract and social summary

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| Abstract | Commission attributed "2.5% to 8%" | SWD 3.2.5: 2.5% by-product, 5% co-product; 8% mass appears in fn 13 (brief §1.4) | OK | – |
| Abstract | "The 5% value share DeDuCE gives leather ... is a constant in the model's code" | DeDuCE `4. Deforestation attribution (Python)-Statistical.py` l.1661-1663, 1665-1666, 1687-1691, 1883-1884: `F_PP*0.95` / `F_PP*0.05`. The code comment says only "share 95% and 5%". It does not call the 5% a value share. Only the SWD (fn 13) calls it value-based. | OK on the constant; FLAG on "value share" | Say "the 5% share DeDuCE gives leather, which the SWD treats as a value-based co-product share". Do not imply DeDuCE claims it is a value share; the SI (basis of the 5%) has not been read (brief gap 4). |
| Abstract | Hide/beef price ratio 51% (2005) to 15% (2025) | 1.747/3.430 = 0.509; 1.412/9.692 = 0.146 | OK | See FLAG C1 (the beef price is composition-driven) |
| Abstract | Economic factor 7.1% to 2.9%, 2005-2022 | alpha_weighted 0.0713, 0.0289 | OK | – |
| Abstract | "Under the six allocation rules tested, ... 21,000 to 87,000 ha" | 21,107 (2.5%) to 87,442 (FAOSTAT mass). That range spans **7** headline rules (5 fixed + FAOSTAT mass + economic). Methods also lists 6 plus the economic rule. Fig 2 and Fig 3 show 6 rules **without** FAOSTAT mass. | WRONG count / inconsistent | Say "seven rules" everywhere, or drop FAOSTAT mass from the range (then 21,000-84,000) |
| Abstract | "two-thirds of it in Brazil" | 66.5%, computed at the 5% rule only (identical for any fixed alpha; different under economic and FAOSTAT mass) | MINOR | Add "at the 5% factor" |
| Abstract | Benefit/cost "39 to 262 under every rule and period" | Min 38.51 (2.5%, 2022); max 262.04 (FAOSTAT mass, 2015-20); all sensitivities lie between (k=0.80 2022: 41.8; unamortised 2022: 43.3) | OK (rounding) | "about 39 to 262"; see FLAG E1 on interpretation |
| Social summary | "Even then, benefits beat costs 39-fold" | 39 is the minimum over all rules (2.5% in 2022). Under the low-value economic rule it is 48 (2022) or 117 (2015-20). | MINOR / overstated framing | "Even under the lowest allocation tested, the Commission's own figures put benefits at ~39x costs" |

## B. Introduction and Methods

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| §1 | "After two delays" | 2025/2650 confirmed. The 2024/3234 delay is marked UNVERIFIED in the brief. | CHECK | Verify CELEX 32024R3234 before submission |
| §1 | SWD figures 2.5/5/8%, €979m-€1,957m, €16.7m | Brief §1.4 (SWD pp. 18-19, Annex II). Sums 978,468-1,956,936 k€; 16,741.51 k€. | OK | – |
| §1 | "Peer-reviewed estimates of EU leather's deforestation footprint have used mass allocation" | Only one peer-reviewed study is cited (Laroche, 10% mass). DeDuCE (Nature Food, peer-reviewed) uses 5%, which the manuscript itself calls "value-based". | WRONG / internally inconsistent | "The one peer-reviewed estimate specific to EU hides (Laroche et al., 2024) used mass allocation ..." |
| §1 | Laroche: 10%, 1,200-31,000 ha/yr, 2018-2020, upper figure incl. derived goods | Brief §3.1 (Sec 2.3.4, Sec 3.2 p.7) | OK | Laroche also cites "market-value estimates of 5-15%". It would be fair to say so. |
| §1 | US hide value share fell "about fivefold" 2002-13 to 2023-25 | 4.9% to 0.9% = 5.4x (caller-provided companion figures) | OK | – |
| §1 | Lunesu: "similar fall in Italian hide-to-meat price ratios" | Dairy-cow hide/meat price ratio 0.70 (2015) to 0.19 (2023) | OK | Specify "dairy-cow" |
| §2.1 | "imports from every extra-EU partner" | build.py drops: **Namibia** (pandas reads partner code "NA" as NaN, 126 rows); Serbia (XS), Kosovo (XK), Montenegro (XM), CS, AN; Q-codes. Mapped total = 98.0% of the `EXT_EU27_2020` aggregate. Aggregates (EXT_/INT_EU27_2020) are correctly excluded, so there is no double counting. | MINOR | Use `keep_default_na=False` in build.py and map XS→SRB, XK, XM→MNE. Effect at 5%: Namibia ~1 ha/yr, Serbia+Montenegro ~13 ha/yr (2015-20). |
| §2.1 | Conversion factors 1.00/2.33/4.20 | common.py RHE; SWD Annex II (brief l.65-67) | OK | – |
| §2.1 | Hide price = 4101; beef = 0201+0202 | build.py l.43-47. 4101 includes all HS6 lines (410190 has a unit value of ~€0.07-0.13/kg). HS 4101/4104/4107 also cover **equine** (and buffalo) hides. This is not handled and not disclosed. | FLAG | Add the equine/buffalo limitation |
| §2.1 | DeDuCE 5-yr amortised "deforestation risk", meat+leather summed | build.py l.6-10 | OK | Note: amortised values are zero/blank for 2001-2004, so the series effectively runs 2005-2022 |
| §2.1 | DeDuCE "in the version distributed with the trade data of Singh et al. (2024)" | x9p8-deduce-readme.csv describes that file (attribution + trade tabs) | OK | – |
| §2.2 | h = alpha·D/H; EU = Σ RHE·h; exporter attribution | analysis.py l.15-23 | OK | – |
| §2.3 | Economic formula, k = 0.70, P_hide = all extra-EU 4101, P_beef from origin else all origins | analysis.py l.9-12 | OK formula; WRONG description of the fallback | The beef file has only 15 origins (AR AU BO BR CA CN CO IN MX NG NZ PK PY US UY). Every other origin (VEN, KEN, ZAF, NIC, RUS, BIH, PER, PAN, GBR …) gets the world price because it was **not downloaded**, not because it "sold no beef to the EU". Origin prices also come from tiny volumes: CO 2018 = 0.13 t (€62.88/kg), CO 2017 = 0.04 t, BO 2019 = 0.4 t, PY 2012 = 7 t. Add a minimum-volume rule (e.g. ≥100 t) and describe the fallback correctly. |
| §2.3 | "Sensitivity ... all-origin beef price, unamortised" | Implemented | OK | – |
| §2.3 / §3.2 | Mass share "computed from FAOSTAT hide and carcass weights" / "about 9% throughout" | Brazil 9.0-9.3%. Import-weighted across deforestation origins: **10.0-10.6%**. Paraguay 13.5%, Bolivia 12.7%, origin mean 12.1%. This is why FAOSTAT-mass hectares (87,442) exceed the 10% rule (84,430). | WRONG | "about 9% for Brazil and 10-11% import-weighted" |
| §2.4 | €50,170/ha = summed benefits / summed ha | (978,468+1,956,936) k€ / (19,504+39,005) ha = €50,170.13/ha (brief Annex II rows). Row-level values differ: 4101 ≈ €39,900/ha, 4104 ≈ €50,100/ha, 4107 ≈ €52,600/ha, because they embed carbon at €100/t with origin-specific emission intensities. | OK (FLAG wording) | State that it is a pooled average that includes carbon, and that it was applied to a different origin and year mix |
| §2.4 | Cost €16.7m | 16,741.51 k€ (sum of 740.63+3,843.23+12,157.65) | OK | – |
| §2.5 | Python 3.13, pandas, NumPy, pycountry, matplotlib | Matches imports / __pycache__ cpython-313 | OK | – |

## C. Results

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| §3.1 | 5.0% in every one of 2,620 country-years with cattle deforestation | deduce_cattle.csv: amort_cattle > 0 in 2,620 rows (all 2005-2022), share 0.049999999-0.0500000. With unamortised data: 2,679 country-years, also 5.0%. | OK | Say "amortised, 2005-2022" |
| §3.1 | Code assigns 95/5 to deforestation, emissions and peat drainage as fixed multipliers | Lines cited above (area via `Production_attribution`; biomass, SOC top/sub, peatland) | OK | Cite file line numbers and commit 48e4b5a (24 Apr 2026). The reference says "Version 1.0.1, 2024"; the cloned code is a 2026 commit. |
| §3.1 | "therefore a fixed parameter, not a measurement of the value of hides" | Constant is correct. Whether the 5% was originally derived from value data is unknown (SI unread). | FLAG (overstatement risk) | Soften: "a fixed parameter applied to every country and year; whatever its derivation, it cannot track changes in hide value" |
| §3.2 | Hides €1.75 (2005) / €1.41 (2025); beef €3.43 / €9.69; ratio 0.51/0.15 | prices_eu_import.csv | OK | – |
| §3.2 | Weighted factor 7.1% (2005), peak 8.7% (2006), 4.3-6.1% (2008-18), 2.8-3.0% (2020-22) | 0.0713; 0.0866; 0.0426-0.0606; 0.0279-0.0303 | OK | – |
| §3.2 | Brazil 8.3% (2005), 2.8% (2022), 3.0% (2024) | 0.0835, 0.0282, 0.0305 | OK | Note Brazil peaked at 10.1% in 2006 |
| §3.3 | 1.37m t (2005), 0.96m (2022), 0.74m (2025) RHE | Mapped partners: 1,365,652; 962,029; 740,388. Extra-EU aggregate: 1,392,490; 981,669; 755,105. | MINOR | Use the aggregate (1.39 / 0.98 / 0.76) or say "from identified partner countries" |
| §3.3 | Coverage 96-97% every year | 0.957-0.972 of **mapped** imports. Relative to the EXT_EU27_2020 total: 93.5-95.5%. Uncovered includes India (FAOSTAT cattle hides/beef missing, flag M, all years, while DeDuCE gives India ~15,550 ha/yr cattle deforestation and EU imports ~39,000 t RHE/yr), Nepal, Sudan ("SDN and SSD" ISO in DeDuCE does not match), and Serbia ("SRB and MNE"). | MINOR | "94-96% of extra-EU imports"; name India as excluded |
| §3.3 | 42,215 ha at 5%, "within 8%" of SWD 39,005 | 42,215/39,005 = 1.082 | MINOR | "about 8% above" |
| §3.3 | Brazil 66.5%, Paraguay 21.3%, Bolivia 5.3% | 0.6650, 0.2125, 0.0528 | OK | – |
| §3.3 | Range 21,107 (2.5%) to 87,442 (FAOSTAT mass), "across the six rules", "fourfold" | Correct values; 4.14x. There are seven rules. | WRONG count | "seven rules" |
| §3.3 | "economic rule tracked the 5% line until about 2018 and then fell below it" | Economic vs 5%: 2005 92,151 vs 55,139; 2006 139,231 vs 68,994 (above even the 10% line, 137,987); 2007 93,312 vs 58,494; 2013 63,038 vs 46,791; 2009-2010 below. | WRONG | "well above the 5% line in 2005-2008 and 2013-14, close to it in 2015-2018, below it from 2019" |
| §3.3 | 2022: economic 15,885; 5% 25,702; mass 51,718 | embodied_by_year.csv | OK | "mass" = FAOSTAT-weights mass (Laroche 10% = 51,405) |
| §3.4 | 2015-20 BCR 63 to 262, economic 117; 2022 39 to 155, economic 48 | 63.25 / 262.04 / 116.90; 38.51 / 154.99 / 47.60 | OK | – |
| §3.4 | Break-even alpha 0.04%, "about one-sixtieth" of 2.5% | 0.0395% (2015-20 base); 2.5/0.0395 = 63. For 2022 it is 0.065%. | OK | State the base period |
| §4.1 | "raw hides losing two-thirds of their value relative to beef" | Ratio fell 71% | MINOR | "more than two-thirds" |
| §4.1 | Factor fell "by more than half"; 2022 ≈ 2.9%, BCR ≈ 48 | 7.1→2.9 = −59%; 47.6 | OK | – |
| §4.2 | 5% understated value share 2005-08, 2011, 2013-14; overstated every year from 2015 | Weighted alpha > 5%: 2005-08, 2011 (5.06), 2013-14; < 5% 2009-10, 2012 (4.96), 2015-22 | OK | 2011/2012 lie within ±0.1 pp of 5%. Say "roughly equal". |
| §4.3 | "FAOSTAT hide weights and production for some countries are imputed" | Hide production is flagged **I (imputed) in 4,588 of 5,493 records**, and in all 18 years for Brazil, Paraguay, Bolivia, Colombia and Venezuela, at a fixed ratio to beef output (BRA 0.100, PRY 0.156, BOL 0.146, COL 0.120, VEN 0.122) | WRONG (understated) | See FLAG C2 |
| §4.3 | "Brazil's series shows a level break around 2020" | Brazil slaughter 40.65m (2019) → 29.89m (2020), carcass 202 → 262 kg/head, hide 20 → 26 kg/head. Production is continuous. Alpha depends only on the hide/carcass ratio (fixed at 0.10), so the break does not move results. | OK | Say it does not affect results |
| §5 | "from about 7% to about 3% over 2005-2022" | 7.1 → 2.9 | OK | – |
| Ref list | DeDuCE data "(Zenodo, CC BY 4.0)" | The trade dataset 10633818 is CC BY 4.0. The attribution dataset 13624636 is CC BY-NC. The package uses the former's attribution tab. | OK | – |

## D. Tables and figures

| Location | Claim | Verdict | Fix |
|---|---|---|---|
| Table 1, all 11 rows × 4 columns | Match analysis.json (rounded) | OK | – |
| Table 1 caption | €50,170/ha, €16.7m | OK | Add "pooled; includes carbon" |
| Table 2, all rows | Match analysis.json; 2023/2024 Brazil alpha exist while the weighted value is "–" (no DeDuCE after 2022) | OK | Footnote why 2023-24 weighted is blank |
| Fig 1A | Plotted ratio matches; y-axis label "(EU import unit values, EUR/kg)" on a dimensionless ratio | MINOR | "ratio of EU import unit values" |
| Fig 1B | Lines match; Brazil extends to 2024 and reaches 10.1% in 2006 (not in text) | OK | – |
| Fig 2 | Six lines; caption "six allocation rules". FAOSTAT mass (the abstract's 87,000 upper bound) is not shown. The SWD band (2024 trade × 2015-20 deforestation) is drawn across all years. | MINOR | Add FAOSTAT mass or change the abstract; note the band is a single-period benchmark |
| Fig 3 | Six rules; FAOSTAT mass (262/155, cited in text) and sensitivities absent. Caption says "each allocation rule". | MINOR | Add the row or change the caption to "six headline rules" |

## E. Analytical / interpretive flags (beyond arithmetic)

- **C1 (high).** The beef price is an import-composition series, not a price trend. EU beef imports from Brazil fell from 159,010 t (2007) to 36,399 t (2008), and the Brazil beef unit value jumped from €4.51 to €5.58/kg. The world EU beef unit value nearly doubled 2005→2008 (3.43→6.36). Much of the 2005-2009 fall in alpha (and in the "51%→15%" ratio) reflects a shift in which beef the EU imported (fewer cheap frozen cuts), not carcass value. The Limitations mention boneless cuts but not composition shifts. Add a check, e.g. a FAOSTAT producer price or a fixed-composition index, or state it as a limitation and avoid causal "hides cheapened" language for 2005-2009.
- **C2 (high).** FAOSTAT hide output and hide weights are FAO imputations at a fixed national ratio to beef. As a result, (a) "Mass, FAOSTAT weights" is FAO's imputation coefficient, not a measured mass share; (b) the hide denominator H is effectively r_c × beef output, so ha per tonne of hide inherits r_c (Paraguay's 0.156 lowers its h but raises its alpha); (c) "FAOSTAT weights" add no time variation, so the economic factor varies only through prices. Disclose this.
- **C3 (medium).** The economic alpha mixes a single EU-wide hide price (all origins, including equine and low-value 410190) with origin-specific beef prices. Origins selling cheap beef to the EU (Paraguay) get higher alpha. Origin beef prices from <1 t of trade (Colombia, Bolivia) are used without a floor. If the origin is missing, world beef is used (confirmed: analysis.py l.10 `fillna(p_beef_world)`), for most origins.
- **C4 (low).** Silent exclusions: India (no FAOSTAT cattle hides), Namibia (NA parsing bug), Sudan/Serbia (composite DeDuCE ISO). The hectare effect is negligible (well under 1%), but coverage statements should reflect it.
- **C5 (low).** No `XX`/aggregate partner codes are mapped to countries. pycountry returns None for EXT_/INT_EU27_2020, Q*, XS, XK, XM, CS, AN. FAOSTAT "China" (M49 159), "Sudan (former)" and "Serbia and Montenegro" are unmapped, so there is no double counting with "China, mainland" (156→CHN). No iso3 is produced twice. Intra-EU partners are correctly removed (Greece appears as GR, which matches the list).
- **E1 (high, interpretation).** "the environmental benefit of keeping leather in scope exceeded its compliance cost" (abstract, §3.4, §5) presents the SWD's gross benefit as a realised benefit. That benefit assumes inclusion avoids 100% of embodied deforestation (no leakage to non-EU buyers, full compliance). The cost covers recurring operator compliance only, at the 2024 operator count. The paper's own Limitations call this "internal consistency of the Commission's own assessment". The abstract and conclusion should say the same, e.g. "on the Commission's own valuation, the estimated benefit would exceed ...".
- **E2 (medium).** "The 5% is a constant" (§3.1 heading and abstract) is true of the code. The step to "not a measurement of value" is an inference: a fixed value share can still be value-derived (e.g. from a literature average). The SI has not been read. Rephrase as above.
- **E3 (medium).** Comparing the 42,215 ha (2015-20 trade × 2015-20 deforestation) with the SWD's 39,005 (2024 trade × 2015-20 deforestation) is correctly caveated. But the Fig 2 band suggests a time-comparable benchmark.
- **E4 (low).** Exporter attribution of 4104/4107 from tanning countries applies the tanning country's national ha per tonne of hide. This is stated, and it is one direction of bias. Fine.

## Prioritized fix list

1. **Rule count (abstract, §2.3, §3.3, Fig 2/3 captions):** say "seven" rules consistently, or drop FAOSTAT mass from the abstract's 21,000-87,000 and 39-262 ranges (without it: 21,107-84,430 ha; BCR 39-253).
2. **"Mass shares from FAOSTAT weights were about 9% throughout"** → Brazil ~9%; import-weighted 10.0-10.6%; Paraguay 13.5%. Also disclose that these are FAO imputation ratios (C2) and correct the Limitations ("for some countries" → nearly all, including every major supplier).
3. **"The economic rule tracked the 5% line until about 2018"** → wrong. It was 1.7-2.0x the 5% line in 2005-2007 and above it in 2013-14.
4. **Benefit-cost framing (abstract, §3.4, §5, social summary):** make clear these are the Commission's gross-benefit assumptions (100% effectiveness, no leakage), not realised benefits. Fix "Even then ... 39-fold" (39 is the 2.5%/2022 minimum; the economic rule gives 48).
5. **Beef price composition (C1):** add a limitation or a robustness check. The 2005-2009 drop in the ratio and in alpha is partly driven by EU beef import mix (Brazil volumes −77% 2007→2008).
6. **"Peer-reviewed estimates ... have used mass allocation"** → only Laroche et al. Avoid the plural, which conflicts with the Nature Food DeDuCE 5% being called value-based.
7. **"The 5% is a constant" / "value share DeDuCE gives leather"** → attribute the "value-based" label to the SWD. Soften "not a measurement of value" pending the SI. Cite file line numbers and commit 48e4b5a.
8. **Beef fallback description (§2.3):** fallback = origins not downloaded (only 15 origins fetched), not "sold no beef". Add a minimum-volume threshold (Colombia 2018 used 0.13 t at €62.88/kg).
9. **Coverage and totals:** 96-97% is of mapped partners; versus the Extra-EU total it is 93.5-95.5%. Totals 1.39/0.98/0.76m t on the aggregate. Fix the Namibia "NA" parsing in build.py (`keep_default_na=False`). Name India's exclusion.
10. **Equine/buffalo:** HS 4101/4104/4107 include equine hides. Add to Limitations.
11. Small wording: "within 8%" → "about 8% above"; "two-thirds" → "more than two-thirds"; Fig 1A axis label (ratio, not EUR/kg); Fig 2 band note; verify Reg. 2024/3234 ("two delays").

All headline arithmetic (Table 1, Table 2, §3.2 and §3.4 values, the €50,170/ha and €16.7m derivations, 2,620 country-years, Brazil/Paraguay/Bolivia shares, break-even 0.04%) reproduces exactly from the code and raw data.
