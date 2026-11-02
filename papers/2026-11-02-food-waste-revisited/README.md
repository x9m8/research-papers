# US food waste revisited: reproduction package

Kalafatis, P. (2026). *US food waste revisited: a reproduction with public data.* Preprint, x9m8.com. Not peer reviewed.

Reproduction, robustness check and update of Hall, K. D., Guo, J., Dore, M., & Chow, C. C. (2009). The progressive increase of food waste in America and its environmental impact. *PLoS ONE*, 4(11), e7940. https://doi.org/10.1371/journal.pone.0007940

## Contents

- `code/` (run in order from inside `code/`):
  0. `00_nhanes_aggregate.js` browser script (run in a tab on https://wwwn.cdc.gov/): parses NHANES SAS transport files (DEMO, BMX, DR1TOT/DRXTOT) for 1999-2000 to 2021-2023 and returns weighted aggregates only (`runAll()`, `runDiet()`); its output is `data/raw/nhanes/*aggregates.csv`
  1. `01_inputs.py` FAO supply series and splice, body-weight series, F0, IOM baseline intake, coefficient check
  2. `02_reproduce.py` the original calculation 1974-2003, headline numbers, Monte Carlo (100,000 draws, seed 20091124), USDA and EPA comparisons, comparison with digitized published curves
  3. `03_robustness.py` input and assumption variants, one-at-a-time parameter sensitivity
  4. `04_update.py` extension to 2023, Monte Carlo for 2003-2023 change, per-capita (children) correction, self-reported intake
  5. `05_figures.py`, `graphical_abstract.py`, `tables.py` (rewrites the Tables section of the manuscript)
  - helpers: `common.py` (paths, loaders, model equations and parameters), `style.py`
- `results/` `inputs.json`, `reproduction.json`, `robustness.json|csv`, `update.json`, `tables.md`
- `figures/` Figures 1-3 (PNG 300 dpi and PDF), graphical abstract (900 x 420 px)
- `data/raw/` small public inputs (see below); `data/derived/` `fa.csv`, `bw_points.csv`
- `manuscript/` `manuscript.md`, `patch_docx.py`; `out/` Word and PDF (`../build_docs.sh`)

## Data sources

| File | Source | Terms |
|---|---|---|
| `raw/fao/fao_usa_fbsh_fbs.txt` | FAOSTAT bulk files `FoodBalanceSheetsHistoric_E_All_Data_(Normalized).zip` (FBSH, DateUpdate 2023-03-10) and `FoodBalanceSheets_E_All_Data_(Normalized).zip` (FBS, DateUpdate 2025-10-28) from https://bulks-faostat.fao.org/production/, filtered to area 231 (USA), element 664 (kcal/capita/day) for aggregate items 2901-2961 and element 511 (population); retrieved 28 Oct 2026 | FAO statistical data terms (understood to be CC BY 4.0; not re-checked for this package) |
| `raw/nhanes/nhanes_continuous_aggregates.csv`, `nhanes_diet_kcal_aggregates.csv` | weighted aggregates computed by `00_nhanes_aggregate.js` from NHANES public files at https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/ (DEMO, BMX, DRXTOT/DR1TOT). The script also aggregates the 2017-March 2020 pre-pandemic P_ files, but the analysis uses the 2017-2018 (_J) and 2021-2023 (_L) cycles; the P_ rows are not used, 28 Oct 2026 | US government work, public domain |
| `raw/nhanes/ogden2004_ad347_adult_means.csv` | transcribed from Ogden et al. (2004), Advance Data 347, Tables 7, 9, 10: https://www.cdc.gov/nchs/data/ad/ad347.pdf | public domain |
| `raw/other/ers_lafa_calories.csv` | USDA ERS loss-adjusted food availability, calories (https://www.ers.usda.gov/media/5381/calories.csv; data last updated 1 June 2019), table part only | public domain |
| `raw/other/epa_food_msw.txt` | EPA, Food: Material-Specific Data, table of food management 1960-2019 (https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/food-material-specific-data) | public domain |
| `raw/other/eia_product_supplied.csv` | EIA series MTTUPUS2, annual (https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=MTTUPUS2&f=A), selected years | public domain |
| `raw/other/hall2009_fig1_digitized.csv` | digitized from Figure 1 of Hall et al. (2009), method in file header | CC0 1.0 (source article is a public-domain dedication) |

NHANES microdata and the FAOSTAT bulk files are not redistributed; only the aggregates used are included.

**Transfer note.** The analysis environment could not reach these sites directly, and uploading through the x9m8.com media library was refused by the session's permission system. The aggregates were therefore computed in a browser tab and copied into the files above as text; each file's checksum (31-multiplier rolling hash, as computed in the browser) matched after writing. Running `00_nhanes_aggregate.js` in a browser reproduces the NHANES files.

- 5.8 million Btu per barrel (oil conversion) is the EIA crude-oil heat content; the original does not state a factor.
- The 2003-2023 sensitivities that the Monte Carlo omits (end year, splice offset, 2021-23 weight error, extrapolation) are in `results/update.json` under `sensitivity_2003_2023`.

## How to run

```
pip install pandas numpy matplotlib python-docx
cd code
python3 01_inputs.py && python3 02_reproduce.py && python3 03_robustness.py && python3 04_update.py
python3 05_figures.py && python3 graphical_abstract.py && python3 tables.py
bash ../../build_docs.sh   # needs pandoc and LibreOffice
```

Runtime a few seconds. The Monte Carlo uses a fixed seed.

## Notes

- Model equations were coded from the article's equations 1-14 (the simplified equation the text calls eq. 14 is printed with a second label (13)); nominal parameters as in the text (gamma_F = 3.2), Monte Carlo distributions as in its Table 1 (gamma_F = 3.6 +/- 2); draws with C <= 0 or beta >= 0.95 are redrawn (not in the original); medians and 2.5-97.5 percentiles are reported. Intervals reflect parameter uncertainty only.
- Body weights: adults 20-74, pregnant women excluded, men and women combined with weight 0.475/0.525. Survey points at 1974 (NHANES I), 1978.5, 1991 and mid-cycle thereafter.
- F0 and I0 for 1971-74 are re-derived from published means with approximations (see manuscript §2.3).

## AI use

The study was carried out with the assistance of Claude (Anthropic; model claude-opus-5-5) in October 2026, which retrieved data, wrote and ran this code and drafted the manuscript under the author's direction. The author reviewed the work and takes full responsibility for it.
