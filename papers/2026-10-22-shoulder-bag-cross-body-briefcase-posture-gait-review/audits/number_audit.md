# Number audit: "Bags and the body" (scoping review), manuscript v1

Auditor: independent agent, 2026-10-21. Nothing in the package was edited.

**Method.** The pipeline (effects.py, evidence_map.py, figures.py, tables.py) was re-run on a scratch copy. All six result files and the regenerated `## Tables` section are byte-identical to the shipped versions, so the manuscript tables are in sync with the code. Every number in the abstract, text, tables and captions was then checked against `results/`, `data/` and `search_log.md`. map_coding.csv was compared row by row with the studies.csv `reason`/`full_text_read` fields and with extraction.csv. The three figure PNGs were inspected. Values were spot-checked against the source articles where they could be fetched.

**Access limits.** PMC returned a reCAPTCHA page, the Europe PMC `fullTextXML` endpoint returned rate-limit errors on every attempt, and curl to ebi.ac.uk was refused by the proxy (403). J-STAGE PDFs are blocked by robots.txt, and Chrome was not connected. Spot checks therefore used the publisher or repository copies listed below. Yoon 2014, Hyung 2016, Shin 2016, Negrini 2007 and Tseng 2011 could not be checked beyond their abstracts.

Verdicts used below: OK (matches), MINOR (small wording or precision issue), ERROR (the number or claim is wrong), OVERSTATED (the claim goes beyond the evidence), UNSUPPORTED (the coding is not backed by the source text), UNVERIFIED (could not be checked).

---

## A. Numbers in abstract, text, tables, captions

