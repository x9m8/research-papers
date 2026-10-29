# Drive-thru dose–response — reproducibility package

Kalafatis, P. (2026). *Drive-thru dose–response: GLP-1 uptake and US restaurant employment* [Preprint]. x9m8.com.

County-level association between Medicare Part D GLP-1 receptor agonist uptake (2019–2024) and QCEW employment, establishments and wages in limited-service (NAICS 722513) and full-service (722511) restaurants, 2015–2025, with pharmacies, accommodation and grocery as comparison industries, minimum detectable effects, and a benchmark scaled from household-panel evidence.

## Contents
- `code/` — Python (pandas, NumPy, SciPy, matplotlib). Run in this order:
  1. `fetch_data.py` — downloads and reduces the public inputs into `data/raw/` (needs internet and `requests`).
  2. `build_panel.py` — ZIP→county mapping, county GLP-1 uptake by year, QCEW outcomes → `data/derived/`, `results/build.json`.
  3. `analysis.py` — long differences, robustness, event studies, pre-trend tests, descriptives → `results/estimates.json`, `event_study.json`, `descriptives.json`.
  4. `state_secondary.py` — state card-spending check → `results/state_secondary.json`.
  5. `bounds.py` — ratios to the household benchmark and national figures quoted in the text → `results/bounds.json`.
  6. `figures.py`, `tables.py`, `graphical_abstract.py` — figures (300 dpi PNG + PDF) and the Tables section of the manuscript.
  - `common.py` — paths, constants, the fixed-effects OLS with state-clustered standard errors, MDE and Wald helpers. `style.py` — figure style.
  - `fetch_browser.js` — the browser version of step 1 actually used (see "How the results were produced").
- `results/` — result files; `results/provenance.md` lists input file sizes and hash prefixes and result-file SHA-256 hashes.
- `manuscript/` — `manuscript.md`, `patch_docx.py`; `out/` — Word and PDF; `figures/`.

## Data sources (public; not redistributed)
| File in `data/raw/` | Source |
|---|---|
| `partd_glp1_npi_YYYY.csv` (2019–2024) | CMS, Medicare Part D Prescribers – by Provider and Drug, data API https://data.cms.gov/data-api/v1/dataset/{id}/data filtered by `Gnrc_Name` (ten GLP-1 generic names; dataset ids in `fetch_data.py`); prescriber ZIP added from the by-Provider file |
| `partd_provider_zip_YYYY.csv` | CMS, Medicare Part D Prescribers – by Provider (`Prscrbr_NPI`, `Prscrbr_Zip5`, `Tot_Clms`), summed to ZIP |
| `partd_geo_glp1_YYYY.csv` | CMS, Medicare Part D Prescribers – by Geography and Drug (national and state rows for the same generic names) |
| `medicare_enrollment_county.csv` | CMS, Medicare Monthly Enrollment, county, annual rows |
| `qcew_{722511,722513,446110,456110,721,445110,10}.csv` | BLS QCEW open-data API, `https://data.bls.gov/cew/data/api/{year}/a/industry/{naics}.csv`, county rows, private ownership |
| `zcta_county_2020_maxland.csv` | US Census Bureau, 2020 ZCTA-to-county relationship file, https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt, reduced to the county with the largest land-area overlap |
| `affinity_state_monthly.csv` | Opportunity Insights Economic Tracker, `data/Affinity - State - Monthly.csv`, GitHub commit 8048afb24d87af54426014d341959c5c262f87da |

Licences: CMS, BLS and Census data are US government works in the public domain. The Opportunity Insights tracker data are published for public use under the terms in its repository (https://github.com/OpportunityInsights/EconomicTracker); cite Chetty et al. (2024). Code in this package: MIT licence.

## How the results were produced
The analysis environment had no direct internet access. The inputs were fetched on 22 October 2026 in a Chrome tab on data.bls.gov with `fetch_browser.js` (CMS and GitHub allow cross-origin requests; the Census file was reduced on census.gov and carried over in the URL fragment). The Python scripts above were written to a Pyodide 0.26.4 file system in the same tab (Python 3.12, pandas 2.2.0, NumPy 1.26.4, SciPy 1.12.0) and run unchanged; their SHA-256 hashes were checked against the files in `code/`. The result JSON files were copied back and verified byte for byte (hashes in `results/provenance.md`). `bounds.py`, figures and tables were then run locally (Python 3.13, pandas 3.0.5). Running `fetch_data.py` should reproduce the inputs, subject to later revisions of the CMS and BLS files.

## Run
    cd code && python3 fetch_data.py && python3 build_panel.py && python3 analysis.py && python3 state_secondary.py \
      && python3 bounds.py && python3 figures.py && python3 tables.py && python3 graphical_abstract.py

AI use: data retrieval, analysis code and drafting assisted by Claude (Anthropic, claude-opus-5-5), October 2026; the author reviewed all outputs.
