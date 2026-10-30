# Citation audit: Paper 12, "Paying for protein: protein-named US packaged foods, nutrients and breakeven prices"

Auditor: independent citation audit (Claude, Anthropic; did not write the manuscript), 28 October 2026.
Manuscript audited: `/home/claude/p12/pkg/manuscript/manuscript.md` (version 1) and `README.md`.
The manuscript was not edited.

## How sources were checked

- Crossref metadata (`api.crossref.org/works/{DOI}`, via WebFetch) for all 12 DOIs. Curl from the build machine is blocked by the proxy (403), so WebFetch and a Chrome tab I opened myself were used. That tab is now closed. I did not touch any other tab.
- Europe PMC REST abstracts (`resultType=core`) for Kaur 2017, Taillie 2017, Drewnowski 2010, Drewnowski 2025, Drewnowski & Conrad 2024, Beltrá 2024, McKeon & Hallman 2019, Ravandi 2025, Monteiro 2019, Zhou 2026, Koop 2024 (new). I also read the Koop 2024 full text (Europe PMC full-text XML).
- Full text or publisher pages: Lee et al. 2024 (e-fsbh.org, full text: abstract and Methods), Zhou et al. 2026 (nature.com, open full text: abstract, Results, Methods, citation meta tags), CHOICE article (choice.com.au, full text and page metadata), eCFR 21 CFR 101.54 and 101.9(c)(7) (ecfr.gov, current text), FDC API guide (licensing section), FDC Download Datasets page, FDC Data Documentation page, BLS copyright page, and the GroceryDB GitHub README plus the header and first rows of `data/GroceryDB_foods.csv`.
- Abstract only: McKeon & Hallman 2024 (Crossref abstract), Ravandi 2025 (the Nature page is paywalled, so I used the abstract, the Data availability statement and the public repository).
- TheJournal.ie: in Chrome the article is behind a sign-in wall after the first paragraphs, and I did not sign in. WebFetch returned the server-side text, and the quotes below come from that WebFetch result. **Peter should confirm them by reading the article while signed in.**
- BLS series: checked against the package's own `data/raw/bls_ap_2024_2026.tsv`. All 11 series IDs are present, and the October 2025 value is "-" (not published). I did not refetch the series from bls.gov.

## Summary

Every reference exists and its DOI resolves to the cited work. Bibliographic details are mostly correct. Two content problems are serious, and the novelty claim has one significant gap:

1. **Ravandi et al. (2025) is misdescribed (major).** The manuscript says the GroceryDB database "withholds prices from its public release". This is false. GroceryDB's public file `data/GroceryDB_foods.csv` (50,578 rows) has `price`, `price percal` and `package_weight` columns, filled with values (2021 data from Walmart, Target and Whole Foods). The README also says that "price per calorie, and price per gram" are in the cleaned dataset. The "obstacle is data" argument in §1 therefore needs rewriting. Open US shelf prices do exist, but they date from 2021 and cover only three retailers.
2. **Lee et al. (2024) is over-generalised (moderate).** The counts of 289 and 1,230 are correct. However, the study covered only products in Mintel's **nutritional supplements and drinks** categories, in ready-to-drink and powder forms. Conventional foods made up under 1% of the data and were excluded. The next sentence in the manuscript ("Bars, shakes, cereals, chips…") implies a grocery-wide count, which the study does not support.
3. **Uncited close prior work (major for novelty).** Koop et al. (2024), *Public Health Nutrition* 27(1), e211, compared 299 high-protein with 286 normal-protein ultra-processed foods on the German market. It reported nutrients, additives, sweeteners, salt and **price**: high-protein products cost on average 132% more per 100 g (median €1.9 vs €0.8 per 100 g). Its main findings (less sugar, more salt, more additives and sweeteners in high-protein products) closely match this paper's. It must be cited and discussed, and it is a peer-reviewed premium figure to set beside the 31% and 50% press figures.

Smaller corrections:
- Zhou et al. (2026) now has a volume, issue and pages: 7(10), 1011–1020.
- The CHOICE article is bylined to Margaret Rafferty, so it should be cited under her name. The page metadata names Grace Smith instead.
- TheJournal.ie's title ends in a question mark (already correct), and the outlet now calls itself *The Journal*.
- Calling CHOICE and TheJournal "trade press" is wrong. CHOICE is a consumer organisation and The Journal is a news outlet.
- Drewnowski (2010) does not support the sentence in §4.2 it is cited for.
- The Taillie (2017) paraphrase should say "a given low-content claim".
- A new FDC Branded release (2026-10-29) is now posted, so "April 2026 release" should be described as the release current when the data were retrieved.

