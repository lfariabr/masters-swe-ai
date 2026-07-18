# DLE602 Assessment 2 - Presentation Outline (6 slides, 5-7 min)

*Audio-visual proposal seminar. PDF slides. Every member presents for ~equal time. Slides are visual cues - NOT the full report. Target ~5 min 55 s of speech, leaving buffer inside the 5-7 min window.*

## Speaking split (balanced ~115-120 s each, aligned to report roles)

| Presenter | Role | Slides | Time |
|---|---|---|---|
| **Victor** (Literature lead) | opens + the literature arc | Slide 1 + Slide 3 | ~115 s |
| **Luis** (Implementation / methods lead) | our design + the payoff | Slide 4 + Slide 6 | ~120 s |
| **Juan** (Project management lead) | the problem + plan/risks | Slide 2 + Slide 5 | ~120 s |

> Note: Slide 2 (Problem) content is drawn from Luis's report section, but Juan delivers it so the speaking time balances - presenting is not the same as owning. Adjust freely if the group prefers each owner to also present their own section.

---

## Slide 1 - Title & introduction
**Presenter:** Victor · **Time:** ~25 s

**On slide (visual cues only):**
- Project: **ReviewPulse v3.0 - Aspect-Based Sentiment Analysis with Attention-Based Deep Learning**
- DLE602 Deep Learning - Assessment 2
- Group: Luis Faria (A00187785), Victor [ID], Juan [ID]
- One product-style logo/banner image

**Talking points:** Introduce the group and the one-line project. "We are building a system that reads a customer review and tells you the sentiment *for each thing being talked about* - not just one overall score."

---

## Slide 2 - The problem (why aspect-level matters)
**Presenter:** Juan · **Time:** ~60 s

**On slide:**
- The failing example, big and visual: *"The food was **great** but the service was **slow**."* → one review, two opposite opinions
- A single 😐 label vs two labels: food ✅ / service ❌
- "Sentence-level models (our A1 N-gram, the Zhao et al. CNN) collapse this."

**Talking points:** Lead with the example. Make the audience feel the loss: a business reading "neutral" learns nothing; "food good, service bad" is actionable. State the gap our project closes.

---

## Slide 3 - What the literature shows
**Presenter:** Victor · **Time:** ~90 s

**On slide:**
- A horizontal arc/timeline: **CNN (2018) → aspect-aware + attention LSTM (2016) → BERT-for-ABSA (2019) → LLM / generative + neural aspect discovery (2023-2026)**
- One word under each: *deep but flat → attention → contextual → frontier*
- Tiny "we are here" marker on the explainable, low-compute spot

**Talking points:** Tell it as a story of one limitation being solved step by step, not a paper list. Land on the gap: the frontier is heavy and LLM-driven; few projects pair a *light, explainable* model with faithful attention explanations. That is our niche.

---

## Slide 4 - Our approach
**Presenter:** Luis · **Time:** ~90 s

**On slide:**
- Pipeline diagram: review → (optional neural topic model: discover aspects) → **ATAE-LSTM** & **DistilBERT** → per-aspect sentiment → **attention heatmap**
- Dataset chip: SemEval-2014 (Restaurants + Laptops, pre-annotated)
- Eval chip: accuracy, macro-F1, cross-domain, attention heatmaps

**Talking points:** Two models compared - attention-LSTM vs fine-tuned DistilBERT - on a pre-annotated benchmark (feasibility). The interpretability layer is the differentiator: we show *why*. Mention Topic Modelling as the optional aspect-discovery stage, scoped as stretch.

---

## Slide 5 - Plan & risks
**Presenter:** Juan · **Time:** ~60 s

**On slide:**
- Mini Gantt: Modules 8→12 (data/baseline → ATAE-LSTM → DistilBERT → interpretability+demo → eval+report)
- Top 3 risks → mitigations: small data→dropout/early stopping/transfer · heavy compute→DistilBERT on Colab · scope creep→extraction & topic modelling are gated stretch goals
- Critical success factors: data pre-annotated, light compute, working fallback path

**Talking points:** Show it is feasible and de-risked. Emphasise the fallback: even if the transformer underperforms, the ATAE-LSTM path still hits the rubric.

---

## Slide 6 - Expected contribution
**Presenter:** Luis · **Time:** ~30 s

**On slide:**
- Three icons: **aspect-level** · **explainable (attention)** · **live Streamlit demo**
- Close line: "From one score per review to a transparent, per-aspect read - built and demoed in Assessment 3."

**Talking points:** Recap the payoff in one breath and hand off to A3. End on the demo image - leave them picturing the product.

---

## Production checklist
- [ ] Consistent template (fonts, colours, sizes) across all slides - reflects group dynamic (rubric)
- [ ] Title slide has all names + student IDs + subject
- [ ] Export slides to **PDF** (required format)
- [ ] Record voice-over (online students: voice only, no webcam required); naming `DLE602GroupnameAssessment2.mp4`
- [ ] APA reference slide or in-deck citations consistent with the report
- [ ] Rehearse to land 5-7 min; each member speaks ~equal time
