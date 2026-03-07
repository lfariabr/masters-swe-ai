# Module 04 — Introduction to Deep Learning
## ISY503 Intelligent Systems

---

## Task List

| # | Resource / Activity | Type | Status |
|---|---------------------|------|--------|
| 1 | Gupta, D. (2020) — Activation Functions and When to Use Them | Reading | ✅ |
| 2 | Krogh, A. (2008) — What are Artificial Neural Networks? | Reading | ✅ |
| 3 | LeCun, Y. et al. (2015) — Deep Learning (CNNs & RNNs) | Reading | ✅ |
| 4 | Hulten, G. (2018) — Building Intelligent Systems (ProQuest eBook) | Reading | 🔥 WIP |
| A1 | Deep Learning Discussion Forum Post | Activity | 🕐 |
| A2 | ANN Details (learning rate, loss fn, batch, epoch, dropout) | Activity | 🕐 |

---

## Key Highlights

---

### Resource 1 — Gupta, D. (2020): Activation Functions and When to Use Them

**Source:** Gupta, D. (2020, 30 January). Fundamentals of deep learning—Activation functions and when to use them? [Blog post]. Analytics Vidhya. Retrieved from https://www.analyticsvidhya.com/blog/2020/01/fundamentals-deep-learning-activation-functions-when-to-use-them/

#### 1. What is an Activation Function?

- A neuron applies a **linear transformation** on its inputs: `x = (weight × input) + bias`
- An **activation function** then applies a **non-linear transformation**: `Y = Activation(Σ(weight × input) + bias)`
- Without activation functions, a neural network is equivalent to a **linear regression model** — it cannot learn complex patterns
- Activation functions introduce **non-linearity**, enabling networks to represent intricate relationships in data

#### 2. Forward and Back Propagation

- **Forward propagation**: input flows through each layer; every neuron applies linear transformation + activation, passing the result to the next layer
- **Back-propagation**: the output error is computed; weights and biases are updated by propagating the gradient backwards through the network
- The **gradient** of the activation function determines how effectively weights update during backprop — zero gradients block learning

#### 3. Activation Functions Compared

| Function | Formula | Range | Key Trait | Best Use Case |
|----------|---------|-------|-----------|---------------|
| Binary Step | f(x) = 1 if x≥0, else 0 | {0,1} | Zero gradient — blocks backprop | Binary classifiers only (legacy) |
| Linear | f(x) = ax | (−∞, ∞) | Constant gradient — no improvement per layer | Simple/interpretable tasks |
| Sigmoid | f(x) = 1/(1+e^−x) | (0, 1) | Non-linear; vanishing gradient for \|x\|>3 | Binary classification (output layer) |
| Tanh | tanh(x) = 2sigmoid(2x)−1 | (−1, 1) | Zero-centred; steeper than sigmoid | Hidden layers (preferred over sigmoid) |
| ReLU | f(x) = max(0, x) | [0, ∞) | Fast; sparse activation; dying ReLU for x<0 | Hidden layers (default choice) |
| Leaky ReLU | f(x) = 0.01x if x<0, else x | (−∞, ∞) | Fixes dying ReLU; non-zero gradient for x<0 | When dead neurons are a problem |
| Param. ReLU | f(x) = ax if x<0, else x | (−∞, ∞) | Learnable slope 'a'; network tunes it | When Leaky ReLU still underperforms |
| ELU | f(x) = a(e^x−1) if x<0, else x | (−∞, ∞) | Log curve for negatives; no dead neurons | Deeper networks needing smooth negatives |
| Swish | f(x) = x · sigmoid(x) | (−∞, ∞) | Smooth, non-monotonic; outperforms ReLU on deep models | Deep networks (Google-discovered) |
| Softmax | e^xi / Σe^xj | (0, 1) summing to 1 | Probability distribution over all classes | Multi-class output layer |

#### 4. Choosing the Right Activation Function

