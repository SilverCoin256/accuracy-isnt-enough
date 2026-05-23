"""
calibration_analysis.py
-----------------------
Runs the full analysis pipeline for the NHSJS manuscript:
  - Trains Logistic Regression, Random Forest, CatBoost
  - Computes AUC, ECE (before/after isotonic calibration)
  - Bootstrap CI on AUC (1000 resamples)
  - DPD and EOD for gender and age groups
  - Writes results.json for figure_generation.py

Requires: ibm_hr_attrition.csv in data/
See data/README.md for download instructions.
"""

import json
import warnings
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

try:
    from catboost import CatBoostClassifier
    HAS_CATBOOST = True
except ImportError:
    HAS_CATBOOST = False
    print("CatBoost not installed -- skipping CB model")

RANDOM_SEED = 42
DATA_PATH   = "data/ibm_hr_attrition.csv"


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def ece(y_true, y_prob, n_bins=10):
    """Expected Calibration Error with equal-width bins."""
    bins = np.linspace(0, 1, n_bins + 1)
    total_ece = 0.0
    bin_data  = []
    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        mask = (y_prob >= lo) & (y_prob < hi)
        if mask.sum() == 0:
            bin_data.append({"mean_conf": (lo + hi) / 2, "frac_pos": 0.0, "n": 0})
            continue
        mc = y_prob[mask].mean()
        fp = y_true[mask].mean()
        bin_data.append({"mean_conf": float(mc), "frac_pos": float(fp), "n": int(mask.sum())})
        total_ece += (mask.sum() / len(y_true)) * abs(mc - fp)
    return float(total_ece), bin_data


def dpd(y_pred, group):
    """Demographic Parity Difference between two binary group values."""
    vals = np.unique(group)
    rates = [y_pred[group == v].mean() for v in vals]
    return float(abs(rates[0] - rates[1]))


def eod(y_true, y_pred, group):
    """
    Equalized Odds Difference: max of |TPR_0 - TPR_1| and |FPR_0 - FPR_1|.
    """
    vals = np.unique(group)
    tprs, fprs = [], []
    for v in vals:
        mask = group == v
        yt, yp = y_true[mask], y_pred[mask]
        pos = yt == 1
        neg = yt == 0
        tpr = yp[pos].mean() if pos.sum() > 0 else 0.0
        fpr = yp[neg].mean() if neg.sum() > 0 else 0.0
        tprs.append(tpr)
        fprs.append(fpr)
    return float(max(abs(tprs[0] - tprs[1]), abs(fprs[0] - fprs[1])))


def bootstrap_auc(y_true, y_prob, n=1000, seed=42):
    rng = np.random.default_rng(seed)
    scores = []
    for _ in range(n):
        idx = rng.integers(0, len(y_true), size=len(y_true))
        try:
            s = roc_auc_score(y_true[idx], y_prob[idx])
        except ValueError:
            continue
        scores.append(s)
    scores = np.array(scores)
    return {
        "samples": scores.tolist(),
        "ci_lo": float(np.percentile(scores, 2.5)),
        "ci_hi": float(np.percentile(scores, 97.5)),
    }


# ------------------------------------------------------------------
# Load and preprocess
# ------------------------------------------------------------------

