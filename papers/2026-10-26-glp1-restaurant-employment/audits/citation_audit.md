# Citation audit: paper 11

**Manuscript:** "Drive-thru dose–response: GLP-1 uptake and US restaurant employment" (`pkg/manuscript/manuscript.md`, v1)
**Auditor:** independent citation audit (Claude, claude-opus-5-5), 22 October 2026. The manuscript was not edited.
**Scope:** attributed claims and quotations, DOIs, URLs, data-source descriptions, novelty, in-text vs reference list, APA 7.

## 0. What was read, and how

| Source | What I read | Route |
|---|---|---|
| Hristakeva, Liaukonytė & Feler (2026), JMR | Full abstract, verbatim, from the Crossref record. SAGE page (`/doi/full/…`) shows "Get access", so the **full text is paywalled and was not read**. SSRN preprint 5073929 was behind a Cloudflare challenge, which I did not bypass. | Chrome fetch of api.crossref.org; Chrome on journals.sagepub.com |
| Bina & Tonsor (2026), JAAE | **Full text** (CC BY 4.0 open access on Cambridge Core): abstract, data section, results sentences on outlet frequency. | Chrome on cambridge.org |
| Wang & Balagtas (2026), SSRN | Full abstract, verbatim, from Crossref. Full text not read. | Crossref |
| Resendiz (2026), CMC thesis | Repository record and abstract. The full text is embargoed until 27 April 2028 and restricted to Claremont users. Chrome was not permitted on that domain, so this was read through WebFetch, which returns a summary. | WebFetch |
| KFF poll (Montero et al., 2025) | KFF page | WebFetch summary, with short quotes |
| Cubanski & Neuman (2024), KFF | KFF page | WebFetch summary, with short quotes |
| Chetty et al. (2024), QJE | Crossref metadata only. The paper is cited for the dataset, which was checked against the repository's data dictionary. | Crossref; GitHub raw |
| Cameron & Miller (2015); Roth (2022); Bloom (1995) | Crossref metadata. I did not reread the content; the attributed uses are standard, see §1. | Crossref |
| CMS Part D methodology (RY26, 21 Apr 2026, PDF) | Methodology PDF | WebFetch summary |
| CMS data.json catalog; Medicare Monthly Enrollment API | Live records (county 2019 and 2024 rows, field names) | Chrome fetch on data.cms.gov |
| BLS QCEW annual industry slices | Live CSVs for 722513 (2019, 2022, 2025), 721 (2025), 446110 (2021, 2022), 456110 (2022); QCEW home page | Chrome fetch on data.bls.gov and bls.gov |
| Census ZCTA–county file | Directory listing: file present, dated 2021-12-09, 6.5 MB | WebFetch |
| OI Economic Tracker | Commit 8048afb via the GitHub API; `docs/oi_tracker_data_dictionary.md` | Chrome |

---

## 1. Claims table

Status key: **OK** = supported. **MINOR** = supported but imprecise. **FIX** = misstates or overstates the source. **UNCITED** = factual claim with no source.

