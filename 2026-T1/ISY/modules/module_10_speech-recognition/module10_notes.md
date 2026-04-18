# Module 10 — Speech Recognition
## ISY503 Intelligent Systems

## TL;DR
- **ASR** converts speech to text via a pipeline: acoustic analysis → acoustic model → lexicon → language model → decoder
- Classical approach uses **MFCC features** + **HMM** per word class; modern systems replace GMMs with **DNNs** (~30% WER improvement)
- **RNNs/LSTMs + CTC** remove the need for aligned training data, enabling end-to-end models
- **Noise** and **privacy** are first-class real-world concerns; mitigated by ambient noise adjustment and careful data governance

## Glossary

| Term | Full Name | One-liner |
|------|-----------|-----------|
| **ASR** | Automatic Speech Recognition | System that translates spoken audio into text |
| **WER** | Word Error Rate | Key ASR metric: (substitutions + insertions + deletions) / total words |
| **Phoneme** | — | Smallest unit of sound that distinguishes meaning (English has ~44); e.g. "bat" = /b/ /æ/ /t/ |
| **MFCC** | Mel-Frequency Cepstral Coefficients | Compact feature vector per 25 ms speech frame, inspired by how the human ear filters frequencies |
| **Filter Bank** | — | Collection of frequency-band filters; spectral representation before MFCC compression |
| **HMM** | Hidden Markov Model | Probabilistic model of time-series sequences; models speech as hidden states with observable acoustic emissions |
| **GMM** | Gaussian Mixture Model | Probability distribution used inside HMM states to model acoustic feature vectors |
| **GMM-HMM** | — | Classical ASR acoustic model: GMMs estimate emission probabilities for each HMM state |
| **DNN** | Deep Neural Network | Multi-layer network; replaces GMMs in acoustic modelling, delivering ~30% WER improvement |
| **DNN-HMM** | — | Hybrid model: DNN estimates HMM state posteriors instead of GMMs |
| **RNN** | Recurrent Neural Network | Neural network with feedback loop over sequences; state `Sₜ = f(Sₜ₋₁, Xₜ)` carries memory |
| **LSTM** | Long Short-Term Memory | RNN variant with gating mechanism (forget / input / output gates) that prevents vanishing gradients |
| **BPTT** | Backpropagation Through Time | Training algorithm for RNNs — unfolds the network through time steps, then applies backprop |
| **CTC** | Connectionist Temporal Classification | Loss function that maximises correct labelling over all possible alignments; introduces blank symbol (Ø), removing need for pre-aligned data |
| **DBN** | Deep Belief Network | Generatively pre-trained deep network; used to initialise DNN weights in DNN-HMM hybrids |
| **LM** | Language Model | Assigns probabilities to word sequences; from n-grams to neural / LSTM-based models |
| **N-gram** | — | Sequence of n consecutive words; used to estimate `P(wᵢ | wᵢ₋ₙ₊₁…wᵢ₋₁)` |
| **Word Embedding** | — | Dense vector representation of a word in a continuous space; semantically similar words cluster together |
| **Beam Search** | — | Heuristic decoder that keeps the top-n candidate sequences at each step; practical for large-vocabulary ASR |
| **Viterbi** | — | Dynamic programming decoder that finds the most probable HMM state sequence; intractable at scale |
| **Coarticulation** | — | Phonetic phenomenon where adjacent sounds merge; makes continuous speech harder to segment than isolated words |
| **pyaudio** | — | Python library for microphone access; required for real-time speech capture |
| **SpeechRecognition** | — | Python package wrapping cloud ASR APIs (Google, etc.); `adjust_for_ambient_noise()` reduces noise impact |

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | **Watch & summarise Microsoft Research (2017) — ASR Overview** | ✅ |
| **2** | **Read & summarise Joshi (2016) — Chapter 7: Speech Recognition (Python ML Cookbook)** | ✅ |
| **3** | **Read & summarise Zocca et al. (2016) — Deep Learning in Speech Recognition** | ✅ |
| **4** | **Read & summarise Vlahos (2019) — Privacy in Speech Recognition** | ✅ |
| 5 | Activity 1: Noise Reduction (250-word outline) | 🕐 |

---

## Key Highlights

---

### 1. Microsoft Research. (2017). Automatic Speech Recognition — An Overview

