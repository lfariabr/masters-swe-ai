# MLN601 A2 - Single Walkthrough (v4)

One file, three uses: (1) study review, (2) rehearsal, (3) the thing next to the camera while
you scroll `MLN601FariaLuisBrief2v4.ipynb` on video. Replaces the old script + cues + cue card.

Target: 8:30-9:30. Webcam and notebook visible together. Glance at a cue, look back at the
notebook, say it in your own words. Do NOT read prose.

## The story spine (say it as ONE sentence if you blank)

> **6,497 raw -> 1,177 duplicates removed -> 5,320 unique -> zero train/test overlap ->
> SVM 0.824 ranks best -> required tree 0.793 -> balanced tree recovers recall 0.59 -> 0.73**

## The numbers box (pause after each)

> **0.824** SVM RBF (AUC leader) | **0.813** LogReg | **0.793** tuned tree | **0.792** balanced tree
> **0.787** SMOTE tree | **0.736** NB | **0.657** default tree | **0.500** baseline
> recall low: **0.588** tuned -> **0.734** balanced (FN 164 -> 106; FP 114 -> 183)
> **63/37** imbalance | split **4,256 / 1,064** | tree: **gini, depth 5, leaf 20** | alcohol **0.58**
> kernels (CV): **rbf 0.826 > linear 0.804 > poly 0.795 > sigmoid 0.703**

---

## Walkthrough - segment by segment

### 0. Introduction and A1 to A2 (0:50) - screen: title cell (nb cell 0)

Cues: name + ID | same wine data, new question | regression "how far off" -> classification
"which side of the line" | promise: six CRISP-DM stages, two defensible recommendations.

Spoken anchor: "In Assessment 1 I predicted the numerical score; here the same data becomes a
binary question: should this wine be flagged as likely low quality? That changes the target,
the models and, most importantly, what an error means."

### 1. Business Understanding (0:45) - screen: Section 1 (nb cell 1)

Cues: low-cost screen for expert tasting | quality <6 = low = positive class (the event we ACT
on) | false negative = weak wine shipped unflagged | decision support, not automated rejection.

### 2. Data Understanding (1:10) - screen: balance, heatmap, pairplot (nb cells 8-12)

Cues: 6,497 raw red+white, wine_type kept | audit found **1,177 exact duplicates** -> **5,320
unique** | balance ~**63% high / 37% low** -> accuracy alone flatters | heatmap: alcohol +
volatile acidity are the signals, sulphur features correlate | pairplot: heavy class overlap ->
motivates testing a nonlinear kernel later.

Transition: "That duplicate finding directly changed my preparation step."

### 3. Data Preparation (1:00) - screen: dedup + split + leakage cells (nb cells 9, 14-15)

Cues: duplicate leakage = identical row in train and test = part of the exam seen in advance
(risk also existed in A1; the stricter A2 audit caught it) | dedup BEFORE split -> **zero
overlap** | drop quality columns from features | stratified 80/20: **4,256 / 1,064** | scaler
AND SMOTE live inside Pipelines -> each CV fold learns only from its own training portion.

Transition: "With a genuinely unseen test set, I could tune the required tree honestly."

### 4. Modelling (1:30) - screen: baseline + grid + params (nb cells 16-19)

Cues: required model = Decision Tree | Gini: 0 pure, 0.5 max mix; splits reduce weighted
impurity | GridSearchCV 5-fold, scoring roc_auc -> **gini, depth 5, leaf 20** | why pruning:
unconstrained tree memorises | two controlled imbalance experiments: **balanced** (same
structure, minority mistakes cost more) and **SMOTE** (synthetic minority rows inside training
folds only) | SVM: widest-margin boundary around support vectors; C = violation penalty;
kernel trick = nonlinear boundary without building the higher dimension; gamma = how local RBF is.

Delivery check: keep the SVM explanation under 40 seconds.

### 5. Evaluation (2:45) - screen: report, comparison table, ROC, importance (nb cells 20-28)

Definitions in one breath each: precision = of the flagged, how many truly low; recall/
sensitivity = of the truly low, how many caught (3 of 10 = 30%); specificity = truly high
correctly cleared; balanced accuracy = mean of the two sides; G-mean punishes a weak side.

The three beats, in order:

1. **Required tree:** AUC **0.793**, catches **234 of 398** low wines -> recall **0.588**,
   specificity 0.829. Good ranking, weak catch rate at the default threshold.
2. **The lever:** balanced tree catches **292** -> recall **0.734**, F1 0.669, balanced
   accuracy 0.729. Not free: false alarms 114 -> **183**, specificity falls to 0.725. PAUSE
   here and name the trade: 58 fewer weak batches shipped, ~70 extra unnecessary tastings.
   SMOTE reaches recall 0.709 / AUC 0.787 - helps, but simple class weighting beats it, so I
   keep class weighting.
3. **The ranking winner:** RBF SVM AUC **0.824** - ranks a random low wine above a random high
   wine ~82% of the time - yet its default-threshold recall is only 0.590. Two winners, no
   contradiction: **AUC judges the ranking across all thresholds; recall judges one chosen
   operating point.** SVM = technical winner; balanced tree = operational screening winner
   (catches more, rules can be inspected).

Kernel line (the tested hypothesis): "linear kernel already reaches 0.804, so the boundary is
mostly linear - but RBF finds a further 0.02 of nonlinear structure the tree alone missed."

Importance: alcohol **0.58**, volatile acidity next.

### 6. Deployment and lessons (1:00) - screen: Section 6 (nb cell 29) - slow down, reflective

Cues: deploy the balanced tree as the interpretable screening policy, threshold set against
real costs | validate on another producer or period; monitor red and white separately | lesson
1: sophisticated is not automatically better - SMOTE helped, class weighting was simpler and
stronger | lesson 2: "best model" is incomplete until you name the objective and the threshold.

### 7. Close (0:20) - camera

"Assessment 1 taught me to measure how wrong a numerical prediction is. Assessment 2 taught me
to separate classes, inspect the errors, and choose which errors matter most. Thank you."

---

## Technical cheat sheet (understand, never read verbatim)

- **Score vs decision vs metric:** the model outputs a probability per wine (the score); the
  threshold turns score into a 0/1 decision (flag or clear); recall/precision/F1 grade the
  decisions, AUC grades the scores. Move the threshold and the first three change; AUC does not.
- **AUC as pairs:** all (real low, real high) pairs in the test set = 398 x 666 = **265,068
  duels**. AUC 0.793 = the low wine got the higher suspicion score in ~79% of them.
- **Duplicate leakage:** identical row in train and test = exam seen in advance; inflates any
  metric (RMSE in A1, AUC here).
- **Gini impurity:** how mixed a node is; 0 = pure, 0.5 = 50/50. Splits chosen to reduce it.
- **NB, broken assumption intact ranking:** correlated features double-count evidence, so the
  probabilities are wrong but the winner of each pair usually is not; that is why AUC survives.

## Recording method (the anti-stiffness part)

1. Talk to ONE person (a colleague at the warehouse), not to "the audience".
2. Describe what you SEE - scroll, point at the plot, "here you can see". Eyes on the screen,
   not on text: that is what kills the reading voice.
3. Warm-up take per block: say it once with NOTHING in front of you, then record the second
   telling - always looser.
4. Flubbed a phrase? Keep going. Only redo a block if you lost the thread.
5. Pause AFTER every number. One breath. Reads as confidence.
6. Smile at the open and the close.

### Record in 4 blocks, then join

| Block | Segments | ~Time |
|---|---|---|
| A | 0 + 1 (intro + business) | 1:35 |
| B | 2 + 3 (data + prep, the DUPLICATE catch) | 2:10 |
| C | 4 + 5 (modelling + evaluation, the LEVER beat) | 4:15 |
| D | 6 + 7 (lessons + close) | 1:20 |

### Three-pass rehearsal

1. Navigation pass: scroll every stop without speaking.
2. Cue pass: explain each segment from the cues, no full sentences.
3. Timed pass: record once, no restarts for minor wording.

### Pre-flight

- [ ] v4 notebook open at the top, font zoomed for video
- [ ] Webcam picture-in-picture ON, audio checked
- [ ] Only THIS file next to the camera
- [ ] Rehearsed out loud: score/threshold/AUC three layers + "broken assumption, intact ranking"
- [ ] File: `MLN601FariaLuisBrief2.mp4`
