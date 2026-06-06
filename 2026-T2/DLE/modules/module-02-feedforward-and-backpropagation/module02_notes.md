# Module 2: Feedforward Neural Network and Backpropagation

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow, Bengio & Courville (2016) - Deep feedforward networks Ch.6 | ✅ |
| **2** | Read & summarise Reed & Marks (1999) - MLP representational capabilities Ch.4 | ✅ |
| 3 | Watch & summarise Fernandes (2018) - Neurons and artificial neurons | 🔥 WIP - needs manual listen/authenticated access |
| **4** | Read & summarise Pathmind (n.d.) - Beginner's guide to neural networks and deep learning | ✅ |
| 5 | Activity 1: Understanding Feedforward Networks | 🕐 |
| 6 | Activity 2: Interactive Knowledge Sharing - Backpropagation | 🕐 |
| 7 | Activity 3: The Disadvantage of Neural Networks | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

**Purpose:** Chapter 6 explains deep feedforward networks as function approximation models. It connects MLP structure, nonlinear hidden layers, output-unit choice, architecture design, and backpropagation into the core workflow used to train neural networks.

---

#### 1. Feedforward Networks as Function Approximators

- **Feedforward network:** A model where information flows from input, through hidden layers, to output without feedback loops.
- **Goal:** Learn a mapping `y = f(x; theta)` that approximates an unknown target function `f*`.
- **Hidden layers:** Intermediate layers whose desired outputs are not directly specified by training data; the learning algorithm discovers useful internal representations.
- **Depth:** The number of composed layers in the model. A chain such as `f(x) = f3(f2(f1(x)))` is deeper than a single transformation.
- **Nonlinearity:** A purely linear stack is still linear overall, so useful MLPs need nonlinear activation functions.

| Design element | Role |
|---|---|
| **Weights** | Scale and combine input signals |
| **Biases** | Shift activation thresholds |
| **Activation functions** | Introduce nonlinearity |
| **Hidden layers** | Learn intermediate representations |
| **Output layer** | Converts learned features into the prediction format |

#### 2. Learning XOR and Why Hidden Layers Matter

- **XOR problem:** A simple binary task that a linear model cannot solve in the original input space.
- **Representation shift:** A hidden layer can transform the input into a feature space where a linear output layer can solve the task.
- **ReLU default:** Goodfellow et al. present rectified linear units, `g(z) = max(0, z)`, as the default modern activation for many feedforward networks.
- **Module activity link:** The XOR example is the foundation for Activity 1 because it shows what a feedforward network does in concrete terms: it learns a nonlinear representation, then maps that representation to an output.

#### 3. Gradient-Based Learning, Cost Functions, and Output Units

| Output type | Typical task | Common loss / interpretation |
|---|---|---|
| **Linear unit** | Regression | Gaussian output; maximum likelihood becomes mean squared error |
| **Sigmoid unit** | Binary classification | Bernoulli output; cross-entropy / negative log-likelihood |
| **Softmax unit** | Multiclass classification | Multinoulli output; cross-entropy / negative log-likelihood |

- **Nonconvexity:** Neural network losses are usually nonconvex, so training aims to reduce cost to a low value rather than guarantee a global optimum.
- **Initialization:** Weights are usually initialised to small random values; biases can be zero or small positive values.
- **Cross-entropy preference:** Maximum likelihood / cross-entropy often gives better gradients than mean squared error for sigmoid or softmax classification outputs.
- **Regularisation:** Total cost often combines the main loss with a regularisation term such as weight decay.

#### 4. Hidden Units and Architecture Design

| Hidden unit | Practical note |
|---|---|
| **ReLU** | Strong default; easy to optimise because active units have stable gradients |
| **Leaky ReLU / PReLU** | Preserve gradient when the input is below zero |
| **Maxout** | Learns a piecewise linear activation but uses more parameters |
| **Sigmoid / tanh** | Historically common but can saturate and slow learning |
| **Softplus / hard tanh / RBF** | Useful in some cases, but less common as default choices |

