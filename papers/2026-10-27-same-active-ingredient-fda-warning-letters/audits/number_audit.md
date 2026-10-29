# Paper 13 ("Same as Wegovy") — independent number and methods audit

Auditor: Claude (independent audit pass), 22 Oct 2026. No package file other than this report was edited.
Scratch re-run: `/tmp/claude-0/-home-claude/e77537ee-4bde-5960-ac22-2794b7601af1/scratchpad/p13audit`

## 1. Reproduction

The full pipeline ran without errors on a scratch copy: 01 → 06, then figures, tables and graphical_abstract.
- Byte-identical: all 15 `results/*` files, `data/coding/{pass1_rules,pass2_reader,disagreements,adjudication_log}.csv`, and all 163 letter texts.
- Figures: every PNG matches pixel for pixel (`ImageChops` bounding box = None).
- Snapshot SHA-256 recomputed: `e9176b7f…a924084`. This matches the README, the manuscript and `snapshot_manifest.json`.
- openFDA file SHA-256: `017252792a2c…3809393`. The manuscript and README give no hash for this file, so it should be added.
- `frozen_before_pass2.sha256`: the hashes it lists for `02_rules.py` and `CODEBOOK.md` match the current files. **However, the file also lists the hash of `pass2_reader_log.txt`, and its mtime (06:07:34.028) is the same second as the final pass-2 log.** It was therefore written after pass 2, not before. The package cannot verify the claims that "its SHA-256 was recorded before pass 2 began" (README) and "frozen … before pass 2 began / not run until pass 2 was finished" (§2.3). See fix F3.

## 2. Number check (abstract, text, tables, captions, figures)

All checks are against the results files. Rows marked OK need no change.