| Location | Claim | Correct value / source | Verdict | Fix |
|---|---|---|---|---|
| Abstract, §2.3, Fig 1 | 12 queries, 936 hits, 789 unique, +9 other, 798 screened | search_log: 12 queries, hits sum = 936; 789 unique; 9 other records listed; 798 | OK | — |
| §2.3 / Fig 1 | 733 excluded at title/abstract; 65 assessed | 798 − 65 = 733; studies.csv has 65 rows | OK | — |
| Abstract, §2.3, Fig 1 | "24 in full text"; "Twenty-four were read in full" | studies.csv `full_text_read`: only 18 say yes (16 plain yes, the thesis, and deVette, whose "abstract is full text"). The other 6 say abstract (Presta2020, CorriganLi2012_ISBS, Guleria2023, Ellapen2021), abstract + methods (Zhao2023) or partial, from a fetch summary (Mache_ISBS) | ERROR | "24 were assessed at the full-text stage; 18 were read in full and 6 (two reviews, a model, a single-case report, a duplicate and one off-protocol record) were excluded on the abstract or partial text" |
| §2.3, Fig 1 box | 41 not obtained "because of a paywall, a bot check … or no locatable copy" | studies.csv marks Rafi2026, Serafim2026 and Oja1982 as OA but not retrieved, and Mandrekar2019 as "OA per Unpaywall but publisher page not readable" | OVERSTATED | Add "or open access but not retrieved in this session (4)" |
| Fig 1 box | Abstract only n = 41 "charted in the evidence map" | Only 40 charted: Corrigan2014 was removed as a duplicate (map_summary: Abstract only = 40) | ERROR | "41 (40 charted; 1 duplicate of the included thesis)" |
| Fig 1 box | Included 13 "(9 adult with SDs, 2 adolescent)" | Fig 3 and effects_summary have 8 adult studies with usable SDs. The ninth (Tseng2011) has marginal SDs that §2.5 says were not converted | ERROR (inconsistent) | "8 adult with usable SDs" or "9 adult with dispersion (1 marginal)" |
| Fig 1 / §2.3 | Excluded at full text n = 11 | 11 "no" rows in studies.csv; matches the search_log list | OK | — |
| Abstract, §2.4, §3.1 | 60 records charted; 13 / 7 / 40 | map_summary: 60; included 13, excluded 7, abstract only 40 | OK | — |
| §3.1 | 45 adults, 5 older adults, 10 children/adolescents | map_summary by_pop. Note: two of the "older adult" records (Matsuo2008, Bampouras2016) also include young adults | OK / MINOR | "five included older adults" |
| §3.1 | One-shoulder 31, hand 16, non-bag 13, cross-body 8 | map_summary reproduces these, **but** Son2013 has an empty `outcomes` field, and evidence_map.py drops any record without an outcome from the long table. Son2013 therefore counts in none of the bag totals. Corrected counts: one-shoulder 32, hand-carried 17. One record ("unclear", Bergmann1997) is not mentioned | ERROR (coding/code) | Code Son2013 outcomes = gait; recount; mention the 1 unclear record |
| §3.1 | Gait 19, posture 11, forces 9, EMG 9, balance 7, joint angles 7, effort 6, comfort 1, pressure 1 | Matches map_summary, but gait becomes ≥20 once Son2013 is coded, and the coding gaps in section C (balance, coordination, kinetics) change several of these counts. Coordination (2) is not mentioned | MINOR→ERROR after recoding | Recount after fixing coding |
| §3.1, Abstract | "None measured pain or musculoskeletal symptoms" | True of map_coding. Checks: Tajik2026 used pain NRS only as an inclusion criterion (MDPI full text). Bloswick1994 measured fatigue, not symptoms (abstract). Rodrigues2020's abstract does not mention pain. 40 records were charted from abstracts only, so the claim cannot be fully verified | OK but needs a hedge | "none of the 60 records, as far as their full texts or abstracts show, measured pain…" |
| §3.1 | Median 16, range 5–258, 29 records | map_summary reproduces these, but `n` is missing for records where the screening record gives it: Presta2020 n = 1, Pascoe1997 n = 10, Cho2013 n = 30 (abstract). Full-text-excluded records have no n even though they were read. Adding the three known values: k = 32, median 15.5, range 1–258 | ERROR (incomplete coding) | Fill n from the reasons and full texts; recompute; say "where sample size was coded" |
| §3.1 | "Only five records studied people in their own working lives: mail carriers, firefighters, manual workers, and women carrying their own bags" | Code count = 5 (Rodrigues, Bloswick, Lin1996, Park2018, Gomez2018). Lin1996 is titled "Part II. Biomechanical laboratory study", Park2018 used simulated firefighting, and Rodrigues was a lab gait test with the participants' own bags. Angelini2018 (firefighters) and Oja1982 (postal delivery) are coded as plain "adult" | OVERSTATED / inconsistent | "Seven records studied occupational groups (mail carriers, firefighters, manual workers) or participants' own bags, mostly in laboratory tests" |
| §3.1, §4.3, Conclusion | "Briefcases appeared in one abstract-only record" | Only Zultowski2008 mentions a briefcase in studies.csv reasons, and its outcome (sway) is outside the protocol. Consistent with the data, but the 40 abstract-only records were not re-read | OK (data-consistent) | Optional: "…in one abstract-only record (sway only, outside protocol)" |
| §3.1 | 13 included: 8 young adults + 1 CLBP men + 1 women 18–59 + 1 women >75 + 2 adolescents | Sums to 13. Shin2016 mean age is 80.9 (SD 5.5); "over 75" is not in extraction and the abstract says only "very advanced age" | UNVERIFIED (">75") | "women with a mean age of 81" |
| §3.1 | "Loads were mostly 5% to 15%; one study went to 30%" | Corrigan went to 30%. Hyun2018's 20 kg barbell ≈ 27.6% BM (extraction, confirmed: BM 72.38 kg). Tajik went to 20% | ERROR | "two studies used loads of about 28–30%" |
| §3.2 / Table 2 | Hardie trapezius 3.57→8.31 %MVC, g = 1.25; cross-body 4.69, g = 0.51; ES opposite 3.61 vs 2.51, g = 0.95 | Matches effects_all; source values confirmed (johk.pl PDF) | OK | — |
| §3.2 / Table 2 | Yoon g = 0.94–1.22, "with the larger values for the longer straps" | g values OK. Yoon's abstract (J-STAGE) reports no significant correlation between strap length and muscle activity, and the three CIs overlap almost entirely | OVERSTATED | Drop "with the larger values…" or add "the author found no significant effect of strap length" |
| §3.2 / Table 2 | ES opposite side, Yoon g = 0.59–0.70 | effects_all 0.59, 0.62, 0.70 | OK | — |
| §3.2 | "Strap-side erector spinae activity changed little in either study" | Hardie −0.08; Yoon −0.34, −0.42, −0.14 | OK / MINOR | Could say "changed little or fell slightly" |
| §3.2 | Corrigan peak ES rising on both sides, normalised to no bag | Extraction: R 1.10/1.13/1.20, L 1.07/1.15/1.32. Note: the thesis abstract does not list the erector spinae among muscles that increased | OK (descriptive) | Add "no test reported" |
| §3.2 | Tajik 10% and 20% dumbbell, men with and without CLBP, means only | Confirmed (MDPI: 30 men, 23–28 y, right-hand dumbbells 10%/20% BW, no SDs; tables are images) | OK | — |
| §3.3 / Table 2 | Corrigan double support 26.2→27.7/29.5/31.1, g = 0.36/0.95/1.40; stride width and length | Matches effects_all (SE×√15). Direction confirmed in the thesis abstract (right shoulder; DS and width up, stride length down). Undisclosed: extraction flags possible copy errors in the thesis tables (large-bag stride lengths identical to small-bag) and that only the small bag was used | OK / MINOR | State "small hockey bag" in Table 1; note the thesis data issue in limitations |
| §3.3 | "In 143 and 61 women" (Rodrigues), g between −0.17 and 0.38 | g range matches. The 143 and 61 are habitual right- and left-shoulder carriers. 54 women who alternated sides were not extracted (143 + 61 = 204 of 258) | MINOR | "143 right-shoulder and 61 left-shoulder carriers (54 who alternated sides not analysed)" |
| §3.3 | "Gait responded to load more than to carriage style" | No included study gives usable gait data comparing carriage styles: Hyung is pelvic only, Suzuki is figures only, Son2013 is excluded | UNSUPPORTED | Delete or rephrase as "Gait effects grew with load (one study); carriage style was not compared on gait with usable data" |
| §3.3 | Shin: very old women turned faster with a light bag | Abstract confirms. g = 0.65 (CI −0.03 to 1.34) | OK | — |
| §3.4 | Hyung 36 comparisons, g −0.87 to 1.38 | effects_all: 36 rows, min −0.870, max 1.378 | OK | — |
| §3.4 | Sussman changes in lateral and forward lean, head tilt | Source abstract confirms head tilt 1.65→2.69 and forward lean WO 7.12. Extraction note: the abstract's WO lateral lean (7.22 ± 2.01) differs from the table value used (6.39 ± 1.11), which is not disclosed | OK / MINOR | Note the abstract/table discrepancy |
| §3.4 | Negrini ~17% BM; Ozgul 15% | 16.8 (3.8)%; 15% | OK | — |
| §3.5 | Tseng: 9 men, HR 149 vs 141, RPE 15.5 vs 11.2, slightly above backpack; nine slope × speed combinations | 149.1/141.3; 15.5/11.2; backpack 147.2 and 14.1; 3 slopes × 3 speeds. Task included ascent **and descent**; text says "climbing" | OK / MINOR | "ascending and descending stairs" |
| §4.1 | Cross-body "rests on one study of 12 women" | Cho2013 (n = 30 women, read in full, excluded for lacking a no-load comparator) directly compared one-shoulder and cross-body bags and found significant differences in both upper trapezius muscles (J-STAGE abstract). studies.csv itself flags it as "useful for one-shoulder vs cross-body". Hardie did **not** test one-shoulder vs cross-body: the contralateral value has no significance marker (source PDF) | OVERSTATED / incomplete | Report Cho2013 as secondary evidence and state that Hardie gave no direct test |
| Abstract | "a cross-body bag roughly halved the trapezius effect" | g fell from 1.25 to 0.51 (−59%); the raw increase fell from 4.74 to 1.12 %MVC (−76%). CIs overlap, and there was no direct test | OVERSTATED | "…was associated with a smaller trapezius increase (g 0.51 vs 1.25), though the two were not compared statistically" |
| §4.1, Conclusion | Effects "about one standard deviation" for both muscles | Trapezius 0.94–1.25; opposite erector spinae 0.59–0.95 | OVERSTATED (ES) | "about 0.6 to 1.2 standard deviations" |
| §4.2 | "most tested students for a few minutes on a treadmill" | Only 3 of 13 included studies used a treadmill (Hardie, Yoon, Sussman) | ERROR | "in a laboratory" |
| §4.2 | "Ten per cent … is 7 kg for a 70 kg adult, heavier than most handbags and close to a loaded laptop briefcase" | The arithmetic is right. The handbag and briefcase comparisons have no source | Opinion presented as fact | Source it or mark it as an estimate |
| §4.4 | "41 of 65 could not be read in full" | Consistent with the flow, but see the 24-vs-18 issue above: 47 of 65 were not read in full | ERROR (follows from above) | Revise |
| Fig 3 caption | 8 studies, 89 outcomes; one value beyond the axis, g = 4.6 (peak vGRF, 20 kg barbell) | effects_summary 8/89; Hyun g = 4.63. Source confirms 1.18 ± 0.08 vs 1.59 ± 0.08 N/BW | OK | — |
| Fig 3 caption | "Outlined dots are muscles or measurements on the bag side" | The flag comes from a text match on "bag side / strap side". Problems: (a) Hardie cross-body strap-side trapezius and ES are outlined, but in the cross-body condition the bag hangs on the opposite (right) hip; (b) side-specific non-EMG outcomes are never outlined, e.g. Rodrigues R/L stride length for right/left carriers and Hyung R/L pelvic tilt | ERROR | Recode: "strap-side" vs "bag-side" separately, or limit the caption to "strap-side muscles" |
| Fig 2 caption | "the blue disc is the number of included full-text studies" | The disc **area** encodes the included count, but the printed number is the total. Where included = total (e.g. cross-body angles, hand-carried angles) the yellow disc is hidden. The "unclear" bag row (1 record) is not shown, though the caption says n = 60 | MINOR | "blue disc area ∝ included studies; number = all records"; note that 1 record with unclear bag type is not shown |
| Table 1 | Sussman load "NR" | Extraction: 5.9 kg (13 lb) | ERROR | "5.9 kg (13 lb)" |
| Table 1 | "Tseng et al. (2011)" | Two authors (Tseng & Liu), as in the text and reference list | ERROR | "Tseng & Liu (2011)" |
| Table 1 / refs | "Hyun et al. (2018)", "Hyun, S. H., et al." | e-jer article page lists Hyun & Ryew (2018), 14(1):152–155 | ERROR (citation) | "Hyun & Ryew (2018)"; complete the reference |
| Table 1 | Suzuki: no load given | Source: 3.3 kg contents; 4.0 kg (shoulder) / 4.8 kg (cross-body) total; ages 22–44 | MINOR | Add the loads |
| Table 1 | Rodrigues "258 F (143 and 61 analysed by side)" | See §3.3 row | MINOR | Name the sides |
| Table 1 | All other cells (n, sex, mean age, load, task) | Match extraction.csv. Hardie 12 F, 20.6 y; Hyun 9 M, 23.0 y confirmed at source | OK | — |
| Table 2 | 18 rows | Byte-identical to tables.py output; all g/CI match effects_all | OK | — |

