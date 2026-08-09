# Module 11 - The Perceptron

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Watch & summarise Art of the Problem (2019) - history of neural networks / the perceptron | ✅ |
| **2** | Read & summarise Bhardwaj (2020) - What is a Perceptron? Basics of Neural Networks *(local PDF; see citation note)* | ✅ |
| **3** | Listen & summarise Golden (2014) - LM101-015: How to build a machine that can learn anything | ✅ |
| **4** | Listen & summarise Kennedy et al. (2017) - Data Skeptic: The Perceptron | ✅ |
| **5** | Watch & summarise Ritvikmath (2019) - Perceptron (manual walkthrough) | ✅ |
| **6** | Read & summarise Lang (2024) - Activation Functions in Neural Networks *(local PDF; see citation note)* | ✅ |
| **7** | Read & summarise Forsyth (2014) - The Noble Perceptron | ✅ |
| **8** | Read & summarise Rosenblatt (1958) - The Perceptron: A Probabilistic Model (original paper) | ✅ |
| **9** | Read & summarise Roach (2016) - Training a Perceptron Model in Python | ✅ |
| 10 | Activity 1: Perceptron Settings (`a1_..._perceptron_with_visualization.ipynb`) - forum | 🔥 |
| 11 | Activity 2: Interactive perceptron demos (owenshen24 / TF Playground / Khan) - forum | 🕐 |

> **One-line frame:** the **perceptron** (Rosenblatt, 1958) is the *first trainable* artificial neural network
> (McCulloch-Pitts, 1943, modelled a neuron; Rosenblatt's is the one that **learns**) and the
> atom every deep net is built from: **inputs × weights + bias → weighted sum → activation → output**. It learns
> by nudging weights after each misclassified example (`w ← w + η·(target − pred)·x`). It **converges to a
> zero-error separator only when the data is linearly separable** (Perceptron Convergence Theorem); on
> non-separable data there is **no such guarantee** - the updates can cycle, so you cap the epochs. Its
> famous failure (**XOR** / Minsky-Papert, 1969) is fixed by **stacking layers** + swapping the hard **step**
> activation for a **smooth** one (sigmoid/tanh/ReLU) so error can be back-propagated - which is exactly the road
> to deep learning.

> ℹ️ **Citations reconciled to the files on hand.** Resources **2** and **6** are cited (here and in `notes.md`)
> as the PDFs actually on file - **Bhardwaj (2020)** "What is a Perceptron?" and **Lang (2024)** "Activation
> Functions in Neural Networks". The original module brief listed **Sharma (2017)** for both (same topics,
> different authors/years); swap back to the Sharma sources if you prefer the brief's exact references.

---

## Key Highlights

### 1. Art of the Problem (2019). The history of neural networks / the perceptron.

**Citation:** Art of the Problem. (2019, 14 November). *The beauty of deep neural networks (the pattern machine part 3)* [Video]. https://www.youtube.com/watch?v=r1U6fenGTrU

**Purpose:** The "why it matters" arc - traces the whole idea from biological neurons to Rosenblatt's machine to
modern deep learning, and pinpoints the *two* changes that turned a 1958 toy into today's technology.

---

#### 1. From brain to machine
- Two modes of thought: **intuitive** (fast, felt) vs **logical** (slow, stepwise). Classic computers automated
  the logical side; **neural networks** were built to automate **intuition** - sensing the world from experience.
- **Neuron as a switch:** biology showed the brain is a mesh of **neurons** that fire past a threshold.
  **McCulloch & Pitts** modelled a neuron as an electrical switch: sum weighted inputs; if they clear a
  **threshold**, fire the output. Wire enough together → any logical function.
- **Distributed representation:** a concept ("cat") isn't one neuron - it's a **pattern of many neurons firing
  together** (like a musical **chord** vs a single note). Meaning separates out layer by layer.

#### 2. Rosenblatt's perceptron (1958)
- Three layers: **sensory units** (read the retina/pixels) → **association units** (random connections) →
  **response units** (one output per class, wired to a light).
- **Learning = turning knobs (weights).** Show an example; if the output is wrong, wiggle the connection weights
  to force the correct output neuron on. Repeat until no tuning is needed - Rosenblatt called that
  **generalization/abstraction**.
