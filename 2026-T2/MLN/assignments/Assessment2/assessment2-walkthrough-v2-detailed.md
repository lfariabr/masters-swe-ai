# MLN601 Assessment 2 - Detailed Recording Walkthrough v3

This is the long-form rehearsal script for `MLN601FariaLuisBrief2.ipynb` (the v6 notebook).

- **Target duration:** 8:30-9:30 at 120-135 spoken words per minute.
- **Recording language:** English.
- **Use:** read it aloud during early rehearsals; for the final recording, speak from the ideas
  and use `assessment2-walkthrough.md` as the shorter cue sheet.
- **Core story:** a laboratory sample represents a bottling-lot proxy; the model prioritises
  human quality-control review; it never releases or rejects a lot automatically.
- **Structure guarantee:** every block below is ONE notebook section, in notebook order, with
  the cell range on screen. If the screen shows a section, the script for that section is the
  only thing you say. Nothing is narrated before its cell appears.

---

## Fixes From the 16 Jul Takes (read once before rehearsing)

**Take 2 (12:41)** broke at four joints; **take 3 (aborted at 7:36)** confirmed the root cause:
the old script narrated in an order the notebook does not have (correlation table narrated in
"preparation", ablation narrated before 4.1). This version mirrors the notebook cell by cell,
so that failure mode is structurally gone. What remains is discipline:

1. **Clock.** Time each block against its window. Over by 15 seconds means cut commentary,
   never numbers. Take 2 lost two minutes narrating heatmap and pairplot element by element;
   they get one sentence each.
2. **Fact traps (all three happened on camera):**
   - **6,497** raw rows. Take 2 said "6,400"; take 3 said "6,597". Say it slowly: "six thousand,
     four hundred and ninety-seven".
   - **1,473** IQR-flagged rows. Take 3 said "fourteen thousand". Say: "one thousand, four
     hundred and seventy-three rows, about twenty-three percent".
   - **62.6 / 37.4** class balance. Take 3 stumbled on "thirty-seven point four".
3. **Pronunciation:** "Gini" (not "genie"), "SMOTE" as "ess-mote" once slowly, "balanced tree".
4. **Long markdown paragraphs are for the marker, not for narration.** Never read them. Speak
   the numbers against the gates and move on.
5. The scripted transitions worked in take 3 (the diagnosis-to-treatment line landed well).
   Keep delivering them; they are the joints.

---

## Block 0 - Title (cell 0) - 0:00-0:50

**Screen:** Notebook title and metadata.

**Spoken walkthrough:**

> Hello, my name is Luis Guilherme de Barros Andrade Faria, student ID A00187785. In this
> assessment, I revisit the UCI Wine Quality dataset as classification. Assessment 1 predicted a
> numerical quality score. Assessment 2 asks an operational question: should a sample be flagged
> as likely low quality?
>
> I frame this as quality-control screening for a wine producer. Each UCI row is a proxy for a
> representative sample from a bottling lot. The model routes higher-risk lots to additional
> review before release. UCI has no real batch IDs or production records, so this demonstrates
> technical feasibility, not production readiness.

**Check your understanding:** Why is this classification rather than regression? Why do we say
"proxy lot sample" instead of claiming that each row is a real production lot?

---

## Block 1 - Section 1: Business Understanding (cell 1) - 0:50-1:55

**Screen:** Section 1, especially the business question and success criteria.

**Spoken walkthrough:**

> The business problem is to release bottling lots efficiently without allowing weak batches to
> reach distribution. Laboratory tests and expert tasting already exist. The proposed improvement
> is consistent triage: routine lots follow the standard process and higher-risk lots receive more
> intensive review.
>
> Following the brief, quality below 6 is low, class 1; quality 6 or above is high, class 0. Low is
> the positive class because it triggers action.
>
> A false negative is a weak lot the model misses, so it may continue toward release. A false
> positive is an acceptable lot sent to unnecessary review. I prioritise sensitivity to catch weak
> lots, while specificity prevents the review queue becoming impractical.
>
> Before modelling, I define three cross-validation gates: AUC at least 0.75, sensitivity at least
> 0.70 and specificity at least 0.70. Defining them early prevents post-hoc model selection.

**Check your understanding:** Explain false negative and false positive without using statistical
language. Why are sensitivity and specificity both required?

