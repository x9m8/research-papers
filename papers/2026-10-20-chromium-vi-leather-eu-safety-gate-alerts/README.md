# Fewer alerts, same allergy: hexavalent chromium in EU leather goods, 2005-2026

Code and data for Kalafatis (2026), preprint, x9m8.com. Contact: x9m8x7@gmail.com.

## Contents
- `raw/` Safety Gate snapshot (20 Oct 2026) and yearly alert totals. See `data/get_data.md`.
- `code/` run in this order from inside `code/`:
  1. `build.py` - one row per notification, Cr(VI)/leather classification, concentration extraction -> `results/alerts.csv`
  2. `analysis.py` - composition, yearly series and trends, notifiers, concentrations -> `results/analysis.json`
  3. `sensitivity.py` - S1-S7 -> `results/sensitivity.json`
  4. `figures.py` - Figures 1-3 (PNG 300 dpi + PDF) -> `figures/`
  5. `tables.py` - Tables 1-3 -> `results/tables.md` (also inserted into `manuscript/manuscript.md`)
  6. `graphical_abstract.py`
- `audits/` independent number audit (with hand validation of extraction and classification) and citation audit.
- `manuscript/` manuscript source. `lit/` literature brief.

## Requirements
Python 3.10+, pandas, numpy, scipy, statsmodels, matplotlib. The only randomness is the bootstrap (seed 20261020) and figure jitter (seed 1).

## Licence
Code: MIT. Derived tables: CC BY 4.0. Safety Gate content remains subject to the European Commission's reuse policy.
