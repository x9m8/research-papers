# Provenance

Inputs fetched 22 October 2026 in the browser (see README). Size in bytes and the first 16 hex digits of the SHA-256 of each input as written to `data/raw/`:

| File | Bytes | SHA-256 (prefix) |
|---|--:|---|
| partd_provider_zip_2019.csv | 288129 | 30d4814dc6ecd7b2 |
| partd_provider_zip_2020.csv | 287247 | 78d349451257ff35 |
| partd_provider_zip_2021.csv | 287893 | 2a6ead4e9f584bf5 |
| partd_provider_zip_2022.csv | 289403 | 4486a9e53892dd01 |
| partd_provider_zip_2023.csv | 290827 | 2cb8605a3fd82826 |
| partd_provider_zip_2024.csv | 293531 | 060d9601de0336b9 |
| partd_glp1_npi_2019.csv | 6668671 | a6ce2053ca62a8e5 |
| partd_glp1_npi_2020.csv | 8112413 | e86332462a066b8f |
| partd_glp1_npi_2021.csv | 9456479 | 4297b072db4d57a8 |
| partd_glp1_npi_2022.csv | 11905318 | 84eec81198b1edd0 |
| partd_glp1_npi_2023.csv | 17909922 | 8f7edc520296c33a |
| partd_glp1_npi_2024.csv | 21600152 | 7416c765e4a7a4c3 |
| partd_geo_glp1_2019.csv | 38553 | b1987e7fd935cb51 |
| partd_geo_glp1_2020.csv | 38319 | 553711b9c714e679 |
| partd_geo_glp1_2021.csv | 38492 | 0ec344d369ae330b |
| partd_geo_glp1_2022.csv | 39134 | eba511d5e3044b39 |
| partd_geo_glp1_2023.csv | 38597 | 71042ff91f47302e |
| partd_geo_glp1_2024.csv | 44622 | 0a5ac3aaa46385ee |
| medicare_enrollment_county.csv | 1256186 | 88fc25f23e22d39f |
| qcew_722511.csv | 1215012 | 867319f82f55c670 |
| qcew_722513.csv | 1203640 | 3c6e88616e015847 |
| qcew_446110.csv | 682090 | 09d131a52ec91d67 |
| qcew_456110.csv | 384416 | 28dfb2b89f1dd037 |
| qcew_721.csv | 1008294 | 7a78507d308e6e3c |
| qcew_445110.csv | 1111837 | 9ed0ad1734a158de |
| qcew_10.csv | 1319739 | f35fa8addc95c3ee |
| zcta_county_2020_maxland.csv | 405509 | 34f55b8435b98e98 |
| affinity_state_monthly.csv | 1045717 | 7251f67cfba66d2f |

Row counts from the CMS API (all pages retrieved and checked against the API's `found_rows`): by-Provider file 1,240,595 (2019), 1,255,175 (2020), 1,287,454 (2021), 1,332,309 (2022), 1,380,665 (2023), 1,416,883 (2024) prescribers; GLP-1 prescriber-drug rows 123,888; 152,357; 180,863; 230,236; 351,240; 426,932; county enrollment rows 42,599. QCEW 446110 is absent from 2022 and 456110 before 2022 (NAICS 2022 revision), as expected.

Result files produced in Pyodide and copied back (SHA-256, identical on both sides):

| File | SHA-256 |
|---|---|
| build.json | 1d519ea7f66ee66a6d2c5e81db8c41fce304b2d17a5d4f7232c680483bd130ed |
| estimates.json | f6ec3650b765660d98c21c41680b2932946e854db76fa172680868bb56cce348 |
| event_study.json | 8d422bed0eb1109cc487fc5c55d9fb1ea5ac8195eccb39b4062c72c5dc6be793 |
| descriptives.json | a17c23d667193b1be65a6bd76f038afa9fc97bf551f9ecf01c6057002a540d02 |
| state_secondary.json | c297cdb751a07614a7367c4914ddc3d4a8c480ba353cd3738d727556c8efe191 |

Code run in Pyodide (SHA-256 matched the files in `code/`): common.py 44f25d22…, build_panel.py e7e2c13a…, analysis.py 80abb2c8…, state_secondary.py 2f026ef1….