| # | Location | Claim in manuscript | Source says | Status |
|---|---|---|---|---|
| 1 | Abstract, §1, §2.5 | Adopting households spend 8.0% less at fast-food chains, coffee shops and limited-service restaurants (Hristakeva et al.) | Abstract (Crossref, verbatim): "Results show an 8.0% decline in spending at fast-food chains, coffee shops, and limited-service restaurants." | OK. The quotation in §1 matches exactly. The abstract does not give a horizon for the 8.0% figure, so do not pair it with "within six months" (the manuscript currently does not). |
| 2 | §1 | Households with at least one user cut grocery spending 5.3% within six months | Abstract: "reduce grocery spending by 5.3% within six months of adoption" | OK |
| 3 | §1 | Survey responses on adoption linked to transaction data from a US household panel | Abstract: "survey responses on medication adoption linked to transaction data from a representative U.S. household panel" | OK |
| 4 | §1 | Wang & Balagtas: matched staggered DiD; grocery spending fell 6.2% in the adoption half-year; abstract has no restaurant outcomes | Abstract: "matched panel of adopter and never-adopter households … staggered difference-in-differences event studies … spending falls 6.2% and calories 3.6% in the adoption half-year". No mention of restaurants or food away from home. | OK. One word is unsupported: "**another** transaction panel". The abstract does not name the vendor, so it may be the same kind of panel. Write "a transaction panel". |
| 5 | §1 | Bina & Tonsor: meal reports from a consumer survey; users differ in where they eat and in meal skipping; largest among shorter-term users; associations, not effect of starting | Abstract: "Using meal reporting from a consumer survey…we examine associations…GLP-1 users differ substantially from non-users in their outlet choices, meal skipping rates…These differences are most prominent among shorter-term users." | OK |
| 6 | §4.2 | Bina & Tonsor "report that users eat out in different places from non-users"; a shift to full-service would show as a negative contrast | The full text reports that users' meal-location frequency is "higher for FAH Online Retail, FAFH Fine, FAFH Casual, and, to a lesser extent, FAFH Quick" relative to non-users. Users are also less likely to source meals from physical retail and more likely to skip meals. | MINOR. Accurate but vague. The direction the full text reports (more fine and casual dining, less so quick-service) bears directly on the substitution argument and should be stated. These are descriptive, cross-sectional frequencies. |
| 7 | §1 | Resendiz: state panel 2017–2024, two-way fixed effects, Medicaid GLP-1 coverage and spending; no significant effect of coverage or total spending on establishments, revenue, employment or wages | Repository abstract: same period and method. Coverage and aggregate spending show no significant effect on any outcome. | OK |
| 8 | §1 | "Only Zepbound spending was significantly associated with fewer fast-food establishments, and less robustly with lower employment" | Zepbound spending is negative for establishments at 5% ("strongest finding", holds across measurement approaches) and for employment at 10% ("sensitive to the measurement approach"). With spending **normalised by Medicaid enrolment**, effects strengthen: employment becomes significant under all measures and **revenue becomes significant**. Wegovy and Saxenda show nothing. The author frames these as "emerging but detectable effects". | MINOR. The establishment and employment results are right. The manuscript omits the normalised results, where employment is robust and revenue is significant. |
| 9 | §4.2 | "Consistent with Resendiz (2026), who found **no overall association** … **only one drug-specific association was significant**" | See row 8: one drug, but associations with establishments (5%), employment (10%, and significant across measures when normalised) and revenue (when normalised). The thesis presents these as detectable effects, not a null. | **FIX.** "Only one drug-specific association" is wrong; it is one drug with several associated outcomes. "Consistent with" overstates the agreement. Suggested wording: "Resendiz (2026) found no association for Medicaid coverage or total GLP-1 spending, but did find negative associations between Zepbound spending and fast-food establishments and employment, which the author reads as early evidence of an effect." |
| 10 | §1 | Thesis full text embargoed until 2028; only the abstract is public | "Available for download on Thursday, April 27, 2028", restricted to Claremont users | OK (could add "27 April 2028") |
| 11 | §1 | "In a **November 2025** national poll, 12% currently using and 18% ever used" (Montero et al., 2025) | KFF: "12% who say they are currently using them"; "nearly one in five (18%) adults now say they have ever used". Fielded 27 Oct–2 Nov 2025, n = 1,350 adults; published 14 Nov 2025. | MINOR. The figures are right. Most fieldwork was in October, so write "In a national poll fielded from late October to early November 2025". |
| 12 | §4.3 | By law Part D could not cover drugs used for weight loss; plans could cover Wegovy for its cardiovascular indication only from March 2024 (Cubanski & Neuman, 2024) | KFF, 22 Mar 2024 (updated 27 Mar): "Medicare is prohibited under current law from covering drugs used for weight loss…"; "Part D plans…are now able to cover Wegovy for its heart health benefits", after the FDA "has just approved a new use". The post gives no exact date. | OK. "From March 2024" is a fair reading of the post's date. FDA approval was 8 March 2024; cite FDA or CMS if an exact date is wanted. |
| 13 | §4.3 | "Part D covers people aged 65 and over and some disabled people" | Medicare eligibility also covers people with ESRD. The Monthly Enrollment file has aged, disabled and ESRD fields. | MINOR, uncited. Add "and people with end-stage renal disease" or leave as is. |
| 14 | §4.3 | "Commercial, Medicaid, cash-pay and compounded use, which drove much of the recent growth in use for weight loss" | No source given | **UNCITED.** Add a source, or recast it as the author's reasoning. |
| 15 | §2.3 | Inference from t with G−1 degrees of freedom (Cameron & Miller, 2015) | C&M (2015) recommend T(G−1) critical values with few clusters | OK |
| 16 | §2.4 | A pre-trend test that passes is weak evidence (Roth, 2022) | Roth (2022): pre-tests often have low power, and conditioning on passing them distorts inference | OK |
| 17 | §2.5 | MDE = (t₀.₉₇₅ + t₀.₈₀) × SE (Bloom, 1995) | Bloom (1995) defines the MDE as a multiplier (≈2.8 for a two-sided 5% test at 80% power) times the SE | OK |
| 18 | §2.6 | OI Tracker publishes monthly card spending on accommodation and food services by state, "indexed to January 2020" (Chetty et al., 2024) | Data dictionary: `spend_acf` = "Spending in accomodation and food service"; all spending variables are "measured relative to January 6 to February 2, 2020, seasonally adjusted, and calculated as a 7 day moving average". The state monthly file exists. | MINOR. Write "relative to 6 January–2 February 2020, seasonally adjusted". Seasonal adjustment matters for the 2022 and 2025 annual means. Data now come from Affinity Solutions. |
| 19 | §2.6 | "The only public restaurant spending series below the national level that I found" is the OI Tracker | The brief itself lists BEA state PCE "Food services and accommodations" (annual, to 2025), which is also sub-national and also mixes in hotels | **FIX (overstatement).** Suggested wording: "The only public monthly series below the national level…; BEA's annual state PCE also combines food services with accommodation." |
| 20 | Transparency | OI Tracker, GitHub commit 8048afb | Commit 8048afb24d87af54426014d341959c5c262f87da exists, dated 2026-10-21T23:52Z ("Update Employment data 2026-10-21") | OK. Add a dataset reference (see §4). |
| 21 | §2.1 | CMS Provider-and-Drug file: claims and 30-day fills by prescriber and drug, by brand and generic name; "Rows with fewer than 11 claims are suppressed" | Methodology (RY26): the file excludes providers with fewer than 11 total claims and drugs with fewer than 11 claims for a provider. These rows are **omitted, not blanked**. Within kept rows, values of 1–10 are blanked. Drug and generic names come from linking NDCs to a commercial drug database. Fields used in the code: `Brnd_Name`, `Gnrc_Name`, `Tot_Clms`, `Tot_30day_Fills`. | MINOR. Write "Rows with fewer than 11 claims are omitted". §4.3 already says "omits". |
| 22 | §2.1 | Prescriber city and state but no ZIP; ZIP taken from Part D Prescribers by Provider, joined on NPI | The code pulls `Prscrbr_State_FIPS` from the Provider-and-Drug file and `Prscrbr_Zip5` from the Provider file. The brief verified the field lists. | OK |
| 23 | §2.1 | ZIP codes mapped to counties with the 2020 ZCTA–county file, by largest land area | File exists (dated 2021-12-09). The code uses `AREALAND_PART` and keeps the county with the largest overlap. | OK. Optionally state that ZIP codes are treated as ZCTAs, so PO-box and unique ZIPs drop out; this is the 0.8–1.0% unmatched. |
| 24 | §2.1 | Denominator: county Part D enrollees from Medicare Monthly Enrollment | The live API has county rows with `MONTH = "Year"` for 2019 and 2024 and the field `PRSCRPTN_DRUG_TOT_BENES` (total, PDP and MAPD). The code uses that field. | OK |
| 25 | §2.1 | Geography-and-Drug file "not subject to the row suppression" | Methodology: summary tables are built from all Part D PDE data. Small cells may still be blanked. | OK. Could say "built from all claims rather than from the provider-level rows". |
| 26 | §2.2 | QCEW annual averages 2015–2025, private, by county; 722511 full-service, 722513 limited-service | Live: `/cew/data/api/2025/a/industry/722513.csv` returns HTTP 200 (3,241 rows). bls.gov/cew lists "Employment and Wages, Annual Averages, 2025". The code filters `own_code == 5` (private). | OK |
| 27 | §2.2 | Pharmacies: 446110 to 2021, 456110 from 2022 | Live: 446110 present for 2021, **HTTP 404 for 2022**; 456110 present for 2022 | OK |
| 28 | §2.2 | Accommodation 721; Supermarkets 445110 | Live: 721 present for 2025; 445110 is used in the code | OK |
| 29 | §2.2 | Alaska and Connecticut dropped because county definitions changed | Live QCEW: Alaska 02261 (Valdez-Cordova) in 2019 becomes 02063 and 02066 by 2022. Connecticut has counties 09001–09015 through 2022, but **planning regions 09110–09190 in 2025**. | OK. Optionally name the changes. |
| 30 | §2.7 | All data retrieved 22 October 2026 | Consistent with the OI commit dated 21 Oct 2026 | OK |
| 31 | §3.1 | National uptake 1.3 to 4.6; fills ×4.2; semaglutide and tirzepatide share 10.3% to 76.1% | `results/descriptives.json`: 1.285 to 4.639; 29.86 m / 7.06 m = 4.23; 0.728/7.06 = 10.3%; 22.74/29.86 = 76.1% | OK (internal check) |
| 32 | §4.1 | Rise of 3.4 points; MDE 3.4–13.7× the benchmark; rule-out 4.7–18.6× | 4.639 − 1.285 = 3.35; 1.10/0.32 = 3.4; 1.10/0.08 = 13.75; 1.49/0.32 = 4.66; 1.49/0.08 = 18.6 | OK (internal check) |
| 33 | §3.4 vs Table 3 | No-controls CI "(−1.30 to −0.00)" in text, "(−1.30 to 0.00)" in table | — | MINOR. Typographic inconsistency; use one form. |

