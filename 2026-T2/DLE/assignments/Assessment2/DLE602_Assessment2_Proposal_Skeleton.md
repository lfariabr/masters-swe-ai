# Review Pulse v2: Aspect-Based Sentiment Analysis of Customer Reviews with Attention-Based Deep Learning
*DLE602 Deep Learning - Assessment 2 Proposal Skeleton v2*

## Working Metadata

| Item | Detail |
|---|---|
| Subject | DLE602 - Deep Learning |
| Assessment | Assessment 2 - Deep Learning Project Proposal Presentation |
| Task | Propose a deep-learning project (literature review + plan) and present it |
| Deliverables | 1,000-word report (+/-10%) + 5-7 minute audio-visual presentation |
| Group | 3 people: Luis Faria (A00187785), Victor [surname - confirm + student ID], Juan [surname - confirm + student ID] |
| Weight | 30% |
| Due | Sunday end of Module 8; README currently records 26/07/2026 |
| Learning outcomes | SLO b, SLO c, SLO d, SLO e |
| Feeds into | Assessment 3 (the build) - same project, implemented in Python |
| Current status | v2 skeleton: group set (Luis + Victor + Juan; IDs to confirm), recent 2023-2026 literature folded into the spine, Topic Modelling scoped as an optional neural aspect-discovery stage, problem statement tightened to a word-counted draft. Still to finalise: surnames/IDs on the cover, full prose, APA pass, slide deck + recording |

---

## Project in One Sentence

> Build and evaluate an **aspect-based sentiment analysis (ABSA)** system that predicts sentiment **per aspect** of a customer review (e.g. *food = positive, service = negative*), comparing an **attention-LSTM** with a **fine-tuned transformer**, and adding an **attention-visualisation** layer for interpretability.

**Portfolio framing:** this is the deep-learning successor to *Review Pulse* (my classical, sentence-level sentiment classifier on ~8,000 Amazon reviews). v1 gives one polarity per review; v2 resolves sentiment at the aspect level — the upgrade is the whole point.

---

## Brief Requirements Snapshot

| Required element | How this skeleton handles it | Evidence target |
|---|---|---|
| Identify an interesting DL project from quality literature | ABSA framed as the aspect-level evolution of sentence-level sentiment (Zhao et al. 2018 → Pontiki et al. 2014 → attention-LSTM → BERT) | Literature review section narrates the evolution and positions our project in the gap |
| Select and analyse quality research articles similar to the seed paper | 4-6 peer-reviewed papers (SemEval task paper, ATAE-LSTM, TD-LSTM, BERT-for-ABSA, BERT) | Reference list + synthesis, not summary, of each |
| Concise project description + specific aim(s)/research question(s) | Problem statement + 3 research questions below | Stated explicitly and tied to the aim |
| Demonstrate sound project management | Activity plan, milestones to A3, risk + contingency table | Gantt-style plan + risk register in appendices |
| 1,000-word report with abstract, cover page, ToC, captions, word count, page numbers | Word budget + section shells below; formatting checklist in Appendix A | Final document assembled to spec |
| 5-7 minute audio-visual presentation (all members, PDF slides) | Presentation plan section maps the report to a 6-slide arc | Slide outline + speaking split |
| APA referencing | Reference starter list in APA; checklist item | Final APA pass before submission |

## Rubric Strategy

> Report criteria total 85%; the remaining weight sits with the audio-visual presentation. Confirm exact split against the LMS rubric.

| Rubric area | Weight | High-distinction move |
|---|---:|---|
| Problem Statement and Aim | 20% | State the aspect-level gap crisply, with a concrete failing example, then 2-3 sharp research questions clearly linked to the relevant body of knowledge |
| Analysis, Synthesis and Application of Literature | 25% | Critically *compare* approaches (CNN vs attention-LSTM vs BERT) and argue why our design follows, rather than summarising each paper in isolation |
| Project Planning and Management | 25% | Feasible plan with milestones to A3, explicit risk analysis, contingency plan, and named critical success factors (data already annotated, light compute) |
| Overall Structure and Flow of Proposal | 15% | Tight required sections (abstract, intro, body, conclusion), arguments that build toward A3, pitched at a DL-literate audience |
| Presentation (confirm weight) | ~15% | Engaging 5-7 min, not a report read-out; every member presents; clean consistent PDF slides |