| Location | Claim | Correct value | Verdict | Fix |
|---|---|---|---|---|
| Abstract / 3.1 | 597 records → 163 letters; 5 brand-holder; 4 incidental; 154 included | flow.json: same | OK | — |
| Abstract / 3.6 | median κ 0.93 across 22 codes | 0.928 | OK | — |
| Abstract / 3.2 | 110 (71%) on 3 days; 55/30/25 | 110/154 = 71.4% | OK | — |
| Abstract | 109 telehealth+clinic letters all cited 502(bb) | 109/109 | OK | — |
| Abstract | "same active ingredient as a branded drug in 75 of them" | 75 (65+10). The code is broader: it includes "generic of", "compounded version", "bioidentical" and "active ingredient in" | Number OK; wording too narrow | Say "claims of sameness with a branded drug" |
| Abstract | firm-branded labels from Feb 2026, 51 letters | 51 = 30 Feb + 21 Jun; 0 in Sep | OK | — |
| Abstract | "…and retatrutide or other unapproved incretins (22 letters)" in the sentence on non-telehealth sellers | 22 is the total. Of these, 6 went to telehealth/clinic; 16 to the named groups (14 research, 1 compounder, 1 API/other) | **Misattributed** | Write "(16 letters; 22 overall)" or drop the parenthetical |
| 3.1 | posting lag median 8, IQR 7–11, max 106 | same | OK | — |
| 3.1 | semaglutide 148, tirzepatide 112, retatrutide 22 | summary.json same | OK | — |
| 3.1 | 92 / 17 / 14 / 17 / 9 (3+6) / 5 | same | OK | — |
| 3.1 | website 141, inspection 13 | same. These are not exclusive: 1 letter has both, and 1 (Chengdu, a 704(a)(4) records request) has neither | OK | Optional note |
| 3.2 | 34 issue dates, 26 single-letter | same | OK | — |
| 3.2 | 18 before / 136 after 22 May 2025 | same | OK | — |
| 3.2 | all 109 telehealth/clinic letters in the three batches | 54 + 30 + 25 = 109 | OK | — |
| 3.2 | press release "the issuance of 30 warning letters to telehealth companies" | Verified verbatim on fda.gov (3 Mar 2026). The release names no firms | OK | "matching the 30 letters dated 20 Feb" is an inference; say "consistent with" |
| 3.2 | "Only one included letter discussed the shortage status of the recipient's own product" | **7.** ProRx (723704) says tirzepatide was not on the shortage list. Six Sep-2025 retatrutide letters (rows 21, 23, 30, 41, 42, 61) say retatrutide "is not used to compound a drug that appears on the drug shortage list". These were coded 0, inconsistently | **Inaccurate** | "Only one letter tied a violation to semaglutide or tirzepatide no longer being on the shortage list; six others noted retatrutide was not on it." Relabel the Table 1 row (see below) |
| 3.3 / Table 1 | 502(a) 115 (74.7; 67.3–80.9); 502(bb) 110 (71.4; 63.8–78.0); 505(a) 46; 502(f)(1) 32; incretin 22; CGMP 14; Rx 13; sterility 11 | prevalence.csv same | OK | — |
| 3.3 | "dispensing without a prescription in 13" | 13 letters cite §503(b). In 4 of them (rows 4, 5, 20, 162) §503(b) appears only in the opening list of violated sections. The body never alleges sale without a prescription. The explicit allegation (C_no_rx) is 9 | **Overstated wording** | Say "cited the prescription requirement, section 503(b), in 13 (9 explicitly alleged sale without a prescription)". Same for the online pharmacy "12" in 3.4 and "sale without prescription" in the abstract |
| 3.3 | salt forms 0; "two early letters … general footnote" | rows 0–1, both issued 2 Oct 2023; general footnote verified | OK | — |
| 3.3 | brand names 86 (55.8), sameness 76 (49.4), approval 64 (41.6), firm 51 (33.1), research 17 (11.0), generic 15 (9.7) | same | OK | — |
| 3.4 | 6 telehealth/clinic letters alleged unapproved drugs, all with retatrutide | V_unapproved = V_other_peptide in all 109 | OK | — |
| 3.4 | sameness 75, brand 74 | 65+10, 61+13 | OK | — |
| 3.4 | Hims & Hers quote "Same active ingredient as Ozempic and Wegovy" | verbatim in letter 716567 (dba Hims) | OK | Add "on its website as reviewed in Aug 2025" |
| 3.4 | online pharmacy 13/14, 13, 12 | same | OK (see Rx wording) | — |
| 3.4 | research 17/17 unapproved; 14 incretin | same | OK | — |
| 3.4 | compounders 9/9 CGMP and sterility; 7 × 503B, 3 × 503A | same. 503A = 3 includes Genogenix (a 503B facility) and Thrive, both coded from a footnote saying repackaged drugs are ineligible for 503A/503B. 503B = 7 includes Thrive (a 503A pharmacy) on the same basis | Numbers OK; basis weak | Footnote it or recode (see 3 below) |
| 3.4 | Harbin "relabelled semaglutide bought from another firm as its own" | FDA: 2 batches bought from **two** unapproved suppliers and labelled with Harbin as manufacturer. FDA says this "may have been an attempt to circumvent" IA 66-80 | Minor | "from other firms" |
| 3.5 | Sep: sameness 41/55 (75%), brand 43 (78%), generic 11 (20%), firm 0 | waves.csv same | OK | — |
| 3.5 | Feb: 30/30 "when in fact it is not"; approval 24 (80%) | 30 (grep); 24 (23 template + 1 quoted) | OK | — |
| 3.5 | Jun: firm 21/25 (84%); 11 letters on "FDA-approved/-licensed" pharmacies | 21; 11 (grep) | OK | — |
| 3.5 | implied approval 24% → 80% → 84% | 13/55 = 23.6%, 80%, 84% | OK | — |
| 3.6 | 94.7% of cells; 16 codes κ ≥ 0.80; eligibility 96.9% (0.77); seller 82.2% (0.70) | 0.9467; 16; 0.969/0.767; 0.822/0.702 | OK | — |
| 3.6 | κ: Rx 0.22, approval 0.34, sameness 0.55, shortage 0.17, salt 0.00 | 0.216, 0.345, 0.550, 0.173, 0.000 | OK | (0.345 rounds to 0.34 or 0.35 depending on convention; fine) |
| 3.6 | 225 disagreements; 220 reader / 5 rules | 191 code + 5 eligibility + 29 seller = 225; 220/5 | OK | — |
| 3.6 | rules-only: Rx 13→68, approval 64→98; others within one letter | sensitivity file same | OK | — |
| 3.7 | close-outs 2, both compounders; 0 response letters | Tailstorm 503B, Thrive 503A | OK | — |
| 3.7 | 85 records, 24 events, 20 firms; 49 (57.6%) sterility; 2025 = 38, 2026 = 27 | same. "20 firms" counts "Carolina Infusion" and "Carolina Infusion, LLC" separately, so the true count is 19. Totals 57+27+1 = 85; no overlap; all records returned | Minor | 19 firms, or say "20 firm names" |
| 4.2 | "three batches account for 71%" | OK | OK | — |
| 4.3 | "siding with its own reading in 220 of 225" | OK | OK | — |
| Table 1 | all n, %, CI, agreement, κ | match prevalence.csv and agreement.csv | OK | Relabel "Mentions drug shortage" (n = 1). Under the codebook definition, roughly 9–10 included letters mention the shortage list. The operational meaning was narrowed in adjudication |
| Table 2 | all 96 cells | match prevalence_by_seller.csv | OK | — |
| Fig 1A | monthly stacks | Sep 2025 bar = 57 (55 batch + Motion Pharmacy + Chengdu); Feb 2026 = 31 (incl. Thrive) | OK | — |
| Fig 1B | recalls by quarter | Bars match from 2024Q2 onward. **12 of the 85 records (2021Q1–2023Q3) fall before the axis start and are not shown** | Caption incomplete | Add "records before Oct 2023 (n = 12) not shown", or extend the axis |
| Fig 2 | heatmap % | matches Table 2 and prevalence_by_seller | OK | — |
| Fig 3A | batch % | matches waves.csv | OK | — |
| Fig 3B / caption | κ and agreement; salt κ 0, 2 discordant | matches | OK | — |
| Graphical abstract | 71%; 49% (76/154); 33% all from 2026 batches; 109 letters | all correct | OK | Title quote issue (below) |
| Title / GA / social summary | "Same as Wegovy" in quotation marks | No letter quotes that phrase as a seller claim. The closest is Zealthy's website question "Is Semaglutide the same as Wegovy and Ozempic?" The typical quoted claim is "Same active ingredient as Ozempic and Wegovy" | **Implied quote not verbatim** | Use a verbatim quote (e.g. "Same active ingredient as … Wegovy"), or explain in the intro that the title paraphrases. "look-alike label claims" in the social summary mischaracterises firm-branded labels; say "labels naming the seller as compounder" |

