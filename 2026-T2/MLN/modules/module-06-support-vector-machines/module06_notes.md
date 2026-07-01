# Module 6 - Support Vector Machines

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Watch & summarise Jedamski (2019) - When should you consider using SVM? | ✅ |
| 2 | Watch & summarise Aharoni (2007) - Kernel trick visualisation (YouTube) | 🔥 needs manual watch |
| 3 | Listen & summarise Kennedy, Jaffe & Malone (2017a) - Maximal margin classifiers podcast | 🔥 needs manual listen |
| 4 | Listen & summarise Kennedy, Jaffe & Malone (2017b) - Kernel trick & SVM podcast | 🔥 needs manual listen |
| **5** | Read & summarise Brownlee (2020) - Support vector machines for machine learning | ✅ |
| **6** | Read & summarise scikit-learn (2011) - SVM documentation | ✅ |
| **7** | Read & summarise scikit-learn (2011) - Metrics & the confusion matrix | ✅ |
| 8 | Read & summarise Ozer, Sarica & Arga (2020) - SVM in breast cancer (paywalled) | 🔥 needs manual access |
| 9 | Activity 1: Kernel trick using spreadsheet (Malakar 2016) | 🕐 |
| 10 | Activity 2: Classify muffin vs cupcake recipes with SVM | 🕐 |
| 11 | Activity 3: Breast cancer classification with SVM | 🕐 |
| 12 | Activity 4: Face recognition with SVM on LFW | 🕐 |
| 13 | Activity 5: Wine classification with SVM | 🕐 |

**Activity notebooks (this folder):**
- `MLN601_Module06_Kernel_Trick_for_SVM_Malakar-2016.xlsx` (Activity 1)
- `MLN601_Module06_Classification_of_Muffin_and_Cupcake_Recipes_using_SVM.ipynb` (Activity 2)
- `MLN601_Module06_Breast_Cancer_Classification_Using_SVM.ipynb` (Activity 3)
- `MLN601_Module06_SVM_Face_Recognition_using_LFW.ipynb` (Activity 4)
- `MLN601_Module06_Wine_Classification_and_SVM.ipynb` (Activity 5)

---

## Key Highlights

### 1. When Should You Consider Using SVM? (Jedamski 2019)

**Citation:** Jedamski, D. (2019, 15 May). *When should you consider using SVM?* [Video file]. LinkedIn Learning - Applied Machine Learning Algorithms.
**Local source:** `r1_When-Should-You-Use-SVM_transcript.txt`

**Purpose:** A practical decision guide - not the maths, but *when* an SVM is the right tool and when it is the wrong one. These are guidelines, not hard rules; feel for the trade-offs comes with practice.

---

