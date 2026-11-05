# Citation audit: Paper 18, "Retractions in nutrition and obesity research: reasons, timing and citations"

Independent auditor: Claude (Anthropic), 29 October 2026. I did not write the manuscript. I audited `pkg/manuscript/manuscript.md`, `pkg/README.md` and `lit/brief.md`. I did not edit the manuscript.

How each check was done:
- **Metadata:** checked against api.crossref.org/works/DOI, through WebFetch or a Chrome tab I opened myself. The arXiv DOI was checked against api.datacite.org.
- **Retraction status:** for every DOI, I looked for `updated-by` or `relation` entries in Crossref. Crossref now includes Retraction Watch notices, so this covers both sources.
- **Content:** read on the publisher site, PMC, Europe PMC or the OSF API. Each row below says whether I read the full text (**FT**) or only the abstract (**ABS**).
- **Data sources:** the GitLab commit, licence, file size and SHA-256 came from the GitLab API. I read the Crossref documentation page and both Crossref blog posts in full. The OpenAlex licence came from openalex.org/about.
- **Limits:** one Chrome tab, now closed. I did not get past any bot check: SAGE and PNAS served Cloudflare pages, and I left them.

## 1. Summary

All 19 references exist. Their DOIs resolve to the works described, and in-text citations match the reference list one to one (19 and 19, no orphans). No cited work has been retracted or has an expression of concern. The data-source statements are accurate. Commit `827665ab699e4a798060b95c40268de417b7f2e1` and its message match. The CSV is 67,716,155 bytes, and its SHA-256 `7020113802…c303` matches GitLab's `x-gitlab-content-sha256` header. The project has no licence set, and the README has no licence or citation text. The documentation lists 20 fields and says reasons use "a controlled vocabulary maintained by Retraction Watch". Both Crossref blog quotes are verbatim. OpenAlex data are CC0.

The fixes below are needed. None changes a result.

1. **Sebo & Sebo (2025), 10.1080/08989621.2025.2484555.** This work is not retracted, and it supports the claim it is cited for. However, the same authors' companion study (10.1080/08989621.2025.2465621) was retracted on 24 February 2026, after an expression of concern on 1 August 2025. The publisher's notice says the editors "were unable to reproduce the results". The cited paper relies on that study in its false-positive check. The manuscript correctly avoids the retracted paper. I recommend adding a second, independent source for the coverage claim, or a short note.
2. **Sánchez-Calabuig et al. (2026) were described wrongly.** The 45 articles were *withdrawn* (retracted) between 2000 and 2025. The manuscript says "published between 2000 and 2025". The abstract says the study covered "nutrition articles withdrawn between 2000 and 2025".
3. **Avenell et al. (2019) were described wrongly.** The manuscript says "many with hip-fracture outcomes". In the source, all 12 affected trial reports were chosen *because* they had hip-fracture outcomes.
4. **The Crossref forum post (2024) has a named author,** Martyn Rittman (username mrittman), so it should be cited under his name, not "Crossref". The post also says the CSV is updated "each working day" (around 23:00 UTC), not daily.
5. **Two Crossref blog posts have DOIs** that the references leave out: Hendricks et al. 2023 is 10.13003/c23rw1d9 and Rittman 2025 is 10.13003/692016.
6. **Bhat et al. (2025): the subtitle is missing.** The article and PubMed/PMC give the title as "…Clinical Cardiovascular Literature: Analysis of the Retraction Watch Database". Crossref omits the subtitle.
7. **A sentence in §2.1 cites the wrong source.** It says the database is compiled "from publisher websites, scholarly databases and community reports" and cites Hendricks et al. (2023). That wording comes from the Crossref documentation page (Crossref, n.d.), not the 2023 announcement.
8. **Shamsi et al. (2025): drop a hedge.** I verified the full text. The hedge "as summarised from their article page" can go: Table 4 reports Misconduct 87 (82.9%), and reasons came from the Retraction Watch database.
9. **Joseph (2026) needs two caveats.** It is a MetaArXiv preprint posted 27 October 2026, two days before this audit, and not peer reviewed. Its 71.1% covers Retraction Watch retractions with a PubMed ID, retracted 1990–2023, with citations from Europe PMC. The manuscript compares it with this paper's OpenAlex 76.2%, so it should say the two figures come from different populations and citation sources.
10. **Small wording points:**
    - Parvin et al. found records in Web of Science and took the details from Retraction Watch. "Analyses of the Retraction Watch database" therefore fits Bhat, Zilberman and Okyay better than Parvin; "analyses using Retraction Watch data" covers all four.
    - The OpenAlex documentation describes `counts_by_year` as covering "roughly the last ten years". I confirmed empirically that it starts at 2012 for two pre-2012 works.
    - The claim that Hindawi caused most 2023 retractions has no source. Van Noorden (2023) supports it.

