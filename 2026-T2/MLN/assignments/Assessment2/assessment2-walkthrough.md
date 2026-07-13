# MLN601 A2 - Operational Lot-Screening Walkthrough (v6)

Use this beside the camera while scrolling `MLN601FariaLuisBrief2v6.ipynb`.
Target: 8:00-9:00. Speak from cues; do not read notebook prose.
Keep `assessment2-glossary.md` nearby during rehearsal when a metric or modelling term is unclear.

## Story spine

> One laboratory sample represents one bottling lot -> 6,497 raw rows -> 1,177 exact
> duplicates removed -> 5,320 unique proxies -> zero split overlap -> three predefined
> operational gates -> Balanced Tree is the only candidate that passes all three -> human
> quality-control staff retain the release decision.

## Numbers box

| Item | Number |
|---|---:|
| 5-fold cross-validation (CV) gates | AUC >= 0.75; sensitivity >= 0.70; specificity >= 0.70 |
| Balanced Tree CV | AUC 0.787; sensitivity 0.731; specificity 0.703 |
| Balanced Tree test | AUC 0.792; sensitivity 0.734; specificity 0.725 |
| Test confusion matrix | TN 483; FP 183; FN 106; TP 292 |
| AUC-tuned tree | AUC 0.793; sensitivity 0.588 |
| RBF SVM | AUC 0.824; sensitivity 0.590 |
| Operational trade | 58 more weak lots caught; 69 more acceptable lots reviewed |
| Tree settings | gini; depth 5; minimum leaf 20 |
| Strongest signal | alcohol importance about 0.62; target correlation -0.4145 |
| Outlier audit | 1,473 rows flagged by IQR; retained as plausible measurements |
| SHAP example | P(low) 0.797; alcohol +0.222; volatile acidity +0.070 |

## Walkthrough

### 0. Introduction (0:45) - title cell

Cues: name + student ID | producer and bottling operation | sample is a lot proxy, not a
bottle | model routes review, human makes final release decision.

Anchor: "The question is whether routine laboratory measurements can identify production
lots at risk of low sensory quality before their bottles reach distribution."

### 1. Business Understanding (1:00) - Section 1

Cues: current process already has lab tests and expert tasting | improvement is consistent
triage | low quality `<6` is positive because it triggers action.

Explain the errors:

- False negative: weak lot follows normal release path.
- False positive: acceptable lot receives extra tasting, retest or hold.

Point to the gates. Say they were set before modelling, so the final recommendation is not
chosen after seeing the test result.

### 2. Data Understanding (1:20) - validation table, outliers, balance and correlations

Cues: UCI red + white `vinho verde` | no real `batch_id`, production date or release outcome |
technical feasibility, not proven production ROI.

Audit story: schema/types/finite/domain checks pass; 1,177 exact duplicates are the recorded
quality issue. Removal is conservative because UCI cannot prove whether they are repeated
measurements or separate identical samples.

IQR flags 1,473 rows, but a statistical flag is not proof of a measurement error. Retain them
because the values are physically plausible and rare weak lots matter to screening.

Correlation signs use low quality as 1: alcohol -0.4145, density +0.2872, volatile acidity
+0.2699. Between predictors, free and total SO2 are +0.720 while density and alcohol are
-0.668. Pairplot overlap means imperfect screening is realistic.

### 3. Data Preparation (0:55) - split and feature ablation

Cues: deduplicate before split | source quality and derived text labels excluded | stratified
80/20 gives 4,256 train and 1,064 test | exact overlap is zero | scaler and SMOTE stay inside
training folds.

Feature-engineering result: bound SO2 and free-SO2 ratio were tested, but not retained. Tuned
CV AUC fell 0.7910 -> 0.7892 and balanced-accuracy gain was only 0.0075, below the 0.01 rule.

### 4. Modelling (1:15) - tuning and CV approval table

