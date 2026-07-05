# MLN601 · Module 6 - One-Pager

> **Support Vector Machines · Maximal Margin · Support Vectors · Soft Margin (C) · Kernel Trick (RBF/poly) · Evaluation**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **An SVM separates two classes with the maximum-margin hyperplane - the single boundary that sits as far as possible from the nearest points of each class.** Only those nearest points (the **support vectors**) define the boundary; everything else is ignored, which is why SVM is naturally **robust to outliers**.
> (Brownlee 2020 · scikit-learn SVM user guide, s1.4)

## 🖤 Zone 1 - Geometry: hyperplane, margin, support vectors
- 🖤 **Hyperplane** = the separating line/plane in n-dimensional feature space. Line form: `B0 + B1·X1 + B2·X2 = 0`.
- 🔵 Plug a point in: **> 0 → class 0**, **< 0 → class 1**, **near 0 → uncertain**; large magnitude = high confidence.
- 🖤 **Margin** = perpendicular distance from the boundary to the *closest* points only. Best hyperplane = **maximises the margin**.
- 🖤 **Support vectors** = those closest points. They alone "support" the boundary → move a far-away outlier and nothing changes.
- 🔴 Exam line: "the decision boundary is defined by a small number of points (the support vectors), not the whole dataset."

## 🖤 Zone 2 - Soft margin & C (the bias-variance dial) ⭐ SLO b) - THE TUNING CORE
- 🖤 Real data isn't perfectly separable → **relax** the margin, allowing violations via **slack variables**. `C` sets how much.
- 🔴 **Sign-convention trap** (two sources disagree - trust **scikit** when coding):

| `C` (scikit framing) | Boundary | Bias / Variance |
|---|---|---|
| **Low C** | Smoother, wider margin, more regularised, more support vectors | ↑ bias, ↓ variance |
| **High C** | Classifies every training point correctly, harder/tighter boundary | ↓ bias, ↑ variance (**overfit risk**) |

- 🔵 `C = 0` → back to the rigid maximal-margin classifier (no violations). Brownlee frames C the opposite way; same maths, read carefully.

## 🖤 Zone 3 - The Kernel Trick (bend the boundary)
- 🖤 Key insight: linear SVM can be written using only the **dot product** of points: `f(x) = B0 + Σ aᵢ·⟨x, xᵢ⟩`.
- 🖤 Swap the dot product for a **kernel** `K(x, xᵢ)` → curve the boundary into higher dimensions **without computing those coordinates**.

| Kernel | Formula (informal) | Effect |
|---|---|---|
| **Linear** | `K = Σ(x·xᵢ)` | Straight boundary (the dot product itself) |
| **Polynomial** | `K = (1 + Σ x·xᵢ)^d` | Curved; `d=1` == linear; degree `d` set by hand |
| **RBF (radial)** | `K = exp(-γ·Σ(x - xᵢ)²)` | Very local; complex closed regions. Default `γ ≈ 0.1`, usually `0 < γ < 1` |

- 🔴 **gamma (RBF only):** **low γ** = each point reaches far (smooth boundary) · **high γ** = influence is local (tight, wiggly → **overfit**).
- 🔵 Aharoni viz: 2D red/blue dots not linearly separable; lift with `z = x² + y²` → a plane separates them cleanly.

