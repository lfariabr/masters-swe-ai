# Module 12 - Practical Methodologies and the Future of Deep Learning

> Key Highlights from the Module 12 resources: define success, establish a baseline, diagnose errors, iterate with evidence, and understand the research directions that may extend deep learning beyond pattern recognition.

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow et al. (2016) - Practical Methodology (Ch.11) | ✅ |
| **2** | Read & summarise Smith (2017) - Best Practices for Novel DL Applications | ✅ |
| **3** | Read & summarise Sejnowski (2020) - The Unreasonable Effectiveness of Deep Learning | ✅ |
| **4** | Read & summarise Chollet (2017) - The Future of Deep Learning | ✅ |
| 5 | Activity 1: Last Opinion - error analysis as practical methodology | 🕐 |
| 6 | Activity 2: The Future is Here - propose a currently infeasible DL application | 🕐 |
| 7 | Activity 3: Discussion - strongest, hardest, and weakest DL topics | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning - Chapter 11: Practical Methodology.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning*. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/ (Chapter 11)

**Purpose:** Presents a disciplined process for developing deep learning systems. Its central claim is that correctly applying a common algorithm usually matters more than sloppily applying an obscure one.

---

#### 1. The practical design loop

```text
Define goal + metric
        ↓
Build end-to-end baseline
        ↓
Instrument + diagnose bottleneck
        ↓
Make one evidence-based change
        ↓
Measure again and repeat
```

- **Define the goal first:** choose a performance metric and a realistic target based on the real application, safety needs, cost, human performance, or published benchmarks.
- **Build end-to-end early:** a working baseline exposes integration, data, evaluation, and deployment problems that isolated model experiments hide.
- **Instrument before changing:** determine whether the bottleneck is underfitting, overfitting, optimisation, data quality, preprocessing, evaluation, or software defects.
- **Iterate incrementally:** gather data, alter capacity, tune hyperparameters, change regularisation, or replace an algorithm only when diagnostics support that action.

#### 2. Metrics must represent the real objective

| Metric | Use it when | Main warning |
|---|---|---|
| **Accuracy / error rate** | classes and mistake costs are reasonably balanced | misleading for rare classes |
| **Precision** | false positives are costly | can improve by predicting fewer positives |
| **Recall** | missing a true event is costly | can improve by predicting more positives |
| **F1** | one score must balance precision and recall | hides the selected decision threshold |
| **Coverage** | the model may abstain and defer to a human | 100% accuracy is trivial at 0% coverage |

- **Training objective versus evaluation metric:** the differentiable loss guides weight updates; the evaluation metric decides whether the deployed system solves the actual problem.
- **Asymmetric cost:** a blocked legitimate email may cost more than permitted spam. The metric should reflect that imbalance.
- **Rare-event example:** a classifier that always predicts "no disease" can achieve 99.9999% accuracy while detecting nobody.
- **Abstention:** Street View targeted human-level **98% accuracy** while maximising coverage, with a project target of **95% coverage**.

#### 3. Choose a sensible baseline

| Data/problem structure | Starting model suggested by the chapter |
|---|---|
| A few fixed-size features and possibly linear boundary | logistic regression or simple statistical model |
| Fixed-size vectors requiring nonlinear modelling | feedforward network |
| Images or known grid topology | convolutional network |
| Sequential inputs or outputs | gated recurrent network such as LSTM or GRU |
| Closely related solved task | copy the established architecture and consider transfer learning |

- **Optimisation defaults:** SGD with momentum and learning-rate decay, or Adam; add batch normalisation when optimisation is difficult.
- **Regularisation defaults:** use early stopping almost universally and mild regularisation unless the dataset contains tens of millions of examples.
- **Transfer instead of reinvention:** reuse a trained model when the new task resembles an established application.

#### 4. Diagnose before gathering data or changing architecture

| Training result | Validation/test result | Likely diagnosis | Next action |
|---|---|---|---|
| Poor | Poor | underfitting, failed optimisation, bad inputs, or software defect | fit a tiny set; tune learning rate; increase capacity; inspect data/code |
| Good | Poor | overfitting or train/test pipeline mismatch | regularise, gather representative data, verify evaluation path |
| Good | Good | target reached | stop or reconsider whether further gains justify the cost |

