# Module 8 x Review Pulse - Theory-to-Code Bridge

## From the shipped BiLSTM (v2.3.0) to the proposed ATAE-LSTM (v3.0.0)

> **Why this file exists.** Module 8 (RNN/LSTM) is not abstract for you - you already built and shipped a BiLSTM in [`review-pulse`](https://github.com/lfariabr/review-pulse). This document maps each Module 8 concept onto the *actual code you wrote*, reads your real results through the theory, and turns that into the DLE602 Assessment 2 proposal: evolving Review Pulse **v2.3.0 (ISY503, document-level sentiment)** into **v3.0.0 (DLE602, aspect-level sentiment with ATAE-LSTM)**.
>
> Repo cloned locally at `~/Desktop/sEngineer/review-pulse` (tip = tag `v2.3.0`, no v3 code yet - greenfield).

---

## Part A - Module 8 theory, already living in your code

Every core idea from the readings has a concrete home in the BiLSTM you shipped. This is the fastest active-recall drill you have: read the concept, then open the file and see it.

| Module 8 concept (source) | Where it lives in Review Pulse | What to notice |
|---|---|---|
| **Recurrence over a sequence** (Goodfellow §10.2; Kelleher "as deep as a sequence is long") | `src/models/bilstm.py:64` `nn.LSTM(...)` | One LSTM reused across up to 256 time steps; depth = sequence length. |
| **Parameter sharing across time** (Goodfellow §10.1) | same `nn.LSTM` module | The *same* weights process token 1 and token 200. That is why a 30k-word vocab does not explode the parameter count. |
| **Hidden state as a lossy summary** (Goodfellow §10.2) | `src/models/bilstm.py:100` `torch.cat([hidden[-2], hidden[-1]])` | The whole review is compressed into one 512-d vector (256 forward + 256 backward). That vector *is* `h(t)` - the lossy summary the theory describes. |
| **Bidirectionality** (Goodfellow §10.3) | `bidirectional=True`, `bilstm.py:64` + the concat at `:100` | Forward pass reads left-to-right, backward reads right-to-left; you fuse both endpoints. Context from *both* sides of each word. |
| **Vanishing/exploding gradients** (Goodfellow §10.7; Mittal) | the reason the next two rows exist | Backprop through 256 steps multiplies by the same recurrent weights repeatedly - the core training pain. |
| **Gradient clipping** (Goodfellow §10.11.1) | `src/training/bilstm.py:39` `CLIP = 5.0` + `:76` `clip_grad_norm_(...)` | This is *literally* equation 10.48-10.49: if the gradient norm exceeds 5.0, rescale it. You are running the textbook fix. |
| **Gated cell / stacked layers** (Goodfellow §10.10) | `n_layers=2`, `dropout=0.5` in `bilstm.py:64-72` | Two stacked LSTM layers with inter-layer dropout; the LSTM cell's forget/input/output gates are inside PyTorch's `nn.LSTM`. |
| **Pre-trained embeddings** (Kelleher, word2vec/GloVe) | `src/tokenization/vocab.py:68` `load_glove(...)` | GloVe 6B 100d initialises the embedding matrix, left trainable. The "words in similar contexts get similar vectors" idea from Kelleher, wired in. |
| **Padding / variable length** (Goodfellow §10.1 - variable-length sequences) | `bilstm.py:93` `pack_padded_sequence` + `padding_idx=0` at `:49` | You mask the pad tokens so the LSTM's summary reflects only *real* words - a correctness detail most students miss. |
| **Truncation trade-off** (compression vs information loss) | `src/tokenization/sequence.py:9` `MAX_LEN = 256` + `:23` `[:max_len]` | Reviews longer than 256 tokens are cut. Any long-range signal past token 256 is discarded before the LSTM even sees it - relevant to Part B. |

**Training setup for the record** (`src/training/bilstm.py`): Adam @ `lr=1e-3` (`:38,201`), `BCEWithLogitsLoss` (`:202`), 10 epochs (`:37`), `seed=42` (`:180`), best checkpoint by validation F1. Clean, reproducible, fixed-seed - exactly the ML hygiene the assessments reward.

---

## Part B - Your honest result, read through the theory

Held-out test split (1,159 reviews, stratified 70/15/15, seed 42):

| Model | Accuracy | F1 |
|---|---:|---:|
| TF-IDF + Logistic Regression (baseline) | 82.7% | 81.9% |
| **BiLSTM + GloVe** | **81.0%** | **80.3%** |
| DistilBERT | 88.2% | 88.6% |

**The uncomfortable, valuable fact: your BiLSTM lost to the TF-IDF baseline.** Do not hide this - it is your strongest critical-analysis material, and Module 8 explains exactly why:

1. **Dataset size vs model capacity.** ~5,600 training reviews is small for a 2-layer BiLSTM (hundreds of thousands of recurrent params). TF-IDF + LogReg has far less to fit and generalises better in the low-data regime. The sequence model's extra capacity bought overfitting, not signal.
2. **Document-level binary sentiment barely needs order.** For "is this review positive or negative?", a bag-of-words signal (great, terrible, refund) is often enough - which is precisely what TF-IDF captures. The BiLSTM's whole advantage (word *order* and long-range context) is under-used by the task.
3. **The 256-token truncation + lossy summary.** Squeezing a whole review into one 512-d vector, after cutting anything past token 256, throws away detail that a sparse TF-IDF vector keeps.
4. **DistilBERT wins because self-attention beats recurrence at long-range context** - the pre-trained transformer sidesteps the vanishing-gradient bottleneck (Goodfellow §10.7) that the BiLSTM only *mitigates*.

> **Proposal one-liner (SLO c):** "Our own benchmark shows a BiLSTM does not automatically beat a linear baseline on document-level sentiment; the sequence model's value appears only when the *task itself* depends on structure the bag-of-words cannot see. That motivates moving from document-level to **aspect-level** sentiment, where word-to-aspect association is the whole point."

That sentence is the hinge from v2.3.0 to v3.0.0. It makes the LSTM's earlier "failure" the *reason* for the new architecture.

---

## Part C - v3.0.0: ATAE-LSTM (the proposed extension)

**ATAE-LSTM = Attention-based LSTM with Aspect Embedding** (Wang, Huang, Zhu & Zhao, 2016, EMNLP). It is the natural next step *within the LSTM family* - and it is the perfect Module 8 capstone because it is **LSTM + attention**, i.e. the exact bridge between recurrence (Module 8) and the transformer (DistilBERT).

### The task change: document-level → aspect-level (ABSA)
- **v2.3.0 question:** "Is this review positive or negative?" (one label per review).
- **v3.0.0 question:** "What is the sentiment *toward a given aspect*?" e.g. *"The camera is great but the battery is terrible"* → `camera: positive`, `battery: negative`.
- A single bag-of-words / single-hidden-vector model **cannot** do this - the same sentence has two opposite labels depending on the aspect. This is a task where **the sequence model's structure finally earns its keep**, answering Part B directly.

### Architecture delta from your existing BiLSTM
You keep most of the pipeline (GloVe embeddings, tokenizer, training loop, gradient clipping, seed) and add three things from Wang et al. (2016):

| Component | Current BiLSTM (v2.3.0) | ATAE-LSTM (v3.0.0) |
|---|---|---|
| **Aspect embedding** | none | learn an embedding per aspect term; **append it to every word vector** at input (the "AE" in ATAE) |
| **Sequence read-out** | final hidden state only (`hidden[-2]`+`hidden[-1]`) | **attention over all hidden states**, conditioned on the aspect - a weighted sum, not just the last step |
| **Output** | 1 logit (binary) | sentiment over {pos, neu, neg} for the (sentence, aspect) pair |

The attention layer computes a weight for each word conditioned on the aspect, so the model *learns to look at "great" when asked about the camera and "terrible" when asked about the battery*. That attention-weighted representation replaces the single lossy summary - and is conceptually the same move the transformer makes, just aspect-conditioned and single-headed.

### Why this is a strong DLE choice (not just novelty)
- **Stays in Module 8's family** (it is an LSTM) so the theory you studied applies directly, while introducing **attention** so you can critically compare against DistilBERT's self-attention (SLO c, e).
- **Genuinely new deliverable** over the ISY503 work - new task (ABSA), new architecture, new dataset labelling - which matters for the reuse note below.
- **Bounded scope** - it reuses ~70% of your shipped pipeline, so it is finishable inside the A2 → A3 window.

---

## Part D - Mapping to the assessment

### Assessment 2 (Proposal Presentation, due 26/07/2026, 7-10 min + 4-5 Q&A, group, 30%)
Your architecture-evolution slide almost writes itself:

**RNN → LSTM → BiLSTM (shipped) → ATAE-LSTM (proposed) → [transformer baseline: DistilBERT]**

- **SLO b** (pre-process signals/text): GloVe embeddings + aspect embeddings, tokenisation, truncation choices - all evidenced in code.
- **SLO c** (critical analysis): the honest BiLSTM-loses-to-baseline result → the argument for aspect-level modelling. Cite Goodfellow §10.7 and Wang et al. (2016).
- **SLO d** (collaboration): group roles across the v3.0.0 issues.
- **SLO e** (communicate technical info): the live demo of the existing Streamlit app grounds the proposal in something real and running.

### Assessment 3 (Final Project, source + 1500 words, due 19/08/2026, 40%)
- Implement `src/models/atae_lstm.py` + `src/training/atae_lstm.py` mirroring your BiLSTM structure.
- Benchmark ATAE-LSTM vs a plain aspect-agnostic BiLSTM vs DistilBERT on an ABSA dataset (SemEval-2014 Task 4 restaurants/laptops is the standard, or aspect-label a subset of your Amazon reviews).
- Report accuracy/F1 per aspect - reuse `src/evaluation/` and the Laib et al. (2019) discipline of *beating named baselines on standard metrics*, not quoting one number.

### One honesty flag (raise it, do not bury it)
Review Pulse was built for **ISY503 Assessment 3**. Reusing the same repo for DLE602 is fine **if the DLE deliverable is genuinely new work** (ATAE-LSTM + ABSA is), but you must be transparent: state in the report/declaration that this extends a prior individual/group project, and that the *assessed contribution* is the v3.0.0 aspect-level work. Confirm the reuse framing with Dr Tayab in class - it is a five-minute question that removes all self-plagiarism risk.

---

## Part E - Momentum (keep the 100+ commit streak)
Suggested issues to open on `review-pulse` for the v3.0.0 milestone:
1. `feat: aspect-labelled dataset loader` (SemEval-2014 or aspect-tagged Amazon subset).
2. `feat: aspect embedding layer + ATAE input concatenation`.
3. `feat: aspect-conditioned attention read-out`.
4. `feat: ATAELSTMSentiment model` (`src/models/atae_lstm.py`).
5. `feat: training loop + checkpoint for ATAE-LSTM` (reuse clip=5.0, seed=42).
6. `feat: per-aspect evaluation + comparison table vs BiLSTM/DistilBERT`.
7. `docs: v3.0.0 release notes + DLE602 A2 presentation outline`.

Tag the result **v3.0.0** to mark the DLE milestone, matching your existing v1→v2.3 release cadence.

---

## References
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning*, Ch.10. MIT Press. https://www.deeplearningbook.org/ (see [module08_notes.md](module08_notes.md) for the detailed summary)
- Kelleher, J. D. (2019). *Deep learning*, Ch.5. MIT Press.
- Wang, Y., Huang, M., Zhu, X. & Zhao, L. (2016). Attention-based LSTM for aspect-level sentiment classification. *Proceedings of EMNLP 2016*, 606-615. https://aclanthology.org/D16-1058/
- Laib, O., Khadir, M. T. & Mihaylova, L. (2019). Toward efficient energy systems ... with LSTM recurrent neural networks. *Energy, 177*, 530-542. https://doi.org/10.1016/j.energy.2019.04.075
- Review Pulse source: https://github.com/lfariabr/review-pulse (v2.3.0)