The novelty claim holds as worded ("I am not aware of one for nutrition and obesity with an all-field comparison"). See section 6.

## 2. Claims table

Source read: FT = full text, ABS = abstract only, T = title/metadata only.

| # | Manuscript location and claim | Source | Read | Verdict |
|---|---|---|---|---|
| 1 | §1: twelve trial reports from one group, "many with hip-fracture outcomes", retracted for misconduct | Avenell 2019 | FT (PMC6830710) | **Needs fix.** All 12 were chosen because they had hip-fracture outcomes ("assessed more likely to have had impact because they had hip fracture outcomes"). Say "with hip-fracture outcomes". They were published 1998–2011 and "eventually retracted for research misconduct". |
| 2 | §1: cited in 1,158 publications by 2016, including 68 reviews, guidelines and trials; 13 would probably change; by 2018 only one reassessed | Avenell 2019 | FT | Accurate. The source says 13 "guidelines, systematic or other reviews would likely change their findings", and by 2018 "only one of the 68 … appeared to have undertaken a reassessment". |
| 3 | §1: "see also Bolland et al., 2016"; §4.3: the trials took a long time to come to light | Bolland 2016 | ABS (Europe PMC; Neurology is paywalled) | Supported as context. The source covers 33 RCTs over 15 years by one group, with integrity concerns. The retraction years themselves come from the Avenell correction (2016–2019). |
| 4 | §1 and §4.2: Shamsi found 105 retracted articles 1997–2023 in WoS "Nutrition & Dietetics"; misconduct most common; mean time to retraction 1,488 days; 82.9% misconduct | Shamsi 2025 | FT (escienceediting.org) | Accurate. Search string `WC= Nutrition & Dietetics AND DT=Retracted Publication`, November 2024. Table 1 gives the mean of 1,488 days. Table 4 gives Misconduct 87 (82.9%). Drop the hedge "as summarised from their article page". |
| 5 | §1: Sánchez-Calabuig found 45 articles "published between 2000 and 2025" | Sánchez-Calabuig 2026 | ABS (Europe PMC/PubMed 42012409; SAGE full text blocked by bot check, not open access) | **Needs fix.** The abstract says "withdrawn between 2000 and 2025". PubMed and PMC were searched on 30 April 2025. |
| 6 | §1: leading causes 18.9% / 15.1% / 11.3%; median time to retraction 4.2 years; 1,155 Scopus citations, 53% after retraction | Sánchez-Calabuig 2026 | ABS | Accurate. The percentages are not whole-number shares of 45 (18.9% = 10/53), so their denominator is probably coded causes. Consider "of coded causes". |
| 7 | §4.2: Sánchez-Calabuig coded the notices themselves into exclusive categories | Sánchez-Calabuig 2026 | ABS | Accurate: "eight exclusive categories (κ = 0.86)". |
| 8 | §1: neither study compared nutrition with other fields | Shamsi FT; Sánchez-Calabuig ABS | | Accurate. Shamsi mentions other studies only in passing in the discussion and uses no common-data baseline. |
| 9 | §1: field-specific analyses of the Retraction Watch database exist for diabetes (Parvin) | Parvin 2026 | FT available (PMC13404472); read abstract and methods | **Wording.** Parvin used Web of Science (1978–2024, 316 articles) and took the details from Retraction Watch. Say "using Retraction Watch data". |
| 10 | §1: …cardiovascular medicine (Bhat) | Bhat 2025 | FT (PMC12296457), methods read | Accurate. Bhat extracted the "(HSC) Medicine-Cardiology" and "(HSC) Medicine-Cardiovascular" subject codes from the Retraction Watch database. |
| 11 | §1: …infectious diseases (Zilberman) | Zilberman 2023 | T only (paywalled; Europe PMC has no abstract) | Supported by the title ("an analysis using the retraction watch database"). Content not read. |
| 12 | §1: …medicine as a whole (Okyay) | Okyay 2025 | FT (PMC12669648) | Accurate. Descriptive Retraction Watch analysis of medicine over 50 years; no nutrition, diet or obesity subgroup. |
| 13 | §1, §2.1: in September 2023 Crossref acquired the database and made it openly available; owned and distributed by Crossref since then | Hendricks 2023 | FT (blog) | Accurate. The post says the database "has been acquired by Crossref and made a public resource". |
| 14 | §2.1: database "compiled … from publisher websites, scholarly databases and community reports" | cited to Hendricks 2023 | FT | **Cite Crossref (n.d.) instead or as well.** The documentation page says "searching scholarly databases, checking publisher websites, web searches, and reports from the community". |
| 15 | §1: since October 2024 a "daily-updated CSV file in a public repository" | Crossref 2024 forum post | Read via WebFetch (Chrome had no permission for this domain) | **Wording and author.** The CSV moved from Crossref Labs to the GitLab repository and is updated "each working day at about 23:00 UTC". The author is mrittman (Martyn Rittman). |
| 16 | §2.1: the file has 20 documented fields, and reasons come from a controlled vocabulary | Crossref n.d. | FT | Accurate. The page lists 20 column headings. Reason: "This uses a controlled vocabulary maintained by Retraction Watch." |
| 17 | §2.1: "No licence is stated for the dataset in the repository or on the Crossref documentation page" | GitLab API; Crossref n.d. | FT | Accurate. The GitLab project `license` is null. The README at the commit (4,044 characters) contains no licence or citation text. The documentation page's only licence text is the site-wide footer ("The content of this site is licensed under a Creative Commons Attribution 4.0 International License"), which is about the website. |
| 18 | §2.1 and README: Crossref describes the data as "freely available" and asks for "a citation to the source" | Rittman 2025 | FT | **Verbatim, confirmed.** "Like the rest of our metadata, the retractions are freely available." and "…we kindly request that you provide a citation to the source." The same paragraph also says "Crossref metadata is freely available to reuse without a license". That is consistent with the manuscript's cautious wording; adding it is optional. |
| 19 | §2.1 and §5: commit 827665a ("Retraction Watch data for 2026-10-28"); 67,716,155 bytes; SHA-256 7020…c303 | GitLab API | Checked | Accurate. Committed 2026-10-28T23:00:10Z by build-retractionwatch-csv; project 61336882, created 2024-09-02; repository holds README.md and retraction_watch.csv. The size and SHA-256 headers match. |
| 20 | §1: "most retractions have been attributed to misconduct rather than error" (Fang) | Fang 2012 | FT (PMC3479492) | Accurate. Of 2,047 biomedical and life-science articles, 67.4% were misconduct and 21.3% error. A 2012 correction exists (10.1073/pnas.1220649110); its content was not read (PNAS bot check). |
| 21 | §1 and §4.2: only 5.4% of post-retraction citation contexts acknowledged the retraction | Hsiao & Schneider 2021 | FT (PMC9520488) | Accurate. "Among the 13,252 postretraction citation contexts, only 722 (5.4%)…" |
| 22 | §1 and §4.2: census of more than 22,000 retracted biomedical papers; 71.1% cited in a later year | Joseph 2026 | ABS (OSF API; PDF download blocked cross-origin) | Accurate: "15,992 retracted papers (71.1%) were cited in a later year". **Add caveats:** preprint posted 2026-10-27, not peer reviewed; covers retractions with a PubMed ID, retracted 1990–2023; citations come from Europe PMC, not OpenAlex. |
| 23 | §4.2: Avenell showed such citations can distort systematic reviews and guidelines in "nutrition-adjacent clinical research" | Avenell 2019 | FT | Accurate. The trials were vitamin D, vitamin K, folate or mecobalamin and calcium supplementation trials, alongside bisphosphonate (risedronate, alendronate) trials. The conclusion says they "distorted the evidence base". |
| 24 | §4.4: "No database of retractions is complete" | Sebo & Sebo 2025 (2484555) | FT (tandfonline) | Supported: the Retraction Watch database found 815 of 878 (92.8%), PubMed 86.3%, Web of Science 83.6%. **Caution:** see section 4. |
| 25 | §2.3: Newcombe hybrid-score intervals | Newcombe 1998 | T | Appropriate citation for the method. Content not re-read. |
| 26 | §2.4: OpenAlex `counts_by_year` "for each citing year from 2012 onwards" | Priem 2022; OpenAlex docs | Docs read | Docs say "roughly the last ten years". The API returned 2012 as the earliest year for two pre-2012 works (Newcombe 1998, Fang 2012). Suggested wording: "which, at the time of query, covered citing years 2012 onwards". |
| 27 | §5 and README: "OpenAlex data are CC0" | openalex.org/about | Read | Accurate: "All OpenAlex data is released under a CC0 public-domain license". There is no reference for it; consider citing the About page. |
| 28 | Acknowledgements: "OurResearch for OpenAlex" | — | — | **Unverified.** The current About page calls OpenAlex "a small nonprofit team" and does not name OurResearch. Check the current organisation name. |
| 29 | §2.2: Hindawi "was responsible for a large share of 2023 retractions" | none | — | **Unsourced.** Van Noorden (2023) says "the bulk of 2023's retractions were from journals owned by Hindawi" (more than 8,000 articles). Metadata verified via Crossref; text read through a fetch summary. |
| 30 | §1: "in 2023, 11,132 of the 13,227 retractions … cited a paper mill, compromised peer review or computer-generated content" | own results | — | Not a citation. Point to the results file (for example `comparison.json` or `trends.json`) so readers can see where it comes from. |

