# Eating less, eating differently — reproducibility package

Kalafatis, P. (2026). *Eating less, eating differently: the cost of an adequate diet on GLP-1 drugs* [Preprint]. x9m8.com.

## Contents
- `code/` — Python 3.13 with pandas, NumPy, SciPy (HiGHS), CVXPY (Clarabel) and matplotlib.
  - `common.py` — paths, DRIs (RDA/AI, UL), Thrifty Food Plan costs, exclusions.
  - `build.py` — links FNDDS 2017–2018 nutrients to ERS PP-NAP 2017/2018 prices; CPI inflation to 2026 → `results/foods_priced.csv`, `build.json`.
  - `basket.py` — current diet of eligible adults from NHANES 2017–March 2020 food records → `results/basket.csv`, `basket.json`.
  - `categories.py` — WWEIA category composites and P95/P99 limits → `results/categories.csv`.
  - `model.py` — nutrient constraints and the least-cost diet from any foods.
  - `catmodel.py` — category models: closest adequate (QP), closest (L1), cheapest, best achievable (elastic), feasibility bisection, per-nutrient maxima.
  - `within.py` — food-level variant (foods chosen within categories).
  - `results.py` → `results/results.json`, `diets_by_category.csv`; `figures.py`, `tables.py`, `graphical_abstract.py`.
- `data/eligible_P.csv` — eligible sample (SEQN, sex, age, weights), built with the companion paper's code.
- `results/`, `audits/` (independent number and citation audits; fixes applied in version 1), `manuscript/`.

## Public inputs (not redistributed; place in `data/raw/`)
- NHANES 2017–March 2020: P_DR1IFF.xpt and P_DR2IFF.xpt from https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/ (converted to `p_dr1iff.csv` with columns SEQN, code, g, keeping DR1DRSTZ == 1, and `p_dr2iff.csv` with SEQN, code, g, kcal).
- FNDDS 2017–2018 and 2021–2023 "At A Glance – FNDDS Nutrient Values" xlsx from the USDA ARS FNDDS download page.
- ERS Purchase to Plate National Average Prices (CSV) from https://www.ers.usda.gov/data-products/purchase-to-plate
- ERS Food Price Outlook: annual percent changes in CPIs and the historical CPI forecast series (CSV).

## Run
    cd code && python3 build.py && python3 basket.py && python3 categories.py && python3 results.py && python3 figures.py && python3 tables.py

AI use: analysis code and drafting assisted by Claude (Anthropic, claude-opus-5-5), October 2026; the author reviewed all outputs.
