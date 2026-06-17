# Module 4 - Decision Trees

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Brid (2018) / Koli (2023) - Introduction to Decision Trees (terminology, Gini/entropy/info-gain, pruning) | ✅ |
| **2** | Watch & summarise Two Minute Papers (2016) #55 - Decision Trees & Boosting, XGBoost | ✅ |
| 3 | Read & summarise Morde (2019) - XGBoost Algorithm: Long May She Reign! | 🔥 Primer ready |
| **4** | Read & summarise Brownlee (2019) - Plotting XGBoost trees in Python | ✅ |
| **5** | Read & summarise scikit-learn (2015) - Decision Tree documentation | ✅ |
| 6 | Activity 1: Visualising a decision tree (Google Developers, ML Recipes #2) | 🕐 |
| 7 | Activity 2: Decision tree classifier from scratch (Google Developers #8 - Gini impurity) | 🕐 |
| 8 | Activity 3: Decision tree in sklearn - Wine dataset (Babu 2020) | 🕐 |
| 9 | Activity 4: Random Forest vs XGBoost - UCI Wine (Sblendorio 2019) | 🕐 |

---

## Key Highlights

### 1. Introduction to Decision Trees (Brid 2018; Koli 2023)

**Citation:** Brid, R. (2018, 26 October). *Introduction to decision trees.* Medium. https://medium.com/@MrBam44/decision-trees-91f61a42c724
**Local source summarised:** Koli, S. (2023, 28 February). *Decision Trees: A Complete Introduction With Examples.* Medium - a topic-equivalent primer covering the same ground (terminology, entropy/Gini/information gain, pruning, sklearn). Read the official Brid article for the set reading; this summary captures the shared concepts.

**Purpose:** Builds the vocabulary and the splitting maths behind decision trees with no heavy code, then closes with the scikit-learn hyperparameters you actually tune.

---

#### 1. Anatomy of a tree
- A **decision tree** is a **non-parametric supervised** learner with a hierarchical structure: **root node -> decision (internal) nodes -> leaf (terminal) nodes**, joined by **branches**.
- **Root node** = where splitting begins (the best single predictor). **Decision nodes** = nodes produced by a split. **Leaf nodes** = no further split possible; hold the class label or predicted value. **Sub-tree** = any branch section. **Pruning** = cutting nodes to stop overfitting.
- Drawn **upside down** (root on top). In plain terms it is **a stack of if-else rules**: check a condition, follow the matching branch, repeat until a leaf.
- Handles **both categorical and numerical** data, and **both classification and regression** (hence **CART**).

#### 2. How a split is chosen - two criteria families
The whole algorithm reduces to one question repeated greedily: *which attribute split makes the children purest?*

| Family | Impurity metric | Split type | Note |
|---|---|---|---|
| **ID3** (Iterative Dichotomiser 3) | **Entropy** + **Information Gain** | multi-way | from information theory |
| **CART** (Classification & Regression Trees) | **Gini index** | **binary only** | scikit-learn default |

- **Entropy** measures impurity / randomness: `H(X) = - Σ pᵢ·log₂(pᵢ)`. Pure node -> entropy 0; 50/50 split -> entropy 1. Higher entropy = more information content.
- **Gini index** = `Σ pᵢ(1 - pᵢ)` - probability of misclassifying a random sample. **Prefer the attribute with the LOWER Gini.**
- **Information Gain** = `entropy(parent) - weighted-average entropy(children)`. The ID3 loop: (1) entropy of target; (2) split on each attribute, compute weighted child entropy, subtract from parent = gain; (3) pick the **largest information gain** as the decision node; (4) recurse on impure branches (entropy > 0); a branch with entropy 0 becomes a leaf.

#### 3. Pruning & overfitting
- A **too-large tree overfits** (memorises noise); a **too-small tree underfits** (misses structure).
- **Pruning** shrinks the tree without losing accuracy. Two types named: **Cost-Complexity Pruning** and **Reduced-Error Pruning**.
- **Decision tree -> decision rules:** read each root-to-leaf path as one if-then rule. This is the source of the tree's **explainability**.

#### 4. Strengths and weaknesses

| ✅ Advantages | ⚠️ Disadvantages |
|---|---|
| Little data prep; **no normalisation / scaling needed** | **Unstable** - a small data change can restructure the whole tree |
| Tolerant of missing values | Deep trees get **complex** (many layers) |
| **Intuitive / white-box** - explain to stakeholders | Can be **slow to train** |
| Handles categorical + numerical, classification + regression | **Overfits** easily -> fix with **Random Forest** / ensembles |

#### 5. The scikit-learn knobs (hyperparameters)
| Parameter | What it controls |
|---|---|
| `criterion` | split quality - `"gini"` (default) or `"entropy"` |
| `splitter` | `"best"` (greedy) or `"random"` |
| `max_depth` | hard cap on tree depth (default `None` = grow fully) |
| `min_samples_split` | min samples needed to split an internal node |
| `max_leaf_nodes` | grow best-first up to N leaves |

Minimal workflow (iris): `DecisionTreeClassifier().fit(X, y)` -> `.predict(obs)` / `.predict_proba(obs)` -> visualise with `plot_tree(clf)` or `dtreeviz`.

#### Key Takeaways for MLN601
1. **Activity 2** (decision tree from scratch) is literally this resource's maths - **Gini, impurity, information gain**. Read this before attempting it.
2. Decision trees are the **building block of the Random Forest** you already used in **Assessment 1** - the cons here (instability, overfitting) are exactly *why* the ensemble beat a single tree.
3. The "no scaling needed" point contrasts with linear regression (Module 3), where you used `StandardScaler`. Trees split on thresholds, so monotonic feature scaling is irrelevant.

---

### 2. Decision Trees and Boosting, XGBoost (Two Minute Papers 2016)

**Citation:** Two Minute Papers. (2016, 25 March). *Decision trees and boosting, XGBoost | Two Minute Papers #55* [Video]. https://www.youtube.com/watch?v=0Xc9LIb_HTw

**Purpose:** A two-minute intuition for **why we combine many weak trees** - the conceptual bridge from a single decision tree to XGBoost. *(Summarised from the local transcript.)*

---

#### 1. Weak learners
- A single shallow tree is a **weak learner**: individually **only slightly better than random guessing**.
- Toy example: predict who likes computer games from age/gender. One tree splits on age > 15; another could split on "uses a computer daily". Each alone is mediocre.

#### 2. Boosting = many weak learners -> one strong learner
- **Boosting** combines a large number of weak trees into a **strong learner**.
- Trick: output **scores (positive/negative)** instead of hard yes/no decisions - this makes combining trees easy and is the basis of gradient boosting.
- **Doctor-committee analogy:** one doctor may be wrong, so you consult several; a well-chosen committee produces an accurate diagnosis even if no single member is expert.
- **Adaptive version:** bring in new "doctors" specifically to cover the **deficiencies** of existing members (this is the intuition behind AdaBoost / gradient boosting adding learners that target the previous errors / residuals).

#### 3. Why it matters
- Big advantage over neural networks: **you can see why and how** the model reached a decision (interpretable).
- The library **XGBoost** has won a *staggering* number of **Kaggle** competitions - simple method, very respectable accuracy.

#### Key Takeaways for MLN601
1. This is the **"so what" behind your A1 result**: a RandomForest (a bag of trees) beat LinearRegression because **ensembles of trees capture non-linearity** a single line cannot.
2. Sets up **Resource 3 (XGBoost)** and **Activity 4 (Random Forest vs XGBoost)** - boosting (sequential, fixes errors) vs bagging (parallel, votes) is the key contrast.
3. Interpretability + accuracy is the recurring exam theme: trees/ensembles sit in the **explainable** corner (links to the PwC XAI framing in the module intro).

---

### 3. XGBoost Algorithm: Long May She Reign! (Morde 2019)

**Citation:** Morde, V. (2019, 8 April). *XGBoost algorithm: Long may she reign!* Towards Data Science. https://towardsdatascience.com/https-medium-com-vishalmorde-xgboost-algorithm-long-she-may-rein-edd9f99be63d

**Purpose:** Traces the family tree from a single decision tree to XGBoost and explains the engineering that makes it the default for tabular data. *(Article is paywalled - this is a primer from established knowledge; verify details against the original on manual read.)*

---

#### 1. The evolution of tree-based algorithms
| Stage | What it adds |
|---|---|
| **Decision Tree** | one greedy tree of if-then rules |
| **Bagging** | train many trees on **bootstrap samples**, **average / majority-vote** -> lowers variance |
| **Random Forest** | bagging **+ random feature subset** per split -> decorrelates the trees |
| **Boosting** | trees built **sequentially**, each correcting the previous one's errors |
| **Gradient Boosting** | formalises boosting as **gradient descent on a loss function** |
| **XGBoost** | gradient boosting **+ systems & algorithmic optimisations** ("eXtreme") |

#### 2. The hiring-interview analogy
Morde frames it as an HR manager shortlisting candidates: a single interviewer with fixed criteria = one tree; a **panel voting independently** = bagging / random forest; **interviewers who each learn from the previous round's mistakes** = boosting; a slick, optimised hiring pipeline = XGBoost.

#### 3. Why XGBoost is fast *and* accurate
| Systems optimisations | Algorithmic enhancements |
|---|---|
| **Parallelised** tree construction | **Regularisation** (L1 + L2) to curb overfitting |
| **Tree pruning** depth-first then prune back (`max_depth`) | **Sparsity awareness** - handles missing values natively |
| **Hardware/cache awareness** + **out-of-core** blocks for big data | **Weighted quantile sketch** for optimal split points |
| | **Built-in cross-validation** each iteration |

#### 4. When to reach for it (and limits)
- **Shines on structured / tabular** data of small-to-medium size - the Kaggle workhorse.
- **Limits:** many hyperparameters to tune; can overfit if left unchecked; **deep learning still wins on unstructured data** (images, text, audio). No Free Lunch still applies.

#### Key Takeaways for MLN601
1. Directly supports **Assessment 3 (model selection)** and **Activity 4** - you can justify *why* a boosted ensemble might beat your A1 RandomForest.
2. Connects the dots: **bagging (parallel) vs boosting (sequential)** is the single most testable distinction in this module.
3. The regularisation + missing-value handling are concrete answers to "how would you improve the model?" in an assessment discussion.

---

### 4. Plotting XGBoost Trees in Python (Brownlee 2019)

**Citation:** Brownlee, J. (2019, 11 December). *How to visualize gradient boosting decision trees with XGBoost in Python.* Machine Learning Mastery. https://machinelearningmastery.com/visualize-gradient-boosting-decision-trees-xgboost-python/

**Purpose:** The hands-on "how do I actually see one tree" tutorial - turns a trained ensemble into a readable diagram.

---

#### 1. The core API
- **`plot_tree(model)`** (from the XGBoost Python API) renders an individual tree; **`xgb.to_graphviz(model)`** gives higher-resolution output.
- **Dependency:** the **Graphviz** library must be installed (system package + Python wrapper).

#### 2. Selecting and orienting a tree
- An XGBoost model is **many trees** - choose one with **`num_trees`** (0-indexed): `plot_tree(model, num_trees=4)` draws the 5th tree.
- **`rankdir='LR'`** switches the layout to **left-to-right** (easier to read than the default top-down).
- Bump resolution with `fig = plt.figure(dpi=180)`.

#### 3. Reading the diagram
- Each node shows the **feature and threshold** of the split (use a **DataFrame** / set `feature_names` so labels read `alcohol` not `f7`).
- **Leaf nodes** show the model's **output score**; branch colours mark the left/right paths.
- Reading a single tree exposes which features the model splits on first - a window into feature importance.

#### Key Takeaways for MLN601
1. This is your **explainability deliverable** - **Activity 3** asks you to *extract the DT rules as a text report*; `plot_tree` / `export_text` is how.
2. For **A1's RandomForest**, the same idea applies: plot one representative tree (or a feature-importance bar) to discuss *why* `alcohol` tends to dominate quality.
3. Reinforces the module's selling point: trees are **white-box** - you can literally draw the decision path.

---

### 5. scikit-learn Decision Tree Documentation (Pedregosa et al. 2015)

**Citation:** Pedregosa, F., et al. (2011/2015). *Scikit-learn: Machine learning in Python.* JMLR 12, 2825-2830. User guide: https://scikit-learn.org/stable/modules/tree.html

**Purpose:** The authoritative reference - the precise API, the impurity maths, and the exact knobs for controlling overfitting.

---

#### 1. Advantages & disadvantages (the official list)
| ✅ Advantages | ⚠️ Disadvantages |
|---|---|
| Easy to interpret & **visualise**; white-box boolean logic | **Overfits** via over-complex trees (mitigate by pruning) |
| Little data prep; handles numerical + categorical | **Unstable** - small data changes -> different tree (mitigate by ensembles) |
| **Prediction cost O(log n_samples)** | Predictions are **piecewise-constant** -> poor at extrapolation |
| Supports **multi-output** problems | Learning the optimal tree is **NP-complete** (greedy heuristics only) |
| Can be validated with statistical tests | Struggles with **XOR / parity** concepts; **biased on imbalanced classes** |

#### 2. Classifier vs Regressor
| | `DecisionTreeClassifier` | `DecisionTreeRegressor` |
|---|---|---|
| Target | integer class labels | continuous floats |
| Criteria | `gini`, `entropy`/`log_loss` | `squared_error`, `friedman_mse`, `absolute_error`, `poisson` |
| Predict | `.predict()`, `.predict_proba()` | `.predict()` |

#### 3. The impurity maths (split quality)
- **Gini:** `H(Qₘ) = Σ pₘₖ(1 - pₘₖ)`  ·  **Entropy:** `H(Qₘ) = - Σ pₘₖ·log(pₘₖ)`, where `pₘₖ` = proportion of class k in node m.
- **Regression MSE (default):** `H(Qₘ) = (1/nₘ) Σ (y - ȳₘ)²`  ·  **MAE:** mean abs deviation from the **median** (3-6x slower).
- **Split objective:** pick the split θ that minimises the **weighted child impurity**
  `G(Qₘ, θ) = (n_left/nₘ)·H(left) + (n_right/nₘ)·H(right)`.

#### 4. Practical overfitting controls
| Parameter | Tip |
|---|---|
| `max_depth` | start at **3**, increase carefully (each level doubles samples needed) |
| `min_samples_split` | raise above default 2 |
| `min_samples_leaf` | try **5** to start - guarantees leaf size |
| `min_impurity_decrease` | only split if impurity drops enough |
| `ccp_alpha` | **cost-complexity pruning** applied *after* training |

Plus: **balance imbalanced classes** (sample equally or weight), apply **dimensionality reduction** (PCA / feature selection) when features >> samples, and **inspect** with `export_text()` / `plot_tree(max_depth=3)`.

#### Key Takeaways for MLN601
1. The doc explicitly warns trees are **biased on imbalanced classes** - your **A1 wine `quality` is imbalanced** (mostly 5-6), so this is a real limitation to name in the discussion.
2. `ccp_alpha` and `max_depth`/`min_samples_leaf` are the concrete levers for the "how would you reduce overfitting?" assessment question.
3. **Piecewise-constant + poor extrapolation** is the precise reason a single tree underperforms a tuned ensemble - and a clean contrast with the smooth line from Module 3's linear regression.

---

## Synthesis - how Module 4 fits together

| Concept | One-line takeaway | Resource |
|---|---|---|
| Single tree | Greedy if-then rules; split to maximise purity (Gini / info-gain) | R1, R5 |
| Why it fails alone | Unstable + overfits + piecewise-constant | R1, R5 |
| Bagging -> Random Forest | Parallel trees, average/vote -> lower variance | R3 |
| Boosting -> XGBoost | Sequential weak learners fix prior errors -> lower bias | R2, R3 |
| Explainability | Trees are white-box; plot or export the rules | R4, R1 |
| A1/A3 link | Ensembles beat the linear baseline because quality is non-linear | all |
