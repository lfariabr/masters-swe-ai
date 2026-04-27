# Building ReviewPulse: A Multi-Domain Sentiment Classifier (with TF-IDF + LR as Baseline and BiLSTM as Neural Network)

Tags: #machinelearning #nlp #python #streamlit
<!-- 117 tests in detail -->
<!-- v1.0.0 in detail -->
<!-- add linkage -->
---

**ISY503 Assessment 1 was a case study. Assessment 2 was a regression notebook. Assessment 3 forced me to ship a working NLP system - parser, models, evaluation, UI, ethics - and defend every choice in front of a marker who was about to type real text into the box.**

---

## Context: Masters' degree ISY503 in 12 Weeks

I am doing my Master's in Software Engineering & AI ([open-sourced repo with 900+ commits in ~1 year](https://github.com/lfariabr/masters-swe-ai)) at Torrens University Australia. **[ISY503 Intelligent Systems](https://github.com/lfariabr/masters-swe-ai/tree/master/2026-T1/ISY/)** is one of the two subjects in my current term (T1-2026). The 12-week ride covers ground in this order:

1. The nature and purpose of intelligent systems
2. Introduction to machine learning
3. Machine learning models
4. Introduction to deep learning
5. Machine learning in depth
6. Machine learning in practice
7. Deep learning in practice
8. Computer vision
9. Natural language processing
10. Speech recognition
11. Emotional intelligence and AI ethics
12. Deploying intelligent systems

The assessments follow the following path:
- Assessment 1 (week 5): a case study on the application of an intelligent system. 
- Assessment 2 (week 8): a programming task on a regression model. 
- Assessment 3 (week 12): build something end to end. 

> The whole subject converges on one question: *can you actually take an ML idea and make it usable?*