**Citation:** Microsoft Research. (2017, 7 June). Automatic Speech Recognition – An Overview [Video file]. Retrieved from https://www.microsoft.com/en-us/research/video/automatic-speech-recognition-overview/

**Purpose:** A comprehensive academic lecture by IIT Bombay researcher Preethi Jyothi covering the history, architecture, and challenges of ASR systems — from early frequency detectors to modern DNN-based systems.

---
<!-- 17m34s -->

#### 1. What is ASR and Why Does It Matter?
- **Definition:** ASR accurately translates spoken utterances into text (words, syllables, sub-word units, characters)
- **Applications:** YouTube captions, voice mail transcription, dictation, Siri, Cortana, Google Voice
- **Social value:** Enables technology access for illiterate users; supports endangered language preservation
- **Key distinction:** ASR = transcription only; spoken language understanding is a separate downstream module

#### 2. Why ASR is Difficult
| Source of Variability | Impact |
|---|---|
| Style of speech | Continuous speech harder than isolated words due to coarticulation |
| Environment | Noise, reverberation, interfering speakers |
| Speaker characteristics | Accent, rate, age, emotion |
| Task constraints | Vocabulary size (command-control vs. voice search), language morphology |

- **Coarticulation:** preceding words physically affect the production of following words, creating continuous merging

#### 3. History of ASR
| Era | System | Capability |
|---|---|---|
| 1920s | Radio Rex | Frequency detector for single vowel (500 Hz) — not real recognition |
| 1962 | IBM SHOEBOX | 16 words (digits + operations), isolated word recognition |
| 1975 | HARPY (CMU) | 1,000-word vocabulary, connected speech — ARPA-funded |
| 1980s | Statistical models (HMMs) | Large vocabulary, formulated as noisy channel problem |
| 2006+ | Deep Neural Networks | State-of-the-art; ~30% improvement in recognition rate |

#### 4. ASR System Pipeline

```mermaid
flowchart LR
  A[Audio Signal] --> B[Acoustic Analysis\nMFCC / Filter Banks]
  B --> C[Acoustic Model\nHMM or DNN]
  C --> D[Pronunciation Dictionary\ne.g. CMUdict]
  D --> E[Language Model\nn-gram or neural]
  E --> F[Decoder\nViterbi / Beam Search]
  F --> G[Transcript]
```

- **Acoustic Analysis:** Raw speech → discrete frames (10–25 ms) → MFCC feature vectors
- **Acoustic Model:** Maps feature vectors → phoneme sequence (HMMs or DNNs)
- **Pronunciation Dictionary:** Maps phonemes → words (~150,000 entries in CMUdict)
- **Language Model:** Probability distribution over word sequences (n-grams or neural LM)
- **Decoder:** Combines all components to find the most likely word sequence

#### 5. Phonemes
- **Phoneme:** Basic unit of speech sound (e.g., "bat" = /b/ /ae/ /t/); ~44 phonemes in English
- Phonemes enable **generalisation**: a model trained on some words can recognise unseen words by composing known phonemes
- Pronunciation dictionaries (expert-created) map words → phoneme sequences

#### 6. From HMMs to DNNs
- **HMM acoustic model:** Each HMM state has emission probabilities (Gaussian Mixture Models); transition probabilities govern frame–phoneme alignment
- **DNN acoustic model:** Replaces GMMs; takes fixed window of speech frames, outputs posterior probability over phones
- DNNs led to ~30% word error rate reduction when Microsoft shifted in 2012
- **Word Error Rate (WER):** Key evaluation metric = substitutions + insertions + deletions / total words

#### 7. Open Problems
- Accent adaptation remains a major challenge (e.g., 10% WER for standard Indian English vs. 39% WER for heavily accented speech)
- Room acoustics (reverberation, interfering speakers) and out-of-vocabulary words still degrade performance

#### Key Takeaways for ISY503
1. Provides the foundational architecture that all other module resources build upon
2. MFCC features (introduced here) are the input to the HMM system in R2 and are preprocessed away in R3's deep learning pipeline
3. The noisy channel formulation directly motivates Activity 1's noise reduction problem

---

### 2. Joshi, P. (2016). Python Machine Learning Cookbook — Chapter 7: Speech Recognition

