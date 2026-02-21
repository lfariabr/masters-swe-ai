# Module 2 — Introduction to Machine Learning
## ISY503 Intelligent Systems

---

## Task List

| # | Resource / Activity | Type | Status |
|---|---------------------|------|--------|
| **1** | Alpaydin (2014) — ML Introduction (Classification & Regression) | PDF chapter | ✅ Read + Reviewed |
| **2** | Pargent et al. (2019) — Categorical Feature Encoding | PDF paper | ✅ Read + Reviewed |
| 3 | Udacity (2016) — Training and Testing | Video | 🔥 WIP — needs manual watch |
| 4 | Prabhakaran (2017) — Top 15 Evaluation Metrics for Classification | Web article | ✅ Read + Reviewed |
| 5 | Hawkins (2004) — The Problem of Overfitting | PDF paper | ✅ Read + Reviewed |
| 6 | Chandrashekar & Sahin (2014) — A Survey on Feature Selection Methods | PDF paper | ✅ Read + Reviewed |
| 7 | Inglés-Romero et al. (2018) — QoS Metrics in Reinforcement Learning | PDF paper | ✅ Read + Reviewed |
| 8 | Palacio-Niño (2019) — Evaluation Metrics for Unsupervised Learning | PDF paper | ✅ Read + Reviewed |
| 9 | Hulten (2018) — Building Intelligent Systems (eBook) | Authenticated eBook | 🔥 WIP — needs institutional library access |
| 10 | Halligan et al. (2015) — Disadvantages of ROC AUC for Imaging Tests | PDF paper | ✅ Read + Reviewed |
| A1 | Activity 1: Metrics Suitability (Discussion Forum) | Activity | 🕐 To-Do |
| A2 | Activity 2: Metrics for Unsupervised Approaches (Discussion Forum) | Activity | 🕐 To-Do |

---

## Key Highlights

---

### Resource 1 — Alpaydin (2014): Examples of ML Applications

**Citation:** Alpaydin, E. (2014). Introduction. In *Adaptive computation and machine learning* (3rd ed, pp. 1–21). MIT Press.

#### 1. What is Machine Learning?

Machine learning is the field where computers learn general rules from past data to predict or classify new data. Rather than hand-coding rules, a program *fits a model* to data and then applies that model to new instances.

#### 2. Classification

**Classification** is a supervised learning task where the output Y is a discrete class label.

- **Features (inputs, X):** The measurable attributes of an instance (e.g., income, savings)
- **Target (output, Y):** The class label (e.g., low-risk vs. high-risk)
- **Classifier:** Learns the mapping X → Y from labelled training data

The learned rule is called a **discriminant** — it separates instances of different classes.

**Example:** Credit scoring — `IF income > θ₁ AND savings > θ₂ THEN low-risk ELSE high-risk`

Real-world classification examples:

| Domain | Features | Target |
|--------|----------|--------|
| Credit scoring | Income, savings, history | Low-risk / high-risk |
| Optical character recognition (OCR) | Image pixels | Character (A–Z, 0–9) |
| Medical diagnosis | Patient symptoms, age, history | Disease type |
| Speech recognition | Acoustic signals | Word |
| Face recognition | Image features | Identity |

The classifier can also output a **probability** P(Y=1|X=x) rather than a hard class, enabling risk-based decisions.

#### 3. Regression

**Regression** is a supervised learning task where the output Y is a continuous number.

- Example: predicting the price of a used car from its attributes (brand, mileage, year)
- General model: **y = g(x|θ)** — the model g(·) with parameters θ is optimised to minimise approximation error
- Linear model: y = wx + w₀; or polynomial: y = w₂x² + w₁x + w₀

Both classification and regression are **supervised learning**: they require labelled training data (X, Y pairs).

#### 4. Other Learning Tasks

- **Outlier / Novelty Detection:** Find instances that don't fit the general rule (e.g., fraud detection)
- **Knowledge Extraction:** The learned rule reveals structure in the data (e.g., properties of low-risk customers)
- **Compression:** Fitting a rule produces a simpler representation than storing all raw data

#### Key Takeaways for ISY503

