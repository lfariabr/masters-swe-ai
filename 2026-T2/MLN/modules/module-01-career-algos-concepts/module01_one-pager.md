# MLN601 · Module 1 — One-Pager

> **Careers · Key Concepts · Applications · Algorithms · Software**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4.

**Pen legend:** 🖤 Black = core facts / skeleton · 🔵 Blue = examples & connections · 🔴 Red = traps, ethics & assessment hooks

---

## 🖤 The Big Idea (box it, top of page)
> **ML = algorithms that learn patterns from data instead of hand-coded rules** → to **predict** or **discover structure**.
> ML ⊂ AI. This subject = **classical / "shallow" ML** (not deep learning).

## 🖤 The Workflow (write as a spine down the left)
```
Problem → Data → Features X + Labels y → Train/Test split
       → model.fit() → model.predict() → Evaluate → Interpret → Communicate limits
```
🔴 *Memorise this. It repeats in every module and every assessment.*

## 🖤 Shallow vs Deep (two columns)
| Classical / Shallow (THIS subject) | Deep Learning (background only) |
|---|---|
| Features = **manual**, need domain expertise | Features **auto-learned** from raw data |
| Regression, SVM, decision tree, K-means, perceptron | Neural networks, many layers |
| Explainable, light compute, tabular data | Black-box, heavy infra, images/audio/text |

🔵 Most real business data is **structured/tabular** → shallow ML is still the workhorse.

## 🖤 3 Types of Learning
- **Supervised** → labelled data → predict (most of this subject) 🔵 regression, trees, SVM, logistic, perceptron
- **Unsupervised** → no labels → find structure 🔵 K-means clustering
- **Reinforcement** → actions + rewards (background only)

## 🖤 Key Vocab (quick-fire, write small, 2 cols)
- **Feature** = measurable input var · **Label/target (y)** = what you predict
- **X** = feature matrix → rows = *samples*, cols = *features*
- **Model parameter** = learned from data (e.g. regression coefficient)
- **Hyperparameter** = you / search sets it (tree depth, k, regularisation) 🔴 *know this difference cold*
- **Train set** = fit on it · **Test set** = stays hidden until evaluation

## 🖤 The Python Stack (write as a little tower)
`NumPy` (arrays) → `Pandas` (tables) → `Matplotlib/Seaborn` (viz) → **`scikit-learn`** (the ML) → all inside `Jupyter`
🔵 scikit-learn's killer pattern: **`fit()` / `predict()` / `transform()` / `score()`** — same shape for every algorithm.
🔵 Cloud ML vendors: AWS SageMaker · Google Cloud AI · Azure ML.

## 🔴 Pitfalls (red box — these are marks-losers)
- **Data leakage** → fit preprocessing on TRAIN only → use **Pipelines**
- **Wrong metric** → accuracy hides minority class (imbalance)
- **No `random_state`** → not reproducible
- **Overfitting** → use cross-validation / simpler model

## 🔵 Applications (2 case studies — your forum ammo)
- **Target pregnancy prediction** (Hill 2012) → purchases → predict life event. 🔴 *"Accurate" ≠ "acceptable" → privacy, consent; hiding it = trust problem.*
- **COVID-19 severity** (Jiang 2020) → 53 patients, predict ARDS. KNN & SVM ~80%. 🔴 *Tiny data, 5 positives → class imbalance, needs external validation.*

## 🔵 Career Angle (Townes 2017)
"Skilled in ML" = the new "proficient in Excel." 🔵 *Tie software-eng background → ML automation, product analytics, responsible AI.*

## 🔴 Assessment Hook (bottom red strip)
**A1 = Regression, due 28 Jun (20%).** Module 1 habits that earn marks:
1. State the **target** clearly  2. Explain **features + preprocessing**  3. Clean **train/test or CV**  4. Report **regression metrics** (not just charts)  5. Discuss **overfitting + limits**

---

### Margin prompts (answer in blue while you write)
1. Where in *your* current work could the `X → fit → predict → evaluate` loop replace a manual decision?
2. Pick one case study — who are the **stakeholders** who'd see the same prediction differently?
