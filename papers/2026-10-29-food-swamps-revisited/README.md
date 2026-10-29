# Food swamps and obesity revisited: reproduction package

Kalafatis, P. (2026). *Food swamps and obesity revisited: a reproduction with public data.* Preprint, x9m8.com. Not peer reviewed.

Reproduction and reanalysis of Cooksey-Stowers, K., Schwartz, M. B., & Brownell, K. D. (2017). Food swamps predict obesity rates better than food deserts in the United States. *IJERPH*, 14(11), 1366. https://doi.org/10.3390/ijerph14111366

## Contents

- `code/` analysis scripts (run in order from inside `code/`):
  1. `00_exits.py` counts OpenStreetMap `highway=motorway_junction` nodes per county (point in polygon) and cross-checks 17 states against the Overpass API
  2. `01_build.py` assembles the county files (`data/derived/county_base.csv`, `county2016.csv`)
  3. `02_reproduce.py` descriptive comparison with the original's Table 3, OLS (Table 6), IV (Tables 7-8), stratified IV (Table 9), interpretation of the coefficient
  4. `03_robustness.py` robustness grid (state fixed effects, size controls, weights, zero denominators, instrument codings)
  5. `04_update.py` 2016 counts with CDC PLACES obesity (BRFSS 2018), long difference 2007/2009 to 2016/2018
  6. `05_figures.py`, `graphical_abstract.py`, `tables.py` (rewrites the Tables section of the manuscript)
  7. `06_vintage_check.py` which Atlas release / count year matches the original's Table 3
  8. `07_construction_search.py` search over 1,372 ratio constructions for the one matching the published traditional-RFEI descriptives
  - helpers: `common.py` (paths, control sets, published targets), `econ.py` (OLS, 2SLS, clustered SEs, first-stage F, exact Anderson-Rubin sets), `style.py`
- `results/` JSON and CSV outputs (`reproduction.json`, `robustness.json|csv`, `update.json`, `build_meta.json`, `exits_meta.json`, `vintage_check.json`, `construction_search.csv|json`, `tables.md`)
- `figures/` Figures 1-3 (PNG 300 dpi and PDF), graphical abstract (900 x 420 px)
- `manuscript/` `manuscript.md` and `patch_docx.py`; `out/` Word and PDF builds (`../build_docs.sh`)
- `data/derived/` merged county files and per-county exit counts (derived from public data)

## Data sources (raw files are not redistributed; place them in `data/raw/`)

| File | Source | Licence / terms |
|---|---|---|
| `atlas_nov2012.xls`, `atlas_feb2014.xls`, `atlas_aug2015.xls`, `atlas_2025_csv.zip` | USDA ERS Food Environment Atlas, archived and current releases: https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads | US government work, public domain |
| `acs/acs5_county_tables.json` | ACS 5-year tables B19083, B08301, B15002, B01003 for all counties, 2006-2010, 2008-2012, 2016-2020, from `https://data.census.gov/api/access/data/table?id=ACSDT5Y{year}.{table}&g=010XX00US$0500000` (retrieved 22 Oct 2026) | US government work |
| `acs/acs5_county_tables_2018.json` | same, ACS 2014-2018 | US government work |
| `places_county_obesity_2018_2019.csv` | CDC PLACES county data (GIS-friendly), 2020 release (BRFSS 2018), Socrata id `mssc-ksj7`: https://data.cdc.gov/resource/mssc-ksj7.csv (fields stateabbr, countyfips, totalpopulation, obesity_crudeprev, obesity_adjprev); the second block (2021 release, `kmvs-jkvx`) carries no obesity field under that name and is not used | US government work |
| `osm/motorway_junction_qlever.tsv` | OpenStreetMap nodes tagged `highway=motorway_junction` with longitude < -60 and latitude > 15, queried from the QLever SPARQL endpoint https://qlever.cs.uni-freiburg.de/api/osm-planet, now redirecting to https://qlever.dev/api/osm-planet (index of planet file 2026-09-21, built with osm2rdf), 22 Oct 2026; query below | (c) OpenStreetMap contributors, ODbL 1.0 |
| `osm/overpass_17states_2026-10-22.txt` | Overpass API (https://overpass-api.de), same tag, 16 states and DC, used only as a cross-check | ODbL 1.0 |
| `geo/geojson-counties-fips.json` | 2010 Census cartographic county boundaries (500k) with CENSUSAREA (land area, sq mi), as redistributed at https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json (repository HEAD 0c447c47b757ad74edecab31f0d72f849d2e67c2) | US government work |

The derived exit counts in `data/derived/exits_osm.csv` are derived from OpenStreetMap data and are available under the ODbL.

QLever query used:

```
PREFIX osmkey: <https://www.openstreetmap.org/wiki/Key:>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
SELECT ?n ?wkt ?ref ?name WHERE { ?n osmkey:highway "motorway_junction" . ?n geo:hasGeometry/geo:asWKT ?wkt .
  OPTIONAL { ?n osmkey:ref ?ref } OPTIONAL { ?n osmkey:name ?name }
  FILTER (geof:longitude(?wkt) < -60 && geof:latitude(?wkt) > 15 && (geof:longitude(?wkt) > -180)) }
```

## How to run

```
pip install pandas numpy scipy geopandas shapely pyogrio xlrd openpyxl matplotlib python-docx
cd code
python3 00_exits.py && python3 01_build.py && python3 02_reproduce.py && python3 03_robustness.py && python3 04_update.py
python3 06_vintage_check.py && python3 07_construction_search.py && python3 05_figures.py && python3 graphical_abstract.py && python3 tables.py
bash ../../build_docs.sh   # needs pandoc and LibreOffice
```

Everything is deterministic (no random draws). Runtime under a minute apart from loading the spreadsheets.

## Notes

- Store counts: the original says it used 2009 data; its Table 3 and sample sizes match the 2007 counts in the February 2014 release, which is the main specification here; 2009 counts (November 2012 release) are a variant.
- The instrument substitutes OpenStreetMap motorway junctions (2026) for ESRI StreetMap highway exits (commercial, not available).
- Standard errors are clustered by state (49 clusters in the contiguous US).

## AI use

The study was carried out with the assistance of Claude (Anthropic; model claude-opus-5-5) in October 2026, which retrieved data, wrote and ran this code and drafted the manuscript under the author's direction. The author reviewed the work and takes full responsibility for it.
