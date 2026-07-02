# Module 6 - Classification

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Kelleher & Tierney (2018) - Supervised vs Unsupervised Learning | ✅ |
| **2** | Read & summarise Witten et al. (2017) - Algorithms: 1R, Naive Bayes, Decision Trees (§4.1-4.3) | ✅ |
| **3** | Read & summarise Witten et al. (2017) - Decision Trees in practice: numeric/missing/pruning (§6.1) | ✅ |
| **4** | Read & summarise Koturwar, Girase & Mukhopadhyay (2015) - Survey of classification in big data | ✅ |
| 5 | Activity 1: Build a decision tree by hand (Han Exercise 8.7) + forum post | 🕐 |
| 6 | Activity 2: Handle missing values in the most important attribute + forum post | 🕐 |

**Local sources (this folder):**
- `r1_Supervised-vs-Unsupervised-Learning_Kelleher-Tierney-2018.pdf` (Resource 1)
- `r2_Algorithms-Basic-Methods-4.1-4.3-1R-NaiveBayes-DecisionTrees_Witten-2017.pdf` (Resource 2)
- `r3_Trees-and-Rules-6.1-Decision-Trees-Pruning_Witten-2017.pdf` (Resource 3)
- `r4_Survey-of-Classification-Techniques-in-Big-Data_Koturwar-2015.pdf` (Resource 4)

---

## Key Highlights

### 1. Supervised versus Unsupervised Learning (Kelleher & Tierney 2018)

**Citation:** Kelleher, J. D. & Tierney, B. (2018). *Data science* (Chapter 4: Machine Learning 101, pp. 99-104). Cambridge, MA: MIT Press.
**Local source:** `r1_Supervised-vs-Unsupervised-Learning_Kelleher-Tierney-2018.pdf`

**Purpose:** Frames where classification sits in the wider ML map - the split between supervised and unsupervised learning - and introduces the ideas (target attribute, learning bias, correlation) that make a classifier possible in the first place.

---

#### 1. ML is a two-step partnership

- **Modelling stage of CRISP-DM.** ML runs inside the *modelling* phase: (1) an algorithm is applied to a dataset to find patterns, represented as a **model** (decision tree, regression, neural net); (2) the model is then used - either its *structure* reveals which attributes matter (e.g. stroke factors), or it *labels* new examples (spam / not spam).
- **Each algorithm carries a learning bias.** There are too many possible input→output functions to try them all, so every algorithm prefers certain kinds of function. The real skill in ML is matching an algorithm's **learning bias** to the dataset - usually found by experiment, not theory.

#### 2. Supervised vs unsupervised

| | **Supervised** | **Unsupervised** |
|---|---|---|
| Target attribute? | **Yes** - every instance is labelled | **No** labels |
| Goal | Learn a function: attributes → target (e.g. spam/not-spam) | Find *regularities* / structure |
| Typical task | **Classification**, prediction | **Clustering** (Module 9) |
| Cost | Labelling data is slow/expensive | No labelling needed, but learning is harder |
| Example | Spam filter, term-deposit prediction (BDA A2) | Grouping diabetes patients by similarity |

- **"Supervised" = the labelled data supervises the search.** The algorithm checks each candidate function against the known answers and uses that feedback to steer toward the best fit. Classification (this module) is the flagship supervised task.
- **Unsupervised** most commonly means **cluster analysis**: iteratively group rows that are more similar to each other than to the rest, maximising within-cluster similarity and across-cluster diversity. Similarity is usually **Euclidean distance** - but attributes with different ranges must be **normalized** first, or the wide-range attribute dominates.

#### 3. Correlation is the fuel for prediction

- **Pearson r** measures the strength of a *linear* relationship between two numeric attributes, from **-1 to +1** (`r=0` none, `±1` perfect). Rough reads: `±0.7` strong, `±0.5` moderate, `±0.3` weak.
- **Derived attributes can beat raw ones.** BMI (weight ÷ height²) correlates with diabetes (`r=0.877`) more strongly than weight (`0.655`) or height alone - because it models the *interaction*. **Attribute design** is where a lot of data-science value is created.
- **No correlation → no prediction.** If no input attribute (or function of them) correlates with the target, the best a model can do is always predict the target's central tendency. Strong correlation → a good chance of an accurate model.

