# BDA601 · Module 7 - One-Pager

> **Model evaluation - confusion matrix · precision/recall/F1 · cross-validation · cost-benefit · ROC/AUC · metric selection**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **A model's score on its own training data is a lie.** Evaluation is two disciplines glued together: pick a **metric that matches the decision** (accuracy is not it), and get that number from a **sampling protocol that never let the model see the test data**. Then, and only then, compare models.
> (Han §8.5.1 + §8.5.6 · Witten Ch.5 · Srivastava 2019)

## 🖤 Zone 1 - The confusion matrix is the foundation

```text
                 PREDICTED
                 yes      no
        ┌──────┬────────┬────────┐
ACTUAL  │ yes  │   TP   │   FN   │  P = TP + FN   (all real positives)
        │ no   │   FP   │   TN   │  N = FP + TN   (all real negatives)
        └──────┴────────┴────────┘
        good model = everything on the diagonal
```

- 🖤 **TP** = caught it · **TN** = correctly ignored it · **FP** = false alarm (Type-1) · **FN** = miss (Type-2).
- 🔵 Off-diagonal cells tell you *which* classes get confused, not just how often. An *m x m* table for *m* classes.
- 🔴 **Resubstitution error** = error measured on the **training** set. It is **optimistically biased** - the model already memorised those rows. Every metric below is computed on a **held-out test set**.

## 🖤 Zone 2 - The metric family ⭐ SLO d) - THE GRADED CORE

| Metric | Formula | Answers |
|---|---|---|
| **Accuracy** | `(TP+TN)/(P+N)` | overall % correct |
| **Error rate** | `(FP+FN)/(P+N)` = `1 - accuracy` | overall % wrong |
| **Sensitivity / Recall** (TPR) | `TP/P` | of real positives, how many caught? (**completeness**) |
| **Specificity** (TNR) | `TN/N` | of real negatives, how many caught? |
| **Precision** | `TP/(TP+FP)` | of predicted positives, how many right? (**exactness**) |
| **F1** | `2·P·R / (P+R)` | harmonic mean - balances precision & recall equally |
| **Fβ** | `(1+β²)·P·R / (β²·P + R)` | β weights recall vs precision. **F2 favours recall · F0.5 favours precision** |

- 🔵 `accuracy = sensitivity·(P/(P+N)) + specificity·(N/(P+N))` - accuracy is just a class-weighted blend of the two rates.
- 🔵 **Harmonic mean punishes extremes:** precision 0, recall 1 → F1 = **0**, not 0.5. You cannot game F1 by maxing one side.
- 🔴 **Precision and recall move inversely.** Compare precision **at a fixed recall** (e.g. precision @ recall = 0.75), or collapse both into F1.

## 🖤 Zone 3 - Why accuracy lies (the imbalanced-data trap)

**The cancer trap - screen 10,000 people, only 300 have cancer (3%). Build the laziest model: always predict "no".**

```text
                 PREDICTED
                 cancer    no
        ┌──────┬────────┬────────┐
ACTUAL  │cancer│  TP=0  │ FN=300 │   P = 300     ← every single one MISSED
        │  no  │  FP=0  │TN=9700 │   N = 9,700
        └──────┴────────┴────────┘

accuracy    = (TP+TN)/total =  9700/10000 = 97%   ← looks brilliant
sensitivity = TP/P          =     0/300   =  0%   ← learned NOTHING
specificity = TN/N          =  9700/9700  = 100%
```

