---
title: "\"Same active ingredient\": what FDA warning letters allege about compounded GLP-1 sellers"
subtitle: "A systematic content analysis of public FDA warning letters on compounded and unapproved semaglutide and tirzepatide, 2023–2026"
---

**Peter Kalafatis**

Independent researcher, x9m8.com, New York, NY, USA. Correspondence: x9m8x7@gmail.com

**Preprint, not peer reviewed.** Version 1, October 2026.

## Abstract

After the US shortages of semaglutide and tirzepatide ended in 2024–2025, the Food and Drug Administration (FDA) turned to warning letters to police compounded and unapproved versions. I analysed every letter returned by full-text searches of FDA's public warning-letter index for these drugs and related terms. The searches, run on 21 October 2026, returned 163 letters; 154 met inclusion criteria after excluding five letters to the brand-name manufacturers and four in which the drugs were incidental. Each letter was coded twice, by an AI-written rule-based coder and by an AI reading pass, against a written codebook; median Cohen's κ across 22 codes was 0.93, and disagreements were adjudicated by re-reading. The letters were issued in bursts: 110 (71%) were dated on three days, 9 September 2025, 20 February 2026 and 8 June 2026. Letters to the 109 telehealth platforms, clinics and med spas all cited false or misleading advertising of compounded drugs; FDA cited claims of sameness with a branded drug (for example, "same active ingredient as") in 75 of them and, from February 2026, labels presenting the seller as the compounder (51 letters). Letters to online pharmacies, research-peptide sellers, compounders and API suppliers instead alleged unapproved new drugs, sale without a prescription, CGMP and sterility failures, and retatrutide or other unapproved incretins (16 of these letters; 22 letters overall). Letter counts describe FDA's enforcement choices, not the size or behaviour of the market, and every finding is an FDA allegation rather than an adjudicated violation.

**Keywords:** semaglutide; tirzepatide; compounding; FDA warning letters; drug advertising; telehealth; content analysis; drug regulation; GLP-1 receptor agonists

**Social media summary:** 154 FDA warning letters on compounded GLP-1s: most cite telehealth sellers' "same active ingredient" claims and labels.

## 1. Introduction

Semaglutide and tirzepatide were on FDA's drug shortage list from 2022, and while they were listed, pharmacies and outsourcing facilities could compound copies under sections 503A and 503B of the Federal Food, Drug, and Cosmetic Act (FDCA). FDA declared the tirzepatide injection shortage resolved on 2 October 2024 and reaffirmed that decision on 19 December 2024; it declared the semaglutide injection shortage resolved on 21 February 2025 (FDA, 2026a). The agency set grace periods after which it would no longer refrain from acting against compounders whose products depended on the shortage. For 503B outsourcing facilities these ended on 19 March 2025 (tirzepatide) and 22 May 2025 (semaglutide). For 503A pharmacies FDA announced 18 February and 22 April 2025, later extended to those dates or the date of the district court's ruling on a preliminary injunction, whichever was later; the courts denied injunctions on 5 March 2025 (tirzepatide) and 24 April 2025 (semaglutide), after which FDA said its 503A discretion had ended (FDA, 2026a).

A large market had grown in the meantime, much of it sold online. In a review of 79 websites selling compounded GLP-1 receptor agonists in July–September 2024, Chetty et al. (2025) found that 36.7% stated or implied the products were FDA approved, 8.9% called them generic and 63.3% used a phrase such as "same active ingredients as [brand name]". Commentators raised concerns about marketing and safety (Mattingly & Conti, 2025; Donohue, 2025), and case reports and pharmacovigilance studies described dosing errors and other harms with compounded products (Lambson et al., 2023; McCall et al., 2026). Semaglutide vials test-bought from illegal online pharmacies were judged probably substandard or falsified (Ashraf et al., 2024). After the shortages ended, a secret-shopper study of 75 clinics and med spas in two states (August–October 2025) found compounded products still offered, some supplied by facilities not licensed for sterile compounding (DiStefano et al., 2026).

FDA's warning letters are the agency's most visible response. FDA describes a warning letter as "informal and advisory" and does not consider it final agency action (FDA, 2024): it tells a firm that FDA considers it to be in violation of the law and gives it a chance to respond, but it is not a court finding. Letters are posted publicly, and content analyses of them have been used to describe compliance problems in compounding pharmacies (Dmour, 2023), online direct-to-consumer promotion (Kim, 2015, who also included untitled letters) and data integrity (Rogers et al., 2020); FDA warnings and warning letters have also been used as data sources in studies of adulterated dietary supplements (Tucker et al., 2018; Cohen et al., 2022). I am not aware of a systematic content analysis of the warning letters on compounded and unapproved semaglutide and tirzepatide.

