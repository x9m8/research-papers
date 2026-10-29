# Citation audit: "Bags and the body" (manuscript.md, version 1)

Auditor: independent AI agent (Claude), 21 October 2026. The manuscript was not edited.

## How this audit was done, and its limits

- **Metadata:** checked against Crossref (`api.crossref.org/works/<DOI>`) for 16 DOIs. Motricidade 10.6063/motricidade.16954 returned a fetch error from Crossref on two tries. The DOI resolves through the DOI handle API to the publisher page, so its metadata was taken from the publisher PDF header.
- **Claims:** checked against these sources:
  - publisher or repository full texts (johk.pl, BMC/Scoliosis, J-NIOSH copy of Industrial Health, nature.com, mdpi.com, rcaap.pt, ISBS OJS, uOttawa);
  - PMC table sub-pages, which loaded without a bot check;
  - abstracts.
- **Access problems:** Europe PMC REST (`www.ebi.ac.uk`) returned RATE_LIMIT_EXCEEDED on every attempt, more than 10 tries spread over about 30 minutes. PMC article pages showed a reCAPTCHA, which was not bypassed. curl is blocked by the network proxy.
- **Not verified:** for these reasons, some details of Shin 2016, Hyun 2018, Ozgul 2012 and Corrigan 2012 could not be re-read. They are marked **NOT VERIFIED** below; none was assumed to be correct. The Corrigan thesis PDF (10 MB) loads only up to about 75,000 characters through the fetch tool, which ends before the results chapter and appendix tables.
- **No sign-ins:** no email address was sent to any service, nothing was signed in, and Chrome was not used.

Verdict codes:
- **OK**: supported verbatim.
- **OK-minor**: supported, but the wording needs a small fix.
- **FIX**: wrong, or the citation is wrong.
- **NV**: not verified in this audit.

---

## 1. Claims table

