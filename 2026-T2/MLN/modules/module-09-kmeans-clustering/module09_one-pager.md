# MLN601 · Module 9 - One-Pager

> **K-means Clustering · distance metrics · inertia/WCSS/SSE · choosing k · evaluation without labels · DBSCAN/OPTICS**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **K-means is *unsupervised* - no labels, no target column. You pre-pick `k`, it places `k` centroids and assigns every point to its *nearest* one (a distance calc), iterating until the centroids stop moving. It minimises *inertia*. Clustering is *discovery*, not prediction - the module's clean break from Modules 3-8.**
> (Raghupathi 2018 · Hodgson/DotActiv 2020 · scikit-learn `2.3` · **Wk 9 lecture**)

⚠️ **K-means ≠ KNN.** K-means = *unsupervised*, `k` = number of **clusters**. KNN = *supervised*, `k` = number of **voting neighbours**. Same letter, opposite worlds - the classic trap.

---

## 🖤 Zone 1 - Distance = the engine ⭐ (class - NOT in readings)
- 🖤 **"Nearest centroid" needs a distance.** Similarity ↑ = alike (≈1), dissimilarity ↓ = alike (0). **Proximity** = either (ask which).
- 🔵 **Euclidean** `√(Σ(aᵢ−bᵢ)²)` - the default. **Square then root:** square kills the sign (so +3/−3 don't fake-cancel), root re-normalises scale. Symmetric → fill upper triangle only.
- 🔵 **Minkowski = the generic form** `(Σ|aᵢ−bᵢ|^r)^(1/r)`: **`r=1` Manhattan** · **`r=2` Euclidean** · **`r=∞` Chebyshev/supremum** (max single-attr diff).
- 🔵 **Binary vectors:** **SMC** counts 0-0 as similar · **Jaccard** ignores 0-0. 🔴 *His point:* two students who **both** lack PR *are* alike → pick the metric to match what "absent" means.
- 🔵 **Documents → cosine** `(D1·D2)/(‖D1‖‖D2‖)` - uses **actual counts** (10× vs 1× ≠ identical), not just present/absent.

## 🖤 Zone 2 - Lloyd's loop + the objective
- 🖤 **Loop:** place k centroids → **assign** each point to nearest → **move** each centroid to the **mean** of its points → repeat **until no point changes cluster** (stopping rule).
- 🔵 **Objective = inertia = WCSS = SSE** (one quantity, 4 names; class calls it **SSE**): `Σ min‖xᵢ−μⱼ‖²`. **Lower better, 0 optimal, NOT normalised** → compare across k only.
- 🔵 **Centroids are means, NOT data points.** Outputs: `labels_` (vector) + `cluster_centers_` (matrix).
- 🔴 **Scale features first** - distance-based → an unscaled wide feature dominates every centroid. High-dim inflates distance → **PCA first**.

## 🖤 Zone 3 - Choosing k (the hard part) ⭐ SLO b)/c) - THE GRADED CORE
| Method | How | Read as |
|---|---|---|
| **Elbow** ⭐ | plot **WCSS (y) vs k (x)** | the **bend** |
| **Silhouette** | tight-to-own vs far-from-next | **max** avg silhouette |
| **Gap statistic** | vs a random no-cluster distribution | **largest gap** |

- 🔴 Elbow/WCSS is what **Activity 1** requires; the forum grills *"did everyone get the same k?"* - the honest **"no, and here's why"** *is* the graded insight. There is **no single right k**.

## 🖤 Zone 4 - k-means++ & big-data variants
- 🔴 **Always `init='k-means++'` + `random_state=<seed>` + `n_init`.** k-means++ seeds far-apart centroids (converges only to a *local* min otherwise); seed = repo's fixed-seed rule.
- 🔵 **`MiniBatchKMeans`** = big data (mini-batch per step, slightly worse, much faster) · **`BisectingKMeans`** = large k (divisive, no empty clusters).
- 🔴 **Activity 2 = 1M weather rows, k=12** → the MiniBatch case. Run both, **time them**.

## 🖤 Zone 5 - Evaluation: the fork ⭐ SLO c)/d)
- 🖤 Metric must be **permutation-invariant** (cluster "0"/"1" are arbitrary names).
- 🔵 **Ground truth known:** **ARI** (corrects for chance, use over Rand) · Homogeneity (1 class/cluster) · Completeness (1 cluster/class) · V-measure (harmonic mean).
- 🔵 **No ground truth (realistic):**

  | Metric | Range | Dir |
  |---|---|---|
  | **Silhouette** | −1..+1 | **↑** |
  | **Calinski-Harabasz** | unbounded | **↑** |
  | **Davies-Bouldin** | 0↑ | **↓** |

- 🔴 **Directions as a SET:** inertia ↓ · silhouette ↑ · CH ↑ · DB ↓. Mixing signs = backwards conclusion. All 3 (no-GT) are **biased toward convex clusters** - don't claim K-means "beat" DBSCAN.

## 🖤 Zone 6 - Limits → the rest of the family ⭐ (class)
- 🖤 **intra**-cluster similarity **↑** (tight), **inter**-cluster similarity **↓** (far apart). Mnemonic: **inter**state = between two states.
- 🔴 **K-means fails on:** different **sizes/densities** · **non-globular shapes** (his **S-shape** - K-means only makes **spherical** blobs) · **outliers** (centroid = mean; one 700K salary drags the average).
- 🔵 **The fixes (lecture-only, know they exist):**
  - **K-medoids / K-median** → median / real point as centre = outlier-robust.
  - **DBSCAN** → density: **eps + minPts**; core/border/**noise** points; arbitrary shapes; **no k needed**; but scattered data → everything = noise.
  - **OPTICS** → DBSCAN that adapts to **varying density**.

---

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - ML Project (40%)** · notebook + model selection + **up to 2000 words** · due **19 Aug 2026** · SLOs **a) b) c) d)**.
> ⚠️ **A3 is a REGRESSION task** (like A1 - "swap the dataset", keep GridSearchCV + XAI), **not** a clustering assessment. Activity 2's bike-sharing question is *"would K-means even help here?"* - answer with **flat geometry / even size / inductive**; if you cluster, **justify k with an elbow plot** and **evaluate with silhouette**.

## 🔴 If you only memorise 5 things
1. **Unsupervised, no labels.** "Nearest centroid" needs a **distance** (Euclidean default; Minkowski `r`=1/2/∞ → Manhattan/Euclidean/Chebyshev).
2. **inertia = WCSS = SSE** = `Σ min‖xᵢ−μⱼ‖²`, **lower better**, not normalised. **Scale features first.**
3. **Choosing k is the graded part** - elbow (WCSS vs k), silhouette, gap. No single right answer.
4. **Directions as a set:** inertia ↓ · silhouette ↑ · Calinski-Harabasz ↑ · Davies-Bouldin ↓.
5. **K-means = spherical + mean** → fails on odd shapes/outliers → **K-medoids, DBSCAN (no k, any shape, handles noise), OPTICS.**

*(Runner-up: **K-means ≠ KNN** · **intra** ↑ / **inter** ↓ · SMC counts 0-0 as similar, Jaccard doesn't.)*

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your school's operational records (IT tickets, or student rows with no "correct grouping" label) are the **no-ground-truth** case. Which metric must you use to judge the clusters - and why can't you use accuracy?
2. You already carry **z-scores** through the pipeline. Z-score *is* standardisation. One line: why is that a hard prerequisite for K-means but irrelevant to a decision tree? And which distance metric would you reach for on your **binary** attendance/flag columns - Euclidean or Jaccard?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 Watch Rose (2018) - intro K-means video (LinkedIn Learning)
- [ ] 🔥 Data Skeptic (2015) podcast - manual listen (no transcript; ~10-15 min "MINI"), note the centroid analogy
- [ ] 🕐 Activity 1: Country clusters + **WCSS/elbow** → post how you chose k (365 Data Science)
- [ ] 🕐 Activity 2: Weather 1M records, k=12 → try `MiniBatchKMeans`, answer the bike-sharing (A3) question
