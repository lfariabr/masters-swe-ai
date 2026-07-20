# MLN601 · Module 8 - One-Pager

> **Logistic Regression · sigmoid & log-odds · the `C` dial · imbalance · precision/recall/F1**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Logistic regression = linear regression pushed through a sigmoid, so the output is a probability in (0, 1), then thresholded (`≥ 0.5` → positive) to give a class. It is a *classification* algorithm despite the name.**
> (Brownlee 2019 · Raschka & Mirjalili 2019, ch.3)

---

## 🖤 Zone 1 - From line to S-curve
- 🖤 **Linear core, unchanged:** `z = β₀ + β₁x₁ + β₂x₂ + …`
- 🖤 **Sigmoid wraps it:** `p = 1 / (1 + e^(−z))` → bounds output between asymptotes at **0 and 1** (a plain line gives impossible p<0 or p>1).
- 🔵 **Log-odds / logit** is the interpretable trick - the sigmoid rearranges to a *linear* equation:

  ```
  ln( p / (1−p) ) = β₀ + βᵢxᵢ        ← "ln(odds) = linear combination"
  odds = p/(1−p)   (p=0.8 → odds 4)
  ```
- 🔵 **Exp(β) = odds ratio** - the headline number. Titanic: sex ≈ **13.8** (women ~14× more likely to survive), 1st class ≈ **10.5×** vs 3rd (reference group).
- 🔴 Odds ratios = the **explainability payoff** → ties straight back to **Module 7 XAI**. LR is *intrinsically interpretable*.

## 🖤 Zone 2 - How it learns
- 🖤 **Three-step loop:** **predict** (sigmoid) → **evaluate error** (log-loss) → **train** (gradient descent), repeat.
- 🔵 **Cost = negative log-likelihood (log-loss).** Log-likelihood is *maximised*, so its *negative* is what gradient descent *minimises*. Punishes confident-and-wrong hardest.
- 🔵 **Coefficients learned by MLE** (Maximum-Likelihood Estimation). In practice: L-BFGS / ADAM; from scratch: gradient descent.
- 🔴 **"LR = one neuron"** - a linear combo through a non-linear activation. The single most useful sentence to carry into the neural-net / deep-learning subjects.

## 🖤 Zone 3 - Two dials: `C` and `penalty` ⭐ SLO c) - THE GRADED CORE
- 🔴 **Lecturer (wk 8): tune `penalty` AND `C`, nothing else.** `penalty` = L1 / L2 (default L2); `C` ∈ `{0.2, 0.5, 0.8, 1.0}`. He expects no other hyperparameter to move your result. *(L1 needs `liblinear`/`saga`; `lbfgs` is L2-only. `penalty` deprecated in sklearn 1.8 → use `l1_ratio`: 0=L2, 1=L1.)*
- 🖤 **`C = 1 / λ`** (inverse regularisation). The *counter-intuitive* exam trap:

  | `C` | Regularisation | Complexity | Risk |
  |---|---|---|---|
  | **high** `C` (e.g. 100) | **low** (λ→0) | more complex | **overfit** |
  | **low** `C` | **high** (λ large) | simpler | **underfit** |

- 🔵 Default `C=1`; on Iris `C=100` separates the 3 petal groups cleanly → *that gap is why you tune.*
- 🔵 **Scale features first** - regularisation only behaves when features share a scale (`sag`/`saga` need it to converge). `StandardScaler` before fit.
- 🔴 **Golden rule:** never tune all hyperparameters - tune the few with impact. For LR the grid is essentially `{'C': [...]}` via `GridSearchCV(cv=5)`. (Also real in practice: `solver`, `class_weight`, `max_iter`, `l1_ratio`.)

## 🖤 Zone 4 - The scikit-learn recipe
```python
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C=100.0, random_state=1, solver='lbfgs')  # multinomial by default
lr.fit(X_train_std, y_train)       # fit on STANDARDISED features
lr.predict_proba(X_test_std[:3])   # per-class probabilities (rows sum to 1)
lr.predict(X_test_std[:3])         # crisp labels = argmax of the probabilities
```
- 🔵 **`predict_proba`** = probabilities; **`predict`** = argmax of them.
- 🔴 **Version drift:** `multi_class='ovr'` was **deprecated in sklearn 1.5, removed in 1.8** - modern LR is multinomial by default; for explicit OvR wrap in `OneVsRestClassifier(...)`.
- 🔴 **Convergence warning?** → `max_iter=1000` and/or scale features.

