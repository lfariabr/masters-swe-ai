# DLE602 · Module 8 - One-Pager

> **Recurrent Neural Networks · Long Short-Term Memory · sequential & time-series data**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

> 🔴 **Pre-class ask from Dr Tayab (have this ready before you walk in):** *"Think of ONE real-world problem involving sequential or time-series data that could be addressed using an RNN or LSTM."* Your answer is pre-loaded in Zone 6.

---

## 🖤 The Big Idea (box it, centre of page)
> **An RNN is ONE rule reused at every time step. The hidden state `h(t)` carries a lossy summary of everything seen so far, so the network can process sequences of any length with a fixed set of weights.**
> **The catch:** reusing one rule means backprop multiplies by the same matrix over and over, so gradients vanish or explode. **LSTM's gated memory cell is the fix.**
> (Goodfellow, Bengio & Courville 2016, Ch.10 §10.1-10.2, §10.7, §10.10)

---

## 🖤 Zone 1 - Feedforward vs CNN vs RNN (his class agenda item #1)
- 🖤 All three fight the **same enemy**: too many parameters. They differ in **what they share weights across**.

| | Feedforward (MLP) | CNN | RNN |
|---|---|---|---|
| **Data shape** | fixed-size vector | **grid** (image) | **sequence** (text, audio, time series) |
| **Shares weights across** | nothing | **space** (kernel slid over the image) | **time** (one update rule per step) |
| **Key property** | - | **translation invariance** | **order sensitivity** + variable length |
| **Input length** | fixed | fixed-ish | **variable** ✅ |
| **Memory of the past** | none | none (local receptive field) | **yes** - the hidden state |

- 🔵 **Kelleher's line to quote:** an RNN is *"as deep as a sequence is long."*
- 🔴 **Activity 1 trap - "when would you STILL prefer a CNN?"** When order does not matter and **local spatial patterns** do: images, or even text where a bag of local n-grams is enough. CNNs also **parallelise** (all positions at once); RNNs must go step by step, so CNNs train faster.

## 🖤 Zone 2 - How an RNN actually processes a sequence
```text
        y1        y2        y3              yt
        ↑         ↑         ↑               ↑
 h0 →  [h1]  →   [h2]  →   [h3]  → ... →  [ht]
        ↑         ↑         ↑               ↑
        x1        x2        x3              xt
   (same W, U, V weights reused at EVERY step)
```
- 🖤 **Recurrence:** `h(t) = f(h(t-1), x(t); θ)` - state now depends on state before + current input.
- 🖤 **Unfolding** turns the loop into a deep chain; **depth = sequence length**.
- 🔵 **Parameter sharing pays off:** "I went to Nepal **in 2009**" vs "**In 2009**, I went to Nepal" - one shared rule extracts the year from *either* position. A feedforward net would relearn it per position.
- 🔵 **BPTT (Back-Propagation Through Time)** = plain backprop on the unfolded graph. Goodfellow: *"No specialized algorithms are necessary."*
- 🔵 **Teacher forcing:** during training feed the **true** `y(t-1)` instead of the model's own guess. Faster/parallel, but causes a train-vs-test mismatch.
- 🔵 **Three shapes:** output every step · output every step (output→hidden only) · **read all, emit one** (← sentiment classification uses this).

## 🖤 Zone 3 - Why basic RNNs are hard to train ⭐ SLO c) - HIS HEADLINE LIMITATION
- 🖤 Strip the nonlinearity and the recurrence is just `h(t) = Wᵗ · h(0)`. Eigendecompose `W = QΛQᵀ`:

```text
 h(t) = Q · Λᵗ · Q · h(0)      ← eigenvalues raised to the power t
   |λ| < 1  →  decays to 0   =  VANISHING gradient  (the common case)
   |λ| > 1  →  blows up      =  EXPLODING gradient  (rare, but destroys the run)
```
- 🔴 **The cruel trade-off (say this in the exam):** to store a memory *robustly*, the RNN must sit exactly where gradients vanish. So long-range signal is **always exponentially weaker** than short-range signal. It is not impossible to learn, just drowned out.
- 🔴 **The damning number:** plain-SGD RNNs fail on dependencies of only **10-20 steps** (Bengio et al. 1994).
- 🔵 **Fix for EXPLODING = gradient clipping** (§10.11.1): `if ‖g‖ > v: g ← g·v/‖g‖`. Same direction, bounded length.
- 🔵 **Fix for VANISHING = architecture** → that is Zone 4. Clipping does **not** help vanishing.