This paper asks three descriptive questions. Which statutory violations and marketing claims did FDA cite in these letters? How did they differ by the type of seller? And how were the letters distributed in time relative to the end of the shortages? Because FDA chooses whom to warn and when, the analysis describes FDA's enforcement, not the market it regulates.

## 2. Methods

### 2.1 Corpus

The sampling frame was FDA's warning-letter index, the database behind the agency's Warning Letters page (FDA, 2026c), which covers letters posted since 2021. On 21 October 2026 (US Eastern time; 01:43–01:45 UTC on 22 October) I queried the index's JSON source (`view_name=warning_letter_solr_index`) from a browser session on fda.gov with full-text searches for semaglutide, tirzepatide, retatrutide, Ozempic, Wegovy, Mounjaro, Zepbound, GLP-1, liraglutide, cagrilintide and incretin, and retrieved the HTML page of every letter returned. The snapshot (query results and the article section of each letter page) was frozen with a SHA-256 hash, and the plain text of each letter was hashed separately. The index records issue date, posting date, issuing office, FDA's subject line and links to any response or close-out letter.

A letter was included if FDA alleged a violation involving a semaglutide-, tirzepatide- or other incretin-containing product that the recipient sold, marketed, compounded, repackaged, manufactured or supplied. Letters to the holders of the approved brands (Novo Nordisk and Eli Lilly) about their own products were excluded, as were letters in which a GLP-1 drug was incidental (for example, mentioned only as a clinical-trial exclusion criterion) or in which no incretin ingredient was attributed to the product (for example, a dietary supplement or oral drops marketed with "GLP-1" in the name). Duplicate postings were to be removed; none were found. A product attributed to the recipient counted even if named once (one included letter lists a semaglutide lot only in a disposition table). Amendments to the codebook made after coding are listed in the package.

### 2.2 Codebook

The codebook (in the reproducibility package) was written before the corpus was coded. It defines one seller type per letter, assigned hierarchically: 503B outsourcing facility; 503A compounding pharmacy; telehealth platform; research-chemical seller (products labelled for research use or not for human consumption); online pharmacy or marketplace; clinic or med spa; active pharmaceutical ingredient (API) supplier; other. It defines 11 violation codes anchored to the FDCA provisions cited (for example, section 505(a) unapproved new drug; 502(a) false or misleading labelling; 502(bb) false or misleading advertising or promotion of a compounded drug; 502(f)(1) inadequate directions for use; 503(b) prescription requirement; CGMP or insanitary conditions under 501(a)(2)(B) and 501(a)(2)(A); sterility assurance; failure to meet the conditions of 503A or 503B; salt forms; retatrutide or other unapproved incretins), seven claim codes (claims of sameness with a branded drug, "generic", FDA approval, firm-branded products, research-use labelling, sale without prescription and use of brand names) and four context codes. Codes are binary and apply at the letter level: a code is present if the letter alleges or cites it, whichever product it concerns.

### 2.3 Coding and reliability