**Citation:** Joshi, P. (2016). Python Machine Learning Cookbook. Birmingham, England: Packt. Retrieved from https://search.ebscohost.com/login.aspx?direct=true&AuthType=shib&db=nlebk&AN=1285067&site=ehost-live&custid=ns251549&ebv=EB&ppid=pp_155

**Purpose:** A hands-on practical chapter covering audio signal processing, feature extraction, Hidden Markov Models, and building a complete word-level speech recogniser in Python — bridges theory from R1 with concrete implementation.

---

#### 1. Audio Signal Fundamentals
- **Digital audio:** Continuous waveforms sampled at discrete rates; speech commonly at **44,100 Hz** (44.1 kHz)
- **Normalisation:** Raw 16-bit integer data must be normalised to floats before processing
- **Time domain → Frequency domain:** Fourier transform decomposes audio into component frequencies

| Representation | Tool | Purpose |
|---|---|---|
| Time domain waveform | `scipy.io.wavfile` | Read/visualise raw audio |
| Frequency domain | `np.fft.fft` | Reveal spectral content |
| Power spectrum | 10 * log10(FFT²) | Perceptually weighted frequency analysis |

#### 2. Feature Extraction — MFCC and Filter Banks
- **MFCC (Mel-Frequency Cepstral Coefficients):** Compact feature vectors derived from filter banks; biologically motivated (mimics cochlear filtering)
- Extracted using `python_speech_features` library: `mfcc()` and `logfbank()`
- Each window produces a feature vector; stacked vectors form the input matrix for classifiers

```python
from features import mfcc, logfbank
mfcc_features = mfcc(audio, sampling_freq)    # shape: (windows, 13)
filterbank_features = logfbank(audio, sampling_freq)  # shape: (windows, 26)
```

#### 3. Generating and Synthesising Audio
- Audio signals are superpositions of sinusoids: `audio = np.sin(2π * freq * t)`
- Noise can be added: `audio += 0.4 * np.random.rand(n)`
- Musical notes have specific frequencies (e.g., A4 = 440 Hz); overlapping sinusoids synthesise chords

#### 4. Hidden Markov Models (HMMs) for Speech Recognition
- **HMM definition:** Probabilistic model representing sequences of hidden states; each state emits observable outputs (acoustic feature vectors)
- HMMs are ideal for speech because **speech is inherently a time-series** signal with variable duration
- Parameters: `n_components` (hidden states), `cov_type='diag'` (diagonal covariance), `n_iter=1000`

```python
from hmmlearn import hmm
model = hmm.GaussianHMM(n_components=4, covariance_type='diag', n_iter=1000)
model.fit(mfcc_features)
score = model.score(test_features)  # log-likelihood
```

#### 5. Building a Word-Level Speech Recogniser
- **Architecture:** One HMM per word class; recognition = highest log-likelihood score
- **Dataset:** 7 words × 15 audio files each (fruit words: apple, orange, kiwi, pineapple, etc.)
- **Pipeline:**
  1. Load `.wav` files per class
  2. Extract MFCC features
  3. Train one HMM per class
  4. For test file: score against all HMMs → argmax = predicted word

| Component | Role |
|---|---|
| MFCC extraction | Convert raw audio to feature matrix |
| `HMMTrainer.train(X)` | Fit Gaussian HMM to class features |
| `HMMTrainer.get_score(x)` | Return log-likelihood for test input |
| Argmax over scores | Classify word |

#### Key Takeaways for ISY503
1. This chapter provides the practical implementation of concepts from R1 (MFCC → HMM pipeline)
2. The HMM-per-class pattern is the classical ASR acoustic model before DNNs — understanding it makes DNN replacements in R3 more meaningful
3. The `show_all=True` argument in the Activity 1 video (getting multiple transcription candidates) mirrors the same uncertainty-handling philosophy as HMM scoring

---

### 3. Zocca, V., Spacagna, G., Slater, D., Roelants, P. (2016). Python Deep Learning — Chapter 6: RNNs and Speech Recognition

**Citation:** Zocca, V., Spacagna, G., Slater, D., Roelants, P. (2016). Python Deep Learning. Retrieved from https://search.ebscohost.com/login.aspx?direct=true&AuthType=shib&db=nlebk&AN=1513367&site=ehost-live&custid=ns251549&ebv=EB&ppid=pp_193

