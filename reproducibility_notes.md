# Reproducibility Notes

## Random seeds

All scripts use `random_seed = 42` throughout. This includes:
- Train/test split (`train_test_split` with `random_state=42`)
- Calibration hold-out split (same seed)
- Random Forest (`random_state=42`)
- CatBoost (`random_seed=42`)
- Bootstrap resampling (`np.random.default_rng(42)`)

Figure 2's bootstrap distribution uses the same seed in `figure_generation.py`.

## Expected outputs

If you run the analysis on the IBM HR dataset with these seeds, you should get:

| Metric | Expected value |
|---|---|
| CatBoost AUC | ~0.818 |
| RF AUC | ~0.802 |
| LR AUC | ~0.777 |
| CatBoost ECE (pre-cal) | ~0.053 |
| RF ECE (pre-cal) | ~0.065 |
| LR ECE (pre-cal) | ~0.041 |
| CatBoost bootstrap 95% CI | ~[0.748, 0.888] |
| Gender DPD | ~0.015 |
| Gender EOD | ~0.121 |
| Age EOD | ~0.266 |

Minor floating-point variation across different OS/hardware is normal and won't change conclusions.

## Package versions tested

```
Python 3.10
scikit-learn 1.5.2
catboost 1.2.7
numpy 1.26.4
pandas 2.2.2
matplotlib 3.9.0
```

Newer versions should also work.

## CatBoost note

CatBoost installation can sometimes be slow or fail on some platforms. If `pip install catboost` doesn't work, try `pip install catboost --no-cache-dir`. If CatBoost is unavailable, the script will run LR and RF only and still produce valid results and figures.
