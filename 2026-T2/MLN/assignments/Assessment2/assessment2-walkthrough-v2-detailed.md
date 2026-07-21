# MLN601 Assessment 2 - Recording Walkthrough v5 (for notebook v8)

Video: ENGLISH, 7-10 min, filename `MLN601FariaLuisBrief2.mp4`.

This version replaces the previous walkthrough. The central story is now the controlled
comparison of model families and imbalance treatments. Read each printed conclusion, add one
sentence about why it matters to the wine-lot operation, then move on.

## Ground rules

- Show the student card and state name, student number, subject and assessment at the start.
- Record the executed notebook, not slides.
- If a block runs 15 seconds over, shorten commentary but keep the key result.
- Say clearly: class 1 means low quality and is the positive class.
- Say clearly: the test set was never resampled or used during model selection.
- Pronounce: **Gini** = "JEE-nee"; **SMOTE** = "smote"; **AUC** = "A-U-C".
- Do not list every hyperparameter. Explain the experiment and show the selected values.

## Fact traps

- Raw data: 6,497 samples.
- Exact duplicates removed: 1,177.
- Modelling data: 5,320 rows.
- Training and test: 4,256 and 1,064 rows.
- Class balance: 62.6% high quality and 37.4% low quality.
- Approved model: Random Forest with class weighting.
- CV approved metrics: AUC 0.835, sensitivity 0.748, specificity 0.766, balanced accuracy 0.757.
- Test approved metrics: AUC 0.834, sensitivity 0.714, specificity 0.806, balanced accuracy 0.760.
- Test confusion matrix: 284 low-quality lots caught, 114 missed, 129 false alarms, 537 correctly cleared.
- Average SMOTE movement: sensitivity +0.154, specificity -0.104, AUC approximately unchanged.

## Block 0 - Identity and title (cells 0-1) | 0:00-0:35

Suggested wording:

"Hello, my name is Luis Faria. This is MLN601 Assessment 2. I will present an operational
screening system for wine bottling lots. The notebook follows CRISP-DM and compares nine model
families under original, SMOTE and class-weighted training conditions."

Show the student card briefly, then scroll to Business Understanding.

## Block 1 - Business Understanding (cells 2-3) | 0:35-1:15

Suggested wording:

"One row represents one laboratory sample treated as one bottling lot. The model does not
release or reject wine. It flags lots for extra tasting by quality-control staff. Missing a weak
lot is more costly than reviewing an acceptable one, but a model that flags everything is also
not useful. I therefore declared three cross-validation gates before modelling: AUC, sensitivity
and specificity must each be at least 0.75, 0.70 and 0.70 respectively."

Transition: "I will now show the data and the controls used before any model was trained."

## Block 2 - Data Understanding (cells 4-23) | 1:15-2:20

Suggested wording:

"The source contains 6,497 red and white wine samples with eleven physicochemical measurements.
I added wine type as a predictor. The reproducibility cell pins the runtime and random state.
The quality audit found no schema, missing-value or range failures. The IQR review flagged 1,473
unusual rows, but these remained because they are plausible wines rather than confirmed errors.

I removed 1,177 exact duplicates before splitting, leaving 5,320 independent rows. Quality below
six is low quality, class 1 and the positive review class. The final balance is 62.6% high and
37.4% low. Free and total sulphur dioxide have a positive correlation of 0.72. Alcohol has the
strongest target relationship at minus 0.41, so higher alcohol is associated with lower modelled
risk. The pair plot also shows substantial class overlap, which is why no single measurement is
enough for screening."

Transition: "The next step prevents leakage and keeps the test partition untouched."

## Block 3 - Data Preparation (cells 24-26) | 2:20-2:55

Suggested wording:

"Target columns are excluded from predictors and the data is split once using stratification:
4,256 training rows and 1,064 test rows, with zero overlap. Scaling, median binarisation and SMOTE
are fitted inside each cross-validation fold. This means validation rows do not influence
preprocessing or synthetic samples. Most importantly, the test set remains outside every search
and is never resampled."

Optional transparent clarification:

"I answered this incorrectly in our conversation. After checking the implementation, the exact
answer is that only training folds are resampled. The held-out test data is never resampled."

Transition: "With that boundary fixed, I can compare treatments fairly."

## Block 4 - Candidate matrix and rationale (cells 27-29) | 2:55-3:40

Suggested wording:

"The matrix contains nine model families plus a majority baseline. Logistic Regression tests an
interpretable linear boundary. KNN tests local similarity but is sensitive to scaling and twelve
dimensions. Decision Tree tests readable rules, while SVM tests maximum-margin boundaries.
Gaussian, Bernoulli, Multinomial and Complement Naive Bayes test different distributional
assumptions. Bernoulli uses fold-fitted median binarisation, while Multinomial and Complement use
MinMax scaling because they require non-negative inputs. Random Forest is the ensemble candidate:
it averages 200 trees to reduce the variance of a single tree, at the cost of direct readability."

Point at the pipeline definitions and five-fold StratifiedKFold. Mention that the grids are light
and use ROC-AUC consistently.

## Block 5 - Three experiments (cells 30-35) | 3:40-4:35

Suggested wording:

"Experiment A trains all nine families on the original distribution. This is the untreated
reference and shows what each model can do without an imbalance intervention.