## B. Methods vs code

| Location | Claim | Code / data | Verdict | Fix |
|---|---|---|---|---|
| §2.5 | d = (mean_carry − mean_noload)/√((SD_c² + SD_0²)/2) | effects.py `sdav`, `diff` | OK | — |
| §2.5 | Hedges correction | J = 1 − 3/(4(n−1) − 1), i.e. df = n − 1 (paired). Methods do not state the df | OK / MINOR | Add "df = n − 1" |
| §2.5 | 95% CI assumes r = 0.5; 0.2 and 0.8 in result files | var = 2(1−r)/n + g²/(2n). At r = 0.5 this equals the standard Borenstein formula (1/n + d²/2n)·2(1−r). At r = 0.2 and 0.8 it does **not**, because the d² term is not scaled by 2(1−r). Example, Hardie trapezius: r = 0.8 CI in the files is 0.63–1.86 against 0.77–1.73 by the standard formula. The main-text CIs are unaffected | MINOR (sensitivity files) | Use var = (1/n + g²/2n)·2(1−r), or describe the formula used |
| §2.4/§2.5 | SE converted to SD | SE·√n_analysed, applied to Corrigan only | OK | Could add "SD = SE·√n" |
| §2.5 | Not converted: change scores, normalised ratios without comparison SD, means without dispersion, pooled SDs | Negrini (change scores; adolescent anyway), Corrigan EMG (comparison SD "NA"), Tajik (no SD), Tseng (dispersion label "SD (marginal…)" ≠ "SD", so sd() returns NaN) | OK | The Tseng exclusion works only through a string mismatch; make it explicit in code |
| §2.5 | "no-load" comparisons | Regex classifies as no-load: "no bag (control)", "no bag", "no load", "no load (0%)", "same participants without bag", "no backpack (WO)", "no backpack (NoBP)", "empty load (no load)", "unloaded neutral". Excluded: all rucksack/backpack comparators. All classifications checked correct | OK | — |
| §2.5 | "adult studies" | `adult` = age_group contains "adult" and not "ADOLESCENT"; includes Shin2016 (mean 81 y) | OK | — |
| §2.4 | Extraction from tables or text, nothing from figures | Consistent with search_log. Tajik tables are images (still tables) | OK | — |
| Extraction completeness | Hardie conditions | Hardie Table 1 also has a **one-strap rucksack** (a one-shoulder backpack) condition (trapezius left 6.42 ± 2.83), which was not extracted. It is an eligible asymmetric condition | ERROR (omission) | Extract it, or justify leaving it out |

