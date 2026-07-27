# Module 9 - Class Notes (Week 9 live session)

Extracted from `MLN601 - Machine Learning - Lecturer Week 1 - Week 12` (Teams recording, week 9 segment, ~2h34m).
Facilitator: Dr Kamran Shaukat.

> **Shape of the session:** ~10 min assessment admin (A1 marking held back to be fair to extensions;
> A2 just submitted; A3 previewed) → a **recap of the whole course** (ML → supervised/unsupervised) →
> **similarity/distance metrics** (the part missing from the readings) → **cluster analysis theory** →
> **K-means worked by hand** → **limitations → DBSCAN / OPTICS / K-medoids** → activities.
>
> ⚠️ **The live lecture is substantially broader than the 4 module readings.** The readings are K-means-only;
> the lecturer built the *whole clustering family* around it. Everything in sections 2 and 6 below is
> lecture-only material not covered by resources 1-4.

---

## 1. Course recap (his framing, almost verbatim)

- **Machine learning** = "a branch of AI which performs certain action without explicitly being programmed", learning patterns from data.
- **Algorithm vs model:** an algorithm is step-by-step instructions; run it on data and it *learns patterns* → the output is a **model**. ("Model is the output of an algorithm executed on data.")
- **Measurement vs model** (a student asked): a *measurement* is a quantity used inside the algorithm (entropy, information gain, a distance, Bayes' theorem); the *model/algorithm* is the technique that consumes those measurements. e.g. Naive Bayes = model, Bayes theorem = measurement; K-means = model, the distance = measurement.
- **Supervised** (label known) → **classification** (categorical label: binary / multi-class) or **regression** (continuous label). **Unsupervised** (no idea what you're predicting) → **clustering**: explore, then let the data separate into groups by *similarity*.
- **His clustering intuition:** grouping students by gender / continent / domestic-vs-international; supermarket aisles (dairy together, produce together) - "you need to calculate the similarity of one item to another."

---

## 2. Similarity & distance metrics ⭐ (lecture-only - NOT in the readings)

This is the biggest gap between the readings and the lecture. He spent ~40 min here because "changing the similarity metric can make a huge difference to the performance of your algorithm."

- **Similarity** = numerical measure of how alike two objects are, **higher = more alike**, usually in [0,1]. **Dissimilarity** = the reverse, **min 0 = identical**. **Proximity** = umbrella term for either (so if asked to "calculate proximity" you must ask which).

### Numeric attributes
| Metric | Formula (idea) | Note |
|---|---|---|
| **Euclidean distance** | `√( Σ (aᵢ − bᵢ)² )` | the default. **Why square then root:** squaring kills the sign (so +3 and −3 don't cancel to a fake "similar"), the root re-normalises back to the real scale. Symmetric: `d(P1,P3) = d(P3,P1)`, so you only fill the upper triangle of a distance matrix; diagonal = 0. |
| **Minkowski distance** | `( Σ |aᵢ − bᵢ|^r )^(1/r)` | **the generalised form** - `r` picks the metric below |
| → `r = 1` | **Manhattan** | no square, no root - just absolute differences summed |
| → `r = 2` | **Euclidean** | the squared/rooted one |
| → `r = ∞` | **Supremum / Chebyshev** ("supremom" in the transcript) | take the **maximum** single-attribute difference |

He worked all three by hand on a 4-point example (P1-P4, two attributes). Worth re-deriving one from the `.srt` if it doesn't click.

### Binary attributes (vectors of 0/1)
- **Simple Matching Coefficient (SMC)** = (matches) / (total), counts **0-0 matches as similarity**.
- **Jaccard coefficient** = ignores 0-0 matches (only 1-1 over 1-1 + mismatches).
- ⭐ **His key point:** SMC and Jaccard can disagree hard. If "0 = attribute absent", does *both absent* count as similar? Two international students who **both** lack PR *are* alike on that feature (SMC says similar; Jaccard says nothing). Choose the metric to match what "absence" means in your domain.

### Documents
- **Cosine similarity** - for term-frequency vectors. SMC/Jaccard only see present/absent (1/1), but a word appearing **10× vs 1×** should not read as identical. Cosine uses the **actual counts**: `cos = (D1·D2) / (‖D1‖‖D2‖)`. His example landed at ~0.3 (≈30% similar).

---

## 3. Cluster analysis - the two quantities

- **Goal:** objects in the **same** cluster highly similar; objects in **different** clusters highly dissimilar.
- **Intra-cluster similarity** = distances *within* one cluster. **Inter-cluster similarity** = distances *between* clusters. Mnemonic he gave: **"interstate = between two states"** → inter = between clusters.
- **Aim:** **maximise intra-cluster similarity** (points in a cluster tight/cohesive) and **minimise inter-cluster similarity** (clusters far apart, so points can't leak into the wrong one). *(He mis-spoke the direction once mid-lecture but stated it correctly in the wrap-up - this is the correct version.)*
- **Applications he named:** document grouping, gene/bioinformatics (cancer cells), data reduction, customer segmentation, image segmentation, anomaly detection, recommender systems (YouTube playlists, movie genres), social networks, market-basket, supermarket/store layout, hospital wards.
- **Crowd-sourced examples (your class):** Luis → **student engagement segmentation**; Ferdi → insurance at-risk policyholders; Suleiman → students by learning style / academic performance for personalised support; another → Uber **Pool** ride-sharing (cluster nearby pickup/drop-off) and Uber Eats order batching; client/customer segmentation by turnover replacing a manual team-leader-with-Excel process.

---

## 4. Types of clustering

| Axis | Type A | Type B |
|---|---|---|
| **Structure** | **Partitional** - flat split into k groups | **Hierarchical** - nested tree (suburb → city → state → country) |
| **Membership** | **Exclusive** - a point belongs to exactly one cluster (partitional) | **Non-exclusive** - a point can belong to several (hierarchical) |
| **Coverage** | **Complete** - every point assigned | **Partial** - only cluster a subset of interest |

K-means is **partitional, exclusive, complete**.

---

## 5. K-means, worked by hand ⭐

- **k = how many clusters you want.** You must set it up front.
- **Loop:** place k centroids randomly → for every point compute distance to each centroid → assign to nearest → **recompute each centroid as the mean of its assigned points** → repeat until **no point changes cluster** (the halting/stopping criterion).
- **Objective function = SSE (sum of squared errors)** - the squared distance of points to their centroid. (This is the same quantity the readings call **inertia / WCSS**.)
- **His worked example:** 7 instances, 2 attributes (x,y), k=2, initial centroids = instance 1 (1,1) and instance 4 (5,7). Euclidean distances → assign → recompute centroids as column means of each group → re-assign. A point that was equidistant in round 1 got resolved in round 2 once centroids moved. He showed a 6-iteration figure where iterations 5 and 6 were identical → stop.
- **Ties:** if a point is equidistant to two centroids, assign to either - the next iteration resolves it.

---

## 6. Limitations → DBSCAN / OPTICS / K-medoids ⭐ (lecture-only)

He was explicit: *"this is not part of your ML course, but you should know these exist."* Great context for A3 and for the "why did K-means fail?" comparison questions.

**Where K-means struggles:**
1. **Different cluster sizes / densities** - a sparse-but-real cluster gets torn apart or absorbed.
2. **Non-globular / non-convex shapes** - his **S-shape** example: K-means slices it into two spherical blobs when the true structure is one curved cluster. K-means clusters are always roughly **spherical**.
3. **Outliers** - because centroids are **means** (his vice-chancellor-salary analogy: one 700K salary drags the "average employee" estimate).

**The alternatives:**
| Algorithm | Fixes | How |
|---|---|---|
| **K-medoids / K-median** | outlier sensitivity | use the **median / an actual data point** as the centre instead of the mean |
| **DBSCAN** | non-globular shapes, noise, **and you don't specify k** | density-based: parameters **eps** (radius) + **minPts**. A point with ≥ minPts neighbours in its eps-radius = **core point**; on the edge = **border point**; otherwise = **noise/outlier**. Forms arbitrary shapes. |
| **OPTICS** | DBSCAN's weakness with **varying density** | like DBSCAN but can **adjust the reachability distance** along the way, so clusters of different densities are handled. |

**K-means vs DBSCAN (his summary table):**
- K-means: **must** specify k · always returns clusters (even from scattered data) · **spherical** shape · struggles with noise/outliers.
- DBSCAN: **k not required** · **arbitrary shapes** · handles noise/outliers · **but** on very scattered data may label *everything* as noise → no clusters at all.

---

## 7. Assessment notes (from the admin bookends)

- **A1** marking is being **held back deliberately** until the extension students submit, so results + feedback publish together (expected before the following week's lecture).
- **A2** - he confirmed a couple of just-late / wrong-extension submissions as **on time / no penalty**.
- **A3 is a REGRESSION task**, "similar to Assessment 1" - reuse your A1 model zoo, just swap the dataset; keep GridSearchCV + explainable AI. **Not a clustering assessment.** Detailed spec to come in the next 1-2 lectures.
- Course is near its end; the two module-9 activities (365 Data Science pros/cons video + the K-means implementation notebook) were offered as optional in-class work.

---

## What this changes in the module notes

1. **Distance metrics were entirely absent** from resources 1-4 but are ~40 min of the lecture and the *foundation* of clustering. Add Euclidean/Minkowski (Manhattan/Euclidean/Chebyshev), SMC vs Jaccard (the "0-0 counts?" point), and cosine → promote into notes + one-pager.
2. **SSE = inertia = WCSS** - add SSE as the lecturer's name for the objective (a 4th synonym alongside the readings' three).
3. **DBSCAN / OPTICS / K-medoids** are lecture-only but he leaned on them hard as the answer to "why K-means failed". This is exactly the module09_notes.md "algorithm comparison" material made concrete - cross-link it.
4. **intra vs inter-cluster + the interstate mnemonic** - clean framing worth capturing.
5. **A3 is regression, not clustering** - important expectation-setting; note it so we don't over-invest clustering into A3.
