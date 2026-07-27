# BDA601 · Module 9 - One-Pager

> **Clustering · k-means (elbow + silhouette) · hierarchical (dendrograms) · DBSCAN · when k-means lies to you**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Modules 6-8 all had a label to predict. Module 9 drops it: clustering groups similar records with no target `y` at all. K-means is the default tool - pick k centroids, assign, recompute, repeat - but it silently assumes clusters are round, similarly sized, and similarly dense. When real data breaks that assumption, k-means still runs and still answers, just wrong.**
> (Le 2019 · Sharma 2019 · scikit-learn "Demonstration of k-means assumptions")

## 🖤 Zone 1 - Clustering, defined, and the four families (Le)
- 🖤 **Unsupervised:** no target/label - the clean break from Modules 6-8. Points in the same group should be **similar**; points in different groups should be **dissimilar**.
- 🔵 **Four families, by what "similar" means:** connectivity (distance), **centroid** (k-means), **density** (DBSCAN), graph-based (cliques). This module covers k-means, hierarchical, DBSCAN.
- 🖤 **K-means algorithm:** pick k random centroids → assign every point to its nearest centroid (this partition is a **Voronoi diagram**) → recompute each centroid as the **mean** of its points → repeat until convergence.
- 🔴 **Source erratum (Le's worked example):** pairs Manhattan distance with a mean-based update - internally inconsistent. Manhattan + **median** = **k-medians**, a different algorithm. Textbook k-means = Euclidean + mean. Cite the mechanics, not the pairing.

## 🖤 Zone 2 - Choosing k: elbow + silhouette (Sharma) ⭐ SLO d) - THE GRADED CORE
- 🖤 **Two properties of a "good" cluster** (the rubric for judging any result by eye): **within-cluster similarity** (tight) and **between-cluster dissimilarity** (far apart).

| Metric | What it measures | Direction |
|---|---|---|
| **Inertia** | sum of **squared** intracluster distances (point → centroid) | lower is better (tight only) |
| **Dunn Index** | min(inter-cluster) / max(intracluster) | higher is better (tight **and** separated) |
| **Silhouette** | per-point fit to own vs. nearest other cluster, [-1, +1] | closer to +1 is better; ~0 overlapping; negative = wrong cluster |

- 🔴 **Inertia alone lies** - it only rewards tightness, never separation. Same shape as Module 7's "accuracy alone lies."
- 🔵 **Elbow method:** plot k vs inertia; inertia always decreases as k grows, so read *where the drop flattens*. Sharma's wholesale-customer example: sharp drop k=2→4, flattens after - **"anywhere 6-10" is defensible**, no single right answer.
- 🔴 **k=n degenerate case** = Module 8's R²=1.0 trap in a different hat: driving a metric to "perfect" by adding unlimited complexity is not a good model, it's a sign you stopped modelling.
- 🔵 **K-Means++:** random init risks a bad local optimum; K-Means++ spreads initial centroids apart on purpose (`sklearn` default). Stops on: centroids stop moving, assignments stop changing, or max iterations.

## 🖤 Zone 3 - When k-means lies: geometry vs. initialisation (bonus scikit-learn doc) ⭐ feeds Activity 2 directly

| Failure mode | Category | Fix |
|---|---|---|
| Non-optimal k | - | silhouette / domain knowledge |
| **Anisotropic (elliptical) blobs** | geometric assumption violation | `GaussianMixture` |
| **Unequal variance** | geometric assumption violation | `GaussianMixture` |
| **Unevenly sized blobs** | initialisation luck | `n_init` (more random restarts) |

- 🔴 **Two different problems - don't conflate them.** The first two rows are k-means' objective function (minimise squared Euclidean distance) baking in "round, similarly-sized, similarly-dense" - **no `k` or `n_init` fixes this, only a different algorithm does.** The last row is a local-minimum/bad-luck problem - `n_init` fixes *that*, but does nothing for elliptical or unequal-variance data. The algorithm never tells you which failure you're looking at.
- 🔵 **Feature scale:** k-means is distance-based - unscaled large-magnitude columns dominate. `StandardScaler` **whenever magnitudes aren't already comparable** (not an unconditional mandate - if the geometry itself is wrong, scaling won't save you).