In parallel, I am taking [**CCF501 Cloud Computing Fundamentals**](https://github.com/lfariabr/masters-swe-ai/tree/master/2026-T1/CCF), and the more I sit with both subjects, the more obvious it gets: a model file on a laptop helps nobody. The work behind the scene and the interface surrounding the model is the actual work.

---

## The Theory to A Working System

From Assessment 1, the case study, to Assessment 2, I felt the jump from theory to practice, and I loved it. Assessment 3 was different: the brief gave me a dataset of Amazon product reviews, asked for a sentiment classifier, and required a simple interface with a text box, a button, and an output of `Positive review` or `Negative review`. The facilitator would test it with their own inputs.

That last part forces us to keep it honest: a model that only behaves on the test split is not a system, it is a number in a table and a model that has to handle whatever someone types live is a small product.

This article is the build story documenting what I shipped, why I built a baseline I was not asked for, and the result where the simpler model out-performed the neural one on the held-out set.

![ReviewPulse Streamlit app showing the text input, model selector, and classify button](UPLOAD_IMAGE_HERE)

---

## Why ReviewPulse, and not just a notebook with a button

The brief allowed for a simple solution: text area, classify button, label. I could have stopped there, but instead I opted to treat the assessment as a portfolio piece and named it **ReviewPulse**. 4 reasons it was worth the extra scaffolding:

1. **The portfolio signal is ML engineering, not modelling.** Anyone can fit a model: Loading raw data, auditing labels, building a baseline, and shipping a UI is the harder, more interesting story.
2. **A baseline I was not asked for.** Adding a TF-IDF + Logistic Regression model alongside the required neural network is the only honest way to answer "is the architecture earning its keep, or is the data carrying it?"
3. **A name forces product thinking.** A repo called `assessment-3` reads like coursework. A repo called `ReviewPulse` reads like a small product, which forces the README, the app, and the error analysis to be written for a stranger, written for a stranger, which raises my own bar and keeps the build-in-public habit alive.
4. **It plugs into next term.** The deployment patterns, the model interface, and the evaluation harness all transfer into BDA601 Big Data & Analytics in T1-2027. The assessment becomes infrastructure for what comes next.

I'm still tempted to add DistilBERT or RoBERTa as a third model. Both are legit and sit on the future-work list

---

## The Architecture

```
review-pulse/
├── app.py                       # Streamlit UI
├── src/
│   ├── parser.py                # pseudo-XML -> DataFrame
│   ├── preprocess.py            # cleaning, audit, splits
│   ├── dataset.py               # vocab, padding, DataLoaders
│   ├── baseline.py              # TF-IDF + Logistic Regression
│   ├── model.py                 # BiLSTMSentiment
│   ├── train.py                 # training loop + checkpointing
│   ├── inference.py             # predict_sentiment()
│   └── evaluate.py              # metrics, confusion matrix
├── tests/                       # 117 unit tests
└── outputs/                     # saved models, plots, error CSVs
```

The shape is intentional. Each module does one thing. The Streamlit app and the evaluation script both call into the same `predict_sentiment()` function, so there is no second copy of the inference logic hiding in `app.py` waiting to drift.

> *Tip: every time you see two code paths producing predictions, you have a bug waiting to happen. Centralise inference once, call it from anywhere.*

---

## The Dataset

The data is the **Blitzer, Dredze and Pereira (2007)** Amazon multi-domain sentiment corpus. The local copy contains **8,000 labelled reviews** spread across four domains:

| Domain | Positive | Negative |
|---|---:|---:|
| books | 1,000 | 1,000 |
| dvd | 1,000 | 1,000 |
| electronics | 1,000 | 1,000 |
| kitchen_&_housewares | 1,000 | 1,000 |

A few details that mattered later:

- The labels are **derived from filenames** (`positive.review`, `negative.review`), not from independent human annotation. That sounds harmless until you remember the file label is what the model is being asked to learn.
- The files are **pseudo-XML**: tag-shaped but not strict XML. A naive parser falls over.
- Each review carries a star **rating** alongside the text.

I kept the rating column even though it was not the training signal, because a positive-file review with a 2-star rating is exactly the kind of label noise you want to surface during error analysis.

---

## From-Scratch Pipeline

The 4 steps to go from raw `.review` files to a stratified, leakage-safe training set.

### 1. Parse the pseudo-XML

`src/parser.py` walks the four domain folders and turns each `.review` file into rows of `text`, `rating`, `label`, `domain`, `source_file`. BeautifulSoup with the `html.parser` backend handles the tag-soup structure without tripping on malformed XML.

> *Tip: pseudo-XML is the most common shape of "real" research data. Lenient parsers beat strict ones every time.*

### 2. Audit the labels before trusting them

`src/preprocess.py` runs an `audit_labels()` pass that flags:

- 3-star reviews living in either positive or negative files
- positive-file reviews with low ratings
- negative-file reviews with high ratings

In *this* dataset, the audit returned **zero ambiguous rows**. The curators were careful. But the audit code is the more durable artefact. Re-run it on a noisier corpus and the same logic flags exactly the rows you would not want to train on quietly.

### 3. Clean text without erasing sentiment

The classic cleaning trap with sentiment is aggressive normalisation that strips the very tokens the model needs. `"not bad"` is not `"bad"`. The cleaning pipeline lowercases, normalises whitespace and HTML artefacts, strips punctuation conservatively, and **keeps negation cues**. Outliers (very short or very long reviews) are removed after looking at the actual length distribution rather than guessing thresholds.

### 4. Stratified splits, fixed seed

A 70/15/15 train/validation/test split, stratified on label, with a fixed seed. Vocabulary is built **from training text only**, because building it across the full corpus would leak vocabulary signal from the test set into the model and inflate scores.

> *Tip: "vocab from train only" is one of the cheapest data-leakage prevention rules and one of the most commonly skipped.*

---

## Two Models, One Test Set

The brief required a neural network. It did not require a baseline. I built both anyway.

### The baseline

`TfidfVectorizer(max_features=30_000, ngram_range=(1,2)) + LogisticRegression`. Sklearn pipeline, no surprises. The point is not novelty, it is to set a floor that the neural model has to clear.

### The neural model

`BiLSTMSentiment` in PyTorch:

- Embedding layer initialised from **GloVe 100-dimensional** vectors when available, learned otherwise.
- Dropout.
- Bidirectional LSTM.
- Linear head producing a single logit.
- `pack_padded_sequence` so the LSTM ignores padding tokens.

Training details:

| Choice | Value |
|---|---|
| Optimiser | Adam |
| Loss | `BCEWithLogitsLoss` |
| Gradient clipping | Yes |
| Checkpointing | Best validation F1 (not loss) |
| Device | Apple MPS when available |
| Best epoch | 9 |

Validation F1 at the best checkpoint: **84.0%**. The neural model was, on validation, the better classifier.

Then I ran the held-out test set.

---

## The Result

| Model | Test F1 |
|---|---:|
| TF-IDF + Logistic Regression | **81.9%** |
| BiLSTM + GloVe | 80.3% |

The simpler model won.

![Model comparison chart showing TF-IDF Logistic Regression versus BiLSTM test performance](UPLOAD_IMAGE_HERE)

A few honest reflections:

- 8,000 reviews is a small dataset. BiLSTMs are hungry, they often shine only after you give them more data than this.
- TF-IDF with bigrams already captures the most discriminative signal in product reviews. Words like *"refund"*, *"broken"*, *"love"*, *"recommend"* are doing a lot of the work.
- The validation/test gap (84.0% to 80.3%) suggests mild overfitting that a larger, more diverse corpus might have absorbed.

I considered burying this and presenting only validation numbers. I did not. The lesson, *stronger architecture does not automatically mean better generalisation*, is more useful to anyone reading this than a flattering chart.

> *Tip: if the held-out result surprises you, that is information, not embarrassment. Write it up.*

---

## Error Analysis: Where Both Models Failed

Reporting accuracy and F1 is the start. Looking at the *actual rows* both models got wrong is where the engineering happens.

![Confusion matrix from the ReviewPulse evaluation workflow](UPLOAD_IMAGE_HERE)

A representative slice from the demo cases:

| Case | Input (excerpt) | Baseline | BiLSTM |
|---|---|---|---|
| Clear positive | *"This blender is absolutely incredible..."* | Positive 73.8% (correct) | Positive 97.9% (correct) |
| Clear negative | *"Broke after two days..."* | Negative 95.9% (correct) | Negative 99.6% (correct) |
| Negation trap | *"This is not bad at all..."* | Negative 66.9% (wrong) | Negative 74.6% (wrong) |
| Sarcasm | *"Oh great, stopped working after a week..."* | Negative 52.5% (low conf) | Negative 64.6% (low conf) |
| Domain-shifted (books) | *"One of the best thrillers I have read..."* | Positive 69.4% (correct) | Positive 86.2% (correct) |

The shared failure modes were the predictable ones:

#### **Negation:**
neither bag-of-bigrams nor a small BiLSTM reliably handle *"not bad at all"*. The negation flips the polarity, the model averages tokens.

#### **Sarcasm:**
*"oh great"* is positive on the surface and negative in spirit. Both models read the surface.

#### **Mixed sentiment:**
*"the camera is great, but the software crashes"* gets pulled toward whichever sentiment dominates the token count.

#### **Short ambiguous inputs:**
*"It is okay."* lands at low confidence by both models, which is honestly the right behaviour.

#### **Out-of-domain text:**
anything outside books, DVDs, electronics, and kitchen items drifts toward instability.

![Example error analysis output showing negation, sarcasm, or domain-shift failure cases](UPLOAD_IMAGE_HERE)

These are the rows that go on the slide. They are also the rows that make the ethics section concrete instead of generic.

---

## The Streamlit Demo

The brief asked for a text box and a button. The app has both, plus the small affordances that make a demo not feel like a homework submission:

- A **review text area** for free-form input.
- An explicit **Classify** button, no auto-running on every keystroke.
- A **model selector** so the marker can compare baseline vs BiLSTM live.
- A **Generate sample review** button for when someone freezes at the input field.
- A **prediction label** (`Positive review` / `Negative review`) and a **confidence score**, with the label clearly the headline.

![ReviewPulse prediction screen showing a positive review classification with confidence](UPLOAD_IMAGE_HERE)

![ReviewPulse prediction screen showing a negative review classification with confidence](UPLOAD_IMAGE_HERE)

Streamlit was the right call. The audience for this demo is a facilitator with limited time, not a frontend engineer. Streamlit Cloud took the project from `streamlit run app.py` on my laptop to a public URL that fits in a presentation slide.

> *Tip: Streamlit + Streamlit Cloud is the cheapest path from "model on disk" to "model on a URL". For a coursework demo, the trade is correct.*

---

## Ethics and Limitations: Defense in Layers

The ethics section is built around things this *specific* model can actually get wrong.

#### **Label provenance:**
the dataset uses filename-derived labels, not fresh human annotation. The signal is the curator's filing, not necessarily the reviewer's intent. The audit step exists for that reason.

#### **Binary simplification:**
neutral, mixed, and sarcastic reviews are forced into a positive or negative bucket. The model cannot say "I don't know."

#### **Uncalibrated confidence:**
a 98% confidence is the model's logit, not a probability of correctness. High confidence on a sarcasm case still means the model is wrong, just emphatically.

#### **Domain bias:**
the training data is books, DVDs, electronics, and kitchen/housewares. Logistics complaints, healthcare reviews, finance app feedback, social media posts, the model has not earned the right to an opinion on any of those.

#### **The honest gap:**
no production scaffolding. For a marked deployment that lives on Streamlit Cloud, the risk is contained. For anything real, the next steps are confidence calibration (Platt scaling or isotonic regression), human review on low-confidence cases, periodic label audits, broader and fresher data, and explainability tools like LIME or attention maps.

The point is not to hedge. The point is to be specific about what would have to change before this becomes anything more than a coursework demo.

---

## The AI-Assisted Workflow (Being Honest About It)

This article, and a meaningful chunk of the build plan, leaned on AI assistants - it has become the workflow itself, and it is part of how I work. Here's how the labour split actually went:

- **ChatGPT** helped me reason about the validation/test gap and how to frame the baseline-beats-neural result without undermining the assessment requirement.
- **Claude** read the source files (assessment brief, plan, individual report, demo cases, ethics notes) and produced this draft.
- **I** made every architecture decision, ran every command, captured every screenshot, debugged the BiLSTM training loop, audited the labels, and reviewed every word before this article went public.

AI is a planning and drafting accelerator, not a replacement for understanding what you and I deployed or why. Anyone who cannot defend their architecture verbally has skipped the part that matters.

---

## What This Term Taught Me

3 things I am taking forward:

1. **Build the baseline first.** Always. It is cheap, and it is the only honest answer to "did your fancy model help?" The TF-IDF model in this project took 30 minutes. It is the reason I have anything worth writing about.
2. **Validation F1 is not a contract.** The held-out test set is where claims live. If the gap surprises you, that is information, not embarrassment.
3. **A working ML system is a model file plus everything around it.** Parser, preprocessing, splits, baseline, evaluation, error analysis, UI, ethics. Skipping any one of those weakens the whole. The interface around the model is the work.

And a practical one: **stop fighting the cleaning pipeline once it preserves negation cues**. Most "model is broken" debugging in sentiment ends up being preprocessing that ate the wrong tokens.

---

## Building in Public

Studying for a Master's while working a 9-5 job means assignments stop being abstract: the same patterns - data parsing, label audits, baselines before neural models, error analysis on real inputs - show up at work the same week I learn them. I am sharing this publicly because the learning compounds when it is open.

- [Assessment Brief - ISY503 Assessment 3](https://github.com/lfariabr/masters-swe-ai/blob/master/2026-T1/ISY/assignments/Assessment3/ISY503_Assessment3.md)
- [Implementation plan + technical artefacts](https://github.com/lfariabr/masters-swe-ai/tree/master/2026-T1/ISY/assignments/Assessment3)
- [ReviewPulse source code](https://github.com/lfariabr/review-pulse)
- [Live app on Streamlit Cloud](https://review-pulse.streamlit.app/)

If you are training your first NLP model on a small dataset, what surprised you most: the parsing, the cleaning choices, or the moment your baseline beat your neural model?

---

## Let's Connect

- **LinkedIn:** [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)
- **GitHub:** [github.com/lfariabr](https://github.com/lfariabr)
- **Portfolio:** [luisfaria.dev](https://luisfaria.dev)

---

## References

Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? In *Proceedings of the 2021 ACM FAccT Conference* (pp. 610-623). https://doi.org/10.1145/3442188.3445922

Blitzer, J., Dredze, M., & Pereira, F. (2007). Biographies, Bollywood, boom-boxes and blenders: Domain adaptation for sentiment classification. *Proceedings of the 45th Annual Meeting of the Association of Computational Linguistics*, 440-447. https://aclanthology.org/P07-1056/

Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation, 9*(8), 1735-1780. https://doi.org/10.1162/neco.1997.9.8.1735

Pennington, J., Socher, R., & Manning, C. D. (2014). GloVe: Global vectors for word representation. *Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 1532-1543. https://aclanthology.org/D14-1162/

---

*Built with ☕ and a stubborn baseline by [Luis Faria](https://luisfaria.dev)*