- **The failure:** move/rotate the shapes so same-class images share no pixels → the single-layer net breaks.
  **Adding a new layer** let it solve harder problems - *"adding more layers gives more abstraction power"* - the
  essence of **deep learning**.

#### 3. The two advances that unlocked deep learning
| Change | From → To | Why it mattered |
|---|---|---|
| **Activation** | binary **step** → **smooth** (gradual) | wiggling a weight now gives a *proportional* change → you learn **direction AND magnitude** of error → tune all weights **as a batch** (backprop), millions× more efficient |
| **Hardware** (~2009) | CPU → **GPU** | parallel math → 10-50× faster → the "**Big Bang** of deep learning" |

#### Key Takeaways for MLN601
1. The perceptron is the **historical + structural root** of everything in your DLE602 CNN work - this module is
   the bridge from shallow ML to deep learning.
2. **Step → smooth activation** is the single conceptual hinge (it makes **backpropagation** possible) - links
   straight to Resource 6 (activation functions).
3. **More layers = more abstraction** but originally **untrainable** (too slow) - the tension that Resource 3's
   Minsky-Papert story and the XOR problem make concrete.

---

### 2. Bhardwaj, A. (2020). What is a Perceptron? Basics of Neural Networks.

**Citation:** Bhardwaj, A. (2020, 11 October). *What is a perceptron? - Basics of neural networks*. Towards Data Science. *(Original module brief listed Sharma (2017) - see the citation note above.)*

**Purpose:** The clean mechanical definition - the four parts of a perceptron and how they combine into a
decision boundary. The best "draw-it-yourself" resource.

---

#### 1. The four parts
1. **Input values** `x1…xn`
2. **Weights + a bias** `w1…wn`, `b` (bias = the threshold the sum must clear)
3. **Weighted sum** `Σ wᵢxᵢ`
4. **Activation function** → maps the weighted sum + bias to the final output

- **History note:** introduced by **Frank Rosenblatt, 1957, Cornell Aeronautical Laboratory**; first ran as
  software on an **IBM 704**, later custom hardware for image recognition. Early optimism collapsed when it was
  shown to be **only linearly separable** → poor pattern recognition → public lost interest. Modern fix =
  **activation functions** (non-linearity).

#### 2. From weighted sum to a decision boundary
- Raw **weighted sum** can be any number; an **activation function** squashes it into a useful range (e.g.
  **logistic** → 0-1, **tanh** → −1-1) and enables **non-linear** classification.
- **Binary classifier example:** with `wx=−0.5, wy=0.5, b=0`, the boundary `−0.5x + 0.5y = 0` (i.e. `y = x`) is
  the **decision boundary**; a **step** activation labels one side `1`, the other `0`.
- The perceptron is used for **supervised learning of binary classifiers** - the building block of neural nets.
- Teaser: the **"perceptron trick"** learns good weights automatically (the update rule, covered in Resources 5 & 9).

#### Key Takeaways for MLN601
1. Memorise the pipeline: **inputs × weights → + bias → weighted sum → activation → output.** This is the
   single most testable diagram in the module.
2. **Bias = threshold**, and it's what lets the boundary shift off the origin - connects to Resource 9's trick of
   folding the threshold in as `w0` with `x0 = 1`.
3. **Linearly separable only** (without non-linear activations) - the limitation every other resource circles back to.

---

### 3. Golden, R. (2014). LM101-015: How to build a machine that can learn anything (The Perceptron).

**Citation:** Golden, R. (2014, 27 October). *LM101-015: How to build a machine that can learn anything (The Perceptron)* [Audio podcast]. Learning Machines 101. https://www.learningmachines101.com/lm101-015-perceptron/

**Purpose:** The deep, theory-rich account - where the perceptron came from, the **Perceptron Learning Theorem**,
its two fundamental limitations, and how **SVM and logistic regression** are its close cousins that address those
limitations in different ways (they share the linear-neuron lineage, *not* the same objective or guarantee).

---

#### 1. Foundations: McCulloch-Pitts → Rosenblatt
- **McCulloch-Pitts formal neuron (1943):** a brain-cell model that acts like a **logic gate / IF-THEN rule** -
  invented *before* the first digital computer. Enough MP-units → **any** logical function (representation).