## 3. Reference table

CR = Crossref, DC = DataCite. "Retraction / EoC" reports Crossref `updated-by` entries, which include Retraction Watch notices.

| Reference | DOI resolves / metadata | Retraction / EoC | Notes |
|---|---|---|---|
| Avenell et al. 2019, BMJ Open 9(10) e031909 | CR: matches (authors, title, volume, issue, article number) | None. Has a correction (10.1136/bmjopen-2019-031909corr1, 16 December 2019) that only fixes reference details. | OK |
| Bhat et al. 2025, JACC: Advances 4(8) 101802 | CR: matches. CR title has no subtitle; the article and PMC show ": Analysis of the Retraction Watch Database" | None | Add the subtitle |
| Bolland et al. 2016, Neurology 87(23) 2391–2402 | CR: matches | None | OK |
| Crossref n.d., documentation page | Page live, content confirmed | n/a | OK. Live URL is www.crossref.org/… (the non-www URL also works). |
| Crossref 2024 forum post | Post exists: title and date (11 October 2024) match; author mrittman | n/a | Change author to Rittman, M.; label [Online forum post] |
| Crossref & Retraction Watch 2026, data set, commit 827665ab… | GitLab API confirms commit, message and date | n/a | OK |
| Fang et al. 2012, PNAS 109(42) 17028–17033 | CR: matches | None. Correction 10.1073/pnas.1220649110 (17 December 2012), content unread | OK. Optionally note the correction |
| Hendricks et al. 2023, Crossref Blog | Post exists; authors and date match | n/a | Add https://doi.org/10.13003/c23rw1d9 |
| Hsiao & Schneider 2021, QSS 2(4) 1144–1169 | CR: matches (issued 2021; PubMed lists February 2022) | None | OK; keep 2021 (CR) |
| Joseph 2026, MetaArXiv preprint | CR: posted content, sole author Stephan Joseph, 2026-10-27; title matches | None | OK. Label clearly as a preprint |
| Newcombe 1998, Stat Med 17(8) 873–890 | CR: matches | None | OK |
| Okyay et al. 2025, JKMS 40(46) e300 | CR: matches; published online 2025-10-15 | None | OK |
| Parvin et al. 2026, MJIRI 40, 20 | CR: title and authors match. CR has no volume or article-number fields; PMC citation "2026 Feb 28;40:20" confirms 40, 20 | None | OK |
| Priem et al. 2022, arXiv 2205.01833 | DC: title and authors match; v2 June 2022 | n/a | OK |
| Rittman 2025, Crossref Blog | Post exists; author and date match | n/a | Add https://doi.org/10.13003/692016 |
| Sánchez-Calabuig et al. 2026, Nutrition and Health, advance online | CR: 7 authors match; online 2026-04-21; no volume or issue | None | OK |
| Sebo & Sebo 2025, Accountability in Research 33(2) 2484555 | CR: title matches; online 2025-03-29, issue 2026-02-17 | **None on this DOI.** Companion 10.1080/08989621.2025.2465621 has an EoC (2025-08-01) and was retracted (2026-02-24; notice 10.1080/08989621.2026.2633865) | See section 4. Year: CR "issued" is 2025, so (2025) with 33(2) is consistent with CR. Using 2026 (the issue year) is also defensible. |
| Shamsi et al. 2025, Science Editing 12(2) 131–137 | CR: matches | None | OK |
| Zilberman et al. 2023, CMI 29(11) 1454.e1–1454.e3 | CR: 4 authors (Zilberman, Margalit, Yahav, Tau) match | None | OK |

