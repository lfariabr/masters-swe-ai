# Module 8 — Logistic Regression

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Watch & summarise McCormick (2018) — logistic regression on Titanic (odds ratios, confusion matrix) | ✅ |
| **2** | Listen & summarise OCDevel/Renelle (2017) — MLG 007, LR as classification via sigmoid | ✅ |
| **3** | Watch & summarise Jedamski (2019) — the key hyperparameter is `C` | ✅ |
| **4** | Read & summarise Raschka & Mirjalili (2019) — training LR with scikit-learn (pp. 72–78) | ✅ |
| **5** | Read & summarise Brownlee (2019/2023) — LR for ML, everything you need | ✅ |
| **6** | Read & summarise Allison (2014) — measures of fit for LR (SAS 1485-2014) | ✅ |
| **7** | Read & summarise Jayaswal/Narkhede (2020) — confusion matrix, precision, recall, F1 | ✅ |
| **8** | Read & summarise Pedregosa et al. (2011) — scikit-learn `LogisticRegression` reference | ✅ |
| 9 | Activity 1: Kaggle survey — top ML algorithms/frameworks (forum) | 🕐 |
| 10 | Activity 2: LR exam pass/fail prediction (Dhiraj 2020) | 🕐 |
| 11 | Activity 3: LR purchase prediction (GeeksforGeeks 2019) | 🕐 |
| 12 | Activity 4: tuning `C` on the Iris dataset (validation curves) | 🕐 |
| 13 | Activity 5: red-wine quality classification with LR (Cortez 2009) | 🕐 |

> **One-line frame:** logistic regression is linear regression pushed through a **sigmoid** so the output is a
> **probability in (0, 1)**, then thresholded (`≥ 0.5` → positive) to give a class. Its **primary** tuning dial is **`C`**
> (inverse regularisation), though `solver`, `class_weight` and `max_iter` also matter in practice. Because it is transparent (each feature has a signed coefficient / odds ratio), it is
> the natural **baseline classifier** and directly relevant to the Assessment 2 wine classification.

---

## Key Highlights

### 1. McCormick, K. (2018). Logistic Regression [Video].

**Citation:** McCormick, K. (2018, 20 August). *Logistic regression* [Video file]. LinkedIn Learning — Machine Learning & AI Foundations: Classification Modeling.

**Purpose:** A statistician's walkthrough of logistic regression on the Titanic data — the S-curve intuition, how to *read* the coefficient table, and why a good technique can still under-perform on a given dataset.

---

#### 1. Why not just linear regression?
- Fitting a plain line to a 0/1 target (survived/died) produces **impossible predictions** — probabilities below 0 and above 1, and a line that fits the cloud badly.
- Logistic regression applies a **log transform** that bounds predictions between **asymptotes at 0 and 1** — the **S-curve**.
- **Popcorn metaphor:** the curve is flat, then pops steeply through a threshold, then flattens. On the Titanic males, age barely matters at 4-6 years old, then changes sharply in the late teens — that steep middle is what the sigmoid is trying to locate.

#### 2. The formula (same core, wrapped in math)
- Linear core is unchanged: `z = β₀ + β₁x₁ + β₂x₂ + …` (intercept = "the constant").
- To score, you **reverse the log transform** with the antilog (`EXP`): `p = 1 / (1 + e^(−z))`.
- **Dummy coding** is required for categoricals — that is why passenger class and port-embarked each expand into several variables.

#### 3. Reading the coefficient table (the part statisticians love)
| Column | Meaning |
|---|---|
| **B (unstandardised beta)** | plug straight into the `z` formula |
| **Sig / p-value** | is the variable statistically significant? **low = significant.** Age, class, sex significant; *embarked was not* (p = 0.064 > 0.05) |
| **Exp(B) = odds ratio** | the antilog of beta — the headline number reported in the news |

- **Odds ratios read out loud:** sex ≈ **13.8** (women ~14× more likely to survive than men); first class ≈ **10.5×** more likely than third (the reference group); age just **under 1** (older = less likely, and a 10-year gap compounds to ~a third less likely).

#### 4. When a strong technique performs poorly
- Training accuracy 65%, **test accuracy 55% — a 10-point gap** = a warning sign, not a reason to abandon logistic regression.
- Diagnose before you dismiss: drop the non-significant `embarked` block, or add a missing variable. **The technique is fine; the *specification* needs work.**