- **Problem:** representation ≠ knowing *which* rules you need. **Rosenblatt** (Air Force-funded, late 1950s)
  wanted a net that **learns from experience** → the **Perceptron**: input (sensor) → association (**hidden**,
  random fixed connections) → response (output, **modifiable** connections).

#### 2. The Perceptron Learning Rule + Theorem
- **Rule:** compare actual vs desired output. If actual **<** desired → **increase** weights from active hidden
  units; if actual **>** desired → **decrease** them. Update **after every example**; order doesn't matter if each
  is shown enough.
- **Perceptron Learning Theorem (Rosenblatt, 1962):** *if* a correct classification of all patterns is
  **possible**, the rule will **eventually** find it.
- **Two fundamental limitations:**
  1. **Assumes a solution exists** - no guarantee otherwise.
  2. **It's about memorization, not generalization** - guarantees it fits the *training* stimuli, says nothing
     about unseen inputs.

#### 3. XOR, Minsky-Papert, and the cousins
| Model | How it relates | What it fixes |
|---|---|---|
| **Perceptron** | single MP-unit output | baseline; memorizes, needs separability |
| **SVM** (Vapnik, ~1960s→90s) | output is an MP-unit ±1; **max-margin** boundary | **soft margin** permits errors on non-separable data; the margin aids generalization |
| **Logistic regression** | **sigmoidal** MP-unit → probability 0-1 | outputs **probabilities** (not a hard label); a smoother, probabilistic view of the same boundary |

- **XOR / the poisonous-flowers problem:** color and size *alone* can't decide edibility (large-purple &
  small-yellow poisonous; the other two safe) → a **single** neuron faces an **algebraically inconsistent** system
  → **impossible**. Add **one hidden unit** (active when both sensors fire) → solvable.
- **Overselling:** 1958 press called it a "human being without a life"; **Minsky & Papert (1969)** *Perceptrons*
  gave a realistic (often misquoted-as-pessimistic) appraisal → funding/attention shifted away → the first "AI
  winter" for neural nets. **Lesson: give conservative estimates.**

#### Key Takeaways for MLN601
1. **Perceptron ≈ SVM ≈ logistic regression** - same MP-neuron lineage, equivalent in special cases. Ties this
   module straight back to Modules 6 (SVM) and 8 (logistic regression).
2. **Memorization vs generalization** is the exam-grade distinction - and it's *exactly* the gap PAC (Module 10)
   formalises. Perceptron Theorem = memorization guarantee; PAC = generalization guarantee.
3. **XOR needs a hidden layer** - the concrete reason single-layer perceptrons are limited and multilayer nets exist.

---

### 4. Kennedy, M., Jaffe, B. & Malone, K. (2017). The Perceptron (Data Skeptic mini-episode).

**Citation:** Kennedy, M., Jaffe, B. & Malone, K. (2017, 10 March). *The perceptron* [Audio podcast]. Data Skeptic. https://podtail.com/en/podcast/data-skeptic/mini-the-perceptron/

**Purpose:** The plain-English one-minute overview - the five defining features of the algorithm, stated simply.

---

#### 1. The five characteristics
- **Online updates:** adjusts weights **after every example**, not as a batch.
- **Step activation function** (hard threshold).
- **Linearly separable data only.**
- **Convergence guaranteed** *if* the data meets that criterion.
- **Very efficient** - simple algorithm, runs fast.
- **The real power is multi-layer** perceptron networks (not covered in the mini-episode, but the reason the
  technique matters).

#### Key Takeaways for MLN601
1. A perfect **memory hook / revision checklist**: *online, step, linear-only, converges-if-separable, efficient.*
2. **Online (per-example) updates** contrast with batch gradient descent - a distinction worth stating out loud.
3. Confirms Resource 3's punchline: the single perceptron is a stepping stone; **multilayer** is the destination.

---

### 5. Ritvikmath (2019). Perceptron (manual walkthrough).

**Citation:** Ritvikmath. (2019, 30 January). *Perceptron* [Video]. https://www.youtube.com/watch?v=4Gac5I64LM4

**Purpose:** The **worked-by-hand** resource - real numbers for the parameters, the classification rule, and the
weight-update step. This is the one to replicate on paper.

---

