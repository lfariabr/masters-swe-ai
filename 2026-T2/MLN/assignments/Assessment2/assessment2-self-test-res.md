# MLN601 Assessment 2 - Self-Test: my answers + grading

Scored **78/100**. Solid band. The big A1 weak spot (leakage direction) is now FIXED - arrow
right this time. Two real gaps, both new-material: **why tuning dropped accuracy (Q5)** and
**why Naive Bayes survives violated independence (Q9b)**. Both are 30-second beats in the
video, so lock them before recording.

| Q | Topic | Score | Verdict |
|---|---|---|---|
| 1 | Reframing regression -> classification | 5/5 | got it |
| 2 | Positive class choice | 5/5 | "seek and destroy" - exactly it |
| 3 | Baseline accuracy vs AUC | 8/8 | got it |
| 4 | ROC curve | 10/10 | clean, both parts |
| 5 | Tuning dropped accuracy | 0/12* | blanked - LEARN THIS (see fix) |
| 6 | Confusion matrix + threshold lever | 10/10 | best answer - both directions right |
| 7 | Stratify + leakage direction | 11/12 | A1 gap closed, arrow correct |
| 8 | Hyperparameters + roc_auc scoring | 11/12 | one muddle on thresholds |
| 9 | Generative vs discriminative | 5/13 | (a) right, (b) blank - LEARN THIS |
| 10 | The honest finding | 13/15 | linear boundary + interpretability nailed |
| B | AUC != accuracy trap | 0/5 | skipped |

*Q5 is worth 10 in the quiz; table normalised to match the key.

---

## Per question

### Q1 - reframing. 5/5
B. Same wines, new question: "how far off?" became "which side of the line?".

### Q2 - positive class. 5/5
"Low quality is what we want to seek and destroy" - that is the whole idea. The positive
class is the event you ACT on, so recall/precision on it measure the useful thing.

### Q3 - baseline. 8/8
B. Accuracy 0.633 is free under 63/37 imbalance; AUC 0.5 exposes zero ranking skill.

### Q4 - ROC. 10/10
TPR vs FPR, trade-off across thresholds, diagonal = random, above = discriminative power.
All there.

### Q5 - tuning dropped accuracy. 0 (the gap - LEARN THIS)
My answer: "don't know" - and the honest note that coming from RMSE/R-squared this felt
unmeasurable. That instinct is actually the key to the fix:

**The fix.** In A1 there was ONE number to optimise (error). In A2 there are TWO layers:
the model outputs a *score* (ranking), and a *threshold* turns it into a decision. Accuracy
lives at one threshold (0.5); AUC judges the ranking across ALL thresholds.

GridSearchCV was told `scoring="roc_auc"`, so it picked the tree with the best RANKING
(0.773 -> 0.809), and happily paid for it with accuracy at the 0.5 threshold
(0.786 -> 0.737). No contradiction: the two metrics answer different questions, and under
63/37 imbalance accuracy is a soft target anyway (0.633 is free).

One-liner to remember: **you get what you optimise - we optimised ranking, so accuracy was
negotiable.**

### Q6 - confusion matrix. 10/10 (best answer)
Recall 0.66 = catch 66% of truly low wines, miss 1 in 3. Missing a low wine is the costly
error (bad batch ships, brand damage). Lever = decision threshold, and BOTH directions were
stated correctly (lower threshold -> recall up + more false alarms; higher -> the reverse).
This was the hardest applied question and it was flawless.

### Q7 - stratify + leakage. 11/12
Part 1: B, correct. Part 2: "info must flow from training to test, never vice-versa" - the
ARROW IS RIGHT this time (A1's miss, now closed). One point off for loose phrasing: strictly,
the scaler is FIT on train only and merely APPLIED to test; nothing is fit on test, ever.

### Q8 - hyperparameters. 11/12
(a) and (b) full marks - depth caps complexity, leaf size 20 blocks rules built on a handful
of samples, unconstrained tree memorises and fails on unseen data.
(c) right conclusion, one muddle: "we opted to push the threshold to favor recall" - no
threshold was pushed during tuning. AUC is *threshold-free*; that is exactly WHY it suits an
imbalanced problem. Threshold-moving is a separate, later lever (your own Q6 answer).

### Q9 - generative vs discriminative. 5/13 (the gap - LEARN THIS)
(a) Correct: discriminative learns the boundary directly; generative learns each class's
feature distribution. (Add for completeness: NB then inverts with Bayes' rule to classify.)
(b) Blank. **The fix:**

Classification only needs the **right ORDER, not the right probabilities**. Violated
independence makes NB's probability values wrong (over-confident - correlated evidence gets
double-counted), but it often does NOT flip which class scores higher. Wrong values, same
winner. Since AUC measures ranking, NB stays useful: 0.771, level with the default tree.
That is the Domingos & Pazzani (1997) result in one line: **broken assumption, intact
ranking.**

Warehouse anchor: two dashboards double-count the same delayed truck - the delay NUMBER is
inflated, but the WORST route still ranks worst. Decisions survive; calibration does not.

### Q10 - the honest finding. 13/15
(a) Linear boundary - correct, 5/5. (c) Interpretability ("easy to showcase") - correct,
5/5. (b) 3/5: "we dug deep and reported honestly" is true but generic. The sharper point:
**without LogReg in the lineup, AUC 0.809 would have looked more impressive than it is.**
The comparator is what makes the evaluation honest - model choice becomes evidence-based,
not loyalty-based.

### Bonus - skipped. 0/5
The trap answer is B: AUC = P(random low wine ranked above random high wine). Your own
numbers prove AUC != accuracy: 0.809 vs 0.737 could not disagree if they were the same thing.

---

## The 3 things to actually lock in (before recording)

1. **You get what you optimise.** Grid scored on roc_auc -> better ranking (0.773 -> 0.809),
   worse accuracy at 0.5 (0.786 -> 0.737). Two layers: score (ranking) vs threshold
   (decision). This is a spoken beat in Evaluation - do not blank it on camera.
2. **NB: broken assumption, intact ranking.** Correlated features double-count evidence ->
   probabilities wrong -> winner usually unchanged -> AUC survives (0.771). The 6.5 beat.
3. **AUC is threshold-FREE.** Never say "we pushed the threshold" about tuning. Thresholds
   are the deployment lever (Q6), not the tuning mechanism.

Band: 78/100 = solid. A1 was 80 with a 0/12 blank too - same pattern: strong on what you
have used, blank on what you have only read. The two fixes above ARE video beats, so
rehearsing them closes the gap and preps the recording at the same time.
