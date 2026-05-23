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

```
python3 calibration_analysis.py
python3 figure_generation.py
```

Then make sure `figures/fig1_reliability_diagram.png`, `fig2_bootstrap_distribution.png`, and `fig3_fairness_comparison.png` are in the same directory as `manuscript.tex` before compiling.

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
- [ ] Word count within journal limits (typically 3,000-8,000 words)
