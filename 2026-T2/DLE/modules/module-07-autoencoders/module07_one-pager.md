# DLE602 · Module 7 - One-Pager

> **Autoencoders · encoder/decoder bottleneck · undercomplete = PCA · sparse / denoising / contractive · manifold learning · stacking & transfer · deepfakes**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **An autoencoder is trained to copy its input to its output - and the *only* reason it is useful is that it copies *badly*.**
> Squeeze `x` through a bottleneck code `h`, and the network must decide what to keep and what to throw away. That decision *is* the learned representation.
> (Goodfellow, Bengio & Courville 2016, Ch.14 · Baldi 2012)

```
        x  ──►  encoder f  ──►   h   ──►  decoder g  ──►  r ≈ x
     (input)                  (CODE)                  (reconstruction)
                                │
                                └── the ONLY part you keep; the decoder is scaffolding
```

---

## 🖤 Zone 1 - The anatomy + the one trap
- 🖤 **Encoder** `h = f(x)` · **Decoder** `r = g(h)` · loss `L(x, g(f(x)))`.
- 🔵 **Undercomplete** = `dim(h) < dim(x)` → forced compression → must learn salient features.
  **Overcomplete** = `dim(h) ≥ dim(x)` → free capacity → *dangerous without a regularizer*.
- 🔴 **THE CAPACITY TRAP (memorise this):** give `f`/`g` too much capacity and the AE learns the **identity function** - in the degenerate case the encoder maps example #i to the integer `i` and the decoder maps it back. **Perfect reconstruction, zero learning.**
- 🔴 That trap *is* the answer to Activity 3: **yes, autoencoders may cause overfitting** - and regularization is the cure (Module 4, now unsupervised).

## 🖤 Zone 2 - Undercomplete linear AE = PCA ⭐ SLO c) - THE GRADED CORE
- 🖤 **Claim (state it with the conditions or you lose the mark):** an **undercomplete** AE with **linear** encoder/decoder and **squared-error (MSE)** loss recovers the **PCA subspace** at its global optimum.
- 🔵 **Baldi (2012) proves it** in the `n/p/n` framework (`B: Fⁿ→Gᵖ` encoder, `A: Gᵖ→Fⁿ` decoder, `p < n`):
  - the squared-error landscape has **no local minima**;
  - every critical point = projection onto some eigenvector subspace of `Σxx`;
  - the **global min = projection onto the top-`p` eigenvectors = PCA**; all others are **saddles**.
  - Tied weights `A = Bᵀ` (Hebbian flavour) hold *under the coordinate choice `C = I`* - the solution is otherwise invariant to any invertible `C`.
- 🔵 **Boolean AE (`F=G={0,1}`, Hamming) = clustering:** decoder → centroids, encoder → nearest-centroid (Voronoi) assignment into `2ᵖ` clusters. NP-hard in general.
- 🖤 Baldi's thesis: *"Hebbian learning, autoencoders and clustering are three faces of the same die."*
- 🔴 **Activity 1 killer line:** *"Linearly, an autoencoder offers nothing distinct - it **is** PCA. The distinct value is entirely in the **nonlinear, deep, stackable** generalisation, plus the ability to shape `h` by choosing the regularizer."*

## 🖤 Zone 3 - The regularized zoo (what forces `h` to be useful)
Instead of limiting capacity, add a term to the loss demanding another property. Now even an **overcomplete nonlinear** AE learns something real.

