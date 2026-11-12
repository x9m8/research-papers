"""
Independent sanity check of the in-browser (JavaScript, multi-start Nelder-Mead) curve fit,
using scipy.optimize.curve_fit on the one full raw daily series kept in this package
(pkg/data/raw/grumpy_cat_daily_pageviews.json). This does NOT re-derive all 26 memes (the other
25 memes' raw daily series were not transferred out of the browser — see README.md and
lit/brief.md for why), but it independently confirms that the browser-side fitting approach
produces sensible, non-degenerate parameter estimates on real data, using a completely different
optimizer (Levenberg-Marquardt via scipy) and a different language/runtime.

Run: python3 refit_check.py
Writes: pkg/results/grumpy_cat_refit.json
"""
import json
import hashlib
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "grumpy_cat_daily_pageviews.json"
OUT = ROOT / "results" / "grumpy_cat_refit.json"

EXPECTED_SHA256 = "e687cc20679ad7d3b67dd8b3767911a45ca67235bda22b1f37e4e3c9bf59eaac"


def exponential(t, A, k, c):
    return A * np.exp(-k * t) + c


def powerlaw(t, A, alpha, c):
    return A * np.power(t + 1, -alpha) + c


def stretched(t, A, tau, beta, c):
    return A * np.exp(-np.power(t / tau, beta)) + c


def r2_score(y, yhat):
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot


def aic(k, n, rss):
    return n * np.log(max(rss, 1e-9) / n) + 2 * k


def main():
    raw_bytes = RAW.read_bytes()
    actual_hash = hashlib.sha256(raw_bytes).hexdigest()
    assert actual_hash == EXPECTED_SHA256, (
        f"raw data provenance check FAILED: {actual_hash} != {EXPECTED_SHA256}"
    )

    obj = json.loads(raw_bytes)
    series = obj["series"]
    baseline = obj["baseline"]

    post = [(d, v) for d, v in series if d >= 1]
    t = np.array([p[0] for p in post], dtype=float)
    v = np.array([p[1] for p in post], dtype=float)

    results = {}

    # Exponential
    p0 = [v[0] - baseline, 1 / 30, baseline]
    popt, _ = curve_fit(exponential, t, v, p0=p0, bounds=([0, 1e-6, 0], [np.inf, 10, np.inf]), maxfev=20000)
    yhat = exponential(t, *popt)
    rss = float(np.sum((v - yhat) ** 2))
    results["exponential"] = {
        "A": float(popt[0]), "k": float(popt[1]), "c": float(popt[2]),
        "r2": float(r2_score(v, yhat)), "aic": float(aic(3, len(v), rss)),
        "halflife_days": float(np.log(2) / popt[1]),
    }

    # Power-law
    p0 = [v[0] - baseline, 1.0, baseline]
    popt, _ = curve_fit(powerlaw, t, v, p0=p0, bounds=([0, 1e-3, 0], [np.inf, 10, np.inf]), maxfev=20000)
    yhat = powerlaw(t, *popt)
    rss = float(np.sum((v - yhat) ** 2))
    results["powerlaw"] = {
        "A": float(popt[0]), "alpha": float(popt[1]), "c": float(popt[2]),
        "r2": float(r2_score(v, yhat)), "aic": float(aic(3, len(v), rss)),
    }

    # Stretched exponential
    p0 = [v[0] - baseline, 5.0, 0.5, baseline]
    popt, _ = curve_fit(
        stretched, t, v, p0=p0,
        bounds=([0, 1e-3, 0.02, 0], [np.inf, 1000, 4, np.inf]), maxfev=40000
    )
    yhat = stretched(t, *popt)
    rss = float(np.sum((v - yhat) ** 2))
    results["stretched"] = {
        "A": float(popt[0]), "tau": float(popt[1]), "beta": float(popt[2]), "c": float(popt[3]),
        "r2": float(r2_score(v, yhat)), "aic": float(aic(4, len(v), rss)),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    print(f"wrote {OUT}")
    for model, r in results.items():
        print(f"  {model}: R2={r['r2']:.4f}  AIC={r['aic']:.1f}")


if __name__ == "__main__":
    main()
