# Module 09 — Representation Learning

## TL;DR
- **A good representation is one that makes the next task easier** - always defined *relative to a downstream task*, never absolutely (Goodfellow Ch.15). The Roman-numeral test: `210 ÷ 6` is easy, `CCX ÷ VI` is not - same numbers, different encoding.
- **Supervised nets already do representation learning** as a side effect: everything before the final linear/softmax layer exists to hand it a linearly separable representation.
- **Greedy layer-wise unsupervised pretraining** (§15.1, the assigned deep-dive) trained the first deep nets in 2006. That specific 2006 procedure is now **largely historical**; its descendant - **modern self-supervised pretraining** (word2vec/GloVe → BERT, and SSL in vision) - is very much alive across *both* language and vision.
- **Four load-bearing ideas:** unsupervised/self-supervised pretraining · transfer learning & domain adaptation (Goodfellow's own example is books→electronics *sentiment* - the Review Pulse setup) · disentangling causal factors · **distributed representations** (`n` features → `kⁿ` concepts; `O(nᵈ)` regions vs `O(n)` for one-hot/k-means/kNN).
- **Bengio et al. (2013)** unifies the field into three families - **probabilistic models, autoencoders, manifold learning**. **Zhong et al. (2016)** gives the timeline (PCA 1901 → LDA 1936 → manifold 2000 → deep 2006): *deep learning is not a new idea*, it is feature-learning + big data + GPUs.
- **A rep can reconstruct well yet be useless for the task** - *compact ≠ useful* (the live-class autoencoder-vs-PCA point, and the answer to reflection Q3). Always evaluate a representation **against its downstream task**, and beware **shortcut features** (learning the *background* instead of the object).
- **The unifying thesis** (Ch.15 last line, = Activity 2 prompt): *"Feedforward and recurrent networks, autoencoders and deep probabilistic models all learn and exploit representations."*

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow, Bengio & Courville (2016) — *Deep Learning* Ch.15 (Representation Learning) | ✅ |
| **2** | Read & summarise Bengio, Courville & Vincent (2013) — *Representation Learning: A Review and New Perspectives* | ✅ |
| **3** | Read & summarise Zhong, Wang, Ling & Dong (2016) — *An Overview on Data Representation Learning* | ✅ |
| **4** | Read & summarise Ghosh (2019) — *Representation Learning: A Review and Perspectives* (Medium synthesis) | ✅ |
| 5 | **Forum reflection** (≤100 words + example): pick one — *what makes a rep good* / *learned vs manual* / *reconstruct-well-but-unsuitable-for-classification* | 🕐 |
| 6 | **Autoencoder-vs-PCA notebook** (`DLE602_Module_09_..._Activity.ipynb`): run it, fill the `LATENT_DIM` 2/4/8/16 table, answer embedded Qs + write reflection | 🕐 |
| 7 | **GenAI-critique** (forum): evaluate "representation learning is *always* better than manual feature engineering" — attack *always* / *best* (data size, interpretability, bias/shortcuts) | 🕐 |
| 8 | **Design-a-solution** (forum): pick image/text/audio/time-series/graph → raw input · preserve · ignore · rep model · latent rep · downstream task · one ethical risk | 🕐 |

---

## Live Class Notes (Wk 9, Tayab) — what the lecture added beyond the readings

*Class recording 29 Jul 2026 (1h12). Framing question: "How can a neural network learn the most useful way to represent data?" These five points are the parts of the live lecture the four readings did **not** already cover.*

1. **Representation = a way of encoding data for a model, and the same data has many.** image→pixels · word→numerical vector · audio→waveform/spectrogram · customer→behavioural features · face→learned facial features · graph node→embedding. *Which* encoding you pick is decided by the task.
2. **Task-specific: same image, different task, different features.** One face → **emotion** needs mouth/eyes/eyebrow · **identity** needs stable facial structure · **age** needs skin texture · **face direction** needs head pose. Proof there is no absolute "best" representation — only best *for a task*.
3. **Shortcuts / spurious features (ethics, SLO d).** Classify apples vs oranges where every apple is on a white background and every orange on black → the model learns the **background**, not the fruit, and fails to generalise. A good rep must show **invariance** — stay stable under position, scale, lighting, background, minor noise — and keep only task-relevant signal.
4. **Compact ≠ useful (the notebook's central question).** The autoencoder-vs-PCA activity's thesis: *"Has the model learned a useful representation, or only a compact one?"* Good **reconstruction** optimises `p(x)`; it does **not** guarantee a latent space a classifier can separate. Don't over-compress the bottleneck to the point the input can't be reproduced. → this is exactly **reflection Q3**.
5. **Live A3 mapping (do use this in the report).** Tayab's five rep-learning families = **CNN · RNN/LSTM · autoencoders · language models · GNN.** He told the group **Review Pulse uses approach 2 — RNN/LSTM** (sequential context + temporal patterns) — and *could* fold in **4 — language-model sentence embeddings** and **3 — autoencoder latent/compression.** Transfer learning framed as the norm now: *"reuse learned features and fine-tune for a new task instead of training from scratch"* (cost is the driver).

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Ch. 15 — Representation Learning.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning* (Ch. 15). Cambridge, MA: MIT Press. https://www.deeplearningbook.org/contents/representation.html

**Purpose:** The spine of the module. Defines what a *good* representation is, why supervised nets already do representation learning as a side effect, and lays out the four load-bearing ideas — unsupervised pretraining, transfer learning, disentangling causal factors, and distributed representations — that tie every deep-learning architecture in the course together.

---

#### 1. What is a "good" representation? (the framing)
- **The Roman-numeral test.** `210 ÷ 6` is trivial in Arabic numerals, near-impossible in `CCX ÷ VI`. Same information, different *representation* — the task is easy or hard depending on how the data is encoded. This is the whole chapter in one image.
- **Operational definition:** *a good representation is one that makes a subsequent learning task easier.* It is always defined **relative to the downstream task** — there is no context-free "best" representation.
- **Day-job hook (St Cat's):** the same student record is easy or hard to work with depending on how you represent it - raw Synergetic tables vs the shaped **Student 360** profile, or a hand-thresholded "at-risk" SQL flag vs a learned low-dimensional engagement vector. The representation you choose decides how hard the next question is to answer.

#### 2. Supervised nets already do representation learning
- A feedforward net trained by supervised learning = **representation learning in disguise**. The last layer is a linear (softmax) classifier; **everything before it exists to hand that classifier a linearly separable representation.**
- Classes not linearly separable in the raw input often *become* linearly separable in the last hidden layer.
- **Key distinction:** supervised training imposes *no explicit* condition on the intermediate features — they are shaped implicitly by the loss. Other algorithms (sparse coding, autoencoders) are *explicitly* designed to shape the representation (independence, sparsity, reconstruction).
- **The core trade-off (recurs everywhere):** preserve as much information about the input as possible **vs.** attain nice properties (independence, sparsity, low dimension). You cannot max both.

#### 3. §15.1 — Greedy Layer-Wise Unsupervised Pretraining (the assigned deep-dive)
- **What it is:** train a deep net **one layer at a time**, each layer via an unsupervised single-layer learner (RBM, single-layer autoencoder, sparse coding), freezing lower layers, then optionally **fine-tune** the whole stack with a supervised objective.
- **Why the three words:**
  - **Greedy** — optimises each layer independently, not jointly.
  - **Layer-wise** — the independent pieces are the layers; lower layers are fixed once trained.
  - **Pretraining** — it is only phase 1; a supervised fine-tune usually follows.
- **Historical weight:** this is the trick (Hinton et al., 2006) that *started the 2006 deep-learning renaissance* — the first way to train deep fully-connected nets before ReLU / dropout / batch-norm existed. It acts as **both a regulariser and a parameter initialisation.**

| | Greedy layer-wise pretraining (2006) | Modern supervised (ReLU + dropout + batchnorm) |
|---|---|---|
| When it wins | tiny labelled set, huge unlabelled set, poor initial representation (words!) | medium-to-large labelled sets (CIFAR-10, MNIST) |
| Status today | **the exact 2006 procedure is largely historical** | dominant for direct supervised tasks |
| Mechanism | learns input distribution `p(x)` first, one frozen layer at a time | learns `p(y\|x)` directly |

- **When/why it works (§15.1.1):** two ideas fused — (1) initialisation has a **regularising** effect (Erhan et al., 2010: pretrained nets consistently halt in the same, smaller region of function space → reduced variance); (2) features useful for modelling `p(x)` are often useful for `p(y|x)`. Most helpful when **labelled data is scarce, unlabelled data is abundant, and the true function is complicated.**
- **Historical vs modern — the distinction that matters:** the *specific 2006 greedy layer-wise* procedure Goodfellow calls "largely abandoned" *is* mostly historical. But its idea — **pretrain a representation on unlabelled data, then fine-tune** — did not die; it evolved into **modern self-supervised pretraining**, which is dominant across *both* language (word2vec / GloVe → BERT, DistilBERT) *and* vision (contrastive/masked SSL). One-hot word vectors carry *zero* similarity info (every pair is √2 apart); learned embeddings encode similarity by distance — which is why words were the first domain where pretraining decisively won and never left.

#### 4. §15.2 — Transfer learning & domain adaptation
- **Transfer learning:** exploit what was learned under distribution `P₁` to generalise better under `P₂`. Works when the two tasks share underlying factors (edges, shapes, lighting for vision). Deeper representations → fewer labelled examples needed in the transfer setting.
- **Domain adaptation:** *same task, shifted input distribution.* The textbook's own example is **sentiment analysis trained on book / DVD / music reviews then applied to electronics reviews** — denoising-autoencoder pretraining handles this well (Glorot et al., 2011). *(This is literally the Review Pulse multi-domain Amazon setup — see the Module 8 bridge doc.)*
- **Concept drift** = transfer learning across *time* (distribution drifts gradually).
- **One-shot learning** (1 labelled example) works because the representation *already cleanly separated the classes* beforehand — one example is enough to label the cluster. **Zero-shot / zero-data learning** (0 examples) needs *more*: on top of a clean representation, it requires **task information `T` and a shared semantic representation** across modalities (e.g., recognising a cat from having *read* "cats have four legs and pointy ears"). That shared space is what enables **multimodal** anchoring (image ↔ word).

#### 5. §15.3 — Disentangling causal factors (what makes a representation *good*, deeper answer)
- **Central hypothesis:** an ideal representation has features that correspond to the **underlying causes** of the data, with separate directions for separate causes — it *disentangles* them.
- If `y` is one of the salient causes of `x`, then modelling `p(x)` reveals `y` almost for free (the mixture-model figure): unsupervised learning of `p(x)` **helps** supervised `p(y|x)` — the theoretical justification for semi-supervised learning. When `p(x)` is uninformative about `y` (uniform `x`), it does **not** help.
- **Salience is learned, not fixed:** MSE-trained models drop small-but-meaningful features (the ping-pong ball; the ears on a face). **GANs** redefine salience — any pattern the discriminator can recognise becomes salient — so they *generate* the ears that an MSE loss omits (Lotter et al., 2015, predictive generative networks). Note this is generation/prediction, not autoencoder-style reconstruction of the input.
- **Causal bonus (Schölkopf et al., 2012):** modelling `p(x|cause)` is robust to shifts in `p(cause)` — good for domain shift and non-stationarity ("the laws of the universe are constant").

#### 6. §15.4 — Distributed representations (the big statistical-efficiency argument)
- **Distributed:** many features set independently → `n` features with `k` values describe `kⁿ` concepts. Each direction in representation space = one underlying factor.
- **Symbolic / one-hot / non-distributed:** input → a single symbol; `n` symbols carve only `n` regions.

| | Distributed | Non-distributed (one-hot / local) |
|---|---|---|
| Regions from `n` params in `Rᵈ` | `O(nᵈ)` (exponential in `d`) | `O(n)` (linear) |
| Examples | neural nets, RBMs, sparse coding, word embeddings | k-means, kNN, decision trees, Gaussian mixtures, n-grams |
| Generalisation | via **shared attributes** ("cat" & "dog" share `has_fur`) | only **local** (smoothness prior) → curse of dimensionality |

- **Why it generalises without overfitting:** even though it distinguishes exponentially many regions, capacity stays bounded — VC-dimension of linear-threshold nets is only `O(w log w)`. A powerful representation + a *weak* linear classifier = a strong regulariser.
- **Empirical payoff (Radford et al., 2015):** face-generating nets learn directions where `man-with-glasses − man-without-glasses + woman-without-glasses = woman-with-glasses`. Gender and glasses are disentangled directions, discovered with **no labels** — the same vector-arithmetic property as word2vec `king − man + woman = queen`.

#### 7. §15.5–15.6 — Depth and the generic priors
- **Exponential gains from depth:** functions representable by a depth-`k` net can need an *exponential* number of units at depth 2 or `k−1`. Depth = **feature re-use through composition** (each path re-uses sub-features), buying statistical efficiency on top of the distributed-representation efficiency.
- **The generic priors** deep learning bets on (the closing list — good exam fodder): **smoothness, linearity, multiple explanatory factors, causal factors, depth/hierarchy, shared factors across tasks, manifolds, natural clustering, temporal/spatial coherence, sparsity, simplicity of factor dependencies.**
- **The chapter's thesis sentence:** *"Feedforward and recurrent networks, autoencoders and deep probabilistic models all learn and exploit representations."* — this is **verbatim the prompt for Activity 2.**

#### Key Takeaways for DLE602
1. **Activity 2 is answered on the last page of this chapter** — the statement to critique is Goodfellow's own concluding sentence. Agree, with the four families as evidence: FF nets (implicit, via the loss), RNN/LSTM (Module 8, representations over time), autoencoders (Module 7, explicit reconstruction), deep probabilistic models (RBMs/DBNs, latent factors). Representation learning is the *unifying* lens over the whole course.
2. **Direct line to your Review Pulse work:** GloVe embeddings = the learned distributed representation §15.1 says is *the* reason pretraining survived in NLP; DistilBERT = supervised / self-supervised pretraining + transfer; the books→electronics **domain-adaptation sentiment example is Goodfellow's own**, not a coincidence with your multi-domain Amazon dataset.
3. **Links back:** distributed representations (§15.4) explain *why* embeddings beat one-hot (Module 3 NLP); depth (§15.5) re-justifies CNNs (Module 5) and deep nets (Module 2); autoencoders (Module 7) are the §15.1 single-layer learner.

---

### 2. Bengio, Y., Courville, A. & Vincent, P. (2013). Representation Learning: A Review and New Perspectives.

**Citation:** Bengio, Y., Courville, A. & Vincent, P. (2013). Representation learning: A review and new perspectives. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 35*(8), 1798–1828. https://arxiv.org/abs/1206.5538

**Purpose:** The canonical survey that Goodfellow Ch.15 condenses and Ghosh's blog re-tells. Its contribution is a **taxonomy**: it unifies three "apparently disconnected" approaches — probabilistic models, autoencoders, and manifold learning — and frames the whole field around three driving questions.

---

#### 1. The three driving questions
- **What makes one representation better than another?** → the priors + disentangling answer.
- **How do we compute a representation (inference)?** → a cheap feed-forward encoder vs an expensive posterior computation.
- **What are the right objectives for learning good representations?** → the open problem: unlike classification, the training target is *far removed* from the ultimate goal (analogous to the credit-assignment problem in RL).

#### 2. Three families, unified

| Family | Representation defined by | Cost / catch |
|---|---|---|
| **Probabilistic models** (directed: sparse coding, PCA; undirected: RBM, DBM) | posterior `p(h\|x)` over latent variables | inference often **intractable**; the RBM's factorises so it *is* tractable |
| **Autoencoders** (sparse, denoising, contractive) | a directly-learned **parametric encoder** `f(x)` | cheap forward pass; needs regularisation to avoid learning the identity |
| **Manifold learning** (PCA, Isomap, LLE) | low-dim tangent structure the data lies on | assumes dense sampling; non-parametric variants scale poorly |

- **Explaining away** — in directed models (sparse coding), observing an effect makes a-priori-independent causes dependent (the *burglary vs earthquake* alarm example). Yields a parsimonious `p(h|x)` at extra inference cost. RBMs and plain autoencoders lack it.
- **Sparse coding** wins in the low-data regime (< 1000 labelled examples/class on CIFAR-10) precisely because explaining-away activates only a few bases.

#### 3. Three properties of a good representation
1. **Distributed** — expressive; `O(2ᵏ)` regions from `O(N)` params (vs `O(N)` regions for k-means/kNN/trees/SVMs).
2. **Abstract & invariant** — deeper layers → more abstract features, invariant to local input changes (built explicitly via pooling in CNNs).
3. **Disentangled** — separate the factors of variation. Distinct from invariance: **invariance discards** information in a chosen direction; **disentangling preserves** all factors but separates them, deferring the choice of which are relevant.

#### Key Takeaways for DLE602
1. **This is the "New Perspectives" behind the module title** — every phrase in the module intro ("learn good features", "task-specific representations", the emotion-vector example) traces to this paper.
2. **The 3-family taxonomy is the best mental index for the whole course:** autoencoders = Module 7; probabilistic RBMs/DBNs = the pretraining story; manifold = the geometric prior. Cite this paper (not just the blog) for academic credibility in A2/A3.
3. **The "objectives are ill-defined" point is genuinely current** — it is *why* self-supervised objectives (masked-language-modelling in BERT/DistilBERT) matter: they are a better-defined proxy target than raw reconstruction.

---

### 3. Zhong, G., Wang, L.-N., Ling, X. & Dong, J. (2016). An Overview on Data Representation Learning: From Traditional Feature Learning to Recent Deep Learning.

**Citation:** Zhong, G., Wang, L.-N., Ling, X. & Dong, J. (2016). An overview on data representation learning: From traditional feature learning to recent deep learning. *The Journal of Finance and Data Science, 2*(4), 265–278. https://doi.org/10.1016/j.jfds.2017.05.001

**Purpose:** The **history** resource. Its key argument: *deep learning is not a totally new idea* — it is the convergence of a century of feature-learning research with two enabling factors (big labelled data + GPUs). Read for the timeline and the traditional (shallow) methods the deep era replaced.

---

#### 1. The two intertwined timelines
- **Representation learning:** PCA (Pearson, 1901) → LDA (Fisher, 1936) → manifold learning (Isomap, LLE — *Science*, 2000) → deep learning (Hinton, 2006).
- **Neural networks (a bumpier road):** McCulloch–Pitts neuron (1943) → Hebbian learning (1949) → Perceptron (Rosenblatt, 1958) → **XOR wall** (Minsky & Papert, 1969) → backprop (Werbos, 1974; Rumelhart–Hinton–Williams, 1986) → the two blockers **overfitting + gradient diffusion** → greedy pretraining unlocks depth (Hinton, 2006).
- **The punchline:** the two streams *merge* in the deep-learning era. DL = feature-learning progress **+** large labelled datasets **+** GPGPU hardware.

#### 2. Traditional (shallow) feature learning — the taxonomy
- Every method is classifiable on 4 axes: **linear/nonlinear · supervised/unsupervised · generative/discriminative · global/local.**

| Method | Axes | One-liner |
|---|---|---|
| **PCA** (1901) | linear · unsupervised · generative · global | orthogonal projection to max-variance axes → Eigenfaces |
| **LDA** (1936) | linear · supervised · discriminative · global | max between-class / within-class scatter → Fisherfaces (robust to lighting) |
| **KPCA / GDA** | nonlinear (kernel) | kernel-trick versions of PCA/LDA |
| **Isomap, LLE, LE, LPP** (manifold) | nonlinear · local | preserve *local* neighbourhood / geodesic structure |

- **Global vs local:** global methods (PCA/LDA) preserve global structure; **manifold learning** preserves local similarity to recover the low-dim manifold hidden in high-dim data.

#### 3. The deep era
- **2006 trigger:** Hinton & Salakhutdinov — greedy layer-wise pretraining + fine-tuning beats SOTA on MNIST and document retrieval.
- **2012 inflection:** **AlexNet** wins ImageNet (dropout + ReLU + GPU). 2013–2016 winners are all deep CNNs: OverFeat, VGGNet, GoogLeNet, ResNet.
- **DeCAF insight:** activations from a supervised CNN (AlexNet's 6th FC layer) **transfer** as generic features to new tasks + an SVM — empirical transfer learning.
- Toolboxes of the era: Theano, Caffe, TensorFlow, MXNet.

#### Key Takeaways for DLE602
1. **Best resource for the "big picture" slide** in A2 — a one-line timeline from PCA (1901) to your ATAE-LSTM (2016) shows examiners you place your work in the field's history.
2. **Grounds the "why deep" argument:** the two blockers (overfitting, gradient diffusion) are the same vanishing-gradient story from Module 8 — pretraining, then ReLU / dropout, dissolved them.
3. **TF-IDF is explicitly labelled feature *engineering*, excluded from feature *learning*.** That is the exact dividing line your Review Pulse baseline (TF-IDF + LogReg) vs BiLSTM/DistilBERT sits on — hand-crafted representation vs learned representation.

---

### 4. Ghosh, A. (2019, 8 December). Representation Learning: A Review and Perspectives.

**Citation:** Ghosh, A. (2019, 8 December). *Representation learning: A review and perspectives* [Blog post]. Medium. https://medium.com/@aganirbanghosh007/representation-learning-a-review-and-perspectives-ea923618d79c

**Purpose:** A 42-minute practitioner synthesis that **stitches Goodfellow Ch.15 and Bengio et al. (2013) together in plain language**, adds concrete benchmark numbers, and includes a runnable Keras greedy-layer-wise pretraining example. Best used as the "clarify anything confusing" companion — as the module intro says, it answers questions the essential resources raise.

---

#### 1. The empirical wins (concrete numbers for your report)
- **Speech:** Microsoft MAVIS (2012) cut word error rate ~30% vs Gaussian-mixture SOTA on 309h of speech.
- **Vision:** MNIST error broke the SVM 1.4% barrier → 0.27%; ImageNet SOTA error 26.1% → 15.3% (AlexNet era).
- **NLP:** RNN language models dropped perplexity 140 → 102 and WSJ word error 17.2% → 14.4%; word embeddings (Hinton, 1986 → neural LMs) power Google image search and the SENNA multi-task NLP system.

#### 2. The "what makes a representation good" checklist (mirrors Bengio 2013)
- **Distributed** (expressive, `O(2ᵏ)` regions) → **Depth / abstraction** (feature re-use + invariance) → **Disentangling** (separate independent factors) → **Good criteria** (the hard open problem: the target is far from the objective, like RL credit assignment).

#### 3. Concrete build recipe (the practitioner value-add)
- Walks through greedy layer-wise pretraining as **stacked autoencoders in Keras**: train a base autoencoder → strip its output layer → freeze hidden layers → add + train a classifier head → reattach for the next layer. This is §15.1's Algorithm 15.1 turned into code.

#### Key Takeaways for DLE602
1. **Use it to unstick, not to cite as primary** — for academic claims, cite Goodfellow / Bengio et al. (the sources it re-tells), and reserve the blog for the benchmark numbers and the code recipe.
2. **The Keras stacked-autoencoder recipe** is a ready template if you ever want to *demonstrate* representation learning in the Review Pulse repo (e.g., pretrain an encoder on unlabelled reviews).
3. **Its structure = your revision structure:** distributed → depth → disentangle → objectives is the exact four-beat you should be able to recite for Activity 1's "why should we care?" opener.
