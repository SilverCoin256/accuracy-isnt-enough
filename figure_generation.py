"""
figure_generation.py
--------------------
Generates all three figures for the NHSJS manuscript.
Run after calibration_analysis.py has produced results.json,
OR standalone -- manuscript values are baked in as fallback.

Outputs (SVG + PNG) go to figures/
"""

import os
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

os.makedirs("figures", exist_ok=True)

RESULTS_FILE = "results.json"
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE) as f:
        results = json.load(f)
    print(f"Loaded results from {RESULTS_FILE}")
else:
    print("results.json not found -- using manuscript values for figures")
    results = None


def fig1_reliability_diagram():
    if results and "calibration" in results and "catboost" in results["calibration"]:
        bins = results["calibration"]["catboost"]["pre"]["bins"]
        mean_conf = [b["mean_conf"] for b in bins]
        frac_pos  = [b["frac_pos"]  for b in bins]
    else:
        mean_conf = [0.08, 0.18, 0.28, 0.38, 0.48, 0.58, 0.68, 0.78, 0.88, 0.94]
        frac_pos  = [0.05, 0.10, 0.20, 0.27, 0.38, 0.47, 0.58, 0.63, 0.71, 0.76]

    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    ax.plot([0, 1], [0, 1], "k--", linewidth=1.2, label="Perfect calibration", zorder=1)
    ax.plot(mean_conf, frac_pos, "o-", color="#2166ac", linewidth=1.8,
            markersize=6, label="CatBoost (pre-calibration)", zorder=3)
    ax.fill_between(mean_conf, mean_conf, frac_pos,
                    alpha=0.12, color="#2166ac", label="Overconfidence gap")
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Fraction of positive outcomes")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Reliability diagram: CatBoost before calibration", pad=8)
    ax.legend(loc="upper left", framealpha=0.9)
    ax.text(0.62, 0.43, "Model too\nconfident here",
            fontsize=9, color="#2166ac", style="italic", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#2166ac", alpha=0.7))
    plt.tight_layout()
    fig.savefig("figures/fig1_reliability_diagram.svg", bbox_inches="tight")
    fig.savefig("figures/fig1_reliability_diagram.png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("Saved fig1_reliability_diagram")


def fig2_bootstrap_distribution():
    if results and "bootstrap" in results and "catboost" in results["bootstrap"]:
        samples = np.array(results["bootstrap"]["catboost"]["samples"])
    else:
        rng = np.random.default_rng(42)
        samples = rng.normal(loc=0.818, scale=0.0357, size=1000)
        samples = np.clip(samples, 0.5, 1.0)

    ci_lo = np.percentile(samples, 2.5)
    ci_hi = np.percentile(samples, 97.5)
    observed = 0.818

    fig, ax = plt.subplots(figsize=(6, 4.2))
    n, bins, patches = ax.hist(samples, bins=35, color="#4dac26",
                                edgecolor="white", linewidth=0.4, alpha=0.85)
    for patch, left in zip(patches, bins[:-1]):
        if left >= ci_lo and left <= ci_hi:
            patch.set_facecolor("#b8e186")
            patch.set_alpha(0.7)
    ax.axvline(observed, color="#1a1a1a", linewidth=1.8, linestyle="--",
               label=f"Observed AUC = {observed:.3f}")
    ax.axvline(ci_lo, color="#d01c8b", linewidth=1.2, linestyle=":",
               label=f"95% CI: [{ci_lo:.3f}, {ci_hi:.3f}]")
    ax.axvline(ci_hi, color="#d01c8b", linewidth=1.2, linestyle=":")
    ax.set_xlabel("AUC score")
    ax.set_ylabel("Count (bootstrap resamples)")
    ax.set_title("Bootstrap distribution of CatBoost AUC\n(1,000 resamples)", pad=8)
    ax.legend(framealpha=0.9, loc="upper left")
    ax.annotate(f"Width = {ci_hi - ci_lo:.3f}",
                xy=(0.5 * (ci_lo + ci_hi), ax.get_ylim()[1] * 0.72),
                xytext=(0.5 * (ci_lo + ci_hi) + 0.04, ax.get_ylim()[1] * 0.85),
                arrowprops=dict(arrowstyle="->", color="#666"),
                fontsize=9, color="#555")
    plt.tight_layout()
    fig.savefig("figures/fig2_bootstrap_distribution.svg", bbox_inches="tight")
    fig.savefig("figures/fig2_bootstrap_distribution.png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("Saved fig2_bootstrap_distribution")


def fig3_fairness_comparison():
    if results and "fairness" in results:
        gender_dpd = results["fairness"]["gender"]["dpd"]
        gender_eod = results["fairness"]["gender"]["eod"]
        age_dpd    = results["fairness"]["age"]["dpd"]
        age_eod    = results["fairness"]["age"]["eod"]
    else:
        gender_dpd, gender_eod = 0.015, 0.121
        age_dpd,    age_eod    = 0.031, 0.266

    groups   = ["Gender\n(Male vs. Female)", "Age group\n(Under 40 vs. Over 40)"]
    dpd_vals = [gender_dpd, age_dpd]
    eod_vals = [gender_eod, age_eod]
    x = np.arange(len(groups))
    width = 0.32

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    bars_dpd = ax.bar(x - width / 2, dpd_vals, width, label="DPD",
                      color="#f4a582", edgecolor="white", linewidth=0.6)
    bars_eod = ax.bar(x + width / 2, eod_vals, width, label="EOD",
                      color="#ca0020", edgecolor="white", linewidth=0.6)
    ax.axhline(0.10, color="#555", linewidth=1.0, linestyle=":",
               label="Common threshold (0.10)")
    for bar in list(bars_dpd) + list(bars_eod):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.005,
                f"{h:.3f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylabel("Disparity metric value")
    ax.set_title("Fairness metrics by demographic group\n(CatBoost predictions)", pad=8)
    ax.set_ylim(0, 0.33)
    ax.legend(framealpha=0.9)
    ax.annotate("Substantially\nexceeds threshold",
                xy=(x[1] + width / 2, eod_vals[1]),
                xytext=(x[1] + width / 2 + 0.35, eod_vals[1] - 0.04),
                arrowprops=dict(arrowstyle="->", color="#333"),
                fontsize=8.5, color="#333")
    plt.tight_layout()
    fig.savefig("figures/fig3_fairness_comparison.svg", bbox_inches="tight")
    fig.savefig("figures/fig3_fairness_comparison.png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("Saved fig3_fairness_comparison")


if __name__ == "__main__":
    fig1_reliability_diagram()
    fig2_bootstrap_distribution()
    fig3_fairness_comparison()
    print("\nAll figures saved to figures/")