---

## 2. Crossref and URL table

All DOI checks used the Crossref REST API (`api.crossref.org/works/<DOI>`), fetched in my own Chrome tab and through WebFetch on 22 Oct 2026.

| DOI | Crossref result | Matches manuscript? |
|---|---|---|
| 10.1177/00222437251412834 | journal-article; Hristakeva, Sylvia; Liaukonytė, Jūra; Feler, Leo; *Journal of Marketing Research* 63(3), 427–444; online 2026-04-01, print 2026-06 | Yes |
| 10.1017/aae.2026.10049 | journal-article; Bina, Justin D.; Tonsor, Glynn T.; *Journal of Agricultural and Applied Economics*; pp. 1–21; online 2026-07-06; no volume or issue (FirstView); CC BY 4.0 | Yes ("Advance online publication" is correct) |
| 10.2139/ssrn.7434663 | posted-content (preprint); Wang, Xuejian; Balagtas, Joseph; SSRN (Elsevier); 2026 | Yes |
| 10.1177/0193841X9501900504 | Bloom, Howard S.; *Evaluation Review* 19(5), 547–556; Oct 1995 | Yes |
| 10.3368/jhr.50.2.317 | Cameron, A. Colin; Miller, Douglas L.; *Journal of Human Resources* 50(2), 317–372; 2015 | Yes |
| 10.1093/qje/qjad048 | Chetty, R.; Friedman, J. N.; Stepner, M.; Opportunity Insights Team (group author), then 54 team members; *QJE* 139(2), 829–889; online 2023-10-04, print 2024 | Yes. Using issue year 2024 is APA-correct. |
| 10.1257/aeri.20210236 | Roth, Jonathan; *AER: Insights* 4(3), 305–322; 2022-09 | Yes |
| (not cited) 10.2139/ssrn.5073929 | SSRN preprint of Hristakeva et al. | Exists; no need to cite |