## C. Evidence-map coding (map_coding.csv vs studies.csv / extraction)

| Record | Coding | Source text | Verdict | Fix |
|---|---|---|---|---|
| Son2013 | outcomes blank, n blank | Title "Gait changes caused by… carrying a handbag" | ERROR: the record is silently dropped from all bag and outcome counts | outcomes = gait |
| Presta2020 | posture, n blank | Reason "single-case (n = 1)"; title "gait swing phase and pelvic tilt" | ERROR | outcomes = gait;kinematics; n = 1 |
| Pascoe1997 | n blank | Reason "n = 10" | ERROR | n = 10 |
| Cho2013 and other full-text exclusions (Wang2021, Ramadan2018, deVette2014, Mache_ISBS) | n blank | Full texts read; Cho n = 30 (abstract) | Incomplete | Fill n |
| Bampouras2016 | gait | Title includes "static postural stability" | Incomplete | add balance |
| Matsuo2008 | gait | Title "relationship with lower limb coordination" | Incomplete | add coordination |
| Hyun2018 | gait;kinetics | Title "dynamic balance"; Table 1 lists balance | Incomplete | add balance |
| Zhang2010, Kellis2009, Hong2005 | no kinetics | Titles mention ground reaction force / ground reactions | Incomplete | add kinetics |
| deVette2014 | gait | Title "Kinetic and kinematic effects" | MINOR | kinetics;kinematics |
| Rafi2026 | shoulder same-side | Reason gives no bag type; title "asymmetrical load magnitude and location" | UNSUPPORTED | unclear or non-bag, after checking the abstract |
| Li2018 | shoulder same-side | Reason gives no bag type | UNSUPPORTED | unclear |
| Wang2018a, Wang2018b, Wang2020 | non-bag load | Reasons give no load type. The same group's Wang2021 used messenger bags | UNSUPPORTED | Check abstracts; likely bags |
| Lee2014, Lee2016, Shi2015 | non-bag load | Reasons: "Asym load", "Right-hand load"; type not stated | UNSUPPORTED | unclear, unless the abstract says otherwise |
| Gomez2018 | non-bag load | "Heavy sacks on shoulder" | Questionable | arguably a shoulder-carried bag |
| Wang2021 | cross-body | "symmetric bilateral messenger bags" comparator; asymmetric condition not described | Plausible, not explicit | Confirm |
| Oja1982 | population "adult" | "manual postal delivery" | Inconsistent | adult (mail carriers): field count +1 |
| Angelini2018 | population "adult" | Title "firefighter obstacle crossing" | Inconsistent | adult (firefighters): field count +1 |
| Corrigan2014 | status "duplicate report" | studies.csv status "abstract only" | OK (removed as a duplicate), but Fig 1 then overstates the charted count | — |
| All other rows | — | Consistent with reasons and extraction | OK | — |

