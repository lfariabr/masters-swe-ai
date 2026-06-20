# Module 4 - Regularization

> Key Highlights for the four Module 4 resources. The throughline: a central problem in deep learning is making a model that performs well on **new** data, not just the training set. Every technique here buys generalisation by trading a little bias for a lot less variance.

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow et al. (2016) Ch.7 - regularization strategies for deep models | ✅ |
| **2** | Read & summarise Wang & Klabjan (2017) - regularization for unsupervised deep nets (RBM/DBN/DBM) | ✅ |
| **3** | Read & summarise Kukačka, Golkov & Cremers (2017) - a taxonomy of regularization | ✅ |
| **4** | Read & summarise Shubham (2018) - regularization techniques in Python/Keras (the Activity 1 case study) | ✅ |
| 5 | Activity 1: Programming - run Shubham's MNIST case study, observe regularization | 🕐 |
| 6 | Activity 2: Analysis - find an area where overfitting is actually desirable | 🕐 |
| 7 | Activity 3: "I Wish" - would regularization knowledge have improved your A1 submission? | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning, Chapter 7.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning.* Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/ (Chapter 7, "Regularization for Deep Learning").

**Purpose:** The definitive catalogue of regularization for deep nets. Defines what regularization *is* (the bias-variance trade), then works through the full toolkit - parameter penalties, dataset augmentation, early stopping, dropout, bagging and more. This chapter is the conceptual backbone of the whole module.

---

#### 1. What regularization is - the bias-variance trade

- **Definition (Ch.5, used here):** "any modification we make to a learning algorithm that is intended to reduce its **generalization error but not its training error**."
- **Mechanism:** regularization works by **trading increased bias for reduced variance**. A good regulariser makes a profitable trade - cuts variance a lot while barely raising bias.
- **Three regimes:** (1) model family *excludes* the true process → **underfitting / high bias**; (2) model family *matches* it → the sweet spot; (3) model family includes the true process *plus* many others → **overfitting / high variance**. **The goal of regularization is to move a model from regime 3 into regime 2.**
- **Deep-learning reality:** the true data-generating process (images, audio, text) is almost always *outside* the model family - "fitting a square peg into a round hole." So the best model is usually a **large model regularised appropriately**, not a perfectly-sized small one.

#### 2. Parameter norm penalties (§7.1) - L2 vs L1

Add a penalty `Ω(θ)` to the objective: `J̃(θ) = J(θ) + α·Ω(θ)`, where `α ≥ 0` sets the strength (`α = 0` → no regularization). **Penalise weights `w`, not biases** (biases need less data, regularizing them causes underfitting).

| | **L2 (weight decay / ridge)** | **L1 (lasso)** |
|---|---|---|
| **Penalty** | `Ω = ½‖w‖₂²` (sum of squares) | `Ω = ‖w‖₁` (sum of absolute values) |
| **Effect on weights** | shrinks all weights toward 0, most along **low-curvature (unimportant) directions** of the Hessian | drives many weights to **exactly 0** |
| **Result** | smaller, "smoother" weights; more robust to input noise | **sparse** model → feature selection / compression |
| **Bayesian view (MAP)** | Gaussian prior on weights | Laplace prior on weights |

- **§7.2 - penalty ≈ constraint:** a norm penalty is equivalent to a **constrained optimization** problem (L2 ≈ confining the weights to a ball of fixed radius). Useful mental model: regularization "reins in" the size of the weight vector.

#### 3. The rest of the toolkit (§7.4-7.13)

| Technique | One-line idea |
|---|---|
| **Dataset augmentation** (§7.4) | create fake training data via label-preserving transforms (rotate/flip/scale). Best for **object recognition**; never transform away the label (b↔d, 6↔9). |
| **Noise robustness + label smoothing** (§7.5) | inject noise on inputs (≈ a norm penalty), on weights, or **soften one-hot targets** (label smoothing) so the model can't chase 0/1 forever. |
| **Semi-supervised / multitask** (§7.6-7.7) | share representations across unlabeled data or related tasks → better generalisation through shared structure. |
| **Early stopping** (§7.8) | **the most common regularizer in deep learning.** Hold out a validation set, stop when validation error starts rising. Number of training steps becomes a hyperparameter; "free lunch" - cheap and effective; ≈ L2 in simple settings but tunes effective capacity automatically. |
| **Parameter tying / sharing** (§7.9) | force groups of weights to be equal. **CNNs** are the headline case - shared convolutional filters encode shift-equivariance and slash parameter count. |
| **Sparse representations** (§7.10) | penalise the *activations* (not weights) toward sparsity. |
| **Bagging & ensembles** (§7.11) | train several models on bootstrap samples and average → variance reduction. |
| **Dropout** (§7.12) | randomly drop units each step → trains an **exponential ensemble of sub-networks with shared weights**. A cheap approximation to bagging; at test time use the **weight-scaling rule** (multiply by keep probability). |
| **Adversarial training** (§7.13) | train on deliberately perturbed inputs to flatten the function near data points. |

