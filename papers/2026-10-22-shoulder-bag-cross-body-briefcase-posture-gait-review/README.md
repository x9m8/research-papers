# Bags and the body: one-shoulder, cross-body and hand-carried bags in adults

Scoping review and evidence map. Kalafatis (2026), preprint, x9m8.com. Contact: x9m8x7@gmail.com.

## Contents
- `data/search_log.md` all Europe PMC query strings, hit counts, other sources and the flow of records.
- `data/studies.csv` screening record for the 65 reports assessed in detail (decision, reason, DOI, URL).
- `data/extraction.csv` values extracted from full texts (tables/text only; nothing digitised from figures).
- `data/map_coding.csv` evidence-map coding (population, bag type, outcome domain, n) for every report.
- `code/` run from inside `code/`: `effects.py` -> `evidence_map.py` -> `figures.py` -> `tables.py` -> `graphical_abstract.py`.
  `tables.py` rewrites the `## Tables` section of `manuscript/manuscript.md`, overwriting manual edits there.
- `results/` effect sizes (all r scenarios), map counts. `audits/` independent number and citation audits.

## Requirements
Python 3.10+, pandas, numpy, matplotlib.

## Licence
Code MIT; coding and extraction tables CC BY 4.0.
