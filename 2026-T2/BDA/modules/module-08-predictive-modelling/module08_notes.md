# Module 8 - Predictive Modelling

## TL;DR

Module 6 built classifiers, Module 7 scored them - Module 8 adds the **regression** half of supervised learning and closes the loop back to the business.
- **Data mining defined (McCormick):** find previously unknown relationships in data **collected for business reasons** (not experiments), prove them, and **deploy** - *"we're not done until we deploy."* A model that never scores new data is worthless.
- **Linear regression (Lee Ch6):** predict a **number**. **Simple** (1 feature) → **multiple** (2+ features) → **polynomial** (curve, degree n) → **polynomial multiple**. Pick features with `corr()`; judge with **R²** (1.0 = perfect fit).
- **The overfitting demo:** on the toy dataset, degree 2 → R² 0.9474, degree 3 → 0.9889, degree 4 → **R² = 1.0 and worthless**. A perfect training fit is a red flag, not a win. This is **bias vs variance**.
- **Logistic regression (Lee Ch7):** predict a **probability**. Linear regression breaks on binary outcomes (it predicts negative values), so wrap it in the **sigmoid** - the inverse of the **logit** (log-odds) - to squash (-∞, ∞) into **(0, 1)**, then threshold at **0.5**. Despite the name, it is a **classifier**.
- **Loop back to Module 7:** Ch7 re-derives the confusion matrix, accuracy, precision, recall, F1, FPR and ROC/AUC - and repeats the imbalanced-data warning (997/1000 accuracy from a "dumb algorithm").

⚠️ **Two traps flagged below:** the textbook's **bias/variance advice is self-contradictory** (Resource 2 §5), and **Activity 1's `load_boston()` no longer exists** in modern scikit-learn (§4).

Feeds **SLO d)** and **Assessment 2** (due **26/07/2026**, end of this module).

---

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Watch & summarise McCormick (2017) - The essential elements of predictive analytics and data mining | ✅ |
| **2** | Read & summarise Lee (2019) - Supervised Learning: Linear Regression (Ch6, pp. 119-149) | ✅ |
| **3** | Read & summarise Lee (2019) - Supervised Learning: Classification Using Logistic Regression (Ch7, pp. 151-175) | ✅ |
| 4 | Activity 1: Boston house-price - correlations, top 3 features, degree-2 polynomial, R² on 30% test + forum post | 🕐 |

**Local sources (this folder):**
- `r1_Essential-Elements-of-Predictive-Analytics-and-Data-Mining_McCormick-2017.md` (Resource 1 - LinkedIn Learning transcript + knowledge-check questions)
- `r2_Supervised-Learning-Linear-Regression-Ch6_Lee-2019.pdf` (Resource 2)
- `r3_Classification-Using-Logistic-Regression-Ch7_Lee-2019.pdf` (Resource 3)

---

## Key Highlights

### 1. The Essential Elements of Predictive Analytics and Data Mining (McCormick 2017)

**Citation:** McCormick, K. (2017). *The essential elements of predictive analytics and data mining* [Video file]. LinkedIn Learning. Retrieved from https://www.linkedin.com/learning/the-essential-elements-of-predictive-analytics-and-data-mining/introduction-3
**Local source:** `r1_Essential-Elements-of-Predictive-Analytics-and-Data-Mining_McCormick-2017.md` (transcript)

**Purpose:** Defines what data mining actually **is** - and, more usefully, what separates it from statistics, BI reporting and EDA. The whole video hangs on one word: **deployment**.

---

#### 1. McCormick's definition (worth memorising)

> *"Data mining is the **selection and analysis of data, accumulated during the normal course of doing business**, to find and confirm **previously unknown relationships** that can produce **positive and verifiable outcomes** through the **deployment of predictive models** when applied to **new data**."*

He emphasises four things, each of which excludes a neighbouring discipline:

