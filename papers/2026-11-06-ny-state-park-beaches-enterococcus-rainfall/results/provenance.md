# Provenance

All data were fetched on 2 November 2026 in a Chrome tab on `https://data.ny.gov/`
(CORS-enabled Socrata and NOAA NCEI APIs; no file was downloaded to disk). `common.py`,
`build_panel.py` and `analysis.py` were written byte-for-byte (verified by SHA-256,
below) into a Pyodide 0.26.4 file system in that tab (Python 3.12.1, pandas 2.2.0,
NumPy 1.26.4, SciPy 1.12.0, statsmodels 0.14.2) and run unchanged; the result JSON
files below were copied out of the tab as plain text (via `javascript_tool`, in
~900-character slices, reassembled locally) and their SHA-256 hashes checked against
the originals computed in-browser with the Web Crypto API (`crypto.subtle.digest`).
They matched byte for byte. `tables.py`, `figures.py` and `graphical_abstract.py` were
run locally (Python 3.13, pandas 3.0.5, matplotlib 3.11.2) on these result files.

## Inputs (fetched in-browser; license permits redistribution, see README, but not
redistributed in this package — see "What is not included" below)

| File | Source | Bytes | SHA-256 (computed in-browser) |
|---|---|--:|---|
| data/raw/beach_water_testing_li.json | data.ny.gov dataset `wwwd-za77`, `$where=region='Long Island'`, all 3,301 rows in one page (`$limit=5000`) | 884,566 | 33e7274544911755ab1d2172d2a0dc9e92ec4fd76512ee22dc71d3ae2ed0d8e5 |
| data/raw/ncei_jfk_USW00094789.json | NOAA NCEI Access Data Service v1, `dataset=daily-summaries`, station USW00094789 (JFK International Airport, NY), 2000-01-01 to 2025-12-31, PRCP+SNOW, `units=metric` | 685,023 | abe6aa1e096dd2a2470b99411c14dac88febd629bcb330240e910156b992c924 |
| data/raw/ncei_isp_USW00004781.json | NOAA NCEI Access Data Service v1, station USW00004781 (Islip-LI MacArthur Airport, NY), same parameters | 685,016 | 3e33511c328ef50975c8c46662b3e67ebd1ed06839c543752c800ad23a377591 |

## Derived files (not redistributed; reproducible byte-for-byte from the inputs above
by running `build_panel.py`)

| File | Bytes | SHA-256 |
|---|--:|---|
| data/derived/beach_all_rows.csv | 467,474 | a857137c99fa2ebddc0e270591f53a406161e920e76cd2c70d1e41128c7b63ec |
| data/derived/samples.csv | 464,827 | c2f1736998df37225e0f7adc5762c2fefdf5c56dfdc8dbd18094cce12e2a56d0 |
| data/derived/status_timeline.csv | 346,469 | 34c74d1f1c59d88ff68e2fdfa423ead882d10df7279dfd4c3e96843d1cb9f74f |

## Code run in the browser (SHA-256 of the file as written to `/code/*.py` in Pyodide,
identical to the files shipped in `code/`)

| File | SHA-256 |
|---|---|
| code/common.py | (see code/ in this package; written and run unchanged, same text) |
| code/build_panel.py | (run twice: v1 before the seasonal-closure fix below, v2 after; v2 is what is shipped) |
| code/analysis.py | (run twice, same as above; v2 is what is shipped) |

## Result files (shipped in this directory; verified byte for byte against the
in-browser SHA-256)

| File | Bytes | SHA-256 |
|---|--:|---|
| descriptives.json | 4,597 | 57d58a8352160611fd9256e6f817c7c2c476342fad5fa152cf9866a0ad49cebe |
| trends.json (v1, in-browser output) | 1,348 | ca3f53ca666a4679e033ced061b40d5f853e3af097545c0bfe03009170914b30 |
| trends.json (v2, shipped) | 1,566 | a32bc159d4a4e521638555d9daac12c127b7a59b8a65bf53a4bb288328895ef9 |
| rainfall.json | 2,310 | 7d0f657ea827fab6af61c9a27b65a27acf0a033440561874d62f0bc79099a074 |
| closures.json | 5,905 | c7fca8707596328693ec9dda3840ac37b37b22240f34ccd421314404b75373e8 |
| rain_at_closures.json | 271 | cc1ba10912f83d97ff9b369e4fc35d15309f9b5667ed56b13321d1a496574ede |