## 3. Independent re-code of a stratified random sample

**Sample design.** 31 included letters were drawn (`random_state = 13`), stratified by seller group:
- telehealth 9
- clinic/med spa 5
- online pharmacy 5
- research chemical 5
- compounder 4 (Boothwyn 503A; Apothecary, Tailstorm, Genogenix 503B)
- API/other 3, with the Harbin letter forced in, plus Chengdu and New Life Pharma

Rows sampled: 3, 5, 13, 16, 19, 20, 29, 40, 53, 59, 65, 66, 74, 75, 80, 81, 84, 86, 87, 109, 117, 120, 122, 127, 128, 137, 138, 139, 145, 157, 158.

**Method.** I read every full letter body against CODEBOOK.md and the logged reading conventions, and recorded my codes before comparing them with `final_codes.csv`.

**Caveat on blindness.** Before coding I had seen the pass-2 log header and lines 0–50, which cover 8 sampled rows, and the aggregate tables. So this re-code is informed rather than fully blind. Like the original coding, it was also done by an AI model.

**Results.**
- Agreement: 711/713 cells (99.7%).
- Seller type: 31/31.
- 20 of the 22 codes: 31/31 each. This includes all five low-κ codes: Rx (5/5 positives match), implied approval (7/7), sameness (9/9), shortage (0/0) and salt form (0/0).
- Disagreements:
  1. Genogenix `V_503A_conditions`: final 1, auditor 0. The only basis is footnote 7 ("repackaged drugs are not eligible for the exemptions … under 503A and 503B") in a letter to a registered 503B facility. That is a statement of ineligibility, not an FDA finding that 503A conditions were not met. Thrive (rows 503A/503B) was coded the same way in adjudication.
  2. Harbin `V_sterility`: final 1, auditor 0. The only basis is FDA's finding that water used for a non-sterile API intended for sterile products was not tested for endotoxin. The codebook's "endotoxin" keyword makes 1 defensible, but it is not a sterility-assurance failure of a product. It drives "sterility 2/5 (40%)" for API/other.

