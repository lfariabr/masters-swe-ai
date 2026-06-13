# Module 3 - Deep Learning Applications: NLP, Speech Recognition and Computer Vision

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow, Bengio & Courville (2016) - Applications Ch.12 | ✅ |
| **2** | Read & summarise Zhao, Gui & Zhang (2018) - Deep CNN for Twitter sentiment analysis | ✅ |
| **3** | Read & summarise Noda et al. (2015) - Audio-visual speech recognition using deep learning | ✅ |
| 4 | Activity 1: Interactive Knowledge Sharing - NLP (flowchart) | 🕐 |
| 5 | Activity 2: Interactive Knowledge Sharing - Speech Recognition (flowchart) | 🕐 |
| 6 | Activity 3: Interactive Knowledge Sharing - Computer Vision (flowchart) | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning - Chapter 12: Applications.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

**Purpose:** Chapter 12 surveys how deep learning is put to work in the three flagship application areas of the module - computer vision, speech recognition, and NLP - plus the large-scale infrastructure that makes them possible. It is the conceptual map for all three Module 3 activities.

---

#### 1. Large-Scale Deep Learning (Section 12.1)

- **Connectionism:** A single neuron is not intelligent, but a large population acting together is. Network size is the key driver of capability gains since the 1980s.
- **Why GPUs:** Neural nets need high memory bandwidth and massive parallelism with little branching - exactly what graphics hardware (and later GP-GPU / CUDA) provides.
- **Distributed training:** scale beyond one machine via the patterns below.

| Strategy | What it does |
|---|---|
| **Data parallelism** | different examples on different machines (easy for inference) |
| **Model parallelism** | one example split across machines, each runs part of the model |
| **Async SGD** | cores update shared parameters lock-free via a parameter server |
| **Model compression** | train a big model, then fit a small model to mimic it for cheap inference |
| **Dynamic structure** | cascades / mixture-of-experts compute only the parts needed per input |

#### 2. Computer Vision (Section 12.2)

- **Core tasks:** object recognition, detection (bounding boxes), transcription (e.g. street numbers), per-pixel labelling, plus image synthesis / restoration.
- **Minimal preprocessing:** vision needs little - mainly standardising pixels to a common range (e.g. [0,1]); with big data + big models, let the model learn invariances.
- **Contrast normalisation:** **GCN** (global) maps each image onto a sphere by subtracting the mean and rescaling std; **LCN** (local) normalises within small windows to make edges stand out.
- **Dataset augmentation:** translations, rotations, flips, colour perturbation - cheap way to cut generalisation error because object class is invariant to these.

#### 3. Speech Recognition (Section 12.3)

- **The task (ASR):** map an acoustic signal `X` (20 ms frames) to the most probable word sequence `y` = argmax P(y|X).
- **The shift:** GMM-HMM dominated from the 1980s to ~2009; deep nets replaced the GMM (acoustic-feature → phoneme mapping), cutting TIMIT phoneme error from ~26% to ~20.7%, then unsupervised pretraining became unnecessary.

| Era | Approach |
|---|---|
| 1980s-2009 | **GMM-HMM** (GMM maps acoustics→phonemes, HMM models sequence) |
| ~2009-2012 | **RBM-pretrained deep nets** replace GMM (big WER drop ~30%) |
| 2013+ | **ReLU + dropout**, 2-D conv over spectrograms, **end-to-end LSTM RNN + CTC** (TIMIT 17.7%) |

#### 4. Natural Language Processing (Section 12.4) - most relevant to your A1/A2

- **n-grams:** the classical baseline - MLE by counting, crippled by the **curse of dimensionality** (`|V|^n` possible grams, most unseen → zero probability), patched with **smoothing** and **back-off**. This is exactly the A1 model.
- **Neural language models (NLMs):** beat n-grams by using **word embeddings** (distributed representations) so semantically similar words (`dog`/`cat`) share statistical strength - the leap from one-hot to learned meaning.
- **High-dimensional output tricks:** large vocab softmax is expensive; mitigations include **short lists**, **hierarchical softmax** (O(log|V|)), **importance sampling**, and **noise-contrastive estimation**.
- **Neural machine translation:** **encoder-decoder** maps a sentence to a semantic vector then out to another language; the fixed-size bottleneck is relieved by the **attention mechanism** (Bahdanau et al., 2015) - a softmax-weighted average over input positions, differentiable so it trains by gradient descent.