## D. Flow numbers vs search_log.md

936 (sum of Q1–Q12 hits verified), 789, 9, 798, 733, 65, 41, 24, 11 and 13 all match the log. Issues:

- The "24 full texts" includes 6 records assessed from the abstract or partial text only (see section A).
- Of the 9 other-source records, 4 never reached the 65: Simpson (backpack), **Gai et al. 2025 systematic review**, **SSRC systematic review of asymmetrical load-carrying**, and NCT06992518. The 2 Europe PMC reviews (Guleria, Ellapen) were taken forward to detailed assessment while these 2 directly relevant reviews were dropped at screening, which is inconsistent.

## E. Figures

- **Fig 1.** No overlaps. Content errors: "(9 adult with SDs…)" should be 8; "charted in the evidence map" should be 40; "Full text read n = 24" should be relabelled. The arrow into the "Excluded n = 733" box is very short but legible.
- **Fig 2.** No overlaps. The x labels fit. Disc area encodes the included count while the label shows the total, so where they are equal the yellow ring disappears. The "unclear" row (1 record) is omitted. Counts will change after the Son2013 and other recoding.
- **Fig 3.** Panel titles match effects_summary (2/24, 2/39, 4/26). The "4.6 →" label sits on top of that row's grey CI bar (slight overlap, top right of the Gait panel). Bag-side outlines are wrong for the cross-body rows and missing for non-EMG side-specific outcomes (see section A). The legend icon for "Bag-side" is a black ring, while plotted outlined dots are filled with the bag colour. Acceptable, but could be clearer.