---

## Block 2 - Sections 2.1-2.3: Acquisition, Quality, Duplicates (cells 2-9) - 1:55-3:00

**Screen:** Sections 2.1-2.2, the validation register and outlier audit outputs, then 2.3 with
the class-balance chart.

**Spoken walkthrough:**

> I combine the red and white wine files from the UCI Machine Learning Repository. Together they
> contain six thousand, four hundred and ninety-seven observations, 11 laboratory measurements and
> the expert quality score. I add `wine_type` to distinguish red and white samples.
>
> The validation register checks schema, numeric types, missing and non-finite values, non-negative
> measurements, valid quality levels and the rule that free sulfur dioxide cannot exceed total
> sulfur dioxide. Every hard check passes.
>
> The IQR audit flags one thousand, four hundred and seventy-three rows as statistically unusual,
> about twenty-three percent. I retain them: the values remain plausible laboratory measurements,
> an IQR flag is not evidence of an error, and rare weak lots are important to this screening
> problem.
>
> The material issue is 1,177 identical rows. Without sample IDs, I cannot prove they are all
> accidental duplicates; some may be separate samples with identical values. However, retaining
> them risks identical records crossing train and test. I remove them before splitting, leaving
> 5,320 unique proxies.
>
> The resulting balance is 62.6 percent high and 37.4 percent low, so accuracy alone is misleading.

**Check your understanding:** Why is deduplication a conservative choice rather than proof that the
data is wrong? What would duplicate leakage do to the reported metrics?

---

## Block 3 - Section 2.4: Relationships With the Target (cells 10-13) - 3:00-3:45

**Screen:** Heatmap, pairplot, target-correlation ranking and the interpretation cell. This is
still Data Understanding - preparation has not started yet.

**Spoken walkthrough:**

> The heatmap confirms what Assessment 1 showed: alcohol dominates. The required pairplot shows
> class overlap: there is useful signal, but no single feature separates the classes cleanly,
> which is why we need a model.
>
> In the target-correlation ranking, low quality is encoded as 1, so the sign must be interpreted
> carefully. Alcohol is strongest at negative 0.4145, meaning higher alcohol is associated with a
> lower probability of low quality. Density and volatile acidity have the strongest positive
> relationships. Correlation is association, not causation or tree importance.
>
> Between laboratory attributes, free and total sulfur dioxide correlate at plus 0.720, while
> density and alcohol correlate at minus 0.668. So the predictors should not be interpreted as
> independent evidence.

*(Clock note: the heatmap and pairplot get exactly the one sentence each scripted above. This is
where take 2 lost its two minutes.)*

**Transition into Section 3 (this landed well in take 3 - keep it):**

> Everything up to here was diagnosis: the audit tells me the data is clean, but duplicated and
> imbalanced. Section 3 is the treatment. It decides what the model is allowed to see: which
> features enter, how the target is encoded, and how the split protects the test set.

**Check your understanding:** Why is alcohol's negative correlation not a negative business result?
Why does correlation between predictors matter for interpretation?

---

## Block 4 - Section 3: Data Preparation (cells 14-15) - 3:45-4:30

**Screen:** Section 3 markdown (the four safeguards) and the split cell with its assertions.

**Spoken walkthrough:**

> Preparation uses four safeguards. First, the exact duplicate rows I just described are removed
> before target engineering and splitting. Second, the source quality score and derived labels are
> excluded from predictors, while `wine_type` remains. Third, an 80/20 stratified split produces
> 4,256 training and 1,064 test observations, preserves class proportions and is checked for zero
> exact overlap. Fourth, scaling and SMOTE stay inside pipelines, so each validation fold learns
> preprocessing from its own training portion only.
>
> I also announce two candidate engineered features here: bound sulfur dioxide and the free-to-total
> sulfur ratio. They will be retained only if AUC or balanced accuracy improves by at least 0.01.
> The verdict comes from training data only, in Section 4.1.

*(Do NOT give the ablation numbers here - the screen for them is 4.1. Announcing the rule here and
delivering the verdict there is exactly how the notebook is written.)*

**Check your understanding:** Why is each of the four safeguards a leakage control? Why announce
the feature rule before seeing the result?

---

## Block 5 - Section 4: Modelling (cells 16-17) - 4:30-5:20

