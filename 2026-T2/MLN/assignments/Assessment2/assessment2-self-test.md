# MLN601 Assessment 2 - Self-Test (40 min)

A closed-book check on the wine-quality classification assessment: CRISP-DM, ROC/AUC,
imbalance, the confusion matrix, tree tuning, leakage, and the generative vs discriminative
contrast (Naive Bayes).

**How to use it**
- Time-box: ~40 minutes. Write your answers on paper or in a scratch file first.
- Questions get harder as you go (Q1 easy → Q10 hard). Total = 100 points (+5 bonus).
- **Do not scroll to the Answer Key until you are done.** Then self-grade with the rubric.
- For written questions, 2-4 honest sentences is enough. "I don't know" beats a bluff.
- Bonus reason to do this NOW: everything you recall here is exactly what you say in the
  video. This is rehearsal disguised as a quiz.

Your key numbers to reason from (combined red+white, 6,497 wines, held-out test set of 1,300):

| Model | Test AUC | Accuracy |
|---|---|---|
| Logistic Regression | 0.814 | 0.752 |
| Decision Tree (tuned) | **0.809** | 0.737 |
| Decision Tree (default) | 0.773 | 0.786 |
| Naive Bayes (Gaussian) | 0.771 | 0.703 |
| Majority baseline | 0.500 | 0.633 |

Classes: **63% high / 37% low** (low = positive class). Tuned-tree recall: **high 0.78 vs
low 0.66**. Best params: `max_depth=6`, `min_samples_leaf=20`, gini. Feature importance:
**alcohol 0.49**, volatile acidity 0.21. The two sulfur-dioxide features correlate at 0.72.

---

## Section A - Foundations (easy)

### Q1. Reframing the problem (5 pts) - multiple choice
A1 used the SAME wine data as regression; A2 turns it into **binary classification**. What
fundamentally changed?

- A) The dataset was replaced with a bigger one
- B) The target: the numeric quality score became a two-class label (low < 6 vs high >= 6), so the question shifts from "how far off?" to "which side of the line, and how well separated?"
- C) The features were rescaled to 0-1
- D) Nothing - classification and regression are the same task with different names

### Q2. The positive class (5 pts) - written, 1-2 lines
The notebook deliberately makes **"low quality" the positive class** (label 1). Why that
choice, in business terms?

### Q3. The majority baseline (8 pts) - multiple choice
The `DummyClassifier` that always predicts "high" scores **accuracy 0.633** but **AUC 0.500**.
What does that pair of numbers tell you?

- A) The baseline is a decent model - 63% is a passing grade
- B) Accuracy inherits the class imbalance for free (63% is the cost of saying "high" every time), while AUC 0.5 exposes that it has zero ability to rank or separate the classes
- C) AUC is broken for baselines
- D) The baseline overfits

---

## Section B - Metrics & interpretation (medium)

### Q4. The ROC curve (10 pts) - written
In 2-4 sentences: (a) what is on the two axes of a ROC curve, and what does moving along the
curve correspond to? (b) What does the diagonal line represent, and why does the tuned tree's
curve sitting well above it matter?

### Q5. Accuracy went DOWN with tuning (10 pts) - written
The default tree scores **accuracy 0.786**, the tuned tree only **0.737** - yet the tuned tree
is the better model (AUC 0.773 → 0.809). Explain how tuning can lower accuracy while
improving the model, and why that is not a contradiction here.

### Q6. Reading the confusion matrix (10 pts) - written
Tuned-tree recall is **0.78 for high** wines but only **0.66 for low** wines.
- (a) In plain words, what does "recall 0.66 for low" mean?
- (b) Which of the two errors (missing a low wine vs flagging a good wine as low) is more
  costly for the business framing (a screen that flags weak batches for expert tasters), and
  what lever could shift the balance?

---

## Section C - Pipeline, tuning, leakage (hard)

### Q7. Stratified split + scaler placement (12 pts) - multiple choice + one line
**Part 1 (MC):** the 80/20 split uses `stratify=y`. Why?

- A) To shuffle the rows more randomly
- B) To preserve the 63/37 high/low ratio in both train and test, so the test metrics are not distorted by a lucky or unlucky class mix
- C) To make training faster
- D) Because Decision Trees require stratification