#### Key Takeaways for DLE602

1. **This chapter is the spine of all three activities:** Section 12.2 → CV flowchart, 12.3 → speech flowchart, 12.4 → NLP flowchart. Each activity wants input, output, decision points and error sources - Ch.12 gives you the canonical pipeline for each.
2. **Direct A1 link:** the n-grams subsection (12.4.1) and its curse-of-dimensionality / smoothing discussion is the theory behind your Assessment 1 N-gram classifier, and frames *why* a neural approach (embeddings) generalises better.
3. **Direct A2/A3 link:** the **attention mechanism** (12.4.5.1) and encoder-decoder are the foundation for the ABSA "Review Pulse v2" proposal - the same softmax-weighted-average idea that makes aspect-aware attention work. Pairs with [Zhao et al. (2018)](#2-zhao-j-gui-x--zhang-x-2018-deep-convolution-neural-networks-for-twitter-sentiment-analysis) below.

---

### 2. Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis.

**Citation:** Zhao, J., Gui, X. & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. IEEE Access, 6, 23253-23260. Retrieved from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8244338

**Purpose:** The assessment-critical paper. It builds **GloVe-DCNN**, a deep CNN that fuses pre-trained word embeddings with classical features to classify tweet sentiment, and benchmarks it against n-gram baselines on five Twitter datasets - including STS-Test and STS-Gold, the same datasets used in your Assessment 1.

---

#### 1. The Feature Set (four streams concatenated)

The model's novelty is combining learned semantics with hand-built signals into one vector `v`:

| Feature stream | What it captures |
|---|---|
| **GloVe word embeddings** | 200-dim vectors trained unsupervised on a 20-billion-token Twitter corpus; capture latent semantic / co-occurrence relationships |
| **Word N-grams (BoW)** | unigram + bigram presence - the classical baseline feature |
| **Word sentiment polarity score** | lexicon-based (AFINN + SentiWordNet), via PMI: `SenScore(w) = PMI(w,pos) - PMI(w,neg)` |
| **Twitter-specific features** | hashtags, emoticons, negation, POS tags, capitalised words |

- **GloVe intuition:** learns word vectors from *ratios* of co-occurrence probabilities (the classic ice/steam vs solid/gas example), so synonyms land close together.

#### 2. The DCNN Architecture

- **Pipeline:** tokens → embedding lookup → concatenate the four feature streams → **convolution** (multiple filter windows, window size 7 worked best) → **k-max pooling** → repeat (3 conv + 3 k-max pooling layers) → **fully-connected softmax** → P(positive)/P(negative).
- **k-max pooling:** keeps the top-k most discriminative fragments and **retains word order** - the key advantage over BoW, which cannot express how negation flips sentiment.
- **Regularisation:** dropout (0.5) on fully-connected layers to fight over-fitting; batch size 128, learning rate 0.001.

#### 3. Heavy Preprocessing (the unglamorous but essential step)

- Remove non-ASCII/non-English, URLs, numbers, stopwords; expand negations (`won't` → `will not`), acronyms/slang; replace emoticons/emoji with text; tokenise with Tweet-NLP.

#### 4. Results vs Baselines

| Model | Role | Note |
|---|---|---|
| **BoW-SVM / BoW-LR** | baseline | uni+bigram features, classical ML |
| **GloVe-SVM / GloVe-LR** | stronger baseline | full feature set, classical classifier |
| **GloVe-DCNN** | proposed | best on all 5 datasets |

- **Headline numbers:** highest accuracy **87.62%** (STS-Test); improvement over baseline ranged **+3.68% to +19.14%**; evaluated with 10-fold CV averaged over 100 replications, reporting accuracy + precision/recall/F1.
- **Five datasets:** STS-Test (359 tweets), SemEval-2014 Task 9 (~5,892), **STS-Gold (2,034)**, SED (2,648), SSTd (3,326).

#### Key Takeaways for DLE602

1. **This is your Assessment 1 reference paper** (the brief says you "must refer to" it). It defines the deep-learning-vs-baseline comparison you replicate: BoW n-grams as the baseline, a deep model as the improvement.
2. **Dataset overlap is real:** STS-Test and STS-Gold appear here *and* in your A1 plan - so this paper is both the method blueprint and the benchmark precedent for your own numbers.
3. **A2/A3 bridge:** GloVe-DCNN proves the move from sparse n-grams to dense embeddings + a deep net; Review Pulse v2 (ABSA) is the natural next step, swapping sentence-level CNN for aspect-aware attention from [Goodfellow Ch.12.4.5](#4-natural-language-processing-section-124---most-relevant-to-your-a1a2).

---

### 3. Noda, K., Yamaguchi, Y., Nakadai, K., Okuno, H. G., & Ogata, T. (2015). Audio-visual speech recognition using deep learning.

**Citation:** Noda, K., Yamaguchi, Y., Nakadai, K., Okuno, H. G. & Ogata, T. (2015). Audio-visual speech recognition using deep learning. Applied Intelligence, 42(4), 722-737. Retrieved from https://search-proquest-com.torrens.idm.oclc.org/docview/1674443602

**Purpose:** A worked research example of the speech-recognition branch, and a clean case study in **multimodal deep learning**. It tackles the noise problem by fusing a deep-learning audio pathway with a CNN lip-reading pathway, which is the central idea for the Module 3 speech activity.

---

#### 1. The Noise Problem and the Multimodal Idea

- **Core insight:** when audio is corrupted by noise, a speaker's **lip motion** (visual channel) complements the degraded audio - so combine both modalities.
- **Three building blocks**, each a different deep architecture serving a clear role:

| Component | Architecture | Job |
|---|---|---|
| **Audio pathway** | **Deep denoising autoencoder** | reconstruct clean MFCC features from noise-corrupted ones |
| **Visual pathway** | **CNN** | predict phoneme labels straight from raw mouth-area images (no lip-shape model needed) |
| **Fusion** | **Multi-stream HMM (MSHMM)** | integrate audio + visual HMMs, weighting each stream by its reliability |

#### 2. Why Each Architecture Fits

- **Denoising autoencoder:** trained on pairs of (deteriorated, clean) audio so it learns to output noise-robust features - a simple, effective mechanism.
- **CNN for lip-reading:** local receptive fields + shared weights + spatial subsampling give **shift/rotation invariance** - beats older image-based methods (PCA, DCT) that break under lighting/translation changes, and needs no hand-labelled lip shapes.
- **MSHMM decision fusion:** explicitly turns *down* the audio stream weight when audio reliability drops, which is why the visual channel helps most exactly when noise is worst.

#### 3. Results

- **Audio gain:** ~**65% word-recognition-rate gain** using denoised MFCCs vs raw MFCCs at 10 dB SNR.
- **Multimodal gain:** adding the visual stream gives a *further* gain specifically below 10 dB SNR - confirming the complement-the-noisy-audio hypothesis.
- **Dataset:** Japanese audiovisual corpus, 6 speakers, 400 words, 24,000 recordings; 39-dim MFCCs; 64x64 down to 16x16 mouth crops. Optimised with Hessian-free (second-order) training.

#### Key Takeaways for DLE602

1. **Template for the speech-recognition activity:** it gives you a complete input → process → output → error-source pipeline (noisy audio + video in, word out, with SNR-driven decision points) - exactly the flowchart Activity 2 asks for.
2. **Reinforces the module's thesis:** the right *architecture* is chosen per *sub-task* (autoencoder denoises, CNN sees, HMM sequences) - echoing Goodfellow Ch.12's point that some specialisation is still needed.
3. **CNN cross-link:** the same CNN strengths (local receptive fields, shared weights, invariance) used here for lip images are the ones used in [Zhao et al.](#2-zhao-j-gui-x--zhang-x-2018-deep-convolution-neural-networks-for-twitter-sentiment-analysis) for text - useful to note that one architecture serves vision *and* language.
