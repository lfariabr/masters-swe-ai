# MLN601 Assessment 2 - Recording Walkthrough v4 (for notebook v7)

Video: ENGLISH, 7-10 min, filename `MLN601FariaLuisBrief2.mp4`.
Big change since v3: **the v7 notebook narrates itself** - every table/figure prints its
number and a one-line conclusion. On camera: read the printed line, expand it with ONE
sentence, move on. This script is now a safety net (timings + transitions + fact traps),
not a word-by-word text.

## Ground rules (from the 16 Jul takes)

- **Clock rule**: if a block runs 15s over, cut commentary, never numbers.
- **Fact traps - say these aloud 5x before recording:**
  - "six thousand four hundred ninety-seven" (6,497 - NOT 6,400 / 6,597)
  - "one thousand four hundred seventy-three, about twenty-three percent" (1,473 - NOT 14,000)
  - "sixty-two point six versus thirty-seven point four" (62.6 / 37.4)
- Pronounce: **Gini** = "JEE-nee" | **SMOTE** = "smote" (one syllable)
- Never read long markdown paragraphs - point at the printed table captions instead.
- Transitions are the joints. They are written below - say them as written.

## Block 0 - Title (cells 0-1) | 0:00-0:50

- Name, subject, assessment; "an operational screening system for wine bottling lots".
- One sentence: CRISP-DM start to finish, decision tree as the required technique.

## Block 1 - Section 1 Business Understanding (cells 2-3) | 0:50-1:55

- The story: one row = one lab sample = one bottling lot. Model flags risky lots for
  extra tasting. "QC staff decide - the model never releases or rejects a lot."
- FN (weak lot escapes) costs more than FP (unnecessary review).
- Point at the gates: "success is defined BEFORE modelling - AUC 0.75, sensitivity 0.70,
  specificity 0.70, in cross-validation."
- **Transition**: "So what data do we have to work with?"

## Block 2 - Sections 2.1-2.3: data + audit (cells 4-14) | 1:55-3:00

- 2.1-2.2: quick scroll - source, variables table. "Six thousand four hundred
  ninety-seven samples, red and white combined, wine_type flag added."
- 2.3: one line - pinned versions, RANDOM_STATE 42, local-first loading.
- Table 2.1: "every hard check passes." Table 2.2 + Figure 2.1 (boxplots):
  "the IQR audit flags one thousand four hundred seventy-three rows, about
  twenty-three percent - unusual but plausible wine, so they stay. Flag is not error."
- **Transition**: "One issue does need action: duplicates."

## Block 3 - Sections 2.4-2.5: target, balance, relationships (cells 15-23) | 3:00-3:55

- 2.4: "quality below six is low, class one - the positive class, because low is what
  triggers review." 1,177 exact duplicates removed BEFORE splitting - leakage control.
  Result: 5,320 rows, "sixty-two point six versus thirty-seven point four" (Figure 2.2).
- 2.5 heatmap (Figure 2.3): ONE sentence - "free and total SO2 correlate at 0.72,
  chemically expected - that motivates an engineered feature tested in Section 3."
- Target ranking (Table 2.3 / Figure 2.4): "alcohol is the strongest signal, minus 0.41 -
  more alcohol, less risk of low quality. Watch alcohol - it returns in every act."
- Pairplot (Figure 2.5): ONE sentence - "the classes overlap everywhere; no single
  measurement separates them, so we need a model."
- Interpretation table: don't read it - "summarized here."
- **Transition (diagnosis -> treatment, it worked in take 3)**: "That completes the
  diagnosis. Now the treatment: preparing the data without fooling ourselves."

## Block 4 - Section 3 Data Preparation (cells 24-26) | 3:55-4:35

- Four safeguards, count them on screen: dedup first; target columns excluded from
  predictors; stratified 80/20 split - "four thousand two hundred fifty-six train,
  one thousand sixty-four test, zero overlap, checked"; scaling and SMOTE inside pipelines.
- Announce the ablation: "two sulfur features enter a pre-declared trial - kept only if
  they gain at least 0.01. **The verdict comes in Section 4.1** - not here."
- **Transition**: "With clean inputs, six candidates compete."

## Block 5 - Section 4 Modelling (cells 27-29) | 4:35-5:20

- Read the six-candidate list as questions: baseline = "what does no skill look like";
  default tree = overfitting; tuned tree = GridSearchCV, 5 folds, ROC-AUC;
  balanced tree = same structure, cost-weighted errors; SMOTE = synthetic alternative;
  SVM = benchmark from another family.
