# Citation audit: "Less food, nearly the same bill: the cost of an adequate diet on GLP-1 drugs"

Auditor: independent AI citation auditor (Claude, claude-opus-5-5), 21 October 2026.
Manuscript audited: `/home/claude/p10/pkg/manuscript/manuscript.md` (not edited).
Methods: Crossref REST API (api.crossref.org) for every DOI; Europe PMC REST API (abstracts, open-access full-text XML, preprints); publisher full text (Wiley, for Almandoz 2024); USDA/ERS/FNS/ARS/NCHS pages and PDFs; the local raw data files in `pkg/data/raw/` (CPI and FNDDS); WebSearch for novelty. The literature brief (`lit/brief.md`) was used only as a source of leads. Every verdict below is based on the source itself unless marked otherwise.

Verdict key: **OK** = supported as written; **MINOR** = supported, but the wording or detail should be tightened; **FIX** = misstated, misattributed or missing a citation; **UNVERIFIED** = could not be checked against the primary source.

---

## 1. Summary of main problems (most important first)

1. **Almandoz et al. (2024) energy figures are misframed (FIX).** The paper says intakes of 1,200–1,500 kcal for women and 1,500–1,800 kcal for men "have been recommended as safe during weight reduction". These are general safe-minimum intakes during weight loss, citing earlier literature. The paper does not suggest them as intakes for people on anti-obesity medication.
2. **No numeric protein target in the joint advisory (FIX).** §2.4 cites Mozaffarian et al. (2025) for protein targets "proposed during GLP-1 therapy". The advisory's full text (AJCN version, PMC12612741) gives no g/kg or g/day figure. Almandoz et al. (2024) does give one: "at least 60 to 75 g/day and up to 1.5 g/kg body weight/day".
3. **"healthful foods such as …" is taken out of context (FIX).** In the advisory, this phrase comes from a baseline-assessment step ("Current dietary habits should be assessed, including 1) intake of healthful foods such as …"). It is not a dietary recommendation. The recommendation appears in §5.3: "clinicians should emphasize a diversity of nutrient-dense, minimally processed foods such as fruits, vegetables, whole grains, legumes, lean proteins, nuts, and seeds". "Acceptance of supplements where diet cannot meet the need" is also a paraphrase the text does not support. The advisory says "Dietary supplements can be proactively considered for at-risk nutrients".
4. **"nutritious diet at minimal cost" contradicts the TFP 2021 report (FIX).** USDA says that the "minimal cost" descriptor "is no longer appropriate under the 2018 Farm Bill". The report describes the TFP as "the cost of a healthy, practical diet on a limited budget".
5. **The Thrifty Food Plan comparison has a household-size problem (FIX, substantive).** The June 2026 report states: "The costs given are for individuals in 4-person households." A 1-person household adds 20%, giving $10.03/day for women and $12.60/day for men aged 20–50. This changes "about 10% above the Thrifty Food Plan" (§3.1), the Table 1 and Figure 1 benchmarks, and the Discussion's claim about "a single adult". The report also lists costs for ages 51–70 ($54.50 women and $64.80 men a week), which suit a sample with a mean age of about 50.
6. **The vitamins D and E sentence needs a citation and a correction (FIX).** "Supplements are the usual source" is not supported. In NHANES 2003–2006, 70% (vitamin D) and 60% (vitamin E) of the US population were below the EAR even counting supplements (Fulgoni et al., 2011). This shows that most people do not get enough from supplements either.
7. **Several requirements and constants have no citation (FIX):** DRI reference weights of 70/57 kg, the AMDRs, fibre at 14 g/1,000 kcal and the linoleic and α-linolenic energy shares (IOM, 2005); saturated fat below 10% of energy (Dietary Guidelines); WWEIA food categories. The FNDDS gap list leaves out **fluoride and chloride**, which also have AIs and no FNDDS values.
8. **The novelty sentence holds in substance but should be narrowed (MINOR).** No study or preprint was found that optimises diet cost or feasibility at GLP-1-typical intakes. Linear-programming diet studies do exist, and some cover low energy levels, so the claim should be specific to GLP-1 therapy and state how the search was done (§5).
9. **Reference-list details (MINOR):** Fulgoni needs the "III" suffix. The NCHS pages carry a date (first published July 2022), so "n.d." is wrong, and their titles are not exact. The PP-NAP title is not the one ERS recommends. The 2026 TFP report is issued by the "Food and Nutrition Administration". The NASEM abbreviation is used before it is introduced. Two parenthetical citations are out of alphabetical order. The ERS forecast file is due to update on 23 October 2026.
10. **Companion paper (CHECK).** The cited URL opens, but only in a logged-in browser session. There the post shows the date "October 24, 2026", which is still in the future. An unauthenticated fetch failed. Confirm the post is public before this preprint is released. Its content supports the claim made here.

All 11 DOIs resolve on Crossref to the cited works. Authors, year, title, journal, volume, issue and pages match, with two exceptions: the Fulgoni suffix, and Stigler's end page, which Crossref does not supply.

---

## 2. Claims table

