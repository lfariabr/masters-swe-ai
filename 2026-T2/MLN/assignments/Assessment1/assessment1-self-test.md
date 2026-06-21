# MLN601 Assessment 1 - Self-Test (40 min)

A closed-book check on the wine-quality regression assessment: CRISP-DM, metrics,
linear vs regularised vs tree models, cross-validation, leakage, and your own results.

**How to use it**
- Time-box: ~40 minutes. Write your answers on paper or in a scratch file first.
- Questions get harder as you go (Q1 easy → Q10 hard). Total = 100 points (+5 bonus).
- **Do not scroll to the Answer Key until you are done.** Then self-grade with the rubric.
- For written questions, 2-4 honest sentences is enough. "I don't know" beats a bluff.

Your key numbers to reason from (combined red+white, held-out test set):

| Model | RMSE | R² |
|---|---|---|
| Random Forest (best) | 0.61 | 0.50 |
| Ridge / Lasso / ElasticNet / Linear | ~0.74 | ~0.27 |
| Mean baseline | 0.86 | ~0 |

Per-type mean absolute residual: **red 0.39** (341 test wines) vs **white 0.45** (959).
Single-type Random Forests: red-only R² **0.53**, white-only **0.56**, combined **0.50**.

---

## Section A - Foundations (easy)

### Q1. CRISP-DM (5 pts) - multiple choice
How many stages does CRISP-DM have, and what is the **first** one?

- A) 5 stages, starting with Data Understanding
- B) 6 stages, starting with Business Understanding
- C) 6 stages, starting with Data Preparation
- D) 4 stages, starting with Modelling

### Q2. Problem type (5 pts) - multiple choice
The task is framed as **regression** (not classification) because:

- A) wine comes in categories (red / white)
- B) the target `quality` is a numeric score treated as continuous, not a fixed set of unordered classes
- C) we chose a Random Forest
- D) there are 12 input features

### Q3. The baseline (8 pts) - multiple choice
Why include a "mean baseline" that predicts the average quality for every wine?

- A) It is the model we actually submit
- B) It is a reference floor that any useful model must beat - and R² is defined relative to it
- C) It makes the Random Forest train faster
- D) It scales the features before modelling

---

## Section B - Metrics & interpretation (medium)

### Q4. RMSE vs MAE (10 pts) - written
Your RF scored **MAE 0.44** but **RMSE 0.61**. In 2-4 sentences:
(a) which metric punishes a single large error (e.g. predicting 5 for a true-9 wine) more, and why;
(b) why RMSE is almost always **≥** MAE.

### Q5. R² (10 pts) - multiple choice + one line
**Part 1 (MC):** R² = 0.50 for the Random Forest means:

- A) the model is 50% accurate
- B) the model explains about 50% of the variation in quality; the rest is unexplained
- C) predictions are off by 0.50 quality points on average
- D) half of the predictions are exactly correct

**Part 2 (written, one line):** the mean baseline scored R² = **−0.0005**. What does a *negative* R² mean?

### Q6. Why the forest wins (10 pts) - written
In 2-4 sentences, explain why the Random Forest (R² 0.50) beat **every** linear model
(~0.27) on this data. What can a forest represent that a straight-line model cannot?

---

## Section C - Pipeline, tuning, leakage (hard)

### Q7. Scaler placement (12 pts) - multiple choice
Why is `StandardScaler` placed **inside** the `Pipeline` (with Ridge/Lasso/ElasticNet)
rather than applied once to `X_train` before `GridSearchCV`?

- A) For reproducibility of the random seed
- B) Because the Random Forest needs scaled inputs
- C) So that during 5-fold cross-validation the scaler is fit on each fold's **training portion only**, preventing the validation fold from leaking into the scaling
- D) To make the code shorter

### Q8. Ridge vs Lasso (12 pts) - written
(a) What is the difference between the **L2 (Ridge)** and **L1 (Lasso)** penalties?
(b) Which one can drive some coefficients **exactly to zero** (acting as feature selection)?
(c) As `alpha` grows very large (say 10,000), what happens to the coefficients and to the model's predictions?

---

## Section D - Synthesis (hardest)

### Q9. "More data didn't help" (13 pts) - written
On the combined set the RF scored R² **0.50**, yet the red-only RF scored **0.53** and
white-only **0.56**. Pooling gave *more* rows but a *lower* R². Explain why this can
happen, and what it tells you about **model choice vs dataset size** as levers for
performance.

### Q10. Diagnose and prescribe (15 pts) - written
The residual plots show the model **compresses predictions toward the middle** (it rarely
predicts below 5 or above 7), and the per-type table shows **red 0.39 vs white 0.45**
mean absolute residual.

- (a) Why does the middle-compression happen?
- (b) Propose **one concrete improvement** that targets it, and predict its likely effect.
- (c) Why is this model still framed as "decision support", not automation?

---

### Bonus (5 pts) - multiple choice (the classic trap)
You tuned `n_estimators = [200, 400]` (number of trees). Does adding **more trees** risk
overfitting the same way more `max_depth` does?

- A) Yes - more trees always overfit more
- B) No - averaging more trees mainly reduces variance and plateaus; it is `max_depth` that controls an individual tree's complexity and can overfit
- C) Yes - trees and depth are the same control
- D) More trees reduce the number of features used

---
---

