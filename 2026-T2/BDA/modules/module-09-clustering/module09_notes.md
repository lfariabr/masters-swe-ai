# Module 9 - Clustering

## TL;DR
- **Why:** Modules 6-8 were all **supervised** - labelled data, predict a target `y`. Module 9 drops the label entirely: **clustering** groups similar records with no target variable at all.
- **K-means** (the module's core algorithm): pick k random centroids → assign every point to its nearest centroid → recompute centroids as the mean of their points → repeat until convergence. It's **distance-based**, and it **assumes clusters are round, similarly sized, and similarly dense** - real data that violates that assumption still gets an answer, just the wrong one.
- **Choosing k has no single right answer** - the elbow method (k vs inertia) and silhouette score (per-point fit, -1 to +1) give a defensible range, not a verdict. Pushing k → n always "improves" inertia and is worthless - the same overfitting trap as Module 8's R²=1.0 demo.
- **Alternatives when k-means' assumptions break:** `GaussianMixture` (elliptical/unequal-variance clusters), **hierarchical clustering** (dendrogram, no k needed upfront), **DBSCAN** (density-based, arbitrary shapes, auto-flags outliers instead of forcing every point into a cluster).
- **Assessment 3 familiarisation** starts this module (due Week 12, 40%).

## Task List

| # | Task | Status |
|---|------|--------|
| 1 | Read & summarise Xu & Wunsch (2009) - Cluster Analysis (Ch1, pp. 1-12) | 🔥 WIP - needs manual access (ebook) |
| **2** | Read & summarise Le (2019) - An Introduction to Big Data: Clustering | ✅ |
| **3** | Read & summarise Sharma (2019) - The Most Comprehensive Guide to K-Means Clustering | ✅ |
| **4** | Watch & summarise Sullivan (2017) - Spark for Machine Learning and AI: K-means Clustering | ✅ |
| 5 | Activity 1: Determine the Value of K (forum post) | 🕐 |
| 6 | Activity 2: Clustering Tool - run the scikit-learn K-means example, explain the 4 graphs (8 vs 3 clusters) | 🕐 |

**Local sources (this folder):**
- `r2_An-Introduction-to-Big-Data-Clustering_Le-2019.pdf` (Resource 2)
- `r3_The-Most-Comprehensive-Guide-to-K-Means-Clustering_Sharma-2019.pdf` (Resource 3 - Sharma's article; site has since retitled/updated it from "The Most Comprehensive Guide" but it's the same Analytics Vidhya piece)
- `r4_Spark-for-ML-and-AI-K-means-Clustering_Sullivan-2017.md` (Resource 4 - Sullivan video transcript)
- `bonus_Demonstration-of-K-means-Assumptions_scikit-learn-docs.pdf` - not one of the four listed resources, but directly useful for Activities 1 and 2 (see the bonus section below)
- ⚠️ **Resource 1** (Xu & Wunsch, *Cluster Analysis*) is a ProQuest/EBSCO ebook behind Torrens auth - no local PDF exists. Summarise once you can access and paste/export the chapter text; until then this file's Key Highlights below cover Resources 2-4 plus the bonus scikit-learn doc.

---

## Key Highlights

### 2. An Introduction to Big Data: Clustering (Le 2019)

**Citation:** Le, J. (2019). *An introduction to big data: Clustering*. Retrieved from https://medium.com/cracking-the-data-science-interview/an-introduction-to-big-data-clustering-1a911b83e590
**Local source:** `r2_An-Introduction-to-Big-Data-Clustering_Le-2019.pdf`

**Purpose:** A compact tour of the three clustering *families* - centroid (k-means), graph/hierarchical, and density (DBSCAN) - with worked-by-hand examples for each. Where Sharma (R3) goes deep on k-means alone, Le's value is the **breadth**: it's the resource that shows k-means is one choice among several, not the only shape clustering can take.

---

#### 1. Clustering, defined, and the four model families

- **Clustering** = unsupervised grouping of data points so that points in the same group are similar, and points in different groups are dissimilar. **Unsupervised** because there is no target/label to predict - the module's clean break from Modules 6-8.
- Four families, by what "similar" means: **connectivity** (distance), **centroid** (central individual + distance - k-means), **density** (connected dense regions - DBSCAN), **graph-based** (cliques). Le covers **k-means, hierarchical, DBSCAN**.

#### 2. K-means, worked by hand

- **Algorithm:** pick k random means → assign every point to its nearest mean (this partition is a **Voronoi diagram**) → recompute each cluster's centroid as the new mean → repeat until convergence.
- 🔵 **Worked example** (9 points, k=2, Manhattan distance): random centroids `(2,8)` and `(8,1)` → after 1 round of reassign-and-recompute, centroids move to `(4,5)` and `(2,2)` → after another round, `(6,7)` and `(1,3)` → third round: **centroids stop moving** ((6,7) and (1,3) recur) → **converged**.
  - ⚠️ **Source erratum:** Le's own worked example pairs **Manhattan distance** with **mean-based** centroid updates - that combination is internally inconsistent. Textbook k-means pairs **Euclidean** distance with the **mean** (minimising squared error); pairing Manhattan distance with a **median** update is the correct combination, and that variant is called **k-medians**, not k-means. Cite the worked steps for the mechanics, not as a precise definition of vanilla k-means.
- 🔴 **Choosing k is a bias/variance problem in disguise:** increasing k **without penalty always reduces error**, down to zero error at k=n (every point its own cluster). That extreme is useless - it's Module 8's overfitting lesson wearing a different hat: a "perfect" clustering (k=n) is not evidence of a good model, it's a sign you've stopped modelling anything.
- **Two selection criteria:**
  - **SSE (sum of squared errors):** minimise the within-cluster squared distance to centroid. Plotted against k, this is the **elbow method**.
  - **Silhouette:** per-point score comparing distance to own cluster vs. nearest neighbouring cluster. **+1** = well-matched, **0** = borderline, **-1** = likely wrong cluster. 🔵 Worked example: 3 clusters of 2 points each → per-point silhouettes `0.8, 0.75, 0.43, 0.64, 0.83, 0.86` → **average silhouette 0.72**, a strong signal the clustering is sound.

#### 3. Hierarchical clustering (graph-based)

- **Agglomerative** (bottom-up): every point starts as its own cluster; repeatedly **merge the two nearest clusters** until one cluster remains. **Divisive** (top-down) is the reverse - starts as one cluster, splits.
- Produces a **dendrogram** - a tree where the merge height = the distance at which two clusters combined. You don't have to pick k in advance; you **cut the tree** at whatever height gives the granularity you want.
- **Linkage methods** (how "distance between clusters" is defined) - this table is the exam-shaped part:

| Linkage | Rule | Effect |
|---|---|---|
| **Single** | minimum distance between any two points across clusters | can chain together, good at flagging outliers |
| **Complete** | maximum distance between any two points across clusters | tighter, more compact clusters |
| **Average** | mean distance across all cross-cluster pairs | balances the two above |
| **Centroid** | distance between the two cluster centroids | simple, but centroids can be non-representative |

- 🔵 **Worked example** (single-linkage, US city distances): BOS+NY merge first (206mi, nearest pair) → BOS/NY + DC (223mi) → SF+LA (379mi) → CHI joins the east-coast cluster (671mi) → SEA joins the west-coast cluster (808mi) → DEN joins the east-coast cluster (996mi) → the two remaining super-clusters merge last (1059mi). **The merge order *is* the result** - you read the story of the clustering off the sequence, not just the final groups.

#### 4. DBSCAN (density-based)

- Groups points by **density** rather than distance-to-centroid: for each point, draw an ε-radius shape and count neighbours; if ≥ **minPoints** fall inside, it's a cluster core, and the cluster **expands** outward from there.
- 🔴 **Two properties k-means cannot match:** DBSCAN finds **arbitrarily shaped** clusters (not just round/convex ones), and it **does not force every point into a cluster** - points outside any dense region are left unclustered, i.e. **flagged as outliers automatically**. K-means has no concept of "doesn't belong anywhere" - it forces every point into its nearest centroid, however bad the fit.

#### Key Takeaways for BDA601
1. **This is the resource that supplies Activity 1's real answer bank.** The activity asks you to describe, step by step, how you'd choose k - the elbow/SSE method and the silhouette method (with the worked numeric example) are directly citable, not just conceptual.
2. **The k=n degenerate case is this module's version of Module 8's R²=1.0 trap.** Any time a metric can be driven to a "perfect" value by adding complexity without limit, that metric alone cannot be your stopping rule - you need judgement (the elbow) or a second metric (silhouette) that penalises over-fragmentation.
3. **Day-job anchor:** DBSCAN's built-in outlier detection is the more useful mental model for warehouse anomaly work (e.g. transaction records that don't fit any customer segment) than k-means, which will happily and wrongly assign an anomaly to whichever segment happens to be nearest.
4. Cross-links: k-means here is the same algorithm Sharma (R3) covers in far more implementation depth, and Sullivan (R4) runs in PySpark - the three resources triangulate on one algorithm from theory → depth → code.

