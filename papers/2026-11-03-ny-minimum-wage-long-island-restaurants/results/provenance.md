# Provenance

Inputs fetched 28 October 2026 in a Chrome tab on data.bls.gov (see README). The Python steps `build_panel.py` and `analysis.py` were run in Pyodide 0.26.4 (Python 3.12.1, pandas 2.2.0, NumPy 1.26.4, SciPy 1.12.0) in that tab; the result files below were copied back and their SHA-256 hashes checked against the in-browser originals. `summary.py`, `figures.py`, `tables.py` and `graphical_abstract.py` were run locally (Python 3.13, pandas 3.0.5).

## Inputs and intermediate files (in-browser)

| File | Bytes | SHA-256 |
|---|--:|---|
| data/raw/qcew_ny_nj_pa_quarterly.csv (not redistributed) | 2299282 | 0d2a00bac6b633c6ac09a58aa6027fe3bb3858938fba987a16b162152f2bfb9a |
| data/raw/minwage_schedule.csv (v2, 29 Oct) | — | 254ee733bb388149fc6b50df02420887b89c34776e572de2d2f4141b0a63b42d |
| data/derived/panel.csv (not redistributed) | 1612258 | b8406f75f98a50d55b230877c2b4e7963d65e1a1bc5a08cf8e5b8109c554d85e |
| data/derived/schedule_quarterly.csv (v2) | — | ecf96d1a397af1b4041732ab918ef37413b94d87d0cd7cc41a17b16efb744ed8 |

## Code run in the browser

| File | SHA-256 |
|---|---|
| code/common.py | 173b47e53db6dabfdf218759ed2bf8a83a013bc51a1e67fcc81787f2748649be |
| code/build_panel.py | af5310df38080fbd50d20cbb520bdb596c2b9432dbddbed17a186dca4caad41a |
| code/analysis.py (v2, 29 Oct) | a3fc42dbe6c11e95ebbd4cf0e0864c3d3185c8aeff0839495d796e018dd2c18b |

## Result files (verified byte for byte)

| File | SHA-256 |
|---|---|
| build.json (v2) | 7fd6c7203141259b8f820e87dd131f57f9bff6c7b11080b5b77f255fa8d2d059 |
| estimates.json | 1fee4951123fe01e5b58432bfe091ba84e773f2f6a0a730f8eb100d60cfb345a |
| event_study.json | b1b87305b408eaca8130575502db0f4888f31ec6b68d1a9ff8ea38746ec2f917 |
| scm.json (v2) | 857e5a82adcbe3855c7fb658f77006562c9c3abc46096692bffb70ca220fcc50 |
| panel.json | d9bf83a7acc4c9f174f12e54a861e09c39dc3cf48a734239cb3421def0acebdb |
| descriptives.json | aa9ad0e6d3bfbb4abd14cfcf13648bf28bfd25f3de7c0d68c1311dd510a88339 |
| break.json | 1a62f691dd0afe6b1b7278af18af745087fd998d728a8bed8458ba3a635800bc |

Version 2 (29 October 2026): rerun in Pyodide in a new data.bls.gov tab from the same stored QCEW extract (hash above). Only build.json (2016 fast-food rate) and scm.json (added post-period rank) changed; estimates, event_study, panel, descriptives and break files and panel.csv were byte-identical to version 1.