**Template letters.** In the sample, telehealth/clinic letters are near-template, so κ is uninformative for them. The informative checks were the judgment codes.

**Targeted checks of the low-κ codes across the whole corpus (adjudication log):**
- **Rx (55 disagreements, all rules = 1, reader = 0).** These come from the Feb/Jun footnote that cites 21 CFR 201.1 and 503(b)(1) (rows 89–153) or from definitional text (rows 0, 2, 3, 6). The reader is correct. Final Rx = 1 exactly where the opening lists §503(b) (13/13). In 4 of these letters there is no without-prescription text, so the result describes a citation, not an allegation (see the 3.3 fix).
- **Implied approval (56).** Sep-2025 boilerplate "imply … same as an FDA-approved product" was correctly scored 0. The reader correctly added quoted "authorized by the FDA", "approval from the FDA" and "FDA-licensed" claims. A corpus grep found no included letter with final = 0 that quotes an FDA-approval, registration or licence claim.
- **Sameness (37).** Every reader-positive I inspected quotes "active (pharmaceutical) ingredient in", "main ingredient in", "bioidentical" or "same results". Every reader-negative I inspected is brand-name parentheticals, "clinically proven" or "FDA approval" claims. The adjudication holds up.
- **Shortage (9).** The rules hits are 503B boilerplate. However, the narrowed operational definition was applied inconsistently: the six retatrutide letters make the same "not … on the drug shortage list" statement about the recipient's product as ProRx does (see the 3.2 fix). The codebook definition ("mentions the drug shortage (list) status") also differs from the operational one.
- **Salt form (2).** Rows 0–1 contain only a general footnote. Final 0 is correct.

## 4. Inclusion/exclusion, hash, dates, recalls

**Exclusions.** All 9 decisions were checked by reading the relevant text.
- X1: 3 Lilly OPDP letters and 1 Novo OPDP letter (9 Sep 2025), plus Novo postmarketing ADE reporting (5 Mar 2026). Correct.
- X2: Ralph DeFronzo (GLP-1 only as a clinical-trial exclusion criterion). Correct.
- X2: Veronvy drops, Fantasy Face "GLP-1 Weight Control Oral Solution" (eBay) and Biodrive "Evolv GLP-1 Biomimetic" supplement. These are GLP-1-*branded* products with no incretin ingredient, so the decision is defensible and is disclosed in §2.1. It extends codebook X2 ("no GLP-1 product attributed"), so the codebook should be amended to match.

**Inclusions with fewer than 3 GLP-1 mentions (5).**
- ProRx 696742, Tailstorm, Chengdu and PekCura are correct.
- PQ Pharmacy (row 83) is borderline: semaglutide appears only as one lot in a table. Consider a note.

**Snapshot and dates.**
- Snapshot hash matches (see 1).
- Duplicates: 0 by text hash. The 161 unique company–date pairs reflect the 3 same-day Lilly letters, not duplicates.
- Date and batch statistics all reproduce (timeline.json).

**Recalls.** The openFDA counts reproduce, with all records returned per query and no overlap between queries. Two caveats:
- The firm count includes a name variant (19 actual firms).
- The series also includes approved-brand recalls (e.g. Wegovy temperature abuse), so it is not a compounded-only series. The text does not claim it is, but a sentence would help.
- "Dominated by sterility concerns at a handful of firms": 49 sterility records come from 12 firms, and ProRx, Thrive and Carolina Infusion account for about 30. The claim is acceptable.