**Screen:** Section 4 markdown with the candidate line-up and parameter rationale.

**Spoken walkthrough:**

> The Decision Tree is the required classification technique and remains the central model. A
> majority baseline establishes the no-skill floor, and an unconstrained default tree exposes
> overfitting, because it can create rules around small groups and noise.
>
> Five-fold GridSearchCV tunes criterion, depth and minimum leaf size for AUC. In five-fold CV, the
> model trains on four training-data folds and validates on the fifth, rotating five times. The
> test set remains closed. The parameter ranges are deliberate: depths 3 to 8 test readable trees,
> and minimum leaf sizes up to 20 test whether broader rules generalise better.
>
> The Balanced Tree keeps the tuned structure but makes low-class mistakes more costly. SMOTE
> creates synthetic minority examples only inside training folds. The kernel SVM is a technical
> benchmark. Unlike the trees, the SVM needs feature scaling, so the scaler lives inside the
> pipeline: it is fit only on each fold's training data, and the validation fold never leaks into
> it. That is the same discipline as SMOTE - anything learned from data happens inside the fold.

**Check your understanding:** Describe five-fold CV in your own words. Why do the trees not need
scaling while the SVM does?

---

## Block 6 - Section 4.1: Training-Only Selection and Ablation (cells 18-19) - 5:20-6:05

**Screen:** Section 4.1 - tuning results, the candidate-versus-gates table and the ablation output.
This is the block that had "nothing to say" in take 2; it is the selection moment of the whole
assessment.

**Spoken walkthrough:**

> Section 4.1 is where selection happens, still on training data only. The selected tree uses
> Gini, depth 5 and minimum leaf size 20.
>
> First, the feature verdict: with the two engineered sulfur features, cross-validated AUC falls
> from 0.7910 to 0.7892 and balanced accuracy improves by only 0.0075, below my 0.01 rule. I retain
> the simpler 12-feature set. Rejecting a feature by a predeclared rule is a result, not a failure.
>
> Then the gates. The AUC-tuned tree fails sensitivity at 0.643. SMOTE fails specificity at 0.696.
> The SVM has the highest AUC at 0.827, but sensitivity is only 0.631. Only the Balanced Tree
> passes every gate: AUC 0.787, sensitivity 0.731 and specificity 0.703.
>
> The RBF kernel also won the kernel search, 0.826 against 0.804 for linear, which supports a
> moderately nonlinear boundary, consistent with the overlap in the pairplot.

**Transition into Section 5 (the other joint that broke take 2):**

> Section 4 ends with the candidates and their cross-validation numbers, and the selection is
> frozen there. Section 5 opens the held-out test set with one job only: confirm the frozen
> choice. It is the final exam, not a second chance to pick.

**Check your understanding:** Why is the model with the highest AUC not automatically approved?
Why is the ablation verdict delivered here and not in Section 3?

---

## Block 7 - Sections 5, 5.1-5.3: Evaluation, XAI, Approval (cells 20-31) - 6:05-8:15

**Screen:** Test metrics, ROC curves, confusion matrices, the tree, SHAP outputs (5.1), the
operational result (5.2) and the approval table (5.3), in scroll order.

**Spoken walkthrough:**

> On the held-out test set, the Balanced Tree confirms AUC 0.792, sensitivity 0.734, specificity
> 0.725, balanced accuracy 0.729 and F1 0.669. It meets the criteria defined in Business
> Understanding.
>
> The confusion matrix makes this concrete. The test set has 1,064 proxies: 666 genuinely high
> and 398 genuinely low. Those are the row sums of the matrix - the figure shows only the four
> cells. Of the 398 low-quality proxies, the model flags 292 and misses 106; that is the 73
> percent sensitivity. Of the 666 high-quality proxies, it clears 483 and unnecessarily flags 183.
>
> Compared with the AUC-tuned tree, balancing catches 58 additional weak proxies but sends 69
> additional acceptable proxies to review. This exchanges tasting effort and possible delay for
> fewer weak lots escaping screening.
>
> The SVM has the highest test AUC, 0.824. AUC is the probability that a random low sample receives
> a higher risk score than a random high sample; it is not 82.4 percent accuracy. At the operating
> threshold, SVM sensitivity is only 0.590, below the gate.
>
> In Section 5.1 I add SHAP, because the tree diagram and feature importance are global views.
> Alcohol has importance around 0.62, followed by volatile acidity, but importance does not prove
> causation. Global SHAP adds direction, and local SHAP explains one prediction: for the selected
> correctly flagged proxy, alcohol contributes plus 0.222 and volatile acidity plus 0.070 toward
> low quality, producing a low-quality probability of 0.797. The additivity check reconstructs the
> model probability within numerical tolerance. SHAP explains the model's reasoning; it does not
> prove chemical causation.
>
> In Section 5.3, I approve only the Balanced Decision Tree, for a controlled, human-supervised
> pilot. It passes all gates and exposes inspectable rules. No model is approved for automated
> release or rejection.