---

### 3. The Most Comprehensive Guide to K-Means Clustering (Sharma 2019)

**Citation:** Sharma, P. (2019, 19 August). *The most comprehensive guide to K-Means clustering you'll ever need* [Web log post]. Analytics Vidhya. Retrieved from https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/
**Local source:** `r3_The-Most-Comprehensive-Guide-to-K-Means-Clustering_Sharma-2019.pdf` *(the site has since re-titled the live page "K-Means Clustering Algorithm" and updated it - same author, same URL, same core content)*

**Purpose:** The deepest single-algorithm treatment in the module - properties, evaluation metrics, initialisation, stopping criteria, known failure modes, and a full from-scratch + scikit-learn implementation.

---

#### 1. K-means, defined by its objective

- K-means is **centroid-based**: minimise the **sum of squared distances** between each point and its assigned centroid.
- **Five-step loop:** (1) **Initialise** - pick k random points as centroids. (2) **Assign** - each point joins its nearest centroid. (3) **Update** - recompute each centroid as the mean of its assigned points. (4) **Repeat** (2)-(3) until convergence. (5) **Output** final centroids + assignments.
- **Two properties that define a "good" cluster** (memorise these - they're the rubric for judging *any* clustering result by eye):
  1. **Within-cluster similarity:** points in the same cluster should be close to each other.
  2. **Between-cluster dissimilarity:** points in different clusters should be far apart.
- 🔵 **Worked business example:** a bank wants to offer credit-card deals to millions of customers. Instead of one strategy per customer (unworkable at scale), segment into k income-based groups and design **k strategies**. This *is* the point of clustering - it converts an intractable per-record decision into a tractable per-segment one.

#### 2. Evaluation metrics - a family, like Module 7's confusion-matrix metrics

| Metric | What it measures | Direction |
|---|---|---|
| **Inertia** | sum of **squared** intracluster distances (point → its centroid) | **lower is better** (tight clusters) |
| **Dunn Index** | min(inter-cluster distance) / max(intracluster distance) | **higher is better** (far-apart AND tight) |
| **Silhouette score** | per-point fit to own cluster vs. nearest other cluster, in [-1, 1] | **closer to +1 is better**; ~0 = overlapping; negative = wrong cluster |

- 🔴 **Inertia alone is not enough** - it only rewards property 1 (tightness) and says nothing about property 2 (separation). The Dunn Index fixes this by explicitly trading off both properties in one ratio. This is the same shape of lesson as Module 7's "accuracy alone lies" - **one metric optimises one property; you need a metric (or a pair) that captures what you actually care about.**

#### 3. Choosing k - the elbow method, mechanically

- Run k-means for a **range of k values** (e.g. 1-19), record inertia each time, plot **k vs inertia**.
- Inertia **always decreases** as k grows (more clusters can only reduce or match distance-to-centroid) - the question is *where the rate of decrease flattens*. That bend is the "elbow" - the point where adding another cluster stops buying you much.
- 🔵 **Worked numeric example** (wholesale customer data): k=2 → inertia ≈ 2600. Sweeping k=1→19, the elbow curve drops sharply from k=2→4, then flattens gradually - Sharma reads the elbow as **"anywhere between 6 and 10"** is defensible, with the final call also weighing **computational cost** (higher k = more compute).
- 🔴 **There is no single correct k** - the elbow gives a *range*, not a point. This directly answers the "how do I decide" tension the resource itself poses, and it is exactly the same "no universal threshold" lesson from Module 8's R²/MAE discussion (Dr. Chen, Week 8 lecture) - **evaluation metrics here compare options, they don't hand you a verdict.**

#### 4. Initialisation matters: K-Means++

- **Problem:** vanilla k-means picks k **random** starting centroids - bad luck can converge to a poor local optimum, and results **vary run to run**.
- **K-Means++ fix:** pick the first centroid randomly, then pick each subsequent centroid **preferentially far from the ones already chosen** (probability ∝ squared distance to nearest existing centroid) - spreads the starting points out on purpose. Costs more upfront compute but converges faster and more reliably to a good solution. `sklearn.cluster.KMeans(init='k-means++')` is the default in practice.
- **Stopping criteria (any one triggers a stop):** (1) centroids stop moving between iterations, (2) point-to-cluster assignments stop changing, (3) a max-iteration cap is hit.

#### 5. Known failure modes and fixes

| Challenge | Why it happens | Fix |
|---|---|---|
| **Uneven cluster sizes** | k-means assumes roughly similar-sized, similar-density clusters | try a **higher k**, or a density method (DBSCAN) instead |
| **Uneven density** | tightly-packed points dominate the mean, sparse points get reassigned away | same as above; consider density-based alternatives |
| **Sensitivity to outliers** | squared-distance objective is pulled hard by extreme values | detect/remove/transform outliers *before* clustering, or use a robust variant |
| **Feature scale mismatch** | distance-based algorithm - when feature magnitudes aren't meaningfully comparable, the larger-range feature dominates the distance calculation | **`StandardScaler`** before fitting when magnitudes differ (worked in the Python example: raw `Channel`/`Region` columns have tiny magnitude vs `Fresh`/`Milk`/`Grocery` - unscaled, k-means would effectively ignore the small-magnitude columns) |

#### Key Takeaways for BDA601
1. **This is the deepest resource on the algorithm the module's own activities use** - Activity 2 literally runs a scikit-learn K-means example and asks you to compare 8-cluster vs 3-cluster output; the two defining properties (within-cluster similarity, between-cluster dissimilarity) are your vocabulary for describing *why* one number of clusters looks better than another in the graphs.
2. **Scale your features whenever their magnitudes aren't already comparable** - unlike a decision tree (Module 6), which is scale-invariant, k-means is **distance-based** and will silently let large-magnitude columns dominate. `StandardScaler` is the default move here, the same caution as `LSTAT`/`RM`/`PTRATIO` in Module 8, but applied automatically rather than as a modelling choice. If the underlying geometry itself is the problem (elliptical or unequal-variance clusters), scaling alone won't fix it - that's when you reach for `GaussianMixture` or `DBSCAN` instead (see the bonus section below).
3. **Day-job anchor:** the bank credit-card example maps directly onto customer segmentation you could run on warehouse transaction/usage data - k found via the elbow method, `StandardScaler`'d features, sanity-checked with silhouette before trusting the segments enough to act on them (echoing McCormick's "we're not done until we deploy" from Module 8 - a cluster nobody acts on is just a scatter plot).
4. Cross-links: inertia/Dunn/silhouette here are Module 7's "no single metric tells the whole story" lesson, restated for unsupervised learning; the elbow method's "no universal answer, just a defensible range" echoes Dr. Chen's R²/AUC threshold guidance from Module 8's Week 8 lecture.