| # | Claim in manuscript (location) | Source cited | Verbatim evidence (source) | Verdict | Fix |
|---|---|---|---|---|---|
| 1 | Liraglutide reduced energy intake at an ad libitum lunch by about 16% (§1) | van Can et al., 2014 | Abstract: "decreased ad libitum energy intake by ∼16%". Methods: "an ad libitum lunch meal was provided for assessment of energy intake" (PMC4052428) | OK (MINOR) | The 16% is pooled across liraglutide 1.8 and 3.0 mg. Optionally write "liraglutide (1.8 and 3.0 mg)". |
| 2 | Semaglutide 1.0 mg reduced intake by 24% across a day of ad libitum meals (§1) | Blundell et al., 2017 | "a 24% reduction in total energy intake across all ad libitum meals throughout the day"; "dose-escalated to 1.0 mg" (Europe PMC abstract) | OK | None. |
| 3 | Semaglutide 2.4 mg reduced intake by 35% at a test lunch (§1) | Friedrichsen et al., 2021 | "Ad libitum energy intake was 35% lower with semaglutide versus placebo"; "measured during ad libitum lunch" (PMID 33269530) | OK | None. |
| 4 | Oral semaglutide 50 mg: relative reduction at lunch 39 percentage points greater than with placebo (§1) | Gabe et al., 2024 | "Energy intake was measured during an ad libitum lunch"; "relative change from baseline in ad libitum energy intake at week 20 … was -39.2% points" vs placebo; "dose-escalated to 50 mg" (institutional abstract, research.regionh.dk) | OK | None. The abstract's "16% to 39%" is acceptable because the advisory uses the same range. |
| 5 | Advisory "summarised these as 'observed caloric reductions of 16%–39%'" (§1) | Mozaffarian et al., 2025 | AJCN full text (PMC12612741), §2.3: "with observed caloric reductions of 16%–39%". Typeset exactly so. | OK | None. The quote matches the AJCN version character for character. (The AJLM co-publication prints "16-39%".) |
| 6 | Advisory "recommended managing diet quality to protect nutrient intake at lower energy" (§1) | Mozaffarian et al., 2025 | "proactively managing dietary composition and quality to maximize nutrient intake within a lower calorie intake" (§2.3) | OK | None. |
| 7 | "Clinical guidance suggests energy intakes of roughly 1,200 to 1,500 kcal a day for women and 1,500 to 1,800 kcal for men on anti-obesity medication" (§1) | Almandoz et al., 2024 | "In general, energy intakes of 1200 to 1500 kcal/day for women and 1500 to 1800 kcal/day for men have been recommended as safe during weight reduction [54]." The preceding sentence says "recommended minimum goals for energy intake during weight loss should be personalized." (Wiley full text) | **FIX** | Replace with: "A review of nutrition with anti-obesity medications notes that intakes of 1,200–1,500 kcal a day for women and 1,500–1,800 kcal for men have been recommended as safe during weight reduction, and that patients below 1,200 kcal may have difficulty meeting nutritional needs by diet alone (Almandoz et al., 2024)." |
| 8 | Prorating usual intake by 20% to 50% sharply raises the share below the EAR (§1) | Fulgoni et al., 2024 | "Four levels of caloric reduction (20%, 30%, 40%, and 50%) were modeled by prorating daily calorie intake"; at 30%, "75%-91% … below the EAR for vitamin A, calcium, and magnesium (vs. … 45%-56% … without caloric reduction)" (PMID 39025331) | OK | Optional: "for most of 14 nutrients". |
| 9 | Companion paper: at a 35% cut, most would fall short of zinc, folate, calcium and magnesium; NHANES 2021–2023 (§1) | Kalafatis, 2026 | Companion Table: at −35%, zinc 83.3%, folate 74.1%, calcium 86.8%, magnesium 97.4% below the EAR; "NHANES August 2021–August 2023" | OK (CHECK) | The content is correct. The post was visible only when logged in, dated 24 Oct 2026. Confirm it is public. In §2.1, "The sample was the one defined in" would be clearer as "Eligibility was defined as in", because the companion's sample came from a different cycle (n = 2,134). |
| 10 | "Neither asked what eating differently would cost" (§1) | Fulgoni 2024; Kalafatis 2026 | Fulgoni 2024 models only proration and supplements, with no cost analysis (abstract) | OK | None. |
| 11 | Grocery prices rose by about 31% between 2017–2018 and 2025 (§1) | USDA ERS, 2026a | ERS file "Annual percent changes in selected Consumer Price Indexes, 1974 through 2025": food at home 2018 0.4, 2019 0.9, 2020 3.5, 2021 3.5, 2022 11.4, 2023 5.0, 2024 1.2, 2025 2.3. Recomputed factor from the mean of 2017 and 2018 to 2025: 1.3115. | OK | This is a derived figure, so consider "computed from USDA ERS (2026a)". |
| 12 | SNAP benefits are set by the cost of the TFP (§1) | USDA FNS, 2021 | "It is the basis for the maximum Supplemental Nutrition Assistance Program (SNAP) benefit allotments." (TFP 2021, p. 1) | OK | None. |
| 13 | TFP is "USDA's estimate of a nutritious diet at minimal cost" (§1) | USDA FNS, 2021 | "previous updates to the Thrifty Food Plan described the Plan as 'minimal cost,'" and "USDA believes such a descriptor is no longer appropriate under the 2018 Farm Bill" (p. vii). The Plan "describes the cost of a healthy, practical diet on a limited budget" (p. ix) | **FIX** | Replace with "USDA's estimate of the cost of a healthy, practical diet on a limited budget (USDA FNS, 2021)". |
| 14 | Least-cost diet problem "as old as linear programming" (§1) | Stigler, 1945 | Crossref confirms the title, journal, year, volume and issue. Full text not read. | OK | None. (Stigler's own solution was heuristic, and Dantzig's simplex method came later. "As old as" is acceptable.) |
| 15 | Diet optimisation "used to show how cost constraints change food choices" (§1) | Darmon et al., 2006 | "To predict, for French women, the impact of a cost constraint on the food choices required to provide a nutritionally adequate diet"; "Introducing and strengthening a cost constraint decreased the energy provided by meat, fresh vegetables, fresh fruits …" (abstract) | OK | None. |
| 16 | Diet optimisation used "to translate recommendations into realistic diets close to what people already eat" (§1) | Maillot et al., 2010 | "an isocaloric modeled diet was designed by linear programming to simultaneously meet the French nutrient recommendations for 32 nutrients while deviating the least from the observed food intake" (abstract) | OK | None. |
| 17 | TFP selects "a dietary pattern as close to current consumption patterns as possible" subject to cost and nutrient constraints (§1) | USDA FNS, 2021 | p. 18: "the optimization model selects a dietary pattern as close to current consumption patterns as possible." p. 11: "cost also serves as a constraint, limiting the cost of the Thrifty Food Plan Market Baskets." | OK | Add a pin cite (USDA FNS, 2021, p. 18), as APA requires for direct quotations. |
| 18 | "I am not aware of an optimisation study at the energy intakes typical of GLP-1 therapy" (§1) | none (author statement) | See §5 | MINOR | See replacement text in §5. |
| 19 | NHANES 2017–March 2020 cycle recorded every food with its USDA food code and weight (§2.1) | NCHS, n.d.-a, n.d.-b | Pages resolve: "National Health and Nutrition Examination Survey 2017-March 2020 Data Documentation, Codebook, and Frequencies Dietary Interview - Individual Foods, First Day (P_DR1IFF)"; "First Published: July 2022" (P_DR2IFF is the same) | MINOR | Date them 2022 and use the exact titles (see the reference list). |
| 20 | FNDDS 2017–2018 nutrient values, with 2021–2023 for missing codes (§2.1) | USDA ARS, n.d. | The ARS "FNDDS Download Databases" page resolves and lists both releases. The local At-A-Glance files confirm the nutrient columns. | OK | None. |
| 21 | PP-NAP 2017–2018: national average retail price per 100 edible grams as eaten, from retail scanner data, linked to NHANES food codes (§2.2) | USDA ERS, 2023 | Documentation: "The price per 100 edible grams of the food in nominal dollars for the years of the IRI data used to estimate the price." Landing page: the estimates use "retail grocery scanner data from Circana (formerly IRI)". Years 2011–12 to 2017–18; files last updated 3/8/2023. ERS citation: "Purchase to Plate National Average Prices from the Purchase to Plate Suite [data product]" | OK (MINOR) | Use ERS's recommended title in the reference. |
| 22 | CPI factor 1.312 to 2025, and 1.343 with the ERS September 2026 forecast of 2.4% (interval 1.8–3.0%) (§2.2) | USDA ERS, 2026a, 2026b | ERS summary (updated 9/25/2026): "Food-at-home prices are forecast to increase 2.4 percent, with a forecast interval of 1.8 to 3.0 percent", and the page "summarizes the September 2026 Food Price Outlook forecasts". Local historical forecast file: food at home, month 9, 2026→2026: lower 1.8, midpoint 2.4, upper 3.0. Recomputed: 1.3115 × 1.024 = 1.3430. | OK | ERS lists the next forecast update as **10/23/2026**. Re-check before release, or keep "September 2026 forecast" explicit, as now. |
| 23 | TFP June 2026: $58.50/week women, $73.50 men aged 20–50, or $8.36 and $10.50/day (§2.2, Table 1, Fig. 1) | USDA FNS, 2026 | "Official USDA Thrifty Food Plan: U.S. Average, June 2026": Female 20–50 $58.50, Male 20–50 $73.50 a week; "The costs given are for individuals in 4-person households"; 1-person household +20%; "Issued August 2026"; agency on the document: "Food and Nutrition Administration" | **FIX** (substantive) | The numbers are correct (58.50/7 = 8.36; 73.50/7 = 10.50). State that they apply to individuals in four-person households, and give the one-person figures ($10.03 and $12.60 a day) wherever the text speaks of a single adult (§4.1). Consider also giving the 51–70 costs ($54.50 and $64.80 a week). Update the author to the agency named on the document. |
| 24 | Current diet cost "about 10% above the Thrifty Food Plan" (§3.1) | USDA FNS, 2026 (implicit) | 9.12/8.36 = 1.091; 11.69/10.50 = 1.113 | MINOR | The arithmetic is right against the four-person figures. Against one-person figures, the current diet is about 9% *below* the TFP. Say which figures are used. |
| 25 | TFP optimises over food categories rather than single foods (§2.3) | USDA FNS, 2021 | Modeling Categories are "used in the optimization model to generate a set of categories in amounts that satisfy the model's constraints" (p. 2); "a total of 95 categories were used in the optimization model" (p. 17) | OK | None. |
| 26 | WWEIA categories: 155 for women, 154 for men (§2.3) | none | No citation for the WWEIA category system | MINOR | Cite the WWEIA Food Categories documentation (USDA ARS), or point to the FNDDS citation already given, since the FNDDS files carry the WWEIA category number. |
| 27 | RDA/AI for adults 31–50 for the listed nutrients (§2.4) | NASEM, 2019, Appendix J | The 2019 report's Appendix J holds the DRI summary tables (NCBI Bookshelf NBK545442). Spot checks: Mg 420/320, Zn 11/8, Ca 1,000, choline 550/425, LA 17/12, ALA 1.6/1.1. | OK (MINOR) | Introduce the abbreviation at first use: "(National Academies of Sciences, Engineering, and Medicine [NASEM], 2019, Appendix J)". |
| 28 | ULs, sodium CDRR of 2,300 mg (§2.4) | none at that sentence | The CDRR is set in NASEM (2019); not quoted from a page in this audit | MINOR | Add "(NASEM, 2019)" after "2,300 mg". |
| 29 | AMDRs; LA ≥5% and ALA ≥0.6% of energy; fibre ≥14 g/1,000 kcal (§2.4) | none | Defined in the IOM 2005 macronutrient report (Crossref: 10.17226/10490) | **FIX** | Cite Institute of Medicine (2005). |
| 30 | Saturated fat below 10% of energy (§2.4) | none | This limit comes from the Dietary Guidelines for Americans, not the DRIs | **FIX** | Cite the Dietary Guidelines edition used. Verify the edition and URL; this audit did not check them. |
| 31 | "the US diet meets their RDAs only rarely from food and supplements are the usual source" (vitamins D and E) (§2.4) | none | Fulgoni et al. (2011), NHANES 2003–2006: "more of the population had total usual intakes below the EAR for vitamins A, C, D, and E (34, 25, 70, and 60%, respectively)". Total intake includes supplements, so most people do not meet the requirement through supplements either. | **FIX** | Replace with: "Most US adults do not meet the requirements for vitamins D and E from food, and most remain below the EAR even when supplements are counted (Fulgoni et al., 2011); the current diet of eligible adults supplied 3.9–4.5 µg of vitamin D and 8.0–9.2 mg of vitamin E (§3.1)." |
| 32 | Protein 0.8 g/kg of reference weight; DRI reference weights 70 kg men and 57 kg women (§2.4) | none for the weights | The DRI protein RDA footnote says it is "Based on g protein per kg of body weight for the reference body weight, e.g., for adults 0.8 g/kg". RDA 56 g ÷ 0.8 = 70 kg; 46 g ÷ 0.8 = 57.5 kg. The 70/57 kg reference-weight table is in the IOM 2005 report, but its page was not opened here. | FIX (UNVERIFIED page) | Cite IOM (2005) and confirm the table and page number. |
| 33 | 1.2 g/kg "closer to the targets proposed during GLP-1 therapy (Mozaffarian et al., 2025; Almandoz et al., 2024)" (§2.4) | Mozaffarian 2025; Almandoz 2024 | Advisory: no numeric protein target anywhere in the text. Almandoz: "protein intakes of at least 60 to 75 g/day and up to 1.5 g/kg body weight/day have been recommended during weight reduction"; table: ">60–75 g/d and up to 1.5 g/kg body weight/d is typical" | **FIX** | Drop Mozaffarian 2025 from this citation, or cite it only for the qualitative emphasis on protein. Suggested text: "with 1.2 g/kg as an alternative within the range recommended during weight reduction with anti-obesity medication (at least 60–75 g a day and up to 1.5 g/kg; Almandoz et al., 2024)". Note that 0.8 g/kg × 57 kg = 45.6 g, below Almandoz's 60–75 g floor. Also fix the order: (Almandoz et al., 2024; Mozaffarian et al., 2025). |
| 34 | Iodine, chromium, manganese, molybdenum, biotin and pantothenic acid have no values in FNDDS (§2.4) | USDA ARS (implicit) | FNDDS 2017–2018 and 2021–2023 At-A-Glance nutrient files (local copies) have no column for any of these six. **Fluoride and chloride**, which also have AIs, are absent too. | MINOR | Add fluoride and chloride to the list and cite USDA ARS. |
| 35 | Advisory's emphasis on "healthful foods such as fruits, vegetables, nuts, beans, whole grains, yogurt, and seafood" (§4.1) | Mozaffarian et al., 2025 | The words are verbatim, but the sentence is about assessment: "Current dietary habits should be assessed, including 1) intake of healthful foods such as fruits, vegetables, nuts, beans, whole grains, yogurt, and seafood". The recommendation is in §5.3: "clinicians should emphasize a diversity of nutrient-dense, minimally processed foods such as fruits, vegetables, whole grains, legumes, lean proteins, nuts, and seeds." | **FIX** | Quote §5.3 instead: "That fits the joint advisory's advice to 'emphasize a diversity of nutrient-dense, minimally processed foods such as fruits, vegetables, whole grains, legumes, lean proteins, nuts, and seeds'". |
| 36 | Advisory's "acceptance of supplements where diet cannot meet the need" (§4.1) | Mozaffarian et al., 2025 | "Dietary supplements can be proactively considered for at-risk nutrients, such as vitamin D, calcium, B12, or a multivitamin-mineral tablet, at appropriate doses and tailored to each person's needs." (§5.3) | MINOR | Write "and its advice that supplements can be proactively considered for at-risk nutrients such as vitamin D and calcium (Mozaffarian et al., 2025)". |
| 37 | Joint advisory: version of record | Mozaffarian et al., 2025 | Crossref lists a corrigendum: AJCN 2026;123(6):101303, doi:10.1016/j.ajcnut.2026.101303. It corrects the description of one observational study ("a larger reduction in added sugars and a greater increase in dietary protein …"), not any passage quoted here. | OK | No change needed. Optionally note the corrigendum. |
| 38 | "the energy reductions come from short laboratory studies" (§4.2) | trials above | The trials ran 12 weeks (Blundell, crossover), 20 weeks (Friedrichsen, Gabe) and an incomplete crossover (van Can), with intake measured at single test meals or a day of ad libitum meals | OK | None. |

