# Individual Contribution Report — ISY503 Assessment 3
**Target length:** 250 words ±10% per report

---

## Luis Faria — A00187785

### 1. Group Details

| Student ID | Name | Email |
|---|---|---|
| A00187785 | Luis Guilherme de Barros Andrade Faria | Luis.Faria@Student.Torrens.edu.au |
| A00106473 | Samiran Shrestha | Samiran.Shrestha@Student.Torrens.edu.au |
| A00179705 | Victor Javier Dorantes Meneses | Victor.Meneses@Student.Torrens.edu.au |

> - Source code: https://github.com/lfariabr/review-pulse
> - Presentation: http://
> - Video recording: http://
> - Live Demo: https://review-pulse.streamlit.app/

### 2. Team Contribution Table

| Team Member | Student ID | Main Contribution | % |
|---|---|---|---:|
| Luis Faria | A00187785 | Full technical implementation, app, tests, docs | 60% |
| Victor Meneses | A00179705 | Dataset, error analysis, ethics presentation | 20% |
| Samiran Shrestha | A00106473 | Problem framing, live demo, future work | 20% |
| **Total** | | | **100%** |

### 3. Draft Report (~250 words)

My primary contribution to ReviewPulse was the full technical implementation of the ML pipeline — nine source modules, the Streamlit web app, 117 unit tests, and all project documentation.

On the data side, I built the pseudo-XML parser (`src/parser.py`), the preprocessing pipeline with negation expansion (`src/preprocess.py`), and the vocabulary builder and PyTorch DataLoaders (`src/dataset.py`). I then implemented both models: the TF-IDF + Logistic Regression baseline (`src/baseline.py`) and the bidirectional LSTM (Hochreiter & Schmidhuber, 1997) initialised with GloVe 100-dimensional embeddings (`src/model.py`). The training loop (`src/train.py`) uses Adam with gradient clipping, F1-based checkpointing, and Apple MPS device support. I implemented evaluation with confusion matrix and error analysis (`src/evaluate.py`), a unified inference API (`src/inference.py`), and the Streamlit web app with model selector and sample review generator (`app.py`). I also produced the presentation outline, 10 acceptance test cases with real model outputs, and this document.

An important ethical consideration is that the Blitzer et al. (2007) dataset uses filename-derived labels rather than human raters. Because the dataset uses filename-derived labels rather than direct human annotation, we audited for possible rating/text conflicts and ambiguous boundary cases. In this dataset, we found zero ambiguous rows, but the risk remains relevant in broader sentiment classification settings. BiLSTM confidence values are also uncalibrated — 98% confidence does not imply 98% accuracy — and the model generalises poorly to out-of-distribution text such as logistics reviews (Bender et al., 2021). Any production deployment requires human oversight and periodic label audits.

I estimate my contribution at 60% as the primary technical implementer. Victor contributed 20% covering dataset analysis, error analysis, and ethics. Samiran contributed 20% covering the problem framing, live demo delivery, and future work.

### 4. Appendices

**A1 — GitHub Repository**
https://github.com/lfariabr/review-pulse

**A2 — Live App**
https://review-pulse.streamlit.app/

*[Insert 2–3 screenshots: (i) sidebar with model selector, (ii) positive review prediction with confidence bar, (iii) negation trap case showing failure mode]*

**A3 — Sample Test Cases Output**

Ten acceptance test cases run against both trained models (baseline checkpoint `outputs/baseline.joblib`, BiLSTM checkpoint `outputs/bilstm.pt` epoch 9):

> *Table A3. Sample Test Cases Output.*

| Case | Input (excerpt) | Baseline | BiLSTM |
|---|---|---|---|
| Clear positive | "This blender is absolutely incredible…" | Positive 73.8% ✅ | Positive 97.9% ✅ |
| Clear negative | "Broke after two days…" | Negative 95.9% ✅ | Negative 99.6% ✅ |
| Negation trap | "This is not bad at all…" | Negative 66.9% ❌ | Negative 74.6% ❌ |
| Sarcasm | "Oh great, stopped working after a week…" | Negative 52.5% ⚠️ | Negative 64.6% ⚠️ |
| Domain-shifted (books) | "One of the best thrillers I have read…" | Positive 69.4% ✅ | Positive 86.2% ✅ |

Full results: https://github.com/lfariabr/review-pulse/blob/main/docs/demo-test-cases.md

**A4 — Future Work**

> *Table A4. Future Work possibilities and opportunities.*

| Priority | Extension | Rationale |
|---|---|---|
| High | DistilBERT / RoBERTa | Contextual embeddings handle negation and sarcasm through attention — the shared failure mode in both current models |
| High | Confidence calibration (Platt scaling) | BiLSTM logits are uncalibrated; 98% confidence ≠ 98% accuracy |
| Medium | Additional training domains | Current model is trained on 4 product categories only; broader domains would validate generalisation |
| Medium | LIME / attention visualisation | Makes predictions auditable — necessary for any production or high-stakes deployment |
| Low | FastAPI backend | Decouple inference from Streamlit for easier integration with external systems |

### 5. Statement of Acknowledgement

I acknowledge that I have used the following AI tool(s) in the creation of this report:
- Anthropic Claude Sonnet 4.6
- OpenAI ChatGPT

Both tools were used to assist with understanding ML concepts, structuring the technical pipeline, improving clarity of academic language, and supporting APA 7th referencing conventions.

Prompt examples:
1. "I built a BiLSTM sentiment classifier with `pack_padded_sequence` to stop the LSTM processing padding tokens. My training achieves val F1=84.0% at epoch 9, but test F1 drops to 80.3% while the TF-IDF baseline reaches 81.9% on the same held-out set. Can you help me understand why the neural model didn't generalise better despite the stronger validation score?"
2. "I need to compare two approaches for sentiment analysis — TF-IDF + Logistic Regression vs BiLSTM with GloVe — in an academic report where the simpler model wins on the held-out test set. How do I frame this honestly without undermining the neural architecture requirement of the assessment rubric?"
3. "Format this as APA 7th: Bender, Emily M., Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell, 2021, article titled On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?, conference ACM FAccT 2021, pages 610 to 623."

I confirm that the use of these tools has been in accordance with the Torrens University Australia Academic Integrity Policy and TUA, Think and MDS's Position Paper on the Use of AI. I confirm that the final output is authored by me and represents my own critical thinking, analysis, and synthesis of sources. I take full responsibility for the final content of this report.

### References

- Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? In *Proceedings of the 2021 ACM FAccT Conference* (pp. 610–623). https://doi.org/10.1145/3442188.3445922
- Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, Boom-boxes and Blenders: Domain adaptation for sentiment classification. In *Proceedings of the 45th Annual Meeting of the ACL* (pp. 440–447). ACL. https://aclanthology.org/P07-1056/
- Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation, 9*(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735