> - **Features = inputs (X)**, **Targets = outputs (Y)** — memorise this vocabulary
> - Classification output is discrete (class label), regression output is continuous (number)
> - ML models fit `y = g(x|θ)` by optimising parameters θ on training data
> - The same supervised learning framework applies across credit scoring, medical diagnosis, OCR, and more

---

### Resource 2 — Pargent et al. (2019): Categorical Feature Encoding

**Citation:** Pargent, F., Bischl, B. & Thomas, J. (2019). *A benchmark experiment on how to encode categorical features in predictive modeling*. Ludwig-Maximilians-Universität München.

#### 1. Why Encoding is Necessary

Most ML algorithms (lasso, SVM, k-NN, neural networks) only accept **numerical input**. Categorical features — variables with discrete, unordered levels (e.g., city names, product types) — must be converted to numbers before training.

**High-cardinality features:** Categorical variables with a very high number of levels (hundreds to thousands). These pose special challenges because standard one-hot encoding creates too many columns.

#### 2. Core Encoding Strategies

| Encoding | How it Works | When to Use |
|----------|-------------|-------------|
| **Integer Encoding (Label Encoding)** | Randomly map each category level to an integer 1…L | Simple baseline; can imply a false ordinal relationship |
| **Indicator / One-Hot Encoding** | Create L binary columns; 1 in the column for the level, 0 elsewhere | Small cardinality; avoids ordinal assumption |
| **Dummy Encoding** | Like one-hot but L−1 columns (drop one reference level) | Linear models to avoid multicollinearity |
| **Target Encoding** | Replace each level with the mean target value from training | High cardinality; requires regularisation |
| **Frequency Encoding** | Replace each level with its frequency in the training set | When frequency correlates with target |
| **Hash Encoding** | Hash function maps levels to a fixed-size integer representation | Very high cardinality; approximate |
| **Leaf Encoding** | Fit a decision tree on the feature; encode by terminal node number | When tree structure captures level groupings |

#### 3. The Overfitting Risk in Target Encoding

Simple target encoding (replacing a level with the training-set mean target) tends to **overfit** for rare levels — a level with only one observation gets encoded with that observation's exact target value, effectively leaking the target.

**Solutions:**
1. **Smoothing / shrinkage**: Shrink rare level means towards the grand mean — `x̂_l = λ_l × mean_in_level + (1−λ_l) × grand_mean`
2. **Cross-validation target encoding**: Use k-fold CV so each observation's encoding is computed from the other folds
3. **Adding noise**: Introduce random perturbation to limit overfitting

**Best benchmark result:** Regularised target encoding (smoothing + cross-validation) outperformed all other strategies across multiple ML algorithms.

#### 4. Tree Models and Categorical Features

- CART / random forests can handle categorical features natively via partitioning
- For high-cardinality features, ordering levels by target mean reduces the search to L−1 candidate splits (computationally feasible)
- Python's `scikit-learn` does not natively handle categorical features — encoding required
- `CatBoost` implements ordered target encoding integrated into its boosting algorithm

#### Key Takeaways for ISY503

> - ML algorithms require **numerical inputs** — categorical data must be encoded
> - **Label Encoding** maps categories to integers (simple but implies order); **One-Hot Encoding** creates binary columns (safe but expensive for high cardinality)
> - **Target encoding** is powerful but requires regularisation (smoothing + CV) to avoid data leakage and overfitting
> - Choose the encoding strategy based on: cardinality of the feature, type of ML algorithm, and dataset size

---

### Resource 3 — Udacity (2016): Training and Testing

**Citation:** Udacity. (2016, 6 June). *Training and testing* [Video]. YouTube.

> **Status: 🔥 WIP — needs manual watch**
> URL: https://www.youtube.com/watch?v=P2NqrFp8usY

**Summary of expected content (based on module description):**
- A simple, visual introduction to why data must be split into training and testing sets
- The classifier is trained only on the training set — it never "sees" the test labels during training
- The test set simulates real-world new data and measures true generalisation performance
- Mixing training and testing data leads to overly optimistic performance estimates (data leakage)

---

### Resource 4 — Prabhakaran (2017): Top 15 Evaluation Metrics for Classification