- **Depth vs width:** One hidden layer may represent many functions, but deeper networks can represent some functions more efficiently with fewer units.
- **Universal approximation:** A sufficiently large MLP can approximate broad classes of functions, but this does not guarantee that training will find the right parameters or generalise well.
- **Validation-driven design:** Depth, width, activation choice, and connection structure are practical design decisions guided by validation performance.
- **Skip connections:** Some architectures add non-chain links to help gradients flow to earlier layers.

#### 5. Backpropagation

- **Forward propagation:** Computes activations from input through hidden layers to output and then computes the cost.
- **Backpropagation:** Computes gradients by applying the chain rule backward through the computational graph.
- **Common misconception:** Backpropagation is not the whole learning algorithm. It computes gradients; an optimiser such as stochastic gradient descent uses those gradients to update parameters.
- **Computational graph:** Represents variables and operations so gradients can be propagated through each operation.
- **Efficiency:** Backprop avoids recomputing repeated subexpressions and scales with the graph structure rather than expanding the chain rule naively.

#### Key Takeaways for DLE602

1. Module 2 is the bridge from "what is deep learning?" to "how networks actually learn."
2. Activity 1 should explain XOR as a representation-learning example: a hidden layer makes a nonlinearly separable task linearly solvable in a learned space.
3. Activity 2 should distinguish backpropagation from optimisation: backprop computes gradients; SGD or another optimiser updates weights.
4. Activity 3 can critique neural networks on interpretability, data hunger, compute cost, hyperparameter sensitivity, and overfitting risk.
5. Assessment 1 is still N-gram based, but this module prepares the conceptual contrast with deep models used in Twitter sentiment research.

---

### 2. Reed, R. D., & Marks, R. J. (1999). Neural smithing: Supervised learning in feedforward artificial neural networks.

**Citation:** Reed, R. D. & Marks, R. J. (1999). Neural smithing: Supervised learning in feedforward artificial neural networks. Cambridge, MA: MIT Press. Retrieved from http://search.ebscohost.com.torrens.idm.oclc.org/login.aspx?direct=true&db=nlebk&AN=9366&site=ehost-live&authtype=ip,sso&custid=ns251549&ebv=EB&ppid=pp_31

**Purpose:** Chapter 4 explains what multilayer perceptrons can represent. It clarifies layer-counting conventions, universal approximation, and the practical tradeoff between network depth, size, capacity, and generalisation.

---

#### 1. MLP Structure and Layer Counting

- **Standard MLP:** A cascade of perceptron layers with input nodes, one or more hidden layers, and output nodes.
- **Hidden layers:** Called hidden because they are not directly observable from system inputs and outputs.
- **Fully connected structure:** In the standard MLP, nodes in each layer connect to nodes in adjacent layers, with no same-layer, feedback, or shortcut connections.
- **Layer-counting ambiguity:** Some count the input layer; others count only active computational layers. Reed and Marks prefer counting active layers, so it is clearer to state the number of hidden layers explicitly.

| Notation | Meaning |
|---|---|
| `10/3/2` | 10 inputs, 3 hidden units, 2 outputs |
| `16/10/5/1` | 16 inputs, two hidden layers with 10 and 5 units, 1 output |

#### 2. Representational Capability

- **Representational capability:** The range of mappings a network can implement when its weights vary.
- **Existence vs training:** A proof that a network can represent a mapping does not guarantee that a training algorithm can find the required weights.
- **Single-layer limitation:** Single-layer networks can represent only linearly separable functions.
- **Decision regions:** MLPs can form nonconvex and disjoint decision regions, not only simple convex regions.

#### 3. Universal Approximation and Its Limits

| Claim | Practical interpretation |
|---|---|
| **One hidden layer can be sufficient** | Many continuous functions can be approximated with enough hidden units |
| **Two hidden layers can form arbitrary regions** | More layers can build complex decision boundaries efficiently |
| **Existence proofs are not recipes** | They do not tell you how to choose weights or guarantee learnability |
| **Universal approximation is not unique to neural nets** | Polynomials, kernels, wavelets, and other systems can also approximate broad function classes |