---

## 3. Crossref verification table (api.crossref.org, 21 Oct 2026)

| Reference | DOI | Authors | Year | Title | Journal | Vol(Issue) | Pages | Result |
|---|---|---|---|---|---|---|---|---|
| Almandoz et al. | 10.1002/oby.24067 | 12 authors, order matches (Almandoz … Neff) | 2024 (online 10 Jun 2024; print Sep 2024) | match | Obesity | 32(9) | 1613–1631 | OK |
| Blundell et al. | 10.1111/dom.12932 | 7, match | 2017 | match | Diabetes, Obesity and Metabolism | 19(9) | 1242–1251 | OK |
| Darmon et al. | 10.1016/j.jneb.2005.11.028 | 3, match | 2006 | match | Journal of Nutrition Education and Behavior | 38(2) | 82–90 | OK |
| Friedrichsen et al. | 10.1111/dom.14280 | 5, match | 2021 | match | Diabetes, Obesity and Metabolism | 23(3) | 754–762 | OK |
| Fulgoni et al. | 10.1016/j.tjnut.2024.07.022 | 6; first author is **Victor L Fulgoni III** | 2024 | match | The Journal of Nutrition | 154(9) | 2732–2742 | MINOR: add "III" |
| Gabe et al. | 10.1111/dom.15802 | 7, match (Maria Buur Nordskov Gabe …) | 2024 | match | Diabetes, Obesity and Metabolism | 26(10) | 4480–4489 | OK |
| Maillot et al. | 10.3945/ajcn.2009.28426 | 4, match | 2010 | match | The American Journal of Clinical Nutrition | 91(2) | 421–430 | OK |
| Mozaffarian et al. | 10.1016/j.ajcnut.2025.04.023 | 18, match, no suffixes | 2025 (print Jul 2025) | match | The American Journal of Clinical Nutrition | 122(1) | 344–367 | OK; corrigendum 10.1016/j.ajcnut.2026.101303 exists |
| NASEM | 10.17226/25353 | Committee to Review the DRIs for Sodium and Potassium; FNB; HMD; NASEM (eds. Stallings, Harrison, Oria) | 2019 | Dietary Reference Intakes for Sodium and Potassium | National Academies Press | — | — | OK |
| Stigler | 10.2307/1231810 | George J. Stigler | 1945 | The Cost of Subsistence | Journal of Farm Economics | 27(2) | 303 (first page only) | OK. End page 314 not confirmed (Crossref gives only the first page; the OUP issue page shows a bot check, which was not bypassed). |
| van Can et al. | 10.1038/ijo.2013.162 | 6, match (Europe PMC; Crossref fetch failed twice) | 2014 | match | International Journal of Obesity | 38(6) | 784–793 | OK (via Europe PMC, PMID 23999198) |
| *Suggested additions* | | | | | | | | |
| Fulgoni et al. (2011) | 10.3945/jn.111.142257 | Victor L. Fulgoni III, Debra R. Keast, Regan L. Bailey, Johanna Dwyer | 2011 | Foods, Fortificants, and Supplements: Where Do Americans Get Their Nutrients? | The Journal of Nutrition | 141(10) | 1847–1854 | Verified |
| Institute of Medicine (2005) | 10.17226/10490 | Panel on Macronutrients … Food and Nutrition Board (corporate) | 2005 | Dietary Reference Intakes for Energy, Carbohydrate, Fiber, Fat, Fatty Acids, Cholesterol, Protein, and Amino Acids | National Academies Press | — | — | Verified |

