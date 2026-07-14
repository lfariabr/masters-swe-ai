# Module 7 - Class Notes (Week 7 Live Lecture)
## Model Evaluation · Dr. Chen Zhan

> **Source:** Week 7 live lecture recording (14 Jul 2026, ~3h04m), Dr. Chen Zhan. This file captures what the **lecture** added on top of the four readings in [module07_notes.md](module07_notes.md). Where they overlap (confusion matrix, precision/recall/F1, holdout, cross-validation, ROC/AUC) the resource notes carry the detail. This file focuses on the **conceptual framing (3 questions)**, the **metrics for the other two task families (regression + clustering)** that the readings never touch, Dr. Chen's **reporting rules**, and the **Assessment 2 debrief**.

---

## TL;DR
Evaluation exists to answer **three questions**: will it work on unseen data, which model is better, and are the errors acceptable to the business. Different **tasks** need different **metric families**: classification → confusion matrix; regression → MAE/RMSE/R²; clustering → silhouette/elbow. Dr. Chen's practical bar for a classifier is **AUC > 0.8** (a convention, like p < 0.05). His reporting rule: **do not list every metric** - start with the confusion matrix, then pick **2-3 that match the business**. And the line that decides marks: **"a strong report justifies why you chose the metric that fits the problem, not merely which metric is the highest."** The A2 debrief confirms the **interpretation section carries the most marks**, and that **PySpark is no longer mandatory**.

## 1. The three questions evaluation answers ⭐
Dr. Chen framed the whole module around three questions:

| # | Question | What it is really asking |
|---|---|---|
| **1** | **Future performance** | How well will the model work on data it has **never seen**? The training data is not the point - the model is useful only if the pattern **transfers**. |
| **2** | **Model comparison** | Which model is better, **under the same problem, the same split and the same metrics**? Different algorithms, and even the same algorithm with different parameters, give very different results. |
| **3** | **Decision value** | Are the errors **acceptable** in this business, ethical and safety context? |

> **His closing line on this:** *"Evaluation is not only a score. It is an argument that the model is reliable enough for your specific use case."* That reframing is worth quoting in a report.

## 2. Different tasks need different metric families ⭐
The readings only cover classification. The lecture explicitly covered all three task families, because the **output data type** decides the metric:

| Task | Output | Metric family |
|---|---|---|
| **Classification** | categorical / binary label | confusion matrix → accuracy, precision, recall, specificity, F1, ROC/AUC |
| **Prediction (regression)** | a **number** (e.g. tomorrow's temperature: 7 to 15 °C) | **MAE, RMSE, R²** + residual plots |
| **Clustering** | groups (unsupervised) | **silhouette score**, elbow curve, Davies-Bouldin |

The **strategy** layer (holdout, validation, cross-validation, no leakage) is **task-independent** - it applies to all three. Only the **metrics** change.

## 3. Choosing the metric (his decision rules)

| Situation | Use |
|---|---|
| **Balanced** classes | accuracy + confusion matrix are appropriate |
| **Imbalanced** classes (the usual reality) | precision, recall, F1, AUC. *"Even an empty guess - everyone is healthy - gives 99% accuracy and represents nothing about the model."* |
| Need to **rank** or set a **threshold** | AUC and PR curves |
| Errors carry **different costs** | cost-benefit analysis |

- 🔴 **The reporting rule (say this in the exam):** **do not list every metric.** *"Start with the confusion matrix, then choose about two or three metrics that match your business the most."* A metric dump is a weak report.
- 🔴 **His summary slide, verbatim in spirit:** *"A strong report justifies **why** you choose a metric that fits the analytical problem, not merely **which** metric is the highest."*

## 4. ROC / AUC - the lecture's extra detail 🔴
This came out of a question I asked live about the ROC plot, so it is worth pinning down:

- The **dotted diagonal is the random-guess baseline**. What you actually measure is the **area under the curve**, not the distance above the diagonal at a point.
- **Scale:** max **1.0**, min **0.0**, **0.5 = random guessing** (a coin toss).
- 🔴 **The practical bar: AUC above ~0.8 is considered a good classifier.** Dr. Chen was explicit that this is **a convention, not a derivation** - "like using p < 0.05 for significance in conventional statistics." Below that, go back and change the feature set or the method.
- 🔴 **AUC close to 0 is a debugging signal, not a bad model.** It means you are **systematically predicting the opposite** (every sick patient called healthy and vice-versa) - trace back and find the bug in the model or the plot.

## 5. Regression metrics (not in the readings)

| Metric | Mechanism | Note |
|---|---|---|
| **MAE** (mean absolute error) | average of `|actual - predicted|`; the **absolute value neutralises** positive and negative gaps so they do not cancel out | the simple, interpretable one |
| **RMSE** | **squares** the error to neutralise sign, then roots it → **penalises large errors more strongly** | the most commonly used |
| **R²** | proportion of the **variance explained** by the model | not an error metric at all - a **goodness-of-fit** metric |

- 🔵 **How he reads R²:** R² = 0.7 means **30% of the variability is unexplained** - that leftover is either **variables you did not include** or something **unobserved / unmeasurable**. So R² doubles as a **feature-engineering signal**: a low R² tells you the feature set is incomplete. Usually reported alongside linear regression.

### His practical checklist for regression models
1. **Compare against a simple baseline** (e.g. always predict the average, or the last known value). Same philosophy as the ROC 0.5 line: a data-driven model must beat the trivial one.
2. **Inspect the residuals**, not just the summed error. Look for **systematic bias**, **outliers**, or **errors concentrated in one subgroup** - that pattern matters more than the error total.
3. **Report the error in a meaningful business unit** - dollars, minutes, days, years. Not a bare float.
4. **Guard generalisation** with train/test or cross-validation, and never touch the test set before the end.

## 6. Clustering metrics (preview of Module 9, but examinable now)
Unsupervised, so there is no ground truth to compare against. The goal is **maximise within-cluster similarity** and simultaneously **maximise between-cluster distance**.

- **Metrics:** **silhouette score** (the standard - it combines both aspects into one number), **elbow curve**, **Davies-Bouldin index**.
- 🔴 **A high score is not enough.** *"A segmentation is valuable only if stakeholders can name and act on the cluster."* Combine the metric with **cross-tabs and domain interpretation**.

### Four clustering pitfalls he listed
| Pitfall | Why it is bad |
|---|---|
| **Too many clusters** | mathematically better, but meaningless to the business and impossible to act on |
| **One giant cluster** | hides the important subgroups - if everything is the same group, the result says nothing |
| **Unstable clusters** | a good clustering survives adding a few points or nudging a parameter/feature. If it does not, it is not real |
| **No domain meaning** | a cluster must be explainable using the variables that matter in the problem (his example: cell types should land on ~4-5 biologically meaningful clusters, not 30) |

## 7. Data leakage - his framing 🔴
The rule is in the readings, but his mental model is the most usable version:

> **Treat the test set as data that arrives tomorrow.** Today you train on what you have; you have **no knowledge at all** of the rows that will arrive tomorrow. That is the guarantee of an independent evaluation.

Nothing from the test set may influence **preprocessing, feature selection, or hyperparameter tuning**. He repeated it in the code practical: `StringIndexer` is fitted on **training only**.

- **His split ratios:** holdout **70/30 or 80/20** (the readings say 2/3-1/3 - both are fine, it is a preference). Cross-validation: **5-fold or 10-fold**.

## 8. Code practical (LA1) - and the one result that matters
Two decision trees predicting `income` on the Larose `adult_ch6` data, from different feature sets.

- **Contingency table:** the old PySpark function is **deprecated** - build it manually with `groupBy(actual).pivot(prediction).count().fillna(0)`.
- **Metrics:** `MulticlassClassificationEvaluator` for accuracy / precision / recall / F1 (set `labelCol`, `predictionCol`, `metricName`); `BinaryClassificationEvaluator` on the **`rawPrediction`** column for AUC (raw prediction = the model's confidence score, which the probability is derived from).
- 🔴 **The live finding, and it is the point of the whole module:** Model 1 scored **accuracy ≈ 0.8**, Model 2 scored **accuracy ≈ 0.9** - **but Model 2's AUC dropped.** Dr. Chen: *"this case is confirming that accuracy might be misleading in some cases."*
  - **This is exactly the Random Forest result in my A2:** RF has the best AUC (0.8334) yet the **worst recall at the default threshold** (0.479 vs the tree's 0.500). A higher headline number on one metric with a worse ranking underneath. Worth citing in the A2 interpretation, since it echoes the lecturer's own demonstration.

### Activity 2 - the scenario table he walked through
| Scenario | Main concern | Metric that fits |
|---|---|---|
| **Fraud detection** | missing a fraudulent transaction | **recall** |
| **Spam filtering** | blocking a **genuine** email | **precision** |
| **Imbalanced classification** | neither alone is enough | **F1 / AUC** |

His instruction: do not just memorise the table - go back to the **definition** of each metric and explain **why** its formula targets that specific concern.

---

## 9. Assessment 2 debrief (the marking hints) 🔴

**Scope:** Telco customer churn. Source code **+** report. **30%** of the grade. Due **26/07/2026**.

### Requirements
- **Report ≥ 1000 words.** More is fine - *"I won't criticise a report with 2000 words."* But **500-600 words will be marked down**: he treats length as correlated with quality.
- **Report is prose, not code.** 🔴 *"Do not paste or copy your code into the report - that violates the purpose of the report."* Plots generated by the notebook **may** be reused in the report.
- **Notebook sections:** problem statement → EDA (visual **and** statistical) → data cleaning & feature selection → model building (decision tree) → evaluation.
- **Feature selection must be justified.** Manual picking is allowed, but the report must say **why** - and ideally back it with a **data-driven** argument (correlation analysis) and **a plot that justifies the choice**.
- **Missing values** must be explicitly handled and explained. Duplicates too.

### 🆕 What he relaxed
- 🔴 **PySpark is NOT mandatory.** *"The size of the data doesn't fit the big-data situation, so PySpark won't be necessary. You won't get any penalty for using packages or platforms other than PySpark."* pandas + scikit-learn is fully acceptable.
- **R is allowed** (submit **R Markdown**, not a bare `.R` file). Julia or similar is fine.
- ❌ **SPSS and SAS Viya are NOT allowed** - *"not programming languages, more like Excel-like interactive tools."* It must be a statistical **programming language**.

### Deliverables
- **Notebook (`.ipynb`) - required.** Not a plain `.py`. Results and plots must be **visible below each code chunk**.
- **Report (Word or PDF) - required.**
- Modified dataset - optional, *"honestly I don't pay attention to this one."* Files may be submitted separately; no need to zip.

### 🔴 Where the marks actually are
The rubric runs: understanding the data (visualisations + statistics) → pipeline, preprocessing and feature selection (harmonising, anomalies, redundancies, inconsistencies, **correlation analysis**) → model building → presentation and clarity → handling missing values → **interpretation**.

> **The single most important sentence of the debrief:** *"The most abundant mark will go to the interpretation of the data analysis. That's what distinguishes a good, extraordinary submission from an average one - everyone can do a more or less similar implementation, but the interpretation highlights your thinking."*

Translation: the modelling is table stakes. **The marks are won by converting the numbers into a business argument** - what does this model tell a stakeholder, and what should they do about it.

### AI policy
Cannot use AI to **generate** the report or submission. Can use it as a **tutor / pair** while learning and building. Follow the AI policy on the submission declaration.

---

### Day-job anchors
1. **The three questions** map straight onto shipping a pipeline change: will it hold on tomorrow's loads (future performance), is it better than the current job (model comparison), and can the business live with the failure mode (decision value)?
2. **"Treat the test set as data that arrives tomorrow"** is the cleanest statement of why you never tune a transformation on the rows you are about to validate it on.
3. **Report the error in business units** - a warehouse SLA breach measured in "hours of stale data" lands with stakeholders; an RMSE of 0.043 does not.