---

### 4. Spark for Machine Learning and AI: K-means Clustering (Sullivan 2017)

**Citation:** Sullivan, D. (2017). *Spark for machine learning and AI: K-means clustering* [Video file]. LinkedIn Learning. Retrieved from https://www.linkedin.com/learning/spark-for-machine-learning-ai/k-means-clustering
**Local source:** `r4_Spark-for-ML-and-AI-K-means-Clustering_Sullivan-2017.md` (transcript)

**Purpose:** The PySpark implementation walkthrough - same k-means algorithm as R2/R3, now in the exact toolchain the module's own activities are built around, on a synthetic dataset engineered to make the "does k-means actually find the clusters" answer checkable by eye.

---

#### 1. The workflow, PySpark-native

```text
CSV (header, inferSchema)  →  VectorAssembler(inputCols=[col1,col2,col3], outputCol='features')
                            →  df with a new 'features' vector column
                            →  KMeans(k=3, seed=1)
                            →  kmodel = KMeans.fit(vcluster_df)
                            →  kmodel.clusterCenters()
```

- Same **VectorAssembler → algorithm.fit()** pattern used for every PySpark ML model this subject has covered (Modules 6-8) - **k-means is not a new toolchain, it's a new algorithm dropped into the same pipeline shape.**
- `KMeans(k=3, seed=1)` - **`k` is set explicitly**, not discovered by the algorithm (k-means never tells you the "right" k on its own - that's the whole reason R2's elbow/silhouette and R3's elbow-with-cost-tradeoff exist as separate steps *before* this one).
- `seed` fixes the random initial centroids for **reproducibility** - the same reproducibility point Module 8's `random_state` and Module 6's PySpark `random_state` practicals already made. One more instance of the pattern: **anything with a random starting point needs a fixed seed if you want to compare runs.**

#### 2. Sanity-checking the result against ground truth

- **Synthetic 3-column dataset engineered in three visible bands:** rows 1-25 have values in **1-10**, rows 26-50 in **15-60**, rows 51-75 in **60-100** - a dataset built so a human can eyeball the "correct" 3-cluster answer before running anything.
- `clusterCenters()` returns exactly what the synthetic data promises: centroids near **(5, 5, 5)**, **(35, 31, 34)**, and **(80, 80, 80)** - one centroid per band, at roughly the band's midpoint.
- 🔵 **Why this matters pedagogically:** it's the only resource in the module where you can **verify** k-means worked, rather than just trust the metric. Real data (Activity 2's iris example) won't hand you this luxury - which is exactly why R2's silhouette and R3's Dunn Index/elbow method exist: they're the substitute for "eyeballing the bands" when you can't.
- A harmless **BLAS warning** appears on `.fit()` (`"BLAS library... wasn't able to load"`) - purely a missing-optional-speedup notice, **no effect on results**. Cosmetic, not a bug - don't chase it.

