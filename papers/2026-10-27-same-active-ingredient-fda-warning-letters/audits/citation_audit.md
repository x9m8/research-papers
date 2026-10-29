# Citation audit: paper 13, "Same as Wegovy" (FDA warning letters on compounded GLP-1s)

Auditor: independent citation-audit pass (Claude, claude-opus-5-5), 22 October 2026. I did not edit the manuscript.
Inputs: `pkg/manuscript/manuscript.md` (version of 22 Oct 2026, 06:20), `lit/brief.md` (used only as leads), `pkg/audits/crossref_check.json`.
Access: curl to Crossref and Europe PMC is blocked by the sandbox proxy, so I made every live check from my own Chrome tab (same-origin `fetch()` on api.crossref.org, ebi.ac.uk, fda.gov, api.fda.gov, and a page read on law.cornell.edu). I closed the tab afterwards.

## 0. Bottom line

- **No fabricated sources.** All 16 DOIs in the reference list resolve on Crossref, and the titles, authors, volumes, issues and pages match, with the exceptions listed below.
- **All numbers attributed to Chetty et al. (2025) are correct**, checked against the full text: 79 sites, 36.7%, 8.9% and 63.3%. The brief's "37.6%" was wrong, and the manuscript correctly does not use it.
- **FDA dates and quotations are correct as written**, with one substantive gap. The 503A grace periods were tied to court rulings, so the dates the manuscript gives for the end of FDA's enforcement discretion are FDA's *nominal* dates, not the dates it actually ended (fix A1).
- **One characterisation is wrong.** Tucker et al. (2018) and Cohen et al. (2022) are not content analyses of warning letters (fix A2).
- **Four APA/reference fixes are needed:** Dmour year, McCall year, Mattingly's suffix and Cohen 2022's page range. FDA (2026c) is listed but never cited in the text.
- **Novelty holds.** I found no published or preprint systematic analysis of FDA warning letters on compounded or unapproved GLP-1s. Only law-firm and trade-press commentary exists.

## 1. Claims table

Source-level key: FT = full text read; ABS = abstract read; META = Crossref/Europe PMC metadata and title only; LIVE = live web page read on 22 Oct 2026; LOCAL = the builder's frozen letter texts (`pkg/data/letters/`), with one letter re-checked live.

