# Literature Review - draft section (DLE602 Assessment 2)

*Target ~320-360 words. Critical synthesis, not summary - the arc builds toward our design. APA in-text citations below; confirm authors/year of the 2023-2026 sources against each source before submission (see skeleton reference list).*

---

Deep learning reset the baseline for sentiment analysis: Zhao, Gui and Zhang (2018) show that a convolutional network over word vectors outperforms hand-engineered features for Twitter sentiment. Yet their model, like our Assessment 1 N-gram classifier, resolves a whole text to a single polarity - the very limitation that aspect-based sentiment analysis (ABSA) exists to remove. Pontiki et al. (2014) reframed the problem in SemEval-2014 Task 4, defining the aspect-level benchmark and annotation scheme we adopt and shifting the question from *"is this review positive?"* to *"which aspect is positive?"*.

The sequence-modelling line answers that question by conditioning on the aspect. Tang et al. (2016) show that target-dependent LSTMs (TD-LSTM) outperform target-agnostic ones by encoding the aspect's position, but they still weight all context words equally. Wang et al. (2016) close that gap with ATAE-LSTM, adding an aspect embedding and an attention mechanism so the model learns *which* words matter for *which* aspect - the design we adopt as our first model and the source of our interpretability layer.

The transformer era diverges from recurrence. Devlin et al. (2019) replace sequential encoding with pretrained bidirectional attention, and Sun, Huang and Qiu (2019) adapt BERT to ABSA by constructing an auxiliary sentence per aspect, recasting classification as sentence-pair inference - the basis of our second (DistilBERT) model. Recent work pushes further: comparative benchmarks report strong transformer results on the same SemEval-2014 sets (Jayakody et al., 2024), and large language models now perform ABSA in zero- and few-shot settings (Simmering & Huoviala, 2023), a shift mapped by a recent systematic review of the field (Hua et al., 2024).

We build on, rather than chase, this frontier. Heavy LLM pipelines rarely pair a light, reproducible model with faithful explanations; and where reviews lack gold aspects, neural aspect discovery (He et al., 2017) can surface them unsupervised - our optional Topic Modelling stage. Our niche is explainable, low-compute aspect sentiment, evaluated honestly against this body of work.

*(~350 words)*
