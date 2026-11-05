---
title: "Retractions in nutrition and obesity research: reasons, timing and citations"
subtitle: "A comparison with the whole Crossref Retraction Watch database, with citation counts after retraction from OpenAlex"
---

**Peter Kalafatis**

Independent researcher, x9m8.com, New York, NY, USA. Correspondence: x9m8x7@gmail.com

**Preprint, not peer reviewed.** Version 1, October 2026.

## Abstract

Earlier studies of retracted nutrition articles were small and lacked a comparison with other fields. In the Crossref-distributed Retraction Watch database (67,840 retractions to 28 October 2026), I identified 716 in nutrition and obesity research, by subject code or journal title, and compared them with the rest. Retractions in the field rose from 27 in 2000–2009 to 420 in 2020–2026, peaking at 119 in 2024. Among journal articles, misconduct was cited less often in the field than elsewhere (57.4% vs 69.7%); with bulk-retracted conference papers included in the comparison, the shares were close (56.6% vs 59.0%). Paper mills (12.4% vs 20.9%) and compromised peer review (24.1% vs 38.3%) were less common. Errors without a misconduct flag (13.5% vs 8.7%), ethics or consent problems (10.9% vs 6.3%) and authorship disputes (18.2% vs 13.5%) were more common. Time to retraction was similar (median 1.90 vs 1.78 years). In OpenAlex, 76.2% of the field's papers retracted in 2012–2023 were cited in a later year, much like matched biomedical retractions (77.5%). Journals named for nutrition, diet or obesity had no paper-mill retractions, so results depend on the field definition. Only 28 retractions concerned GLP-1 or other obesity drugs, too few to analyse.

**Keywords:** retractions; research integrity; nutrition; obesity; dietetics; Retraction Watch; post-retraction citation; paper mills; OpenAlex

**Social media summary:** 716 retracted nutrition papers: less misconduct than other journals, more errors, most still cited.

## 1. Introduction

Nutrition science has a credibility problem that predates the current wave of retractions. Its findings reach the public quickly, through dietary guidance, food labelling and the press, and a retracted trial can keep shaping that guidance long after the notice appears. One well-documented case shows how. Avenell et al. (2019) followed 12 trial reports from one research group, all with hip-fracture outcomes, that were eventually retracted for research misconduct. By 2016 they had been cited in 1,158 publications, including 68 systematic reviews, meta-analyses, narrative reviews, guidelines and clinical trials. Of those 68, the authors judged that 13 would probably change their findings if the retracted trials were removed, and by 2018 only one had been reassessed (see also Bolland et al., 2016).

Two field-level descriptions of retractions in nutrition exist. Shamsi et al. (2025) searched the Web of Science category "Nutrition & Dietetics" and found 105 retracted articles from 1997 to 2023. Misconduct was the most common reason (87 of 105, 82.9%), and the mean time from publication to retraction was 1,488 days. Sánchez-Calabuig et al. (2026) searched PubMed for human-nutrition articles retracted between 2000 and 2025 and found 45. The leading causes were methodological or statistical errors (18.9%), lack of ethics approval (15.1%) and data-integrity breaches (11.3%); these shares appear to be of coded causes rather than of articles. The median time to retraction was 4.2 years. Of 1,155 citations in Scopus, 53% came after retraction. Neither study compared nutrition with other fields, so it is hard to tell whether these figures describe nutrition or retractions in general. Field-specific analyses using Retraction Watch data exist for diabetes (Parvin et al., 2026), cardiovascular medicine (Bhat et al., 2025) and infectious diseases (Zilberman et al., 2023), and for medicine as a whole (Okyay et al., 2025). I am not aware of one for nutrition and obesity with an all-field comparison, nor of a comparison of post-retraction citation of nutrition retractions with a matched set of other biomedical retractions.

Comparison matters because the database has changed. In September 2023 Crossref acquired the Retraction Watch database and made it openly available (Hendricks et al., 2023). Since October 2024 it has been published as a CSV file in a public repository, updated each working day (Rittman, 2024). Recent years in the database are dominated by mass retractions. In 2023, 11,132 of the 13,227 retractions in the database cited a paper mill, compromised peer review or computer-generated content (results file trends.json), and most of that year's retractions came from journals owned by Hindawi (Van Noorden, 2023). A field's figures can move with those events rather than with anything particular to the field. Across biomedicine, most retractions have been attributed to misconduct rather than error (Fang et al., 2012). Retracted papers also keep being cited. In biomedicine, only 5.4% of post-retraction citation contexts acknowledged the retraction (Hsiao & Schneider, 2021). A recent preprint census of Retraction Watch retractions with a PubMed identifier, retracted 1990–2023, found that 71.1% were cited in a later year, using citations from Europe PMC (Joseph, 2026).

This paper asks four questions. How many retractions in nutrition and obesity research does the open database hold, and how has that number changed? For what reasons, compared with the rest of the database? How long after publication? And are the papers still cited after retraction, compared with other retracted biomedical papers? Because "nutrition research" has no natural boundary, I define the field in several ways and report how much each answer depends on the definition. Because the rest of the database contains many conference papers retracted in bulk, I also compare journal articles with journal articles. I also planned a subgroup on GLP-1 receptor agonists and other anti-obesity drugs, to be analysed only if it held at least 30 retractions.

## 2. Methods

### 2.1 Data

The Retraction Watch database is compiled by Retraction Watch from scholarly databases, publisher websites, web searches and community reports (Crossref, n.d.), and has been owned and distributed by Crossref since September 2023 (Hendricks et al., 2023). I used the CSV file `retraction_watch.csv` from the public repository https://gitlab.com/crossref/retraction-watch-data at commit 827665a ("Retraction Watch data for 2026-10-28"; Crossref & Retraction Watch, 2026). The file had 73,444 rows and 20 documented fields (Crossref, n.d.), including subject codes, journal, publisher, author countries, the dates of the original article and the notice, DOIs, the nature of the notice and the reasons for it, drawn from a controlled vocabulary maintained by Retraction Watch. No licence is stated for the dataset in the repository or on the Crossref documentation page. Crossref describes the retraction data as freely available and asks users to cite the source (Rittman, 2025). This paper therefore shares code and aggregate results only, not record-level rows.

I kept the 68,002 rows whose notice was a retraction, excluding corrections, expressions of concern and reinstatements. I removed duplicate record identifiers, and where the same original DOI appeared more than once I kept the earliest notice (162 rows dropped). That left 67,840 retractions.

### 2.2 Defining the field

I used three rules, set before looking at the results.

