# NHSJS Submission Guide

This guide walks through how to submit this paper to the National High School Journal of Science (NHSJS).

## Step 1: Compile the PDF

You need LaTeX installed. If you don't have it:
- Download TeX Live (Windows/Linux) from https://tug.org/texlive/
- Or MacTeX (macOS) from https://tug.org/mactex/

Then compile:
```
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

This produces `manuscript.pdf`.

If you don't want to install LaTeX, you can also use Overleaf (free online): https://overleaf.com. Upload `manuscript.tex` and compile there.

## Step 2: Generate the figures

Make sure you've run the analysis first (or skip this if you're using the pre-generated figures):
```
python calibration_analysis.py
python figure_generation.py
```

Then copy `figures/fig1_reliability_diagram.png`, `fig2_bootstrap_distribution.png`, and `fig3_fairness_comparison.png` into the same directory as `manuscript.tex` before compiling.

## Step 3: Submit to NHSJS

1. Go to https://nhsjs.com/submissions
2. Create an account or log in
3. Select "Research Article" as the submission type
4. Upload `manuscript.pdf`
5. Fill in the abstract, keywords, and author information
6. Upload figures as separate files if requested

## Formatting checklist

- [ ] PDF compiled successfully, no missing figures
- [ ] Author name and email on title page
- [ ] Abstract under 250 words
- [ ] All figures referenced in text with captions
- [ ] References formatted consistently
- [ ] Word count within journal limits (typically 3,000–8,000 words)

## What NHSJS looks for

NHSJS reviews for:
- Scientific rigor (methods clearly described, results honest)
- Originality (this paper is new work, not reproduced from elsewhere)
- Clarity (readable by advanced high school students)
- Reproducibility (code and data publicly available)

This paper addresses all four. The dataset is publicly available, the code is on GitHub, and the methods are standard and well-documented.