- 🖤 **Why it happens (arithmetic, not ML):** accuracy is dominated by the **biggest class**. With 97% of rows negative, getting negatives right is worth 97 points; the positives - the entire reason the model exists - are worth 3. A rock with "no" painted on it beats most real models.
- 🖤 **Why the fix works:** sensitivity and specificity score each class **against its own total** (`/P` and `/N`, not `/everybody`), so neither class can hide behind the other. Accuracy is just a size-weighted blend of the two - and that weighting is what does the lying.
- 🔴 Han's version with a *real* classifier: **96.4% accuracy hiding 30% sensitivity** - still missing 7 of every 10 cancers.
- 🔴 **Rule:** accuracy is only trustworthy when classes are **roughly balanced**. The moment the interesting class is rare (cancer, fraud, churn, a failed load), report **sensitivity + specificity** (or precision + recall) separately - never a lone accuracy figure.
- 🔵 Classifiers are also judged on **speed · robustness · scalability · interpretability** - not just the score.

## 🖤 Zone 4 - Reliable estimates: how you get an honest number

```text
TRAIN  →  build the model(s)
VALID  →  tune hyperparameters / pick the scheme
TEST   →  final error estimate. USED ONCE. NEVER touched before that.
```

- 🔴 **Golden rule:** the test set may **never** influence any choice (feature, threshold, hyperparameter). Peeking = optimistic bias.
- 🔵 After the estimate is locked, you *may* fold validation + test back into training to build the shipped model.

| Method | How | Verdict |
|---|---|---|
| **Holdout** | 2/3 train, 1/3 test | simple; can draw an unrepresentative split |
| **Stratification** | force each class into train/test at its true proportion | cheap insurance against unlucky splits |
| **Repeated holdout** | resplit + average | kills luck-of-the-draw variance |
| **Stratified 10-fold CV** ⭐ | 10 folds; each is test once, train 9x; average | **THE DEFAULT.** Repeat 10x (10 x 10-fold) for a reliable number |
| **Leave-one-out** | n-fold CV, 1 row out each time | max training data, deterministic; expensive; **cannot stratify** |
| **0.632 bootstrap** | sample n rows **with replacement**; unpicked rows = test | best for **very small** datasets |

- 🔵 **Bootstrap maths:** `(1 - 1/n)ⁿ ≈ e⁻¹ = 0.368` never picked → train ≈ **63.2%** unique rows. Estimate: `e = 0.632·e_test + 0.368·e_train`.
- 🔴 **k trade-off:** small k → high selection bias, low variance. k = n (LOO) → low bias, high variance. **k = 10 is the recommended default.**
- 🔴 Hyperparameter tuning happens in the **validation set / inner CV** only. Doing it properly = **nested (inner/outer) CV**.

## 🖤 Zone 5 - Cost-benefit and the ROC curve

- 🖤 **Errors are not equally costly.** A missed cancer (FN) >> an unnecessary follow-up (FP). Lending to a defaulter >> denying a good customer. So weight each confusion-matrix cell by its **real-world cost** and compare **average cost per decision**, not `(TP+TN)/total`.

```text
 TPR   1 ┤        ,-─────  M1  (hugs top-left = good)
(= sens) │      ,'   ,--─   M2
         │    ,'  ,-'
         │  ,' ,-'      ,'   diagonal = random guessing
         │,',-'      ,-'
       0 └────────────────── 1
              FPR (= 1 - specificity)
```

- 🔵 **How it is drawn:** rank rows by predicted `P(positive)`, walk the list top-down, **move UP on a TP, RIGHT on a FP**. Needs a **probabilistic** classifier (Naive Bayes, logistic regression; trees can be adapted to emit probabilities).
- 🔴 **AUC:** `1.0` = perfect · `~0.5` = random. Bands: **.90-1 excellent · .80-.90 good · .70-.80 fair · .60-.70 poor · .50-.60 fail**.
- 🔴 **AUC is threshold-independent** - it judges the model's **ranking** ability across all cut-offs, which is why it beats accuracy on imbalanced data. Then pick the operating threshold that matches your cost structure.

## 🖤 Zone 6 - The practitioner toolkit (and the metric-selection message)