# 🛑 STOP - Answer Key below. Do the quiz first.

<br><br><br><br><br><br><br><br>

---

## Answer Key & Rubric

### Q1 - **B** (5 pts)
6 stages: Business Understanding → Data Understanding → Data Preparation → Modelling →
Evaluation → Deployment. In this assessment, stage 6 becomes "lessons learned."

### Q2 - **B** (5 pts)
`quality` is a numeric score (ordinal 3-9), modelled as a continuous target. Classification
is for unordered categories. (Nuance: it is *ordinal*, which is why the report calls treating
it as continuous a simplification - full marks if you noted that.)

### Q3 - **B** (8 pts)
The baseline is the "null model." R² = 0 by construction for it, so it is the floor every
real model must clear to prove the features carry signal.

### Q4 (10 pts)
- (a) **RMSE** punishes the large error more. It **squares** each error before averaging, so a
  4-point miss contributes 16, a 1-point miss only 1 - big misses dominate. MAE treats every
  error linearly (a 4-point miss counts as 4).
- (b) RMSE ≥ MAE because squaring then square-rooting weights large errors more heavily; they
  are equal only if every error is identical.
- *Scoring:* 6 pts for "RMSE, because it squares errors"; 4 pts for the ≥ explanation.

### Q5 (10 pts)
- **Part 1: B** (6 pts). R² = fraction of variance in `quality` explained by the model.
  (Not accuracy, not average error - those are common wrong picks.)
- **Part 2** (4 pts): a negative R² means the model predicts **worse than just guessing the
  mean** - it adds noise rather than signal. (The baseline's −0.0005 is essentially 0.)

### Q6 (10 pts)
A linear model fits **one global straight line per feature** (a fixed slope). A Random Forest
is many decision trees splitting on thresholds, so it captures **non-linear curves and
interactions** (e.g. "alcohol helps *only when* volatile acidity is low"). Wine chemistry →
quality is non-linear, so the forest explains ~twice the variance.
- *Scoring:* full marks for "non-linearity and/or feature interactions a straight line can't model."

### Q7 - **C** (12 pts)
The leakage point. If you scale all of `X_train` first, the scaler's mean/std are computed
using rows that later become validation folds - the validation data leaks into training, and
CV scores come out too optimistic. Inside the Pipeline, `GridSearchCV` re-fits the scaler on
each fold's training rows only. (A = wrong: reproducibility is the seed. B = wrong: trees
don't need scaling.)

### Q8 (12 pts)
- (a) **L2/Ridge** penalises the **sum of squared** coefficients - shrinks them smoothly toward
  zero but rarely to exactly zero. **L1/Lasso** penalises the **sum of absolute** coefficients.
- (b) **Lasso** can set coefficients **exactly to zero** → built-in feature selection.
- (c) As `alpha → huge`, the penalty dominates: coefficients shrink toward **0**, and the model
  approaches the **mean baseline** (underfitting - high bias).
- *Scoring:* 4 pts each part.

### Q9 (13 pts)
Red and white are **partly different populations**. Pooling adds rows but also **heterogeneity**
- the model now has to fit two overlapping patterns at once, so per-type sharpness drops even
though total data rose. Lesson: **more data is not a guaranteed lever**; here the bigger win
came from **model choice** (linear → forest, +0.23 R²) than from sample size. The combined
model is still the better *deliverable* (one pipeline serves both via `wine_type`), but raw
volume ≠ better fit.
- *Scoring:* 7 pts for "different populations / heterogeneity"; 6 pts for "model > data as the lever here."

### Q10 (15 pts)
- (a) **Class imbalance:** training data is overwhelmingly quality 5-6-7, with very few 3, 4, 8,
  9. The model learns the "safe bet" of predicting near the middle, so it under-predicts great
  wines and over-predicts poor ones. (5 pts)
- (b) Any *one* defensible fix (5 pts), e.g. **class-balanced / stratified resampling or sample
  weighting** to expose the model to more extreme-score wines → should reduce the middle-
  compression and lower error at the tails (possibly at a small cost in the middle). Other valid
  answers: gradient boosting, an ordinal model, quantile loss.
- (c) **Decision support** because the target is a **subjective, ordinal human score**; even the
  best model leaves ~50% of variance unexplained and is unreliable at the extremes, so it should
  screen/assist experts, not replace tasting. (5 pts)

### Bonus - **B** (5 pts)
More trees mostly **reduces variance and plateaus** - a Random Forest *averages* its trees, so
extra trees rarely hurt (just cost compute). It is **`max_depth`** (individual-tree complexity)
that drives overfitting. Confusing the two is the classic mistake.

---

## Score yourself

| Band | Total /100 | Read |
|---|---|---|
| 85-100 | You own this material - submission-confident and viva-ready |
| 70-84 | Solid; revisit whichever section lost points |
| 50-69 | Concepts landing but fragile - re-read the cells behind the misses |
| < 50 | Re-walk the code walkthrough, then retake in a day |

**Where each question maps in the notebook/report**
- Q1-Q3 → Business Understanding + Modelling intro
- Q4-Q6 → Evaluation (metrics, model comparison)
- Q7-Q8 → Modelling cell (Pipeline, GridSearchCV, regularisation)
- Q9 → §5.3 dataset comparison
- Q10 → §5.2 residual diagnostics + §6 lessons learned