### URL checks

| Reference | URL | Result |
|---|---|---|
| Kalafatis 2026 | https://x9m8.com/glp1-nutrient-gaps-eating-less-nhanes/ | Opens in a logged-in browser session: "Eating less of the same: modelled nutrient gaps on GLP-1 drugs", dated **October 24, 2026**, marked "Preprint, version 1". An unauthenticated WebFetch failed. **Confirm it is publicly published** before release. |
| NCHS P_DR1IFF / P_DR2IFF | wwwn.cdc.gov/…/P_DR1IFF.htm, P_DR2IFF.htm | Both resolve. Title: "…2017-March 2020 Data Documentation, Codebook, and Frequencies"; neither page uses the word "pre-pandemic". First published July 2022. |
| USDA ARS FNDDS | ars.usda.gov/…/fndds-download-databases/ | Resolves ("FNDDS Download Databases"), lists 2017–2018 and 2021–2023. |
| USDA ERS PP-NAP | https://www.ers.usda.gov/data-products/purchase-to-plate | Resolves; PP-NAP files last updated 3/8/2023. |
| USDA ERS Food Price Outlook (2026a, 2026b) | https://www.ers.usda.gov/data-products/food-price-outlook | Resolves. File titles match: "Annual percent changes in selected Consumer Price Indexes, 1974 through 2025" (updated 5/22/2026); "Historical Consumer Price Index (CPI) forecast series" (updated 9/25/2026; next update 10/23/2026). |
| USDA FNS 2021 | https://www.fna.usda.gov/sites/default/files/resource-files/TFP2021.pdf | Resolves through a 302 redirect to an Azure Front Door host; correct document (FNS-916, August 2021). |
| USDA FNS 2026 | https://fns-prod.azureedge.us/sites/default/files/resource-files/cnpp-costfood-june2026.pdf | Resolves to the correct document ("Issued August 2026"). This is a CDN host; the equivalent fna.usda.gov path did not resolve to WebFetch. Keep this URL. |

