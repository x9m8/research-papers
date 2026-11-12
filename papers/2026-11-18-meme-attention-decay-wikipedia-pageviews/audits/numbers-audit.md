# Numbers audit — "How memes fade" (p30)

Independent auditor. All checks below were re-derived from scratch (own code, own
optimizer/fetches), not by re-running the authors' scripts unmodified, except where noted.

## CONFIRMED ISSUES

1. **Half-life claim misattributes "under half a day" to the wrong meme (§3.1).** The text says:
   "several of the fitted exponential half-lives reflect directly (under half a day for `Harlem
   Shake (meme)` and `Doge (meme)`)." Checking `results/meme_table.csv` / `data/raw/meme_fit_summary.json`:
   `exp_halflife_days` = Harlem_Shake 0.05 (yes, <0.5), **Doge (meme) 0.96 (not <0.5)**. The meme
   that actually has a sub-half-day half-life among the four poor-fit memes is `Success Kid`
   (0.42 days), not Doge. I independently re-fetched Doge's pageviews via Chrome and refit it
   (exp k=0.72, half-life = ln(2)/0.72 ≈ 0.96 days), confirming the underlying number (0.96) is
   itself correct — the manuscript text is simply citing the wrong meme name. Fix: replace "Doge
   (meme)" with "Success Kid" in that sentence, or drop the specific examples.

2. **Discussion §4.5's generalization about short half-lives overreaches.** "(for example
   ... several memes' exponential half-lives under half a day) are visibly degenerate boundary
   solutions reflecting a poor underlying fit (R² near 0)." This is not true of all such cases:
   `T-pose` has exp half-life 0.29 days (<0.5) but R²=0.854 (a genuinely good, non-degenerate
   fast-decay fit), and `Woman yelling at a cat` (0.27 days) has R²=0.28–0.68 depending on model,
   not uniformly "near 0." Only `Harlem Shake` (0.05) and `Success Kid` (0.42, see #1) among the
   sub-half-day cases are actually poor fits. Minor wording issue, not a data error, but it
   overstates how the two patterns (short half-life, poor fit) correlate.

## VERIFIED / CONFIRMED FINE

- **SHA-256 hashes**: both reproduced independently. `meme_fit_summary.json` →
  `2eae316a2d79108a357e99686fe5d631a59692854fd161231c803d568ec945e8` ✓. `grumpy_cat_daily_pageviews.json`
  → `e687cc20679ad7d3b67dd8b3767911a45ca67235bda22b1f37e4e3c9bf59eaac`, 426 points ✓.
- **Grumpy Cat refit, fully independent**: wrote a fresh fitting script (not `refit_check.py`),
  using `scipy.optimize.differential_evolution` (global optimizer) + Nelder-Mead polish instead
  of the paper's `curve_fit`/Levenberg-Marquardt. Got R² exp=0.9839, power-law=0.9932, stretched
  exp=0.9927 — matches the claimed values to 4 decimals. Re-running the authors' own
  `refit_check.py` also reproduces identically. This is the most solid result in the paper.
- **Independent re-fetch/re-fit of 6 memes via Chrome** (Harambe, Salt Bae, Ice Bucket Challenge
  — clean decay; Success Kid, Doge, Harlem Shake — reported unfittable), using a fresh JS
  Nelder-Mead implementation written for this audit: peak dates and peak view counts matched
  the manuscript exactly for all 6 (e.g. Harambe peak 19,880 views on day 0, Doge 111,957, etc.).
  R² values matched closely: Salt Bae and Ice Bucket Challenge matched to 3-4 decimals on all
  three models; Success Kid, Doge, Harlem Shake all independently confirmed R²<0.1 on all three
  models and the reported AIC-winning model. Harambe's power-law fit initially looked off
  (I got R²=0.788 vs. reported 0.7516) until I added the same non-negativity floor constraint
  (c≥0) the paper's model specifies — with that constraint my fit converges to A=45337.6,
  α=0.862, c=0, R²=0.7516, exactly matching. No real discrepancy; good reproduction.
- **AIC-win tally**: recounted `best_model` directly from `meme_table.csv`: stretched exp=14,
  exponential=7, power-law=5, sum=26. Matches `summary_stats.json` exactly, and matches every
  instance in the abstract, §3.2, and the Conclusion — no drift anywhere in the final text.
- **Median/mean R²** (0.54/0.58/0.58 median; 0.56/0.55/0.58 mean) recomputed from the raw per-meme
  R² values in `meme_fit_summary.json` — matches `summary_stats.json` and the manuscript text.
- **Nyan Cat three-way tie**: confirmed — exp, power-law, and stretched-exp R² are all 0.4576
  (identical to 4 decimals) in the raw data, exactly as claimed.
- **Goncharov τ≈72,000 days**: raw data gives se.tau=71978.315 — matches "nearly 72,000 days."
- **Four "no fittable decay" memes genuinely R²<0.1 for all three models**: confirmed from raw
  data (Success Kid ≤0.0037, Goncharov ≤0.0202, Harlem Shake 0.034, Doge ≤0.0645) — all <0.1,
  and no other meme in the 26 also qualifies (Big Chungus comes closest at 0.1119, just over).
  This also matches `n_poor_fit_all_models_r2_below_0.1: 4` and `n_good_fit_best_model_r2_above_0.9: 7`.
- **Abstract/Results/Table/Discussion consistency**: no sign of the earlier "6/6" vs "7/5" drift
  the brief asked me to check for — all four locations now consistently say 14/7/5.
- **~900-character browser→sandbox transfer constraint**: independently reproduced — fetching a
  full year of daily data and returning the raw JSON through the JS tool truncates well short of
  the full payload (confirmed truncation occurs, consistent with the stated constraint, though I
  did not pin down the exact byte count as precisely "900").
- **Direct network access blocked in this sandbox**: confirmed — curl/WebFetch to wikimedia.org
  fail here; same-origin `fetch()` from a live Chrome tab on en.wikipedia.org works and was used
  for all independent re-fetches above.

## MINOR / SOFT FINDING (not a numbers error per se)

- **Sharknado exclusion reason, checked directly**: I fetched Sharknado's full post-July-2015
  pageview series. Its true maximum (76,206 views) falls on **2015-07-23**, about three weeks
  into the dataset — not literally "the very first day of the fetched range" as §2.2 states.
  The underlying concern (no real pre-peak baseline inside the window, since the dance craze
  predates the data) is legitimate, but the specific phrasing is imprecise; "within the first
  month of the data" would be accurate, "the very first day" is not. I did not check Caramelldansen
  or Loituma in the same way (time-boxed), so I can't say whether the same imprecision recurs there.
- **Kony 2012 exclusion**: checked directly — max pageviews anywhere in the July2015–Nov2026
  window is 18,375, far below what a true viral peak would show, consistent with "only thin,
  disconnected secondary spikes." Reason holds up.

Not checked in depth (out of scope/time): `code/make_figures.py` figure-generation fidelity;
the remaining 20 memes' fits (no raw series available to re-fetch and verify beyond the 6
sampled); film-exclusion rationale for Morbius/Dear Evan Hansen/West Side Story/Saltburn.
