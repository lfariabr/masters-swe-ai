# Module 7 - Model Evaluation

## TL;DR

A classifier's accuracy on its own training data is optimistically biased, so Module 7 is about estimating **future** performance honestly and picking the better model.
- **Metrics:** build everything from the **confusion matrix** (TP/TN/FP/FN) - accuracy, **sensitivity/recall**, specificity, **precision**, **F1/Fβ**. Raw accuracy **lies on imbalanced data** (97% accurate yet catches 0 cancers), so split into sensitivity/specificity or precision/recall.
- **Reliable estimates:** keep **train / validation / test** separate (test used once); on limited data the default is **stratified 10-fold cross-validation**, with leave-one-out and the **0.632 bootstrap** as alternatives.
- **Cost-aware selection:** errors are not equally costly, so compare probabilistic classifiers with **ROC curves** (TPR vs FPR) and **AUC** (1.0 perfect, 0.5 random) - threshold-independent.
- **Toolkit:** F1, lift/gain, KS, AUC-ROC, log loss, Gini for classification; RMSE/RMSLE, R²/adjusted-R² for regression. Core message: **different problems need different metrics**.

Feeds **SLO d)** and **Assessment 2** (train, evaluate, compare) plus the two forum activities below.

---

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Han, Pei & Kamber (2011) - Metrics for Evaluating Classifier Performance (§8.5.1) | ✅ |
| **2** | Read & summarise Witten et al. (2017) - Credibility: training/testing, cross-validation, other estimates (§5.1, §5.3-5.5) | ✅ |
| **3** | Read & summarise Han, Pei & Kamber (2011) - Comparing Classifiers on Cost-Benefit & ROC Curves (§8.5.6) | ✅ |
| **4** | Read & summarise Srivastava (2019) - Twelve important model evaluation metrics | ✅ |
| 5 | Activity 1: Build & compare two decision-tree models in PySpark (Larose adult dataset) + forum post | 🕐 |
| 6 | Activity 2: "Please explain" - why different problems need different metrics + forum post | 🕐 |

**Local sources (this folder):**
- `r1_Metrics-for-Evaluating-Classifier-Performance-8.5.1_Han-2011.pdf` (Resource 1)
- `r2_Credibility-Training-Testing-Cross-Validation-5.1-5.5_Witten-2017.pdf` (Resource 2)
- `r3_Comparing-Classifiers-Cost-Benefit-and-ROC-8.5.6_Han-2011.pdf` (Resource 3)
- `r4_Twelve-Important-Model-Evaluation-Metrics_Srivastava-2019.pdf` (Resource 4)
- `a1_DSPR_Data_Sets.zip` (Activity 1 datasets - Larose adult_ch6 train/test)

---

## Key Highlights

### 1. Metrics for Evaluating Classifier Performance (Han, Pei & Kamber 2011)

**Citation:** Han, J., Pei, J. & Kamber, M. (2011). *Data mining: Concepts and techniques* (3rd ed., §8.5.1 "Metrics for Evaluating Classifier Performance", pp. 364-370). Waltham, MA: Elsevier / Morgan Kaufmann.
**Local source:** `r1_Metrics-for-Evaluating-Classifier-Performance-8.5.1_Han-2011.pdf`

**Purpose:** Establishes the vocabulary (confusion matrix, TP/TN/FP/FN) and the full family of accuracy metrics - and shows *why raw accuracy lies* on imbalanced data, which is the whole reason this module exists.

---

#### 1. The confusion matrix is the foundation

- **Four building blocks.** Every metric is built from counts on a held-out **test set** (never the training set):
  - **TP** - positive tuples correctly labelled positive
  - **TN** - negative tuples correctly labelled negative
  - **FP** - negative tuples wrongly labelled positive (false alarm)
  - **FN** - positive tuples wrongly labelled negative (miss)
- **Confusion matrix** = an *m x m* table (rows = actual class, columns = predicted). A good classifier puts almost everything on the **diagonal**; off-diagonal cells show exactly *which* classes are being confused.
- **P = TP + FN** (all real positives), **N = FP + TN** (all real negatives).
- **Resubstitution error** = error measured on the *training* set. It is **optimistically biased** because the model has already seen those rows - always evaluate on a test set.