In-text and reference-list match: all 19 cited works appear in the list, and all 19 list entries are cited. Narrative "Hsiao and Schneider (2021)" and parenthetical "&" are both correct APA. The retracted Sebo paper (2465621) is not cited, as the brief advised.

## 4. Sebo & Sebo: why it needs care

The cited paper (2484555) is a separate study: 878 retracted publications in 131 high-impact journals, searched 15 December 2024. It has no notice in Crossref and none on the publisher's page as of 29 October 2026. However:

- The same authors' "preliminary study" (2465621), on the same three databases, was retracted. The notice says concerns were raised "about the reliability of the data in the article and the reproducibility", and the editors "were unable to reproduce the results".
- The cited paper uses that retracted study in its methods ("in our previous small study … we did not find any false positives (Sebo and Sebo 2025)") and in its discussion.

The specific claim the manuscript cites (that no single source is complete) rests on 2484555's own counts, so it still stands. However, a paper on retractions should avoid looking as if it leans on a cluster with a retraction. Options:

- **(a)** Keep the citation and add a clause: "(Sebo & Sebo, 2025; a related study by the same authors was later retracted)".
- **(b)** Replace or supplement it with an independent coverage study. Candidates appear in Sebo's reference list but I did not verify them here, so they must be checked before use: Ortega & Delgado-Quirós (2024, *Scientometrics*), and Schneider et al. (2023, STI conference paper on Crossref, Retraction Watch, Scopus and Web of Science).