**Purpose:** Explains how Recurrent Neural Networks (RNNs) and LSTMs are applied to language modelling and speech recognition — showing how deep learning replaces or simplifies classical HMM-based pipelines.

---

#### 1. Recurrent Neural Networks (RNNs)
- **Core idea:** RNNs apply the same function recurrently over sequences: `Sₜ = f(Sₜ₋₁, Xₜ)`
- Unlike feedforward networks, RNNs have **memory**: hidden state `Sₜ` carries information from all previous steps
- Parameters `U` (input→state), `W` (state→state), `V` (state→output) are **shared across all time steps**

| RNN Input/Output Pattern | Example Application |
|---|---|
| One-to-one | Image classification |
| One-to-many | Image captioning |
| Many-to-one | Sentiment classification |
| Many-to-many (indirect) | Machine translation |
| Many-to-many (direct) | Frame-level phoneme labelling in ASR |

- **Training:** Backpropagation Through Time (BPTT) — unfold RNN through time, then apply standard backprop

#### 2. Vanishing and Exploding Gradients
- **Vanishing gradients:** Gradients shrink to near-zero as they propagate backwards through many time steps → network loses ability to learn long-term dependencies
- **Exploding gradients:** Gradients grow exponentially → unstable training; mitigated by **gradient clipping**
- **LSTM (Long Short-Term Memory):** Designed to solve vanishing gradients via gating mechanisms (forget, input, output gates) maintaining a separate cell state `cₜ`

#### 3. Language Modelling with RNNs
- **N-gram models:** Approximate word probability using n-word windows; suffer from **curse of dimensionality** (exponential combinations)
- **Neural language models:** Learn word **embeddings** (distributed representations) — semantically similar words cluster together in embedding space
- **Word2Vec insight:** `embed(woman) - embed(man) ≈ embed(queen) - embed(king)` — embeddings capture analogies
- **Character-level models:** Model distribution over characters instead of words; smaller vocabulary, but requires longer sequences

#### 4. Deep Learning Speech Recognition Pipeline

```mermaid
flowchart LR
  A[Audio Signal] --> B[Preprocessing\nMFCC / Filter Banks]
  B --> C[Acoustic Model\nDNN-HMM or LSTM-CTC]
  C --> D[Pronunciation Dictionary]
  D --> E[Language Model\nRNN / LSTM]
  E --> F[Decoder\nBeam Search]
  F --> G[Transcript]
```

| Component | Classical | Deep Learning |
|---|---|---|
| Acoustic features | MFCC (hand-crafted) | CNNs can learn preprocessing |
| Acoustic model | GMM-HMM | DNN-HMM hybrid, then LSTM-CTC |
| Language model | N-gram | RNN/LSTM language model |
| Alignment | Required (pre-labelled) | CTC removes need for alignment |

#### 5. Key DL Contributions to ASR
- **DNN-HMM hybrid:** Replace Gaussian Mixture Models with Deep Belief Networks (DBNs) for emission probabilities → better phone recognition
- **CTC (Connectionist Temporal Classification):** Global objective function that maximises probability of correct labelling over all possible alignments; introduces blank symbol (Ø) to handle unaligned output (e.g., "ØaaØabØØ" → "aab")
- **Attention-based models:** Encoder-decoder architecture with dynamic attention window — learns where to focus in input sequence
- **End-to-end models:** CTC and attention models learn acoustic + language model jointly, outputting words directly without phoneme modelling

#### 6. Decoding
- **Viterbi algorithm:** Guaranteed optimal but intractable for large vocabularies
- **Beam search:** Heuristic; keeps top-n candidate sequences during search — practical for large vocabulary ASR

#### Key Takeaways for ISY503
1. This chapter explains why DL replaced HMMs: CTC removes the alignment requirement that makes HMM-based ASR fragile
2. The speech recognition pipeline here directly connects to both R1 (overview) and R2 (HMM implementation)
3. Understanding LSTMs and CTC is foundational for any serious work in speech-to-text or audio ML

---

### 4. Vlahos, J. (2019). Smart talking: Are our devices threatening our privacy?