## 🖤 Zone 4 - The LSTM memory cell + gates ⭐ (his class agenda item #4)
- 🖤 **The clever idea:** a **linear self-loop** (the cell state) whose weight is **gated**, so the net *learns* when to remember and when to forget instead of decaying at a fixed rate. That creates a path where the gradient can flow far without vanishing.

```text
      c(t-1) ──×──────────────(+)──────────────→ c(t)   ← the cell (self-loop)
               ↑                ↑           ↓
            FORGET           INPUT       OUTPUT
             (σ)              (σ)          (σ)
               ↖──────── x(t) + h(t-1) ────────↗        → h(t)
```

| Gate | Activation | Job (one line) |
|---|---|---|
| **Forget** | sigmoid [0,1] | how much of the **old cell state to keep vs erase** |
| **Input** | sigmoid [0,1] | how much of the **new candidate to write in** |
| **Output** | sigmoid [0,1] | how much of the cell to **expose as `h(t)`** |

- 🔵 **Sigmoid decides *whether* (a filter, 0=block/1=pass); tanh decides *how much* (candidate in [-1,+1], can push a value up or down).**
- 🔵 **GRU** = leaner cousin, **2 gates**: `update` (does forget+input in one) + `reset`. Roughly tied with LSTM in practice.
- 🔴 **Notation warning:** Goodfellow Ch.10 writes the gates `f` / `g` / `q`; most other texts write `i` / `f` / `o` plus a separate tanh candidate. **Same three jobs, different letters** - do not panic if the symbols differ.
- 🔴 **Say "mitigates", never "resolves".** LSTM *eases* the vanishing gradient; it does not delete it. That word choice is a credibility marker.
- 🔴 **Activity 2 answer in one sentence:** *Yes, LSTMs generally beat plain RNNs, because the gated linear self-loop preserves a gradient path across many steps, whereas the plain RNN's repeated `Wᵗ` multiplication is guaranteed to vanish or explode.*

## 🖤 Zone 5 - What they are used for (Activity 3)
| Application | Why a sequence model |
|---|---|
| **NLP / sentiment / translation** | meaning depends on word **order** and long-range context |
| **Speech recognition** | audio is inherently temporal |
| **Time-series forecasting** | next value depends on the history (energy, demand, sensors) |
| **Handwriting / music generation** | output *is* a sequence |
| **Video** | CNN per frame **+** RNN across frames |

- 🔵 **seq2seq / encoder-decoder** (Sutskever et al. 2014): encoder LSTM compresses the sentence into a vector; decoder LSTM generates the translation word by word, feeding its own output back until `<eos>`. Source words fed in **reverse** helps.
- 🔵 **Image captioning** = swap the encoder for a **CNN** → CNN encodes image, LSTM decodes caption. The CNN+RNN bridge.
- 🔴 **Input/output structures (he quizzed this in class):**

| Structure | Task |
|---|---|
| one-to-one | image classification |
| one-to-many | image caption generation |
| **many-to-one** ⭐ | **sentiment / classify a whole review** ← the answer he wanted |
| many-to-many | machine translation, sequence labelling |

- 🔴 **Activity 3 verdict:** RNN/LSTM is strongest where the **output itself is a sequence** or the input is inherently temporal → **NLP and speech over computer vision**. Vision is CNN territory; RNNs only join for *video* or *captioning*.
- 🔴 **His caveat = the Activity 1 answer:** *"CNN can also be used for sequential problems, particularly when **local patterns are more important than long-term dependencies**."*
- 🔵 **Applied proof (Laib et al. 2019):** per-cluster LSTMs forecasting Algerian gas demand → **MAPE 5.48%**, beating MLP, SARIMAX and MLR, especially on irregular holiday days. Design: K-means (3 clusters) → MLP router → one LSTM per cluster.

