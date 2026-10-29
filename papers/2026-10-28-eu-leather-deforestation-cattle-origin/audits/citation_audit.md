# Citation audit: "Where the cattle were raised" (paper 14)

Audited file: `/home/claude/p14/pkg/manuscript/manuscript.md` (not edited).
Auditor: independent AI agent, 22 October 2026. I used the scoping brief (`/home/claude/p14/lit/brief.md`) only as a map. For shared EU legal sources I relied on the paper 8 audit (`/home/claude/p8/pkg/audits/citation_audit.md`, 21 October 2026), and re-checked the parts this paper relies on.

## How sources were read

Bash egress was blocked (proxy 403 on api.crossref.org), so I used three other routes.

**Read directly by me**
- Laroche et al. supplement code, `01_calculations.R`, all 307 lines.
- Laroche supplement files `conversion_factors_leather.csv` and the published output `out_mean.rds`, read with pyreadr.
- DeDuCE v2.1 `about.pdf` (the Zenodo file "0. About the data.pdf") and `ReadMe.txt`.
- DeDuCE v2.1 attribution extract and the v2.0 readme.
- BACI v202601 `readme.csv`.
- FAOSTAT hide extract, including its flags.
- The full DeDuCE v2.1 physical trade file (61.5 MB). I fetched it in a Chrome tab on zenodo.org with JavaScript and scanned every row.
- The SWD PDF. I fetched it in Chrome on environment.ec.europa.eu and extracted the text with pdf.js. I read pages 18–19, 28, 31 and 35 (printed numbers) directly.
- Zenodo API records for 11085413 and 18953516.
- The live x9m8.com page of paper 8.

**Read via WebFetch** (quotes extracted by a helper model; accurate in substance)
- Laroche et al. 2024, full text (Chalmers OA PDF).
- Mammadova et al. 2020, full text (MDPI HTML).
- Buljan et al. 2000, UNIDO PDF.
- CEPII BACI web page.
- Singh & Persson 2026, PMC full text.
- Crossref and DataCite APIs.
- OpenAlex searches.

**Not read**
- Kastner et al. 2011 beyond its Crossref metadata. Its algorithm is checked through Laroche's code, which implements it as `trace.origins` and labels it "function from Kastner et al. 2011 paper".

Verdict key:
- **OK**: supported as written.
- **MINOR**: supported, but the wording or reference needs tightening.
- **FIX**: wrong or misleading.
- **UNVERIFIED**: could not be checked.

---

## 1. Claims table

