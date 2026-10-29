# Number audit, round 2: "Bags and the body" (revised manuscript.md)

Auditor: independent agent, 2026-10-21. Nothing in the package was edited. No network used.

**Method.** effects.py, evidence_map.py, figures.py, tables.py and graphical_abstract.py were re-run on a scratch copy. All result files, the `## Tables` section and all four PNGs are byte-identical to the shipped versions, so text-independent outputs are in sync with the data. Every number in the abstract, social summary, §1–5, Tables 1–2 and captions was checked against map_summary.json, effects_summary.json, effects_all.csv, map_cells.csv, map_coding.csv, studies.csv, extraction.csv and search_log.md. The in-text citations and the reference list were cross-matched by script (22 = 22, no orphans either way).

**Overall.** Most high-priority fixes are in, and the reported numbers now match the result files. The main remaining items are: §4.4 still says 41 of 65 not read in full (should be 47); the map-coding gaps from round 1 were only partly fixed; the pain claim is still unhedged in the abstract, §3.1 and the graphical abstract; and several Table 1 and minor wording fixes were not made.

## 1. Status of round-1 fixes

### Number audit fix list

| # | Fix | Status | Remaining issue / fix |
|---|---|---|---|
| 1 | 24 vs 18 full texts | PARTLY DONE | Abstract, §2.3 and Fig 1 are fixed. **§4.4 still says "Forty-one of 65 reports could not be read in full"**: 47 of 65 were not read in full (41 abstract-only + 6 abstract/partial). Fix: "Forty-seven of 65 reports were not read in full (41 with no full text obtained, 6 assessed from abstract or partial text)…". Also §3.1 says "7 were excluded at full text", but 2 of those 7 (Presta2020, Mache_ISBS) were assessed from the abstract or partial text: "7 were excluded after detailed assessment". |
| 2 | Novelty claim; cite Gai and SSRC; consistent review screening | PARTLY DONE | Badawy 2018 and Gai 2025 are cited and the sentence is narrowed. The SSRC conference-abstract review is not mentioned. Review screening is still inconsistent: Guleria and Ellapen were taken to detailed assessment, while Gai and SSRC were dropped at title screening (search_log unchanged). Fix: add one clause on the SSRC abstract, and one line in §2.3 or §4.4 on how reviews were handled. |
| 3 | Cross-body hedging; add Cho2013 | MOSTLY DONE | §3.2 and §4.1 are good, and Cho 2013 is added (n = 30, static, no no-load; matches studies.csv). The **abstract** still says "a cross-body bag produced a smaller trapezius rise", with no mention that there was no direct test. Fix: "…was associated with a smaller trapezius rise (g 0.51 vs 1.25; not tested directly)". |
| 4 | Son2013 coding and recount | DONE | Son2013 is coded gait. One-shoulder is 30, not the predicted 32, because Rafi2026 and Li2018 were moved to non-bag. Text, map_summary and Fig 2 agree (30/17/16/8; gait 20). |
| 5 | map_coding gaps | PARTLY DONE | Done: n for Presta (1), Pascoe (10) and Cho (30); populations for Oja and Angelini; Bergmann moved off "unclear". **Not done:** Hyun2018 balance (Table 1 lists "balance" for Hyun, so the table and the map disagree); Bampouras balance; Matsuo coordination; Zhang2010, Kellis2009 and Hong2005 kinetics; deVette kinetics/kinematics; Presta still "posture" (title: gait swing phase, pelvic tilt); n still blank for full-text records Son2013, Wang2021, Ramadan2018 and deVette2014; Wang2018a/b, Wang2020, Lee2014/2016 and Shi2015 still "non-bag" without support. Recoding would change §3.1 counts (balance about 9, coordination 3, kinetics about 12–13, gait 21) and Fig 2. Fix: finish the coding, then re-run evidence_map.py and figures.py and update §3.1. |
| 6 | Load range 28–30% | DONE | — |
| 7 | "treadmill" → "laboratory" | DONE | — |
| 8 | "Gait responded to load more than style" | DONE (removed) | — |
| 9 | Yoon strap length | DONE | — |
| 10 | Occupational records | DONE | "Seven records…" matches field_studies = 7. |
| 11 | "about one SD" | DONE | §4.1: "about one SD in the trapezius and 0.6 to 0.95 in the back muscle" (data 0.94–1.25 and 0.59–0.95). Conclusion has no SD claim. |
| 12 | Pain hedge; Lin Part I | PARTLY DONE | §4.2 is hedged, and the Conclusion says "not tested experimentally". **Still unhedged:** the abstract ("no study measuring pain"), §3.1 ("None measured pain or musculoskeletal symptoms") and the graphical abstract ("0 of 60 charted"). Field and comfort work (Lin et al. Part I) is still not acknowledged. Fix: "none, as far as full texts or abstracts show"; add one sentence in §4.2 on Lin Part I. |
| 13 | Fig 1 numbers | DONE | 24 (18 in full text); 41 (40 charted; 1 duplicate); 8 adult with SDs. |
| 14 | Fig 3 bag-side outlines; 4.6 label | PARTLY DONE | The label no longer overlaps (fixed). The caption is reworded to "strap or load side as labelled by the study authors", but (a) "(strap side)" in the Hardie outcome names was added by the extractor, not the authors; (b) for Hardie cross-body, strap-side ES (g 0.31) is outlined but the load-side right ES (g 0.49) is not; (c) side-specific non-EMG outcomes (Rodrigues L/R step/stride by carry side, Hyung left pelvic tilt) are never outlined, though the caption implies all strap/load-side measures are. Fix: caption "Outlined dots are muscle-activity measures on the strap side", or recode bag_side. |
| 15 | Fig 2 caption | NOT DONE | The caption still says "the blue disc is the number of included full-text studies". The printed number is all records, and blue disc area is the included count. Where they are equal (cross-body angles 1/1, hand-carried angles 2/2) the yellow disc is hidden. The legend ("number shown") partly helps. Fix: "blue disc area ∝ included full-text studies; the number is all records". (The 1 "unclear" record no longer exists, so that part is moot.) |
| 16 | Table 1 cells | PARTLY DONE | Done: Sussman 5.9 kg; Tseng & Liu; Hyun & Ryew. **Not done:** Suzuki loads (4.0 kg shoulder / 4.8 kg cross-body; these are not in extraction.csv either); Rodrigues "143 right- and 61 left-shoulder carriers"; Corrigan "small hockey bag" (also asked by citation audit #12). The legend still defines "NR", which is no longer used in any cell: drop it. |
| 17 | Hyun & Ryew reference | DONE | — |
| 18 | Shin age; Tseng stairs | PARTLY DONE | Tseng done. §3.1 still says "one [studied] women over 75". Fix: "women with a mean age of 81" (Table 1 already says 81 y). |
| 19 | "OA but not retrieved (4)" | DONE | — |
| 20 | Hardie one-strap rucksack; disclosures | PARTLY DONE | Sussman abstract/table discrepancy is disclosed in §4.4. Hardie's one-strap rucksack condition is still neither extracted nor justified (extraction.csv has only one-shoulder and cross-body conditions). The Corrigan thesis table issue (identical stride lengths, small bag only) is not disclosed. |
| 21 | Code | PARTLY DONE | The variance formula is fixed: effects.py now uses (1/n + g²/2n)·2(1−r), and the §2.5 text matches. Not done: §2.5 still does not state df = n − 1 for Hedges' J; Tseng non-conversion still relies on the dispersion string "SD (marginal…)" ≠ "SD". |
| 22 | §4.2 handbag/briefcase comparison | NOT DONE | "heavier than most handbags and close to a loaded laptop briefcase" is still unsourced. Fix: cite a source, or mark it as an estimate ("probably heavier than…"). |

### Citation audit fix list

| # | Fix | Status | Note |
|---|---|---|---|
| 1 | Novelty sentence, Badawy and Gai | DONE | See number fix 2 for SSRC. |
| 2 | Corrigan ES wording | DONE | Values 1.07–1.32 match extraction. |
| 3 | Sussman load | DONE | — |
| 4 | Two-author citations | DONE | Shin & Yoo, Tseng & Liu and Hyun & Ryew are correct in text, Table 1 and the references. |
| 5 | Full reference metadata; add Corrigan & Li | DONE | The list matches the round-1 corrected list. |
| 6 | Stairs wording | DONE | — |
| 7 | Abstract "roughly halved" | DONE / see above | Replaced, but the abstract still needs "not tested directly". |
| 8 | NV items | OPEN | Cannot be checked offline: Yoon methods; Corrigan table/SE; Shin values; Hyun details; Ozgul 15% BW and all-male; Tajik SDs. |
| #12 | "hockey bag" | NOT DONE | Table 1 says "Shoulder-carried sports bag". |

## 2. New or remaining number issues (abstract, social summary, §2–5, tables, captions)

| Location | Issue | Fix |
|---|---|---|
| §4.4 | "Forty-one of 65 reports could not be read in full" (see fix 1) | 47 of 65 |
| Abstract, graphical abstract | "a median of 15.5 participants per study": the median covers only the 32 records with n coded, including single-case Presta (n = 1) | "median 15.5 (32 records reporting n)" |
| Abstract, §3.1, graphical abstract | Pain claims unhedged (see fix 12) | Hedge |
| Abstract | Cross-body "produced a smaller rise" (see fix 3) | Add "not tested directly" |
| §3.1 | Coordination (2 records) not mentioned in the outcome list | Add "coordination (2)" |
| §3.1 | "women over 75" | "mean age 81" |
| §3.1 | "7 were excluded at full text": 2 were not read in full | "after detailed assessment" |
| §3.3, Table 1 | Rodrigues "143 and 61" sides not named | Name the sides |
| Table 1 vs map | Hyun outcomes include balance in Table 1 but not in map_coding | Add balance to the coding |
| search_log.md flow table | Still says "Full texts assessed 24" and "9 adult with extractable mean + dispersion", which conflicts with Fig 1 (18 in full text; 8 with SDs) | Update the log (package consistency) |
| §4.1 | "Gait changes … grow steadily with heavier ones" rests on one study (Corrigan) | "in one study, grew with heavier loads" |

Checked and correct: 12 queries / 936 / 789 / 9 / 798 / 733 / 65 / 41 / 24 / 18 / 6 / 11 / 13; 60 charted (65 − 2 reviews − 1 model − 2 duplicates); 13/7/40; populations 45/5/10; bags 30/17/16/8; outcomes 20/11/9/9/7/7/6/1/1; k = 32, median 15.5, range 1–258; field 7; trapezius g 0.94–1.25; ES 0.59–0.95; Hardie 3.57→8.31, cross-body 4.69, g 0.51; Corrigan DS 26.2→27.7/29.5/31.1, g 0.36/0.95/1.40; Rodrigues −0.17 to 0.38; Hyung 36, −0.87 to 1.38; Tseng 149/141, 15.5/11.2; Negrini ~17%; Fig 3 caption 8 studies, 89 outcomes, g = 4.6; all 18 Table 2 rows; Table 1 ages (Hardie 20.6→21, Yoon 22.65→23, Hyung 20.68→21, Shin 80.9→81, Tseng 22.4→22).

## 3. Citations

All 22 in-text citations have reference entries, and all 22 references are cited (Hyun & Ryew only in Table 1, which is acceptable). New references since round 1 (Borenstein 2009, Cho 2013, Qureshi & Shamus 2012) were not verified against Crossref (no network). The Cho DOI 10.1589/jpts.25.1129 and title match studies.csv. The Qureshi DOI (10.46743/1540-580X/2012.1415) and pages and the Borenstein DOI should be checked online before submission.

## 4. Figures

| Figure | Issue | Fix |
|---|---|---|
| Fig 1 | Numbers correct (936/789, 9, 798, 733, 65, 24 (18 in full text), 41 (40 charted; 1 duplicate), 13 (8 adult with SDs, 2 adolescent), 11). No overlaps. | — |
| Fig 2 | Counts match map_cells.csv. Caption still describes the blue disc as "the number" (see fix 15). The figure will change once the coding gaps are fixed. | Fix the caption; regenerate after recoding |
| Fig 3 | Panel counts 2/24, 2/39, 4/26 match. The 4.6 label is now clear of the CI bar. Outline coding is still inconsistent with the caption (see fix 14). | Narrow the caption or recode |
| Graphical abstract | Values match (60; 13; 15.5; 0.94–1.25; 0.59–0.95). "0 of 60 charted" pain is unhedged, and the median lacks "of 32 reporting n". | Hedge; add the k |