## 🖤 Zone 4 - When to use SVM vs when to avoid (Jedamski 2019)
| ✅ SVM shines | ❌ Avoid SVM |
|---|---|
| **Binary classification** (weak at regression) | You need **transparency / feature importance** (it's a black box) |
| **"Short & fat" data** - many features, few rows (features > samples) | **"Tall & thin"** - many rows, few features (slow, no payoff) |
| Complex, **non-linear** boundaries (kernel trick) | You want a **fast benchmark** (slow to train *and* predict) |
| **Outlier-heavy** data (only support vectors matter) | Limited time / compute |

- 🔵 Day-job link: SVM fits **wide, low-volume** problems - e.g. classifying a SKU from hundreds of engineered attributes - far better than a high-throughput streaming decision.

## 🖤 Zone 5 - The scikit workflow (what every notebook does) ⭐ SLO c)
```text
make_pipeline(StandardScaler(), SVC(kernel="rbf"))  ->  GridSearchCV over C & gamma (spaced exponentially: 1e-3,1e-2,...)
```
- 🔴 **ALWAYS scale first** - SVM is *not* scale-invariant. `Pipeline(StandardScaler(), SVC())` so the same scaling hits train + test.
- 🔵 **Imbalanced classes:** `class_weight="balanced"`. **Probabilities:** SVM has none natively - `probability=True` uses expensive Platt scaling; for a confidence *ranking* prefer `decision_function`.

| Estimator | Use for | Notes |
|---|---|---|
| `SVC` | Classification (kernels) | libsvm; `O(n_features · n_samples²⁻³)` - scales poorly to huge n; multi-class = **one-vs-one** |
| `LinearSVC` | Linear classification | liblinear; **much faster**, scales to millions; **one-vs-rest**; no `support_` |
| `NuSVC` | Classification | `nu` ≈ fraction of errors & support vectors |
| `SVR` / `LinearSVR` | Regression | ignores points inside the epsilon-tube |
| `OneClassSVM` | Outlier / novelty | unsupervised |

## 🖤 Zone 6 - Evaluation: never trust accuracy alone (scikit metrics)
```text
confusion_matrix -> rows = TRUTH, cols = PREDICTION (scikit convention)
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
```
| Metric | Formula | Reads as |
|---|---|---|
| Precision | `TP / (TP + FP)` | when I predict positive, how often right? ("don't cry wolf") |
| Recall (sensitivity) | `TP / (TP + FN)` | of real positives, how many caught? ("miss nothing") |
| F1 | `2·P·R / (P + R)` | harmonic mean; best = 1 |

- 🔴 **Breast cancer (Activity 3):** a **false negative = missed malignancy** is the costly error → **recall on the malignant class** is THE metric, not accuracy.
- 🔵 Report `classification_report` (precision/recall/f1/support per class) + the confusion matrix. Multi-class averaging: **macro** treats rare classes equally; **weighted** by support; **micro** = global tally.
- 🔵 SVM exposes `decision_function` → slide the threshold → draw **ROC / PR curves** to show the trade-off honestly.

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 2 - Classification** · notebook + mark-up + source code + 7-10 min presentation + **1500 words** (±10%) · **40%** · due **26/07/2026** · SLOs **b) c) d)**. Module 6 addresses **SLOs b) & d)**; it also seeds **Assessment 3** (ML Project, 40%, due 19/08/2026).
> SVM is a strong **candidate classifier** for A2, and its whole evaluation toolkit (confusion matrix + precision/recall/F1/ROC from Resource 7) **is** the graded rubric. Even if the brief mandates a Decision Tree, SVM is the natural high-dimensional comparator - and the metrics vocabulary is shared.

## 🔴 If you only memorise 5 things
1. **Max-margin hyperplane defined only by support vectors** → outlier-robust.
2. **C = soft-margin dial:** low C = smoother/regularised, high C = tight/overfit (trust scikit's sign).
3. **Kernel trick:** linear → polynomial → RBF bends the boundary without computing higher-dim coords; **RBF adds gamma** (low = smooth, high = wiggly).
4. **Always `StandardScaler` + `GridSearchCV(C, gamma)`**; SVM is not scale-invariant.
5. **Judge with confusion matrix + precision/recall/F1**, not accuracy - on cancer data, **recall on malignant** rules.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your warehouse has a "wide, low-volume" table (hundreds of engineered SKU attributes, few labelled rows). Why is that exactly the shape SVM beats logistic regression on - and what would you scale first?
2. If a defect-detection SVM must never miss a bad unit, which metric do you optimise (precision or recall), and how does moving the `decision_function` threshold trade one for the other?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🔥 Watch Aharoni (2007) kernel-trick visualisation + the two Linear Digressions podcasts (Res. 3 & 4) - manual.
- [ ] 🕐 Activity 1 - Kernel trick by hand in the Malakar (2016) spreadsheet (compute `z = x² + y²`).
- [ ] 🕐 Activity 2 - Muffin vs cupcake SVM (tune `C`, watch the boundary harden).
- [ ] 🕐 Activity 3 - Breast cancer SVM (report **recall on malignant** + confusion matrix).
- [ ] 🕐 Activity 4 - Face recognition on LFW (RBF `SVC`, expect PCA/eigenfaces - features >> samples).
- [ ] 🕐 Activity 5 - Wine classification with SVM (ties straight to your A1/A2 wine data).
