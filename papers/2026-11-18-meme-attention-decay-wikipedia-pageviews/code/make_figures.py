"""
Figures for the manuscript. All data read from pkg/data/raw/ and pkg/results/ (hash-checked,
provenance-tracked — see analyze.py / refit_check.py). Run after analyze.py and refit_check.py.

Run: python3 make_figures.py
Writes: pkg/figures/fig1_grumpy_cat_decay.png (+.pdf), pkg/figures/fig2_model_comparison.png (+.pdf),
        pkg/figures/graphical_abstract.png
"""
import json
import hashlib
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "exponential": "#4C72B0",
    "power-law": "#DD8452",
    "stretched exponential": "#55A868",
    "data": "#444444",
}

plt.rcParams.update({
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
})


def exponential(t, A, k, c):
    return A * np.exp(-k * t) + c


def powerlaw(t, A, alpha, c):
    return A * np.power(t + 1, -alpha) + c


def stretched(t, A, tau, beta, c):
    return A * np.exp(-np.power(t / tau, beta)) + c


def fig1_grumpy_cat():
    raw_path = ROOT / "data" / "raw" / "grumpy_cat_daily_pageviews.json"
    expected = "e687cc20679ad7d3b67dd8b3767911a45ca67235bda22b1f37e4e3c9bf59eaac"
    b = raw_path.read_bytes()
    assert hashlib.sha256(b).hexdigest() == expected
    obj = json.loads(b)
    refit = json.loads((ROOT / "results" / "grumpy_cat_refit.json").read_text())

    series = obj["series"]
    days = np.array([d for d, v in series])
    views = np.array([v for d, v in series])

    tt = np.linspace(1, 365, 500)
    exp_p = refit["exponential"]
    pl_p = refit["powerlaw"]
    se_p = refit["stretched"]

    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.scatter(days, views, s=6, color=PALETTE["data"], alpha=0.55, label="Daily pageviews (English Wikipedia)")
    ax.plot(tt, exponential(tt, exp_p["A"], exp_p["k"], exp_p["c"]), color=PALETTE["exponential"], lw=1.8,
            label=f"Exponential (R²={exp_p['r2']:.3f})")
    ax.plot(tt, powerlaw(tt, pl_p["A"], pl_p["alpha"], pl_p["c"]), color=PALETTE["power-law"], lw=1.8,
            label=f"Power-law (R²={pl_p['r2']:.3f})")
    ax.plot(tt, stretched(tt, se_p["A"], se_p["tau"], se_p["beta"], se_p["c"]), color=PALETTE["stretched exponential"], lw=1.8,
            label=f"Stretched exponential (R²={se_p['r2']:.3f})")
    ax.axvline(0, color="#999999", lw=1, ls=":")
    ax.set_yscale("log")
    ax.set_xlim(-60, 365)
    ax.set_xlabel("Days since peak (14 May 2019, the day Grumpy Cat died)")
    ax.set_ylabel("English Wikipedia daily pageviews (log scale)")
    ax.set_title("Grumpy Cat: attention decay after a peak, three candidate models")
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig1_grumpy_cat_decay.png", dpi=300)
    fig.savefig(FIG_DIR / "fig1_grumpy_cat_decay.pdf")
    plt.close(fig)
    print("wrote fig1_grumpy_cat_decay.{png,pdf}")


def fig2_model_comparison():
    import csv
    rows = list(csv.DictReader(open(ROOT / "results" / "meme_table.csv")))
    rows = sorted(rows, key=lambda r: -max(float(r["exp_r2"]), float(r["pl_r2"]), float(r["se_r2"])))

    titles = [r["title"].replace("_", " ").replace("(meme)", "").strip() for r in rows]
    best_r2 = [max(float(r["exp_r2"]), float(r["pl_r2"]), float(r["se_r2"])) for r in rows]
    best_model = [r["best_model"] for r in rows]
    colors = [PALETTE[m] for m in best_model]

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    y = np.arange(len(rows))
    ax.barh(y, best_r2, color=colors, height=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(titles, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlabel("Best-fitting model's R² (post-peak decay, day +1 to +365)")
    ax.set_title("Decay-curve fit quality across 26 memes")
    ax.set_xlim(0, 1)
    from matplotlib.patches import Patch
    handles = [Patch(color=PALETTE[m], label=f"{m} (AIC-best)") for m in
               ["exponential", "power-law", "stretched exponential"]]
    ax.legend(handles=handles, fontsize=8, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig2_model_comparison.png", dpi=300)
    fig.savefig(FIG_DIR / "fig2_model_comparison.pdf")
    plt.close(fig)
    print("wrote fig2_model_comparison.{png,pdf}")


def graphical_abstract():
    raw_path = ROOT / "data" / "raw" / "grumpy_cat_daily_pageviews.json"
    obj = json.loads(raw_path.read_bytes())
    series = obj["series"]
    days = np.array([d for d, v in series])
    views = np.array([v for d, v in series])
    refit = json.loads((ROOT / "results" / "grumpy_cat_refit.json").read_text())
    se_p = refit["stretched"]
    tt = np.linspace(1, 365, 300)

    fig = plt.figure(figsize=(9, 4.2), dpi=100)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1])

    ax1 = fig.add_subplot(gs[0])
    ax1.scatter(days, views, s=5, color="#444444", alpha=0.5)
    ax1.plot(tt, stretched(tt, se_p["A"], se_p["tau"], se_p["beta"], se_p["c"]), color=PALETTE["stretched exponential"], lw=2)
    ax1.axvline(0, color="#999999", lw=1, ls=":")
    ax1.set_yscale("log")
    ax1.set_xlabel("Days since peak", fontsize=9)
    ax1.set_ylabel("Pageviews (log)", fontsize=9)
    ax1.set_title("One meme's decay", fontsize=10)

    import csv
    rows = list(csv.DictReader(open(ROOT / "results" / "meme_table.csv")))
    wins = {"exponential": 0, "power-law": 0, "stretched exponential": 0}
    for r in rows:
        wins[r["best_model"]] += 1
    ax2 = fig.add_subplot(gs[1])
    labels = list(wins.keys())
    vals = [wins[k] for k in labels]
    colors = [PALETTE[k] for k in labels]
    ax2.bar(range(3), vals, color=colors, width=0.6)
    ax2.set_xticks(range(3))
    ax2.set_xticklabels(["Exponential", "Power-law", "Stretched\nexponential"], fontsize=8)
    ax2.set_ylabel("Memes best fit\n(of 26, by AIC)", fontsize=9)
    ax2.set_title("No single law dominates", fontsize=10)
    for i, v in enumerate(vals):
        ax2.text(i, v + 0.3, str(v), ha="center", fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.suptitle("How memes fade: comparing decay curves of Wikipedia attention", fontsize=11, y=0.98)
    fig.savefig(FIG_DIR / "graphical_abstract.png", dpi=100)
    plt.close(fig)
    print("wrote graphical_abstract.png")


if __name__ == "__main__":
    fig1_grumpy_cat()
    fig2_model_comparison()
    graphical_abstract()