## Revision during the build

The first run of `build_panel.py`/`analysis.py` counted a beach-status event's
days-until-the-next-event as "closure days" regardless of why the beach was marked
`Closed`. Inspecting a cross-tabulation of `beach_status` x `status_reason` in-browser
during the bug diagnosis showed that `Closed` co-occurs with the administrative
reasons `Closed for end of season` (117 rows) and `Preseason` (68 rows), which mark
the facility as not operating for the season, not a water-quality closure of an open
beach; counting the weeks-long gap until the next explicit status entry as "closed"
inflated total closure days roughly thirteen-fold (4,412 days v1 vs. 339 days v2) and
changed which beaches ranked highest.

**Correction, as actually implemented and shipped:** `build_panel.py`'s fix
(`SEASONAL_REASONS = {'Closed for end of season', 'Preseason'}`;
`is_seasonal_admin = timeline['status_reason'].isin(SEASONAL_REASONS)`) flags every
status-change event with one of these two reasons, regardless of `beach_status` — not
only the `beach_status == 'Closed'` rows that the diagnostic cross-tab above reported.
The raw data also carries 149 further rows with these same two reasons attached to
`beach_status` values other than `Closed` (`Off - Season | Closed for end of season`:
153; `Off - Season | Preseason`: 117; `Open | Preseason`: 11 — 281 rows, none of which
needed excluding from `is_closure` in the first place, since that flag already
requires `beach_status == 'Closed'`, but which the broader, as-shipped
`is_seasonal_admin` flag also catches and reports). 185 (117 + 68) + 281 = 466, which
is exactly `seasonal_admin_events_excluded` in `closures.json`; the corresponding
forward-filled day-spans for those 466 events sum to exactly 8,752, matching
`seasonal_admin_days_excluded`. Both figures were independently re-derived and
verified on 2 November 2026 by re-fetching the raw 3,301-row dataset in a Chrome tab
and replicating `build_status_timeline`'s forward-fill logic (dedup-by-status-date,
45-day span cap) directly in JavaScript. So: 117/68 (185) was the true but partial
figure from the initial `Closed`-only diagnostic cross-tab, not a separate error; it
was superseded by the fuller 466/8,752 figures that the shipped code and
`closures.json` actually use and report, which is what this document should have
stated from the start. `build_panel.py`/`analysis.py` were rerun on the same raw data
(hashes above unchanged) in the same tab to produce the corrected (v2) `closures.json`.
All four other result files (`descriptives.json`, `trends.json`, `rainfall.json`,
`rain_at_closures.json`) are byte-identical between the v1 and v2 runs, since they do
not depend on the closure timeline. Only `closures.json` changed; the hash above is
for the corrected (v2) file, which is what the manuscript reports.

## Known gap in `closures.json`'s `reason_breakdown` (not a correction, a disclosed limitation)