| Element | What it means | What it rules out |
|---|---|---|
| **The data is not new** | it was collected for **business reasons**, not for an experiment | designed experiments, polls, interviews |
| **Not testing hypotheses** | the relationships are **previously unknown** - you discover, you do not confirm a prior belief | hypothesis testing |
| **Verifiable outcomes** | it must be **proven**, and **useful** to the business | exploratory data analysis |
| **Applied to new data** | *"we're not done until we deploy"* | BI reporting on historical data |

- 🔴 **The exam-shaped point:** statistics, hypothesis testing, BI reporting and EDA each **overlap** with data mining, but **none has the complete list** of these elements. That combination is what makes a project "true data mining."

#### 2. The predictive analytics loop

```text
PAST data  ──→ build the MODEL ──→ (a rule set: IF store_card AND spend > X THEN purchase)
                                             │
CURRENT data (nightly / real-time) ──→ SCORE ──→ propensity score
                                                        │
                                                     ACTION
                                        (send the offer / don't send it)
                                     (service the equipment / let it run)
```

- **Past data is the basis of the model; current data is what you score.** Two datasets, two jobs.
- **The model itself is unglamorous** - McCormick describes it as *"an extended if-then-else statement"*. The value is not the model's sophistication, it is the action it triggers.
- **The focus is binary classification** - which is why Modules 6, 7 and 8 keep landing on the same confusion matrix.
- 🔴 **Deployment = taking action based on a prediction.** That is a **different** thing from *running* the model to make the prediction - the knowledge check in the R1 transcript tests exactly this distinction.

#### 3. Why he says "data mining" at all

There is *"a lot of competition among words"* - predictive analytics, data science, big data. He uses **data mining** because he uses **CRISP-DM** (Cross-Industry Standard Process for Data Mining), the **de facto standard process**, and that standard uses the term. Pragmatic, not philosophical.

#### Key Takeaways for BDA601
1. **This is the "so what" resource of the whole subject.** Modules 5-7 taught you to clean, build and score. McCormick's point is that **none of it counts until a decision changes** - which is precisely the criterion Dr. Chen said carries the most marks in A2 ("the interpretation distinguishes an extraordinary submission from an average one").
2. **"Data accumulated during the normal course of doing business"** describes the Telco churn dataset exactly - nobody ran an experiment on customers; the data is exhaust from billing and support systems. The A2 report can open on this framing.
3. **Day-job anchor:** your warehouse *is* the data accumulated during the normal course of doing business. A model that flags at-risk records but never triggers a ticket, an alert or a retry is not deployed - it is a dashboard. McCormick would say the project is not finished.
4. Cross-links: CRISP-DM lines up with the analytics lifecycle from Module 1; the binary-classification focus connects straight to Modules 6-7.

---

### 2. Supervised Learning - Linear Regression (Lee 2019, Ch6)

**Citation:** Lee, W. (2019). *Python machine learning* (Chapter 6 "Supervised Learning - Linear Regression", pp. 119-149). Indianapolis, IN: John Wiley and Sons.
**Local source:** `r2_Supervised-Learning-Linear-Regression-Ch6_Lee-2019.pdf`

**Purpose:** The regression half of supervised learning - predicting a **numeric** label rather than a class. Builds from multiple regression to polynomial regression on the Boston housing data, and lands on the **bias-variance trade-off**.

---

#### 1. Vocabulary and the four flavours

- **Features** = independent variables = explanatory variables. **Label** = dependent variable = target.
- **Classification vs regression:** both predict a value from a set of inputs. Classification predicts a **categorical** value; regression estimates a **numeric** one. Same machinery, different output type - which is exactly why Module 7's metric families split the way they do.

| Type | Relationship modelled |
|---|---|
| **Simple linear** | 1 independent → 1 dependent, a straight line |
| **Multiple** | **2+ independent** → 1 dependent |
| **Polynomial** | 1 independent → 1 dependent, via an **nth-degree polynomial** (a curve) |
| **Polynomial multiple** | **2+ independent** → 1 dependent, via an nth-degree polynomial |