#### 2. The metric family (memorise the formulas)

| Metric | Formula | What it answers |
|---|---|---|
| **Accuracy** (recognition rate) | (TP + TN) / (P + N) | Overall % correct |
| **Error rate** | (FP + FN) / (P + N) = 1 - accuracy | Overall % wrong |
| **Sensitivity / Recall** (TP rate) | TP / P | Of real positives, how many caught? (*completeness*) |
| **Specificity** (TN rate) | TN / N | Of real negatives, how many caught? |
| **Precision** | TP / (TP + FP) | Of predicted positives, how many right? (*exactness*) |
| **F1** (harmonic mean) | 2·precision·recall / (precision + recall) | Balances precision & recall equally |
| **Fβ** | (1+β²)·precision·recall / (β²·precision + recall) | Weights recall β times as much as precision (the β² term implements that balance; F2 favours recall, F0.5 favours precision) |

- **accuracy = sensitivity·(P/(P+N)) + specificity·(N/(P+N))** - accuracy is just a class-weighted blend of the two rates.

#### 3. Why accuracy fails on imbalanced data

- **The cancer trap.** If only 3% of tuples are "cancer = yes", a model that predicts "no" for *everyone* scores **97% accuracy** while catching **zero** cancers. Accuracy is only trustworthy when classes are **roughly balanced**.
- **The fix:** report **sensitivity** and **specificity** separately (or precision/recall). In the worked example a classifier with 96.4% accuracy has only **30% sensitivity** - it is near-useless at the rare positive class, and only the split metrics reveal it.
- **Precision-recall trade-off.** They move inversely - you can push one up by sacrificing the other. Compare precision *at a fixed recall* (e.g. precision @ recall = 0.75), or collapse both into **F1** / **Fβ**.

#### 4. Beyond accuracy - other comparison axes

Classifiers are also judged on **speed** (cost to build/use), **robustness** (handling noise & missing values), **scalability** (behaviour as data grows - the Module 6 big-data theme), and **interpretability** (trees/rules are readable, neural nets are black boxes).

#### Key Takeaways for BDA601
1. This resource is the **evaluation half** of Module 6: you built Naive Bayes / decision-tree classifiers there, now you score them here. TP/TN/FP/FN and the confusion matrix are the shared currency of everything downstream (ROC, cost-benefit, the blog metrics).
2. **Activity 1** literally asks for a *contingency table* (= confusion matrix) comparing two decision-tree models on accuracy, precision, recall and F1 - this resource is the formula sheet for it.
3. **Day-job anchor:** the cancer trap is the same reason a "99.9% of queries succeed" dashboard on a warehouse pipeline can still be hiding every failed nightly load - the rare, expensive class is exactly the one raw accuracy hides. Track the minority class explicitly.
4. Cross-links: sensitivity/specificity feed **ROC** (Resource 3), F1/precision/recall are re-derived in **Srivastava** (Resource 4), and MLN601 Module 5 hits the same confusion-matrix vocabulary.

---

### 2. Credibility: Training, Testing & Cross-Validation (Witten et al. 2017)

**Citation:** Witten, I. H., Frank, E., Hall, M. A. & Pal, C. J. (2017). *Data mining: Practical machine learning tools and techniques* (4th ed., Chapter 5 "Credibility: Evaluating What's Been Learned", §5.1 pp. 163-165, §5.3-5.5 pp. 167-171). Cambridge, MA: Morgan Kaufmann.
**Local source:** `r2_Credibility-Training-Testing-Cross-Validation-5.1-5.5_Witten-2017.pdf`

**Purpose:** Answers "how do I get a *reliable* estimate of future performance from limited data?" - the sampling side of evaluation (holdout, cross-validation, leave-one-out, bootstrap) that stops you fooling yourself.

---

#### 1. Training error is not future error

