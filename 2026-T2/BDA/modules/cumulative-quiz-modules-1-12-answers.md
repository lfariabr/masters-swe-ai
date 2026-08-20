# BDA601 Cumulative Quiz - Modules 1-12 - Answer Key

Grade yourself honestly before reading further. Partial credit is fine if the mechanism is right even when the wording differs.

### 1. Module 1 - The Vs and the lifecycle (6 points)

Volume, Variety, Velocity (the core three) - plus Veracity (uncertainty) and Value/Connectedness depending on how the module framed it. Marr's point: data only creates value when it's tied to strategy - better decisions, customer/market understanding, better products/services, improved operations, or monetisation. Without a business question driving it, more data is just more storage cost.

### 2. Module 2 - Data lake anatomy (8 points)

- **3 tiers:** Intake → Management → Consumption.
- **3 zones of the Intake tier:** Source System → Transient Landing → Raw.
- **Schema-on-read** (data lake): the data is stored as-is, raw, and structure is applied only when it's read/queried - this is what lets a lake ingest the ~80% of data that's semi/unstructured without forcing it into a table shape upfront. **Schema-on-write** (warehouse): structure must be defined and enforced before data is stored, which works for the ~20% that's already clean and structured but rejects or mangles everything else.

### 3. Module 3 - Integration pipeline and CAP (9 points)

**Pipeline:** schema alignment → record linkage → data fusion.

**CAP theorem:** in a distributed system you can only guarantee two of Consistency, Availability, and Partition tolerance at once. Partition tolerance is non-negotiable because network partitions *will* happen in any real distributed system - you can't opt out of network failures. So the real trade-off in practice is **Consistency (CP) vs Availability (AP)**: when a partition happens, do you refuse requests until data is consistent (CP), or stay available and risk serving stale/inconsistent data (AP)?

### 4. Module 4 - Spark internals (9 points)

Spark is faster than Hadoop/MapReduce mainly because of **in-memory computation** (avoiding repeated disk I/O between stages) plus **lazy DAG optimisation**, which builds an execution plan and optimises it before running anything.

An **RDD** (Resilient Distributed Dataset) is an immutable, distributed collection of objects, partitioned across a cluster. Fault tolerance comes from **lineage** - Spark tracks the sequence of transformations that built the RDD, so if a partition is lost it can be recomputed from that lineage rather than needing a replicated copy sitting idle.

UDFs are discouraged because they're opaque to Spark's Catalyst optimiser and Tungsten execution engine - the engine can't reason about or optimise a black-box Python/Scala function the way it can with built-in functions, and UDFs often force expensive serialization between the JVM and the UDF's runtime.

### 5. Module 5 - Exploring and cleaning (7 points)

Outlier rule: any value more than **1.5x the IQR** below Q1 or above Q3 is flagged as an outlier.