| URL | Check | Result |
|---|---|---|
| data.cms.gov …/medicare-part-d-prescribers-by-provider-and-drug | Loaded; latest data 2024; matches data.json `landingPage` | OK |
| data.cms.gov …/medicare-part-d-prescribers-by-provider | Loaded; latest data 2024 | OK |
| data.cms.gov …/medicare-part-d-prescribers-by-geography-and-drug | Matches data.json `landingPage` exactly | OK |
| data.cms.gov …/medicare-monthly-enrollment | Matches data.json `landingPage`; API returns county rows | OK |
| kff.org …/medicare-spending-on-ozempic-and-other-glp-1s-is-skyrocketing | Resolves; title, authors and date match | OK |
| kff.org …/kff-health-tracking-poll-prescription-drug-costs-…-glp-1-use/ | Resolves; title, authors and date match | OK |
| scholarship.claremont.edu/cmc_theses/4084 | Resolves; access-restricted record | OK |
| bls.gov/cew/ | Resolves; QCEW home page | OK. A more specific URL is in §4. |
| www2.census.gov …/tab20_zcta520_county20_natl.txt | Present in the directory listing (2021-12-09, 6.5 MB) | OK |
| github.com/OpportunityInsights/EconomicTracker @ 8048afb | Commit exists | OK |

