# Lower economic value, same forest — reproducibility package

Kalafatis, P. (2026). *Lower economic value, same forest: the EU's leather exemption from deforestation rules* [Preprint]. x9m8.com.

## Contents
- `code/` — Python 3.13 with pandas, NumPy, pycountry and matplotlib.
  - `build.py` — assembles `results/panel.csv` from DeDuCE, FAOSTAT and Eurostat Comext.
  - `analysis.py` — embodied deforestation under each allocation rule, economic allocation factors, benefit-cost ratios → `results/analysis.json`, `embodied_by_year.csv`, `embodied_by_origin_year.csv`.
  - `figures.py`, `tables.py`, `graphical_abstract.py`.
- `data/raw/` — DeDuCE v2.0 cattle rows (Singh et al., 2024, Zenodo 10.5281/zenodo.10633818, CC BY 4.0) and Eurostat Comext extracts (DS-045409, reuse permitted with attribution).
- `results/` — all outputs quoted in the paper.
- `audits/` — independent number and citation audits, with the fixes applied in version 1.
- `manuscript/` — the manuscript in Markdown.

## FAOSTAT inputs (not redistributed)
Download `Production_Crops_Livestock_E_All_Data_(Normalized).zip` from https://bulks-faostat.fao.org/production/ and keep the cattle rows (Items "Raw hides and skins of cattle" and "Meat of cattle with the bone, fresh or chilled"; Elements Production, Yield/Carcass Weight, Producing Animals/Slaughtered) as `data/raw/faostat_qcl_cattle.csv`. Retrieved 21 October 2026.

## Run
    cd code && python3 build.py && python3 analysis.py && python3 figures.py && python3 tables.py

DeDuCE code inspected: https://github.com/chandrakant6492/DeDuCE at commit 48e4b5a (24 April 2026), file "4. Deforestation attribution (Python)-Statistical.py", lines 1661–1691 and 1883–1884.

AI use: analysis code and drafting assisted by Claude (Anthropic, claude-opus-5-5), October 2026; the author reviewed all outputs.
