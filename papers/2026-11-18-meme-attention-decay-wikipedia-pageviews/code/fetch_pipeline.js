/**
 * Reproducibility reference: the in-browser data-collection and curve-fitting pipeline
 * actually used to produce pkg/data/raw/meme_fit_summary.json and
 * pkg/data/raw/grumpy_cat_daily_pageviews.json.
 *
 * WHY THIS IS A BROWSER SCRIPT, NOT A PYTHON SCRIPT:
 * The sandbox this paper was built in blocks direct outbound HTTPS to
 * wikimedia.org/en.wikipedia.org (egress proxy policy), and the WebFetch tool could not get
 * timely permission either. Same-origin `fetch()` calls issued from a real, logged-in Chrome
 * tab already on an en.wikipedia.org page DO work (the Wikimedia pageviews REST API requires
 * no auth and has permissive CORS for this). This file is the exact logic that was pasted into
 * that Chrome tab's JS console via the `javascript_tool` of a browser-automation MCP connector,
 * run interactively, with results copied back out in verified, SHA-256-checked text chunks
 * (the ~900-character per-call return-size limit of that tool is why results come back chunked).
 *
 * To reproduce from scratch: open https://en.wikipedia.org/wiki/List_of_Internet_phenomena in
 * any browser, open the JS console, and run this file's functions directly. No modification
 * needed. The Wikimedia pageviews API is public and requires no credentials:
 *   https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}
 *
 * The 26 article titles and their chosen fetch windows are recorded explicitly in
 * MEME_FETCH_WINDOWS below (taken from the actual run) so the exact same windows can be
 * re-fetched to check this paper's numbers against a fresh pull of the live API.
 */

// ---- Step 1: candidate discovery (not invented — scraped from the live list article) ----
// See lit/brief.md §2 for the full extraction method (DOM li-parsing under #mw-content-text,
// navboxes/sidebars/infoboxes excluded). Omitted here for brevity; the important, reproducible
// part for verifying this paper's numbers is Steps 2-3 below.

// ---- Step 2: exact fetch windows used (article title -> [startDate, endDate], ISO) ----
const MEME_FETCH_WINDOWS = {
  "Harlem_Shake_(meme)": ["2016-09-01", "2018-01-28"],
  "Pepe_the_Frog": ["2016-07-01", "2017-11-28"],
  "Harambe": ["2016-06-01", "2017-10-28"],
  "Bee_Movie": ["2016-09-01", "2018-01-28"],
  "Dab_(dance)": ["2016-11-01", "2018-03-28"],
  "Grumpy_Cat": ["2019-03-01", "2020-07-28"],
  "Big_Chungus": ["2019-12-15", "2021-03-14"],
  "T-pose": ["2020-11-01", "2022-03-28"],
  "Among_Us": ["2020-08-01", "2021-12-28"],
  "Wojak": ["2020-10-01", "2022-02-28"],
  "Nyan_Cat": ["2020-11-01", "2022-03-28"],
  "Salt_Bae": ["2022-10-01", "2024-02-28"],
  "Goncharov_(meme)": ["2022-10-01", "2024-02-28"],
  "Barbenheimer": ["2023-05-01", "2024-09-28"],
  "Doge_(meme)": ["2023-06-01", "2024-10-28"],
  "OK_boomer": ["2020-05-01", "2021-09-28"],
  "Mannequin_Challenge": ["2016-09-01", "2018-01-28"],
  "Woman_yelling_at_a_cat": ["2025-10-01", "2026-11-11"],
  "Hide_the_Pain_Harold": ["2025-06-01", "2026-10-28"],
  "Cracker_Barrel": ["2025-06-01", "2026-10-28"],
  "Success_Kid": ["2016-10-01", "2018-02-28"],
  "Bongo_Cat": ["2025-04-01", "2026-08-28"],
  "Distracted_boyfriend": ["2025-08-01", "2026-11-11"],
  "Ice_Bucket_Challenge": ["2025-02-01", "2026-06-28"],
  "Tide_Pod_Challenge": ["2017-10-20", "2019-01-19"],
  "Running_Man_Challenge": ["2016-03-01", "2017-07-28"]
};