---

## 3. In-text vs reference list, and APA 7

- **Every in-text citation has a reference entry, and every reference is cited.** The 2026a–d suffixes are all used, in §2.1.
- **First citation of Hristakeva et al.** §1 has "Hristakeva, Liaukonytė and Feler (2026)". APA 7 uses "et al." from the first citation for three or more authors, so write "Hristakeva et al. (2026)". This is a style point, not an error.
- **Agency names.** APA writes "U.S. Bureau of Labor Statistics" and "U.S. Census Bureau", with periods.
- **Data sets that change over time** should carry a retrieval date: "Retrieved October 22, 2026, from …".
- **Resendiz.** APA 7 format for an unpublished thesis in a repository is "[Bachelor's thesis, Claremont McKenna College]. Scholarship@Claremont. URL".
- **Missing dataset reference.** The OI Economic Tracker data are used, but only the Chetty et al. paper is in the reference list. Add a data set entry and cite it in §2.6 alongside Chetty et al.
- **QCEW reference.** Give the downloadable data or open-data access page, not just the landing page.
- **Bina & Tonsor.** Advance online publication with no volume is correct. APA does not require the page range "1–21" for online-first articles.
- **Software (optional).** APA does not require references for pandas, NumPy, SciPy or Pyodide; the text names versions, which is enough.

---

## 4. Corrected reference list (ready to paste)

Bina, J. D., & Tonsor, G. T. (2026). Meal location and protein choices of GLP-1 users. *Journal of Agricultural and Applied Economics*. Advance online publication. https://doi.org/10.1017/aae.2026.10049

Bloom, H. S. (1995). Minimum detectable effects: A simple way to report the statistical power of experimental designs. *Evaluation Review*, *19*(5), 547–556. https://doi.org/10.1177/0193841X9501900504

Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, *50*(2), 317–372. https://doi.org/10.3368/jhr.50.2.317

Centers for Medicare & Medicaid Services. (2026a). *Medicare Part D prescribers – by provider and drug, data years 2019–2024* [Data set]. Retrieved October 22, 2026, from https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider-and-drug

