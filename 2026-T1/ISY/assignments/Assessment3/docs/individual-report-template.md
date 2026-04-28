# Individual Contribution Report Template — ISY503 Assessment 3

**Target length:** 250 words ±10% per report

---

## Slide Assignment

| Presenter | Slides | Content | Approx. time |
|---|---|---|---|
| **Luis** | 1, 4, 5, 6, 7, 12 | Title · Preprocessing · Architecture · Training · Results · Summary | ~6.25 min |
| **Victor** | 3, 8, 10 | Dataset · Error Analysis · Ethics & Limitations | ~3.5 min |
| **Samiran** | 2, 9, 11 | Problem Statement · Live Demo · Future Work | ~3.75 min |

---

## Luis Faria — A00187785

### Student Details

- **Name:** Luis G. B. A. Faria
- **Student ID:** A00187785
- **Slides presented:** 1, 4, 5, 6, 7, 12 (Title · Preprocessing · Architecture · Training · Results · Summary)
- **GitHub:** https://github.com/lfariabr/review-pulse

### Team Contribution Table

| Team Member | Student ID | Main Contribution | % |
|---|---|---|---:|
| Luis Faria | A00187785 | Full v1.0.0 technical implementation, app, tests, docs, PR hardening | 60% |
| Victor Meneses | A00179705 | DistilBERT implementation (v2.0.0), dataset analysis, error analysis, ethics presentation | 25% |
| Samiran Shrestha | A00106473 | Problem framing, live demo, future work | 15% |
| **Total** | | | **100%** |

### Draft Report (~250 words)

My primary contribution to ReviewPulse was the full technical implementation of the v1.0.0 ML pipeline — nine source modules, the Streamlit web app, 117 unit tests, all project documentation, and hardening of Victor's DistilBERT extension (PR #22) through Issues #23–#27.

On the data side, I built the pseudo-XML parser (`src/parser.py`), the preprocessing pipeline with negation expansion (`src/preprocess.py`), and the vocabulary builder and PyTorch DataLoaders (`src/dataset.py`). I then implemented both v1 models: the TF-IDF + Logistic Regression baseline (`src/baseline.py`) and the bidirectional LSTM (Hochreiter & Schmidhuber, 1997) initialised with GloVe 100-dimensional embeddings (`src/model.py`). The training loop (`src/train.py`) uses Adam with gradient clipping, F1-based checkpointing, and Apple MPS device support. I implemented evaluation with confusion matrix and error analysis (`src/evaluate.py`), a unified inference API (`src/inference.py`), and the Streamlit web app with model selector and sample review generator (`app.py`). I also produced the presentation outline, 10 acceptance test cases with real model outputs, and this document.

An important ethical consideration is that the Blitzer et al. (2007) dataset uses filename-derived labels rather than human raters. We audited for possible rating/text conflicts and ambiguous boundary cases and found zero ambiguous rows, but the risk remains relevant in broader sentiment classification settings. BiLSTM and DistilBERT confidence values are uncalibrated — high confidence does not imply high accuracy — and both models generalise poorly to out-of-distribution text such as logistics reviews (Bender et al., 2021). Any production deployment requires human oversight and periodic label audits.

I estimate my contribution at 60% as the primary v1.0.0 technical implementer. Victor contributed 25% covering the DistilBERT implementation, dataset analysis, error analysis, and ethics. Samiran contributed 15% covering the problem framing, live demo delivery, and future work.

### APA References

- Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? In *Proceedings of the 2021 ACM FAccT Conference* (pp. 610–623). https://doi.org/10.1145/3442188.3445922
- Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, Boom-boxes and Blenders: Domain adaptation for sentiment classification. In *Proceedings of the 45th Annual Meeting of the ACL* (pp. 440–447). ACL. https://aclanthology.org/P07-1056/
- Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation, 9*(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735

---

## Victor Meneses — A00179705

### Student Details

- **Name:** Victor Meneses
- **Student ID:** A00179705
- **Slides presented:** 3, 8, 10 (Dataset · Error Analysis · Ethics & Limitations)
- **Code contribution:** DistilBERT implementation (`src/model_bert.py`, `src/train_bert.py`, PR #22)

### Team Contribution Table

| Team Member | Student ID | Main Contribution | % |
|---|---|---|---:|
| Luis Faria | A00187785 | Full v1.0.0 technical implementation, app, tests, docs, PR hardening | 60% |
| Victor Meneses | A00179705 | DistilBERT implementation (v2.0.0), dataset analysis, error analysis, ethics presentation | 25% |
| Samiran Shrestha | A00106473 | Problem framing, live demo, future work | 15% |
| **Total** | | | **100%** |

### Draft Report (~250 words) — suggested content

My primary contribution to ReviewPulse was implementing the Hugging Face DistilBERT extension (v2.0.0) and presenting the dataset analysis, error analysis, and ethical considerations.

On the technical side, I implemented `src/model_bert.py` — a wrapper around `distilbert-base-uncased` from Hugging Face — and `src/train_bert.py` — the full training loop with head-first fine-tuning, partial encoder unfreezing, and checkpoint serialisation to `outputs/distilbert.pt`. The training strategy freezes the DistilBERT encoder and trains the classification head first, then unfreezes the last two transformer layers for partial fine-tuning. The compact 29 MB checkpoint is integrated into the Streamlit app as a selectable third model. On the held-out test set, DistilBERT achieved 88.2% accuracy and 88.6% F1, outperforming both the TF-IDF baseline (81.9% F1) and the BiLSTM (80.3% F1) by a clear margin (Devlin et al., 2019).

I presented slides 3, 8, and 10. Slide 3 covers the Blitzer et al. (2007) dataset — 8,000 Amazon reviews across four domains, balanced at 50/50, with a zero-ambiguity label audit. Slide 8 covers the 220 misclassified examples across v1 models: negation, sarcasm, and out-of-distribution failure modes. Slide 10 addresses ethics: label noise, domain bias, dataset age, and deployment risk.

An important ethical consideration I want to highlight is that DistilBERT confidence values remain uncalibrated — the model can output 95% confidence on incorrect predictions. Platt scaling is the recommended next step before any production use.

I estimate my contribution at 25%. Luis contributed 60% as the primary v1.0.0 implementer and PR hardening. Samiran contributed 15% covering problem framing, live demo delivery, and future work.

### APA References

- Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, Boom-boxes and Blenders: Domain adaptation for sentiment classification. In *Proceedings of the 45th Annual Meeting of the ACL* (pp. 440–447). ACL. https://aclanthology.org/P07-1056/
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. In *Proceedings of NAACL-HLT 2019* (pp. 4171–4186). https://doi.org/10.18653/v1/N19-1423
- Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. *Foundations and Trends in Information Retrieval, 2*(1–2), 1–135. https://doi.org/10.1561/1500000011

---

## Samiran Shrestha — A00106473

### Student Details

- **Name:** Samiran Shrestha
- **Student ID:** A00106473
- **Slides presented:** 2, 9, 11 (Problem Statement · Live Demo · Future Work)

### Team Contribution Table

| Team Member | Student ID | Main Contribution | % |
|---|---|---|---:|
| Luis Faria | A00187785 | Full v1.0.0 technical implementation, app, tests, docs, PR hardening | 60% |
| Victor Meneses | A00179705 | DistilBERT implementation (v2.0.0), dataset analysis, error analysis, ethics presentation | 25% |
| Samiran Shrestha | A00106473 | Problem framing, live demo, future work | 15% |
| **Total** | | | **100%** |

### Draft Report (~250 words) — suggested content

My primary contribution to ReviewPulse was framing the problem for the audience, running the live demo, and presenting the future work roadmap, as well as contributing to [any additional work: research, documentation, team coordination].

I presented slides 2, 9, and 11. Slide 2 establishes the commercial motivation for sentiment analysis — product feedback loops, brand monitoring, recommendation systems — and articulates the core challenge: real reviews are messy. They vary in length from two words to over 800, span multiple domains, use negation ("not bad at all"), and employ sarcasm ("oh great, another broken product"). I framed our goal as building two systems and letting the data decide which one wins.

Slide 9 is the live demo. I ran the Streamlit app live, demonstrating a clear positive, a clear negative, the negation failure mode, and the sarcasm case where both v1 models sit near 50% confidence — which is honest uncertainty, not a hard error. I also demonstrated the DistilBERT option, which handles the negation case more confidently due to its contextual pre-training. I showed the Generate button to load a random acceptance test case.

Slide 11 presents the next steps after DistilBERT (v2.0.0): RoBERTa for further accuracy gains; Platt scaling for confidence calibration; additional training domains; and LIME for explainability.

An important ethical consideration is that binary sentiment classification is reductive. Real reviews express nuanced opinions — mixed, hedged, or ironic — that a positive/negative label cannot capture. Deploying a binary classifier in high-stakes contexts risks suppressing legitimate nuance.

I estimate my contribution at 15% covering the problem framing, live demo delivery, and future work. Luis contributed 60% as the primary v1.0.0 implementer. Victor contributed 25% covering the DistilBERT implementation, dataset analysis, error analysis, and ethics.

### APA References

- Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, Boom-boxes and Blenders: Domain adaptation for sentiment classification. In *Proceedings of the 45th Annual Meeting of the ACL* (pp. 440–447). ACL. https://aclanthology.org/P07-1056/
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. In *Proceedings of NAACL-HLT 2019* (pp. 4171–4186). https://doi.org/10.18603/v1/N19-1423

---

## Notes for all team members

- **Word count:** 250 words ±10% (225–275). The draft sections above are calibrated to this target — trim or expand as needed.
- **Percentage split:** 60% Luis / 25% Victor / 15% Samiran — agreed and fixed for v2.0.0.
- **Ethics paragraph:** Each report includes a distinct ethical angle — do not duplicate across reports.
- **Speaker notes:** Work from `review-pulse/docs/presentation-outline.md` for slide-specific wording.
- **GitHub evidence:** Luis's commit history + Victor's PR #22 are the primary evidence records.