| Classification | Gist | Shines when |
|---|---|---|
| **Gain / Lift charts** | rank by prob, bucket into deciles, count responders captured | **campaign targeting** - which deciles to mail |
| **Kolmogorov-Smirnov** | max separation of the pos vs neg distributions (0-100) | measuring class separation |
| **AUC-ROC** | area under TPR vs FPR | imbalanced data; ranking quality |
| **Log loss** | penalises **confident wrong** calls; scores probabilities directly | you need **calibration**, not just order |
| **Gini** | `2·AUC - 1` (good > 60%) | single-number ranking score |
| **Concordant-discordant** | % of pos/neg pairs ranked correctly | raw predictive power |

| Regression | Gist |
|---|---|
| **RMSE** | squares errors → punishes big misses; **very outlier-sensitive** |
| **RMSLE** | log version - forgives large absolute gaps when both values are large |
| **R² / Adjusted R²** | how much better than predicting the mean; **adjusted** penalises useless added features |

- 🔵 **ROC vs Lift:** ROC is nearly independent of the base response rate; lift shifts when it changes - ROC travels better across datasets.
- 🔵 **Log loss vs AUC:** AUC only cares about the *order* of probabilities; log loss also rewards **confidence** in correct calls.
- 🔴 **The Activity 2 thesis:** *different problems need different metrics*. Pharma → **specificity** (avoid false alarms) · churn/attrition → **sensitivity** (catch every leaver) · marketing campaign → **lift** · price prediction → **RMSE/R²**.

## 🔴 Assessment Hook (bottom red strip)
> **A2 = Visualisation and Model Development** · source code + report (**1000 words** ±10%) · **30%** · due **26/07/2026** · SLOs **c) d) e)**.
> Module 6 trained the classifier; **Module 7 is the evidence that it works.** A2's marks live here: a confusion matrix, precision/recall/F1 (not bare accuracy), a defensible train/test split, and a stated reason for the metric you chose.
> **Then A3 = "Model Evaluation"** · source code + 7-10 min presentation · **40%** · due **19/08/2026** · SLOs **c) d) e)**. This module is literally that assessment's title - the sheet you are writing now is A3's spine.

## 🔴 If you only memorise 5 things
1. **Everything is built from the confusion matrix.** TP/TN/FP/FN → accuracy, sensitivity, specificity, precision, F1.
2. **Accuracy lies on imbalanced data** (97% accurate, 0 cancers caught). Always split it into sensitivity/specificity or precision/recall.
3. **Training error is not future error.** Train / validation / test - and the **test set is used once**.
4. **Stratified 10-fold cross-validation is the default answer** to "how good is this model?" on limited data.
5. **ROC/AUC compares probabilistic models without fixing a threshold** (1.0 perfect, 0.5 random) - because errors have different costs.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your pipeline dashboard says "99.9% of queries succeed". That is an **accuracy** number on wildly imbalanced data - what is its **sensitivity** to a failed nightly load, and which rare-but-expensive class is it hiding?
2. A missed bad load (FN) silently corrupts the warehouse for days; a false alert (FP) costs five minutes of triage. Given that cost asymmetry, which way do you slide the ROC threshold - and what does that do to precision?
3. Where in your work do you effectively validate a transformation on the same rows you tuned it on? What would a fresh "test partition" (e.g. a later date slice) actually be?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 **Activity 1** - PySpark on Larose `adult_ch6` train/test: build **Model 1** (Income ~ Marital Status + Capital Gains/Losses) and **Model 2** (Income ~ Marital Status + Age), build a **contingency table** for each, compare **accuracy / precision / recall / F1**, post to the "Model Evaluation" forum and reply to peers.
- [ ] 🕐 **Activity 2** - "Please explain": why *different evaluation metrics are used for different kinds of problems* (Srivastava 2019). Use scenarios, state whether you agree and why. Post + reply to peers.
- [ ] 🔥 **A2 is due 26/07/2026** - lock in the evaluation section: confusion matrix + precision/recall/F1 + the justification for the metric you picked.
