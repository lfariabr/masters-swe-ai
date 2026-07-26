# MLN601 · Module 9 - One-Pager

> **K-means Clustering · unsupervised · inertia/WCSS · choosing k · evaluation without labels**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **K-means is *unsupervised* - no labels, no target column. You pre-pick `k`, it places `k` centroids and assigns every point to its nearest one, iterating until the centroids stop moving. It minimises *inertia* (within-cluster sum-of-squares). Clustering is *discovery*, not prediction - the module's clean break from Modules 3-8.**
> (Raghupathi 2018 · Hodgson/DotActiv 2020 · scikit-learn `2.3 Clustering`)

⚠️ **K-means ≠ KNN.** K-means = *unsupervised*, `k` = number of **clusters**. KNN = *supervised*, `k` = number of **voting neighbours**. Same letter, opposite worlds - the classic trap.

---

## 🖤 Zone 1 - Lloyd's algorithm (the 3-step loop)
- 🖤 **1. Initialise** `k` centroids · **2. Assign** each point to its nearest centroid · **3. Update** each centroid to the **mean** of its points → repeat 2-3 **until centroids move < tolerance**.
- 🔵 **Centroids are means, NOT data points** - they live in the data's space but generally aren't members of it.
- 🔵 **Two outputs:** a **label vector** (`labels_`, which cluster each point is in) + a **matrix of centres** (`cluster_centers_`).
- 🔵 **Voronoi framing:** each iteration = the Voronoi diagram of the current centroids; each cell → a cluster.
- 🔴 **Converges, but only to a *local* minimum** - highly dependent on where you start. That's *why* k-means++ exists (Zone 4).

## 🖤 Zone 2 - The objective: inertia = WCSS ⭐ SLO c)
- 🖤 **One quantity, three names:** **inertia = within-cluster sum-of-squares = WCSS**. Do not treat as separate.
  ```
  inertia = Σᵢ  min_{μⱼ}  ‖ xᵢ − μⱼ ‖²      ← squared distance to the NEAREST centroid, summed
  ```
- 🔵 **Lower is better, 0 is optimal** - but **not normalised**, so there's no absolute "good" value. You compare it *across k*, never as a standalone score.
- 🔴 **Scale features FIRST.** K-means is distance-based → an unscaled wide-range feature dominates every centroid. Same discipline as Module 8 regularisation, different reason. `StandardScaler` before `.fit()`.
- 🔴 **High dimensions inflate distances** (curse of dimensionality) → run **PCA first** to alleviate *and* speed up.

## 🖤 Zone 3 - Choosing k (the actual hard part) ⭐ SLO b)/c) - THE GRADED CORE
| Method | How | Read the answer as |
|---|---|---|
| **Elbow** ⭐ | run K-means for each k; plot **WCSS (y) vs k (x)** | the **"elbow"** - where the curve bends |
| **Silhouette** | how tight-to-own vs far-from-next each point is | the k that **maximises** avg silhouette |
| **Gap statistic** | between-cluster variation vs its value under a **random no-cluster** distribution | the **largest gap** |

- 🔴 **The elbow / WCSS method is what Activity 1 requires** - and what the discussion forum grills: *"did everyone get the same k? if not, why?"* The honest answer (real data rarely gives a clean bend) **is** the graded insight.
- 🔵 There is **no single right k**. The algorithm is easy; justifying `k` is the thinking.

## 🖤 Zone 4 - k-means++ & the big-data variants
- 🔴 **Always `init='k-means++'` + `random_state=<seed>`.** k-means++ seeds centroids far apart (beats random); the seed satisfies the repo's fixed-seed rule. Also bump **`n_init`** (several restarts, keep the best).
- 🔵 **`MiniBatchKMeans`** - random mini-batch per iteration, streaming centroid update. **Big data**; slightly worse, much faster.
- 🔵 **`BisectingKMeans`** - divisive: repeatedly split one cluster in two until k. **Large k**; no empty clusters, similar-sized groups.
- 🔴 **Activity 2 = 1M weather rows, k=12** → the textbook `MiniBatchKMeans` case. Run both, **time them**, comment on the gap.