- **Sigmoid / Tanh**: good classifiers but suffer from **vanishing gradient** — avoid in deep hidden layers
- **ReLU**: the modern default for hidden layers — computationally efficient and fast convergence
- **Leaky ReLU / Parameterised ReLU / ELU / Swish**: use when dead neurons appear or ReLU underperforms in very deep networks
- **Softmax**: always use at the output layer for **multi-class classification**
- **Rule of thumb**: start with ReLU in hidden layers; switch to variants if training stalls

#### Key Takeaways for ISY503

- Activation functions are what make neural networks capable of learning non-linear relationships — without them, a deep network collapses into linear regression
- Two key failure modes: **vanishing gradient** (sigmoid/tanh) and **dying ReLU** (standard ReLU with negative inputs)
- **ReLU** is the modern default for hidden layers; **Softmax** for multi-class outputs
- Choice of activation function directly impacts convergence speed, model depth feasibility, and final accuracy

---

### Resource 2 — Krogh, A. (2008): What are Artificial Neural Networks?

**Source:** Krogh, A. (2008). What are artificial neural networks? *Nature Biotechnology*, 26(2), 195–197. https://www.proquest.com/scholarly-journals/what-are-artificial-neural-networks/docview/222305221/se-2?accountid=176901

#### 1. Biological Inspiration

- The human brain performs sophisticated pattern recognition through a **highly interconnected network of neurons** communicating via electric pulses along axons, synapses, and dendrites
- Key biological analogy: dendrites (inputs) → nucleus/cell body (processing) → axon terminals (output)
- In ANNs, a **model neuron** (McCulloch-Pitts, 1943) receives N weighted inputs; if the total exceeds a **threshold**, output = 1; otherwise = 0
- Synaptic **weights** can be positive (excitatory) or negative (inhibitory)

#### 2. How a Threshold Unit Learns

- Each neuron computes: **total input = Σ(weight_i × x_i)**
- If total ≥ threshold → output = 1; otherwise → output = 0
- The **decision boundary** is a **hyperplane** (a line in 2D, a plane in 3D)
- **Linear separability**: a threshold unit can only classify problems where classes are separable by a hyperplane
- **Non-linearly separable** problems (e.g., XOR) require multi-layer networks with hidden layers

#### 3. Multi-Layer Networks and Back-Propagation

- **Perceptrons** (Rosenblatt, 1969): early single-layer networks — limited to linearly separable problems; Minsky & Papert (1969) showed this limitation
- **Multi-layer perceptrons (MLPs)**: hidden layers between input and output enable solving non-linear problems
- **Back-propagation** (Rumelhart, Hinton & Williams, 1986): the key algorithm that unlocked deep learning
  - Initialise all weights to small random numbers
  - For each training example: compute output, measure error (sum of squared differences), update weights to reduce error
  - Gradient descent iteratively minimises the total error across all training examples
  - Repeats until the error no longer decreases significantly

#### 4. Over-fitting and Generalisation

- **Over-fitting**: the network learns training data too well (too many parameters relative to training examples) → poor performance on new data
- Example: a network with 10 hidden units solving a 2-class, 100-example problem has 221 free parameters — too many
- **Cross-validation**: split data into k folds; train on k-1, test on 1; repeat → unbiased estimate of generalisation
- **Regularisation** and **ensemble averaging** over several networks help limit over-fitting

#### 5. Extensions and Applications

- Multi-class classification: add one output unit per class
- Regression: replace step function with a continuous function; minimise squared error
- **Applications demonstrated**: speech recognition (NETtalk), protein secondary structure prediction, cancer classification, gene prediction
- Other related architectures: Boltzmann machines, unsupervised networks, Kohonen nets, support vector machines

#### Key Takeaways for ISY503