**Citation:** Vlahos, J. (2019, 26 March). Smart talking: Are our devices threatening our privacy? The Guardian. Retrieved from https://www.theguardian.com/technology/2019/mar/26/smart-talking-are-our-devices-threatening-our-privacy

**Purpose:** Investigative journalism exposing how always-on voice devices (Amazon Echo, Google Home, Apple HomePod, children's toys) create layered privacy risks — from intentional data retention to accidental recording and hacker exploitation.

---

#### 1. The Core Privacy Problem
- Voice assistants listen **continuously** for wake words; only transmit after trigger — but this does not eliminate risk
- **By-catch:** Devices often record bystanders (spouse, children, guests) without their knowledge
- Companies retain recordings to improve AI — this data lives in the cloud, often indefinitely unless user manually deletes

| Company | Retention Model |
|---|---|
| Apple | Tagged with random ID (not name); identifier stripped after 6 months |
| Google | Linked to user account; user can listen back to past queries |
| Amazon | Linked to user account; retained until user deletes |

#### 2. High-Profile Privacy Incidents
- **Amazon Echo in murder case (Bentonville, 2015):** Police sought Echo recordings as murder evidence; Amazon resisted citing First Amendment; user ultimately consented; case dismissed
- **Google Home Mini (2017):** Hardware flaw caused "phantom touch events" → device recorded thousands of short clips 24/7 without user knowledge; fixed via software update
- **CloudPets stuffed animals:** 800,000+ customer credentials and 2M recordings exposed in unsecured database; hackers demanded ransom; Bluetooth pairing had no encryption

#### 3. Legal Framework
- **Local recordings:** Law enforcement needs a **search warrant**
- **Cloud recordings:** "Reasonable expectation of privacy is eviscerated" (Reidenberg, Fordham Law) — you've shared data with a third party, waiving 4th Amendment protection
- US government requested data on 170,000+ Google accounts in 2017 alone

#### 4. Security Vulnerabilities
- **DolphinAttack (Zhejiang University, 2017):** Ultrasonic commands (>20 kHz, inaudible to humans) successfully hijacked voice interfaces of Amazon, Apple, Google, Microsoft, Samsung — triggered malicious websites, fake messages, even car navigation hijacks
- **CloudPets hack:** Unencrypted Bluetooth pairing turned plush toys into remote surveillance devices

#### 5. Ethical Dilemmas
- Hello Barbie (Mattel): Children's conversations reviewed for product improvement — raises questions when a child discloses abuse
- Siri suicide prevention: When told "I want to kill myself," Siri responds with crisis resources — illustrates blurry line between helpful listening and liability
- Alexa and emergency situations: No clear standard for when a device should autonomously call for help

#### 6. Recommendations
- Review privacy policies before adopting any voice device
- Check and delete stored voice recordings periodically (Google/Amazon dashboards)
- Prefer local processing (Apple's model) over constant cloud streaming
- Be especially cautious with children's smart toys

#### Key Takeaways for ISY503
1. Every ASR system from R1/R2/R3 that improves accuracy also increases the volume of data collected — accuracy and privacy exist in tension
2. The always-on architecture required for wake-word detection is the root cause of most privacy incidents — a technical design choice with social consequences
3. Relevant to assessments involving AI ethics, system design trade-offs, or any discussion of responsible AI deployment

---

## Activity Notes

### Activity 1: Noise Reduction
- **Source:** The AI University. (2019, 30 October). Automatic Speech Recognition – Noise Reduction [Video file]. Retrieved from https://www.youtube.com/watch?v=tuqkqrgbWiE
- **Task:** Watch from minute 1:20; write ~250 words in bullet form outlining the problem noise creates for ASR and solutions to reduce it
- **Status:** 🕐 Not started

**Key concepts from transcript (for reference when completing the activity):**
- Problem: Noise causes wrong transcriptions (e.g., "he is going to bed" → "he is going to tip")
- Solution 1: `recognizer.adjust_for_ambient_noise()` — calibrates noise threshold before listening
- Solution 2: `SciPy` filters for audio pre-processing; professional audio editing software
- Solution 3: `show_all=True` in `recognize_google()` — returns multiple candidate transcriptions with confidence scores, letting user pick the best match
- Real-time microphone input: `Microphone` class + `recognizer.listen(mc)` method; requires `pyaudio` (Python ≤ 3.6)
