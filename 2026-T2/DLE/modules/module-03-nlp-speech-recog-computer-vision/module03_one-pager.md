# DLE602 · Module 3 - One-Pager

> **Deep Learning Applications: NLP, Speech Recognition & Computer Vision - one architecture family, many jobs**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape, 4 zones).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Deep learning solves real tasks by matching the right architecture to the sub-task: CNN for vision, embeddings + attention for language, autoencoder for denoising. Generic nets work, but some specialisation is still needed.**
> (Goodfellow Ch.12. The payoff of M1+M2: now the nets *do* something.)

## 🖤 Zone 1 - The Enabler: Large-Scale DL (§12.1)
- 🔵 **Connectionism:** one neuron is dumb; a *huge population* together is intelligent. **Scale drives capability** (biggest gain since the 1980s).
- 🔵 **Why GPUs:** nets need massive parallelism + high memory bandwidth, little branching - exactly graphics hardware (CUDA / GP-GPU).

| Scale trick | What it buys |
|---|---|
| **Data parallelism** | different examples on different machines |
| **Model parallelism** | one example split across machines |
| **Async SGD** | lock-free shared-parameter updates |
| **Model compression** | train big → fit a small model to mimic it for cheap inference |

## 🖤 Zone 2 - Computer Vision (§12.2)
- 🖤 **Core tasks:** object recognition / detection (bounding boxes) / per-pixel labelling / transcription.
- 🔵 **Minimal preprocessing:** just standardise pixels to `[0,1]`; with big data, let the model learn invariances.
- 🔵 **GCN** (global) maps an image onto a sphere; **LCN** (local) normalises small windows → makes **edges pop**.
- 🔵 **Augmentation** (flips, rotations, colour jitter) = cheap generalisation, because class is invariant to them.
- 🔴 CNN wins via **local receptive fields + shared weights + subsampling** → shift/rotation invariance (same trick lip-reads in Zone 3).

## 🖤 Zone 3 - Speech Recognition (§12.3 + Noda 2015)
- 🖤 **ASR task:** acoustic signal `X` (20 ms frames) → `y = argmax P(y|X)` (most probable word sequence).

| Era | Approach |
|---|---|
| 1980s-2009 | **GMM-HMM** (GMM: acoustics→phonemes, HMM: sequence) |
| ~2009 | deep nets **replace GMM** → TIMIT 26% → **20.7%** error |
| 2013+ | ReLU+dropout, conv over spectrograms, **end-to-end LSTM + CTC** (17.7%) |

- 🔵 **Noda multimodal AVSR:** denoising **autoencoder** (clean audio) + **CNN** (lip-reading) + **multi-stream HMM** (fuses, weights each stream by reliability).
- 🔴 Result: ~**65% recognition gain** at 10 dB noise; the **video channel helps most exactly when audio is worst.**

## 🖤 Zone 4 - NLP ⭐ THE ASSESSMENT SPINE (§12.4 + Zhao 2018)
- 🖤 **n-grams** = chain rule + Markov assumption + count (MLE). 🔴 Dies to the **curse of dimensionality** (`|V|^n` grams → unseen = 0), patched by **smoothing / back-off**. *(This is your A1.)*
- 🔵 **Word embeddings** = the leap: `dog` and `cat` get *nearby vectors* → share statistical strength (one-hot can't).
- 🔵 **Big-vocab softmax tricks:** short-list · hierarchical softmax `O(log|V|)` · importance sampling.
- 🔵 **Attention (Bahdanau):** a **softmax-weighted average** over input positions; differentiable → trains by gradient descent. Powers encoder-decoder translation.
- 🔴 **Zhao GloVe-DCNN** (your A1 paper): GloVe embeddings + n-grams + lexicon polarity + Twitter features → **3 conv + 3 k-max pooling** → softmax. **k-max pooling keeps word order** (BoW can't).

## 🔴 Activity Prep - 3 flowcharts (input → process → output → errors)
- **Activity 1 NLP** · **Activity 2 Speech** · **Activity 3 Vision** - each: pick an app, name the DL algo/dataset/model, draw the flow with decision points + failure modes.
- 🔵 Steal the templates: Zhao's tweet→preprocess→GloVe-DCNN→pos/neg pipeline (NLP), Noda's noisy-audio+video→MSHMM→word (Speech).

## 🔴 Assessment Hook (bottom red strip)
> **Module 3 contains your Assessment 1 reference paper.** Zhao et al. (2018) GloVe-DCNN is the model you must cite, and it benchmarks on **STS-Test + STS-Gold - the exact datasets in your A1** (due **28/06/2026**, 30%). Precedent to beat: **87.62%** acc, **+3.68% to +19.14%** over the n-gram baseline. Attention (§12.4.5) → the **A2/A3 ABSA "Review Pulse v2"** foundation.

## 🔴 If you only memorise 5 things
1. **Match architecture to sub-task** - CNN sees, autoencoder denoises, embeddings+attention read.
2. **Scale is the enabler** - connectionism + GPUs made depth practical.
3. **Speech:** GMM-HMM → deep nets → end-to-end LSTM+CTC; multimodal beats noise.
4. **NLP arc:** n-grams (curse of dim.) → embeddings (similarity) → attention (focus).
5. **Zhao 2018 = your A1 paper**, on your A1 datasets (STS-Test/Gold). Know it cold.

---

### Margin prompts (answer in blue while you write)
1. Why does one-hot `dog`/`cat` doom n-grams, and which Zone 4 idea repairs it?
2. In Noda's AVSR, *why* does the visual stream matter more as SNR drops? (reliability weighting)

### This-week to-dos (still 🕐 in your notes)
- [ ] Activity 1 - **NLP** flowchart (forum)
- [ ] Activity 2 - **Speech Recognition** flowchart (forum)
- [ ] Activity 3 - **Computer Vision** flowchart (forum)
- [ ] Re-read Zhao (2018) with your A1 hat on - map its pipeline onto your own code
