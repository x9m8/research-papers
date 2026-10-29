# Eating less of the same — reproducibility package

Kalafatis, P. (2026). *Eating less of the same: modelled nutrient gaps on GLP-1 drugs* [Preprint]. x9m8.com.

## Contents
- `code/` — Python 3.13 with pandas, NumPy, SciPy and matplotlib.
  - `common.py` — EARs, AIs, scenarios.
  - `usual.py` — sample selection, usual intake (NRC variance adjustment, day 1 as reference, mean-matched back-transformation; supplements added after shrinkage), cut-point prevalence with Taylor-linearised SEs → `results/prevalence.json`, `usual_L.csv`.
  - `curves.py` — continuous 0–45% curves and per-person counts → `results/curves.json`.
  - `validate.py` — check against official NCI-method estimates (USDA ARS, WWEIA 2017–March 2020, non-Hispanic White adults, Tables TB) → `results/validation_ars.csv`.
  - `figures.py`, `tables.py`, `graphical_abstract.py`.
- `results/`, `audits/` (independent number and citation audits; fixes applied in version 1), `manuscript/`.

## NHANES input files (public, not redistributed)
Place these in `data/raw/` (downloaded 21 October 2026 from https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/):
- 2021/DataFiles/: DEMO_L, BMX_L, DR1TOT_L, DR2TOT_L, DIQ_L, BPQ_L (.xpt)
- 2017/DataFiles/: P_DEMO, P_BMX, P_DR1TOT, P_DR2TOT, P_DS1TOT, P_DS2TOT, P_DIQ, P_BPQ (.xpt)

## Run
    cd code && python3 usual.py && python3 curves.py && python3 validate.py && python3 figures.py && python3 tables.py

AI use: analysis code and drafting assisted by Claude (Anthropic, claude-opus-5-5), October 2026; the author reviewed all outputs.
