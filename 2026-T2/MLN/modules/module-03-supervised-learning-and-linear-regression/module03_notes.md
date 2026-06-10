# Module 3 - Supervised Learning and Linear Regression

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| 1 | Watch & summarise IntuitiveML (2020) - intuition behind linear regression (least squares + correlation) | 🔥 Primer ready - needs manual watch (YouTube) |
| **2** | Read & summarise Raschka & Mirjalili (2019) - Ch.1 *Giving Computers the Ability to Learn from Data* | ✅ |
| 3 | Read & summarise Bento (2020) - *Linear Regression in Real Life* (road-trip story) | 🔥 Primer ready - needs manual read (Medium paywall/404) |
| 4 | Watch & summarise Fowers (2019) - linear regression with sklearn, from scratch | 🔥 Primer ready - needs manual watch (YouTube) |
| **5** | Read & summarise *Choosing the Right Estimator* - scikit-learn ML map | ✅ |
| 6 | Activity 1: SkLearn Linear Regression - Boston Housing (The Semicolon, 2017) | 🕐 |
| 7 | Activity 2: Predicting House Prices with Linear Regression (Valkov, 2019) | 🕐 |

---

## Key Highlights

### 1. IntuitiveML (2020). Intuition Behind Linear Regression. [Video]

**Citation:** IntuitiveML (2020, 1 August). *Intuition behind linear regression* [Video file]. https://www.youtube.com/watch?v=uAZMhpNBq8M

**Purpose:** A visual, intuition-first primer on *why* linear regression works: the line of best fit, the method of least squares, and how correlation between input and outcome drives the slope.

> ⚠️ **Status: needs manual watch** - no offline transcript available. The primer below covers the concepts the video walks through so you can watch at 1.5x and just confirm/annotate.

---

#### 1. The line of best fit
- Linear regression fits a single straight line `ŷ = b₀ + b₁x` through a cloud of points so the line **summarises the trend** (e.g. study hours to exam score).
- **`b₁` (slope)** = how much `y` changes per 1-unit change in `x`; **`b₀` (intercept)** = predicted `y` when `x = 0`.
- The line is a **model**: once fitted, plug in a new `x` to predict `ŷ`.

#### 2. The method of least squares
- The "best" line is the one that **minimises the sum of squared vertical distances** (residuals) between each actual point `yᵢ` and the line's prediction `ŷᵢ`.
- **Residual** `eᵢ = yᵢ − ŷᵢ`. We square residuals so positives and negatives don't cancel, and so big misses are penalised more.
- Cost (to minimise): `SSE = Σ(yᵢ − ŷᵢ)²`. The closed-form Ordinary Least Squares (OLS) solution sets the slope/intercept that make this smallest.

#### 3. Correlation drives the fit
- **Correlation (r)** measures the strength/direction of the linear relationship (−1 to +1). A strong correlation gives a steep, confident line; near-zero correlation gives a near-flat, low-value line.
- Correlation is the *intuition* behind the slope sign: positive correlation, positive slope.
- 🔴 **Trap:** correlation ≠ causation, and a high `r` only captures the **linear** part of a relationship (curves look weak to `r`).