## Suggested Word Budget (1,000 words)

| Section | Target words | Notes |
|---|---:|---|
| Abstract / executive summary | 80-100 | The project, the gap, the planned models, expected contribution |
| Problem statement, aim & research questions | 130-160 | The aspect-level gap + 3 RQs + aim |
| Literature review | 320-360 | Evolution + critical synthesis + positioning |
| Proposed approach & methods | 230-270 | Dataset, model progression, evaluation, interpretability, deployment |
| Project plan & risk management | 120-150 | Milestones to A3 + risk/contingency (keep tables in appendix) |
| Conclusion | 40-60 | One tight forward-looking close into A3 |
| Total body | ~1,000 | Cover page, ToC, captions, references, and tables outside the count if allowed |

## Draft Thesis

Sentence-level sentiment models, including the deep CNN of Zhao, Gui, and Zhang (2018) and classical baselines such as Review Pulse, collapse a multi-faceted opinion into a single label and therefore lose the aspect-level detail that businesses actually act on. This project proposes an aspect-based sentiment analysis system on the SemEval-2014 benchmark that compares an attention-based LSTM (ATAE-LSTM) with a fine-tuned transformer (DistilBERT) and adds an attention-visualisation layer, arguing that learned representations plus attention are necessary to resolve sentiment per aspect and to explain *why* a prediction was made.

---

# Proposal Content (section shells)

## 1. Problem Statement, Aim & Research Questions

**Problem.** Most sentiment systems assign a single polarity to a whole text. Our Assessment 1 N-gram classifier and the deep CNN of Zhao, Gui and Zhang (2018) both do exactly this. Real customer reviews are mixed: *"the food was great but the service was slow"* carries two opposite opinions, one per aspect. A single label collapses that detail and hides precisely what product, hospitality, and customer-experience teams need to act on.

**Aim.** Design and evaluate an aspect-based sentiment analysis (ABSA) system that predicts sentiment per aspect of a review, compares an attention-based LSTM (ATAE-LSTM) with a fine-tuned transformer (DistilBERT), and exposes interpretable attention-based explanations of each prediction.

**Research questions.**
- **RQ1** - Does aspect-level modelling produce more useful, fine-grained sentiment than a sentence-level baseline on the same reviews?
- **RQ2** - How does an attention-LSTM (ATAE-LSTM) compare with a fine-tuned transformer (DistilBERT) on the SemEval-2014 aspect sentiment task (accuracy, macro-F1)?
- **RQ3** - Do attention weights give faithful, human-readable explanations of aspect-level predictions?

> Draft above is ~150 words (problem + aim + RQs), inside the 130-160 target. The A1 tie-in is deliberate continuity; the failing-example sentence is the hook - keep it. Optional RQ4 if the group adopts the Topic Modelling stage (see Section 3): *Can a neural topic model surface the review aspects without gold annotation, and how does discovery quality affect downstream aspect sentiment?*

## 2. Literature Review (spine to write against)

Write this as a **critical synthesis** that builds toward our design, not a list of summaries.

| Stage | Paper | What it contributes | How we use it |
|---|---|---|---|
| Sentence-level deep sentiment | Zhao, Gui & Zhang (2018) | CNN + word vectors for Twitter sentiment (our A1 seed) | Establishes deep sentiment, and the *limitation* we improve on (no aspects) |
| The ABSA task itself | Pontiki et al. (2014) | Defines SemEval-2014 Task 4, the benchmark + annotations | Justifies task choice and evaluation protocol |
| Target/aspect-aware LSTMs | Tang et al. (2016) | TD-LSTM / TC-LSTM condition on the target term | Motivates aspect-conditioned sequence models |
| Attention for aspects | Wang et al. (2016) | ATAE-LSTM: aspect embedding + attention | Our **first** model; the attention we visualise |
| Transformer era | Devlin et al. (2019) | BERT: pretrained contextual representations | Background for transfer learning |
| BERT for ABSA | Sun, Huang & Qiu (2019) | Auxiliary-sentence construction for aspect sentiment with BERT | Our **second** model's design |