- We care about **future performance on new data**, not past performance on the data used to build the model.
- **Resubstitution error** (error on the training set) is **hopelessly optimistic** - the model has memorised those rows. A pruned tree can look *worse* on training data yet **generalise better** because the unpruned one is **overfitted**.
- The honest estimate comes only from a **test set** that played *no part* in building the model, and both sets must be **representative** of the underlying problem.

#### 2. Three datasets - keep them separate

| Set | Job |
|---|---|
| **Training** | Build the classifier(s) |
| **Validation** | Tune hyperparameters / pick the best scheme |
| **Test** | Estimate the *final* error rate - used **once**, at the very end |

- The **golden rule:** the test set may **never** influence any choice (feature, hyperparameter, model). Peeking introduces **optimistic bias**.
- After the estimate is locked, you *may* fold validation + test data back into training to build the final production model - that maximises data use without contaminating the estimate.

#### 3. Holdout & cross-validation (the limited-data workhorses)

- **Holdout:** typically **2/3 train, 1/3 test**. Simple, but you may get an unrepresentative split.
- **Stratification:** force each class to appear in train and test in roughly its full-dataset proportion - a cheap safeguard against unlucky splits (**stratified holdout**).
- **Repeated holdout:** redo the split several times with different random samples and average - reduces the luck-of-the-draw variance.
- **k-fold cross-validation:** split into *k* equal folds; each fold is held out for testing once while the other *k-1* train; average the *k* error rates. **Every instance is used once for testing and k-1 times for training.**
- **The standard:** **stratified 10-fold cross-validation** - empirically the best bias/variance trade-off. For a reliable number, **repeat it 10 times (10 x 10-fold = 100 runs)** and average.

#### 4. Other estimates - leave-one-out & bootstrap

| Method | How | Pro | Con |
|---|---|---|---|
| **Leave-one-out (LOO)** | n-fold CV; leave out 1 instance each time | Max training data; deterministic (no random folds) | Very expensive (n runs); **cannot stratify** - pathological on 50/50 random data |
| **0.632 bootstrap** | Sample n rows *with replacement* for training; unpicked rows (~36.8%) are the test set | Best for **very small** datasets | Optimistically biased if model memorises |

- **Bootstrap maths:** probability a row is *never* picked in n draws → (1 - 1/n)ⁿ ≈ **e⁻¹ = 0.368**, so training ≈ **63.2%** unique rows, test ≈ 36.8%.
- **0.632 estimate:** `e = 0.632·e_test + 0.368·e_train` - blends the pessimistic test error with the optimistic resubstitution error.
- **Hyperparameter selection** (e.g. *k* in k-NN) must use the **validation set / inner CV only** - never the test set. Doing it properly inside CV means **nested (inner/outer) cross-validation**, which is compute-heavy but distributes easily across machines.