- **S (subject code):** the record carries the Retraction Watch subject code "(BLS) Nutrition" or "(HSC) Nutrition".
- **J (journal title):** the journal or source title contains *nutri-*, *dietet-*, *diet*, *dietary*, *obes-*, *adipos-*, *appetite*, *eating*, *bariatric*, *vitamin* or *breastfeed-*. Titles naming animals, plants, soil, crops, mycorrhiza, nutrient uptake or use, livestock, poultry, aquaculture, veterinary science or feed are excluded.
- **K (article title):** the article title names a nutrition, diet or obesity topic (nutrition, nutrient, diet, dietary, obesity, overweight, body mass index, weight loss, weight gain, weight management, calories, energy intake, vitamins, micronutrients, malnutrition, undernutrition, stunting, breastfeeding, food intake, food insecurity, eating, appetite or ketogenic).

The primary definition is S or J, a classification by venue and by Retraction Watch's own coders. Article-title keywords (K) catch many papers on diet-induced obesity in animal models and on obesity as a clinical risk factor, which are not nutrition research in the usual sense, so K enters only the broad definition (S or J or K) and a sensitivity analysis. Further sensitivity analyses used each rule alone, both S and J, the primary definition plus food-science journals (titles containing *food*, *dairy* or *beverage*), and the primary definition without the publisher Hindawi, whose journals accounted for most retractions in 2023 (Van Noorden, 2023). The GLP-1 and anti-obesity-drug subgroup was defined by article-title terms (semaglutide, liraglutide, tirzepatide, exenatide, dulaglutide, lixisenatide, GLP-1, glucagon-like peptide, anti-obesity drug or medication, orlistat, phentermine, lorcaserin, naltrexone–bupropion, sibutramine, rimonabant) across the whole database.

### 2.3 Measures

**Counts over time** are by year of the retraction notice and by year of the original publication. **Reasons** were grouped into 14 non-exclusive groups from the Retraction Watch vocabulary (the mapping is in `code/common.py`): fabrication, falsification or manipulation; plagiarism; duplicate publication; paper mill; compromised peer review or rogue editor; computer-generated content; forged authorship or affiliation; image problems; data concerns or unreliable results; honest error; ethics approval or consent; authorship dispute or approval; publisher error; and limited or no information in the notice. A composite "any misconduct" flag combines the first seven groups. "Error, no misconduct flag" marks records with an error reason and none of the misconduct groups. Fifty of the 110 distinct reasons in the retraction records are not mapped to any group (Table S1). As a mapping sensitivity check, a broader misconduct composite adds four of them (Breach of Policy by Author, Taken from Dissertation/Thesis, and Misconduct by Third Party or by Company/Institution), and the unmapped reason "Concerns/Issues about Referencing/Attributions" is reported on its own. **Time to retraction** is the interval between the original publication date and the notice date in years, excluding records flagged "Date of Article and/or Notice Unknown" and negative intervals. **Countries** are counted per retraction: a retraction counts once for each country in its author affiliations.

The main comparison is between journal articles in the field and journal articles in the rest of the database, with conference papers excluded from both sides. The rest of the database holds 13,920 retracted conference papers (20.7%), 10,065 of them retracted in 2010–2019, against 28 in the field. I also report the comparison with all retractions, and a comparison against the rest of the biomedical part of the database, meaning retractions with at least one subject code in the Basic Life Sciences (BLS) or Health Sciences (HSC) groups and not in the field. For proportions I report differences in percentage points with Newcombe hybrid-score 95% confidence intervals (Newcombe, 1998). For differences in median time to retraction I report bootstrap 95% intervals (2,000 resamples, seed 20261029). The comparisons are descriptive. With tens of thousands of records in the comparison groups, small differences are statistically clear without being important.

### 2.4 Citations after retraction

For every primary-definition retraction with a DOI and a notice dated 2012–2023 (n = 432), I drew a comparison sample of other biomedical retractions with a DOI. The sample had two per field record, drawn at random within the same retraction year (n = 864; seed 20261029). I looked up both sets in OpenAlex (Priem et al., 2022) on 29 October 2026 and took the `counts_by_year` field, which gives the number of citing works indexed by OpenAlex by citing year and which, at the time of query, covered citing years from 2012 onwards. The OpenAlex flag `is_retracted` was also recorded. Post-retraction citations are citing works published in the calendar years after the retraction year, up to 2025 (the last complete year). I excluded the retraction year itself, because works published that year may have been written before the notice. Outcomes were the share cited at least once after the retraction year, citations per paper and per post-retraction year, and, for papers published in 2012 or later (whose citations are fully covered by `counts_by_year`), the share of 2012–2025 citations that fell after the retraction year. For the field-to-comparison difference in the share cited, and for the ratio of mean annual citation rates, I report bootstrap intervals (2,000 resamples, within groups but not within year strata).

These counts have firm limits. They count citing works, not the way the retracted paper was cited, so a citation that criticises or flags the paper counts the same as one that relies on it. They depend on OpenAlex's reference matching and coverage. They date citations by the citing work's publication year, not by when it was written. And they cover only papers with a DOI that OpenAlex could match.

### 2.5 Software, data and AI use

The analysis environment had no direct internet access. The CSV file was fetched with JavaScript in a Chrome browser tab from the GitLab API at the commit above (67,716,155 bytes; SHA-256 7020113802228518d52d8da3b64ed3a30c59e37e828d8377bce72a5cbad7c303). The selection, analysis and citation scripts were run unchanged in Pyodide 0.26.4 (Python 3.12.1, pandas 2.2.0, NumPy 1.26.4) in the same tab, after their SHA-256 hashes were checked against the files in the reproducibility package. OpenAlex was queried from the same tab. Only aggregate result files were copied back, and each was verified byte for byte against its in-browser SHA-256 hash. Figures and tables were produced locally with Python 3.13 and matplotlib. The study was carried out with the assistance of Claude (Anthropic; model claude-opus-5-5) in October 2026. Claude retrieved the data, wrote and ran the analysis code, searched the literature and drafted the text under the author's direction. Independent AI agents checked the numbers against the result files, re-ran the analysis and checked the citations; their corrections are included in this version. The author reviewed the work and takes full responsibility for it.

## 3. Results

### 3.1 How many, and when

Of the 67,840 retractions, 545 met the subject-code rule, 276 the journal-title rule and 105 both, giving 716 under the primary definition (1.1% of the database). Article-title keywords added 447 more, for 1,163 under the broad definition. Only 28 primary records were conference papers (3.9%), against 20.7% of the rest of the database (13,920 records). The journals with the most primary-definition retractions were a mix of general venues (BioMed Research International, 27; PLoS One, 19; Evidence-Based Complementary and Alternative Medicine, 14) and field-named journals (Food Science & Nutrition, 24; Romanian Journal of Diabetes, Nutrition and Metabolic Diseases, 15). Hindawi (105), Elsevier (104) and Wiley (81) were the leading publishers.

