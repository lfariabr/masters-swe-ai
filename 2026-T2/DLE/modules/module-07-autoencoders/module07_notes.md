# Module 07 — Autoencoders

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow et al. (2016) Ch.14 — autoencoder types, manifold learning, applications | ✅ |
| **2** | Read & summarise Baldi (2012) — theory of linear & Boolean autoencoders, clustering view | ✅ |
| **3** | Read & summarise Bengio (2012) — representation learning, greedy layer-wise, transfer learning | ✅ |
| **4** | Read & summarise Dickson (2020) — how deepfakes use two autoencoders | ✅ |
| 5 | Activity 1: Comparison — autoencoders vs linear factor models for dimensionality reduction | 🕐 |
| 6 | Activity 2: Fake to Real — an *ethical* deepfake application | 🕐 |
| 7 | Activity 3: Discussion — "Autoencoders may cause overfitting?" | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning — Chapter 14: Autoencoders.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning.* Cambridge, MA: MIT Press. Ch.14. https://www.deeplearningbook.org/

**Purpose:** The spine of the module. Defines the autoencoder, catalogues the regularized variants (sparse, denoising, contractive), explains *why* copying-the-input can still learn something useful (manifold learning), and lists the two production applications: dimensionality reduction and information retrieval.

---

#### 1. What an autoencoder is (and the one trap)
- **Definition:** a neural net trained to copy its input to its output through a bottleneck. Two parts: an **encoder** `h = f(x)` and a **decoder** `r = g(h)`. `h` is the **code**.
- **The whole point is *imperfect* copying.** If it learns `g(f(x)) = x` everywhere it is useless. It is deliberately restricted so it can only copy *approximately*, and only copy inputs that resemble the training data. Forced to prioritise, it learns useful structure.
- **Undercomplete** = code dimension `< input` dimension. This alone forces it to capture the most salient features.
- **The capacity trap:** give the encoder/decoder too much capacity and even an undercomplete AE can "cheat" — e.g. a powerful encoder maps each example to an integer index and the decoder maps back. It copies perfectly and learns nothing. *(This is the overfitting story for Activity 3.)*
- **Key link to Module 6:** a **linear** decoder + MSE loss makes the AE span the **same subspace as PCA**. A **nonlinear** encoder/decoder gives you a *nonlinear generalisation of PCA*. This is the single most important sentence connecting M6 → M7.

#### 2. The regularized autoencoder zoo
Rather than limiting capacity by keeping it shallow/small, add a term to the loss that demands another property. Now a nonlinear, even overcomplete, AE can still learn something useful.

| Variant | What is added | What it buys you |
|---|---|---|
| **Sparse AE** | penalty `Ω(h)` on the code (e.g. L1 / Laplace prior) → `L(x,g(f(x))) + Ω(h)` | few active units; features tuned to statistical structure; good for feature learning for another task |
| **Denoising AE (DAE)** | corrupt the input `x̃`, train to reconstruct clean `x` → `L(x, g(f(x̃)))` | must *undo* corruption, can't be identity; implicitly learns the structure of `p_data(x)` |
| **Contractive AE (CAE)** | penalise the Jacobian `Ω = λ‖∂f/∂x‖²_F` | features insensitive to small input changes; learns manifold tangent directions |

- **Sparse AE nuance:** unlike weight decay, the sparsity penalty has **no clean Bayesian/prior interpretation** because it depends on the *data*. Better read as approximating maximum likelihood of a latent-variable generative model where `log p_model(h)` is sparsity-inducing.
- **DAE geometry (the money insight):** the vector `g(f(x)) − x` learned by a DAE **estimates the score** `∇x log p_data(x)` — it points toward the nearest point on the data manifold. Denoising = learning which direction increases probability.
- **CAE vs DAE:** DAE makes the *reconstruction* resist finite-size perturbations; CAE makes the *encoder* resist infinitesimal ones. In the small-noise limit they coincide.

#### 3. Depth, manifolds, and why it all works
- **Depth pays** the same dividends as in any feedforward net (Ch.6.4.1): exponentially cheaper representation of some functions, exponentially less training data. Deep AEs compress far better than shallow/linear ones (Hinton & Salakhutdinov 2006).
- **Common training trick:** greedily pretrain a **stack of shallow autoencoders**, then compose — which is why you still meet shallow AEs even when the goal is deep.
- **Manifold learning is the unifying idea:** real data concentrates near a low-dimensional **manifold**. Training balances two opposing forces — (1) reconstruct the training examples, (2) satisfy the regularization/constraint (stay insensitive to off-manifold directions). The compromise makes `h` a **local coordinate system** for the manifold: sensitive along the manifold, insensitive orthogonal to it.

