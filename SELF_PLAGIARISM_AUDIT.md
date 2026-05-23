# Self-Plagiarism Audit

## Scope

This audit checks for textual or structural self-plagiarism between the NHSJS
manuscript and the four empirically overlapping prior papers by the same author:

- **A** — Discover AI manuscript (governance-aware HR-AI evaluation)
- **B** — AAI paper (evaluation discipline, metric bounding)
- **C** — IEEE BigData manuscript (eight-stage correction pipeline)
- **D** — JEI manuscript (GADRS, calibration zones, SSI)

Papers on governance/institutional theory (NeurIPS, AAAI, Stanford, Columbia)
share zero empirical content and are not included here.

---

## Text-Level Check

### Abstract

| Paper | NHSJS Abstract overlap |
|---|---|
| A | None. A's abstract mentions "nine-stage framework," "governance-aware," "proxy audit," "SHAP stability" — all absent in NHSJS |
| B | None. B frames around "metric bounding" and "evaluation discipline" terminology not present in NHSJS |
| C | None. C mentions "metric scope violations," "eight-stage correction" — absent |
| D | None. D mentions "GADRS," "SSI," "zone-level calibration," "AURC" — all absent |

**Verdict: No abstract text overlap.**

### Introduction

The NHSJS introduction is written from scratch with a student investigative
framing ("I kept running into a question I couldn't shake"). None of the four
prior papers open with this framing or use similar phrasing. All four open
with academic problem statements about evaluation reliability, deployment
contexts, or governance gaps.

**Verdict: No introduction text overlap.**

### Background / Related Work

Prior papers cite Guo et al. (2017), Hardt et al. (2016), Niculescu-Mizil &
Caruana (2005), and Breiman (2001) — the NHSJS paper also cites these because
they are the primary sources for calibration, fairness, and random forests.
Citation of shared primary literature is not self-plagiarism. The prose
explanations of these concepts are rewritten from scratch for a high school
audience with new analogies (weather forecast, cats vs. dogs).

**Verdict: Shared citations only, no prose overlap.**

### Methods Section

All four papers describe the IBM HR dataset, CatBoost, and stratified
train/test splits. The NHSJS methods section uses simpler language, fewer
details, and different emphasis (no leakage-aware preprocessing, no proxy
audit, no nine-stage pipeline structure). The sentences and structure are
newly written.

Closest comparison: Paper C's methods section describes "leakage-aware
preprocessing, CatBoost gradient boosting, stratified 5-fold cross-validation."
The NHSJS paper describes "80/20 stratified split, three classifiers, no
hyperparameter tuning." These are different enough to not constitute overlap.

**Verdict: Structural parallelism from shared methodology; no prose reuse.**

### Results

All papers report AUC, ECE, and fairness metrics. Numbers are shared because
they come from the same dataset and classifiers. Reporting the same empirical
results across papers is replication, not self-plagiarism — as long as the
framing and interpretation are different. The NHSJS results are interpreted
through a "what is the AUC hiding?" investigative lens, distinct from
governance readiness scores (A), metric bounds (B), correction stages (C),
or governance composite scores (D).

**Verdict: Shared empirical results, distinct framing and interpretation.**

### Discussion

None of the four prior papers include a "What I'd Do Differently" discussion
subsection. None use the "cats versus dogs" framing. The NHSJS discussion
focuses on dataset size as the moderating variable — a point that appears
briefly in B but is not a primary argument there.

**Verdict: No prose overlap in discussion.**

---

## Structural Self-Plagiarism Check

| Structural Element | Prior papers | NHSJS |
|---|---|---|
| Number of sections | 7–10 | 6 + intro + conclusion |
| Framework figure | Yes (A, C, D) | No |
| Multi-panel dashboard figure | Yes (A, C) | No |
| Composite governance score | Yes (A, D) | No |
| Proxy audit table | Yes (A, B, C) | No |
| Zone-level analysis | Yes (D) | No |
| "What I'd do differently" | No | Yes |
| Weather forecast analogy | No | Yes |
| Student-voice first person | No | Yes |

**Verdict: Structurally distinct. No table, section, or argument architecture
is replicated from prior papers.**

---

## Risk Assessment

### High-risk items requiring disclosure

1. **Same dataset.** This is unavoidable and standard practice in ML research.
   The paper states this explicitly and acknowledges prior work using the same
   benchmark. This is not self-plagiarism.

2. **Same numerical results.** CatBoost AUC 0.818, ECE 0.053, EOD 0.266 appear
   in prior papers. These are verified experimental results, not invented
   numbers. Reporting consistent results is a virtue, not a violation.

### Recommended disclosure language (already in manuscript)

The manuscript does not claim novelty for the empirical findings themselves.
The contribution claim is educational/investigative framing, not new algorithms
or metrics. The paper's code availability statement and dataset reference are
transparent about the shared empirical base.

---

## Overall Self-Plagiarism Risk: LOW

No prose passages, tables, figures, or argument structures are directly
reused from prior papers. Shared numerical results and shared literature
citations are acknowledged and expected in replicated experimental work.
