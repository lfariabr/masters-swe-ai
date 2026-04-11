# Module 09 — Natural Language Processing
## ISY503 Intelligent Systems

## Task List

| # | Task | Status |
|---|------|--------|
| 1 | **Watch & summarise CrashCourse (2017) — NLP overview video** | **✅** |
| 2 | **Read & summarise Ali (2023) — NLTK sentiment analysis tutorial** | **✅** |
| **3** | **Read & summarise Hardeniya (2016) — text classification Ch.6** | **✅** |
| **4** | **Read & summarise Thanaki (2017) — deep learning for NLU/NLG Ch.9** | **✅** |
| **5** | **Read & summarise Devlin & Chang (2018) — Open Sourcing BERT** | **✅** |
| 6 | Activity 1: Read Metz (2019) bias article + write 100-word report | 🕐 |
| 7 | Activity 2: Read Ben Abacha & Zweigenbaum (2015) MEANS + peer discussion | 🕐 |

---

## Key Highlights

### 1. CrashCourse. (2017). Natural Language Processing: Crash Course Computer Science #36

**Citation:** CrashCourse. (2017, 22 November). Natural language processing: Crash course computer science #36 [Video file]. Retrieved from https://www.youtube.com/watch?v=fOvTtapxa9c

**Purpose:** Introductory overview of NLP — from sentence parsing and chatbots to the physics of speech recognition (spectrograms, phonemes) and speech synthesis. Bridges linguistics and computer science in ~12 minutes.

---

#### 1. Why NLP Is Hard
- Programming languages are small, rigid, error-intolerant — natural languages are the opposite
- Natural languages have: large diverse vocabularies, ambiguous words, multiple meanings, accents, slurring, implicit context
- NLP = interdisciplinary field combining **computer science + linguistics**

#### 2. Sentence Deconstruction — Parts of Speech & Parse Trees
- **9 parts of speech:** noun, pronoun, article, verb, adjective, adverb, preposition, conjunction, interjection
- Problem: many words have multiple roles — "rose" and "leaves" can be noun or verb
- Solution: **phrase structure rules** — encode grammar formally, e.g.:
  - Sentence → Noun Phrase + Verb Phrase
  - Noun Phrase → Article + Noun | Adjective + Noun
- **Parse tree:** applies those rules to a sentence → tags every word + reveals sentence structure
- Enables voice search decomposition: "where's the nearest pizza?" → question type: WHERE, noun: pizza, dimension: nearest

#### 3. Natural Language Generation
- Phrase structure rules work **both ways** — parsing input AND generating output text
- **Knowledge Graph** (Google, 2016): ~70 billion facts + relationships between entities → used to craft informational sentences
- Example output: *"Thriller was released in 1983 and sung by Michael Jackson"*

#### 4. Chatbots — Rule-Based → ML-Based

| Era | Approach | Example | Limitation |
|-----|----------|---------|------------|
| 1960s | Rule-based (hundreds of hand-coded rules) | ELIZA (MIT, therapist bot) | Brittle, unwieldy to maintain |
| Modern | ML-trained on gigabytes of real human chat | Customer service bots | Still fails on complex/ambiguous intent |

- Facebook experiment: chatbots negotiating with each other developed a **simplified protocol** (not "evil" — just efficient compression of communication)

#### 5. Speech Recognition — How It Works

**Historical milestones:**

| Year | System | Capability |
|------|--------|-----------|
| 1952 | Audrey (Bell Labs) | 10 digits, spoken slowly |
| 1962 | IBM Shoebox | 16 words |
| 1971–76 | Harpy (Carnegie Mellon, DARPA-funded) | 1,000+ words |
| 1980s–90s | ML-based systems | Real-time continuous speech |
| Today | Deep neural networks | State-of-the-art accuracy |

**Signal processing pipeline:**

```
Microphone → Waveform (amplitude vs time)
           → Spectrogram (frequency vs time, via Fast Fourier Transform)
           → Identify formants (resonance peaks)
           → Match phonemes (~44 in English)
           → Separate words + sentences
           → Text output
```

- **Waveform:** raw audio — amplitude of diaphragm displacement over time
- **Spectrogram:** converts waveform to frequency-domain view; brightness = loudness of that frequency
- **Fast Fourier Transform (FFT):** algorithm that converts waveform → spectrum (like an EQ visualiser)
- **Formants:** resonance peaks in the spectrum; each vowel has a distinctive formant pattern
- **Phonemes:** ~44 sound pieces that make up English words; speech recognition = pattern-matching phonemes in spectrograms

