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
| 6 | Evaluation | 2:00 | Metrics table, ROC (4 curves), confusion matrix, importances |
| 6.5 | Naive Bayes (generative angle) | 0:30 | Section 5.4 + ROC |
| 7 | Deployment / Lessons | 1:00 | Section 6 |
| 8 | Close + experience | 0:30 | Camera (no screen) |
| | **Total** | **~9:15** | |

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
into **6,497 raw rows**, with a `wine_type` flag. The quality check found **1,177 exact
duplicates**, so I removed them before modelling, leaving **5,320 unique wines**. Here you
can see the final class balance: about **63% high quality and 37% low** - so the classes are
moderately imbalanced, which becomes important later.

This correlation heatmap shows `alcohol` has the strongest link with quality, and several
features - like the two sulfur-dioxide measures - are correlated with each other.

And this is the seaborn **pairplot** the brief asks for. The key takeaway is that the two
classes **overlap heavily** - no single feature cleanly separates a good wine from a bad one.
That tells me upfront to expect a *useful-but-imperfect* classifier, not a perfect one."

## 4. CRISP-DM Stage 3: Data Preparation (1:00)
> *Direction: Section 3 + the split cell. Point at `stratify` and the Pipeline.*

"Stage three, Data Preparation. The most important change was removing duplicates **before**
the split. Otherwise, an identical row can appear in training and testing, so the test set is
not genuinely unseen. In the previous draft this affected 359 test rows. The final split has
**zero exact overlap**, with 4,256 training and 1,064 test wines.

I also removed the original quality score from the features so it cannot leak into training,
and used an **80/20 stratified split** to preserve the class ratio. A Decision Tree is
scale-invariant, while Logistic Regression needs scaling, so its `StandardScaler` sits inside
a Pipeline and is fitted only on training data during cross-validation."

## 5. CRISP-DM Stage 4: Modelling (1:30)
> *Direction: Section 4, then the best-params output. Emphasise 'roc_auc' and the hyperparameters.*

"Stage four, Modelling. I compared five models so the tree could be read in context: a
majority-class **baseline**, a **default** Decision Tree, the **tuned** Decision Tree - which is
the required model - Logistic Regression, and a Gaussian Naive Bayes, both as optional context. For tuning I used
`GridSearchCV` with **5-fold cross-validation**, searching `max_depth`, `min_samples_leaf`,
the split criterion, and `class_weight`, all scored on **ROC AUC** rather than accuracy. The
best configuration came out as `max_depth` of 5 and a minimum leaf size of 20 - a moderate,
pruned tree, which makes sense: an unconstrained tree grows until its leaves are pure and just
memorises the training data. The pruning is what stops it overfitting."

## 6. CRISP-DM Stage 5: Evaluation (2:00)
> *Direction: the most important part. Show the metrics table, then the ROC curve, then the
> confusion matrix, then feature importance. Pause on every number.*

"Stage five, Evaluation - judged on the held-out test set. Here's the metrics table. The
tuned Decision Tree reaches an **AUC of 0.793**, far above the baseline's 0.500. In plain
English, that means a random low-quality wine receives a higher risk score than a random
high-quality wine about 79% of the time. Now look at
this ROC curve, with all four models overlaid: the tuned tree, in orange, sits well above
the diagonal, which is random guessing.

Here's the honest part. Logistic Regression - the simpler model - scored **0.813**, which is
0.020 above the required tree on this test split. Tuning still matters: it lifts the tree's
AUC from **0.657 to 0.793** and accuracy from 0.68 to 0.74 by pruning the overfit default
tree. Removing duplicates also lowers the earlier draft AUC from 0.809 to 0.793. That is a
more credible result, not a worse project.

The confusion matrix shows the trade-off: the model confirms high-quality wines well - recall
of **0.83** - but catches the low-quality ones less reliably, recall **0.59**. That's the
cost of the imbalance and class overlap.

Finally, **feature importance**: `alcohol` dominates at 0.58, then `volatile acidity` at 0.19
- which matches both the EDA and real wine chemistry. The fact that the model agrees with
domain knowledge gives me confidence it's learning something real."

## 6.5 Naive Bayes - the generative counterpoint (0:30)
> *Direction: scroll to section 5.4 and point at the dark-red Naive Bayes curve on the ROC. Ties to Module 5 - say it with a bit of pride.*

"One more comparison, and it ties straight to Module 5. The Decision Tree and Logistic
Regression are *discriminative* - they learn the decision boundary directly. Gaussian Naive
Bayes is *generative*: it models how
each feature is distributed per class and inverts it with Bayes' rule. Its big assumption -
that the features are independent given the class - my own correlation heatmap shows is *not*
true here. It still scores an **AUC of 0.736** - above the untuned tree at 0.657, but below
the tuned tree and Logistic Regression. This is consistent with classic evidence that Naive
Bayes classification can remain useful when independence is violated, although the
discriminative models fit this dataset better."

## 7. CRISP-DM Stage 6: Deployment / Lessons Learned (1:00)
> *Direction: Section 6. More reflective tone, slower.*

"Stage six, Deployment. For this assessment, deployment means reflection. What worked: the
Decision Tree remained interpretable, AUC evaluated ranking across thresholds, and removing
duplicates made the test genuinely unseen. What was harder: the classes overlap heavily and
low-quality recall is only 0.59, so the model is a *screen*, not an oracle. Next time I would
test Random Forest or gradient boosting, tune the threshold to the real cost of missing a bad
batch, and validate on wine from a different producer or time period. The key lesson is that
evaluation design can change credibility as much as model choice."

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
- [ ] Make sure to mention: 1,177 duplicates removed; zero split overlap; tree AUC 0.793;
      Logistic Regression 0.813; low-quality recall 0.59; Naive Bayes 0.736.
