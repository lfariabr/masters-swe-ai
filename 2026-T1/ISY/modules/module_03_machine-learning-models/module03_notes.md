# Module 3 — Machine Learning Models
## ISY503 Intelligent Systems

---

## Task List

| # | Resource / Activity | Type | Status |
|---|---------------------|------|--------|
| **1** | Analytics India Magazine (2018) — 6 Types of Classification Algorithms | Video | ✅ Watched + Reviewed |
| **2** | Brownlee (2019) — A Gentle Introduction to Model Selection | Article | ✅ Read + Reviewed |
| **3** | Arlot & Celisse (2010) — A Survey of Cross-Validation Procedures | Academic paper | ✅ Read + Reviewed |
| **4** | Feurer & Hutter (2019) — Hyperparameter Optimization | Book chapter | ✅ Read + Reviewed |
| A1 | Extra Machine Learning Models (Linear Regression, PCA, AdaBoost, XGBoost) | Activity | ✅ Done + Posted |
| A2 | K-Fold Cross-Validation Discussion (K = 1, 2, 5, 10, N–2, N–1) | Activity | ✅ Done + Posted |

---

## Key Highlights

### 1. Analytics India Magazine (2018). 6 Types of Classification Algorithms [Video]

**Citation:** Analytics India Magazine. (2018, 15 February). *6 types of classification algorithms* [Video file]. https://www.youtube.com/watch?v=ppXFoltcX7A

**Purpose:** Introduces seven supervised classifiers — Logistic Regression (LR), Naïve Bayes (NB), Stochastic Gradient Descent (SGD), K-Nearest Neighbours (KNN), Decision Tree (DT), Random Forest (RF), and Support Vector Machine (SVM) — in a short visual format.

#### 1. KNN (K-Nearest Neighbours)
Classifies by majority vote of K nearest neighbours; lazy learner, no training phase, sensitive to K and feature scale.

#### 2. Decision Tree
Recursively splits data on best feature thresholds forming interpretable rules; prone to overfitting without pruning.

#### 3. Random Forest
Ensemble of decision trees trained on random feature subsets via bagging; reduces variance and overfitting risk.

#### 4. Naive Bayes
Applies Bayes' theorem assuming feature independence; fast, probabilistic classifier, excels on text classification.

#### 5. SVM (Support Vector Machine)
Finds maximum-margin hyperplane between classes; uses kernels (RBF, polynomial) to handle non-linear boundaries.

#### 6. Logistic Regression
Models class probability via sigmoid function; linear decision boundary, interpretable coefficients, fast to train.

#### 7. SGD (Stochastic Gradient Descent)
Optimises model weights via gradient updates on one sample at a time; scalable to large datasets, sensitive to learning rate.

---

### 2. Brownlee, J. (2019). A Gentle Introduction to Model Selection for Machine Learning

**Citation:** Brownlee, J. (2019, 2 December). *A gentle introduction to model selection for machine learning*. Machine Learning Mastery. https://machinelearningmastery.com/a-gentle-introduction-to-model-selection-for-machine-learning/

**Purpose:** Explains what model selection is, why performance alone is insufficient, and introduces the two main families of model selection techniques.

#### 1. What Is Model Selection?

**Model selection** is the process of choosing one final machine learning model from a collection of candidate models for a training dataset. It applies to:
- Comparing **different algorithm types** (e.g. logistic regression vs. SVM vs. KNN)
- Comparing **same-type models** with different hyperparameter configurations (e.g. SVM with different kernels)

> *Model selection is distinct from model assessment.* Selection = choosing the best among candidates. Assessment = evaluating how well the chosen model will generalise.

#### 2. Considerations for Model Selection

The concept of a "best" model is not useful — all models carry some predictive error from data noise, incomplete sampling, and algorithm limitations. The goal is a **"good enough" model** that satisfies one or more of:

| Criterion | Description |
|-----------|-------------|
| Stakeholder constraints | Simplicity, explainability, maintainability |
| Resource constraints | Acceptable training/inference time and cost |
| Naive baseline comparison | Better than a trivial default |
| Peer comparison | Best among tested alternatives |
| State-of-the-art comparison | Competitive with published benchmarks |

**Key insight:** Model selection is not selecting a pre-fitted model but selecting a **model development pipeline** — because different algorithms require different data preparation steps (filtering, transformation, feature selection, feature engineering).

#### 3. Model Selection Techniques

Two main classes:

| Class | Mechanism | Best suited for |
|-------|-----------|-----------------|
| **Probabilistic Measures** | Score via in-sample error + complexity penalty | Simpler linear models (LR, logistic regression) |
| **Resampling Methods** | Estimate out-of-sample error by splitting data | All model types; most practical setting |

**Probabilistic measures** include:
- **AIC** (Akaike Information Criterion)
- **BIC** (Bayesian Information Criterion)
- **MDL** (Minimum Description Length)
- **SRM** (Structural Risk Minimization)

> Training error is *optimistically biased*; probabilistic measures add a complexity penalty to compensate.

**Resampling methods** include:
- Random train/test splits
- **Cross-validation** (k-fold, LOO, etc.) — most widely used
- Bootstrap

> "Probably the simplest and most widely used method for estimating prediction error is cross-validation." — *The Elements of Statistical Learning*, 2017

#### Key Takeaways for Intelligent Systems

- Never judge a model on training error alone — always estimate out-of-sample performance.
- Select among **pipelines**, not just algorithms; data preprocessing is part of what is being compared.
- When data is sufficient: use **train / validation / test** split. When data is limited: use **cross-validation**.
- Probabilistic criteria (AIC/BIC) are tractable for linear models; resampling (CV) is the universal fallback.

---

### 3. Arlot, S. & Celisse, A. (2010). A Survey of Cross-Validation Procedures for Model Selection

**Citation:** Arlot, S. & Celisse, A. (2010). A survey of cross-validation procedures for model selection. *Statistics Surveys*, 4, 40–79. https://projecteuclid.org/download/pdfview_1/euclid.ssu/1268143839

**Purpose:** Provides a rigorous theoretical and empirical survey of cross-validation methods, establishing when and why they work for model selection.

#### 1. Cross-Validation Philosophy (Section 4.1)

As noted by Larson (1931), **training and evaluating a model on the same data yields an overoptimistic result** — the resubstitution error is biased downward (overfitting).

CV's solution: **split the data** so the training sample and the validation sample are independent.
- **Training sample** → used to fit the algorithm
- **Validation sample** → used to estimate its true risk (generalisation error)

Averaging estimates over multiple splits gives a **cross-validation estimate** of the risk.

**Why CV is universal:**
- Assumes only that data are identically distributed (i.i.d.) and that training/validation splits are independent
- Applies to regression, classification, density estimation — almost any statistical framework
- Most other model selection procedures (e.g. Cp/Mallows) are framework-specific

#### 2. From Validation to Cross-Validation (Section 4.2)

| Method | Description |
|--------|-------------|
| **Hold-out (simple validation)** | Single train/validation split. Fast but high variance estimate. |
| **Cross-validation (general)** | Average over B splits of the data. Lower variance, more reliable. |

#### 3. Classical CV Examples (Section 4.3)

##### 3a. Exhaustive Data Splitting (Section 4.3.1)

**Leave-One-Out (LOO):**
- Training set size: n − 1 (one data point is left out at a time)
- Each of the n data points is successively the validation point
- Requires **n model fits** — computationally expensive for large datasets
- Essentially unbiased estimate of the risk, but high variance

$$\hat{L}^{LOO}(A; D_n) = \frac{1}{n} \sum_{j=1}^{n} \gamma\left(A(D_n^{(-j)}); \xi_j\right)$$

**Leave-p-Out (LPO):**
- Exhaustive CV where p data points are left out each time
- Considers all C(n, p) subsets — computationally infeasible for large p
- LPO with p = 1 = LOO