#### 4. Applications (Section 14.9)
- **Dimensionality reduction** — the first and original motivation. A 30-unit bottleneck AE beat PCA-to-30-dims on both reconstruction error and interpretability.
- **Information retrieval → semantic hashing:** train the AE to produce a **low-dimensional binary** code, store entries in a hash table keyed by that code. Retrieval = look up the same code; near-matches = flip a few bits. Extremely fast search.

#### Key Takeaways for DLE602 (Deep Learning)
1. **Activity 1 (AE vs linear factor models):** the killer line is *"an autoencoder with a linear decoder and MSE loss recovers PCA; the nonlinear autoencoder is a nonlinear generalisation of PCA."* AEs add: nonlinearity, learned (not hand-fixed) local dimensionality, and task-shaping via the regularizer choice (sparse/denoising/contractive).
2. **Activity 3 (overfitting):** *yes* — an unconstrained/overcomplete AE with too much capacity learns the identity (the "index each example" degenerate case). Regularization (sparse/denoising/contractive) is exactly the cure — this is Module 4 all over again, now on an unsupervised net (echoes Wang & Klabjan from M4).
3. **Bridge from Module 6:** linear factor models → autoencoders is the same "compress `x` into `h`" goal; M7 is where it goes nonlinear and deep. Module 9 (Representation Learning) is next.

---

### 2. Baldi, P. (2012). Autoencoders, Unsupervised Learning, and Deep Architectures.

**Citation:** Baldi, P. (2012). Autoencoders, unsupervised learning and deep architectures. *Proceedings of ICML Workshop on Unsupervised and Transfer Learning, PMLR 27*, 37–49. http://proceedings.mlr.press/v27/baldi12a/baldi12a.pdf

**Purpose:** The *theory* paper. Builds one mathematical framework (`n/p/n` autoencoder) that covers both linear and Boolean AEs, and reveals a surprising unifying claim: **all autoencoders are secretly doing clustering.**

---

#### 1. The general `n/p/n` framework
- An AE is defined by an **encoder** `B: Fⁿ → Gᵖ` and a **decoder** `A: Gᵖ → Fⁿ`, minimising distortion `Δ(A∘B(x), x)` over the training set. `p < n` is the **compression / feature-extraction** regime.
- Choose the sets/functions and you get every AE variant: `F=G=ℝ` with linear maps → **linear AE**; `F=G={0,1}` with Hamming distance → **Boolean AE** (the most extreme nonlinear case).

#### 2. The linear autoencoder = PCA (proven, not hand-waved)
- The squared-error landscape has **no local minima** — every critical point is a projection onto a subspace of eigenvectors of the data covariance `Σxx`.
- The **global minimum** is the projection onto the top-`p` eigenvectors = **PCA**. Every other critical point is a **saddle**.
- At the optimum the hidden activities are the dot products with the first `p` eigenvectors — i.e. the PCA coordinates. Ties the M6 covariance→eigenvector story to AEs rigorously.
- **Weight symmetry:** at the optimum `A = Bᵀ` (tied weights), consistent with a **Hebbian** learning rule.

#### 3. The Boolean autoencoder = clustering
- With unrestricted Boolean functions and Hamming distance, the optimal decoder maps each hidden code to a **centroid**, and the optimal encoder assigns each input to its **nearest centroid (Voronoi)** — this is literally **k-means-style clustering** into `2ᵖ` clusters.
- **Complexity:** in general Boolean AE learning is **NP-hard** (reduces to hypercube clustering); tractable only in special cases (fixed small `k`, or linear-over-ℝ).

#### 4. Composition & the big picture
- **Vertical composition (stacking):** the optimal deep AE can be built by training shallow AEs and composing — for linear, top-`p` projection = top-`p₁` then top-`p` projection; for Boolean, hierarchical clustering. This *justifies greedy layer-wise pretraining* mathematically.
- **Horizontal composition:** widen the hidden layer by training separate AEs (different inits/samples) and concatenating codes.
- **Unifying thesis:** *"Hebbian learning, autoencoders, and clustering are three faces of the same die."* Autoencoders also solve clustering **and** labelling at once — the hidden activity *is* the cluster label.
- **Information-theory framing:** `n>p` = compression (lossy if `m > k`); `n<p` with noise = a **noisy-channel coding** problem (linear codes as a special case).