## F. Overstatements and interpretation

1. **"I was not able to find a review focused on asymmetric bag carriage in adults"** (§1). The search itself found two related reviews, listed in search_log as other-source records and excluded at screening:
   - Gai, Meng & Liu (2025), a systematic review of load carriage and gait in older adults that covers asymmetric carriage (8 studies);
   - an SSRC (Kharazmi University) poster, "Kinematics and Kinetics Analysis of Asymmetrical Load-Carrying During Gait: A Systematic Review", covering one-hand loads.

   Neither is specific to bags in working-age adults, so the sentence can stand only if it is narrowed and these two are cited. Suggested: "The closest reviews cover asymmetric load carriage in general (SSRC poster) or in older adults (Gai et al., 2025); I found none focused on bags in working-age adults."
2. **"None measured pain"** is true of the coded records, but 40 of 60 were coded from abstracts. Lin et al.'s companion paper ("Letter-carrier satchels: Part I. Field study", about 300 USPS carriers) rated comfort in real work and was retrieved by Q12 but excluded at screening. The conclusion's "Whether everyday bag carriage causes pain has not been studied" and §4.3's call for "a field study" should acknowledge observational and field work outside the experimental scope (Lin Part I; children's backpack-pain surveys excluded at screening). Suggested: "…has not been tested experimentally; observational field data are limited to comfort ratings".
3. **Cross-body interpretation** (abstract "roughly halved"; §4.1 "rests on one study of 12 women"). Hardie did not test cross-body against one-shoulder. The CIs overlap (1.25 [0.49, 2.00] vs 0.51 [−0.09, 1.11]). In the cross-body condition the "strap-side" trapezius is on the side away from the bag, so it is not the same muscle-to-load relationship. Cho2013 (n = 30, read in full) directly compared the two methods and is omitted. Also, Hardie's cross-body condition raised activity in the opposite trapezius (g 0.37) and in the bag-side erector spinae (0.49), so the load is redistributed rather than simply reduced.
4. "Gait responded to load more than to carriage style" (§3.3): no usable data compares styles on gait. Unsupported.
5. Yoon "larger values for the longer straps": the author reports no significant strap-length effect.
6. "Only five records studied people in their own working lives": most were laboratory tests (see section A).
7. "most tested students … on a treadmill": only 3 of 13 used a treadmill.
8. "about one standard deviation" for the erector spinae (0.59–0.95) in §4.1 and the Conclusion.
9. "one study went to 30%": two studies were at about 28–30%.

