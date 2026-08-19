# MLN601 Cumulative Quiz - Modules 1-12 - Answer Key

Grade yourself honestly before reading further. Partial credit is fine if the mechanism is right even when the wording differs.

### 1. Module 1 - Parameter vs hyperparameter (6 points)

- **Parameter (learned):** a regression coefficient (`b0`, `b1`), a perceptron weight, a logistic regression coefficient, a tree's chosen split threshold.
- **Hyperparameter (set by you):** tree `max_depth`, k in K-means, `C` in SVM/logistic regression, learning rate `eta`.
- The algorithm learns parameters by fitting to data; you (or `GridSearchCV`) set hyperparameters before or around training.

### 2. Module 2 - CRISP-DM and leakage (8 points)

Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment (loop back to any phase anytime).

`Global = NA + EU + JP + Other` means the label is a sum of features already in the training set - the model is not predicting sales, it is doing arithmetic on columns that already contain the answer. This is caught (or should be caught) in **Data Understanding/Data Preparation**, when you inspect how each column was derived, before Modeling. An R2 of 0.9999 is a red flag, not a win, because real-world tabular data rarely explains itself that cleanly - the "too good to be true" instinct from Module 2 applies directly.

### 3. Module 3 - Regression metrics (7 points)

- **MAE 0.40:** on average, predictions miss the true wine quality score by 0.40 points, with every error weighted equally.
- **RMSE 0.90:** the typical miss is larger once big errors are squared and re-rooted; RMSE is always >= MAE.
- **R2 0.55:** the model explains 55% of the variance in wine quality; 45% is unexplained by the features.
- RMSE more than double MAE signals a **few large misses** dragging the squared-error metric up, not a uniform spread of small errors - worth investigating outliers or a poorly-fit subgroup.

### 4. Module 4 - Trees and ensembles (9 points)

Gini impurity = `sum(p_k * (1 - p_k))` across classes at a node; lower means purer (fewer mixed classes).

| | Bagging (Random Forest) | Boosting (XGBoost) |
|---|---|---|
| Trees trained... | in parallel, on bootstrap samples | in sequence, each correcting the prior tree's errors |
| Cures... | variance (instability) | bias (weak learners) |
| Combine predictions by... | averaging / majority vote | weighted sum of weak learners |

### 5. Module 5 - Bayes' rule and the base-rate fallacy (9 points)

`P(A|B) = P(B|A) * P(A) / P(B)`

Worked example: prior = 1/1000, false-positive rate = 5%, population = 10,000.
- True positives: about 10 (everyone who actually has the disease, assuming the test also catches them).
- False positives: about 5% of the ~9,990 healthy people = about 500.
- `P(disease | positive) = 10 / (10 + 500) ≈ 2%`, nowhere near the test's headline 95% accuracy.

The rare prior means the pool of healthy people is so much larger than the pool of sick people that even a small false-positive rate produces more false alarms than true hits.

### 6. Module 6 - SVM soft margin and kernels (9 points)

`C` controls how much the SVM tolerates margin violations. **Low C** = wider, smoother margin, more tolerant of misclassified points, more regularised (higher bias, lower variance). **High C** = the model tries to classify every training point correctly, producing a tighter, more complex boundary (lower bias, higher variance, overfitting risk).

Kernel trick, one sentence: it lets the SVM compute how similar two points would be in a bent, more complex feature space, using only a formula on the original points, without ever building that new space by hand.

### 7. Module 7 - Explainable ML quadrant (7 points)

```
              GLOBAL                 LOCAL
        +------------------+------------------+
INTRIN- | logistic          | decision tree's   |
  SIC   | regression        | if-else path for  |
        | coefficients      | one row           |
        +------------------+------------------+
POST-   | permutation       | SHAP on one       |
  HOC   | importance        | prediction        |
        +------------------+------------------+
```

### 8. Module 8 - Logistic regression (7 points)