#### Key Takeaways for DLE602
1. **Regularization = generalisation insurance.** Memorise the one-liner: *trade a little bias for a lot less variance to beat overfitting.* This frames every other resource in the module.
2. **L1 vs L2 is the exam staple:** L2 shrinks (ridge, Gaussian prior), L1 sparsifies (lasso, Laplace prior). The Shubham blog (Resource 4) is exactly these two, in Keras.
3. **Early stopping and dropout are the two you will reach for first** in practice - and dropout is already inside the GloVe-DCNN you cite for **Assessment 1**.
4. Connects forward: every model you build in **A1 (sentiment classifier)** and **A2/A3 (Review Pulse v2 ABSA)** needs these to avoid memorising the training tweets/reviews.

---

### 2. Wang, B. & Klabjan, D. (2017). Regularization for unsupervised deep neural nets.

**Citation:** Wang, B. & Klabjan, D. (2017). *Regularization for unsupervised deep neural nets* (arXiv:1608.04426). Retrieved via Torrens Library / ProQuest.

**Purpose:** Shows that **overfitting happens in unsupervised deep nets too** (restricted Boltzmann machines, deep belief networks, deep Boltzmann machines), then extends the standard regularizers to that setting and proposes a new, more robust one.

---

#### 1. The setting - unsupervised building blocks

- **RBM** (restricted Boltzmann machine): an energy-based model with one visible and one hidden layer; stack them to build **DBNs** and **DBMs**. Trained with stochastic gradient descent + **contrastive divergence (CD-k)**.
- **Why it matters:** RBM/DBN weights are often used to **pre-train / initialise** a supervised feedforward net. If the unsupervised stage overfits, that bad initialisation propagates.

#### 2. Methods compared and proposed

| Method | What it does |
|---|---|
| **Weight decay (L2), adaptive L1, L2+AL1** | classic norm penalties carried over to RBMs; L2+AL1 ≈ elastic net |
| **Dropout (DO) / DropConnect (DC)** | mask nodes (DO) or weights (DC) per example/mini-batch → model averaging |
| **Network pruning (SNP / INP)** | delete low-magnitude weights and retrain; simple (SNP) or iterative (INP) |
| **Partial Dropout / DropConnect (PDO / PDC)** ⭐ | **the paper's contribution** - always keep the *important* (large-magnitude) weights/nodes, and only randomly drop the rest. Reduces the variance that plain dropout introduces by killing influential weights. |

#### 3. Empirical verdict

- Tested on **MNIST, NORB** (vision), **20 Newsgroups, Reuters21578** (text), **ISOLET** (speech).
- The most robust methods across all datasets: **L2, L2+AL1, and PDC**.
- **PDC (partial DropConnect) is the most stable overall → the recommended choice.**
- Side note: unsupervised nets tend to need **less regularization** than supervised feedforward nets.

#### Key Takeaways for DLE602
1. **Overfitting is not just a supervised problem** - the same penalties (L2, dropout) generalise to unsupervised pre-training.
2. **Dropout's weakness:** dropping high-magnitude weights adds variance; the fix (**partial** dropout/DropConnect) keeps the important weights. A neat illustration of *why* a regularizer can be improved rather than just applied.
3. Reinforces Goodfellow's framing from Resource 1: dropout ≈ model averaging, weight decay ≈ shrinkage.

---

### 3. Kukačka, J., Golkov, V. & Cremers, D. (2017). Regularization for deep learning: A taxonomy.

**Citation:** Kukačka, J., Golkov, V. & Cremers, D. (2017). *Regularization for deep learning: A taxonomy* (arXiv:1710.10686). Retrieved via Torrens Library / ProQuest.

**Purpose:** Unifies a sprawling, inconsistently-defined field. Provides a working definition and a **5-category map** so seemingly unrelated methods (augmentation, dropout, batch norm) can be seen as variations on the same theme.

---

#### 1. A broader working definition

- **Definition 1:** "Regularization is **any supplementary technique that aims at making the model generalize better**, i.e. produce better results on the test set."
- Deliberately **broader than Goodfellow's** ("reduce test error but not training error") - because some techniques (e.g. weight decay in AlexNet) actually reduce *training* error too.

#### 2. The taxonomy - 5 places you can regularize

Anchored to the empirical-risk equation `L̂ = (1/|D|) Σ E(f_w(xᵢ), tᵢ) + R(...)`. Every regularizer touches one of these five elements:

| # | Where | What lives here |
|---|---|---|
| 1 | **Data (`D`)** §3 | dataset augmentation, dropout-as-input-noise, batch/layer normalization, label smoothing |
| 2 | **Architecture (`f`)** §4 | convolutions, weight sharing, pooling, residual/skip connections, multi-task heads, dropout |
| 3 | **Error function (`E`)** §5 | choice of loss (cross-entropy, Dice for class imbalance) |
| 4 | **Regularization term (`R`)** §6 | **weight decay (L2)**, smoothness/Jacobian penalties, soft weight-sharing |
| 5 | **Optimization** §7 | weight **initialization**, SGD update rules (momentum, Adam), **early stopping** (termination) |