#### 6. Language Models Improve Accuracy
- People say words differently (accents, mispronunciations) → ambiguity in phoneme matching
- **Language model:** stores statistics about word sequences
  - "she was" is most likely followed by an adjective → if recogniser is unsure between "happy" vs "harpy", it picks "happy"
- Combining acoustic signal analysis + language model statistics = significantly higher accuracy

#### 7. Speech Synthesis (Text-to-Speech)
- Reverse of recognition: text → break into phonemes → play sounds in sequence
- 1937 Bell Labs: audible but robotic phoneme chaining
- 1980s: improved but still discontinuous/awkward
- Today (Siri, Cortana, Alexa): much better — but not quite human yet
- **Positive feedback loop:** more voice usage → more training data → better accuracy → more usage

#### Key Takeaways for ISY503
1. Parse trees and phrase structure rules are the foundation of voice assistants — every "hey Siri" query runs through this pipeline
2. Spectrograms + FFT + phoneme matching explain *why* accents affect accuracy — the formant patterns shift
3. The ML shift in chatbots (rule-based → data-driven) mirrors the same evolution seen in computer vision (Module 8) and classification (Module 3)

---

### 2. Ali, M. (2023). NLTK Sentiment Analysis Tutorial for Beginners

**Citation:** Navlani, A. (2019). Text Analytics for Beginners using NLTK. Retrieved from https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk *(Note: updated version authored by Moez Ali, 2023)*

**Purpose:** Practical step-by-step guide to text preprocessing and sentiment analysis using Python's NLTK library. Demonstrates the full pipeline from raw text to VADER sentiment scores on real Amazon review data.

---

#### 1. What is Sentiment Analysis?
- **Definition:** Determining the emotional tone (positive, negative, neutral) of a piece of text
- **Applications:** brand monitoring, customer feedback, market research, social media analysis
- **Challenge:** sarcasm, irony, and figurative language are hard for rule-based systems

#### 2. Three Sentiment Analysis Methodologies

| Method | How it works | Pros | Cons |
|--------|-------------|------|------|
| **Lexicon-based (VADER)** | Predefined rules, scores for positive/negative words | Simple, interpretable, no training data needed | Less accurate on complex/ambiguous text |
| **ML-based** | Train a classifier (SVM, Decision Tree, NN) on labelled data | More accurate on complex text | Requires labelled data; computationally expensive |
| **Transformer-based (BERT, GPT-4)** | Pre-trained on massive corpora, fine-tuned | State-of-the-art accuracy | Needs significant compute; not always practical |

#### 3. Text Preprocessing Pipeline
- **Tokenization:** splits raw text into individual words/tokens using `nltk.word_tokenize()`
- **Stop word removal:** filters high-frequency, low-meaning words ("the", "and", "of") using `nltk.corpus.stopwords`
- **Stemming:** removes suffixes to get the root form ("jumping" → "jump")
- **Lemmatization:** reduces to dictionary base form based on POS ("jumped" → "jump"; "jumping" → "jumping" as present participle) — via `WordNetLemmatizer`

#### 4. Bag of Words (BoW) Model
- Represents each document as a **vector of word frequencies**
- Ignores word order and grammar — just counts occurrences
- Essential for feeding text into ML algorithms that require numerical input
- VADER accepts raw text directly, so BoW is not needed for the lexicon-based pipeline

#### 5. End-to-End VADER Pipeline (Amazon Reviews)
```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return 1 if scores['pos'] > 0 else 0

df['sentiment'] = df['reviewText'].apply(get_sentiment)
```
- `polarity_scores()` returns `{'neg': x, 'neu': y, 'pos': z, 'compound': w}`
- Threshold of `pos > 0` → classified as positive (1), otherwise negative (0)

#### Key Takeaways for ISY503
1. VADER is the quickest entry point for Assessment 3 sentiment tasks — no training data required
2. For higher accuracy, the pipeline shown here extends naturally to ML or BERT-based classifiers (Resource 5)
3. The preprocessing steps (tokenize → stop words → lemmatize) are standard across all NLP pipelines in this module

---

