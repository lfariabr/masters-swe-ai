# MLN601 Cumulative Quiz - Modules 1-12

**Scheduled:** Thursday, 20 August 2026

**Time box:** 50 minutes

**Mode:** Closed book, written answers, then check the separate answer key

Do not open `cumulative-quiz-modules-1-12-answers.md` until every question has an answer. This is the full-course quiz - one question sampled from each module, plus a synthesis question at the end tying model families together.

## Questions

### 1. Module 1 - Parameter vs hyperparameter (6 points)

Give one example of a model parameter and one example of a hyperparameter from any module. Which one does the algorithm learn from data, and which one do you set before training?

### 2. Module 2 - CRISP-DM and leakage (8 points)

Name the six CRISP-DM phases in order. Then explain, using the `vgsales` example (`Global = NA+EU+JP+Other`), which phase is responsible for catching that kind of leakage and why an R2 of 0.9999 should make you suspicious, not pleased.

### 3. Module 3 - Regression metrics (7 points)

You train a model and get MAE = 0.40, RMSE = 0.90, R2 = 0.55 on the wine quality target. Explain what each number tells you on its own, and explain why RMSE being more than double the MAE is itself informative.

### 4. Module 4 - Trees and ensembles (9 points)

Define Gini impurity in one sentence. Then complete this table from memory:

| | Bagging (Random Forest) | Boosting (XGBoost) |
|---|---|---|
| Trees trained... | | |
| Cures... | | |
| Combine predictions by... | | |

### 5. Module 5 - Bayes' rule and the base-rate fallacy (9 points)

Write Bayes' rule. Then explain, with a worked numeric example (prior, false-positive rate, population size), why a 95%-accurate test for a disease with a 1-in-1000 prior can still mean most positive results are wrong.

### 6. Module 6 - SVM soft margin and kernels (9 points)

Explain what the `C` hyperparameter controls in scikit-learn's SVM, using the correct direction (low C vs high C). Then explain the kernel trick in one sentence, without using the word "dimension."

### 7. Module 7 - Explainable ML quadrant (7 points)

Draw or describe the 2x2 grid from Module 7 (intrinsic/post-hoc by global/local). Place these four in the correct quadrant: SHAP on one prediction, a decision tree's if-else path for one row, permutation importance, logistic regression coefficients.

### 8. Module 8 - Logistic regression (7 points)

State the sigmoid formula. Then explain the counter-intuitive relationship between `C` and regularisation strength in logistic regression, and say what happens to the decision boundary at very high `C`.

### 9. Module 9 - K-means (7 points)

Explain why K-means needs the elbow method (or silhouette score) instead of just training with the k that gives the lowest inertia. Then name one metric you can use when you have no ground-truth labels, and state whether higher or lower is better for it.

### 10. Module 10 - PAC learning theory (7 points)

Define epsilon and delta in one sentence each, using the distinction between "accuracy of one model" and "confidence across training runs." Then explain, in one sentence, why `train_test_split` is PAC theory in disguise.

### 11. Module 11 - The perceptron (9 points)

Write the perceptron's online update rule. Then explain what happens when you run a perceptron on data that is not linearly separable, and name the theorem that guarantees convergence when the data is separable.

### 12. Module 12 - Enterprise-grade ML and Snorkel (8 points)

Complete the Module 12 architecture in three clauses: `train in ______ -> score in ______ -> govern ______`.

Then put these Snorkel components in the correct pipeline order and state what each stage outputs: discriminative model, labelling functions, generative label model, unlabelled data, probabilistic labels.

### 13. Synthesis - the family tree (7 points)

Perceptron, SVM, logistic regression, and decision trees all solve classification, but differ in what they optimise and how explainable they are. Pick any two of these four models and explain, in two or three sentences, the key difference in what each one is trying to maximise or minimise.

## Score Guide

- **90-100:** The whole course still holds together as one system, not twelve disconnected modules.
- **75-89:** Core mechanics are solid; a couple of modules need a re-read.
- **60-74:** Gaps are showing across multiple modules - schedule a `/module-compression` pass.
- **Below 60:** Re-read the one-pagers for the modules you missed, then retake closed book.
