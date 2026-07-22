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

Cell-by-cell wording (cells 36, 39 and 41 are markdown titles only, no separate line - read
them silently and move straight to the code cell below each):

**Cell 37 (code -> Table 4.5, Table 4.6):**

"Table 4.5 is the master comparison. It contains 22 tuned model-treatment combinations plus the
majority baseline, all measured on the same five folds. Table 4.6 shows treatment deltas against
each untreated model.

Class weighting creates a cost-sensitive effect without generating synthetic wines. Random Forest
also improves stability by averaging trees. In this run its weighted version reaches 0.835 AUC,
0.748 sensitivity, 0.766 specificity and 0.757 balanced accuracy - the row I will select as the
approved model two cells from now."

**Cell 38 (code -> Figure 4.1, sensitivity vs specificity scatter):**

Legend note: "SMOTE endpoint" is the legend box title, not an entry - titles have no marker, which
is why it looks blank. The real entries are the nine model names. Each colour is one model family:
the circle (no separate label) is where it starts, untreated; the X marker, listed in the legend,
is where it lands after SMOTE; the arrow shows the movement between the two.

"This scatter plot shows the main trade-off. Each colour is one model family. The circle is where
it starts, untreated. The X marker, which the legend calls the SMOTE endpoint, is where it lands
after SMOTE. The arrow shows the movement between the two. Across the nine families, SMOTE
increases sensitivity by about 0.154 and reduces specificity by about 0.104, while average AUC is
nearly unchanged. So SMOTE mostly changes the operating point. It catches more weak lots, but
sends more acceptable lots to review."

**Cell 40 (code -> Table 4.7, gates and frozen finalists):**

Table 4.7 only lists role, model and treatment - no metrics. Do not read numbers off this table;
those live in Table 4.5 from cell 37.

"The gates are applied here, before I look at the test set. For each treatment, the model with the
best balanced accuracy wins that role. That gives four finalists: best untreated, best SMOTE, best
class weighted, and best ensemble.

For the overall winner, if two models are within 0.01 of each other, I favour the more
interpretable one. Random Forest with class weighting comes out on top."

**Cell 42 (code -> Table 4.8, feature ablation):**

"The sulphur feature ablation was then applied to that approved family using training CV only. The
gain was 0.0013, below the pre-declared 0.01 rule, so the engineered features were rejected. A
negative result is useful because it avoids extra production complexity without measurable gain."

**Cell 43 (markdown -> Interpretation / findings):**

Read the printed findings on screen, then say the transition below.

Transition: "Only now do I open the test set, once, for the frozen finalists."

## Block 7 - Held-out evaluation (cells 44-49) | 6:05-7:05

**Cells 44-45 (markdown, header + intro):**

"The test set is opened now, once, only for the three unique finalists: SVM original, SVM SMOTE,
and weighted Random Forest."

**Cell 46 (code -> Table 5.1, finalist test metrics):**

"The approved forest scores AUC 0.834, sensitivity 0.714, specificity 0.806, balanced accuracy
0.760 - close to its cross-validation numbers."

**Cell 47 (code -> Figure 5.1, ROC curves):**

"The ROC curve ranks the three finalists. Random Forest sits highest, confirming it separates the
classes best overall."

**Cell 48 (code -> Figure 5.2, confusion matrices, three panels left to right: SVM original, SVM
SMOTE, weighted Random Forest):**

"These are the operating points. The untreated SVM, on the left, has high specificity but misses
too many weak lots. SMOTE, in the middle, catches more but raises false alarms. The weighted
forest, on the right, is the approved model: 284 of 398 weak lots caught, 114 missed, 129 false
alarms among acceptable lots."

**Cell 49 (code -> Table 5.2, classification report):**

"This report confirms the same result for the low-quality class specifically, not just overall
accuracy."

Transition: "Performance explains what was selected. SHAP explains how the approved model reaches
its scores."

## Block 8 - Explainable AI and approval (cells 50-60) | 7:05-8:25

**Cell 50 (markdown, 5.1 header):**

"The approved model is tree based, so I use SHAP's TreeExplainer on 500 held-out rows."

**Cell 51 (code -> printed additivity check, no table/figure number) + Cell 52 (interpretation):**

"This check confirms the feature contributions add up exactly to each prediction, at machine
precision."

**Cell 53 (code -> Table 5.3, then Figure 5.3 beeswarm, same cell) + Cell 54 (interpretation):**

"Table 5.3 ranks features by SHAP importance: alcohol first, then volatile acidity, then density.
Figure 5.3, the beeswarm plot below it, adds direction - lower alcohol pushes a lot toward low
quality. This is a pattern the model learned, not a cause-and-effect claim."

**Cell 55 (code -> Table 5.4, then Figure 5.4 waterfall, same cell) + Cell 56 (interpretation):**

"Table 5.4 and Figure 5.4, the waterfall chart, break down one flagged lot: a 0.719 chance of low
quality, with its low alcohol, 9.4, as the biggest reason why. This gives staff a concrete reason
to check that lot by hand."

**Cell 57-58 (markdown, 5.2 operational result):**

"Weighted Random Forest is the approved model, with the test results shown earlier."

**Cell 59-60 (markdown, 5.3 approval table):**

"This table records the decision for every finalist. Weighted Random Forest is approved for a
shadow pilot; the others remain benchmarks."

Transition: "I will finish with what changed in my understanding and what still needs production
evidence."

## Block 9 - Lessons, deployment and close (cells 61-69) | 8:25-9:30

**Cell 61-62 (markdown, §6 - What went well / Challenges / What can be improved):**

"Section 6 covers lessons learned. What went well: the model matrix made selection measurable
instead of assumed. The challenge was that classification needs several metrics at once, and
SMOTE, weighting and ensembles each solve a different problem. What's next: calibrate the
threshold with real costs, and run a supervised shadow pilot before any live deployment."

**Cells 63-69 (markdown, Integrity Declaration, Acknowledgement, References, Appendices A-C -
scroll through, no need to read aloud):**

"The remaining sections cover academic integrity, AI tool acknowledgement, references, the
glossary, and two appendices: the Sommelier API prototype and the proposed review pipeline."

Closing line:

"In conclusion, this assessment recommends a class-weighted Random Forest for human-supervised
wine-lot triage, selected through training-only cross-validation, confirmed once on an untouched
test set, and explained globally and per lot. Thank you."

## Rehearsal sequence

1. Scroll the v8 notebook once and confirm every cell range.
2. Rehearse the three experiment definitions without looking at the script.
3. Say the fact traps aloud five times.
4. Practise the test-set correction once in a neutral, factual tone.
5. Do one audio-only take with a stopwatch and target 9:15 to 9:30.
6. Record the screen, webcam and student card. Restart a block if needed and edit later.
