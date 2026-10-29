# "Same active ingredient" — reproducibility package

Kalafatis, P. (2026). *"Same active ingredient": what FDA warning letters allege about compounded GLP-1 sellers* [Preprint]. x9m8.com.

A systematic content analysis of all public FDA warning letters in FDA's warning-letter index that mention semaglutide, tirzepatide or related GLP-1 terms (snapshot of 21 October 2026, US Eastern time).

## Contents
- `code/` — Python 3.13 (pandas, NumPy, BeautifulSoup, scikit-learn, statsmodels, matplotlib).
  - `CODEBOOK.md` — eligibility rules, seller-type hierarchy, violation/claim/context codes (written before coding; left unchanged). `CODEBOOK_AMENDMENTS.md` — definitions clarified after coding and audit.
  - `common.py` — paths, policy event dates, code labels.
  - `01_build_corpus.py` — parses the frozen snapshot; writes letter texts (`data/letters/`), `results/corpus_index.csv` (index metadata + SHA-256 of each letter text and raw page) and `results/snapshot_manifest.json`.
  - `02_rules.py` — pass 1: deterministic regex coder → `data/coding/pass1_rules.csv`. Written before pass 2 and not run until pass 2 was finished. Its SHA-256 and the codebook's are in `data/coding/frozen_before_pass2.sha256`, but that file was written at the end of pass 2 (it also holds the pass-2 log hash), so it shows the files did not change after coding; it does not by itself prove they were fixed before reading.
  - `03_parse_pass2.py` — pass 2 (reading log `data/coding/pass2_reader_log.txt`, with the reading conventions adopted during coding) → `data/coding/pass2_reader.csv`.
  - `04_agreement.py` — percent agreement and Cohen's κ per variable → `results/agreement.csv/.json`, `data/coding/disagreements.csv`.
  - `05_adjudicate.py` — adjudication decisions with reasons, including logged post-audit recodes (6 shortage codes, 1 sterility code) → `data/coding/adjudication_log.csv`, `results/final_codes.csv`.
  - `06_analysis.py` — flow, prevalence (Wilson CIs), by seller type, timeline, batches, close-outs, openFDA recalls, rules-only sensitivity, open dataset.
  - `figures.py`, `tables.py`, `graphical_abstract.py`, `style.py`.
- `results/` — all numbers reported in the paper. `open_dataset.csv` lists all 163 retrieved letters with URL, dates, hashes, eligibility and codes.
- `figures/`, `manuscript/`, `out/` (Word and PDF).

## Data sources (public, US government works)
- FDA warning-letter index, JSON source used by the Warning Letters page:
  `https://www.fda.gov/datatables/views/ajax?search_api_fulltext=<term>&view_display_id=warning_letter_solr_block&view_name=warning_letter_solr_index&start=0&length=1000`
  Terms: semaglutide, tirzepatide, retatrutide, Ozempic, Wegovy, Mounjaro, Zepbound, GLP-1, liraglutide, cagrilintide, incretin. Letter pages: `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/<slug>`.
  Pulled 2026-10-22 01:43–01:45 UTC from a browser session on fda.gov (the endpoint blocks scripted clients). Snapshot file `data/raw/fda_wl_snapshot_2026-10-21.json`, SHA-256 `e9176b7f9317d38a653405ab5bc1758b95d460e768c6af3ec104a0403a924084`.
- openFDA drug enforcement API: `https://api.fda.gov/drug/enforcement.json?search=product_description:<term>&limit=1000` (semaglutide, tirzepatide, retatrutide), pulled 2026-10-22; file `data/raw/openfda_enforcement_glp1_2026-10-22.json`, SHA-256 `017252792a2cc59c3ade04c09985e6acee6c3540b0b99d1fce963e73d2809393`. Includes recalls of approved branded products.
- FDA pages cited for policy dates and the 3 March 2026 press release (see manuscript references).

FDA content is a US government work and not subject to copyright; the snapshot and letter texts are included so that results can be reproduced exactly. The FDA index changes over time: a re-pull will not necessarily return the same letters.

## Responsible use
Warning letters are FDA allegations, not adjudicated findings. A firm listed in `open_dataset.csv` may have disputed the allegations, corrected the issues or received a close-out letter not shown in the index. Do not describe any listed firm as having violated the law on the basis of this dataset. Corrections: x9m8x7@gmail.com.

## Run
    cd code && python3 01_build_corpus.py && python3 02_rules.py && python3 03_parse_pass2.py && python3 04_agreement.py && python3 05_adjudicate.py && python3 06_analysis.py && python3 figures.py && python3 tables.py && python3 graphical_abstract.py
    bash ../../build_docs.sh   # Word + PDF (pandoc, python-docx, LibreOffice)

## AI use and limitations of the coding
All coding (rule writing, the reading pass and adjudication) was done by Claude (Anthropic, claude-opus-5-5) in October 2026 under the author's direction; no human coder took part and no protocol was pre-registered. The reading pass used a reading aid that replaced sentences repeated verbatim in four or more letters with tags (`code/reading_aid.py`; output in `data/coding/reading_aid/`; tag numbers for tied sentences may differ between runs, the set of tagged sentences does not). The author reviewed the outputs and is responsible for the content.