- **Important warning:** Universal approximation means neural networks are powerful enough, not automatically good enough.
- **Efficiency issue:** A shallow network may need an impractically large number of hidden units for some functions.
- **Generalisation issue:** Fitting training data does not imply the network will perform well on new inputs.

#### 4. Size Versus Depth

- **More layers can reduce size:** Some functions require many more units in a shallow network than in a deeper network.
- **Boolean-function examples:** Extra depth can reduce the number of required nodes exponentially for some logical functions.
- **Weight magnitude:** More depth can sometimes avoid very large weights required by shallow solutions.
- **Caveats:** These are often asymptotic or existence results, so real model choice still depends on data, assumptions, training method, and validation performance.

#### Key Takeaways for DLE602

1. Reed and Marks sharpen the architecture discussion from Goodfellow: capacity is not just about adding units; depth changes what can be represented efficiently.
2. The resource supports Activity 3 because disadvantages include no guarantee of learnability, possible overfitting, and difficulty choosing architecture.
3. For implementation work, the safest architecture argument is empirical: start simple, validate, then add depth or width when performance justifies it.

---

### 4. Pathmind. (n.d.). A beginner's guide to neural networks and deep learning.

**Citation:** Pathmind. (n.d.). A beginner's guide to neural networks and deep learning. Retrieved from https://pathmind.com/wiki/neural-network.

**Purpose:** Provides an accessible overview of neural networks, common problem types, network elements, feedforward learning, gradient descent, and classification outputs. It is useful as a plain-language companion to the more formal Goodfellow and Reed readings.

---

#### 1. What Neural Networks Do

- **Pattern recognition:** Neural networks learn numerical patterns in vectorised data such as images, text, sound, and time series.
- **Classification:** Learn mappings from labelled examples to labels such as spam/not spam or positive/negative sentiment.
- **Clustering:** Group unlabelled examples by similarity.
- **Regression / predictive analytics:** Learn continuous or future-oriented outputs from historical inputs.
- **Automatic feature extraction:** Deep networks can learn useful feature hierarchies rather than requiring all features to be hand-engineered.

| Task type | Example |
|---|---|
| **Classification** | Detect faces, classify sentiment, label fraud |
| **Clustering** | Group similar documents, images, or audio |
| **Anomaly detection** | Detect unusual behaviour or failures |
| **Regression** | Predict churn, equipment breakdown, or time-series values |

#### 2. Neural Network Elements

- **Node:** A computation point that combines weighted inputs, adds bias, and passes the result through an activation function.
- **Weights:** Parameters that amplify or dampen signals.
- **Activation function:** Determines whether and how strongly a signal passes forward.
- **Layer:** A group of nodes whose outputs become the next layer's inputs.
- **Deep network:** A network with multiple layers that learns increasingly abstract feature hierarchies.

#### 3. Feedforward Learning and Gradient Descent

```text
input * weight = guess
ground truth - guess = error
error * contribution = adjustment
```

- **Feedforward pass:** Inputs move through the model to produce a guess.
- **Loss/error:** The guess is compared with the target label or value.
- **Weight update:** The model adjusts weights according to their contribution to the error.
- **Gradient descent:** Uses the relationship between weights and error to move parameters toward lower error.
- **Chain rule:** Enables error signals to be attributed back through layers, which aligns with the backpropagation process in Goodfellow.

#### 4. Output Layer and Classification

- **Logistic regression output:** Converts continuous network signals into probabilities for binary classification.
- **Decision threshold:** Determines whether a predicted probability becomes label `0` or `1`.
- **Tradeoff:** Lower thresholds can increase false positives; higher thresholds can increase false negatives.
- **Softmax connection:** For multiple labels, the same idea generalises to output probabilities across more than two classes.

#### Key Takeaways for DLE602

1. This resource is useful for plain-English explanations in discussion posts, especially when describing forward pass, error, and updates.
2. It reinforces that neural networks need the right data and task framing before architecture matters.
3. For Activity 2, the guide's feedback-loop framing can be paired with Goodfellow's precise distinction between backpropagation and optimisation.
4. For Activity 3, the guide supports a balanced critique: neural networks are powerful but can be inefficient, data-hungry, and not inherently interpretable.