- **Big insight:** methods that look unrelated are "methodologically surprisingly close." Augmentation, dropout and batch norm all sit in the **data** branch; dropout *also* sits in architecture and optimization (it spans branches).
- **R vs E:** the regularization term `R` is independent of the targets `t`, so it can be evaluated on **unlabeled** data → enables semi-supervised learning. The error term `E` cannot.

#### 3. Practical recommendations (§8)

- Start with **methods that usually work** (ReLU, proven architectures), tune hyperparameters "lazily."
- Begin with a **simple dataset + simple network**, then scale both up.
- **Get more real data** if you can (labeled > unlabeled, same-domain > similar-domain); otherwise **augment**.
- **Data augmentation is more expressive than loss terms** - loss penalties only constrain an infinitesimal neighbourhood of each sample; augmentation can use rich transformation distributions.

#### Key Takeaways for DLE602
1. **The single best mental model for the module:** there are exactly **5 levers** - data, architecture, error, regularization term, optimization. Any technique you meet can be filed under one.
2. Resolves the terminology confusion: "regularization" in this course means the **broad** definition (anything that helps generalisation), not just the L2 penalty term.
3. Directly useful for **Activity 1 flowcharts and assessments** - you can justify a design choice by naming *which lever* it pulls.

---

### 4. Shubham, J. (2018). An overview of regularization techniques in deep learning (with Python code).

**Citation:** Shubham, J. (2018, 19 April). *An overview of regularization techniques in deep learning (with Python code)* [Web log post]. Analytics Vidhya. Retrieved from https://www.analyticsvidhya.com/blog/2018/04/fundamentals-deep-learning-regularization-techniques/

**Purpose:** The beginner-friendly, **hands-on** resource - and the source of the **Module 4 Activity 1 case study** (MNIST digit recognition in Keras). Turns the theory from Resources 1-3 into runnable code.

---

#### 1. The four techniques, with Keras one-liners

| Technique | Idea | Keras |
|---|---|---|
| **L2 / L1** | add a penalty term to the cost; smaller weights → simpler model. L2 = weight decay (weights → near 0); L1 = lasso (weights → exactly 0, compresses model) | `Dense(64, kernel_regularizer=regularizers.l2(0.01))` |
| **Dropout** | randomly remove nodes + their connections each iteration → different sub-network each time ≈ ensemble. Most-used DL regularizer. | `Dropout(0.25)` |
| **Data augmentation** | cheaply enlarge the training set (rotate, flip, scale, shift, ZCA-whiten images) | `ImageDataGenerator(...)` |
| **Early stopping** | hold out a validation set; stop when validation error stops improving. `patience` = epochs to wait before stopping. | `EarlyStopping(monitor='val_acc', patience=2)` |

#### 2. The case study (Activity 1)

- **Task:** the "Identify the Digits" practice problem (MNIST-style), a 5-hidden-layer net (500 nodes each) in Keras, 70:30 train/validation split, fixed seed for reproducibility.
- **Observed results** (vs a plain net baseline):
  - **L2** → small improvement; **L1** → no improvement here; **Dropout** → small improvement.
  - **Data augmentation (ZCA-whitening)** → the **biggest accuracy leap** ("works every time").
  - **Early stopping** → stops after ~5 idle epochs; a tool to *tune the number of epochs* rather than boost peak accuracy.
- **Takeaway from the author:** regularization is essential when training deep nets on large data; combine L1/L2 + dropout + augmentation + early stopping, and tune hyperparameters (λ, dropout rate, learning rate).

#### Key Takeaways for DLE602
1. **This is the Activity 1 deliverable** - download the dataset, run each regularizer, and report what changed (Activity asks you to "observe the outcome and pay extra attention to the regularization technique").
2. **Data augmentation winning** matches Kukačka et al.'s claim (Resource 3) that augmentation is the most expressive lever - a satisfying theory-meets-practice moment.
3. Fixed seed + explicit train/val split = the reproducibility discipline expected in your assessment notebooks.

---

### How Module 4 connects to the assessments

- **A1 (sentiment classifier, due 28/06/2026):** the GloVe-DCNN you cite (Zhao et al., 2018) already uses **dropout**. Activity 3 ("I Wish") explicitly asks whether regularization knowledge would have improved your A1 - the honest answer is yes: early stopping + dropout + L2 are what stop the classifier from memorising the training tweets.
- **A2 / A3 (Review Pulse v2, ABSA):** the same toolkit keeps the attention-LSTM / fine-tuned transformer from overfitting the SemEval / client reviews. Augmentation (back-translation) - which you proposed in the Module 3 Activity 1 flowchart - is literally the §7.4 / taxonomy "data" lever.