---

## 4. In-text vs reference list, and APA 7 points

- **Matching:** every in-text citation has a reference entry, and every entry is cited. No orphans either way.
- **Order inside parentheses:** "(Mozaffarian et al., 2025; Almandoz et al., 2024)" should be "(Almandoz et al., 2024; Mozaffarian et al., 2025)".
- **Abbreviations:** "NASEM" first appears as "(NASEM, 2019, Appendix J)" without being introduced. Write it out at first use. Each of the other group authors is introduced at first use.
- **Direct quotations** need page or section pin cites (APA 7.3.x): the TFP quote (p. 18) and the advisory quotes (the AJCN article uses section numbers, e.g. "Section 2.3" and "Section 5.3").
- **NCHS:** use the date 2022 (2022a, 2022b), not "n.d.", and the exact title. A retrieval date is acceptable for pages that may change.
- **Fulgoni:** "Fulgoni, V. L., III," per APA's rule for suffixes.
- **PP-NAP:** use ERS's recommended title and "[Data set]"; APA prefers "[Data set]" to "[data product]".
- **ERS datasets** are updated on a schedule, so add retrieval dates.
- **2026 TFP:** the issuing agency on the document is "Food and Nutrition Administration". Use it as the group author, or keep "U.S. Department of Agriculture" as author with the agency in the source line.
- **NASEM:** the description in parentheses after the title is acceptable but non-standard. Cite the appendix in text and keep the reference to the book.
- **Missing citations:** IOM 2005 (AMDRs, fibre, fatty-acid shares, reference weights); NASEM 2019 at the CDRR; the Dietary Guidelines for the saturated-fat limit; Fulgoni 2011 for vitamins D and E; optionally WWEIA documentation and solver software (HiGHS, CVXPY, Clarabel).