Retractions in the field rose from 27 in 2000–2009 to 263 in 2010–2019 and 420 from 2020 to 28 October 2026 (Figure 1a). The peak years were 2023 (100) and 2024 (119), followed by 70 in 2025 and 27 so far in 2026. In 2023, 71 of the 100 came from Hindawi, and 72 carried a paper-mill, peer-review or computer-generated-content reason. The field's share of all retractions stayed between about 0.5% and 2.6% a year from 2012 onwards (Figure 1b). It was 2.6% in 2017, 0.5% in 2022 and 0.8% in 2023, when mass retractions in other fields swelled the denominator, and 1.8% in 2024.

Only 28 retractions in the whole database had a GLP-1 or anti-obesity-drug term in the title, 3 of them in the primary definition and 7 in the broad one. This is below the threshold of 30 set in advance, so the subgroup is not analysed further. Of the 28, 15 carried a misconduct flag and 13 had at least one author from China.

### 3.2 Reasons

Among journal articles, some form of misconduct was cited in 57.4% of the field's retractions, against 69.7% in the rest of the database (difference −12.3 percentage points, 95% CI −16.0 to −8.6; Table 1, Figure 2). With conference papers left in, the gap nearly disappears (56.6% vs 59.0%; −2.4, −6.1 to +1.2), because only 18.0% of the 13,920 conference retractions in the rest of the database cite a misconduct reason (results file summary.json). Against the rest of the biomedical subjects the field's share was also lower (60.0%; −3.5, −7.2 to +0.1), and lower again when conference papers were excluded from both sides (62.9%; −5.4, −9.2 to −1.8; results file comparison.json). The broader misconduct mapping gave the same picture: 58.0% vs 70.1% among journal articles, and 57.4% vs 65.7% with all retractions (Table 1).

The kind of misconduct differed too. Among journal articles, paper mills (12.4% vs 20.9%), compromised peer review (24.1% vs 38.3%), computer-generated content (9.9% vs 16.7%) and image problems (10.5% vs 16.5%) were less common in the field. Fabrication, falsification or manipulation (9.4% vs 7.3%) and plagiarism (12.9% vs 10.6%) were slightly more common, and duplicate publication was similar (11.8% vs 11.1%). Concerns about referencing or attributions, a reason left unmapped in my grouping, were cited in 16.0% vs 25.2%.

Reasons outside misconduct were more frequent in the field. Among journal articles, errors without a misconduct flag accounted for 13.5% of retractions, against 8.7% in the rest of the database (difference +4.8 points, 95% CI +2.4 to +7.6). Ethics approval or consent problems were cited in 10.9% (vs 6.3%), and authorship disputes or lack of author approval in 18.2% (vs 13.5%). Data concerns or unreliable results were slightly less common (46.4% vs 50.3%). Notices with limited or no information were much rarer in the field when all retractions were compared (6.0% vs 18.3%), but this gap is due entirely to conference papers: among journal articles there was no difference (4.9% vs 4.2%; +0.8, −0.6 to +2.7).

The comparison changed over time (Table 1 covers all years; by-period results are in comparison.json). Among journal articles retracted in 2010–2019, misconduct was about as common in the field as elsewhere (59.5% vs 56.9%; +2.6, −3.6 to +8.5). Among those retracted in 2020–2026 it was much less common (56.3% vs 76.1%), as paper-mill (21.0% vs 29.9%) and peer-review (37.5% vs 52.6%) retractions grew faster in the rest of the database. Excluding Hindawi from both sides, misconduct was cited equally often (49.9% vs 50.9%), while paper-mill cases remained rarer in the field (2.5% vs 7.7%).

### 3.3 Time to retraction

Among journal articles, the median time from publication to retraction was 1.90 years in the field (interquartile range 0.97–4.84; n = 656 with valid dates) and 1.78 years in the rest of the database (1.00–3.67), a difference of 0.12 years (bootstrap 95% CI −0.10 to +0.36; Table 2). With all retractions the difference was larger (1.84 vs 1.48 years; 0.36, 0.17 to 0.57), but this comes from the fast retraction of conference papers in the comparison group: for notices dated 2010–2019, the rest of the database had a median of 0.71 years with all retractions and 2.03 years for journal articles. Against the rest of biomedicine there was no difference (1.84 vs 1.86 years; −0.02, −0.21 to +0.21), and none among journal articles (1.90 vs 1.97; −0.07, −0.30 to +0.18). Within 2020–2026 the medians were 1.76 and 1.69 years (1.83 and 1.76 among journal articles). The distribution had a longer tail in the field: 24.4% of the field's journal-article retractions came more than five years after publication, against 16.3% in the rest of the database. Excluding Hindawi from both sides, the field was slower (2.26 vs 1.65 years; 0.61, 0.28 to 1.06), because Hindawi's fast mass retractions dominate the 2023 comparison group.

By reason, retractions for fabrication, falsification or manipulation had the longest medians (5.53 years in the field, 4.28 elsewhere), followed by duplicate publication (3.43 and 3.20). Paper-mill and peer-review retractions came quickly and uniformly (medians 1.61 and 1.52 years in the field, with narrow interquartile ranges; Figure 3a). Errors without a misconduct flag were retracted after a median of 1.29 years in the field and 1.50 elsewhere.

### 3.4 Countries

Authors from 92 countries appeared in the field's retractions. China was named in 26.4% of them, against 54.9% in the rest of the database and 49.6% in the rest of biomedicine (26.5% vs 50.2% among journal articles). The United States was named in 18.2% (vs 9.1%), Iran in 8.7% (vs 2.9%) and Japan in 5.0% (vs 2.3%; Table 2). Among journal articles, the gap for China was 10.3% vs 20.4% for retractions dated 2010–2019 and 37.8% vs 63.5% for 2020–2026.

### 3.5 Sensitivity to the definition of the field

Several findings held under every definition (Table 3). Each definition had a larger share of errors without a misconduct flag than the rest of the database (12.5% to 21.9%, vs 7.2%, or 8.7% among journal articles), a smaller share of retractions with a Chinese author (10.5% to 33.5%, vs 54.9% or 50.2%) and a larger share with a US author (16.3% to 26.7%, vs 9.1% or 11.0%). Compared with all other retractions, the share citing any misconduct was never higher (33.3% to 58.5%, vs 58.9% to 59.0%). Compared with other journal articles, it was lower under every definition (34.3% to 59.6%, vs about 70%).

Other findings depended on the definition. Journals whose titles name nutrition, diet or obesity (rule J) had no paper-mill retractions at all, and only 6.2% cited compromised peer review. Their misconduct share was 43.8%. Where both rules applied (n = 105) the misconduct share was 33.3% and the error-only share 21.9%. The paper-mill and peer-review cases in the primary definition came almost entirely through the subject code, applied to articles in general journals. Removing Hindawi left 611 retractions, of which 2.5% were paper-mill and 12.4% peer-review cases. Time to retraction among journal articles differed from the rest by −0.09 to +0.14 years for the primary, subject-code, title-keyword, broad and food-science definitions. It was longer for records meeting both rules (2.78 vs 1.78 years), the primary definition without Hindawi (2.33) and the journal rule (2.23).