#### Key Takeaways for BDA601
1. **This is Activity 2's toolchain in miniature** - if you run the scikit-learn iris example for Activity 2 (a different library, same algorithm), the vector-assembly → fit → inspect-centres shape is identical to what Sullivan demonstrates in PySpark here.
2. **The engineered 3-band dataset is a good mental benchmark**, even outside this activity: before trusting k-means on real (unlabelled) data, it's worth first running it on a toy dataset with **known** structure to confirm your pipeline (scaling, `k`, seed) is behaving sensibly - the same "know your baseline before you trust the real thing" instinct as Module 8's train/test split discipline.
3. **Day-job anchor:** `seed=1` here is the same reproducibility discipline your day job's DB queries need when someone asks "why did I get a different answer running this twice" - random initialisation without a fixed seed is a silent source of "it worked yesterday" bugs.
4. Cross-links: `VectorAssembler` is the exact function used for every other PySpark model this subject has built (Modules 6, 8) - k-means slots into a pipeline you already know.

---

### Bonus (local, not in the official resource list): Demonstration of k-means assumptions

**Citation:** scikit-learn developers. (n.d.). *Demonstration of k-means assumptions* [Documentation]. scikit-learn 1.9.0. Retrieved from https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_assumptions.html
**Local source:** `bonus_Demonstration-of-K-means-Assumptions_scikit-learn-docs.pdf`