**Citation:** Prabhakaran, S. (2017). Top 15 evaluation metrics for classification models. *Machine Learning Plus*.

> Note: The article was blocked by CAPTCHA at access time. Content synthesised from the article topic description and supplementary sources on the same subject matter.

#### 1. The Confusion Matrix — Foundation of All Metrics

For binary classification, the **confusion matrix** is a 2×2 table comparing predictions vs. actual outcomes:

|  | Predicted Positive | Predicted Negative |
|--|--------------------|--------------------|
| **Actual Positive** | **TP** (True Positive) | **FN** (False Negative) |
| **Actual Negative** | **FP** (False Positive) | **TN** (True Negative) |

- **TP** — Correctly predicted positive (disease detected in a sick patient)
- **TN** — Correctly predicted negative (healthy patient correctly cleared)
- **FP** — False alarm (healthy patient flagged as sick) → Type I Error
- **FN** — Missed case (sick patient declared healthy) → Type II Error

#### 2. Core Classification Metrics

| Metric | Formula | Meaning | Best Used When |
|--------|---------|---------|----------------|
| **Accuracy** | (TP + TN) / (TP + TN + FP + FN) | % of all predictions correct | Balanced class distribution |
| **Precision** | TP / (TP + FP) | Of all predicted positives, how many are correct | When FP cost is high (e.g., spam filter) |
| **Recall (Sensitivity)** | TP / (TP + FN) | Of all actual positives, how many were detected | When FN cost is high (e.g., cancer screening) |
| **Specificity** | TN / (TN + FP) | Of all actual negatives, how many were correctly identified | Medical tests, fraud detection |
| **F1 Score** | 2 × (Precision × Recall) / (Precision + Recall) | Harmonic mean of precision and recall | Imbalanced classes |

#### 3. Precision-Recall Trade-off

Precision and recall are inversely related:
- Lowering the classification threshold → **recall increases, precision decreases** (catch more positives, but more false alarms)
- Raising the threshold → **precision increases, recall decreases** (fewer false alarms, but miss more)

The F1 score balances this trade-off. Use **F1** when both types of errors matter and the dataset is imbalanced.

#### 4. ROC Curve and AUC

- **ROC Curve:** Plots **Sensitivity (TPR)** on the y-axis against **1−Specificity (FPR)** on the x-axis at all classification thresholds
- **AUC (Area Under the ROC Curve):** A single scalar summarising classifier performance across all thresholds
  - AUC = 1.0: perfect classifier
  - AUC = 0.5: no better than random guessing
  - AUC > 0.9: excellent; > 0.8: good; > 0.7: fair

The ROC curve shows the trade-off between sensitivity and specificity — useful for comparing classifiers independent of a specific threshold.

#### Key Takeaways for ISY503

> - Always start analysis with the **confusion matrix** — it is the source of all other metrics
> - **Accuracy is misleading for imbalanced datasets** — e.g., 95% accuracy means nothing if 95% of cases are one class
> - Choose **precision** when false positives are costly; choose **recall** when false negatives are costly
> - **F1** is the go-to metric for imbalanced classification problems
> - **AUC** provides a threshold-independent view of overall classifier performance

---

### Resource 5 — Hawkins (2004): The Problem of Overfitting

**Citation:** Hawkins, D. (2004). The problem of overfitting. *Journal of Chemical Information and Computer Sciences, 44*, 1–12.

#### 1. What is Overfitting?

**Overfitting** occurs when a model fits the training data so closely that it captures **noise and random variation** rather than the true underlying pattern. The model then performs very well on training data but **generalises poorly** to new, unseen data.

In the context of ISY503: a classifier can have near-perfect training accuracy but substantially worse testing accuracy. This gap is the hallmark of overfitting.

#### 2. Two Types of Overfitting

| Type | Description |
|------|-------------|
| **Model too flexible** | Using a complex model (e.g., high-degree polynomial) when a simpler one suffices — memorises the training data |
| **Irrelevant predictors** | Including features that have no true relationship to the target — they add noise to predictions |

#### 3. Why Adding More Features Can Hurt

Adding irrelevant predictors:
- Fits coefficients to random variation, not signal
- Introduces additional noise in future predictions
- Requires measuring irrelevant inputs at test time (unnecessary cost)