## 🖤 Zone 4 - Hierarchical clustering (Le)
- 🖤 **Agglomerative** (bottom-up, the common case): every point starts as its own cluster → repeatedly merge the two nearest clusters → one cluster remains. **Divisive** = the reverse.
- 🔵 **Dendrogram:** merge height = distance at which two clusters combined. No need to pick k upfront - **cut the tree** at whatever height gives the granularity you want.

| Linkage | Rule | Effect |
|---|---|---|
| **Single** | min distance across clusters | can chain, flags outliers |
| **Complete** | max distance across clusters | tighter, more compact |
| **Average** | mean distance across pairs | balances the two above |
| **Centroid** | distance between centroids | simple, can be non-representative |

- 🔵 US-city worked example (single-linkage): merge order **is** the result - BOS+NY first (nearest), ending with the two coastal super-clusters merging last.

## 🖤 Zone 5 - DBSCAN + PySpark toolchain (Le, Sullivan)
- 🔴 **Two properties k-means cannot match:** DBSCAN finds **arbitrarily shaped** clusters (not just round/convex), and it **does not force every point into a cluster** - low-density points are left unclustered, i.e. **auto-flagged as outliers**. K-means has no "doesn't belong anywhere" concept.
- 🔵 Mechanics: ε-radius + minPoints - if ≥ minPoints fall inside a point's radius, it's a cluster core; the cluster expands from there.

```text
CSV (header, inferSchema)  →  VectorAssembler(inputCols=[...], outputCol='features')
                            →  KMeans(k=3, seed=1)
                            →  kmodel = KMeans.fit(df)
                            →  kmodel.clusterCenters()
```

- 🖤 Same **VectorAssembler → .fit()** pattern as every PySpark model in Modules 6-8 - k-means is a new algorithm in the same pipeline shape, not a new toolchain.
- 🔵 Sullivan's engineered 3-band dataset (bands 1-10 / 15-60 / 60-100) returns centroids ≈**(5,5,5)**, **(35,31,34)**, **(80,80,80)** - the one resource where you can *verify* k-means worked instead of just trusting a metric.
- 🔴 `seed=1` fixes random initial centroids - same reproducibility discipline as Module 8's `random_state`: anything with a random start needs a fixed seed to compare runs.

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Model Evaluation**: source code + presentation, **7-10 minutes**, **40%**, due **19/08/2026**, SLOs **c) d) e)**.
> Module 9 is **familiarisation week only** for A3 - no deliverable due yet. But this module's toolkit (clustering) plus Module 7's evaluation metrics and Module 8's predictive modelling are what A3 draws from - start reading the brief this week.

## 🔴 If you only memorise 5 things
1. **No label, no target** - clustering is unsupervised; that's the whole break from Modules 6-8.
2. **Choosing k has no single right answer** - elbow + silhouette give a defensible range, not a verdict (k=n is always "perfect" and always useless).
3. **Two different failure categories:** geometric (elliptical/unequal-variance → switch algorithm to `GaussianMixture`) vs. initialisation luck (uneven-sized blobs → raise `n_init`). Don't conflate them.
4. **DBSCAN's superpower:** arbitrary shapes + automatic outlier detection - k-means forces every point somewhere, however bad the fit.
5. **Scale features when magnitudes differ** (`StandardScaler`) - but scaling doesn't fix a geometry problem, only a magnitude problem.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your warehouse has transaction/usage records with no natural label. Pick one column set you'd cluster on, and say whether you'd expect round, similarly-sized groups (k-means is fine) or messier shapes/outliers (DBSCAN would serve you better).
2. If you ran k-means on warehouse data and got one huge cluster and several tiny ones, which of Zone 3's two categories would you suspect first, and what's the one-line test to tell them apart?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 **Activity 1:** Determine the Value of K (forum post) - use Le's SSE/silhouette worked examples + Sharma's elbow method as the citable answer bank; mention that the geometric assumptions (Zone 3) have to hold for elbow/silhouette to mean anything.
- [ ] 🕐 **Activity 2:** Clustering Tool - run the scikit-learn K-means example, explain the 4 graphs (8 vs 3 clusters) using Zone 3's failure-mode table as vocabulary.
- [ ] 🔥 **Resource 1** (Xu & Wunsch, *Cluster Analysis*) - EBSCO/ProQuest ebook behind Torrens auth, still needs manual access + summary.
- [ ] 🕐 Start familiarising with the **Assessment 3** brief (due 19/08/2026, 40%) - no deliverable yet, just read it this week.