*(Multivariate linear regression - more than one **correlated dependent** variable - is named but out of scope.)*

#### 2. The Boston workflow, end to end

**Dataset:** 506 rows, 13 numeric predictors, target **MEDV** (median home value in $1000s). From StatLib at Carnegie Mellon.

1. **Inspect** - `dataset.data`, `.feature_names`, `.DESCR`, `.target`; load into a DataFrame, then attach `df['MEDV'] = dataset.target`.
2. **Cleanse** - `df.info()` (scikit-learn needs **numeric** fields; encode strings if present - Boston is all-numeric) and `df.isnull().sum()` (Boston has **no missing values**).
3. **Feature selection via correlation** - *"we do not want to use all of these features... not all of them are relevant."* Use `df.corr()`, the **pairwise correlation** of columns.
   - **-1.00** = perfect negative · **0.00** = none · **+1.00** = perfect positive.
   - Programmatically: `df.corr().abs().nlargest(3, 'MEDV').index` → `['MEDV', 'LSTAT', 'RM']`, values `[1.0, 0.7377, 0.6954]`. **Ignore MEDV** - it correlates perfectly with itself.
   - **The two winners:** **LSTAT** (% lower-status population, **-0.7377** - as it rises, prices fall) and **RM** (avg rooms per dwelling, **+0.6954** - more rooms, higher price).
4. **Split** - `train_test_split(x, Y, test_size=0.3, random_state=5)` → 354 train / 152 test.
5. **Train** - `LinearRegression().fit(x_train, Y_train)`.
6. **Evaluate** - `model.score(x_test, Y_test)` → **R² = 0.6162**.

#### 3. Reading the trained model

**Formula:** `Y = β₀ + β₁x₁ + β₂x₂`

- `model.intercept_` → **0.3844** (β₀) · `model.coef_` → **[-0.6596, 4.8320]** (β₁ for LSTAT, β₂ for RM).
- 🔵 **The coefficients are interpretable, and that is the point:** RM's **+4.83** means each extra room adds ~$4,830 to the predicted price; LSTAT's **-0.66** means each percentage point of lower-status population subtracts ~$660.
- Predicting by hand for `LSTAT=30, RM=5`: `0.3844 + (-0.6596 × 30) + (4.8320 × 5) = 4.7569` - which matches `model.predict([[30,5]])`. The model is arithmetic you can do on paper.
- With two features you can plot a **3D hyperplane** (`plot_surface`) instead of a 2D line.

#### 4. Polynomial regression - when a straight line is not enough

| Degree | Formula | Name |
|---|---|---|
| 1 | `Y = β₀ + β₁x` | simple linear |
| 2 | `Y = β₀ + β₁x + β₂x²` | **quadratic** |
| 3 | `Y = β₀ + β₁x + β₂x² + β₃x³` | cubic |
| n | `Y = β₀ + β₁x + ... + βₙxⁿ` | general |

- 🔵 **Mechanically:** `PolynomialFeatures(degree=2).fit_transform(x)` expands each row into `[1, x, x²]` (verify with `get_feature_names()`), then you fit an ordinary **`LinearRegression`** on the expanded matrix. **Polynomial regression is still linear regression** - linear in the *coefficients*, just fed engineered features. This is the single most useful mechanical insight in the chapter.
- **For two features at degree 2** the expansion becomes `['1', 'x', 'y', 'x^2', 'x y', 'y^2']` → `Y = β₀ + β₁x₁ + β₂x₂ + β₃x₁² + β₄x₁x₂ + β₅x₂²`. Note the **interaction term** `x₁x₂` appears for free.
- **On Boston:** degree-2 polynomial multiple regression lifts **R² from 0.6162 → 0.7340** on the same test set. A real gain from the same two features.

#### 5. Bias, variance and the overfitting demo ⭐

**The demo to remember** - fitting a 6-point toy dataset:

| Degree | R² (training) | Verdict |
|---|---|---|
| 1 (straight line) | 0.8658 | underfits |
| **2** | 0.9474 | better |
| **3** | 0.9889 | better still |
| **4** | **1.0000** | 🔴 **fits perfectly - and is worthless** |

> *"You get an R-Squared value of 1! However, before you celebrate... while your algorithm may fit the training data perfectly, it is unlikely to perform well with new data. This is known as **overfitting**."*

- **Bias** = the algorithm's inability to capture the true relationship. Straight line → **high bias** (misses the points). Curvy line → **low bias** (hits them all).
- **Variance** = how much the fit changes across datasets. The curvy line gives **wildly different RSS** on new points → **high variance**. The straight line's RSS stays similar → **low variance**.
- **RSS** (residual sum of squares) = the summed prediction error, measured on the **test** points.
- **Overfitting** = a curve that fits all points. **Underfitting** = a line that fits few.
- **Countermeasures:** **Regularization** (automatically penalises extra features) · **Bagging** / bootstrap aggregation (subsets train weak learners, combined by averaging or max vote) · **Boosting** (all data per learner, but **misclassified points get more weight** for the next one). **Ensemble learning** = several models combined on one dataset.

> ⚠️ **ERRATUM - the book contradicts itself here.** After correctly stating that the **straight line has high bias** and the **curvy line has low bias**, the chapter advises: *"the ideal algorithm should have the following: **High bias**, with the line hugging as many points as possible; Low variance"* (Figure 6.19). That is wrong by the chapter's own definition - a line that **hugs many points** has **LOW** bias, and high bias is exactly what you do *not* want. The standard formulation is **low bias AND low variance**, with a **trade-off** between them (pushing one down tends to push the other up), the goal being the sweet spot that minimises **total error on unseen data**. Witten Ch5 and Srivastava (Module 7 R4, on choosing *k*) both state it conventionally. **Answer "low bias, low variance" in any assessment.**