- **More data is not always the answer:** if the model cannot fit the current training data, new examples do not fix its capacity, optimisation, implementation, or input-quality problem.
- **Learning curves:** double dataset sizes on a logarithmic scale to estimate whether additional data will materially reduce generalisation error.
- **Capacity trade-off:** aim for the lowest generalisation error under runtime and memory constraints, not simply the largest network.

#### 5. Hyperparameter selection and debugging

- **Learning rate first:** if only one hyperparameter can be tuned, tune the learning rate. Too large can diverge; too small can train slowly or remain stuck.
- **Grid search:** reasonable for roughly three or fewer hyperparameters, but cost grows exponentially with dimensions.
- **Random search:** usually explores influential hyperparameters more efficiently because every trial tests new values instead of repeating irrelevant grid combinations.
- **Debugging toolkit:** visualise predictions and worst errors; fit one or a few examples; compare analytical and numerical gradients; monitor activation and gradient histograms; verify train/test preprocessing consistency.
- **Street View lesson:** the highest-confidence errors revealed crops that removed digits. Widening the crop improved coverage by **10 percentage points**, a data-pipeline fix, not a novel architecture.

#### Key Takeaways for Deep Learning (DLE602)
1. Module 12 turns the entire subject into an engineering loop: metric → baseline → diagnosis → controlled change → measurement.
2. ReviewPulse v3 follows this methodology through one shared evaluation contract, review-only baselines, aspect-conditioned models, error subsets, confusion matrices, latency, and artifact-size evidence.
3. The strongest final-project discussion is not "DistilBERT won" but why it won, what it cost, where all models failed, and which next experiment the evidence justifies.

---

### 2. Smith, L. N. (2017). Best Practices for Applying Deep Learning to Novel Applications.

**Citation:** Smith, L. (2017). *Best practices for applying deep learning to novel applications*. Retrieved from https://arxiv.org/ftp/arxiv/papers/1704/1704.01568.pdf

**Purpose:** Guides domain experts who are new to deep learning through a phased project process. It adds domain analogy, reproducibility, visual diagnostics, and deliberate scope escalation to Goodfellow's methodology.

---

#### 1. Seven iterative phases

| Phase | Core question | Deliverable |
|---|---|---|
| **1. Prepare** | Is DL worthwhile and what does success mean? | metrics, targets, assumptions, compute budget |
| **2. Prepare data** | Is the dataset relevant, diverse, balanced, and representative? | train/validation/test data and preprocessing |
| **3. Find an analogy** | Which solved DL problem is structurally closest? | literature, code, reproducible reference result |
| **4. Simple baseline** | What is the smallest end-to-end system that works? | reproducible baseline |
| **5. Visualise/debug** | Why is the system producing these results? | diagnostics, unit tests, error analysis |
| **6. Fine-tune** | Which controlled changes improve the stated metrics? | architecture, loss, regularisation, hyperparameter evidence |
| **7. Add complexity** | Does the remaining gain justify ensembles or end-to-end complexity? | justified advanced system or a decision to stop |

- **Iteration is expected:** later findings may force a return to metrics, data, or problem framing.
- **Do not choose DL for fashion:** compare its likely benefit with the current state of the art, human performance, labelled-data availability, training cost, and project value.

#### 2. Make the network's job easier

- **Use prior knowledge carefully:** normalisation, relevant preprocessing, physics, or established heuristics can reduce the function the model must learn.
- **Avoid unnecessary human feature engineering:** the point of representation learning is to let the network discover useful structure where manual design is expensive or brittle.
- **Limited data:** use transfer learning, domain adaptation, synthetic data, or the closest available pretraining dataset.
- **Representative coverage:** class balance alone is not enough; examples must cover the expected problem space.

#### 3. Analogy before architecture

- **Experts reuse:** find the closest existing application, reproduce its published result where possible, and understand its code before modifying it.
- **Match problem structure:** images suggest CNNs; sequences suggest RNN/LSTM/GRU; similarity tasks may suggest Siamese networks; complex decisions may suggest reinforcement learning.
- **Record differences:** the gap between the reference task and the new domain identifies what data, architecture, loss, or evaluation must change.

#### 4. Error analysis versus ablative analysis