#### Key Takeaways for BDA601
1. Module 6 is the **modelling stage** of the lifecycle you met in Module 1: cleaned data (Modules 4-5) now feeds a **supervised classifier**. Clustering is deferred to **Module 9 (unsupervised)**.
2. The **target attribute `y`** in the Bank Marketing dataset (term deposit: yes/no) is exactly what makes A2 a *supervised classification* problem.
3. Day-job link: a labelled column in your warehouse (churned? / fraud? / returned?) is what turns a reporting table into a *training set*. No label = you are in unsupervised territory and must cluster instead.

---

### 2. Algorithms - The Basic Methods: 1R, Naive Bayes, Decision Trees (Witten et al. 2017, §4.1-4.3)

**Citation:** Witten, I. H., Frank, E., Hall, M. A. & Pal, C. J. (2017). *Data mining: Practical machine learning tools and techniques* (4th ed., Chapter 4, §4.1-4.3, pp. 93-113). Cambridge, MA: Morgan Kaufmann.
**Local source:** `r2_Algorithms-Basic-Methods-4.1-4.3-1R-NaiveBayes-DecisionTrees_Witten-2017.pdf`

**Purpose:** The three foundational classifiers, taught "simplicity first". Establishes the recurring worked example (the 14-row weather dataset) and the core machinery - entropy, information gain, Laplace smoothing - that the activities test.

---

#### 1. 1R - the one-rule baseline (§4.1)

- **1R = a one-level decision tree.** Build a rule set from a *single* attribute: for each value, predict the majority class; count the training errors; pick the attribute with the fewest errors. Cheap, and surprisingly often accurate - "always try the simplest thing first".
- **Missing** is treated as just another attribute value. **Numeric** attributes are discretized: sort by value, place breakpoints where the class changes.
- **Overfitting trap:** 1R gravitates to attributes with many values (an ID-code attribute gives 0 training error but is useless on new data). Fix: force a **minimum count of the majority class per partition** (e.g. 3).

#### 2. Naive Bayes - simple probabilistic modelling (§4.2)

- **Uses all attributes**, assuming each contributes **independently, given the class** ("naive"). Built on **Bayes' rule**: `P(H|E) ∝ P(E1|H)·P(E2|H)·...·P(Ek|H)·P(H)`, then normalise so the class probabilities sum to 1.
- **The zero-frequency veto → Laplace smoothing.** If an attribute value never co-occurs with a class in training, its probability is 0 and vetoes everything (multiplied through). Fix: **add 1 to every count** (Laplace estimator) so no probability is ever exactly zero.

  > This is the **same idea as add-k smoothing** you met in DLE (n-gram language models) - a regulariser against overfitting the training counts.

- **Missing values are free** - simply omit that attribute from the product (a missing fraction drops from *both* class likelihoods and cancels in normalisation).
- **Numeric attributes:** assume a **Gaussian** per class - compute mean + std, then use the normal-density `f(x)` in place of a fraction.
- **Where it breaks:** redundant / correlated attributes. Adding a duplicate of an attribute *squares* its influence. Naive Bayes rewards careful attribute selection (Module 5).

#### 3. Decision trees - divide and conquer (§4.3)

- **Recursive:** pick the best attribute for the root, branch per value, recurse on each subset; stop when a node is pure (one class).
- **"Best" = highest information gain.** Purity is measured with **entropy** (units: **bits**):
  `Info(p1,...,pn) = -Σ pi·log2(pi)` - zero when a node is pure, maximal when classes are 50/50.
  `Gain(attr) = Info(parent) - weighted Info(children)`. On the weather data: `Gain(outlook)=0.247`, the winner.
- **Highly-branching attributes bias information gain** (again the ID-code problem: gain = full 0.940 but worthless). Fix: the **gain ratio** divides gain by the *split's own* intrinsic information, penalising many-way splits.

