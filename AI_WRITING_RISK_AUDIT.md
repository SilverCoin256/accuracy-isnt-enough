# AI-Writing Risk Audit

## Overview

This audit checks the NHSJS manuscript for patterns commonly detected as
AI-generated writing. Flagged patterns and their resolution status are listed below.

---

## High-Risk AI-Writing Patterns

### 1. Parallel sentence triplets

**Pattern:** Three-item lists with identical grammatical structure and similar length.
**Risk:** Very high in AI prose. ("It does not measure X. It does not measure Y. It does not measure Z.")

**Status in manuscript:** The Introduction uses one three-item list structure
("It doesn't tell you whether the model's confidence estimates...") but with
varying clause lengths. Review this passage if any sentence feels too rhythmic.
**Recommendation:** Break the third item into a new sentence with different structure if needed.

### 2. "This paper argues / This paper demonstrates / This paper proposes"

**Status:** ABSENT. The paper uses "I investigated," "I wanted to test," and
"I ran three classifiers" — all first-person, student-voiced.

### 3. "It is important to note / It is worth noting / Notably"

**Status:** ABSENT.

### 4. "Moreover / Furthermore / Additionally"

**Status:** ABSENT.

### 5. Inflated transition phrases ("Given this context," "In light of the above,")

**Status:** ABSENT. Transitions are either direct ("But calibration analysis showed...")
or missing (paragraph breaks without explicit connector).

### 6. Over-balanced paragraph structure (claim → evidence → implication, every paragraph)

**Status:** LOW RISK. Some paragraphs skip the implication step (Results 4.2, 4.3).
The Discussion starts with the summary before breaking into sub-questions, which is
atypical of strict AI paragraph geometry.

### 7. Excessive citation density (3+ citations per sentence)

**Status:** LOW RISK. Maximum 2 citations per sentence, most sentences uncited.

### 8. Ornamental vocabulary

**Status:** LOW RISK. The vocabulary is mostly plain. Potentially elevated words:
"systematically," "substantive," "instability" — these are common enough in
student writing to be non-problematic.

### 9. Every section ending with a "larger significance" sentence

**Status:** ABSENT. Section 4.2 ends with an observation, 4.3 with a comparison.
Not every section wraps up with implications language.

### 10. Perfect flow / synthetic cadence

**Status:** Sentence lengths vary. Short sentences ("That's useful.") appear
alongside longer technical ones. The weatherforecast analogy and the "I found this
one of the more surprising results" are non-AI markers.

---

## Voice Authenticity Markers (Positive)

Phrases that signal student authorship and resist AI detector flags:

| Passage | Why it works |
|---|---|
| "I kept running into a question I couldn't shake" | Slightly informal, personal |
| "What does that number actually tell you?" | Rhetorical, conversational |
| "That's a pretty good score." | Colloquial — AI systems rarely write this |
| "These gaps might not matter much for...cats versus dogs" | Concrete, slightly humorous framing |
| "I found this one of the more surprising results" | Personal, evaluative |
| "That's not catastrophic, but it's not nothing either" | Double negative + informal qualifier |
| "What I'd Do Differently" as a section heading | Genuinely student-voiced |
| The Conclusion paragraph opening | First-person narrative |

---

## Sentence Rhythm Analysis

Sample from Introduction — lengths measured in words:

- "When someone says an AI system is '82% accurate,' it sounds pretty solid." — 16
- "More than four out of five predictions correct." — 9 (fragment — not AI style)
- "But I kept running into a question I couldn't shake: what does that number actually tell you?" — 18
- "The more I read about machine learning evaluation, the more I realized that accuracy—and even the more sophisticated version called AUC—leaves out some things that matter." — 32
- "It doesn't tell you whether the model's confidence estimates are trustworthy." — 14

Range: 9–32 words. Sufficient variation.

---

## Risk Zones That Need Monitoring

1. **Background section** — technically accurate but could sound like a textbook. The weather
   analogy breaks it up, but if the ECE definition paragraph is too precise and academic in
   final form, consider adding one informal phrasing within it.

2. **Table captions** — these are fine as-is; table captions are not a detection target.

3. **Discussion 5.1 and 5.2** — these are the most "essay-structured" subsections. They could
   benefit from one sentence of genuine hedging or personal reflection to stay student-voiced.

---

## Overall AI-Writing Risk Level: LOW

The manuscript has strong student-voice markers, variable syntax, first-person framing,
informal analogies, and genuine hedging. It avoids all common AI template patterns.
The main ongoing risk is the Background section reading as slightly textbook-like,
which is acceptable for a science journal paper by a high school student.
