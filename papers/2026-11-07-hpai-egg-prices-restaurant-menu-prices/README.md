# Bird flu, egg prices and restaurant menu prices in US CPI data — reproducibility package

Kalafatis, P. (2026). *Bird flu, egg prices and restaurant menu prices in US CPI data* [Preprint]. x9m8.com.

## Contents
- `code/` — Python 3.13 (pandas, NumPy, SciPy, statsmodels, matplotlib).
  - `common.py` — loaders for the raw BLS extracts and the derived APHIS monthly aggregate.
  - `a1_hpai_to_prices.py` — local projections of egg prices on monthly HPAI layer losses → `results/a1_hpai_to_prices.json`.
  - `a2_passthrough.py` — distributed-lag pass-through to restaurant CPI, sensitivity, falsification, reduced-form projections, descriptive inflation → `results/a2_passthrough.json`.
  - `a3_bounds.py` — implied bounds for the two egg-price waves → `results/a3_bounds.json`.
  - `figures.py`, `style.py`, `graphical_abstract.py`, `tables.py` (also rewrites the Tables section of the manuscript).
- `data/raw/` — compact BLS extracts (see `data/SOURCES.md` for source URLs, retrieval times, SHA-256 hashes and known issues).
- `data/derived/` — `aphis_table_egg_layer_losses_monthly.csv`, the monthly commercial table-egg layer loss aggregate used in the analysis, derived from the public APHIS dashboard. The underlying detection-level APHIS extract is **not** included; see `data/SOURCES.md` for why and how to reproduce the aggregate yourself.
- `results/`, `figures/`, `manuscript/`, `out/` (docx and PDF), `audits/` (empty; independent audits are run separately).

## Data (public)
BLS time-series files (https://download.bls.gov/pub/time.series/) and the USDA APHIS HPAI confirmed-detections dashboard (https://www.aphis.usda.gov/livestock-poultry-disease/avian/avian-influenza/hpai-detections/commercial-backyard-flocks). Raw BLS bulk files are not redistributed; the small BLS extracts used are included. The APHIS detection-level extract is not redistributed either, because the dashboard states its data are for restricted government purposes; only the derived monthly aggregate is included (`data/derived/`), and the live dashboard is cited so a reader can pull the same public figures themselves. No data were uploaded anywhere.

## Run
    cd code && python3 a1_hpai_to_prices.py && python3 a2_passthrough.py && python3 a3_bounds.py && python3 figures.py && python3 graphical_abstract.py && python3 tables.py
    cd .. && bash ../build_docs.sh   # pandoc -> patch_docx.py -> soffice (paths in the script are absolute to the build machine)

AI use: data retrieval, analysis code, reference checks and drafting assisted by Claude (Anthropic, claude-sonnet-5), October–November 2026; the author reviewed all outputs.