**Recent literature (2023-2026) - cite for currency.** The classic spine above (2014-2019) earns the marks for *foundations*; these recent works show the field's current frontier and protect us against a "dated reading list" critique. Use them in the synthesis, not as a separate list.

| Stage | Work | What it contributes | How we use it |
|---|---|---|---|
| Recent survey / map of the field | Systematic review of ABSA: domains, methods, trends (2024, *Artificial Intelligence Review*) [authors - confirm via DOI 10.1007/s10462-024-10906-z] | A 2024 taxonomy of ABSA subtasks and methods | Positions our ATSC scope on the current map; recency anchor |
| Modern transformer SOTA on **our** benchmark | Jayakody et al. (2024), comparative study (arXiv 2407.02834) | Benchmarks deep-NN ABSA on SemEval-2014 Restaurants/Laptops; reports LSA+DeBERTa as strongest (~90% / ~86%) | Realistic upper bound; justifies DistilBERT as the feasible, lighter cousin |
| LLM / generative frontier | Simmering & Huoviala (2023), LLMs for ABSA (arXiv 2310.18025) | GPT-3.5/4 in zero/few-shot vs fine-tuning for ABSA via prompting | Frame as the frontier our interpretable, light-compute design deliberately contrasts with |
| Topic-model bridge (see Section 3) | He et al. (2017) ABAE - unsupervised neural attention for aspect extraction; LDA + ABSA exploration (2024) | Neural, attention-based aspect *discovery* without gold labels | Optional aspect-discovery stage; ties Topic Modelling into the DL + attention narrative |

**Positioning / gap.** Strong ABSA models exist - increasingly LLM-driven - but student/portfolio projects rarely pair a *light, reproducible* transformer baseline with an **interpretability layer** and a cross-domain demo on real customer feedback. Our niche is explainable, low-compute aspect sentiment, positioned honestly against the heavier LLM frontier.

> Target ~320-360 words. Synthesis verbs: *compare, contrast, build on, diverge from* — not *the authors say*. The arc to narrate: CNN (2018) → aspect-aware/attention LSTM (2016) → BERT-for-ABSA (2019) → LLM/generative + neural aspect discovery (2023-2026, where we sit).

## 3. Proposed Approach & Methods

**Dataset.** SemEval-2014 Task 4 — Restaurants (~3k sentences) and Laptops (~3k), each annotated with aspect terms/categories and polarity. Already annotated → no manual labelling (key feasibility point). Restaurants maps cleanly to service/customer-feedback framing.

**Scope decision.** Focus on **Aspect Sentiment Classification** given gold aspect terms (the well-defined ATSC/ACSA setting), not full end-to-end aspect extraction. This keeps A3 feasible; extraction is a documented stretch goal.