Experiment B repeats the same models and grids with SMOTE inside the training part of each fold.
The flow is fold training data, preprocessing, SMOTE, classifier, then untouched fold validation.
The held-out test set remains outside this process.

Experiment C uses class weighting for Logistic Regression, SVM, Decision Tree and Random Forest.
Unlike SMOTE, weighting creates no synthetic observations. It changes the penalty assigned to
classification errors. The three arms therefore isolate model choice from treatment choice."

Transition: "The important question is not whether a technique sounds useful, but what movement
it causes in the same metrics."

## Block 6 - Comparison, gates and ablation (cells 36-43) | 4:35-6:05

Suggested wording:

"Table 4.5 is the master comparison. It contains 22 tuned model-treatment combinations plus the
majority baseline, all measured on the same five folds. The delta table and scatter plot show the
main trade-off. Across the nine families, SMOTE increases sensitivity by about 0.154 and reduces
specificity by about 0.104, while average AUC is nearly unchanged. So SMOTE mostly changes the
operating point. It catches more weak lots, but sends more acceptable lots to review.

Class weighting creates a similar cost-sensitive effect without generating synthetic wines.
Random Forest also improves stability by averaging trees. In this run its weighted version
reaches 0.835 AUC, 0.748 sensitivity, 0.766 specificity and 0.757 balanced accuracy.

The gates are applied without reading the test set. Among passing candidates, I select the
highest balanced accuracy. Differences below 0.01 are treated as a technical tie and resolved by
interpretability. This freezes four roles: best untreated, best SMOTE, best weighted and best
ensemble. Duplicate roles are evaluated only once. Random Forest with class weighting is the
approved model.

The sulphur feature ablation was then applied to that approved family using training CV only. The
gain was 0.0013, below the pre-declared 0.01 rule, so the engineered features were rejected. A
negative result is useful because it avoids extra production complexity without measurable gain."

Transition: "Only now do I open the test set, once, for the frozen finalists."

## Block 7 - Held-out evaluation (cells 44-49) | 6:05-7:05

Suggested wording:

"The unique finalists are SVM on the original distribution, SVM with SMOTE and weighted Random
Forest. On the untouched test set, the approved forest achieves AUC 0.834, sensitivity 0.714,
specificity 0.806 and balanced accuracy 0.760. These values are close to cross-validation.

The confusion matrix translates this into operations. Of 398 low-quality lots, 284 are caught and
114 are missed. There are 129 false alarms among acceptable lots, while 537 are correctly cleared.
The untreated SVM has high specificity but misses too many weak lots. SMOTE improves sensitivity
but accepts more false alarms. The weighted forest provides the strongest balance under the
declared gates."

Point at the ROC curves and confusion matrices. Do not read every table row.

Transition: "Performance explains what was selected. SHAP explains how the approved model reaches
its scores."

## Block 8 - Explainable AI and approval (cells 50-60) | 7:05-8:25

Suggested wording:

"Because the approved model is tree based, I use TreeExplainer on a fixed sample of 500 held-out
rows. The maximum additivity error is approximately three times ten to the minus fifteen, so the
feature contributions reconstruct the class-1 score at machine precision.

Globally, alcohol is the most influential feature, followed by volatile acidity and density. The
beeswarm adds direction: lower alcohol tends to push predictions toward low quality, consistent
with the earlier exploratory result. This is an association learned by the model, not a causal
claim.

For a correctly flagged example, the predicted low-quality probability is 0.719. Alcohol at 9.4
adds about 0.148 toward low-quality risk, with volatile acidity and density also contributing.
This gives quality-control staff a concrete reason to inspect the laboratory record while keeping
the final decision human supervised.

The approval table documents the result for every finalist. Weighted Random Forest is approved
for a shadow pilot. The alternatives remain useful benchmarks, but they do not provide the same
balance at the default threshold."

Transition: "I will finish with what changed in my understanding and what still needs production
evidence."

## Block 9 - Lessons, deployment and close (cells 61-69) | 8:25-9:30

Suggested wording:

"What went well was moving from one preferred model to a controlled matrix. The baseline, common
folds and declared gates made the result measurable, and the A1 feedback helped me make the
business context and chart interpretations explicit.

The main challenge was moving from regression thinking to classification. AUC, sensitivity,
specificity, precision, thresholds and confusion-matrix counts can move in different directions.
SMOTE, weighting and ensemble learning also address different problems, which is why comparing
them directly was important.

The next step is to estimate the real cost of missed weak lots and unnecessary holds, then
calibrate the threshold. A shadow pilot should monitor drift, calibration, hold rate, escapes and
red-versus-white performance. The Sommelier API currently serves the earlier balanced tree, so
aligning it with this approved weighted forest is a documented deployment backlog item rather
than something I claim is already complete.

In conclusion, this assessment recommends a class-weighted Random Forest for human-supervised
wine-lot triage. It was selected through training-only cross-validation, confirmed once on an
untouched test set and explained globally and per lot. Thank you."

## Rehearsal sequence

1. Scroll the v8 notebook once and confirm every cell range.
2. Rehearse the three experiment definitions without looking at the script.
3. Say the fact traps aloud five times.
4. Practise the test-set correction once in a neutral, factual tone.
5. Do one audio-only take with a stopwatch and target 9:15 to 9:30.
6. Record the screen, webcam and student card. Restart a block if needed and edit later.
