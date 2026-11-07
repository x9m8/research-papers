# Data sources, retrieval and integrity (paper 23)

All retrieved 2026-11-02/03 (UTC) in a Chrome tab opened for this task (the shell cannot reach these hosts). Nothing was uploaded anywhere. Because browser tools could not save files, each BLS dataset was parsed in the browser, serialised to compact text, transcribed into `data/raw/`, and checked by SHA-256 against the value computed in the browser.

| File in data/raw | Source | Content | SHA-256 (file = in-browser value) |
|:--|:--|:--|:--|
| bls_wide.txt | https://download.bls.gov/pub/time.series/cu/ (cu.data.1.AllItems, .2.Summaries, .7.OtherNorthEast, .11.USFoodBeverage); /ap/ (ap.data.3.Food); /ce/ (ce.data.70b, 70c, 05b); retrieved 2026-11-03T02:54Z | 17 series x 261 months (2005-01 to 2026-09), one line per series, blank = missing | 80e387f00cbd04e457a58f8442f1903351d8194923656014e976616fef0d15d3 |
| bls_ppi_wide.txt | https://download.bls.gov/pub/time.series/wp/ (wp.data.2.FarmProducts); retrieved 2026-11-03 | WPU0171, WPU01710703, same grid | 2384ec272d6b69263b850c88f544bbde9a97710413e81b6a842be11d251a4481 |

Additional in-browser hash (not stored as a file): long-format BLS cu extract (112,265 characters) 71eff8189ec379a69e3f05328c8645dc9871f4bf719d0c6eebc71779d1cd7620.

Series identifiers (checked against cu.series / wp.series / ce.series where listed; see manuscript Methods): CUUR0000SEFH, CUUR0000SAF11, CUUR0000SEFV, CUUR0000SEFV01, CUUR0000SEFV02, CUURS12ASEFV, CUURS12ASAF11, CUUR0000SA0, CUURS12ASA0, CUSR0000{SEFH,SAF11,SEFV,SEFV01} (seasonally adjusted, loaded but not used in results), APU0000708111, WPU0171, WPU01710703, CES7072200008, CES7072200003, CES0500000003.

Known data issues: no BLS CPI or average-price value for October 2025 (footnote code X in the source); CES wage series end 2026-08 (all-employee series 2006-03 start); USDA AMS/ERS wholesale egg price and layer inventory files were not obtained.

## USDA APHIS HPAI layer-loss data — not redistributed

The layer-loss shock used in the analysis (`L`, `n` in `code/common.py`'s `monthly_layers()`) comes from the USDA APHIS dashboard "Confirmations of Highly Pathogenic Avian Influenza in Commercial and Backyard Flocks": https://www.aphis.usda.gov/livestock-poultry-disease/avian/avian-influenza/hpai-detections/commercial-backyard-flocks (embeds a Tableau view at https://publicdashboards.dl.usda.gov/t/MRP_PUB/views/VS_Avian_HPAIConfirmedDetections2022/HPAI2022ConfirmedDetections). It was read via the dashboard's own Tableau embedding API, worksheet "ExportToCsv", on 2026-11-03T02:59Z: 2,297 confirmed detections (date, state, county, production type, birds affected), of which 169 are commercial table-egg detections (layers, pullets, breeders).

The dashboard's data carries a USDA stated-use restriction (see the dashboard page's own disclaimer) that is inconsistent with redistributing the underlying detection-level extract in a public reproducibility package, so **that extract is not included here**. What *is* included is `data/derived/aphis_table_egg_layer_losses_monthly.csv` (SHA-256 22a4e112c6656e9afa562eb89e3e793434dc637e4e84b4f032e0acc433da42d4): the monthly aggregate — millions of commercial table-egg layer birds confirmed and flock count, February 2022 to September 2026 — computed from that extract and used directly by every result in this package (total 152.3949 million birds, 136 flocks; see Table 2 and §3.1 of the manuscript). This aggregate carries no county-, date-of-week- or flock-identifying detail.

A reader can reproduce `aphis_table_egg_layer_losses_monthly.csv` from scratch: open the dashboard URL above, read the "ExportToCsv" worksheet (date, state, county, production, birds affected), filter to production = "Commercial Table Egg Layer", and sum birds affected by calendar month of confirmed diagnosis. The dashboard is a live, current snapshot and is expected to show more detections after this paper's retrieval date (it already updated between visits during this project), so a reproduction after 2026-11-03 will not match exactly; the version used here is the derived CSV in this package.

The "more than 378.5 million egg-laying chickens" figure quoted in §2.1 of the manuscript, for scale, is likewise drawn from the same APHIS page (context text above the dashboard, attributed by APHIS only to "USDA National Agricultural Statistics Service" with no further citation); it is background only, not an input to any regression, table or figure, and its source text is not separately redistributed here.

Licences/terms: BLS data are public domain US government works (BLS asks for citation). APHIS dashboard data are subject to a USDA stated data-use restriction (the dashboard disclaimer states the data are for restricted government purposes), which is why the detection-level extract is not shipped in this package; the aggregate figures used here are cited to the live dashboard above rather than redistributed as raw APHIS data.
