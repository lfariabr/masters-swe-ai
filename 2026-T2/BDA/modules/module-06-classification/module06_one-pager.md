# BDA601 · Module 6 - One-Pager

> **Classification - supervised learning · 1R · Naive Bayes · decision trees · pruning · big-data scale**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Classification is a lifecycle, not just an algorithm:** define a meaningful label, prepare ethical features, train on labelled data, evaluate on unseen data, then monitor drift. Success means useful generalisation - not memorising training rows.
> (Kelleher & Tierney Ch.4 · Witten et al. §4.1-4.3 + §6.1)

## 🖤 Zone 1 - Frame the learning problem

| | **Supervised** | **Unsupervised** |
|---|---|---|
| Data | labelled - target `y` known | unlabelled - no target |
| Goal | learn attributes → class | discover hidden structure |
| BDA task | **classification** | clustering (Module 9) |
| Example | predict deposit `y=yes/no` | group similar customers |

- 🔵 **Two phases:** train/learn a model → evaluate it on **unseen data**.
- 🔵 **Learning bias:** every algorithm prefers certain patterns - match model to data by evidence.
- 🔴 **Prediction needs signal:** correlation or another dependency between features and target. Feature engineering can expose stronger signal than raw columns.
- 🔵 **Question → output:** categorical answer = **classification**; numerical answer = **regression**.
- 🔴 Before modelling, verify that the label is meaningful and trustworthy; choose relevant, ethical features with no target leakage.

## 🖤 Zone 2 - Three baseline classifiers ⭐ SLO d) - THE GRADED CORE

| Method | Core idea | Strength | Main trap |
|---|---|---|---|
| **1R** | best rule from **one attribute** | fast, interpretable baseline | high-cardinality IDs overfit |
| **Naive Bayes** | combine class probabilities | fast; missing-friendly | assumes conditional independence |
| **Decision tree** | recursively split on best attribute | readable; captures interactions | grows too specific without pruning |

- 🔵 **1R:** majority class per attribute value; choose the attribute with fewest training errors.
- 🔵 **Naive Bayes:** `P(C|x) ∝ P(C) · Π P(xᵢ|C)`; omit a missing feature from the product.
- 🔴 **Zero-frequency veto:** one zero makes the whole product zero → **Laplace smoothing = add 1 to each count**.

## 🖤 Zone 3 - Build a decision tree by hand

```text
labelled rows
    ↓
entropy of parent
    ↓
gain for every candidate attribute
    ↓
split on MAX gain
    ↓
repeat on each child until pure / stopping rule
```

- 🔵 **Entropy = impurity:** `Info(S) = -Σ pᵢ log₂(pᵢ)` bits. Pure node = `0`; binary 50/50 = `1`.
- 🔵 **Information gain:** `Gain(A) = Info(parent) - Σ (|child|/|parent|) Info(child)`.
- 🔴 **Many-value bias:** an ID can create pure branches but predict nothing new. **Gain ratio** penalises highly branching splits.
- 🔵 **Numeric feature:** test binary thresholds such as `age < t`; nominal feature branches by category.

## 🖤 Zone 4 - Make the tree generalise: missing values + pruning

- 🔵 **Missing values:** sophisticated tree method sends a row fractionally down branches, weighted by observed branch frequencies. Alternatives: 1R treats missing as a value; Naive Bayes omits it.

| Fit | Meaning |
|---|---|
| **Underfit** | too simple - poor on training and test data |
| **Good fit** | captures patterns that transfer to unseen data |
| **Overfit** | memorises training noise - test performance drops |

- 🔴 **Postpruning:** grow the full tree, then simplify using a pessimistic error estimate.
  - **Subtree replacement** = replace a subtree with one leaf.
  - **Subtree raising** = promote a strong child subtree.
- 🔵 Control complexity with pruning, `maxDepth`, minimum samples and stopping criteria.
- 🔴 Detect overfitting by comparing training vs test performance - never judge a model only by training accuracy.

## 🖤 Zone 5 - Build and evaluate it in PySpark

```text
raw DataFrame → dropna / impute
      ↓
StringIndexer → VectorAssembler(features)
      ↓
randomSplit([0.8, 0.2], seed)
      ↓
DecisionTreeClassifier.fit(train)
      ↓
model.transform(test)
      ↓
metrics + feature importance
```

- 🔵 `StringIndexer` encodes categories; `VectorAssembler` creates Spark's required feature vector. Encoded numbers **do not imply natural order**.
- 🔴 Fix the random `seed` for reproducible results. At big-data scale, Spark distributes this workflow across partitions.
- 🔵 **Metrics:** accuracy = overall correctness · precision = predicted positives that were right · recall = actual positives found · F1 = precision/recall balance · ROC-AUC = discrimination across thresholds (`0.5` ≈ random; higher is better).
- 🔴 **Accuracy can mislead on imbalanced data** - a model predicting every rare cancer case as healthy may be 99% accurate but useless.
- 🔵 **Feature importance** explains which inputs drove the tree. After deployment, monitor **data drift** and retrain when new data diverges.

## 🔴 Assessment Hook (bottom red strip)
> **A2 = Visualisation and Model Development** · source code + report (**1000 words** ±10%) · **30%** · due **26/07/2026** · SLOs **c) d) e)**.
> Module 6 supplies A2's modelling logic: define the labelled target, justify a classifier, train it on cleaned features, and avoid overfitting. Module 7 will supply the evaluation evidence.
> **Dr. Chen, Week 6:** start early and use a real-world dataset. Spark is not mandatory - Python, R or another suitable package is acceptable. Justify preprocessing, features, algorithm and evaluation.

## 🔴 If you only memorise 5 things
1. **Classification = supervised learning:** labelled features → known target class.
2. **1R is the baseline; Naive Bayes multiplies probabilities; trees split recursively.**
3. **Entropy measures impurity; choose the split with maximum information gain.**
4. **Laplace smoothing fixes zero frequencies; gain ratio fixes many-value split bias.**
5. **Pruning fights overfitting; precision/recall/F1/AUC test usefulness - accuracy alone can mislead.**

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Which warehouse column could become a trustworthy target label - churned, defaulted, returned, converted - and who defines its business meaning?
2. If a customer ID produces a perfect tree split, why is that probably leakage or memorisation rather than useful prediction?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 Complete **Activity 1** - Han Exercise 8.7, construct the decision tree by hand, post it, and respond to peers
- [ ] 🕐 Complete **Activity 2** - identify the most important attribute, choose and justify a missing-value strategy, post it, and respond to peers
- [ ] Review the **Assessment 2 brief** and identify its target variable, candidate features, and proposed classifier
