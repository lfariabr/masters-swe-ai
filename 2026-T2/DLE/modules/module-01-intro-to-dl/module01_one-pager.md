# DLE602 · Module 1 — One-Pager

> **Introduction to Deep Learning & Neural Networks — the nesting, the depth, the N-gram**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape, 4 zones).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Deep learning = a machine that learns its own layered features from raw data, instead of you hand-coding them.**
> (Goodfellow Ch.1's whole argument, and the spine of the subject.)

## 🖤 Zone 1 — The Nesting ⭐ (draw as 4 nested boxes)
```
AI ⊃ Machine Learning ⊃ Representation Learning ⊃ Deep Learning
```
| Layer | Core idea | Example |
|---|---|---|
| **AI** | systems doing tasks that need intelligence | rule bases, chess |
| **ML** | improve *from data*, not hand-coded rules | logistic regression, naive Bayes |
| **Representation learning** | model learns the *features* itself | autoencoders |
| **Deep learning** | learns **many composed levels** of representation | MLP, CNN feature hierarchy |

- 🔴 **Old ML is only as good as the features you feed it** — bad representation sinks a sound model.
- 🔵 DL's move: learn the intermediate features from raw data → less manual feature engineering.

## 🖤 Zone 2 — Depth = Composition (not "more neurons")
- A deep model **stacks simple functions**; each layer → a more useful representation.
- 🔵 **Image example:** edges → corners/contours → object parts → final label.
- 🔵 **MLP** = a math function mapping input → output by composing layers.
- 🔴 Strength is the **staged build-up of abstractions**, not raw neuron count.

## 🖤 Zone 3 — Why now? + History (draw as a timeline arrow)
- 🔴 **Rule-based AI fails** on tasks easy for humans, hard to formalise: speech, faces, vision.
- 🔵 **Why it works now:** more **DATA** + more **COMPUTE** + **bigger models** + better training.
```
Cybernetics → Connectionism (1980s) → modern Deep Learning
```
- 🔵 **Connectionism:** many simple units networked → intelligent behaviour.
- 🔵 **Brain-inspired, NOT brain-simulation.**
- 🔴 **Backpropagation** = the engine that trains internal representations (← Module 2!).

## 🖤 Zone 4 — N-GRAMS ⭐ THE ASSESSMENT 1 CORE (Jurafsky & Martin)
- **Language model** = assigns probability to a word sequence / predicts the next word.
- Full word history is impractical → 🔴 **Markov assumption**: condition on only the last **N-1** words.

| Model | Uses | Trade-off |
|---|---|---|
| **Unigram** `P(w)` | nothing before it | ignores order/context |
| **Bigram** `P(w \| prev)` | 1 word back | local context, pragmatic first pick |
| **Trigram** `P(w \| prev2)` | 2 words back | richer, but **sparse + data-hungry** |

- 🔵 **MLE (bigram):** `P(wn|wn-1) = C(wn-1, wn) / C(wn-1)` — counts ÷ context count.
- 🔵 Use **log probabilities** → avoid underflow from multiplying tiny numbers.
- 🔴 **Sparsity / "zero problem":** an unseen N-gram gets probability 0. Fixes:
  - **Smoothing** (add-one: simple but blunt) · **Backoff** (drop to lower order) · **Interpolation** (mix orders — usually strongest).

## 🔴 Assessment Hook (bottom red strip)
> **A1 = Programming Problems** · source code + **500-word** report · **30%** · due **28/06/2026** · SLOs **a) b)**.
> Build an **N-gram sentiment classifier** on **2 Twitter datasets**. 🔴 A1 uses **classical N-grams, not a deep net** — this reading frames *why* N-grams are the simpler baseline. Familiarise with the brief **this week.**

## 🔴 If you only memorise 5 things
1. **AI ⊃ ML ⊃ Rep. learning ⊃ DL** — DL = learned hierarchical features.
2. Old ML needs **hand-made features**; DL **learns them** from raw data.
3. **Depth = composition** (edges → parts → object), not just more neurons.
4. **Why now** = data + compute + bigger models + **backprop**.
5. **A1 = N-grams** + Markov assumption + **smoothing/backoff/interpolation** for unseen text.

---

### Margin prompts (answer in blue while you write)
1. For your A1 classifier — **bigram or trigram** on tweets? Justify (context vs sparsity on short, noisy text).
2. Name a task **trivial for you** but near-impossible to write as explicit rules — that's the gap DL fills.

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] Activity 1 — **Introduce Yourself** forum
- [ ] Activity 2 — **Assessment 2 & 3 Preparation** discussion
- [ ] Finish 🔥 Kelleher Ch.1 + Jedamski video (both WIP)
