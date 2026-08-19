# Module 12 Follow-up Quiz

**Scheduled:** Thursday, 20 August 2026, early morning

**Time box:** 20 minutes

**Mode:** Closed book, written answers, then check the separate answer key

Do not open `module12_follow-up-quiz-answers.md` until every question has an answer. State the metric, the diagnostic, and the evidence where relevant; avoid vague answers such as "tune the model."

## Questions

### 1. Metric versus loss (8 points)

In one sentence each, distinguish the training loss from the evaluation metric. Give one example where 99%+ accuracy is a worthless number.

### 2. Choosing a metric under asymmetric cost (10 points)

For a system that may abstain and defer to a human, name the metric that captures "how much of the workload the model can safely handle unaided." A false negative is far more costly than a false alarm. Which metric is primary, and what does thresholding on it change about deployment?

### 3. Train/validation diagnosis table (12 points)

Fill in the likely diagnosis and one evidence-based next move for each cell:

| Train | Validation | Diagnosis | Next move |
|---|---|---|---|
| poor | poor | | |
| good | poor | | |
| good | good | | |

### 4. The debugging order (10 points)

List, in order, the first three things to check when a model is confidently wrong on a specific input, before touching the architecture. Why does "gather more data" fail as a fix when the training error is already poor?

### 5. A high-confidence wrong prediction (10 points)

A prediction is wrong with high confidence because a source-system field was silently truncated upstream. Which diagnostic exposes this? Why would changing the network architecture be the wrong first move? Why might train and validation metrics both look fine even with this bug present?

### 6. Smith's seven phases (12 points)

Name the seven phases in order. Which phase explicitly asks "does the residual error justify the added complexity," and why does it come last rather than first?

### 7. Error analysis versus ablative analysis (10 points)

Define both in one sentence each. A "perfect performance" ceiling is often unreachable — name two reasons why, and what should replace it as the comparison point.

### 8. High-dimensional optimisation (8 points)

Explain the "needle in a haystack" versus "haystack of needles" contrast. What does this imply about whether overparameterisation should be feared?

### 9. Chollet's four future directions (12 points)

Name Chollet's four proposed directions for deep learning's future. For each, give one word for the capability it targets (e.g. reasoning, discrete optimisation, automation, transfer).

### 10. Applying the module to Assessment 3 (8 points)

In three concise bullets, state how ReviewPulse v3 embodies the practical-methodology loop: what was the baseline, what diagnostic distinguished the aspect-conditioned models from the review-only ones, and what is one next experiment the measured gaps justify.

## Score Guide

- **90-100:** Can connect metric choice, diagnosis, phased methodology, and future-capability language into one coherent story.
- **75-89:** Core distinctions are sound; tighten the debugging order or the error-versus-ablative contrast.
- **60-74:** Review the train/validation diagnosis table and Smith's seven phases before applying the framework.
- **Below 60:** Re-read the one-pager, then retake the quiz closed book.
