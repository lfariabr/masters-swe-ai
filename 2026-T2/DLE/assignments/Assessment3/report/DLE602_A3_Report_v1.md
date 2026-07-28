<!--
DLE602 Assessment 3 - Deep Learning Final Project Report - v1 Markdown source
Brief requirement: 1,500 words (+/-10%), i.e. 1,350-1,650 words, Report and Source Code.
Body target here follows the six-section budget from REVIEWPULSE_V3_EPIC.md Section 14 (~1,500 words total).
The declared count covers prose and list items in Sections 1-6 only; it excludes headings, cover details,
the Table of Contents, figure/table captions and contents, references and appendices.
Reproducible count: select from "## 1. Project Evolution" through the line before "## 7. References";
remove headings, Markdown table rows, captions, separators and the declaration; strip Markdown emphasis
markers; then apply whitespace-token counting (`wc -w`). Result: 1,459.
Data source: all figures below are read from the committed review-pulse artifacts at commit bf36c3b3
(outputs/absa/evaluation/results.json, comparison.md, error_analysis.json; outputs/absa/*_metrics.json;
docs/dle602-a3/target-gru.md). No number in this report is invented or illustrative.
-->

# ReviewPulse v3.0: Aspect-Based Sentiment Analysis - Implementation Report

**Subject:** DLE602 Deep Learning - Assessment 3: Deep Learning Final Project<br>
**Group members:** Luis Guilherme de Barros Andrade Faria (A00187785); Victor Javier Dorantes Meneses (A00179705); Juan Sebastian Martinez Contreras (A00167145)<br>
**Project name:** ReviewPulse v3.0<br>
**Repository:** [lfariabr/review-pulse](https://github.com/lfariabr/review-pulse), evaluation commit `bf36c3b3`<br>
**Learning facilitator:** Dr Tayab Din Memon<br>
**Date:** August 2026

---

## Table of Contents

1. Project Evolution, Problem, Aim and Research Questions
2. Requirements and Scope
3. Data and Implementation Method
4. Deep Learning Principles Applied
5. Results and Critical Analysis
6. Limitations and Conclusion
7. References
8. Appendix A - Optional Exploratory Track (GRU/CNN)
9. Statement of Acknowledgement

---

## 1. Project Evolution, Problem, Aim and Research Questions

ReviewPulse began in ISY503 (v1.0.0) as a review-level binary classifier over Amazon reviews, then hardened its architecture and added DistilBERT in v2.x. Both versions reduce a whole review to one label. Assessment 2 proposed **ReviewPulse v3.0**: an aspect-based sentiment analysis (ABSA) system answering *"the food was great but the service was slow"* with two opposite, correctly attributed labels instead of one averaged verdict. This report covers the implementation, not the proposal: it presents the system actually built and the evidence actually measured against the same research questions submitted in A2.

**Aim.** Implement and critically evaluate a low-compute ABSA system on SemEval-2014 Restaurants, measuring whether explicit aspect conditioning improves sentiment classification, comparing ATAE-LSTM against DistilBERT, and producing indicative token-level evidence.

**Research questions.** RQ1: does aspect conditioning improve classification on multi-aspect sentences over target-agnostic baselines? RQ2: how do ATAE-LSTM and DistilBERT compare on accuracy, macro-F1 and efficiency? RQ3: what human-readable evidence do attention or attribution outputs provide?

## 2. Requirements and Scope

The implementation delivers the four-model ladder submitted in A2 (TF-IDF, target-agnostic LSTM, ATAE-LSTM, DistilBERT) against one shared contract: identical official test split, identical three-class label order, one evaluation runner producing accuracy, macro-F1, per-class metrics, confusion matrices, the mixed-polarity multi-aspect subset, and efficiency evidence (training time, cold/warm latency, artifact size). A separate `predict_aspects(review, aspects, model_name)` API and Streamlit v3 workflow expose the models without widening the legacy `predict_sentiment()` contract used by ISY503. Reproducibility is a first-class requirement: fixed seeds, sentence-grouped leakage-safe splits, development-set early stopping and best-checkpoint restoration, with configuration and history persisted alongside every checkpoint.

Three items were deliberately scoped out of the core evaluation: automatic aspect extraction, Topic Modelling and Laptops cross-domain transfer remain unimplemented stretch goals, as agreed in A2. A GRU and a CNN variant were added afterward as an *optional* exploratory track, gated behind the core four-model result and reported separately (Appendix A) rather than retrofitted into the submitted comparison.

## 3. Data and Implementation Method

The dataset is SemEval-2014 Task 4 Restaurants (Pontiki et al., 2014). The official test partition contains 1,120 retained aspect instances after excluding the original `conflict` label from the three-class task; 228 of those instances, spanning 80 sentences, form the **mixed-polarity multi-aspect subset**, the analytical evidence that RQ1 actually depends on. Development data is a fixed-seed split of the official training data, grouped by `sentence_id` before expansion into aspect instances, so no sentence contributes examples to two partitions.

Four models share this data under one evaluation command. TF-IDF and Logistic Regression form the review-only classical baseline. A three-class, review-only bidirectional LSTM (embedding 100, hidden 128 per direction, dropout 0.5) tests whether recurrence alone closes the aspect gap. ATAE-LSTM (Wang et al., 2016) adds an aspect embedding and aspect-conditioned attention over the same recurrent backbone, exposing per-token attention weights. DistilBERT is fine-tuned as a sentence-pair classifier following Sun, Huang and Qiu's (2019) auxiliary-sentence formulation, encoding `(review, aspect)` jointly through `distilbert-base-uncased`.

All three neural trainers apply the same reproducibility protocol: seed 42, Adam/AdamW optimisation, development macro-F1 checkpoint selection, patience-2 early stopping and restoration of the best epoch before test evaluation. ATAE-LSTM trained 8 epochs on CPU (14.17 s); DistilBERT trained 2 epochs on Apple MPS (133.65 s), improving development macro-F1 from 0.609 to 0.675 between epochs with no material overfitting recorded. Every run persists its configuration, epoch history, selected checkpoint and an overfitting diagnostic, so the reported metrics trace back to a specific, inspectable training run rather than a single unverified number.

Token evidence is aligned back to character offsets in the raw review, not to a lowercased or contraction-expanded copy, so the Streamlit v3 app can highlight the exact visible substring the model attended to. TF-IDF and the target-agnostic LSTM instead return an explicit "not supported" evidence status, since a review-only model has no aspect-specific attention to show.

The Streamlit v3 workflow sits alongside the legacy ISY503 page rather than replacing it: a user picks legacy review-level sentiment or DLE602 aspect sentiment, then for the latter enters one review and one or more comma-separated aspects. Each aspect is scored independently through `predict_aspects()`, which validates and de-duplicates the aspect list, calls the selected model once per aspect, and preserves the user's input order. Missing artifacts, empty reviews and unknown model names raise controlled application errors instead of silently falling back to a different model, so a failed load is always visible rather than masked.

## 4. Deep Learning Principles Applied

The four-model ladder was chosen to isolate one deep learning principle at each stage. TF-IDF represents text as sparse, engineered features and therefore has no representation-learning component; it is the classical control. The target-agnostic LSTM introduces **learned distributed representations** and **recurrence**: gated units accumulate context across the sequence and mitigate the vanishing-gradient problem that limits plain RNNs, but the same review representation is reused for every aspect, so it cannot separate opposing opinions in one sentence.

ATAE-LSTM adds an explicit **attention mechanism** conditioned on an aspect embedding (Wang et al., 2016): rather than pooling the recurrent states uniformly, the model learns a weighted sum where weights depend on the target aspect, giving two different reads of the same sentence for "food" and "service". DistilBERT applies **transfer learning** from a large pretrained language model, distilled for lower compute, and reframes ABSA as sentence-pair classification (Sun, Huang & Qiu, 2019) so the aspect participates in self-attention across the whole encoder rather than through a single learned vector.

**Regularisation and optimisation** are applied consistently: dropout (0.5) and weight decay control overfitting in the recurrent models; AdamW's decoupled weight decay regularises DistilBERT's fine-tuning; development-set early stopping with best-checkpoint restoration prevents any model from being reported at an over-trained epoch. These controls make the RQ2 efficiency-versus-accuracy comparison fair: every model is evaluated at its own best generalising checkpoint, not at a fixed epoch count that could favour one architecture arbitrarily.

## 5. Results and Critical Analysis

**Table 1** reports the four canonical models on the shared official test set and the mixed-polarity subset.

| Model | Test accuracy | Test macro-F1 | Mixed accuracy | Mixed macro-F1 | Training | Warm ms/example | Artifact |
|---|---:|---:|---:|---:|---:|---:|---:|
| TF-IDF review-only | 0.7018 | 0.4605 | 0.4430 | 0.3319 | 0.14 s | 0.009 | 0.77 MB |
| LSTM review-only | 0.6687 | 0.4326 | 0.4167 | 0.3264 | 9.32 s | 0.103 | 2.25 MB |
| ATAE-LSTM | 0.6438 | 0.4799 | **0.4737** | **0.4491** | 14.17 s | 0.128 | 2.64 MB |
| DistilBERT sentence-pair | **0.8259** | **0.7231** | 0.6623 | 0.6427 | 133.65 s | 3.506 | 256.11 MB |

*Table 1. Four-model comparison on SemEval-2014 Restaurants (1,120 test examples; 228 mixed-polarity examples across 80 sentences), commit `bf36c3b3`.*

**RQ1** is answered directly by the mixed-polarity columns, the metric this whole project exists to move. Both aspect-conditioned models beat both review-only models on the subset that actually contains opposing opinions: DistilBERT gains 22 points of accuracy and 32 points of macro-F1 over the review-only LSTM on mixed sentences, and ATAE-LSTM gains a smaller but consistent margin over its own review-only counterpart. The error analysis confirms this at the instance level: across all disagreements, aspect-conditioned models correctly resolve 61 mixed-subset cases where both review-only models fail, against only 4 cases in the reverse direction.

**RQ2** is a genuine efficiency-versus-accuracy trade-off, not a clean win. DistilBERT is the strongest model on every accuracy metric but costs roughly 9x ATAE-LSTM's training time, 27x its warm-latency per example, and almost 100x its artifact size. A more critical finding is that ATAE-LSTM's *full-test* accuracy (0.6438) is lower than the review-only LSTM (0.6687) and TF-IDF (0.7018), even though it wins on the mixed subset. Attention conditioning on a comparatively small benchmark appears to trade some full-test accuracy for the aspect-discrimination ability the project actually measures, a nuance the literature review anticipated rather than a contradiction of it.

**RQ3** is illustrated by a genuine disagreement case: for *"Great food but the service was dreadful!"*, ATAE-LSTM's attention concentrates on "Great", "was" and "dreadful" for both aspects yet predicts *positive* for both, including the gold-negative "service" aspect; DistilBERT correctly labels "service" negative but also mislabels "food" negative. Both cases show the caveat in practice: attention and attribution reveal where a model concentrated probability mass, not why it chose an answer, and a model can look at the right words while still deciding wrong.

Across the full test set the four models disagree with each other on 428 aspect instances and agree while all being wrong on 134, evidence that the remaining error is shared difficulty (sarcasm, implicit aspects, short fragments) rather than one model's idiosyncrasy. This distribution supports keeping ATAE-LSTM as the deployed low-compute option: its errors overlap substantially with DistilBERT's, so the accuracy gap is concentrated in genuinely hard cases rather than in cases DistilBERT solves trivially.

## 6. Limitations and Conclusion

The mixed-polarity subset (228 examples) is small enough that single-run metrics carry real sampling variance; only a documented overfitting diagnostic, not multi-seed repetition, currently guards against this. Aspects are gold-provided rather than automatically extracted, and even the best model (DistilBERT) still mislabels aspects in the same sentence inconsistently, showing aspect-conditioning is a genuine improvement rather than a solved problem. The optional GRU/CNN track is intentionally partial at time of writing: GRU has an exploratory, matched-control result against the LSTM alone (Appendix A); CNN and the unified six-model comparison remain open.

In summary, the implementation confirms the A2 thesis with measured evidence: explicit aspect conditioning materially improves classification specifically on multi-aspect sentences, DistilBERT is the strongest but most expensive option, and ATAE-LSTM offers an interpretable, low-compute alternative whose attention output is informative but not causal. Future work is the completed six-model comparison and the Streamlit v3 release package.

**Word count (Sections 1-6 prose and list items): 1,459 words.**

## 7. References

Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *Proceedings of NAACL-HLT 2019*, 4171-4186.

Pontiki, M., Galanis, D., Pavlopoulos, J., Papageorgiou, H., Androutsopoulos, I., & Manandhar, S. (2014). SemEval-2014 Task 4: Aspect based sentiment analysis. *Proceedings of SemEval 2014*, 27-35.

Sun, C., Huang, L., & Qiu, X. (2019). Utilizing BERT for aspect-based sentiment analysis via constructing auxiliary sentence. *Proceedings of NAACL-HLT 2019*, 380-385.

Tang, D., Qin, B., Feng, X., & Liu, T. (2016). Effective LSTMs for target-dependent sentiment classification. *Proceedings of COLING 2016*, 3298-3307. https://aclanthology.org/C16-1311/

Wang, Y., Huang, M., Zhu, X., & Zhao, L. (2016). Attention-based LSTM for aspect-level sentiment classification. *Proceedings of EMNLP 2016*, 606-615.

Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253-23260.

## 8. Appendix A - Optional Exploratory Track (GRU/CNN)

Issue #94 added a target-agnostic BiGRU as a matched-control ablation against the review-only LSTM (same embedding/hidden dimensions, dropout, optimiser and split). At matched settings the GRU used 10.31% fewer parameters, trained 17.83% faster and produced a 9.99% smaller artifact, with a slightly higher full-test macro-F1 (0.4603 vs 0.4326) but slightly lower mixed-polarity macro-F1 (0.3156 vs 0.3264). This is a useful negative-boundary result: changing the recurrent cell alone does not resolve the missing-aspect-conditioning limitation that motivates ATAE-LSTM and DistilBERT. The GRU and LSTM candidates were trained from different commits and are not part of Table 1; a Text CNN baseline (#95) and a frozen six-model comparison (#96) remain open work, to be reported only if they pass the same reproducibility gates as the core four models.

## 9. Statement of Acknowledgement

We declare that, except where referenced, the work submitted for this assessment is our own. We have read and are aware of the Torrens University Australia Academic Integrity Policy and Procedure. We are aware that we need to keep a copy of all submitted material and drafts, and will do so accordingly.