| Method | Uses | Strength | Main weakness |
|---|---|---|---|
| **1R** | 1 attribute | fastest baseline; interpretable | ignores attribute interactions |
| **Naive Bayes** | all attrs, independent | fast, robust, missing-value friendly | assumes independence; hurt by redundant attrs |
| **Decision tree** | best attr, recursively | readable rules; handles interactions | overfits without pruning (→ §6.1) |

#### Key Takeaways for BDA601
1. **Activity 1 is a by-hand decision tree** - this section is the exact recipe: compute `Info`, compute `Gain` per attribute, split on the max, recurse.
2. **Activity 2 is missing values** - Naive Bayes (omit the attribute) and 1R (missing = its own value) each give a defensible, quotable strategy; the deeper tree-based approach comes in §6.1.
3. Ties back to Module 5: **entropy/gain need clean, well-typed attributes**; redundant attributes (which reduction/PCA removes) actively hurt Naive Bayes.
4. Day-job link: 1R is the "what single column predicts this best?" gut-check you can run in SQL before reaching for any ML.

---

### 3. Trees and Rules - Decision Trees in Practice (Witten et al. 2017, §6.1)

**Citation:** Witten, I. H., Frank, E., Hall, M. A. & Pal, C. J. (2017). *Data mining: Practical machine learning tools and techniques* (4th ed., Chapter 6, §6.1, pp. 210-221). Cambridge, MA: Morgan Kaufmann.
**Local source:** `r3_Trees-and-Rules-6.1-Decision-Trees-Pruning_Witten-2017.pdf`

**Purpose:** Turns the textbook §4.3 tree into a **real-world** classifier (the C4.5 algorithm): handling numeric attributes, missing values, and - the headline - **pruning** to stop overfitting.

---

#### 1. Numeric attributes and missing values

- **Numeric = binary split.** Sort the values, evaluate a two-way `< threshold` test at each candidate breakpoint via information gain; put the threshold halfway between values. Store the sort order once so children don't need re-sorting.
- **Key asymmetry:** a **nominal** attribute is tested once per path (branch = value exhausts it); a **numeric** attribute can be tested **many times** down one path - readable trees may need multiway numeric tests.
- **Missing values → fractional instances.** Don't discard the row. Split the instance into weighted pieces sent down each branch in proportion to the training instances that took each branch; recombine the weighted leaf decisions at prediction time. Gain calculations just use the weights instead of integer counts.

#### 2. Pruning - the headline

- **Why:** a fully grown tree is **overfitted** - pure on training, poor on test data. **Postpruning** (grow full, then cut back) beats prepruning because it catches *combination-lock* effects (two attributes useless alone, powerful together).
- **Two operations:**

  | Operation | What it does |
  |---|---|
  | **Subtree replacement** | replace a whole subtree with a single leaf (works leaves→root) |
  | **Subtree raising** | lift the most-popular subtree to replace its parent (costlier; reclassifies instances) |

- **Decide with a pessimistic error estimate.** Training error is useless (the tree was built to minimise it). C4.5 instead takes the **upper confidence limit** of the error at each node (default confidence `c=25%`, `z=0.69`) as a pessimistic estimate. If a subtree's combined child error exceeds the parent's estimate, prune it. (Worked labor-negotiations example: children combine to `0.51` vs parent `0.46` → prune.)
- **CART's cost-complexity pruning** is the more thorough alternative: generate a sequence of ever-smaller trees ranked by error-increase-per-leaf `α`, then pick the best via a **holdout set or cross-validation**.

#### 3. Cost and trees→rules

- **Complexity of tree induction:** `O(m·n·log n) + O(n·(log n)²)` for *m* attributes, *n* instances - trees are cheap, which is why they are the "workhorses" of practical ML.
- **Trees → rules:** read one rule per leaf (conjunction of the root-to-leaf tests), then greedily drop conditions that don't raise the pessimistic error. Concise, but slow.