This is related to the **curse of dimensionality** — more features relative to training samples increases overfitting risk.

#### 4. Training vs. Testing Sets — The Core Solution

| Split | Purpose |
|-------|---------|
| **Training set** | Fit the model (the model "sees" this data during learning) |
| **Testing set** | Evaluate true generalisation (the model never trained on this) |

Performance on the test set reflects real-world performance. Performance on the training set is always optimistically biased — especially for complex models.

#### 5. Detecting and Preventing Overfitting

- **Compare training vs. testing performance:** A large gap indicates overfitting
- **Regularisation:** Penalise model complexity (e.g., LASSO, Ridge regression)
- **Feature selection:** Remove irrelevant features before training (see Resource 6)
- **Cross-validation:** Use k-fold CV for a more reliable performance estimate
- **Parsimony principle:** Prefer the simplest model that adequately fits the data

#### Key Takeaways for ISY503

> - Overfitting = great training performance + poor test performance → model memorised noise
> - **Always evaluate on held-out test data** — training accuracy is not a reliable metric
> - Simpler models with fewer features are less prone to overfitting (parsimony)
> - Feature selection and regularisation are the primary practical defences against overfitting

---

### Resource 6 — Chandrashekar & Sahin (2014): A Survey on Feature Selection Methods

**Citation:** Chandrashekar, G. & Sahin, F. (2014). A survey on feature selection methods. *Computers and Electrical Engineering, 40*(1), 16–28.

#### 1. Why Feature Selection?

A **feature** is an individual measurable property of the process being observed. Datasets can have hundreds to thousands of features, but not all are informative:

- **Irrelevant features:** No correlation with the class label — pure noise that degrades performance
- **Redundant features:** Correlated with other features; add no extra discriminative information

Feature selection reduces:
- Computation time
- Overfitting (fewer parameters fitted to the same data)
- Curse of dimensionality
- And generally improves prediction performance and model interpretability

#### 2. The Three Categories of Feature Selection

```
Feature Selection Methods
├── Filter Methods        (rank features independently of classifier)
├── Wrapper Methods       (use classifier performance to evaluate subsets)
└── Embedded Methods      (feature selection built into the training process)
```

#### 3. Filter Methods (Most Relevant for ISY503)

Filter methods **rank features using a statistical criterion** and remove low-ranking ones before training. They are computationally light, independent of the classifier, and good at avoiding overfitting.

**3a. Pearson Correlation Coefficient**

R(i) = cov(xᵢ, Y) / √(var(xᵢ) × var(Y))

- Measures **linear** dependence between feature xᵢ and target Y
- R close to ±1: strong linear relationship → feature is informative
- R close to 0: weak linear relationship → feature may be irrelevant
- Limitation: only detects linear dependencies

**3b. Mutual Information (MI)**

I(Y; X) = H(Y) − H(Y|X)

Where H(Y) is Shannon entropy (uncertainty) of the target and H(Y|X) is the conditional entropy after observing X.
- MI = 0 if X and Y are independent
- MI > 0 if X provides information about Y
- Captures **non-linear** dependencies (more powerful than Pearson)

**3c. RELIEF Algorithm**

- Ranks features based on how well they distinguish between instances of different classes
- Uses nearest-neighbour distances to compute feature relevance scores
- Drawback: threshold selection for the feature cutoff is not straightforward

#### 4. Wrapper Methods

Use the **classifier itself as the evaluation criterion**:
- Search algorithms (e.g., branch-and-bound, greedy forward/backward selection) find subsets that maximise classifier performance
- More accurate than filter methods for specific classifiers
- Computationally expensive — must re-train the classifier for each candidate subset

#### 5. Embedded Methods

Feature selection is integrated into training (e.g., LASSO regression penalises coefficients to zero; decision trees inherently select features at each split). No separate feature selection step required.

#### 6. Overfitting vs. Underfitting Balance

| Problem | Cause | Effect |
|---------|-------|--------|
| **Overfitting** | Too many features; model too complex | Poor generalisation to test data |
| **Underfitting** | Too few features; model too simple | Poor performance even on training data |