| # | Manuscript claim (location) | Source checked | Evidence (verbatim where possible) | Verdict | Fix |
|---|---|---|---|---|---|
| 1 | "The European Commission's assessment … attributes direct imports of hides and leather to the exporting country, so leather tanned or made into goods elsewhere is credited to the processing country or left out" (Abstract; also §1 ¶1 "attributed to the exporting country"; §2.4 "The exporter model follows the Commission's assessment") | SWD draft-labelled PDF, Annex I, printed pp. 28 and 31 (PDF pp. 29, 32) | p. 28: D_p is "the summed product of the deforestation intensity I r,c,p of raw commodity r in country c, the volume of the derived product placed on the EU market … M p,c, and the conversion factor f p over time period 2015-2020". p. 31: the raw intensity "is only valid for derived products under the assumption that the country of origin is the same as the country of production … a separate deforestation intensity factor is computed for derived products. This derived-product intensity factor I derived … combining the domestic deforestation occurring in the country where the product is processed, the imported deforestation embodied in the raw commodities sourced V in from other countries, and exported deforestation associated with raw commodities exported V out for further processing". Then: "For leather products, limited statistics are available in FAOSTAT. Therefore, bilateral trade statistics from UN Comtrade were used to capture leather-related trade flows." | **FIX** | The SWD does **not** describe pure exporter attribution. It describes a one-step origin adjustment: the partner country's intensity is blended with the intensity of the raw hides that partner imports, using Comtrade for leather. Annex II does not show whether, or how, I_derived was applied to 4104 and 4107. What is true is that the SWD (i) covers only direct imports of 4101, 4104 and 4107, with no goods, (ii) does not deduct EU exports, and (iii) does not trace beyond one trade step. Rewrite the Abstract, §1 and §2.4. Suggested text: "The Commission's assessment counts only direct EU imports of hides and leather, charged at the deforestation intensity of the partner country (adjusted, in its stated method, for that country's own raw-hide imports), and ignores leather goods and EU exports." Name the paper's comparator "exporter attribution (the method of the companion paper)" rather than "the Commission's method". The 37,727 vs 39,005 ha match in §3.3 shows the two are numerically close; say so, without asserting they are the same method. |
| 2 | SWD put embodied deforestation at "roughly 19,500 to 39,000 hectares a year … using average 2015–2020 imports" (§1) | SWD Annex II (printed p. 35); paper 8 audit #11–12 | Rows: 4101 "283-565", 4104 "17,495-34,989", 4107 "1,726-3,451" ha. p. 28: "over time period 2015-2020" | OK, apart from the attribution wording | The sum of 19,504–39,005 is derived, not printed. Drop "attributed to the exporting country" (see #1). |
| 3 | Importers of finished leather goods "such as footwear and handbags" would not face equivalent due diligence; derived products "cannot be considered at this stage" (European Commission, 2026, p. 19) (§1) | SWD, printed p. 18 = PDF p. 19 | "importers of finished leather goods (such as footwear, handbags or other articles) could continue to place them on the Union market w[ithout]…"; "The inclusion of derived products to address this situation cannot be considered at this stage due to the specificities of the sector including the high number of new products…" | MINOR | The quote is exact. The printed page number is **18**; 19 is the PDF page. APA uses the printed number: change to "p. 18". |
| 4 | Original Annex I listed 4101, 4104, 4107; removed by Delegated Regulation (EU) 2026/2102 "in 2026" (§1) | Paper 8 audit #1, #3, #25 (EUR-Lex) | Entries "ex 4101 … ex 4104 … ex 4107" deleted; adopted 13 July 2026; OJ L 2026/2102, 17.9.2026; in force 18.9.2026 | OK | Optional: "ex" headings (cattle only); in force 18 September 2026. |
| 5 | EUDR covers placing on the market and export (§1) | Reg. 2023/1115 title | "…on the making available on the Union market and the export from the Union of certain commodities…" | OK | — |
| 6 | Companion paper: "leather tanned in a third country from South American hides was assigned to the tanning country" (Kalafatis, 2026) (§1) | x9m8.com live page, read in Chrome | "Embodied deforestation is attributed to the exporting country, not the country of cattle origin, so leather tanned in third countries from South American hides is assigned to the tanning country." | OK | — |
| 7 | Brazilian wet-blue is finished in Italy (Mammadova et al., 2020) (§1); "customs-level studies show specific Brazil–Italy chains" (§4.4) | Mammadova et al. 2020, full text | "Most of the Italian imports of Brazilian leather are in a semi-processed form (i.e., wet-blue)"; customs data "for the period of August 2017–August 2018, based on customs declarations"; "Crossmatch of the customs data on both sides shows that the biggest consignee on the Italian side…" | OK / MINOR | §4.4: this is one study and one year of customs data, and its link to the Veneto district is inferred. Suggest "a customs-level study of one year shows specific Brazil–Italy links". |
| 8 | Laroche et al. extended Kastner et al. (2011) to derived products incl. leather goods using BACI (§1) | Laroche 2024 full text, pp. 2, 5 | "using the method of Kastner et al. (2011)"; "We use bilateral trade flow data from the BACI (2024) database" | OK | — |
| 9 | In Laroche's code all leather products, converted to RHE, enter one trade matrix traced once against FAOSTAT hide production (supplement file 01_calculations.R) (§1, §2.4) | `01_calculations.R`, lines 145–149 and 227–237 | `curr.trade[processing.level > considered.stage, CF := 0]` … `curr.trade <- curr.trade[, .(tons = sum(tons)), by = c("j","i")]` … `check <- trace.origins(curr.trade, curr.production[,.(BACI.Code, p)])`; production = FAO items 919 and 957 | OK | Cite the supplement as its own reference (see §4: Kastner et al., 2024), not as "Laroche et al., 2024, supplement…". |
| 10 | Laroche 2018–2020: ~1,220 kt; one-third EU, 13% Brazil, 12% China, 8% India; 1,200–31,000 ha depending on products; 10% allocated (§1) | Laroche full text pp. 5, 6, 8; `out_mean.rds` recomputed | "causes a net increase in the EU's apparent consumption of hides to 1220 thousand tons"; "One-third of these hides originates directly from the EU, 13% from Brazil, 12% from China, 8% from India"; "~1200 to 31,000 ha of forest annually"; "we attribute 10% of total pasture expansion deforestation to cattle and buffalo hides." rds, EU (5707), 2018–2020 mean: level 4 = 1,220,483 t, 30,979 ha; level 1 = 1,235 ha; origin shares 34.5 / 12.7 / 12.3 / 8.5% | OK | — |
| 11 | Supplement holds annual results 2012–2022 (§1) | `out_mean.rds`; article p. 4 | Years in rds: 2012…2022. Article: "Results for all countries for the years 2012–2022 are available at" [Zenodo] | OK | — |
| 12 | BACI v202601, HS 2002; reconciles exporter and importer reports; values and quantities in tonnes (Gaulier & Zignago, 2010) (§2.1) | BACI readme.csv; CEPII page | "Version: 202601 / Release Date: 2026 01 22"; "Values in thousand USD and quantities in metric tons"; reference "Gaulier, G. and Zignago, S. (2010) … CEPII Working Paper, N°2010-23" | OK | — |
| 13 | "Quantities were cleaned as in Laroche et al. (2024): where a flow's unit value was more than 20 times above or below the median …, **or the quantity was missing**, the quantity was replaced by value divided by the median unit value" (§2.1) | `01_calculations.R` lines 177–192; article text | Code: `trade.data <- trade.data[!is.na(q)]` ("exclude cases without quantity or value"), then `threshold.factor <- 20` and `q := v / unit.price.median`. The article text does not describe the cleaning. | **FIX** | Only the 20× outlier rule is "as in Laroche". Laroche **dropped** flows with missing quantity, which §2.7 itself says. Reword: "Outlier quantities were replaced following the supplement code of Kastner et al. (2024): … Unlike that code, flows with missing quantities were imputed in the same way rather than dropped." |
| 14 | Hide production = FAOSTAT cattle + buffalo hides, as in Laroche; India has no cattle-hide output in FAOSTAT (§2.1) | Laroche code line 146 (`fao.production.codes <- c(919, 957)`); local FAOSTAT extract | India: "Raw hides and skins of buffaloes" 25 records; "Raw hides and skins of cattle" 0 records | OK | — |
| 15 | "None of the 2005–2024 production records used is flagged as an official figure; almost all are imputed" (§2.1) | Local FAOSTAT extract, items 919 and 957, Production, 2005–2024 | Flags: I = 4,150; E = 1,095; M = 154; no A (official) | MINOR | "Almost all" overstates it: about 79% of valued records are imputed (I) and 21% estimated (E). Suggest "none is flagged as official; about four-fifths are imputed and the rest estimated". |
| 16 | DeDuCE v2.1 (Singh et al., 2026), five-year amortised "deforestation risk", 2005–2023, "Cattle meat" + "Leather" rows; leather share fixed at 5.0% as in v2.0 (§2.1) | v2.1 attribution extract; About the data | Columns include "Deforestation risk, amortized (ha)"; commodities ['Cattle meat', 'Leather']; leather/(meat + leather) = 0.0500 in 2,867 country-years (min 0.04999999999998, max 0.05000000000001). About: "amortised over 5 years, available from 2005 onwards" | OK | — |
| 17 | v2.1 documentation says leather and wood are excluded from DeDuCE's physical trade model because FAOSTAT has no bilateral trade data; the v2.1 physical file has "Cattle meat" but no leather rows (§2.1) | About the data.pdf, p. 1–2; full physical CSV scanned (414,730 lines) | "As FAOSTAT does not provide bilateral trade data for leather and wood products, these items are excluded from this dataset." The only cattle commodity in the file is "Cattle meat" (19,996 rows); there are no leather or hide rows. | OK | — |
| 18 | Licence of v2.1 is CC BY 4.0 "on Zenodo and in its 'About the data' file" (§2.1) | Zenodo API; DataCite; About PDF p. 3 | Zenodo/DataCite: "cc-by-4.0". About: "This dataset is licensed under the Creative Commons Attribution license, which allows others to remix, adapt, and build upon the work as long as they credit the original creators." No version number. | MINOR | The About file names CC BY without a version. Write: "CC BY 4.0 on Zenodo; the 'About the data' file says Creative Commons Attribution". |
| 19 | v2.0 readme says CC BY-NC-SA; Zenodo record says CC BY 4.0 (§2.1) | Local v2.0 readme line 43; DataCite 10633818 | "This dataset is copyrighted under the Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) license"; DataCite "cc-by-4.0" | OK | — |
| 20 | Laroche mean factors: 1.00 for raw and wet-blue, 4.02 for crust and finished, 1.03–4.02 for articles; min and max sets (§2.2) | `conversion_factors_leather.csv` | 4101xx = 1; 410411/410419 = 1; 410441/410449 = 4.02; 4107xx = 4.02; article CFmean range 1.03 (640312) to 4.02 | OK | — |
| 21 | SWD factors 1.00, 2.33, 4.20 (§2.2) | SWD Annex II (printed p. 35) | "4101 1.00 … 4104 2.33 … 4107 4.20" | OK | — |
| 22 | UNIDO: 1,000 kg wet-salted gives 350 kg shaved wet-blue (262 grain + 88 split) and 255 kg finished (195 + 60), giving 2.86 and 3.92 (Buljan et al., 2000) (§2.2) | Buljan, Reich & Ludvik 2000, UNIDO PDF | "Shaved weight, grain: 262 kg"; "Shaved weight, split: 88 kg"; "Finished leather, grain: 195 kg - 138 m2"; "Finished leather, split: 60 kg - 60 m2" (p. 4; also Fig. 7 p. 9, §5.5 p. 19). 1000/350 = 2.857; 1000/255 = 3.92 | OK | — |
| 23 | Laroche "state that they assume 'at least three-quarters' of leather goods are bovine; whether their factors already include this is not stated" (§2.2) | Laroche p. 5; CSV | "we assume that at least three-quarters of these traded goods are manufactured from bovine hides." It refers to goods described only as "leather", not to all leather goods. CSV: pure-leather articles (4203.10, 4203.30, 4203.40, 4205) carry 4.02, the same as finished leather. | MINOR | Write "goods described only as 'leather'". You can also add that the factors appear not to include a 0.75 scaling, because articles made wholly of leather carry the finished-leather factor of 4.02. That is an inference, so label it as one. |
| 24 | Kastner et al. (2011) re-export algorithm, R = (I − T diag(x)^−1)^−1 P (§2.3) | Laroche code `trace.origins` (an implementation of Kastner 2011); Crossref metadata | `A <- trade.matrix %*% diag(einsdurchx)`; `R <- solve(diag(nrow(A))-A) %*% diag(production.vector)`; `R_bar <- diag(c) %*% R` | OK (via implementation) | — |
| 25 | Allocation rules: 2.5% and 5% (Commission by-product and co-product), 3.5% PEFCR, 8% Commission mass, 10% Laroche; economic rule with boneless yield 0.70 (Kalafatis, 2026) (§2.5) | Paper 8 audit #4–6, #27; paper 8 manuscript line 54; Laroche p. 5 | Paper 8: "*k* = 0.70 the share of carcass weight sold as boneless beef"; SWD 2.5% / 5% / 8% verified; PEFCR "Hides and skins: 3,5%" | MINOR | The PEFCR is named but not in the reference list. Add De Rosa-Giglio et al. (2018), or make clear the rules are taken from Kalafatis (2026). |
| 26 | Pooled comparator "replicates the method of Laroche et al." (§2.4); validation differences "BACI HS 2012 (version 202401), DeDuCE version 1.0 and dropped flows without quantities" (§2.7) | Laroche code lines 30, 182, 250; CSV processing levels; `pkg/code/common.py` | Code: "BACI_HS12_V202401.zip"; "DeDuCE_Deforestation_attribution_v1.0.0 (2001-2022).xlsx"; `!is.na(q)`. Laroche includes 411420, 411510 and 411520 at processing level 3 in its core run; this paper's pooled core leaves them out (`EXTRA3`, sensitivity only). Laroche's FAOSTAT download is dated 20231227. | **FIX** (omission) | Add to §2.7: "and their core includes patent and composition leather and leather waste (4114.20, 4115), which this replication adds only in a sensitivity run; they also used an older FAOSTAT vintage (December 2023)". The listed differences are otherwise correct. |
| 27 | Laroche published output for 2018–2020: 1,220 kt; EU 34.5%, Brazil 12.7%, China 12.3%, India 8.5%; 30,979 ha at 10% (§3.6) | `out_mean.rds` recomputed | 1,220,483 t; 30,979.4 ha; 0.3446 / 0.1270 / 0.1229 / 0.0853 | OK | Name the file in full: `output/apparent_consumption_leather_embodied_deforestation_HS12codes_2012-2022_different_processing_levels_mean.rds` (inside `supplement.zip`). |
| 28 | "DeDuCE's authors caution that its recent years are less reliable" (§4.4) | v2.0 explainer (paper 8 audit #21); v2.1 About file; Singh & Persson 2026 (PMC) | v2.0: "we strongly caution against drawing policy conclusions based on trends in the data for the last few years of the time-series (especially for years 2021-2022…)". The v2.1 About file contains **no** such caution; I found none in Singh & Persson 2026. | MINOR | Attribute it precisely: "the authors cautioned, for v2.0, against relying on trends in 2021–2022 (Singh et al., 2024); the v2.1 documentation does not repeat this". |
| 29 | Sources and licences in Transparency: BACI Etalab 2.0; DeDuCE v2.1 and v2.0 CC BY 4.0 on Zenodo; Laroche supplement CC BY 4.0 on Zenodo | CEPII page; Zenodo/DataCite | "BACI is distributed under the Etalab Open Licence 2.0"; 18953516, 10633818 and 11085413 all "cc-by-4.0" | OK | Optional: repeat that the v2.0 readme says CC BY-NC-SA. |
| 30 | FAOSTAT and BACI retrieved on 22 Oct 2026 (§2.8); FAO reference retrieval date | Package README | Hides file retrieved 22 Oct; the cattle and price file (used for the mass and economic rules) on 21 Oct 2026 | MINOR | State both dates, or keep 22 Oct and add "(cattle file 21 October)". |

Not cited in the manuscript, so not audited: NGO reports (Earthsight, EIA, AidEnvironment, Stand.earth, Mighty Earth) and Walker et al. (2013). The manuscript cites none of them, which is acceptable.

---

## 2. Crossref / DataCite / URL verification

| Reference | Identifier | Registry result | Status |
|---|---|---|---|
| Laroche et al. (2024) | 10.1016/j.ecolecon.2024.108288 | Crossref: Perrine C.S.J. Laroche; Manuela Gómez-Suárez; U. Martin Persson; Florence Pendrill; Florian Schwarzmueller; Catharina J.E. Schulp; Thomas Kastner. *Ecological Economics* 224, art. 108288, 2024-10; CC BY 4.0 (vor) | Matches |
| Laroche supplement | 10.5281/zenodo.11085413 (DataCite) | Creators **in order**: Kastner, Thomas; Laroche, Perrine C.S.J.; Gómez-Suárez, Manuela; Persson, U. Martin; Pendrill, Florence; **Schwarzmüller**, Florian; Schulp, Catharina J.E. Version 1.0; Dataset; issued 2024-04-29; CC BY 4.0; IsSupplementTo the article; IsVersionOf 10.5281/zenodo.11085412 (concept DOI, the one in the article's data statement). Single file `supplement.zip`, 114,804,973 bytes | **Author order wrong in manuscript** (FIX) |
| Kastner et al. (2011) | 10.1016/j.ecolecon.2011.01.012 | Crossref: Thomas Kastner; Michael Kastner; Sanderine Nonhebel. *Ecological Economics* 70(6), 1032–1040, 2011-04 | Matches |
| Singh & Persson (2026) | 10.1038/s43016-026-01305-4 | Crossref: Chandrakant Singh; U. Martin Persson. *Nature Food* 7(2), 138–151; online 2026-02-23 | Matches, but **not cited in text** |
| Singh et al. (2024), v2.0 | 10.5281/zenodo.10633818 | DataCite: Singh; Persson; Croft; Kastner; West, Christopher D.; 2024; v2.0; CC BY 4.0; issued 2024-04-22 | Matches |
| Singh et al. (2026), v2.1 | 10.5281/zenodo.18953516 | DataCite: same five creators; 2026; v2.1; CC BY 4.0; issued 2026-03-11; IsNewVersionOf 10633818. Files: ReadMe.txt, 0. About the data.pdf, 1. …xlsx (21.6 MB), 2. Physical … csv (61.5 MB), 3. Hybrid … csv (359.0 MB) | Matches. Note: the ReadMe.txt inside v2.1 suggests citing "(2024) … (Version 2.1) … zenodo.10633818", which is inconsistent. The About PDF and DataCite give 2026 and 18953516; the manuscript correctly follows those. |
| Mammadova et al. (2020) | 10.3390/f11040472 | Crossref: Aynur Mammadova; Mauro Masiero; Davide Pettenella. *Forests* 11(4), 472; 2020-04-22 | Matches |
| Gaulier & Zignago (2010) | CEPII WP 2010-23; BACI page URL | BACI page live; cites "CEPII Working Paper, N°2010-23"; version 202601, updated January 22, 2026 | Matches |
| Buljan et al. (2000) | leatherpanel.org PDF | Live. Title page: "MASS BALANCE IN LEATHER PROCESSING", "US/RAS/92/120", "Prepared by J. Buljan, G. Reich, J. Ludvik", "9 August 2000", UNIDO | Matches |
| Kalafatis (2026) | x9m8.com URL | Live (Chrome). "Cite as: Kalafatis, P. (2026). Lower economic value, same forest: the EU's leather exemption from deforestation rules [Preprint]. x9m8.com." | Matches |
| SWD (2026) | environment.ec.europa.eu PDF | Live (fetched); 37 PDF pages; cover title as in reference; draft-labelled | Matches (title follows paper 8's corrected form) |
| Delegated Reg. 2026/2102 | ELI URL | Verified in paper 8 audit (EUR-Lex, 21 Oct 2026); title and OJ reference match | Matches |
| Reg. 2023/1115 | ELI URL | Verified in paper 8 audit: OJ L 150, pp. 206–247 | Matches |
| Eurostat DS-045409 | API URL | Verified in paper 8 audit (dataflow title) | Matches, but **not cited in text** |
| FAOSTAT QCL | bulk URL | Verified in paper 8 audit (datasets_E.json FileLocation) | Matches |

---

## 3. In-text vs reference list (APA 7)

**Cited in text, present in list:** Buljan et al. (2000); European Commission (2026); FAO (2026); Gaulier & Zignago (2010); Kalafatis (2026); Kastner et al. (2011); Laroche et al. (2024); Mammadova et al. (2020); Singh et al. (2024); Singh et al. (2026). Regulation 2023/1115 and Delegated Regulation 2026/2102 are named in the text, which is acceptable for legislation.

**In list, not cited in text**
- **Singh & Persson (2026).** Add a citation where DeDuCE is introduced (§2.1: "DeDuCE … (Singh & Persson, 2026; Singh et al., 2026)"), or delete the entry. The DeDuCE ReadMe asks users to cite both.
- **Eurostat (2026).** §2.1 names "Eurostat Comext (DS-045409)" without a citation. Add "(Eurostat, 2026)".

**Ambiguity**
- Two references begin "Laroche … (2024)" with identical author lists. As written they would need 2024a/2024b. Using the correct DataCite creator order for the supplement (Kastner first) removes the clash. Change "(Laroche et al., 2024, supplement file 01_calculations.R)" to "(Kastner et al., 2024, file 01_calculations.R)". Do the same for the §2.2 factors ("the supplement of Laroche et al. (2024)" → "the supplement (Kastner et al., 2024)"), the §2.1 cleaning rule, and §2.7 ("read from their Zenodo supplement" → add "(Kastner et al., 2024)").

**Named but not referenced**
- PEFCR leather 3.5% (§2.5). Add De Rosa-Giglio et al. (2018), as in paper 8, or mark it as taken from Kalafatis (2026).

**Page locator**
- SWD "p. 19" should be "p. 18" (printed page).

---

## 4. Corrected reference list (APA 7, ready to paste)

Buljan, J., Reich, G., & Ludvik, J. (2000). *Mass balance in leather processing* (US/RAS/92/120, Regional Programme for Pollution Control in the Tanning Industry in South-East Asia). United Nations Industrial Development Organization. https://leatherpanel.org/sites/default/files/publications-attachments/mass_balance.pdf

Commission Delegated Regulation (EU) 2026/2102 of 13 July 2026 amending Regulation (EU) 2023/1115 of the European Parliament and of the Council as regards the list of relevant commodities and relevant products. *Official Journal of the European Union*, L, 2026/2102, 17 September 2026. https://eur-lex.europa.eu/eli/reg_del/2026/2102/oj/eng

De Rosa-Giglio, P., Fontanella, A., Gonzalez-Quijano, G., Ioannidis, I., Nucci, B., & Brugnoli, F. (2018). *Product environmental footprint category rules (PEFCR): Leather* (Final version, 25 April 2018). Leather Pilot Technical Secretariat. https://web.archive.org/web/20220205045047/https://ec.europa.eu/environment/eussd/smgp/pdf/PEFCR_leather.pdf *(add only if the 3.5% source is cited directly)*

European Commission. (2026). *Commission staff working document accompanying the document Commission Delegated Regulation (EU) …/... amending Regulation (EU) 2023/1115 of the European Parliament and of the Council as regards the list of relevant commodities and relevant products* [Draft-labelled copy of SWD(2026) 194 final]. https://environment.ec.europa.eu/document/download/9b5c8907-8651-440f-be8f-bb2d3d549763_en?filename=Commission%20Staff%20Working%20Document%20on%20Delegated%20Regulation%20on%20EUDR%20list%20of%20relevant%20commodities%20and%20products.pdf

Eurostat. (2026). *EU trade since 1988 by HS2-4-6 and CN8* (DS-045409) [Data set]. Retrieved October 21, 2026, from https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409

FAO. (2026). *FAOSTAT: Crops and livestock products* (QCL) [Data set]. Food and Agriculture Organization of the United Nations. Retrieved October 22, 2026, from https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip

Gaulier, G., & Zignago, S. (2010). *BACI: International trade database at the product-level. The 1994–2007 version* (CEPII Working Paper No. 2010-23). CEPII. Data version 202601 retrieved October 22, 2026, from https://www.cepii.fr/DATA_DOWNLOAD/baci/doc/baci_webpage.html

Kalafatis, P. (2026). *Lower economic value, same forest: The EU's leather exemption from deforestation rules* [Preprint]. x9m8.com. https://x9m8.com/eu-deforestation-regulation-leather-exemption/

Kastner, T., Kastner, M., & Nonhebel, S. (2011). Tracing distant environmental impacts of agricultural products from a consumer perspective. *Ecological Economics*, *70*(6), 1032–1040. https://doi.org/10.1016/j.ecolecon.2011.01.012

Kastner, T., Laroche, P. C. S. J., Gómez-Suárez, M., Persson, U. M., Pendrill, F., Schwarzmüller, F., & Schulp, C. J. E. (2024). *Supplement code and data for "Accounting for trade in derived products when estimating European Union's role in driving deforestation"* (Version 1.0) [Data set and code]. Zenodo. https://doi.org/10.5281/zenodo.11085413

Laroche, P. C. S. J., Gómez-Suárez, M., Persson, U. M., Pendrill, F., Schwarzmueller, F., Schulp, C. J. E., & Kastner, T. (2024). Accounting for trade in derived products when estimating European Union's role in driving deforestation. *Ecological Economics*, *224*, Article 108288. https://doi.org/10.1016/j.ecolecon.2024.108288

Mammadova, A., Masiero, M., & Pettenella, D. (2020). Embedded deforestation: The case study of the Brazilian–Italian bovine leather trade. *Forests*, *11*(4), Article 472. https://doi.org/10.3390/f11040472

Regulation (EU) 2023/1115 of the European Parliament and of the Council of 31 May 2023 on the making available on the Union market and the export from the Union of certain commodities and products associated with deforestation and forest degradation and repealing Regulation (EU) No 995/2010. *Official Journal of the European Union*, L 150, 206–247. https://eur-lex.europa.eu/eli/reg/2023/1115/oj/eng

Singh, C., & Persson, U. M. (2026). Global patterns of commodity-driven deforestation and associated carbon emissions. *Nature Food*, *7*(2), 138–151. https://doi.org/10.1038/s43016-026-01305-4

Singh, C., Persson, U. M., Croft, S., Kastner, T., & West, C. D. (2024). *Commodity-driven deforestation, associated carbon emissions and trade 2001–2022* (Version 2.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10633818

Singh, C., Persson, U. M., Croft, S., Kastner, T., & West, C. D. (2026). *Commodity-driven deforestation, associated carbon emissions and trade 2001–2023* (Version 2.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18953516

**Changes from the manuscript list**
- **Laroche supplement:** re-authored as Kastner, T., Laroche, … per DataCite and Zenodo, with Schwarzmüller spelled with the umlaut as in the record. In-text citations become "Kastner et al., 2024".
- **PEFCR:** optional addition.
- **Everything else** is unchanged and verified.

---

## 5. Novelty findings

**What Laroche et al. (2024) already did** (confirmed in the code, the published output and the article):
- Applied the Kastner et al. (2011) physical model to bovine hides and derived products up to consumer goods, on BACI HS12 v202401, for 2012–2022 (reported as the 2018–2020 mean).
- Ran min, mean and max conversion factors, with an EU27 aggregate.
- Pooled all stages into one RHE matrix, traced once. Goods made in third countries are **already** attributed to hide-producing countries, in proportion to each processor's total hide-equivalent supply.

The manuscript states this accurately in §1 and §4.2. That is good practice; the brief had flagged it as unknown.

**The paper's four stated contributions, checked**

1. **Stage-specific tracing.** Accurate. Laroche pools stages. I found no other study that traces leather by stage.
2. **Annual 2005–2023 series with DeDuCE v2.1.** Accurate as an extension: Laroche's output covers 2012–2022 with DeDuCE v1.0. "Annual series" is not itself new, because Laroche's supplement is annual. The novelty is 2005–2011, 2023, and v2.1. The manuscript already says the supplement holds annual results, so this is fine.
3. **Term-by-term reconciliation with the "exporter-based figure used by the Commission".** Needs rewording (claims table #1). The SWD's stated method includes a one-step derived-product origin adjustment using Comtrade for leather. The reconciliation is with exporter attribution as implemented in the companion paper, which reproduces the SWD's total closely (37,727 vs 39,005 ha). It is not with an exporter-attribution method the Commission says it used.
4. **Seven allocation rules, five factor sets, and a mass-balance test of the factors.** Accurate. I found no prior mass-balance test of the SWD's 2.33 and 4.20 against FAOSTAT hide output.

**Search for other studies tracing EU leather deforestation to cattle origin through processing countries**
- Searches run: WebSearch, standard and extended; OpenAlex "leather deforestation trade", 3,394 hits, first 50 screened; OpenAlex works citing Laroche et al. 2024, 5 hits.
- No such footprint study found. Closest items:
  - Mammadova et al. 2020 and Mammadova's 2019 Padova PhD thesis: a Brazil–Italy case study, not a footprint.
  - Mammadova et al. 2022, *Forests* 13(2):233: a systemic-risk framing.
  - Global Canopy (MacFarquhar, Morrice & Vasconcelos, 2019), "Hidden deforestation in the Brazil–China beef and leather trade": links Chinese processors to Western brands but "doesn't quantify" deforestation.
  - NGO reports (Earthsight, EIA, AidEnvironment, Mighty Earth): chain-specific evidence, not footprints.
  - DeDuCE's hybrid (IOTA/GLORIA) model: covers leather in goods implicitly, but merges it with meat.
  - The five works citing Laroche (e.g., *Nat Rev Earth Environ* 2025, 10.1038/s43017-025-00660-3; *ERL* 2025 gravity model): none are leather-specific multi-stage tracing.
- This negative rests on open indexes only (no Scopus or WoS). Wording such as "the most complete earlier estimate" (§1) is appropriately cautious. Do not add "first".

---

## 6. Prioritised fix list

1. **Characterisation of the Commission's method** (Abstract sentence 1, §1 ¶1, §2.4, §4.1 "exporter-based figure used by the Commission", §1 contribution 3).
   - The SWD (Annex I, printed pp. 28 and 31) defines a derived-product intensity that adds deforestation embodied in raw commodities the partner country imports, using UN Comtrade for leather. It is therefore not pure exporter attribution.
   - Reword so that the comparator is "exporter attribution of direct imports (the method of the companion paper)". Say that the SWD counts only direct hides and leather imports at partner-country intensities, adjusted at most one trade step, and omits goods and EU exports. Note that Annex II does not show how the adjustment was applied to 4104 and 4107.
   - Keep the useful fact that the paper's exporter model with the SWD factors reproduces 37,727 vs 39,005 ha.
2. **Supplement authorship.** DataCite and Zenodo list Kastner, T. first. Fix the reference (see §4) and change every in-text "Laroche et al., 2024, supplement…" to "Kastner et al., 2024". This also removes the identical-author/year clash.
3. **§2.1 quantity cleaning "as in Laroche".** Laroche's code drops flows with missing quantity. Only the 20× outlier rule matches.
4. **§2.7 validation differences.** Add that Laroche's core includes 4114.20, 4115.10 and 4115.20 at processing level 3 (excluded from this replication's core) and used FAOSTAT downloaded in December 2023.
5. **Uncited references.** Cite Singh & Persson (2026) where DeDuCE is introduced, and Eurostat (2026) where Comext is used, or remove them.
6. **SWD page.** "p. 19" → "p. 18" (printed page).
7. **§4.4 DeDuCE reliability caution.** It comes from the v2.0 explainer (2021–2022); the v2.1 documentation does not contain it. Cite Singh et al. (2024) and specify.
8. **§2.1 FAOSTAT flags.** "Almost all imputed" → about 79% imputed (I) and 21% estimated (E); none official.
9. **§2.1 v2.1 licence.** The About file says "Creative Commons Attribution license" with no version. "CC BY 4.0" is from Zenodo and DataCite.
10. **§2.2 "at least three-quarters".** It applies to goods described only as "leather". Optionally note that pure-leather articles carry 4.02, which suggests no 0.75 scaling is built into the factors (auditor inference).
11. **§2.5 PEFCR 3.5%.** Add the PEFCR reference, or attribute the rule set explicitly to Kalafatis (2026).
12. **§4.4 Mammadova.** "customs-level studies show" → "a customs-level study of one year shows".
13. **§2.8 retrieval dates.** Note the cattle and price file was retrieved 21 October 2026.

**Verified with no change needed**
- Laroche 1,220 kt, origin shares (34.5 / 12.7 / 12.3 / 8.5%), 1,200–31,000 ha, 10% allocation, 30,979 ha, annual 2012–2022 output.
- Pooled single-matrix tracing in `01_calculations.R`; BACI HS12 v202401 and DeDuCE v1.0 in Laroche's code.
- Laroche factor values (1.00 / 4.02 / 1.03–4.02).
- SWD factors 1.00 / 2.33 / 4.20, Annex II range 19,504–39,005 ha, 2015–2020 trade, the p. 18 quotes.
- Buljan mass balance (262 + 88; 195 + 60) and the 2.86 and 3.92 ratios.
- DeDuCE v2.1: 5.0% leather share (2,867 country-years); leather excluded from the physical model (quote, and full-file scan showing "Cattle meat" only); CC BY 4.0 on Zenodo.
- v2.0 readme CC BY-NC-SA discrepancy.
- BACI v202601 and Etalab 2.0; Gaulier & Zignago 2010.
- FAOSTAT items 919 and 957; India without cattle hides.
- Mammadova wet-blue to Italy.
- Paper 8 limitation quote and title.
- All DOIs resolve to matching metadata.