## 5. Corrected entries (APA 7)

In-text changes:

- §1: "(Crossref, 2024)" becomes "(Rittman, 2024)". Change "daily-updated CSV file" to "a CSV file updated each working day".
- §2.1: "…community reports and has been owned … since September 2023 (Crossref, n.d.; Hendricks et al., 2023)".
- §1: "found 45 retracted between 2000 and 2025" (in place of "published").
- §1: "Twelve trial reports from one research group, all with hip-fracture outcomes, …".

Reference entries:

Bhat, V., Kaushik, S., Kumar, A., Bellur, S., & Kalra, A. (2025). Retractions and withdrawals in clinical cardiovascular literature: Analysis of the Retraction Watch Database. *JACC: Advances, 4*(8), 101802. https://doi.org/10.1016/j.jacadv.2025.101802

Hendricks, G., Lammey, R., Ofiesh, L., Bilder, G., & Pentz, E. (2023, September 12). *News: Crossref and Retraction Watch*. Crossref Blog. https://doi.org/10.13003/c23rw1d9

Rittman, M. [mrittman]. (2024, October 11). *Changes to delivery of Retraction Watch metadata* [Online forum post]. Crossref Community Forum. https://community.crossref.org/t/changes-to-delivery-of-retraction-watch-metadata/12368

Rittman, M. (2025, January 29). *Retraction Watch retractions now in the Crossref API*. Crossref Blog. https://doi.org/10.13003/692016

Optional additions (metadata verified on Crossref 29 October 2026):

Van Noorden, R. (2023). More than 10,000 research papers were retracted in 2023 — a new record. *Nature, 624*(7992), 479–481. https://doi.org/10.1038/d41586-023-03974-8 (for the Hindawi claim in §2.2)