#### 1. Parameters & inputs
- **Use it when:** the data is **linearly separable** (a line/plane/hyperplane can split the classes).
- **`ω` (omega)** = weight vector of length **(dimensions + 1)** - the extra slot is the **constant/bias** term
  (`ω₀`); the matching input `x₀` is always **1**.
- **`ν` (nu)** = **learning rate.** High → fast steps but overshoots; low → slow but fewer mistakes.

#### 2. Classify, then update
- **Classify:** take the **dot product** `ω·x` (= `ωᵀx`). If **> 0** → class A ("X"); if **≤ 0** → class B
  ("triangle"). The boundary `ω·x = 0` is a **line** (e.g. `ω=(0,1,0.5)` → `x₂ = −2x₁`).
- **Update rule (per misclassified point):**
  ```
  ωᵢ' = ωᵢ + ν · D · xᵢ
  ```
  where **`D = +1`** if the point should be in the upper set, **`−1`** if lower. Recompute the line; a fix can
  briefly break a previously-correct point, but you **loop** until all correct or a **stopping criterion**
  (max iterations / distance) is hit.
- **Non-separable trick:** if a **circle** (not a line) separates the data, map to **polar coordinates** (r, θ) -
  the ring becomes linearly separable. (Foreshadows the **kernel trick**.)

#### Key Takeaways for MLN601
1. The **`ω ← ω + ν·D·x`** update is the algorithm's heart - know it cold; it's the same rule as Resource 9's
   `w += η·(target − pred)·x`.
2. **Bias-as-extra-dimension** (`x₀ = 1`) is why `ω` has `dim + 1` entries - a recurring implementation detail.
3. The **polar-coordinate** rescue = the intuition for why non-linear feature maps / kernels exist (ties to SVM,
   Module 6).

---

### 6. Lang, N. (2024). Activation Functions in Neural Networks: How to Choose the Right One.

**Citation:** Lang, N. (2024, 12 December). *Activation functions in neural networks: How to choose the right one*. Towards Data Science. *(Original module brief listed Sharma (2017) - see the citation note above.)*

**Purpose:** The activation-function catalogue - what they are, the properties that matter (non-linearity,
differentiability, saturation), the main functions, and how to pick one per layer.

---

#### 1. Why activation functions exist
- The neuron forms a **weighted sum**, then the **activation function** decides how strongly it fires. Without a
  **non-linear** activation, a whole network can only learn **linear** relationships.
- **Two required properties:** **non-linearity** (learn complex structure) and **differentiability** (so
  **backpropagation** can compute gradients and update weights).
- **Danger property - saturation / vanishing gradient:** where the curve flattens, gradients → ~0 and learning
  stalls.

#### 2. The functions (compare)
| Function | Range | Use / note | Weakness |
|---|---|---|---|
| **Linear** | (−∞, ∞) | output layer for **regression** | can't learn non-linear structure |
| **Sigmoid** | 0 → 1 | **binary** output as a probability | **vanishing gradient**; not zero-centred |
| **Tanh** | −1 → 1 | **zero-centred** → trains better; RNNs | still saturates / vanishing gradient |
| **ReLU** `max(0,x)` | 0 → ∞ | **default for hidden layers**; cheap, no vanishing gradient | **dying ReLU** (20-50% of neurons can go dead), unbounded |
| **Leaky ReLU** | (−∞, ∞) | small negative slope `α` (e.g. 0.01) → prevents dead neurons | extra hyperparameter `α` |
| **Softmax** | 0 → 1, Σ=1 | **multi-class** output layer (probabilities) | overconfident; costly for many classes |

#### 3. How to choose
- **Hidden layers → ReLU / Leaky ReLU** (efficient, no vanishing gradient).
- **Output layer → match the task:** **sigmoid** (binary), **softmax** (multi-class), **linear** (regression).

#### Key Takeaways for MLN601
1. The perceptron's original **step** function is the *degenerate* activation; everything here explains **why we
   replaced it** (differentiability → backprop → deep learning) - direct payoff of Resource 1's "step → smooth" hinge.
2. **Hidden = ReLU, output = task-specific** is a rule of thumb you'll reuse in every DLE602 network.
3. **Vanishing gradient** and **dying ReLU** are the two failure modes worth naming - they explain many training
   pathologies.

