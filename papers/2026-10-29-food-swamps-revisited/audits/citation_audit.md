# Citation audit: Paper 17, "Food swamps and obesity revisited"

Auditor: independent citation auditor (Claude), 22 October 2026. The manuscript was not edited.
Manuscript audited: `/home/claude/p17/pkg/manuscript/manuscript.md`. The scoping brief was used only for leads.

## 0. What was read and how

| Source | What I read | How |
|---|---|---|
| Cooksey-Stowers, Schwartz & Brownell (2017) | **Full text**: abstract, §§1–5, all 9 main tables, Appendix Tables A1–A5 with captions and notes, and the reference list (refs 1–49 visible) | Live mdpi.com HTML in my own Chrome tab, with table text extracted from the DOM. The tables are HTML text, not images. |
| Dunn (2010), Anderson & Matsa (2011), Currie et al. (2010), Cobb et al. (2015), Spence et al. (2009), Lee et al. (2022), Young (2022), Andrews et al. (2019), Montiel Olea & Pflueger (2013), Bast & Buchhold (2017), Greenlund et al. (2022), Zhang et al. (2014) | Abstracts | OpenAlex `abstract_inverted_index`, reconstructed |
| Black et al. (2014) | Abstract | Europe PMC REST (`resultType=core`) |
| Courtemanche & Carden (2011) | Abstract excerpts and bibliographic data | RePEc/IDEAS page via WebFetch |
| Lee et al. (2022) | The F = 104.7 threshold sentence | arXiv 2010.05058 PDF via WebFetch |
| Anderson & Rubin (1949), Cameron & Miller (2015) | Metadata only; cited for standard methods | Crossref |
| All 17 DOIs | Crossref `/works/{doi}` JSON (title, authors, container, volume, issue, pages, year, update-to/updated-by) | Fetched same-origin inside my Chrome tab on api.crossref.org. Bash access to Crossref and MDPI is blocked by the proxy (403). |
| Data URLs | ERS download page, 2025 Atlas ReadMe and VariableList, the archived XLS headers, CDC Socrata metadata for `mssc-ksj7`, the GitHub API for the plotly commit, QLever `?cmd=stats`, data.census.gov table API, api.census.gov, ODbL licence page, PCD article page | Chrome tab and local files in `pkg/data/raw` |