**Purpose:** Not one of the four listed Module 9 resources, but it's already in the module folder and it directly primes **both** learning activities - it's the "here's exactly when k-means lies to you" companion piece to R2/R3's theory.

---

#### 1. Four ways k-means produces "unintuitive and possibly undesirable clusters"

| Failure mode | Root cause | scikit-learn's fix |
|---|---|---|
| **Non-optimal k** | there's no single "true" k in real data | pick k via silhouette analysis / domain knowledge (R2, R3's elbow method) |
| **Anisotropic (elliptical) blobs** | k-means minimises **Euclidean** distance to centroid, so it implicitly assumes **spherical (isotropic)** clusters | switch to `GaussianMixture`, which allows elliptical clusters |
| **Unequal variance** | k-means is mathematically equivalent to maximum-likelihood estimation for gaussians with the **same** variance - it can't represent a mix of tight and spread-out clusters correctly | `GaussianMixture` again (models per-cluster variance) |
| **Unevenly sized blobs** | not a hard k-means limitation per se, but sparse/high-dimensional data increases the risk of landing in a bad local minimum | increase `n_init` (more random restarts, keep the best-inertia run) |

- 🔴 **Two different problems, don't conflate them.** The first three rows are **geometric assumption violations**: k-means' objective function (minimise squared Euclidean distance to centroid) bakes in the assumption that clusters are round, similarly sized, and similarly dense - when real data isn't, k-means still runs and still returns an answer, just the wrong one, and **no choice of k or `n_init` fixes it** (only a different algorithm, like `GaussianMixture`, does). The fourth row (uneven-sized blobs risking a bad local minimum) is a **separate, unrelated problem**: it's about *initialisation luck*, not geometry - increasing `n_init` (more random restarts, keep the best-inertia run) fixes *that*, but it does nothing for anisotropic or unequal-variance data. **The algorithm never tells you which kind of failure you're looking at** - that judgement is on you.