### 3.6 Citations after retraction

OpenAlex matched 425 of the 432 field papers and 853 of the 864 comparison papers, and flagged 99.1% and 99.3% of them as retracted (Table 4). In the field, 76.2% were cited by at least one work published after the retraction year, compared with 77.5% of the comparison sample (difference −1.3 points, 95% CI −6.1 to +3.4). Altogether the 425 field papers received 5,768 such citations up to 2025. The median paper received 3 post-retraction citations in both groups, and 37.4% of field papers received five or more.

The mean annual citation rate after retraction was higher in the field (2.15 vs 1.27 citing works per year; ratio 1.69, 95% CI 1.11 to 2.70), while the medians were close (0.54 vs 0.50). Neither period-specific ratio excluded 1 (Table 4). The higher mean reflects a minority of heavily cited papers. These papers were also more cited before retraction. In the year before the notice the field's papers averaged 4.19 citing works, against 2.82 in the comparison sample (Figure 3b). For papers published in 2012 or later, 37.1% of their 2012–2025 citations came after the retraction year in the field and 38.5% in the comparison sample. Citations fell after the notice in both groups but did not stop. Five years after the retraction year the field's papers still averaged 1.78 citing works per year (Figure 3b).

## 4. Discussion

### 4.1 Main findings

Nutrition and obesity research accounts for about 1% of the retractions in the open Retraction Watch database. Its retractions have risen in number, with the same 2023–2024 surge seen across the database. Among journal articles, retractions in the field cite misconduct less often than retractions elsewhere (57.4% vs 69.7%). The difference is largest for paper-mill, peer-review-manipulation and computer-generated-content cases. Errors, ethics-approval or consent problems and authorship disputes are more common. Whether the field looks "as bad as" the rest therefore depends on the comparison: with all retractions, including bulk-retracted conference papers, the misconduct shares are close (56.6% vs 59.0%). The paper-mill and peer-review retractions that the field does have come mainly from articles in general and mixed-subject journals that Retraction Watch coded as nutrition, especially Hindawi titles. Journals whose own titles name nutrition, diet or obesity had none. Time to retraction was similar to that of other journal articles and other biomedical retractions.

Once retracted, nutrition papers kept being cited about as often as other retracted biomedical papers. About three in four were cited again in a later year. A minority of heavily cited papers pushed the field's mean citation rate above the comparison's, but they were also more cited before retraction, so I do not read this as evidence that nutrition is worse at heeding retractions.

### 4.2 Comparison with earlier work

The counts here are larger than in earlier nutrition studies (716 under the primary definition, against 105 in Shamsi et al., 2025, and 45 in Sánchez-Calabuig et al., 2026), mainly because the field is defined more broadly and the data run to October 2026. The shares by reason are not directly comparable. Shamsi et al. reported misconduct in 87 of 105 Web of Science articles (82.9%), using reasons from the Retraction Watch database. Sánchez-Calabuig et al. coded the notices themselves into exclusive categories. My grouping is non-exclusive and uses the Retraction Watch vocabulary directly. The most comparable figure is the share of citations after retraction. Sánchez-Calabuig et al. found 53% of all Scopus citations to their 45 articles came after retraction. Here 37.1% of 2012–2025 citations came after the retraction year, for papers published from 2012 on. The windows, citation sources and inclusion rules differ. Both studies agree that retraction does not end citation.

The citation result is in line with biomedicine as a whole. Joseph (2026) found that 71.1% of retracted biomedical papers were cited in a later year. That figure comes from a different population (Retraction Watch retractions with a PubMed identifier, retracted 1990–2023) and a different citation source (Europe PMC), and the study is a preprint, so it is a rough benchmark for this paper's 76.2% rather than a direct comparison. Hsiao and Schneider (2021) showed that most post-retraction citation contexts did not mention the retraction. My counts cannot say how the citing works used the retracted nutrition papers. Avenell et al. (2019) showed, for retracted trials of vitamin, calcium and bone-drug treatments, that such citations can distort systematic reviews and guidelines.

### 4.3 Interpretation

Three readings of the reason profile are possible, and the data cannot separate them. First, nutrition and dietetics journals may have been less targeted by paper mills and peer-review manipulation than general open-access venues; the absence of such retractions in field-named journals is consistent with this. Second, the field may have been targeted as much but detected less; retractions record what was caught, not what happened. Third, the higher share of error, ethics and authorship reasons may reflect the field's research designs. Human trials and cohort studies need ethics approval and consent and often have many contributors, and errors in dietary assessment or analysis can be found and corrected by the authors. Fabrication cases had the longest medians (above five years in the field), which suggests that serious misconduct in nutrition trials can take a long time to come to light, as in the trials studied by Bolland et al. (2016) and Avenell et al. (2019). The overall time to retraction, however, was similar to that of other journal articles. This reading is an interpretation, not a finding.

### 4.4 Limitations