Centers for Medicare & Medicaid Services. (2026b). *Medicare Part D prescribers – by provider, data years 2019–2024* [Data set]. Retrieved October 22, 2026, from https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider

Centers for Medicare & Medicaid Services. (2026c). *Medicare monthly enrollment* [Data set]. Retrieved October 22, 2026, from https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment

Centers for Medicare & Medicaid Services. (2026d). *Medicare Part D prescribers – by geography and drug, data years 2019–2024* [Data set]. Retrieved October 22, 2026, from https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-geography-and-drug

Chetty, R., Friedman, J. N., Stepner, M., & Opportunity Insights Team. (2024). The economic impacts of COVID-19: Evidence from a new public database built using private sector data. *Quarterly Journal of Economics*, *139*(2), 829–889. https://doi.org/10.1093/qje/qjad048

Cubanski, J., & Neuman, T. (2024, March 22). *Medicare spending on Ozempic and other GLP-1s is skyrocketing*. KFF. https://www.kff.org/policy-watch/medicare-spending-on-ozempic-and-other-glp-1s-is-skyrocketing/

Hristakeva, S., Liaukonytė, J., & Feler, L. (2026). The no-hunger games: How GLP-1 medication adoption is changing consumer food demand. *Journal of Marketing Research*, *63*(3), 427–444. https://doi.org/10.1177/00222437251412834

Montero, A., Kearney, A., Mulugeta, M., Kirzinger, A., & Hamel, L. (2025, November 14). *KFF health tracking poll: Prescription drug costs, views on Trump administration actions, and GLP-1 use*. KFF. https://www.kff.org/public-opinion/kff-health-tracking-poll-prescription-drug-costs-views-on-trump-administration-actions-and-glp-1-use/

Opportunity Insights. (2026). *Economic Tracker: Affinity – State – Monthly* (Version 8048afb) [Data set]. GitHub. Retrieved October 22, 2026, from https://github.com/OpportunityInsights/EconomicTracker

