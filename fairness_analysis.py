"""
fairness_analysis.py
Standalone fairness metric computation for the NHSJS paper.
Computes DPD and EOD for gender and age groups.
Run after calibration_analysis.py has produced results.json,
or directly on the dataset to re-verify the fairness numbers.
"""

import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    print("CatBoost not installed -- skipping CatBoost fairness metrics")

RESULTS_FILE = "results.json"
DATA_PATH = "data/ibm_hr_attrition.csv"
RANDOM_SEED = 42


def load_data(path):
    # try comma first, then semicolon
    try:
        df = pd.read_csv(path)
        if df.shape[1] < 5:
            df = pd.read_csv(path, sep=";")
    except Exception:
        df = pd.read_csv(path, sep=";")
    return df


def compute_dpd(y_pred, group_mask):
    """Demographic Parity Difference: |P(y_hat=1|group=0) - P(y_hat=1|group=1)|"""
    rate_a = y_pred[group_mask == 0].mean()
    rate_b = y_pred[group_mask == 1].mean()
    return abs(rate_a - rate_b)


def compute_eod(y_true, y_pred, group_mask):
    """
    Equalized Odds Difference: max of |TPR_a - TPR_b| and |FPR_a - FPR_b|.
    Matches the definition used in the paper.
    """
    results = {}
    for group_val, label in [(0, "group_0"), (1, "group_1")]:
        mask = group_mask == group_val
        yt = y_true[mask]
        yp = y_pred[mask]
        tp = ((yt == 1) & (yp == 1)).sum()
        fn = ((yt == 1) & (yp == 0)).sum()
        fp = ((yt == 0) & (yp == 1)).sum()
        tn = ((yt == 0) & (yp == 0)).sum()
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        results[label] = {"tpr": tpr, "fpr": fpr}
    tpr_diff = abs(results["group_0"]["tpr"] - results["group_1"]["tpr"])
    fpr_diff = abs(results["group_0"]["fpr"] - results["group_1"]["fpr"])
    return max(tpr_diff, fpr_diff)


def run_fairness_analysis():
    print("Loading data...")
    df = load_data(DATA_PATH)

    # encode target
    df["Attrition_bin"] = (df["Attrition"] == "Yes").astype(int)

    # gender mask: Male=0, Female=1
    df["gender_mask"] = (df["Gender"] == "Female").astype(int)

    # age mask: Under40=0, Over40=1
    df["age_mask"] = (df["Age"] >= 40).astype(int)

    # drop non-numeric / target columns
    drop_cols = ["Attrition", "Attrition_bin", "gender_mask", "age_mask",
                 "EmployeeCount", "Over18", "StandardHours"]
    feature_cols = [c for c in df.columns if c not in drop_cols
                    and df[c].dtype != object]

    X = df[feature_cols].values
    y = df["Attrition_bin"].values
    gender_mask = df["gender_mask"].values
    age_mask = df["age_mask"].values

    X_train, X_test, y_train, y_test, gm_train, gm_test, am_train, am_test = (
        train_test_split(X, y, gender_mask, age_mask,
                         test_size=0.2, random_state=RANDOM_SEED,
                         stratify=y)
    )

    if not CATBOOST_AVAILABLE:
        print("Install catboost to get CatBoost fairness metrics.")
        return

    print("Training CatBoost...")
    cb = CatBoostClassifier(iterations=300, depth=6, learning_rate=0.05,
                             random_seed=RANDOM_SEED, verbose=0)
    cb.fit(X_train, y_train)

    y_pred = (cb.predict_proba(X_test)[:, 1] >= 0.5).astype(int)

    gender_dpd = compute_dpd(y_pred, gm_test)
    gender_eod = compute_eod(y_test, y_pred, gm_test)
    age_dpd    = compute_dpd(y_pred, am_test)
    age_eod    = compute_eod(y_test, y_pred, am_test)

    report = {
        "model": "CatBoost",
        "threshold": 0.5,
        "gender": {"dpd": round(gender_dpd, 4), "eod": round(gender_eod, 4)},
        "age":    {"dpd": round(age_dpd, 4),    "eod": round(age_eod, 4)},
    }

    print("\n=== Fairness Results (CatBoost) ===")
    print(f"  Gender DPD: {gender_dpd:.4f}   EOD: {gender_eod:.4f}")
    print(f"  Age    DPD: {age_dpd:.4f}   EOD: {age_eod:.4f}")

    with open("fairness_results.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nSaved to fairness_results.json")


if __name__ == "__main__":
    run_fairness_analysis()
