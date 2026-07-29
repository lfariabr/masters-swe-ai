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

## 🖤 Zone 2 - Greedy layer-wise unsupervised pretraining ⭐ SLO c) - THE ASSIGNED DEEP-DIVE
*(Goodfellow Ch.15, Section 15.1 - the section Tayab told you to read)*
- 🖤 **What:** before training the whole net, train it **one layer at a time on UNLABELLED data** (freeze each layer once done), then **fine-tune** the full stack on your labelled task. Pretrain first, then specialise.
- 🔵 **The three words:** **greedy** = one layer at a time (not all together) · **layer-wise** = a layer is frozen once trained · **pretraining** = this is only phase 1; the labelled fine-tune comes after.
- 🔵 **Why it helped - reason 1 (better starting point):** nets start from random weights; pretraining gives a **smarter start**, so the net lands in a smaller, consistent region → less overfitting (Erhan 2010). *"regularising" = anything that curbs overfitting.*
- 🔵 **Why it helped - reason 2 (learning the data helps the task):** learning **what the data looks like** (`p(x)` - free, no labels) hands you features that also help **predict the label** (`p(y|x)`). → best when **you have few labels but tons of unlabelled data** (your exact case: thousands of student records, few hand-labelled "at-risk").
- 🔴 **Old trick, living idea:** the *specific 2006 procedure* is **mostly dead**. But its idea - *pretrain on unlabelled data → fine-tune* - is **exactly what BERT/DistilBERT do** (= your winning Review Pulse model). Now called **self-supervised pretraining**, dominant in text *and* vision.
- 🔵 **Why text adopted it first:** one-hot words (`cat=[1,0,0]`, `dog=[0,1,0]`) are **all equally far apart** (√2) - the model can't tell cat is closer to dog than to table. **Embeddings fix that** (put cat near dog) → NLP jumped on pretraining and never let go.

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
- 🔴 **Shortcuts / spurious features (class - SLO d, ethics):** apples always on white bg, oranges on black bg → the net learns **background, not fruit** → collapses out of distribution. A good rep must **ignore irrelevant variation** (position, scale, lighting, background, noise = **invariance**) and keep only task-relevant signal. *[St Cat's: don't let an "at-risk" model latch onto which campus/teacher instead of real engagement.]*
- 🔴 **Compact ≠ useful (the autoencoder notebook's thesis = reflection Q3 answer):** an autoencoder can **reconstruct** digits beautifully yet hand a classifier a latent space it can't separate - reconstruction optimises `p(x)`, not class separation. *"Has the model learned a **useful** representation, or only a **compact** one?"* → judge a rep **against its downstream task**, never by compression alone.
- 🔵 **Task-specific = same image, different task (class):** one face → **emotion** needs mouth/eyes/brow · **identity** needs stable bone structure · **age** needs skin texture · **head-direction** needs pose. Same data, different useful features → proof there is no absolute "best" rep.
- 🔵 **Salience is learned, not fixed:** MSE drops small features (ping-pong ball, ears); **GANs** *generate* them by redefining salience (Lotter 2015).
- 🔵 **Bengio's 3 families (the mental index):** **probabilistic models** (RBM/DBN, sparse coding) · **autoencoders** (Module 7) · **manifold learning** (PCA, Isomap, LLE).
- 🔵 **Zhong's timeline:** PCA 1901 → LDA 1936 → manifold 2000 → deep learning (Hinton 2006). *Deep learning is not a new idea* = feature-learning + big data + GPUs.
- 🔴 **The thesis sentence (= Activity 2 prompt, verbatim):** *"Feedforward and recurrent networks, autoencoders and deep probabilistic models all learn and exploit representations."*

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Deep Learning Final Project** · source code + 1500-word report · **group** · **40%** · due **19/08/2026** · SLOs **c) d) e)**.
> Module 9 feeds A3 directly: *"analyse the dataset, consider how best to represent input data, evaluate the impact of representation learning."* 🔴 **Tayab's pre-class reflection = your prep:** *how is your input represented, and could another representation make the task easier?*
> **Answer (Review Pulse):** today = **GloVe 100d embeddings → BiLSTM → one 512-d document vector** (document-level). A single vector **can't** separate *"camera great, battery terrible."* **ATAE-LSTM (v3.0.0)** appends an **aspect embedding** + aspect-conditioned attention → the *same sentence gets a different representation per aspect*. That is the Roman-numeral point applied: better encoding → easier task.
> 🔴 **Tayab mapped it live (Wk9 class):** the 5 rep-learning families = **CNN · RNN/LSTM · autoencoders · language models · GNN.** He said your project uses **approach 2 - RNN/LSTM** (sequential context + temporal patterns), and you *could* fold in **4 - language-model sentence embeddings** and **3 - autoencoder latent/compression.** Name-drop this mapping in the A3 report to show you placed your architecture in the taxonomy.

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

### This-week to-dos (actual post-class deliverables Tayab assigned Wk9)
- [ ] 🕐 **Forum reflection (≤100 words + 1 example):** pick one - *what makes a rep good* / *learned vs manual* / *reconstruct-well-but-unsuitable-for-classification*. Draft ready (TF-IDF→GloVe example); post it.
- [ ] 🕐 **Autoencoder-vs-PCA notebook:** run `DLE602_Module_09_..._Activity.ipynb`, fill the `LATENT_DIM` 2/4/8/16 table, answer the embedded questions + write the reflection (central Q: *useful or only compact?*).
- [ ] 🕐 **GenAI-critique activity (forum):** evaluate the claim *"representation learning is always better than manual feature engineering because neural nets discover the best features."* Attack **"always"** + **"best"** → dataset size, interpretability, bias/shortcuts, expert features still valuable.
- [ ] 🕐 **Design-a-solution activity (forum):** pick a problem (image/text/audio/time-series/graph) → raw input · info to preserve · irrelevant variation to ignore · suitable rep-learning model · expected latent rep · downstream task · **one limitation / ethical risk.**