| Analysis | Comparison | Question answered |
|---|---|---|
| **Error analysis** | current performance → perfect performance | What remaining failures prevent success? |
| **Ablative analysis** | baseline performance → current performance | Which added components actually created the gain? |

- **Activity 1 nuance:** error analysis is useful, but "perfect performance" may be impossible because of irreducible ambiguity, label noise, incomplete inputs, or Bayes error.
- **Practical recommendation:** compare current performance with a realistic target or human/reference ceiling, categorise failures, and prioritise categories by frequency, cost, and fixability.

#### Key Takeaways for Deep Learning (DLE602)
1. ReviewPulse's closest-task analogy is ABSA research, not generic binary sentiment. That analogy justifies SemEval data, aspect-conditioned inputs, ATAE-LSTM, and sentence-pair DistilBERT.
2. The canonical four-model ladder is methodologically sound: simple TF-IDF baseline → target-agnostic LSTM → aspect-aware ATAE-LSTM → pretrained Transformer, with GRU/CNN activated only after core gates passed.
3. Negative results are evidence. GRU and TextCNN failing to close the mixed-polarity gap supports the conclusion that changing the review-only encoder does not supply missing aspect information.

---

### 3. Sejnowski, T. J. (2020). The Unreasonable Effectiveness of Deep Learning in Artificial Intelligence.

**Citation:** Sejnowski, T. (2020). *The unreasonable effectiveness of deep learning in artificial intelligence*. Proceedings of the National Academy of Sciences. Retrieved from https://www.pnas.org/content/early/2020/01/23/1907373117

**Purpose:** Connects the history of neural networks with unresolved theoretical paradoxes and future research. It argues that deep learning succeeds in high-dimensional real-world problems despite conventional statistical and optimisation intuitions suggesting that it should not.

---

#### 1. From handcrafted rules to high-dimensional learning

- **Early symbolic AI:** handcrafted low-dimensional rules worked in controlled toy environments but did not scale to noisy, uncertain vision and language.
- **Perceptron:** Rosenblatt's single-layer model learned labelled linear classifications, but could not solve nonlinearly separable problems.
- **Multilayer revival:** Boltzmann machines and backpropagation showed in the 1980s that hidden-layer networks could be trained; backpropagation was more efficient but less biologically local.
- **Modern shift:** large datasets, parallel hardware, and scalable learning moved AI toward data-driven perception, language, prediction, and control.

#### 2. The high-dimensional paradoxes

| Conventional intuition | Deep learning observation |
|---|---|
| Too many parameters should overfit | overparameterised networks can generalise well |
| Nonconvex optimisation should get trapped | SGD often reaches useful solutions |
| One good optimum must be found | many different parameter settings perform well |

- **Saddle points:** in high-dimensional parameter spaces, many critical points are saddles, not bad local minima.
- **Many good solutions:** overparameterisation changes the search from a "needle in a haystack" to a "haystack of needles."
- **Theory gap:** we still lack a complete account of why SGD, architecture, inductive bias, and sample complexity combine so effectively.
- **Blessing of dimensionality:** high-dimensional geometry can provide useful routes and representations that low-dimensional intuition misses.

#### 3. Brain inspiration without brain equivalence

- **Useful inspiration:** cortex influenced layered, parallel, locally connected systems such as CNNs; dopamine reward-prediction signals influenced reinforcement-learning theory.
- **Important difference:** biological neurons, memory, sleep, communication, and control are far richer than artificial units.
- **Future systems problem:** autonomy may require lifelong learning, memory management, routing among specialist networks, planning, social intelligence, and stable updates without catastrophic forgetting.

#### 4. Future learning directions

- **Self-supervised learning:** learn from abundant raw sensory streams by predicting hidden or future information, without requiring large labelled datasets.
- **Imitation and generative learning:** acquire behaviour from demonstrations and model joint distributions capable of producing new examples.
- **Hybrid reasoning:** neural systems may need memory and algorithmic mechanisms for copying, sorting, navigation, planning, and general reasoning.
- **Caution:** current success does not imply that scaling today's architectures alone will produce artificial general intelligence; Sejnowski explicitly anticipates major breakthroughs.