- **Back-propagation** is the cornerstone of ANN training — gradient-based weight updates propagate error signals backward through the network
- **Hidden layers** give ANNs the power to solve non-linear classification and regression problems
- **Over-fitting** is a persistent risk — always evaluate on independent test data; use cross-validation
- ANNs achieve state-of-the-art performance across biology, medicine, engineering and language when properly trained and regularised

---

### Resource 3 — LeCun, Y., Bengio, Y. & Hinton, G. (2015): Deep Learning

**Source:** LeCun, Y., Bengio, Y. & Hinton, G. (2015). Deep learning. *Nature*, 521(7553), 436–444. https://www.proquest.com/scholarly-journals/deep-learning/docview/1685003444/se-2?accountid=176901

#### 1. What is Deep Learning?

- **Deep learning**: representation-learning methods with multiple levels of representation — each layer transforms its input into a more abstract representation
- Key advantage: **features are learned automatically from raw data**, not hand-engineered by experts
- Enabled breakthroughs in: speech recognition, visual object recognition, object detection, drug discovery, genomics, NLP
- A deep-learning system may have **hundreds of millions of adjustable weights** trained on millions of labelled examples

#### 2. Supervised Learning and Optimisation

- **Supervised learning**: the model is shown labelled examples and learns to map input → output
- **Objective (loss) function**: measures error (distance) between the model's output scores and the desired output
- **Stochastic Gradient Descent (SGD)**: most common optimisation method; shows the model a mini-batch of examples, computes gradients, adjusts weights in the direction that reduces error
- The **weight vector** is adjusted in the opposite direction to the gradient — equivalent to moving downhill on the error landscape

#### 3. Backpropagation in Multilayer Networks

- **Backpropagation**: applies the **chain rule of calculus** to compute gradients through all layers efficiently
- At each layer: compute the total input z, apply non-linear function f(z), propagate activation forward
- On the backward pass: compute the derivative of the error with respect to each unit's input, propagate back layer by layer
- **ReLU** (f(z) = max(0, z)) is the preferred non-linearity — learns much faster than tanh/sigmoid in deep networks

#### 4. Convolutional Neural Networks (CNNs) — p.439

CNNs are designed for **array-structured data**: images (2D pixel arrays), audio spectrograms (2D), video (3D), sequences (1D).

**Four key design principles:**

1. **Local connections**: each unit connects to a small local patch of the previous layer's feature map — not all units (reduces parameters)
2. **Shared weights (filter banks)**: all units in a feature map share the same filter weights — the same pattern is detected regardless of its position in the input
3. **Pooling**: merges semantically similar features into one; **max-pooling** takes the maximum over a local patch — creates spatial invariance to small shifts and distortions, reduces dimensionality
4. **Many layers**: 2–3 stages of [convolution + non-linearity (ReLU) + pooling], followed by fully-connected layers and a Softmax output

**Architecture flow:**
```
Input Image → [Conv + ReLU + Pool] × N → Fully Connected → Softmax Output
```

*CNN architecture (convolutional stack):*
```mermaid
flowchart LR
    A[Input Image\n H×W×C] --> B[Conv + ReLU\nfeature maps]
    B --> C[Max Pooling\nreduce H,W]
    C --> D[Conv + ReLU\ndeeper features]
    D --> E[Max Pooling\nreduce H,W]
    E --> F[Fully Connected\nlayers]
    F --> G[Softmax\nclass probabilities]
```

- **Why CNNs work**: natural signals (images, audio) have local statistics that repeat across positions; pooling provides robustness to small transformations
- **ImageNet 2012 breakthrough**: deep CNN (AlexNet) halved error rates → triggered the modern computer vision revolution

#### 5. CNN Applications

| Domain | Application |
|--------|-------------|
| Computer Vision | Image classification, object detection, semantic segmentation |
| Face Recognition | Near human-level performance in face verification |
| Autonomous Vehicles | Traffic sign recognition, pedestrian/object detection |
| Medical Imaging | Biological image segmentation, connectomics |
| Industry | Real-time chips from NVIDIA, Mobileye, Intel, Qualcomm |