---

## 5. Novelty findings

**Searches run (21 Oct 2026).**
- Europe PMC (MED plus PPR preprints), abstract-field queries combining GLP-1/semaglutide/tirzepatide/incretin/anti-obesity medication with: "linear programming", "diet optimization/optimisation", "optimization model", "quadratic programming" and "goal programming" (1 hit, irrelevant: a GLP-1R agonist peptide-design paper); food or diet cost, Thrifty Food Plan, grocery, affordability (96 hits, all about drug cost, drug cost-effectiveness or the food industry; none costs a diet); "nutrient adequacy"/"nutrient gap" (5 hits).
- Europe PMC full-text queries combining "linear programming"/"diet optimization"/"diet modelling" with semaglutide/tirzepatide/GLP-1 RA, 2021–2026 (19 hits, none relevant); meal plans or food patterns meeting DRIs on GLP-1 (12 hits); Thrifty Food Plan/SNAP with GLP-1 and diet cost (9 hits, all versions of the joint advisory).
- Three web searches, two of them extended.

**Closest work found (none optimises diet cost or feasibility at GLP-1 intakes).**
- Fulgoni et al. (2024), already cited: proportional proration of intake and nutrient adequacy, with no optimisation and no cost.
- Hungund, S. (2026). *The GLP-1 nutritional paradox: A structured review with novel quantitative frameworks for sarcopenic risk and micronutrient adequacy in GLP-1 receptor agonist pharmacotherapy* [Preprint]. Research Square. DOI 10.21203/rs.3.rs-10929531/v1 (from Europe PMC PPR1313719; not Crossref-checked). It proposes a "Nutrient Density Requirement Index" for the dietary quality needed at suppressed intake. It is a review and index proposal, with no food-level optimisation and no costing. It is adjacent work and could be cited as such.
- Bergia, Brown, Braun and Messina (2026), *Adv Nutr* 17(8):100689, "The Pharmacological Window Hypothesis": a narrative piece. It cites a diet-optimisation study in older adults on plant-to-animal protein ratios, but it does not model GLP-1 intakes or cost.
- Spreckley et al. (2026), *Obes Rev* (via the brief; not re-checked): a scoping review finding little nutrition evidence on incretin therapies, with no cost analysis.
- The joint advisory, Almandoz 2024, observational intake studies (e.g. Johnson et al., 2025; *J Transl Med* 2026 preliminary study, doi:10.1186/s12967-026-07702-4) and demand-side studies of GLP-1 users' grocery spending: none optimises.
- General linear-programming diet literature (Darmon, Maillot, Parlesak 2016, the TFP, Cost of the Diet, Bai et al. CoNA): optimisation at fixed or habitual energy levels, not at GLP-1-typical cuts. The USDA Food Pattern modelling behind the Dietary Guidelines covers 1,200–1,600 kcal patterns, but it is food-pattern modelling, not cost optimisation.

**Does the sentence hold?** Yes in substance: I found no published study or preprint that estimates the cost or feasibility of a nutritionally adequate diet at the energy reductions measured in GLP-1 trials. The current wording, "an optimisation study at the energy intakes typical of GLP-1 therapy", is broader than what was searched. Diet-optimisation studies at roughly 1,100–1,500 kcal may exist outside the GLP-1 context, for example for older women or low-energy menus, so the sentence should be tied to GLP-1 therapy and to the search. Suggested replacement:

