# MLN601 · Module 3 - One-Pager

> **Supervised Learning · Linear Regression · Least Squares · scikit-learn · Estimator Map**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4.

**Pen legend:** 🖤 Black = core facts / skeleton · 🔵 Blue = examples & connections · 🔴 Red = traps & assessment hooks

---

## 🖤 The Big Idea (box it, top of page)
> **Supervised learning = learn a model from LABELLED data to predict on unseen data.** It splits two ways:
> **Classification** (discrete labels) · **Regression** (continuous number). 🔵 *This module = the regression branch.*
> **Linear regression** = fit a straight line `ŷ = b₀ + b₁x` through the data.

## 🖤 The Core Equation (write big, centre-left)
```
ŷ = b₀ + b₁x          b₀ = intercept (y when x=0)
                       b₁ = slope (Δy per +1 x)
```
🔵 Multivariate: `ŷ = b₀ + b₁x₁ + b₂x₂ + …` → a plane/surface, not a line.
🔴 *b₀, b₁ are PARAMETERS = learned from data. Don't confuse with hyperparameters.*

## 🖤 How the line is chosen → Least Squares (the heart of it)
```
residual eᵢ = yᵢ − ŷᵢ        (vertical gap: actual − predicted)
minimise  SSE = Σ(yᵢ − ŷᵢ)²   (sum of SQUARED residuals = OLS)
```
🔵 Square the errors so +/− don't cancel **and** big misses hurt more.
🔵 **Correlation (r)** is the intuition behind the slope: strong r → steep, confident line (−1 … +1).
🔴 *r only sees the LINEAR part — a curve looks "weak" to r. And r ≠ causation.*

## 🖤 3 Types of Learning (Raschka Ch.1 — quick spine)
| Type | Labels? | Goal |
|---|---|---|
| **Supervised** ⭐ | ✅ yes | predict label/value |
| Unsupervised | ❌ no | find structure (clustering, dim-reduction) |
| Reinforcement | reward | actions that maximise reward (background) |

🔵 *Galton 1886 coined "regression" → children's heights regress toward the mean.*

## 🖤 The sklearn Workflow (write as a code ladder)
```
train_test_split(X, y, test_size=0.2, random_state=42)
LinearRegression().fit(X_train, y_train)   → .coef_  .intercept_
            .predict(X_test)
evaluate:   r2_score / RMSE
```
🔵 Same `fit() / predict() / score()` shape as every sklearn model (Module 1).
🔴 *Always set `random_state` → reproducible split.*

## 🖤 Choosing the Right Estimator (the map → regression path)
```
>50 samples? → labelled? → predicting a QUANTITY? → REGRESSION
   <100K samples → LinearRegression → Ridge / Lasso / ElasticNet
   >100K samples → SGD Regressor          (try SVR if non-linear)
```
🔵 **Ridge** = shrink all coefs · **Lasso** = some coefs → 0 (feature select) · **ElasticNet** = both.
🔵 "Try next" arrows = **No Free Lunch theorem** made practical → compare a handful.

## 🔴 Pitfalls (red box - these are marks-losers)
- **Data leakage** → fit scaling/preprocessing on **TRAIN ONLY**, reapply to test. *"Test score looks too good" = suspect leakage* (Raschka says this outright).
- **No `random_state`** → results not reproducible.
- **Judge on a chart, not a metric** → always report **R² / RMSE** on the held-out test set.
- **Overfitting** → train great, test poor → regularise (Ridge/Lasso) or simplify.
- **r ≠ causation**, and linearity is an assumption — check residuals.

## 🔵 Module 3 in practice (your two activities)
- **Activity 1** = Boston Housing (The Semicolon) → load, fit, predict house prices, read the error.
- **Activity 2** = Valkov house prices → build it, then extend to **multivariate** regression.

## 🔴 Assessment Hook (bottom red strip)
**A1 = Regression Analysis, due 28 Jun (20%).** Module 3 gives you the *actual algorithm*. Marks live in:
1. Clean **target + features**  2. Honest **train/test split** (`random_state`)  3. `LinearRegression().fit()` → **predict**  4. Report **R²/RMSE** (not just charts)  5. Discuss **overfitting + Ridge/Lasso** and limits. 🔵 *Hang it on the CRISP-DM spine from Module 2.*

---

### Margin prompts (answer in blue while you write)
1. In *your* data (Review Pulse / ClinicTrends), what's one continuous target you could predict, and its top 2 features?
2. Where could **leakage** sneak in — a feature that secretly contains the answer (cf. vgsales R²=0.9999)?