### 3. Hardeniya, N. et al. (2016). Natural Language Processing: Python and NLTK — Chapter 6

**Citation:** Hardeniya, N. (2016). Natural language processing: Python and NLTK. Birmingham, England: Packt.

**Purpose:** Chapter 6 builds a practical end-to-end text classification system — from preprocessing and TF-IDF feature extraction to supervised classifiers (Naive Bayes, SVM, Random Forest) and unsupervised topic modelling (K-means, LDA, LSI) — using SMS spam detection as the running example.

---

#### 1. Text Classification as an NLP Problem
- **Text classification** = assigning a label to a document based on its content
- Challenge: ML algorithms need **numerical input**, but text is unstructured
- Solution: convert text → numerical features via **TF-IDF** or **BoW**

#### 2. TF-IDF — Term Frequency–Inverse Document Frequency
- **TF (Term Frequency):** how often a word appears in a document
- **IDF (Inverse Document Frequency):** penalises words that appear in many documents (they carry less discriminative signal)
- **TF-IDF score** = TF × IDF → high for rare, distinctive words; low for common words like "the"
- Transforms the text corpus into a **Term-Document Matrix (TDM)** used as feature input for classifiers

#### 3. Supervised Classification Algorithms for Text

| Algorithm | Best used when | Key trait |
|-----------|---------------|-----------|
| **Naive Bayes** | Small datasets, baseline | Fast, probabilistic, assumes feature independence |
| **SVM (Support Vector Machine)** | High-dimensional text data | Finds maximum-margin hyperplane; strong for sparse TF-IDF vectors |
| **Random Forest** | General purpose, robust | Ensemble of decision trees on random feature subsets; currently one of the best performers |

```python
from sklearn.ensemble import RandomForestClassifier
RF_clf = RandomForestClassifier(n_estimators=10)
predicted = RF_clf.predict(X_test)
```

#### 4. Text Clustering — Unsupervised Grouping
- **Use case:** "I have millions of unlabelled documents — can I group them into meaningful categories?"
- **K-means algorithm:**
  1. Pick `k` random centroids
  2. Assign each document to its nearest centroid
  3. Recompute centroids
  4. Repeat until centroids stabilise
