# Fewer employers, more firms without payroll: US leather and allied product manufacturing, 2004–2023 — reproducibility package

Kalafatis, P. (2026). *Fewer employers, more firms without payroll: US leather and allied product manufacturing, 2004–2023* [Preprint]. x9m8.com.

## Contents
- `data/raw/` — extracted NAICS 316, manufacturing (31-33) and all-industry rows from the Census files (the "raw" input of the code). `data/source_files.csv` — URL, bytes, SHA-256, Last-Modified, retrieval date for all 41 source files (+ the 2007 state file; the 2007 national NES file was rejected by the server).
- `code/` — Python 3.13 (pandas, NumPy, matplotlib). Run in this order: `build_series.py` → `analysis.py` → `figures.py` → `graphical_abstract.py` → `tables.py`. `common.py`, `style.py` are shared.
- `results/` — `series_aggregate.csv`, `series_subindustry.csv`, `series_employer_harmonised_groups.csv`, `size_distribution.csv`, `flags_summary.csv`, `concordance_observed_codes.csv`, `summary.json` (every number in the text), `tables.md`, `provenance.md`. **`results/dataset/`** is the citable open dataset (CC0) with `DATA_DICTIONARY.md`.
- `figures/` — fig1_indexed_series, fig2_nonemployer_share, fig3_size_distribution (PNG 300 dpi + PDF), graphical_abstract.png (900×420).
- `manuscript/`, `out/` (docx and PDF), `audits/`.

## Data sources (public, no key)
- County Business Patterns national files: https://www2.census.gov/programs-surveys/cbp/datasets/<year>/cbp<yy>us.txt (2004–2007) or .zip (2008–2023)
- Nonemployer Statistics national files: https://www2.census.gov/programs-surveys/nonemployer-statistics/datasets/<year>/historical-datasets/nonemp<yy>us.txt (2004–2015) or .zip (2016–2024); 2007 from nonemp07st.txt (state file) summed.
Licence: US Census Bureau data are US government works. The extract and derived files here are released CC0 1.0. Full raw files are not redistributed (URLs and hashes in `data/source_files.csv`).

## How the extraction was done
The shell could not reach www2.census.gov, so each file was fetched with JavaScript in a browser tab on www2.census.gov (2 November 2026), hashed in the browser, unzipped there, and only the NAICS 316, 31-33 and all-industry rows were kept and copied out; the two extract CSVs' SHA-256 values were compared with the in-browser originals (see `results/provenance.md`). The analysis ran locally.

## Run
    cd code && python3 build_series.py && python3 analysis.py && python3 figures.py && python3 graphical_abstract.py && python3 tables.py

AI use: data retrieval, code and drafting assisted by Claude (Anthropic, claude-sonnet-5-5), November 2026; the author reviewed all outputs.