---

### 7. Forsyth, J. (2014). The Noble Perceptron.

**Citation:** Forsyth, J. (2014, 29 January). *The noble perceptron* [Web log post]. https://jaredforsyth.com/posts/the-noble-perceptron

**Purpose:** The **applied** resource - the perceptron on real datasets (heart attack, US voting, Iris), with
honest results including where it fails.

---

#### 1. The intuition + the math
- **Binary classification of linearly separable classes:** find a line/hyperplane, then classify new points by
  which side they fall on. Boundary: `x₁w₁ + x₂w₂ + … = 0`; weights indicate each feature's usefulness.
- **Always split train/test** so final accuracy is measured on unseen data.
- **Heart-attack example:** predict a second heart attack from **BP + BMI** (real world → a dozen features).

#### 2. Real datasets, real results
| Dataset | Setup | Result |
|---|---|---|
| **US 1984 voting** (16 features) | 70-30 split, 5 random runs | **~93%** avg accuracy; weights reveal partisan votes |
| **Iris** (4 measurements, 3 species) | **3 perceptrons vote** (one-vs-one) | first two species → **100%** after 2 epochs |
| → Iris hard pair | versicolor vs virginica | overlap → **not** linearly separable → **~89%** |
| **Dataset #8** (JS demo) | not separable | perceptron **never settles** - bounces forever |

- **Stopping criterion:** quit when fully classified **or** no accuracy gain for **20 epochs**.