> "In searches of Europe PMC (including preprints) and the web in October 2026, I found no study that used diet optimisation to estimate the cost or feasibility of a nutritionally adequate diet at the energy reductions measured in GLP-1 trials; existing work prorates current intake (Fulgoni et al., 2024; Kalafatis, 2026) or proposes nutrient-density indices without costing them."

If the last clause is kept, add Hungund (2026) as the citation for the nutrient-density index.

---

## 6. Corrected APA 7 reference list (ready to paste)

Additions are marked † (they cover claims that currently lack a citation). The item marked ‡ has details the author must confirm before use.

Almandoz, J. P., Wadden, T. A., Tewksbury, C., Apovian, C. M., Fitch, A., Ard, J. D., Li, Z., Richards, J., Butsch, W. S., Jouravskaya, I., Vanderman, K. S., & Neff, L. M. (2024). Nutritional considerations with antiobesity medications. *Obesity*, *32*(9), 1613–1631. https://doi.org/10.1002/oby.24067

Blundell, J., Finlayson, G., Axelsen, M., Flint, A., Gibbons, C., Kvist, T., & Hjerpsted, J. B. (2017). Effects of once-weekly semaglutide on appetite, energy intake, control of eating, food preference and body weight in subjects with obesity. *Diabetes, Obesity and Metabolism*, *19*(9), 1242–1251. https://doi.org/10.1111/dom.12932

Darmon, N., Ferguson, E. L., & Briend, A. (2006). Impact of a cost constraint on nutritionally adequate food choices for French women: An analysis by linear programming. *Journal of Nutrition Education and Behavior*, *38*(2), 82–90. https://doi.org/10.1016/j.jneb.2005.11.028

Friedrichsen, M., Breitschaft, A., Tadayon, S., Wizert, A., & Skovgaard, D. (2021). The effect of semaglutide 2.4 mg once weekly on energy intake, appetite, control of eating, and gastric emptying in adults with obesity. *Diabetes, Obesity and Metabolism*, *23*(3), 754–762. https://doi.org/10.1111/dom.14280

† Fulgoni, V. L., III, Keast, D. R., Bailey, R. L., & Dwyer, J. (2011). Foods, fortificants, and supplements: Where do Americans get their nutrients? *The Journal of Nutrition*, *141*(10), 1847–1854. https://doi.org/10.3945/jn.111.142257

Fulgoni, V. L., III, Agler, A., Ricciuto, L., DiFrancesco, L., Williams, D., & Hertzler, S. R. (2024). Impact of simulated caloric reduction on nutrient adequacy among U.S. adults with overweight or obesity (National Health and Nutrition Examination Survey [NHANES] 2015–2018). *The Journal of Nutrition*, *154*(9), 2732–2742. https://doi.org/10.1016/j.tjnut.2024.07.022

Gabe, M. B. N., Breitschaft, A., Knop, F. K., Hansen, M. R., Kirkeby, K., Rathor, N., & Adrian, C. L. (2024). Effect of oral semaglutide on energy intake, appetite, control of eating and gastric emptying in adults living with obesity: A randomized controlled trial. *Diabetes, Obesity and Metabolism*, *26*(10), 4480–4489. https://doi.org/10.1111/dom.15802

† Institute of Medicine. (2005). *Dietary Reference Intakes for energy, carbohydrate, fiber, fat, fatty acids, cholesterol, protein, and amino acids*. The National Academies Press. https://doi.org/10.17226/10490

Kalafatis, P. (2026). *Eating less of the same: Modelled nutrient gaps on GLP-1 drugs* [Preprint]. x9m8.com. https://x9m8.com/glp1-nutrient-gaps-eating-less-nhanes/

Maillot, M., Vieux, F., Amiot, M. J., & Darmon, N. (2010). Individual diet modeling translates nutrient recommendations into realistic and individual-specific food choices. *The American Journal of Clinical Nutrition*, *91*(2), 421–430. https://doi.org/10.3945/ajcn.2009.28426

Mozaffarian, D., Agarwal, M., Aggarwal, M., Alexander, L., Apovian, C. M., Bindlish, S., Bonnet, J., Butsch, W. S., Christensen, S., Gianos, E., Gulati, M., Gupta, A., Horn, D., Kane, R. M., Saluja, J., Sannidhi, D., Stanford, F. C., & Callahan, E. A. (2025). Nutritional priorities to support GLP-1 therapy for obesity: A joint Advisory from the American College of Lifestyle Medicine, the American Society for Nutrition, the Obesity Medicine Association, and The Obesity Society. *The American Journal of Clinical Nutrition*, *122*(1), 344–367. https://doi.org/10.1016/j.ajcnut.2025.04.023

National Academies of Sciences, Engineering, and Medicine. (2019). *Dietary Reference Intakes for sodium and potassium*. The National Academies Press. https://doi.org/10.17226/25353

National Center for Health Statistics. (2022a). *National Health and Nutrition Examination Survey 2017–March 2020 data documentation, codebook, and frequencies: Dietary interview – Individual foods, first day (P_DR1IFF)*. Centers for Disease Control and Prevention. Retrieved October 21, 2026, from https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DR1IFF.htm

