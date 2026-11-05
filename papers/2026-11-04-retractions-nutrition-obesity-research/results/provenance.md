# Provenance

Version 2 (after the independent audits, 29 October 2026). Input fetched 29 October 2026 (commit dated 28 October 2026) in a Chrome tab with JavaScript from the GitLab API
(`https://gitlab.com/api/v4/projects/61336882/repository/files/retraction_watch.csv/raw?ref=827665ab699e4a798060b95c40268de417b7f2e1`).
`select_records.py`, `analysis.py`, `citation_sample.py` and `citations.py` (with `common.py`) were run unchanged in Pyodide 0.26.4
(Python 3.12.1, pandas 2.2.0, NumPy 1.26.4) in that tab after their SHA-256 hashes were checked against the files in `code/`.
OpenAlex was queried from the same tab with `fetch_openalex.js` (29 October 2026). The result JSON files were copied back as compact JSON,
rewritten with the same formatting (`restore_results.py`), and their SHA-256 hashes checked against the in-browser originals: all matched. In version 2, `common.py`, `select_records.py` and `analysis.py` were revised (journal-article-only comparisons, a broader misconduct mapping, unmapped reasons) and re-run in a new Pyodide session on the same CSV (hash re-checked). `selection.json`, `trends.json` and `citation_dois.json` were byte-identical to version 1, so `citations.json` (and its OpenAlex query) was not re-run. New and changed result files were copied back as compact JSON (for `comparison.json` and `sensitivity.json`, as the additions to the version 1 files) and verified byte for byte against the in-browser hashes.
`summary.py`, `figures.py`, `tables.py` and `graphical_abstract.py` were run locally (Python 3.13). Nothing was uploaded anywhere.

## Inputs and intermediate files (in-browser, not redistributed)

| File | Bytes | SHA-256 |
|---|--:|---|
| data/raw/retraction_watch.csv | 67716155 | 7020113802228518d52d8da3b64ed3a30c59e37e828d8377bce72a5cbad7c303 |
| data/derived/records.csv (version 2; two added columns) | 28165898 | ee4bc48b42bcc00d001ace666ce6d2c0089e85a8ce7581f5b173db5643eaafbb |
| data/derived/citation_dois.json | 121977 | 90274194505298d6f5e8417c9f5545ed5ed431cda4a4f939c7883820842fedc5 |
| data/derived/openalex.json | 199195 | ff5dba0d64200850c9f111f1f898e2093edf2a627e6a25aec8e2c17ca12a5518 |

## Code run in the browser (hash-checked)

| File | SHA-256 |
|---|---|
| code/common.py | 0a55010627b9ebb33245c7c5af469707e445aa21b910dee1c5ebba59ba3032f2 |
| code/select_records.py | b1b0da2d7986dd1cb18b36e8eb888e12a2b33ffbf8acd4cde4fa437457c78d43 |
| code/analysis.py | 3f65fa8ff6a0532b9e34716628d759bb4532e43ef210ca65d760ea0ed66d6c02 |
| code/citation_sample.py | 8b2e0bb1b97beaad102f157b123398cfa70decbd1254254d15cb2ed1713d5df8 |
| code/citations.py (version 1 run only) | 457992d050d18b9913a451f19be23230172f2072bfc3580fe3f2c6b5e9c0fd38 |
| code/fetch_openalex.js (version 1 run only) | bcbd38f142963f7702ddfc9a6cde9d981b2706c7a572677969e03fc39365f320 |

## Result files (verified byte for byte against the in-browser files)

| File | SHA-256 |
|---|---|
| selection.json | 306a4610e2f0ba098797321964c37f16533ca513d3dbca05736a6f374f4c8a5a |
| trends.json | 1bc08e47690c9d62758fcdaf190114db3c86eccbc6ebbbfa888e29fed051bf63 |
| comparison.json | d7fa5eaf886b1eba15c4533b310e84a58dc3f828c455d5ce835716d76132117c |
| sensitivity.json | aa21067d874a01104f4abfc19972e7f8fb22e0e86bc08a0e8621f8e89be167d8 |
| unmapped_reasons.json | b1eb7955cff51bb25d052400134ee01bd74ff00144793efdabc07c75189b0add |
| citations.json | 02ffb7f3d005bffb3b0ddc188c6f10ba483101f5228f57d1b4a5640d3f4e8e44 |

`summary.json` and `tables.md` are derived locally from these files.
Note: OpenAlex citation counts change over time; re-running `fetch_openalex.py` later will give somewhat different numbers.