| Variant | Objective | What it buys | Failure it prevents |
|---|---|---|---|
| **Sparse AE** | `L(x, g(f(x))) + Ω(h)` (L1 / Laplace) | few active units; interpretable, feature-selecting code | dense uninformative codes |
| **Denoising AE (DAE)** | `L(x, g(f(x̃)))` - corrupt `x̃`, rebuild clean `x` | robustness; implicitly learns `p_data(x)` structure | identity function (can't just copy - the copy is broken) |
| **Contractive AE (CAE)** | `L + λ‖∂f/∂x‖²_F` (Jacobian penalty) | encoder insensitive to tiny input wiggles; learns manifold **tangent** directions | over-sensitivity to noise directions |

- 🔵 **DAE money insight:** under **Gaussian corruption + squared-error loss**, the learned vector `g(f(x)) − x` estimates the **score** `∇x log p_data(x)` (up to a noise-dependent scale). Plain English: *denoising teaches the net which direction points back toward real data.*
- 🔵 **DAE vs CAE - regularize different objects:** DAE hardens the **reconstruction** against *finite* perturbations; CAE hardens the **encoder** against *infinitesimal* ones. Related under small-noise assumptions (Alain & Bengio 2013), **not** universally identical.
- 🔵 **Sparse-AE nuance:** the sparsity penalty has **no clean Bayesian prior** interpretation (it depends on the data) - read it as approximating ML of a latent-variable model with a sparsity-inducing `log p_model(h)`.

## 🖤 Zone 4 - Manifolds, depth & transfer (why anyone bothers)
- 🖤 **Manifold learning is the unifying idea:** real data concentrates near a low-dimensional surface. Training balances two opposing forces:
  ```
  (1) reconstruct the training points   ⇄   (2) obey the regularizer / stay insensitive
        (sensitive ALONG the manifold)          (insensitive ORTHOGONAL to it)
  ```
  The compromise makes `h` a **local coordinate system on the manifold**.
- 🔵 **Depth pays:** deep AEs compress far better than shallow/linear (Hinton & Salakhutdinov 2006). **Greedy layer-wise pretraining** = train shallow AEs, stack them, then optionally fine-tune. Baldi's **vertical composition** is the mathematical justification.
- 🔵 **Bengio (2012) - the transfer assumption:** unsupervised features help because **`P(x)` is structurally related to `P(y|x)`**. Deep learners transfer better than shallow ones; with 1-64 labels per class, the representation must be *generic*.
- 🔴 **Bengio's honest caveat (gold for Critical Analysis):** **variance ≠ importance.** In face images most pixel variance is *pose*; **identity hides in low-variance components**. Cutting low-variance directions (PCA-style) can throw away exactly the signal you want.
- 🔵 **Practical tips worth stealing:** search learning rate in the **log domain**; **random search > grid search**; **early stopping**; top-layer dimensionality should track the number of classes.

## 🖤 Zone 5 - Applications (the concrete payoff)
🔴 *Dr Tayab's week-7 email names four: **image denoising · anomaly detection · data compression · deepfake generation**. Note that **anomaly detection is NOT in Goodfellow Ch.14's applications section** - it is lecturer-added, so it will come from the lecture, not the reading.*

| Application | Mechanism (one line) | Source |
|---|---|---|
| **Data compression / dim. reduction** | keep `h`, drop the decoder; 30-unit bottleneck AE beat PCA-to-30 on reconstruction *and* interpretability | Goodfellow 14.9 |
| **Image denoising** | the **DAE trained as a product, not a trick**: feed a grainy/corrupted image, output the clean one | Goodfellow 14.5 · lecture |
| **Anomaly detection** ⚠️ | train the AE on **normal data only** → it reconstructs normal well, anomalies badly → **reconstruction error `‖x − g(f(x))‖²` IS the anomaly score**; threshold it | **lecture only - not in Ch.14** |
| **Information retrieval / semantic hashing** | AE emits a **low-dim binary** code used as a **hash-table key**; near-matches = flip a few bits → extremely fast search | Goodfellow 14.9 |
| **Deepfake generation** | **two AEs that SHARE an encoder**; swap the decoders | Dickson 2020 |

- 🔵 **Why anomaly detection works (be able to say this):** the AE only ever learned the manifold of the *normal* data, so an off-manifold input has **no good code** - the reconstruction fails, and the size of that failure is the signal. Same logic as the manifold picture in Zone 4, used as a detector.
- 🔵 **Deepfakes (Dickson 2020) in detail:** train decoder-A on the actor, decoder-B on the target, **shared encoder**; at generation time feed the actor's code into the **target's decoder**. The shared encoder learns a generic "face" code (pose/expression); each decoder renders one identity. *2020-era cost per Dickson: a GTX-1080-class GPU or a few hundred dollars of cloud, thousands of cropped frames, days-to-two-weeks of training.*
- 🔴 **Ethical deepfake angles for Activity 2:** voice/face restoration for ALS or stroke patients · consented historical/educational re-enactment · cross-language film dubbing with lip sync · **privacy-preserving face anonymisation in released datasets**. Lead with **consent + provenance**.

---

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 2 - Deep Learning Project Proposal Presentation** · 1000-word report ±10% + 5-7 min presentation · **group, 30%** · due **26/07/2026** · SLOs **b) c) d) e)**
> **Assessment 3 - Deep Learning Final Project** · source code + 1500-word report ±10% · **group, 40%** · due **19/08/2026** · SLOs **c) d) e)**
>
> Module 7 is where you **identify possible uses of autoencoders and possible input datasets, particularly for A3**. Concretely: **Bengio (2012) is the citable justification for your Review Pulse transfer-learning story** - and he cites **Glorot et al. (2011b)**, who used **stacked denoising autoencoders with sparse rectifiers for domain adaptation in sentiment classification**. That is literally your task, one deep-learning generation earlier. Cite it in the A2 literature/method section.
>
> 🔴 **Dr Tayab (week-7 email) widens the A2 hook:** this module supports Assessment 2 if your project involves **feature extraction, dimensionality reduction, image processing, or representation learning**. Review Pulse hits **feature extraction + representation learning** - so the M7 material belongs in the A2 proposal, not just A3.