##### 3b. Partial Data Splitting (Section 4.3.2)

**V-Fold Cross-Validation (VFCV) — also called K-Fold CV:**
- Data is partitioned into V subsamples of approximately equal size (≈ n/V each)
- Each subsample successively plays the role of the validation set
- Requires only **V model fits** — much more efficient than LOO
- Introduced by Geisser (1975) as a computationally tractable alternative to LOO
- **VFCV with V = n is equivalent to LOO**

| V (K) value | Training size | Validation size | Notes |
|-------------|---------------|-----------------|-------|
| V = 2 | n/2 | n/2 | High bias, low compute |
| V = 5 | 4n/5 | n/5 | Common practical choice |
| V = 10 | 9n/10 | n/10 | Common practical choice |
| V = n (LOO) | n − 1 | 1 | Unbiased, but O(n) compute |

Other partial splitting methods: **BICV** (Balanced Incomplete CV), **RLT** (Repeated Learning-Testing), **MCCV** (Monte-Carlo CV — allows repeated splits).

#### Key Takeaways for Intelligent Systems

- Use CV to get an unbiased estimate of how well your model generalises to unseen data.
- **LOO**: use when data is very small (maximises training data per fold); expensive for large n.
- **K-Fold (V-Fold)**: default practical choice — k = 5 or k = 10 is standard. Balances bias and compute cost.
- K-Fold with K = n collapses to LOO; K = 1 is invalid (no validation set).
- For model selection in ISY503: use **5-fold or 10-fold CV** to compare classifiers on your dataset.

---

### 4. Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization

**Citation:** Feurer, M. & Hutter, F. (2019). Hyperparameter optimization. In F. Hutter, L. Kotthoff & J. Vanschoren (Eds), *Automated machine learning* (pp. 3–34). Cham, Switzerland: Springer. https://link.springer.com/chapter/10.1007/978-3-030-05318-5_1

**Purpose:** Surveys hyperparameter optimisation (HPO) methods, covering the formulation of HPO as a blackbox problem and the practical search strategies used to find optimal configurations.

#### 1. What Are Hyperparameters?

**Hyperparameters** are model settings that are not learned from data during training — they must be set *before* training begins. Examples:
- Number of neighbours K in KNN
- Max depth of a Decision Tree
- Regularisation strength (C, λ) in SVM or logistic regression
- Learning rate and batch size in gradient-based methods

**Hyperparameter optimisation (HPO)** = finding the configuration of hyperparameters that minimises a loss (or maximises performance) on a validation set.

> "Babysitting your model to make it even better." — ISY503 Module 3 overview

#### 2. HPO as a Blackbox Problem (Section 1.3)

HPO treats the mapping from hyperparameter configuration → validation performance as a **blackbox function**: expensive to evaluate (requires training a full model), non-convex, and with no accessible gradient. Global optimisation algorithms are preferred.

#### 3. Model-Free Blackbox Methods (Section 1.3.1)

**Grid Search:**
- User specifies a finite set of values per hyperparameter; evaluates the **Cartesian product** of all combinations
- Suffers from the **curse of dimensionality**: evaluations grow exponentially with the number of hyperparameters
- For N hyperparameters with budget B, only B^(1/N) distinct values per hyperparameter can be explored

**Random Search:**
- Samples configurations **at random** until a computational budget is exhausted
- Outperforms grid search when hyperparameters have **unequal importance** (many real-world cases)
- For N hyperparameters with budget B, explores **B distinct values per hyperparameter** (vs. B^(1/N) for grid)
- Advantages: easy to parallelise, no communication overhead, flexible budget allocation

| Method | Values explored per HP (budget B, N HPs) | Best when |
|--------|-------------------------------------------|-----------|
| Grid search | B^(1/N) | All HPs equally important, small N |
| Random search | B | Some HPs more important than others |

**Population-Based Methods:**
- Genetic algorithms, evolutionary strategies (e.g. CMA-ES), particle swarm optimisation
- Maintain a *population* of configurations, improve via mutations and crossover
- Embarrassingly parallel (N configurations evaluated simultaneously)
- CMA-ES is competitive in black-box benchmarks

