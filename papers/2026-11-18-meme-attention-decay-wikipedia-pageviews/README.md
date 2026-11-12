# How memes fade: comparing decay curves of Wikipedia attention across internet phenomena

Peter Kalafatis, independent researcher. x9m8.com Research Papers series.

Preprint manuscript, data, and code for a study fitting three candidate decay curves
(exponential, power-law, stretched exponential) to the post-peak English Wikipedia pageview
trajectories of 26 real, independently verified internet memes and viral phenomena.

## Headline result

No single decay law describes meme attention uniformly. A stretched exponential has the lowest
AIC for 14 of 26 memes, a plain exponential for 7, and a power-law for 5, but median R² is close
across all three models (0.54–0.58). The much bigger pattern is **between-meme** variation in
whether any smooth decay curve fits at all: seven memes (e.g. `Grumpy Cat`, `Ice Bucket
Challenge`, `Barbenheimer`) have R² above 0.9, while four (`Success Kid`, `Goncharov (meme)`,
`Harlem Shake (meme)`, `Doge (meme)`) have R² below 0.1 for all three models — their attention
collapses to baseline in a day or two with no fittable decay shape at all.

## Data source and a real sandbox constraint, disclosed plainly

All pageview data come from the free, public **Wikimedia REST pageviews API**
(`wikimedia.org/api/rest_v1/metrics/pageviews`), which requires no authentication and covers
July 2015 onward. The sandbox this paper was built in blocks direct outbound HTTPS to
`wikimedia.org`/`en.wikipedia.org`, and the available web-fetch tool could not get timely
permission either (both confirmed by direct testing, not assumed — see `lit/brief.md` §1). The
workaround, consistent with this series' practice on earlier papers that hit the same wall: run
the entire data-collection and curve-fitting pipeline as JavaScript inside a real, logged-in
browser tab (same-origin `fetch()` calls to the API work fine from an `en.wikipedia.org` page),
and bring results back to this sandbox as small, **SHA-256-hash-verified** JSON rather than bulk
raw data (the browser-to-sandbox text channel used could only reliably return ~900 characters per
round trip).

Concretely, this means:
- `pkg/data/raw/meme_fit_summary.json` — peak date, baseline, and all three models' fitted
  parameters/R²/AIC for **all 26 memes** (hash-verified; see below).
- `pkg/data/raw/grumpy_cat_daily_pageviews.json` — **one full raw daily pageview series**
  (426 days around the 2019-05-17 peak), kept as a concrete, hash-verified raw-data sample and
  used for Figure 1 and the independent re-fit in §3.4 of the manuscript.
- The other 25 memes' full daily series are **not** redistributed here, per this series' stated
  practice of not redistributing bulk third-party data. They are fully reproducible on demand:
  `pkg/code/fetch_pipeline.js` documents the exact method and the exact fetch window used for
  every meme, and can be pasted into any browser's JS console on an `en.wikipedia.org` page to
  re-derive every number in this paper from the live API.

### Verifying the provenance hashes yourself

```
python3 -c "
import hashlib
print(hashlib.sha256(open('data/raw/meme_fit_summary.json','rb').read()).hexdigest())
print(hashlib.sha256(open('data/raw/grumpy_cat_daily_pageviews.json','rb').read()).hexdigest())
"
```
Expected: `2eae316a2d79108a357e99686fe5d631a59692854fd161231c803d568ec945e8` and
`e687cc20679ad7d3b67dd8b3767911a45ca67235bda22b1f37e4e3c9bf59eaac` respectively. Both scripts in
`pkg/code/` also assert these hashes before running, so a corrupted or substituted data file will
fail loudly rather than silently produce wrong numbers.

## Repository layout

```
lit/brief.md                         scoping brief: reachability tests, sample construction,
                                      novelty check, literature check, statistical plan
pkg/
  code/
    fetch_pipeline.js                the actual in-browser data-collection + curve-fitting
                                      pipeline (JavaScript), with every meme's exact fetch window
    refit_check.py                   independent scipy.optimize.curve_fit re-derivation of the
                                      Grumpy Cat fit, as a cross-check on the browser-side method
    analyze.py                       loads meme_fit_summary.json, computes summary statistics
    make_figures.py                  all three figures
  data/raw/
    meme_fit_summary.json            26-meme fitted-parameter summary (hash-verified)
    grumpy_cat_daily_pageviews.json  one full raw daily series (hash-verified)
  results/
    summary_stats.json               AIC-win counts, median/mean R² by model
    meme_table.csv                   full per-meme table (Table 1 source)
    grumpy_cat_refit.json            independent scipy re-fit output
  figures/
    fig1_grumpy_cat_decay.png/.pdf   Figure 1
    fig2_model_comparison.png/.pdf   Figure 2
    graphical_abstract.png           900x420 graphical abstract
  manuscript/manuscript.md           full manuscript source (Markdown)
  out/
    Kalafatis_2026_meme-attention-decay.docx   Word manuscript (line-numbered, double-spaced,
                                                Times New Roman, 8.5pt single-spaced tables)
    Kalafatis_2026_meme-attention-decay.pdf    rendered, visually checked PDF (22 pages)
  audits/                            (reserved for the independent audits of this package)
README.md                            this file
```

## Reproducing the analysis from the files in this package

```
cd pkg/code
python3 refit_check.py   # -> pkg/results/grumpy_cat_refit.json
python3 analyze.py       # -> pkg/results/summary_stats.json, meme_table.csv
python3 make_figures.py  # -> pkg/figures/*.png, *.pdf
```

## Reproducing the data collection from scratch (live API)

Open `https://en.wikipedia.org/wiki/List_of_Internet_phenomena` in any browser, open the
JavaScript console, and paste the contents of `pkg/code/fetch_pipeline.js`. The `MEME_FETCH_WINDOWS`
object gives the exact per-meme date ranges used; `fetchDailyPageviews` and `buildSeries`
reproduce the peak-finding and trimming logic; `fitAll` reproduces the curve fitting.

## Status

Preprint manuscript complete and self-checked; not yet independently audited. See
`pkg/manuscript/manuscript.md` §4.5 (Limitations) for honestly disclosed caveats, including the
sample's exclusions, the resurgence-peak ambiguity for several memes, and the degenerate
boundary-solution parameters (e.g. near-zero exponential half-lives) that signal "no real decay
signal" rather than a meaningful fast decay rate.