## 🔴 If you only memorise 5 things
1. **An autoencoder is only useful because it copies badly.** Bottleneck or regularizer - something must break the copy, or it learns the identity.
2. **Undercomplete + linear + MSE ⇒ PCA** (Baldi: global optimum = top-`p` eigenvectors, no local minima, everything else a saddle). The value of AEs = the **nonlinear, deep, stackable** generalisation.
3. **The zoo, in one line each:** sparse = *few units fire*; denoising = *rebuild clean from corrupted* (learns the score / manifold); contractive = *ignore tiny input wiggles* (Jacobian penalty).
4. **`h` is a local coordinate system on the data manifold** - sensitive along it, insensitive orthogonal to it. Depth + stacking is what makes those coordinates transfer. **Anomaly detection is this idea weaponised:** train on normal only, and **reconstruction error = anomaly score**.
5. **Yes, AEs can overfit** (identity-function trap, overcomplete + high capacity) - and **variance ≠ importance** (face pose vs identity). Both are "critical analysis" marks waiting to be collected.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your student data warehouse has ~40 correlated indicators per student (attendance, grades, logins, incidents). A **linear** AE on them gives you PCA - nothing new. What would a **denoising** AE add that PCA cannot, given how noisy and partially-missing those columns actually are?
2. **Anomaly detection, your version:** train an AE on **only** the "normal" nightly ETL rows, then flag any row whose reconstruction error blows past a threshold. How is that different from - and better than - the hard-coded validation rules you write today?
3. **Semantic hashing** = a learned binary code used as a hash key. How is that different from the composite index / surrogate key you already build in SQL - and where would a *learned* key ("find me students who look like this one") beat an *exact* key?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🔴 **PRE-CLASS (Dr Tayab):** come ready to *verbally* discuss - **"How is an autoencoder different from PCA? Both reduce dimensionality, so what additional capability does an autoencoder provide?"** No written response required. → **Zone 2 is your answer**: linear+undercomplete+MSE ⇒ it *is* PCA; the extra capability is **nonlinearity, depth/stacking, and a learned regularizer that shapes what `h` keeps**.
- [ ] 🕐 **Activity 1 - Comparison** (≤150 words): do autoencoders offer anything distinct from linear factor models for dimensionality reduction? *Open with the linear-AE = PCA equivalence, then pivot to nonlinearity + stacking + regularizer choice.* (Same question as the pre-class prompt - kill two birds.)
- [ ] 🕐 **Activity 2 - Fake to Real** (≤150 words): an **ethical** deepfake application, with the scientific/technical mechanism (two AEs, shared encoder, swapped decoders).
- [ ] 🕐 **Activity 3 - Discussion Forum**: *"Autoencoders may cause overfitting?"* - agree, cite the identity-function/overcomplete trap and name regularization (sparse/denoising/contractive) as the cure.