#### Key Takeaways for BDA601
1. Han (Resource 1) gives the **metric**; Witten gives the **sampling protocol** that makes the metric trustworthy. You need both: a precision number from a leaked test set is worthless.
2. **10-fold stratified CV is the default answer** whenever the assessment or a real project asks "how good is this model?" on limited data - and it maps directly onto PySpark's `CrossValidator`.
3. **Day-job anchor:** this is the discipline behind never validating a warehouse transformation on the same rows you tuned it on - hold out a fresh slice (or a later date partition) so your "it works" number reflects tomorrow's loads, not yesterday's.
4. Cross-links: Han §8.5.2-8.5.4 (Resource 1's tail) covers holdout/subsampling/CV from the other textbook; Srivastava (Resource 4) re-teaches k-fold with the bias/variance trade-off for *k*.

---

### 3. Comparing Classifiers on Cost-Benefit & ROC Curves (Han, Pei & Kamber 2011)

**Citation:** Han, J., Pei, J. & Kamber, M. (2011). *Data mining: Concepts and techniques* (3rd ed., §8.5.6 "Comparing Classifiers Based on Cost-Benefit and ROC Curves", pp. 373-377). Waltham, MA: Elsevier / Morgan Kaufmann.
**Local source:** `r3_Comparing-Classifiers-Cost-Benefit-and-ROC-8.5.6_Han-2011.pdf`

**Purpose:** Drops the assumption that all errors cost the same, and gives a **threshold-independent** visual tool (ROC/AUC) for comparing probabilistic classifiers - the natural next step once single-number accuracy proves too blunt.

---

#### 1. Costs and benefits are not symmetric

- Real applications assign **different costs** to FP vs FN and **different benefits** to TP vs TN. A **false negative on cancer** (missed disease) costs far more than a **false positive** (an unnecessary follow-up).
- So instead of `(TP+TN)/total`, compute the **average cost/benefit per decision**, weighting each cell of the confusion matrix by its real-world cost.
- Same logic in business: cost of **loaning to a defaulter** >> cost of denying a good customer; cost of **mailing non-responders** vs missing responders in target marketing.

#### 2. The ROC curve

- **ROC** (receiver operating characteristic) plots **TPR (y) vs FPR (x)** as the decision **threshold t** sweeps from high to low.
  - **TPR = TP/P = sensitivity** (y-axis)
  - **FPR = FP/N = 1 - specificity** (x-axis)
- Requires a **probabilistic** classifier: rank tuples by predicted P(positive), then walk the list top-down - **move up** on a true positive, **move right** on a false positive.
- **Reading the curve:** a good model hugs the **top-left** (steep early rise). The **diagonal = random guessing**; the closer a curve sits to the diagonal, the weaker the model. In the worked comparison, **M1 dominates M2** because it stays further above the diagonal.

#### 3. AUC - collapsing the curve to one number

| AUC | Meaning |
|---|---|
| **1.0** | Perfect classifier |
| **~0.5** | No better than random |
| Higher = better | Area under the ROC curve = overall ranking quality |

- **AUC is threshold-independent** - it summarises performance across *all* thresholds, so you compare models without committing to one operating point.
- Naive Bayes and backprop return probabilities natively; decision trees can be adapted to output class probabilities so they too can be ROC-plotted.

#### Key Takeaways for BDA601
1. This is the **model-selection** payoff of the module: given two trained classifiers, ROC/AUC tells you which to ship *and* lets you pick an operating threshold that matches your cost structure.
2. **AUC beats accuracy for imbalanced problems** (the cancer/fraud case from Resource 1) because it never assumes a 0.5 threshold or equal class costs - it judges the model's *ranking* ability.
3. **Day-job anchor:** cost-sensitive thinking is exactly a data-quality alerting trade-off - a missed bad load (FN) can silently corrupt a warehouse for days, while a false alert (FP) just costs five minutes of triage, so you deliberately tune the threshold toward high recall.
4. Cross-links: TPR/FPR come straight from Resource 1's sensitivity/specificity; Srivastava (Resource 4) adds AUC-ROC, Gini (= 2·AUC - 1), lift/gain and KS as sibling ranking metrics.

---

### 4. Twelve Important Model Evaluation Metrics (Srivastava 2019)

**Citation:** Srivastava, T. (2019, 6 August; updated 2025). *Eleven/Twelve important model evaluation metrics for machine learning everyone should know* [Web log post]. Analytics Vidhya. Retrieved from https://www.analyticsvidhya.com/blog/2019/08/11-important-model-evaluation-error-metrics/
**Local source:** `r4_Twelve-Important-Model-Evaluation-Metrics_Srivastava-2019.pdf`

**Purpose:** An industry-practitioner tour that widens the toolkit beyond the textbook - classification *and* regression metrics - and hammers the core message: **different problems demand different metrics** (the exact statement Activity 2 asks you to explain).

---

#### 1. Two model families → two metric families

- **Classification** (class or probability output) vs **regression** (continuous output) need **different metrics**.
- **Class-output** algorithms (SVM, KNN) → judged with the **confusion matrix**. **Probability-output** algorithms (logistic regression, random forest, boosting) → judged with two different families: **threshold-sweeping** metrics like **ROC/AUC** (vary the cut-off to trace TPR vs FPR) *and* **probability-calibration** metrics like **log loss** (score the predicted probabilities directly, no threshold involved). Converting probability → class is just applying a threshold (default 0.5).

#### 2. Classification metrics

| Metric | Gist | When it shines |
|---|---|---|
| **Confusion matrix** | TP/TN/FP/FN table; FP = Type-1 error, FN = Type-2 error | Foundation for all class metrics |
| **F1 / Fβ** | Harmonic mean of precision & recall; HM punishes extremes (precision 0, recall 1 → F1 = 0, not 0.5) | Need precision *and* recall together |
| **Gain & Lift charts** | Rank by predicted prob, bucket into deciles, measure responders captured | **Campaign targeting** - which deciles to mail |
| **Kolmogorov-Smirnov (KS)** | Max separation between positive & negative distributions (0-100) | Degree of class separation |
| **AUC-ROC** | Area under TPR vs (1-specificity); threshold-independent | Imbalanced data; ranking quality |
| **Log loss** | Negative avg log of corrected predicted probs; penalises *confident* wrong calls | Care about probability *calibration*, not just order |
| **Gini** | 2·AUC - 1 (good > 60%) | Single-number ranking score |
| **Concordant-Discordant ratio** | % of positive/negative pairs correctly ranked | Raw predictive power |

- **Rule-of-thumb AUC bands:** .90-1 excellent, .80-.90 good, .70-.80 fair, .60-.70 poor, .50-.60 fail.
- **ROC vs Lift:** ROC is **almost independent of the response rate**; lift shifts when the population's base rate changes - so ROC travels better across datasets.
- **Log loss vs AUC:** AUC only cares about the *order* of probabilities; **log loss** also rewards assigning *high confidence* to correct calls - closer to true positives should mean lower loss.

#### 3. Regression metrics

| Metric | Gist |
|---|---|
| **RMSE** | Root mean squared error; squares → punishes large errors, very **outlier-sensitive** (remove outliers first) |
| **RMSLE** | Log version; forgives big absolute gaps when both actual & predicted are large |
| **R² / Adjusted R²** | R² = how much better than predicting the mean (0 = baseline, 1 = perfect); **Adjusted R²** penalises useless added features |

#### 4. Cross-validation as the honesty check

- Reiterates Witten's message from a Kaggle angle: a great **public leaderboard** score that tanks on the **private** board is **overfitting**. **k-fold CV** exposes it *before* you see test results.
- **Bias/variance trade-off in choosing k:** small *k* → higher selection bias, low variance; large *k* (→ LOO at k=n) → low bias, high variance. **k = 10 is the recommended default.**

#### Key Takeaways for BDA601
1. **This is the Activity 2 resource.** The statement to explain in your own words - *"different evaluation metrics are used for different kinds of problems"* - is this article's thesis: pharma wants **specificity** (avoid false alarms), an attrition/churn model wants **sensitivity** (catch every leaver), a campaign wants **lift**, a regression wants **RMSE/R²**.
2. It **unifies Resources 1-3**: confusion-matrix metrics (R1), CV (R2) and ROC/AUC (R3) all reappear here, plus the practitioner extras (lift, KS, log loss, Gini) you'll meet in industry.
3. **Day-job anchor:** picking the metric to match the decision is the same instinct as choosing the right SLA for a pipeline - freshness, completeness and correctness are *different* metrics, and optimising the wrong one gives a green dashboard over a broken warehouse.
4. Practical: `sklearn.model_selection.KFold` / PySpark `CrossValidator` implement the k-fold shown here - the same tooling you'll use for Activity 1's two-model comparison.

---

## Where this module fits

- **Modules 4-6** built and cleaned data then trained classifiers; **Module 7 scores and selects** them - the quality gate before deployment.
- **Confusion matrix → metrics (R1) → reliable sampling (R2) → cost-aware ranking (R3) → the full practitioner toolkit (R4)** is the logical arc.
- Feeds directly into **Assessment 2** (train + *evaluate* + compare models) and the two discussion-forum activities below.