Coding was done in two independent passes. Pass 1 is a deterministic rule-based coder: regular expressions applied to the letter text, FDA's subject line and the company name. It was written before pass 2 began and was not run until pass 2 was finished. Its SHA-256 hash, with the codebook's, was recorded in a file written at the end of pass 2 together with the hash of the pass-2 log, so the package shows that neither file changed after coding but cannot itself prove that the rules were fixed before reading. Pass 2 was a reading of every letter by the coder (the AI model described in §2.6), recording codes and a short justification for each letter. To make full reading feasible, sentences repeated verbatim in four or more letters were shown once in a legend and referenced by a tag in each letter; all other text was read in full. Interpretive conventions that arose during reading (for example, that FDA's boilerplate sentence "Your claims imply that your products are the same as an FDA-approved product when they are not" does not by itself establish a quoted sameness claim) were written into the coding log at the point they were adopted, and earlier letters were recoded where a convention changed their code.

Agreement between passes was measured over all 163 retrieved letters as percent agreement and Cohen's κ (Cohen, 1960) for eligibility, seller type and each code. Every disagreement was then adjudicated by re-reading the passage matched by the rule and the surrounding letter text; decisions and reasons are logged. After an independent audit (also by an AI model), the shortage code was applied consistently to six letters and one sterility code resting only on water-system endotoxin control was removed; these post-audit changes are logged. Both passes and the adjudication were carried out by the same AI system; no human coder took part, so the two passes are independent instruments but not independent judges.

### 2.4 Outcomes and analysis

The primary outcomes are the frequencies of each code among included letters, with Wilson 95% confidence intervals, overall and by seller type. The secondary outcome is the distribution of letters over time, by issue date, with the shortage-resolution dates and grace-period deadlines marked as events. Because most letters fall on a few dates chosen by FDA, I did not fit an interrupted time series or any before–after test: a change in letter counts would measure FDA's scheduling, not a change in the market. I report the three letter batches that shared an issue date with a common template and compare the claims cited in each, the lag between issue and posting, and any close-out letters shown in the index. As a side series, I retrieved all openFDA drug recall (enforcement) records whose product description mentions semaglutide, tirzepatide or retatrutide (openFDA, 2026), deduplicated by recall number. These records include recalls of approved branded products as well as compounded ones.

### 2.5 Responsible reporting

Every finding is reported as FDA's allegation. A warning letter is not an adjudication; firms may have disputed the allegations, corrected the problems or closed the matter after the letter, and the index shows only some of these outcomes. Firms are named in the text only if they are large public companies (Novo Nordisk, Eli Lilly and Hims & Hers Health); all other results are aggregates. The open dataset lists recipients because the letters are public records, with the letter URL, date and hash, and with a note that each entry records an allegation.

### 2.6 Software, data and AI use

Analyses used Python 3.13 with pandas, NumPy, scikit-learn (κ), statsmodels (Wilson intervals) and BeautifulSoup; figures used matplotlib. The study was carried out with the assistance of Claude (Anthropic; model claude-opus-5-5) in October 2026, which retrieved the data, wrote the codebook and the rule-based coder, performed the reading pass and the adjudication, wrote and ran the analysis code, searched the literature and drafted the text under the author's direction. The author reviewed the work and takes full responsibility for it. No protocol was pre-registered.

## 3. Results

### 3.1 Corpus

The eleven searches returned 597 records, which resolved to 163 unique letters; all 163 were retrieved in full (flow counts in the package file results/flow.json). Five letters were to the brand holders: three to Eli Lilly and one to Novo Nordisk on 9 September 2025 about direct-to-consumer promotion of their approved products, and one to Novo Nordisk on 5 March 2026 about postmarketing adverse-event reporting. Four letters were excluded as incidental. The remaining 154 letters were included. They were issued between 2 October 2023 and 24 September 2026 and were posted a median of 8 days after issue (interquartile range 7–11 days; maximum 106).

Most included letters named semaglutide (148 by text search) or tirzepatide (112), and 22 named retatrutide. By seller type, 92 letters went to telehealth platforms, 17 to clinics or med spas, 14 to online pharmacies or marketplaces, 17 to research-chemical sellers, 9 to compounders (3 503A pharmacies and 6 503B outsourcing facilities) and 5 to API suppliers or other manufacturers. Websites or social media were the basis of 141 letters and inspections of 13 (one letter cited both, and one followed a records request).

### 3.2 Timing

The letters came in bursts (Figure 1A). Of 154 letters, 110 (71%) were dated on three days: 55 on 9 September 2025, 30 on 20 February 2026 and 25 on 8 June 2026. The 154 letters fell on 34 issue dates, 26 of which carried a single letter. Eighteen letters predated 22 May 2025, the last of the grace-period deadlines (Figure 1A marks FDA's announced 503A dates), and 136 came after it. All 109 letters to telehealth platforms and clinics came after it, and all were issued in the three batches; letters to online pharmacies, research-chemical sellers, compounders and API suppliers were spread across the period. FDA's press release of 3 March 2026 announced "the issuance of 30 warning letters to telehealth companies" (FDA, 2026b), consistent with the 30 letters dated 20 February 2026; the release names no firms. Only one letter tied a violation to semaglutide or tirzepatide no longer being on the shortage list (a 2026 letter to an outsourcing facility about tirzepatide); six others stated that retatrutide was not used to compound a drug on the shortage list.

### 3.3 Violations and claims

Overall, FDA cited false or misleading labelling under section 502(a) in 115 letters (74.7%; 95% CI 67.3–80.9) and false or misleading advertising or promotion of a compounded drug under 502(bb) in 110 (71.4%; 63.8–78.0) (Table 1). It alleged unapproved new drugs in 46 (29.9%), inadequate directions for use in 32 (20.8%), retatrutide or another unapproved incretin in 22 (14.3%), CGMP or insanitary conditions in 14 (9.1%), the prescription requirement of section 503(b) in 13 (8.4%; 9 letters explicitly alleged sale without a prescription) and sterility-assurance failures in 10 (6.5%). No letter attributed semaglutide or tirzepatide salt forms to the recipient; two early letters mentioned salt forms only in a general footnote.

Among claims, the letters cited the seller's use of approved brand names in 86 letters (55.8%), claims of sameness with a branded product in 76 (49.4%), claims or FDA findings of implied FDA approval in 64 (41.6%), firm-branded labels presenting the seller as the compounder in 51 (33.1%), "research use only" labelling in 17 (11.0%) and the word "generic" in 15 (9.7%).

### 3.4 By seller type

The violations FDA cited differed sharply by seller type (Figure 2; Table 2). Every one of the 109 letters to telehealth platforms and clinics cited sections 502(a) and 502(bb); only 6 of them alleged an unapproved new drug, all because the seller also offered retatrutide. In these letters FDA quoted claims of sameness in 75 and brand names in 74; a letter to Hims & Hers Health, for example, quoted the claim "Same active ingredient as Ozempic and Wegovy" from its website as reviewed in August 2025. Online pharmacies were cited for unapproved new drugs (13 of 14), inadequate directions for use (13) and the prescription requirement (12; 8 with an explicit allegation of sale without a prescription); FDA said several also offered opioids or other controlled drugs. All 17 research-chemical sellers were cited for unapproved new drugs despite labels such as "research use only", and 14 for retatrutide or other investigational incretins. All 9 compounders were cited for CGMP or insanitary conditions and sterility-assurance failures; all 6 outsourcing facilities were cited for failing the conditions of section 503B, and one 503A pharmacy for compounding what FDA alleged were essentially copies of approved products. API suppliers and other manufacturers were cited for CGMP failures; one letter alleged that a foreign API maker labelled semaglutide bought from other firms as its own.

### 3.5 The three telehealth batches

The three batches shared templates but differed in what FDA emphasised (Figure 3A). All 110 letters in them cited 502(bb). In September 2025 FDA quoted sameness claims in 41 of 55 letters (75%), brand names in 43 (78%) and "generic" in 11 (20%); no letter cited firm-branded labels. In February 2026 every one of the 30 letters alleged that the pictured label presented the seller as the compounder "when in fact it is not", and 24 (80%) included FDA's finding that the claims implied FDA approval. In June 2026, 21 of 25 letters (84%) alleged firm-branded labels, and 11 letters objected to claims that the compounding pharmacies or outsourcing facilities supplying the seller were "FDA-approved" or "FDA-licensed". The rise in the implied-approval code, from 24% to 80% and 84%, largely reflects FDA's adoption of that finding in its templates rather than a measured change in sellers' websites.

### 3.6 Coder agreement

Before adjudication the two passes agreed on 94.7% of letter-code cells; median κ across the 22 codes was 0.93, and 16 codes had κ of 0.80 or more (Table 1; Figure 3B). Agreement was 96.9% on eligibility (κ 0.77) and 82.2% on seller type (κ 0.70). Five codes had κ below 0.60: prescription requirement (0.22), implied FDA approval (0.34), sameness (0.55), shortage-list status (0.17) and salt form (0.00, with two discordant letters). Re-reading showed that most of these disagreements arose where the rules matched FDA's boilerplate (the statutory definition of a prescription drug, the 503B shortage-list condition, the sentence on implied sameness) rather than an allegation, or missed paraphrased claims ("the active ingredient in", "bioidentical"). Of 225 disagreements, adjudication sided with the reading pass in 217 and with the rules in 8 (6 of them post-audit recodes of the shortage code). Using the rule-based codes alone would raise the prescription-requirement count from 13 to 68 letters and the implied-approval count from 64 to 98 (sensitivity file in the package); the counts for 502(a), 502(bb), firm-branded labels, research-use labelling and retatrutide were unchanged or within one letter.

### 3.7 Close-outs and recalls

The index showed close-out letters for 2 of the 154 included letters, both to compounders, and no posted response letters. The openFDA search returned 85 unique recall records (24 recall events, 17 firms after merging name variants) naming semaglutide, tirzepatide or retatrutide; 49 (57.6%) gave lack of assurance of sterility as the reason (Figure 1B). Recalls with an initiation date in 2025 numbered 38 and in 2026, 27.

## 4. Discussion

### 4.1 What the letters show

FDA's warning letters on compounded and unapproved GLP-1 products fall into two families. The larger, issued in three batches after the shortages ended, targets the marketing of compounded semaglutide and tirzepatide by telehealth platforms and clinics: apart from six letters about retatrutide, it does not allege that the drugs were unapproved or contaminated, but that the sellers' websites misled consumers, chiefly by implying sameness with Ozempic, Wegovy, Mounjaro or Zepbound, by implying FDA approval and, from 2026, by putting the seller's name on the label. The smaller family, spread over three years, targets what FDA alleged were unapproved products or deficient manufacturing: injectables offered without a prescription by online pharmacies, "research peptides" including retatrutide, and the compounders and API makers whose operations FDA inspected or reviewed.

The claims FDA cited match those that Chetty et al. (2025) counted on websites in 2024, before the crackdown: sameness phrasing on 63.3% of sites and statements or implications of FDA approval on 36.7%. In my reading, the letters show FDA moving from those claims to the identity of the seller, a concern that is not about the drug's chemistry but about who is responsible for it.

### 4.2 What the letters cannot show

Letter counts are a record of FDA's choices. The three batches account for 71% of letters, and their timing (September 2025, February and June 2026) does not line up with the shortage dates in any simple way. The September 2025 batch coincided with letters to the brand holders about their own promotion, and FDA described its telehealth letters as part of a crackdown on misleading direct-to-consumer advertising launched that month (FDA, 2026b); this suggests an advertising initiative rather than a response to compounding volume. Comparing counts before and after 22 May 2025 would therefore say nothing about whether compounding grew or shrank; I did not attempt it. Nor do the letters measure harm: the recall series and the adverse-event reports FDA has received (FDA, 2026d) are separate signals, and the recalls are dominated by sterility concerns at a handful of firms.

### 4.3 Limitations

The coding was done entirely by an AI system. The rule-based pass and the reading pass are different instruments, but the same system wrote both, wrote the codebook and adjudicated the disagreements, siding with its own reading in 217 of 225 cases; the package cannot prove that the rules were fixed before reading (§2.3). The κ values therefore measure agreement between a crude and a careful instrument, not between independent human coders, and they cannot rule out errors that both passes share. No human coded a sample, and no protocol was pre-registered. A reading aid collapsed repeated boilerplate into a legend, which made full reading feasible but could hide small wording changes inside sentences counted as identical. Several conventions (for example, what counts as a sameness claim, and that FDA's template finding of implied approval counts as an implied-approval code) were fixed during reading; they are logged, but they affect the reported frequencies, as the rules-only sensitivity shows. Seller type is sometimes ambiguous: FDA labelled all 2025–2026 marketing letters "(Telehealth)", and I reclassified recipients as clinics or med spas from their names or the letter text. The corpus depends on FDA's full-text index, which changed between searches on the same day, and may miss letters posted only as images or in the FDA archive; untitled letters, Form 483 observations and state referrals were not included. Codes are letter-level, so a letter that also concerned other drugs may carry codes about them. The independent audit re-coded a stratified sample of 31 letters and agreed on 99.7% of cells, but it too was done by an AI model and was not fully blind. Finally, the index shows response and close-out letters only when FDA posts them, so the absence of a close-out does not mean that a firm failed to respond.

## 5. Conclusion

In 154 public warning letters, FDA's enforcement against compounded and unapproved semaglutide and tirzepatide has two faces: template letters to telehealth sellers about claims of sameness, approval and authorship, and individual letters to online pharmacies, peptide sellers and manufacturers that FDA alleged were selling unapproved drugs or making them under deficient conditions. The letters document what FDA alleged and when it chose to act. Whether those letters changed what sellers say and sell is a separate question that needs dated observation of the websites themselves.

## Acknowledgements

Claude (Anthropic; model claude-opus-5-5) assisted with data retrieval, coding, analysis code, literature search and drafting in October 2026, as described in §2.6. The author reviewed all outputs and is responsible for the content.

## Author contributions

P.K. conceived the study, directed the analysis, and reviewed and approved the manuscript.

## Financial support

This research received no specific grant from any funding agency, commercial or not-for-profit sector.

## Conflicts of interest

The author operates a restaurant (The Heritage Diner), a leather-goods business (Marcellino NY) and a real-estate brokerage brand (Maison Pawli). None is related to pharmaceuticals, compounding, telehealth or weight-loss products, and the author declares no competing interests.

## Research transparency and reproducibility

All data are public FDA records. The reproducibility package contains the frozen snapshot hash, the query log, the letter texts' SHA-256 hashes, the codebook, the rule-based coder, the reading-pass log, the agreement and adjudication files, the analysis code and an open dataset of all 163 retrieved letters with their codes. The open dataset names recipients because the letters are public records; each row records an FDA allegation, not a finding of violation, and some firms may have responded to FDA or corrected the issues. Corrections: anyone who believes an entry or a statement in this paper is inaccurate can write to x9m8x7@gmail.com; verified errors will be corrected in a dated new version, with a note of what changed.

## References

Ashraf, A. R., Mackey, T. K., Vida, R. G., Kulcsár, G., Schmidt, J., Balázs, O., Domián, B. M., Li, J., Csákó, I., & Fittler, A. (2024). Multifactor quality and safety analysis of semaglutide products sold by online sellers without a prescription: Market surveillance, content analysis, and product purchase evaluation study. *Journal of Medical Internet Research*, *26*, e65440. https://doi.org/10.2196/65440

Chetty, A. K., Chillakanti, M., Ramachandran, R., Ross, J. S., & Chen, A. S. (2025). Online advertising of compounded glucagon-like peptide-1 receptor agonists. *JAMA Health Forum*, *6*(1), e245018. https://doi.org/10.1001/jamahealthforum.2024.5018

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, *20*(1), 37–46. https://doi.org/10.1177/001316446002000104

Cohen, P. A., Avula, B., Katragunta, K., & Khan, I. (2022). Recalls, availability, and content of dietary supplements following FDA warning letters. *JAMA*, *328*(4), 393–395. https://doi.org/10.1001/jama.2022.9734

DiStefano, M. J., Tilley, A., Paratane, D., Gyimah Gyamfi, H., Moore, G. D., & Nair, K. V. (2026). Postshortage compounded GLP-1 RA market in 2 states with potentially high demand. *JAMA Health Forum*, *7*(7), e262207. https://doi.org/10.1001/jamahealthforum.2026.2207

Dmour, I. (2023). Content analysis of US FDA warning letters issued to compounding pharmacies regarding violations of current good manufacturing practices between 2017 and 2022. *Journal of Pharmaceutical Innovation*, *18*(3), 965–979. https://doi.org/10.1007/s12247-022-09692-4

Donohue, J. M. (2025). Using compounded GLP-1 receptor agonists—Informing and protecting consumers. *JAMA Health Forum*, *6*(1), e245012. https://doi.org/10.1001/jamahealthforum.2024.5012

Kim, H. (2015). Trouble spots in online direct-to-consumer prescription drug promotion: A content analysis of FDA warning letters. *International Journal of Health Policy and Management*, *4*(12), 813–821. https://doi.org/10.15171/ijhpm.2015.157

Lambson, J. E., Flegal, S. C., & Johnson, A. R. (2023). Administration errors of compounded semaglutide reported to a poison control center—Case series. *Journal of the American Pharmacists Association*, *63*(5), 1643–1645. https://doi.org/10.1016/j.japh.2023.06.017

Mattingly, T. J., II, & Conti, R. M. (2025). Marketing and safety concerns for compounded GLP-1 receptor agonists. *JAMA Health Forum*, *6*(1), e245015. https://doi.org/10.1001/jamahealthforum.2024.5015

McCall, K. L., Mastro Dwyer, K. A., Casey, R. T., Samana, T. N., Sulicz, E. K., Tso, S. Y., Yalanzhi, E. R., & Piper, B. J. (2026). Safety analysis of compounded GLP-1 receptor agonists: A pharmacovigilance study using the FDA adverse event reporting system. *Expert Opinion on Drug Safety*, *25*(3), 581–588. https://doi.org/10.1080/14740338.2025.2499670

openFDA. (2026). *Drug recall enforcement reports API* [Data set]. US Food and Drug Administration. Retrieved October 22, 2026, from https://api.fda.gov/drug/enforcement.json

Rogers, C. A., Ahearn, J. D., & Bartlett, M. G. (2020). Data integrity in the pharmaceutical industry: Analysis of inspections and warning letters issued by the bioresearch monitoring program between fiscal years 2007–2018. *Therapeutic Innovation & Regulatory Science*, *54*(5), 1123–1133. https://doi.org/10.1007/s43441-020-00129-z

Tucker, J., Fischer, T., Upjohn, L., Mazzera, D., & Kumar, M. (2018). Unapproved pharmaceutical ingredients included in dietary supplements associated with US Food and Drug Administration warnings. *JAMA Network Open*, *1*(6), e183337. https://doi.org/10.1001/jamanetworkopen.2018.3337

US Food and Drug Administration. (2024). *Regulatory procedures manual, chapter 4: Advisory actions* (Revision 12, July 2024). https://www.fda.gov/media/71878/download

US Food and Drug Administration. (2026a). *FDA clarifies policies for compounders as national GLP-1 supply begins to stabilize* (content current as of 04/01/2026). Retrieved October 22, 2026, from https://www.fda.gov/drugs/drug-alerts-and-statements/fda-clarifies-policies-compounders-national-glp-1-supply-begins-stabilize

US Food and Drug Administration. (2026b, March 3). *FDA warns 30 telehealth companies against illegal marketing of compounded GLP-1s* [Press release]. https://www.fda.gov/news-events/press-announcements/fda-warns-30-telehealth-companies-against-illegal-marketing-compounded-glp-1s

US Food and Drug Administration. (2026c). *Warning letters* [Database]. Retrieved October 21, 2026, from https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters

US Food and Drug Administration. (2026d). *FDA's concerns with unapproved GLP-1 drugs used for weight loss* (content current as of 10/01/2026). Retrieved October 22, 2026, from https://www.fda.gov/drugs/drug-alerts-and-statements/fdas-concerns-unapproved-glp-1-drugs-used-weight-loss

## Tables

**Table 1.** Violations, claims and letter features cited by FDA in 154 included warning letters (issued 2 October 2023 to 24 September 2026), with Wilson 95% confidence intervals, and agreement between the rule-based coder and the reader before adjudication (all 163 retrieved letters). κ is undefined when both coders are constant.

| Code | Letters, n | % (95% CI) | Agreement, % | κ |
|:--|--:|--:|--:|--:|
| *Statutory violations alleged* | | | | |
| Unapproved new drug (505(a)) | 46 | 29.9 (23.2–37.5) | 99.4 | 0.99 |
| False/misleading compounded-drug advertising or promotion (502(bb)) | 110 | 71.4 (63.8–78.0) | 100.0 | 1.00 |
| False/misleading labeling (502(a)) | 115 | 74.7 (67.3–80.9) | 100.0 | 1.00 |
| Inadequate directions for use (502(f)(1)) | 32 | 20.8 (15.1–27.9) | 99.4 | 0.98 |
| Prescription requirement cited (503(b)) | 13 | 8.4 (5.0–13.9) | 66.3 | 0.22 |
| CGMP / insanitary conditions (501(a)(2)(B)/(A)) | 14 | 9.1 (5.5–14.7) | 96.3 | 0.80 |
| Sterility assurance | 10 | 6.5 (3.6–11.5) | 100.0 | 1.00 |
| 503A conditions not met | 8 | 5.2 (2.7–9.9) | 98.8 | 0.88 |
| 503B conditions not met | 12 | 7.8 (4.5–13.1) | 99.4 | 0.96 |
| Salt form / ineligible API | 0 | 0.0 (0.0–2.4) | 98.8 | 0.00 |
| Retatrutide or other unapproved incretin | 22 | 14.3 (9.6–20.7) | 100.0 | 1.00 |
| *Claims and marketing features cited* | | | | |
| "Same as" / same active ingredient claim | 76 | 49.4 (41.6–57.2) | 77.3 | 0.55 |
| "Generic" claim | 15 | 9.7 (6.0–15.4) | 98.2 | 0.90 |
| Implied FDA approval claim | 64 | 41.6 (34.1–49.5) | 65.6 | 0.34 |
| Firm-branded product | 51 | 33.1 (26.2–40.9) | 99.4 | 0.99 |
| "Research use" / not for human consumption | 17 | 11.0 (7.0–17.0) | 97.5 | 0.87 |
| Offered without prescription | 9 | 5.8 (3.1–10.7) | 100.0 | 1.00 |
| Use of approved brand names | 86 | 55.8 (48.0–63.4) | 93.9 | 0.88 |
| *Letter features* | | | | |
| Telehealth / online prescribing features | 1 | 0.6 (0.1–3.6) | 99.4 | 0.66 |
| Inspection-based | 13 | 8.4 (5.0–13.9) | 99.4 | 0.96 |
| Website / social media review | 141 | 91.6 (86.1–95.0) | 99.4 | 0.97 |
| Shortage-list status of recipient's product | 7 | 4.5 (2.2–9.1) | 94.5 | 0.17 |
| Eligibility (include/exclude) | | | 96.9 | 0.77 |
| Seller type (8 categories) | | | 82.2 | 0.70 |

**Table 2.** Selected violations and claims by seller type: number of letters (% of letters to that seller type). Seller type as coded from the letter text; compounders combine 503A pharmacies (n = 3) and 503B outsourcing facilities (n = 6).

| Code | Telehealth (n = 92) | Clinic/med spa (n = 17) | Online pharmacy (n = 14) | Research chemical (n = 17) | Compounder (n = 9) | API/other (n = 5) |
|:--|--:|--:|--:|--:|--:|--:|
| Unapproved new drug (505(a)) | 5 (5) | 1 (6) | 13 (93) | 17 (100) | 8 (89) | 2 (40) |
| Inadequate directions for use (502(f)(1)) | 5 (5) | 1 (6) | 13 (93) | 3 (18) | 8 (89) | 2 (40) |
| Prescription requirement cited (503(b)) | 0 (0) | 0 (0) | 12 (86) | 1 (6) | 0 (0) | 0 (0) |
| False/misleading compounded-drug advertising or promotion (502(bb)) | 92 (100) | 17 (100) | 1 (7) | 0 (0) | 0 (0) | 0 (0) |
| CGMP / insanitary conditions (501(a)(2)(B)/(A)) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 9 (100) | 5 (100) |
| Sterility assurance | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 9 (100) | 1 (20) |
| 503A conditions not met | 5 (5) | 1 (6) | 0 (0) | 0 (0) | 1 (11) | 1 (20) |
| 503B conditions not met | 5 (5) | 1 (6) | 0 (0) | 0 (0) | 6 (67) | 0 (0) |
| Retatrutide or other unapproved incretin | 5 (5) | 1 (6) | 0 (0) | 14 (82) | 1 (11) | 1 (20) |
| "Same as" / same active ingredient claim | 65 (71) | 10 (59) | 1 (7) | 0 (0) | 0 (0) | 0 (0) |
| "Generic" claim | 11 (12) | 3 (18) | 1 (7) | 0 (0) | 0 (0) | 0 (0) |
| Implied FDA approval claim | 48 (52) | 9 (53) | 3 (21) | 3 (18) | 0 (0) | 1 (20) |
| Firm-branded product | 45 (49) | 6 (35) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| Use of approved brand names | 61 (66) | 13 (76) | 8 (57) | 4 (24) | 0 (0) | 0 (0) |
| "Research use" / not for human consumption | 0 (0) | 0 (0) | 0 (0) | 17 (100) | 0 (0) | 0 (0) |
| Offered without prescription | 0 (0) | 0 (0) | 8 (57) | 1 (6) | 0 (0) | 0 (0) |

## Figures

![**Figure 1.** (A) FDA warning letters on compounded or unapproved GLP-1 products by month of issue and seller type, October 2023 to September 2026 (n = 154). Dashed lines mark: 1, tirzepatide shortage declared resolved (2 October 2024); 2, resolution reaffirmed (19 December 2024); 3, announced tirzepatide 503A date (18 February 2025; extended until the court ruling of 5 March 2025); 4, semaglutide shortage declared resolved (21 February 2025); 5, tirzepatide 503B grace period ends (19 March 2025); 6, announced semaglutide 503A date (22 April 2025; extended until the court ruling of 24 April 2025); 7, semaglutide 503B grace period ends (22 May 2025). Letter counts reflect FDA's enforcement timing, not market activity. (B) openFDA drug recall records whose product description names semaglutide, tirzepatide or retatrutide, by quarter of recall initiation; 12 records initiated before October 2023 are not shown. The series includes recalls of approved branded products.](../figures/fig1_timeline.png)

![**Figure 2.** Percentage of letters to each seller type in which FDA cited each violation (above the line) or claim (below the line). Seller type coded from the letter text. Numbers are percentages of letters to that seller type; small groups (compounders, n = 9; API suppliers and other manufacturers, n = 5) give imprecise percentages.](../figures/fig2_heatmap.png)

![**Figure 3.** (A) Claims cited by FDA in the three batches of letters to telehealth platforms, clinics and online sellers (9 September 2025, n = 55; 20 February 2026, n = 30; 8 June 2026, n = 25). The implied-approval code includes FDA's template finding that claims implied FDA approval. (B) Agreement between the rule-based coder and the reading pass before adjudication, all 163 retrieved letters: Cohen's κ (circles) and proportion agreement (diamonds); the dotted line marks κ = 0.80. κ for salt form is 0 with two discordant letters and no reader-coded positives.](../figures/fig3_waves_agreement.png)
