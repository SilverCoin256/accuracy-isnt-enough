# dev log

keeping notes on what I tried as I built this project

---

## getting started -- data loading

got the IBM HR dataset from kaggle. first loading attempt broke immediately because
the CSV is semicolon-delimited not comma-delimited (took me an embarrassingly long
time to figure out). fixed by passing `sep=None, engine="python"` to pandas.

basic setup: 1470 records, 35 features, binary target (attrition). only 16% are
attrition=Yes so the dataset is imbalanced. decided not to resample since I wanted
to see calibration behavior on the natural class distribution.

split 80/20 with stratification. ended up with 294 test examples.

---

## first models -- LR and RF

logistic regression and random forest were straightforward. had to scale features
for LR (forgot this the first time and it didn't converge -- max_iter warning).

LR AUC came out higher than RF which surprised me a bit. usually RF does better
on tabular data in my experience from reading benchmarks.

---

## adding catboost

had to `pip install catboost` -- package is large, took a few minutes. used
default hyperparameters (iterations=300, depth=6, lr=0.05) as a starting point.
didn't tune anything since the goal was evaluation not optimization.

CatBoost AUC came out between LR and RF, which felt like a reasonable result.

---

## calibration -- debugging the sklearn API issue

first attempt used `CalibratedClassifierCV(cv='prefit')` which is how most
tutorials I found describe post-hoc calibration. threw an error:

```
InvalidParameterError: The 'cv' parameter of CalibratedClassifierCV must be
an int... Got 'prefit' instead.
```

looked it up -- this was a valid option in older sklearn but was removed at
some point. switched to using IsotonicRegression directly, which works and
is actually cleaner since I can see exactly what's happening.

needed a calibration holdout from the training set (used 20% of train for this).

the counterintuitive result: LR ECE got slightly WORSE after correction (0.047
to 0.058). RF and CatBoost both improved. my best guess is that the calibration
fitting set (~235 examples) was too small to reliably estimate a correction for LR
which was already pretty well calibrated. could also just be noise. not sure.

---

## bootstrap

conceptually this took me a while to get right. the key thing: you're resampling
the TEST SET with replacement, not generating new test data. each resample of 294
examples gives you a slightly different AUC. do this 1000 times and you get a
distribution of AUC values, and the 2.5th/97.5th percentiles give the 95% CI.

the intervals came out at ~0.16 wide for all three models. this was wider than I
expected. ran with 2000 resamples to double-check -- same result. it's just what
happens with 294 test examples.

---

## fairness metrics

gender EOD was small (0.026) which makes sense -- the dataset doesn't have a
strong gender signal apparently.

age EOD came out at 0.258 which seems large. I re-ran the calculation manually
on a small subset to make sure it wasn't a bug -- it's real. still not sure
if this reflects something in the dataset structure or just a consequence of how
the synthetic data was generated.

open question: does the age EOD change after calibration correction? CatBoost was
both the most miscalibrated model AND had the worst age EOD. might be related. 
didn't have time to check before submission.

---

## figures

tried using seaborn style sheets at first (`plt.style.use('seaborn-v0_8-whitegrid')`)
but everything looked too polished/corporate. went back to basic matplotlib with
minimal rcParams tweaks. also tried annotating with arrow annotations but they
looked awkward so replaced with plain text annotations.

figures are saved as both SVG and PNG. SVG for the paper, PNG as backup.

---

## writing the paper -- first draft

abstract took the longest. kept rewriting it because I kept starting with a
definition ("AUC measures rank discrimination...") and then realizing that's
boring and not what I actually want to say. ended up starting with the
observation about the habit instead.

the methods section was hard to write without it sounding like a recipe.
i probably rewrote the dataset paragraph 3-4 times.

---

## things that tripped me up mid-project

- forgot that isotonic regression needs the calibration set to be *separate*
  from training and test. my first version was accidentally fitting on part
  of the test set. had to redo the split logic

- the fairness metrics section took a while to understand conceptually.
  DPD is simpler (just compare positive rate), EOD is more subtle (it's
  comparing the full error structure, not just one number).

- latex compilation kept failing on the url in the references section.
  something to do with how hyperref handles long URLs inside the reference list.
  ended up just leaving them as plain text.

---

## things I want to follow up on eventually

- [ ] does the age EOD change after calibration correction?
- [ ] would hyperparameter tuning change the calibration picture significantly?
- [ ] what does zone-level calibration look like (is the overconfidence concentrated
      in the high-confidence region or spread out)?
- [ ] would results replicate on a real (non-synthetic) HR dataset?
