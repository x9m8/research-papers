# Long Island minimum wage and restaurants — reproducibility package

Kalafatis, P. (2026). *Regional minimum wages and restaurant employment on Long Island, New York* [Preprint]. x9m8.com.

Compares restaurant employment, establishments and average weekly wages in Nassau and Suffolk counties (Long Island) with upstate New York counties, 2014Q1–2026Q1, using New York's regional minimum-wage schedule (Long Island & Westchester vs rest of state, from 31 Dec 2016), with placebo inference over random halves of the comparison counties, a synthetic control, and county panels including Pennsylvania.

## Contents
- `code/` — Python (pandas, NumPy, SciPy, matplotlib). Run in this order:
  1. `fetch_data.py` — downloads the BLS QCEW quarterly industry files and reduces them to `data/raw/qcew_ny_nj_pa_quarterly.csv` (needs internet and `requests`).
  2. `build_panel.py` — county-quarter panel and quarterly minimum-wage schedule → `data/derived/`, `results/build.json`.
  3. `analysis.py` — gap paths, window differences, elasticities, placebo inference, robustness, synthetic control, county panels, 2017Q1 break check → `results/estimates.json`, `event_study.json`, `scm.json`, `panel.json`, `descriptives.json`, `break.json`.
  4. `summary.py` — derived numbers quoted in the text → `results/summary.json`.
  5. `figures.py`, `tables.py`, `graphical_abstract.py` — figures (300 dpi PNG + PDF), the Tables section of the manuscript (`results/tables.md`).
  - `common.py` — paths, constants, minimum-wage schedule builder, helpers. `style.py` — figure style. `fetch_browser.js` — the browser version of step 1 actually used.
- `data/raw/minwage_schedule.csv` — minimum-wage rates coded by hand from official sources (below); the only raw file included.
- `results/` — result files; `results/provenance.md` lists input, code and result hashes.
- `manuscript/` — `manuscript.md`, `patch_docx.py`; `out/` — Word and PDF; `figures/`.

## Data sources
| File | Source |
|---|---|
| `data/raw/qcew_ny_nj_pa_quarterly.csv` (not redistributed) | U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages open-data API, `https://data.bls.gov/cew/data/api/{year}/{qtr}/industry/{naics}.csv`, NAICS 10, 722, 7224, 7225, 722511, 722513; county rows, private ownership, NY (36), NJ (34), PA (42); 2014Q1–2026Q1 (earlier years returned 404). NJ rows and NAICS 7224/7225 are extracted but not used. |
| `data/raw/minwage_schedule.csv` | New York State Department of Labor, *History of the Minimum Wage in New York State*, https://dol.ny.gov/history-minimum-wage-new-york-state; 12 NYCRR Part 146 Hospitality Industry Wage Order, https://forms.labor.ny.gov/WP/CR146.pdf (§146-1.2 general and fast-food rates, §146-1.3(b) tipped food-service cash wage); Part 146 wage-order summary (rev. 02/26), https://forms.labor.ny.gov/WP/Part146.pdf (2025–2026 rest-of-state tipped rates); NYSDOL minimum wage page, https://dol.ny.gov/minimum-wage (2027 off-ramp); U.S. DOL Wage and Hour Division state tables, https://www.dol.gov/agencies/whd/state/minimum-wage/history and https://www.dol.gov/agencies/whd/minimum-wage/state (Pennsylvania $7.25), all read 28 October 2026; NYS Division of the Budget, *Report on New York's Minimum Wage Increases Scheduled for 2023* (30 Sep 2022), Table 1, https://dol.ny.gov/system/files/documents/2022/10/minimum-wage-2023.pdf (first fast-food rate, $9.75 outside NYC from 31 Dec 2015), read 29 October 2026. |

Licences: BLS and U.S. DOL data are US government works in the public domain. New York State Department of Labor documents are public government records; the rates are facts transcribed from them. Code in this package: MIT licence.

Not used: Connecticut (QCEW reports Connecticut by planning region from 2024); New Jersey (no official quarterly rate history assembled).

## How the results were produced
The analysis environment had no direct internet access. The QCEW files were fetched on 28 October 2026 in a Chrome tab on data.bls.gov with `fetch_browser.js`. `common.py`, `build_panel.py` and `analysis.py` were written to a Pyodide 0.26.4 file system in the same tab (Python 3.12.1, pandas 2.2.0, NumPy 1.26.4, SciPy 1.12.0), their SHA-256 hashes checked against the files in `code/`, and run unchanged. The result JSON files were copied back and verified byte for byte (hashes in `results/provenance.md`). Steps 4–5 were run locally (Python 3.13, pandas 3.0.5, matplotlib 3.11). Running `fetch_data.py` should reproduce the inputs, subject to later QCEW revisions. Both fetch scripts treat an HTTP 200 response with no matching county rows as a failure. Version 1 was revised on 29 October 2026 after independent number and citation audits: the fast-food schedule gained its 31 Dec 2015 rate, and the synthetic control now reports a post-period-fit rank (the post/pre ratio is uninformative because the pre-period fit is exact by construction). The rerun reproduced all other result files byte for byte.

## Run
    cd code && python3 fetch_data.py && python3 build_panel.py && python3 analysis.py && python3 summary.py \
      && python3 figures.py && python3 tables.py && python3 graphical_abstract.py

AI use: data retrieval, analysis code and drafting assisted by Claude (Anthropic, claude-opus-5-5), October 2026; the author reviewed all outputs.