## 🖤 Zone 5 - Evaluation: the fork in the road ⭐ SLO c)/d)
> An evaluation metric **must be permutation-invariant** - cluster "0" vs "1" are arbitrary names.

**A. Ground truth known** (you have labels to check against):
- 🔵 **Adjusted Rand Index** (corrects for chance - use over plain Rand) · **Homogeneity** (each cluster = one class) · **Completeness** (each class → one cluster) · **V-measure** (harmonic mean of the two).

**B. No ground truth** (the realistic case):
| Metric | Range | Direction |
|---|---|---|
| **Silhouette** `s=(b−a)/max(a,b)` | −1 to +1 (~0 = overlap) | **higher ↑** |
| **Calinski-Harabasz** (variance ratio) | unbounded | **higher ↑**, fast |
| **Davies-Bouldin** | 0 upward | **lower ↓** |

- 🔴 **Memorise the directions as a SET:** inertia ↓ · silhouette ↑ · Calinski-Harabasz ↑ · Davies-Bouldin ↓. Mixing signs = a backwards conclusion.
- 🔴 **All three (B) are biased toward convex clusters** - do **not** use them to claim K-means "beat" DBSCAN.

## 🖤 Zone 6 - Where K-means fits (and where it fails)
- 🔵 **Preconditions:** numeric, continuous, **flat geometry**, **even cluster sizes**, not-too-many clusters, **inductive** (can label *new* data).
- 🔴 **Weaknesses (exam-grade):** must specify k up front · **sensitive to outliers** (one bad point drags a centroid) · assumes convex/isotropic clusters (fails on elongated/irregular shapes) · only a local minimum.
- 🔵 **vs DBSCAN** = non-flat geometry, uneven sizes, outlier removal, *transductive*. **vs Gaussian mixtures** = density estimation, not scalable.

---

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Machine Learning Project (40%)** · notebook + model selection + **up to 2000 words** · due **19 Aug 2026** · SLOs **a) b) c) d)**.
> Module 9 feeds A3's **bike-sharing** project. The live question (Activity 2): *is K-means useful here?* Answer it with the **"flat geometry / even size / inductive"** criteria - and if you cluster, **justify k with an elbow plot** and **evaluate with silhouette** (no ground-truth labels to lean on).

## 🔴 If you only memorise 5 things
1. **Unsupervised, no labels.** Lloyd's loop: init → assign-to-nearest → move-to-mean → repeat till stable.
2. **inertia = WCSS**, one quantity: `Σ min‖xᵢ−μⱼ‖²`, **lower better**, not normalised. **Scale features first.**
3. **Choosing k is the graded part** - elbow (plot WCSS vs k), silhouette, gap statistic. No single right answer.
4. **Directions as a set:** inertia ↓ · silhouette ↑ · Calinski-Harabasz ↑ · Davies-Bouldin ↓.
5. **`init='k-means++'`, `random_state`, `n_init`.** Weak on: outliers, non-convex shapes, high dimensions (→ PCA).

*(Runner-up: **K-means ≠ KNN** - clusters vs neighbours, unsupervised vs supervised.)*

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your school's operational records (IT tickets, or student rows with no "correct grouping" label) are exactly the K-means case: **no ground truth**. If you clustered them, which metric would you *have* to use to judge the result - and why can't you use accuracy?
2. You already carry **z-scores** through the pipeline. Z-score *is* feature standardisation. Explain in one line why that step is a hard prerequisite for K-means but irrelevant to a decision tree.

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 Watch Rose (2018) - intro K-means video (LinkedIn Learning)
- [ ] 🔥 Data Skeptic (2015) podcast - manual listen (no transcript; ~10-15 min "MINI"), then note the centroid analogy
- [ ] 🕐 Activity 1: Country clusters + **WCSS/elbow** → post how you chose k (365 Data Science)
- [ ] 🕐 Activity 2: Weather 1M records, k=12 → try `MiniBatchKMeans`, answer the bike-sharing (A3) question
