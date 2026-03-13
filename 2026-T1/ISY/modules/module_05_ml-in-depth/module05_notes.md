# Module 05 — Machine Learning In-Depth
## ISY503 Intelligent Systems

---

## Task List

| # | Resource / Activity | Type | Status |
|---|---------------------|------|--------|
| R1 | Pierson (2019) — Grouping ML algorithms | Video (Lynda) | 🔥 WIP — needs manual watch |
| R2 | Dave (2018) — Regression in Machine Learning | Article (PDF) | ✅ Read + Reviewed |
| R3 | Cuesta (2017) — Text Classification Ch.4 | Book chapter (PDF) | ✅ Read + Reviewed |
| R4 | Ross (2017) — Unsupervised ML capabilities | Article (PDF) | ✅ Read + Reviewed |
| R5 | WTF is the Bias-Variance Tradeoff? | Infographic (PDF) | ✅ Read + Reviewed |
| R6 | Zhao (2019) — SVM Visual Explanation | Video (YouTube) | 🔥 WIP — needs manual watch |
| R7 | Maini (2017) — ML for Humans Pt 2.1 | Article (PDF) | ✅ Read + Reviewed |
| R8 | Maini (2017) — ML for Humans Pt 3 | Article (PDF) | ✅ Read + Reviewed |
| A1 | Azure classification tutorial | Hands-on (MS Learn) | 🕐 To-Do |

---

## Key Highlights

---

### R2 — Dave (2018): Regression in Machine Learning

#### 1. What is Regression?

**Regression** is a **supervised learning** technique used to predict **continuous values**. Unlike classification (which assigns discrete labels), regression models output a quantity — e.g. predicting house prices, salaries, or stock values.

#### 2. Five Types of Regression

| Type | How it works | When to use |
|------|-------------|-------------|
| **Simple Linear Regression** | Fits Y = a + bX using least-squares | Linear relationship between X and Y |
| **Polynomial Regression** | Transforms features to degree n (e.g. Y = a + bX + cX²), still linear model | Curved relationships; watch for overfitting at high degrees |
| **Support Vector Regression (SVR)** | Finds hyperplane with max margin; fits error within a threshold (epsilon tube) | When margin-fitting is preferable to minimising all errors |
| **Decision Tree Regression** | Partitions data via ID3 (maximising **standard deviation reduction** instead of information gain) | Non-linear, interpretable relationships |
| **Random Forest Regression** | Ensemble of decision trees; averages predictions across all trees | When single trees overfit; generally more robust |

#### 3. Key Mechanics

- **Cost function (MSE):** Mean Squared Error — average squared difference between actual and predicted values. Training minimises this.
- **Gradient Descent:** Iterative optimisation — start with random coefficients, compute gradient, update coefficients, repeat until cost is minimised.
- **Coefficient of Deviation (CV):** Used in decision trees to decide when to stop branching (prevents overfitting).
- **Random Forest vs Decision Tree:** Random Forest creates random subsets of features and builds smaller trees → reduces overfitting.

> In regression: leaf node value = **mean** of branch. In classification: leaf node value = **mode** of branch.

#### Key Takeaways for ISY503
- Regression = supervised + continuous output. Classification = supervised + discrete output.
- MSE + Gradient Descent are the engine of most regression training.
- Polynomial degree too high → overfitting. Use CV/Random Forest to counter.
- SVR trades MSE minimisation for a margin-tolerance approach — links directly to SVM concepts (R6).

---

### R3 — Cuesta (2017): Text Classification (Ch. 4, Practical Data Analysis)

#### 1. What is Classification?

A **classifier** automatically assigns a **category** to an input based on learned patterns from labelled training data. Tom Mitchell's framing: *"How can we build computer systems that automatically improve with experience?"*

Two problem types:
- **Binary classification** — two categories (e.g. Spam / Not Spam)
- **Multiclass classification** — many categories (e.g. Positive / Neutral / Negative)

Common algorithms: SVM, neural networks, decision trees, **Naive Bayes**, hidden Markov models.

#### 2. Supervised Classification Pipeline

```
Training Data → Feature Extraction → Trained Classifier → Class Label
New Text     → Feature Extraction ↗
```

Accuracy is tested against a hand-classified **test set** (split from training data).

#### 3. Bayesian Classification

**Bayes Theorem:** `P(A|B) = P(B|A) · P(A) / P(B)`

- **Prior probability** P(A): likelihood before observing data
- **Posterior probability** P(A|B): updated likelihood after observing data B

#### 4. Naive Bayes Algorithm

- Simplest Bayesian classifier — assumes **attribute independence** (independent feature model)
- Efficient to train; widely used for **text classification**
- For spam detection: multiply word probabilities per category
  - `P(category | word₁, word₂, ..., wordₙ) = P(category) × ∏ P(word | category)`

#### 5. Email Subject Line Tester — Practical Application

- Dataset: **SpamAssassin** (spam, easy ham, hard ham)
- Features: word frequency (>3 characters, excluding stop words)
- Implementation: Python `training()` and `classifier()` functions
- Results with training set size:

| Training size | Accuracy |
|--------------|---------|
| 200 | 82% |
| 300 | 85% |
| 500 | 87% |
| 800 | 92% |

> **Optimal training threshold: ~700 texts → 92% accuracy.** More data = better performance, but gains diminish.

#### Key Takeaways for ISY503
- Classification assigns discrete labels; Naive Bayes is a fast, probabilistic baseline.
- Feature extraction (word frequency vectors) is critical — quality features = quality classifier.
- More training data generally improves performance, but there are diminishing returns.
- Foundational for **Assessment 2** (text/data classification task).

---

### R4 — Ross (2017): Understanding the Real Capabilities of Unsupervised ML

#### 1. Two Types of Machine Learning

| Type | Also called | Input | Output | Examples |
|------|-------------|-------|--------|---------|
| **Trained** | Supervised | Input + Output data | Classification or Regression | Siri, Facebook photo tagging, weather forecasts |
| **Untrained** | Unsupervised | Input data only | Clusters / patterns | Anomaly detection, customer segmentation |

#### 2. Supervised Learning Recap

- **Classification:** machine predicts discrete responses (spam or not spam). Learns from labelled input.
- **Regression:** machine predicts continuous responses (e.g. stock price). Identifies patterns in sequences.

#### 3. Unsupervised (Untrained) Learning

- Requires only **input data** — no predefined labels or output categories.
- Most commonly implements **cluster analysis**: groups data so items within a cluster are more similar to each other than to items in other clusters.
- The machine determines what is **"normal"** for a dataset and flags anomalies.
- Does **not** label anything as "bad" — it identifies what is *different* from the rest.

#### 4. Real-World Application: Cybersecurity

- Tracks login behaviour (when, where, from what device).
- Creates user behaviour clusters over time.
- Flags logins that fall significantly outside the established model.
- Example: an employee logs in from a new city → may or may not be flagged depending on cluster behaviour of peer group.

#### 5. The Human Element

- ML cannot replace human judgement — it still needs:
  - Humans to decide **which data points are meaningful**
  - Human verification of results
- "In order for the machine to have actual knowledge, it needs your intelligence."

#### Key Takeaways for ISY503
- Unsupervised learning = no labels, self-organising clusters.
- Useful when you don't know what categories exist in advance.
- Cybersecurity, customer segmentation, anomaly detection are prime use cases.
- "Garbage in, garbage out" — ML quality depends on input data quality.

---

### R5 — WTF is the Bias-Variance Tradeoff?

#### 1. Why it Matters

The **Bias-Variance Tradeoff** is one of the most important concepts for supervised ML and predictive modelling. It breaks down prediction error into diagnosable components.

**Total Error = Bias² + Variance + Irreducible Error**

| Error type | What it is | Can be reduced? |
|-----------|-----------|----------------|
| **Bias²** | Error from wrong assumptions in the algorithm | Yes — choose a more flexible model |
| **Variance** | Error from sensitivity to specific training data | Yes — choose a simpler/regularised model |
| **Irreducible Error** | Noise inherent in the data | No — inherent randomness or mis-framed problem |

#### 2. Bias Explained

- **Bias** = the difference between your model's expected predictions and the true values.
- Caused by algorithms that are **too rigid** (limited flexibility) to learn complex signals.
- Result: **underfitting** — the model can't capture the underlying trend even with more data.
- Example: fitting a linear regression to a non-linear dataset.

#### 3. Variance Explained

- **Variance** = an algorithm's sensitivity to specific training data sets.
- High variance algorithms produce drastically different models with different training sets.
- Result: **overfitting** — the model memorises noise rather than learning the signal.
- Example: an unconstrained polynomial that snakes through every data point.

#### 4. The Tradeoff

| | High Bias, Low Variance | High Variance, Low Bias |
|---|---|---|
| **Behaviour** | Consistent but inaccurate on average | Accurate on average but inconsistent |
| **Algorithm type** | Less complex, parametric (linear, Naive Bayes) | More complex, non-parametric (decision trees, KNN) |
| **Problem** | Underfitting | Overfitting |

> The tradeoff exists because an algorithm cannot simultaneously be **more complex** and **less complex**. Within each family there are further tradeoffs (e.g. regularisation for regression, pruning for decision trees).

#### 5. Optimal Balance

A proper ML workflow finds the optimal point where Total Error is minimised:

- Separate training and test sets
- Try appropriate algorithms
- Fit model parameters
- Tune impactful hyperparameters
- Use proper performance metrics
- Apply systematic cross-validation

#### Key Takeaways for ISY503
- Bias = underfitting. Variance = overfitting. Goal = minimise both simultaneously.
- Total error has three components; only bias and variance are controllable.
- Ensemble methods (e.g. Random Forests) often reduce both compared to simpler models.
- Always try multiple algorithms — no single model wins on every problem (No Free Lunch theorem).

---

### R7 — Maini (2017): Machine Learning for Humans, Part 2.1 — Supervised Learning

#### 1. Supervised Learning Framework

In supervised learning: start with **training examples** (X) and associated correct **labels** (Y). The algorithm learns the relationship f such that Y = f(X) + ε.