## G. Spot-check of extraction values against sources (10+ values)

| Study | Source used | Values checked | Result |
|---|---|---|---|
| Hardie 2015 | johk.pl publisher PDF (Table 1) | Trap L control 3.57 ± 2.00, ipsi 8.31 ± 4.58, contra 4.69 ± 2.07; Trap R 4.55/5.22/6.10; ES L 3.66/3.41/4.87; ES R 2.51 ± 0.94, 3.61 ± 1.19, 3.02 ± 0.99; rucksack 3.02 ± 1.46; n 12 F, 20.6 y, 1.1 m/s, 5 min, left shoulder, 10% BW | All match. Also found an unextracted 1-strap rucksack column |
| Hyun 2018 | e-jer.org article page | 1-step time 0.55 ± 0.04 / 0.54 ± 0.04; COM velocity 1.53 ± 0.10 / 1.64 ± 0.11; XCOM angle 4.14 ± 2.78 / 6.70 ± 1.60; peak vGRF 1.18 ± 0.08 / 1.59 ± 0.08; n 9 M, 23.0 y, BM 72.38 | All match. Authors: Hyun & Ryew |
| Sussman 2001 | ISBS OJS page (abstract) | Head tilt WO 1.65 ± 0.61 vs 1SR 2.69 ± 0.87; forward lean WO 7.12 ± 2.16 | Match (WO head-tilt SD 0.61 at source vs 0.62 extracted; table not seen). Lateral lean differs between abstract and table, as flagged in extraction |
| Tajik 2026 | MDPI full text | 30 M, 23–28 y, 15 CLBP; right hand 10/20% BW; means only; pain NRS only at inclusion | Match. EMG cell values are in image tables and were not verified |
| Suzuki 2025 | nature.com | n = 26, shoulder and cross-body bags, 10 min, figures only | Match. Loads (4.0/4.8 kg) not in Table 1 |
| Corrigan 2012 | uOttawa thesis abstract | n = 15 M, 23.44 y, right shoulder, 10/20/30%; DS and width up, stride length down | Direction matches. Table values and the SE label could not be checked (PDF text lacked tables) |
| Yoon 2014 | J-STAGE abstract | n = 20 students; no significant strap-length correlation | n matches; table values unverified (PDF blocked) |
| Shin 2016 | J-STAGE abstract | 10 women; faster turning with bag | Matches; numbers unverified |
| Cho 2013 (excluded) | J-STAGE abstract | 30 women; significant trapezius difference, one-side vs cross-body | Relevant to the cross-body claim |
| Rodrigues 2020 | Motricidade abstract | 258 women 18–59; with vs without bag | Matches; no pain measure mentioned |

---

## Fix list (priority order)

