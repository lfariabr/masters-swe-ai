# DLE602 · Module 5 - One-Pager

> **Convolutional Neural Networks: the architecture built for grid data (images, audio, text windows)**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape, 4 zones).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **A CNN is just a neural network that swaps general matrix multiply for `convolution` in at least one layer. Loss, backprop and SGD are unchanged - only *which weights exist* changes.**
> (Goodfellow Ch.9. The win: a dense layer on a 256×256 image is intractable; convolution makes it routine.)

## 🖤 Zone 1 - Convolution + the 3 ideas ⭐ SLO a/c - THE GRADED CORE
- 🔵 **Convolution** = slide a small **kernel/filter** over the input, multiply-and-sum at each spot → a **feature map** that records *where* the feature fired. (Libraries skip the kernel flip = technically cross-correlation; the net learns the kernel either way.)
- 🖤 Use it when data has **grid topology**: 1D (text/time), 2D (images), 3D (video). *CNN = where in space · RNN = when in sequence.*

| Idea | What | Why it wins |
|---|---|---|
| **Sparse interactions** | kernel ≪ input; each output sees a small **receptive field** | fewer params/ops: `O(m×n)` → `O(k×n)`, `k ≪ m` |
| **Parameter sharing** | the **same** kernel weights reused at every position | learn one detector once, apply everywhere |
| **Equivariance** | shift input → feature map shifts the same way `f(g(x))=g(f(x))` | a feature is detectable in *any* location |

- 🔴 **Not** equivariant to scale/rotation - those need augmentation (← Module 4) or multi-filter pooling.

## 🖤 Zone 2 - Pooling = the invariance knob (§9.3)
- 🔵 **Pooling** replaces an output with a **summary statistic of its neighbours** - usually **max pooling** (the max in a rectangle). Think `GROUP BY window, MAX(activation)`.
- 🖤 **Payoff = approximate invariance to small translations:** you keep *that* a feature is present, deliberately discard exactly *where*. Shift the input a little → pooled output barely moves.
- 🔵 **Downsampling:** space the pooling regions `k` apart → fewer units → smaller, cheaper later layers. Also lets variable-size inputs feed a **fixed-size** classifier.
- 🖤 **Conv-layer pipeline:** `Convolution (linear) → ReLU → Pool → (often) Dense`. The ReLU `max(0,z)` comes *after* convolution; convolution alone has no nonlinearity.

## 🖤 Zone 3 - The landmark architectures ⭐ SLO c (Activity 2 = the narrative)
> **Story arc: deeper, then smarter/cheaper.** AlexNet (depth+GPU) → VGG (small-filter depth) → GoogleNet (width + 1×1 bottleneck) → ResNet (skip connections, 152 layers).

| Net | Year | Depth | Top-5 err | The one idea |
|---|---|---|---|---|
| **AlexNet** | 2012 | 8 (5c+3fc) | 15.3% | deep CNN + **GPUs** win; ReLU, **dropout**, augmentation; ~60M params |
| **VGG16** | 2014 | 16 | ~7.0% | stacks of small **3×3** filters; **but >500MB model** |
| **GoogleNet/Inception** | 2014 | 22 | **6.67%** 🏆 | **inception module** (1×1/3×3/5×5 parallel); **1×1 = bottleneck** to cut channels |
| **ResNet** | 2015 | 152 | - | **skip connections** make very-deep trainable |

- 🔴 **Activity 4 (compute vs memory):** VGG's **>500MB** model + AlexNet's **6-day, 2-GPU** train = your real-number evidence, not hand-waving. Every Module 4 regularizer (ReLU, dropout, weight decay, augmentation, early stop) shows up here *in production*.

