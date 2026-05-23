# Environment Setup

Everything you need to run this analysis on a fresh machine.

## Requirements

- Python 3.9 or later (3.10 recommended)
- pip

## Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` pins the versions used in the paper:
```
scikit-learn==1.5.2
catboost==1.2.7
numpy==1.26.4
pandas==2.2.2
matplotlib==3.9.0
```

## Get the dataset

The IBM HR Analytics Employee Attrition dataset is free on Kaggle:

1. Go to: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
2. Download `WA_Fn-UseC_-HR-Employee-Attrition.csv`
3. Rename it to `ibm_hr_attrition.csv` and put it in the `data/` folder

## Run the analysis

```bash
# Step 1: main pipeline (AUC, ECE, bootstrap, fairness) -- writes results.json
python3 calibration_analysis.py

# Step 2: generate figures -- writes figures/*.svg and figures/*.png
python3 figure_generation.py

# Optional: standalone fairness check
python3 fairness_analysis.py

# Optional: standalone bootstrap check
python3 bootstrap_analysis.py
```

## Expected outputs

After running `calibration_analysis.py`, you should see `results.json` in
the project root. Key values to check:
- `auc.logistic_regression`: ~0.798
- `auc.random_forest`: ~0.759
- `auc.catboost`: ~0.762
- `fairness.age.eod`: ~0.258

After running `figure_generation.py`, check `figures/` for:
- `fig1_reliability_diagram.svg`
- `fig2_bootstrap_distribution.svg`
- `fig3_fairness_comparison.svg`

## Tested environments

| Python | scikit-learn | CatBoost | OS     | Status |
|--------|-------------|----------|--------|--------|
| 3.10   | 1.5.2       | 1.2.7    | macOS  | ✓      |
| 3.11   | 1.8.0       | 1.2.10   | macOS  | ✓      |

## Troubleshooting

**"No module named catboost"** — run `pip install catboost==1.2.7`

**CSV separator error** — the script handles both comma and semicolon
separators automatically.

**"Only one class present"** in bootstrap — this is expected for a small
number of resamples; the script skips those and continues.