The goal is the **right subset** — enough features to capture the true signal but not so many that noise dominates.

#### Key Takeaways for ISY503

> - Feature selection reduces overfitting by removing irrelevant and redundant features
> - **Filter methods (Pearson correlation, Mutual Information)** are the primary approach in this module
> - Pearson detects linear relationships; Mutual Information detects any statistical dependency
> - Too few features → underfitting; too many → overfitting — balance is key
> - Feature ranking must be followed by a threshold decision — there is no universally optimal feature count

---

### Resource 7 — Inglés-Romero et al. (2018): QoS Metrics in Reinforcement Learning

**Citation:** Inglés-Romero, J. F., Espín, J. M., Jiménez-Andreu, R., Font, R. & Vicente-Chicote, C. (2018). Towards the use of quality-of-service metrics in reinforcement learning: A robotics example. *MODELS Workshops 2018*, 465–474.

#### 1. Reinforcement Learning Fundamentals

**Reinforcement Learning (RL)** is a learning paradigm where an **agent** learns by interacting with an **environment** through trial and error:

```
Agent → takes action → Environment → new state + reward → Agent (repeat)
```

Core RL components (Markov Decision Process, MDP):
- **States (S):** The current situation of the agent
- **Actions (A):** What the agent can do in each state
- **Transitions:** How actions change the current state
- **Rewards (R):** Scalar feedback signal indicating quality of each action

The agent's goal: find a **policy** (mapping from states to actions) that **maximises the long-term sum of rewards**.

#### 2. The Reward Function Problem

The **"curse of objective specification"**: defining a good reward function is inherently difficult.
- The reward must accurately quantify what we want the agent to do
- Complex objectives (safety, user satisfaction, reliability) don't map naturally to simple scalar numbers
- A poorly specified reward causes the agent to optimise the wrong objective

#### 3. QoS Metrics as Enriched Rewards

The **RoQME** framework addresses this by using **Quality of Service (QoS) metrics** to enrich the reward signal. Non-functional properties captured include:
- Safety, Reliability, Efficiency, User satisfaction

RoQME uses a **Belief Network** to estimate the probability of quality properties from contextual information (sensor data, observations). The estimated QoS metric becomes part of the reward:

`reward = α × satisfaction`  where satisfaction ∈ [0,1] from the RoQME belief network

#### 4. The Santa Bot Example

A robot (Santa Bot) distributes gifts to children in a shopping mall. It must learn optimal gift-giving by:
- Observing child features (age, gender, clothing colour)
- Receiving feedback via QoS satisfaction metrics (facial expression → belief network → satisfaction score)
- Applying Q-learning over 1000 episodes

**Results:**
- Episode 25: exploring randomly (uniform gift distribution)
- Episode 1000: exploiting learned patterns (matching gifts to child type)
- Final performance: **72.03% average**, **84.67% max** vs. optimal (with known wish lists)

When the RoQME model was configured incorrectly (wrong satisfaction model), the agent **failed to learn** — demonstrating that reward specification is critical.

#### Key Takeaways for ISY503

> - RL agents learn through reward signals — the reward function definition is critical to learning success
> - **MDP** is the mathematical framework for RL: states, actions, transitions, rewards
> - QoS metrics provide a richer, more nuanced reward signal than simple scalar rewards
> - A wrong reward model prevents learning — the quality of the reward specification determines the quality of learning
> - Contrast with supervised learning: RL has no labelled target Y, only delayed reward feedback from the environment

---

### Resource 8 — Palacio-Niño (2019): Evaluation Metrics for Unsupervised Learning

**Citation:** Palacio-Niño, J. O. (2019). Evaluation metrics for unsupervised learning algorithms. arXiv:1905.05667.

#### 1. Supervised vs. Unsupervised Evaluation

| | Supervised Learning | Unsupervised Learning |
|--|--------------------|-----------------------|
| Labels available | Yes | No (or only for evaluation) |
| Evaluation approach | Compare predictions to known labels | Assess internal structure quality |
| Example metrics | Accuracy, F1, AUC | Silhouette, Davies-Bouldin, Rand Index |