#### 4. Bayesian Optimisation (Section 1.3.2)

**Bayesian optimisation** is state-of-the-art for HPO of expensive blackbox functions:
- Builds a **surrogate model** (e.g. Gaussian Process) of the objective function
- Uses an **acquisition function** to decide where to evaluate next, balancing exploration and exploitation
- Shown to outperform grid/random search for tuning deep neural networks
- Handles constraints and multi-objective optimisation

#### Key Takeaways for Intelligent Systems

- Always tune hyperparameters — the default configuration is rarely optimal.
- **Grid search**: systematic but inefficient for high-dimensional hyperparameter spaces.
- **Random search**: preferred baseline when hyperparameter importance is unequal (the common case).
- Combine CV with HPO: tune hyperparameters using cross-validation to avoid overfitting to the validation set.
- For ISY503 practical work: use `GridSearchCV` or `RandomizedSearchCV` from scikit-learn with k-fold CV.

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.svm import SVC

# Grid search example
param_grid = {'C': [0.1, 1, 10], 'kernel': ['rbf', 'linear']}
grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring='f1')
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)

# Random search example (more efficient for larger spaces)
from scipy.stats import loguniform
param_dist = {'C': loguniform(0.01, 100), 'kernel': ['rbf', 'linear']}
rand_search = RandomizedSearchCV(SVC(), param_dist, n_iter=20, cv=5, random_state=42)
rand_search.fit(X_train, y_train)
print(rand_search.best_params_)
```

---

## Module Summary: Core Vocabulary

| Term | Definition |
|------|------------|
| Supervised Learning | Learns a mapping from inputs to outputs using labelled training data. |
| Classification | Supervised task where the output is a discrete class label. |
| Regression | Supervised task where the output is a continuous numeric value. |
| Overfitting | Model fits training data too closely; fails to generalise to unseen data. |
| Hyperparameter | Model setting chosen *before* training; not learned from data (e.g. K in KNN, C in SVM). |
| Model Selection | Process of choosing the best model/pipeline from a set of candidates. |
| Model Assessment | Estimating how well the chosen model will generalise to new data. |
| Cross-Validation (CV) | Estimates generalisation error by averaging performance over multiple train/validation splits. |
| K-Fold CV | Splits data into K folds; each fold serves as validation once; requires K model fits. |
| Leave-One-Out (LOO) | CV where n−1 samples train the model and 1 is validated; unbiased but O(n) compute. |
| Bagging | Bootstrap aggregating — trains each model on a random data subset; used by Random Forest to reduce variance. |
| Ensemble | Combines predictions from multiple models to improve accuracy and reduce variance. |
| Grid Search | Evaluates all hyperparameter combinations (Cartesian product); grows exponentially with number of HPs. |
| Random Search | Randomly samples hyperparameter configs; outperforms grid search when HPs have unequal importance. |
| Bayesian Optimisation | Builds a surrogate model of the objective function to guide the next evaluation; state-of-the-art for HPO. |
| AIC / BIC | Probabilistic model selection criteria; penalise model complexity to correct for optimistic training error. |

---

## Activities

### Activity 1: Extra Machine Learning Models

```bash
Linear Regression: Predicts a continuous numeric output as a weighted sum of input features; fits a line/plane by minimising mean squared error. Supervised regression algorithm — interpretable coefficients, fast to train, assumes linear relationship.

Principal Component Analysis (PCA): Unsupervised dimensionality reduction technique that projects data onto orthogonal axes (principal components) ordered by explained variance. Reduces noise, removes correlated features, and compresses data — not a classifier but a preprocessing step.

AdaBoost (Adaptive Boosting): Sequential ensemble that trains weak learners (typically shallow trees) where each iteration reweights misclassified samples so the next learner focuses on harder cases. Final prediction is a weighted vote of all learners; sensitive to outliers and noise.