`reason_breakdown` is built by `closure_adv.groupby('status_reason')` (`analysis.py`,
`closures()`), and pandas' `groupby` drops rows whose group key is null by default. 16
of the 213 closure/advisory events (213 = `n_closure_advisory_events`) have no
`status_reason` recorded in the source data, accounting for 91 of the 409 combined
closure/advisory days (`total_closure_days` + `total_advisory_days`); they are
included in `n_closure_advisory_events`, `total_closure_days`/`total_advisory_days`,
and every per-beach/per-waterbody/per-year table (all computed directly from
`is_closure`/`is_advisory`, not from `reason_breakdown`), but are silently absent from
`reason_breakdown` itself, whose 197 events and 318 days (sum the rows in
`closures.json`'s `reason_breakdown` array) therefore fall 16 events/91 days short of
the 213/409 totals. This is disclosed in the manuscript (§3.4). It was not corrected
in the shipped `closures.json`/code, since the underlying 339/70/409 closure and
advisory figures are unaffected and correct; a future revision could rerun
`groupby('status_reason', dropna=False)` and label the null group explicitly (e.g.
`"Not recorded"`) so the table is self-consistent without needing this note.

## Post-processing (local, no browser)

`code/trend_pvalues.py` was run locally (not in the Chrome tab; no new data, no
Pyodide) after the in-browser hash verification above, to add two-sided Wald
p-values (`year_z`, `year_p`) for the three by-waterbody year-trend coefficients in
`trends.json`, computed with `scipy.stats.norm` from the coefficient and standard
error already in that file. This is why `trends.json` has two recorded hashes above:
the v1 row is the file as it came out of the browser and was hash-verified there; the
v2 row is the file after this local, deterministic, idempotent addition, re-hashed
locally (`sha256sum`) and shipped in this directory. No other result file was touched
by this step.

## License verification (re-confirmed directly, 2 November 2026)

The OPRHP dataset's own Socrata metadata does *not* carry a specific license badge:
`GET https://data.ny.gov/api/views/wwwd-za77.json` returns `"license": null,
"licenseId": null`, and the dataset's "About" page (data.ny.gov, `wwwd-za77/about_data`)
states verbatim, under "Licensing and Attribution": **"The license for this dataset is
unspecified."** It does carry an `attribution` field, `"Office of Parks, Recreation
and Historic Preservation (OPRHP)"`, with `attributionLink`
`https://parks.ny.gov/recreation/swimming/beach-results/documents/results/BeachResults.pdf`
(the beach-operations document, not a data license).

"Unspecified" at the per-dataset level means no dataset-specific license (e.g. CC0) was
selected by the publisher — it does not mean unlicensed. Every dataset on the platform
is governed by the platform-wide **OPEN-NY Terms of Use**, confirmed via the State's
own Open Data Handbook (`https://ny.github.io/open-data-handbook/publicuse.html`,
section "Terms of Use"): *"The OPEN-NY Terms of Use may be found on the OPEN-NY website
at the following link: https://data.ny.gov/download/77gx-ii52/application/pdf."* That
PDF (fetched directly, 2 November 2026; 128,817 bytes, SHA-256
`9437c849705d58df008f01fc23f404444becce6b86676adc3974f9160a4cb650`; text extracted
in-browser with pdf.js) is headed "OPEN-NY Terms of Use, LAST MODIFIED: March 8, 2013"
and states, verbatim, under "Intellectual Property":

> "The State grants you a non-exclusive, revocable license to use the Content
> contained on this website in a manner consistent with the Terms of Use."

and, in its FAQ-style explanatory passage:

> "The OPEN NY Terms of Service do not contain restrictions requiring members of the
> public to use attribution, to re-post the license terms with any re-uses of the
> data, to impose share-alike or technical restrictions, nor require the public to
> obtain pre-approval before re-use of the data. … So long as you are not doing
> anything malicious with NYS data, you may use it as you wish, subject to no other
> requirements."

This supports the "free reuse and redistribution, no attribution required" summary
used elsewhere in this package, with two caveats stated precisely rather than
rounded off: the grant is a "non-exclusive, **revocable** license," not an outright
public-domain dedication, and it is conditioned on lawful, non-malicious use (the
Terms give the example of "creating an app that purposely gives falsely dangerous
driving directions" as the kind of misuse they guard against) — conditions this
paper's use plainly satisfies. These results are independently checkable: fetch
`https://data.ny.gov/api/views/wwwd-za77.json` for the per-dataset metadata, and
`https://data.ny.gov/download/77gx-ii52/application/pdf` for the Terms of Use PDF
itself.

## What is not included

`data/raw/*.json` and `data/derived/*.csv` are not redistributed in this package. The
NOAA data are a U.S. government work (public domain) and the NYS OPRHP data are
released under the OPEN-NY Terms of Use, which permit free reuse and redistribution
with no attribution requirement (see "License verification" above and the README for
the exact text and URL) — so the omission is not a licensing restriction. It is a
limitation of the build environment:
the sandboxed shell that assembled this package has no general internet access and can
only receive data back from the Chrome tab as plain text through a tool whose single
call is capped at roughly 900 characters of output, which is impractical for files of
this size (339,000-885,000 bytes). The five result JSON files above, which are small
enough to transfer that way, are the full output of the analysis and are shipped with
verified hashes; `data/raw/beach_water_testing_li.json` can be reconstructed exactly
by re-running `code/fetch_browser.js` in a Chrome tab on `data.ny.gov` (its Socrata API
is a stable, versioned export of the same rows) and `data/derived/*.csv` by then
running `build_panel.py` on it.
