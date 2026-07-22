# Module 9 — K-means Clustering

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| 0 | Watch Rose (2018) — intro video, basic K-means understanding (LinkedIn Learning) | 🕐 |
| **1** | Read & summarise Raghupathi (2018) — 10 interesting use cases for K-means | ✅ |
| 2 | Listen & summarise Data Skeptic (2015) — K-means clustering podcast | 🔥 WIP — needs manual listen |
| **3** | Read & summarise Hodgson / DotActiv (2020) — K-means and why it's good for business | ✅ |
| **4** | Read & summarise Pedregosa et al. — scikit-learn `2.3. Clustering` reference | ✅ |
| 5 | Activity 1: Country clusters + WCSS / elbow method (365 Data Science) | 🕐 |
| 6 | Activity 2: Weather data clustering, 1M records, k=12 (Tewari 2018) | 🕐 |

> **One-line frame:** K-means is **unsupervised** — no labels. You pick **k**, it finds **k centroids** and assigns every
> point to its nearest one, iterating until the centroids stop moving. It minimises **inertia** (within-cluster
> sum-of-squares, WCSS). The hard part is not the algorithm, it is **choosing k** (elbow / silhouette / gap statistic)
> and **evaluating clusters** when you have no ground truth to check against.

---

## Key Highlights

### 1. Raghupathi, K. (2018). 10 Interesting Use Cases for the K-Means Algorithm.

**Citation:** Raghupathi, K. (2018, 27 March). *10 interesting use cases for the K-means algorithm* [Web log post]. DZone.

**Purpose:** A short history plus a breadth-first tour of where K-means is actually deployed in industry — the "why should I care" resource, and the one that feeds the discussion-forum activities.

---

#### 1. History and definition
- The term **"k-means"** was coined by **James MacQueen (1967)**, in *Some methods for classification and analysis of multivariate observations*.
- The standard algorithm was used at **Bell Labs in 1957** for pulse-code modulation, and published by **E. W. Forgy (1965)** — hence it is also known as the **Lloyd-Forgy method**.
- **Clustering** = dividing data points into groups such that points in the same group are more similar to each other than to points in other groups.
- **Goal:** find groups in the data, where the number of groups is the variable **k**. The algorithm works **iteratively**, assigning each point to one of the k groups based on the features provided.

#### 2. The two outputs
| Output | What it is |
|---|---|
| **k centroids** | one centroid per identified cluster |
| **Labelled dataset** | every data point assigned to exactly one cluster |

#### 3. When K-means suits the data
- Best on data that is **numeric**, **continuous**, and has a **smaller number of dimensions**.
- The mental test: *"you want to make groups of similar things from a randomly distributed collection of things."*

#### 4. The ten use cases
| Domain | Use case |
|---|---|
| **Text / NLP** | **Document classification** — vectorise each doc, use term frequency, cluster the vectors |
| **Logistics** | **Delivery store optimisation** — K-means finds optimal drone launch locations; a genetic algorithm then solves the truck route as a TSP |
| **Public safety** | **Identifying crime localities** — cluster crime category × area to surface crime-prone zones |
| **Marketing** | **Customer segmentation** — segment by purchase history, interests, activity (e.g. prepaid telecom recharge/SMS/browsing patterns) |
| **Sport** | **Fantasy league stat analysis** — find similar players from player stats |
| **Insurance** | **Fraud detection** — isolate new claims by proximity to clusters of known fraudulent patterns |
| **Transport** | **Rideshare data analysis** — Uber trip data → traffic, transit time, peak pickup localities |
| **Security** | **Cyber-profiling criminals** — correlate user data preferences from log analysis |
| **Telecom** | **Call detail record (CDR) analysis** — cluster customer activity across 24 hours to segment by usage |
| **IT ops** | **Automatic clustering of IT alerts** — group high-volume network/storage/DB alerts to prioritise and predict failures |

#### Key Takeaways for MLN601
1. **Clustering is discovery, not prediction** — this is the module's break from Modules 3-8. There is no target column and no accuracy score.
2. The **IT alerts** and **CDR** cases are the closest analogues to a data-warehouse job — high-volume operational records, no labels, and the business question is *"what natural groups exist here?"*
3. Several use cases are **hybrid pipelines** (K-means + genetic algorithm for delivery). Clustering is often a *pre-processing / segmentation* step feeding another model, not the final answer.

---

### 2. Data Skeptic (2015). K-means Clustering [Podcast]. 🔥

