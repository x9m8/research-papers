# Inputs (download into data/raw/)

All retrieved 20 October 2026.

- `fred_20261020.json`: a JSON object mapping FRED series id to the CSV text downloaded from
  https://fred.stlouisfed.org/graph/fredgraph.csv?id=WPU0419 (only WPU0419 is used). Series page: https://fred.stlouisfed.org/series/WPU0419
- `LivestockPrices.csv`, `Meat-Statistics.csv`, `WholesalePrices.csv`: USDA ERS Livestock and Meat Domestic Data, machine-readable files
  (https://www.ers.usda.gov/data-products/livestock-and-meat-domestic-data).
- `AMS_2829_2025-08-26.pdf`, `AMS_2829_2025-09-30.pdf`: USDA AMS By-Product Drop Value (Steers)(Cattle)
  https://esmis.nal.usda.gov/sites/default/release-files/p5547r46g/1257cs964/z316s222h/AMS_2829.PDF and
  https://esmis.nal.usda.gov/sites/default/release-files/p5547r46g/cr56q013x/1r66m2528/AMS_2829.PDF
  (read by hand; their hide prices are in `data/anchors.csv`).