Cues: required model is Decision Tree | default tree shows overfit | grid searches criterion,
depth and leaf size for AUC | selected gini/depth 5/leaf 20 | class weighting changes error
cost | SMOTE changes training distribution | SVM is a benchmark only.

Read the CV table by gate, not by rank:

- AUC tree fails sensitivity: 0.643.
- SMOTE fails specificity: 0.696.
- SVM fails sensitivity: 0.631 despite AUC 0.827.
- Balanced Tree alone passes all three: 0.787 / 0.731 / 0.703.

### 5. Evaluation, XAI and Approval (2:20) - metrics, matrices, tree and SHAP

Start with the approved model. On 1,064 held-out proxy lots, Balanced Tree catches 292 of 398
low-quality samples and misses 106. It clears 483 high-quality samples and unnecessarily flags
183. Test AUC 0.792, sensitivity 0.734, specificity 0.725.

Point to the AUC-tuned and balanced matrices. Balancing catches 58 additional weak proxy lots
at the cost of 69 additional acceptable lots going to review. This is the operational trade,
not a free improvement.

SVM line, under 20 seconds: "RBF SVM ranks best at AUC 0.824, but catches only 59% of weak
lots at its current threshold. Ranking leadership does not satisfy the screening gate."

Approval sentence: "I approve the Balanced Decision Tree for a controlled, human-supervised
pilot. I do not approve any model for automated lot release or rejection."

Show feature importance: alcohol about 0.62, volatile acidity next. Explain that importance
comes from tree splits, while correlation is a separate univariate relationship.

SHAP line: "Global SHAP adds direction; local SHAP explains one decision. In the selected correctly
flagged proxy, alcohol contributes +0.222 and volatile acidity +0.070 toward low quality, producing
P(low) 0.797. The additivity assertion verifies the explanation against the tree probability."

Limit: SHAP explains what the model used. It does not prove chemistry causation or prescribe a
production adjustment.

### 6. Deployment and Lessons (1:25) - Section 6

Cue - what went well: baseline made improvement measurable | learned how metrics answer different
questions | clearer lot-screening context | incorporated A1 feedback into criteria, validation,
correlation analysis and explicit model approval.

Cue - challenges: classification was harder than regression because confusion matrix, AUC,
precision, sensitivity, specificity, F1 and threshold must be read together | SMOTE must remain
inside CV folds | highest-AUC model was not the approved model.

Cue - future: collect real lot/timestamp/tasting/release data | estimate business costs and tune the
threshold | externally validate | use Sommelier API for shadow-mode engineering, model versioning,
SHAP and monitoring, while stating that the same UCI data is not external validation.

Rollback: staff retain authority; disable model routing and return to the manual workflow.

### 7. Close (0:20) - camera

"This assessment moves from predicting a score to improving a production decision. The model
does not replace quality control; it helps quality-control staff focus attention consistently
before a bottling lot is released. Thank you."

## Rehearsal and Recording

1. Navigation pass: scroll every notebook stop without speaking.
2. Gate pass: explain why each candidate passes or fails from the CV table.
3. Operational pass: explain the confusion matrices as lots, holds and escapes.
4. Timed pass: one complete take, target 8:30.

### Pre-flight

- [ ] v6 notebook executed and open at the title
- [ ] Webcam picture-in-picture and microphone checked
- [ ] Physical student card ready and shown at the beginning
- [ ] Name and student ID stated in the first 20 seconds
- [ ] UCI row-to-lot proxy limitation stated
- [ ] Three gates stated before model results
- [ ] Balanced Tree is the only approved model
- [ ] SVM explanation under 20 seconds
- [ ] Human release authority stated
- [ ] Recording between 7 and 10 minutes
- [ ] No PowerPoint; walkthrough uses the Jupyter Notebook
- [ ] Four separate files ready: `.ipynb`, `.pdf`, `.txt`, `.mp4`
- [ ] No ZIP/RAR; video link permissions tested if a URL is submitted
- [ ] Final filename `MLN601FariaLuisBrief2.mp4`
