# What chrome buys — reproducibility package

Kalafatis, P. (2026). *What chrome buys: a meta-analysis of paired chrome-free and chrome leather tests* [Preprint, not peer reviewed]. x9m8.com.

## Contents
- `code/` — Python 3.13 with pandas, NumPy, SciPy, statsmodels and matplotlib. Run in this order from `code/`:
  1. `screen.py` — merges the OpenAlex and Europe PMC exports, deduplicates (DOI, then normalised title), applies the rule-based pre-screen → `results/records_dedup.csv`, `results/prescreen_counts.json`.
  2. `prisma.py` — study-flow counts from the pre-screen, the manual title/abstract decisions and the full-text log → `results/prisma.json`, `results/fulltext_log.csv`.
  3. `meta.py` — log ratios of means, two-level random-effects model (REML) with shared-control covariance, cluster-robust check, Paule–Mandel two-stage check, sensitivity, leave-one-out, moderators, small-study test; shrinkage-temperature descriptives; reporting counts → `results/effects.csv`, `results/meta.json`, `results/ts_descriptive.csv`.
  4. `figures.py` (uses `style.py`) → `figures/fig1_forest_tensile`, `fig2_pooled_sensitivity`, `fig3_shrinkage` (.png 300 dpi and .pdf).
  5. `tables.py` → `results/tables.md` and the Tables section of `manuscript/manuscript.md`.
  6. `graphical_abstract.py` → `figures/graphical_abstract.png` (900 × 420 px).
- `data/extraction/` — the author's own data (CC BY 4.0):
  - `screening_ta_manual.csv` — title/abstract decision for each of the 429 records that passed the pre-screen.
  - `fulltext_screening.csv` — decision and reason for each full text obtained.
  - `extraction.csv` — one row per chrome-free arm and outcome: means, SDs, n, units, and the table or text location of every value (`source`).
  - `replicates.csv` — individual replicate values (Aguilar et al., 2023).
  - `study_characteristics.csv` — comparator source, developer status, integrity flag.
  - `env_chem_evidence.csv` — the narrative table of chemical, effluent, LCA and end-of-life results, with what each extraction rests on.
- `results/`, `figures/`, `manuscript/` (manuscript.md, patch_docx.py), `out/` (Word and PDF), `audits/` (empty until the independent audits are run).

## Data sources
- OpenAlex REST API (https://api.openalex.org/works), queried 21–22 October 2026; metadata CC0. Query strings in `data/raw/search_searchmeta.jsonl`.
- Europe PMC REST API (https://www.ebi.ac.uk/europepmc/webservices/rest/search), queried 21–22 October 2026; three Boolean queries listed in the same file.
- Full texts of the included and excluded studies were read from open-access copies (publisher sites, PubMed Central, journal repositories); the DOI of each is in `fulltext_screening.csv`.

## Not redistributed
- `data/raw/search_*.jsonl` and `results/records_dedup.csv` contain publishers' abstracts. They are kept for the author's records but are not part of the public package; they can be rebuilt from the APIs above with the listed queries (OpenAlex results change over time).
- Full texts of articles are not redistributed.

## Notes and known issues
- `integrity_flag` in `study_characteristics.csv`: 1 = Atinafu & Teferi (2026), phrases typical of generated text, excluded from the primary analyses; 2 = Aguilar et al. (2023), same article published twice in one issue with unregistered DOIs, retained and reported without it. Gómez-García et al. (2026) has editing residue but is not flagged; it is reported without it.
- Undocumented-arm omissions are listed in `fulltext_screening.csv` (`notes`): Gómez-García tara and quebracho arms (table not captured), Atinafu tensile (ranges), Qiao F-90 (composition not stated).
- Cluster-robust SEs are CR1 and are close to the model SEs by construction; CR2 was not implemented. Prediction intervals use t on k − 2 df.
- The DOI printed on Aguilar et al. (2023) (10.47750/pnr.2023.14.S02.23) did not resolve in Crossref or doi.org during checking; the same article was published again in the same issue (pp. 269–282, printed DOI 10.47750/pnr.2023.14.s02.34) and was treated as a duplicate report.
- Crossref lists Chakraborty et al. with the placeholder year 1970; the article's running header gives 2008. Crossref lists "Author" as the only author of Valeika et al. (2010); names were taken from the article.
- Where n was not stated it is set to 3 in `meta.py` (sensitivity at 2 and 5).

AI use: searching, screening, extraction, analysis code and drafting were done with Claude (Anthropic, claude-opus-5-5) in October 2026 under the author's direction; the author reviewed all outputs.