## 🖤 Zone 5 - Evaluation: go BEYOND accuracy ⭐ SLO c) / d)
- 🖤 **Imbalance is LR's Achilles heel** - it favours the majority class. A 3%-prevalence disease scores **97% accuracy while catching ZERO cases**. Accuracy lies.
- 🔵 **Confusion matrix (2×2):** TP · FN (Type II) · FP (Type I) · TN.
- 🔵 **Precision = `TP/(TP+FP)`** (of flagged-positive, how many real - FP hurts). **Recall = `TP/(TP+FN)`** (of actual positives, how many caught - FN hurts). **F1 = `2·P·R/(P+R)`** (harmonic mean).
- 🔵 Fraud/medical → maximise **recall**; spam → maximise **precision**.
- 🔴 **Two imbalance fixes:** `class_weight='balanced'` (built-in, light) **vs SMOTE** (resample) - *compare both & justify* = distinction-band move.
- 🔴 **Fit ≠ predictive power** (Allison): report a pseudo-R² too - **Tjur's R²** (abs. diff of the two class mean-probabilities) is easy, capped at 1, and almost nobody in the cohort uses it.

## 🖤 Zone 6 - Sigmoid vs softmax + limits (⭐ live class exercise, wk 8)
| | **Sigmoid** | **Softmax** |
|---|---|---|
| Use for | **binary** (2 outcomes) | **multi-class** (3+ outcomes) |
| Output | one number in (0,1) = a probability | distribution over classes, **sums to 1** |
| Examples | COVID/not · rainy/not · low/high wine | rainy/windy/cloudy/sunny · cat/dog/bird |

- 🔵 **Binomial LR** = 2 categories · **Multinomial LR** = 3+ **unordered** categories (grades HD/D/C/P are *ordered*; weather is not).
- 🔴 **His trap:** share price **up or down** → sigmoid. Share **price itself** → *neither* - that's continuous = **regression**.
- 🔵 **Assumptions:** observations independent · dependent variable binary.
- 🔴 **Limitations:** assumes a **linear decision boundary** (struggles with non-linear data) · **sensitive to outliers** · overfits with many features + few rows · **can't handle missing values** (impute first).
- 🔴 **"There is no best model."** Valid comparisons need the *same dataset and split*. You may *assume* LR will struggle on non-linear data - you can't *guarantee* it. Hence: implement 5+ models and compare in a table.

---

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 2 - Classification (40%)** · notebook + mark-up + source code + 7-10 min presentation + **1500 words** (±10%) · due **26 Jul 2026** · SLOs **b) c) d)**.
> This module *is* the assessment engine: build the **LR baseline** on the red-wine data, **tune `C`** with `GridSearchCV(cv=5)`, fix the **imbalance** (positive class = "bad" wine = minority) with SMOTE *or* `class_weight='balanced'`, and **report precision/recall/F1** on the minority class - never accuracy alone.

## 🔴 If you only memorise 5 things
1. **Sigmoid over a linear core** → probability → threshold `≥0.5` → class. `ln(p/(1−p)) = β₀+βᵢxᵢ`.
2. **`C = 1/λ`**: smaller `C` = **stronger** regularisation = simpler model. (The classic trap.) Tune it with **`penalty`** (L1/L2) - the lecturer's only two dials.
3. **Scale features, fixed seed, `GridSearchCV`** the `C` - the reproducible tuning drill.
4. **Accuracy lies on imbalanced data** → confusion matrix + **precision / recall / F1**; pick precision-vs-recall consciously.
5. **Sigmoid = binary, softmax = multi-class.** Plus LR's limits: linear boundary, outlier-sensitive, no missing values.

*(Runners-up: **Exp(β) = odds ratio** = the interpretability payoff · imbalance levers `class_weight='balanced'` vs **SMOTE** - compare & justify.)*

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your warehouse data is skewed too (most orders "normal", few "flagged/returned"). If you built an LR to flag the rare bad orders, why would raw **accuracy** make a useless model look great - and which metric would your ops team actually care about?
2. An **odds ratio of 13.8** on "supplier X" would let you tell a non-technical manager "orders from X are ~14× more likely to be returned." Which of your DB columns would you *dummy-code* to get clean, quotable odds ratios like that?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 Activity 1: Kaggle survey - top ML algorithms/frameworks (discussion forum post)
- [ ] 🕐 Activity 2: LR exam pass/fail prediction (Dhiraj 2020) - run defaults, comment notebook, post
- [ ] 🕐 Activity 3: LR purchase prediction (GeeksforGeeks 2019) - read confusion matrix
- [ ] 🕐 Activity 4: tune `C` on Iris (validation curves)
- [ ] 🔥 Activity 5: red-wine quality classification with LR (Cortez 2009) → feeds Assessment 2