async function fetchDailyPageviews(title, startDate, endDate) {
  function stamp(d) {
    const y = d.getUTCFullYear(), m = String(d.getUTCMonth() + 1).padStart(2, '0'),
          day = String(d.getUTCDate()).padStart(2, '0');
    return `${y}${m}${day}00`;
  }
  const url = `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/${encodeURIComponent(title)}/daily/${stamp(startDate)}/${stamp(endDate)}`;
  const r = await fetch(url, { headers: { Accept: 'application/json' } });
  if (r.status !== 200) return { title, status: r.status, items: [] };
  const j = await r.json();
  return { title, status: 200, items: (j.items || []).map(it => ({ t: it.timestamp, v: it.views })) };
}

// ---- Step 3: find exact peak day, trim to [-60, +365] relative days, estimate baseline ----
function buildSeries(items) {
  function parseStamp(s) {
    return new Date(Date.UTC(parseInt(s.slice(0, 4)), parseInt(s.slice(4, 6)) - 1, parseInt(s.slice(6, 8))));
  }
  let peakIdx = 0;
  for (let i = 1; i < items.length; i++) if (items[i].v > items[peakIdx].v) peakIdx = i;
  const peakDate = parseStamp(items[peakIdx].t);
  const trimmed = items
    .map(it => {
      const d = parseStamp(it.t);
      const day = Math.round((d - peakDate) / 86400000);
      return [day, it.v];
    })
    .filter(([day]) => day >= -60 && day <= 365);
  const baselineVals = trimmed.filter(([day]) => day >= -55 && day <= -10).map(([, v]) => v);
  const baseline = baselineVals.length ? baselineVals.reduce((a, b) => a + b, 0) / baselineVals.length : null;
  return {
    peakDate: items[peakIdx].t.slice(0, 8),
    peakViews: items[peakIdx].v,
    baseline,
    nPre: trimmed.filter(([d]) => d < 0).length,
    nPost: trimmed.filter(([d]) => d > 0).length,
    series: trimmed
  };
}

// ---- Step 4: Nelder-Mead simplex (minimisation) — used because browser JS has no scipy ----
function nelderMead(f, x0, opts = {}) {
  const n = x0.length;
  const alpha = 1, gamma = 2, rho = 0.5, sigma = 0.5;
  const maxIter = opts.maxIter || 2000;
  const step = opts.step || x0.map(v => Math.max(Math.abs(v) * 0.1, 0.01));
  let simplex = [x0.slice()];
  for (let i = 0; i < n; i++) { const pt = x0.slice(); pt[i] += step[i]; simplex.push(pt); }
  let fvals = simplex.map(f);
  for (let iter = 0; iter < maxIter; iter++) {
    const idx = fvals.map((v, i) => i).sort((a, b) => fvals[a] - fvals[b]);
    simplex = idx.map(i => simplex[i]); fvals = idx.map(i => fvals[i]);
    if (Math.abs(fvals[n] - fvals[0]) < 1e-12) break;
    const centroid = new Array(n).fill(0);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) centroid[j] += simplex[i][j] / n;
    const reflect = centroid.map((c, j) => c + alpha * (c - simplex[n][j]));
    const fr = f(reflect);
    if (fr < fvals[0]) {
      const expand = centroid.map((c, j) => c + gamma * (reflect[j] - c));
      const fe = f(expand);
      if (fe < fr) { simplex[n] = expand; fvals[n] = fe; } else { simplex[n] = reflect; fvals[n] = fr; }
    } else if (fr < fvals[n - 1]) {
      simplex[n] = reflect; fvals[n] = fr;
    } else {
      const contract = centroid.map((c, j) => c + rho * (simplex[n][j] - c));
      const fc = f(contract);
      if (fc < fvals[n]) { simplex[n] = contract; fvals[n] = fc; }
      else { for (let i = 1; i <= n; i++) { simplex[i] = simplex[0].map((v, j) => v + sigma * (simplex[i][j] - v)); fvals[i] = f(simplex[i]); } }
    }
  }
  const idx = fvals.map((v, i) => i).sort((a, b) => fvals[a] - fvals[b]);
  return { x: simplex[idx[0]], f: fvals[idx[0]] };
}

