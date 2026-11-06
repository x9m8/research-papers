# Enterococcus exceedances, closures, and rainfall at NY State Park beaches — reproducibility package

Kalafatis, P. (2026). *Enterococcus exceedances, closures, and rainfall at New York
State Park beaches on Long Island: Eleven bathing seasons at 15 OPRHP beach stations,
2015–2025* [Preprint]. x9m8.com.

## Scope

This package covers the 15 beach stations the New York State Office of Parks,
Recreation and Historic Preservation (OPRHP) operates on Long Island (Jones Beach,
Robert Moses, Sunken Meadow, Heckscher, Wildwood, Orient Beach, Hither Hills), for
the 2015–2025 bathing seasons. It does **not** cover the beaches Nassau County,
Suffolk County, or individual towns operate and test independently — no comparable
public bulk dataset or API with adequate historical coverage was found for those in
this round of work — and it does not extend before 2015. See the manuscript's
Limitations section for the full discussion.

## Contents

- `code/` — Python 3.12/3.13 with pandas, NumPy, SciPy, statsmodels and matplotlib.
  - `common.py` — paths, the 104 CFU/100 mL threshold, the beach-to-rain-station
    assignment, waterbody groupings.
  - `fetch_browser.js` — the exact JavaScript, run in a Chrome tab (not in this
    sandbox's shell, which has no general internet access), that fetched the raw
    data directly from the Open Data NY and NOAA NCEI REST APIs and loaded it into
    an in-browser Pyodide (Python-in-WebAssembly) runtime.
  - `build_panel.py` — cleans the raw rows, classifies exceedances, assigns rainfall
    features (same-day, 48h, 72h cumulative), and forward-fills the beach-status log
    into a daily closure/advisory timeline, excluding seasonal/administrative closures
    (`Closed for end of season`, `Preseason`).
  - `analysis.py` — descriptive tables, the beach-fixed-effects logistic regressions
    (trend and rainfall), and the closure/advisory breakdowns → the five `results/*.json`
    files.
  - `trend_pvalues.py` — a small local (non-browser) post-processing step that adds
    Wald p-values for the by-waterbody year-trend coefficients already in `trends.json`.
  - `style.py`, `figures.py`, `tables.py`, `graphical_abstract.py`.
- `results/` — the five result JSON files, `tables.md`, and `provenance.md` (full
  chain of custody: what was fetched, what was computed where, and SHA-256 hashes for
  every input, derived, and result file, including a transparent note on a correction
  made during the build — see "Revision during the build" in `provenance.md`).
- `figures/` — `fig1_annual_exceedance`, `fig2_by_beach`, `fig3_rainfall` (PNG + PDF,
  300 dpi) and `graphical_abstract.png`.
- `manuscript/manuscript.md`, `patch_docx.py`; `../out/` holds the built `.docx`/`.pdf`.

## Data sources and licenses

- **OPRHP beach water quality testing** (dataset `wwwd-za77`, data.ny.gov / Open Data
  NY): https://data.ny.gov/d/wwwd-za77. The dataset's own Socrata license field is
  "unspecified" (no dataset-specific badge was selected); it is governed instead by
  the platform-wide **OPEN-NY Terms of Use**
  (https://data.ny.gov/download/77gx-ii52/application/pdf, last modified March 8,
  2013), which grants "a non-exclusive, revocable license to use the Content" and
  states that it imposes "no restrictions requiring... attribution... share-alike or
  technical restrictions, nor require... pre-approval before re-use," conditioned on
  lawful, non-malicious use. Re-confirmed directly on 2 November 2026 (metadata API
  call + in-browser PDF text extraction); the verbatim text and exact URLs are in
  `results/provenance.md` under "License verification."
- **NOAA NCEI GHCN-Daily**, Access Data Service v1:
  https://www.ncei.noaa.gov/access/services/data/v1, stations USW00094789 (JFK
  International Airport) and USW00004781 (Islip-LI MacArthur Airport). A U.S.
  government work, public domain.

## What is not included, and why

`data/raw/*.json` (the ~3,301 raw beach rows and the two stations' daily rainfall,
totalling roughly 2.3 MB) and `data/derived/*.csv` (the cleaned sample table and the
forward-filled status timeline) are **not** shipped in this package. This is a
build-environment limitation, not a licensing one: both source licenses permit
redistribution. The data were fetched directly in a Chrome browser tab by
cross-origin `fetch()` (the sandbox shell used to assemble this package has no
general internet access), analysed there in an in-browser Pyodide runtime, and only
the small aggregate result files were copied back to this package as plain text; the
~900-character-per-call transfer used for that is impractical for files of this size.
`provenance.md` documents the SHA-256 hash of every raw and derived file, computed
in-browser with the Web Crypto API, so the pipeline's output can be checked for exact
reproduction. `data/raw/beach_water_testing_li.json` can be reconstructed exactly by
re-running `code/fetch_browser.js` in a browser against the stable, versioned Open
Data NY and NOAA NCEI APIs, and `data/derived/*.csv` by then running `build_panel.py`
on it.

## Run (once the raw files above are in `data/raw/`)

    cd code && python3 build_panel.py && python3 analysis.py && python3 trend_pvalues.py \
      && python3 figures.py && python3 tables.py && python3 graphical_abstract.py
    cd .. && bash ../build_docs.sh   # pandoc -> patch_docx.py -> soffice PDF

AI use: data retrieval, analysis code, and drafting assisted by Claude (Anthropic,
claude-sonnet-5), November 2026; independent AI agents checked every number against
the result files and every citation against its source; the author reviewed all
outputs.
