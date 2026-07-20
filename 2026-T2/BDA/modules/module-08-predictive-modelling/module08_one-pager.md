# BDA601 · Module 8 - One-Pager

> **Predictive modelling · linear regression · polynomial & bias-variance · logistic regression · "we're not done until we deploy"**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **One linear core - `β₀ + β₁x₁ + β₂x₂ + ...` - answers everything here. Leave it bare → predict a NUMBER (linear regression). Feed it engineered features (x², xy) → still linear, now a CURVE. Wrap it in the sigmoid → predict a PROBABILITY (logistic regression, a classifier). And none of it counts until a decision changes: "we're not done until we deploy."**
> (McCormick 2017 · Lee 2019 Ch6 + Ch7)

## 🖤 Zone 1 - Data mining, defined (McCormick) 🔴 the "so what" of the whole subject
- 🖤 **Definition:** selection & analysis of data **accumulated during the normal course of doing business**, to find & confirm **previously unknown relationships** that give **verifiable outcomes** through the **deployment** of models on **new data**.
- 🔵 Four elements, each **excludes** a neighbour: data-not-new → rules out *experiments*; previously-unknown → rules out *hypothesis testing*; verifiable & useful → rules out *EDA*; applied-to-new-data → rules out *BI reporting*.
- 🔴 **Exam point:** stats / hypothesis testing / BI / EDA each **overlap** data mining but **none has the full list**. That combination = "true data mining."
- 🔴 **Deployment = taking ACTION on a prediction** - a *different* thing from *running* the model. A model that never triggers a ticket/offer/retry is a dashboard, not a deployment.
- 🖤 Loop: `PAST data → MODEL (an "if-then-else")` · `CURRENT data → SCORE → ACTION`. Uses the term "data mining" because **CRISP-DM** does.

## 🖤 Zone 2 - Linear regression: predict a NUMBER (Lee Ch6) ⭐ SLO d) - THE GRADED CORE
- 🖤 **Four flavours:** simple (1 feature) → **multiple** (2+) → **polynomial** (curve, degree n) → polynomial-multiple.
- 🔵 **Boston workflow:** inspect → cleanse (numeric only, no nulls) → **feature-select with `df.corr()`** → 70/30 split → `.fit()` → **R²**.
  - `corr().abs().nlargest(3,'MEDV')` → **LSTAT -0.7377** (poorer area, price ↓), **RM +0.6954** (more rooms, price ↑). Ignore MEDV (corr 1.0 with itself).
  - `Y = β₀ + β₁·LSTAT + β₂·RM` = `0.384 - 0.66·LSTAT + 4.83·RM`. **R² = 0.6162.**
