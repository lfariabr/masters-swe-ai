# Module 12 Follow-up Quiz - Answer Key

Use this after completing `module12_follow-up-quiz.md` closed book. Equivalent answers earn credit when they preserve the same diagnostic and methodological distinctions.

## 1. Metric versus loss (8 points)

- **Loss** is a differentiable proxy that guides weight updates during training.
- **Metric** is the number that judges whether the deployed system solves the real problem, and it does not need to be differentiable.

A fraud or rare-disease detector that always predicts "no" can score 99%+ accuracy while catching zero true cases; accuracy alone hides rare-class failure.

## 2. Choosing a metric under asymmetric cost (10 points)

**Coverage** is the metric for "how much of the workload the model can handle unaided" - the fraction of cases resolved without deferring to a human.

When false negatives cost far more than false alarms, **recall** is primary, but recall alone is gameable (flag everything, recall = 1.0). The correct framing is recall thresholded to a target (e.g. recall ≥ 0.90 on validation) with precision reported alongside, or an F-beta score with β > 1. Thresholding on recall changes deployment by shifting cases from "no flag" into either "auto-flag" or a **middle abstention band** that routes to a human with the underlying evidence, rather than letting the model force a binary call on every case.

## 3. Train/validation diagnosis table (12 points)

| Train | Validation | Diagnosis | Next move |
|---|---|---|---|
| poor | poor | underfit, optimisation failure, bad data, or a code/implementation bug | fit a tiny subset to isolate the bug; tune the learning rate; inspect data and preprocessing; add capacity only after the above are ruled out |
| good | poor | overfitting, or a train/test distribution mismatch | regularise (dropout, weight decay, early stopping); gather more representative data; verify the pipeline treats train and validation identically |
| good | good | target reached | stop, or justify the marginal cost of chasing further gains |

## 4. The debugging order (10 points)

In order: (1) visualise the worst / highest-confidence errors, (2) try to overfit one or a few examples to confirm the model *can* learn the task, (3) compare analytical and numerical gradients, and verify identical preprocessing between train and serving.

"Gather more data" fails when training error is already poor because the bottleneck is capacity, optimisation, or a code/data defect, not a shortage of examples - more rows of the same broken signal do not repair any of those, and more data is not a universal fix (module 12, Zone 2).

## 5. A high-confidence wrong prediction (10 points)

The diagnostic is **inspecting the highest-confidence errors** and tracing the specific instance back to its source data - the same move that found the cropped Street View digits. Second-best: verify that preprocessing is identical across train and serving, since silent truncation often enters on only one side.

Architecture is the wrong first move because the failure is **upstream of the model** - the network is correctly fitting a corrupted input, so a bigger or more complex architecture will fit that corrupted signal more confidently, not correct it.

Train and validation metrics can both look fine because if the truncation is present consistently in both splits, the model is fitting the same (bad) function on both - the diagnosis table cannot see a data-contract bug; only instance-level inspection can.

## 6. Smith's seven phases (12 points)

1. Prepare (is DL worthwhile, define success)
2. Prepare data
3. Find an analogy
4. Simple baseline
5. Visualise / debug
6. Fine-tune
7. Add complexity

**Phase 7 ("Add complexity")** explicitly asks whether the residual error justifies ensembles or added architectural complexity. It comes last because complexity should be earned by measured, diagnosed gaps in a working baseline, not chosen upfront - reversing the order risks debugging a complicated system with no simple baseline to isolate the fault against.

## 7. Error analysis versus ablative analysis (10 points)

- **Error analysis** compares current performance against a realistic ceiling to find which failure categories block success.
- **Ablative analysis** compares a baseline against the current system to find which added components actually caused the gain.

"Perfect performance" is often unreachable because of **label noise / ambiguity** (annotators disagree) and **irreducible (Bayes) error** from missing or insufficient input information. A realistic human or reference-system ceiling should replace the imaginary 100% target, and remaining errors should be prioritised by frequency, cost, and fixability.

## 8. High-dimensional optimisation (8 points)

"Needle in a haystack" is the classical intuition: one hard-to-find optimum in a vast bad space, so more parameters should make the search harder. "Haystack of needles" is Sejnowski's high-dimensional finding: overparameterised networks have **many** good solutions and mostly saddle points rather than bad local minima, so adding capacity does not make the search proportionally harder.

Implication: overparameterisation should not be feared by default; classical low-dimensional intuition about "too many parameters causes overfitting or gets you stuck" does not transfer cleanly to deep, high-dimensional networks.

## 9. Chollet's four future directions (12 points)

1. **Models as programs** - reasoning (loops, branches, memory, abstraction beyond a fixed differentiable mapping).
2. **Beyond backprop alone** - discrete optimisation (gradients combined with search / RL / evolution for non-differentiable structure).
3. **Automated ML** - automation (learned architecture and weights, less manual design).
4. **Lifelong modular reuse** - transfer (reusable features/subroutines, learning new tasks from little data).

## 10. Applying the module to Assessment 3 (8 points)

- **Baseline:** a TF-IDF review-only classifier established the simplest end-to-end system before any neural or aspect-aware model was built.
- **Diagnostic:** the mixed-polarity subset (sentences with conflicting sentiment across aspects) separated the two aspect-conditioned models (ATAE-LSTM, DistilBERT) from the four review-only models - the aspect-conditioned pair showed the smallest accuracy drop, evidence that reading the aspect matters specifically on the hard cases, not just on average.
- **Next experiment:** the measured gaps justify multi-seed uncertainty estimates, same-device efficiency comparison, cross-domain evaluation, calibration/abstention, or automatic aspect extraction - pick whichever gap the report's evidence points to most directly.
