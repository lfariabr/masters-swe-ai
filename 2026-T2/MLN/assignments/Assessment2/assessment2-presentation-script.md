# MLN601 Assessment 2 - Video Presentation Script (7-10 min)

Timed script for the video (screen recording + webcam picture-in-picture).
**Spoken lines** are what you say to camera. **Directions** (in *italics*) are what to show
on screen + delivery tips. Target: ~9 min (middle of the 7-10 range, safe).

## Golden rules (video rubric - 15%)
- Picture-in-picture: webcam on + notebook on screen at the same time.
- **Vary tone and volume** - emphasise the numbers and the honest conclusion (the marker rewards this).
- **Touch ALL 6 CRISP-DM stages** and close with your own personal experience.
- Point at what's on screen ("here you can see..."). Don't read the slide, tell the story.
- Pace: ~150 words/min. Don't rush. Pause after each important number.

## Time map
| # | Segment | Time | Show on screen |
|---|---|---|---|
| 0 | Intro + purpose | 0:45 | Title cell |
| 1 | A1 -> A2 (the hook) | 0:45 | Title cell / table |
| 2 | Business Understanding | 0:45 | Section 1 |
| 3 | Data Understanding | 1:30 | EDA: class balance, heatmap, pairplot |
| 4 | Data Preparation | 1:00 | Section 3 + split |
| 5 | Modelling | 1:30 | Section 4 + grid + best params |
| 6 | Evaluation | 2:00 | Metrics table, ROC, confusion matrix, importances |
| 7 | Deployment / Lessons | 1:00 | Section 6 |
| 8 | Close + experience | 0:30 | Camera (no screen) |
| | **Total** | **~8:45** | |

---

## 0. Intro + purpose (0:45)
> *Direction: camera on your face, smile, high energy at the start. Show the title cell.*

"Hi, my name is Luis Faria, and this is my Assessment 2 for MLN601, Machine Learning, with
Dr. Kamran Shaukat. In Assessment 1 I treated the UCI wine quality dataset as a *regression*
problem - predicting the exact quality score. Today I'm revisiting the *same* data, but as a
*binary classification* task: is a wine high or low quality? I'll walk you through the whole
notebook following the six stages of CRISP-DM, share the results, and finish with what I
learned along the way."

## 1. A1 -> A2: the hook (0:45)
> *Direction: this is the part that impresses. Speak with conviction.*

"The interesting shift here is conceptual. In regression I was asking *'how far off is my
number?'* - measured with RMSE and R-squared. In classification I'm asking *'which side of
the line does it fall on, and how well do I separate the two groups?'* - measured with the
**AUC-ROC curve**. Same wines, but a completely different question, a different baseline, and
a whole new vocabulary of metrics. So everything downstream - the target, the models, the
evaluation - had to change with it."

## 2. CRISP-DM Stage 1: Business Understanding (0:45)
> *Direction: scroll to Section 1.*

"Stage one, Business Understanding. The practical idea is a fast, low-cost screen that flags
wine batches likely to score poorly, so expert tasters spend their time where it matters.
Following the brief, I split the quality score: **below 6 is 'low', 6 or above is 'high'**.
I deliberately made *low quality the positive class*, because the action we care about is
*flagging the weak batches*. And throughout, this is framed as **decision support**, not
automation - quality is a subjective human score, so the model assists experts, it doesn't
replace them."

## 3. CRISP-DM Stage 2: Data Understanding (1:30)
> *Direction: show, in sequence, the class-balance chart, the heatmap, then the pairplot.*

"Stage two, Data Understanding. I loaded both the red and white wine files and combined them
into one dataset of **6,497 wines**, with a `wine_type` flag. Here you can see the class
balance: about **63% high quality and 37% low** - so the classes are *imbalanced*, which
becomes important later.

This correlation heatmap shows `alcohol` has the strongest link with quality, and several
features - like the two sulfur-dioxide measures - are correlated with each other.

And this is the seaborn **pairplot** the brief asks for. The key takeaway is that the two
classes **overlap heavily** - no single feature cleanly separates a good wine from a bad one.
That tells me upfront to expect a *good-but-imperfect* model, not a perfect one. I also found
1,177 duplicate rows; with no unique wine ID, those are likely real wines with identical
readings, so I kept them rather than throw away valid data."

## 4. CRISP-DM Stage 3: Data Preparation (1:00)
> *Direction: Section 3 + the split cell. Point at `stratify` and the Pipeline.*