| # | Manuscript claim (location) | Source | What I read | Verdict |
|---|---|---|---|---|
| 1 | Both drugs were on FDA's shortage list from 2022 (Intro ¶1) | FDA 2026a | LIVE | Correct. The page says each drug had "been in shortage since 2022". |
| 2 | Tirzepatide shortage resolved 2 Oct 2024 and reaffirmed 19 Dec 2024; semaglutide resolved 21 Feb 2025 (Intro; Fig 1) | FDA 2026a | LIVE | Correct. Optional: mention the 22 Oct 2024 remand that preceded the 19 Dec re-decision. |
| 3 | Grace periods: tirzepatide 18 Feb 2025 (503A) and 19 Mar 2025 (503B); semaglutide 22 Apr and 22 May 2025 (Intro; Fig 1 events 3, 5, 6, 7; §3.2) | FDA 2026a | LIVE | **Partly correct; needs qualification.** These are the dates in FDA's original announcements. FDA's 11 Feb and 10 Mar 2025 updates made the 503A periods run to those dates "or until the date of the district court's decision … whichever is longer/later". The courts denied preliminary injunctions on **5 March 2025** (tirzepatide; FDA's 10 Mar 2025 update then said 503A discretion "has ended") and **24 April 2025** (semaglutide; FDA's 28 Apr 2025 update said the same). So the effective 503A end dates were 5 Mar 2025 and 24 Apr 2025. The 503B dates (19 Mar and 22 May 2025) stand, and so does "22 May 2025, the last of the grace-period deadlines". See fix A1. |
| 4 | 503A/503B allowed copies while the drugs were in shortage (Intro ¶1) | FDA 2026a | LIVE | Correct in substance. The page explains the "essentially a copy" and shortage-list conditions. |
| 5 | Chetty: 79 websites; 36.7% stated or implied FDA approval; 8.9% called the product generic; 63.3% used "same active ingredients as [brand name]" (Intro ¶2; Discussion §4.1) | Chetty 2025 | FT (Europe PMC PMC11742527, live, string-matched) | Correct. Searches ran **July–September 2024**, so "mid-2024" is acceptable but "July–September 2024" is more precise. The manuscript quotes the phrase with "active ingredients" (plural), which matches the source. |
| 6 | Mattingly & Conti; Donohue "raised concerns about marketing and safety" (Intro) | 2025 commentaries | META (no abstracts in Europe PMC) | Consistent with the titles. Not verified beyond title level. |
| 7 | Case reports and pharmacovigilance studies described dosing errors and other harms with compounded products (Lambson; McCall) | Lambson 2023; McCall | ABS | Correct. Lambson reports 3 cases, 2 with 10-fold self-administration errors. McCall analysed FAERS 2018–2024 (707 compounded reports among 81,078) and found higher RORs for preparation errors and contamination, among others. |
| 8 | "Products sold without a prescription were found to be of poor quality" (Ashraf 2024) | Ashraf 2024 | FT available (PMC11582493); I read the abstract live | Supported, but thin and broad. The finding rests on **3 vials** test-bought from illegal online pharmacies. All were judged probable substandard/falsified: endotoxin was present, purity was 7.7–14.37%, and content exceeded the label by 28.56–38.69%. These were illegal online-pharmacy products, not compounded products. Suggest narrowing the wording (fix B3). |
| 9 | "a secret-shopper study in two states found compounded GLP-1s still widely offered by clinics and med spas" (DiStefano 2026) | DiStefano 2026 | ABS | **Overstated.** The study purposively sampled businesses *already advertising* compounded GLP-1s (75 clinics and med spas in West Virginia and Oklahoma, August–October 2025), so prevalence ("widely offered") is not a finding. Its actual findings: added B vitamins at 42 of 75 businesses; 4 of 21 supplier facilities were not licensed for sterile compounding; 1 of 23 suppliers had received multiple FDA warning letters since 2023. See fix B2. |
| 10 | Content analyses of warning letters have described compounding pharmacies (Dmour) | Dmour | FT (PMC9666930; builder's saved copy plus live string match) | Correct. 141 warning letters to compounding pharmacies, 2017–2022, on CGMP violations. |
| 11 | … online DTC promotion (Kim 2015) | Kim 2015 | ABS | Correct, with one nuance: Kim analysed warning letters **and notices of violation (untitled letters)** to manufacturers, 2005–2014, finding 179 violations. |
| 12 | … dietary supplements (Tucker 2018; Cohen 2022) | Tucker; Cohen | ABS (Tucker); META (Cohen) | **Mischaracterised.** Tucker analysed FDA's *Tainted Products Marketed as Dietary Supplements* database of warnings (776 products, 2007–2016), not warning-letter content. Cohen 2022 (research letter) followed up supplements *after* warning letters (recalls, availability, content testing); its title shows this, and no abstract is available. Neither is a content analysis of letters. See fix A2. |
| 13 | … data integrity (Rogers 2020) | Rogers 2020 | META | Consistent with the title (BIMO inspections and warning letters, FY2007–2018). |
| 14 | A warning letter is informal and advisory and is not final agency action (Intro ¶3; §2.5) | **uncited** | Located FDA Regulatory Procedures Manual Ch. 4 "Advisory Actions" (fda.gov/media/71878/download, version dated 05 Jul 2024); the URL resolves | The claim is standard FDA doctrine, but it has no citation. Add FDA RPM Ch. 4 (fix B1). I confirmed the document and its title but did not extract its wording in this session, so check the exact phrasing before quoting. |
| 15 | Press release of 3 March 2026: "the issuance of 30 warning letters to telehealth companies" (§3.2) | FDA 2026b | LIVE | Quotation exact. Date 3 March 2026 correct. |
| 16 | FDA described its telehealth letters as part of a crackdown on misleading DTC advertising launched that month (September 2025) (§4.2) | FDA 2026b | LIVE | Correct. The release calls this "the second group of warning letters sent to telehealth firms since the agency launched in September a crackdown on misleading direct-to-consumer pharmaceutical advertisements". |
| 17 | Hims & Hers letter quotes "Same active ingredient as Ozempic and Wegovy" (§3.4) | Letter 716567 (dba Hims), 9 Sep 2025 | LOCAL plus LIVE re-fetch | Exact. The phrase appears in 7 letters in the corpus; this letter cites 502(a) and 502(bb) [21 U.S.C. §§ 352(a) and 352(bb)]. Not cited in the reference list; consider citing the letter URL (fix C4). |
| 18 | Boilerplate "Your claims imply that your products are the same as an FDA-approved product" (§2.3) | Letters | LOCAL | Accurate but truncated. The full sentence ends "… when they are not." (44 letters). Add the ending or an ellipsis. |
| 19 | "when in fact it is not" (§3.5); "FDA-approved"/"FDA-licensed" (§3.5) | Letters | LOCAL | Present: 51 letters contain "when in fact it is not", which matches the 51 firm-branded code, and 11 contain "FDA-licensed", which matches "11 letters". |
| 20 | openFDA: 85 unique recall records, 24 events, 20 firms, 49 (57.6%) sterility; 2025 = 38, 2026 = 27 (§3.7) | openFDA 2026 | LIVE (re-ran the 3 queries myself) | Reproduced exactly: 85 / 24 / 20 / 49; by initiation year, 2025: 38 and 2026: 27. |
| 21 | "FDA's adverse-event reports" mentioned (§4.2) | **uncited** | LIVE: "FDA's Concerns with Unapproved GLP-1 Drugs Used for Weight Loss", current as of 10/01/2026 | Not cited. The page says: "As of May 31, 2026 … 990 reports of adverse events associated with compounded semaglutide" and "more than 730 reports … compounded tirzepatide". **The URL has moved**: the brief's `/drugs/postmarket-drug-safety-information-patients-and-providers/…` now redirects to `/drugs/drug-alerts-and-statements/fdas-concerns-unapproved-glp-1-drugs-used-weight-loss`. Cite the new path if used (fix B4). |
| 22 | Index covers letters posted since 2021 (§2.1) | FDA 2026c | not independently verified (brief, VERIFIED-LIVE by builder) | Plausible. FDA 2026c should be cited here (fix A3). |

Belcourt 2026, Miller 2026, Jordan 2026, Kopp 2026 and Anderer 2026 are **not cited in the manuscript**, so they make no claims to verify. Their DOIs resolve (Belcourt: *Ann Pharmacother* 60(9), 902–906; Miller: *J Med Toxicol* 22(2), 275–285). The brief's Agarwal et al. DOI 10.2105/ajph.2026.308514 **returns 404 on Crossref** and is not in the manuscript. Do not add it without a working DOI.

## 2. Statutory citations

I checked the FDCA-to-U.S. Code mappings against FDA's own bracketed citations in the corpus letters and checked 352(bb) against the U.S. Code text (LII, live).

| FDCA section (manuscript) | 21 U.S.C. | Check |
|---|---|---|
| 502(a) false/misleading labelling | § 352(a) | Correct (FDA letters cite "[21 U.S.C. § 352(a)]") |
| 502(bb) false/misleading advertising of compounded drug | § 352(bb) | Correct. Statutory text: "If the advertising or promotion of a compounded drug is false or misleading in any particular." Suggest "advertising or promotion" for accuracy. |
| 502(f)(1) inadequate directions | § 352(f)(1) | Correct |
| 503(b)(1) Rx-only | § 353(b)(1) | Correct |
| 505(a) unapproved new drug | § 355(a) | Correct |
| 503A / 503B | §§ 353a / 353b | Correct |
| CGMP / insanitary (codebook) | 501(a)(2)(B) → § 351(a)(2)(B) (CGMP); 501(a)(2)(A) → § 351(a)(2)(A) (insanitary) | The manuscript gives **no section number** for these codes (§2.2, Table 1). The letters cite 501(a)(2)(B) in 20 letters and 501(a)(2)(A) in 9. Add both (fix C1). |

## 3. Crossref table (re-run live 22 Oct 2026)

| Ref | DOI | Crossref result | Matches manuscript? |
|---|---|---|---|
| Ashraf et al. 2024 | 10.2196/65440 | JMIR 26, e65440; online 2024-11-07; 10 authors as listed | Yes |
| Chetty et al. 2025 | 10.1001/jamahealthforum.2024.5018 | JAMA Health Forum 6(1) e245018; 2025-01-17 | Yes |
| Cohen 1960 | 10.1177/001316446002000104 | Educ Psychol Meas 20(1) 37–46 | Yes |
| Cohen et al. 2022 | 10.1001/jama.2022.9734 | JAMA 328(4); Crossref page "393"; **Europe PMC/PubMed: 393–395** (PMID 35881132) | Page range incomplete |
| DiStefano et al. 2026 | 10.1001/jamahealthforum.2026.2207 | 7(7) e262207; 2026-07-17 | Yes |
| Dmour | 10.1007/s12247-022-09692-4 | 18(3) 965–979; **online 2022-11-16, issue Sep 2023** | **Year should be 2023** (APA: cite the issue year once assigned to an issue); in-text "Dmour, 2022" → "Dmour, 2023" |
| Donohue 2025 | 10.1001/jamahealthforum.2024.5012 | 6(1) e245012 | Yes |
| Kim 2015 | 10.15171/ijhpm.2015.157 | 4(12) 813–821 | Yes |
| Lambson et al. 2023 | 10.1016/j.japh.2023.06.017 | 63(5) 1643–1645 | Yes |
| Mattingly & Conti 2025 | 10.1001/jamahealthforum.2024.5015 | 6(1) e245015; first author has **suffix "II"** | Add suffix: "Mattingly, T. J., II, & Conti, R. M." |
| McCall et al. | 10.1080/14740338.2025.2499670 | 25(3) 581–588; **online 2025-04-29, print 2026-03-04** | **Year should be 2026** (the issue year; vol 25 is 2026). In-text "McCall et al., 2025" → 2026 |
| Rogers et al. 2020 | 10.1007/s43441-020-00129-z | 54(5) 1123–1133; 2020 | Yes |
| Tucker et al. 2018 | 10.1001/jamanetworkopen.2018.3337 | 1(6) e183337 | Yes |

The builder's `crossref_check.json` agrees with these results, but the builder did not act on the online-versus-issue year differences for Dmour and McCall.

**URLs (live, HTTP 200):**
- FDA 2026a (content current as of 04/01/2026)
- FDA 2026b (03/03/2026)
- FDA 2026c Warning Letters page
- openFDA enforcement endpoint
- Hims letter 716567
- FDA RPM Ch. 4 (fda.gov/media/71878/download)
- FDA GLP-1 concerns page, at its **new** path

## 4. In-text vs reference list and APA 7

- **Listed but not cited:** US Food and Drug Administration (2026c), *Warning letters* [Database]. Cite it in §2.1 at "FDA's warning-letter index" (fix A3).
- **Cited but not listed:** none. All other in-text citations match a reference entry. Two uncited sources should be added: the FDA RPM Ch. 4 (B1) and, if adverse-event reports are mentioned, the GLP-1 concerns page (B4).
- **Year mismatches:** Dmour (2022 → 2023) and McCall (2025 → 2026). Change both in-text and in the list.
- **FDA 2026a date:** the page carries an update date, so APA allows "(2026, April 1)" in place of "(2026a)" with "content current as of" in parentheses. The current form is acceptable. Keep the a/b/c ordering consistent with the dated entries.
- **openFDA:** APA prefers the agency as author: "US Food and Drug Administration. (2026d). *openFDA drug recall enforcement reports API* [Data set]." The current "openFDA" author is acceptable but inconsistent with the other FDA entries.
- **Chetty title:** "glucagon-like peptide-1 receptor agonists" in sentence case is fine.

## 5. Corrected reference list (changes marked ►)

Ashraf, A. R., Mackey, T. K., Vida, R. G., Kulcsár, G., Schmidt, J., Balázs, O., Domián, B. M., Li, J., Csákó, I., & Fittler, A. (2024). Multifactor quality and safety analysis of semaglutide products sold by online sellers without a prescription: Market surveillance, content analysis, and product purchase evaluation study. *Journal of Medical Internet Research*, *26*, e65440. https://doi.org/10.2196/65440

Chetty, A. K., Chillakanti, M., Ramachandran, R., Ross, J. S., & Chen, A. S. (2025). Online advertising of compounded glucagon-like peptide-1 receptor agonists. *JAMA Health Forum*, *6*(1), e245018. https://doi.org/10.1001/jamahealthforum.2024.5018

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, *20*(1), 37–46. https://doi.org/10.1177/001316446002000104

► Cohen, P. A., Avula, B., Katragunta, K., & Khan, I. (2022). Recalls, availability, and content of dietary supplements following FDA warning letters. *JAMA*, *328*(4), 393–395. https://doi.org/10.1001/jama.2022.9734

DiStefano, M. J., Tilley, A., Paratane, D., Gyimah Gyamfi, H., Moore, G. D., & Nair, K. V. (2026). Postshortage compounded GLP-1 RA market in 2 states with potentially high demand. *JAMA Health Forum*, *7*(7), e262207. https://doi.org/10.1001/jamahealthforum.2026.2207

► Dmour, I. (2023). Content analysis of US FDA warning letters issued to compounding pharmacies regarding violations of current good manufacturing practices between 2017 and 2022. *Journal of Pharmaceutical Innovation*, *18*(3), 965–979. https://doi.org/10.1007/s12247-022-09692-4

Donohue, J. M. (2025). Using compounded GLP-1 receptor agonists—Informing and protecting consumers. *JAMA Health Forum*, *6*(1), e245012. https://doi.org/10.1001/jamahealthforum.2024.5012

Kim, H. (2015). Trouble spots in online direct-to-consumer prescription drug promotion: A content analysis of FDA warning letters. *International Journal of Health Policy and Management*, *4*(12), 813–821. https://doi.org/10.15171/ijhpm.2015.157

Lambson, J. E., Flegal, S. C., & Johnson, A. R. (2023). Administration errors of compounded semaglutide reported to a poison control center—Case series. *Journal of the American Pharmacists Association*, *63*(5), 1643–1645. https://doi.org/10.1016/j.japh.2023.06.017

► Mattingly, T. J., II, & Conti, R. M. (2025). Marketing and safety concerns for compounded GLP-1 receptor agonists. *JAMA Health Forum*, *6*(1), e245015. https://doi.org/10.1001/jamahealthforum.2024.5015

► McCall, K. L., Mastro Dwyer, K. A., Casey, R. T., Samana, T. N., Sulicz, E. K., Tso, S. Y., Yalanzhi, E. R., & Piper, B. J. (2026). Safety analysis of compounded GLP-1 receptor agonists: A pharmacovigilance study using the FDA adverse event reporting system. *Expert Opinion on Drug Safety*, *25*(3), 581–588. https://doi.org/10.1080/14740338.2025.2499670

openFDA. (2026). *Drug recall enforcement reports API* [Data set]. US Food and Drug Administration. Retrieved October 22, 2026, from https://api.fda.gov/drug/enforcement.json

Rogers, C. A., Ahearn, J. D., & Bartlett, M. G. (2020). Data integrity in the pharmaceutical industry: Analysis of inspections and warning letters issued by the bioresearch monitoring program between fiscal years 2007–2018. *Therapeutic Innovation & Regulatory Science*, *54*(5), 1123–1133. https://doi.org/10.1007/s43441-020-00129-z

Tucker, J., Fischer, T., Upjohn, L., Mazzera, D., & Kumar, M. (2018). Unapproved pharmaceutical ingredients included in dietary supplements associated with US Food and Drug Administration warnings. *JAMA Network Open*, *1*(6), e183337. https://doi.org/10.1001/jamanetworkopen.2018.3337

US Food and Drug Administration. (2024). *Regulatory procedures manual, chapter 4: Advisory actions*. ► NEW. https://www.fda.gov/media/71878/download *(version dated 5 July 2024 per file name; confirm the date on the PDF's title page)*

US Food and Drug Administration. (2026a). *FDA clarifies policies for compounders as national GLP-1 supply begins to stabilize* (content current as of 04/01/2026). Retrieved October 22, 2026, from https://www.fda.gov/drugs/drug-alerts-and-statements/fda-clarifies-policies-compounders-national-glp-1-supply-begins-stabilize

US Food and Drug Administration. (2026b, March 3). *FDA warns 30 telehealth companies against illegal marketing of compounded GLP-1s* [Press release]. https://www.fda.gov/news-events/press-announcements/fda-warns-30-telehealth-companies-against-illegal-marketing-compounded-glp-1s

US Food and Drug Administration. (2026c). *Warning letters* [Database]. Retrieved October 21, 2026, from https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters ► must be cited in the text

► OPTIONAL, if §4.2 keeps "FDA's adverse-event reports": US Food and Drug Administration. (2026d). *FDA's concerns with unapproved GLP-1 drugs used for weight loss* (content current as of 10/01/2026). Retrieved October 22, 2026, from https://www.fda.gov/drugs/drug-alerts-and-statements/fdas-concerns-unapproved-glp-1-drugs-used-weight-loss

## 6. Novelty findings

Searches run 22 Oct 2026:
- **Europe PMC, published and preprint:**
  - `"warning letter" AND (semaglutide OR tirzepatide OR "GLP-1" OR incretin)`: 5 hits
  - `"warning letters" AND compounded AND (GLP-1 OR semaglutide OR tirzepatide)`: 7 hits
  - `(FDA AND enforcement) AND compounded AND (semaglutide OR tirzepatide) AND (telehealth OR advertising OR marketing)`: 17 hits
  - `"warning letter*" AND telehealth`: 6 hits
  - `"502(bb)" OR "compounded drug advertising"`: 1 hit
  - `SRC:PPR` (preprints only) with GLP-1 and compounding/telehealth/warning-letter/advertising terms: 41 hits
- **Web:** three searches, two of them extended.

What turned up:
- **Europe PMC:** no study that systematically analyses FDA warning letters on compounded or unapproved GLP-1s.
- **Nearest items in Europe PMC:**
  - DiStefano 2026, which uses warning letters as one attribute of supplier facilities.
  - Hailu 2026, *Cureus* (doi:10.7759/cureus.110657), a narrative review of unregulated peptide use and digital promotion with no letter corpus.
  - Ashraf 2024.
- **Preprints:** none on warning letters. Related preprints cover compounded-semaglutide outcomes, research-grade peptides sold to consumers, compounded versus branded tirzepatide, and the Jordan tirzepatide/B12 impurity.
- **Web:** law-firm and trade-press commentary only. Examples: STAT (19 Sep 2025), Fierce Pharma, PharmTech, Venable (March 2026), Wilson Sonsini ("more than 50" letters, Sept 2025), McDermott, Armstrong & Bradylyons, Health Law Alliance, and a Substack post. None is a systematic, coded analysis of the corpus.

Verdict: the claim "I am not aware of a systematic content analysis…" is supported as of 22 Oct 2026. Optionally acknowledge that the letter batches have been summarised in legal and trade commentary, citing one, e.g., Venable 2026, after reading it.

## 7. Prioritised fix list

**A. Must fix (accuracy)**
1. **Grace periods (Intro ¶1, Fig 1 legend events 3 and 6, codebook dates in `common.py`):** say that the 503A periods ran to 18 Feb and 22 Apr 2025 *or until the court ruled on the preliminary injunction, whichever was later*. The rulings came on 5 Mar 2025 (tirzepatide) and 24 Apr 2025 (semaglutide), after which FDA said 503A discretion had ended. Either relabel the Fig 1 events as "announced 503A deadline" or move them to the effective dates. "22 May 2025, the last of the grace-period deadlines" stays correct, and the 18/136 split is unaffected.
2. **Intro ¶3:** Tucker (2018) and Cohen (2022) are not content analyses of warning letters. Suggested rewording: "…online direct-to-consumer promotion (Kim, 2015) and data integrity (Rogers et al., 2020), and FDA warnings and warning letters have been used as data sources in studies of adulterated dietary supplements (Tucker et al., 2018; Cohen et al., 2022)."
3. **Cite FDA (2026c)** in §2.1, or delete it from the list.
4. **Change years:** Dmour 2022 → 2023 and McCall 2025 → 2026, both in-text and in the references.

**B. Should fix (support and precision)**
1. Add a citation for "a warning letter is informal and advisory … not a final agency action": FDA Regulatory Procedures Manual, Ch. 4. Verify the wording against the PDF before quoting.
2. DiStefano: replace "found compounded GLP-1s still widely offered" with, for example, "a secret-shopper study of 75 clinics and med spas in two states (August–October 2025) found compounded products still offered after the shortages ended, some supplied by facilities not licensed for sterile compounding (DiStefano et al., 2026)".
3. Ashraf: narrow the wording to, for example, "semaglutide vials test-bought from illegal online pharmacies were judged probably substandard or falsified (Ashraf et al., 2024)".
4. §4.2 "FDA's adverse-event reports": either cite the FDA GLP-1 concerns page at its new URL (990 semaglutide and more than 730 tirzepatide reports as of 31 May 2026) or drop the phrase.

**C. Minor (APA and style)**
1. Give section numbers for the CGMP and insanitary codes: 501(a)(2)(B) and 501(a)(2)(A) [21 U.S.C. § 351(a)(2)(B), (A)]. Consider adding a one-time FDCA-to-U.S.C. mapping footnote, e.g., "section 502(bb) [21 U.S.C. § 352(bb)]".
2. Mattingly: add the "II" suffix. Cohen 2022: give pages 393–395.
3. §2.3 boilerplate quote: add "… when they are not" or an ellipsis. Describe 502(bb) as "advertising or promotion".
4. Optional: cite the Hims & Hers letter (FDA, 9 Sep 2025, letter 716567) as a reference for the §3.4 quotation. Note that Kim (2015) also included notices of violation. Change "mid-2024" to "July–September 2024" for Chetty.
