# DLE602 Cumulative Quiz - Modules 1-12

**Time box:** 50 minutes

**Mode:** Closed book, written answers, then check the separate answer key

Do not open `cumulative-quiz-modules-1-12-answers.md` until every question has an answer. This is the full-course quiz - one question sampled from each of Modules 1-11, a lighter check on Module 12 (already covered in detail via the module notes, one-pager and its own follow-up quiz), and a synthesis question tying the pipeline together at the end.

## Questions

### 1. Module 1 - Representation over features (6 points)

In one sentence, explain what "learning layered representations" means and why it beats hand-built features. Then explain the technical link between the N-gram reading and Assessment 1.

### 2. Module 2 - Why depth needs nonlinearity (8 points)

Explain, using XOR as the example, why a single linear layer cannot solve every classification problem but a feedforward network with a hidden layer and a nonlinear activation can. Then state, in one sentence, what backpropagation actually computes and how it uses the chain rule.

### 3. Module 3 - The NLP arc (8 points)

Name the progression from n-grams to the deep-learning leap in NLP (two named techniques). Then explain, from the Zhao et al. (2018) reference paper, what GloVe-DCNN fuses together and roughly what accuracy it reached on the STS-Gold dataset.

### 4. Module 4 - The five regularisation levers (9 points)

Name Kukacka et al.'s five levers for regularisation. Then explain, in one sentence each, what L1 does differently from L2, and why dropout is described as "a cheap approximation to bagging an exponential ensemble."

### 5. Module 5 - What makes convolution work (9 points)

Name the three structural ideas (Goodfellow Ch.9) that make convolution effective on grid data, and explain in one sentence what each buys you. Then order these four architectures by year: ResNet, AlexNet, VGG16, GoogLeNet/Inception.

### 6. Module 6 - Four linear factor models (8 points)

Complete this table from memory:

| Model | What it separates / preserves |
|---|---|
| PCA | |
| Factor analysis | |
| ICA | |
| SFA | |

### 7. Module 7 - Autoencoders and PCA (9 points)

State the formal result linking undercomplete linear autoencoders trained with squared-error loss to PCA, and name whose proof it is. Then name the three regularised autoencoder variants covered in the module and, in one phrase each, what property each one enforces on the code `h`.

### 8. Module 8 - Why plain RNNs fail and how LSTM fixes it (9 points)

Explain why backpropagation through time on a plain RNN causes gradients to vanish or explode - name the specific mechanism. Then name the three LSTM gates and state, in one sentence, how the cell state's linear self-loop avoids the same failure mode.

### 9. Module 9 - A representation is relative to what (7 points)

Using the Roman-numeral example (or an equivalent of your own), explain why "a good representation" cannot be defined in the abstract. Then explain, in one sentence, how the specific 2006 greedy layer-wise pretraining procedure relates to modern self-supervised pretraining (name one example from NLP and one from vision).

### 10. Module 10 - Directed vs undirected graphical models (8 points)

State the factorisation formula for a directed graphical model and explain what kind of relationship it is naturally suited to representing. Then explain why exact inference in these models is typically intractable, and name two approximate techniques used to work around it.

### 11. Module 11 - Activations vs gradients, and the snow-leopard problem (9 points)

Explain the difference between what activations show you and what gradients show you about a network, and name the module's counterexample that visualises gradients during training. Then explain the "snow-leopard problem" and name the CNNComparator finding that is the same failure mode in a different dataset.

### 12. Module 12 - Loss vs metric (6 points)

In one sentence, distinguish the training loss from the evaluation metric. Then name one metric appropriate when a model may abstain and defer to a human, and explain briefly why that differs from optimising accuracy alone.

### 13. Synthesis - the sequential bottleneck across three modules (8 points)

Modules 8, 9 and 11 each touch the same underlying problem from a different angle: an LSTM's hidden state is a fixed-size summary that has to carry everything relevant across time. Referencing all three modules, explain: (a) why this is a representation problem (Module 9's framing), (b) what specifically fails during training as a result (Module 8's gradient mechanism), and (c) which Module 11 technique would let you see the failure happening, rather than just infer it from a loss curve.

## Score Guide

- **90-100:** The whole course - representation, optimisation, architecture families, interpretability, and methodology - still holds together as one system, not twelve disconnected modules.
- **75-89:** Core mechanics are solid; a couple of modules need a re-read.
- **60-74:** Gaps are showing across multiple modules - schedule a `/module-compression` pass on the weak ones.
- **Below 60:** Re-read the one-pagers for the modules you missed, then retake closed book.