Resendiz, K. J. (2026). *Do GLP-1 weight loss drugs affect fast food industry performance? Evidence from state Medicaid programs* [Bachelor's thesis, Claremont McKenna College]. Scholarship@Claremont. https://scholarship.claremont.edu/cmc_theses/4084

Roth, J. (2022). Pretest with caution: Event-study estimates after testing for parallel trends. *American Economic Review: Insights*, *4*(3), 305–322. https://doi.org/10.1257/aeri.20210236

U.S. Bureau of Labor Statistics. (2026). *Quarterly Census of Employment and Wages: County annual averages by industry, 2015–2025* [Data set]. Retrieved October 22, 2026, from https://www.bls.gov/cew/downloadable-data-files.htm

U.S. Census Bureau. (2021). *2020 ZCTA to county relationship file* [Data set]. https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt

Wang, X., & Balagtas, J. (2026). *The effects of GLP-1 medications on household grocery purchases* [Preprint]. SSRN. https://doi.org/10.2139/ssrn.7434663

Notes on the list:
- I did not load `bls.gov/cew/downloadable-data-files.htm` (the brief marks it unverified). If you would rather not use it, keep `https://www.bls.gov/cew/`, which I verified.
- If the OI entry is added, cite it in §2.6 as "(Chetty et al., 2024; Opportunity Insights, 2026)".
- If you want a source for the March 2024 Wegovy date, add the FDA's 8 March 2024 approval announcement. I did not verify its URL, so none is given here.

---

## 5. Novelty check

**Searches run:** web searches (extended mode) on GLP-1 with county or area-level restaurant employment and sales, Medicare Part D, QCEW, foot traffic and card data, NBER working papers, and DiD on county or MSA. I also checked the leads in the brief. Crossref and SSRN full-text search were not run beyond the brief's checks. SSRN was behind a Cloudflare challenge.

**Findings:**
- **Resendiz (2026)** is still the only study I found linking area-level (state) GLP-1 exposure to fast-food establishments, revenue, employment or wages. Its results are not a clean null (see claims 8 and 9).
- **No study found** links county GLP-1 prescribing to restaurant employment, establishments or wages, or contrasts limited-service with full-service restaurants at area level.
- Industry and trade items (CRE Daily, July 2026, citing *Commercial Observer*, Newmark and McKinsey; NRA "GLP-1 Usage and Restaurants", May 2026; William Blair; Circana via NRN) are aggregate, survey-based or anecdotal. None ties GLP-1 use by area to restaurant outcomes.
- A medRxiv preprint (2025) and a PMC article on GLP-1 use among Medicare fee-for-service beneficiaries describe geographic variation in prescribing. Neither uses restaurant outcomes. They could be cited as precedent for area-level Part D or Medicaid prescribing measures.

**Verdict.** The claim in §1 ("I am not aware of an earlier study that links county GLP-1 prescribing to restaurant employment, or that contrasts limited-service with full-service restaurants at the area level") holds as written. It is correctly phrased as "not aware of". This is a "not found" result, not proof that no such study exists.

---

## 6. Prioritised fix list

**Priority 1: misstatements of sources**
1. **§4.2, Resendiz.** Replace "who found no overall association … only one drug-specific association was significant" and "The pattern is consistent with" with a description that matches the thesis abstract. Zepbound spending is negatively associated with establishments (5%) and employment (10%, robust when normalised by enrolment), and revenue becomes significant when normalised. The author reads this as emerging evidence of an effect. Suggested text is in claims row 9.
2. **§1, Resendiz.** Add the normalised-spending results: employment significant across all measures, revenue significant. Otherwise "less robustly with lower employment" understates the thesis.
3. **§2.6.** Drop "The only public restaurant spending series below the national level". BEA state PCE (annual, food services combined with accommodation) also exists. Use "the only monthly…" and mention BEA.

**Priority 2: precision**
4. **§4.3.** Add a source for "Commercial, Medicaid, cash-pay and compounded use … drove much of the recent growth", or mark it as the author's assessment.
5. **§4.2.** Say what Bina & Tonsor actually report: users' meal-location frequency is higher for fine and casual dining and, to a lesser extent, quick-service, relative to non-users. These are descriptive frequencies. This bears on the substitution reading.
6. **§2.6.** The OI index is "relative to 6 January–2 February 2020, seasonally adjusted, 7-day moving average", not "indexed to January 2020".
7. **§1, KFF poll.** "A national poll fielded from late October to early November 2025", not "a November 2025 national poll".
8. **§1, Wang & Balagtas.** "a transaction panel", not "another transaction panel"; the vendor is not identified.
9. **§2.1.** "Rows with fewer than 11 claims are omitted", not "suppressed". This matches §4.3 and the CMS methodology.

**Priority 3: references and style**
10. Add the Opportunity Insights data set reference and cite it in §2.6.
11. Use "Hristakeva et al. (2026)" at first mention (APA 7).
12. Write "U.S." in the BLS and Census author names. Add retrieval dates to the CMS and BLS data set entries. Change Resendiz to "[Bachelor's thesis, …]. Scholarship@Claremont."
13. §3.4: "−0.00" in the text vs "0.00" in Table 3. Pick one form.
14. Optional: in §4.3, add ESRD to the Medicare eligibility description. In §2.2, name the boundary changes: Alaska 02261 split into 02063 and 02066; Connecticut moved to planning regions 09110–09190 in later QCEW years. In §2.1, note that ZIP codes are treated as ZCTAs.

**Unresolved: could not be verified with the access available**
- Hristakeva et al. full text (paywalled; SSRN behind Cloudflare). It is unknown whether the paper reports full-service restaurants, and what horizon the 8.0% applies to. The manuscript does not rely on either, which is safe.
- Resendiz full text (embargoed to 2028). Coefficients and outcome data sources are unknown.
- BLS downloadable-data-files URL (not loaded).
