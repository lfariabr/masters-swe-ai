# DLE602 · Module 6 - One-Pager

> **Linear Factor Models: discover a smaller set of hidden factors behind complex observed data**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape, 4 zones).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Observed data is often a noisy mixture of simpler hidden factors:** `x = Wh + b + noise`.
> Every model in this module changes what it wants the hidden representation `h` to preserve: variance, shared causes, independence, slowness, or sparsity. *(Goodfellow Ch.13)*

## 🖤 Draw the shared model across the centre
```text
 hidden factors h        mixing W + offset b         observed data x
[engagement, mastery]  -------------------------->  [Canvas, grades, attendance]
                                      + noise  ----> [measurement error / randomness]
```
- 🔵 **Latent variable `h`** = a factor we cannot observe directly but infer from patterns in `x`.
- 🔴 It is the **backstage of the data-generating process**, not the internal backstage of the algorithm.

## 🖤 Zone 1 - PCA: variance, direction, eigenvalues ⭐ SLO b/c
- 🔵 **Variance** = how spread out values are around their mean. More spread means the feature separates observations more strongly, but high variance can still be noise.
- 🖤 **PCA rotates the coordinate system** and finds the direction where the data cloud has maximum variance. It then projects the data onto the best directions.

```text
student data cloud           rotate axes             keep strongest axis
Canvas ↑       • •              ↗ PC1                 ●────●────●────●
       |    • •             ↗                           compressed data
       | • •        --->  PC2
       +------→ grades
```

| Term | Plain-English meaning |
|---|---|
| **Eigenvector** | the direction / weighted combination of original features |
| **Eigenvalue** | how much variance that direction captures |
| **Principal component** | each observation projected onto that direction |
| **Loading** | how strongly an original variable contributes to a component |

- 🔴 **Why direction?** In many dimensions, the useful pattern may be diagonal rather than aligned with one original column. Keep the largest eigenvalues to retain maximum spread with fewer dimensions.
- 🔴 **Limit:** PCA preserves geometry and variance, not meaning. Outliers or noise may dominate.

## 🖤 Zone 2 - PCA vs Factor Analysis vs ICA ⭐ Activity 1 core

| Model | The question it asks | Key condition | Use it when... |
|---|---|---|---|
| **PCA** | Which directions retain most variance? | orthogonal, uncorrelated components | compressing / visualising many correlated features |
| **Factor analysis** | Which hidden causes explain shared covariance? | latent Gaussian factors + variable-specific noise | inferring constructs like engagement or mastery |
| **ICA** | Which independent sources were mixed together? | independent, **non-Gaussian** sources | separating speakers, EEG signals, interference |

- 🔵 **Uncorrelated ≠ independent.** Independence is stronger: two variables may have zero linear correlation but still depend on each other nonlinearly.
- 🔴 **When ICA over PCA?** Choose ICA when observations are linear mixtures of hidden non-Gaussian sources and you need to **recover the sources**, not merely reduce dimensions.
- 🔵 **Cocktail party:** microphones observe mixed voices `x`; ICA estimates each original speaker `h` without being told the mixing weights.

## 🖤 Zone 3 - SFA and Sparse Coding

| Model | What `h` should do | Anchor | Main trade-off |
|---|---|---|---|
| **SFA** | change slowly over time | pixels change fast; object identity stays stable | slowness may suppress useful fast-changing features |
| **Sparse coding** | use only a few active basis features | image = a few edges/textures | strong codes, but optimisation is needed for every input |

- 🔵 **SFA objective:** minimise change between `h(t)` and `h(t+1)`. Constraints: zero mean, unit variance, decorrelation. Without them, every feature could collapse to the same constant.
- 🔵 **Sparse objective:** `reconstruction error + λ||h||₁`. L1 pushes many activations to exactly zero; larger `λ` = sparser code.
- 🖤 **Dictionary:** learned basis vectors such as edges or textures. The code says which few basis vectors reconstruct the input.
- 🔴 Module 4 link: L1 regularised **weights** there; here L1 regularises the **latent code** to select active features.

## 🖤 Zone 4 - Why this belongs in Deep Learning ⭐
- 🖤 **Linear factors are shallow representation learning:** convert high-dimensional `x` into a simpler `h`.
- 🔵 **Manifold view:** PCA fits a flat low-dimensional surface through high-dimensional data. Real-world structure is often curved and nonlinear.
- 🖤 **Bridge:** `linear encoder + linear decoder` → add nonlinear layers → **autoencoder** (Module 7) → stack representations → deep learning.
- 🔴 **"Deep" means multiple learned nonlinear transformations**, not that latent variables themselves are deep.
- 🔵 **Review Pulse spectrum:** TF-IDF uses explicit features; GloVe transfers dense word representations; DistilBERT learns contextual nonlinear representations. PCA/sparse coding are useful baselines, not replacements for context.

## 🔴 Activity Prep - Module 6 forums
- **Act 1 Comparison (≤150 words):** ICA over PCA = independent non-Gaussian source recovery vs maximum-variance compression.
- **Act 2 Idea Generation:** NLP = compress embeddings/topics; speech = ICA speaker/noise separation; vision = PCA compression, SFA stable identity, sparse edge features.
- **Act 3 Open Forum:** ask: *Does a latent factor represent a real cause, or only a useful statistical explanation?*

## 🔴 Assessment Hook (bottom red strip)
> **A2 Deep Learning Project Proposal Presentation** · 1000 words +/-10% + 5-7 min · 30% · due **26/07/2026** · SLOs **b/c/d/e**.
> Module 6 helps justify preprocessing, representation choice, and interpretable baselines for Review Pulse v2. **A3 Final Project** · source code + 1500 words +/-10% · 40% · due **19/08/2026** · SLOs **c/d/e**. A strong experiment can compare raw embeddings, PCA-reduced embeddings, and fine-tuned transformer representations using accuracy/F1, dimensionality, and compute cost.

## 🔴 If you only memorise 5 things
1. **One equation:** `x = Wh + b + noise` - observations are mixtures of hidden factors.
2. **PCA = maximum variance; Factor Analysis = hidden shared causes; ICA = independent sources.**
3. **Eigenvector = direction; eigenvalue = variance captured in that direction.**
4. **SFA wants slow features; sparse coding wants few active features.**
5. **Linear factors are the bridge to autoencoders:** same representation goal, but deep models learn nonlinear layers.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. If grades, attendance, Canvas activity, and submissions move together, what latent factors might explain them? Which claims would still require evidence? *(engagement/mastery are hypotheses, not proven causes)*
2. If PCA compresses 40 student indicators into 5 components, what is gained and lost? *(gain: speed, less redundancy; loss: original-column meaning and possibly low-variance signal)*

### This-week to-dos (still 🕐 in your notes)
- [ ] Activity 1 - write the ≤150-word ICA vs PCA comparison
- [ ] Activity 2 - propose NLP, speech, and vision applications using factor models
- [ ] Activity 3 - post one precise latent-variable question to the open forum
- [ ] From memory, explain `variance → eigenvector → eigenvalue → principal component`