## Claims table

| # | Manuscript claim (location) | Source | Verdict | Evidence (what I read) |
|---|---|---|---|---|
| 1 | Mintel data: 289 high-protein product launches worldwide in 2013 and 1,230 in 2023 (§1) | Lee et al., 2024 | **Partly supported. Narrow the wording.** | Full text: "Number of products: more than quadrupled, increasing from 289 to 1,230." Methods: data from Mintel. Collection "focused on products marketed as high protein, specifically within the categories of nutritional supplements and drinks". Conventional foods were under 1% and were excluded, leaving only RTD and powder forms. Suggested wording: "…counted 289 high-protein supplement and drink launches (ready-to-drink and powder) in 2013 and 1,230 in 2023." |
| 2 | "High"/"excellent source" claim requires ≥20% DV per RACC; "good source" 10–19% (21 CFR 101.54(b)(1), (c)(1)) (§1, Table 1) | 21 CFR 101.54 | **Supported** | eCFR current text. (b)(1): "high," "rich in," or "excellent source of" when the food has "20 percent or more of the RDI or the DRV per reference amount customarily consumed". (c)(1): "good source," "contains," or "provides" at "10 to 19 percent". Note: both paragraphs exclude meal and main-dish products (§101.13(l), (m)), which have their own rule in (b)(2)/(c)(2). That matters because frozen dinners are in the sample, so add a clause. Also, 101.54(e) defines "more/added/extra/plus" protein claims, which the E1 phrase list partly matches. Consider citing it. |
| 3 | Protein DV is 50 g for adults and children ≥4 y (21 CFR 101.9(c)(7)(iii)) | 21 CFR 101.9 | **Supported** | (c)(7)(iii): "a value of 50 grams of protein shall be the DRV for adults and children 4 or more years of age". |
| 4 | When a protein claim is made, protein %DV must be declared and corrected for quality (101.9(c)(7)(i)–(ii)) | 21 CFR 101.9 | **Supported** | (c)(7)(i): the %DV of the "corrected amount of protein per serving… shall be given if a protein claim is made for the product". (ii) defines the PDCAAS-corrected amount. |
| 5 | Spanish study of 4,325 processed foods: 90.8% of protein-claim foods "less healthy" (PAHO NPM); more of them high in sodium than non-claim foods | Beltrá et al., 2024 | **Supported** | Abstract (EPMC): 4,325 foods, 13% with protein claims; 90.8% "less healthy"; proportions high in fat or sodium were larger among foods with protein claims, and more of them contained sweeteners. Optional: the study also found more sweeteners and fewer foods high in free sugar, which matches this paper's findings. |
| 6 | Preliminary US abstract using proprietary Label Insight data: protein claims most common in dairy, frozen foods and cereals | McKeon & Hallman, 2019 | **Supported** | Abstract (EPMC): Label Insight database (>330,000 foods); the three categories with "the greatest proportion of protein claims relative to all products in that category" were Dairy, Frozen Food, and Cereal & Breakfast Foods. It also compared nutrients (cereal: protein and fat higher). Suggest saying it also compared nutrient content. Calling Label Insight "proprietary" is a fair description (a commercial database), but the abstract does not use that word. |
| 7 | 1,022 US adults rated a protein cereal healthier, although per cup it had more sugar, sodium and calories | McKeon & Hallman, 2024 | **Supported** | Crossref abstract: Special K Original vs Special K Protein; n = 1,022; once servings were equalised to one cup, the protein version had more sugar, sodium and calories. |
| 8 | 145,609 US launches 2015–2024; quote "imperfect signals of overall nutritional quality"; protein claims grouped with other "Plus" claims; no price analysis | Zhou et al., 2026 | **Supported. Update the reference.** | Full text (nature.com): "final analytical sample included 145,609 products"; Mintel GNPD 2015–2024; Plus claims include "High/Added Protein"; abstract says "attribute-based claims are imperfect signals of overall nutritional quality". The quoted phrase appears in the title and the abstract. I found no price analysis in the text (no occurrence of "price"). I did not inspect the supplementary figures for any separate protein-claim breakdown, so "did not analyse protein separately" is unverified. The manuscript does not say that, though. |
| 9 | Purchases with a "low" claim did not necessarily have better nutrient profiles (§1) | Taillie et al., 2017 | **Supported with nuance** | Abstract (EPMC): purchases with *any* low-content claim had lower mean energy, sugar, fat and sodium densities, but "purchases featuring a given low-content claim did not necessarily offer better overall nutritional profiles". Suggest: "…purchases carrying a given low-content claim did not necessarily have better overall nutrient profiles…" |
| 10 | Health-related claims have a substantial effect on choices, mostly in artificial settings | Kaur et al., 2017 | **Supported** | Abstract (EPMC): "Health-related claims have a substantial effect on dietary choices. However, this finding is based on research mostly conducted in artificial settings." OR 1.75 (1.60–1.91). |
| 11 | CHOICE audited 175 Australian supermarket products; "around 50% more per 100 grams" for products promoting protein | CHOICE, 2026 | **Supported. Fix author and description.** | Full text: "an audit of 175 supermarket products, comparing products labelled as high-protein to their regular versions… you'll pay around 50% more per 100 grams for products that promote protein on the label." The comparison is against **regular versions**, so it is a matched comparison like C2. Worth saying. The byline is "by Margaret Rafferty", fact-checked, dated 8 Sep 2026. The page's `author`/schema metadata says "Grace Smith", but APA cites the visible byline. The article also computes protein per dollar (Coles Greek yoghurt: about 10% more protein per dollar for the added-protein version), which supports the paper's point about which yardstick to use. |
| 12 | TheJournal.ie: basket of 10 Irish products; average mark-up 31% per 100 g or 100 ml; lower price per gram of protein in most protein versions (Flynn, 2026) | Flynn, 2026 | **Supported (via WebFetch; sign-in wall in browser)** | WebFetch text: "we compared the 'high protein' and normal versions of a basket of 10 products"; "the average mark-up per 100g or 100ml was 31%"; "Across the rest of our basket… you were paying a lower price per gram of protein in the protein versions". One product (Avonmore protein milk) was about the same, at 5c per gram. So "most" is accurate: 9 of 10 cheaper per gram, 1 equal. Byline Valerie Flynn, 29 Sep 2026. **Re-verify while signed in.** |
| 13 | "Consumer groups outside the US" (§1) and "non-US trade-press figures/audits" (§2.4, §4.3) | CHOICE; Flynn | **Mislabelled** | CHOICE is a consumer organisation; The Journal is a news outlet. Neither is trade press. Suggested: "a consumer organisation (CHOICE) and a news outlet (The Journal)…" and "non-US consumer and news audits". |
| 14 | Drewnowski (2010) showed protein is associated with higher price per 100 g after adjustment for energy | Drewnowski, 2010 | **Supported** | Abstract: "protein, fiber, vitamins, and minerals were associated with higher price per 100 g, after adjustment for energy" (1,387 foods, FNDDS 1.0 and CNPP prices). |
| 15 | Later work priced protein from dairy, eggs, beans and pulses per gram | Drewnowski, 2025; Drewnowski & Conrad, 2024 | **Mostly supported** | 2025: cost of a 1-oz equivalent of PDCAAS-corrected protein; milk, yogurt and cheese "comparable with eggs and beans in terms of protein cost". 2024: pulses "among the lowest-cost protein sources (per 100 g and per 100 kcal)". Neither abstract says "per gram". Suggest "priced protein from dairy, eggs, beans and pulses". |
| 16 | "The more general point is the one Drewnowski made… (Drewnowski, 2010, 2025): whole foods such as eggs, milk and beans remain among the cheapest sources of protein in the US" (§4.2) | Drewnowski 2010, 2025 | **2010 does not support this; 2025 partly does** | The 2010 abstract does not address eggs, milk or beans as cheap protein. It reports that meats had the highest price per serving and that protein was linked to higher price per 100 g. The 2025 paper supports milk, eggs and beans being comparable in protein cost, and Drewnowski & Conrad (2024) support pulses as low-cost protein. Fix: cite "(Drewnowski, 2025; Drewnowski & Conrad, 2024)" and drop 2010 here. |
| 17 | The largest open grocery database with processing scores withholds prices from its public release (§1) | Ravandi et al., 2025 | **Contradicted** | Abstract: GroceryDB has over 50,000 items from Walmart, Target and Whole Foods, analysed "by store, food category and price range". Data availability statement: GroceryDB "is available to the public" and is "openly available". The public GitHub file `data/GroceryDB_foods.csv` has 50,578 rows, and its header includes `price`, `price percal` and `package_weight`, with values present (for example 5.29, 2.79). README: "Calories, price per calorie, and price per gram are found in this dataset." "Largest open grocery database with processing scores" is unverified; it is plausible, but I found no source stating it. Rewrite the passage (see the fix list). |
| 18 | Ingredient marker classes chosen with reference to substances and cosmetic additives characteristic of NOVA UPF | Monteiro et al., 2019 | **Supported** | Abstract (EPMC) names food substances never or rarely used in kitchens (HFCS, hydrogenated or interesterified oils, hydrolysed proteins) and additive classes (flavours, flavour enhancers, colours, emulsifiers, sweeteners, thickeners…). |
| 19 | FDC Branded Foods is a public database of label information supplied by manufacturers and data aggregators | USDA ARS, 2026 | **Supported (aggregators: not explicit on the page I read)** | FDC Data Documentation: Branded Foods holds "Data from labels of national and international branded foods collected by a public-private partnership"; source "Manufacturers: based on food label information". "Data aggregators" is not stated on that page. Either change it to "collected through a public-private partnership", or cite a page that names the data partners. |
| 20 | FDC data are public domain under CC0 1.0 Universal (Transparency; README) | FDC API guide | **Supported** | API guide, Licensing: "USDA FoodData Central data are in the public domain and they are not copyrighted. They are published under CC0 1.0 Universal (CC0 1.0)". FDC asks users to cite FDC as the source and gives a suggested citation. |
| 21 | BLS average price data are a US government work (Transparency; README "Public domain") | BLS copyright page | **Supported** | BLS: "everything that we publish… is in the public domain, except for previously copyrighted photographs and illustrations". Suggest saying "public domain (BLS)" rather than only "US government work". |
| 22 | BLS AP series IDs, no October 2025 value published | BLS, 2026 | **Consistent with package data** | All 11 series IDs are in `bls_ap_2024_2026.tsv`, and the 2025 M10 value is "-" (for example eggs APU0000708111). I did not cross-check against live bls.gov. |
| 23 | FDC Branded "April 2026 release" (title, abstract, §2.1, Conclusion) | USDA ARS, 2026 | **Accurate, but now superseded** | The Download Datasets page lists `FoodData_Central_branded_food_csv_2026-04-30.zip` and, newer, `FoodData_Central_branded_food_csv_2026-10-29.zip` (October 2026). Suggested wording: "the April 2026 release, the latest available when the data were retrieved on 22 October 2026". |
| 24 | Novelty: "I am not aware of a US study that brings these strands together for protein-marketed packaged foods using open data" (§1) | (none) | **Holds only if narrowed; uncited prior work** | See the Novelty section. Koop et al. (2024) did nutrients, additives, sweeteners and price for high-protein vs normal UPF (Germany). It is uncited and has to be added. |