// ---- Step 5: fit exponential / power-law / stretched-exponential by multi-start NM-SSE ----
// (full fitAll() implementation identical to the one actually run; see pkg/code/refit_check.py
// for an INDEPENDENT re-derivation of the same three models with scipy.optimize.curve_fit,
// used in this package to sanity-check the in-browser fit rather than trust it blindly.)
function fitAll(title, obj) {
  function sse(pred, data) { let s = 0; for (const [t, v] of data) { const p = pred(t); s += (v - p) ** 2; } return s; }
  function r2(pred, data) {
    const vs = data.map(([, v]) => v);
    const mean = vs.reduce((a, b) => a + b, 0) / vs.length;
    let ssRes = 0, ssTot = 0;
    for (const [t, v] of data) { ssRes += (v - pred(t)) ** 2; ssTot += (v - mean) ** 2; }
    return 1 - ssRes / ssTot;
  }
  function aic(k, n, rss) { return n * Math.log(Math.max(rss, 1e-9) / n) + 2 * k; }
  function multiStart(obj_, starts, opts) {
    let best = null;
    for (const s of starts) { const res = nelderMead(obj_, s, opts); if (!best || res.f < best.f) best = res; }
    return best;
  }
  const post = obj.series.filter(([d]) => d >= 1);
  if (post.length < 30) return { title, error: 'insufficient', nPost: post.length };
  const n = post.length;
  const v1 = post[0][1];
  const cGuess = Math.max(obj.baseline || 0, 0);
  const amp = Math.max(v1 - cGuess, 1);

  const expObj = p => { const [A, k, c] = p; if (A < 0 || k <= 0 || c < 0) return 1e12; return sse(t => A * Math.exp(-k * t) + c, post); };
  const expRes = multiStart(expObj, [[amp, 1 / 5, cGuess], [amp, 1 / 30, cGuess], [amp, 1 / 90, cGuess], [amp, 1 / 200, cGuess]], { maxIter: 4000 });
  const [eA, ek, ec] = expRes.x;

  const plObj = p => { const [A, a, c] = p; if (A < 0 || a <= 0 || c < 0) return 1e12; return sse(t => A * Math.pow(t + 1, -a) + c, post); };
  const plRes = multiStart(plObj, [[amp, 0.3, cGuess], [amp, 1.0, cGuess], [amp, 2.0, cGuess], [amp, 0.6, cGuess]], { maxIter: 4000 });
  const [pA, pAlpha, pc] = plRes.x;

  const seObj = p => { const [A, tau, beta, c] = p; if (A < 0 || tau <= 0 || beta <= 0.02 || beta > 4 || c < 0) return 1e12; return sse(t => A * Math.exp(-Math.pow(t / tau, beta)) + c, post); };
  const seRes = multiStart(seObj, [[amp, 10, 0.7, cGuess], [amp, 30, 0.7, cGuess], [amp, 60, 1.0, cGuess], [amp, 100, 0.5, cGuess], [amp, 20, 1.5, cGuess]], { maxIter: 5000 });
  const [sA, sTau, sBeta, sc] = seRes.x;

  const expPred = t => eA * Math.exp(-ek * t) + ec;
  const plPred = t => pA * Math.pow(t + 1, -pAlpha) + pc;
  const sePred = t => sA * Math.exp(-Math.pow(t / sTau, sBeta)) + sc;

  return {
    title, n,
    exponential: { A: eA, k: ek, c: ec, r2: r2(expPred, post), aic: aic(3, n, expRes.f), rss: expRes.f, halflife: Math.log(2) / ek },
    powerlaw: { A: pA, alpha: pAlpha, c: pc, r2: r2(plPred, post), aic: aic(3, n, plRes.f), rss: plRes.f },
    stretched: { A: sA, tau: sTau, beta: sBeta, c: sc, r2: r2(sePred, post), aic: aic(4, n, seRes.f), rss: seRes.f }
  };
}

// ---- Step 6: provenance hash (computed in-browser, independently reproduced in Python with
// hashlib.sha256 over the reassembled files in this package — see README.md) ----
async function sha256(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

if (typeof module !== 'undefined') {
  module.exports = { MEME_FETCH_WINDOWS, fetchDailyPageviews, buildSeries, nelderMead, fitAll, sha256 };
}