"Stage three, Data Preparation. The data was already clean and numeric, so prep was light but
deliberate. First, I removed the original quality score from the features so it can't leak
into training. Second, I used an **80/20 stratified split** - stratified so the high/low ratio
is preserved in both sets, which matters under imbalance. That gives 5,197 training and 1,300
test wines. Third, on scaling: a Decision Tree is **scale-invariant** - it splits on
thresholds - so it needs no scaling. The Logistic Regression comparator *does*, so I put its
scaler **inside a Pipeline**, which means it's refit on each fold during cross-validation and
never sees the validation data. That's how I prevent leakage."

## 5. CRISP-DM Stage 4: Modelling (1:30)
> *Direction: Section 4, then the best-params output. Emphasise 'roc_auc' and the hyperparameters.*

"Stage four, Modelling. I compared four models so the tree could be read in context: a
majority-class **baseline**, a **default** Decision Tree, a **tuned** Decision Tree - which is
the required model - and Logistic Regression as optional context. For tuning I used
`GridSearchCV` with **5-fold cross-validation**, searching `max_depth`, `min_samples_leaf`,
the split criterion, and `class_weight`, all scored on **ROC AUC** rather than accuracy. The
best configuration came out as `max_depth` of 6 and a minimum leaf size of 20 - a moderate,
pruned tree, which makes sense: an unconstrained tree grows until its leaves are pure and just
memorises the training data. The pruning is what stops it overfitting."

## 6. CRISP-DM Stage 5: Evaluation (2:00)
> *Direction: the most important part. Show the metrics table, then the ROC curve, then the
> confusion matrix, then feature importance. Pause on every number.*

"Stage five, Evaluation - judged on the held-out test set. Here's the metrics table. The
tuned Decision Tree reaches an **AUC of 0.809**, far above the baseline's 0.500. Now look at
this ROC curve: the tuned tree, in orange, sits well above the diagonal, which is random
guessing.

Here's the honest part. The Logistic Regression - the *simpler* model - scored **0.814**, so
the two are **essentially level**. That's a genuine finding, not a failure: it tells me a
straight-line boundary captures almost as much as the tree on this data. And notice tuning
actually *lowered* raw accuracy from 0.79 to 0.74 - because I optimised for *ranking*, AUC,
not accuracy. Under imbalance, accuracy is misleading: a model that always predicts 'high'
already scores 63%.

The confusion matrix shows the trade-off: the model confirms high-quality wines well - recall
of 0.78 - but catches the low-quality ones less reliably, recall 0.66. That's the cost of the
imbalance and the class overlap.

Finally, **feature importance**: `alcohol` dominates at 0.49, then `volatile acidity` at 0.21
- which matches both the EDA and real wine chemistry. The fact that the model agrees with
domain knowledge gives me confidence it's learning something real."

## 7. CRISP-DM Stage 6: Deployment / Lessons Learned (1:00)
> *Direction: Section 6. More reflective tone, slower.*

"Stage six, Deployment. For this assessment, deployment means reflection. What worked: framing
it as classification made the Decision Tree a natural, **interpretable** fit, and AUC-ROC gave
an honest read where accuracy would have flattered a lazy model. The white-box tree and the
importance chart make the result explainable to a non-technical stakeholder - a real advantage
for quality control. What was harder: the classes overlap so heavily that no tuning produced a
clean separation - the model is a *screen*, not an oracle. And what I'd do next time: try an
ensemble like Random Forest to see how much a single tree leaves on the table, and tune the
decision threshold to the real cost of missing a bad batch, instead of defaulting to 0.5."

## 8. Close + personal experience (0:30)
> *Direction: back to camera, no screen. Eyes on the lens. Finish with energy.*

"To close on a personal note: across both assessments the same lesson kept coming back.
Assessment 1 taught me to measure *how much I'm wrong*; Assessment 2 taught me to measure
*how well I separate* - and both taught me that choosing the right model and evaluating it
*honestly* matters more than piling on data or complexity. Thanks for watching."

---

## Recording checklist
- [ ] Webcam + screen at the same time (picture-in-picture). Test before recording.
- [ ] Notebook already open and scrolled to the top, font large enough to read on video.
- [ ] Clean audio (no echo). Speak at a measured pace, vary the tone on the numbers.
- [ ] Timer: if you go past 10 min, cut segment 5 (Modelling) first.
- [ ] File name: `MLN601FariaLuisBrief2.mp4` (or paste the URL into the submission field).
- [ ] Make sure to mention AUC 0.809, the tie with logistic regression, and recall 0.78 vs 0.66
      (the numbers the marker wants to hear).