#### Key Takeaways for MLN601
1. This is the **classification twin** of the Module 3 linear-regression story — same `β₀ + βᵢxᵢ` core, wrapped in a sigmoid.
2. **Odds ratios (Exp β)** are the explainability payoff, and tie straight into the Module 7 XAI theme — logistic regression is *intrinsically* interpretable.
3. A train/test gap is a **possible overfitting** signal (it can also come from sampling variance, leakage, or distribution shift) — confirm with **cross-validation** before concluding overfitting and reaching for `C`. See resources 3, 4, 8.

---

### 2. OCDevel / Renelle, T. (2017). MLG 007: Logistic Regression [Podcast].

**Citation:** Renelle, T. (2017, 19 February). *Episode #007: Logistic regression* [Audio podcast]. Machine Learning Guide (ocdevel.com/mlg/7).

**Purpose:** Positions logistic regression against linear regression and lays out the predict → evaluate error → train loop in plain language, with no diagrams needed.

---

#### 1. Classification vs regression
- Supervised learning splits into **regression** (continuous values) and **classification** (assign a class). Despite the name, **logistic regression is a classification algorithm**.
- It outputs the **probability an input belongs to a class** (a number in [0, 1]), then thresholds: `≥ 0.5` → positive class, `< 0.5` → negative (sklearn's `predict` assigns exactly `0.5` to the positive class).
- **Multiclass:** assign a probability per class and take `argmax`.

#### 2. The three-step loop
| Step | What happens |
|---|---|
| **Predict** | run inputs through the linear core, then the **sigmoid** `1 / (1 + e^(−θᵀx))` |
| **Evaluate error** | measure inaccuracy with the **negative log-likelihood (log-loss)** cost — log-likelihood is *maximised*, so its negative is what gradient descent *minimises*; penalises confident-and-wrong more harshly |
| **Train** | update parameters `θ` with **gradient descent**, nudging by the derivative of the cost |

#### 3. Composability — the bridge to neural nets
- ML architectures are **compositional**: logistic regression is *a function (sigmoid) of another function (linear regression)*.
- This is exactly a **single neuron**: a linear combination fed through a non-linear activation. Understanding LR is the foundation for deep learning.
- **Softmax** generalises the sigmoid when outputs must form a proper probability distribution (sum to 1) — flagged but out of scope here.

#### Key Takeaways for MLN601
1. Reinforces the sigmoid + threshold mental model from resource 1, without the statistics table.
2. The **log-loss / gradient-descent** loop is the same optimisation machinery you saw in linear regression — only the cost function changes.
3. "LR = one neuron" is the single most useful sentence to carry forward into the AI-core subjects.

---

### 3. Jedamski, D. (2019). Key Hyperparameters to Consider [Video].

**Citation:** Jedamski, D. (2019, 15 May). *What are the key hyperparameters to consider?* [Video file]. LinkedIn Learning — Applied Machine Learning Algorithms.

**Purpose:** The practical bridge from theory to code — `C` is the **primary** focus of LR tuning (though not the only parameter with practical impact — see `solver`, `class_weight`, `max_iter`, `l1_ratio` in resources 4 & 8), and this explains what it does.

---

#### 1. Import, inspect, and the golden rule
- `from sklearn.linear_model import LogisticRegression`; printing the object shows every default.
- **Golden rule:** *never tune all hyperparameters.* Tune the few with the largest impact; leave the rest on defaults.
- Every sklearn estimator exposes **`.fit(X_train, y_train)`** and **`.predict(X_test)`** — pass training features + labels to fit, test features to predict.

#### 2. `C` — the primary dial to tune
- `C` is a **regularisation parameter that controls how closely the model fits the training data**; regularisation combats **overfitting** by discouraging overly complex models.
- **Counter-intuitive:** `C = 1/λ` (the inverse of the true regularisation strength λ). So:

| `C` | Regularisation | Model complexity | Risk |
|---|---|---|---|
| **high** `C` (e.g. 100) | **low** (λ→0) | more complex | **overfit** |
| **low** `C` | **high** (λ large) | simpler | **underfit** |

- Default is `C = 1`.

#### 3. What it looks like on Iris
- On the 3-class Iris petal plot: `C = 100` cleanly separates the three groups; as `C` shrinks, the boundary degrades until the smallest `C` just splits the plot in half.
- **The default (`C=1`) is not always best** — here `C=100` wins. That is the whole justification for **hyperparameter tuning** (directly sets up Activity 4).

#### Key Takeaways for MLN601
1. This is the **actionable core** of the module: when you `GridSearchCV` a logistic regression, the grid is essentially `{'C': [...]}`.
2. The `C = 1/λ` inversion is the single most common exam/interview trap — **smaller `C` = stronger regularisation**.
3. Ties straight into **Assessment 2**: the Module 7 lecture named `GridSearchCV(cv=5)` as a grade lever, and for LR the parameter you tune is `C`.

---

### 4. Raschka, S. & Mirjalili, V. (2019). Training a Logistic Regression Model with scikit-learn.

**Citation:** Raschka, S. & Mirjalili, V. (2019). *Python Machine Learning* (3rd ed., pp. 72–78). Packt. [Ch. 3, "A Tour of ML Classifiers Using scikit-learn"]

**Purpose:** The canonical code recipe — fit, predict, `predict_proba`, and the regularisation/`C` story with the actual math behind it.

---

#### 1. The scikit-learn recipe
```python
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C=100.0, random_state=1, solver='lbfgs')  # multinomial by default
lr.fit(X_train_std, y_train)      # fit on STANDARDISED features
lr.predict_proba(X_test_std[:3])  # class-membership probabilities (rows sum to 1)
lr.predict(X_test_std[:3])        # crisp labels (argmax of the probabilities)
```
- **`predict_proba`** returns per-class probabilities; **`predict`** is just the `argmax`.
- Single-row prediction needs a 2-D array: `lr.predict(X[0].reshape(1, -1))`.
- **Note (version drift):** Raschka's book passes `multi_class='ovr'`, but that argument was **deprecated in sklearn 1.5 and removed in 1.8** — modern LR is multinomial by default. For explicit one-vs-rest, wrap the estimator: `OneVsRestClassifier(LogisticRegression(...))`.

#### 2. Solvers
- Convex loss, so most solvers converge easily. Options: **`newton-cg`, `lbfgs`, `liblinear`, `sag`, `saga`**.
- **`lbfgs`** (limited-memory BFGS) is the modern default and handles multinomial; **`liblinear`** is OvR-only.

#### 3. Regularisation, `C`, and the bias-variance tradeoff
- **L2 regularisation** adds `(λ/2)‖w‖²` to the cost, shrinking weights to penalise extreme values — handles collinearity, filters noise, prevents overfitting.
- **`C = 1/λ`** (convention borrowed from SVMs). **Decreasing `C` → stronger regularisation → smaller weight coefficients** (demonstrated with the L2 regularisation-path plot).
- **Feature scaling is strongly recommended** — LR still fits unscaled inputs, but regularisation only behaves well when features share a scale, and the `sag`/`saga` solvers need it to converge. Standardise first.
- **Bias-variance:** high variance ∝ overfitting (sensitive to training randomness); high bias ∝ underfitting (systematic error). Tuning `C` finds the sweet spot.

#### Key Takeaways for MLN601
1. This is the **copy-paste template** for the wine classifier — `fit → predict_proba → predict`, on standardised features.
2. Confirms resource 3's `C = 1/λ` story with the actual L2 penalty term — read the two together.
3. **`random_state=1`** = the reproducibility discipline the CLAUDE.md ML guidelines require (fixed seeds).

---

### 5. Brownlee, J. (2019, updated 2023). Logistic Regression for Machine Learning.

**Citation:** Brownlee, J. (2023, updated). *Logistic regression for machine learning* [Web log post]. MachineLearningMastery.com.

**Purpose:** The single most complete plain-English reference — the logistic function, the log-odds representation, MLE, making predictions by hand, data-prep assumptions, and the imbalance problem that dominates Assessment 2.

---

#### 1. The logistic function and representation
- **Sigmoid:** `1 / (1 + e^(−value))` — S-shaped, maps any real number into (0, 1), originally from population-growth ecology.
- Representation is stored as **coefficients** (β / b's), just like linear regression: `y = e^(b₀+b₁x) / (1 + e^(b₀+b₁x))`.

#### 2. Log-odds — the interpretable trick
- Rearranged: **`ln(p / (1−p)) = b₀ + b₁x`**, i.e. **`ln(odds) = linear combination`**.
- The left side is the **log-odds / logit / probit**. Odds = `p/(1−p)` (e.g. p=0.8 → odds 4). This is why LR is interpretable: each coefficient is a signed effect on the log-odds.

#### 3. Learning + a worked prediction
- Coefficients are learned by **Maximum-Likelihood Estimation (MLE)** — search for β's that push predictions toward 1 for the default class and 0 for the other. Modern optimisers: **L-BFGS, ADAM**; from scratch: gradient descent.
- **By hand:** with `b₀=−100, b₁=0.6`, height 150 → `p ≈ 0.0000454` → snap to class 0 (`< 0.5`).

#### 4. Data prep + the imbalance problem (**Assessment 2 critical**)
- **Assumptions:** binary output, remove noise/outliers, roughly linear log-odds relationship, remove highly-correlated inputs, watch for non-convergence.
- **The major problem — skewed classes:** LR **favours the majority class**. On a 3%-prevalence disease, predicting "all normal" scores **97% accuracy while catching zero cases**. Accuracy is the wrong metric; recall on the minority collapses.
- LR is prominent in **XAI** (clear parameter interpretation) and **federated / low-resource** settings (lightweight).

#### Key Takeaways for MLN601
1. The **imbalance trap** is the whole reason the Module 7 lecture named **SMOTE** as a distinction-band lever — the wine "bad" class is the minority.
2. **Accuracy ≠ good model** on imbalanced data — hand off directly to resource 7 (precision/recall/F1).
3. Log-odds = the intrinsic explainability that connects this module back to Module 7's XAI.

---

### 6. Allison, P. D. (2014). Measures of Fit for Logistic Regression.

**Citation:** Allison, P. D. (2014). *Measures of fit for logistic regression* (Paper 1485-2014). SAS Global Forum, Statistical Horizons LLC & University of Pennsylvania.

**Purpose:** The statistician's caution — "does my model fit?" has **two different answers**, and the popular tests each have traps. Deepens the evaluation section beyond accuracy.

---

#### 1. Two questions that are NOT the same
| Approach | Statistic | Reads |
|---|---|---|
| **Predictive power** | R²-type, ROC AUC, rank correlations | 0 → 1, **higher = better** |
| **Goodness-of-fit** | deviance, Pearson χ², Hosmer-Lemeshow | p-value; **p < 0.05 → reject the model** |
- **Crucial:** a high R² model can *fail* goodness-of-fit, and a low R² model can *pass* it. GOF tests whether you could do better by adding non-linearities/interactions — not how well you predict.

#### 2. Which pseudo-R²?
- **McFadden's R²** = `1 − ln(Lₘ)/ln(L₀)` — Allison now prefers it over Cox-Snell.
- **Cox-Snell R²** — generalises to other ML models, but its **upper bound is < 1** (max ~0.75 at p=0.5, only ~0.48 at p=0.9), which is unsettling. Nagelkerke rescales it to cap at 1, but the correction is ad hoc.
- **Tjur's R² (coefficient of discrimination)** — Allison's favourite: for each class, average the predicted probabilities, take the **absolute difference of the two means**. Upper bound is a true 1.0, intuitive, model-agnostic (can compare LR vs trees).

#### 3. Goodness-of-fit caveats
- Deviance & Pearson χ² work when data aggregates into **profiles** (rows with identical predictor values); low χ²/df with high p = good.
- The popular **Hosmer-Lemeshow test has serious problems** (arbitrary grouping) — Allison steers toward alternatives.

#### Key Takeaways for MLN601
1. For the wine classifier, report **more than accuracy** — a pseudo-R² *plus* the confusion-matrix metrics is the "explain your model" rigour the Module 7 lecturer wants.
2. **Tjur's R²** is a genuinely quotable, easy-to-compute discrimination measure that almost nobody in the cohort will use.
3. Reinforces the theme: **fit ≠ predictive power** — two separate questions, keep them separate in the write-up.

---

### 7. Jayaswal, V. / Narkhede, S. (2020). Understanding the Confusion Matrix (Precision, Recall, F1).

**Citation:** Narkhede, S. (2018) / Jayaswal, V. (2020, 14 September). *Performance metrics: Confusion matrix, precision, recall, and F1 score.* Towards Data Science.

**Purpose:** The metrics that replace accuracy when classes are imbalanced — exactly the evaluation toolkit Assessment 2 needs.

---

#### 1. The confusion matrix (2×2, binary)
| | Predicted + | Predicted − |
|---|---|---|
| **Actual +** | **TP** | **FN** (Type II error) |
| **Actual −** | **FP** (Type I error) | **TN** |
- Tumour example (100 people): TP=10, TN=60, FP=22, FN=8. Even with imbalance, a good model wants **TPR/TNR high, FPR/FNR low**.

#### 2. Precision vs recall — and when each dominates
- **Precision** = `TP / (TP + FP)` — of everything flagged positive, how much truly is. (Uses TP and FP only; `FN` drives recall, not precision. Both ignore TN, which is why they suit retrieval / imbalance.)
- **Recall (TPR)** = `TP / (TP + FN)` — of all actual positives, how many caught.
- **Fraud / medical diagnosis → maximise recall** (missing a positive is catastrophic; tolerate low precision).
- **Spam filtering → maximise precision** (a real email lost to the spam folder is worse than a spam that slips through).

#### 3. F1 score
- **F1 = harmonic mean of precision and recall** = `2·(P·R)/(P+R)` — one number balancing both, robust on imbalanced data.
- **Fβ** weights recall β× more than precision (β=2 → recall twice as important).

#### Key Takeaways for MLN601
1. This is the **direct answer** to resource 5's imbalance problem — the metrics you report *instead of* accuracy.
2. For the **Assessment 2 wine target** (positive class = **bad** wine, the minority) you must decide precision vs recall consciously and justify it — recall on "bad" wine is the sharp end.
3. `classification_report` in sklearn prints precision/recall/F1 per class in one call — pair it with the confusion matrix in the notebook.

---

### 8. Pedregosa et al. (2011). scikit-learn `LogisticRegression` Reference.

**Citation:** Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR, 12*, 2825–2830. [`sklearn.linear_model.LogisticRegression` documentation, v1.9.0]

**Purpose:** The API reference — the exact parameters, solver/penalty compatibility, and the class-imbalance switch you will actually type.

---

#### 1. The signature that matters
`LogisticRegression(C=1.0, solver='lbfgs', max_iter=100, class_weight=None, random_state=None, l1_ratio=0.0, …)` — **regularisation is applied by default.**

| Parameter | Role |
|---|---|
| **`C`** | inverse regularisation strength; **smaller = stronger** regularisation; `C=np.inf` = unpenalised |
| **`solver`** | optimiser (see below) |
| **`class_weight='balanced'`** | auto-reweight inversely to class frequency — the **built-in imbalance fix** (`n_samples / (n_classes · bincount(y))`) |
| **`max_iter`** | raise from 100 if the solver fails to converge |
| **`random_state`** | reproducibility (fixed seed) |
| **`l1_ratio`** | 0 = pure L2, 1 = pure L1, between = elastic-net (note: `penalty` arg deprecated from v1.8) |

#### 2. Solver ↔ penalty compatibility
- **`lbfgs`, `newton-cg`, `newton-cholesky`, `sag`** → **L2 or none only**.
- **`liblinear`** → L1 or L2 (not both); **binary-only** for multiclass (needs `OneVsRestClassifier`).
- **`saga`** → the only solver supporting **elastic-net** (L1+L2).
- Multiclass (`n_classes ≥ 3`): all solvers except `liblinear` optimise the multinomial loss.

#### 3. Practical notes
- `class_weight='balanced'` is a **lighter-weight alternative to SMOTE** for imbalance — worth comparing both in Assessment 2.
- Use standardised, C-ordered float arrays for performance.

#### Key Takeaways for MLN601
1. `class_weight='balanced'` and **SMOTE** are two levers for the same problem — compare them and explain the choice (that comparison *is* the distinction-level rationale).
2. If your LR throws a **convergence warning**, the fix is usually `max_iter=1000` and/or scaling features — a common notebook gotcha.
3. The solver/penalty table decides *which* regularisation you can even use — `saga` if you want elastic-net, `lbfgs` for plain L2.

---

## Synthesis — how the eight fit together

```
                 THEORY                          PRACTICE                     EVALUATION
  sigmoid + log-odds (R2,5)  →  fit/predict/predict_proba (R4,8)  →  confusion matrix, P/R/F1 (R7)
  odds ratios / interpret (R1)     the one dial: C = 1/λ (R3,4,8)      pseudo-R² & GOF, Tjur (R6)
  LR = one neuron (R2)             imbalance: SMOTE / class_weight (R5,8)
```

**The through-line to Assessment 2:** logistic regression is the interpretable **baseline** for the wine
classification. Tune **`C`** with `GridSearchCV(cv=5)`, fix the **class imbalance** (SMOTE *or*
`class_weight='balanced'` — compare them), and report **precision / recall / F1** on the minority "bad" class,
not accuracy. Every one of those moves is a lever the Module 7 lecture named for the distinction band.
