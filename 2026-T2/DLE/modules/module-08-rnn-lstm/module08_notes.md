# Module 8 — Recurrent Neural Networks and Long Short-Term Memory

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow, Bengio & Courville (2016), Ch.10 — sequence modelling, RNNs, BPTT, LSTM | ✅ |
| **2** | Read & summarise Kelleher (2019), Ch.5 — RNN + LSTM the intuitive way (buffer, gates, seq2seq) | ✅ |
| **3** | Read & summarise Laib, Khadir & Mihaylova (2019) — LSTM for natural-gas day-ahead forecasting | ✅ |
| **4** | Read & summarise Mittal (2019) — Understanding RNN and LSTM (blog primer) | ✅ |
| 5 | Activity 1: Comparison — CNN vs RNN, and when you would still prefer a CNN | 🕐 |
| 6 | Activity 2: What Do You Think? — do LSTMs really beat plain RNNs, and why (≤100 words) | 🕐 |
| 7 | Activity 3: Applications — which of NLP / speech / vision suits RNNs best (verbal, referenced) | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep Learning, Ch.10 — Sequence Modeling: Recurrent and Recursive Nets.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning.* Cambridge, MA: MIT Press. https://www.deeplearningbook.org/ (Chapter 10)

**Purpose:** The rigorous, canonical treatment. It explains *why* RNNs exist (parameter sharing across time), *why* they are hard to train (vanishing/exploding gradients through a deep unrolled graph), and *how* LSTM and GRU gates fix it. Dr Tayab flagged **§10.2 (RNNs)** and **§10.10 (LSTM / gated RNNs)** as the core, plus §10.7 (long-term dependencies).

---

#### 1. Why RNNs — parameter sharing across time
- **The core idea:** an RNN reuses the *same* weights at every time step, instead of learning a separate rule per position. This is what lets one network handle **variable-length** sequences and **generalise a pattern across positions**.
- Goodfellow's example: "I went to Nepal in 2009" vs "In 2009, I went to Nepal." You want the model to extract `2009` regardless of *where* it sits. A fully connected feedforward net would need to learn the rule separately at each position; an RNN shares one rule.
- **Unfolding a computational graph:** the recurrence `h(t) = f(h(t-1), x(t); θ)` is unrolled into a chain. The same `θ` (and the same `f`) appears at every step, giving "a very deep computational graph" whose depth equals the sequence length.
- **The hidden state is a lossy summary.** `h(t)` compresses the whole past `(x(1)…x(t))` into a fixed-length vector. It is *necessarily* lossy — the training objective decides which aspects of the past survive.

