# Module 8 - Class Notes (Week 8 live session)

Extracted from `MLN601 - Machine Learning - Lecturer Week 1 - Week 12.docx` (Teams transcript, week 8 segment).
Facilitator: Dr Kamran Shaukat.

> **Shape of the session:** ~20 min Assessment 2 recap → ~25 min logistic regression lecture →
> breakout rooms for individual A2 progress checks. The LR lecture is **conceptual and shallow on maths**
> ("we are not going into the math of that one") - the graded depth is *implementation + comparison*, not derivation.

---

## 1. What he actually said about logistic regression

### Definition (his framing, almost verbatim)
> *"Logistic regression is a supervised machine learning algorithm used for classification problems.
> Unlike linear regression, which predicts continuous values, it predicts the **probability** that an input
> belongs to a specific class."*

- **Don't be confused by the word "regression" in the name** - he said this three separate times. Expect it as a knowledge-check / exam gotcha.
- It uses the **sigmoid** to convert the input into a probability between 0 and 1.
- Wine example used explicitly: *"whether the wine quality is bad or good"* - he anchors the whole lecture to Assessment 2.

### Two types
| Type | When | Categories |
|---|---|---|
| **Binomial** LR | dependent variable has **2** possible categories | yes/no, COVID/not-COVID, low/high quality |
| **Multinomial** LR | **3 or more *unordered*** categories | rainy/windy/cloudy/sunny; cat/dog/sheep |

- **"Unordered" matters:** grades (HD / D / C / P / F) *are* ordered; weather and animals are not. He drew that line deliberately.

### Assumptions he named
1. **Independence** - each data point should be independent of the others.
2. **Binary dependent variable** - target takes two values (1/0, high/low, legitimate/fraudulent).

---

## 2. Sigmoid vs softmax - the live class exercise ⭐

He stopped the lecture and made the room search and answer this. **You were called on twice.**

| | **Sigmoid** | **Softmax** |
|---|---|---|
| Use for | **binary** classification (2 outcomes) | **multi-class** (3+ outcomes) |
| Output | a single number in (0, 1), read as a probability | a probability distribution across classes (sums to 1) |
| Examples he gave | COVID vs not-COVID · rainy vs not-rainy · share price up vs down · low vs high wine quality | rainy/windy/cloudy/sunny · cat/dog/bird · HD/D/C/P/F grades |

**Your answer** ("sigmoid for binary classification or multi-label task, softmax for multi-class") was marked
**correct with a caveat** - he said the last line of your sigmoid definition drifted into softmax territory.
Clean version to memorise: *sigmoid = one probability for one binary question; softmax = a normalised
distribution over mutually exclusive classes.*

**Trap he set:** "share price will go **high or low**" → sigmoid (binary). But **share *price* itself** →
**neither** - that is a continuous target, so it is **regression**, not classification at all.

---

## 3. Limitations of LR (crowd-sourced in class - your contributions included)

- Struggles with **non-linear relationships**; assumes a **linear decision boundary**.
- **Sensitive to outliers.** ← he singled this out as an important point and said the course has *not* covered outliers, and that he would **add content on outliers and on market-basket analysis** to the subject.
- Tends to **overfit when there are many features but few observations**.
- **Cannot handle missing values directly** - you must impute first.

## 4. "There is no best model" - his repeated theme

> *"There is no such good, best, better model based on each of the dataset. You have to try multiple models
> and then you can say, okay, this one is performing good or bad."*

- Performance claims are only valid **on one dataset, with the same train/test split**.
- You may *assume* a model will struggle (LR on highly non-linear data) but **you cannot guarantee it**.
- Even *within* one algorithm, hyperparameters change everything (SVM linear vs RBF kernel).
- **After SMOTE**, expect *some* models to jump 5-6% (those that handled imbalance badly) and others only 2-3%. Not uniform - and that variation is itself worth commenting on.

---

## 5. Hyperparameters - what he wants you to tune

He is narrower than the readings: **`penalty` and `C`, nothing else.**

> *"You just need to change this penalty attribute - L1, L2, default is L2 - or maybe you can work with
> this C value. 1.0, 0.5, 0.2, 0.5, 0.8 ... and then see whether you have any improvement or not."*

- For your dataset he expects **no other hyperparameter to have significant impact**.
- **⚠️ Version caution:** if you use L1 you must pair it with a compatible solver (`liblinear` or `saga` - `lbfgs` is L2/none only). Also note the `penalty` argument is **deprecated from sklearn 1.8** in favour of `l1_ratio`; if your environment is on 1.8+, express L1/L2 through `l1_ratio` (0 = L2, 1 = L1) rather than `penalty`. Check the version before quoting his exact snippet.

**How to find hyperparameters (his method):** search the model name → open the first scikit-learn link → every hyperparameter and its possible values is listed there → drop them into your `param_grid`.

---

## 6. Assessment 2 recap (from the first 20 minutes)

Mostly a re-statement of the Week 7 spec, but confirming:

- **Binarise `quality`**: he stated it twice with slightly different wording - once as "0-6 low, above 6 high", then as "**less than 6 is low, greater than or equal to 6 is high**". ⚠️ The Week 7 dictation (see [module07_notes-class.md](../module-07-automated-explainable-ml/module07_notes-class.md)) is the authoritative one: **`< 6` → 1 (bad)**, **`>= 6` → 0 (good)**.
- **CRISP-DM** structure is mandatory.
- **Data understanding**: he called out that students missed the **seaborn pair plot** last time - do more visualisation.
- **Modelling**: implement **5 or more models** (KNN, LR, SVM, Gaussian/Multinomial/Bernoulli/Complement Naive Bayes, decision tree, ANN). *"Only the difference is the import and the object creation - the rest is 100% the same."*
- **SMOTE** for imbalance (over- vs under-sampling; SMOTE is the one he showed).
- **5-fold cross-validation** + **GridSearchCV**.
- **Explainable AI** - one or two graphs, clearly labelled as XAI.
- **Comparison table** of all models across metrics - he named this as what he looks for.
- **Deployment section**: students under-wrote it. Say what went wrong, what went right, how you would improve it.
- **Presentation**: 7-10 min screen recording, webcam on, state your name + show student ID at the start. Deliverables = `.ipynb` + PDF + TXT + MP4. If the MP4 is too large, host it on OneDrive/Drive/YouTube and **make it publicly accessible** (no access-request friction for the marker).

---

## What this changes in the module notes

1. **"The one dial is `C`"** needs softening → the lecturer wants **`penalty` *and* `C`**. Covered in [module08_notes.md](module08_notes.md) resources 4 & 8, but he elevates `penalty` to co-equal.
2. **Softmax was "flagged but out of scope"** in the readings (resource 2) - the lecturer made it a **live assessed discussion point**. Promote it.
3. **Outlier sensitivity** is not in any of the eight readings, and he flagged it as a gap he intends to fill. Worth knowing before Assessment 3.
4. **"No best model"** is the framing for the A2 comparison table - it is the *reason* you implement five models, not just a requirement to satisfy.
