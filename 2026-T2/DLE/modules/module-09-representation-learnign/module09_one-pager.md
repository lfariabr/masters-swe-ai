# DLE602 · Module 9 - One-Pager

> **Representation Learning · what makes a representation "good" · manual features vs learned · greedy layer-wise pretraining · transfer & domain adaptation · distributed representations · disentangling causal factors**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **A good representation is one that makes the *next task easier* - always defined relative to a downstream task, never absolutely. Deep nets don't just classify; every layer before the final linear/softmax exists to *learn a representation* that hands the classifier something linearly separable. Representation learning is the unifying lens over the whole course.**
> (Goodfellow, Bengio & Courville 2016, Ch.15 · Bengio et al. 2013 · **Tayab pre-class, Wk 9**)

🔵 **The Roman-numeral test:** `210 ÷ 6` is trivial; `CCX ÷ VI` is near-impossible. *Same information, different encoding* → the task is easy or hard depending on representation. That is the whole module in one line.

---

## 🖤 Zone 1 - Manual features vs learned representations ⭐ (Tayab's core comparison)
- 🖤 **Traditional ML = manual feature engineering** (hand-pick features: SIFT/HOG for images, **TF-IDF** for text). Labour-intensive; limited by human ingenuity.
- 🔵 **Deep nets learn task-specific features directly from raw data** (pixels, text, audio, graphs). Tayab's example: don't process every pixel independently - learn *"smiling / angry / confused"* representations (**low-dimensional state vectors**, not high-dim images).
- 🔴 **Zhong (2016) draws the line explicitly:** TF-IDF is *feature engineering*, **excluded** from feature *learning*. → this is exactly where your **Review Pulse TF-IDF baseline vs BiLSTM/DistilBERT** sits: hand-crafted vs learned representation.
- 🔵 **Supervised nets do it as a side effect** (no explicit constraint on hidden features); autoencoders/sparse coding do it *explicitly* (shape `h` for sparsity/independence). **Core trade-off:** preserve input info **vs** attain nice properties. Can't max both.

## 🖤 Zone 2 - §15.1 Greedy layer-wise unsupervised pretraining ⭐ SLO c) - THE ASSIGNED DEEP-DIVE
- 🖤 **What:** train a deep net **one frozen layer at a time**, each via an unsupervised single-layer learner (RBM / autoencoder / sparse coding), then **fine-tune** the whole stack.
- 🔵 **The three words:** **greedy** (each layer optimised alone) · **layer-wise** (lower layers fixed once trained) · **pretraining** (phase 1 only; supervised fine-tune follows).
- 🔵 **Why it worked (§15.1.1):** (1) init has a **regularising** effect (Erhan 2010: pretrained nets halt in the same smaller region → less variance); (2) features for `p(x)` help `p(y|x)`. Best when **labels scarce + unlabelled abundant + true function complex**.
- 🔴 **Historical vs modern - the distinction that matters:** the *exact 2006 procedure* is **largely historical**. But its idea - *pretrain on unlabelled data, then fine-tune* - became **modern self-supervised pretraining**, dominant in **both** NLP (word2vec/GloVe → BERT/DistilBERT) **and** vision (contrastive/masked SSL). One-hot words carry **zero** similarity (every pair √2 apart) → embeddings won here first and never left.

## 🖤 Zone 3 - Transfer, domain adaptation & the extremes ⭐ SLO e)
- 🖤 **Transfer learning:** exploit `P₁` to generalise on `P₂` when they share underlying factors. Deeper reps → fewer labels needed downstream.
- 🔴 **Domain adaptation = same task, shifted input.** Goodfellow's *own* example: **sentiment trained on book/DVD/music reviews → applied to electronics** (denoising-AE pretraining, Glorot 2011). **This IS your multi-domain Amazon setup** - not a coincidence.
- 🔵 **Concept drift** = transfer across *time*. **One-shot** (1 example) needs a rep that already separates classes; **zero-shot** needs *more* - **task info `T` + a shared semantic space** (recognise a cat from having *read* "cats have 4 legs, pointy ears") → enables **multimodal** anchoring (image ↔ word).

## 🖤 Zone 4 - Distributed representations (the efficiency argument) ⭐
- 🖤 **Distributed:** `n` features set independently → `kⁿ` concepts; each *direction* = one underlying factor.

| | Distributed | Non-distributed (one-hot / local) |
|---|---|---|
| Regions from `n` params in `Rᵈ` | `O(nᵈ)` (exponential) | `O(n)` (linear) |
| Examples | neural nets, RBMs, **word embeddings** | k-means, kNN, decision trees, n-grams |
| Generalises via | **shared attributes** (cat & dog share `has_fur`) | local smoothness only → curse of dim |