def load_data(path):
    df = pd.read_csv(path, sep=None, engine="python")
    drop_cols = ["EmployeeNumber", "EmployeeCount", "StandardHours", "Over18"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    df["Attrition"] = (df["Attrition"] == "Yes").astype(int)
    df["Gender"]    = (df["Gender"] == "Male").astype(int)
    df["OverTime"]  = (df["OverTime"] == "Yes").astype(int)

    cat_cols = df.select_dtypes("object").columns.tolist()
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    y = df.pop("Attrition").values
    X = df.copy()
    return X, y, df


def main():
    print(f"Loading data from {DATA_PATH}...")
    try:
        X, y, df_raw = load_data(DATA_PATH)
    except FileNotFoundError:
        print(f"ERROR: {DATA_PATH} not found. See data/README.md for download instructions.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    # Scale for LR
    scaler = StandardScaler()
    Xtr_sc = scaler.fit_transform(X_train)
    Xte_sc = scaler.transform(X_test)

    # Group arrays for fairness
    gender_test = X_test["Gender"].values if "Gender" in X_test else None
    age_test    = (X_test["Age"].values < 40).astype(int) if "Age" in X_test else None

    # Calibration hold-out from training set
    Xtr2, Xcal, ytr2, ycal = train_test_split(
        X_train, y_train, test_size=0.2, random_state=RANDOM_SEED, stratify=y_train
    )
    Xtr2_sc = scaler.transform(Xtr2)
    Xcal_sc = scaler.transform(Xcal)

    results = {"auc": {}, "calibration": {}, "bootstrap": {}, "fairness": {}}

    # ------------------------------------------------------------------
    # Models
    # ------------------------------------------------------------------
    models = {}

    # Logistic Regression
    lr = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
    lr.fit(Xtr2_sc, ytr2)
    models["lr"] = ("LR", lr, Xte_sc, Xtr2_sc, Xcal_sc)

    # Random Forest
    rf = RandomForestClassifier(n_estimators=300, random_state=RANDOM_SEED)
    rf.fit(Xtr2, ytr2)
    models["rf"] = ("RF", rf, X_test, Xtr2, Xcal)

    # CatBoost
    if HAS_CATBOOST:
        cb = CatBoostClassifier(
            iterations=300, depth=6, learning_rate=0.05,
            random_seed=RANDOM_SEED, verbose=0
        )
        cb.fit(Xtr2, ytr2)
        models["catboost"] = ("CatBoost", cb, X_test, Xtr2, Xcal)

    # ------------------------------------------------------------------
    # Evaluate each model
    # ------------------------------------------------------------------
    for key, (name, clf, Xte, Xtr_fit, Xcal_fit) in models.items():
        print(f"\n--- {name} ---")

        prob_te = clf.predict_proba(Xte)[:, 1]
        auc_val = roc_auc_score(y_test, prob_te)
        print(f"  AUC: {auc_val:.4f}")
        results["auc"][key] = float(auc_val)

        # ECE before calibration
        ece_pre, bins_pre = ece(y_test, prob_te)
        print(f"  ECE (pre):  {ece_pre:.4f}")

        # Post-hoc calibration via isotonic regression on cal set
        prob_cal_fit = clf.predict_proba(Xcal_fit)[:, 1]
        ir = IsotonicRegression(out_of_bounds="clip")
        ir.fit(prob_cal_fit, ycal)
        prob_cal = ir.predict(prob_te)

        ece_post, bins_post = ece(y_test, prob_cal)
        print(f"  ECE (post): {ece_post:.4f}")

        results["calibration"][key] = {
            "pre":  {"ece": ece_pre,  "bins": bins_pre},
            "post": {"ece": ece_post, "bins": bins_post},
        }

        # Bootstrap CI
        bs = bootstrap_auc(y_test, prob_te)
        print(f"  95% CI: [{bs['ci_lo']:.3f}, {bs['ci_hi']:.3f}]")
        results["bootstrap"][key] = bs

        # Fairness (CatBoost only for main table; compute for all)
        y_pred_bin = (prob_te >= 0.5).astype(int)
        if gender_test is not None:
            g_dpd = dpd(y_pred_bin, gender_test)
            g_eod = eod(y_test, y_pred_bin, gender_test)
            print(f"  Gender DPD: {g_dpd:.4f}  EOD: {g_eod:.4f}")
        else:
            g_dpd, g_eod = None, None

        if age_test is not None:
            a_dpd = dpd(y_pred_bin, age_test)
            a_eod = eod(y_test, y_pred_bin, age_test)
            print(f"  Age    DPD: {a_dpd:.4f}  EOD: {a_eod:.4f}")
        else:
            a_dpd, a_eod = None, None

        results["fairness"][key] = {
            "gender": {"dpd": g_dpd, "eod": g_eod},
            "age":    {"dpd": a_dpd, "eod": a_eod},
        }

    # Copy top-level fairness from catboost for figure script
    cb_key = "catboost" if HAS_CATBOOST else "rf"
    results["fairness"]["gender"] = results["fairness"][cb_key]["gender"]
    results["fairness"]["age"]    = results["fairness"][cb_key]["age"]

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results.json")
    print("Run  python figure_generation.py  to produce the figures.")


if __name__ == "__main__":
    main()
