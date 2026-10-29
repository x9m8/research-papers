# Validated, not confirmed: the track record of statistically validated exoplanets

Code and data for Kalafatis (2026), preprint, x9m8.com. Contact: x9m8x7@gmail.com.

## Contents
- `raw/` NASA Exoplanet Archive tables and VizieR extracts, snapshot 15 October 2026. See `data/get_data.md`.
- `code/` analysis pipeline, run in this order from inside `code/`:
  1. `build.py`: planet-level table (`results/planets.csv`) and per-paper validation lists with each paper's FPPs (`results/batches.csv`).
  2. `analysis.py`: composition, track record, calibration, Kaplan–Meier follow-up, TESS check (`results/analysis.json`).
  3. `sensitivity.py`: S1–S5 (`results/sensitivity.json`).
  4. `figures.py`: Figures 1–5 (`figures/`, PNG 300 dpi + PDF).
  5. `tables.py`: Tables 1–3 (`results/tables.md`, also inserted into the manuscript).
- `code/overturn_reasons.csv`: the 21 overturned planets, what each turned out to be, and the refuting publication with DOI. Checked against sources in `audits/citation_audit.md`.
- `audits/`: independent number audit and citation audit.
- `manuscript/`: manuscript source.

## Requirements
Python 3.10+, pandas, numpy, scipy, matplotlib. No randomness; every result is deterministic.

## Licence
Code: MIT. Derived tables: CC BY 4.0. Raw archive and VizieR data remain under their providers' terms.