National Center for Health Statistics. (2022b). *National Health and Nutrition Examination Survey 2017–March 2020 data documentation, codebook, and frequencies: Dietary interview – Individual foods, second day (P_DR2IFF)*. Centers for Disease Control and Prevention. Retrieved October 21, 2026, from https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DR2IFF.htm

Stigler, G. J. (1945). The cost of subsistence. *Journal of Farm Economics*, *27*(2), 303–314. https://doi.org/10.2307/1231810 ‡(end page 314 not confirmed on Crossref)

U.S. Department of Agriculture, Agricultural Research Service. (n.d.). *FNDDS download databases* [Food and Nutrient Database for Dietary Studies 2017–2018 and 2021–2023]. Retrieved October 21, 2026, from https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/food-surveys-research-group/docs/fndds-download-databases/

U.S. Department of Agriculture, Economic Research Service. (2023). *Purchase to Plate National Average Prices from the Purchase to Plate Suite* [Data set]. https://www.ers.usda.gov/data-products/purchase-to-plate

U.S. Department of Agriculture, Economic Research Service. (2026a). *Food Price Outlook: Annual percent changes in selected Consumer Price Indexes, 1974 through 2025* [Data set]. Retrieved October 21, 2026, from https://www.ers.usda.gov/data-products/food-price-outlook

U.S. Department of Agriculture, Economic Research Service. (2026b). *Food Price Outlook: Historical Consumer Price Index (CPI) forecast series* [Data set]. Retrieved October 21, 2026, from https://www.ers.usda.gov/data-products/food-price-outlook

U.S. Department of Agriculture, Food and Nutrition Administration. (2026). *Official USDA Thrifty Food Plan: U.S. average, June 2026*. https://fns-prod.azureedge.us/sites/default/files/resource-files/cnpp-costfood-june2026.pdf

U.S. Department of Agriculture, Food and Nutrition Service. (2021). *Thrifty Food Plan, 2021* (FNS-916). https://www.fna.usda.gov/sites/default/files/resource-files/TFP2021.pdf

van Can, J., Sloth, B., Jensen, C. B., Flint, A., Blaak, E. E., & Saris, W. H. M. (2014). Effects of the once-daily GLP-1 analog liraglutide on gastric emptying, glycemic parameters, appetite and energy metabolism in obese, non-diabetic adults. *International Journal of Obesity*, *38*(6), 784–793. https://doi.org/10.1038/ijo.2013.162

‡ Dietary Guidelines for Americans, for the saturated-fat limit below 10% of energy. The author should add the edition actually used, with its verified URL. This audit did not verify one, so no reference text is supplied.

Optional: Hungund, S. (2026). *The GLP-1 nutritional paradox: A structured review with novel quantitative frameworks for sarcopenic risk and micronutrient adequacy in GLP-1 receptor agonist pharmacotherapy* [Preprint]. Research Square. https://doi.org/10.21203/rs.3.rs-10929531/v1 (DOI from Europe PMC; check on Crossref before use).

In-text changes that follow from this list: rename "USDA FNS, 2026" to "USDA FNA, 2026", introducing it as "(U.S. Department of Agriculture, Food and Nutrition Administration [USDA FNA], 2026)"; rename "NCHS, n.d.-a, n.d.-b" to "NCHS, 2022a, 2022b".

---

## 7. Prioritised fix list

1. **§1, Almandoz energy sentence:** reframe the figures as intakes "recommended as safe during weight reduction", not guidance for people on anti-obesity medication (claim 7).
2. **§2.4, protein:** remove Mozaffarian 2025 as a source for a numeric protein target and cite Almandoz's "≥60–75 g/day and up to 1.5 g/kg" (claim 33). Put the citations in alphabetical order.
3. **§4.1, advisory quotes:** replace the "healthful foods …" assessment quote with the §5.3 recommendation, and restate the supplement point using the advisory's own wording (claims 35–36).
4. **§1, TFP description:** replace "nutritious diet at minimal cost" with "the cost of a healthy, practical diet on a limited budget" (claim 13).
5. **TFP benchmark (§2.2, §3.1, §4.1, Table 1 note, Figure 1 caption):** state that the costs are for individuals in four-person households, give the one-person figures ($10.03 and $12.60 a day), and revisit "a single adult" and "about 10% above" (claims 23–24). Consider adding the 51–70 benchmarks.
6. **§2.4, vitamins D and E:** add Fulgoni et al. (2011) and remove "supplements are the usual source" (claim 31).
7. **§2.4, uncited requirements:** cite IOM (2005) for the AMDRs, fibre, LA/ALA shares and the 70/57 kg reference weights (confirm the page); cite NASEM (2019) for the CDRR; cite the Dietary Guidelines for saturated fat (claims 28–30, 32).
8. **§1, novelty sentence:** use the replacement in §5.
9. **§2.4, FNDDS gaps:** add fluoride and chloride (claim 34).
10. **References:** apply the corrected list in §6 (Fulgoni "III"; NCHS 2022a/b and exact titles; PP-NAP title; FNA as the 2026 author; NASEM abbreviation at first use; retrieval dates on the ERS datasets; pin cites for direct quotes).
11. **Before release:** confirm the companion preprint URL is publicly live, since it is dated 24 Oct 2026 and was visible only when logged in. Re-check the ERS forecast after its 23 Oct 2026 update, or keep "September 2026 forecast" explicit.
12. **Optional:** say that van Can's 16% is pooled across 1.8 and 3.0 mg; label the 31% grocery-price rise as computed from ERS data; cite the WWEIA categories and the solver software.