## In-text citations vs reference list

There is a one-to-one match: 19 in-text sources and 19 reference entries. Every in-text citation has an entry, and every entry is cited at least once. Checked: Lee 2024; 21 CFR 101.54; 21 CFR 101.9; Beltrá 2024; McKeon & Hallman 2019, 2024; Zhou 2026; Taillie 2017; Kaur 2017; CHOICE 2026; Flynn 2026; Drewnowski 2010, 2025; Drewnowski & Conrad 2024; Ravandi 2025; USDA ARS 2018, 2026; Monteiro 2019; BLS 2026.

Notes:
- If CHOICE is re-attributed to Rafferty, all in-text "(CHOICE, 2026)" become "(Rafferty, 2026)": §1, §2.4 and Table/scenario text.
- The CFR in-text style "(21 CFR 101.54(b)(1))" is acceptable. APA legal style would be "(21 C.F.R. § 101.54(b)(1), 2026)". Pick one and use it throughout, including the Table 1 and Figure 1 captions.
- Koop et al. (2024) must be added (new entry).

## Reference table

| Reference | DOI / URL status | Metadata check | Correction needed |
|---|---|---|---|
| Beltrá, Borrás & Ropero (2024) | 10.3390/nu16244281 resolves (Crossref) | Correct: Nutrients 16(24), 4281 | None. Optional APA: "Article 4281". |
| CHOICE (2026) | URL live; published 2026-09-08 | Byline Margaret Rafferty (visible); metadata author Grace Smith | **Author → Rafferty, M.**; title ends with "?" (CHOICE as site name) |
| Drewnowski (2010) | 10.3945/ajcn.2010.29300 resolves | Correct: AJCN 92(5), 1181–1188 | None (but see claim 16) |
| Drewnowski (2025) | 10.1016/j.cdnut.2024.104539 resolves | Correct: Curr Dev Nutr 9(1), 104539, Jan 2025 | None. Optional "Article 104539". |
| Drewnowski & Conrad (2024) | 10.3389/fnut.2024.1438369 resolves | Correct: Front Nutr 11, 1438369 | None. Optional "Article 1438369". |
| Flynn (2026) | URL live (sign-in wall) | Byline, date and title confirmed | Site now styled *The Journal*; keep TheJournal.ie or use "The Journal (TheJournal.ie)". |
| 21 C.F.R. § 101.9 | eCFR | Section title "Nutrition labeling of food." | None |
| Kaur, Scarborough & Rayner (2017) | 10.1186/s12966-017-0548-1 resolves | Correct: IJBNPA 14(1), 93 | None |
| Lee, Cho, Yi & Park (2024) | 10.52361/fsbh.2024.4.e9 resolves | Correct: Food Suppl Biomater Health 4(2), e9 | None (content fix only) |
| McKeon & Hallman (2019) | 10.1093/cdn/nzz051.P04-149-19 resolves | Correct: Curr Dev Nutr 3(Suppl. 1) | None. APA would write "3(Supplement_1)"; either is acceptable. |
| McKeon & Hallman (2024) | 10.3390/foods13081139 resolves | Crossref given name "Gina Pope" → G. P.; Foods 13(8), 1139 | None |
| Monteiro et al. (2019) | 10.1017/S1368980018003762 resolves | 12 authors in correct order; PHN 22(5), 936–941 | None |
| 21 C.F.R. § 101.54 | eCFR | Section title confirmed | None |
| Ravandi et al. (2025) | 10.1038/s43016-024-01095-7 resolves | Correct: Nat Food 6(3), 296–308 | None (content fix only) |
| Taillie et al. (2017) | 10.1016/j.jand.2017.01.011 resolves | Correct: JAND 117(9), 1366–1374.e6 | None |
| BLS (2026) | download.bls.gov path as given | Not refetched (proxy) | Optional: name the dataset "Average Price Data (AP)". |
| USDA ARS (2018) SR Legacy | fdc.nal.usda.gov | SR Legacy April 2018 zip listed on the Download page | None (FDC suggests citing FDC as source; fine) |
| USDA ARS (2026) Branded | fdc.nal.usda.gov | 2026-04-30 zip listed | Add "retrieved October 22, 2026" or a note that it was superseded on 29 Oct 2026. |
| Zhou, Zheng, Kaiser & Gómez (2026) | 10.1038/s43016-026-01435-9 resolves | Published online 24 Sep 2026; **now in Nat Food 7(10), 1011–1020** (citation meta tags) | **Replace "Advance online publication" with 7(10), 1011–1020.** |
| **Koop et al. (2024)**, new | 10.1017/S1368980024001836 (EPMC; PMC11604323) | PHN 27(1), e211 | **Add** |