**Topic Modelling - where it fits (and where it does not).** Topic Modelling (LDA / BERTopic) is *unsupervised theme discovery*; ABSA is *supervised per-aspect sentiment*. They are not interchangeable, so Topic Modelling is **not** a third sentiment model. It earns a place in exactly one slot: the **aspect-discovery front-end**. SemEval gives gold aspects, but real reviews do not - so a neural topic model (BERTopic, or He et al.'s attention-based ABAE) can *discover* candidate aspects unsupervised, which the ASC models then score. This (a) closes the realistic "where do aspects come from?" gap, (b) stays inside Deep Learning by using **neural** topic models (transformer embeddings + attention), not classical LDA alone, and (c) reinforces - rather than dilutes - the attention theme. **Decision: include it as an optional/stretch pipeline stage and an EDA layer (a topic map of the corpus motivates which aspects matter), explicitly bounded in the risk register so it cannot threaten the core ATSC deliverable.** If the group wants it as a first-class contribution, it becomes RQ4; otherwise it stays a stretch goal and a portfolio-shine figure.

**Model progression (each step demonstrates subject concepts).**

| Model | Role | DL concepts (subject modules) |
|---|---|---|
| TF-IDF + Logistic Regression (sentence-level) | Classical baseline showing the aspect gap | contrast point; ties to Review Pulse |
| ATAE-LSTM (BiLSTM + aspect-aware attention) | First deep model | embeddings / representation learning (M1, M9), RNN/LSTM (M8), attention |
| DistilBERT fine-tuned (aspect as auxiliary sentence) | Modern model | transfer learning, contextual representations |
| Attention / saliency visualisation | Interpretability layer | visual analytics (M11) |

**Evaluation.** Accuracy and macro-F1 on aspect sentiment; per-class breakdown; cross-domain check (train Restaurants → test Laptops) for generalisation; qualitative attention heatmaps. Fixed seeds, explicit train/dev/test splits, no leakage.

**Deployment (A3 portfolio shine).** A Streamlit demo: user types a review, sees per-aspect sentiment and the attention heatmap. Mirrors the live Review Pulse v1 app.

> Target ~230-270 words. Put the two tables in an appendix if word count is tight.

## 4. Project Plan & Management

Indicative plan from proposal (Module 8) to A3 submission (Module 12 / README: 19/08/2026).

| Phase | Window | Output | Owner |
|---|---|---|---|
| Data pipeline + classical baseline | Modules 8-9 | Loaded SemEval data, baseline metrics | Impl. lead (Luis) |
| ATAE-LSTM implementation | Module 9-10 | Trained attention-LSTM + metrics | Impl. lead |
| DistilBERT fine-tuning | Module 10 | Trained transformer + metrics | Impl. lead + B |
| Interpretability + Streamlit demo | Module 11 | Attention heatmaps, live demo | Impl. lead |
| Evaluation, comparison, report | Module 11-12 | 1,500-word A3 report, figures | All |
| Buffer + submission | Module 12 | Cleaned repo, zip, references | All |

**Critical success factors:** data is pre-annotated; compute is light (DistilBERT on Colab free tier); a working classical/LSTM path exists even if the transformer underperforms.

## 5. Presentation Plan (5-7 min, PDF slides)

| Slide | Content | ~Time |
|---|---|---|
| 1 - Title | Project name, group members + IDs, subject | 15s |
| 2 - The problem | The "great food, slow service" gap; why aspect-level matters | 60s |
| 3 - What the literature shows | CNN → attention-LSTM → BERT, in one arc | 90s |
| 4 - Our approach | Dataset + the two models + interpretability | 90s |
| 5 - Plan & risks | Milestones to A3, key risks + mitigations | 60s |
| 6 - Expected contribution | Aspect-level + explainable + live demo | 30s |

> Every member speaks for roughly equal time. Slides are visual cues, NOT the full report.

---

# Appendices

## Appendix A - Submission Checklist

| Checklist item | Status |
|---|---|
| Project identified and clearly described | Drafted |
| 4-6 quality papers selected and critically synthesised | Spine drafted; finalise set |
| Problem statement + aim + research questions stated | Drafted |
| Project plan with milestones to A3 | Drafted |
| Risk analysis + contingency plan | Drafted (Appendix B) |
| Cover page with official names + project name | To do |
| Table of contents | To do |
| Abstract / executive summary | To do |
| Word count stated at end (before references) | To do |
| Page numbers in footer | To do |
| Figures/tables labelled with captions | To do |
| 5-7 min presentation slides (PDF) + speaking split | To do |
| APA references checked | To do |
| Group member names + IDs confirmed | To do |

## Appendix B - Risk Register

| Risk | Impact | Mitigation / contingency |
|---|---|---|
| Transformer fine-tuning too heavy for our hardware | Could block A3 build | Use DistilBERT + Colab free GPU; contingency: ship ATAE-LSTM only (still hits rubric) |
| SemEval data is small → overfitting | Inflated/weak results | Dropout, early stopping, pretrained embeddings/transfer; report cross-domain generalisation |
| Full aspect-term extraction is complex | Scope creep | Scope to aspect sentiment classification with gold terms; extraction as stretch goal |
| Attention != faithful explanation (known debate) | Over-claiming interpretability | Frame attention as indicative, not causal; cite the limitation |
| Group coordination / uneven load | Delivery + marks risk | Defined roles, shared repo, weekly check-ins, equal presentation split |
| Domain mismatch (SemEval vs clinic/Amazon) | Demo looks off-domain | Train on SemEval, present cross-domain demo explicitly as transfer, not in-domain accuracy |
| Topic Modelling stage expands scope | Distracts from core ATSC, threatens A3 | Keep it optional/stretch; gate it behind a working ASC pipeline; ship core deliverable with gold aspects regardless |

## Appendix C - Next Draft Tasks

1. Confirm group members and roles; add Victor's + Juan's surnames + student IDs to the cover page (Luis = A00187785 done).
2. Lock the final 4-6 paper set and pull APA citations - including confirming authors/year for the 2023-2026 additions (survey DOI 10.1007/s10462-024-10906-z; arXiv 2407.02834; arXiv 2310.18025).
3. Problem statement + research questions drafted to ~150 words (done in Section 1); decide whether Topic Modelling becomes RQ4 or stays a stretch goal.
4. Draft the literature review as critical synthesis (~340 words).
5. Finalise the method section + the two model tables.
6. Build the activity plan into a simple Gantt for the slides.
7. Assemble the 1,000-word document to format spec; build the 6-slide deck.
8. APA pass + record the 5-7 min presentation.

---

# Reference Starter List

Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *Proceedings of NAACL-HLT 2019*, 4171-4186. https://aclanthology.org/N19-1423/

Pontiki, M., Galanis, D., Pavlopoulos, J., Papageorgiou, H., Androutsopoulos, I., & Manandhar, S. (2014). SemEval-2014 Task 4: Aspect based sentiment analysis. *Proceedings of the 8th International Workshop on Semantic Evaluation (SemEval 2014)*, 27-35. https://aclanthology.org/S14-2004/

Sun, C., Huang, L., & Qiu, X. (2019). Utilizing BERT for aspect-based sentiment analysis via constructing auxiliary sentence. *Proceedings of NAACL-HLT 2019*, 380-385. https://aclanthology.org/N19-1035/

Tang, D., Qin, B., Feng, X., & Liu, T. (2016). Effective LSTMs for target-dependent sentiment classification. *Proceedings of COLING 2016*, 3298-3307. https://aclanthology.org/C16-1311/

Torrens University Australia. (2024). *DLE602 Assessment 2 brief: Deep Learning Project Proposal Presentation*.

Wang, Y., Huang, M., Zhu, X., & Zhao, L. (2016). Attention-based LSTM for aspect-level sentiment classification. *Proceedings of EMNLP 2016*, 606-615. https://aclanthology.org/D16-1058/

Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253-23260. https://doi.org/10.1109/ACCESS.2017.2776930

### Recent additions (2023-2026) - authors confirmed from the PDFs in `ARTICLES/`; still confirm journal volume/issue/pages before final submission

He, R., Lee, W. S., Ng, H. T., & Dahlmeier, D. (2017). An unsupervised neural attention model for aspect extraction. *Proceedings of ACL 2017*, 388-397. https://aclanthology.org/P17-1036/  *(the Topic-Modelling-to-ABSA bridge: neural, attention-based aspect discovery)*

Hua, Y. C., Denny, P., Wicker, J., & Taskova, K. (2024). A systematic review of aspect-based sentiment analysis: Domains, methods, and trends. *Artificial Intelligence Review, 57*, Article 296. https://doi.org/10.1007/s10462-024-10906-z

Jayakody, D., Isuranda, K., Malkith, A. V. A., de Silva, N., Ponnamperuma, S. R., Sandamali, G. G. N., & Sudheera, K. L. K. (2024). Aspect-based sentiment analysis techniques: A comparative study. *arXiv* preprint arXiv:2407.02834. https://arxiv.org/abs/2407.02834

Simmering, P. F., & Huoviala, P. (2023). Large language models for aspect-based sentiment analysis. *arXiv* preprint arXiv:2310.18025. https://arxiv.org/abs/2310.18025

Setiadi, D. R. I. M., Marutho, D., & Setiyanto, N. A. (2024). Comprehensive exploration of machine and deep learning classification methods for aspect-based sentiment analysis with Latent Dirichlet Allocation topic modeling. *Journal of Future Artificial Intelligence and Technologies*. https://doi.org/10.62411/faith.2024-3