- Uses the same TF-IDF matrix as input
- `MiniBatchKMeans` available for large datasets to reduce training time

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=5, init='k-means++', max_iter=100)
km.fit(X_train)
```

#### 5. Topic Modelling — LDA and LSI

| Method | Full name | Approach |
|--------|-----------|---------|
| **LDA** | Latent Dirichlet Allocation | Probabilistic: each doc is a mix of topics; each topic is a mix of words |
| **LSI** | Latent Semantic Indexing | Linear algebra (SVD): finds latent semantic dimensions in the corpus |

- Both implemented via the **gensim** library
- Input: BoW or TF-IDF corpus
- Output: top terms per topic + document-topic assignments

```python
from gensim import corpora, models
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=5)
```

#### Key Takeaways for ISY503
1. TF-IDF + SVM is the practical gold standard for text classification — outperforms pure BoW in most tasks
2. K-means is reused from Module 3 clustering; applying it to text uses the exact same logic but over TF-IDF vectors
3. LDA/LSI are powerful for exploration when you have no labels — e.g., discovering themes in customer reviews

---

### 4. Thanaki, J. (2017). Python Natural Language Processing — Chapter 9

**Citation:** Thanaki, J. (2017). Python Natural Language Processing. Birmingham, England: Packt.

**Purpose:** Chapter 9 introduces deep learning for NLP — distinguishes NLU from NLG, covers ANN/DNN fundamentals, implements machine translation (LSTM encoder-decoder + attention), and demonstrates abstractive summarisation as an NLG application.

---

#### 1. NLU vs NLG

| Dimension | NLU (Natural Language Understanding) | NLG (Natural Language Generation) |
|-----------|--------------------------------------|----------------------------------|
| **Goal** | Machine *comprehends* human language | Machine *produces* human language |
| **Focus** | Syntax, semantics, ambiguity resolution | Coherence, fluency, relevance |
| **Key challenge** | Pragmatics ambiguity (long-distance context) | Ensuring generated text is coherent |
| **DL example** | Machine translation (understanding source) | Abstractive summarisation |
| **App example** | Google NER, POS taggers, question answering | Gmail Smart Reply, image captioning |

#### 2. Stages and Types of AI
- **Three stages:** Machine Learning → Machine Intelligence → Machine Consciousness
- **Three types:** Narrow AI (ANI) → General AI (AGI) → Superintelligence (ASI)
- Deep learning is the leading technique pushing toward AGI

#### 3. ANN and DNN Foundations

| Concept | Description |
|---------|-------------|
| **Perceptron** | Single-layer feedforward NN (Rosenblatt, 1958); weighted inputs → threshold output |
| **ANN** | Multi-layer, biological-neuron-inspired; learns by adjusting weights via gradient descent |
| **DNN** | Many-layer ANN; hierarchical feature learning from raw data |
| **Gradient descent** | Optimisation: minimise loss by stepping in direction of steepest descent |
| **Activation function** | Introduces non-linearity; common choices: ReLU, sigmoid, softmax |
| **Loss function** | Measures prediction error (e.g., cross-entropy for classification) |
| **Backpropagation** | Computes gradients recursively from output to input layers |

#### 4. Classical NLP vs Deep Learning NLP

| Approach | Feature engineering | Workflow |
|----------|--------------------|---------| 
| **Classical NLP** | Hand-crafted (NER, POS tags) | Preprocess → feature engineering → ML model |
| **Deep learning NLP** | Learned from data (Word2Vec, GloVe embeddings) | Preprocess → dense embeddings → DNN |

Deep learning advantage: no hand-crafted features; the network learns relevant representations automatically.

#### 5. Machine Translation — LSTM Encoder-Decoder

Architecture progression:
1. **Dictionary-based** (1954): word-for-word mapping; no syntax awareness
2. **Statistical MT (SMT)**: probabilistic alignment of bilingual corpus (IBM, Google Translate original)
3. **Neural MT (NMT)**: sequence-to-sequence LSTM

```
Source sentence → [Encoder LSTM] → hidden state S → [Decoder LSTM] → target sentence (word by word)
```

**Limitation of vanilla LSTM:** fixed-size hidden state `S` becomes lossy for long sentences.

**Attention mechanism** (solution): stores all encoder outputs; decoder queries each one for relevance using softmax scoring → extracts a **context vector** = weighted sum of encoder outputs.

```
Context vector = Σ (relevance_score_i × encoder_output_i)
```

**Bidirectional RNN:** two RNNs per layer (forward + backward) → each word has context from both directions. Google NMT: 1 bidirectional encoder layer + 7 unidirectional encoder layers + 8 unidirectional decoder layers.

#### 6. Abstractive Summarisation (NLG Application)
- Uses LSTM to read a short article and generate a **one-line summary** — not extracting sentences but generating new text
- Differs from extractive summarisation (which just selects existing sentences)
- Training is compute-intensive; practically demonstrated with recipe text dataset

#### Key Takeaways for ISY503
1. NLU/NLG distinction maps directly to Module 9's scope: BERT (R5) is primarily NLU; Smart Reply/summarisation are NLG
2. Attention mechanism is the conceptual predecessor to the Transformer architecture underlying BERT (R5)
3. Bidirectional context is why BERT outperforms unidirectional LSTMs — connects directly to next resource

---

### 5. Devlin, J. & Chang, M. W. (2018). Open Sourcing BERT

**Citation:** Devlin, J., Chang, M. W. (2018). Open Sourcing BERT: State-of-the-Art Pre-training for Natural Language Processing. Retrieved from https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html

**Purpose:** Announces Google's open-source release of BERT — a bidirectional pre-trained language model that dramatically advances NLP benchmarks by learning from context in both directions simultaneously, then fine-tuning for specific tasks with minimal data.

---

#### 1. The Training Data Problem in NLP
- Classic ML: "garbage in, garbage out" — models are only as good as their training data
- Labelled NLP datasets are expensive and scarce
- BERT's solution: **pre-train on unlabelled text** (BooksCorpus + Wikipedia) → fine-tune on small labelled task dataset

#### 2. Bidirectional vs Unidirectional Pre-training

| Model | Direction | Context captured |
|-------|-----------|-----------------|
| GPT (OpenAI) | Left-to-right only | Word meaning depends only on preceding words |
| ELMo | Shallow bidirectional (two separate LSTMs) | Partial context from both sides |
| **BERT** | **Deep bidirectional (Transformer)** | **Full left + right context simultaneously at every layer** |

Why bidirectionality matters: the word "bank" in "I went to the bank to deposit money" vs "I sat on the river bank" has different meaning — full context is needed to disambiguate.

#### 3. Pre-training Tasks
BERT is pre-trained on two tasks simultaneously:

| Task | Description | Purpose |
|------|-------------|---------|
| **Masked Language Model (MLM)** | 15% of tokens randomly masked; model predicts missing word | Forces bidirectional context learning |
| **Next Sentence Prediction (NSP)** | Given sentence A and B, predict if B follows A | Captures sentence-pair relationships (QA, inference) |

Example MLM: "I want to [MASK] that car because it is cheap" → model must predict "buy".

#### 4. Fine-tuning for Downstream Tasks
BERT's pre-trained weights are the starting point; a task-specific output layer is added and the whole model is fine-tuned:

| Task type | What changes | Training time |
|-----------|-------------|---------------|
| Classification (sentiment) | Add softmax layer | ~30 minutes on TPU |
| Question answering | Add span-prediction head | ~30 minutes on TPU |
| Named entity recognition | Add token-level classifier | ~30 minutes on TPU |

#### 5. Benchmark Results

| Benchmark | Previous best | BERT | Improvement |
|-----------|--------------|------|-------------|
| SQuAD v1.1 (QA) | ~91% F1 | **93.2% F1** | Surpasses human-level (91.2%) |
| GLUE (11 NLP tasks) | — | +7.6 points | Across all 11 tasks simultaneously |

#### 6. BERT's Name and Architecture
- **BERT** = **B**idirectional **E**ncoder **R**epresentations from **T**ransformers
- Built on the **Transformer** attention architecture (Vaswani et al., 2017)
- Two model sizes: BERT-Base (110M parameters) and BERT-Large (340M parameters)
- Open-sourced at: https://github.com/google-research/bert

#### Key Takeaways for ISY503
1. BERT solves the data scarcity problem by separating pre-training (general language understanding, unsupervised) from fine-tuning (task-specific, small labelled set)
2. MLM is BERT's core innovation — enables true bidirectional context unlike prior unidirectional LMs
3. Activity 1 (Metz 2019) critiques BERT's bias; understanding BERT's architecture explains *why* bias propagates from training data

---

### Activity 1: Metz, C. (2019). We Teach A.I. Systems Everything, Including Our Biases

**Citation:** Metz, C. (2019). We Teach A.I. Systems Everything, Including Our Biases. The New York Times. Retrieved from https://www.proquest.com/newspapers/we-teach-i-systems-everything-including-our/docview/2314131571/se-2?accountid=176901

**Purpose:** Newspaper investigation revealing how universal language models like BERT absorb and amplify historical biases from their training corpora, with concrete examples of gender and political bias discovered by researchers.

---

#### 1. How Bias Enters Language Models
- BERT and peers learn from **massive text corpora**: BooksCorpus, Wikipedia, news articles, digitised books
- These texts encode **decades of cultural, gender, and racial bias**
- The model has no mechanism to distinguish factual associations from biased ones
- Result: biases from the training data are **baked in** to the model weights

#### 2. Documented Examples of BERT Bias

| Bias type | Finding | Source |
|-----------|---------|--------|
| **Gender–occupation** | "programmer" associated more with men than women (Carnegie Mellon study) | CMU researchers |
| **Word–gender association** | 99 of 100 common words (e.g., "jewelry", "money", "horses") more associated with men | Dr. Robert Munro |
| **Missing pronouns** | Google and AWS cloud NLP services failed to recognise "hers" as a pronoun; "his" was correctly identified | Dr. Munro |
| **Political sentiment** | Primer's BERT-based system consistently rated Trump headlines as negative, regardless of actual content | John Bohannon, Primer |

#### 3. Why Universal Language Models Are Particularly Risky
- **"Universal language models"** (BERT, ELMo, ERNIE, GPT-2) are general-purpose → bias propagates to *every* downstream application
- Unlike narrow models trained on specific datasets, universal models affect search engines, chatbots, hiring tools, and ad services simultaneously
- "Even the people building these systems don't understand how they are behaving" — Emily Bender, UW computational linguistics

#### 4. Industry Response and Path Forward
- Google: "Mitigating bias from our systems is one of our A.I. principles, and is a top priority"
- Amazon: corrected "hers" pronoun issue after Munro reported it
- Sean Gourley (Primer CEO) predicts a **"billion-dollar industry"** of algorithm auditing specialists
- Proposed solution: treat AI like biology — deeply understand internal behaviour before deployment

#### Key Takeaways for ISY503
1. Assessment 3 requires implementing sentiment analysis — this article is a critical reminder that model outputs reflect training data biases, not objective truth
2. The Activity 1 task asks you to research bias in NLP models *other than BERT* — use this article as a frame but investigate ELMO, GPT-2, or commercial APIs
3. Bias is not a bug — it is an emergent property of learning from human-generated data; mitigation requires intentional debiasing techniques and diverse training corpora

---

### Activity 2: Ben Abacha, A. & Zweigenbaum, P. (2015). MEANS: A Medical Question-Answering System

**Citation:** Ben Abacha, A. & Zweigenbaum, P. (2015). MEANS: A medical question-answering system combining NLP techniques and semantic web technologies. *Information Processing and Management, 51*(5), 570–594. https://doi.org/10.1016/j.ipm.2015.04.006

**Purpose:** Presents MEANS, a hybrid medical question-answering system that combines deep NLP analysis with semantic web technologies (ontologies, SPARQL) to retrieve precise answers to clinical questions from MEDLINE articles.

---

#### 1. The Medical QA Problem
- 35% of US adults use the internet to self-diagnose (Pew Research, 2013)
- Doctors ask ~7.6 questions per two half-days of practice (Ely et al., 1999); only 30% of information needs are met
- Standard search engines return too many results to filter quickly — clinicians need **precise, contextualised answers**
- QA systems must understand *both* the question (intent, entities) *and* the answer source (documents, databases)

#### 2. Three-Step MEANS Architecture

```
Step 1: Offline Corpus Annotation (NLP)
  ↓  Named Entity Recognition (diseases, drugs, symptoms)
  ↓  Relation extraction between medical entities