**Citation:** Data Skeptic. (2015, 20 February). *[MINI] K-means clustering* [Audio podcast]. Retrieved from https://podcasts.apple.com/no/podcast/mini-k-means-clustering/id890348705?i=1000335938852

**Status:** 🔥 **WIP — needs manual listen.** No transcript is available at the cited Apple Podcasts URL or on the Data Skeptic site, and no local transcript exists in this module folder. Summarising it without listening would mean inventing content.

**What the module brief says to expect** (from the resource overview, *not* from the episode itself):
- Notes that **supervised applications are more prevalent than unsupervised** ones in practice.
- Uses a **simple, maths-free analogy** to explain the **centroid** and its relationship to K-means.
- Covers some **key application areas**.

**To complete this one:** listen via the Apple Podcasts link (it is a "MINI" episode, typically ~10-15 min), then either write the highlights directly or drop an audio file into this folder and run the `transcript-generator` skill on it.

---

### 3. Hodgson, E. / DotActiv (2020). K-Means Clustering and Why It's Good For Business.

**Citation:** Hodgson, E. (2020, 25 February). *K-means clustering and why it's good for business* [Web log post]. DotActiv.

**Purpose:** The practical **workflow** resource — the four-step process of running a cluster analysis, the three statistical methods for choosing k, and how to evaluate the result. This is the closest thing the module has to a procedure you can follow.

---

#### 1. What it is (business framing)
- **Unsupervised** — no labelled data, no training set.
- The objective, stated as an optimisation: **maximise similarity *within* clusters, minimise similarity *between* clusters.**
- **Advantages:** simple, flexible, and fast enough to cluster large datasets in a short time.
- **Disadvantages:** ⚠️ you **must specify k up front** (time-consuming, and harmful if chosen without a statistical or knowledge-backed method), and it is **sensitive to outliers**, which can change your groupings.

> **Cross-link:** outlier sensitivity is exactly the limitation the week 8 lecturer flagged for logistic regression and said he would add content on — see [module08_notes-class.md](../module-08-logistic-regression/module08_notes-class.md). It is a recurring weakness, not a one-off.

#### 2. The four-step process
| Step | What you do |
|---|---|
| **1. Collect and clean** | standardised format: each **row** = an observation, each **column** = a clustering variable. Remove or impute missing data. **Standardise the variables** so they are comparable |
| **2. Choose k** | via industry knowledge *or* one of three statistical methods (below) |
| **3. Run the algorithm** | identify centroids → assign each point to its nearest centroid → **re-iterate**, reallocating points until clusters are internally homogeneous and mutually heterogeneous |
| **4. Evaluate** | *"Your goal shouldn't be to just create clusters. It should be to create meaningful, accurate clusters that generate insights."* |

#### 3. Three ways to choose k ⭐
| Method | How it works | Read the answer as |
|---|---|---|
| **Elbow method** | run K-means for each candidate k; compute the total **within-cluster sum of squares (WSS/WCSS)**; plot WSS (y) vs k (x) | the **"elbow"** — the x-value where the curve bends |
| **Silhouette coefficient** | measures how close each point is to its own cluster's centroid; check across values of k | the k that **maximises** the average silhouette |
| **Gap statistic** | compares between-cluster variation for each k against its **expected value under a no-cluster (random) distribution** | the largest gap |

- **⭐ The elbow / WCSS method is the one Activity 1 explicitly requires.**

#### 4. What a cluster analysis gives you back
- A **vector of integers** (which cluster each point belongs to) — this is `labels_` in sklearn.
- A **matrix of cluster centres** — `cluster_centers_`.
- The **within-cluster sum of squares**, the **inter-cluster sum of squares**, and the **number of points per cluster**.

#### 5. Evaluating clusters
- **Good clusters** = points are close to their centroid *and* close to each other.
- **Inertia** — how far apart points within a cluster are. Measured from 0 upward; **smaller is better**.
- **Silhouette coefficient** — how far points in one cluster are from points in another. Range **−1 to 1**; **closer to 1 is better**. (Doubles as both a *choose-k* tool and an *evaluate* tool.)

#### 6. Business use cases
**Consumer segmentation** (demographic + psychographic + behavioural + performance data, then *profile* each cluster to tailor marketing) · **delivery optimisation** · **document sorting** · **customer retention / churn** (frequency, recency, average spend, basket composition) · **discount analysis** (bundle buyers vs EDLP vs on-sale-before-expiry).

