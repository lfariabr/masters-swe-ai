<!--
DLE602 Assessment 3 - Deep Learning Final Project Report - v3 Markdown source
Brief requirement: 1,500 words (+/-10%), i.e. 1,350-1,650 words, Report and Source Code.
The declared count covers prose and list items in Sections 1-6 only. It excludes headings, cover details,
the Table of Contents, Markdown table contents and captions, references and appendices.
Reproducible count: select from "## 1. Project Evolution" through the line before "## 7. References";
remove headings, fenced Mermaid blocks, Markdown table rows, image rows, captions, separators and the word-count declaration;
strip Markdown emphasis markers; then apply whitespace-token counting (`wc -w`).
Canonical four-model source: review-pulse commit bf36c3b3.
Supplemental six-model sources: artifact commit cef08fa and evaluation commit 941148c, merged in 0f02be3.
Release packaging and Git LFS deployment source: merged PR #101, commit 0ef3a26.
Reviewed ReviewPulse baseline for this report: commit 49395f5 (merged PR #117).
No result below is invented or illustrative.
-->

# ReviewPulse v3.0: Aspect-Based Sentiment Analysis - Implementation Report

**Subject:** DLE602 Deep Learning - Assessment 3: Deep Learning Final Project<br>
**Group members:** Luis Guilherme de Barros Andrade Faria (A00187785); Victor Javier Dorantes Meneses (A00179705); Juan Sebastian Martinez Contreras (A00167145)<br>
**Project:** ReviewPulse v3.0<br>
**Repository:** [lfariabr/review-pulse](https://github.com/lfariabr/review-pulse)<br>
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
8. Appendix A - Supplemental Six-Model Track
9. Appendix B - Project Delivery Record
10. Appendix C - Reproduction Commands
11. Appendix D - Future Expansion Roadmap
12. Appendix E - Application Acceptance Evidence
13. Appendix F - Independent Reproduction Record
14. Academic Integrity Declaration
15. Statement of Acknowledgement

---

## 1. Project Evolution, Problem, Aim and Research Questions

ReviewPulse began in ISY503 as a review-level binary sentiment classifier: v1.0 established the classical pipeline and v2.x hardened the application and added a Transformer option. Those releases assign one label to a whole review and therefore average away mixed opinions. DLE602 v3.0 implements aspect-based sentiment analysis (ABSA), so *"the food was great but the service was slow"* can produce separate labels for `food` and `service`. This report evaluates the completed implementation against the research questions established in Assessment 2, using
  only newly generated DLE602 results rather than checkpoints or metrics from the earlier ISY503 project.

```mermaid
flowchart LR
    V1["ReviewPulse v1.0<br/>ISY503"] --> V2["ReviewPulse v2.x<br/>ISY503"]
    V2 --> V3["ReviewPulse v3.0<br/>DLE602"]
    V1 --- C1["Binary review sentiment<br/>TF-IDF + BiLSTM"]
    V2 --- C2["Hardened review sentiment<br/>+ DistilBERT"]
    V3 --- C3["Three-class aspect sentiment<br/>six-model ABSA comparison"]
```

*Figure 1. ReviewPulse evolved from one binary label per Amazon review to one three-class prediction per supplied restaurant aspect.*

**Aim.** Implement and critically evaluate a low-compute ABSA system on SemEval-2014 Restaurants, testing whether explicit aspect conditioning improves sentiment classification, comparing ATAE-LSTM with DistilBERT, and presenting indicative token-level evidence.

**Research questions.** RQ1: does aspect conditioning improve classification on multi-aspect sentences over target-agnostic baselines? RQ2: how do ATAE-LSTM and DistilBERT compare on accuracy, macro-F1 and efficiency? RQ3: what human-readable evidence do attention or attribution outputs provide?

## 2. Requirements and Scope

The submitted four-model ladder comprises TF-IDF, a target-agnostic LSTM, ATAE-LSTM and DistilBERT. All models use the official Restaurants test split, the fixed label order `negative`, `neutral`, `positive`, and one evaluation contract covering accuracy, macro-F1, per-class metrics, confusion matrices, a mixed-polarity multi-aspect subset, training time, inference latency and artifact size. A separate `predict_aspects(review, aspects, model_name)` API and Streamlit v3 page expose ABSA without widening the legacy `predict_sentiment()` contract.

Reproducibility requirements include fixed seeds, sentence-grouped leakage-safe development splits, development macro-F1 checkpoint selection, early stopping and restoration of the best neural checkpoint. The implementation persists configuration, training history and provenance with each artifact. Invalid input, unavailable checkpoints and unsupported evidence views produce explicit errors or states rather than silent fallback.

Automatic aspect extraction, Topic Modelling and Laptops transfer remain outside the implemented core. A target-agnostic GRU and review-only TextCNN were completed only after the four-model gates passed. They are reported as exploratory controls in Appendix A and do not retroactively redefine the Assessment 2 experiment.

## 3. Data and Implementation Method

The dataset is SemEval-2014 Task 4 Restaurants (Pontiki et al., 2014). The reproducible audit in Table 1 found 105 original `conflict` annotations: 91 in training and 14 in the official test data. All were counted before exclusion from the three-class task.

| Split | Original aspect instances | Positive | Negative | Neutral | Excluded `conflict` | Retained three-class instances |
|---|---:|---:|---:|---:|---:|---:|
| Train | 3,693 | 2,164 | 805 | 633 | 91 | 3,602 |
| Official test | 1,134 | 728 | 196 | 196 | 14 | 1,120 |
| **Total** | **4,827** | **2,892** | **1,001** | **829** | **105** | **4,722** |

*Table 1. SemEval Restaurants audit before three-class filtering; all annotated offsets were valid.*

The official test set therefore contains 1,120 retained aspect instances. Of these, 228 instances across 80 sentences form the **mixed-polarity multi-aspect subset**: sentences with at least two retained gold aspects carrying different polarities. This analytical subset is distinct from the removed SemEval `conflict` label.

Development data is derived from the official training partition using seed 42 and grouped by `sentence_id` before sentences are expanded into aspect instances. Consequently, aspects from one sentence cannot leak across training and development. The deterministic grouped split contains 2,875 training and 727 development instances. It is not formally class-stratified; instead, label distributions are recorded and audited after grouping. Raw review text and annotated character offsets remain the alignment source; model-specific tokenisation occurs only after offset validation.

TF-IDF with Logistic Regression is the classical review-only baseline. A three-class bidirectional LSTM adds learned embeddings and recurrence while still receiving only the review, following the target-independent control motivated by target-dependent LSTM research (Tang et al., 2016). ATAE-LSTM adds an aspect embedding and aspect-conditioned attention (Wang et al., 2016). DistilBERT, a distilled pretrained Transformer (Sanh et al., 2019), is fine-tuned as a `(review, aspect)` sentence-pair classifier following the auxiliary-sentence ABSA formulation of Sun, Huang and Qiu (2019).

The neural trainers use Adam or AdamW, configured regularisation, development macro-F1 selection, patience-based early stopping and best-checkpoint restoration. Canonical ATAE-LSTM training used CPU, while DistilBERT used Apple MPS. Because the hardware differs, training and latency observations describe the executed environment; they are not a controlled hardware benchmark.

ATAE-LSTM exposes its learned attention distribution. DistilBERT evidence uses gradient × input attribution for the predicted class, aggregates wordpieces onto exact visible spans, and excludes special and aspect-sequence tokens. Both methods return aligned tokens, offsets and normalised within-view scores. Review-only models explicitly report token evidence as unsupported.

```mermaid
flowchart LR
    XML["SemEval Restaurants XML"] --> AUDIT["Parse, audit and validate offsets"]
    AUDIT --> SPLIT["Sentence-grouped train/dev<br/>+ official test"]
    SPLIT --> R["Review only"]
    SPLIT --> RA["Review + aspect"]
    R --> BASE["TF-IDF · LSTM · GRU · TextCNN"]
    RA --> COND["ATAE-LSTM · DistilBERT"]
    BASE --> EVAL["Shared three-class evaluation"]
    COND --> EVAL
    COND --> EVID["Indicative token evidence"]
    EVAL --> APP["predict_aspects API + Streamlit v3"]
    EVID --> APP
```

*Figure 2. ReviewPulse v3 data, model-input and delivery flow. GRU and TextCNN are exploratory review-only controls.*

The Streamlit workflow accepts one review and comma-separated manual aspects. It validates and de-duplicates the list, preserves input order and scores each aspect independently. A sample generator supports repeatable demonstrations. Missing artifacts, empty reviews, empty aspect lists and unknown models surface controlled messages, allowing the same interface to demonstrate both successful inference and predictable failure handling.

Implementation is separated into data, model, training, inference, evaluation and presentation modules under `src/absa`, with model adapters enforcing one prediction payload. Automated tests cover parsing and split leakage, trainer controls, artifact provenance, all six inference paths, exact evidence offsets, safe heatmap rendering, packaging and legacy compatibility. At the merged release-package baseline, the complete local suite records 363 passing tests and three expected skips. Appendix C identifies the commands that regenerate the documented evidence.

## 4. Deep Learning Principles Applied

The model ladder isolates a principle at each stage. TF-IDF uses sparse engineered features and acts as a classical control. The LSTM introduces distributed representations and bidirectional recurrence, which model sequential context but still create the same review representation for every aspect. This deliberately exposes why representation learning alone cannot resolve contradictory labels attached to identical review input.

ATAE-LSTM conditions the recurrent representation on an aspect embedding and learns a weighted combination of hidden states. It can therefore read the same sentence differently for `food` and `service`. DistilBERT transfers contextual knowledge from BERT-style pretraining (Devlin et al., 2019) and allows review and aspect tokens to interact throughout the Transformer encoder. Its substantially larger parameter count tests whether pretrained contextual transfer justifies additional compute and storage.

Dropout and weight decay limit overfitting; early stopping and best-checkpoint restoration prevent reporting a convenient final epoch instead of the best observed development checkpoint. The fixed test split, label order and metric implementation support comparison of predictive behaviour. They do not, however, make cross-device timing controlled, nor does one fixed seed establish variance across retraining.

Attention and gradient attribution are treated as diagnostic views rather than model reasoning. Attention can vary without changing a prediction and need not identify causal features (Jain & Wallace, 2019). Accordingly, ReviewPulse labels darker tokens as higher-scored evidence within one aspect view and makes no claim that the view faithfully explains the decision.

## 5. Results and Critical Analysis

**Table 2** reports the canonical four-model experiment on the shared official test set.

| Model | Test accuracy | Test macro-F1 | Mixed accuracy | Mixed macro-F1 | Training | Warm ms/example | Artifact |
|---|---:|---:|---:|---:|---:|---:|---:|
| TF-IDF review-only | 0.7018 | 0.4605 | 0.4430 | 0.3319 | 0.14 s | 0.009 | 0.77 MB |
| LSTM review-only | 0.6687 | 0.4326 | 0.4167 | 0.3264 | 9.32 s | 0.103 | 2.25 MB |
| ATAE-LSTM | 0.6438 | 0.4799 | **0.4737** | **0.4491** | 14.17 s | 0.128 | 2.64 MB |
| DistilBERT sentence-pair | **0.8259** | **0.7231** | **0.6623** | **0.6427** | 133.65 s | 3.506 | 256.11 MB |

*Table 2. Canonical four-model comparison: 1,120 test instances and 228 mixed-polarity instances, commit `bf36c3b3`. Timing is observational across CPU and MPS.*

![Four canonical model confusion matrices](assets/four-model-confusion-matrices.png)

*Figure 3. Full-test confusion matrices generated by the canonical #84 evaluation runner at commit `bf36c3b3`; rows are gold labels and columns are predictions.*

**RQ1.** Both aspect-conditioned models outperform both review-only neural and classical controls on mixed-polarity accuracy and macro-F1. Against the review-only LSTM, DistilBERT gains 24.6 percentage points of mixed accuracy and 31.6 points of mixed macro-F1. ATAE-LSTM gains 5.7 and 12.3 points respectively. Four-model error analysis found 61 mixed cases where both aspect-conditioned models were correct and both review-only models were wrong, against four in the reverse direction. The result supports the benefit of explicit aspect input specifically where identical review text carries opposing labels.

**RQ2.** DistilBERT leads every predictive metric, but its 256.11 MB artifact is almost 100 times ATAE-LSTM's 2.64 MB artifact. ATAE-LSTM is weaker on full-test accuracy than TF-IDF and the LSTM, yet stronger on mixed macro-F1 and neutral-class discrimination. This is an important negative result: lightweight attention improves the target-sensitive behaviour central to RQ1 without guaranteeing higher aggregate accuracy. DistilBERT took longer and had higher latency in the recorded runs, but numerical timing ratios are not interpreted as architectural speedups because it ran on MPS while ATAE-LSTM ran on CPU.

The class-level results in Table 3 expose the positive-class dominance hidden by accuracy. DistilBERT leads all three classes, while every smaller model performs substantially worse on neutral examples. ATAE-LSTM nevertheless provides the strongest neutral F1 among the lightweight neural models.

| Model | Negative F1 | Neutral F1 | Positive F1 |
|---|---:|---:|---:|
| TF-IDF review-only | 0.3827 | 0.1794 | 0.8195 |
| LSTM review-only | 0.3605 | 0.1322 | 0.8053 |
| ATAE-LSTM | 0.3759 | **0.2888** | 0.7749 |
| DistilBERT sentence-pair | **0.7772** | **0.4931** | **0.8991** |

*Table 3. Full-test per-class F1 from the canonical four-model evaluation; bold identifies the overall best and the strongest lightweight neutral result.*

**Table 4** presents the verified report example used to answer RQ3.

| Model / aspect | Prediction | Confidence | Highest-scored visible tokens |
|---|---|---:|---|
| ATAE-LSTM / food | positive | 86.4% | `Great` 0.241; `food` 0.131; `was` 0.127 |
| ATAE-LSTM / service | positive | 74.2% | `Great` 0.193; `!` 0.132; `dreadful` 0.130 |
| DistilBERT / food | negative | 82.7% | `dreadful` 0.288; `the` 0.163; `service` 0.151 |
| DistilBERT / service | negative | 91.3% | `dreadful` 0.488; `food` 0.095; `service` 0.095 |

*Table 4. Indicative evidence for “Great food but the service was dreadful!” from the verified #85 export. Gold labels are food-positive and service-negative.*

**RQ3.** The evidence changes with the supplied aspect, but neither model resolves both gold labels in this example. ATAE-LSTM predicts both aspects positive; DistilBERT predicts both negative. Some high-scored tokens are sentiment-bearing, while others are function words or belong to the opposite aspect. The visualisation is therefore useful for inspecting model sensitivity and diagnosing errors, not for claiming a faithful or causal explanation.

Across the canonical test set, the four models disagree on 428 instances and all miss 134. These counts demonstrate complementary predictions and shared failures, but the present experiment does not categorise those failures by linguistic phenomenon. Appendix A shows that adding GRU and TextCNN does not overturn the conclusion: neither review-only extension closes the mixed-polarity gap.

## 6. Limitations and Conclusion

The 228-instance mixed subset is comparatively small, and results come from one frozen seed rather than a multi-seed distribution. Apple MPS can remain nondeterministic despite seed control, so provenance identifies exact commits and a shared prediction hash rather than promising bit-identical retraining. Gold aspect terms are supplied manually in the application; automatic extraction and cross-domain Laptops evaluation are unimplemented. Evidence scores are model-specific and normalised within each view, so they should not be compared as absolute importance across models or examples.

ReviewPulse v3.0 nevertheless answers the submitted questions with measured implementation evidence. Explicit aspect conditioning materially improves classification on the mixed-polarity subset. DistilBERT provides the strongest predictions at substantially greater storage cost, while ATAE-LSTM offers a small aspect-aware alternative with stronger mixed-polarity behaviour than the review-only controls. Its attention and DistilBERT attribution provide indicative token-level evidence, not exposed reasoning. The completed GRU and TextCNN extensions reinforce rather than change this result. Next research steps are multi-seed uncertainty estimates, controlled same-device efficiency measurement, cross-domain evaluation and automatic aspect extraction; the remaining delivery step is the reproducible v3.0.0 submission package.

**Word count (Sections 1-6 prose and list items): 1,550 words.**

## 7. References

Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *Proceedings of NAACL-HLT 2019*, 4171-4186. https://aclanthology.org/N19-1423/

Jain, S., & Wallace, B. C. (2019). Attention is not explanation. *Proceedings of NAACL-HLT 2019*, 3543-3556. https://aclanthology.org/N19-1357/

Pontiki, M., Galanis, D., Pavlopoulos, J., Papageorgiou, H., Androutsopoulos, I., & Manandhar, S. (2014). SemEval-2014 Task 4: Aspect based sentiment analysis. *Proceedings of SemEval 2014*, 27-35. https://aclanthology.org/S14-2004/

Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). DistilBERT, a distilled version of BERT: Smaller, faster, cheaper and lighter. *Proceedings of the 5th Workshop on Energy Efficient Machine Learning and Cognitive Computing*. https://arxiv.org/abs/1910.01108

Sun, C., Huang, L., & Qiu, X. (2019). Utilizing BERT for aspect-based sentiment analysis via constructing auxiliary sentence. *Proceedings of NAACL-HLT 2019*, 380-385. https://aclanthology.org/N19-1035/

Tang, D., Qin, B., Feng, X., & Liu, T. (2016). Effective LSTMs for target-dependent sentiment classification. *Proceedings of COLING 2016*, 3298-3307. https://aclanthology.org/C16-1311/

Wang, Y., Huang, M., Zhu, X., & Zhao, L. (2016). Attention-based LSTM for aspect-level sentiment classification. *Proceedings of EMNLP 2016*, 606-615. https://aclanthology.org/D16-1058/

## 8. Appendix A - Supplemental Six-Model Track

The supplemental evaluation preserves the four-model experiment and adds target-agnostic GRU and TextCNN records generated under the shared six-model contract. It uses artifact source commit `cef08fa`, evaluation source commit `941148c`, seed 42, prediction SHA-256 `9d439207a8fdcafed5328d513ee4921bfc8b0dc4ecefcb3e7a9622f66f40e196` and the same 1,120 test instances.

| Model | Scope | Test accuracy | Test macro-F1 | Mixed accuracy | Mixed macro-F1 | Training | Artifact |
|---|---|---:|---:|---:|---:|---:|---:|
| TF-IDF | A2 core | 0.7018 | 0.4605 | 0.4430 | 0.3319 | 0.14 s | 0.77 MB |
| LSTM | A2 core | 0.6687 | 0.4326 | 0.4167 | 0.3264 | 8.07 s | 2.25 MB |
| GRU | Exploratory | 0.6750 | 0.4603 | 0.4079 | 0.3156 | 7.02 s | 2.02 MB |
| TextCNN | Exploratory | 0.6893 | 0.4498 | 0.4167 | 0.3106 | 25.13 s | 1.81 MB |
| ATAE-LSTM | A2 core | 0.6438 | 0.4799 | 0.4737 | 0.4491 | 10.84 s | 2.64 MB |
| DistilBERT | A2 core | **0.8250** | **0.7199** | **0.6667** | **0.6473** | 122.08 s | 256.11 MB |

*Table A1. Frozen supplemental six-model comparison. The five smaller models ran on CPU and DistilBERT on MPS; timing is observational.*

GRU uses 10.31% fewer parameters than LSTM and obtains slightly higher full-test macro-F1, but lower mixed macro-F1. TextCNN records zero neutral F1 on the mixed subset. These negative results show that changing the review-only encoder does not supply the missing aspect information. In the shared six-model predictions, 55 mixed cases are correct for both aspect-conditioned models and wrong for all selected review-only models, versus three in the reverse direction; 454 instances contain disagreement and all six models miss 131.

## 9. Appendix B - Project Delivery Record

### Implemented risk outcomes

| Risk | Mitigation applied | Observed outcome / contingency |
|---|---|---|
| Neural overfitting | Development early stopping and best-checkpoint restoration | Selected epoch, history and diagnostic persisted per model |
| Transformer compute/storage | Apple MPS training and explicit artifact measurement | Strongest model, but 256.11 MB; lightweight ATAE remains available |
| Sentence leakage | Group development split by `sentence_id` | Automated disjointness checks pass |
| Artifact loading failure | Explicit paths, validation and controlled UI errors | Missing models fail visibly rather than changing model silently |
| Optional-scope delay | Four-model result frozen before GRU/CNN activation | Six-model track completed without replacing the canonical experiment |
| Unequal contribution | Issue ownership, pull-request review and contribution record | Juan delivered independent Streamlit QA in PR #120; Victor's reproduction remains pending, and only evidenced work is claimed |

*Table B1. Implemented project-risk mitigations, observed outcomes and retained contingencies.*

### Contribution log

| Contributor | Status | Contribution / assigned validation | Evidence / hand-off |
|---|---|---|---|
| Luis Faria | Completed | Architecture, ABSA implementation, all training/evaluation integration, token evidence, six-model integration, Streamlit integration, Git LFS deployment, release packaging and report consolidation | ReviewPulse PRs #90, #92, #93, #97, #98-#102; academic commits `f3b7247`, `6d50ac0` |
| Victor Dorantes | Assigned 29 Jul; evidence pending | Independently reproduce the constrained installation/tests, validate RQ1/RQ2 results and verify the cited publications | Required evidence: `validation-victor.md`, commands/results and a reviewed PR; summarised in Appendix F |
| Juan Martinez | Independent QA delivered; corrective review in progress | Executed 12 deployed-Streamlit cases across all six models, multi-aspect inputs, sample generation, evidence views, invalid inputs, model switching and v2/v3 compatibility; recorded predictions, screenshots and five behaviours requiring triage/retest | ReviewPulse PR #120, merge commit `1e6689f`; `docs/dle602-a3/validation-juan.md`; companion screenshot record; selected evidence mapped in Appendix E |

*Table B2. Contribution status, assigned validation work and required traceable evidence.*

Assignments are not treated as completed contributions. Juan's executed QA is recorded as an evidenced contribution even where it exposes failures rather than confirming acceptance. Victor remains pending until his reproduction record is submitted and reviewed.

## 10. Appendix C - Reproduction Commands

The restricted SemEval XML files must be acquired separately and placed as documented in the repository. From the verified environment:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt -c constraints-a3.txt
git lfs pull
.venv/bin/python -m pytest -q
.venv/bin/python -m src.absa.data.audit
.venv/bin/python -m src.absa.evaluation.runner --device auto
.venv/bin/python scripts/export_absa_evidence.py
.venv/bin/streamlit run app.py
```

The frozen supplemental evaluation is regenerated by adding
`--models tfidf target_lstm target_gru text_cnn atae_lstm distilbert` to the evaluation command after the six verified artifacts are available.

## 11. Appendix D - Future Expansion Roadmap

ReviewPulse v3.0 is intentionally an academic comparison environment rather than a production platform. Its six-model ladder, manual gold-aspect input and Streamlit interface make the research questions inspectable, but the same design should not be scaled by simply running every model for every incoming review. Future releases would separate experimental benchmarking from the smaller set of models selected for operational inference.

| Release scenario | Primary objective | Candidate capabilities | Architectural direction |
|---|---|---|---|
| v3.1 - Reproducible service | Harden the existing ABSA workflow without changing its research scope | Three-class probability distributions, confidence calibration, abstention thresholds, CSV/JSON export, batch requests, latency/load tests and model-version metadata | Retain Streamlit as the demonstration client and introduce a versioned inference API |
| v4.0 - Aspect intelligence | Remove the requirement for users to know and enter every aspect | Automatic aspect extraction, user correction, synonym/category normalisation, batch review analysis and emerging-topic discovery | Add an extraction pipeline, persistent result store and analyst dashboard |
| v5.0 - Operational monitoring | Analyse feedback continuously rather than through isolated submissions | Review-platform connectors, scheduled ingestion, trend analysis, alerts, feedback capture, drift monitoring and domain-specific retraining | Add asynchronous jobs, inference workers, PostgreSQL/object storage and observability |
| Later SaaS/enterprise track | Support multiple organisations and governed use | Tenant isolation, authentication, role-based access, audit logs, retention controls, personal-data handling and usage limits | Separate web, API, worker and storage tiers; scale workers independently |

*Table D1. Prospective ReviewPulse release scenarios; listed capabilities are planned rather than part of the evaluated v3.0 implementation.*

For v3.1, **FastAPI** is the preferred default because the immediate requirement is a small typed HTTP layer around the existing `predict_aspects` and comparison services. Streamlit could remain the visible client while the API provides explicit request schemas, model-version responses and machine-readable errors for batch or third-party consumers. Model execution is compute-bound, so an asynchronous web endpoint alone would not create inference capacity; batch work should instead move through a bounded queue and independently scalable workers.

**Django with Django REST Framework** becomes the stronger alternative if v3.1 is deliberately widened to include user accounts, administrative workflows, permissions, persistent business records or early multi-tenancy. Adopting Django only for model endpoints would add product infrastructure before it is required. The decision is therefore based on release scope: FastAPI for an inference-first service, or Django/DRF when application management becomes a first-class requirement.

```mermaid
flowchart LR
    CLIENTS["Streamlit, batch client or future web UI"] --> API["Versioned service layer<br/>FastAPI initially<br/>Django/DRF if product workflows require it"]
    API --> LIVE["Bounded synchronous inference"]
    API --> QUEUE["Batch and scheduled job queue"]
    LIVE --> WORKERS["Selected production model workers"]
    QUEUE --> WORKERS
    REGISTRY["Versioned artifacts and provenance"] --> WORKERS
    WORKERS --> STORE["Predictions, feedback and metrics store"]
    STORE --> OUTPUTS["Dashboard, exports, trends and alerts"]
```

*Figure D1. Prospective service evolution; these components are not claimed as part of the evaluated v3.0 implementation.*

The model strategy would also change with scale. TF-IDF, LSTM, GRU and TextCNN remain useful controls for research and regression detection, while operational traffic would normally use one validated aspect-conditioned model, with a second model retained only when its cost, latency or diagnostic value justifies deployment. Cross-domain use in e-commerce, hospitality, software support or other sectors would require new representative data and domain-specific evaluation rather than assuming that Restaurants performance transfers unchanged.

## 12. Appendix E - Application Acceptance Evidence

**Owner: Juan Martinez.** This appendix records what the running application actually showed an independent group tester. It complements the automated suite rather than repeating it: automated tests verify payload and offset contracts, while Juan's screenshots record the deployed interface, model outputs and failure states visible to a user.

Juan executed 12 authenticated Streamlit cases covering all six models, multi-aspect input, sample generation, model switching, attention and attribution, invalid inputs and v2/v3 compatibility. The initial record contained five passes, two passes with observation and five failures requiring technical triage or retest. A wrong model prediction was treated as a model-quality observation; behaviour contradicting a UI acceptance criterion was treated as a failure.

The complete case record is kept as `docs/dle602-a3/validation-juan.md` in the ReviewPulse repository and was introduced through PR #120. Rather than reproducing all 12 cases, the final appendix selects four captures that demonstrate the breadth and critical value of the validation.

| Figure | Selected evidence | Source evidence |
|---|---|---|
| E1 | Model selector and successful deployed inference confirming availability of the six-model ladder | EV-01 and EV-02 |
| E2 | Separate aspect results for the mixed-polarity `food`/`service` example, including the observed model-quality errors | EV-03A and EV-03B |
| E3 | Side-by-side ATAE-LSTM attention and DistilBERT attribution views used to assess aspect sensitivity and visible-token alignment | EV-07 and EV-08 |
| E4 | Controlled invalid-input state showing the exact user-facing message and the stale-state observation raised during QA | EV-10 and EV-11 |

*Table E1. Four report-facing captures selected from Juan's complete 12-case validation record.*

Attention and attribution captions will repeat that the evidence is indicative rather than causal. Failed cases remain visible because independent QA that identifies a release risk is stronger evidence than a selectively green demonstration. Anonymous public access was outside Juan's authenticated session and remains a separate release gate.

<!-- FINAL ASSET IMPORT: export four readable captures or composites from Juan's companion Word evidence record into report/assets/ using stable e1-e4 filenames. Insert each image with a one-sentence caption, and do not render an empty image placeholder if an asset is unavailable. -->

## 13. Appendix F - Independent Reproduction Record

**Owner: Victor Dorantes.** This appendix records a second person reproducing the reported results from the repository alone, on a machine that is not the development machine. Its purpose is to establish that the numbers in Section 5 are properties of the artifacts and instructions rather than of one local environment.

The full record, including the exact commands, console output and machine specification, is kept as `docs/dle602-a3/validation-victor.md` in the ReviewPulse repository and merged through a reviewed pull request. This appendix carries the summary.

| Check | Expected | Observed | Result |
|---|---|---|---|
| F1. Constrained installation | `pip install -r requirements.txt -c constraints-a3.txt` succeeds with no undocumented manual step | | Pending |
| F2. Artifact retrieval | `git lfs pull` materialises all six artifacts; `git lfs ls-files -s` shows no unresolved pointer | | Pending |
| F3. Test suite | Clean clone reports 357 passed and 9 skipped; the skips are the documented licensed-data absences | | Pending |
| F4. Offline smoke | `scripts/smoke_absa.py` returns one prediction per aspect with no SemEval data present | | Pending |
| F5. Dataset audit | Official retained test count 1,120; mixed-polarity subset 228 instances across 80 sentences | | Pending |
| F6. Headline results | Table 2 accuracy and macro-F1 reproduce from the shipped artifacts | | Pending |
| F7. Reference verification | Each cited work is checked against the original publication and supports the claim made | | Pending |

*Table F1. Independent reproduction checks, expected values and outcomes.*

Where an observed value differs from the expected value, the difference is recorded as observed and explained rather than adjusted. A reproduction that surfaces a genuine discrepancy is more valuable to this report than one that confirms every figure, and F3 in particular is expected to differ from the development machine by design: the six sample-provenance tests skip wherever the frozen evaluation predictions are absent. Rows that receive no evidence before submission are removed from this appendix rather than published as empty claims.

## 14. Academic Integrity Declaration

We declare that, except where referenced, the work we are submitting for this assessment task is our own work. We have read and are aware of the Academic Integrity Policy and Procedure of Torrens University Australia. We are also aware that we need to keep a copy of all submitted material and any drafts, and we agree to do so.

## 15. Statement of Acknowledgement

We acknowledge that we used the following AI-assisted tools in the creation of this assessment:

- OpenAI Codex
- Anthropic Claude
- CodeRabbit

The tools assisted with scaffolding and reviewing the ABSA implementation, debugging training and evaluation code, checking data-leakage and reproducibility controls, reviewing pull requests, reconciling measured results with their artifacts, improving code documentation and academic clarity, and supporting APA 7th referencing conventions. The cited claims were verified against the original publications, and numerical claims were checked against the frozen ReviewPulse evaluation outputs.

Prompt examples:

1. "Review the shared four-model ABSA evaluation: verify that all models use the official Restaurants test split and that the mixed-polarity subset is computed from gold annotations without confusing it with the SemEval conflict label."
2. "Inspect the DistilBERT, ATAE-LSTM and target-LSTM training loops for device handling, repeated loss construction, seed control, early stopping and best-checkpoint restoration, then propose tests for any regression."
3. "Reconcile the A3 implementation report with the frozen four-model and six-model artifacts, correct unsupported efficiency claims, and keep attention and gradient attribution framed as indicative rather than causal evidence."

We confirm that these tools were used in accordance with the Torrens University Australia Academic Integrity Policy and the TUA, Think and MDS Position Paper on the Use of AI. The group retains responsibility for the final implementation, analysis, synthesis and content of this assessment.