**Part 2 (written, one line):** the `StandardScaler` sits **inside** the Logistic Regression
Pipeline (not applied to all of `X_train` first). State the leakage rule this enforces -
careful with the DIRECTION of the arrow.

### Q8. What the tuned hyperparameters do (12 pts) - written
GridSearchCV chose `max_depth=6` and `min_samples_leaf=20`.
- (a) What does each parameter control in the tree?
- (b) What would an UNconstrained tree (no depth limit, leaf size 1) do on this data, and why
  does that hurt test performance?
- (c) Why was the grid scored on `roc_auc` instead of accuracy?

---

## Section D - Synthesis (hardest)

### Q9. Generative vs discriminative (13 pts) - written
The tree and logistic regression are *discriminative*; Gaussian Naive Bayes is *generative*.
- (a) What does each type of model actually learn / model?
- (b) NB assumes features are independent given the class - your own heatmap shows the two
  sulfur-dioxide features correlate at 0.72, so the assumption is violated. Yet NB still
  scores AUC **0.771**. Why does it stay usable despite the broken assumption?

### Q10. The honest finding (15 pts) - written
Logistic Regression (0.814) essentially **ties** with the tuned Decision Tree (0.809).
- (a) What does that near-tie tell you about the shape of the decision boundary in this data?
- (b) Why is reporting this openly a STRENGTH of the assessment, not a failure of the tree?
- (c) Given the tie, name one concrete reason you might still deploy the tree over the
  logistic regression for the wine-screening use case.

---

### Bonus (5 pts) - multiple choice (the classic trap)
Your tuned tree's AUC is **0.809**. Does that mean the model is right 80.9% of the time?

- A) Yes - AUC is just accuracy measured on the ROC curve
- B) No - AUC is the probability that a randomly chosen positive (low wine) is ranked above a randomly chosen negative (high wine); it is about ranking across ALL thresholds, not correctness at one threshold
- C) Yes, but only on the training set
- D) No - AUC is the error rate, so it is right 19.1% of the time

---
---

# 🛑 STOP - Answer Key below. Do the quiz first.

<br><br><br><br><br><br><br><br>

---

## Answer Key & Rubric

### Q1 - **B** (5 pts)
Same wines, different question. Regression asked "how far off is my number?" (RMSE/R²);
classification asks "which side of the line, and how well do I separate the groups?"
(AUC-ROC). The target, the baseline, the models and the whole metric vocabulary change with it.

### Q2 (5 pts)
Because the **action** we care about is flagging the weak batches - the screen exists so
expert tasters spend time where it matters. The positive class should be the event you want
to detect, so recall/precision "for the positive class" directly measure the useful thing.
- *Scoring:* full marks for "low is what we act on / want to catch"; 2 pts if you only said
  "the brief said so."

### Q3 - **B** (8 pts)
The trap of accuracy under imbalance in one row: 63% accuracy is free for a model with zero
skill. AUC strips that away - 0.5 = random ranking, no separation. This is exactly why the
whole assessment is scored on AUC, not accuracy.

### Q4 (10 pts)
- (a) **y-axis TPR (recall of the positive class), x-axis FPR** (false alarms among the true
  negatives). Each point is one **decision threshold**; sliding the threshold from strict to
  lenient traces the curve. (6 pts)
- (b) The diagonal is **random guessing** (TPR = FPR at every threshold). Sitting well above
  it means the model buys true positives at a cheap false-alarm price at many thresholds -
  genuine separation, threshold-independent. (4 pts)

### Q5 (10 pts)
The grid optimised **roc_auc**, not accuracy - so it happily traded raw hit-rate at the 0.5
threshold for better *ranking* across all thresholds. Under a 63/37 imbalance, accuracy is a
soft target (the baseline gets 0.633 for free), so a drop from 0.786 to 0.737 says little;
the AUC rise 0.773 → 0.809 says the tuned tree separates the classes better. You optimise
what you actually care about, and the metrics can disagree.
- *Scoring:* 6 pts for "optimised AUC, not accuracy"; 4 pts for why accuracy is the wrong
  yardstick under imbalance.

