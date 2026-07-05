# MLN601 Assessment 2 - Recording Cue Sheet

Use this while recording. Do **not** read it as prose. Glance at one cue, look back at the
notebook, and explain the point in your own words. Small wording differences are fine.

Target: 8-9 minutes. Webcam and notebook visible together.

## 0. Opening - title cell (30-40 sec)

- Name, student ID, MLN601 Assessment 2.
- Same wine data as A1, new question: exact score -> high/low classification.
- Promise: six CRISP-DM stages, results, lessons learned.
- **Transition:** "So the first change is the business question itself."

## 1. Business Understanding - Section 1 (40 sec)

- Goal: low-cost screen for batches needing expert review.
- Target: quality `<6` = low/positive class; `>=6` = high.
- Decision support, not automated rejection.
- **Transition:** "Before modelling, I needed to understand what the data could actually support."

## 2. Data Understanding - balance, heatmap, pairplot (75 sec)

- Raw data: **6,497 rows**, red + white, `wine_type` flag.
- Found **1,177 exact duplicates** -> **5,320 unique rows**.
- Final balance: about **63% high / 37% low**.
- Heatmap: alcohol strongest positive signal; correlated sulphur measures.
- Pairplot: heavy overlap -> expect useful, not perfect, separation.
- **Transition:** "That duplicate finding directly changed my preparation step."

## 3. Data Preparation - split cell (60 sec)

- Duplicate leakage: identical row in train and test means the answer was partly seen.
- Previous draft: **359 test rows** had exact copies in training.
- Final v3: deduplicate first; **zero train/test overlap**.
- Stratified 80/20 split: **4,256 train / 1,064 test**.
- Remove original quality score from features; scaler only inside Logistic Pipeline.
- **Transition:** "With a genuinely unseen test set, I could tune the required tree honestly."

## 4. Modelling - grid and best parameters (75 sec)

- Required model: Decision Tree. Context only: baseline, Logistic Regression, GaussianNB.
- GridSearchCV: 5 folds, scoring = ROC AUC.
- Search: depth, leaf size, criterion, class weight.
- Winner: **gini, depth 5, min leaf 20, no class weighting**.
- Why pruning: default tree memorises detail and generalises poorly.
- **Transition:** "The held-out test set then answers whether that tuning really helped."

## 5. Evaluation - table, ROC, confusion matrix, importance (2 min)

- Tuned tree: **AUC 0.793**, baseline 0.500, default tree 0.657.
- Plain English: in about **79%** of random low/high pairs, low gets the higher risk score.
- Logistic Regression: **0.813**, 0.020 higher on this split.
- Deduplication changed tree AUC **0.809 -> 0.793**: more credible validation.
- Confusion matrix: high recall **0.83**, low recall **0.59** -> still misses weak batches.
- Importance: alcohol **0.58**, volatile acidity **0.19**.
- **Transition:** "I also tested a model built on a completely different probability assumption."

## 6. Naive Bayes - Section 5.4 and ROC (30 sec)

- Tree/Logistic = discriminative boundary; GaussianNB = generative distributions + Bayes.
- Independence assumption is violated by correlated features.
- NB AUC **0.736**: above default tree, below tuned tree and Logistic.
- Conclusion: useful despite violation, but not the best fit here.
- **Transition:** "Those results shaped the lessons I would carry into a real deployment."

## 7. Deployment / lessons - Section 6 (50 sec)

- Worked: interpretable tree, threshold-independent AUC, deduplicated validation.
- Hard: overlapping classes and low-class recall 0.59.
- Next: ensemble, business-cost threshold, external dataset validation.
- Main lesson: evaluation design affects credibility as much as model choice.

## 8. Close - camera (20-30 sec)

- A1: how wrong is the number? A2: how well do I separate groups?
- Both: honest evaluation matters more than complexity.
- Thank the audience.

## Three-pass rehearsal

1. **Navigation pass:** scroll through every stop without speaking.
2. **Cue pass:** explain each section without reading full sentences.
3. **Timed pass:** record once; do not restart for minor wording mistakes.

Delivery rule: pause after every headline number, then explain what it means.