## Corrected reference entries (APA 7)

Rafferty, M. (2026, September 8). *How much is the protein premium costing you?* CHOICE. https://www.choice.com.au/food-and-drink/nutrition/food-labelling/articles/how-much-is-the-protein-premium-costing-you

Zhou, P., Zheng, Y., Kaiser, H. M., & Gómez, M. I. (2026). On-package claims are imperfect signals of overall nutritional quality. *Nature Food, 7*(10), 1011–1020. https://doi.org/10.1038/s43016-026-01435-9

Koop, J., Fedde, S., Hägele, F. A., Beunink, C., Müller, M. J., & Bosy-Westphal, A. (2024). Nutritional value and environmental aspects of high-protein ultra-processed foods on the German market. *Public Health Nutrition, 27*(1), e211. https://doi.org/10.1017/S1368980024001836
(Author initials are from Europe PMC. Full given names were not checked in Crossref; verify before publishing.)

US Department of Agriculture, Agricultural Research Service. (2026). *FoodData Central: Branded Foods* (April 30, 2026 release) [Data set]. Retrieved October 22, 2026, from https://fdc.nal.usda.gov/download-datasets

All other entries can stay as written.

## Suggested text fixes (for the author; not applied)

- §1, Lee: "Using the Mintel database, Lee et al. (2024) counted 289 high-protein supplement and drink products (ready-to-drink and powder) launched worldwide in 2013 and 1,230 in 2023. Conventional foods were excluded."
- §1, data obstacle: replace the Ravandi sentence with wording such as: "Current US product-level prices are held mostly in proprietary scanner panels or retailer systems. The largest open alternative, GroceryDB, publishes 2021 shelf prices for about 50,000 items from three retailers (Ravandi et al., 2025)." Then either use GroceryDB prices as a check on the breakeven thresholds, or say why it was not used (2021 prices, three retailers, matching to FDC GTINs).
- §1, prior work: add Koop et al. (2024) after Beltrá. In Germany, high-protein ultra-processed foods had less sugar and fat, more salt and more additives (sweeteners, polyols, flavourings), and cost on average 132% more per 100 g than normal-protein comparators.
- §1/§2.4/§4.3: "consumer groups" and "trade-press" → "a consumer organisation and a news outlet" / "non-US consumer and news audits". Consider adding Koop's peer-reviewed 132% as a third premium scenario.
- §1, Taillie: "…purchases carrying a given low-content claim did not necessarily have better overall nutrient profiles…"
- §1/Table 1, CFR: add "(meal and main-dish products follow separate rules, §101.54(b)(2), (c)(2))". Optionally cite 101.54(e) for "more/added/extra/plus" claims.
- §4.2: change "(Drewnowski, 2010, 2025)" to "(Drewnowski, 2025; Drewnowski & Conrad, 2024)", and say "found" rather than "made from food-price data" if 2010 is dropped.
- §2.1: say "label information collected through a public-private partnership with manufacturers", unless a source naming the aggregators is added.
- §2.1 / Abstract: note that the April 2026 release was the latest when retrieved (a 29 October 2026 release now exists).