### Q6 (10 pts)
- (a) Of all the wines that are TRULY low quality, the model catches **66%** - it misses
  about 1 in 3 weak batches. (4 pts)
- (b) In the screening framing, **missing a low wine** (a false negative) is the costlier
  error: a weak batch ships unflagged; a false alarm just costs one expert taste. Lever:
  **lower the decision threshold** (or use `class_weight`) to trade precision for recall on
  the low class. (6 pts - any defensible cost argument + a threshold/weighting lever gets full
  marks)

### Q7 (12 pts)
- **Part 1: B** (6 pts). Stratification preserves the class mix in both sets - crucial under
  imbalance, otherwise a skewed test set biases every metric.
- **Part 2** (6 pts): the scaler is refit on each CV fold's **training portion only**, so
  **validation/answer data never flows INTO training** - not the model, not the scaler, not
  even a mean. (Direction check: it is the validation fold leaking into the scaler we
  prevent - remember the A1 fix.)

### Q8 (12 pts)
- (a) `max_depth` caps how many split levels the tree can stack (its overall complexity);
  `min_samples_leaf` forbids leaves smaller than 20 wines, so no rule is built on a handful
  of samples. (4 pts)
- (b) An unconstrained tree keeps splitting until leaves are pure - it **memorises the
  training set** (noise included). Train accuracy ~1.0, but it generalises worse: the
  default tree's AUC 0.773 vs the pruned tree's 0.809 is that gap made visible. (4 pts)
- (c) Because the deliverable is judged on **ranking/separation under imbalance** - scoring
  the grid on accuracy would have selected a tree that plays the majority-class safe bet.
  Tune on the metric you report. (4 pts)

### Q9 (13 pts)
- (a) **Discriminative** models learn P(class | features) - the boundary - directly.
  **Generative** models learn P(features | class) per class (here: a Gaussian per feature per
  class) plus the priors, and invert with **Bayes' rule** to classify. (6 pts)
- (b) Because classification only needs the **right ORDER** (ranking), not calibrated
  probabilities. Violated independence distorts the probability values but often preserves
  which class wins, so AUC survives - the classic Domingos & Pazzani (1997) result. NB's
  0.771 is level with the default tree despite the "naive" assumption being false. (7 pts)

### Q10 (15 pts)
- (a) A straight-line (linear) boundary captures almost everything the axis-aligned tree
  splits capture - the signal separating low from high wine is **mostly linear** in these
  features; there is little non-linear structure left for the tree to exploit. (5 pts)
- (b) Honest evaluation is the competency being graded: the comparison was run fairly and
  reported as found. It also shows the baseline-and-comparator design working - without
  LogReg in the lineup, "AUC 0.809" would have looked more impressive than it is. Model
  choice should be evidence-based, not loyalty-based. (5 pts)
- (c) Any one of: the tree is a **white-box** - the tree diagram + feature importances
  (alcohol 0.49, volatile acidity 0.21) are directly explainable to a non-technical QC
  stakeholder; it needs no scaling; it handles the features' non-linearities/interactions if
  the data drifts. (5 pts)

### Bonus - **B** (5 pts)
AUC = P(random positive ranked above random negative). It is threshold-free; accuracy lives
at exactly one threshold. The tuned tree makes the trap vivid: AUC 0.809 with accuracy 0.737 -
if AUC "were" accuracy, those two numbers could not disagree.

---

## Score yourself

| Band | Total /100 | Read |
|---|---|---|
| 85-100 | You own this material - record the video today |
| 70-84 | Solid; re-read the sections behind the misses, then record |
| 50-69 | Concepts landing but fragile - re-walk the notebook first |
| < 50 | Re-read the notebook + script, retake tomorrow |

**Where each question maps in the notebook (v2)**
- Q1-Q3 → title/intro + Business Understanding + baseline cell
- Q4-Q6 → Evaluation (ROC figure, metrics table, confusion matrix)
- Q7 → Data Preparation (split cell + LogReg Pipeline)
- Q8 → Modelling (GridSearchCV + best params)
- Q9 → §5.4 generative vs discriminative
- Q10 → Evaluation interpretation + §6 lessons learned
