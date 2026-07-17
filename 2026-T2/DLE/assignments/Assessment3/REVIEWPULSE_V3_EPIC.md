# EPIC - ReviewPulse v3.0: Aspect-Based Sentiment Analysis

**Subject:** DLE602 Deep Learning - Assessment 3<br>
**Assessment:** Deep Learning Final Project<br>
**Due:** 19 August 2026, 11:55pm AEST<br>
**Deliverables:** Python source code, execution instructions, submission ZIP and 1,500-word report (+/-10%)<br>
**Project repository:** [lfariabr/review-pulse](https://github.com/lfariabr/review-pulse)<br>
**Academic tracking issue:** [masters-swe-ai #206](https://github.com/lfariabr/masters-swe-ai/issues/206)<br>
**Target release:** `v3.0.0`<br>
**Proposed implementation branch:** `feat/reviewpulse-v3-absa`<br>
**Status at architecture audit (18 July 2026):** The local `main` clone is clean at commit `3880b2e`; tags `v1.0.0` through `v2.3.0` exist; the legacy app, artifacts and modular packages are present; no virtual environment, SemEval data, ABSA branch or ABSA implementation exists yet.

---

## 1. Epic statement

Evolve ReviewPulse from sentence-level binary sentiment classification into a three-class, aspect-based sentiment analysis (ABSA) system. ReviewPulse v3.0 will accept a review and one or more specified aspects, then predict positive, neutral or negative sentiment separately for each aspect. The implementation will compare review-only baselines with aspect-conditioned deep-learning models and expose indicative token-level evidence where the model supports attention or attribution.

The project will reuse the mature engineering foundation from ReviewPulse v1.x/v2.x while introducing a new dataset, prediction unit, label space, model interfaces, evaluation protocol and user workflow for DLE602.

## 2. Product and academic version history

| Phase | Subject | Primary capability | Models | Academic contribution |
|---|---|---|---|---|
| ReviewPulse v1.0 | ISY503 | Binary sentiment for an entire Amazon product review | TF-IDF + Logistic Regression; BiLSTM + GloVe | Built the initial NLP pipeline, neural sequence model, evaluation workflow and Streamlit product |
| ReviewPulse v2.x | ISY503 | Stronger contextual sentence-level classification and production hardening | DistilBERT plus the v1 models | Added transfer learning, improved accuracy, modular packages, artifact loading, automated tests and release discipline |
| ReviewPulse v3.0 | DLE602 | Three-class sentiment for each specified aspect in a review | TF-IDF; target-agnostic LSTM; ATAE-LSTM; DistilBERT sentence pair | Changes the learning task to ABSA and investigates aspect conditioning, attention, contextual transfer, efficiency and indicative interpretability |

### Context paragraph for the A3 report

> ReviewPulse is a phased academic and engineering project. Versions 1.0 and 2.x were developed for ISY503 and addressed binary sentiment classification at review level: v1.0 established TF-IDF and BiLSTM pipelines, while v2.x added DistilBERT and hardened the reusable application architecture. DLE602 Assessment 3 introduces ReviewPulse v3.0, which changes the task itself from one label per review to three-class sentiment for each specified aspect. Although v3.0 reuses tested infrastructure, it introduces new SemEval data, aspect-conditioned inputs, ATAE-LSTM, a new evaluation protocol and an aspect-aware interface. It is therefore a new deep-learning implementation rather than a resubmission of the ISY503 solution.

This explanation must appear briefly in the A3 report's project background and in the repository release notes.

### Evidence from the existing repository

The local architecture audit confirms that the version story is not aspirational:

- `v1.0.0` delivered TF-IDF, BiLSTM, evaluation, inference and Streamlit for ISY503;
- `v2.0.0` added DistilBERT;
- `v2.1.0` to `v2.3.0` hardened package boundaries and removed compatibility wrappers;
- the repository now separates data, tokenization, models, training, inference, evaluation and app concerns;
- the fast-suite result recorded for `v2.3.0` is 194 passed and 5 deselected, but it must be reproduced in the new local environment before v3 work begins.

ReviewPulse v3.0 will therefore reuse architecture, workflow and testing patterns. It will not reuse binary checkpoints, binary labels, the Amazon parser, the current prediction threshold or the current model output heads as if they were compatible with ABSA.

## 3. Problem, aim and research questions

### Problem

Sentence-level classifiers collapse mixed reviews into one label. A review such as *"the food was excellent but the service was slow"* requires separate predictions for `food` and `service`.

### Aim

Implement and critically evaluate a low-compute ABSA system that measures the value of explicit aspect conditioning, compares ATAE-LSTM with DistilBERT and presents indicative token-level evidence for supported models.

### Research questions

- **RQ1:** How much does explicit aspect conditioning improve sentiment classification on multi-aspect sentences compared with review-only baselines?
- **RQ2:** How do ATAE-LSTM and DistilBERT compare on accuracy, macro-F1 and computational efficiency?
- **RQ3:** What human-readable evidence do attention or attribution visualisations provide for aspect-level predictions?

## 4. Scope

### Core scope

- SemEval-2014 Task 4 **Restaurants** domain.
- Aspect sentiment classification using gold aspect terms for training and evaluation.
- Manual entry of one or more aspects in the Streamlit interface.
- Positive, neutral and negative classification.
- Explicit removal and reporting of the original SemEval `conflict` label.
- Four-model experimental ladder.
- Leakage-safe, sentence-grouped data splitting.
- Standard and mixed-polarity multi-aspect evaluation.
- Attention or attribution output only for capable models.
- Reproducible training, evaluation, inference and artifact loading.
- Preservation of the existing v1.x/v2.x commands, artifacts and test behaviour.
- A separate aspect-inference API that does not widen or break the legacy `predict_sentiment(text, model_name)` contract.

### Stretch scope, gated behind the core Definition of Done

- Laptops cross-domain evaluation.
- Multiple-seed variance estimates.
- Faithfulness testing through token perturbation.
- Automatic aspect extraction.
- Neural Topic Modelling or aspect discovery.
- Hosted model-artifact download and fallback.

### Explicit non-goals

- End-to-end aspect extraction in the core submission.
- Claiming that attention reveals model reasoning or causal explanation.
- Assuming DistilBERT must outperform the lighter models.
- Rebuilding or deleting the existing v1.x/v2.x sentence-level pipeline.
- Allowing stretch work to delay the executable Restaurants implementation.

## 5. Functional requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| FR-01 | Establish a verified v2.3.0 baseline before modification | Python environment and dependency record exist; legacy fast suite is rerun and its result recorded |
| FR-02 | Load and validate SemEval-2014 Restaurants data | Data audit records provenance, checksums where available, split sizes, label counts, offsets and invalid rows |
| FR-03 | Represent each example without losing alignment | Schema includes sentence ID, raw review, aspect, character offsets, retained label and source split |
| FR-04 | Prevent sentence leakage | All aspect instances from one sentence remain in exactly one partition; automated overlap test passes |
| FR-05 | Preserve legacy behaviour | Existing inference API, artifacts and canonical v2 commands remain functional throughout the v3 branch |
| FR-06 | Train review-only TF-IDF baseline | Saved ABSA artifact and repeatable three-class metrics on the common test set |
| FR-07 | Train review-only target-agnostic LSTM | Saved ABSA checkpoint, training history and common metrics |
| FR-08 | Train aspect-conditioned ATAE-LSTM | Saved ABSA checkpoint, aspect-aware inference and aligned attention weights |
| FR-09 | Fine-tune aspect-conditioned DistilBERT | Three-class checkpoint, review-aspect pair encoding and reproducible inference exist |
| FR-10 | Evaluate every model consistently | Accuracy, macro-F1, per-class metrics, confusion matrix, runtime and model-size evidence |
| FR-11 | Evaluate mixed-polarity multi-aspect sentences | Subset is generated from the gold data and included in the comparison table |
| FR-12 | Provide a separate aspect-inference API | `predict_aspects(review, aspects, model_name)` returns one compatible result per aspect |
| FR-13 | Display indicative token-level evidence | ATAE-LSTM attention and optional DistilBERT evidence are aligned and caveated; baselines need no heatmap |
| FR-14 | Provide an explicit v3 application workflow | User can distinguish legacy review sentiment from DLE602 aspect sentiment and run the v3 path without code |
| FR-15 | Segregate v3 artifacts | All new models, vocabularies, metrics and plots live below `outputs/absa/` and do not overwrite legacy files |
| FR-16 | Handle predictable failures | Missing artifacts, empty reviews, empty aspects, unknown models and malformed data produce clear errors |
| FR-17 | Run from documented commands | A clean environment can install, test, audit, evaluate and launch the app using concise instructions |
| FR-18 | Package within practical submission constraints | ZIP and model-artifact sizes are measured before release; any external dependency or download is documented |

## 6. Data and evaluation contract

### Data source

The primary dataset is SemEval-2014 Task 4 Restaurants. The implementation must record the authoritative source, redistribution constraints and file checksums. If redistribution is restricted, the repository will contain an acquisition/preparation script and clear placement instructions rather than unlicensed data.

### Canonical record

```text
AspectExample
  sentence_id: str
  review_raw: str
  aspect: str
  aspect_from: int
  aspect_to: int
  label: positive | neutral | negative
  source_split: train | test
```

Character offsets are retained even if a model later consumes token IDs. The parser must first verify that `review_raw[aspect_from:aspect_to]` matches the annotated aspect or explicitly record why it does not.

### Label policy

1. Parse all original polarity labels.
2. Count and report the original `conflict` examples.
3. Exclude `conflict` from the core three-class task.
4. Do not merge `conflict` with the analytical subset below.

### Mixed-polarity multi-aspect subset

A sentence belongs to this subset when it contains at least two gold aspects associated with different retained polarities. Membership is computed from gold annotations, not model predictions.

### Split policy

- Preserve the official test set.
- Derive development data from the official training data using a fixed seed.
- Group by `sentence_id` before expanding sentences into aspect instances.
- Assert that no `sentence_id` appears in more than one partition.
- Fit tokenizers, vocabularies and TF-IDF features on training data only.

### Preprocessing and alignment policy

The legacy `clean_text()` function is not reused as the canonical ABSA input because it lowercases, expands contractions and removes punctuation. Those transformations can invalidate SemEval character offsets and make token evidence impossible to align reliably.

- Preserve `review_raw` as the source of truth.
- Apply only documented, model-specific normalisation after offset validation.
- Build LSTM tokens together with character spans so attention can be projected back to visible text.
- Feed DistilBERT the raw or minimally normalised `(review, aspect)` pair through the Hugging Face tokenizer.
- Never generate an interpretability view from tokens that cannot be mapped back to the displayed review.

### Review-only baseline policy

TF-IDF and the target-agnostic LSTM receive only `review`. They may encounter identical review features paired with different aspect labels when a sentence has mixed polarity. This contradiction is intentional: it operationalises the limitation measured by RQ1. The report must explain it rather than silently filtering those cases.

### Multiclass output policy

All v3 trainable models emit three logits in the fixed order `negative`, `neutral`, `positive`. Neural training uses integer class IDs and cross-entropy loss; inference uses softmax and returns the highest-probability class plus confidence. The legacy sigmoid threshold remains untouched and is not imported into the ABSA packages.

### Metrics

- Accuracy.
- Macro-F1.
- Precision, recall and F1 per class.
- Confusion matrices.
- Accuracy and macro-F1 on the mixed-polarity multi-aspect subset.
- Training time, inference latency and artifact size using a documented environment.
- Error examples, especially disagreements between review-only and aspect-conditioned models.

No model is required to beat another for the project to succeed. A negative or unexpected result is valid when the experiment is fair, reproducible and critically analysed.

## 7. Model ladder

| Stage | Model | Input | Purpose | Visual evidence |
|---|---|---|---|---|
| 1 | TF-IDF + Logistic Regression | `review` | Classical sanity baseline and historical bridge | None required |
| 2 | Target-agnostic LSTM | `review` | Tests whether recurrence alone resolves the aspect gap | None required |
| 3 | ATAE-LSTM | `(review, aspect)` | Tests explicit aspect embeddings and aspect-aware attention | Attention weights |
| 4 | DistilBERT sentence pair | `(review, aspect)` | Tests pretrained contextual transfer against lighter models | Token attribution or attention visualisation |

The target-agnostic LSTM is a new three-class v3 model, not the binary `BiLSTMSentiment` checkpoint relabelled. Its embedding size, recurrent hidden size, dropout, optimiser, data split and training budget should match ATAE-LSTM as closely as practical. The controlled difference should be aspect conditioning and attention, which makes RQ1 interpretable.

The existing TF-IDF, BiLSTM and DistilBERT implementations remain historical baselines and code references. Their ISY503 metrics must not be placed in the v3 comparison table because they use different data, labels and prediction units.

All v3 models must return a compatible aspect-prediction payload so evaluation and the interface do not contain model-specific branching beyond adapters.

```python
{
    "aspect": "service",
    "label": "negative",
    "confidence": 0.91,
    "model": "atae_lstm",
    "token_evidence": [...],  # optional and model-dependent
}
```

The new public surface is separate from the legacy single-text API:

```python
results = predict_aspects(
    review="The food was great but the service was slow.",
    aspects=["food", "service"],
    model_name="absa_atae",
)
```

An `AspectPredictor` handles one `(review, aspect)` pair internally. `predict_aspects()` validates and de-duplicates the aspect list, calls that predictor once per aspect and preserves user order. The existing `predict_sentiment()` and `Predictor.predict(text)` contracts are not widened.

## 8. Proposed repository evolution

The current package architecture remains intact. New ABSA code should be isolated until the common interfaces are stable.

```text
review-pulse/
  app.py                         # product entry point; legacy/v3 mode selection
  src/
    ...                          # existing v2.3.0 packages remain unchanged
    absa/
      config.py
      labels.py
      data/
        parser.py
        audit.py
        splits.py
        schema.py
      tokenization/
        sequence.py
        transformer.py
      models/
        baseline.py
        target_lstm.py
        atae_lstm.py
        distilbert.py
      training/
        baseline.py
        target_lstm.py
        atae_lstm.py
        distilbert.py
      evaluation/
        metrics.py
        subsets.py
        runner.py
      inference/
        api.py
        loaders.py
        predictors.py
        registry.py
      interpretability/
        attention.py
        attribution.py
      checkpointing.py
  data/
    semeval2014/
  outputs/
    absa/
  tests/
    absa/
  docs/
    dle602-a3/
    issueBreakdown-phase4.md
    releaseNotes/v3.0.0.md
  constraints-a3.txt
```

The exact package split may be simplified during implementation, but these boundaries must remain visible: data, models, training, evaluation, inference and interpretability.

### Reuse rules from the architecture audit

Reuse directly when the contract is task-independent:

- device-resolution patterns;
- package boundary tests;
- checkpoint metadata and clean-load ideas;
- predictor-registry pattern;
- plotting and error-analysis patterns;
- Streamlit resource-caching pattern;
- issue-generation script, release-note structure and conventional commits.

Reimplement or adapt inside `src/absa/` when the current contract is binary or dataset-specific:

- Amazon pseudo-XML parser and rating audit;
- aggressive `clean_text()` preprocessing;
- float-label datasets;
- one-logit BiLSTM and DistilBERT heads;
- sigmoid threshold inference;
- binary F1 and two-class plots;
- `Predictor.predict(text)` and its legacy registry;
- current checkpoint payloads and artifact paths.

Generic extraction from legacy code is deferred until the v3 path works. The first implementation should favour safe adapters over a broad refactor of proven v2 code.

### Environment and dependency gate

The clone has no `.venv`, and the current `requirements.txt` uses broad lower bounds. Before implementation:

1. create a local environment with a recorded Python version;
2. install a mutually compatible PyTorch, scikit-learn, Streamlit and Transformers set;
3. run the legacy fast suite;
4. record the resolved versions in `constraints-a3.txt` or an equivalent lock artifact;
5. use that same constraint set for experiments and the clean-install submission test.

Dependency upgrades are not mixed with ABSA feature issues unless required and evidenced. A library upgrade that changes legacy behaviour becomes a separate compatibility task.

## 9. Work breakdown: GitHub-ready issues

| Order | Proposed issue | Owner | Depends on | Done when |
|---:|---|---|---|---|
| 1 | `chore(v3): establish local environment and v2.3.0 regression baseline` | Luis | - | Python/dependency record exists and legacy fast-suite result is captured |
| 2 | `docs(v3): add phase-4 issue breakdown and v3 architecture guardrails` | Luis | 1 | GitHub-ready issue document, dependency order and non-regression rules exist |
| 3 | `feat(absa): scaffold isolated v3 packages, labels and config` | Luis | 1, 2 | `src/absa`, `tests/absa`, paths, label order and boundary smoke tests exist |
| 4 | `feat(absa-data): document and acquire SemEval Restaurants` | Luis | 3 | Provenance, redistribution decision, acquisition instructions and checksums exist |
| 5 | `feat(absa-data): parse examples, validate offsets and generate audit` | Luis | 4 | Canonical records, offset checks, `conflict` counts and reproducible audit exist |
| 6 | `test(absa-data): add deterministic leakage-safe grouped splits` | Luis | 5 | Official test is preserved and sentence-overlap assertions pass |
| 7 | `feat(absa-eval): add multiclass metrics and mixed-polarity subset` | Luis | 5, 6 | Shared metrics, three-class plots and subset tests pass |
| 8 | `feat(absa-baseline): train three-class TF-IDF review-only baseline` | Luis | 6, 7 | Segregated artifact, metrics and aspect-predictor adapter exist |
| 9 | `feat(absa-lstm): train controlled target-agnostic LSTM` | Luis | 6, 7 | Three-logit checkpoint, history, metrics and adapter exist |
| 10 | `feat(absa-atae): implement aspect-conditioned ATAE-LSTM` | Luis | 6, 7, 9 | Matched recurrent setup, aspect-sensitive predictions and aligned attention exist |
| 11 | `feat(absa-bert): fine-tune three-class DistilBERT sentence-pair model` | Luis + Victor | 6, 7 | Pair encoding, checkpoint, metrics and adapter exist |
| 12 | `feat(absa-eval): publish four-model comparison and error analysis` | Group | 8-11 | Fixed comparison tables, matrices, efficiency evidence and reviewed errors exist |
| 13 | `feat(absa-xai): add indicative token-evidence views` | Luis | 10, 11 | ATAE attention and any Transformer evidence align to displayed text and include caveats |
| 14 | `feat(app): add legacy/v3 mode and multi-aspect workflow` | Luis + Juan | 8-13 | User can distinguish tasks and receive ordered per-aspect results |
| 15 | `test(absa): add integration, artifact and clean-load coverage` | Luis | 8-14 | Legacy regression plus v3 unit and end-to-end smoke paths pass |
| 16 | `docs(dle602): write implementation report and results package` | Group | 12-15 | 1,500-word report draft, version context and captioned evidence are complete |
| 17 | `release: package ReviewPulse v3.0.0 for DLE602 A3` | Group | 15, 16 | Size-checked ZIP, execution instructions, release notes and final tag exist |

The next planning deliverable is `docs/issueBreakdown-phase4.md` in the ReviewPulse repository, using the existing batch issue creator's `### Issue #NN - title` format. Before assigning numbers, check the next free GitHub issue number; PR and issue numbers share one sequence.

### Dependency path

```text
environment + legacy baseline
  -> phase-4 issue breakdown
  -> ABSA boundary scaffold
  -> data provenance
  -> parser + offset audit
  -> grouped splits
  -> multiclass evaluator
  -> TF-IDF + target LSTM
  -> ATAE-LSTM + DistilBERT
  -> comparison + interpretability
  -> legacy/v3 Streamlit integration
  -> regression + clean-load tests
  -> report + ZIP + v3.0.0
```

## 10. Timeline and milestone gates

| Phase | Date | Required outcome | Exit gate |
|---|---|---|---|
| Foundation + data + baseline | 18-26 Jul | Verified legacy suite, phase-4 issues, ABSA boundaries, audited Restaurants data, grouped splits and TF-IDF results | Legacy baseline recorded; offsets valid; no leakage; TF-IDF reproducible |
| LSTM + ATAE-LSTM | 27 Jul-2 Aug | Target-agnostic LSTM and ATAE-LSTM checkpoints and metrics | Both models load cleanly and use the common evaluator |
| DistilBERT | 3-8 Aug | Sentence-pair Transformer checkpoint and metrics | Training and inference complete within available compute |
| Evaluation + interface | 9-13 Aug | Four-model comparison, error analysis, evidence views and Streamlit v3 | End-to-end demo works from review + aspects |
| Report + submission package | 14-19 Aug | Report, source, instructions, artifacts and ZIP | Clean-machine smoke test passes before final packaging |

If a gate fails, scope is reduced before dates move. The reduction order is: Topic Modelling, automatic extraction, Laptops, multi-seed runs, DistilBERT visualisation, then DistilBERT training depth. Restaurants, grouped splits, TF-IDF, ATAE-LSTM, shared evaluation and a working interface remain protected.

## 11. Team responsibilities

| Area | Lead | Shared review |
|---|---|---|
| Architecture, data pipeline, models and integration | Luis | Victor and Juan |
| Literature-to-results interpretation and reference validation | Victor | Luis |
| Milestone tracking, acceptance evidence and submission packaging | Juan | Luis and Victor |
| Evaluation interpretation, report and final QA | Group | Group |

Every group-owned result must have visible evidence: commit, PR review, experiment note, report section or acceptance record. Ownership may be reassigned when a milestone is missed, but the change must be documented.

## 12. Testing and reproducibility strategy

### Required automated coverage

- XML/parser fixtures and malformed-input behaviour.
- Legacy fast-suite regression before and after v3 integration.
- Label mapping and `conflict` exclusion counts.
- Aspect offset validation and token-to-text span alignment.
- Deterministic grouped splits and zero sentence overlap.
- Mixed-polarity subset membership.
- Vocabulary/tokenizer fit boundaries.
- Tensor shapes and masks for both LSTM models.
- Three-logit outputs, integer labels, cross-entropy and softmax probabilities.
- ATAE-LSTM aspect conditioning and normalised attention.
- DistilBERT sentence-pair encoding.
- Prediction payload contract across all models.
- Isolation of `predict_sentiment()` from `predict_aspects()`.
- Artifact save/load and missing-artifact errors.
- No writes to the four legacy artifact paths.
- Multi-aspect inference.
- End-to-end smoke evaluation on a tiny fixture.

### Reproducibility record

Each reported run must capture:

- git commit;
- dataset checksum or source identifier;
- split seed;
- model configuration;
- Python and key dependency versions;
- lock/constraint file used for the run;
- hardware/device;
- training duration;
- best epoch and selection metric;
- test metrics;
- artifact filename, size and checksum.

## 13. Streamlit v3 workflow

The v3 application must make the academic and technical phases visible without making the user understand repository history first:

1. User selects **Legacy review sentiment (ISY503)** or **Aspect sentiment v3 (DLE602)**.
2. The v3 mode accepts a review.
3. User enters one or more comma-separated aspects.
4. User chooses an available v3 model.
5. The app returns one sentiment and confidence per aspect in the supplied order.
6. ATAE-LSTM or DistilBERT may display token-level evidence with an explicit indicative-evidence caveat.
7. Errors explain how to recover without exposing a stack trace.

The current app is hard-coded to Amazon binary sentiment, positive/negative rendering and an ISY503 footer. The v3 integration must update those assumptions without changing legacy predictions. A separate `app_absa.py` is an acceptable contingency if combining both modes threatens the core submission date.

## 14. A3 report plan

The A3 report is new and implementation-focused. It must not repeat the A2 proposal beyond a concise background.

| Section | Indicative words | Evidence |
|---|---:|---|
| Project evolution, problem, aim and RQs | 150-180 | Phased v1.0 -> v2.x -> v3.0 context |
| Requirements and scope | 150-180 | Core requirements and non-goals |
| Data and implementation method | 350-400 | Audit, split, architectures and training decisions |
| Deep-learning principles | 220-260 | Representation learning, recurrence, attention, transfer and regularisation |
| Results and critical analysis | 400-450 | Common metrics, efficiency, subset analysis, errors and evidence |
| Limitations and conclusion | 120-160 | Honest interpretation and future work |

Suggested report figures and tables:

- v1.0/v2.x/v3.0 evolution diagram.
- v3 architecture and model-input comparison.
- label and aspect distribution.
- training curves for neural models.
- four-model results and efficiency table.
- confusion matrices.
- mixed-polarity case comparison.
- illustrative attention/attribution output clearly separated from quantitative results.

## 15. Risk register

| Risk | Probability | Impact | Mitigation | Contingency |
|---|---|---|---|---|
| Small dataset causes overfitting | High | High | Dropout, early stopping, weight decay, fixed development selection | Reduce capacity and report limitations/variance honestly |
| Transformer exceeds free compute | Medium | High | Pilot run, capped sequence length, DistilBERT, checkpointing | Reduce fine-tuned layers or ship ATAE-LSTM as primary deep model |
| Sentence leakage inflates metrics | Medium | High | Group before aspect expansion; automated overlap assertions | Rebuild splits and invalidate/rerun affected results |
| Legacy text cleaning corrupts aspect offsets | High | High | Preserve raw text; validate offsets before model-specific normalisation | Reject invalid rows with audit evidence and fix the parser/alignment path |
| SemEval redistribution is restricted | Medium | High | Record source and licensing before committing data | Ship acquisition script and checksums instead of raw files |
| Model artifact cannot load in assessment environment | Medium | High | Clean-environment load test, pinned versions and checksums | Bundle verified lightweight baseline/ATAE artifacts and CPU path |
| Existing v2 architecture complicates ABSA integration | Medium | Medium | Isolate `src/absa` and use adapters | Run ABSA as a separate app entry point for submission |
| v3 changes regress the 194-test legacy baseline | Medium | High | Record baseline first; preserve APIs and artifact paths; run legacy suite at integration gates | Revert the integration seam and ship the isolated ABSA entry point |
| New checkpoints make the ZIP impractically large | Medium | Medium | Measure artifacts early; use compact state dicts and a documented size budget | Include lightweight core artifacts and provide reproducible DistilBERT retrieval instructions if permitted |
| Scope creep delays the core | High | High | Enforce milestone gates and stretch ordering | Cut extensions immediately and protect Restaurants core |
| Unequal group contribution | Medium | High | Named ownership, dated PR evidence and twice-weekly reviews | Reassign overdue work within 24 hours and document the change |
| Interpretability is overstated | Medium | Medium | Label evidence as indicative and separate it from causal claims | Remove the visualisation rather than make an unsupported claim |

## 16. Definition of Done

ReviewPulse v3.0 is complete when:

- [ ] The local Python environment and v2.3.0 legacy test baseline are recorded.
- [ ] `docs/issueBreakdown-phase4.md` and the corresponding GitHub issue track exist.
- [ ] Restaurants data provenance and preparation are documented.
- [ ] The data audit, aspect offsets and grouped splits are reproducible.
- [ ] Original `conflict` exclusions are counted and reported.
- [ ] TF-IDF, target-agnostic LSTM, ATAE-LSTM and DistilBERT emit the agreed three-class contract.
- [ ] Every completed model is evaluated through the same metrics pipeline.
- [ ] The mixed-polarity multi-aspect subset is defined in code and reported.
- [ ] `predict_aspects()` works without changing the legacy `predict_sentiment()` contract.
- [ ] The app distinguishes legacy review sentiment from v3 aspect sentiment and accepts multiple manual aspects.
- [ ] ATAE-LSTM exposes attention weights; any DistilBERT evidence is appropriately caveated.
- [ ] Missing inputs and artifacts produce useful errors.
- [ ] Legacy regression tests, v3 automated tests and an end-to-end smoke test pass.
- [ ] All v3 outputs remain below `outputs/absa/`; legacy artifacts are unchanged.
- [ ] A clean environment can follow the execution instructions without undocumented configuration.
- [ ] Reported results can be traced to configurations, commits and artifacts.
- [ ] The 1,500-word A3 report critically connects theory, implementation and outcomes.
- [ ] The submission ZIP contains the report, source, execution instructions and permitted artifacts/data instructions.
- [ ] Release notes explain the ISY503 v1.0/v2.x foundation and the new DLE602 v3.0 contribution.
- [ ] The final ZIP and artifact sizes are recorded and acceptable for submission.
- [ ] The final repository state is tagged `v3.0.0`.

## 17. Immediate next actions

1. Create a local virtual environment without modifying application code.
2. Install a compatible dependency set and record Python/package versions.
3. Run the legacy fast suite and record the real local baseline against `3880b2e`.
4. Convert this EPIC into `docs/issueBreakdown-phase4.md`, verify the next free issue number and dry-run the existing issue creator.
5. Create the GitHub issues/milestone only after reviewing the dry-run.
6. Create `feat/reviewpulse-v3-absa` from the verified `main` branch.
7. Scaffold `src/absa`, `tests/absa`, label order, paths and boundary tests.
8. Confirm the authorised SemEval-2014 Restaurants source and redistribution rules.
9. Complete parser, offset audit and grouped-split tests before training any model.
10. Publish the first implementation checkpoint: audit + TF-IDF baseline by 26 July.