## Novelty assessment

Searches: Europe PMC (title queries for "protein claims", "protein claim", high-protein products/foods/snacks/bars with market/survey/labels/price, protein-enriched products, protein with price/cost/affordability; full-text queries for protein claim with price/cost, FoodData Central branded with claims). Web search for high-protein price-premium comparisons. GroceryDB repository.

Relevant prior work:
- **Koop et al. (2024), Germany**, peer reviewed, uncited. 299 high-protein vs 286 normal-protein UPF from supermarkets and online shops. Compared nutrients, energy density, Nutri-Score, additive count, hyper-palatability, sweeteners and **price per 100 g**: on average 132% higher; median €1.9 vs €0.8 per 100 g. Findings: lower sugar and fat, higher fibre and protein, higher salt, more additives (environmentally persistent sweeteners, sugar alcohols, flavourings). This is the closest precedent for both halves of the paper.
- **Beltrá et al. (2024), Spain** (cited): nutrient profile of foods with protein claims, with sweeteners and sodium.
- **McKeon & Hallman (2019), US** (cited): protein-claim prevalence and nutrient comparison on Label Insight, conference abstract only.
- **Zhou et al. (2026), US** (cited): claims including High/Added Protein vs the UK NPM, Mintel GNPD; no prices.
- **Grey literature**: CHOICE (Australia, 175 products, about 50%), The Journal (Ireland, 10 products, 31%), Consumer NZ (28 March 2025, about 17 named products, per-100 g price examples; WebFetch summary only), and safefood (island of Ireland, high-protein snack survey, undated; content not verified).
- **Price data**: GroceryDB (Ravandi et al., 2025) gives open 2021 US prices for about 50k products, so US product prices are not entirely proprietary.