| # | Manuscript claim (section) | Source | Supporting quote / data found | Verdict | Fix |
|---|---|---|---|---|---|
| 1 | Strap-side upper trapezius 3.57 → 8.31 %MVC with a one-shoulder bag; cross-body 4.69 (§3.2, Table 2) | Hardie et al. 2015, Table 1 (johk.pl PDF) | Trapezius left: Control 3.57 ± 2.00; "Ipsilateral shoulder strap" 8.31 ± 4.58; "Contralateral shoulder strap" 4.69 ± 2.07. "all single strapped bags were worn on the left shoulder" | OK | None. Optionally say in Methods that Hardie's "contralateral shoulder strap" condition was coded as cross-body. |
| 2 | Opposite-side erector spinae 2.51 → 3.61 (Table 2) | Hardie Table 1 | Erector spinae right: 2.51 ± 0.94 (control) vs 3.61 ± 1.19 (ipsilateral strap) | OK | None |
| 3 | Strap-side ES "changed little" (§3.2) | Hardie Table 1; Yoon Table 1 | Hardie ES left 3.66 → 3.41. Yoon right ES 0.197 → 0.170/0.166/0.185 | OK | None |
| 4 | Hardie: 12 women, 10% BM, treadmill 5 min (Table 1; §4.1 "one study of 12 women") | Hardie | "Twelve female university students" (20.6 ± 1.16 y); "each containing 10% bodyweight"; "walked on a treadmill for 5 minutes at 1.1 m/s" | OK | None |
| 5 | "a cross-body bag roughly halved the trapezius effect" (Abstract) | Hardie Table 1 | Raw increase: +4.74 (one-shoulder) vs +1.12 %MVC (cross-body), about a 76% reduction. g 1.25 vs 0.51 | OK-minor | "Roughly halved" understates the raw-unit reduction and fits only the g values. Suggest "reduced the trapezius effect by more than half". |
| 6 | Yoon: bag-side UT 0.168 → 0.31 / 0.357 / 0.421 across three strap lengths, larger for longer straps (§3.2, Table 2) | Yoon 2014, Table 1 (PMC table page) | Right UT: no bag 0.168 ± 0.126; shoulder bag at iliac crest 0.310 ± 0.163, below 10 cm 0.357 ± 0.172, below 20 cm 0.421 ± 0.251 | OK | None |
| 7 | Yoon opposite-side ES 0.196 → 0.251 / 0.248 / 0.252 (Table 2) | Yoon Table 1 | Left ES: no bag 0.196 ± 0.063; 0.251 ± 0.111, 0.248 ± 0.094, 0.252 ± 0.089 | OK | None |
| 8 | Yoon EMG "unit labelling ambiguous" (§2.5, §4.4, Table 2 note) | Yoon Table 1 | Title: "(Unit: mV/sec)", but the footnotes define each row as "%MVIC" | OK | None |
| 9 | Yoon: n = 20, 23 y, 10% BM, treadmill 5 min; "both studies … treadmill walking with a 10% body-mass bag" (§3.2, Table 1) | Yoon methods | **NV.** The Methods section could not be read (PMC bot check; Europe PMC rate-limited). | NV | Re-check against the PMC full text before submission. |
| 10 | Corrigan: double support 26.2% → 27.7 / 29.5 / 31.1% at 10/20/30% BM; stride length and width values (§3.3, Table 2) | Corrigan 2012 thesis | Abstract only: "double support time and stride width increased, while stride length decreased as the load of the hockey bag increased." "Fifteen male participants (aged 23.44 ±2.63 years)." The numeric values (appendix Table 4, per extraction.csv) could not be reached. | Direction OK; numbers NV | Re-check the numbers against the thesis appendix. extraction.csv records the "±" values as SE. The thesis text excerpt uses "±" without saying SD or SE, so the SE→SD conversion should be confirmed at the table. |
| 11 | Corrigan: peak ES activity "rising on both sides" with load; listed among studies that "point the same way without usable dispersion" (§3.2) | Corrigan thesis abstract | The abstract's significant EMG increases list semitendinosus, gastrocnemius, rectus abdominis and vastus medialis, **not erector spinae**. The thesis hypothesis was that ES peak EMG "will show no significance or decrease with added weight". extraction.csv ratios: 1.07–1.32 with SE 0.16–0.28, so the data do have dispersion. | FIX | Reword, e.g.: "In Corrigan (2012), peak erector spinae activity, normalised to walking without a bag, was numerically higher on both sides with a shoulder-carried bag (ratios 1.07–1.32), but this was not among the significant effects reported." Also drop "without usable dispersion": SEs are given, but no SD exists for the control because it equals 1 by construction. |
| 12 | Corrigan's bag is a "shoulder-carried sports bag" (Table 1) | Thesis abstract | Thesis abstract: "hockey bag" carried on one side (paraphrased from the uOttawa record); the author attributes the results to the "posterior-lateral carrying style" | OK-minor | Say "hockey bag (shoulder-carried)" to be specific. |
| 13 | Rodrigues: own bags, mostly ≤5% BM; 143 and 61 women analysed by side; n = 258, 18–59 y (§3.3, §4.2, Table 1) | Rodrigues 2020 PDF | "a higher proportion of women carried bags weighing ≤ 5% of their body weight and on the right side"; "55.4% (n=143) of the participants carried the bag on" "the right shoulder"; "with 258 women (18-59 years old) who used" shoulder bags. Table 1 sums: 61 left, 54 both; 214 of 258 (83%) ≤5% | OK | None. Optionally add "(83%)", noting that this is computed from Table 1 and not stated in the paper. |
| 14 | Rodrigues "overground, 2 m plate" (Table 1) | Rodrigues | extraction.csv: "2 m baropodometer". Not re-read verbatim. | NV-minor | None needed if the extraction is correct. |
| 15 | Shin: very old women turned faster when holding a light bag; 10 F, 81 y, ~0.2 kg (§3.3, Table 1) | Shin & Yoo 2016 | **NV.** Full text was unreachable. The title ("Differences in gait velocity … with and without bag in females of very advanced age") fits. extraction.csv gives velocity 67.2 ± 13.6 (bag) vs 59.0 ± 8.8 cm/s (no bag). | NV | Re-check in PMC5011589. In-text citation must be "Shin and Yoo (2016)" (two authors). |
| 16 | Suzuki: 26 young adults, 10 min, shoulder and cross-body bags, results in figures only (§3.3, Table 1) | Suzuki 2025, nature.com | "Gait parameters of 26 healthy, pain-free young adults were assessed over a 10-minute period"; conditions "without luggage (WL), backpack (BP), shoulder bag (SB), and crossbody bag (CB)"; "10 males and 16 females aged 22–44 years" | OK-minor | Numbers appear only in figures, but the text and abstract state the direction ("differences in stance time, pushing time, cadence, and walking speed"). Suggest "reported gait differences by luggage type … with numerical results shown only in figures". |
| 17 | Tajik: 30 men (15 CLBP), 23–28 y; dumbbell 10/20% BM in one hand; higher lumbar activity; means without SDs (§3.2, Table 1) | Tajik 2026, mdpi.com | "Thirty male recruits (age 23–28 years) … 15 individuals with clinically diagnosed chronic low back pain (CLBP)… and 15 asymptomatic controls"; "the entire load was taken in the right hand"; 10% and 20% BW; asymmetric 20%: "0.282 and 0.263%MVIC" (CLBP) vs "0.262 and 0.239%MVIC" (controls); no-load CLBP "baseline activation ranging from 0.100 to 0.154%MVIC" | OK. The "no SDs" detail is NV because Table 1 is an image. | None |
| 18 | Tseng: 9 men, hand-held 10% BM; HR 149 vs 141 bpm; RPE 15.5 vs 11.2; slightly higher than backpack; averaged over 9 slope × speed combinations (§3.5, Table 1) | Tseng & Liu 2011 (J-NIOSH PDF) | "Nine male undergraduate students"; "22.4 (0.49) yr"; "a bag filled with books to obtain a total pack weight of 10% of each participant's body weight"; "held on right hand only". Table 1: empty 141.3 (17.2) bpm, RPE 11.2 (2.9); backpack 147.2 (16.7), 14.1 (2.9); hand-held 149.1 (16.3), 15.5 (3.2). "averaged during ascending and descending" | OK-minor | Values are correct. (a) The text says "Climbing stairs", but the means average **ascending and descending**: say "Walking up and down stairs". (b) Table 1 says "Tseng et al. (2011)": change to "Tseng and Liu (2011)" (two authors). |
| 19 | Sussman: one-strap bag; changes in lateral and forward trunk lean and head tilt; Table 1 "load NR" (§3.4, Table 1) | Sussman et al. 2001 (ISBS PDF) | Conditions WO, 1SR ("one strap on right shoulder"), 2SB, 2SF. Table 1 WO vs 1SR: head tilt 1.65 ± 0.62 vs 2.69 ± 0.87; forward lean 7.12 ± 2.16 vs 3.15 ± 3.91; lateral lean 6.39 ± 1.11 vs 4.83 ± 1.09. Load: "an average weight of 13 pounds" | FIX (Table 1) | Load **was** reported: 13 lb (about 5.9 kg) in every condition, %BM not reported. Change "load NR" to "13 lb (≈5.9 kg); %BM NR". Optionally note that with the one-strap bag, forward and lateral lean were *lower* than without a bag, and that the abstract's WO values differ from its Table 1. |
| 20 | Negrini: one-shoulder load ≈17% BM increased shoulder asymmetry and trunk rotation in standing; 43 adolescents, 12–13 y (§3.4, Table 1) | Negrini & Negrini 2007 (BMC PDF) | "A group of 43 subjects (18 females, 25 males)", "age 12.5 ± 0.5 years"; 8 kg ASYM "correspondent to 16.8 ± 3,8% of body weight"; Table 4 (ASYM vs neutral): shoulder asymmetry 18 ± 17.8 and trunk rotation 3.1 ± 3.4, both significant; "All the subjects were evaluated in the upright position" | OK | None |
| 21 | Ozgul: one-shoulder backpack 15% BM changed pelvic motion; 20 M, 13 y (§3.4, Table 1) | Ozgul et al. 2012 (Hacettepe repository abstract) | "Twenty adolescents (mean age: 13 +/- 1.2 years)"; pelvic rotation range decreased and anterior tilt and obliquity increased on the loaded side. The abstract gives neither the load % nor sex. | Direction OK; "15%" and "M" NV | Confirm 15% BW and all-male sample in the full text. |
| 22 | Hyung: hand, one-shoulder and cross-body bags at 5/10/15% BM; 36 comparisons; 16, 21 y (§3.4, Table 1) | Hyung et al. 2016, Table 1 (PMC table page) | "Table 1. Differences in pelvic tilt and pelvic rotation for each experimental condition (N=16, units:°)." Conditions: hand bag, shoulder bag, cross bag, back pack; loads 0/5/10/15%; 4 outcomes. 3 bags × 3 loads × 4 outcomes = 36 | OK. Age NV. | None |
| 23 | Hyun: 9 M, 23 y, 20 kg barbell at one side (Table 1) | Hyun & Ryew 2018 | **NV** (PMC bot check). Crossref confirms 2 authors. | NV | Table 1 "Hyun et al. (2018)" must be "Hyun and Ryew (2018)". Re-check the details. |
| 24 | Paediatric literature produced "several reviews (for example Ellapen et al., 2021; Guleria et al., 2023)" (§1) | Crossref titles | Ellapen: "Altered cervical posture kinematics imposed by heavy school backpack loading: A literature synopsis (2009–2019)". Guleria: "…among school going students: a scoping review" | OK | None. Both are reviews of school backpacks and students. |
| 25 | Reported with reference to PRISMA-ScR (Tricco et al., 2018) (§2.1) | Crossref | "PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation", *Ann Intern Med* 169(7):467–473 | OK | Reference list truncates authors with "et al.": APA 7 lists 19 + last (see §3). |
| 26 | "I was not able to find a review focused on asymmetric bag carriage in adults" (§1) | Novelty search (§4) | Badawy et al. (2018, *Ergonomics*) is a systematic review of **one-handed carrying** (26 articles). Gai et al. (2025) is a systematic review of load carriage in older adults that includes asymmetric/one-hand studies. A Kharazmi University SSRC poster reviews asymmetrical load-carrying during gait (abstract only). The package's own search_log.md lists Gai 2025 and the SSRC review as found. | FIX (calibrate) | See §4 for suggested wording. |
| 27 | Corrigan cited as thesis rather than journal version | uOttawa record; Crossref | The thesis (2012, MSc Human Kinetics, supervisor J. X. Li; DOI 10.20381/ruor-6220) carries the gait tables. The journal version (Corrigan & Li, 2014, *Res Sports Med* 22(1):23–35) is titled on **muscle activities**, and its full text was not accessible. | OK-minor | Citing the thesis for gait numbers is justified. Add the journal article as the peer-reviewed version (e.g., "Corrigan, 2012; published in part as Corrigan & Li, 2014"). The thesis author is "Corrigan, Liam" in the repository, with no middle initial, so use "Corrigan, L." for the thesis. |