#### 1. When SVM shines
- **Classification, not regression.** SVM can technically do continuous outputs, but the instructor finds it weak for regression. Reach for it on **binary classification** problems.
- **"Short and fat" data - high feature-to-row ratio.** Lots of features, relatively few rows. Many algorithms choke here; SVM is a *distinguishing* performer. (This directly echoes the scikit note: *"still effective in cases where number of dimensions is greater than the number of samples"* - see [resource 6](#6-scikit-learn-support-vector-machines-documentation).)
- **Complex, tangled relationships.** More capable than logistic regression at untangling non-linear structure (via the [kernel trick](#3-kernels-and-the-kernel-trick)).
- **Outlier-heavy data.** Because the boundary is defined only by the **support vectors** (points nearest the margin), far-away outliers are effectively ignored - unlike most algorithms.

#### 2. When to avoid SVM

| Situation | Why avoid |
|---|---|
| Many rows, few features ("tall, thin" data) | Slow to train, payoff not worth it vs. simpler algorithms |
| You need transparency / feature significance | The hyperplane in high-dimensional space is a black box - no clear picture of predictor importance |
| You want a quick benchmark model | SVM is slow both to **train** and to **predict** |
| Limited time or compute | Training cost is high; other models get you there faster |

#### Key Takeaways for MLN601
1. This is the "why/when" companion to the mechanics in resources 5-6. It frames every activity: the **breast cancer** ([Activity 3](#task-list)) and **face recognition** ([Activity 4](#task-list)) cases are exactly the high-dimensional, complex-boundary problems SVM is built for.
2. The outlier-robustness point comes straight from *how* SVM works - only support vectors matter. Keep this in mind when comparing SVM to the decision trees / Naive Bayes of Modules 4-5.
3. Day-job link: in a warehouse/DB setting, SVM fits **wide, low-volume** problems (e.g. classifying a SKU from hundreds of engineered attributes) far better than a high-throughput streaming decision.

---

### 5. Support Vector Machines for Machine Learning (Brownlee 2020)

**Citation:** Brownlee, J. (2020, 15 August). *Support vector machines for machine learning.* Machine Learning Mastery.
**Local source:** `r5_Support-Vector-Machines-for-ML_MachineLearningMastery.pdf`

**Purpose:** A low-maths, developer-friendly walkthrough of what an SVM actually stores and how it predicts - the conceptual bridge before the scikit reference. Read this before [resource 6](#6-scikit-learn-support-vector-machines-documentation).

---

#### 1. Maximal-Margin Classifier (the hypothetical ideal)
- Numeric inputs form an **n-dimensional space**; a **hyperplane** is the line/plane that splits it by class.
- Line equation: `B0 + (B1 * X1) + (B2 * X2) = 0`. Plug a point in: **> 0 → class 0**, **< 0 → class 1**, near 0 → hard to classify (large magnitude → high confidence).
- **Margin** = perpendicular distance from the line to the *closest* points only. The best hyperplane **maximises the margin**.
- Those closest points are the **support vectors** - they alone "support"/define the hyperplane. Everything else is irrelevant to the boundary (this is the outlier-robustness from [resource 1](#1-when-should-you-consider-using-svm-jedamski-2019)).

#### 2. Soft-Margin Classifier (real, messy data)
- Real data isn't perfectly separable, so we **relax** the margin - allowing some points to violate it via **slack variables**.
- The tuning parameter **C** sets how much violation is allowed:

| C value | Behaviour | Bias / Variance |
|---|---|---|
| C = 0 | No violations → back to the rigid Maximal-Margin classifier | - |
| Small C | More tolerant of violations; more support vectors; more sensitive to data | Higher variance, lower bias |
| Large C | Fewer violations allowed; harder boundary | Lower variance, higher bias |

- C also **controls how many support vectors** the model uses. (Note the sign convention differs from scikit's framing in [resource 6](#6-scikit-learn-support-vector-machines-documentation), where *low C = smoother/more regularised* - read both carefully.)

#### 3. Kernels and the Kernel Trick
- Key insight: linear SVM can be rewritten using the **inner (dot) product** of observations rather than the observations themselves. `f(x) = B0 + sum(ai * (x, xi))`.
- The **kernel** `K(x, xi)` is a similarity/distance measure. Swapping the kernel lets the boundary curve into higher dimensions **without explicitly computing the coordinates** - the *kernel trick*.

| Kernel | Formula (informal) | Effect |
|---|---|---|
| **Linear** | `K = sum(x * xi)` | Straight boundary; the dot product itself |
| **Polynomial** | `K = (1 + sum(x*xi))^d` | Curved boundaries; `d=1` == linear; degree set by hand |
| **Radial (RBF)** | `K = exp(-gamma * sum((x - xi)^2))` | Very local; complex closed regions. Good default `gamma ≈ 0.1`, usually `0 < gamma < 1` |

#### 4. Learning & data prep
- The optimisation is a **Quadratic Programming** problem. The standard efficient solver is **Sequential Minimal Optimization (SMO)** - it breaks the problem into analytically solvable sub-problems (used by LIBSVM). Naive numerical optimisation / SGD works but is inefficient.
- **Data prep:** inputs must be **numeric** (one-hot categorical features); basic SVM is for **binary** classification (extensions exist for multi-class & regression).

#### Key Takeaways for MLN601
1. This resource gives you the vocabulary the notebooks assume: **hyperplane, margin, support vectors, C, kernel, gamma**. When [Activity 2 (muffin vs cupcake)](#task-list) asks you to tune `C`, you'll know it's trading margin violations against boundary hardness.
2. **Scale your data first** - SVM is *not* scale-invariant (reinforced in resource 6). Every notebook here should standardise features before fitting.
3. Connects back to Module 3-4: the C parameter is the same **bias-variance** dial you met with regression/trees, just applied to margin width.

---

### 6. scikit-learn - Support Vector Machines Documentation (2011)

**Citation:** Pedregosa, F. et al. (2011). *Scikit-learn: Machine learning in Python.* JMLR 12, 2825-2830. (SVM user guide, s1.4.)
**Local source:** `r6_Support-Vector-Machines_scikit-learn-docs.pdf`

**Purpose:** The practical API reference - which estimator to instantiate, which parameters matter, and the practical-use gotchas. Keep this open while coding the activities.

---

#### 1. Pros, cons, and the estimator zoo

**Advantages:** effective in high-dimensional spaces; still works when **features > samples**; **memory-efficient** (only support vectors stored); **versatile** (swappable kernels, even custom).
**Disadvantages:** with features >> samples, kernel + regularisation choice is **critical to avoid overfitting**; SVMs **don't natively give probabilities** (computed via expensive 5-fold CV / Platt scaling).

| Class | Use for | Notes |
|---|---|---|
| `SVC` | Classification | libsvm-based; supports kernels; `O(n_features x n_samples^2..3)` - scales poorly to huge n |
| `NuSVC` | Classification | Like `SVC` but `nu` param ≈ fraction of errors & support vectors |
| `LinearSVC` | Classification, linear only | liblinear-based; **much faster**, scales ~linearly to millions of samples; uses squared-hinge loss; lacks `support_` |
| `SVR` / `NuSVR` / `LinearSVR` | Regression | Cost function ignores points inside the epsilon-tube |
| `OneClassSVM` | Outlier / novelty detection | Unsupervised |

#### 2. Multi-class strategy
- `SVC` / `NuSVC` train **one-vs-one (ovo)**: `n_classes * (n_classes - 1) / 2` classifiers internally, but expose an **ovr**-shaped decision function by default (`decision_function_shape='ovr'`).
- `LinearSVC` uses **one-vs-rest (ovr)**: trains `n_classes` models.

#### 3. Scores, probabilities, and the two critical RBF knobs
- `decision_function` gives per-class scores; `probability=True` enables `predict_proba` (Platt scaling). **Caveat:** argmax of scores may differ from argmax of probabilities, and a binary sample can be `predict`-ed positive while `predict_proba < 0.5`. If you only need a confidence *ranking*, prefer `decision_function`.
- **The two knobs to tune (RBF):**

| Parameter | Low value | High value |
|---|---|---|
| **C** (all kernels) | Smooth decision surface (more regularisation) | Classifies every training point correctly (risk of overfit) |
| **gamma** (RBF) | Each point has far-reaching influence | Influence is very local (tight, wiggly boundary) |

- Tune them together with **`GridSearchCV`, spaced exponentially** (e.g. `C, gamma in [1e-3, 1e-2, ...]`).

#### 4. Practical-use rules that break notebooks if ignored
- **Always scale** - SVM is *not* scale-invariant. Use a `Pipeline(StandardScaler(), SVC())` so the same scaling hits train and test.
- **Unbalanced classes:** set `class_weight='balanced'` (or per-sample `sample_weight`).
- **Reproducibility:** `random_state` only matters when `probability=True` (or `LinearSVC` dual coordinate descent). Otherwise SVC is deterministic.
- **Speed:** raise `cache_size` (e.g. 500-1000 MB) for large problems; use `LinearSVC`/`SGDClassifier` instead of kernel SVC for very large linear problems.

#### Key Takeaways for MLN601
1. Every activity notebook should be `make_pipeline(StandardScaler(), SVC(...))` + `GridSearchCV` over `C`/`gamma`. That's the whole practical workflow.
2. For the **face recognition** ([Activity 4](#task-list)) task - a high-dimensional problem - `SVC` with RBF is the natural fit; expect PCA/eigenfaces as the pre-processing step (features >> samples territory where SVM excels, per [resource 1](#1-when-should-you-consider-using-svm-jedamski-2019)).
3. Mind the **C sign convention**: Brownlee ([resource 5](#5-support-vector-machines-for-machine-learning-brownlee-2020)) says *low C = fewer violations*, scikit says *low C = smoother/more regularised*. Both describe the same math from opposite ends - trust the scikit framing when coding.

---

### 7. scikit-learn - Metrics & the Confusion Matrix (2011)

**Citation:** Pedregosa, F. et al. (2011). *Scikit-learn: Machine learning in Python.* JMLR 12, 2825-2830. (Metrics & scoring, s3.4.)
**Local source:** `r7_Metrics-and-Scoring_scikit-learn-docs.pdf`

**Purpose:** How to judge whether the SVM is any good. The confusion matrix is the source from which almost every classification metric is derived - accuracy alone lies on imbalanced data.

---

#### 1. The confusion matrix
- `confusion_matrix(y_true, y_pred)`: entry `[i, j]` = observations **actually** in class `i` **predicted** as class `j`. Rows = truth, columns = prediction (scikit convention - Wikipedia flips axes).
- For **binary**, unravel it: `tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()`.
- `normalize='true' | 'pred' | 'all'` reports ratios (divide by row / column / whole-matrix sums) instead of raw counts - useful for imbalanced classes.

|  | Predicted Negative | Predicted Positive |
|---|---|---|
| **Actual Negative** | TN | FP (Type I error) |
| **Actual Positive** | FN (Type II error) | TP |

#### 2. Precision, recall, F1 - the derived metrics

| Metric | Formula | Intuition |
|---|---|---|
| **Accuracy** | `(TP+TN) / total` | Overall correctness - **misleading on imbalanced data** |
| **Precision** | `TP / (TP + FP)` | Of those predicted positive, how many really are? ("don't cry wolf") |
| **Recall** (sensitivity) | `TP / (TP + FN)` | Of the real positives, how many did we catch? ("miss nothing") |
| **F1** | `2 * (P*R) / (P+R)` | Harmonic mean of precision & recall; best = 1, worst = 0 |
| **F-beta** | weighted harmonic mean | `beta > 1` favours recall, `beta < 1` favours precision |

- **Averaging for multi-class:** `macro` (unweighted mean over classes - treats rare classes equally), `weighted` (by support), `micro` (global tally - dominated by frequent classes).

#### 3. `classification_report` - the one-call summary
- `classification_report(y_true, y_pred, target_names=...)` prints **precision, recall, f1-score, support** per class plus `accuracy`, `macro avg`, `weighted avg`. This is the single output to paste when reporting a model's quality.
- `roc_auc_score` / `roc_curve` and `precision_recall_curve` evaluate ranking quality across thresholds (pair with SVM's `decision_function`).

#### Key Takeaways for MLN601
1. **Report the confusion matrix + `classification_report`, not just accuracy** - especially for **breast cancer** ([Activity 3](#task-list)), where a false negative (missed malignancy) is far costlier than a false positive. There, **recall on the malignant class** is the metric that matters.
2. On imbalanced medical/face data, use `class_weight='balanced'` (from [resource 6](#6-scikit-learn-support-vector-machines-documentation)) and judge with **macro-averaged F1**, not accuracy.
3. Because SVM exposes `decision_function`, you can slide the threshold and draw an **ROC/PR curve** - the honest way to show the precision-recall trade-off in your write-ups.
