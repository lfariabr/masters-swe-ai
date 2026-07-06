# MLN601 Assessment 2 - Recording Cue Sheet v4

Glance, look back at the notebook, explain. Do not read complete sentences.

## Technical anchors

- Positive class: `low (<6) = 1` because low wine requires action.
- Gini: node mixing, `1 - sum(p_k^2)`; lower weighted impurity is better.
- Precision: correct low flags / all low flags.
- Recall or sensitivity: caught low wines / all actual low wines.
- Specificity: cleared high wines / all actual high wines.
- F1: harmonic balance of precision and recall.
- Balanced accuracy: average of sensitivity and specificity.
- G-mean: geometric balance; one weak side pulls it down.
- ROC: sensitivity versus false-positive rate across thresholds.
- AUC: ranking quality; 0.5 random, 1.0 perfect.
- SVM margin: separation around the closest support vectors.
- `C`: penalty for margin violations. Higher C penalises errors more.
- Kernel trick: nonlinear separation through implicit higher-dimensional similarity.
- `gamma`: locality of RBF influence.
- SMOTE: synthetic minority training examples, never test examples.

## Navigation and numbers

### Opening - 40 sec

- A1 regression -> A2 binary classification.
- Six CRISP-DM stages.
- Two winners for two objectives.

### Business - 40 sec

- Screen for expert review.
- `<6 low/positive`, `>=6 high`.
- False negative = weak wine missed.
- Human decision support.

### Data - 70 sec

- 6,497 raw -> remove 1,177 duplicates -> 5,320 unique.
- 63% high / 37% low.
- Heatmap: alcohol, volatile acidity, correlated features.
- Pairplot overlap -> imperfect separation + nonlinear test justified.

### Preparation - 55 sec

- Deduplicate before split.
- Remove original quality score.
- Stratified 80/20: 4,256 train / 1,064 test.
- Zero exact overlap.
- Scaler and SMOTE inside folds only.

### Modelling - 80 sec

- Required Decision Tree.
- AUC tree: Gini, depth 5, leaf 20.
- Balanced tree: same structure, only class cost changes.
- SMOTE: same structure, synthetic train examples.
- SVM: support vectors, margin, C, kernel, gamma.
- RBF wins kernel CV.

### Evaluation - 2:30

- Start with confusion matrix language.
- AUC tree: TP 234, FN 164, FP 114, TN 552.
- Recall 0.588, specificity 0.829, AUC 0.793.
- Balanced tree: TP 292, FN 106, FP 183, TN 483.
- Recall 0.734, specificity 0.725, F1 0.669, balanced accuracy 0.729.
- Message: catch 58 more low wines, but create 69 more false alarms.
- SMOTE: recall 0.709, AUC 0.787 -> helps, class weighting still wins.
- RBF SVM: AUC 0.824, recall 0.590, specificity 0.865.
- Two winners:
  - RBF SVM = best ranking.
  - Balanced tree = best recall + interpretability.
- AUC and recall do not contradict each other.

### Deployment - 50 sec

- Prefer balanced tree for screening, conditional on business costs.
- Tune threshold, externally validate, monitor wine type.
- SMOTE not automatically better.
- "Best" requires an objective and threshold.

### Close - 20 sec

- A1: size of numerical error.
- A2: class separation + which errors matter.

## Three rehearsal passes

1. Navigation only - reach each visual without searching.
2. Explain from cues - no full script.
3. Timed recording - continue through small wording mistakes.
