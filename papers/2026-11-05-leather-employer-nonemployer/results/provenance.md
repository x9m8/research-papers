# Provenance

Source files fetched 2 November 2026 in a Chrome tab on www2.census.gov (JavaScript fetch, SHA-256 via Web Crypto, in-browser unzip). Per-file URLs, sizes and hashes: `data/source_files.csv`.

| Extract (in package) | Rows | SHA-256 (in-browser original = package file) |
|---|--:|---|
| data/raw/cbp_naics316_us_2004_2023.csv | 308 + header | 1191ea1e4136fcb3d38bcc21f2961a70fb2227f8091ddfa6f0e74988882e9c82 |
| data/raw/nonemp_naics316_us_2004_2024.csv | 183 + header | 0a6752ab014f5c65470835069de7bfc75c0772fb594d8a31fb3d147887650ca6 |

Notes: the extract step (in the browser) kept only all-legal-form rows for NAICS 00, 31-33 (CBP code 31----) and 316*, recoded NAICS strings, and for NES kept receipts-size class 001. The NES 2007 national file was rejected by the server ("Request Rejected" page); 2007 values were summed from `nonemp07st.txt` (sha256 f34c4da26c5ab8b79a1c93ebe496313ad1d99959ab423244ff03198e9c72f792); the same method reproduces the 2006 national values exactly. The extraction JavaScript is not stored as a script; its logic is described in README and Methods. All Python (build_series.py onward) was run locally with Python 3.13, pandas 3.0.5.

**2007 state-level support for the NAICS 316 total of 5,148 firms.** On 2 November 2026, `nonemp07st.txt` was re-fetched in a Chrome tab (same URL and SHA-256 as above, confirmed byte-for-byte against the hash already recorded in `data/source_files.csv`), and the 51 NAICS-316 state/DC rows were parsed and summed with in-page JavaScript (no raw file content was pulled through the tool interface). The 51 rows, with each state's `ESTAB` value and any suppression flag, are in `data/raw/nonemp07_naics316_by_state.csv`. Summing the 49 reported rows gives 5,148, matching the national total used in the manuscript exactly; Rhode Island and Vermont are withheld ("D") in this file, confirming the manuscript's statement that the figure is a lower bound. This table lets a reader verify the 5,148 sum directly from package contents rather than from `nonemp07st.txt` alone.

**Spot-check of `data/source_files.csv` against the live server (2 November 2026).** Seven of the 41 listed source files were re-checked in a Chrome tab: `cbp04us.txt` and `nonemp04us.txt` (full SHA-256 recomputed, both matched the recorded hash exactly), `cbp12us.zip`, `cbp23us.zip` and `nonemp16us.zip` (HTTP 200, `Content-Length` and `Last-Modified` matched the recorded byte size and header exactly), `nonemp24us.zip` (same, exact match), and `nonemp07st.txt` (full SHA-256 recomputed as part of the 2007 state-sum check above, exact match). All seven URLs resolved and every size, hash and `Last-Modified` value checked was identical to what is recorded in `data/source_files.csv`; no discrepancies were found.

**CBP 2024 directory check (2 November 2026).** The directory listing at `https://www2.census.gov/programs-surveys/cbp/datasets/` was checked again; the last subdirectory listed is still `2023/`. No CBP 2024 directory has been posted as of this date, consistent with Section 2.1.
