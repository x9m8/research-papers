# Retractions in nutrition and obesity research — reproducibility package

Kalafatis, P. (2026). *Retractions in nutrition and obesity research: reasons, timing and citations* [Preprint]. x9m8.com.

Describes retractions in nutrition and obesity research in the Retraction Watch database distributed by Crossref (data to 28 October 2026): counts over time, reasons, time from publication to retraction, author countries and citations after retraction (OpenAlex). Each is compared with the rest of the database and the rest of its biomedical part, and tested against several definitions of the field.

## Contents
- `code/` — Python (pandas, NumPy, matplotlib). Run in this order:
  1. `fetch_data.py` — downloads `retraction_watch.csv` at commit 827665a into `data/raw/` and checks its SHA-256 (needs internet and `requests`).
  2. `select_records.py` — retractions only, deduplicated; field-definition flags (S subject code, J journal title, K article title, F food-science journals), GLP-1/anti-obesity-drug title flag, reason groups, dates → `data/derived/records.csv` (record level, not redistributed), `results/selection.json`, `results/unmapped_reasons.json` (reasons not mapped to any group, counts only).
  3. `analysis.py` — trends, reasons, time to retraction, countries, publishers, field vs rest of database (all retractions and journal articles only, i.e. conference papers excluded from both sides — the main comparison), vs rest of biomedical, with Hindawi excluded, by period, broader misconduct mapping, sensitivity to the definition → `results/trends.json`, `comparison.json`, `sensitivity.json`.
  4. `citation_sample.py` — field DOIs retracted 2012–2023 and a year-matched random sample of other biomedical retractions (2 per field record) → `data/derived/citation_dois.json`.
  5. `fetch_openalex.py` — OpenAlex lookups → `data/derived/openalex.json` (needs internet; `fetch_openalex.js` is the browser version actually used).
  6. `citations.py` — post-retraction citation measures → `results/citations.json`.
  7. `summary.py`, `figures.py`, `tables.py`, `graphical_abstract.py` — derived numbers, figures (300 dpi PNG + PDF), the Tables section of the manuscript (`results/tables.md`), graphical abstract.
  - `common.py` — paths, field rules, reason-group mapping, helpers. `style.py` — figure style. `restore_results.py` — helper used once to write back result files copied from the browser.
- `audits/` — independent number and citation audits; their fixes are applied in version 2.
- `results/` — aggregate result files only; `results/provenance.md` lists input, code and result hashes.
- `manuscript/` — `manuscript.md`, `patch_docx.py`; `out/` — Word and PDF; `figures/`; `audits/`.

## Data sources and licences
| Data | Source | Licence |
|---|---|---|
| Retraction Watch database (`retraction_watch.csv`, 67,716,155 bytes, SHA-256 7020113802228518d52d8da3b64ed3a30c59e37e828d8377bce72a5cbad7c303) | Crossref, https://gitlab.com/crossref/retraction-watch-data, commit 827665ab699e4a798060b95c40268de417b7f2e1 ("Retraction Watch data for 2026-10-28"); documentation https://crossref.org/documentation/retrieve-metadata/retraction-watch/ | **No licence is stated** in the repository or on the documentation page. Crossref describes the retractions as "freely available" and asks for "a citation to the source" (Crossref blog, 29 January 2025). Data compiled by Retraction Watch (Center for Scientific Integrity); acquired and opened by Crossref in September 2023. |
| OpenAlex works (`counts_by_year`, `cited_by_count`, `is_retracted`) | https://api.openalex.org/works, queried 29 October 2026 | CC0 |

**Not redistributed:** the raw CSV, the record-level derived file (`records.csv`), the citation sample DOIs and the OpenAlex responses. Because no licence is stated for the Retraction Watch data, this package ships only code and aggregate tables. To rebuild the record list of the 716 primary-definition retractions, run steps 1–2 and filter `data/derived/records.csv` on `primary == True` (or `broad`, `S`, `J`, `K` for the other definitions). The selection is deterministic for a given commit.

Code in this package: MIT licence.

## How the results were produced
The analysis environment had no direct internet access. The CSV was fetched on 29 October 2026 with JavaScript in a Chrome tab from the GitLab API at the commit above. Steps 2–4 and 6 were run unchanged in Pyodide 0.26.4 (Python 3.12.1, pandas 2.2.0, NumPy 1.26.4) in the same tab after their SHA-256 hashes were checked against the files in `code/`, and step 5 was run there as `fetch_openalex.js`. Only aggregate result files were copied back, and each was verified byte for byte against its in-browser hash (`results/provenance.md`). Step 7 was run locally (Python 3.13, matplotlib). Re-running from a later commit, or querying OpenAlex later, will give somewhat different numbers.

## Run
    cd code && python3 fetch_data.py && python3 select_records.py && python3 analysis.py && python3 citation_sample.py \
      && python3 fetch_openalex.py && python3 citations.py && python3 summary.py && python3 figures.py && python3 tables.py \
      && python3 graphical_abstract.py

## Please cite the data as
Crossref & Retraction Watch. (2026). *Retraction Watch data* (commit 827665ab699e4a798060b95c40268de417b7f2e1) [Data set]. https://gitlab.com/crossref/retraction-watch-data

AI use: data retrieval, analysis code and drafting assisted by Claude (Anthropic, claude-opus-5-5), October 2026; the author reviewed all outputs.