- One line on ranges: "each search range has a reason - depths three to eight keep the
  tree readable; an unlimited tree is included as a control, and it loses."
- SVM scaling line: "the scaler lives inside the pipeline - fit only on each fold's
  training data. Same discipline as SMOTE."
- **Transition**: "Selection happens in cross-validation, against the gates - the test
  set is touched once, later."

## Block 6 - Section 4.1: selection + ablation (cells 30-35) | 5:20-6:10

- 4.1.1 (Tables 4.1-4.2): "the search picks Gini, depth five, minimum leaf twenty.
  RBF is the best SVM kernel."
- 4.1.2 (Table 4.3) - THE table, slow down: "only the balanced tree passes all three
  gates: 0.787, 0.731, 0.703. The AUC-tuned tree misses too many low lots - sensitivity
  0.643. SMOTE fails specificity by a hair - 0.696. Cost-based balancing beats
  synthetic examples. And the SVM has the best AUC, 0.826, but catches too few low lots."
- 4.1.3 (Table 4.4): "the sulfur features gain 0.0075 - below my 0.01 rule - rejected.
  I even re-tuned the tree with them included; they still don't earn their place."
- **Transition (frozen selection)**: "The selection is frozen. Now the final exam:
  data the model has never seen."

## Block 7 - Section 5: held-out test (cells 36-44) | 6:10-7:20

- Table 5.1: "the balanced tree confirms its CV profile - AUC 0.792, sensitivity 0.734,
  specificity 0.725. Near-identical to CV: it generalizes." Note the baseline row:
  "62.6% accuracy, zero low lots caught - that is the accuracy trap."
- Table 5.2 (classification report): one line - "low-class recall 0.734, F1 0.669 -
  we report the minority class, not accuracy."
- ROC (Figure 5.1): "the SVM ranks best on AUC, 0.824 - but ranking is only half the
  story; the threshold decides what actually gets caught."
- Confusion matrices (Figure 5.2) - **the MIDDLE panel is the approved model**. Derive
  the row: "398 low lots in the test set: 292 caught, 106 missed; 183 acceptable lots
  reviewed unnecessarily." Comparison: left (AUC-tuned) misses 164; right (SVM)
  misses 163 despite the best AUC.
- Trade-offs barplot (Figure 5.3): "we catch 58 more weak lots than the AUC-tuned tree
  and accept 69 more false alarms - the right side of the trade, given Section 1's costs."
- Tree plot + importance (Figures 5.4-5.5): "alcohol dominates, 0.62 - the tree agrees
  with Section 2's correlation."
- **Transition**: "The numbers say what the model does. Now WHY it decides - per lot."

## Block 7b - Sections 5.1-5.3: SHAP + approval (cells 46-57) | 7:20-8:20

- 5.1 SHAP, three beats in scroll order:
  - 5.1.1: "the additivity check passes - explanations are exact arithmetic, not estimates."
  - 5.1.2 global (Table 5.4 / Figure 5.6): "alcohol leads again, 0.19; low alcohol
    pushes toward low quality."
  - 5.1.3 local (Table 5.5 / Figure 5.7): "THIS lot: alcohol nine point six adds
    plus 0.22, volatile acidity plus 0.07, probability 0.797 - that is the answer
    QC needs when asking why a lot was flagged."
- 5.2 Operational result: point at the CV vs test table - "near-identical, frozen
  before testing." Don't re-read numbers already said in Block 7.
- 5.3 Approval table: read the four decisions; then the strongest line, slowly:
  "threshold optimisation is deferred - choosing it now would invent a business
  cost function."
- **Transition**: "Approved for a pilot. What did the process teach?"

## Block 8 - Section 6 Lessons (cells 58-59) | 8:20-9:10

- One from each list: went well - "gates before results made selection honest";
  challenge - "a model can lead one metric and still be wrong for the business";
  future - "real lot IDs, real costs, and comparing logistic regression and random
  forest under the same gates."
- Sommelier API: one sentence - "the delivery path already exists as a live FastAPI +
  Streamlit project - Appendix B and the pipeline diagram in Appendix C."

## Block 9 - Closing | 9:10-9:30

- "A balanced decision tree, chosen by pre-declared gates, explained globally and
  per lot, approved for human-supervised triage. Thank you."

## Rehearsal sequence

1. Scroll v7 once with this script beside it - check every cell range lands where expected.
2. Say the 6 transition lines out loud, twice each.
3. Fact traps aloud, 5x each.
4. One audio-only take with a stopwatch; adjust with the clock rule.
5. Record. If a block derails, keep rolling - restart the BLOCK, not the video; cut later.
