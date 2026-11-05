# Independent number audit: Paper 18, "Retractions in nutrition and obesity research: reasons, timing and citations"

Auditor: independent Claude agent (did not write the paper). Date: 29 October 2026.
Scope: rerun of the pipeline from source, spot-check of individual records, check of every number in `manuscript/manuscript.md` and the figures against `results/`, and a review of methods.

## Verdict

**The numbers reproduce exactly, and the manuscript transcribes them correctly. Two headline conclusions are not robust and need rewording before release.**

- Rerun: the same CSV was fetched from the GitLab API at commit 827665a (67,716,155 bytes, SHA-256 matches). The five shipped Python scripts plus `fetch_openalex.js` were hash-checked in the browser and all six matched. Re-running them in Pyodide 0.26.4 (Python 3.12.1, pandas 2.2.0, NumPy 1.26.4) gave **byte-identical** `records.csv`, `citation_dois.json`, `selection.json`, `trends.json`, `comparison.json` and `sensitivity.json`.
- OpenAlex: all 1,296 DOIs were re-queried, more than the 50-paper sample the brief required. Matches were 425/432 and 853/864, and no requests failed. Every value in `citations.json` and Table 4 reproduced to the stated precision. The only drift was total field post-retraction citations: 5,767 now against 5,768 shipped, which is expected live-index drift and does not change any rounded figure. Every work's `counts_by_year` starts at 2012 or later, so the Methods claim about coverage from 2012 holds.
- Manuscript: every number in the abstract, social summary, text, Tables 1–4, captions and graphical abstract was checked. Apart from the wording and counting items in the table below, they all match the result files and are rounded correctly.
- **Conclusion-level problems.** These are not transcription errors. They are in results the package already holds, or that one extra line of code produces:
  1. **"Misconduct about as often as elsewhere" depends on including conference papers.** The comparator holds 13,920 conference retractions (20.7% of the rest), mostly IEEE, and 10,035 of them cite only "Notice – Limited or No Information". When conference papers are excluded from both sides (`comparison.json` → `primary_vs_rest_journal_only`), misconduct is **57.4% vs 69.7%, −12.3 points (95% CI −16.0 to −8.6)**. That is clearly *less* misconduct in the field. The Table 3 row "Primary, excluding conference papers" does not test this, because its comparator still includes the conference papers. Against the rest of biomedicine the difference is −3.5 (−7.2 to +0.1), which is borderline.
  2. **"Takes somewhat longer to retract" is mostly a comparator artefact.** With conference papers excluded from both sides, the median times are 1.90 vs 1.78 years, a difference of +0.12 years (bootstrap 95% CI −0.10 to +0.36; auditor's computation, 1,000 resamples). Against the rest of biomedicine, as the paper already reports, the difference is −0.02 (−0.21 to +0.21). The rest-of-database median for 2010–2019 notices is 0.71 years, against 1.95 in the field. That gap reflects the fast 2010–2011 conference mass retractions, not slow detection in nutrition.

## Rerun details

| Item | Shipped | Rerun | Match |
|---|---|---|---|
| retraction_watch.csv bytes / SHA-256 | 67,716,155 / 7020113…c303 | same | yes |
| Code hashes (common, select_records, analysis, citation_sample, citations, fetch_openalex.js) | provenance.md | same | yes (6/6) |
| records.csv (27,411,487 B) | 5d49783c… | same | byte-identical |
| citation_dois.json (121,977 B) | 90274194… | same | byte-identical |
| selection / trends / comparison / sensitivity .json | provenance.md hashes | same | byte-identical |
| openalex.json | ff5dba0d… | differs, as expected (timestamp, live counts) | n/a |
| citations.json (rerun with fresh OpenAlex data) | see Table 4 | all rounded values identical; post_sum 5,767 vs 5,768 | yes, to the reported precision |

The analysis ran in a tab on cdn.jsdelivr.net (the Pyodide console page) that the auditor created and has since closed. GitLab's page CSP blocked Pyodide. Nothing was uploaded, and the CSV was never written to disk.

## Record spot-check (19 records, sampled at random with seed 777: 14 primary, 3 title-keyword-only, 2 food-journal)

For each record the auditor checked the subject code against S, the journal against J, F and the exclusions, the title against K, each reason against its group(s), the misconduct and error-only composites, and the publication-to-notice interval in days, worked out by hand.

| Record ID | Checks | Result |
|---|---|---|
| 2280 | S (BLS+HSC Nutrition), not J (Heart), K ("diets"); duplication + error → misconduct, not error-only; 486 days | correct |
| 46609 | S, K; peer review, data concerns, ethics (IRB, human-subject welfare); 295 days | correct |
| 19350 | S+J (Appetite); no K term; duplication + error; 3,564 days | correct |
| 19577 | S, K (vitamins); fabrication + image (Falsification/Fabrication of Image); 2,821 days | correct |
| 24804 | S, K ("Dietary"); data concerns + ethics; Ethical Violations by Author counted as ethics, not misconduct, as the mapping intends; 4,254 days | correct |
| 18545 | J only (Surgery for Obesity and Related Diseases); limited info; 551 days | correct |
| 7958 | S+J+K (Nutrition Research, vitamins); data concerns, authorship; 5,238 days | correct |
| 73328 | S (PLoS One), K (calorie); image, duplication (Euphemisms), authorship (Objections by Author); 1,239 days | correct |
| 20033 | J only (J Nutr Sci Vitaminol; topic is a bone drug, an example of J including off-topic papers); duplication; 4,472 days | correct |
| 63356 | S (HSC Nutrition in Int Wound J), K (Vitamin D); peer review; 1,047 days | correct |
| 20013 | J only; limited info; 123 days | correct |
| 45353 | J (Food Science & Nutrition); "Duplication of Content through Error by Journal/Publisher" → publisher error only, correctly not counted as duplication; 251 days | correct |
| 70931 | S (Heliyon); data concerns + authorship; 824 days | correct |
| 54636 | S (HSC Nutrition in *Scanning*, a Hindawi title); paper mill, peer review, computer-generated, ethics; a typical subject-code paper-mill case | correct |
| 47376 | K only (obesity); authorship; 362 days | correct |
| 47921 | K only (high-fat diet); peer review, data concerns; 416 days | correct |
| 37438 | K only (dietary polyphenols); fabrication + image; 3,236 days | correct |
| 43676, 43675 | F (Food and Chemical Toxicology, so F also takes in toxicology); plagiarism; "Date … Unknown" → excluded from time to retraction | correct |

Countries were split correctly on ";", and multi-country records counted once per country. No classification or date errors were found.

Reason vocabulary: all 72 mapped reason strings exist verbatim in the data, so there are no silent typos. 46 of the 110 distinct reasons are unmapped. The larger ones are Investigation by Journal/Publisher (30,909), Investigation by Third Party (17,963), **Concerns/Issues about Referencing/Attributions (15,162)**, **Concerns/Issues about Results and/or Conclusions (9,402)**, **Breach of Policy by Author (4,788)**, Concerns/Issues about Methods (268), Taken from Dissertation/Thesis (374) and Misconduct by Third Party or by Company/Institution (57). See M3 for what this does to the results.

## Discrepancy table

Severity: **High** = changes a conclusion or headline claim; **Medium** = a factual statement that is wrong or misleading; **Low** = wording, counts or presentation.

| # | Location | Stated | Correct / found | Source | Severity | Fix |
|---|---|---|---|---|---|---|
| 1 | Abstract; §3.2 para 1; §4.1 ("no worse and no better"); §5 Conclusion ("about as often linked to misconduct") | Misconduct 56.6% vs 59.0%, "about as often" | Correct as computed, but excluding conference papers from both sides gives 57.4% vs 69.7%, −12.3 pp (−16.0 to −8.6). Against rest of biomedicine: −3.5 (−7.2 to +0.1). | comparison.json `primary_vs_rest_journal_only.reasons.misconduct`; `primary_vs_biomed_rest` | High | Report the journal-article-only comparison in §3.2 and Table 1 (or a new row in Table 3 with the comparator also excluding conference papers). Reword the abstract, §4.1 and §5: misconduct is as common as in the whole database only because of the conference retractions in the comparator; among journal articles it is less common. |
| 2 | Abstract ("Median time … 1.84 years (rest: 1.48)"); §3.3; §4.3 ("longer time to retraction, driven by fabrication cases"); §5 ("They take somewhat longer to happen") | Field slower by 0.36 y (0.17 to 0.57) | Difference falls to +0.12 y (−0.10 to +0.36) with conference papers excluded from both sides (auditor's bootstrap); −0.02 against rest of biomedicine; +0.07 within 2020–2026 (1.76 vs 1.69) | comparison.json `primary_vs_rest_journal_only.ttr`/`ttr_comp`, `by_era`, `primary_vs_biomed_rest.ttr_median_diff`; auditor's computation | High | State that the overall gap comes from the fast conference retractions of 2010–2011 in the comparator and disappears against journal articles or biomedicine. Remove "somewhat longer" from §5, or qualify it. "Driven by fabrication cases" (§4.3) is not shown by any analysis: drop it, or say "fabrication cases had the longest medians". |
| 3 | §3.3 "paper-mill retractions the shortest (1.61 years in both)" | Paper mill shortest | Not the shortest. In the field, error-only is 1.29 and peer review 1.52 (paper mill 1.61). In the rest, peer review 1.45 and error-only 1.50. Paper mill has the **narrowest IQR** (field 1.31–1.92). | comparison.json `ttr_by_reason_primary`/`_rest`; Table 2 | Medium | e.g. "paper-mill and peer-review retractions came quickly and uniformly (medians 1.61 and 1.52 years, narrow IQRs)". |
| 4 | §3.2 para 2 "Notices with limited or no information were less common (6.0% vs 18.3%), in part because … conference retractions" | "in part" | Excluding conference papers: 4.9% vs 4.2%, +0.8 (−0.6 to +2.7). The gap is entirely due to conference papers. | comparison.json `primary_vs_rest_journal_only.reasons.limited_info` | Medium | Replace "in part" with "entirely": no difference remains among journal articles. |
| 5 | §2.3 "Reasons were grouped into 15 non-exclusive groups" | 15 | 14 groups are listed (and 14 are in `REASON_GROUPS`), plus 2 composites, giving 16 rows in Table 1 | code/common.py; §2.3 list | Low | "14 non-exclusive groups". |
| 6 | §3.1 "The journals with the most primary-definition retractions were general or mixed-subject venues: BioMed Research International (27), Food Science & Nutrition (24), PLoS One (19), Romanian Journal of Diabetes, Nutrition and Metabolic Diseases (15) …" | All five described as general/mixed | Food Science & Nutrition and the Romanian journal are field-named (rule J) | selection.json `top_journals_primary`/`top_journals_J` | Low | "…were a mix of general venues (BioMed Research International, PLoS One, eCAM) and field-named journals (…)". |
| 7 | §3.1 "fell to 0.8% in 2023, when mass retractions … swelled the denominator" | Implies 2023 was the low | 2022 was lower (0.54%); 2023 was 0.76% | trends.json `primary_share_by_year` | Low | "was 0.5% in 2022 and 0.8% in 2023". Optional. |
| 8 | §3.5 "It was longest for the journal rule (median 2.21 years) and for records meeting both rules (2.67 years)" | J among the longest | "Primary, excluding Hindawi" is 2.26, longer than J's 2.21 | sensitivity.json | Low | "longest for records meeting both rules (2.67), primary without Hindawi (2.26) and the journal rule (2.21)". |
| 9 | §3.5 "The share citing any misconduct was never higher than in the rest of the database (33.3% to 58.5%, vs 59.0%)" | vs 59.0% | Each definition has its own complement; for S it is 58.9% (58.5 vs 58.9) | sensitivity.json `S: subject code only.misconduct.p_comp` | Low | Add "(vs 58.9–59.0%)", or leave as is. Trivial. |
| 10 | Figure 2 caption "Share of retractions citing each reason group" | each | Plot shows 12 of 16 groups (omits data concerns, honest error, forged authorship, publisher error) | figures/fig2_reasons.png | Low | "selected reason groups (all groups in Table 1)". |
| 11 | Graphical abstract | Bottom sentence | Text is clipped at the right edge ("…retractions were" cut off) | figures/graphical_abstract.png | Low | Wrap the text or widen the canvas in graphical_abstract.py. |
| 12 | results/provenance.md line 8 "all six matched" | six | Five result files are listed and hash-checked (selection, trends, comparison, sensitivity, citations) | provenance.md table | Low | "all five matched". |
| 13 | §3.6 / Table 4 total field post-retraction citations | 5,768 | 5,767 in the auditor's live re-query (29 Oct 2026) | rerun | Info | None needed; the existing note that OpenAlex counts change covers it. |

## Methods review

M1. **Deduplication.** Record ID duplicates are dropped, then repeated DOIs are dropped keeping the earliest notice (162 rows). This is reasonable and deterministic, and the auditor reproduced it exactly. No problems.

M2. **Field definitions and sensitivity.** The rules match the text, and Table 3 reproduces exactly. Two notes. (a) F takes in toxicology journals (e.g. Food and Chemical Toxicology), and J takes in some off-topic papers (e.g. a bone-drug paper in J Nutr Sci Vitaminol); the limitations already cover this. (b) Every Table 3 definition is compared with all other records, *including* conference papers. The sensitivity analysis therefore never tests the conference-paper artefact that drives findings 1, 2 and 4. **Add a comparator excluding conference papers.**

M3. **Reason groups.** These are non-exclusive by design; Table 1 and Figure 2 say so, and per-group comparisons are therefore marginal proportions, which is fine. "Manipulation of Images" and "Falsification/Fabrication of Image" count in both fabrication and image, which is intended. The mapping is one defensible choice, but the misconduct comparison is sensitive to it. Adding Breach of Policy by Author, Taken from Dissertation/Thesis and Misconduct by Third Party or by Company/Institution to misconduct moves the comparison from 56.6 vs 59.0 to **57.4 vs 65.7** (auditor's computation). Adding "Concerns/Issues about Results and/or Conclusions" and "…about Methods" to data concerns moves it from 45.4 vs 40.5 to 45.7 vs 41.3, a negligible change. "Concerns/Issues about Referencing/Attributions", a common marker of citation manipulation by paper mills, is unmapped (field 16.8% vs rest 22.4%). Recommendation: list the unmapped reasons in a supplementary table and mention this sensitivity in §4.4 "Reasons".

M4. **CIs.** `newcombe()` correctly implements Newcombe's hybrid Wilson score method (method 10). The bootstrap for the median difference uses 2,000 resamples with a fixed seed, as stated. The paper's p-value-free, descriptive framing is appropriate.

M5. **Time to retraction.** Negative intervals and "Date … Unknown" records are excluded, as stated, and day counts are correct in all spot checks. Many OriginalPaperDate values sit on the 1st of the month or 1 January (e.g. records 2280 and 20033), so precision is to about a month; a sentence in the limitations would cover it. The comparison is confounded by era and article type (see findings 1 and 2). The by-era rows in Table 2 already show this, but the text does not interpret them.

M6. **OpenAlex matching and the comparison sample.** The year-stratified 2:1 sample is implemented correctly (432 + 864, seed 20261029, no duplicate DOIs). The bootstrap resamples within groups but not within year strata. Because the design is balanced at exactly 2:1 per year this matters little, but it could be noted. Match rates are high (98.4%, 98.7%). `per_page=50` with 50 DOIs per request could in principle truncate results if OpenAlex returned more than 50 works for a batch. No requests failed, and the 1,280 works keyed slightly exceed the 1,278 found, so this did not bite here.

M7. **Citation ratio CI.** This is a percentile bootstrap of the ratio of means, done correctly. Neither period-specific ratio excludes 1 (1.58, 0.97–2.49; 1.74, 0.96–3.11), while the pooled ratio does (1.69, 1.11–2.70). The text's reading ("a minority of heavily cited papers", "also more cited before retraction") is appropriate. The -1 year comparison (4.19 vs 2.82) is descriptive only.

M8. **Hindawi influence.** This is handled well. Excluding Hindawi from both sides gives misconduct of 49.9% vs 50.9%, and paper mill 2.5% vs 7.7%, so the field still has fewer paper-mill cases. The time-to-retraction difference with Hindawi excluded from both sides is +0.61 y (0.31 to 1.09; auditor's computation) because Hindawi's fast mass retractions dominate the 2023 comparator. This should be read together with finding 2, since conference and Hindawi effects pull in opposite directions. The paper should report the comparator excluding conference papers as its main robustness check for timing.

## Not verified by the auditor

- External figures from the literature: Shamsi et al. (105 articles, mean 1,488 days, 82.9%), Sánchez-Calabuig et al. (45 articles, 18.9/15.1/11.3%, 4.2 years, 1,155 citations, 53%), Avenell et al. (1,158 publications, 68, 13, one reassessed), Hsiao & Schneider (5.4%), Joseph (22,483 papers, 71.1%). Checking these is the citation auditor's job.
- That the CSV has "20 documented fields": the file has 20 named columns plus one empty trailing column ("Unnamed: 20"). The Crossref documentation itself was not checked.
- `summary.py`, `figures.py`, `tables.py` and `graphical_abstract.py` were not re-run. Their outputs (`summary.json`, `tables.md`, PNGs) were checked against the verified JSONs by reading them, and all plotted values that could be read off matched.