#### Key Takeaways for DLE602 (Deep Learning)
1. **Reinforces the M6→M7 bridge with proof:** linear AE ≡ PCA *at the global optimum*. When Activity 1 asks "do AEs offer anything distinct from linear factor models?", the honest answer is "linearly, no — they *are* PCA; the value is entirely in nonlinearity, stacking, and clustering-with-labels."
2. **Explains the pretraining recipe** you'll see everywhere (stacked AEs / stacked RBMs) as vertical composition.
3. **Deepest single idea:** the fundamental unsupervised operation under deep architectures may just be **clustering**, composed hierarchically.

---

### 3. Bengio, Y. (2012). Deep Learning of Representations for Unsupervised and Transfer Learning.

**Citation:** Bengio, Y. (2012). Deep learning of representations for unsupervised and transfer learning. *Proceedings of ICML Workshop on Unsupervised and Transfer Learning, PMLR 27*, 17–36. http://proceedings.mlr.press/v27/bengio12a/bengio12a.pdf

**Purpose:** The *why-it-matters* paper and the direct link to your Review Pulse transfer-learning story. Winning writeup of the Unsupervised & Transfer Learning Challenge. Explains representation learning, the "zoo" of layer-wise algorithms, and how unsupervised features transfer to tasks with almost no labels.

---

#### 1. What a good representation is
- The goal: **disentangle the underlying factors of variation** — higher levels more abstract, individual features invariant to nuisances, collectively preserving the input's information.
- **Core transfer assumption:** the input distribution `P(x)` is structurally related to the task `P(y|x)`. Features that capture `P(x)` are *partly* useful for predicting `y`. This is what makes unsupervised pretraining pay off.
- **The challenge setup** was brutal: test classes barely appear in training, and the classifier gets only **1–64 labels per class**. So the representation had to be *generic* — pressure that favours abstract, deep features.

#### 2. Representations as coordinate systems (link to M6)
- **PCA is the linear ancestor** of manifold learning: project onto principal eigenvectors, measure quality by variance explained. But cutting low-variance directions as "noise" is dangerous — the **face identity vs pose** example: most pixel variance is *pose*; identity hides in *low-variance* components. Throwing away low variance can throw away the signal you want.
- Bengio's more ambitious alternative: don't hard-cut — learn to **separate the explanatory factors** and let the classifier pick the relevant ones.
- **Sparse overcomplete** representations often beat dense undercomplete (PCA-style) ones: the set of active units defines a **local chart / coordinate system**, and effective dimensionality can vary by region.

#### 3. The zoo of layer-wise unsupervised algorithms (Section 3)
The section the brief flags — each can be a layer in a deep stack:

| Algorithm | One-line mechanism | Relation to M6 / M7 |
|---|---|---|
| **PCA / ICA / normalization** | linear variance / independence; often used as first *and* last layer | Module 6 directly |
| **Auto-encoders** | reconstruct `x` from `g(h(x))`; nonlinear encoder → stackable, beats PCA | this module |
| **RBMs** | undirected energy model `P(x,h)=e^-energy/Z`; AE reconstruction-error gradient ≈ Contrastive Divergence | the "other" pretraining unit |
| **Denoising AE** | reconstruct clean from corrupted; error `(r(x̃)−x)²` ≈ score matching | robust, overcomplete-safe |
| **Contractive AE** | reconstruction + contraction penalty; keeps few sensitive directions = local dimension | soft, learned-dimension PCA |

- **Greedy layer-wise recipe:** train layer 1 unsupervised on `x`; train layer 2 on layer-1 codes; …; then optionally **supervised fine-tune** the whole stack. Fine-tuning helps most when you have *many* labels — with very few, keep a **low-dimensional top layer** (often a final PCA).

#### 4. Transfer learning results (the part that maps to your project)
- **Deep learners transfer better than shallow ones.** Stacked denoising AEs benefited more from out-of-distribution / multi-task training data than a shallow MLP.
- **Directly relevant to Review Pulse:** Glorot et al. (2011b), cited here, applied stacked denoising AEs with **sparse rectifiers to sentiment classification** (did a user like a product from a short review) for **domain adaptation**, beating the state of the art. That is *literally your task* one deep-learning generation earlier.
- **Practical tips worth stealing:** search learning rate in the **log domain** (start high, divide by 3 until training stops diverging); prefer **random search** over grid search; use **early stopping** on a validation criterion; top-layer dimensionality should track the number of classes.