Sigmoid: `p = 1 / (1 + e^(-z))`, where `z = b0 + b1*x1 + ...`.

`C = 1/lambda` (inverse regularisation strength) - the counter-intuitive part is that a **higher** `C` means **less** regularisation, not more. At very high `C`, the model stops penalising large coefficients, chases every training point, and the decision boundary becomes more complex and prone to overfitting.

### 9. Module 9 - K-means (7 points)

The lowest-inertia solution is always the one with the most clusters (inertia keeps shrinking as k grows, hitting 0 when k = number of points) - it is not a normalised score, so you cannot compare it in isolation or use it to pick k directly. The elbow method looks for the point where adding another cluster stops buying much reduction in inertia.

No-ground-truth metrics: **silhouette score** (higher is better, range -1 to +1), or Calinski-Harabasz (higher is better), or Davies-Bouldin (lower is better) - any one with the correct direction earns the points.

### 10. Module 10 - PAC learning theory (7 points)

- **Epsilon (ε):** the maximum acceptable error of one trained model on unseen predictions - accuracy.
- **Delta (δ):** the probability that an entire training run produces a bad model in the first place - confidence across runs, one level up from epsilon.

`train_test_split` is PAC in disguise because holding out a test set is exactly how you estimate whether a model's error stays under epsilon on data it never saw during training.

### 11. Module 11 - The perceptron (9 points)

`w <- w + eta * (target - prediction) * x`

On non-linearly-separable data, the perceptron's weights never settle - the update rule keeps firing because some point is always misclassified, so training cycles forever unless you cap the number of epochs. When the data **is** linearly separable, the **Perceptron Convergence Theorem** (Rosenblatt, 1962) guarantees the rule will find a separating boundary.

### 12. Module 12 - Enterprise-grade ML and Snorkel (8 points)

`train in the cloud -> score in the DBMS -> govern everywhere`. The cloud gives cheap, scalable compute for training; scoring inside the DBMS avoids moving huge volumes of data out to a separate serving layer (Agrawal reports 5x-24x speedups); governing everywhere means lineage, access control, and monitoring apply across the whole path, not just at training time.

Snorkel pipeline order and outputs:
1. **Unlabelled data** - raw examples with no `y`.
2. **Labelling functions** - each votes `+1` / `-1` / abstain on an example.
3. **Generative label model** - learns a correlation-aware model of the LFs' reliability, outputs **probabilistic labels** per example.
4. **Probabilistic labels** - a soft label (a probability, not a hard 0/1) for every example.
5. **Discriminative model** - trained on the probabilistic labels using a loss that accepts soft targets (log-loss/BCE, not a plain classifier that only accepts hard labels).

This is not majority voting because the generative model weighs each labelling function by its learned accuracy and correlation with the others, instead of counting every vote equally.

### 13. Synthesis - the family tree (7 points)

Any two of:
- **Perceptron vs SVM:** the perceptron just needs any separating line and stops as soon as every training point is correct (pure memorization); the SVM keeps searching for the widest-margin line among all separating options, which is what lets it generalize better.
- **Perceptron vs logistic regression:** the perceptron outputs a hard class via a step function; logistic regression outputs a probability via a sigmoid and is trained by minimising log-loss instead of counting mistakes.
- **SVM vs decision tree:** SVM optimises a margin in feature space and is a black box without extra tooling; a decision tree optimises impurity reduction at each split and is intrinsically explainable by reading the if-else path.
- **Logistic regression vs decision tree:** logistic regression assumes a linear decision boundary and gives interpretable odds ratios; a decision tree can carve non-linear, axis-aligned regions and gives interpretable if-else rules instead of coefficients.

## Score Guide

- **90-100:** The whole course still holds together as one system, not twelve disconnected modules.
- **75-89:** Core mechanics are solid; a couple of modules need a re-read.
- **60-74:** Gaps are showing across multiple modules - schedule a `/module-compression` pass.
- **Below 60:** Re-read the one-pagers for the modules you missed, then retake closed book.
