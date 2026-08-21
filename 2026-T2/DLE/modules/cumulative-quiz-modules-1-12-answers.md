# DLE602 Cumulative Quiz - Modules 1-12 - Answer Key

Use this after completing `cumulative-quiz-modules-1-12.md` closed book. Equivalent answers earn credit when they preserve the same distinctions.

## 1. Module 1 - Representation over features (6 points)

Learning layered representations means the network builds higher-level concepts from simpler ones automatically, instead of a human hand-designing which features matter - representation quality drives performance more than the raw features themselves. The N-gram reading gives the technical foundation (word-sequence probability estimation from local context) that Assessment 1's Twitter sentiment classifier is built on.

## 2. Module 2 - Why depth needs nonlinearity (8 points)

XOR is not linearly separable - no single straight line (a linear layer) can divide its four points into the correct two classes. A hidden layer with a nonlinear activation lets the network combine two linear boundaries into a bent decision surface, which is exactly what XOR needs.

Backpropagation computes the gradient of the loss with respect to every weight in the network by applying the chain rule backward through the computational graph, so an optimiser can then use those gradients to update the weights.

## 3. Module 3 - The NLP arc (8 points)

Progression: classical **n-grams** (the A1 baseline, which suffers the curse of dimensionality) to **word embeddings** and **attention** (encoder-decoder), the deep-learning leap that generalises better.

Zhao et al. (2018)'s **GloVe-DCNN** fuses word embeddings, n-grams, a sentiment lexicon, and Twitter-specific features into a deep CNN, reaching up to roughly **87.62% accuracy** on datasets including STS-Test and **STS-Gold**.

## 4. Module 4 - The five regularisation levers (9 points)

Kukacka et al.'s five levers: **data, architecture, error function, regularisation term, optimisation**.

**L2** (weight decay/ridge) shrinks weights toward zero without forcing them to exactly zero; **L1** (lasso) drives many weights to *exactly* zero, producing sparsity and implicit feature selection.

Dropout randomly zeroes units each forward pass, which is equivalent to training an exponential number of thinned sub-networks that share weights and then implicitly averaging them at test time - a cheap approximation to bagging that ensemble.

## 5. Module 5 - What makes convolution work (9 points)

- **Sparse interactions**: each output unit connects to only a small local region of the input, cutting parameters and computation.
- **Parameter sharing**: the same filter weights are reused across spatial locations, so a feature detector need only be learned once.
- **Equivariance to translation**: shifting the input shifts the detected feature output by the same amount, letting the same filter detect a feature anywhere in the input.

Order by year: **AlexNet (2012) -> VGG16 -> GoogLeNet/Inception -> ResNet**.

## 6. Module 6 - Four linear factor models (8 points)

| Model | What it separates / preserves |
|---|---|
| PCA | preserves the high-variance directions in the data |
| Factor analysis | models shared covariance across variables separately from variable-specific noise |
| ICA | separates independent, non-Gaussian source signals |
| SFA | extracts slowly changing temporal features |

## 7. Module 7 - Autoencoders and PCA (9 points)

**Baldi (2012)** proves that an undercomplete autoencoder with a linear encoder/decoder and squared-error (MSE) loss reaches its global optimum by recovering the **PCA subspace** - the projection onto the top eigenvectors.

Three regularised variants:
- **Sparse**: enforces few active units in `h` (L1/Laplace penalty).
- **Denoising**: reconstructs a clean input from a corrupted one, implicitly learning the data manifold/score.
- **Contractive**: makes the learned features insensitive to small changes in the input.

## 8. Module 8 - Why plain RNNs fail and how LSTM fixes it (9 points)

Unrolled through time, backpropagation through time (BPTT) multiplies by the **same weight matrix repeatedly** at every timestep; depending on its eigenvalues, this product either shrinks toward zero (**vanishing**) or grows without bound (**exploding**) as the sequence gets longer.

LSTM's three gates: **forget, input, output**. The cell state is a **linear self-loop** - an additive, gated path rather than a repeated matrix multiplication - so information can be carried across many timesteps without being forced through the same multiplicative shrink/grow dynamic (it mitigates, though does not fully remove, the vanishing-gradient problem).

## 9. Module 9 - A representation is relative to what (7 points)

`210 / 6` is easy; `CCX / VI` is the same numbers in Roman numerals and is hard - the values are identical, but one encoding makes the downstream task (division) tractable and the other does not. A representation's quality only exists relative to the task it needs to support, never in the abstract.

The 2006 greedy layer-wise unsupervised pretraining procedure (Hinton) - train one frozen layer at a time on unlabelled data, then fine-tune - is now largely historical as a specific technique, but its core idea lives on as modern **self-supervised pretraining**: word2vec/GloVe through **BERT** in NLP, and contrastive/masked self-supervised learning in vision.

## 10. Module 10 - Directed vs undirected graphical models (8 points)

Directed (Bayesian/belief network) factorisation: `p(x) = product over i of p(x_i | Pa_i)`. It is naturally suited to **causal, one-directional** relationships and supports cheap **ancestral sampling**.

Exact inference is typically intractable because the **partition function `Z`** (needed to normalise undirected models) and general inference are **#P-hard** to compute exactly as the graph grows. Approximate techniques used instead: **Gibbs sampling** (MCMC) and **variational (approximate) inference**; energy-based models such as RBMs are the associated model family.

## 11. Module 11 - Activations vs gradients, and the snow-leopard problem (9 points)

**Activations** show how the network **decides** (its inference-time behaviour); **gradients** show how the network **learns** (the training-time update signal). **RNNbow** is the module's counterexample - it visualises gradients *during* training, whereas most surveyed work is activation-based and after training.

The **snow-leopard problem**: a model scores high by learning a shortcut feature (e.g. snow background vs desert background) instead of the actual object, so accuracy hides the wrong reason for a right answer. **CNNComparator's** matching finding: at epoch 100 the model still misclassified a **daffodil as a buttercup** because it had latched onto the colour **yellow** - the same shortcut-feature failure mode in a different dataset.

## 12. Module 12 - Loss vs metric (6 points)

The **loss** is a differentiable proxy used to update weights during training; the **metric** is the number that judges whether the deployed system actually solves the real problem, and need not be differentiable.

**Coverage** (or a recall target with reported precision) is appropriate when a model may abstain and defer to a human - it measures how much of the workload the model can resolve unaided, which plain accuracy cannot capture because accuracy says nothing about the asymmetric cost of a missed case versus a false alarm.

## 13. Synthesis - the sequential bottleneck across three modules (8 points)

(a) **Module 9's framing**: the LSTM hidden state `h(t)` is a representation, and a fixed-size vector is a lossy summary - whatever the current task needs at timestep `t+k` must already have been compressed into `h(t)` at write time, without knowing in advance what will be asked later. That is a representation-adequacy problem, not just an optimisation one.

(b) **Module 8's mechanism**: because BPTT multiplies by the same weight matrix at every step, the gradient connecting a distant timestep back to an early one is a product of many Jacobians, which vanishes (or explodes) as the distance grows - so the network struggles to learn dependencies that span many steps, reinforcing the pressure to over-compress early information into `h(t)`.

(c) **Module 11's technique**: **RNNbow**, since it visualises the gradient of `W` directly and shows dark, short bars for gradients that only reach a short horizon back - making the vanishing-gradient dynamic visible as a shape in the stacked-bar chart, rather than something only inferred indirectly from a flattening loss curve.