- 🔵 **Bounded capacity despite exponential regions:** VC-dim of linear-threshold nets ≈ `O(w log w)`. Powerful rep + *weak* linear classifier = strong regulariser.
- 🔴 **Vector arithmetic payoff (Radford 2015):** `man+glasses − man + woman = woman+glasses`, discovered **with no labels** - same property as word2vec `king − man + woman = queen`.
- 🔵 **Depth (§15.5):** depth-`k` functions can need *exponential* units at depth 2 → depth = **feature re-use by composition**, extra statistical efficiency on top of distributed.

## 🖤 Zone 5 - What makes a rep "good", the deeper answer + the map
- 🖤 **Disentangling causal factors (§15.3):** ideal rep = separate directions for the **underlying causes**. If `y` is a salient cause of `x`, modelling `p(x)` reveals `y` almost free → justifies semi-supervised learning.
- 🔵 **Salience is learned, not fixed:** MSE drops small features (ping-pong ball, ears); **GANs** *generate* them by redefining salience (Lotter 2015).
- 🔵 **Bengio's 3 families (the mental index):** **probabilistic models** (RBM/DBN, sparse coding) · **autoencoders** (Module 7) · **manifold learning** (PCA, Isomap, LLE).
- 🔵 **Zhong's timeline:** PCA 1901 → LDA 1936 → manifold 2000 → deep learning (Hinton 2006). *Deep learning is not a new idea* = feature-learning + big data + GPUs.
- 🔴 **The thesis sentence (= Activity 2 prompt, verbatim):** *"Feedforward and recurrent networks, autoencoders and deep probabilistic models all learn and exploit representations."*

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Deep Learning Final Project** · source code + 1500-word report · **group** · **40%** · due **19/08/2026** · SLOs **c) d) e)**.
> Module 9 feeds A3 directly: *"analyse the dataset, consider how best to represent input data, evaluate the impact of representation learning."* 🔴 **Tayab's pre-class reflection = your prep:** *how is your input represented, and could another representation make the task easier?*
> **Answer (Review Pulse):** today = **GloVe 100d embeddings → BiLSTM → one 512-d document vector** (document-level). A single vector **can't** separate *"camera great, battery terrible."* **ATAE-LSTM (v3.0.0)** appends an **aspect embedding** + aspect-conditioned attention → the *same sentence gets a different representation per aspect*. That is the Roman-numeral point applied: better encoding → easier task.

## 🔴 If you only memorise 5 things
1. **Good rep = makes the next task easier** (Roman numeral); always relative to the downstream task.
2. **Manual feature engineering (TF-IDF) vs learned representation (embeddings)** - Zhong draws the exact line your baseline vs BiLSTM sits on.
3. **Greedy layer-wise pretraining (2006) is historical; its child, self-supervised pretraining, rules NLP *and* vision.**
4. **Distributed rep = `O(nᵈ)` regions from `O(n)` params**, generalises via shared attributes; depth adds feature re-use.
5. **Disentangle the causal factors** = the deep "what is good"; and *everything* (FF/RNN/AE/probabilistic) learns representations (Activity 2).

---

### Margin prompts (answer in blue while you write - anchor to your day job at St Cat's)
1. **Student 360** represents each girl as raw Synergetic fields (attendance %, marks, house, cohort). Tayab's point is that "engagement" isn't one column - it's a **low-dimensional learned state vector**. Which raw signals would you feed a net to *learn* a student-engagement representation, instead of hand-bucketing "at-risk" with SQL thresholds?
2. Teacher **effort/report free-text comments** are your closest Review-Pulse analogue: text → learned embedding (not hand-coded keywords). If you had to justify to Lucas *why* a learned embedding of comment text beats a one-hot keyword flag, what's the one-sentence reason? (hint: one-hot = every word √2 apart, zero similarity; embeddings encode it by distance.)

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 **Pre-class (do in the first hour, 4:00pm start):** re-read Ch.15 §15.1, prep the reflection answer above.
- [ ] 🕐 **Activity 1** - Warm-up (verbal): *"why should we care about representation learning?"* → recite distributed → depth → disentangle → objectives.
- [ ] 🕐 **Activity 2** - Think Before You Write (≤100 words, forum): critique the thesis sentence; agree, cite the 4 families as evidence.
- [ ] 🕐 **Activity 3** - Applications (≤100 words, forum): a computer-vision app that degrades *without* representation learning + why.
