# MLN601 Assessment 2 - Detailed Recording Walkthrough v2

This is the long-form rehearsal script for `MLN601FariaLuisBrief2.ipynb`.

- **Target duration:** 8:30-9:30 at 120-135 spoken words per minute.
- **Recording language:** English.
- **Use:** read it aloud during early rehearsals; for the final recording, speak from the ideas
  and use `assessment2-walkthrough.md` as the shorter cue sheet.
- **Core story:** a laboratory sample represents a bottling-lot proxy; the model prioritises
  human quality-control review; it never releases or rejects a lot automatically.

---

## Take-3 Fixes (from the 16 Jul recording attempt)

The first full take ran **12:41 against a 10:00 limit** and broke at four specific joints.
Every one of them now has a scripted line below (marked **Transition** or flagged inline).

1. **Clock discipline.** The overrun came from Data Understanding: heatmap and pairplot were
   narrated element by element. Each is worth ONE sentence (already scripted in Block 3).
   Time each block against its window; if a block overruns by 15 seconds, cut commentary,
   never numbers.
2. **The Section 2 → 3 joint** ("I lost myself"). Use the diagnosis-to-treatment transition
   at the end of Block 2. Do not re-explain the dedup in Section 3; it was already told.
3. **The SVM scaling sentence** ("I don't have a clue how to explain that"). Scripted in
   Block 4: the scaler lives inside the pipeline, fit only on each fold's training data.
4. **The Section 4 → 5 joint** ("I need a hook"). Scripted: selection frozen in CV, the test
   set is the final exam, not a second chance to pick.
5. **The 398 mystery.** 398 is the bottom ROW SUM of the confusion matrix (292 caught + 106
   missed = all genuinely low proxies in the 1,064-row test set; 483 + 183 = 666 high). The
   figure shows the four cells only, so derive the sums aloud - scripted in Block 5.
6. **Fact traps from the take:** it is **6,497** raw rows, not 6,400; enunciate **"Gini"**
   and **"SMOTE"** slowly once (the transcript heard "genie" and "smart"); say **"balanced
   tree"**, not "balance said tree".
7. **Long paragraphs are for the marker, not for narration.** Never read them. Speak the
   three numbers against the three gates and move on.

---

## Block 0 - Introduction and Story (0:00-0:50)

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

## Block 1 - Business Understanding (0:50-1:55)

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

## Block 2 - Data Acquisition and Quality (1:55-3:10)

**Screen:** Sections 2.1-2.3, data-quality table and class-balance chart.

**Spoken walkthrough:**

> I combine the red and white wine files from the UCI Machine Learning Repository. Together they
> contain 6,497 observations, 11 laboratory measurements and the expert quality score. I add
> `wine_type` to distinguish red and white samples.
>
> The validation register checks schema, numeric types, missing and non-finite values, non-negative
> measurements, valid quality levels and the rule that free sulfur dioxide cannot exceed total
> sulfur dioxide. Every hard check passes.
>
> The IQR audit flags 1,473 rows as statistically unusual. I retain them because their laboratory
> values remain plausible, an IQR flag is not evidence of an error, and rare weak lots are important
> to this screening problem.
>
> The material issue is 1,177 identical rows. Without sample IDs, I cannot prove they are all
> accidental duplicates; some may be separate samples with identical values. However, retaining
> them risks identical records crossing train and test. I remove them before splitting, leaving
> 5,320 unique proxies.
>
> The resulting balance is 62.6 percent high and 37.4 percent low, so accuracy alone is misleading.

**Transition into Section 3 (say this - it is the joint that broke take 2):**

> Everything up to here was diagnosis: the audit tells me the data is clean, but duplicated and
> imbalanced. Section 3 is the treatment. It decides what the model is allowed to see: which
> features enter, how the target is encoded, and how the split protects the test set.

**Check your understanding:** Why is deduplication a conservative choice rather than proof that the
data is wrong? What would duplicate leakage do to the reported metrics?

---

## Block 3 - Exploration and Data Preparation (3:10-4:25)

**Screen:** Correlation ranking, pairplot, Section 3 and feature-ablation output.

**Spoken walkthrough:**

> In the target-correlation table, low quality is encoded as 1, so the sign must be interpreted
> carefully. Alcohol is strongest at negative 0.4145, meaning higher alcohol is associated with a
> lower probability of low quality. Density and volatile acidity have the strongest positive
> relationships. Correlation is association, not causation or tree importance.
>
> Between laboratory attributes, free and total sulfur dioxide have the strongest positive
> correlation at 0.720, while density and alcohol have a strong negative relationship at minus
> 0.668. This means the predictors should not be interpreted as independent evidence.
>
> The heatmap confirms what Assessment 1 showed: alcohol dominates. The pairplot shows class
> overlap: there is useful signal, but no single feature separates the classes cleanly, which
> is why we need a model.