**Coverage.** The database records retractions Retraction Watch has found. Retractions that were never reported, and problems never retracted, are invisible. Coverage of recent months may lag. No database of retractions is complete (Sebo & Sebo, 2025; a related study by the same authors was later retracted, but the cited paper's coverage counts are its own).

**Definition of the field.** No definition of nutrition research is neutral. Subject codes are assigned by Retraction Watch staff and can be broad. Journal-title rules miss nutrition papers in general journals and include some off-topic papers in field-named journals. Title keywords pull in animal models and obesity as a risk factor. I report how each result changes with the definition (Table 3). The direction of the main differences held throughout, but their size did not.

**Comparison group.** The headline comparisons depend on what the field is compared with. Conference papers retracted in bulk make the rest of the database look less misconduct-heavy and faster to retract; Hindawi's mass retractions make it look faster. I report journal articles as the main comparison and show the alternatives (Tables 1 to 3).

**Reasons.** The reason vocabulary describes what notices say, not what was proven. Reasons overlap, and "investigation by journal" (cited in 307 of the field's 716 retractions, 42.9%, and 45.6% elsewhere) or "concerns about data" can hide misconduct that a notice did not name. My grouping into misconduct and error is one of several reasonable choices. Fifty reasons are unmapped (Table S1), including concerns about referencing or attributions (16.8% vs 22.4% with all retractions). The broader misconduct mapping widens the gap with all retractions (57.4% vs 65.7%) and leaves the journal-article comparison unchanged.

**Dates.** Many original publication dates are recorded as the first of a month or of a year, so times to retraction are precise to about a month.

**Denominator.** The comparison is among retractions. It says nothing about the retraction rate per published paper, which would need a count of all nutrition publications by year.

**Citations.** OpenAlex counts citing works, not how they cite. They depend on OpenAlex's reference matching, cover only papers with a matched DOI, and date citations by the citing work's publication year. Post-retraction windows differ by retraction year (2 to 13 calendar years). The comparison sample matches on retraction year only, not on journal, topic or pre-retraction citation level, and the bootstrap does not resample within years.

**Small subgroups.** The GLP-1 and anti-obesity-drug subgroup had 28 records and was not analysed. Early years have few records, so shares before 2008 are unstable.

**Record-level data.** The data have no stated licence, so the package does not include record-level rows. Anyone can rebuild them from the source with the code.

## 5. Conclusion

In the open Retraction Watch database, retractions of journal articles in nutrition and obesity research cite misconduct less often than retractions of other journal articles. They are much less often paper-mill or peer-review-manipulation cases and more often errors, ethics or consent problems and authorship disputes. Compared with all retractions, which include many bulk-retracted conference papers, the misconduct shares are similar. Time to retraction is similar to that of other journal articles, and after retraction the papers go on being cited at about the same rate as other retracted biomedical papers. How much of the field's profile is due to paper mills depends heavily on whether general journals are counted. For readers of nutrition evidence, the practical point is plain: about three in four retracted papers in this field were cited again after the retraction year, so systematic reviews and guidelines should check their sources against retraction data.

## Acknowledgements

The author thanks Retraction Watch and the Center for Scientific Integrity for compiling the database, Crossref for making it openly available, and the OpenAlex team for OpenAlex. Claude (Anthropic; model claude-opus-5-5) assisted with data retrieval, analysis code, literature search and drafting in October 2026, as described in §2.5. The author reviewed all outputs and is responsible for the content.

## Author contributions

P.K. conceived the study, directed the analysis, and reviewed and approved the manuscript.

## Financial support

This research received no specific grant from any funding agency, commercial or not-for-profit sector.

## Conflicts of interest

The author operates a restaurant, The Heritage Diner, in Mount Sinai, New York, and has no other competing interests.

## Research transparency and reproducibility

The Retraction Watch data are openly available from Crossref at https://gitlab.com/crossref/retraction-watch-data (commit 827665ab699e4a798060b95c40268de417b7f2e1). No licence is stated for them, so record-level rows are not redistributed. OpenAlex data are CC0. Code, aggregate result files and their SHA-256 hashes are in the reproducibility package linked from the article page. The package includes instructions for rebuilding the record list from the source.

## References

Avenell, A., Stewart, F., Grey, A., Gamble, G., & Bolland, M. (2019). An investigation into the impact and implications of published papers from retracted research: Systematic search of affected literature. *BMJ Open, 9*(10), e031909. https://doi.org/10.1136/bmjopen-2019-031909

Bhat, V., Kaushik, S., Kumar, A., Bellur, S., & Kalra, A. (2025). Retractions and withdrawals in clinical cardiovascular literature: Analysis of the Retraction Watch Database. *JACC: Advances, 4*(8), 101802. https://doi.org/10.1016/j.jacadv.2025.101802

Bolland, M. J., Avenell, A., Gamble, G. D., & Grey, A. (2016). Systematic review and statistical analysis of the integrity of 33 randomized controlled trials. *Neurology, 87*(23), 2391–2402. https://doi.org/10.1212/WNL.0000000000003387

Crossref. (n.d.). *Retraction Watch*. Crossref documentation. Retrieved October 28, 2026, from https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/

Crossref & Retraction Watch. (2026). *Retraction Watch data* (commit 827665ab699e4a798060b95c40268de417b7f2e1, "Retraction Watch data for 2026-10-28") [Data set]. GitLab. https://gitlab.com/crossref/retraction-watch-data

Fang, F. C., Steen, R. G., & Casadevall, A. (2012). Misconduct accounts for the majority of retracted scientific publications. *Proceedings of the National Academy of Sciences, 109*(42), 17028–17033. https://doi.org/10.1073/pnas.1212247109

Hendricks, G., Lammey, R., Ofiesh, L., Bilder, G., & Pentz, E. (2023, September 12). *News: Crossref and Retraction Watch*. Crossref Blog. https://doi.org/10.13003/c23rw1d9

Hsiao, T.-K., & Schneider, J. (2021). Continued use of retracted papers: Temporal trends in citations and (lack of) awareness of retractions shown in citation contexts in biomedicine. *Quantitative Science Studies, 2*(4), 1144–1169. https://doi.org/10.1162/qss_a_00155

Joseph, S. (2026). *Retracted, still cited as support: A census of post-retraction citations to 22,483 retracted biomedical papers* [Preprint]. MetaArXiv. https://doi.org/10.31222/osf.io/uwqxa_v1

Newcombe, R. G. (1998). Interval estimation for the difference between independent proportions: Comparison of eleven methods. *Statistics in Medicine, 17*(8), 873–890. https://doi.org/10.1002/(SICI)1097-0258(19980430)17:8<873::AID-SIM779>3.0.CO;2-I

Okyay, R. A., Kocyigit, B. F., Qumar, A. B., Yessirkepov, M., & Sumbul, H. E. (2025). Fifty years of retracted medical publications from 1975 to 2024: A comprehensive analysis of trends, reasons, and countries using the Retraction Watch Database. *Journal of Korean Medical Science, 40*(46), e300. https://doi.org/10.3346/jkms.2025.40.e300

Parvin, S., Lotfi, M., & Nouri, M. (2026). Analysis of retracted publications in the diabetes literature. *Medical Journal of the Islamic Republic of Iran, 40*, 20. https://doi.org/10.47176/mjiri.40.20

Priem, J., Piwowar, H., & Orr, R. (2022). *OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2205.01833

Rittman, M. [mrittman]. (2024, October 11). *Changes to delivery of Retraction Watch metadata* [Online forum post]. Crossref Community Forum. https://community.crossref.org/t/changes-to-delivery-of-retraction-watch-metadata/12368

Rittman, M. (2025, January 29). *Retraction Watch retractions now in the Crossref API*. Crossref Blog. https://doi.org/10.13003/692016

Sánchez-Calabuig, M. A., Martínez-Roldán, C., Izcara, S., Pedauyé-Rueda, B., Lozano-Estevan, M. del C., Hervás-Pérez, J. P., & Herrera-Peco, I. (2026). When nutrition science fails: A bibliometric analysis of retracted diet-related articles (2000–2025). *Nutrition and Health*. Advance online publication. https://doi.org/10.1177/02601060261441168

Sebo, P., & Sebo, M. (2025). Comparing the performance of Retraction Watch Database, PubMed, and Web of Science in identifying retracted publications in medicine. *Accountability in Research, 33*(2), 2484555. https://doi.org/10.1080/08989621.2025.2484555

Shamsi, A., Emamat, H., Wang, T., & Safaei, Z. (2025). Trends, reasons, and implications of retracted articles in nutrition and dietetics from 1997 to 2023 in the Web of Science: A bibliometric study. *Science Editing, 12*(2), 131–137. https://doi.org/10.6087/kcse.372

Van Noorden, R. (2023). More than 10,000 research papers were retracted in 2023 — a new record. *Nature, 624*(7992), 479–481. https://doi.org/10.1038/d41586-023-03974-8

Zilberman, T., Margalit, I., Yahav, D., & Tau, N. (2023). Retracted publications in infectious diseases and clinical microbiology literature: An analysis using the Retraction Watch database. *Clinical Microbiology and Infection, 29*(11), 1454.e1–1454.e3. https://doi.org/10.1016/j.cmi.2023.07.022

## Tables

**Table 1.** Reasons for retraction: nutrition and obesity research (primary definition) compared with the rest of the Retraction Watch database, for journal articles only (conference papers excluded from both sides; the main comparison), for all retractions, and against the rest of the biomedical subjects (all retractions). JA, journal articles; All, all retractions; Biomed. rest, rest of the biomedical subjects; group sizes in brackets. Data to 28 October 2026. A retraction can carry several reasons, so columns do not sum to 100. Differences are percentage points with Newcombe 95% confidence intervals. The last two rows are mapping sensitivity checks: a broader misconduct composite that adds Breach of Policy by Author, Taken from Dissertation/Thesis and Misconduct by Third Party or by Company/Institution, and the unmapped reason Concerns/Issues about Referencing/Attributions.

| Reason group | JA field, % (688) | JA rest, % (53,204) | JA difference (95% CI) | All field, % (716) | All rest, % (67,124) | All difference (95% CI) | Biomed. rest, % (33,877) | Difference vs all field (95% CI) |
|:-------------|------:|-------:|--------:|------:|-------:|--------:|-------:|--------:|
| Any misconduct (composite) | 57.4 (395) | 69.7 | -12.3 (-16.0 to -8.6) | 56.6 (405) | 59.0 | -2.4 (-6.1 to +1.2) | 60.0 | -3.5 (-7.2 to +0.1) |
| Fabrication, falsification or manipulation | 9.4 (65) | 7.3 | +2.2 (+0.2 to +4.6) | 9.4 (67) | 5.9 | +3.4 (+1.5 to +5.8) | 9.5 | -0.2 (-2.1 to +2.2) |
| Plagiarism | 12.9 (89) | 10.6 | +2.4 (+0.0 to +5.1) | 12.4 (89) | 9.3 | +3.1 (+0.9 to +5.7) | 9.0 | +3.5 (+1.2 to +6.1) |
| Duplicate publication | 11.8 (81) | 11.1 | +0.7 (-1.5 to +3.3) | 11.5 (82) | 8.9 | +2.5 (+0.4 to +5.1) | 10.5 | +0.9 (-1.2 to +3.5) |
| Paper mill | 12.4 (85) | 20.9 | -8.6 (-10.8 to -5.9) | 12.0 (86) | 17.3 | -5.3 (-7.5 to -2.7) | 18.2 | -6.2 (-8.4 to -3.6) |
| Compromised peer review or rogue editor | 24.1 (166) | 38.3 | -14.1 (-17.2 to -10.8) | 24.2 (173) | 32.6 | -8.5 (-11.5 to -5.2) | 27.0 | -2.8 (-5.8 to +0.5) |
| Computer-generated content | 9.9 (68) | 16.7 | -6.8 (-8.8 to -4.3) | 9.5 (68) | 14.0 | -4.5 (-6.5 to -2.1) | 10.4 | -0.9 (-2.9 to +1.4) |
| Forged authorship or affiliation | 2.3 (16) | 1.7 | +0.6 (-0.3 to +2.0) | 2.2 (16) | 1.5 | +0.8 (-0.1 to +2.1) | 1.8 | +0.4 (-0.5 to +1.8) |
| Image problems | 10.5 (72) | 16.5 | -6.1 (-8.2 to -3.6) | 10.1 (72) | 13.2 | -3.1 (-5.1 to -0.7) | 22.9 | -12.9 (-14.9 to -10.4) |
| Data concerns or unreliable results | 46.4 (319) | 50.3 | -4.0 (-7.7 to -0.2) | 45.4 (325) | 40.5 | +4.9 (+1.2 to +8.6) | 47.8 | -2.4 (-6.0 to +1.3) |
| Honest error | 15.3 (105) | 10.6 | +4.7 (+2.2 to +7.6) | 14.8 (106) | 8.7 | +6.1 (+3.7 to +8.9) | 12.3 | +2.5 (+0.1 to +5.3) |
| Error, no misconduct flag | 13.5 (93) | 8.7 | +4.8 (+2.4 to +7.6) | 13.1 (94) | 7.2 | +5.9 (+3.6 to +8.6) | 10.1 | +3.0 (+0.7 to +5.7) |
| Ethics approval or consent | 10.9 (75) | 6.3 | +4.6 (+2.4 to +7.1) | 10.5 (75) | 5.0 | +5.4 (+3.4 to +7.9) | 8.0 | +2.5 (+0.4 to +5.0) |
| Authorship dispute or approval | 18.2 (125) | 13.5 | +4.7 (+2.0 to +7.8) | 17.7 (127) | 10.9 | +6.9 (+4.2 to +9.8) | 12.6 | +5.2 (+2.5 to +8.1) |
| Publisher error | 3.9 (27) | 3.2 | +0.7 (-0.5 to +2.4) | 3.9 (28) | 2.8 | +1.1 (-0.1 to +2.8) | 3.0 | +0.9 (-0.3 to +2.6) |
| Limited or no information in notice | 4.9 (34) | 4.2 | +0.8 (-0.6 to +2.7) | 6.0 (43) | 18.3 | -12.3 (-13.9 to -10.3) | 8.2 | -2.2 (-3.7 to -0.2) |
| *Any misconduct, broader mapping* | 58.0 (399) | 70.1 | -12.1 (-15.8 to -8.5) | 57.4 (411) | 65.7 | -8.3 (-12.0 to -4.8) | 61.8 | -4.4 (-8.1 to -0.8) |
| *Concerns about referencing or attributions (unmapped)* | 16.0 (110) | 25.2 | -9.2 (-11.8 to -6.2) | 16.8 (120) | 22.4 | -5.6 (-8.2 to -2.7) | 17.3 | -0.6 (-3.1 to +2.4) |

**Table 2.** Time from publication to retraction (years; median and interquartile range), by period of the retraction notice, for all retractions and for journal articles only (conference papers excluded from both sides), and by reason (all retractions), and the countries most often named in author affiliations (share of retractions with at least one author from the country). Records with an unknown article or notice date are excluded from the timing rows.

| Row | Nutrition and obesity | n | Rest of database | n |
|:--|--:|--:|--:|--:|
| All retractions | 1.84 (0.91–4.75) | 676 | 1.48 (0.67–3.14) | 60,246 |
| Journal articles only (both sides) | 1.90 (0.97–4.84) | 656 | 1.78 (1.00–3.67) | 50,424 |
| All retractions, against the rest of biomedical subjects | 1.84 (0.91–4.75) | 676 | 1.86 (0.94–4.23) | 31,798 |
| Retracted up to 2009 | 1.25 (0.41–3.58) | 29 | 1.25 (0.46–2.75) | 2,209 |
| Retracted up to 2009, journal articles only | 1.15 (0.38–3.18) | 27 | 1.32 (0.50–2.83) | 2,085 |
| Retracted 2010–2019 | 1.95 (0.65–6.10) | 252 | 0.71 (0.15–3.06) | 19,765 |
| Retracted 2010–2019, journal articles only | 2.00 (0.71–6.33) | 243 | 2.03 (0.67–4.54) | 12,639 |
| Retracted 2020–2026 | 1.76 (1.07–4.32) | 395 | 1.69 (1.05–3.18) | 38,272 |
| Retracted 2020–2026, journal articles only | 1.83 (1.10–4.39) | 386 | 1.76 (1.10–3.32) | 35,700 |
| Fabrication, falsification or manipulation | 5.53 (3.22–11.70) | 64 | 4.28 (2.00–8.56) | 3,792 |
| Duplicate publication | 3.43 (1.07–9.93) | 80 | 3.20 (1.22–6.20) | 5,768 |
| Plagiarism | 1.94 (0.58–5.00) | 85 | 2.34 (0.88–4.31) | 5,687 |
| Paper mill | 1.61 (1.31–1.92) | 86 | 1.61 (1.23–2.32) | 11,562 |
| Compromised peer review or rogue editor | 1.52 (1.10–2.15) | 165 | 1.45 (1.03–2.10) | 21,268 |
| Error, no misconduct flag | 1.29 (0.58–2.85) | 92 | 1.50 (0.60–3.32) | 4,609 |
| *Countries (any author), %* | | | | |
| China | 26.4 | 189 | 54.9 | |
| United States | 18.2 | 130 | 9.1 | |
| India | 9.1 | 65 | 9.3 | |
| Iran | 8.7 | 62 | 2.9 | |
| Japan | 5.0 | 36 | 2.3 | |
| United Kingdom | 4.7 | 34 | 2.6 | |
| Pakistan | 4.7 | 34 | 2.4 | |
| Saudi Arabia | 4.3 | 31 | 3.5 | |
| South Korea | 3.9 | 28 | 2.1 | |
| Italy | 3.5 | 25 | 1.5 | |

**Table 3.** Sensitivity of the main comparisons to the definition of the field. Each definition is compared with all other retractions in the database; the last two columns repeat the misconduct and timing comparisons with conference papers excluded from both sides. In the row for the primary definition without conference papers, all columns exclude conference papers from both sides. S: Retraction Watch subject code (BLS) or (HSC) Nutrition; J: journal title names nutrition, diet, obesity, eating, appetite, vitamins or bariatric surgery (animal, plant, soil and feed journals excluded); K: article title names a nutrition, diet or obesity topic; food-science journals: title contains food, dairy or beverage. Columns (percentages unless stated): Misc., any misconduct; Mill, paper mill; Peer rev., compromised peer review or rogue editor; Error only, error with no misconduct flag; 2023+, retracted 2023 or later; China and US, at least one author from the country; Years, median years from publication to retraction; JA, journal articles only, conference papers excluded from both sides.

| Definition | n | Misc. | Mill | Peer rev. | Error only | 2023+ | China | US | Years (rest) | JA misc. (rest) | JA years (rest) |
|:------------------|------:|-----:|-----:|-----:|-----:|------:|-----:|-----:|-----:|-----:|-----:|
| Primary (S or J) | 716 | 56.6 | 12.0 | 24.2 | 13.1 | 44.1 | 26.4 | 18.2 | 1.84 (1.48) | 57.4 (69.7) | 1.90 (1.78) |
| S: subject-code rule | 545 | 58.5 | 15.8 | 29.0 | 12.8 | 48.3 | 30.3 | 18.5 | 1.74 (1.49) | 59.6 (69.6) | 1.82 (1.78) |
| J: journal-title rule | 276 | 43.8 | 0.0 | 6.2 | 17.0 | 34.1 | 12.7 | 20.7 | 2.21 (1.49) | 44.4 (69.6) | 2.23 (1.78) |
| S and J (both rules) | 105 | 33.3 | 0.0 | 1.9 | 21.9 | 39.0 | 10.5 | 26.7 | 2.67 (1.49) | 34.3 (69.6) | 2.78 (1.78) |
| K: article-title rule | 803 | 55.4 | 11.0 | 26.3 | 12.5 | 44.6 | 33.5 | 17.4 | 1.81 (1.48) | 57.6 (69.7) | 1.90 (1.78) |
| Broad (S or J or K) | 1163 | 56.0 | 11.6 | 25.5 | 12.7 | 43.4 | 30.0 | 17.7 | 1.85 (1.48) | 57.6 (69.8) | 1.92 (1.78) |
| Primary + food-science journals | 861 | 56.9 | 13.5 | 24.5 | 12.5 | 42.2 | 24.9 | 16.3 | 1.68 (1.49) | 57.6 (69.7) | 1.69 (1.79) |
| Primary, journal articles (both sides) | 688 | 57.4 | 12.4 | 24.1 | 13.5 | 44.5 | 26.5 | 18.5 | 1.90 (1.78) | 57.4 (69.7) | 1.90 (1.78) |
| Primary, excluding Hindawi | 611 | 49.9 | 2.5 | 12.4 | 14.7 | 36.0 | 18.7 | 20.9 | 2.26 (1.48) | 50.6 (69.7) | 2.33 (1.78) |
| *Rest of database (primary)* | 67,124 | 59.0 | 17.3 | 32.6 | 7.2 | 41.2 | 54.9 | 9.1 | | | |

**Table 4.** Citations after retraction, OpenAlex. Field: primary-definition retractions with a DOI retracted 2012–2023 (found in OpenAlex: 425 of 432); comparison: random sample of other biomedical retractions with a DOI, two per field record within each retraction year (found: 853 of 864). Post-retraction citations are citing works published in the calendar years after the retraction year, up to 2025. Counts are citing works indexed by OpenAlex, not readings of how the paper was cited.

| Measure | Nutrition and obesity | Comparison | Difference or ratio (95% CI) |
|:--|--:|--:|--:|
| Cited at least once after the retraction year, % | 76.2 | 77.5 | -1.3 (-6.1 to +3.4) |
| Cited 5 or more times after the retraction year, % | 37.4 | 35.8 | |
| Post-retraction citations, median per paper | 3 | 3 | |
| Post-retraction citations, mean per paper | 13.6 | 7.4 | |
| Post-retraction citations per year, mean | 2.15 | 1.27 | ratio 1.69 (1.11 to 2.70) |
| Post-retraction citations per year, median | 0.54 | 0.50 | |
| Total post-retraction citations | 5,768 | 6,347 | |
| Share of 2012–2025 citations after the retraction year, % (papers published 2012 or later; n = 338, 686) | 37.1 | 38.5 | |
| Flagged as retracted in OpenAlex, % | 99.1 | 99.3 | -0.2 (-1.4 to +0.8) |
| Retracted 2012–2017: cited after retraction year, % (n = 138, 276) | 87.7 | 80.4 | |
| Retracted 2012–2017: citations per year, mean | 1.83 | 1.16 | ratio 1.58 (0.97 to 2.49) |
| Retracted 2018–2023: cited after retraction year, % (n = 287, 577) | 70.7 | 76.1 | |
| Retracted 2018–2023: citations per year, mean | 2.30 | 1.32 | ratio 1.74 (0.96 to 3.11) |

**Table S1.** Retraction Watch reasons not mapped to any reason group in this analysis (50 of the 110 distinct reasons in the retraction records), with the number of retractions citing each: nutrition and obesity (primary definition, n = 716) and rest of the database (n = 67,124). Reasons marked * are added to the misconduct composite in the broader mapping (Table 1, last rows). Reasons cited by fewer than 20 records in total are omitted (full list in results/unmapped_reasons.json).

| Reason | Nutrition and obesity | Rest of database |
|:--|--:|--:|
| Investigation by Journal/Publisher | 307 (42.9%) | 30,598 (45.6%) |
| Investigation by Third Party | 158 (22.1%) | 17,803 (26.5%) |
| Concerns/Issues about Referencing/Attributions | 120 (16.8%) | 15,040 (22.4%) |
| Concerns/Issues about Results and/or Conclusions | 108 (15.1%) | 9,294 (13.8%) |
| Date of Article and/or Notice Unknown | 40 (5.6%) | 6,877 (10.2%) |
| Breach of Policy by Author * | 10 (1.4%) | 4,777 (7.1%) |
| Removed | 39 (5.4%) | 3,951 (5.9%) |
| Author Unresponsive | 16 (2.2%) | 3,493 (5.2%) |
| Investigation by Company/Institution | 67 (9.4%) | 3,210 (4.8%) |
| Upgrade/Update of Prior Notice(s) | 52 (7.3%) | 2,435 (3.6%) |
| Concerns/Issues about Third Party Involvement | 4 (0.6%) | 1,832 (2.7%) |
| Concerns/Issues about Article | 11 (1.5%) | 1,807 (2.7%) |
| Retract and Replace | 14 (2.0%) | 913 (1.4%) |
| Conflict of Interest | 19 (2.7%) | 800 (1.2%) |
| Objections by Third Party | 14 (2.0%) | 719 (1.1%) |
| Copyright Claims | 5 (0.7%) | 688 (1.0%) |
| Withdrawn to Publish in Different Journal | 4 (0.6%) | 492 (0.7%) |
| Taken from Dissertation/Thesis * | 5 (0.7%) | 368 (0.5%) |
| Withdrawn as Out of Date | 5 (0.7%) | 358 (0.5%) |
| Concerns/Issues about Methods | 11 (1.5%) | 257 (0.4%) |
| Cites Retracted Work | 5 (0.7%) | 202 (0.3%) |
| Notice - Unable to Access via current resources | 4 (0.6%) | 178 (0.3%) |
| Doing the Right Thing | 3 (0.4%) | 133 (0.2%) |
| Legal Reasons and/or Threats | 3 (0.4%) | 111 (0.2%) |
| Miscommunication with/by Author | 1 (0.1%) | 101 (0.2%) |
| Complaints about Author | 2 (0.3%) | 98 (0.1%) |
| Bias Issues or Lack of Balance | 5 (0.7%) | 94 (0.1%) |
| Publishing Ban | 1 (0.1%) | 85 (0.1%) |
| Temporary Removal | 5 (0.7%) | 73 (0.1%) |
| Criminal Proceedings | 2 (0.3%) | 73 (0.1%) |
| Misconduct by Third Party * | 1 (0.1%) | 48 (0.1%) |
| Transfer of Copyright and/or Ownership | 0 (0.0%) | 43 (0.1%) |
| Error by Third Party | 1 (0.1%) | 42 (0.1%) |
| Not Presented at Conference | 1 (0.1%) | 39 (0.1%) |
| Ethical Violations by Company/Institution/Third Party | 3 (0.4%) | 26 (0.0%) |
| Civil Proceedings | 1 (0.1%) | 27 (0.0%) |
| Objections by Company/Institution | 2 (0.3%) | 26 (0.0%) |
| Updated to Retraction | 0 (0.0%) | 22 (0.0%) |
| Misconduct by Company/Institution * | 0 (0.0%) | 8 (0.0%) |

## Figures

![**Figure 1.** Retractions in nutrition and obesity research by year of the retraction notice, 2000 to 28 October 2026. (a) Primary definition (subject code or journal title), split by whether the notice cites a paper mill, compromised peer review or computer-generated content; the line shows the broad definition, which adds article-title keywords. The 2026 bar covers about ten months. (b) Primary-definition retractions as a share of all retractions and of retractions with a biomedical (BLS or HSC) subject code, 2008–2026. Source: Crossref Retraction Watch data, commit 827665a.](fig1_trends.png)

![**Figure 2.** Share of retractions citing selected reason groups (12 of the 16 rows in Table 1): nutrition and obesity research (primary definition, all retractions, n = 716), the rest of the database (all retractions, n = 67,124; journal articles only, n = 53,204) and the rest of the biomedical subjects (n = 33,877). Reasons overlap. All groups, the journal-article comparison for the field and confidence intervals are in Table 1.](fig2_reasons.png)

![**Figure 3.** (a) Years from publication to retraction, median and interquartile range, by reason group, for nutrition and obesity research and the rest of the database. (b) Mean number of citing works per paper per year, by years since the retraction year, for nutrition and obesity retractions with a DOI retracted 2012–2023 (n = 425) and a random sample of other biomedical retractions matched on retraction year (n = 853). OpenAlex counts by citing year, 2012–2025; points based on fewer than 100 papers are omitted, and the papers contributing to each point differ by year since retraction.](fig3_time_citations.png)