## 🖤 Zone 4 - Training a CNN + transfer learning (Zhou + your own project)
- 🖤 **Two-phase loop:** forward (each layer **caches** what it needs) → backward (gradients chain). Clean contract: `backprop()` takes `∂L/∂out`, returns `∂L/∂in`. **Backprop unchanged from Module 2** - only the layer math differs.
- 🔵 **MaxPool** routes the gradient only to the **argmax** cell (rest = 0); **Conv** `∂L/∂filter = Σ ∂L/∂out · image`; SGD `w -= lr·grad` everywhere. NumPy-from-scratch MNIST hits **78%**, same net in Keras **~97.4%**.
- 🔴 **Transfer learning spectrum (Activity 3):** *feature-extraction* (freeze, reuse pretrained features, e.g. **GloVe** embeddings) ↔ *fine-tuning* (unfreeze + keep training, e.g. **DistilBERT**: freeze encoder → fine-tune last layers). **Little data → transfer learning** (avoid overfit); fine-tuning is cheap because early generic layers (edges/word-vectors) stay frozen.

## 🔴 Activity Prep - the 4 Module 5 forum/wiki tasks
- **Act 1 (Initial Rec):** *when CNN over FNN?* → grid data + features can appear anywhere (images, audio spectrograms, text windows). Lead with **sparse interactions + parameter sharing = far fewer params**.
- **Act 2 (Final Rec):** defend a choice using the **AlexNet→VGG→Inception** arc (bigger gives way to smarter/cheaper).
- **Act 3 (Train the Network, cats vs dogs):** forward/backward loop + SGD + lr/epochs + "start small then scale to Keras" + **transfer learning** from a pretrained backbone.
- **Act 4 (wiki Collaboration):** compute vs memory - use VGG >500MB / AlexNet 6-day numbers.

## 🔴 Assessment Hook (bottom red strip)
> **A1 is done (n-gram, due 28/06/2026).** Module 5 finally explains your A1 reference paper: **Zhao et al. (2018) GloVe-DCNN = a CNN over text** - convolution over embedding windows, parameter sharing, pooling. **Your own Review Pulse already proves the transfer-learning lesson:** on 1,159 test reviews, the **fine-tuned DistilBERT (88.6% F1)** beat the from-scratch BiLSTM+GloVe (80.3%) and the TF-IDF baseline (81.9%). Little data + fine-tuned pretrained = best → that's your A2/A3 story. *(A2 proposal due 26/07/2026 30%; A3 final due 19/08/2026 40%.)*

## 🔴 If you only memorise 5 things
1. **CNN = swap matrix-multiply for convolution in ≥1 layer.** Everything else (backprop, SGD) is the same.
2. **The 3 ideas:** sparse interactions · parameter sharing · equivariance to translation. *(This is the exam answer.)*
3. **Pooling = invariance knob** (keep *that* it fired, drop *where*); **convolution = equivariance/efficiency engine**.
4. **Architecture arc:** AlexNet (depth+GPU) → VGG (3×3 depth, huge) → Inception (width + 1×1 bottleneck) → ResNet (skip).
5. **Transfer learning:** little data → reuse a pretrained net; fine-tuning is cheap (freeze the generic early layers). *Your DistilBERT did exactly this.*

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Pooling is a `GROUP BY window, MAX(...)` - so what does the warehouse *lose* and *gain* by aggregating to the window grain? *(loses exact row/location, gains a smaller, shift-robust summary)*
2. Why is fine-tuning DistilBERT cheaper than training a CNN from scratch on the same reviews? *(early layers stay frozen = a reusable materialised view; you only retrain the top/head)*

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] Activity 1 - Initial Recommendation: when CNN over FNN (lead with the 3 ideas)
- [ ] Activity 2 - Final Recommendation: defend a choice via the architecture arc
- [ ] Activity 3 - Train the Network: cats-vs-dogs strategy + transfer learning
- [ ] Activity 4 - wiki Collaboration: compute vs memory (VGG >500MB, AlexNet 6-day)
- [ ] 🔥 finish Fernandes video - Ch.4 (CNNs) + Ch.5 (CNNs in Keras), then summarise