#### Key Takeaways for Deep Learning (DLE602)
1. The paper explains why Module 4's simple "capacity causes overfitting" story needs nuance: modern overparameterised networks can exhibit benign or manageable overfitting.
2. ReviewPulse's DistilBERT result is part of this broader pattern: a large pretrained representation can generalise better than smaller models because capacity interacts with pretraining, optimisation, regularisation, and data structure.
3. Activity 2 should identify not just a futuristic product, but the missing learning, memory, reasoning, data, safety, or compute capability that prevents it today.

---

### 4. Chollet, F. (2017). The Future of Deep Learning.

**Citation:** Chollet, F. (2017). *The future of deep learning* [Web log post]. Retrieved from https://blog.keras.io/the-future-of-deep-learning.html

**Purpose:** Offers a deliberately speculative roadmap from pattern-recognition networks toward systems with abstraction, reasoning, automated design, lifelong learning, and reusable components.

---

#### 1. Current limitation: local generalisation

- **Geometric pattern matching:** contemporary deep networks learn smooth transformations that interpolate between examples similar to their training distribution.
- **Reasoning gap:** abstraction, systematic reasoning, explicit search, long-term memory, and extreme transfer often require algorithmic structure beyond a fixed differentiable mapping.
- **Proposed synthesis:** combine **geometric modules** for intuition/pattern recognition with **algorithmic modules** for logic, search, memory, and abstraction.

#### 2. Four future directions

| Direction | Proposed change | Intended benefit |
|---|---|---|
| **Models as programs** | add manipulable loops, branches, variables, memory, lists, graphs, and search | stronger abstraction and reasoning |
| **Beyond backprop alone** | combine gradients for differentiable modules with search/RL/evolution for discrete structures | train globally non-differentiable systems |
| **Automated ML** | learn architectures and weights in place of hand-tuning every design choice | reduce engineering labour and move humans toward goal/loss design |
| **Lifelong modular reuse** | reuse learned features, architectures, training procedures, and program-like subroutines | learn new tasks from little data and avoid starting from scratch |

- **Backprop remains useful:** Chollet does not predict the disappearance of gradients; he argues that they will be one component inside richer systems.
- **Modularity:** independently reusable subroutines could improve efficiency, transfer, and abstraction in the same way that software libraries do.
- **Meta-learning vision:** a system learns to assemble task-specific models from a library built across many previous tasks.

#### 3. The engineer moves up the value chain

- **Less knob turning:** automation can search hyperparameters and architectures where the objective is measurable.
- **More problem responsibility:** engineers still define data, objectives, constraints, safety, evaluation, and the ecosystem affected by predictions.
- **Loss functions as product specifications:** a mathematically optimised target is only useful when it correctly represents business and societal goals.

#### Key Takeaways for Deep Learning (DLE602)
1. Chollet's four directions provide a strong structure for Activity 2: identify which missing capability blocks the proposed future application.
2. ReviewPulse already demonstrates modular reuse at a small scale: shared data, training, inference, evaluation, and presentation interfaces allow several model families to be compared under one contract.
3. The future-facing lesson is not "bigger models solve everything." It is richer primitives, modular reuse, better objectives, stronger evaluation, and systems that generalise beyond familiar examples.

---

### How Module 12 connects to the assessments

- **Assessment 1 retrospective:** the n-gram classifier established a simple, reproducible baseline with explicit assumptions. Its limitations motivated learned representations and contextual models.
- **Assessment 2 progression:** the proposal defined the problem, research questions, model ladder, dataset, scope, and evaluation plan before implementation, matching the preparation and analogy phases.
- **Assessment 3 delivery:** ReviewPulse v3 applies the practical methodology directly: one shared test set and label contract, multiple baselines, aspect-conditioned models, mixed-polarity error analysis, confusion matrices, efficiency metrics, token evidence, regression tests, reproducible artifacts, and retained negative results.
- **Final critical-analysis angle:** DistilBERT leads predictive metrics but costs far more storage; ATAE-LSTM offers a smaller aspect-aware alternative; GRU/CNN results show that changing a review-only encoder does not repair missing aspect information. The next experiments should follow the measured gaps: multi-seed uncertainty, same-device efficiency, cross-domain evaluation, calibration/abstention, and automatic aspect extraction.