- **ε (epsilon):** irreducible error — inherent noise/randomness in the phenomena
- The model is then applied to **unlabeled test data** to predict Y.

**Two tasks:**
- **Regression:** predict a continuous numerical value (e.g. "How much will that house sell for?")
- **Classification:** assign a label (e.g. "Is this a picture of a cat or a dog?")

#### 2. Linear Regression (Ordinary Least Squares)

Model: `ŷ = β0 + β1 * x + ε`

- β0 = y-intercept, β1 = slope
- **Parametric method** — assumes linear relationship between X and Y
- Goal: learn β0 and β1 that **minimise prediction error**

Two steps to find best parameters:
1. Define a **cost/loss function** measuring inaccuracy
2. Find parameters that **minimise loss**

**MSE Cost Function:**
```
Cost = Σ((β1*xi + β0 - yi)²) / (2*n)
```

#### 3. Gradient Descent

When closed-form solutions are infeasible (complex cost functions), use **gradient descent**:

1. Make initial guess of β0 and β1
2. Compute **partial derivatives** of cost function: [dz/dβ0, dz/dβ1]
3. Update parameters in the **opposite direction** of the gradient (walk downhill)
4. Repeat until **converged** (algorithm reaches minimum loss)

> Gradient descent is foundational to neural networks and used by scikit-learn/TensorFlow.

#### 4. Overfitting and Regularisation

- **Overfitting:** model learns training data too perfectly, doesn't generalise to new data.
- **Underfitting:** model too simple to capture the underlying trend.

**Two ways to combat overfitting:**
1. **More training data** — harder to overfit with more examples
2. **Regularisation** — add a penalty term to the cost function:
   ```
   Cost = MSE + λ * Σβi²
   ```
   - **λ (lambda):** hyperparameter controlling regularisation strength
   - Tuned via **cross-validation** (hold out portion of training data)

> Goal of supervised learning: predict Y as accurately as possible on **unseen test data**.

#### Key Takeaways for ISY503
- Linear regression is the foundational parametric algorithm: learn β parameters via gradient descent.
- Cost function (MSE) + gradient descent = the engine of supervised learning.
- Regularisation (λ penalty) is the primary tool against overfitting.
- Cross-validation selects optimal hyperparameters without touching the test set.

---

### R8 — Maini (2017): Machine Learning for Humans, Part 3 — Unsupervised Learning

#### 1. Unsupervised Learning Overview

Starts with **unlabelled data** (no Y). Goal: find underlying structure.

Two main tasks:
- **Clustering** — group data by similarity
- **Dimensionality reduction** — compress data while preserving structure

> Performance is often subjective and domain-specific (unlike supervised learning with clear accuracy metrics).

#### 2. k-Means Clustering

Groups data into **k clusters** defined by **centroids**.

**Algorithm steps:**
1. **Define k centroids** (initialised randomly)
2. **Assign each point** to its nearest centroid (using Euclidean distance or other metric)
3. **Move centroids** to the average position of all points in their cluster
4. **Repeat steps 2–3** until centroids stop moving (convergence)

| k parameter | Effect |
|------------|--------|
| Larger k | Smaller, more granular clusters |
| Smaller k | Larger, broader clusters |

**Real-world example:** Acxiom's Personicx segments U.S. households into 70 clusters for targeted advertising — used centroid clustering + PCA.

#### 3. Hierarchical Clustering

Builds a **hierarchy of clusters** (useful when you want flexibility in the number of clusters).

**Algorithm steps:**
1. Start with N clusters (one per data point)
2. Merge the two closest clusters
3. Recompute distances between clusters
4. Repeat until 1 cluster remains → produces a **dendrogram**
5. Draw a horizontal cut line to select desired number of clusters

> Average-linkage clustering: distance between clusters = average distance between all their members.

#### 4. Dimensionality Reduction

Reduces complexity while maintaining as much structure/variance as possible.

**Principal Component Analysis (PCA):**
- Selects the most significant **basis vectors** (principal components) that capture maximum variance
- Remaps the data space to a smaller, more compressible representation
- Principal components ordered by how much variance they explain

**Singular Value Decomposition (SVD):**
- Decomposes matrix A (m×n) into: **A = U × Σ × V**
  - U = m×r, Σ = r×r (diagonal — singular values), V = r×n
- Drop the smallest singular values → compressed but still useful representation
- Example: first 50 singular values of a dog image = 85% of total image information; rank-30 dog = 5× fewer values with minimal quality loss

| Technique | Use case |
|-----------|---------|
| **PCA** | Feature reduction, visualisation, pre-processing |
| **SVD** | Matrix factorisation, recommender systems, image compression |

> Unsupervised learning is often used as **preprocessing** for supervised learning (e.g. PCA/SVD before feeding data to a neural network).

#### Key Takeaways for ISY503
- k-means: choose k, assign to nearest centroid, recompute, repeat — simple and powerful.
- Hierarchical clustering: flexible cluster count; dendrogram reveals structure.
- PCA/SVD: reduce dimensions while preserving the most variance — essential for high-dimensional datasets.
- Unsupervised methods often precede supervised pipelines as data preprocessing steps.