*(Clock note: those two figures get one sentence each, exactly as scripted above. This is where
take 2 lost its two minutes.)*
>
> I exclude the original quality score and derived labels from predictors. A stratified 80/20 split
> produces 4,256 training and 1,064 test observations, preserves class proportions and has zero
> exact overlap.
>
> I also test bound sulfur dioxide and the free-to-total sulfur ratio. CV AUC falls from 0.7910 to
> 0.7892, while balanced accuracy improves only 0.0075, below my 0.01 rule. I retain the simpler
> 12-feature set.

**Transition into Section 4:**

> The data is now ready and locked. Section 4 is where the candidates compete, all of them under
> the same cross-validation rules.

**Check your understanding:** Why is alcohol's negative correlation not a negative business result?
Why is rejecting engineered features evidence of good model development?

---

## Block 4 - Modelling and Cross-Validation (4:25-5:55)

**Screen:** Section 4, tuning parameters and the compact CV comparison table.

**Spoken walkthrough:**

> The Decision Tree is the required classification technique and remains the central model. I
> compare it with a majority baseline and an unconstrained default tree, which can overfit by
> creating rules around small groups and noise.
>
> GridSearchCV tunes criterion, depth and minimum leaf size for AUC. In five-fold CV, the model
> trains on four training-data folds and validates on the fifth, rotating five times. The test set
> remains closed. The selected tree uses Gini, depth 5 and minimum leaf size 20.
>
> The Balanced Tree keeps this structure but makes low-class mistakes more costly. SMOTE creates
> synthetic minority examples only inside training folds. RBF SVM remains a technical benchmark.
> Unlike the trees, the SVM needs feature scaling, so the scaler lives inside the pipeline: it is
> fit only on each fold's training data, and the validation fold never leaks into it. That is the
> same discipline as SMOTE - anything learned from data happens inside the fold.
> The RBF kernel reaches CV AUC 0.826 compared with 0.804 for the linear kernel, using C equal to 1
> and gamma set to scale. This supports a moderately nonlinear boundary, consistent with the
> overlapping classes in the pairplot.
>
> CV is the selection point. The AUC tree fails sensitivity at 0.643. SMOTE fails specificity at
> 0.696. SVM has AUC 0.827 but sensitivity 0.631. Only the Balanced Tree passes every gate: AUC
> 0.787, sensitivity 0.731 and specificity 0.703.

**Transition into Section 5 (say this - it is the other joint that broke take 2):**

> Section 4 ends with the candidates and their cross-validation numbers, and the selection is
> frozen there. Section 5 opens the held-out test set with one job only: confirm the frozen
> choice. It is the final exam, not a second chance to pick.

**Check your understanding:** Describe five-fold CV in your own words. Why is the model with the
highest AUC not automatically approved?

---

## Block 5 - Final Evaluation, XAI and Model Approval (5:55-8:20)

**Screen:** Test metrics, ROC curves, confusion matrices, tree, SHAP and approval table.

**Spoken walkthrough:**

> After freezing the selection from training cross-validation, I open the held-out test set. The
> Balanced Tree confirms AUC 0.792, sensitivity 0.734, specificity 0.725, balanced accuracy 0.729
> and F1 0.669. It meets the criteria defined in Business Understanding.
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
> RBF SVM has the highest test AUC, 0.824. AUC is the probability that a random low sample receives
> a higher risk score than a random high sample; it is not 82.4 percent accuracy. At the current
> threshold, SVM sensitivity is only 0.590, below the operational gate.
>
> I approve only the Balanced Decision Tree for a controlled, human-supervised pilot. It passes all
> gates and exposes inspectable rules. No model is approved for automated release or rejection.
> Alcohol has importance around 0.62, followed by volatile acidity, but importance does not prove
> causation.
>
> I then add SHAP because the tree diagram and feature importance are global views. Global SHAP adds
> direction, while local SHAP explains one prediction. For the selected correctly flagged proxy,
> alcohol contributes plus 0.222 and volatile acidity plus 0.070 toward low quality, producing a
> low-quality probability of 0.797. The additivity check reconstructs the model probability within
> numerical tolerance. SHAP explains the model's reasoning; it does not prove chemical causation.

**Check your understanding:** Explain AUC without saying "accuracy". Explain the 58 versus 69
trade-off as if speaking to a quality-control manager.

---

## Block 6 - Deployment, Monitoring and Lessons (8:20-9:40)

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

## Block 7 - Closing (9:40-9:55)

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

1. Read the entire detailed script aloud once, slowly.
2. Explain every Portuguese checkpoint without looking at the answer.
3. Rehearse the four scripted transitions (Blocks 2→3, 3→4, 4→5 and the 398 derivation) until
   they come out without reading - these are exactly where take 2 broke.
4. Record one audio-only attempt from memory, with a stopwatch: note the time at the end of
   each block against its window. Over by 15 seconds means cut commentary, never numbers.
5. Rehearse notebook scrolling with the shorter `assessment2-walkthrough.md`.
6. Record the final video conversationally; use this detailed script only if you lose the thread.
