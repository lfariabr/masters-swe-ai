# BDA601 Cumulative Quiz - Modules 1-12

**Time box:** 50 minutes

**Mode:** Closed book, written answers, then check the separate answer key

Do not open `cumulative-quiz-modules-1-12-answers.md` until every question has an answer. This is the full-course quiz - one question sampled from each of Modules 1-11, a lighter check on Module 12 (already covered in detail via the module notes and one-pager), and a synthesis question tying the pipeline together at the end.

## Questions

### 1. Module 1 - The Vs and the lifecycle (6 points)

Name the Vs of big data covered in Module 1. Then, using Marr's framing, explain why "more data" on its own isn't the point - what has to be true before data creates value?

### 2. Module 2 - Data lake anatomy (8 points)

A data lake has 3 tiers and the Intake tier has 3 zones. Name all 6. Then explain the difference between **schema-on-read** (data lake) and **schema-on-write** (data warehouse), and why that difference matters for ~80% of the data a big organisation collects.

### 3. Module 3 - Integration pipeline and CAP (9 points)

Name the three-step integration pipeline (Dong & Srivastava) in order. Then state Brewer's CAP theorem, explain why partition tolerance is non-negotiable in a distributed system, and say what the *real* trade-off becomes once you accept that.

### 4. Module 4 - Spark internals (9 points)

What makes Spark up to 100x faster than Hadoop/MapReduce? Then explain what an RDD is, how it achieves fault tolerance without replicating data, and why hand-written UDFs are discouraged in favour of Spark's built-in functions.

### 5. Module 5 - Exploring and cleaning (7 points)

State the >1.5x IQR outlier rule. Then rank these four missing-value strategies from most naive to most sophisticated: mean/median imputation, ignore the tuple, most-probable-value imputation, fill with a global constant.

### 6. Module 6 - Classification algorithms (9 points)

Complete this table from memory:

| Algorithm | What it assumes / how it splits | Weak point it's known for |
|---|---|---|
| 1R | | |
| Naive Bayes | | |
| Decision tree (C4.5) | | |

Then explain what "gain ratio" fixes that plain information gain doesn't.

### 7. Module 7 - Reading a confusion matrix (8 points)

A cancer-screening classifier scores 97% accuracy but only catches 3 of 50 actual cancer cases. Using the confusion matrix (TP/TN/FP/FN), explain why accuracy is the wrong headline metric here, name the two metrics you'd report instead, and say what ROC/AUC adds that a single accuracy number can't.

### 8. Module 8 - Regression to classification (8 points)

Explain, in your own words, why "polynomial regression IS linear regression" - what's actually changing between the two. Then explain why a model going from R2 = 0.95 (degree 2) to R2 = 1.0 (degree 4) on training data is a warning sign, not a win.

### 9. Module 9 - K-means mechanics (9 points)

Write out the K-means algorithm's four steps from "pick k centroids" to convergence. Then name the two tools used to choose k, and explain why increasing k until every point is its own cluster is not a valid answer even though it minimises inertia.

### 10. Module 10 - Support, confidence, lift (8 points)

Define support, confidence and lift in one sentence each. Then explain, with a concrete made-up example, a case where confidence is high but lift reveals the rule is actually useless.

### 11. Module 11 - Link prediction as supervised ML (9 points)

Explain how link prediction gets turned into an ordinary binary classification problem: where do the positive examples come from, where do the negative examples come from, and what's the resulting class-imbalance issue?

### 12. Module 12 - Data at rest vs data in motion (6 points)

Give one example of a control appropriate for data at rest and one appropriate for data in motion. Then name the four-way trade-off Ohlhorst frames Big Data security as balancing.

### 13. Synthesis - the pipeline end to end (8 points)

A retailer wants to know "which products tend to be bought together, and which customer segments drive that pattern?" Walk this scenario through the pipeline in order: which module's technique sources/stores the data, which module's technique explores/cleans it, and which two modules' techniques (from 9-11) could answer the actual business question - and what's the key difference in what each of those two techniques would tell you?

## Score Guide

- **90-100:** The whole pipeline - source, store, process, clean, model, evaluate - still holds together as one system, not twelve disconnected modules.
- **75-89:** Core mechanics are solid; a couple of modules need a re-read.
- **60-74:** Gaps are showing across multiple modules - schedule a `/module-compression` pass on the weak ones.
- **Below 60:** Re-read the one-pagers for the modules you missed, then retake closed book.
