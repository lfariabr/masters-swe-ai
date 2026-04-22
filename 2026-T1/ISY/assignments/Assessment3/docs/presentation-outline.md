# Presentation Outline — ISY503 Assessment 3

Target duration: 10–15 minutes total.

---

## Speaker Allocation

| Slides | Presenter | Duration | Content |
|---|---|---:|---|
| 1, 4, 5, 6, 7, 12 | **Luis** | ~6.25 min | Title · Preprocessing · Architecture · Training · Results · Summary |
| 3, 8, 10 | **Victor** | ~3.5 min | Dataset · Error Analysis · Ethics & Limitations |
| 2, 9, 11 | **Samiran** | ~3.75 min | Problem Statement · Live Demo · Future Work |

For slide-by-slide speaker notes and suggested wording, see `review-pulse/docs/presentation-outline.md`.

---

## Slide Structure

1. **Title and team** *(Luis)* — ReviewPulse · team members + IDs · one-line pitch
2. **Problem statement** *(Samiran)* — why sentiment analysis matters commercially · why reviews are hard to classify
3. **Dataset overview** *(Victor)* — Blitzer et al. 2007 · 8,000 reviews · 4 domains · 50/50 balance · label audit
4. **Data pipeline** *(Luis)* — parse → clean → audit → outlier removal → stratified split · negation expansion decision
5. **Model architecture** *(Luis)* — TF-IDF + LogReg baseline · BiLSTM + GloVe · pack_padded_sequence
6. **Training** *(Luis)* — Adam · BCEWithLogitsLoss · gradient clipping · F1 checkpoint · epoch 9 best
7. **Evaluation results** *(Luis)* — test set: TF-IDF 81.9% F1 vs BiLSTM 80.3% · honest finding
8. **Error analysis** *(Victor)* — 220 misclassified · negation / sarcasm / out-of-distribution failure modes
9. **Live demo** *(Samiran)* — Streamlit app · positive / negative / negation trap / sarcasm / Generate button
10. **Ethical considerations** *(Victor)* — label noise · domain bias · uncalibrated confidence · dataset age · deployment risk
11. **Future work** *(Samiran)* — DistilBERT/RoBERTa · Platt scaling · more domains · LIME explainability
12. **Summary & questions** *(Luis)* — full pipeline recap · honest result · GitHub link · Q&A

---

## Must Cover From Brief

- Rationale behind project choice *(Samiran — Slide 2)*
- Ethical considerations made during implementation *(Victor — Slide 10)*
- Accuracy of observed outputs *(Luis — Slide 7)*
- Brief explanation of implementation *(Luis — Slides 4, 5, 6)*
- Evidence of teamwork and version control *(GitHub commit history — github.com/lfariabr/review-pulse)*