#### Key Takeaways for BDA601
1. **Pruning is the exam-critical idea:** the basic §4.3 tree *overfits*; §6.1 is how you make it generalise - the direct link to A2/A3, where a model must perform on *held-out* data, not just training.
2. **Missing values, done properly** = fractional/weighted instances, the sophisticated answer for **Activity 2** (beyond the Naive-Bayes-omit and 1R-as-a-value options).
3. Reuses Module 5 vocabulary: **numeric vs nominal** attribute types decide how the tree may split; confidence intervals echo the dispersion stats.
4. Day-job link: pruning is the "don't build a rule so specific it only ever matches one customer" discipline - a tree memorising your warehouse's training rows is the tabular version of overfitting.

---

### 4. A Survey of Classification Techniques in the Area of Big Data (Koturwar, Girase & Mukhopadhyay 2015)

**Citation:** Koturwar, P., Girase, S. & Mukhopadhyay, D. (2015). *A survey of classification techniques in the area of big data.* Maharashtra Institute of Technology, Pune. arXiv:1503.07477.
**Local source:** `r4_Survey-of-Classification-Techniques-in-Big-Data_Koturwar-2015.pdf`

**Purpose:** Zooms out to *big-data-scale* classification, and directly compares the two headline supervised classifiers - **Decision Tree vs Support Vector Machine** - on the axes that matter when data no longer fits on one machine.

---

#### 1. Classification at big-data scale

- **Two phases:** a *learning* phase (train on a huge labelled set → rules/patterns) then an *evaluation* phase (test accuracy on unseen data). Same supervised/unsupervised split as Resource 1.
- **Scaling decision trees:** partition a huge dataset into *n* pieces, learn a DT on each **in parallel**, then combine via **meta-learning**. Classic trees struggle at scale (build time; data-locality/communication cost), so **distributed C4.5 on MapReduce** is used - robust, fast, simple.
- **Scaling SVM:** vanilla SVM is **not scalable** (repeated scans of the data are expensive on noisy/imbalanced sets). **Clustering-Based SVM (CB-SVM)** scans the data once via hierarchical micro-clustering to pick high-quality samples.

#### 2. Decision Tree vs SVM - the comparison table

| Axis | **Decision Tree** | **SVM** |
|---|---|---|
| Predictive accuracy | Low | **High** |
| Fitting speed | **Fast** | Medium |
| Prediction speed | **Fast** | good only if *few* support vectors |
| Memory usage | **Low** | high if many support vectors |
| Easy to interpret | **Yes** | hard (kernel maps to high-D) |
| Handles categorical | **Yes** | No |
| Handles continuous | limited | **Yes** |
| Overfitting | prone (needs pruning) | **resists** (max-margin) |

- **DT advantages:** easy to understand and generate, reduces problem capacity. **Limits:** needs a separate test set, overfits. **Uses:** text categorisation, image classification.
- **SVM advantages:** high accuracy, learns the dimensionality of the feature space, kernel avoids a separate feature-extraction step, controls the complexity/error trade-off explicitly. **Limits:** kernel selection, expensive training, parameter tuning, no categorical data. **Uses:** text categorisation, handwriting/image recognition.
- **Verdict:** the paper concludes **SVM generally out-classifies DT on accuracy** - but the right tool depends on the application (interpretability and categorical data favour DT).

#### Key Takeaways for BDA601
1. Positions Module 6 inside **big data**: the same DT you build by hand in Activity 1 must be **parallelised (MapReduce/PySpark)** to run on a real lake - the through-line back to Module 4 (Spark).
2. The DT-vs-SVM table is a ready-made **decision matrix** for A2/A3: pick DT when you need to *explain* the model or have categorical features; reach for SVM when raw *accuracy* on high-dimensional data wins.
3. Bridges to the sister subject: **SVM is the whole of MLN601 Module 6** - here it appears as the accuracy-leading alternative to the trees BDA focuses on.
4. Day-job link: "partition → learn in parallel → combine" is exactly how you'd score a classifier across a sharded warehouse instead of pulling every row to one box.
