"""
Main analysis: loads pkg/data/raw/meme_fit_summary.json (26 memes x 3 fitted decay models,
computed in-browser against live Wikimedia pageview data — see pkg/code/fetch_pipeline.js and
lit/brief.md for full provenance) and produces the summary statistics and tables reported in the
manuscript. Also loads pkg/results/grumpy_cat_refit.json (independent scipy re-fit; see
refit_check.py) for cross-validation reporting.

Run: python3 analyze.py
Writes: pkg/results/summary_stats.json, pkg/results/meme_table.csv
"""
import json
import hashlib
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "data" / "raw" / "meme_fit_summary.json"
EXPECTED_SHA256 = "2eae316a2d79108a357e99686fe5d631a59692854fd161231c803d568ec945e8"

MODELS = ["exp", "pl", "se"]
MODEL_NAMES = {"exp": "exponential", "pl": "power-law", "se": "stretched exponential"}
MODEL_NPARAMS = {"exp": 3, "pl": 3, "se": 4}


def main():
    raw_bytes = SUMMARY_PATH.read_bytes()
    actual_hash = hashlib.sha256(raw_bytes).hexdigest()
    assert actual_hash == EXPECTED_SHA256, (
        f"data provenance check FAILED: {actual_hash} != {EXPECTED_SHA256}"
    )
    data = json.loads(raw_bytes)
    assert len(data) == 26, f"expected 26 memes, got {len(data)}"

    wins = {m: 0 for m in MODELS}
    r2_by_model = {m: [] for m in MODELS}
    rows = []
    for row in data:
        title = row["title"]
        if "error" in row:
            continue
        aics = {m: row[m]["aic"] for m in MODELS}
        best = min(aics, key=lambda m: aics[m])
        wins[best] += 1
        for m in MODELS:
            r2_by_model[m].append(row[m]["r2"])
        rows.append({
            "title": title,
            "peak_date": row["peakDate"],
            "peak_views": row["peakViews"],
            "baseline": row.get("baseline"),
            "n_pre": row["nPre"],
            "n_post": row["nPost"],
            "best_model": MODEL_NAMES[best],
            "exp_r2": row["exp"]["r2"], "exp_aic": row["exp"]["aic"], "exp_halflife_days": row["exp"].get("halflife"),
            "pl_r2": row["pl"]["r2"], "pl_aic": row["pl"]["aic"], "pl_alpha": row["pl"]["alpha"],
            "se_r2": row["se"]["r2"], "se_aic": row["se"]["aic"], "se_beta": row["se"]["beta"], "se_tau": row["se"]["tau"],
        })

    summary = {
        "n_memes": len(rows),
        "aic_wins": {MODEL_NAMES[m]: wins[m] for m in MODELS},
        "median_r2": {MODEL_NAMES[m]: stats.median(r2_by_model[m]) for m in MODELS},
        "mean_r2": {MODEL_NAMES[m]: stats.mean(r2_by_model[m]) for m in MODELS},
        "n_poor_fit_all_models_r2_below_0.1": sum(
            1 for r in rows if max(r["exp_r2"], r["pl_r2"], r["se_r2"]) < 0.1
        ),
        "n_good_fit_best_model_r2_above_0.9": sum(
            1 for r in rows if max(r["exp_r2"], r["pl_r2"], r["se_r2"]) > 0.9
        ),
    }

    refit_path = ROOT / "results" / "grumpy_cat_refit.json"
    if refit_path.exists():
        refit = json.loads(refit_path.read_text())
        browser_row = next(r for r in rows if r["title"] == "Grumpy_Cat")
        summary["grumpy_cat_cross_validation"] = {
            "browser_js_nelder_mead": {
                "exp_r2": browser_row["exp_r2"], "pl_r2": browser_row["pl_r2"], "se_r2": browser_row["se_r2"],
            },
            "python_scipy_curve_fit": {
                "exp_r2": refit["exponential"]["r2"],
                "pl_r2": refit["powerlaw"]["r2"],
                "se_r2": refit["stretched"]["r2"],
            },
        }

    out_json = ROOT / "results" / "summary_stats.json"
    out_json.write_text(json.dumps(summary, indent=2))
    print(f"wrote {out_json}")
    print(json.dumps(summary, indent=2))

    out_csv = ROOT / "results" / "meme_table.csv"
    cols = list(rows[0].keys())
    with open(out_csv, "w") as f:
        f.write(",".join(cols) + "\n")
        for r in sorted(rows, key=lambda r: -max(r["exp_r2"], r["pl_r2"], r["se_r2"])):
            f.write(",".join(str(r[c]) for c in cols) + "\n")
    print(f"wrote {out_csv}")


if __name__ == "__main__":
    main()