#### Key Takeaways for DLE602 (Deep Learning)
1. **This is the academic backbone for your A2/A3 transfer-learning narrative.** "Unsupervised/self-taught features transfer when `P(x)` shares factors with `P(y|x)`" is the citable justification for using pretrained embeddings/DistilBERT on 1,159 reviews.
2. **A2/A3 methods menu, cited:** raw features vs PCA-reduced vs learned deep representations; random search for hyper-parameters; log-domain learning-rate tuning; early stopping.
3. **The honest caveat (great for Critical Analysis):** variance ≠ importance (face pose vs identity). A caution against blindly trusting PCA/undercomplete compression.

---

### 4. Dickson, B. (2020). What Is a Deepfake?

**Citation:** Dickson, B. (2020, 5 March). What is a deepfake? *PCMag Australia.* https://au.pcmag.com/news/65869/what-is-a-deepfake

**Purpose:** The fun, concrete payoff. Shows one real-world application of autoencoders — deepfakes — in plain language, and frames the ethics debate for Activity 2.

---

#### 1. How a deepfake uses autoencoders
- A deepfake uses an **autoencoder**: encoder compresses a face image to a small code; decoder reconstructs it. *Analogous to JPEG/MPEG codecs* — but it operates on **features** (eyes, nose, mouth, shapes, textures), not raw pixel groups.
- **The trick = two autoencoders + a swap.** Train AE-A on the **actor's** face and AE-B on the **target's** face — but **share the encoder**. At generation time, feed the actor's encoded expression into the **target's decoder**. Result: the target's face performing the actor's movements.
- Why it works: the shared encoder learns a **generic "face" code** (pose, expression); each decoder learned to render *one specific identity* from that code. Pure encoder/decoder representation transfer.

#### 2. Cost, quality, and the arms race
- **Democratised** what used to need a VFX studio — now a decent GPU (e.g. GTX 1080) or a few hundred dollars of cloud does it. But it's **not trivial/automatic**: thousands of cropped face frames from many angles, plus days-to-two-weeks of training.
- **Detection is cat-and-mouse:** early tells (unnatural blinking, skin-tone artefacts) keep getting fixed. Facebook/Microsoft's Deepfake Detection Challenge ($10M) and DARPA's media-forensics effort are the defensive side.

#### Key Takeaways for DLE602 (Deep Learning)
1. **Activity 2 (ethical deepfake):** the "two-autoencoders-share-an-encoder" mechanism is your technical grounding. Ethical framings that hold up: **voice/face restoration** for ALS or stroke patients, **historical/education** re-enactment with consent, **film dubbing** that syncs lips across languages, **privacy-preserving** face anonymisation in released datasets. Lead with consent + provenance.
2. **Concrete "autoencoder in the wild"** to cite when someone claims AEs have no real use — pairs well with Goodfellow's semantic-hashing and dimensionality-reduction applications.
3. **Ties to your day job framing:** an autoencoder here is a *feature-level* compressor — same idea as reducing 40 noisy student indicators to a handful of factors, just on face pixels.

---

## TL;DR (for the module)
- An **autoencoder** copies input → output through a bottleneck code `h`; the value is that it copies *imperfectly*, so it must learn the data's salient structure.
- **Linear AE + MSE = PCA** (Baldi proves the global optimum is the top-eigenvector projection); the win of AEs is the **nonlinear, deep, stackable** generalisation.
- **Regularized variants** shape what `h` keeps: **sparse** (few active units), **denoising** (reconstruct clean from corrupted — learns the data manifold / score), **contractive** (features insensitive to small input changes).
- Autoencoders learn a **local coordinate system on the data manifold**; deep/stacked AEs pretrain representations that **transfer** to new tasks with few labels (Bengio) — the academic backbone of your Review Pulse transfer story.
- **Applications:** dimensionality reduction, semantic-hashing retrieval, and **deepfakes** (two AEs sharing an encoder, swap decoders).
- **Overfitting warning:** an overcomplete AE with too much capacity learns the identity and nothing useful — regularization is the cure (Module 4, now unsupervised).