## 5. Attribution, naming, current wrongdoing

**Naming.** Firms named in the prose are Novo Nordisk, Eli Lilly and Hims & Hers Health. All are large public companies. The 3 Mar 2026 press release names no firms. No other recipient is named, and Harbin is unnamed. OK.

**Attribution failures:**
- §3.4 "several also sold opioids or other controlled drugs" is stated as fact. Write "FDA said several also offered opioids…".
- §5 Conclusion: "the online pharmacies, peptide sellers and manufacturers **operating outside the law**" is an unattributed finding of illegality, which breaks the paper's own §2.5 rule. **Highest priority.** Suggested wording: "…that FDA alleged were operating outside the approval and compounding framework".
- §4.1 "targets products outside the compounding framework altogether: … and the compounders and API makers…": compounders are inside the framework, so the sentence contradicts itself. Also attribute it ("that FDA alleged…").
- §4.1 "it does not allege that the drugs were unapproved or contaminated" is false for 6 letters (retatrutide). Add "apart from six letters about retatrutide".

**Current wrongdoing.** No sentence implies current wrongdoing. The Hims quote should be dated to the Aug 2025 website review. The §2.5, Responsible use and Transparency caveats are good.

## 6. Overstatements and other methods issues

1. Freeze claim not verifiable (see 1). README and §2.3 assert a pre-pass-2 hash. The freeze file includes the pass-2 log hash and was written with it.
2. The abstract says "every public warning letter in FDA's index that mentioned these drugs". In fact it is letters returned by 11 full-text searches of an index that "changed between searches on the same day" (§4.3). Write "every letter returned by full-text searches…".
3. The codebook still says the rules live in `code/rules.py`; the actual file is `02_rules.py`. It also lists a fifth context code, `F_closeout`, that is not among the 22.
4. The reading-aid files are dated 06:21, after the pass-2 log (06:07), so the shipped aid is a regeneration. This is acknowledged in the README; fine.
5. The §2.3 claim that pass 2 did not look at pass-1 output cannot be verified. It is already partly caveated in §4.3.

## 7. Prioritised fix list

1. **Conclusion "operating outside the law".** Attribute it to FDA. This is a responsible-reporting breach.
2. **Freeze claim (README, §2.3).** Reword. Either the freeze file was regenerated after pass 2 or the claim is unsupported. If an earlier hash record exists, ship it; otherwise say the hashes were recorded together after coding.
3. **§3.2 "Only one … shortage status".** Correct it to the ProRx-versus-retatrutide distinction. Relabel the Table 1 "Mentions drug shortage" row, or recode the six retatrutide letters and update n, κ and agreement accordingly.
4. **Abstract "(22 letters)".** Change to 16, or drop it.
5. **Rx wording.** "Dispensing without a prescription 13" and "12" should become "cited §503(b)", with 9 explicit no-prescription allegations (8 online pharmacies, 1 research seller).
6. **§4.1 corrections.** Add "except six retatrutide letters", and fix the "outside the compounding framework … compounders" contradiction.
7. **§3.4 opioid sentence.** Attribute it to FDA.
8. **Title and graphical-abstract quote.** "Same as Wegovy" is not verbatim. Use a verbatim claim or explain the paraphrase. Fix "look-alike" in the social summary.
9. **Fig 1B.** Disclose the 12 recall records outside the axis.
10. **Footnote-based codes.** Disclose that 503A/503B conditions for Genogenix and Thrive rest on a repackaging footnote, and that Harbin's sterility code rests on water endotoxin control. Or recode them: 503A for compounders would go 3 → 2, and sterility for API/other 2 → 1.
11. **Minor fixes:**
    - recall firms: 19, not 20
    - Harbin: "from other firms"
    - abstract scope wording
    - abstract "same active ingredient" → "sameness"
    - press-release match: "consistent with"
    - codebook: X2 wording, file name, F_closeout
    - add the openFDA file hash
    - note the PQ Pharmacy inclusion