#### Key Takeaways for MLN601
1. This is your **procedure** for Activity 1 and Activity 2 — steps 1-4, with the elbow method at step 2.
2. **Standardise before clustering.** K-means is distance-based, so an unscaled large-range feature will dominate every centroid calculation. Same discipline as regularisation in Module 8, different reason.
3. **Inertia (lower is better) and silhouette (higher is better) point in opposite directions** — do not mix up the sign. Easy exam slip.

---

### 4. Pedregosa et al. scikit-learn — `2.3. Clustering`.

**Citation:** Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR, 12*, 2825–2830. [`2.3. Clustering` documentation, v1.9.0]

**Purpose:** The technical reference — the actual objective function, the algorithm's three steps, its known failure modes, the variants (MiniBatch, Bisecting), and the full menu of evaluation metrics split by whether you have ground truth.

---

#### 1. The API pattern
- Every clustering algorithm comes in **two forms**: a **class** with a `.fit()` method, and a **function** returning an integer label array.
- After fitting, cluster assignments live in **`labels_`**; centroids in `cluster_centers_`.

#### 2. K-means, formally
- KMeans separates samples into **n groups of equal variance**, minimising **inertia**, a.k.a. the **within-cluster sum-of-squares**:

  ```
  inertia = Σᵢ min_{μⱼ ∈ C} ( ‖xᵢ − μⱼ‖² )      ← sum of squared distance to the nearest centroid
  ```