#### 2. Design patterns and how you train them
- **Three canonical shapes:** (a) output at every step with hidden-to-hidden recurrence; (b) output at every step with *output-to-hidden* recurrence only; (c) read the whole sequence, then emit a **single** output at the end.
- An RNN of finite size is **Turing-universal** — but only as a *theoretical* result: it assumes binary inputs, discretised outputs, and exact/unbounded-precision arithmetic (Siegelmann & Sontag's ~886-unit construction). It does **not** mean a small RNN on a GPU is a universal computer in practice.
- **BPTT (Back-Propagation Through Time):** training is *just* ordinary back-propagation applied to the unrolled graph. "No specialized algorithms are necessary." The cost is that the gradient must flow back through the entire sequence length.
- **Teacher forcing:** when the model has output-to-output connections, you train by feeding the *true* target `y(t-1)` (not the model's own prediction) as the next input. It decouples the steps so they can be trained in parallel, but creates a train/test mismatch (at test time the model must consume its *own* outputs).

#### 3. The challenge of long-term dependencies ⭐
- Compose the same function `t` times and you effectively **multiply by the same weight matrix `t` times**. Eigen-decompose `W = Q Λ Qᵀ` and the recurrence becomes `h(t) = Q Λᵗ Q h(0)`.
- **Eigenvalues get raised to the power `t`:** magnitudes `< 1` **decay to zero** (vanishing gradient), magnitudes `> 1` **blow up** (exploding gradient). This is the whole problem in one line.
- The cruel trade-off: to store a memory robustly the RNN *must* sit in the region where gradients vanish. So long-term signal is always exponentially weaker than short-term signal. Empirically, plain-SGD RNNs fail to learn dependencies across even **10–20 steps**.

#### 4. LSTM and GRU — gated paths that neither vanish nor explode ⭐
- **The clever trick:** the LSTM cell has a **linear self-loop** (the cell state `s`) whose weight is *gated* — controlled by another unit — so the network *learns* when to remember and when to forget, instead of using a fixed decay.

| Gate | Activation | Job |
|---|---|---|
| **Forget gate** `f` | sigmoid → [0,1] | how much of the old cell state to keep vs erase |
| **Input gate** `g` | sigmoid → [0,1] | how much of the new candidate to write into the cell |
| **Output gate** `q` | sigmoid → [0,1] | how much of the cell state to expose as the hidden output |

> **Notation note:** this table follows **Goodfellow Ch.10's own symbols** — forget `f` (eq 10.40), external input gate `g` (eq 10.42), output gate `q` (eq 10.43-44). Most other texts (and the Kelleher/Mittal readings) write the input gate as `i` and the output gate as `o`, with a separate **tanh candidate** unit feeding the cell. Same three jobs, different letters — don't let the symbols trip you in the exam.

- **GRU** (gated recurrent unit) is the lean cousin: a single **update** gate does the job of LSTM's forget+input at once, plus a **reset** gate. Empirically GRU and LSTM are roughly tied; no variant clearly beats both.
- **What actually matters:** Greff et al. (2015) found the **forget gate** is the crucial ingredient; Jozefowicz et al. (2015) found initialising the **forget-gate bias to 1** makes a vanilla LSTM as strong as any tuned variant.

#### 5. Making training stable
- **Gradient clipping** (for *exploding* gradients): if `‖g‖ > v`, rescale `g ← g·v/‖g‖`. Keeps the step in the gradient direction but bounds its length, so one exploding step can't wreck the model. Cheap, standard, effective.
- Vanishing gradients are the harder half — that is what the gating architectures (LSTM/GRU), leaky units, and skip-connections through time are for.

#### Key Takeaways for Deep Learning (DLE602)
1. **Activity 2 answer lives here.** LSTMs beat plain RNNs *because* the gated linear self-loop creates a path where the gradient can flow across many steps without vanishing — the plain RNN's repeated `Wᵗ` multiplication cannot. That is the causal mechanism, not just "LSTM is better."
2. **Activity 1 (CNN vs RNN) hinges on parameter-sharing style:** a CNN shares weights across *space* (a kernel slid over a grid, translation-invariant); an RNN shares weights across *time* (one update rule reused per step, order-sensitive). Both fight the parameter explosion, in different domains.
3. Connects straight back to **Module 5 (CNNs)** and forward to **Module 9 (Representation Learning)** — the hidden state `h(t)` is a *learned representation* of the sequence so far, the same lens used for autoencoders in Module 7.

---

### 2. Kelleher, J. D. (2019). Deep Learning, Ch.5 — Convolutional and Recurrent Neural Networks.

**Citation:** Kelleher, J. D. (2019). *Deep learning.* Cambridge, MA: MIT Press. (Chapter 5, ProQuest Ebook Central)

**Purpose:** The plain-English companion to Goodfellow. Same concepts, no heavy maths — ideal for building the mental picture and for phrasing forum answers at the lecturer's deliberately intuitive level. Also gives the cleanest CNN-vs-RNN contrast, which is exactly Activity 1.

---

#### 1. Tailoring a network to its data
- Constraining connections, sharing weights, or adding backward connections is a way of **building domain knowledge into the network** — it narrows the set of functions the net can learn and guides it to a useful solution.
- **CNNs** suit *grid-like* data (images): early neurons detect local visual features, deeper neurons combine them into faces/objects. Weight sharing gives **translation invariance** (LeCun's "flashlight in a dark room" metaphor — same detector slid across the whole image).
- **RNNs** suit *sequential* data (text, time series): each element is processed *in the context of* the previous ones.

#### 2. The RNN as a hidden layer plus a memory buffer
- An RNN has **one hidden layer** plus a **memory buffer** that stores that layer's output for one input and feeds it back alongside the next input.
- The buffer just *stores* — it applies no transformation, so there are **no weights on the hidden→buffer edges** (but there are weights on buffer→hidden). Kelleher's memorable line: an RNN is "**as deep as a sequence is long**."
- **Unrolled through time**, `[X1, X2, …, Xt]` produces hidden states `[h1…ht]` and outputs `[Y1…Yt]`, each horizontal arrow re-using the same stationary weights — which is exactly why the vanishing gradient bites (backprop through `k` steps multiplies by the same weight `k` times).

#### 3. LSTM gates and seq2seq — the applications payoff
- The **cell** runs along the top of the LSTM diagram carrying activations in [-1, +1]. **Sigmoid** layers act as *filters* (0 = block, 1 = pass); **tanh** layers produce the candidate update (can push a value up *or* down).
- **seq2seq / encoder–decoder** (Sutskever et al. 2014): two LSTMs joined. The encoder reads a sentence and its final hidden state becomes a **vector representation of the whole sentence**; the decoder "hallucinates" the translation word by word, feeding each output back as the next input until it emits `<eos>`.
- Source words are fed in **reverse order** — empirically improves translation. **word2vec** embeddings turn words into vectors first (words in similar contexts → similar vectors, e.g. London/Paris).
- **Image captioning** = swap the encoder LSTM for a **CNN**: the CNN encodes the image to a vector, the LSTM decodes it to a caption. This CNN+RNN combination is the practical bridge between Modules 5 and 8.

#### Key Takeaways for Deep Learning (DLE602)
1. **Best single source for Activity 1.** Kelleher literally lays CNN (space, translation-invariant, grid) beside RNN (time, order-sensitive, sequence) in one chapter — cite it for the "most important difference."
2. **Activity 3 (applications) answer:** seq2seq, machine translation, and image captioning show RNN/LSTM is strongest where the *output itself is a sequence* — i.e. NLP and speech — while vision leans on CNNs to produce the input representation.
3. Reinforces the Goodfellow gate story in words you can actually write in a 100-word forum post without equations.

---

### 3. Laib, O., Khadir, M. T. & Mihaylova, L. (2019). Toward efficient energy systems based on natural gas consumption prediction with LSTM recurrent neural networks.

**Citation:** Laib, O., Khadir, M. T. & Mihaylova, L. (2019). Toward efficient energy systems based on natural gas consumption prediction with LSTM recurrent neural networks. *Energy, 177*, 530–542. https://doi.org/10.1016/j.energy.2019.04.075

**Purpose:** The real-world case study — LSTMs applied to **day-ahead natural-gas load forecasting** in Algeria. Shows an RNN not as a toy but inside a deployed forecasting pipeline, and models exactly the kind of "compare against benchmarks with proper error metrics" discipline the assessments reward.

---

#### 1. The problem and the hybrid design
- **Task:** forecast next-day hourly natural-gas consumption for the Algerian grid operator (SONELGAZ) — hard because of a huge, climatically diverse country and irregular holiday/special-day demand.
- **Their contribution — a two-stage FM-MLP (Forecasting Monitoring MLP):**
  1. **Cluster** historical daily consumption profiles with **K-means** — the **elbow method** picked **3 clusters** of similar load shapes.
  2. An **MLP** classifies *which cluster* tomorrow's profile will resemble (a "forecasting monitor").
  3. That routes the forecast to a **dedicated LSTM per cluster** — a specialist model for each load behaviour, rather than one global model.

#### 2. Method details worth citing
- **Inputs:** lagged hourly load (best lag window found empirically), max/min temperature, and calendar variables (day-of-week, month-of-year).
- **Normalisation:** all inputs/outputs scaled to **[0, 1]** before feeding the LSTM — a standard, essential preprocessing step.
- **Error metrics:** **MAPE**, **MAE**, **RMSE** — the same regression-evaluation trio the whole field uses (and that BDA Module 7 covers). Reported on a held-out **test** set.

#### 3. Results
| Result | Value |
|---|---|
| Profile-classification accuracy (the "monitor" MLP) | **98.34%** on the real test set |
| Weighted-average **MAPE** of the assigned LSTMs (test) | **5.48%** |
| Weighted-average **MAE** / **RMSE** (test) | **0.0083** / **0.0108** |
| Benchmarks beaten | MLP-ANN, plain LSTM-RNN, SARIMAX, MLR |

- The gain is **especially pronounced on irregular days** (holidays, special periods) — precisely where a single general model fails and a cluster-specialised LSTM wins.

#### Key Takeaways for Deep Learning (DLE602)
1. **A2/A3 template.** This is the shape of a credible deep-learning project: pick a task, engineer sensible inputs, normalise, train, and *justify* the model by beating named baselines on standard metrics — not by quoting one number in isolation.
2. **LSTM ≠ always the whole answer.** Their winning system pairs clustering + an MLP router + per-cluster LSTMs. Good reminder for the assessments that the architecture should fit the data structure, not the hype.
3. **Day-job anchor:** this is a time-series forecasting pattern you could map onto forecasting daily enrolment, attendance, or resource load at the school — cluster the "day types" (term vs holiday vs exam week), then forecast within each.

---

### 4. Mittal, A. (2019, 12 October). Understanding RNN and LSTM.

**Citation:** Mittal, A. (2019, 12 October). Understanding RNN and LSTM. *Towards Data Science / Medium.* https://towardsdatascience.com/understanding-rnn-and-lstm-f7cdf6dfc14e

**Purpose:** A 4-minute blog primer. Not academically weighty, but a clean, fast refresher on the vocabulary — good for locking in the gate names and the RNN "feedback loop" picture before the heavier sources.

---

#### 1. RNN in one paragraph
- An RNN is "a generalization of a feedforward network that has an **internal memory**." It applies the *same* function to every input, and the current output depends on the previous computation — the output is **copied and fed back** into the network.
- The contrast that matters: in a plain feedforward net all inputs are **independent**; in an RNN all inputs are **related**. The current state uses `tanh` to squash activations into [-1, 1].

#### 2. Advantages, disadvantages, and the LSTM fix
| | Points |
|---|---|
| **RNN advantages** | models sequential/dependent data; can be combined with convolutional layers |
| **RNN disadvantages** | **vanishing & exploding gradients**; hard to train; struggles with long sequences under tanh/ReLU |
| **LSTM fix** | a modified RNN that "makes it easier to remember past data" and **mitigates the vanishing-gradient problem** (Mittal's blog says "resolves" — overstated; the gated self-loop *eases* it, does not delete it); well-suited to classifying/processing/predicting time series with unknown time lags |

- **The three gates, restated simply:** **input gate** (which new values update the memory), **forget gate** (which details to discard — sigmoid outputs 0 = omit, 1 = keep), **output gate** (which memory to expose). Sigmoid decides *whether*, tanh weights *how much* (importance in [-1, 1]).

#### Key Takeaways for Deep Learning (DLE602)
1. Fastest way to memorise the **three-gate vocabulary** for Activity 2 and the exam — but cite Goodfellow/Kelleher for anything you actually submit; a Medium post is background, not evidence.
2. Confirms the same causal chain from the heavyweight sources (vanishing gradient → LSTM gates) in plain language you can paraphrase.
3. Its "RNN = feedback loop" framing pairs well with Kelleher's "memory buffer" framing — two intuitions for the same recurrence.