XGBoost (Extreme Gradient Boosting): Highly optimised gradient boosting framework that builds trees sequentially to minimise a regularised objective (L1/L2). Handles missing values natively, supports parallelisation, and consistently dominates tabular ML benchmarks.
```

#### Activity 2: Extra Machine Learning Models
```bash
K-Fold Cross-Validation is a resampling technique that partitions the dataset into K equal folds; each fold serves as the validation set once while the remaining K-1 folds train the model. Performance is averaged across all K iterations to produce a robust generalisation estimate.

K = 1 means: Invalid — all data is used for training with nothing reserved for validation; no generalisation estimate is possible.
K = 2 means: Half the data trains, half validates per fold; high bias (model sees only 50% of data each round), but fast to compute. Rarely used in practice.
K = 5 means: 80% trains, 20% validates per fold; the standard practical default — good bias-variance tradeoff at reasonable compute cost.
K = 10 means: 90% trains, 10% validates per fold; most common choice in the literature; slightly lower bias than K=5 but higher compute.
K = N–2 means: Near-LOO — only 2 samples left out per fold; almost all data trains each model; very low bias but extremely high compute; rarely justified.
K = N–1 means: Equivalent to Leave-One-Out (LOO); n-1 samples train, 1 validates; maximally unbiased estimate but requires n model fits — O(n) compute.
```

---

## Class Notes

### 04/03/2026 - 11:30AM

#### Exercises

1. Predict if an email is spam or not spam: `R:` Naive Bayes classifier
2. Estimate the price of a used car: `R:` Linear Regression
3. Predict whether a patient has diabetes (Yes/No): `R:` Logistic Regression
4. Predict the number of products sold next week: `R:` Linear Regression
5. Identify a fruit as apple, banana, or orange: `R:` Decision Tree
6. Forecast the temperature for tomorrow: `R:` Linear Regression
7. Predict whether a customer will churn (leave the service) or stay: `R:` Logistic Regression
8. Predict the salary of a professional based on experience, education, and location: `R:` Linear Regression
9. Classify images of animals into categories like cat, dog, or horse: `R:` Random Forest
10. Predict the number of likes a social media post will get based on text and image content: `R:` Linear Regression
11. Determine whether a bank transaction is fraudulent: `R:` Isolation Forest
12. Predict a student’s final exam score based on performance in assignments and attendance: `R:` Linear Regression
13. Classify a movie review as positive, neutral, or negative: `R:` Naive Bayes classifier
14. Estimate the remaining battery life of a smartphone in minutes: `R:` Linear Regression

##### Feedback on Exercise Answers

✅ Correct and well-matched:
- 1 (Naive Bayes — spam),
- 2 (LR — car price),
- 3 (Logistic — diabetes),
- 5 (DT — fruit),
- 7 (Logistic — churn),
- 8 (LR — salary),
- 10 (LR — likes),
- 12 (LR — exam score),
- 13 (Naive Bayes — sentiment),
- 14 (LR — battery life)                                                                                                                                                                                 
⚠️  Partially correct / worth noting:

#4 & #6 — Linear Regression for next-week sales / tomorrow's temperature
Linear Regression is technically valid (continuous output), but both are inherently time series problems. LR ignores temporal ordering and trends. In practice you'd use ARIMA, or LR with lag
features. For this module's scope it's acceptable, but flag it: "LR as a baseline; time series methods preferred."

#9 — Random Forest for image classification
Correct algorithm class (multi-class classification), but Random Forest on raw pixel features performs poorly in practice. Images need CNNs. If this is a structured feature set (colour histogram,
shape descriptors, etc.), RF works. Worth adding: "RF on extracted features; CNN for raw image input."

#11 — Isolation Forest for fraud detection
Good — but Isolation Forest is an unsupervised anomaly detection model, which assumes you have no labelled fraud data. If labels exist (which they usually do in production), supervised classifiers
(XGBoost, Random Forest) are standard. Both are valid depending on context — worth stating the assumption.