#### Key Takeaways for BDA601
1. **This is the critical-thinking companion to Activity 2.** When you run the scikit-learn K-means example and compare 8 vs 3 clusters, this doc is your vocabulary for *why* a given cluster count can look "wrong" even when the code runs cleanly - shape/variance/size mismatches, not just "the wrong k".
2. **Ties directly to Activity 1** ("describe how you'd determine k") - a complete answer should mention that **the elbow/silhouette method assumes k-means' own geometric assumptions hold**; if they don't (elliptical, uneven-density data), no choice of k fixes it and you need a different algorithm (GaussianMixture, DBSCAN) instead.
3. This is the unsupervised-learning analogue of Module 6's "know your model's assumptions" theme (e.g. decision trees assuming axis-aligned splits) - **every algorithm has blind spots baked into its objective function**, and reading real data through that lens is what separates running code from actually modelling.

---

## Where this module fits

- **Modules 6-8** were all **supervised**: labelled data → predict `y` (classification or regression). **Module 9 drops the label entirely** - clustering finds structure with no target variable, which is why R3 spends real time establishing "clustering is an unsupervised learning problem" as its own idea, not an assumed one.
- **The throughline across all four resources:** k-means is one algorithm, covered at four depths - definition + alternatives (R2), full implementation + failure modes (R3), the exact PySpark toolchain (R4), and the exact geometric assumptions that break it (bonus). By the time Activity 2 asks you to explain 8-vs-3 clusters, you have theory, code, and a labelled failure-mode checklist to draw on.
- **Feeds Assessment 3** (familiarisation only this week - due Week 12): clustering plus Module 8's predictive modelling and Module 7's evaluation are the toolkit A3 draws from.