1. **Full-text count.** Replace "24 read in full" (Abstract, §2.3, Fig 1, §4.4) with 18 read in full plus 6 assessed from abstract or partial text. Update §4.4 to "47 of 65 not read in full" or equivalent.
2. **Review claim (§1).** Narrow "not able to find a review" and cite Gai et al. 2025 and the SSRC asymmetric load-carriage review, which the search itself found. Make the screening of reviews consistent.
3. **Cross-body.** Abstract: replace "roughly halved" with a hedged statement noting there was no direct test and the CIs overlap. §3.2/§4.1: add Cho2013 (n = 30) as direct-comparison evidence; note that the cross-body "strap-side" muscle is on the opposite side to the bag and that activity shifts to other muscles.
4. **Son2013.** Code Son2013 outcomes (gait). Recompute §3.1 bag and outcome counts (one-shoulder 32, hand 17, gait 20 at minimum) and Fig 2.
5. **map_coding.csv gaps.** Fill the missing n (Presta 1, Pascoe 10, Cho 30, other full-text exclusions). Add the missing outcomes (Presta, Bampouras, Matsuo, Hyun, deVette, Zhang, Kellis, Hong). Recode the unsupported bag types (Rafi, Li, Wang2018a/b/2020, Lee2014/2016, Shi) and the populations (Oja, Angelini). Recompute the median/range and the field count; say "where coded".
6. **Load range (§3.1).** "Loads were mostly 5–15%; two studies used about 28–30% (Corrigan; Hyun, 20 kg barbell)".
7. **§4.2.** Change "on a treadmill" to "in a laboratory" (only 3 of 13 used a treadmill).
8. **§3.3.** Delete or rewrite "Gait responded to load more than to carriage style".
9. **§3.2.** Remove "with the larger values for the longer straps", or add that Yoon found no significant strap-length effect.
10. **§3.1.** Rewrite "Only five records studied people in their own working lives…" (mostly laboratory tests; seven occupational or own-bag records after recoding).
11. **§4.1 / Conclusion.** "about one SD" → "about 0.6 to 1.2 SD".
12. **Pain claims.** Hedge "None measured pain" for abstract-only coding. Soften the Conclusion's "has not been studied" to "has not been tested experimentally", and acknowledge field/comfort work (Lin et al. Part I).
13. **Fig 1.** "9 adult with SDs" → 8; "charted in the evidence map" → 40 of 41.
14. **Fig 3.** Fix the bag-side outline coding: strap side ≠ bag side for cross-body; flag side-specific gait and pelvis outcomes too. Nudge the "4.6 →" label off the CI bar.
15. **Fig 2.** Clarify the caption (disc area vs printed number); note the 1 "unclear" record not shown.
16. **Table 1.** Sussman load 5.9 kg (13 lb); "Tseng & Liu (2011)"; Suzuki loads 4.0/4.8 kg; Rodrigues "143 right- and 61 left-shoulder carriers"; Corrigan "small hockey bag".
17. **References.** Hyun & Ryew (2018), *J Exerc Rehabil* 14(1), 152–155.
18. **§3.1.** Shin "women over 75" → "mean age 81"; Tseng "climbing" → "ascending and descending".
19. **§2.3.** Add "open access but not retrieved" (4 records) to the reasons for abstract-only assessment.
20. **Extraction.** Extract Hardie's one-strap rucksack condition, or state why it was left out. Disclose Sussman's abstract/table discrepancy and the Corrigan thesis table issue.
21. **Code.** Fix the r = 0.2/0.8 sensitivity variance formula in effects.py (main r = 0.5 results unaffected). Make the Tseng non-conversion explicit rather than relying on a string mismatch. State df = n − 1 for Hedges' J in §2.5.
22. **§4.2.** Source or mark as an estimate the claim that 7 kg is "heavier than most handbags and close to a loaded laptop briefcase".

Sources consulted: Hardie et al. 2015 PDF (johk.pl/wp-content/uploads/2023/03/10.1515_hukin-2015-0005.pdf); Hyun & Ryew 2018 (e-jer.org/journal/view.php?number=2013600478); Sussman et al. 2001 (ojs.ub.uni-konstanz.de/cpa/article/view/3799); Tajik et al. 2026 (mdpi.com/2306-5354/13/1/82); Suzuki et al. 2025 (nature.com/articles/s41598-025-12569-4); Corrigan 2012 (ruor.uottawa.ca item and thesis PDF); Yoon 2014, Shin 2016 and Cho 2013 J-STAGE abstract pages; Rodrigues 2020 (revistas.rcaap.pt/motricidade/article/view/16954); Bloswick 1994 (journals.sagepub.com); Gai et al. 2025 (tpes.buketov.edu.kz/physical-education-trends/article/view/1063); SSRC review (14thcong.ssrc.ac.ir/article_4439.html); Lin et al. Part I (scholars.ttu.edu).
