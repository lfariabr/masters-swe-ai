# A2 Video - Cue Card v4

Keep this beside the camera. Keep the full script closed while recording.

## Story spine

> **6,497 raw -> 1,177 duplicates removed -> 5,320 unique -> zero overlap ->
> AUC tree ranks well -> balanced tree catches more low wines -> RBF SVM ranks best**

## Numbers worth pausing on

- Split: **4,256 train / 1,064 test**; class balance **63/37**.
- AUC tree: **AUC 0.793**, recall **0.588**, specificity **0.829**.
- Balanced tree: **AUC 0.792**, recall **0.734**, specificity **0.725**.
- Operational trade-off: **58 more low wines caught, 69 more false alarms**.
- SMOTE: recall **0.709**, AUC **0.787** - helpful, but class weighting wins.
- RBF SVM: **AUC 0.824**, recall **0.590**, specificity **0.865**.
- Tree parameters: **Gini, depth 5, minimum leaf 20**.

## One-line explanations

- Recall: "Of every genuinely low wine, how many did I catch?"
- Specificity: "Of every genuinely high wine, how many did I clear?"
- AUC: "Across thresholds, how well does the model rank low risk above high?"
- Gini: "How mixed is this tree node?"
- SVM: "Find a wide-margin boundary around the closest support vectors."
- Kernel trick: "Permit nonlinear separation through implicit higher-dimensional similarity."
- SMOTE: "Create synthetic minority examples inside training folds only."

## The conclusion

> **RBF SVM wins ranking. Balanced Decision Tree wins low-quality screening and
> interpretability. Best depends on the cost of false negatives and false positives.**

## Anti-stiffness rules

1. Explain what the current chart shows. Do not recite definitions before showing it.
2. Look at the camera for the conclusion, not at the script.
3. Pause after `0.588 -> 0.734`; then explain the 69 additional false alarms.
4. If wording changes but meaning survives, continue recording.
5. Keep SVM theory below 40 seconds.

## Pre-flight

- [ ] v4 notebook open and zoomed.
- [ ] Webcam picture-in-picture and clean audio.
- [ ] Confusion matrices -> trade-off bars -> ROC navigation rehearsed.
- [ ] Finish between 8:30 and 9:30.
- [ ] Output file: `MLN601FariaLuisBrief2.mp4`.