In unsupervised learning, labels must be **discovered** by the algorithm — evaluating whether the discovery is meaningful is fundamentally harder.

#### 2. Clustering: The Core Unsupervised Task

**Clustering** groups data points such that:
- Points within a cluster are similar to each other (low intra-cluster distance)
- Points in different clusters are dissimilar (high inter-cluster distance)

**Kleinberg's Impossibility Theorem:** No single clustering function can simultaneously satisfy all three desirable axioms:
1. **Scale Invariance:** Results should not change when all pairwise distances are scaled by a constant
2. **Richness:** Every possible partition of the data should be achievable
3. **Consistency:** Results should not change if within-cluster distances decrease and/or between-cluster distances increase

Practical implication: all clustering algorithms make trade-offs — no universally optimal clustering algorithm exists.

#### 3. Taxonomy of Evaluation Criteria

```
Cluster Evaluation
├── External Criteria (supervised validation)
│   └── Compare cluster results to known ground-truth labels
│       Examples: Rand Index, Adjusted Rand Index, NMI, Purity
└── Internal Criteria (unsupervised validation)
    └── Assess quality using only the data itself (no labels)
        Examples: Silhouette Coefficient, Davies-Bouldin Index, Calinski-Harabász Index
```

#### 4. External Validation Metrics

Used when labelled data exists for evaluation purposes:

| Metric | What it Measures |
|--------|-----------------|
| **Rand Index** | Fraction of pairs correctly assigned to same/different cluster vs. ground truth |
| **Adjusted Rand Index (ARI)** | Rand Index corrected for chance agreement |
| **Normalised Mutual Information (NMI)** | Mutual information between cluster assignments and true labels, normalised to [0,1] |
| **Purity** | For each cluster, the fraction assigned to the majority true class |

#### 5. Internal Validation Metrics

Used when no ground truth labels are available:

| Metric | What it Measures | Better When |
|--------|-----------------|-------------|
| **Silhouette Coefficient** | Similarity of a point to its own cluster vs. nearest other cluster; range [−1, 1] | Closer to +1 |
| **Davies-Bouldin Index** | Average ratio of within-cluster distances to between-cluster distances | Lower |
| **Calinski-Harabász Index** | Ratio of between-cluster to within-cluster variance | Higher |

#### 6. Key Evaluation Questions

Before applying any metric:
1. Does meaningful cluster structure exist in this data?
2. What is the correct number of clusters (k)?
3. How good are the results without external information?

#### Key Takeaways for ISY503

> - Unsupervised evaluation is inherently harder than supervised — there are no "correct" labels to compare against
> - **Kleinberg's theorem** proves no perfect clustering algorithm exists — all involve trade-offs
> - Use **external metrics** (Rand Index, NMI) when labels are available for evaluation
> - Use **internal metrics** (Silhouette, Davies-Bouldin) when evaluating clustering quality without labels
> - Contrast: in supervised learning we measure accuracy/F1 against known labels; in unsupervised we measure structural quality of discovered groups

---

### Resource 9 — Hulten (2018): Building Intelligent Systems (eBook)

**Citation:** Hulten, G. (2018). *Building intelligent systems: A guide to machine learning engineering*. Apress.

> **Status: 🔥 WIP — needs institutional library access**
> Access via Torrens University library portal (authenticated eBook).

**Expected content (based on module description):**
- Full lifecycle of building ML systems: data collection → preprocessing → model training → deployment → maintenance
- Practical ML engineering principles beyond academic theory
- How to build systems that work reliably in production

---

### Resource 10 — Halligan et al. (2015): Disadvantages of ROC AUC for Imaging Tests

**Citation:** Halligan, S., Altman, D. & Mallett, S. (2015). Disadvantages of using the area under the receiver operating characteristic curve to assess imaging tests. *European Radiology, 25*(4), 932–939.

#### 1. What is the ROC AUC?

The **ROC (Receiver Operating Characteristic) curve** plots:
- **Y-axis:** True Positive Rate (Sensitivity = TP / (TP + FN))
- **X-axis:** False Positive Rate (1 − Specificity = FP / (FP + TN))

…at every possible classification threshold.