- **Centroids `μⱼ` are means, not data points** — they live in the same space as the data but are generally *not* members of it.
- **Lloyd's algorithm — three steps:**
  1. **Initialise** k centroids (naïvely: pick k random samples from X).
  2. **Assign** each sample to its nearest centroid.
  3. **Update** each centroid to the mean of the samples assigned to it.
  → repeat 2-3 **until the centroids move less than the tolerance** (sklearn's actual stopping rule).
- **Voronoi framing:** each iteration computes the Voronoi diagram of the current centroids; each cell becomes a cluster; centroids move to each cell's mean.
- **Equivalences:** K-means ≡ **expectation-maximisation** with a small, all-equal, diagonal covariance matrix; and ≡ a **Gaussian mixture model with equal covariance per component**.

#### 3. Known drawbacks (exam-grade) ⚠️
- **Inertia assumes clusters are convex and isotropic** — it responds **poorly to elongated clusters** or irregular manifolds.
- **Inertia is not normalised.** Lower is better and 0 is optimal, but there is no absolute scale. In high dimensions Euclidean distances become inflated (**curse of dimensionality**) — run **PCA first** to alleviate it *and* speed up computation.
- **Convergence is guaranteed, but possibly to a local minimum**, and this is **highly dependent on initialisation**.

#### 4. Fixing initialisation: k-means++
- **`init='k-means++'`** initialises centroids to be **generally distant from each other**, giving probably better results than random init.
- Standard practice is also to run the whole thing **several times with different initialisations** (`n_init`).
- `sklearn.cluster.kmeans_plusplus` can be called standalone to seed *other* clustering algorithms.
- `sample_weight` lets you weight samples when computing centres (weight 2 ≡ duplicating that row).

#### 5. Variants
| Variant | What changes | When to use |
|---|---|---|
| **`MiniBatchKMeans`** | each iteration draws a random **mini-batch** of b samples; centroids updated per-sample as a **streaming average** | **large datasets** — converges much faster, results "generally only slightly worse", and in practice the quality gap is often small |
| **`BisectingKMeans`** | **divisive hierarchical**: repeatedly split one cluster into two until k is reached. Split target chosen by `bisecting_strategy='largest_cluster'` (faster, usually as accurate) or `'biggest_inertia'` | **large k**; produces **no empty clusters**, more **similar-sized** clusters, and a visible hierarchy. Beats random-init KMeans; comparable to `k-means++` at lower cost |

> **Activity 2 hook:** the weather notebook is **1 million records with k=12** — exactly the `MiniBatchKMeans` scenario. Worth running both and timing them.

#### 6. Evaluation — the fork in the road ⭐
> *"Evaluating the performance of a clustering algorithm is not as trivial as counting the number of errors or the precision and recall of a supervised classification algorithm."*
>
> An evaluation metric **must not consider the absolute values of the cluster labels** — cluster "0" and cluster "1" are arbitrary names, so any metric has to be **permutation-invariant**.

**A. Ground truth known** (you have labels, you're checking the clustering against them):

| Metric | Range / reads |
|---|---|
| **Rand index** (`rand_score`) | similarity of two assignments, ignoring permutations. ⚠️ **does not give ~0 for random labelling** |
| **Adjusted Rand index** (`adjusted_rand_score`) | **corrects for chance** — use this one instead |
| **Homogeneity** | each cluster contains only members of a **single class**. 0→1, higher better |
| **Completeness** | all members of a class land in the **same cluster**. 0→1, higher better |
| **V-measure** | the **harmonic mean** of homogeneity and completeness (`beta` defaults to 1.0) |
| Mutual Information scores, Fowlkes-Mallows | further alternatives |

**B. Ground truth unknown** (the realistic clustering case):

| Metric | Range | Direction |
|---|---|---|
| **Silhouette Coefficient** — `s = (b − a) / max(a, b)`, where **a** = mean distance to points in the *same* cluster, **b** = mean distance to points in the *next nearest* cluster | **−1 to +1** (~0 = overlapping clusters) | **higher = better** |
| **Calinski-Harabasz Index** (Variance Ratio Criterion) — ratio of between-cluster to within-cluster dispersion | unbounded | **higher = better**; fast to compute |
| **Davies-Bouldin Index** — average 'similarity' between clusters (distance vs cluster size) | **0 upward** | **lower = better**; simpler than silhouette, but Euclidean-only |

⚠️ **All three share one bias:** they score **convex clusters higher** than density-based ones (e.g. DBSCAN's). Do not use them to conclude K-means "beat" DBSCAN.

#### 7. Where K-means sits among the alternatives
| Algorithm | Scalability | Use case | Geometry |
|---|---|---|---|
| **K-Means** | **very large `n_samples`**, medium `n_clusters` (MiniBatch for more) | general-purpose, **even cluster size, flat geometry**, not too many clusters, **inductive** | distances between points |
| **DBSCAN** | very large `n_samples` | **non-flat geometry, uneven sizes, outlier removal**, transductive | distance to nearest points |
| **Spectral clustering** | medium `n_samples`, small `n_clusters` | few clusters, even size, **non-flat geometry** | graph distance |
| **Ward / Agglomerative** | large | many clusters, connectivity constraints | distances / any pairwise |
| **Gaussian mixtures** | **not scalable** | flat geometry, **density estimation** | Mahalanobis to centres |
| **BIRCH** | large | large dataset, outlier removal, **data reduction** | Euclidean |

- **Inductive** (K-means, DBSCAN is not) = the fitted model **can be applied to new, unseen data**. **Transductive** methods cannot.

#### Key Takeaways for MLN601
1. **Inertia = WCSS = what the elbow method plots.** The three names in resources 3, 4 and Activity 1 are the same quantity — do not treat them as separate concepts.
2. **Always set `init='k-means++'` and `random_state=<seed>`.** The first fixes the local-minimum problem, the second satisfies the repo's fixed-seed ML discipline.
3. **Silhouette ↑ good, Davies-Bouldin ↓ good, inertia ↓ good, Calinski-Harabasz ↑ good.** Memorise the directions as a set — mixing them up is the easiest way to draw a backwards conclusion.
4. **"Flat geometry, even cluster size"** is K-means' precondition. If a comparison question asks *why* K-means failed on some dataset, this row of the table is the answer.

---

## Synthesis — how the four fit together

```
        WHAT IT IS                    HOW TO RUN IT                     HOW TO JUDGE IT
  unsupervised, no labels (R1,3)   4 steps: clean → pick k        ground truth? → ARI, homogeneity,
  k centroids + labelled data (R1)    → run → evaluate (R3)          completeness, V-measure (R4)
  minimise inertia/WCSS (R4)       choose k: elbow / silhouette   no ground truth? → silhouette ↑,
  Lloyd's 3 steps, k-means++ (R4)     / gap statistic (R3)           Calinski-Harabasz ↑, D-B ↓ (R4)
  10 industry use cases (R1)       scale features first (R3)      ⚠️ all biased toward convex clusters
                                   big data → MiniBatch (R4)
```

**The through-line:** this module is the **unsupervised counterpart** to everything since Module 3. The
algorithm itself is the easy part — the graded thinking is in **justifying your k** (elbow, with the plot) and
**evaluating without an accuracy score**. Both discussion activities ask exactly that: *"how did you establish the
number of clusters, and did others get a different number?"* Activity 2 also asks whether K-means is useful for
the **bike-sharing project (Assessment 3)** — a real question worth answering with the "flat geometry, even
cluster size, inductive" criteria above.
