# MLN601 · Module 4 - One-Pager

> **Decision Trees · Gini & Entropy · Pruning · Bagging vs Boosting · XGBoost**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4.

**Pen legend:** 🖤 Black = core facts / skeleton · 🔵 Blue = examples & connections · 🔴 Red = traps & assessment hooks

---

## 🖤 The Big Idea (box it, top of page)
> **A decision tree = a stack of if-then rules learned by splitting data so each group gets "purer".** Non-parametric, supervised.
> 🔵 The ONE family that does **both classification AND regression** (CART), takes numeric + categorical, needs **no scaling**.
> 🔴 It is a **white-box / explainable** model - read the rule straight off the path root → leaf.

## 🖤 Anatomy of a Tree (draw it upside-down, top-left)
```
          [Root node]            ← best single split (whole dataset)
          /        \
   [Decision]    [Decision]      ← internal nodes = a test on a feature
    /     \          |
[Leaf]  [Leaf]    [Leaf]         ← terminal: class label / predicted value
```
🔵 Branch = outcome of a test · Sub-tree = any branch section · **Pruning = cut nodes to stop overfitting.**
🔵 Plain English: a tree is just **nested if-else statements.**

## 🖤 How a split is chosen → Impurity (the heart of it)
Greedy rule: at each node pick the split that **maximises purity** (biggest impurity drop).
```
Gini      = Σ pₖ(1 − pₖ)            ← CART default; LOWER = purer; binary splits
Entropy   = −Σ pₖ·log₂(pₖ)          ← 0 = pure, 1 = 50/50; from information theory
Info Gain = entropy(parent) − weighted entropy(children)   ← ID3 picks the MAX
```
🔵 **Regression** trees split on **variance / MSE** instead, then predict the **leaf mean**.
🔴 *Activity 2 is literally this maths - know Gini vs Entropy cold.*

## 🖤 Two classic algorithms (quick table)
| Algo | Metric | Splits |
|---|---|---|
| **ID3** | Entropy + Information Gain | multi-way |
| **CART** ⭐ | Gini index | binary only (sklearn default) |

## 🖤 Strengths vs Weaknesses (lecturer loves this contrast)
| ✅ Strengths | ⚠️ Weaknesses |
|---|---|
| White-box, easy to visualise | **Overfits** deep trees → prune |
| No scaling / normalisation needed | **Unstable** (small data change → new tree) |
| Handles numeric + categorical, missing values | **Piecewise-constant** → poor at extrapolation |
| Fast predict, O(log n) | **Biased on imbalanced classes** |

## 🖤 The sklearn knobs + workflow (code ladder)
```
DecisionTreeClassifier(criterion="gini", max_depth=…, min_samples_leaf=5,
                       ccp_alpha=…, random_state=42).fit(X, y)
   .predict(X)  /  .predict_proba(X)     # regression → DecisionTreeRegressor
```
🔵 Anti-overfit levers: **max_depth ↓ · min_samples_leaf ↑ · ccp_alpha** (cost-complexity pruning, applied *after* fit).
🔴 *No scaling needed (unlike Module 3) - trees split on thresholds, so monotonic scaling is irrelevant.*

## 🖤 One tree → ENSEMBLES (the big Module 4 leap)
| | **Bagging → Random Forest** | **Boosting → XGBoost** |
|---|---|---|
| How | many trees in **parallel**, bootstrap samples | trees **in sequence**, each fixes prior errors |
| Cures | **variance** (instability) | **bias** (weak learners) |
| Combine | **average / majority vote** | weighted sum of weak learners |
| Extra | + random feature subset per split | + regularisation, sparsity, parallelised |

🔴 *Bagging (parallel, vote) vs Boosting (sequential, correct) = THE most testable distinction.*

## 🔵 XGBoost - why it reigns (Morde)
Lineage: **Tree → Bagging → Random Forest → Boosting → Gradient Boosting → XGBoost.**
🔵 Wins on: **L1+L2 regularisation · native missing-value handling · parallelised · smart pruning · built-in CV.** Kaggle's workhorse for **tabular** data (deep learning still wins on images / text).

## 🔵 Explainability (the selling point - PwC XAI)
`plot_tree(model)` / `export_text()` → read the rules. XGBoost: `plot_tree(model, num_trees=i, rankdir="LR")` (needs **graphviz**).
🔵 *"Of all ML techniques, decision trees are the most explainable - you follow the branches to the exact factors used." (PwC)*

## 🔴 Pitfalls (red box - marks-losers)
- **Overfitting** a single deep tree → prune / cap depth / wrap in an ensemble.
- **Instability** → never over-read one tree's exact shape; ensembles are steadier.
- **Imbalanced classes** → the tree biases to the majority (your wine `quality` is mostly 5-6!).
- **Greedy ≠ optimal** → splits are locally best; the globally optimal tree is NP-complete.

## 🔵 Module 4 in practice (your 4 activities)
- **Act 1** visualise a DT (Google #2) · **Act 2** DT from scratch + Gini impurity (Google #8).
- **Act 3** sklearn DT on **wine** (Babu) · **Act 4** **Random Forest vs XGBoost** on UCI wine (Sblendorio).

## 🔴 Assessment Hook (bottom red strip)
**A1 = Regression Analysis, due 28 Jun (20%).** You already used **RandomForestRegressor** - Module 4 is *why it worked*: an ensemble of trees captures **non-linearity** a straight line cannot (your RF **R² ≈ 0.55 > linear baseline**).
🔵 *Write-up gold: `quality` is **ordinal + imbalanced** (mostly 5-6) → sklearn warns trees bias to the majority. Name **pruning / max_depth** as the overfit control, and frame RF as the **non-linear comparator** to your LinearRegression baseline (No Free Lunch). Hang it all on the CRISP-DM spine from Module 2.*

---

### Margin prompts (answer in blue while you write)
1. In your own data (Review Pulse / ClinicTrends), what is one decision a tree could model as if-then rules?
2. Random Forest or XGBoost for that problem - and *why* (variance vs bias)?
