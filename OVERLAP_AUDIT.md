# Overlap Audit Report — NHSJS Paper vs. Prior Manuscripts

## Papers Reviewed

| # | Paper | Venue |
|---|---|---|
| A | discover_ai_manuscript | Discover Artificial Intelligence (Springer) |
| B | For review version by AAI | Applied Artificial Intelligence (T&F) |
| C | ieee_bigdata_manuscript | IEEE BigData 2026 |
| D | manuscript (JEI) | Journal of Economic Issues |
| E | neurIPS.pdf | NeurIPS 2025 |
| F | To Submit - neurIPS Workshop | NeurIPS Workshop |
| G | AAAI symposium | AAAI symposium |
| H | Stanford Intersect | Stanford undergraduate journal |
| I | Columbia junior scientist journal | Columbia JSJ |
| J | World Outlook Submission | World Outlook |

---

## Full Overlap Matrix

| Component | A | B | C | D | NHSJS |
|---|---|---|---|---|---|
| IBM HR dataset | ✓ | ✓ | ✓ | ✓ | ✓ |
| CatBoost | ✓ | ✓ | ✓ | – | ✓ |
| AUC as primary metric | ✓ | ✓ | ✓ | ✓ | ✓ (but critiqued) |
| Calibration / ECE | ✓ | – | ✓ | ✓ | ✓ (simpler, global only) |
| Bootstrap CI on AUC | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fairness DPD / EOD | ✓ | ✓ | ✓ | – | ✓ |
| Zone-level calibration quartiles | – | – | – | ✓ | **NO** |
| GADRS composite score | – | – | – | ✓ | **NO** |
| SSI / SHAP stability index | – | – | – | ✓ | **NO** |
| AURC / selective prediction | – | – | – | ✓ | **NO** |
| Nine-stage governance framework | ✓ | – | – | – | **NO** |
| Proxy variable MI audit | ✓ | ✓ | ✓ | – | **NO** |
| Salary ablation audit | ✓ | – | – | – | **NO** |
| "Evaluation discipline" framing | – | ✓ | – | – | **NO** |
| "Metric bounding" framing | – | ✓ | – | – | **NO** |
| "Eight-stage correction" | – | – | ✓ | – | **NO** |
| Governance/deployment framing | ✓ | ✓ | ✓ | ✓ | **NO** |
| EU AI Act / regulatory language | ✓ | – | – | – | **NO** |
| Oversight saturation / SEDI | – | – | – | – (E,F,G) | **NO** |
| Legitimacy / institutional theory | – | – | – | – (H,I,J) | **NO** |

Papers E, F, G, H, I, J have zero empirical overlap with the NHSJS paper.
They address governance theory, institutional sociology, queueing models,
and oversight saturation — entirely different topics.

---

## Differentiation Assessment

### What is shared vs. prior papers A–D

The NHSJS paper shares:
- The IBM HR dataset (unavoidable — it's the standard small tabular benchmark)
- The general concept of calibration, bootstrap CI, and fairness metrics
- CatBoost as one classifier

### How the NHSJS paper is materially different

1. **No governance framing.** Papers A–D all frame around organizational AI governance, deployment readiness, audit architectures, or metric discipline. The NHSJS paper frames around educational investigation: "what does accuracy hide?" These are structurally different contributions.

2. **No composite metrics.** GADRS (Paper D), nine-stage framework (Paper A), and eight-stage correction (Paper C) are all absent. The NHSJS paper evaluates three specific properties, not an architectural pipeline.

3. **No zone-level analysis.** Paper D's novel contribution is quartile-level calibration zones with SSI across zones. The NHSJS paper uses only global ECE — a simpler, educational-appropriate analysis.

4. **No SHAP analysis.** Papers A–D all include SHAP. The NHSJS paper deliberately omits it to avoid proximity to Paper D's SSI contribution. Permutation importance could be mentioned in future work.

5. **Different voice and scope.** The NHSJS paper is educational, student-investigative, and 3,000–4,000 words. Papers A–D are 6,000–12,000 word technical manuscripts targeting expert reviewers.

6. **Different audience-adjusted depth.** NHSJS explains what AUC is, what calibration means, and what equalized odds measures — concepts treated as assumed knowledge in all prior papers.

### Self-plagiarism risk assessment

LOW-TO-MODERATE. The shared empirical core (IBM HR + calibration + bootstrap + fairness) is the primary risk. However:
- The shared facts are empirical results from the same dataset, which is not self-plagiarism (it is replication across papers)
- No passages from prior papers have been copied
- The framing, scope, audience, structure, and contribution claim are all distinct
- NHSJS is a student-facing journal; A–C target applied ML / data science / BigData venues; D targets a social science journal

Recommended disclosure: include a brief note (already present in the paper) acknowledging that this work uses the IBM HR benchmark previously evaluated in related work by the same author, and that the current paper's focus is educational rather than technical.

---

## Terminology Collision Check

| Term in prior papers | Status in NHSJS |
|---|---|
| "governance-aware evaluation framework" | ABSENT |
| "nine-stage pipeline" | ABSENT |
| "evaluation discipline" | ABSENT |
| "metric bounding" | ABSENT |
| "metric scope violations" | ABSENT |
| "GADRS" | ABSENT |
| "SSI" (SHAP Stability Index) | ABSENT |
| "AURC" | ABSENT |
| "selective prediction" | ABSENT |
| "oversight saturation" | ABSENT |
| "assurance surface inflation" | ABSENT |
| "ceremonial authorization" | ABSENT |
| "legitimacy work" | ABSENT |
| "calibration" | PRESENT (educational context, not novel contribution claim) |
| "ECE" | PRESENT (defined from scratch for NHSJS audience) |
| "bootstrap" | PRESENT (simpler usage) |
| "DPD / EOD" | PRESENT (defined from scratch) |

All high-risk overlap terms are absent. Retained terms are common ML vocabulary, not proprietary framing.