## 🔵 Zone 6 - Your own evidence (answers his pre-class question) 🔴
**Real-world sequential problem = product-review sentiment, and you already built it.** [Review Pulse](https://github.com/lfariabr/review-pulse), 8,000 Amazon reviews, 70/15/15 split, **1,159 test**.

| Model | Accuracy | F1 |
|---|---:|---:|
| TF-IDF + Logistic Regression | 82.7% | 81.9% |
| **BiLSTM + GloVe** | **81.0%** | **80.3%** |
| DistilBERT | 88.2% | 88.6% |

- 🔴 **The honest, high-value finding: your BiLSTM LOST to the linear baseline.** Why (all Module 8 theory): ~5.6k training rows is thin for a 2-layer BiLSTM (overfits); binary document-level sentiment barely needs word order (bag-of-words suffices); `MAX_LEN=256` truncation discards long-range signal; and DistilBERT wins because **self-attention** beats recurrence at long range.
- 🔵 **Theory you can literally point at in your code:** `CLIP = 5.0` + `clip_grad_norm_` = Goodfellow eq. 10.48-49 · `torch.cat([hidden[-2], hidden[-1]])` = the 512-d lossy summary · `pack_padded_sequence` = masking pads so the summary uses real tokens only.

---

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 2 - Deep Learning Project Proposal Presentation** · 1000-word report ±10% + presentation · **30%** · due **26/07/2026** · SLOs **b) c) d) e)**.
> **Module 8 IS the A2 week.** Lecturer's live format supersedes the brief: **7-10 min + 4-5 min Q&A**, presented in class week 8 or 9; if you present live the class recording counts as submission, so you only hand in **PPT + report**.
> ✅ **PRESENTED LIVE 22/07/2026** (Luis / Victor / Juan). His verdict: *"a good project... very nice presentation."* He liked the **differentiator** (aspect-level instead of averaging conflicting sentiment). Two pointers to fix for A3: **(1)** prove there are enough **conflicting-aspect samples** (he flagged reviews skew positive); **(2)** *"while comparing 2 LSTM variants, what value addition?"* → reframe the ladder as **four families** (linear → LSTM → attention-LSTM → transformer), not two LSTMs. Formal feedback comes after the report. Full detail in [module08_notes-class.md](module08_notes-class.md).
> **Your angle:** Review Pulse **v2.3.0 → v3.0.0**, evolving document-level sentiment into **aspect-level (ABSA) with ATAE-LSTM** (Wang et al. 2016) - an LSTM **plus attention**, i.e. the exact bridge from Module 8 to the transformer. The BiLSTM-loses-to-baseline result is your *motivation*, not your embarrassment.
> **A3** (source code + 1500 words · 40% · due **19/08/2026**) = implement and benchmark it.

## 🔴 If you only memorise 5 things
1. **RNN = one shared rule across time; `h(t)` is a lossy summary of the past.** Parameter sharing across *time* is the whole trick (CNN shares across *space*).
2. **Unfold the loop → BPTT is just ordinary backprop on a very deep chain.** Depth = sequence length.
3. **`Λᵗ` is the villain:** eigenvalues < 1 vanish, > 1 explode. Plain RNNs die at **10-20 steps**.
4. **LSTM = gated linear self-loop + 3 gates (forget / input / output).** Sigmoid = *whether*, tanh = *how much*. GRU = 2 gates. It **mitigates**, never *resolves*.
5. **Clipping fixes exploding; architecture (gates) fixes vanishing.** They are not interchangeable.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your school's **nightly ETL job durations** are a time series. If you fed the last 30 nights into an LSTM to predict tomorrow's runtime, what would `h(t)` be summarising - and at what point does truncating history start costing you accuracy?
2. **Student attendance/enrolment across a term is sequential.** Which would you reach for: a SQL window function over lagged weeks, or an LSTM? Justify using the *same* argument that explains why your BiLSTM lost to TF-IDF (data volume vs model capacity, and whether order actually carries the signal).

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [x] ✅ **A2 presented live in class** (22/07). Report still due **26/07/2026**.
- [x] ✅ **Module 08 Reflection posted** (CNN vs RNN · why LSTM remembers longer · is LSTM always better).
- [ ] 🔴 **🆕 NEW activity he assigned in class:** ask a **generative AI** *"LSTM is always better than a basic RNN because it has more memory - correct?"*, then **critique the answer**: is the claim too general? does it get the **gates** right? does it weigh **computational cost**? does it consider **short/simple sequences**? Post to the forum (short response is fine).
- [ ] 🕐 **Activity 3 - Applications:** are RNNs better for NLP, speech, or CV? **Presented verbally in class**, backed with references.
- [ ] 🔴 **A3 prep:** get the **exact** SemEval-2014 restaurant count into the report (in class "thousands"/"100,000" were both wrong - it is ~3k sentences) + report conflicting-aspect sample counts.