**Check your understanding:** Explain AUC without saying "accuracy". Explain the 58 versus 69
trade-off as if speaking to a quality-control manager.

---

## Block 8 - Section 6: Deployment, Monitoring and Lessons (cell 32) - 8:15-9:15

**Screen:** Section 6.

**Spoken walkthrough:**

> What went well was learning to use a baseline and several metrics to make improvement measurable.
> I also defined a clearer lot-screening context and incorporated the Assessment 1 feedback by
> strengthening data validation, correlation analysis, success criteria and the approval decision.
>
> The main challenge was moving from regression to classification. Instead of interpreting one
> prediction error, I had to understand the confusion matrix, ROC-AUC, precision, sensitivity,
> specificity, F1 and threshold together. I found this substantially more difficult because a model
> can improve one metric while weakening another. SMOTE added another challenge because synthetic
> samples must be created only inside cross-validation training folds to avoid leakage.
>
> Future work needs real lot IDs, timestamps, process conditions, tasting outcomes and release
> decisions, followed by temporal or external validation and cost-based threshold tuning. The
> existing Sommelier API provides an engineering path through FastAPI and Streamlit. It could support
> shadow-mode predictions, model versioning, SHAP explanations and monitoring. However, because it
> uses the same UCI data, it demonstrates delivery capability rather than external validation. Staff
> retain authority, and rollback restores the manual workflow.

**Check your understanding:** Which fields are missing for a real pilot? What would trigger rollback
or recalibration?

---

## Block 9 - Closing - 9:15-9:30

**Screen:** Return to the title or keep the deployment conclusion visible.

**Spoken walkthrough:**

> In conclusion, this assessment moves beyond predicting a wine score and focuses on improving a
> production decision. The Balanced Decision Tree does not replace laboratory testing or expert
> judgement. It provides a reproducible way to prioritise attention before a bottling lot is
> released. Thank you.

---

## Why This Is a Portfolio Case

Do not add exaggerated production claims. The credible portfolio story is:

> Designed an end-to-end, CRISP-DM classification study for operational wine-lot screening using
> UCI physicochemical data. Built data-quality validation, duplicate-leakage controls, stratified
> evaluation, cross-validated Decision Tree tuning, class-imbalance experiments and explicit
> model-approval gates. Recommended an interpretable human-supervised screening policy and defined
> the data, monitoring and rollback requirements for a real pilot.

This demonstrates more than model fitting:

- translation from an academic target into an operational decision;
- defensible data-quality and leakage controls;
- metrics selected from asymmetric business errors;
- honest rejection of features and models that did not meet predefined criteria;
- separation between ranking performance and operating-threshold performance;
- model governance, monitoring, rollback and human authority;
- clear limitation that UCI rows are proxy samples, not real production lots.

## Recommended Rehearsal Sequence

1. Scroll the notebook once with this script beside it and confirm every block's cell range
   matches what you see. The blocks are in notebook order; nothing is narrated early.
2. Rehearse the three scripted transitions (Blocks 3→4 and 6→7, plus the 398 derivation in
   Block 7) until they come out without reading.
3. Say the three fact traps aloud five times: "six thousand four hundred and ninety-seven",
   "one thousand four hundred and seventy-three", "thirty-seven point four".
4. Record one audio-only attempt from memory, with a stopwatch: note the time at the end of
   each block against its window. Over by 15 seconds means cut commentary, never numbers.
5. Rehearse notebook scrolling with the shorter `assessment2-walkthrough.md` (note: the short
   cue sheet still has the OLD block order - use this file until it is re-synced).
6. Record the final video conversationally; use this detailed script only if you lose the thread.
