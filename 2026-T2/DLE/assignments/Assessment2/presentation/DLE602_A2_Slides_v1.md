---
marp: true
theme: default
paginate: true
size: 16:9
footer: "DLE602 Deep Learning · Assessment 2 · ReviewPulse v3.0"
style: |
  :root {
    --ink: #1b2733;
    --accent: #1f4e79;
    --accent2: #17a2a2;
    --muted: #5b6b7a;
    --pos: #1a7f4b;
    --neg: #c0392b;
    --bg-soft: #f4f7fa;
  }
  section {
    font-family: "Helvetica Neue", Arial, sans-serif;
    color: var(--ink);
    font-size: 26px;
    padding: 56px 64px;
  }
  h1 { color: var(--accent); font-size: 46px; margin-bottom: 8px; }
  h2 {
    color: var(--accent);
    font-size: 34px;
    border-bottom: 3px solid var(--accent2);
    padding-bottom: 8px;
    margin-bottom: 20px;
  }
  h3 { color: var(--accent2); font-size: 24px; margin: 4px 0; }
  strong { color: var(--accent); }
  em { color: var(--muted); }
  footer { color: var(--muted); font-size: 13px; }
  ul { line-height: 1.5; }
  .sub { color: var(--muted); font-size: 22px; }
  .flow { display: flex; align-items: stretch; gap: 10px; margin: 18px 0; }
  .box {
    flex: 1; background: var(--bg-soft); border: 2px solid var(--accent);
    border-radius: 10px; padding: 12px 10px; text-align: center; font-size: 18px;
  }
  .box small { color: var(--muted); font-size: 14px; }
  .arrow { align-self: center; color: var(--accent2); font-size: 30px; font-weight: 700; }
  .chip {
    display: inline-block; background: var(--accent2); color: #fff;
    border-radius: 16px; padding: 4px 14px; font-size: 18px; margin: 4px 6px 0 0;
  }
  .pos { color: var(--pos); font-weight: 700; }
  .neg { color: var(--neg); font-weight: 700; }
  .lead-quote { font-size: 34px; line-height: 1.35; margin: 24px 0; }
  .here { background: var(--accent2); color:#fff; border-radius: 8px; padding: 2px 10px; font-size:16px; }
  section.title { background: var(--accent); color: #fff; }
  section.title h1 { color: #fff; font-size: 52px; }
  section.title h3 { color: #cfe3f2; }
  section.title strong { color: #fff; }
  section.title .sub, section.title em { color: #d6e4f0; }
  section.refs { font-size: 18px; }
  section.refs h2 { font-size: 30px; }
---

<!-- _class: title -->
<!-- _paginate: false -->
<!-- _footer: "" -->

# ReviewPulse v3.0

### Aspect-Based Sentiment Analysis with Attention-Based Deep Learning

<br/>

**DLE602 Deep Learning - Assessment 2: Project Proposal**

<span class="sub">Luis Faria (A00187785) · Victor [ID] · Juan [ID]</span>
<span class="sub">Learning Facilitator: Dr Tayab Din Memon</span>

<!--
PRESENTER: Victor (~25 s)
Introduce the group and the one-line project. "We are building a system that reads a
customer review and tells you the sentiment FOR EACH THING being talked about - not just
one overall score." Keep it warm and short, then hand to Juan for the problem.
-->

---

## The problem - why one label is not enough

<div class="lead-quote">
"The food was <span class="pos">great</span> but the service was <span class="neg">slow</span>."
</div>

- One review → **two opposite opinions**, one per aspect
- Sentence-level models collapse it to a single 😐 : *food* <span class="pos">good</span> / *service* <span class="neg">bad</span> is lost
- Our A1 N-gram classifier and the Zhao et al. (2018) CNN both do exactly this

**A business reading "neutral" learns nothing. "Food good, service bad" is actionable.**

<!--
PRESENTER: Juan (~60 s)
Lead with the example - read it out loud. Make the audience FEEL the loss: a single
"neutral" score tells a restaurant nothing; per-aspect tells them exactly what to fix.
State the gap our project closes: sentiment per aspect, not per review.
-->

---

## What the literature shows

<div class="flow">
  <div class="box"><strong>CNN</strong><br/>2018<br/><small>deep but flat</small></div>
  <div class="arrow">→</div>
  <div class="box"><strong>ATAE-LSTM</strong><br/>2016<br/><small>attention</small></div>
  <div class="arrow">→</div>
  <div class="box"><strong>BERT-for-ABSA</strong><br/>2019<br/><small>contextual</small></div>
  <div class="arrow">→</div>
  <div class="box"><strong>LLM / neural discovery</strong><br/>2023-2026<br/><small>frontier</small></div>
</div>

- One limitation - a single label per text - solved step by step
- The frontier is **heavy and LLM-driven**; few pair a *light, explainable* model with faithful attention

<span class="here">We are here</span>  explainable · low-compute · aspect-level

<!--
PRESENTER: Victor (~90 s)
Tell it as a STORY of one limitation being solved, not a paper list. CNN lifted accuracy
but stayed sentence-level; ATAE-LSTM added aspect-aware attention; BERT made it contextual;
LLMs pushed zero/few-shot. Land on the gap: the frontier is heavy; our niche is a light,
explainable model with faithful attention. That is where we sit.
-->

---

## Our approach

<div class="flow">
  <div class="box">(review, aspect)</div>
  <div class="arrow">→</div>
  <div class="box"><strong>ATAE-LSTM</strong><br/><small>+ DistilBERT</small></div>
  <div class="arrow">→</div>
  <div class="box">per-aspect<br/>sentiment</div>
  <div class="arrow">→</div>
  <div class="box"><strong>attention<br/>heatmap</strong></div>
</div>

- **Four-model ladder:** TF-IDF + LogReg → target-agnostic LSTM → ATAE-LSTM → DistilBERT
- **Interpretability is the differentiator** - only ATAE-LSTM and DistilBERT expose attention; we show *why*, not just the label
- Optional neural **Topic Modelling** to discover aspects (scoped as stretch)

<span class="chip">SemEval-2014: Restaurants (core) + Laptops (extension)</span>
<span class="chip">accuracy · macro-F1 · efficiency · attention</span>

<!--
PRESENTER: Luis (~90 s)
Four models on a PRE-ANNOTATED benchmark (that is the feasibility win - no manual labelling):
TF-IDF and a target-agnostic LSTM set the sentence-level baselines; ATAE-LSTM adds aspect-aware
attention; DistilBERT adds contextual power at low compute. Only the last two expose attention -
that is our differentiator, showing which words drove each per-aspect call. Efficiency is now
part of the comparison, not just accuracy. Mention Topic Modelling as the OPTIONAL aspect-discovery
stage, not core.
-->

---

## Plan & risks - feasible and de-risked

**Modules 8 → 12**
data + baseline → ATAE-LSTM → DistilBERT → interpretability + Streamlit demo → eval + report

| Risk | Mitigation |
|---|---|
| Small data → overfitting | dropout · early stopping · transfer learning |
| Heavy fine-tuning | DistilBERT on free Colab GPU |
| Scope creep | extraction & topic modelling are **gated stretch goals** |

**Critical success factors:** pre-annotated data · light compute · working LSTM fallback

<!--
PRESENTER: Juan (~60 s)
Show it is feasible and de-risked. Walk the module timeline in one sentence. Emphasise the
FALLBACK: even if the transformer underperforms, the ATAE-LSTM path still meets the rubric.
Zero-cost budget: free Colab, open datasets, open-source libraries.
-->

---

## Expected contribution

<div class="flow">
  <div class="box"><strong>Aspect-level</strong><br/><small>sentiment per thing</small></div>
  <div class="box"><strong>Explainable</strong><br/><small>attention heatmap</small></div>
  <div class="box"><strong>Live demo</strong><br/><small>Streamlit, Assessment 3</small></div>
</div>

<br/>

<div class="lead-quote">
From one score per review to a <strong>transparent, per-aspect read</strong> -
built and demoed in Assessment 3.
</div>

<!--
PRESENTER: Luis (~30 s)
Recap the payoff in one breath: aspect-level, explainable, and a live demo in A3. End on
the demo - leave them picturing the product. Thank the audience.
-->

---

<!-- _class: refs -->

## References (APA)

Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *Proceedings of NAACL-HLT 2019*, 4171-4186.

He, R., Lee, W. S., Ng, H. T., & Dahlmeier, D. (2017). An unsupervised neural attention model for aspect extraction. *Proceedings of ACL 2017*, 388-397.

Hua, Y. C., Denny, P., Wicker, J., & Taskova, K. (2024). A systematic review of aspect-based sentiment analysis: Domains, methods, and trends. *Artificial Intelligence Review, 57*(11), Article 296.

Pontiki, M., Galanis, D., Pavlopoulos, J., Papageorgiou, H., Androutsopoulos, I., & Manandhar, S. (2014). SemEval-2014 Task 4: Aspect based sentiment analysis. *Proceedings of SemEval 2014*, 27-35.

Sun, C., Huang, L., & Qiu, X. (2019). Utilizing BERT for aspect-based sentiment analysis via constructing auxiliary sentence. *Proceedings of NAACL-HLT 2019*, 380-385.

Wang, Y., Huang, M., Zhu, X., & Zhao, L. (2016). Attention-based LSTM for aspect-level sentiment classification. *Proceedings of EMNLP 2016*, 606-615.

Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253-23260.

<!--
Reference slide is not spoken. Trimmed to the papers actually cited on the slides plus the
core method sources. Full 10-entry list lives in the written report.
-->
