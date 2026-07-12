# MLN601 Assessment 2 v5 - Operational Self-Test

Closed-book rehearsal for the notebook and video. Target: 35-40 minutes. Answer each question
aloud in two to four sentences before checking the key.

**CV means cross-validation:** five rotations over training-data folds, used to select the model
before the untouched test set is opened.

## Evidence Box

| Candidate | CV AUC | Sensitivity | Specificity | Passes all gates? |
|---|---:|---:|---:|---|
| AUC-tuned tree | 0.791 | 0.643 | 0.787 | No |
| Balanced tree | 0.787 | 0.731 | 0.703 | Yes |
| SMOTE tree | 0.783 | 0.738 | 0.696 | No |
| RBF SVM | 0.827 | 0.631 | 0.843 | No |

Balanced Tree test: AUC 0.792, sensitivity 0.734, specificity 0.725, TN 483, FP 183,
FN 106, TP 292. Low quality is class 1.

## Questions

### Q1. Operational unit and limitation (10 points)

What does one UCI row represent in the proposed business case, and why can the report not claim
that it has already validated real bottling lots?

### Q2. Business workflow (10 points)

Describe the path from laboratory sampling to final lot-release decision. Where must human
authority remain?

### Q3. Error costs (10 points)

Explain a false negative and false positive as operational events. Why is sensitivity prioritised
without allowing specificity to collapse?

### Q4. Predefined gates (10 points)

State all three model-performance gates. Why must they be declared before inspecting the final
test results?

### Q5. Data-quality issue (10 points)

Why were 1,177 exact rows removed, and what uncertainty prevents calling all of them proven
duplicate measurements?

### Q6. Correlation and importance (10 points)

Low quality is encoded as 1. Interpret alcohol's target correlation of -0.4145. Why is this not
the same quantity as its Decision Tree importance of about 0.62?

### Q7. Feature engineering (10 points)

Which two sulfur features were tested? What evidence caused them to be rejected?

### Q8. Model approval (10 points)

The SVM has the highest CV and test AUC. Why is the Balanced Tree still the only approved model?

### Q9. Confusion-matrix trade-off (10 points)

Compared with the AUC-tuned tree, the Balanced Tree catches 58 more weak proxy lots and creates
69 more false alarms. Explain the business meaning of both numbers.

### Q10. Pilot and rollback (10 points)

Name at least four fields missing from UCI that a real pilot needs, three monitoring metrics and
the rollback procedure.

---

# Answer Key

### A1

One row is treated as a proxy for a representative laboratory sample from a homogeneous bottling
lot, not as a bottle. UCI has no lot ID, production date, line, tasting workflow or release outcome,
so it only supports technical feasibility.

### A2

Assign a lot ID, take a representative sample, record the 11 measurements, score it, route flagged
lots to hold/review and let quality-control staff decide release, retest or rework. The model cannot
release or reject automatically.

### A3

A false negative lets a weak lot continue through normal release. A false positive sends an
acceptable lot to unnecessary tasting or hold. Sensitivity protects against escapes; the 0.70
specificity gate keeps the review queue from becoming operationally unusable.

### A4

CV ROC-AUC >= 0.75, sensitivity >= 0.70 and specificity >= 0.70. Declaring them first prevents
post-hoc model choice and keeps the final held-out test as confirmation rather than tuning data.

### A5

Removing exact rows before splitting prevents identical feature/label records crossing the
train/test boundary. Without source IDs, identical rows could still be separate samples with the
same measurements, so removal is a conservative evaluation decision rather than proof of bad data.

### A6

The negative sign means higher alcohol is associated with a lower probability of class 1, low
quality. Correlation is a standalone linear association; tree importance measures how much learned
splits using that feature reduce impurity, including interactions and repeated splits.

### A7

`bound_sulfur_dioxide = total - free` and `free_so2_ratio = free / total`. Tuned CV AUC fell from
0.7910 to 0.7892, and the balanced-accuracy improvement was only 0.0075, below the 0.01 materiality
rule, so the added complexity was not retained.

### A8

The SVM fails the operational sensitivity gate: CV sensitivity is 0.631 and test sensitivity is
0.590. Balanced Tree is the only candidate passing all CV gates, and its rules are inspectable by
quality-control staff.

### A9

Fifty-eight additional weak proxy lots would be routed to review instead of escaping normal
screening. Sixty-nine additional acceptable lots would incur tasting, hold and possible delay. The
approved policy accepts that review cost to reduce weak-lot escapes.

### A10

Pilot fields include lot ID, production date, tank/line, lab timestamp, tasting outcome and release
decision. Monitor sensitivity, specificity, hold rate, weak-lot escape rate and release lead time.
Rollback disables model routing and restores the existing manual workflow for every lot.
