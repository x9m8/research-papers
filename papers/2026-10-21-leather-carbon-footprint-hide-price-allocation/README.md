# Leather's carbon bill follows the hide price, not the cow

Code and data for Kalafatis (2026), preprint, x9m8.com. Contact: x9m8x7@gmail.com.

Economic allocation factor of US cattle hides (hide value / live steer value), monthly June 2001 – December 2025, and the farm-stage
emissions it assigns to leather.

## Contents
- `data/anchors.csv` USDA AMS hide prices used to scale the price index (role = calibration) and published quotes used only as checks (role = validation*), with sources.
- `data/params.json` emission factor, hide yield, leather yield, and published allocation factors, with sources.
- `data/get_data.md` where to download the public inputs into `data/raw/` (not redistributed here).
- `code/` run in this order from inside `code/` (or `bash run_all.sh`):
  1. `hide_series.py` PPI WPU0419 scaled to $/piece -> `results/hide_monthly.csv`, `hide_calibration.json`
  2. `allocation.py` monthly and annual allocation factor and sensitivity denominators -> `results/allocation_*.csv`, `allocation.json`
  3. `summary.py` headline numbers, decomposition, scaling bounds, trailing means -> `results/summary.json`
  4. `carbon.py` kg CO2e per hide and per m2 -> `results/carbon_annual.csv`, `carbon.json`
  5. `crosscheck.py` checks independent of the scaling -> `results/crosscheck.json`
  6. `tables.py` Tables 1-2 -> `results/tables.md` (also written into the `## Tables` section of `manuscript/manuscript.md`, overwriting any manual edits there)
  7. `fig12.py`, `fig3.py`, `graphical_abstract.py` -> `figures/`
- `audits/` independent number and citation audits. `manuscript/` manuscript source.

## Requirements
Python 3.10+, pandas, numpy, matplotlib. No randomness.

## Licence
Code: MIT. Derived tables: CC BY 4.0. Inputs are US government works.