#### Key Takeaways for BDA601
1. **This chapter IS Activity 1**, step by step: `corr()` → top features → degree-2 polynomial → 70/30 split → R². The only differences: the activity asks for **three** features (the chapter uses two) via **PySpark** (the chapter uses scikit-learn).
2. **R² is the metric that closes the loop with Module 7.** Dr. Chen's framing applies directly: R² = 0.6162 means **38% of the variability in house prices is unexplained** - by features not included, or by something unobserved. The lift to 0.7340 with a degree-2 polynomial is *"27% unexplained"* - progress, not victory.
3. 🔴 **For Assessment 2/3 (not just this activity): default to multiple linear regression.** Dr. Chen said it directly in the Week 8 lecture - *"multiple linear regression should be your number one choice... your benchmarking or baseline model."* Polynomial/interaction terms are an escalation you add **cautiously, only if the baseline underperforms** - they raise both overfitting risk and compute cost. Activity 1 asks for polynomial specifically (it's a teaching exercise), but the general assessment advice is: start simple, justify any complexity you add.
4. 🔴 **Unlike Module 7's AUC > 0.8 bar, regression metrics have no universal threshold.** Chen was asked directly ("is R² > 0.6 moderately good?") and declined to give one - R² depends on how complex the underlying relationship is. MAE/RMSE are worse still: they're **only meaningful for cross-model comparison** on the same dataset (model A's error 100 vs model B's 80 → B is better; there's no absolute "80 is good" line). Don't quote a regression metric as pass/fail in a report - quote it as a comparison.
5. **The degree-4 R² = 1.0 demo is Module 7's Zone 3 in regression form.** A perfect metric on the data you fit is not evidence, it is a warning. Same lesson as resubstitution error, different metric.
6. **Day-job anchor:** correlation-driven feature selection is what you already do informally when deciding which warehouse columns actually drive a KPI. The trap is the same one you hit in A2: `tenure` and `TotalCharges` correlated at **r = 0.826** - correlation finds the signal *and* the redundancy, and you have to decide which.
7. Cross-links: the bias/variance material re-covers Module 6's overfitting/pruning theme with a regression lens; **RMSE** appears here as `mean_squared_error` and is defined properly in Module 7 R4.

---

### 3. Supervised Learning - Classification Using Logistic Regression (Lee 2019, Ch7)

**Citation:** Lee, W. (2019). *Python machine learning* (Chapter 7 "Supervised Learning - Classification Using Logistic Regression", pp. 151-175). Indianapolis, IN: John Wiley and Sons.
**Local source:** `r3_Classification-Using-Logistic-Regression-Ch7_Lee-2019.pdf`

**Purpose:** Fixes linear regression's failure on binary outcomes by routing it through the sigmoid, producing a **probability** in (0, 1). Then evaluates it on the Breast Cancer Wisconsin data - looping the module back to Module 7's confusion matrix and ROC/AUC.

---

#### 1. Why linear regression breaks on binary outcomes

- **The setup:** voter income vs voting preference. Low income → candidate B, high income → candidate A. A binary outcome.
- **The failure:** fit a straight line and *"the predicted value does not always fall within the expected range"* - a very low-income voter gets a **negative** prediction. Negative *what*? The outcome is a category, not a quantity.
- **What you actually want:** a value from **0 to 1** representing the **probability of an event** - a curve, not a line.
- 🔴 **Naming trap:** logistic regression is a **classification** algorithm despite "regression" in its name. Its output is *"the probability of a given input point belonging to a specific class"*, always in **[0, 1]**.

#### 2. Odds → logit → sigmoid (the derivation)

| Step | Formula | What it does |
|---|---|---|
| **Odds** | `P / (1 - P)` | ratio of P(success) to P(failure) |
| **Logit** | `L = ln(P / (1-P))` | log of the odds - maps **(0,1) → (-∞, ∞)** |
| **Sigmoid** | `P = 1 / (1 + e^(-L))` | the **inverse** of the logit - maps **(-∞, ∞) → (0,1)** |

- **Odds worked examples:** a fair coin → 0.5/0.5 = **odds of 1** (a 50% chance). A rigged coin at P(head) = 0.8 → 0.8/0.2 = **4** (four times more likely to land heads than tails); the odds of a tail are 0.2/0.8 = **0.25**.
- 🔵 **The elegant bit:** *"the sigmoid curve is obtained when you **flip the axes** of the logit curve."* The logit has probability on x and the real line on y; flip it and you have exactly the function you want - real numbers in, probability out. The sigmoid is not invented, it is the logit read backwards.
- **With the model's parameters:** `P = 1 / (1 + e^(-(β₀ + xβ)))` - the familiar linear expression `β₀ + xβ` is simply **fed through the sigmoid**. β₀ = intercept, xβ = coefficient, both estimated by **Maximum Likelihood Estimation (MLE)**, not least squares.
- **Threshold (naming the classes explicitly):** the sigmoid returns `P(positive class)`. Lee's convention is **`P ≤ 0.5` → negative class, `P > 0.5` → positive class** - in his voting example, *"anything less than (or equal to) 0.5... will be considered as voting for candidate B, and anything greater than 0.5... candidate A."* **scikit-learn behaves the same way**: `predict()` is `decision_function > 0`, so a probability of **exactly 0.5 lands in the negative class**. Use this convention throughout.
  - ⚠️ **The course brief in `notes.md` states the opposite boundary** (*"any value less than 0.5 to 0 and any value greater than or equal to 0.5 to 1"*, putting exactly 0.5 in the **positive** class). The brief is quoted verbatim from the subject outline so it is left as-is, but be aware the two disagree **only at exactly 0.5** - a measure-zero case with continuous probabilities that will essentially never fire in practice. If it ever matters, **scikit-learn's actual behaviour (0.5 → negative) is what your code will do.**
  - *(Module 7's entire cost-sensitive threshold discussion attaches right here - 0.5 is a default, not a law.)*

#### 3. The Breast Cancer walkthrough

**Dataset:** Breast Cancer Wisconsin (Diagnostic), ships with scikit-learn. **30 features** computed from a digitised image of a fine needle aspirate (FNA). Binary label.

- 🔴 **The encoding trap that matters:** **0 = malignant, 1 = benign.** So the **positive class is "benign"** - the *opposite* of clinical intuition. Every metric below inherits this, and misreading it inverts your whole interpretation.
- **Single feature first** (`mean radius`): `LogisticRegression().fit(...)` → intercept **8.1939**, coefficient **-0.5429**. Plug into the sigmoid and you can plot the S-curve over the scatter.
  - `predict_proba(20)` → `[[0.9349, 0.0651]]` → 93% probability of class 0 → **malignant**. `predict_proba(8)` → `[[0.0208, 0.9792]]` → **benign**. Larger radius → malignant, exactly as the scatter suggested.
- **All 30 features:** `train_test_split(..., test_size=0.25, random_state=1, stratify=cancer.target)` → **75/25 split**, 30 coefficients.
  - 🔵 **`stratify`, explained by the book itself:** *"if the column specified is a categorical variable with 80% 0s and 20% 1s, then the training and test sets would each have 80% 0s and 20% 1s."* The same stratification Witten prescribes in Module 7 - here it is as one parameter.
  - 🔵 **`random_state`** = the seed. Without it *"every time you run this function you will get a different training and testing set"* - the reproducibility point from Module 6's PySpark practical.

#### 4. Evaluation - Module 7, re-derived

**Confusion matrix** via `pd.crosstab(preds, test_labels)` (rows = prediction, cols = actual) or `metrics.confusion_matrix(y_true, y_pred)` (**rows and columns are switched between the two** - a real source of silent errors):

```text
              ACTUAL
            0(mal)  1(ben)
PRED 0(mal)  TN=48   FN=3
     1(ben)  FP=5    TP=87
```

| Metric | Formula | Result on this model |
|---|---|---|
| **Accuracy** | `(TN+TP)/(TN+FN+FP+TP)` | **0.9441** |
| **Precision** | `TP/(FP+TP)` | 0.94 / 0.95 per class |
| **Recall (TPR)** | `TP/(FN+TP)` | 0.91 / 0.97 per class |
| **F1** | `2·(P·R)/(P+R)` - harmonic mean | 0.92 / 0.96 |
| **FPR** | `FP/(FP+TN)` | proportion of negatives misclassified as positive |

- 🔴 **The imbalanced-data warning, again, in Lee's words:** predicting equipment failure where **3 of 1,000 samples are defective**, a *"dumb algorithm"* that always returns "no failure" scores **997/1000 = 0.997**. *"Accuracy works best with evenly distributed data points, but it works really badly for a skewed dataset."* This is the **third independent source** in this subject making the identical point (Han → Dr. Chen → Lee). It will be examined.
- **Reading precision/recall under this encoding** (benign = positive): **low precision** → many FP → **malignant tumours called benign** → patients miss treatment. **Low recall** → many FN → **benign tumours called malignant** → unnecessary treatment and anguish. Hence the book's conclusion that *"having a low precision is more serious than a low recall."* ⚠️ **That conclusion holds only because benign is encoded as positive.** Flip the encoding and it reverses - which is precisely why Module 7 insists you state which class is positive before quoting any metric.
- **ROC:** `roc_curve(test_labels, preds_proba)` returns `(fpr, tpr, threshold)`; `auc(fpr, tpr)` → **AUC = 0.99**.
  - 🔵 **The book's manual derivation is the clearest ROC explanation in the whole subject:** at **threshold 0** everything is predicted positive → FN = 0 and TN = 0 → **TPR = 1, FPR = 1** → the point (1,1). At **threshold 1.0** nothing is predicted positive → TP = 0 and FP = 0 → **TPR = 0, FPR = 0** → the point (0,0). The default **0.5** gives a point in between. Sweep every threshold and you trace the curve. **That is why every ROC starts at (0,0) and ends at (1,1)** - it is forced by the arithmetic, not a convention.
  - *"Generally, aim for the algorithm with the highest AUC"* - matching Dr. Chen's AUC > 0.8 bar.

#### Key Takeaways for BDA601
1. **This chapter is the bridge back to A2.** Your Telco churn model is a binary classifier on business-exhaust data; logistic regression is the natural probability-output baseline to compare a decision tree against, and Ch7 supplies the full evaluation script (`classification_report`, `confusion_matrix`, `roc_curve`, `auc`) in scikit-learn - which Dr. Chen has now explicitly permitted instead of PySpark.
2. **Threshold 0.5 is a default, not a law.** Ch7 states it plainly and moves on; Module 7 showed what happens when you *question* it (your A2 slid the tree to t=0.26 and bought +18.5pp of recall). Ch7 gives the mechanism, Module 7 gives the judgement.
3. **The sigmoid is why probability-output classifiers exist at all** - and therefore why ROC/AUC, log loss and threshold tuning are possible. Class-output algorithms (SVM, KNN) cannot be ROC-plotted without adaptation (Module 7, R4).
4. **Day-job anchor:** logistic regression's coefficients stay **readable**, like linear regression's - each feature's contribution to the log-odds. When you must tell a stakeholder *why* a record was flagged, a logistic model answers; a random forest shrugs. That is Han's **interpretability** axis from Module 7 R1, and it is often worth more than a couple of AUC points.
5. Cross-links: everything in §4 is Module 7 R1 (metrics) and R3 (ROC/AUC) re-derived from a practitioner's angle - use Ch7 for the **code**, Han for the **theory**.

---

## 4. ⚠️ Activity 1 - `load_boston()` is dead (read before you start)

The chapter's code opens with `from sklearn.datasets import load_boston`. **This will not run on any modern scikit-learn.** It was deprecated in 1.0 and **removed in 1.2**, on ethical grounds.

**Source (scikit-learn's own deprecation notice, v1.0):** *"The Boston housing prices dataset has an ethical problem: as investigated in [1], the authors of this dataset engineered a non-invertible variable 'B' assuming that racial self-segregation had a positive impact on house prices [2]. Furthermore the goal of the research that led to the creation of this dataset was to study the impact of air quality but it did not give adequate demonstration of the validity of this assumption."*
- Retrieved from https://scikit-learn.org/1.0/modules/generated/sklearn.datasets.load_boston.html
- `[1]` Carlisle, M. (2019). *Racist data destruction?* Retrieved from https://medium.com/@docintangible/racist-data-destruction-113e3eff54a8
- `[2]` Harrison, D. & Rubinfeld, D. L. (1978). Hedonic housing prices and the demand for clean air. *Journal of Environmental Economics and Management, 5*(1), 81-102. https://doi.org/10.1016/0095-0696(78)90006-2

#### Why `B` is different from an ordinary demographic column

The dataset's own header defines it as **`B = 1000(Bk - 0.63)²`**, where `Bk` is the proportion of Black residents by town. The problem is not that it *records* demographics - it is the **shape of the transform**.

**The square makes it a parabola with its minimum at `Bk = 0.63`.** So `B` is lowest when a town is ~63% Black, and **rises as you move away from that point in either direction**:

| `Bk` (proportion) | `B` |
|---|---|
| **0.00** | **396.90** ← the maximum in the data |
| 0.10 | 280.90 |
| 0.30 | 108.90 |
| 0.50 | 16.90 |
| **0.63** | **0.00** ← the minimum |
| 0.80 | 28.90 |
| 1.00 | 136.90 |

Now pair that with the correlation matrix in Ch6: **`B` correlates +0.3335 with `MEDV`** - higher `B` means higher predicted price. Chain the two together and the encoded claim is: **prices rise the further a town sits from 63%, in either direction.** That is the "racial self-segregation has a positive impact on house prices" assumption scikit-learn names - and it was **built into the arithmetic in 1978, before any model ran**. The `0.63` is a chosen inflection point, not a discovered one.

**Check it against the raw file:** the first rows carry `B` = 396.90, 396.90, 392.83, 394.63. And `1000 × (0 - 0.63)² = 396.90` **exactly** - those are towns with `Bk ≈ 0`, receiving the **maximum** value of `B`, which pushes the predicted price **up**.

**And it is non-invertible** - which is why the dataset could not simply be patched:

```text
Bk = 0.26  →  B = 136.9
Bk = 1.00  →  B = 136.9   ← same output, opposite towns
```

Squaring destroys the information. Given `B = 136.9` you cannot recover whether the town was 26% or 100% Black, so you cannot undo the transform to audit the underlying data. Hence removal rather than repair.

🔴 **The irony that completes the argument:** the Harrison & Rubinfeld paper was about **air quality** (`NOX`) - the title is *"Hedonic prices and the demand for clean air"*. `B` was a control variable, and per scikit-learn's notice the study *"did not give adequate demonstration of the validity of this assumption."*

**This is worth a paragraph in the forum post.** It is a live, current example of the data-ethics thread running through BDA601 (**SLO b** - data security and privacy principles), and Module 12 covers privacy and ethics directly. It is also a concrete case of the Module 5 lesson that a *feature* carries the assumptions of whoever engineered it.

**How to get the data anyway** - the activity's own URL still serves the raw file:

```python
import pandas as pd, numpy as np
raw = pd.read_csv("https://lib.stat.cmu.edu/datasets/boston", sep=r"\s+", skiprows=22, header=None)
data = np.hstack([raw.values[::2, :], raw.values[1::2, :2]])
target = raw.values[1::2, 2]
cols = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','B','LSTAT']
df = pd.DataFrame(data, columns=cols); df['MEDV'] = target
```

*(Each record spans **two lines** in the raw file, which is why the reshape looks odd.)* Alternatives: `fetch_openml(name="boston", version=1)`, or swap in **California housing** (`fetch_california_housing()`), scikit-learn's designated replacement.

**Then the activity maps 1:1 onto Ch6:** `df.corr()` → `nlargest(4, 'MEDV')` (**4**, so that discarding MEDV itself still leaves **three** features - the activity asks for three, the chapter uses two) → `PolynomialFeatures(degree=2)` → 70/30 split → R² on the test set.

In PySpark: `VectorAssembler` → `PolynomialExpansion(degree=2)` → `LinearRegression` → `RegressionEvaluator(metricName="r2")`.

🔴 **The third feature, confirmed in class:** Dr. Chen ran this exact activity live (Week 8 lecture) and his `df.corr()` on Boston returned **LSTAT, RM, PTRATIO** as the top 3 - not just LSTAT/RM from the Lee textbook's 2-feature example. **PTRATIO** = pupil-teacher ratio by town district (the third correlate reflects the *suburb*, where LSTAT and RM reflect the *house/household*). His degree-2 polynomial model on those three features scored **R² ≈ 0.79-0.80** in the PySpark walkthrough - use that as your own Activity 1 benchmark.

---

## Where this module fits

- **Module 6** built classifiers → **Module 7** scored and selected them → **Module 8** adds **regression** (predict a number) and **logistic regression** (predict a probability), then McCormick reminds you that none of it counts until it is **deployed** and changes a decision.
- **The arc:** business-collected data → previously unknown relationship → model → **score new data** → **act**. Ch6 and Ch7 are the two model shapes; McCormick is the reason they exist.
- **Feeds Assessment 2** (due **26/07/2026**): logistic regression is a legitimate probability-output comparison model for churn, and Ch7's scikit-learn evaluation code is directly reusable now that PySpark is optional.
- **Week 8 carries A2's due date** - the delivery schedule puts Assessment 2 (30%, source code + report) at the end of this module.