I found no study that:
(a) uses an open US census of branded labels (FoodData Central) to profile protein-named products against same-category and same-brand comparators, and
(b) expresses value as breakeven prices against BLS whole-food protein costs.

Verdict: the novelty claim **holds only in narrowed form**. Suggested wording: "To my knowledge, this is the first US analysis to use open label data (FoodData Central) to profile protein-marketed packaged foods against same-category and same-brand comparators, and to express their value as breakeven prices against whole-food protein costs. Earlier work did this with proprietary or non-US data (Koop et al., 2024; Beltrá et al., 2024; McKeon & Hallman, 2019; Zhou et al., 2026)."

Do not claim that open US price data are unavailable (GroceryDB). Do not imply the nutrient-and-additive findings are new; they replicate the German and Spanish findings in US data, which is itself worth saying.

## Not verified

- TheJournal.ie text is behind a sign-in wall in the browser. The quotes come from a WebFetch extraction and should be confirmed by Peter.
- Ravandi full text is paywalled. "Largest open grocery database with processing scores" has no source.
- Zhou supplementary figures were not inspected.
- Koop authors' full given names were not checked against Crossref.
- BLS series values were not refetched from bls.gov (the proxy blocks it). They were checked against the package's own raw file only.
- Consumer NZ and safefood details come from WebFetch summaries only.
