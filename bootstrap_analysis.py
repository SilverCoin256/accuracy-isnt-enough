"""
bootstrap_analysis.py
Standalone bootstrap confidence interval analysis for the NHSJS paper.
Re-runs 1000-resample bootstrap on each model's AUC on the test set.
Outputs bootstrap_results.json with intervals and sample distributions.
"""

import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder

try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False

DATA_PATH = "data/ibm_hr_attrition.csv"
RANDOM_SEED = 42
N_BOOTSTRAP = 1000


def load_data(path):
    try:
        df = pd.read_csv(path)
        if df.shape[1] < 5:
            df = pd.read_csv(path, sep=";")
    except Exception:
        df = pd.read_csv(path, sep=";")
    return df


def bootstrap_auc(y_true, y_score, n_resamples=1000, seed=42):
    """Return array of AUC from bootstrap resamples of (y_true, y_score)."""
    rng = np.random.default_rng(seed)
    aucs = []
    n = len(y_true)
    for _ in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        yt = y_true[idx]
        ys = y_score[idx]
        # skip if only one class in resample
        if len(np.unique(yt)) < 2:
            continue
        try:
            aucs.append(roc_auc_score(yt, ys))
        except Exception:
            continue
    return np.array(aucs)


def run_bootstrap_analysis():
    print("Loading data...")
    df = load_data(DATA_PATH)
    df["Attrition_bin"] = (df["Attrition"] == "Yes").astype(int)

    drop_cols = ["Attrition", "Attrition_bin", "EmployeeCount", "Over18",
                 "StandardHours"]
    # encode any remaining object columns
    for col in df.select_dtypes(include="object").columns:
        if col not in drop_cols:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    feature_cols = [c for c in df.columns if c not in drop_cols]
    X = df[feature_cols].values
    y = df["Attrition_bin"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000,
                                                   random_state=RANDOM_SEED),
        "random_forest":       RandomForestClassifier(n_estimators=100,
                                                      random_state=RANDOM_SEED),
    }
    if CATBOOST_AVAILABLE:
        models["catboost"] = CatBoostClassifier(iterations=300, depth=6,
                                                 learning_rate=0.05,
                                                 random_seed=RANDOM_SEED,
                                                 verbose=0)

    results = {}
    for name, model in models.items():
        print(f"Fitting {name}...")
        model.fit(X_train, y_train)
        y_score = model.predict_proba(X_test)[:, 1]
        observed_auc = roc_auc_score(y_test, y_score)

        print(f"  Running {N_BOOTSTRAP} bootstrap resamples...")
        boot_aucs = bootstrap_auc(y_test, y_score, n_resamples=N_BOOTSTRAP,
                                   seed=RANDOM_SEED)
        ci_lo = float(np.percentile(boot_aucs, 2.5))
        ci_hi = float(np.percentile(boot_aucs, 97.5))

        results[name] = {
            "observed_auc": round(observed_auc, 4),
            "ci_lower":     round(ci_lo, 4),
            "ci_upper":     round(ci_hi, 4),
            "ci_width":     round(ci_hi - ci_lo, 4),
            "n_valid_resamples": len(boot_aucs),
        }
        print(f"  AUC={observed_auc:.4f}  95% CI=[{ci_lo:.4f}, {ci_hi:.4f}]  "
              f"width={ci_hi - ci_lo:.4f}")

    with open("bootstrap_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to bootstrap_results.json")


if __name__ == "__main__":
    run_bootstrap_analysis()