Schneider, J., Ye, D., Hill, A. M., & Whitehorn, A. S. (2020). Continued post-retraction citation of a fraudulent clinical trial report, 11 years after it was retracted for falsifying data. *Scientometrics, 125*, 2877–2913. https://doi.org/10.1007/s11192-020-03631-1 (a case study of the retracted Matsuyama et al., 2005, *Chest* trial; only the abstract opening was read, the issue number was not confirmed, and the trial's topic was not checked here)

## 6. Novelty assessment

Searches run on 29 October 2026:

- **Europe PMC REST, titles:** retract* or "Retraction Watch" combined with nutrition, nutritional, diet, dietary, dietetics, obesity, food, supplement*, vitamin* or "weight loss", 2010–2026. 805 hits; after removing notices, the only analysis of retractions was Sánchez-Calabuig 2026.
- **Europe PMC REST, all fields:** "Retraction Watch" or "retracted publications/articles/papers" combined with nutrition, dietetics, obesity, food science, dietary supplement or vitamin D, 2012–2026. 896 hits.
- **Europe PMC REST, post-retraction citation:** "post-retraction" or "after retraction" with citation*, combined with nutrition, diet, obesity, vitamin D or food.
- **Web searches (four):** nutrition or obesity retractions with Retraction Watch; food science, dietary supplement or obesity bibliometric retractions; Retraction Watch by-subject comparisons; post-retraction citation of nutrition or vitamin D trials.

What I found:

- **Nutrition and dietetics retraction studies:** only Shamsi 2025 (Web of Science category, n = 105, no baseline) and Sánchez-Calabuig 2026 (PubMed MeSH, n = 45, citations in Scopus, no baseline). Shamsi is not indexed in Europe PMC. It was found by web search and is already cited.
- **Adjacent single-field studies using Retraction Watch:** diabetes (Parvin 2026), cardiovascular (Bhat 2025), infectious diseases (Zilberman 2023), smoking (de Granda-Orive et al. 2025, *Open Respiratory Archives*, 10.1016/j.opresp.2025.100496; title seen in Europe PMC only, not verified further), veterinary (Christopher 2022; title only). None covers nutrition or obesity.
- **Cross-field retraction comparisons:**
  - Ioannidis et al. 2025, *PLoS Biology*, 10.1371/journal.pbio.3002999. Links the Retraction Watch database to Scopus data on highly cited authors by subfield. The main text has no nutrition-specific analysis (searched the full text for "utrition"). It is author-level, not field-level.
  - Zhou et al. arXiv 2511.21176 (v2, July 2026). Retraction rates by topic. From the abstract I could not tell whether it reports a nutrition topic or uses Retraction Watch data.
  - Neither is a nutrition analysis with an all-field reason, timing and citation comparison. Zhou et al. is relevant to the §4.4 "Denominator" limitation (rates per publication by topic), so consider citing it there after checking it.
- **Post-retraction citation:** well studied biomedicine-wide (Hsiao & Schneider 2021; Joseph 2026) and in single-case studies (Avenell 2019; Schneider et al. 2020). For nutrition, only Sánchez-Calabuig (n = 45, Scopus, no comparison group).

Verdict:

- **"Earlier studies of retracted nutrition articles were small and lacked a comparison with other fields"** holds.
- **"I am not aware of one for nutrition and obesity with an all-field comparison"** holds, and it is properly hedged.
- **The post-retraction citation analysis is not novel as a method.** Its new part is the year-matched comparison with other biomedical retractions for this field. If a novelty sentence is added, narrow it: "I am not aware of a comparison of post-retraction citation of nutrition retractions with a matched set of other biomedical retractions."
- **Do not claim the GLP-1 subgroup as a contribution.** It was not analysed, and the manuscript already says so.

## 7. Not verified

- Sánchez-Calabuig, Bolland and Zilberman full texts: paywalled, or blocked by a bot check.
- Joseph 2026 PDF: read through the OSF API abstract only.
- The content of the Fang 2012 correction.
- The current OpenAlex organisation name ("OurResearch").
- Zhou et al. (arXiv) content beyond its abstract.
- The topic of the Schneider et al. 2020 case-study trial.
- The two candidate replacement coverage sources for Sebo (Ortega & Delgado-Quirós 2024; Schneider et al. 2023).