### Other in-text citation fixes
- Table 1: "Tseng et al. (2011)" → "Tseng and Liu (2011)"; "Hyun et al. (2018)" → "Hyun and Ryew (2018)".
- Table 1: "Shin et al. (2016)" → "Shin and Yoo (2016)". §3.3: "Shin et al. (2016)" → "Shin and Yoo (2016)".
- APA 7 uses "et al." in text only for three or more authors. Hardie (4), Hyung (3), Rodrigues (5), Ozgul (6), Suzuki (8) and Tajik (8) correctly take "et al.". Ellapen (4) and Guleria (3) also take "et al." in text, but the **reference list** must give their full author names.

---

## 2. Crossref table

| Ref | DOI | Crossref result | Discrepancies vs manuscript reference list |
|---|---|---|---|
| Ellapen 2021 | 10.4102/ajod.v10i0.687 | Ellapen T. J.; Paul Y.; Hammill H. V.; Swanepoel M. *African Journal of Disability* 10; online 2021-01-22; no issue, page or article number in Crossref | "et al." must become all 4 authors. Article number: the journal's e-locator is a687; Crossref lists none, so "687" stays acceptable. |
| Guleria 2023 | 10.20463/pan.2023.0025 | Guleria M.; Sharma S. P.; Kumar A. *Physical Activity and Nutrition* 27(3), 020–026; 2023-09-30 | Missing all authors, volume, issue and pages |
| Hardie 2015 | 10.1515/hukin-2015-0005 | Hardie R.; Haskew R.; Harris J.; Hughes G. *Journal of Human Kinetics* 45(1), 39–47; print 2015-03-01, online 2015-04-07 | Missing volume, issue and pages |
| Hyun 2018 | 10.12965/jer.1835120.560 | Hyun Seung-Hyun; Ryew Che-Cheong. *Journal of Exercise Rehabilitation* 14(1), 152–155; 2018 | "et al." is wrong (2 authors). Missing volume, issue and pages. |
| Hyung 2016 | 10.1589/jpts.28.2059 | Hyung Eun-Ju; Lee Hyun-Ok; Kwon Yu-Jeong. *Journal of Physical Therapy Science* 28(7), 2059–2062; 2016 | Missing volume, issue and pages. Initials should be hyphenated (E.-J., H.-O., Y.-J.). |
| Negrini 2007 | 10.1186/1748-7161-2-8 | Negrini Stefano; Negrini Alberto. *Scoliosis* 2(1), article 8; 2007 | Missing volume and article number |
| Ozgul 2012 | 10.3944/aott.2012.2678 | Ozgul Bahar; Akalan N. Ekin; Kuchimov Shavkat; Uygur Fatma; Temelli Yener; Polat Gulden. *Acta Orthop Traumatol Turc* 46(4), 269–274 | Missing volume, issue and pages. Crossref lists "Polat, Gulden", while the Hacettepe repository has "Polat, M. Gulden", so keep "Polat, M. G.". |
| Rodrigues 2020 | 10.6063/motricidade.16954 | Crossref fetch failed (client error, 2 tries). DOI resolves (handle API) to revistas.rcaap.pt/motricidade/article/view/16954. Publisher PDF: "2020, vol. 16, n. 2, pp. 144-155"; authors Bárbara Karen Matos Magalhães Rodrigues, Mariza Araújo Marinho Maciel, Bruna Lima Parente, Pedro Olavo de Paula Lima, Ana Paula Vasconcellos Abdon | Missing volume, issue and pages. Initials: B. K. M. M., M. A. M., B. L., P. O. de P., A. P. V. |
| Shin 2016 | 10.1589/jpts.28.2330 | Shin Sun-Shil; Yoo Won-Gyu. *J Phys Ther Sci* 28(8), 2330–2331; 2016 | "et al." is wrong (2 authors). Missing volume, issue and pages. |
| Suzuki 2025 | 10.1038/s41598-025-12569-4 | 8 authors as listed; *Scientific Reports* 15(1), article 27074; online 2025-07-25 | Matches. APA style is "Article 27074". |
| Tajik 2026 | 10.3390/bioengineering13010082 | 8 authors as listed; *Bioengineering* 13(1), 82; online 2026-01-12 | Matches. APA style is "Article 82". |
| Tricco 2018 | 10.7326/M18-0850 | 28 authors (Tricco … Straus); *Annals of Internal Medicine* 169(7), 467–473; 2018-10-02 | "et al." after 6 authors: APA 7 requires the first 19, an ellipsis, then the last author. |
| Tseng 2011 | 10.2486/indhealth.ms1100 | Tseng Hsien-Yu; Liu Bor-Shong. *Industrial Health* 49(1), 30–36; 2011 | Missing volume, issue and pages |
| Yoon 2014 | 10.1589/jpts.26.1937 | Yoon Jung-Gyu. *J Phys Ther Sci* 26(12), 1937–1939; 2014 | Missing volume, issue and pages |
| Corrigan & Li 2014 (journal version) | 10.1080/15438627.2013.852094 | Corrigan Liam Patrick; Li Jing Xian. *Research in Sports Medicine* 22(1), 23–35; print 2014-01-02 | Not in the reference list (recommended addition) |
| Badawy 2018 (novelty) | 10.1080/00140139.2018.1470680 | Badawy M.; Schall M. C., Jr.; Sesek R. F.; Gallagher S.; Davis G. A.; Capanoglu M. F. *Ergonomics* 61(10), 1345–1354 | New, for the novelty statement |