I used one Chrome tab, created for this audit and closed at the end. I did not touch any other tab or type any credentials. DukeSpace (the first author's 2016 dissertation) showed a bot-check page, so I did not read it. The Wiley page for the Cobb erratum failed to load.

---

## 1. Claims table: attributed claims and quotations

Verdicts: ✅ supported or verbatim · ⚠️ supported with caveat or wording fix · ❌ not supported or misattributed.

### 1a. Claims about the original (Cooksey-Stowers et al., 2017)

| # | Manuscript location and claim | Source check | Verdict |
|---|---|---|---|
| O1 | Abstract and §1: food swamps predict obesity better than deserts. Quote: "food swamps have a positive, statistically significant effect on adult obesity rates" | Abstract, verbatim | ✅ |
| O2 | Abstract: IV "about 20 times" OLS; §1: 2.604 vs 0.125 | Table 8: 2.604 (1.076). Table 6: 0.125 (0.0443). Ratio 20.8. | ✅ |
| O3 | §1: zoning laws "could lower obesity rates by about three percent" | §4.3, verbatim ("policies, like zoning laws, could lower obesity rates by about three percent") | ✅ quote. **But see O24.** |
| O4 | §1: publisher page listed 549 citations on 22 Oct 2026; OpenAlex 642 | MDPI page showed "Citations 549" today. OpenAlex W2770887445 `cited_by_count` = 642 today. Crossref `is-referenced-by-count` = 546. | ✅ |
| O5 | §1: instrument from ESRI StreetMap North America; no code published | §2.1 names "ArcGIS ESRI StreetMap North America". The article has no data or code statement. | ✅ |
| O6 | §1, §2.1, §4.1: first-stage F 7.87, 7.44, 15.66 | Table 7 | ✅ |
| O7 | §1: "no weak-instrument-robust intervals were reported" | None in Tables 7–9 or A5. Note: §4.5 of the original does acknowledge a "potentially weak instrument" and threats to exclusion. | ⚠️ True, but see fairness item F1 |
| O8 | §2.1: Table 6 OLS 0.120 (0.0579), 0.115 (0.0499), 0.125 (0.0443); N 3,069/3,069/3,055; R² 0.559–0.560 | Table 6 | ✅ |
| O9 | §2.1: Table 8 IV 1.510 (0.434), 1.277 (0.383), 2.604 (1.076) | Table 8 | ✅ |
| O10 | §2.1: Table 9 stratified by commuting and inequality; A4/A5 add total food outlets | Table 9, A4, A5 | ✅ |
| O11 | §2.1: "read from the article's HTML … both carry the tables as text" | The HTML tables are text (confirmed). I did not check the PDF. | ✅ (HTML part) |
| O12 | §2.2: the paper used "2009 data" and accessed the Atlas on 1 June 2015 | §2.1 "This paper used 2009 data…". Ref 45 "(accessed on 1 June 2015)". | ✅ |
| O13 | §2.2: Feb 2014 release has 2007 and 2011 counts; Nov 2012 has 2007 and 2009; Aug 2015 has 2007 and 2012 | Local XLS headers: Nov 2012 has FFR07/FFR09 etc.; Feb 2014 has 07/11; Aug 2015 has 07/12. All three are listed as archived versions on the ERS page. | ✅ |
| O14 | §2.4: 1,672 counties had no exit in the original | §4.5 "There were 1672 counties with no highway exits" | ✅ |
| O15 | §2.5: N = 3,108 in the original's table titles; SEs clustered by state | Titles of Tables 4, 6, 7 and 8 say 3108. §3.3 says "robust standard errors clustered by state". | ✅ |
| O16 | §2.5: Table 6–8 notes list fitness centres, natural amenities, % Black, % Hispanic, people over 65, poverty, county size | Table 6, 7 and 8 notes, verbatim list | ✅ |
| O17 | §2.5: Tables 9 and A4 show % bachelor's in place of people over 65 | Tables 9 and A4 rows: LILA, recreation, amenities, milk:soda, bachelor's, Black, Hispanic, poverty, square miles (A4 also total food stores) | ✅ |
| O18 | §2.5: Table 3 medians of 12.2% bachelor's and 80.2% drives to work | Table 3 | ✅ |
| O19 | §3.1: Table 3 store-count medians and SDs (FFR 15, 228.60; GROC 6, 76.80; SUPERC 0, 2.64; CONVS 16, 87.50; SPECS 1, 37.95; fitness 2, 30.31; obesity 30.5, 4.16) | Table 3, all match. **Additional point:** Table 3 also has a second row, "Number of fast food retailers 15.0 (228.58)", which matches the 2007 SD exactly. Worth adding. | ✅ |
| O20 | §3.2: control coefficients (amenities −1.039, SE 0.196; milk:soda 1.501, SE 1.670; constant 34.23, SE 1.573; LILA 0.0138, SE 0.0148) | Table 6, column 3 | ✅ |
| O21 | §3.2: label ambiguity. Table 1 and §2.2.2 put supercenters in the #1 numerator; the Table 3 note says the reverse; §3.3 describes "expanded RFEI 1 with supercenters categorized as healthy" | All three confirmed. The §3.3 quote is verbatim inside "the version of the expanded RFEI 1 with supercenters categorized as healthy". **The manuscript misses one:** §2.4.1 also lists "(2) Expanded RFEI with supercenters categorized as 'healthy' and (3) Expanded RFEI 2 … 'unhealthy'", which matches the Table 3 note. Table 4 of the original, however, follows Table 1. | ✅ (add §2.4.1 and Table 4) |
| O22 | §3.2 and Table 4 row: Table 3 traditional RFEI median 3.5 (SD 1.86); Table 4 mean 3.89 | Table 3; Table 4 cut-off 3.89, with the note "cutoff values … based on the mean" | ✅ |
| O23 | §3.3: correlations of exits with obesity −0.20, fast food 0.86, fitness 0.84, population 0.86, square miles 0.14, traditional RFEI −0.07 | Table A3 | ✅ |
| O24 | **Conclusion (§5)**: "the zoning effect of about three **percentage points**". §3.9 also works in "three points". | The original says "about three **percent**" (§4.3) and does not say whether that is relative or absolute. Reading it as percentage points is an interpretation, not a quotation. | ⚠️ **Fix:** "the zoning effect of 'about three percent' (read here as three percentage points) derived from it", or note the reading once in §3.9 |
| O25 | §3.7: split at 80% commuting and Gini 0.41; published Ns 1,230 and 2,442 | Table 9 headers and Ns (1230/1825; 2442/613) | ✅ |
| O26 | §3.7 and Table 4: abstract quote "stronger in counties with greater income inequality"; Table 9 gives 2.737 (Gini < 0.41) and 1.564 (> 0.41) | Abstract verbatim; Table 9 verbatim. Note: the original's §3.4 says the effect "remained statistically significant in areas with lower income inequality", and §4.4 says stratifying "did not diminish the food swamp effect". The body text is therefore consistent with Table 9, and only the abstract conflicts. | ✅ (see fairness item F3) |
| O27 | §3.9: "a 1 percent increase in fast food restaurants increases obesity by approximately 0.125 percent" | §3.3, verbatim | ✅ |
| O28 | Table 4: food desert 6.2 (8.37); milk:soda 30.2 (62.10); Stata 14 vs 15 | Table 3; §2.4 "STATA/SE version 14"; §2.4.2 "Stata (version 15.0)" | ✅ |
| O29 | Table 4 row "Standard errors: Table notes 'robust'; §3.3 clustered by state" presented as a divergence | §3.3 actually says "robust standard errors clustered by state". "Robust" in the notes is therefore consistent with cluster-robust, and nothing is contradicted. | ⚠️ Present as a clarification, not a discrepancy (or drop the row) |
| O30 | §3.5: "Neither the original nor the main reproduction controls for population directly" | Population is not in any published control list. The original says socio-demographics were added "only if [VIF] was about 2 or under" (§2.4.1). | ✅ Suggest "the published control lists do not include population" |
| O31 | §4.3: "The original's reading of the coefficient as an elasticity overstated the precision of a small number" | The issue is units and magnitude, not precision. Also, the original's own §4.3 says the OLS estimates imply "about 0.003 to 0.12 percent", so the original itself gave a lower bound of the same order as the manuscript's 0.0033. | ⚠️ Reword (see F2) |

### 1b. Claims about other literature

| # | Claim (location) | What the source says | Verdict |
|---|---|---|---|
| L1 | Dunn (2010) "used interstate highways to shift restaurant supply" (§1) | Abstract: "The number of interstate exits in the county of residence is employed as an instrument for restaurant location." County level, BRFSS 2004–2006. No effect in rural counties; higher BMI among females and non-Whites in medium-density counties. | ✅ |
| L2 | Anderson & Matsa (2011) used interstate highways (§1) and found no effect (§1) | Abstract: "We exploit the placement of Interstate Highways in rural areas … We find no causal link between restaurant consumption and obesity." | ✅ |
| L3 | Currie et al. (2010): effects of fast-food proximity "in specific settings" (§1) | Abstract: within 0.1 mile of a school, 5.2% higher obesity among ninth graders; within 0.5 mile, 1.6% higher probability of gaining over 20 kg among pregnant women | ✅ |
| L4 | Black et al. (2014): "Systematic reviews have found mostly null or inconsistent associations [of local food environments with obesity]" (§1) | Abstract: a review of ten reviews on **dietary intake** and inequalities, not obesity. It reports "a trend for greater access and availability to healthy and less healthy foods relating to better and poorer dietary outcomes respectively", which is not "mostly null". | ❌ **Mis-scoped.** Drop it from this sentence, or cite it separately for diet ("evidence on diet suggests modest associations, limited by measurement; Black et al., 2014"). |
| L5 | Cobb et al. (2015): mostly null or inconsistent, "with results depending on how exposure is measured" (§1) | Abstract: "Associations between food outlet availability and obesity were predominantly null"; study quality low. Also: "Indices including multiple food outlets were most consistently associated with obesity in adults (18 expected, 1 not expected, 17 null)." Crossref lists an **erratum** (10.1002/oby.21363, *Obesity* 23(12), 2517–2519), which I could not read. | ✅. Fairness: consider adding that RFEI-type indices were the *most* consistent exposure in Cobb, which cuts in the original's favour. Check the erratum content. |
| L6 | Spence et al. (2009): RFEI used mainly at neighbourhood scale (§2.3) | RFEI computed for 800 m and 1600 m buffers in Edmonton; association only at 800 m. Their RFEI denominator is supermarkets plus specialty food stores. | ✅ (note: the original's Table 1 cites Spence [39] for a "traditional" RFEI whose denominator excludes specialty stores, an optional footnote) |
| L7 | Courtemanche & Carden (2011): supercenters hard to classify "because their effect on weight is itself debated" (§2.3) | The paper finds supercenters **increase** BMI (+0.24 per supercenter per 100,000) and obesity (+2.3 points). One study with a positive finding does not show a debate. The original (§2.2.2) cites refs [49, 50] for "both positive and negative relationships". | ⚠️ Reword: "Courtemanche and Carden (2011) estimated that Walmart Supercenters raise BMI and obesity, yet supercenters also sell fresh food; the original cited evidence in both directions." Or add the original's ref 50 after verifying it. |
| L8 | Andrews et al. (2019) and Lee et al. (2022): F values of 7–16 are where 2SLS t-tests are unreliable (§1) | Andrews et al. abstract: weak instruments make conventional IV inference unreliable and the problem remains important in practice. Lee et al.: the corrected threshold for a valid 5% t-test is F = 104.7 (arXiv text). | ✅ |
| L9 | Lee et al. (2022): need "an F well above 10" (§2.6, §4.1) | Same, F = 104.7 | ✅ (could state 104.7 explicitly) |
| L10 | Effective F of Montiel Olea & Pflueger (2013) equals the clustered Wald F with one instrument (§2.6, Table 2 caption) | MOP abstract: robust test, statistic is a scaled first-stage F. Equality in the just-identified case is standard and is stated in Andrews et al. (2019). I did not re-read that passage. | ✅ (consider citing Andrews et al. 2019 for the equality) |
| L11 | Anderson & Rubin (1949) AR sets; Andrews et al. (2019) (§2.6) | Standard attribution; Crossref metadata correct | ✅ |
| L12 | Cameron & Miller (2015): cluster-robust inference (§2.6) | Standard; metadata correct | ✅ |
| L13 | Young (2022): conventional 2SLS inference often unreliable with non-iid errors (§2.6) | Abstract: "non-iid error processes in highly leveraged regressions … adversely affect the size and power of IV tests"; F pre-tests "largely uninformative" | ✅ |
| L14 | Bast & Buchhold (2017) for the QLever SPARQL engine (§2.4) | The QLever paper (SPARQL+Text engine) is the appropriate engine citation. The OSM planet index was built with **osm2rdf**, per the endpoint stats ("converted to RDF TTL and enhanced by DE-9IM triples using osm2rdf"). | ✅ Optional: cite the osm2rdf paper (Bast, Brosi, Kalmbach & Lehmann, 2021, SIGSPATIAL; DOI not verified here, check before adding) |
| L15 | PLACES 2020 release, 2018 obesity, MRP (Greenlund et al., 2022; Zhang et al., 2014) (§2.7, §4.4) | Greenlund abstract: PLACES model-based estimates for all counties. Zhang: multilevel regression with poststratification to Census 2010 block populations. Socrata `mssc-ksj7` is "PLACES: County Data (GIS Friendly Format), 2020 release"; `obesity_adjprev` is the age-adjusted prevalence among adults aged ≥18, 2018. | ✅ |
| L16 | §4.4: "PLACES estimates use county demographic composition in their models (Zhang et al., 2014), which can induce associations with demographic covariates" | Zhang poststratifies on census population by age, sex and race; the "can induce associations" part is the author's inference | ✅ (inference, fairly worded) |
| L17 | §1: "The food-swamp paper is often read as settling the question in favour of supply-side zoning." | No source cited. This is an opinion about reception. | ⚠️ Soften ("has been cited in support of…") or support it with examples |

### 1c. Data and URL claims

| # | Claim | Check | Verdict |
|---|---|---|---|
| D1 | Atlas July 2025 release: store counts for 2016 and 2020; adult obesity only at state level for 2017 and 2022 | 2025 ZIP files dated 2025-07-30; the ReadMe says "original release date … July 2025". The VariableList has FFR16/20, GROC16/20 etc., and "Adult obesity rate, 2017*" and "2022*" (* = state-level). | ✅ |
| D2 | 2020 counts suppressed below three; 2016 counts have no zeros | Tabulated: GROC20 and FFR20 have no 1s or 2s and have many −9999; FFR16 and GROC16 have 1–3 values and no 0s | ✅ |
| D3 | §2.7: "establishments absent from County Business Patterns are coded −9999" | The ERS ReadMe defines −9999 as data "not available, not applicable, or suppressed". The CBP-absence reading is plausible but is the author's inference. | ⚠️ Quote the ERS definition and state that treating −9999 as zero is an assumption (the 1,500-county check already covers it) |
| D4 | §2.2: Census API now requires a key; ACS 2005–2009 not on data.census.gov | api.census.gov redirected to `missing_key.html` ("A valid key must be included"). data.census.gov returns "There is no table with the ID: ACSDT5Y2009.B19083"; ACSDT5Y2010.B19083 returns data. | ✅ |
| D5 | §2.2: land area from 2010 cartographic boundary file via plotly/datasets, commit 0c447c4 | The commit exists (GitHub API: 0c447c47…, 2026-05-04, "Added a Plotly x Star Wars logo."). It is the repo HEAD at retrieval, not a change to the GeoJSON, which is fine as a pin. The file has GEO_ID and CENSUSAREA (2010 cartographic schema). | ✅ |
| D6 | §2.4: QLever over the OSM planet file of 21 Sep 2026 | Endpoint stats: "PBF from …/planet-260921.osm.pbf". The README URL `qlever.cs.uni-freiburg.de/api/osm-planet` now redirects to `qlever.dev/api/osm-planet`. | ✅ (update the URL in the README) |
| D7 | OSM data licence ODbL 1.0 | https://opendatacommons.org/licenses/odbl/1-0/ resolves | ✅ |
| D8 | ERS download page URL in the reference list | Resolves. It lists the current version and archived Aug 2020, Sep 2017, Aug 2015, Feb 2014, Nov 2012, Jun 2012 and 2011 versions. | ✅ |
| D9 | Overpass API 17-state cross-check | Not opened (cross-check only) | not checked |

---

## 2. Crossref verification table

All 17 DOIs resolve on Crossref, and none has a retraction or correction notice except Cobb (erratum).

| Reference | DOI | Crossref metadata vs manuscript | Issue |
|---|---|---|---|
| Anderson & Matsa 2011 | 10.1257/app.3.1.152 | AEJ: Applied 3(1) 152–188, 2011 | ✅ |
| Anderson & Rubin 1949 | 10.1214/aoms/1177730090 | Ann. Math. Stat. 20(1) 46–63, 1949 | ✅ |
| Andrews, Stock & Sun 2019 | 10.1146/annurev-economics-080218-025643 | Annu. Rev. Econ. 11(**1**) 727–753 | Add issue (1) |
| Bast & Buchhold 2017 | 10.1145/3132847.3132921 | Title "QLever", **subtitle "A Query Engine for Efficient SPARQL+Text Search"**, CIKM '17 pp. 647–656 | Add subtitle |
| Black, Moon & Baird 2014 | 10.1016/j.healthplace.2013.09.015 | Health & Place 27, 229–242 | ✅ metadata (claim ❌, see L4) |
| Cameron & Miller 2015 | 10.3368/jhr.50.2.317 | J. Hum. Resour. 50(2) 317–372 | ✅ |
| Cobb et al. 2015 | 10.1002/oby.21118 | Obesity 23(7) 1331–1344; **updated-by erratum 10.1002/oby.21363** (23(12) 2517–2519) | Note erratum |
| Cooksey-Stowers et al. 2017 | 10.3390/ijerph14111366 | IJERPH 14(11) 1366 | ✅ (APA: "Article 1366") |
| Courtemanche & Carden 2011 | 10.1016/j.jue.2010.09.005 | J. Urban Econ. 69(2) 165–181 | ✅ |
| Currie et al. 2010 | 10.1257/pol.2.3.32 | AEJ: Policy 2(3) 32–63 | ✅ |
| Dunn 2010 | 10.1093/ajae/aaq041 | AJAE 92(4) 1149–1164 | ✅ |
| Greenlund et al. 2022 | 10.5888/pcd19.210459 | PCD 19, **article number 210459**. The publisher's suggested citation is "Prev Chronic Dis 2022;19:210459". | Replace "E31" with "Article 210459" |
| Lee et al. 2022 | 10.1257/aer.20211063 | AER 112(10) 3260–3290 | ✅ |
| Montiel Olea & Pflueger 2013 | 10.1080/00401706.2013.806694 | JBES 31(3) 358–369 (Crossref stores the family name as "Olea") | ✅ keep "Montiel Olea, J. L." |
| Spence et al. 2009 | 10.1186/1471-2458-9-192 | BMC Public Health 9(1), article 192 | APA: "*9*, Article 192" |
| Young 2022 | 10.1016/j.euroecorev.2022.104112 | Eur. Econ. Rev. 147, article 104112 | APA: "Article 104112" |
| Zhang et al. 2014 | 10.1093/aje/kwu018 | Am. J. Epidemiol. 179(8) 1025–1033 | ✅ |

---

## 3. Fairness of statements about the original

- **F1 (§1, §4.1).** The original did acknowledge the instrument's weaknesses. Its §4.5 says, citing Dunn, that "highways are an imperfect instrument", lists exclusion threats (gas stations near highways; traffic deterring activity), and says the authors "attempted to adjust for a potentially weak instrument". One sentence acknowledging this would make the critique fairer, and the critique would be no weaker for it.
- **F2 (§4.3, §3.9).** "Overstated the precision of a small number" is the wrong charge. The error is reading a level-on-ratio coefficient as an elasticity, which misstates units and magnitude. The original's §4.3 also offers "about 0.003 to 0.12 percent" for the OLS range. That lower figure is close to the manuscript's 0.0033, so the manuscript should acknowledge it.
- **F3 (§3.7).** The inequality inconsistency is between the abstract and Table 9. The original's results text ("remained statistically significant in areas with lower income inequality") and discussion are consistent with Table 9. Say so, so readers do not think the whole paper is inconsistent.
- **F4 (Table 4, SE row).** Not a real discrepancy (see O29).
- **F5 (§5 and §3.9).** Three "percent" vs three "percentage points" (see O24).
- **F6.** The label ambiguity also appears in §2.4.1 of the original. Adding it strengthens the manuscript's point.

Everything else about the original is accurately quoted or paraphrased. The six verbatim quotations checked (O1, O3, O12, O21, O26, O27) are exact.

---

## 4. Novelty

- **OpenAlex** (works citing W2770887445, 642 in total): full-text searches for replication/replicate (46 hits), reanalysis (0), re-analysis (262), reproduction (25), reproducibility (32), revisited/revisiting (60), "instrumental variable" (36) and highway (20). I also listed all 38 citing works with "food swamp" in the title. **No replication, reproduction or reanalysis of the original's data or IV was found.** The hits are applications of the food-swamp concept or county RFEI scores, for example:
  - Phillips & Rodríguez 2019/2020 (diabetes hospitalisation)
  - Bevel et al. 2023, *JAMA Oncol* (10.1001/jamaoncol.2023.0634)
  - the North Carolina GIS study 2024 (10.1080/00330124.2024.2306642)
  - Cerceo et al. 2023, a New Jersey state-level mRFEI analysis (10.1155/2023/5052613), which uses a different index and data and is not a re-run.
- **Web** search for "Cooksey-Stowers" with highway exits and replication/critique/weak instrument found the PMC copy, Boston Globe coverage (2017), an APPAM 2015 poster, the first author's **2016 Duke dissertation** "Food Swamps, Obesity & Health Zoning Restrictions on Fast Food Restaurants" (OpenAlex W2552692313; DukeSpace bot-check blocked reading), and a 2026 Preprints.org paper by Cooksey Stowers et al. on an audit tool (10.20944/preprints202608.0829), which cites the 2017 paper but does not re-analyse it.
- **Verdict:** I found no prior replication. The manuscript's implicit claim ("the IV result has not been checked") is supported, worded as "I found no published reproduction".
- **Suggested additions (optional):**
  - The dissertation may document data years and the RFEI construction, and the authors may wish to check it. Cite it only if read.
  - Atanasova et al. (2022), *Soc Sci Med* 299, 114879 (10.1016/j.socscimed.2022.114879): a systematic review of *causal-design* studies of the neighbourhood food environment. It reports effects on adult BMI only in selected groups. It is a better fit than Black et al. for §1's "wider literature" sentence. I verified the abstract via OpenAlex; check the volume on Crossref before use.
  - Zhen (2021), "Food Deserts: Myth or Reality?", *Annu Rev Resour Econ* (10.1146/annurev-resource-101620-080307): a review of causal food-access evidence.

---

## 5. In-text vs reference list (APA 7)

- Every in-text citation has a reference entry, and every reference except one is cited in the text.
- **The USDA ERS Food Environment Atlas reference is never cited in the text.** Add "(U.S. Department of Agriculture, Economic Research Service [USDA ERS], 2012, 2014, 2025)" in §2.2, then use "USDA ERS, 2025" in §2.7.
- **Data sources without reference entries** (APA 7 expects data set references):
  - CDC PLACES county data, 2020 release
  - U.S. Census Bureau ACS 5-year tables (2006–2010, 2014–2018)
  - OpenStreetMap contributors (ODbL), planet file of 21 September 2026
  - plotly/datasets county GeoJSON (2010 cartographic boundary)
  - QLever endpoint (optional)

  Suggested entries are in §6.
- Formatting:
  - Bast & Buchhold: add the subtitle.
  - Greenlund: change E31 to Article 210459.
  - Spence, Young and Cooksey-Stowers: use "Article N" for article numbers.
  - Andrews et al.: add issue (1).
  - Atlas reference: APA prefers "U.S." with periods; the year group "(2012, 2014, 2025)" in a single entry is unusual, so consider separate entries per release, or one entry dated 2025 with the archived releases named in brackets.

---

## 6. Corrected reference list (APA 7)

Anderson, M. L., & Matsa, D. A. (2011). Are restaurants really supersizing America? *American Economic Journal: Applied Economics*, *3*(1), 152–188. https://doi.org/10.1257/app.3.1.152

Anderson, T. W., & Rubin, H. (1949). Estimation of the parameters of a single equation in a complete system of stochastic equations. *The Annals of Mathematical Statistics*, *20*(1), 46–63. https://doi.org/10.1214/aoms/1177730090

Andrews, I., Stock, J. H., & Sun, L. (2019). Weak instruments in instrumental variables regression: Theory and practice. *Annual Review of Economics*, *11*(1), 727–753. https://doi.org/10.1146/annurev-economics-080218-025643

Bast, H., & Buchhold, B. (2017). QLever: A query engine for efficient SPARQL+Text search. In *Proceedings of the 2017 ACM on Conference on Information and Knowledge Management* (pp. 647–656). Association for Computing Machinery. https://doi.org/10.1145/3132847.3132921

[Black, C., Moon, G., & Baird, J. (2014) — keep only if re-scoped to diet per L4.] Black, C., Moon, G., & Baird, J. (2014). Dietary inequalities: What is the evidence for the effect of the neighbourhood food environment? *Health & Place*, *27*, 229–242. https://doi.org/10.1016/j.healthplace.2013.09.015

Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, *50*(2), 317–372. https://doi.org/10.3368/jhr.50.2.317

Centers for Disease Control and Prevention. (2020). *PLACES: County data (GIS friendly format), 2020 release* [Data set]. Retrieved October 22, 2026, from https://data.cdc.gov/resource/mssc-ksj7.csv

Cobb, L. K., Appel, L. J., Franco, M., Jones-Smith, J. C., Nur, A., & Anderson, C. A. M. (2015). The relationship of the local food environment with obesity: A systematic review of methods, study quality, and results. *Obesity*, *23*(7), 1331–1344. https://doi.org/10.1002/oby.21118 (Erratum published 2015, *Obesity*, *23*(12), 2517–2519, https://doi.org/10.1002/oby.21363)

Cooksey-Stowers, K., Schwartz, M. B., & Brownell, K. D. (2017). Food swamps predict obesity rates better than food deserts in the United States. *International Journal of Environmental Research and Public Health*, *14*(11), Article 1366. https://doi.org/10.3390/ijerph14111366

Courtemanche, C., & Carden, A. (2011). Supersizing supercenters? The impact of Walmart Supercenters on body mass index and obesity. *Journal of Urban Economics*, *69*(2), 165–181. https://doi.org/10.1016/j.jue.2010.09.005

Currie, J., DellaVigna, S., Moretti, E., & Pathania, V. (2010). The effect of fast food restaurants on obesity and weight gain. *American Economic Journal: Economic Policy*, *2*(3), 32–63. https://doi.org/10.1257/pol.2.3.32

Dunn, R. A. (2010). The effect of fast-food availability on obesity: An analysis by gender, race, and residential location. *American Journal of Agricultural Economics*, *92*(4), 1149–1164. https://doi.org/10.1093/ajae/aaq041

Greenlund, K. J., Lu, H., Wang, Y., Matthews, K. A., LeClercq, J. M., Lee, B., & Carlson, S. A. (2022). PLACES: Local data for better health. *Preventing Chronic Disease*, *19*, Article 210459. https://doi.org/10.5888/pcd19.210459

Lee, D. S., McCrary, J., Moreira, M. J., & Porter, J. (2022). Valid *t*-ratio inference for IV. *American Economic Review*, *112*(10), 3260–3290. https://doi.org/10.1257/aer.20211063

Montiel Olea, J. L., & Pflueger, C. (2013). A robust test for weak instruments. *Journal of Business & Economic Statistics*, *31*(3), 358–369. https://doi.org/10.1080/00401706.2013.806694

OpenStreetMap contributors. (2026). *OpenStreetMap planet file, 21 September 2026* [Data set; Open Database License 1.0]. Queried via QLever, https://qlever.dev/api/osm-planet

Plotly. (n.d.). *geojson-counties-fips.json* [Data set; 2010 Census cartographic county boundaries], plotly/datasets, commit 0c447c47b757ad74edecab31f0d72f849d2e67c2. GitHub. https://github.com/plotly/datasets

Spence, J. C., Cutumisu, N., Edwards, J., Raine, K. D., & Smoyer-Tomic, K. (2009). Relation between local food environments and obesity among adults. *BMC Public Health*, *9*, Article 192. https://doi.org/10.1186/1471-2458-9-192

U.S. Census Bureau. (2011, 2019). *American Community Survey 5-year estimates, 2006–2010 and 2014–2018, Tables B01003, B08301, B15002 and B19083* [Data set]. Retrieved October 22, 2026, from https://data.census.gov/

U.S. Department of Agriculture, Economic Research Service. (2025). *Food Environment Atlas* [Data set; current release of July 2025 and archived releases of November 2012 and February 2014]. https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads

Young, A. (2022). Consistency without inference: Instrumental variables in practical application. *European Economic Review*, *147*, Article 104112. https://doi.org/10.1016/j.euroecorev.2022.104112

Zhang, X., Holt, J. B., Lu, H., Wheaton, A. G., Ford, E. S., Greenlund, K. J., & Croft, J. B. (2014). Multilevel regression and poststratification for small-area estimation of population health outcomes: A case study of chronic obstructive pulmonary disease prevalence using the Behavioral Risk Factor Surveillance System. *American Journal of Epidemiology*, *179*(8), 1025–1033. https://doi.org/10.1093/aje/kwu018

Optional, if used: Atanasova, P., Kusuma, D., Pineda, E., Frost, G., Sassi, F., & Miraldo, M. (2022). The impact of the consumer and neighbourhood food environment on dietary intake and obesity-related outcomes: A systematic review of causal impact studies. *Social Science & Medicine*, *299*, Article 114879. https://doi.org/10.1016/j.socscimed.2022.114879. The volume number is from memory and must be checked on Crossref first.

Notes on the new entries:
- The ACS release years (2011 for 2006–2010; 2019 for 2014–2018) are publication years from general knowledge, not checked here. Use "n.d." or verify.
- The CDC dataset year of 2020 is the release name. Socrata shows rows last updated on 2021-10-07, so verify the publication date or cite "2020 release" with "n.d.".

---

## 7. Prioritised fix list

**High**
1. **L4, Black et al. (2014):** it reviews *diet*, not obesity, and does not report "mostly null" findings. Drop it from the §1 sentence or re-scope it. Optionally replace it with Atanasova et al. (2022).
2. **O24, §5 "three percentage points":** the original says "about three percent". Quote it accurately and flag the percentage-point reading as the author's interpretation (§3.9 and §5).
3. **Atlas reference not cited in text:** add the in-text citation in §2.2 and §2.7.

**Medium**
4. **L7, Courtemanche & Carden:** the paper finds a positive effect, which is not a "debate". Reword.
5. **F1:** acknowledge that the original's §4.5 flagged the instrument as imperfect and possibly weak, and listed exclusion threats.
6. **F2 and O31, §4.3:** replace "overstated the precision" with "misread the units (a level-on-ratio coefficient as an elasticity)". Note that the original's §4.3 also gives a 0.003% lower figure.
7. **D3, −9999 coding:** quote the ERS definition ("not available, not applicable, or suppressed") and label the zero-coding as an assumption.
8. **O29 and F4:** Table 4 "Standard errors" row. The original says "robust standard errors clustered by state", so this is not a discrepancy. Reword or drop.
9. **Data references:** add APA data-set entries for CDC PLACES, ACS, OpenStreetMap/ODbL and the plotly GeoJSON.
10. **L17:** soften "often read as settling the question" or support it.

**Low**
11. Greenlund: "Article 210459", not "E31".
12. Bast & Buchhold: add the subtitle.
13. Spence, Young and Cooksey-Stowers: use "Article N". Andrews et al.: add issue (1).
14. Cobb et al.: note the 2015 erratum (10.1002/oby.21363), and check that it does not affect the "predominantly null" summary (not read).
15. O21: add §2.4.1 and Table 4 of the original to the label-ambiguity list. O19: mention Table 3's second fast-food row, "Number of fast food retailers 15.0 (228.58)", an exact 2007 match.
16. F3: say that the original's body text agrees with Table 9 on inequality, and only the abstract conflicts.
17. Fairness option: Cobb et al. found multi-outlet indices the most consistent correlate of adult obesity, which is worth one clause.
18. README: the QLever URL now redirects to `https://qlever.dev/api/osm-planet`; optionally cite osm2rdf.
19. Internal consistency (not a citation issue): the SD of the Table 1 traditional RFEI is 3.54 in §3.2 and Table 4 but 3.53 in §3.9. Reconcile.