Ranking, most naive → most sophisticated: **fill with a global constant** → **ignore the tuple** → **mean/median imputation** → **most-probable-value imputation** (uses other attributes/a model to estimate the missing value, so it's the most context-aware).

### 6. Module 6 - Classification algorithms (9 points)

| Algorithm | What it assumes / how it splits | Weak point it's known for |
|---|---|---|
| 1R | Picks the single best attribute and builds rules from it alone | Ignores every other attribute - a baseline, not a real model |
| Naive Bayes | Assumes all attributes are conditionally independent given the class; applies Bayes' rule | The independence assumption is usually false in practice; zero-frequency problem without Laplace smoothing |
| Decision tree (C4.5) | Splits recursively on the attribute with max information gain / gain ratio | Prone to overfitting without pruning; biased toward high-branching attributes unless gain ratio is used |

Gain ratio fixes information gain's bias toward attributes with many distinct values (e.g. an ID column would look "perfect" under plain information gain) by normalising the gain against the intrinsic information of the split itself.

### 7. Module 7 - Reading a confusion matrix (8 points)

97% accuracy with only 3/50 real cancers caught means the classifier is essentially predicting "no cancer" almost every time - on an imbalanced dataset (few actual positives), accuracy is dominated by the easy majority class (TN) and hides near-total failure on the class that actually matters (FN is huge). The two metrics to report instead: **sensitivity/recall** (of actual cancers, how many did we catch - here it's 3/50 = 6%, terrible) and **precision** (of predicted cancers, how many were real). ROC/AUC adds a **threshold-independent** view - it shows performance across every possible decision threshold at once, rather than locking in one arbitrary cutoff the way a single accuracy/precision/recall number does.

### 8. Module 8 - Regression to classification (8 points)

"Polynomial regression IS linear regression" because the model is still linear **in its coefficients** - you're not changing the algorithm, you're expanding the *feature set* by adding powers of the original feature (x, x2, x3...) and then fitting an ordinary linear regression on top of those new features. The regression equation is still a weighted sum of terms.

R2 climbing to a perfect 1.0 on training data (degree 4) is a warning because it means the model has started fitting noise specific to that training set rather than the underlying signal - classic overfitting. A perfect training fit almost always means poor generalisation to new data, the same trap as pushing K-means to k=n in Module 9.

### 9. Module 9 - K-means mechanics (9 points)

1. Pick k initial (often random) centroids.
2. Assign every point to its nearest centroid.
3. Recompute each centroid as the mean of the points assigned to it.
4. Repeat steps 2-3 until assignments stop changing (convergence).

Tools to choose k: the **elbow method** (plot k vs inertia, pick where the curve's improvement flattens) and the **silhouette score** (per-point measure of how well it fits its own cluster vs the nearest other one, -1 to +1). Pushing k toward n isn't valid because inertia trivially keeps dropping as clusters get smaller - at k=n every point is its own cluster with zero inertia, which is a meaningless, overfit "solution" that groups nothing.

### 10. Module 10 - Support, confidence, lift (8 points)

- **Support:** how often X and Y appear together, as a fraction of all transactions.
- **Confidence:** of the transactions containing X, what fraction also contain Y.
- **Lift:** whether Y is more likely given X than Y's own baseline (overall) rate - lift > 1 means a real association, lift ≈ 1 means X tells you nothing extra about Y.

Example: say 90% of all shoppers buy milk regardless of what else is in the basket. A rule "{bread} => {milk}" might show high confidence (90%) simply because almost everyone buys milk anyway - not because bread and milk are actually associated. Lift for that rule would be close to 1 (confidence / baseline rate of milk = 90%/90% = 1), revealing the rule is not actually informative despite the high confidence.

### 11. Module 11 - Link prediction as supervised ML (9 points)

Take a single graph snapshot. **Positive examples**: randomly drop some real edges (but only where doing so doesn't disconnect the graph) and label those dropped node-pairs `link = 1`. **Negative examples**: take unconnected node-pairs from the adjacency matrix and label them `link = 0`. Then extract features for each pair (e.g. via node2vec embeddings, summed per pair) and train an ordinary classifier.

The class-imbalance issue: the number of possible unconnected pairs (negatives) vastly outnumbers the number of real edges you can safely drop as positives - in the module's Facebook example, ~19,000 negative pairs vs ~1,500 positive pairs. This is a **structural** property of sparse real-world graphs, not a data-quality bug, so it needs handling via `class_weight="balanced"` or equivalent, not "fixing" the dataset.

### 12. Module 12 - Data at rest vs data in motion (6 points)

- **At rest** control example: file/disk encryption (or access control lists on stored data).
- **In motion** control example: transport-layer security / TLS (protecting data as it moves over a network).

Ohlhorst's four-way trade-off: **access** (control vs eliminate), **availability** (control vs distribution), **performance** (security overhead vs speed), **liability** (keeping data = keeping risk). Tightening one loosens another - there's no single "solved" configuration.

### 13. Synthesis - the pipeline end to end (8 points)

- **Source/store:** Module 2's data lake (intake tier) sources the transaction and customer data; Module 3's integration + storage (schema alignment/record linkage/fusion into a data hub) unifies it into one queryable view.
- **Explore/clean:** Module 5's exploration and cleaning (missing values, outliers, dimensionality reduction) prepares it for modelling.
- **Answering "which products go together" vs "which customer segments drive it":** Module 10's **association rules** answer the first question directly - support/confidence/lift on item-level co-occurrence within transactions ("if X then Y"). Module 9's **clustering** (K-means) answers the second - grouping customers into segments based on overall similarity in purchasing behaviour, not item-pair co-occurrence. The key difference: association rules are narrow and item-focused (a specific if-then pattern, often low support), while clustering is broad and customer-focused (a whole-record grouping) - "two sides of the same coin" looking at the same data through different lenses.