**References without a DOI:**
- **Sussman 2001** (ISBS OJS article 3799; PDF at article/view/3799/3519).
  - PDF header: "Biomechanics Symposia 2001 / University of San Francisco", pp. 150–153.
  - Nine authors, all at Old Dominion University: Donald H Sussman, Martha Walker, Michael Tamburello, Bonnie VanLunen, Elizabeth A Dowling, Kelly R. Campbell, Joseph D. Flores, Rasha A. Ibrahim, Eleanor A. Larson.
  - The reference list's "et al." after three authors must become all nine (APA lists up to 20).
  - The URL is valid.
- **Corrigan 2012 thesis** (uOttawa).
  - Author "Corrigan, Liam"; supervisor Li, Jing Xian; MSc, Human Kinetics; 2012.
  - Handle http://hdl.handle.net/10393/23531; **DOI 10.20381/ruor-6220**.
  - APA 7 should use the DOI in place of the item URL.
  - The manuscript's thesis title matches the repository.

---

## 3. Corrected APA 7 reference list (ready to paste)

Corrigan, L. (2012). *The effect of unilateral load carriage on the muscle activities of the trunk and lower limbs of young healthy males during gait* [Master's thesis, University of Ottawa]. uO Research. https://doi.org/10.20381/ruor-6220

Corrigan, L. P., & Li, J. X. (2014). The effect of unilateral hockey bag carriage on the muscle activities of the trunk and lower limb of young healthy males during gait. *Research in Sports Medicine*, *22*(1), 23–35. https://doi.org/10.1080/15438627.2013.852094

Ellapen, T. J., Paul, Y., Hammill, H. V., & Swanepoel, M. (2021). Altered cervical posture kinematics imposed by heavy school backpack loading: A literature synopsis (2009–2019). *African Journal of Disability*, *10*, Article 687. https://doi.org/10.4102/ajod.v10i0.687

Guleria, M., Sharma, S. P., & Kumar, A. (2023). Analytical parameters to check association between load carriage system and bag packs-influenced musculoskeletal complications among school going students: A scoping review. *Physical Activity and Nutrition*, *27*(3), 20–26. https://doi.org/10.20463/pan.2023.0025

Hardie, R., Haskew, R., Harris, J., & Hughes, G. (2015). The effects of bag style on muscle activity of the trapezius, erector spinae and latissimus dorsi during walking in female university students. *Journal of Human Kinetics*, *45*(1), 39–47. https://doi.org/10.1515/hukin-2015-0005

Hyun, S.-H., & Ryew, C.-C. (2018). Effect of wearing positions of load on the dynamic balance during gait. *Journal of Exercise Rehabilitation*, *14*(1), 152–155. https://doi.org/10.12965/jer.1835120.560

Hyung, E.-J., Lee, H.-O., & Kwon, Y.-J. (2016). Influence of load and carrying method on gait, specifically pelvic movement. *Journal of Physical Therapy Science*, *28*(7), 2059–2062. https://doi.org/10.1589/jpts.28.2059

Negrini, S., & Negrini, A. (2007). Postural effects of symmetrical and asymmetrical loads on the spines of schoolchildren. *Scoliosis*, *2*, Article 8. https://doi.org/10.1186/1748-7161-2-8

Ozgul, B., Akalan, N. E., Kuchimov, S., Uygur, F., Temelli, Y., & Polat, M. G. (2012). Effects of unilateral backpack carriage on biomechanics of gait in adolescents: A kinematic analysis. *Acta Orthopaedica et Traumatologica Turcica*, *46*(4), 269–274. https://doi.org/10.3944/AOTT.2012.2678

Rodrigues, B. K. M. M., Maciel, M. A. M., Parente, B. L., Lima, P. O. de P., & Abdon, A. P. V. (2020). Use and weight of shoulder bag in female gait and associated factors. *Motricidade*, *16*(2), 144–155. https://doi.org/10.6063/motricidade.16954

Shin, S.-S., & Yoo, W.-G. (2016). Differences in gait velocity and trunk acceleration during semicircular turning gait with and without bag in females of very advanced age. *Journal of Physical Therapy Science*, *28*(8), 2330–2331. https://doi.org/10.1589/jpts.28.2330

Sussman, D. H., Walker, M., Tamburello, M., VanLunen, B., Dowling, E. A., Campbell, K. R., Flores, J. D., Ibrahim, R. A., & Larson, E. A. (2001). Loaded backpack positions affects trunk position during walking. *ISBS Conference Proceedings Archive* (Biomechanics Symposia 2001, University of San Francisco), 150–153. https://ojs.ub.uni-konstanz.de/cpa/article/view/3799

Suzuki, S., Watanabe, D., Shimizu, H., Tanigawa, K., Kashiyama, S., Kawamoto, S., Nagai-Tanima, M., & Aoyama, T. (2025). Effect of luggage type on gait parameters using in-shoe motion sensors. *Scientific Reports*, *15*, Article 27074. https://doi.org/10.1038/s41598-025-12569-4

Tajik, R., Dhahbi, W., Mimar, R., Khaleghi Tazji, M., Ceylan, H. İ., Bayrakdaroğlu, S., Stefanica, V., & Hammami, N. (2026). Neuromuscular and kinetic adaptations to symmetric and asymmetric load carriage during walking in individuals with chronic low back pain. *Bioengineering*, *13*(1), Article 82. https://doi.org/10.3390/bioengineering13010082

Tricco, A. C., Lillie, E., Zarin, W., O'Brien, K. K., Colquhoun, H., Levac, D., Moher, D., Peters, M. D. J., Horsley, T., Weeks, L., Hempel, S., Akl, E. A., Chang, C., McGowan, J., Stewart, L., Hartling, L., Aldcroft, A., Wilson, M. G., Garritty, C., … Straus, S. E. (2018). PRISMA extension for scoping reviews (PRISMA-ScR): Checklist and explanation. *Annals of Internal Medicine*, *169*(7), 467–473. https://doi.org/10.7326/M18-0850

Tseng, H.-Y., & Liu, B.-S. (2011). Effects of load carrying methods and stair slopes on physiological response and postures during stairs ascending and descending. *Industrial Health*, *49*(1), 30–36. https://doi.org/10.2486/indhealth.MS1100

Yoon, J.-G. (2014). Correlations between muscle activities and strap length and types of school bag during walking. *Journal of Physical Therapy Science*, *26*(12), 1937–1939. https://doi.org/10.1589/jpts.26.1937

Add these only if the novelty paragraph is revised as suggested in §4:

Badawy, M., Schall, M. C., Jr., Sesek, R. F., Gallagher, S., Davis, G. A., & Capanoglu, M. F. (2018). One-handed carrying among elderly and obese individuals: A systematic review to identify research gaps. *Ergonomics*, *61*(10), 1345–1354. https://doi.org/10.1080/00140139.2018.1470680

Gai, Z., Meng, Z., & Liu, H. (2025). A systematic review of the biomechanical impact of load carriage on gait in older adults. *Trends in Physical Education and Sport*, *1*(2), 4–14. https://doi.org/10.31489/3081-0531/2025-1-2/4-14

Notes on the list:
- The Crossref record for Ozgul spells the DOI in lower case; DOIs are case-insensitive, so either case is acceptable.
- Rodrigues "Lima, P. O. de P." follows the publisher's full name, "Pedro Olavo de Paula Lima". "Lima, P. O. P." is also defensible.
- The Gai metadata comes from the journal's article page (vol. 1, no. 2, pp. 4–14; DOI as shown there). It was not checked against Crossref.

---

## 4. Novelty check

The search was done with WebSearch and publisher pages. The Europe PMC REST search could not be run in this audit because every call was rate-limited. The package's own search_log.md (Q6, plus the web search) already lists Gai 2025 and the SSRC review as found.

### Reviews that overlap the manuscript's scope

1. **Badawy et al. (2018), *Ergonomics* 61(10):1345–1354.** "One-handed carrying among elderly and obese individuals: a systematic review to identify research gaps" (CDC Stacks copy).
   - It reviewed 26 articles on one-handed carrying, mostly in young and middle-aged adults.
   - "Only two studies evaluated the effect of age as an independent variable during one-handed carrying."
   - It found one-handed carrying generally more demanding than other methods, and cites suggested one-hand limits of about 9–10 kg (men) and 6–7 kg (women).
   - **This is the closest existing review: a systematic review of asymmetric (hand) carriage in adults.**
   - It is not mentioned in the manuscript or in search_log.md. The source dissertation is Badawy, M. (2018), PhD, Auburn University, "Evaluating Responses to One-handed Carrying among Older and Obese Individuals".
2. **Gai, Meng & Liu (2025), *Trends in Physical Education and Sport* 1(2):4–14**, "A Systematic Review of the Biomechanical Impact of Load Carriage on Gait in Older Adults".
   - Five databases searched to June 2025. Eight studies, participants aged ≥60 y (per the paper; some study means are 59.7 y).
   - It covers both symmetric and asymmetric carriage. The asymmetric/one-hand studies are Badawy 2019, Bampouras 2016 (shopping bag), Matsuo 2008 (single-hand) and Zhang 2018 (single-hand and shoulder).
   - It concludes: "Asymmetrical load carriage during walking increases step frequency and step width"; older adults "are advised to carry loads symmetrically and keep the weight below 5% of body mass".
   - Older adults only, so not a competitor for the general adult scope, but it is a direct prior synthesis for the manuscript's older-adult records.
3. **"Kinematics and Kinetics Analysis of Asymmetrical Load-Carrying During Gait: A Systematic Review"** (14th SSRC congress, Kharazmi University, Tehran; poster 1467-SSRC; https://14thcong.ssrc.ac.ir/article_4439.html).
   - Abstract only: no authors shown on the page and no number of studies.
   - Searched PubMed, Scopus and Web of Science. Load is "often performed asymmetrically with one hand."
   - It concludes that load-carrying "significantly alters joint angles and range of motion in the lower extremities."
   - Its scope (asymmetric carriage, gait) overlaps, but no full text or study list is available.
4. **Genitrini, Dotti, Bianca & Ferri (2022), *IJERPH* 19(11):6737**, "Impact of Backpacks on Ergonomics: Biomechanical and Physiological Effects: A Narrative Review" (doi 10.3390/ijerph19116737).
   - A narrative review of backpacks, double packs and T-packs.
   - Asymmetric carriage appears only briefly. It cites Hardie et al. for adults ("wearing a single strap BP resulted in significantly higher activity of the erector spinae on the contralateral side") and recommends "using both shoulder straps, rather than asymmetrically."
   - It does not cover cross-body or hand-carried bags.
   - The PMC ID "PMC9180465" given in the brief could not be confirmed (PMC and Europe PMC unreachable).
5. **Al-Shamrani & Abdel Basset Mohamed (2023), *International Design Journal* 13(1):151–160**, "The Physical Ergonomics Body Posture In Wearing Bags; A Review Article" (doi 10.21608/idj.2023.276157).
   - A descriptive narrative review aimed at bag design. It touches on shoulder, cross-body and hand bags in adults, but is not systematic.
6. **Paediatric reviews**, consistent with the manuscript: Ellapen 2021, Guleria 2023, and the 2003 BMC systematic review "The postural effects of load carriage on young people" (found by search, not re-read).
7. **"Badawy"**: there is no review by Badawy on shoulder bags or handbags. The Badawy item is the one-handed-carrying systematic review in item 1.

### Possibly missed primary studies found incidentally (for the search/limitations section)
- **Qureshi & Shamus (2012)**, *Internet Journal of Allied Health Sciences and Practice* 10(4), Article 5.
  - 65 college students aged 18–30; a 10 lb single-strap bag worn across the body on the right or left shoulder vs no bag.
  - Outcome: static lower-extremity weight distribution.
  - Adults with a no-bag comparator: it appears to meet the eligibility criteria, depending on whether "weight distribution" counts as a posture or balance outcome.
- **Lee (2017)**, *Journal of Musculoskeletal Science and Technology* 1(1):2–6 (doi 10.29273/jkema.2017.1.1.2).
  - Same-side vs cross-body shoulder bag at 10% BW, 20 students, static standing, upper trapezius and ES EMG. There is no no-bag test condition; no-bag was used only for normalisation.
  - It would be excluded, like Cho 2013, but it is a second cross-body EMG study relevant to the Discussion. It reports right UT 333.45 ± 180.07 (same side) vs 124.60 ± 43.72 %RVC (cross-body).
- **ClinicalTrials.gov NCT06992518**, "The Effect of Bag Carrying Style on Gait Parameters in Healthy Adults". It is already in search_log.md; the registry details could not be fetched (robots or empty page).

### Calibration of the novelty claim
The §1 sentence "I was not able to find a review focused on asymmetric bag carriage in adults" is **not accurate as written**:
- Badawy et al. (2018) systematically reviewed one-handed carrying in adults.
- Gai et al. (2025) reviewed load carriage, including asymmetric carriage, in older adults.
- A conference-abstract systematic review of asymmetrical load-carrying during gait exists.
- The package's own search log records the last two as found.

What does appear to be new is a **scoping review and evidence map spanning all three bag modes (one-shoulder, cross-body, hand-carried) in adults, with bags as the object**.

Suggested replacement: "Related reviews exist but are narrower. Badawy et al. (2018) systematically reviewed one-handed carrying, with a focus on older and obese workers. Gai et al. (2025) reviewed load carriage, including asymmetric carriage, in adults aged 60 and over. A systematic review of asymmetrical load-carrying during gait has been presented only as a conference abstract. Reviews of backpacks mention one-strap carriage only in passing (Genitrini et al., 2022). I found no review that maps one-shoulder, cross-body and hand-carried bag carriage together in adults."

---

## 5. Summary of required fixes (priority order)
1. **§1 novelty sentence:** revise (see §4). Cite Badawy et al. 2018 and Gai et al. 2025.
2. **§3.2 Corrigan ES statement:** ES increases were not among the significant effects in the thesis abstract. Reword. "Without usable dispersion" is inaccurate, since SEs exist.
3. **Table 1, Sussman "load NR":** the load was 13 lb (≈5.9 kg).
4. **Two-author citations:** "Tseng et al." → "Tseng and Liu"; "Hyun et al." → "Hyun and Ryew"; "Shin et al." → "Shin and Yoo" (text and Table 1). Fix the reference list to match.
5. **Reference list:** add missing volume, issue and pages for 11 entries, full author lists for Ellapen, Guleria, Sussman and Tricco, and the thesis DOI. Add Corrigan & Li 2014.
6. **§3.5:** "Climbing stairs" → "Walking up and down stairs" (Tseng's means average ascent and descent).
7. **Abstract "roughly halved":** tighten the wording.
8. **Re-verify before submission (NV items):**
   - Yoon methods (n, 10% BM, treadmill 5 min);
   - Corrigan numeric gait table and SE label;
   - Shin details and velocities;
   - Hyun details;
   - Ozgul 15% BW and all-male sample;
   - Tajik absence of SDs.
