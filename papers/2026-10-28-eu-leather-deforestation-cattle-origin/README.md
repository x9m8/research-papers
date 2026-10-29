# Where the cattle were raised — reproducibility package

Kalafatis, P. (2026). *Where the cattle were raised: Tracing the deforestation in EU leather consumption through tanning and manufacturing countries, 2005–2023* [Preprint]. x9m8.com.

## Contents
- `code/common.py` — paths, HS6 stage assignment, conversion-factor sets, allocation rules.
- `code/build.py` — cleans BACI trade (EU27 as one region), FAOSTAT hide production, DeDuCE cattle deforestation, allocation factors and deforestation per tonne of hide → `data/derived/`, `results/build_info.json`.
- `code/trace.py` — stage-wise origin tracing, pooled tracing (Laroche et al. 2024 method) and exporter attribution, every year and scenario → `results/eu_rhe_by_origin.csv.gz`, `results/stage_balance.csv`, `results/eu_routes.csv.gz`.
- `code/analysis.py` — embodied deforestation by rule, comparisons, bridge, routes, sensitivity, validation → `results/analysis.json` and CSVs.
- `code/diagnostics.py` — countries whose exports exceed supply → `results/gap_by_country.csv`, `results/gap_top_countries.json`.
- `code/figures.py`, `code/tables.py` (rewrites the Tables section of `manuscript/manuscript.md`), `code/graphical_abstract.py`, `code/style.py`.
- `manuscript/manuscript.md`, `manuscript/patch_docx.py`; `out/` Word and PDF; `../build_docs.sh` builds them (pandoc, python-docx, LibreOffice).

## Data sources (not redistributed; place in `data/raw/` and `data/laroche/` as named)
- **BACI** HS02, version 202601 (CEPII; Etalab 2.0 licence; cite Gaulier & Zignago 2010). https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS02_V202601.zip. Keep years 2005–2024 and products 4101, 4104, 4107, 4114, 4115 (411520, leather waste, is not used), 4201, 420211, 420221, 420231, 420291, 4203, 4205, 6403, 6404, 6405, as `data/raw/baci/leather_<year>.csv` (columns t,i,j,k,v,q), plus `country-codes.csv` and `product-codes.csv` from the same zip.
- **FAOSTAT** Production (QCL), bulk file `Production_Crops_Livestock_E_All_Data_(Normalized).zip` from https://bulks-faostat.fao.org/production/; keep item codes 919 and 957 (the extract also holds 946, 947, 1806, 1811, unused) from 2000 on, as `data/raw/faostat_qcl_hides.csv`; plus the cattle file of paper 8 (`faostat_qcl_cattle.csv`: raw cattle hides and beef; elements Production, Yield/Carcass Weight, Producing Animals/Slaughtered). Retrieved 22 October 2026 (cattle file 21 October 2026).
- **DeDuCE v2.1** (Singh, Persson, Croft, Kastner & West, 2026; Zenodo https://doi.org/10.5281/zenodo.18953516; CC BY 4.0): rows of commodity group "Pasture" from `1. DeDuCE_Deforestation attributed to agricultural and forestry commodities (2001-2023).xlsx`, as `data/raw/x9p14-deduce21-attrib-cattle.csv`.
- **DeDuCE v2.0** (Zenodo https://doi.org/10.5281/zenodo.10633818; CC BY 4.0 on Zenodo, while the readme in the download says CC BY-NC-SA): cattle rows as `data/raw/x9p8-deduce-attrib-cattle.csv`.
- **Laroche et al. (2024) supplement**, authored on Zenodo as Kastner, Laroche et al. (2024) (Zenodo https://doi.org/10.5281/zenodo.11085413; CC BY 4.0): `input_data/conversion_factors_leather.csv` and `output/…_mean.rds` into `data/laroche/` as `conversion_factors_leather.csv` and `out_mean.rds`.
- **Eurostat Comext** DS-045409 extracts from paper 8 (EU27 extra-EU imports of 4101/4104/4107, and beef 0201/0202 by origin), `data/raw/x9p8-comext-*.csv` (Eurostat reuse policy, attribution).

## Run
    cd code && python3 build.py && python3 trace.py && python3 analysis.py && python3 diagnostics.py && python3 figures.py && python3 tables.py && python3 graphical_abstract.py
    bash ../../build_docs.sh
Python 3.13 with pandas, numpy, openpyxl, pyreadr, matplotlib, python-docx. Run time about four minutes.

## AI use
Data retrieval, reading of the Laroche et al. code, analysis code and the first draft were done with Claude (Anthropic; model claude-opus-5-5) in October 2026 under the author's direction. The author reviewed the work and is responsible for it.
