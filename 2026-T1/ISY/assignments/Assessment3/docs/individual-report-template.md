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
- **Project:** ReviewPulse — Multi-domain Amazon Review Sentiment Classifier (NLP)
- **GitHub:** https://github.com/lfariabr/review-pulse

### Team Contribution Table

| Team Member | Student ID | Main Contribution | Percentage |
|---|---|---|---:|
| Luis Faria | A00187785 | Full technical implementation, app, tests, docs | TBD |
| Victor Meneses | A00179705 | Dataset, error analysis, ethics presentation | TBD |
| Samiran Shrestha | A00106473 | Problem framing, live demo, future work | TBD |
| **Total** | | | **100%** |

### Draft Report

I contributed to the NLP sentiment analysis project by implementing the full technical pipeline. My work spanned nine source modules: a pseudo-XML parser (`parser.py`), preprocessing with negation expansion (`preprocess.py`), vocabulary builder and PyTorch DataLoaders (`dataset.py`), TF-IDF + Logistic Regression baseline (`baseline.py`), and a bidirectional LSTM initialised with GloVe embeddings (`model.py`). I implemented the training loop with MPS device support and F1-based checkpointing (`train.py`), evaluation with confusion matrix and error analysis (`evaluate.py`), a unified inference API (`inference.py`), and the Streamlit web application (`app.py`). I also wrote 117 unit tests, produced the presentation outline, and documented 10 acceptance test cases with real model outputs.

An important ethical consideration is that the Blitzer et al. (2007) dataset uses filename-derived labels rather than human raters — star ratings and review text may conflict. Three-star reviews are excluded entirely, which risks mislabelling boundary-sentiment cases. We audited this explicitly (zero ambiguous rows found). BiLSTM confidence scores are also uncalibrated — 98% confidence does not imply 98% accuracy — and the model generalises poorly to out-of-distribution text such as logistics reviews. Any production deployment requires human oversight and periodic label audits.

I estimate my contribution at [X%]. Victor contributed [Y%] covering dataset analysis, error analysis, and ethics. Samiran contributed [Z%] covering problem framing, live demo delivery, and future work.

### APA References

- Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, Boom-boxes and Blenders: Domain adaptation for sentiment classification. In *Proceedings of the 45th Annual Meeting of the ACL* (pp. 440–447). ACL. https://aclanthology.org/P07-1056/
- Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation, 9*(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735
- Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? In *Proceedings of the 2021 ACM FAccT Conference* (pp. 610–623). https://doi.org/10.1145/3442188.3445922

---

## Victor Meneses — A00179705

### Student Details

- **Name:** Victor Meneses
- **Student ID:** A00179705
- **Slides presented:** 3, 8, 10 (Dataset · Error Analysis · Ethics & Limitations)

### Team Contribution Table

| Team Member | Student ID | Main Contribution | Percentage |
|---|---|---|---:|
| Luis Faria | A00187785 | Full technical implementation, app, tests, docs | TBD |
| Victor Meneses | A00179705 | Dataset, error analysis, ethics presentation | TBD |
| Samiran Shrestha | A00106473 | Problem framing, live demo, future work | TBD |
| **Total** | | | **100%** |

### Draft Report

I contributed to the ReviewPulse project by presenting the dataset analysis, error analysis, and ethical considerations, and [describe any additional contributions: research, documentation, team coordination].

I presented slides 3, 8, and 10. Slide 3 covers the Blitzer et al. (2007) dataset — 8,000 Amazon reviews across four domains, perfectly balanced at 50/50 with labels derived from filenames rather than star ratings. I explained the stratified 70/15/15 split and our label audit result: zero ambiguous or conflicting rows. Slide 8 covers the 220 misclassified examples: negation ("not bad at all" predicted as Negative because "bad" dominates), sarcasm (low confidence near 50%, which is honest uncertainty), and out-of-distribution text such as logistics reviews. Slide 10 covers ethics: label noise, domain bias, uncalibrated confidence values, the 20-year age of the dataset, and deployment risk.

An important ethical consideration I focused on is dataset age. The Blitzer et al. (2007) data was collected approximately 20 years ago — emoji, platform slang, and short-form text were not common in product reviews at that time. This temporal gap may cause the model to underperform on modern review styles. Periodic retraining on more recent data would reduce this distributional shift risk.

I estimate my contribution at [X%]. Luis contributed [Y%] as the primary technical implementer. Samiran contributed [Z%] covering problem framing, live demo, and future work.

### APA References

- Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, Boom-boxes and Blenders: Domain adaptation for sentiment classification. In *Proceedings of the 45th Annual Meeting of the ACL* (pp. 440–447). ACL. https://aclanthology.org/P07-1056/
- Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. *Foundations and Trends in Information Retrieval, 2*(1–2), 1–135. https://doi.org/10.1561/1500000011

---

## Samiran Shrestha — A00106473

### Student Details

- **Name:** Samiran Shrestha
- **Student ID:** A00106473
- **Slides presented:** 2, 9, 11 (Problem Statement · Live Demo · Future Work)

### Team Contribution Table

| Team Member | Student ID | Main Contribution | Percentage |
|---|---|---|---:|
| Luis Faria | A00187785 | Full technical implementation, app, tests, docs | TBD |
| Victor Meneses | A00179705 | Dataset, error analysis, ethics presentation | TBD |
| Samiran Shrestha | A00106473 | Problem framing, live demo, future work | TBD |
| **Total** | | | **100%** |

### Draft Report

I contributed to the ReviewPulse project by framing the problem for the audience, running the live demo, and presenting the future work roadmap, as well as [describe any additional contributions: research, documentation, team coordination].

I presented slides 2, 9, and 11. Slide 2 establishes the commercial motivation for sentiment analysis — product feedback loops, brand monitoring, recommendation systems — and articulates the core challenge: real reviews are messy. They vary in length, span multiple domains, use negation ("not bad at all"), and employ sarcasm. I framed the goal as building two systems and letting the data decide which one wins. Slide 9 is the live demo: I ran the Streamlit app, demonstrating clear positive and negative cases, the negation failure mode, and the sarcasm case where both models sit near 50% confidence. Slide 11 presents four concrete next steps: DistilBERT or RoBERTa for contextual embeddings, Platt scaling for confidence calibration, additional training domains, and LIME for explainability.

An important ethical consideration is that binary sentiment classification is reductive. Real reviews express nuanced opinions — mixed, hedged, or ironic — that a positive/negative label cannot capture. Deploying a binary classifier in high-stakes contexts risks suppressing legitimate nuance and misleading decision-makers.

I estimate my contribution at [X%]. Luis contributed [Y%] as the primary technical implementer. Victor contributed [Z%] covering dataset analysis, error analysis, and ethics.

### APA References

- Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, Boom-boxes and Blenders: Domain adaptation for sentiment classification. In *Proceedings of the 45th Annual Meeting of the ACL* (pp. 440–447). ACL. https://aclanthology.org/P07-1056/
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. In *Proceedings of NAACL-HLT 2019* (pp. 4171–4186). https://doi.org/10.18653/v1/N19-1423