#### Key Takeaways for MLN601
1. This is the conceptual spine of **Assessment 1 (Regression Analysis)** - every model you fit is a least-squares line (or plane) through your data.
2. Connects directly to [Resource 3 (Bento)](#3-bento-b-2020-linear-regression-in-real-life-article) which dramatises least squares with a road-trip story, and [Resource 4 (Fowers)](#4-fowers-r-2019-linear-regression-python-sklearn-from-scratch-video) which codes it in scikit-learn.
3. Anchor: it's the same `fit -> predict -> evaluate` loop from Module 1, now made concrete with a specific algorithm.

---

### 2. Raschka, S. & Mirjalili, V. (2019). Giving Computers the Ability to Learn from Data.

**Citation:** Raschka, S. & Mirjalili, V. (2019). Giving computers the ability to learn from data. In *Python Machine Learning: Machine Learning and Deep Learning with Python, Scikit-learn, and TensorFlow 2* (3rd ed., pp. 1-17). Birmingham, England: Packt.

**Purpose:** The foundational chapter of the course's core textbook. It defines the three types of ML, formalises the supervised-learning vocabulary (classification vs regression), and lays out the end-to-end roadmap for building an ML system.

---

#### 1. The three types of machine learning

| Type | Has labels? | Goal | This module's focus |
|---|---|---|---|
| **Supervised** | ✅ Yes (known outputs) | Predict labels/values on unseen data | ⭐ Regression lives here |
| **Unsupervised** | ❌ No | Discover hidden structure | Clustering, dim. reduction |
| **Reinforcement** | Reward signal (not a label) | Learn actions that maximise reward | Background only (chess engine) |

- **Supervised** = "the right answer is known beforehand" -> learn a model from labelled training data -> predict on new data.
- **Reinforcement** is *related* to supervised, but feedback is a **reward measure**, not ground-truth labels; the agent learns by trial-and-error / planning.

#### 2. Supervised learning splits into classification vs regression

| | **Classification** | **Regression** |
|---|---|---|
| Target type | Discrete, **unordered** class labels | **Continuous** value |
| Example | Spam vs non-spam (binary); A-Z handwriting (multiclass) | Predict SAT score from study time |
| Output | Group membership | A number on a scale |
| Decision object | A **decision boundary** separating classes | A **fitted line/surface** through points |

- This module is the **regression** branch: "given predictor (explanatory) variables and a continuous response, find a relationship that lets us predict an outcome."
- **Terminology lock-in:** predictor variables = **features** (`x`); response variable = **target** (`y`).

#### 3. Regression analysis - the core mechanics
- Fit a straight line to data that **minimises the distance (most commonly the average squared distance) between the points and the line.**
- Learn the **intercept and slope**, then use them to predict `y` for new `x`. (This is exactly Resource 1's least squares.)
- **History, "regression toward the mean":** the term was coined by **Francis Galton (1886)**, *Regression towards Mediocrity in Hereditary Stature* - he observed children's heights regress toward the population mean rather than amplifying parents' extremes.

#### 4. Unsupervised learning (context for later modules)
- **Clustering** = organise unlabelled data into meaningful subgroups by similarity (a.k.a. "unsupervised classification"); e.g. marketing customer segments.
- **Dimensionality reduction** = compress high-dimensional data into a smaller subspace, removing noise and aiding visualisation (e.g. 3D Swiss-Roll to 2D). Useful as a **preprocessing** step.

#### 5. Terminology & notation (exam-ready)

| Term | Symbol | Synonyms |
|---|---|---|
| Training example | row of `X` | observation, record, instance, sample |
| Feature | column / `x` | predictor, variable, input, attribute, covariate |
| Target | `y` | outcome, output, response, dependent variable, label, ground truth |
| Loss function | - | cost function, error function (loss = per-point; cost = averaged/summed over dataset) |

- **Feature matrix `X`**: each **row = one example**, each **column = one feature**. The classic **Iris dataset** = `150 × 4` matrix (150 flowers, 4 measurements), so `X ∈ ℝ¹⁵⁰ˣ⁴`; target `y ∈ {Setosa, Versicolor, Virginica}`.
- Convention: superscript `(i)` = i-th example; subscript `j` = j-th feature.

#### 6. The roadmap for building an ML system
1. **Preprocessing** - raw data rarely usable as-is; clean it, **scale features** to the same range ([0,1] or zero-mean/unit-variance), optionally reduce dimensionality. Randomly split into **train** and **test** sets.
2. **Training & model selection** - many algorithms exist; **No Free Lunch theorem (Wolpert)**: no single model is best for every task, so *compare a handful of algorithms*. ("If the only tool you have is a hammer, you treat everything as a nail.") Pick a **metric** (e.g. accuracy for classification). Use **cross-validation** (split train further into train/validation) to estimate generalisation, and **hyperparameter tuning** ("the knobs you turn", *not* learned from data) to optimise.
3. **Evaluation** - use the held-out **test set** to estimate the **generalisation error**, then predict on new data.

- 🔴 **Leakage warning (stated explicitly):** parameters for scaling / dimensionality reduction must be **obtained from the training set only** and *reapplied* to the test set, otherwise "the performance measured on the test data may be overly optimistic." (Ties straight back to Module 1 & 2 leakage notes.)

#### 7. The Python stack
- **NumPy** (vectorised arrays, on C/Fortran) -> **pandas** (tabular data) -> **Matplotlib** (viz) -> **scikit-learn** (classical ML). TensorFlow reserved for the deep-learning chapters.
- Reference versions: scikit-learn 0.22, NumPy 1.17, pandas 0.25; Python 3.7+.

#### Key Takeaways for MLN601
1. **Parameter vs hyperparameter** is a guaranteed exam/forum distinction: *parameters* (slope, intercept) are **learned from data**; *hyperparameters* (e.g. regularisation strength) are **set by you** and tuned via CV.
2. The **No Free Lunch theorem** is your justification for trying several estimators, which is exactly what Resource 5's [estimator map](#5-choosing-the-right-estimator-scikit-learn-ml-map) operationalises.
3. The **train -> preprocess-on-train-only -> test -> generalisation error** discipline is the backbone of a defensible A1 report and prevents the leakage that inflated the vgsales R² in Module 2.

---

### 3. Bento, B. (2020). Linear Regression in Real Life. [Article]

**Citation:** Bento, B. (2020, 8 May). *Linear regression in real life: real-world problems solved with math.* Towards Data Science. https://towardsdatascience.com/linear-regression-in-real-life-4a78d7159f16

**Purpose:** Teaches the linear-regression model through plain storytelling, an everyday road-trip-on-limited-petrol scenario, so the math (slope, intercept, least squares) lands intuitively before any code.

> ⚠️ **Status: needs manual read** - the Medium/TDS page is paywalled / returns 404 to the fetcher. The primer below reconstructs the concepts from the resource overview; **confirm the article's specific figures** when you skim the original.

---

#### 1. The storytelling device (per resource overview)
- The author uses **driving on a limited amount of petrol** as the running example: given how far you can travel per unit of fuel, predict whether you'll reach your destination.
- The point: linear regression is just **formalising a relationship you already reason about intuitively** ("more fuel, more distance, roughly proportional").

#### 2. The linear model
- Single-feature (simple) linear regression: `ŷ = b₀ + b₁x` (intercept `b₀` + slope `b₁`).
- Slope `b₁` = the **rate** (e.g. km per litre); intercept `b₀` = the baseline offset.

#### 3. Fitting via least squares
- The best line **minimises the sum of squared residuals** `Σ(yᵢ − ŷᵢ)²` (Mean Squared Error when averaged).
- **Residuals** = vertical gaps between actual and predicted; squaring penalises large misses and removes sign cancellation.
- Goodness-of-fit is typically reported with **R²** (fraction of variance in `y` explained by the model).

#### Key Takeaways for MLN601
1. Same least-squares idea as Resources 1 & 2; use this article as the **"explain it to a stakeholder"** version for your A1 write-up's business framing.
2. The real-world framing (a concrete decision under a constraint) is exactly the **Business Understanding** lens from Module 2's CRISP-DM; connect the two.

---

### 4. Fowers, R. (2019). Linear Regression Python Sklearn [From Scratch]. [Video]

**Citation:** Fowers, R. (2019, 25 July). *Linear regression Python Sklearn [From Scratch]* [Video file]. https://www.youtube.com/watch?v=b0L47BeklTE

**Purpose:** A hands-on, step-by-step walkthrough of implementing linear regression in scikit-learn inside a Jupyter notebook - the practical bridge from the math (Resources 1-3) to working code.

> ⚠️ **Status: needs manual watch** - no offline transcript. The primer below is the code skeleton to follow along with.

---

#### 1. The scikit-learn linear-regression workflow
```python
import pandas as pd
from pydataset import data                      # note: the video uses pydataset
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = data('<dataset>')                           # load a built-in dataset
X = df[['feature1', 'feature2']]                 # features (2D)
y = df['target']                                 # target (1D, continuous)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)        # honest hold-out + fixed seed

model = LinearRegression()
model.fit(X_train, y_train)                       # learns coef_ and intercept_
y_pred = model.predict(X_test)                    # predict on unseen data

print(model.coef_, model.intercept_)              # the learned parameters
print(r2_score(y_test, y_pred))                   # evaluate
```

#### 2. Things to watch for (the video's emphasis)
- Imports: **`pydataset`** for the data, and **`train_test_split` from `sklearn.model_selection`**.
- `LinearRegression()` follows scikit-learn's universal **`fit()` / `predict()` / `score()`** pattern (Module 1).
- After fitting, inspect **`model.coef_`** (the slopes `b₁…`) and **`model.intercept_`** (`b₀`).
- 🔴 Always set **`random_state`** so the split is reproducible (Module 1 pitfall).

#### Key Takeaways for MLN601
1. This is the **template you'll adapt** for Activity 1 (Boston housing) and Activity 2 (Valkov house prices), and ultimately the A1 notebook.
2. `pydataset` may not be in your env (Homebrew py3.14): `pip install pydataset --break-system-packages`, or substitute a CSV / `sklearn.datasets` loader.

---

### 5. Choosing the Right Estimator (scikit-learn ML Map)

**Citation:** *Choosing the right estimator* (n.d.). scikit-learn documentation. https://scikit-learn.org/stable/machine_learning_map.html (local copy: `A5_ml_map.svg`)

**Purpose:** A single-page flowchart that routes any problem to a candidate algorithm based on data size, label availability, and task type. The orange **"try next"** arrows mean: *if this estimator underperforms, follow the arrow to the next candidate* - a practical answer to the No Free Lunch theorem.

---

#### 1. The four branches (top-level routing)
| Branch | Trigger question | Labels? |
|---|---|---|
| **Classification** | "predicting a **category**?" | ✅ labelled |
| **Regression** ⭐ | "predicting a **quantity**?" | ✅ labelled |
| **Clustering** | "just looking / grouping?" | ❌ unlabelled |
| **Dimensionality reduction** | "predicting **structure**?" | ❌ unlabelled |

- **Gate 0:** `>50 samples?` - if **no, "get more data"** (don't model yet).
- Then: *Do you have labelled data?* -> supervised (classification/regression) vs unsupervised (clustering/dim-reduction).

#### 2. The regression path (the one that matters for A1)
| If… | Try | Then try next |
|---|---|---|
| `<100K samples`, few features should matter | **Lasso**, **ElasticNet** | - |
| `<100K samples`, all features relevant | **Ridge regression**, **SVR(kernel='linear')** | **SVR(kernel='rbf')**, ensemble regressors |
| `>100K samples` | **SGD Regressor** | - |

- **Plain `LinearRegression` / OLS** is the unregularised starting point; **Ridge/Lasso/ElasticNet** add regularisation to fight overfitting (Ridge = shrink all coefficients; Lasso = drive some to zero for feature selection; ElasticNet = both).

#### 3. The other three branches (reference)
| Task | First-choice estimators | Big-data / fallback |
|---|---|---|
| **Classification** | LinearSVC -> KNeighbors -> SVC, Naive Bayes | SGD Classifier, ensembles, kernel approximation (text) |
| **Clustering** (k known) | **KMeans** | MiniBatch KMeans (`>100K`), GMM/VBGMM, Spectral |
| **Dimensionality reduction** | **PCA** (Randomized) | Isomap, Spectral Embedding, LLE, kernel approximation |

#### 4. Sample-size thresholds (the recurring decision axis)
- **`<50`** -> get more data. **`50-100K`** -> most methods viable (kernel SVM, ensembles). **`>100K`** -> scalable methods only (SGD, MiniBatch).

#### Key Takeaways for MLN601
1. For A1 (continuous target, tabular, modest size) the map lands you squarely on the **regression branch** -> start with `LinearRegression`, then justify **Ridge/Lasso** if you see overfitting, and *say so in the report* (this is the "compare a handful of algorithms" discipline from Raschka).
2. The "try next" arrows are the **No Free Lunch theorem made operational**; pin this map next to your notebook.
3. The local `A5-Estimator.pdf` is a one-box mental model: **Data -> Estimator (best fit) -> Prediction / Classification.**

---

## Module 3 Synthesis - From Intuition to Code

| Lens | Resource | One-line role |
|---|---|---|
| **Intuition** | IntuitiveML (R1) | *Why* least squares finds the best line |
| **Theory + vocab** | Raschka Ch.1 (R2) | The map of ML; classification vs regression; the build roadmap |
| **Story** | Bento (R3) | Least squares dramatised as a real decision under constraint |
| **Code** | Fowers (R4) | `fit/predict/score` in scikit-learn |
| **Algorithm choice** | sklearn map (R5) | Which estimator to reach for, and what to try next |

**The through-line:** linear regression = fit `ŷ = b₀ + b₁x` by **minimising Σ(residual²)** -> learn parameters (slope/intercept) from **training data only** -> evaluate **generalisation** on held-out test data -> report **R² / MSE**, not just a pretty chart.

### Assessment Hook - A1 (Regression Analysis, due 28 Jun, 20%)
Module 3 supplies the *actual algorithm* for A1: clean target + features -> `train_test_split(random_state=…)` -> `LinearRegression().fit()` -> predict -> report **R²/RMSE** -> discuss overfitting (Ridge/Lasso) and limits. Frame the whole thing on the CRISP-DM spine from Module 2.