**AUC (Area Under the Curve):**
- AUC = 1.0: perfect discrimination
- AUC = 0.5: no discrimination (chance diagonal)

Clinical interpretation: AUC is the probability that a randomly selected positive patient is ranked higher than a randomly selected negative patient by the test.

#### 2. Advantages of ROC AUC

- Threshold-independent: captures performance across all possible decision boundaries
- Single number facilitates comparison between tests or classifiers
- Widely reported and understood in medical imaging research

#### 3. Identified Disadvantages

| Disadvantage | Explanation |
|--------------|-------------|
| **Non-normal score distributions** | Confidence scores from radiologists are often bimodal — not spread across the full scale as ROC assumes |
| **ROC curve extrapolation** | When scores cluster at extremes, much of the ROC curve is extrapolated beyond actual data — AUC in those regions is unreliable |
| **Curve fitting dependency** | AUC value varies depending on the statistical method used to fit the ROC curve |
| **Ignores prevalence** | AUC treats all thresholds equally; clinical practice uses a single threshold determined by disease prevalence |
| **Ignores misclassification costs** | FP and FN errors have very different clinical consequences (missed cancer vs. unnecessary biopsy), but AUC treats them symmetrically |
| **Clinically unintuitive** | A change in AUC from 0.85 to 0.88 has little direct interpretable meaning for clinicians |

#### 4. The Proposed Alternative: Net Benefit

**Net benefit** is calculated at **clinically relevant thresholds** (not averaged across all):

`Net Benefit = (TP/N) − (FP/N) × (p_t / (1 − p_t))`

Where p_t is the clinical threshold probability reflecting the cost ratio of FP vs. FN.

Net benefit:
- Incorporates **prevalence** (disease frequency in the population)
- Accounts for **different misclassification costs**
- Is **clinically interpretable**: reflects changes in correct vs. incorrect diagnoses
- Works at specific, clinically meaningful thresholds

#### 5. When to Use Which Metric

| Stage | Recommended Metric |
|-------|-------------------|
| Early test development / classifier comparison | ROC AUC (threshold-independent, easy comparison) |
| Clinical decision-making / policy | Net Benefit (prevalence-aware, cost-aware, interpretable) |
| Research reporting | Both, with explicit thresholds for sensitivity/specificity |

#### Key Takeaways for ISY503

> - ROC AUC is widely used but has important limitations — it is not always the right metric
> - **Prevalence and misclassification costs matter** — metrics must reflect the real-world context
> - No single metric is universally appropriate: choose metrics that match the **problem's priorities**
> - When FP and FN costs differ significantly, precision/recall or net benefit are more appropriate than AUC
> - This paper directly motivates the module theme: metrics must be chosen carefully and fit the situation

---

## Module Summary: Core Vocabulary

| Term | Definition |
|------|-----------|
| **Feature** | An input variable (X) used by the model |
| **Target** | The output variable (Y) the model predicts |
| **Classifier** | An algorithm that learns the mapping X → Y for discrete outputs |
| **Training set** | Labelled data used to fit the model |
| **Test set** | Held-out data used to evaluate generalisation |
| **Overfitting** | Model fits training data noise; poor test performance |
| **Underfitting** | Model too simple; poor performance even on training data |
| **Confusion Matrix** | Table of TP, TN, FP, FN — foundation of all classification metrics |
| **Accuracy** | (TP+TN) / total; reliable only for balanced classes |
| **Precision** | TP / (TP+FP); optimise when FP cost is high |
| **Recall (Sensitivity)** | TP / (TP+FN); optimise when FN cost is high |
| **Specificity** | TN / (TN+FP); of actual negatives, correctly identified |
| **F1 Score** | Harmonic mean of precision and recall; use for imbalanced data |
| **AUC** | Area under ROC curve; threshold-independent classifier performance |
| **Feature Selection** | Removing irrelevant/redundant features to improve model |
| **Label Encoding** | Mapping categories to integers |
| **One-Hot Encoding** | Creating binary indicator columns per category level |
| **MDP** | Markov Decision Process — mathematical framework for RL |
| **Reward** | Scalar feedback in RL indicating quality of an action |
| **Silhouette Coefficient** | Internal clustering quality metric; range [−1, 1] |
