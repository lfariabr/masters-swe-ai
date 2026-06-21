# MLN601 Assessment 1 - Self-Test: my answers + grading

Scored **80/100**. Solid. Two of my earlier weak spots (leakage, R-squared) are now locked
in, so real progress. One actual blank: Q8 (regularisation). Notes below so future-me
doesn't forget the fixes.

| Q | Topic | Score | Verdict |
|---|---|---|---|
| 1 | CRISP-DM | 5/5 | got it |
| 2 | Regression + ordinal | 5/5 | got it, even the nuance |
| 3 | Baseline | 8/8 | got it |
| 4 | RMSE vs MAE | 10/10 | nailed it (power-mean) |
| 5 | R-squared + negative | 10/10 | got it |
| 6 | Why RF wins | 8/10 | one word off |
| 7 | Scaler / leakage | 10/12 | mechanism right, arrow backwards |
| 8 | Ridge vs Lasso | 0/12 | blanked - learn this |
| 9 | More data didn't help | 9/13 | right family, wrong label |
| 10 | Diagnose + prescribe | 15/15 | got it + HITL bonus |

---

## Per question

### Q1 - CRISP-DM. 5/5
My answer: 6 stages, starting with business understanding (B).
Right. Order: Business Understanding -> Data Understanding -> Data Prep -> Modelling ->
Evaluation -> Deployment (which I turn into "lessons learned").

### Q2 - regression vs classification. 5/5
My answer: regression because quality is ordinal, not a fixed set of classes (B).
Right, and I caught the nuance: it's ordinal, so treating it as continuous is a simplification.

### Q3 - the baseline. 8/8
My answer: reference floor, R-squared is defined relative to it (B).
Right. It's the "always guess the mean" null model. R-squared = 0 for it by construction.

### Q4 - RMSE vs MAE. 10/10 (best answer)
My answer: RMSE punishes large errors more because it squares before averaging; it's bigger
than MAE by the power-mean inequality (quadratic mean >= arithmetic mean).
That's a tighter justification than the rubric asked for. RMSE = quadratic mean of errors,
MAE = arithmetic mean, so RMSE >= MAE always, equal only if all errors are identical.

### Q5 - R-squared. 10/10
My answer: model explains ~50% of the variation in quality (B). Negative R-squared = worse
than guessing the mean, model captures no meaningful signal.
Right on both. Negative R-squared = the model is adding noise, not signal.

### Q6 - why the forest wins. 8/10
My answer: RF wins because data isn't linearly correlated, no fixed "recipe of input
features"; forest handles multicollinearity and non-linear relationships better.
**Fix:** the core (non-linear) is right, but swap "multicollinearity" for **interactions**.
Multicollinearity mainly wrecks the *linear model's coefficients* (the density = -102 mess),
not its predictions. RF's predictive edge = non-linearity + **feature interactions**
(e.g. "alcohol helps only when volatile acidity is low"). Keep "non-linear", drop "multicollinearity".

### Q7 - scaler inside the pipeline. 10/12
My answer: scaler fit on each fold's training portion only during CV, so the validation fold
isn't influenced by the training data.
**Fix:** mechanism is right (big jump from my earlier "reproducibility" answer), but the arrow
is backwards. We stop the **validation fold from leaking INTO the scaler/training**, not the
training influencing the validation. Rule: *answer data must never flow into training.*

### Q8 - Ridge vs Lasso. 0/12 (the gap - LEARN THIS)
My answer: "I have no idea."

The fix. All three (Ridge / Lasso / ElasticNet) = linear regression + a penalty on coefficient
size. The penalty stops coefficients blowing up and tames overfitting.

| | Penalty | Effect | Zero out a feature? |
|---|---|---|---|
| Ridge (L2) | alpha x sum(coef^2) | shrinks all coefs **smoothly** toward 0 | no, rarely exactly 0 |
| Lasso (L1) | alpha x sum(\|coef\|) | pushes weak coefs to **exactly 0** | yes - feature selection |
| ElasticNet | blend (l1_ratio) | shrink + select | partly |

`alpha` = strength of the penalty (the dial GridSearchCV tuned - my best Ridge was alpha=10):
- alpha = 0 -> no penalty -> plain OLS.
- alpha huge (e.g. 10,000) -> penalty dominates -> all coefs shrink toward 0 -> predictions
  flatten toward the **mean baseline** -> underfitting (high bias).

So alpha trades fit vs simplicity, tuned by cross-validation.

Mnemonic: **L**asso = **L1** = "least absolute" -> can **zero out** (selection). Ridge = L2 =
squared -> shrinks smoothly, keeps everyone.

### Q9 - more data didn't help. 9/13
My answer: combination brought more complexity and class imbalance; model choice matters,
data size can help but quality/relevance/readiness matter too.
**Fix:** "more complexity" is the right instinct. The precise reason: red and white are
**partly different populations**, so pooling adds **heterogeneity**, not just volume - the
model fits two overlapping patterns at once, so per-type sharpness drops. Careful: *class
imbalance* is really the Q10 issue, not this one. The "model choice > raw data size" lever
conclusion was good.

### Q10 - diagnose + prescribe. 15/15
My answer: too much 5-7 data -> bias; fix with class-balancing and re-run; decision support
because quality is subjective, we give reference points not full automation; ties to
Human-in-the-Loop.
Full marks, and the HITL tie-in wasn't even asked for. (a) imbalance toward middle scores ->
model plays the safe middle bet, (b) class-balanced/stratified resampling targets it,
(c) decision support because the target is subjective and the model is weak at the extremes.

---

## The 3 things to actually lock in

1. **Leakage direction.** Answer data (test or validation) must never flow into training - not
   the model, not the scaler, not even a mean. That's why scaler goes inside the pipeline.
2. **Why RF beats linear = non-linearity + interactions.** Not multicollinearity (that's about
   the linear coefficients being unreliable, a different thing).
3. **Regularisation (Q8).** Ridge shrinks smoothly, Lasso can zero out (selection), alpha =
   penalty strength; alpha big -> underfit toward the mean. Tuned by CV.

Band: 80/100 = "solid". Next pass: drill Ridge/Lasso/alpha until Q8 is automatic.