#### 6. Recurrent Neural Networks (RNNs) — p.441

RNNs are designed for **sequential data**: speech, text, time series, language.

- Process input **one element at a time**, maintaining a hidden **state vector** that encodes the history of all past elements
- The state vector is updated at each time step: information from earlier in the sequence influences processing of later elements
- Can be unfolded in time to look like a very deep feedforward network where all layers share the same weights
- **Training challenge — Backpropagation Through Time (BPTT)**: gradients either **explode** or **vanish** as they propagate over many time steps — standard RNNs struggle to learn long-range dependencies

*RNN temporal unrolling — same weights W reused at every time step:*
```mermaid
flowchart LR
    x0[x₀] --> h0[h₀]
    h0 -->|W| h1[h₁]
    x1[x₁] --> h1
    h1 -->|W| h2[h₂]
    x2[x₂] --> h2
    h2 -->|W| h3[h₃]
    x3[x₃] --> h3
    h0 --> o0[o₀]
    h1 --> o1[o₁]
    h2 --> o2[o₂]
    h3 --> o3[o₃]
```

#### 7. Long Short-Term Memory (LSTM) — p.442

**LSTM** (Hochreiter & Schmidhuber, 1997) directly addresses the vanishing gradient problem.

- Introduces special hidden units called **memory cells** that act like gated accumulators
- **Forget gate**: a separate unit that decides when to reset (clear) the memory cell's contents
- The memory cell has a **self-connection** that is multiplicatively gated — allowing it to maintain information for long periods without the gradient decaying
- **Why LSTMs work**: gradient can flow through the memory cell without vanishing, enabling learning of long-range dependencies
- LSTMs with multiple layers subsequently proved far more effective than conventional RNNs

*LSTM memory cell — gates control information flow:*
```mermaid
flowchart LR
    xt[xₜ input] --> fg[Forget Gate\nf = σ·W·h,x]
    xt --> ig[Input Gate\ni = σ·W·h,x]
    xt --> og[Output Gate\no = σ·W·h,x]
    xt --> cc[Cell Candidate\ng = tanh·W·h,x]
    fg -->|f × Cₜ₋₁| cell[Cell State Cₜ\nmemory]
    ig -->|i × g| cell
    cell --> ht[Hidden State hₜ\no × tanh·Cₜ]
    og --> ht
    ht --> next[Next time step]
```

**LSTM Applications:**

| Application | Description |
|-------------|-------------|
| Speech recognition | Maps acoustics all the way to character sequences (end-to-end) |
| Machine translation | English 'encoder' LSTM → French 'decoder' LSTM |
| Image captioning | CNN extracts image features → LSTM generates text caption |
| Language modelling | Predicts next word in a sequence |

#### 8. Distributed Representations and Language Processing — p.440

- Deep nets learn **distributed representations**: words mapped to dense real-valued vectors (**word vectors / word embeddings**)
- Semantically similar words end up **close together in vector space** (e.g., "Tuesday" and "Wednesday" have similar vectors)
- Traditional **N-grams**: count short symbol sequences; cannot generalise beyond seen contexts; need huge training corpora
- **Neural language models**: associate each word with a vector; the network learns to convert input word vectors into an output word vector predicting the next word

#### Key Takeaways for ISY503

- **CNNs** exploit spatial structure through local connections, shared filter banks, and pooling — the dominant approach for computer vision
- **RNNs** exploit temporal/sequential structure; standard RNNs suffer from vanishing gradients over long sequences
- **LSTMs** are the state-of-the-art RNN variant — gated memory cells enable learning of long-range dependencies essential for language and speech
- The deep learning revolution was enabled by three factors: **more data** (ImageNet), **faster hardware** (GPUs), and **algorithmic advances** (ReLU, dropout, SGD)
- Combining CNNs + RNNs enables powerful multimodal systems (e.g., image captioning: vision CNN → language RNN)
