# MLN601 Assessment 2 - Video Presentation Script v4

Target: 8:30-9:30. Use this to rehearse the argument, not as text to read verbatim.

## Time map

| Segment | Time | Screen |
|---|---:|---|
| Introduction and A1 to A2 | 0:50 | Title |
| Business Understanding | 0:45 | Section 1 |
| Data Understanding | 1:10 | Balance, heatmap, pairplot |
| Data Preparation | 1:00 | Split and leakage checks |
| Modelling | 1:30 | Tree, SMOTE and SVM searches |
| Evaluation | 2:45 | Metrics, confusion matrices, ROC, trade-offs |
| Deployment and reflection | 1:00 | Section 6 |
| Close | 0:20 | Camera |
| **Total** | **~9:20** | |

## 0. Introduction and A1 to A2

> Show the title. Start looking at the camera, then point to the task definition.

"Hi, my name is Luis Faria, and this is my Assessment 2 for MLN601. In Assessment 1 I used
regression to predict the numerical wine quality score. Here the same data becomes a binary
classification problem: should a wine be flagged as likely low quality? That changes the target,
the models and, most importantly, what an error means. I will follow the six CRISP-DM stages and
finish with two different but defensible model recommendations."

## 1. Business Understanding

> Point to `low = 1` and explain why the encoding is intentional.

"The purpose is a low-cost screen that prioritises batches for expert tasting. Following the
brief, quality below 6 is low and quality 6 or above is high. I made low quality the positive
class because that is the event requiring action. A false negative is therefore a genuinely weak
wine that the model fails to flag. This remains decision support, not automated rejection."

## 2. Data Understanding

> Show class balance, heatmap and pairplot. Give one sentence per visual.

"I combined the red and white datasets into 6,497 raw rows and retained wine type as a feature.
The quality audit found 1,177 exact duplicates, leaving 5,320 unique wines. The final target is
about 63 percent high and 37 percent low, so accuracy alone can flatter a model.

The heatmap identifies alcohol and volatile acidity as useful signals and also shows correlated
features. The pairplot shows substantial overlap between classes. That overlap explains why a
single straight boundary or one feature cannot classify every wine correctly, and it motivates
testing a nonlinear kernel later."

## 3. Data Preparation

> Point to deduplication, `stratify`, leakage columns and the zero-overlap assertion.

"I removed duplicates before splitting. Otherwise an identical wine could appear in both the
training and test sets, which is equivalent to seeing part of the exam in advance. I removed the
original quality score from the predictors, used an 80/20 stratified split, and confirmed zero
exact overlap between 4,256 training and 1,064 test rows.

Scaling and SMOTE both sit inside Pipelines. This means each cross-validation fold learns its
scaler and creates synthetic examples from its own training portion only. The final test set keeps
its natural distribution."

## 4. Modelling

> Show the modelling cell and selected parameters. Do not enumerate every grid value.

"The required model is the Decision Tree. Gini impurity tells the tree how mixed a node is: zero
is pure, and for two equally represented classes it reaches 0.5. The tree chooses splits that
reduce weighted impurity. GridSearchCV selected a Gini tree with depth 5 and minimum leaf size 20,
scored by ROC-AUC.

I then ran two controlled imbalance experiments. The balanced tree kept exactly the same structure
but made minority-class mistakes more expensive. The SMOTE Pipeline kept the structure fixed and
created minority examples only inside training folds.

Finally, I compared SVM kernels. An SVM builds a boundary with the widest useful margin around its
closest points, called support vectors. C controls the penalty for violations. The kernel trick
allows a nonlinear boundary without explicitly constructing every higher-dimensional feature, and
gamma controls how local the RBF influence is."

## 5. Evaluation

> Lead with the confusion matrices, then show the operating-point bars, then ROC.

"I treat low quality as positive throughout. Precision asks how many low-quality flags are correct.
Recall, or sensitivity, asks how many genuinely low wines are caught. For example, catching 3 out
of 10 gives 30 percent recall. Specificity asks how many genuinely high wines are correctly cleared.
Balanced accuracy averages sensitivity and specificity, while G-mean penalises a model if either
side is weak.

The AUC-tuned tree reaches AUC 0.793. At its default threshold it catches 234 of 398 low wines, so
recall is 0.588, while specificity is 0.829.

The balanced tree catches 292 low wines. Recall rises to 0.734, F1 to 0.669 and balanced accuracy
to 0.729. But this is not free: false alarms increase from 114 to 183, and specificity falls to
0.725. That is the exact business trade-off created by prioritising weak-batch detection.

SMOTE reaches recall 0.709 and AUC 0.787. It helps compared with the AUC tree, but does not beat
simple class weighting on recall, F1 or balanced accuracy. I would therefore keep class weighting.

The ROC curve asks a different question across every possible threshold. The RBF SVM, with C equal
to 1 and gamma set to scale, has the highest AUC at 0.824. In plain English, it ranks a random low
wine above a random high wine about 82 percent of the time. Yet its default-threshold recall is
only 0.590.

So I have two winners. The RBF SVM is the technical ranking winner. The balanced Decision Tree is
the operational screening winner because it catches more weak wines and its rules can be inspected.
There is no contradiction: AUC evaluates ranking across thresholds, while recall evaluates one
chosen operating point."

## 6. Deployment and lessons learned

> Slow down and make this sound reflective.

"For deployment I would choose the balanced tree as the interpretable screening policy, but only
after setting the threshold against the real costs of a missed weak batch and an unnecessary
tasting. I would validate it on wines from another producer or time period and monitor red and
white wines separately.

The main lesson is that more sophisticated preprocessing is not automatically better: SMOTE helped,
but class weighting was simpler and slightly stronger here. The other lesson is that the phrase
'best model' is incomplete until we specify the business objective and the operating threshold."

## 7. Close

"Assessment 1 taught me to measure how wrong a numerical prediction is. Assessment 2 taught me to
separate classes, inspect the errors, and choose which errors matter most. Thank you."

## Recording checks

- Webcam and notebook visible together.
- Explain the charts instead of reading their titles.
- Pause after `0.588 -> 0.734` and explain the false-alarm cost.
- Keep the SVM explanation below 40 seconds.
- Finish between 8:30 and 9:30.