#### Key Takeaways for MLN601
1. **Non-separable data → the perceptron never converges** (Iris versicolor/virginica; JS dataset #8) - the
   single most important practical caveat, seen in real numbers.
2. **One-vs-one voting** extends a binary perceptron to **multi-class** - a useful pattern.
3. **70-30 split + multiple random runs** = the same honest-evaluation discipline PAC (Module 10) justifies and
   your assessments demand.

---

### 8. Rosenblatt, F. (1958). The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain.

**Citation:** Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. *Psychological Review, 65*(6), 386-408.

**Purpose:** **The original paper.** Read it for how a field is *founded* - Rosenblatt frames the perceptron not
as an engineering gadget but as a **probabilistic theory of how brains store and organise information**.

---

#### 1. The big question + his stance
- Three foundational questions: how is information **sensed**, **stored**, and how does storage **influence
  behaviour**? He tackles storage + influence.
- **Two camps:** **coded-memory** (store a one-to-one image of the stimulus) vs **connectionist/empiricist**
  (store nothing pictorial; memory = **new connections/pathways**). Rosenblatt takes the **connectionist**
  side - *"information is contained in connections or associations rather than topographic representations."*
- **Why probability, not Boolean logic:** he wants to analyse a network with **many random connections** where
  only the **gross organisation** is known - Boolean algebra (McCulloch-Pitts style) can't handle that, so he
  builds the theory in **probability theory** → the notion of **statistical separability**.

#### 2. The architecture (S → A → R)
| Layer | Name | Role |
|---|---|---|
| **S-points** | sensory units | stimuli hit a **retina**; respond all-or-nothing |
| **A-units** | association cells (projection area Aᵢ + association area Aₙ) | receive **random** connections from S; the feature detectors |
| **R-units** | responses | one per class; connected to a **source-set** of A-units; **feedback** (excitatory to own set / inhibitory to the complement) |

- Connections **S → A are random & fixed** (modelling genetic/evolutionary wiring); **A → R are modifiable** by
  **reinforcement** - the part that learns.
- **Learning = reinforcement** of the weights between active A-units and the correct R-unit.

#### Key Takeaways for MLN601
1. The perceptron was born as a **theory of the brain**, not a classifier - the "neural" in neural network is
   literal here (ties to Resource 1's biological framing).
2. **Random fixed input layer + trainable output layer** is Rosenblatt's actual design - Resource 3 notes most
   modern textbooks *simplify* this to a single neuron, losing the two-layer origin.
3. **"Statistical separability" / probabilistic framing** prefigures **PAC** (Module 10) - learning as a
   probabilistic guarantee, not a logical certainty.

---

### 9. Roach, J. (2016). Training a Perceptron Model in Python.

**Citation:** Roach, J. (2016, 24 September). *Training a perceptron model in Python* [Web log post]. https://johnpatrickroach.com/2016/09/24/training-a-perceptron-model-in-python/

**Purpose:** The **implementation** resource - walks the perceptron from math to a working `Perceptron` class
(from Raschka's *Python Machine Learning*), trained on Iris. This is the code pattern for **Activity 1**.

---

#### 1. Math → code
- **Net input** `z = w₀x₀ + w₁x₁ + … + wₘxₘ`, with the **threshold folded in** as `w₀ = −θ`, `x₀ = 1` (so the
  rule is just `Φ(z) = 1 if z ≥ 0 else −1`) - the **unit step** activation.
- **Algorithm:** (1) init weights to 0 / small random; (2) for each sample, predict and **update if wrong**:
  `Δw = η·(target − predicted)·x`, learning rate **η ∈ (0,1)**. All weights update **simultaneously**.
- **Convergence needs linear separability**; otherwise cap **`n_iter`** (max passes) and/or tolerate some
  misclassifications.

#### 2. The `Perceptron` class (OOP)
| Method | Does |
|---|---|
| `__init__(self, eta=0.01, n_iter=10)` | store learning rate **η** + number of passes |
| `fit(self, X, y)` | init `w_ = zeros(1 + n_features)`; loop `n_iter`, apply update rule, track `errors_` per pass |
| `net_input(self, X)` | `np.dot(X, w_[1:]) + w_[0]` (= `z`) |
| `predict(self, X)` | `np.where(net_input(X) >= 0, 1, -1)` (step) |

- **Iris demo:** 100 samples, 2 features (sepal + petal length), labels ±1 → **converges at iteration 6 with 0
  misclassifications**; plotting `errors_` per epoch shows the descent.

#### Key Takeaways for MLN601
1. `errors_` per epoch is the diagnostic to watch - it's what **Activity 1**'s notebook visualises (net sum,
   weights, bias, activation).
2. `w_[0]` (the **bias**) is handled separately from `w_[1:]` - the concrete version of Resource 5's `ω₀`/`x₀=1`
   trick.
3. **`eta` and `n_iter` are the two knobs** you'll tune in the activities - exactly the hyperparameters the forum
   questions ask you to reason about.

---

## Synthesis - how the nine fit together

```
   HISTORY / WHY                THE MECHANISM                 THE LIMIT & THE FIX
 brain → neuron → NN         inputs·weights + bias         linearly separable ONLY
  (Art of Problem R1)         → sum → activation            → non-separable never
   Rosenblatt's S-A-R          (Bhardwaj R2)                  converges (Forsyth R7)
    original (R8)                                             XOR needs a hidden
                             classify: sign(w·x)              layer (Golden R3)
 McCulloch-Pitts → SVM       update: w += η·(t−p)·x
  → logistic regression       (Ritvikmath R5, Roach R9)     step → smooth activation
   cousins (Golden R3)                                       (sigmoid/ReLU/softmax)
                             5 traits: online, step,          = backprop = deep
 memorization not             linear-only, converges,         learning (Lang R6,
  generalization (R3)         efficient (Data Skeptic R4)     Art of Problem R1)
```

**The through-line:** Module 11 is the **"atom of deep learning"** module. A perceptron is
`inputs × weights + bias → activation → output`, trained by the online rule `w ← w + η·(target − pred)·x`. It is
**guaranteed to converge on linearly separable data** (Perceptron Convergence Theorem) and has **no convergence
guarantee** otherwise (the updates can cycle) - the **XOR** problem that stalled the field until **multilayer
networks + smooth, differentiable activations** made **backpropagation** possible. It shares the linear-neuron
lineage with **SVM** (max-margin, soft margin tolerates errors) and **logistic regression** (sigmoid →
probability) - related, but not the same guarantee - and its "memorization not generalization" result is the foil to
**Module 10's PAC** (generalization). Practically, everything converges on **Activity 1's notebook**: tune **η**
and **n_iter**, watch the errors-per-epoch curve, and reason about which settings matter.

> **Lecturer context (Week 10 live session):** Dr Kamran flagged the perceptron as *"very simple, a starting
> point for a neural network"* and the bridge into your **CNN / deep-learning** work. He'll also fold in two
> **off-curriculum** unsupervised topics next class - **anomaly/outlier detection** and **association analysis
> (a priori algorithm)** - worth knowing as "graduate general knowledge." See
> [module10_notes-class.md](../module-10-learning-theory-pac/module10_notes-class.md) §2.

---

## Learning Activity 1 - Perceptron Settings (forum draft)

> **Deliverable:** run `a1_MLN601_Module11_perceptron_with_visualization.ipynb` (Iris, setosa vs versicolor,
> features = sepal length + petal length), then post on (1) the best settings, (2) which settings mattered
> most, (3) other observations. The numbers below come from a reproducible sweep,
> [`a1_perceptron_settings_sweep.py`](a1_perceptron_settings_sweep.py), which reuses the notebook's exact
> `Perceptron` class. Figure: [`a1_perceptron_settings_sweep.png`](a1_perceptron_settings_sweep.png).

**The numbers I got (50-epoch cap unless noted):**

| Setup | Learning rate | Converged? | Epoch it converged |
|---|---|---|---|
| **Zero init** | 0.0001 → 1.0 (all five) | Yes | **6, every time** |
| **Random init** (seed 1) | 0.0001 | Yes | 42 |
| **Random init** | 0.001 | Yes | 5 |
| **Random init** | 0.01 - 0.1 | Yes | **2** |
| **Random init** | 1.0 | Yes | 5 |
| **Not-separable pair** (versicolor vs virginica) | any | **No** | never - stuck at 2 errors forever |

*num_iterations sweep (zero init, lr 0.01):* a cap below 6 never finishes; a cap of 10, 50 or 500 all land on
epoch 6. It is a budget, not a dial.

---

**My post:**

I expected the learning rate to be the big lever. It was not. Here is what actually moved the result.

**The setting that mattered most was the starting weights, not the learning rate.** When I initialised the
weights to zero, the perceptron converged at **epoch 6 for every learning rate I tried, from 0.0001 all the way
to 1.0** - the learning rate made literally no difference. That surprised me until it clicked: from a zero
start, every weight ends up as the learning rate times the same set of numbers, and the classification only
looks at the *sign* of the weighted sum. Scaling all the weights by a constant does not change any sign, so you
get the identical boundary and the identical number of epochs. The learning rate is a red herring for a
perceptron that starts from zero on separable data.

**The learning rate only started to matter once I initialised the weights randomly.** With a random start it
swung the convergence time hard: `0.0001` took **42 epochs** (too small - it can barely overwrite the bad random
starting point), `0.01`-`0.1` snapped to **2 epochs**, and `1.0` bounced back up to **5**. So the sweet spot was
in the middle. Too small is slow, too large overshoots.

**Best settings, and why:** zero-initialised weights, a mid-range learning rate (I would use `0.01`), and
`num_iterations` set comfortably above the convergence epoch (50 is fine). Justification: zero init is the
robust, reproducible choice because it converges in the fewest epochs *regardless* of the learning rate, so
there is no learning rate to tune and everyone gets the same answer. `num_iterations` is not really a tuning
knob - anything below 6 failed to finish, and 10, 50 and 500 all gave the same epoch-6 result. Set it high
enough to be safe and forget it.

**Other observations:**
- **Linear separability beats every hyperparameter.** On the hard pair (versicolor vs virginica, which overlap),
  *no* setting converged - it sat at 2 misclassifications forever, at every learning rate. No amount of tuning
  fixes non-separable data; you need a different model (an SVM soft margin, or a multilayer network). This is the
  single most important practical lesson.
- **The error count does not fall smoothly.** Even on the easy pair it wobbled (1, then 3, then 3, then 1)
  before snapping to 0 at epoch 6, because fixing one misclassified point can briefly break a point that was
  already correct.
- **Day-job connection:** if I framed a St Catherine's "flag an at-risk student" model as a perceptron on two
  features, this activity says the honest first question is not *what learning rate?* but *are these two features
  even linearly separable?* If the classes overlap - which real attendance/engagement data almost always does -
  the perceptron will never settle and I should reach for a soft-margin or multilayer model instead.

**How to reproduce:** `python3 a1_perceptron_settings_sweep.py` (Homebrew python3.14; numpy/pandas/sklearn/
matplotlib). It prints all three sweep tables and saves the errors-per-epoch figure.