- 🔵 **Coefficients are interpretable, and that's the point:** +4.83 = each extra room ≈ +$4,830; -0.66 = each pt of low-status pop ≈ -$660. The model is arithmetic you can do on paper.
- 🔴 **R² = fraction of variance explained.** `0.6162` = **38% still unexplained**. Frame results this way (Dr. Chen's Module 7 language).

## 🖤 Zone 3 - Polynomial regression + the overfitting trap ⭐
- 🔵 **The key mechanical insight:** `PolynomialFeatures(degree=2)` expands `x → [1, x, x²]`, then you fit an ordinary **`LinearRegression`**. **Polynomial regression IS linear regression** - linear in the *coefficients*, fed engineered features. (2 features → `[1,x,y,x²,xy,y²]`; the **interaction term `xy` comes free**.)
- 🖤 On Boston: degree-2 lifts **R² 0.6162 → 0.7340** on the same test set. Real gain, same 2 features.
- 🔴 **The demo to remember** (6-point toy set): deg 2 → 0.9474 · deg 3 → 0.9889 · **deg 4 → R² = 1.0 and WORTHLESS**. A perfect training fit is a **red flag**, not a win = **overfitting**. (Module 7 Zone 3 in regression form.)

```text
Bias     = can't capture true shape.  straight line=HIGH bias, curvy=LOW bias
Variance = fit swings across datasets. curvy=HIGH variance, straight=LOW variance
GOAL ▶ LOW bias AND LOW variance (trade-off: push one down, other tends up)
Cures: Regularization · Bagging · Boosting (ensemble learning)
```
- 🔴 **BOOK ERRATUM:** Lee Fig 6.19 says *"aim for HIGH bias"* - **wrong by its own definitions.** A line hugging many points has **LOW** bias. **Answer "low bias, low variance" in any assessment.**

## 🖤 Zone 4 - Logistic regression: predict a PROBABILITY (Lee Ch7)
- 🔴 **Naming trap:** it's a **CLASSIFIER**, despite "regression." Output = P(input belongs to a class), always in **[0,1]**.
- 🖤 **Why a line fails on binary:** a very low-income voter gets a **negative** prediction - negative *what*? You want a **0→1 curve**, not a line.
- 🔵 **Odds → logit → sigmoid:**

| Step | Formula | Maps |
|---|---|---|
| **Odds** | `P / (1-P)` | P(win)/P(lose). fair coin=1, P=0.8→**4** |
| **Logit** | `ln(P/(1-P))` | (0,1) → (-∞, ∞) |
| **Sigmoid** | `1 / (1 + e^-L)` | (-∞, ∞) → (0,1) = **logit read backwards** |

- 🖤 `P = 1/(1 + e^-(β₀ + xβ))` - the same linear core, fed through the sigmoid. Coefficients by **MLE**, not least squares.
- 🔴 **Threshold:** sigmoid returns P(positive class). Lee & scikit-learn: **P ≤ 0.5 → negative, P > 0.5 → positive** (exactly 0.5 → negative). It's a **default, not a law** (Module 7: slide it for cost).

## 🖤 Zone 5 - Evaluation loops back to Module 7 (Breast Cancer)
- 🔴 **Encoding trap:** **0 = malignant, 1 = benign → positive class = "benign"** (opposite of clinical intuition). Misread it and every metric inverts.
- 🖤 Confusion matrix TN=48 / FN=3 / FP=5 / TP=87 → **accuracy 0.9441**, **AUC 0.99**.
- 🔴 **Imbalanced-data warning, 3rd source (Han→Chen→Lee):** 3/1000 defective, "always say no" scores **997/1000**. Accuracy lies on skewed data. *Will* be examined.
- 🔵 **Clearest ROC derivation in the subject:** threshold 0 → predict all positive → **(FPR 1, TPR 1)**; threshold 1 → predict none → **(0,0)**; 0.5 sits between. That's *why* every ROC runs (0,0)→(1,1) - forced by arithmetic. Aim for **highest AUC** (Chen's >0.8 bar).

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 2 - Visualisation & Model Development** · source code + report **1000 words ±10%** · **30%** · due **26/07/2026** · SLOs **c) d) e)**.
> This module IS A2's engine: logistic regression is the natural **probability-output baseline** to compare your churn tree against, and Ch7 hands you the full scikit-learn eval script (`classification_report`, `confusion_matrix`, `roc_curve`, `auc`) - **PySpark is now optional**. The *interpretation* carries the most marks (Dr. Chen), which is McCormick's whole point.

## 🔴 If you only memorise 5 things
1. **One linear core, three wrappers:** bare = number, engineered features = curve, sigmoid = probability.
2. **Polynomial regression is still linear regression** - linear in the coefficients.
3. **R² = 1.0 is a warning, not a trophy** → overfitting → aim **low bias + low variance** (book's "high bias" is an erratum).
4. **Logistic regression is a classifier;** threshold 0.5 is a default you're free to move for cost.
5. **"We're not done until we deploy"** - a prediction that changes no decision is worthless.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your warehouse *is* "data accumulated during the normal course of doing business." Name one relationship a model could surface in it - and the **action** (ticket, alert, retry) that would make it *deployed* rather than a dashboard.
2. In A2, `tenure` and `TotalCharges` correlate at r = 0.826. Which do you keep, and how is that the same judgement call as picking warehouse columns that actually drive a KPI?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 **Activity 1:** Boston house-price - `corr()` → `nlargest(4,'MEDV')` (4, so 3 survive after dropping MEDV) → `PolynomialFeatures(degree=2)` → 70/30 split → R² on test + forum post. **`load_boston()` is dead** (removed sklearn 1.2) - use the `lib.stat.cmu.edu` CSV workaround or `fetch_california_housing()`.
- [ ] 🔥 **Assessment 2** (due 26/07) - fold logistic regression in as the probability-output comparison model; reuse Ch7's eval code.
- [ ] 🕐 Forum post: work the **`B = 1000(Bk-0.63)²`** data-ethics paragraph into the writeup (SLO b, non-invertible parabola encoding a self-segregation assumption).