Step 2: Online Question Analysis
  ↓  Question type classification (factual WH / boolean yes-no)
  ↓  Focus extraction (main medical entity: e.g., "pyogenic granuloma")
  ↓  PICO frame mapping

Step 3: Answer Retrieval
  ↓  Semantic search via SPARQL on annotated ontology
  ↓  Query relaxation if exact match fails
  → Precise answer + 5-sentence justification context
```

#### 3. PICO Framework for Medical Questions

| Letter | Component | Example |
|--------|-----------|---------|
| **P** | Population / Disease | "pyogenic granuloma" |
| **I** | Intervention / Variable of Interest | "best treatment" |
| **C** | Comparison | (optional) alternative intervention |
| **O** | Outcome | efficacy, side effects |

- Originally designed for therapy questions; less suited for diagnosis, etiology, prognosis
- MEANS uses PICO as a reference representation, supplemented by NER for richer entity relations

#### 4. Question Taxonomy (Ely et al., 2000 — Top 5 of 1,396 questions)
1. What is the drug of choice for condition X?
2. What is the cause of symptom X?
3. What test is indicated in situation X?
4. What is the dose of drug X?
5. How should I treat condition X?

These patterns inform the question classifier in MEANS Step 2.

#### 5. Query Relaxation Strategy
- When exact SPARQL query returns no results (due to NLP errors or implicit information), MEANS **relaxes** the query:
  - Removes the most restrictive constraint
  - Broadens entity scope using ontology hierarchy
- This strategy improves recall without sacrificing precision in the majority of cases
- Evaluated on **CEBM Summarisation corpus** (real MEDLINE questions/answers) — results described as "promising"

#### 6. Ethical Dimension
- A QA system that returns a **wrong medical answer** can cause patient harm
- This is the ethical tension the Activity 2 discussion asks you to explore with peers
- MEANS mitigates this via justification snippets (5-sentence context) so the clinician can verify the answer source

#### Key Takeaways for ISY503
1. MEANS is a hybrid system — it would fail without both the NLP layer (understanding the question) and the semantic web layer (structured knowledge retrieval); neither alone is sufficient
2. The PICO framework is a domain-specific structured representation — analogous to how BoW/TF-IDF is a general structured representation for arbitrary text classification
3. The ethical challenge of wrong medical answers connects directly to Activity 1's bias theme: both highlight that NLP systems deployed in high-stakes domains require rigorous validation
