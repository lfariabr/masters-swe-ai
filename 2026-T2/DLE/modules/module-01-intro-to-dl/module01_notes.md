# Module 1: Introduction to Deep Learning & Neural Network

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow, Bengio & Courville (2016) - Deep learning Ch.1 | ✅ |
| **2** | Read & summarise Jurafsky & Martin (2008) - N-gram language models | ✅ |
| 3 | Read & summarise Kelleher (2019) - Deep learning Ch.1 | 🔥 WIP - needs manual access |
| 4 | Watch & summarise Jedamski (2019) - Applied ML foundations | 🔥 WIP - needs manual listen/authenticated access |
| 5 | Activity 1: Introduce Yourself | 🕐 |
| 6 | Activity 2: Assessment 2 & 3 Preparation discussion | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

**Purpose:** Introduces deep learning as a machine learning approach that learns useful representations from data. The chapter explains why deep learning matters, how it differs from earlier AI and ML approaches, and why modern data and compute made it practical.

---

#### 1. AI, ML, Representation Learning, and Deep Learning

| Layer | Core idea | Example from the chapter |
|---|---|---|
| **Artificial intelligence** | Broad field of systems that perform tasks requiring intelligence | Rule-based knowledge bases, chess systems |
| **Machine learning** | Systems improve from data instead of only hand-coded rules | Logistic regression, naive Bayes |
| **Representation learning** | The model learns useful features, not only the final mapping | Autoencoders |
| **Deep learning** | Learns many composed levels of representation | Multilayer perceptrons, CNN-style feature hierarchies |

- **Rule-based AI limitation:** Many real-world tasks are easy for humans but hard to express as formal rules, such as speech recognition, face recognition, and visual object detection.
- **Feature dependence:** Traditional ML depends heavily on the representation given to it. Poor features can make a simple model ineffective even when the model itself is mathematically sound.
- **Learned representations:** Deep learning reduces the need for manually designed features by learning intermediate features from raw data.

#### 2. Depth and Hierarchical Representation

- **Depth as composition:** A deep model is built by composing multiple simpler functions. Each layer transforms the input into a more useful representation.
- **Image example:** Early layers can detect edges, later layers can detect corners and contours, and deeper layers can detect object parts before the final object label.
- **MLP framing:** A multilayer perceptron is a mathematical function that maps input values to output values by composing layers of simpler functions.
- **Practical implication:** Deep learning is not just "more neurons"; its strength is the staged construction of useful abstractions.

#### 3. Historical Trends in Deep Learning

| Trend | Why it matters |
|---|---|
| **Changing names** | Neural networks have moved through waves including cybernetics, connectionism, and modern deep learning. |
| **More data** | Larger datasets reduce the burden of generalising from very small samples. |
| **Larger models** | Better hardware and software allow networks with more units and connections. |
| **Higher accuracy** | Deep learning improved results in image recognition, speech recognition, sequence modelling, and reinforcement learning. |

- **Neuroscience inspiration, not simulation:** Modern deep learning is partly inspired by the brain, but it is not a literal attempt to model biological neurons.
- **Connectionism:** A major idea from the 1980s is that many simple computational units can produce intelligent behaviour when networked together.
- **Backpropagation:** The chapter positions backpropagation as a central method for training internal representations in neural networks.
- **Modern resurgence:** The current wave became practical through more data, more compute, larger models, and better training techniques.

#### Key Takeaways for DLE602

1. Module 1 should be understood as the conceptual foundation for the whole subject: deep learning is about learned hierarchical representations.
2. The AI > ML > representation learning > deep learning hierarchy is useful for explaining the subject introduction and later comparing models.
3. The discussion activity should connect project ideas to tasks where learned representations matter, such as text, speech, images, or sequential data.
4. Assessment 1 uses an N-gram model rather than a deep neural model, so this reading helps frame why N-grams are simpler than later neural approaches.

---

### 2. Jurafsky, D., & Martin, J. H. (2008). Speech and language processing.

**Citation:** Jurafsky, D. & Martin, J. H. (2008) Speech and language processing. Boston, MA: Pearson. Retrieved from: https://web.stanford.edu/~jurafsky/slp3/

**Purpose:** Introduces N-gram language models, including how they estimate word probabilities, why the Markov assumption is needed, and how sparsity affects language modelling. This is the key technical reading for Assessment 1.

---

#### 1. Language Models and the Markov Assumption

- **Language model:** A model that assigns probabilities to word sequences or predicts the next word given previous words.
- **Sentence probability:** A sentence can be modelled as `P(w1, w2, ..., wn)`.
- **Chain rule:** The full probability can be decomposed into conditional probabilities, but conditioning on the full history is impractical because most full histories are rarely observed.
- **Markov assumption:** N-gram models approximate the full word history using only the most recent `N-1` words.

| Model | Approximation | Strength | Weakness |
|---|---|---|---|
| **Unigram** | `P(w_i)` | Very simple and fast | Ignores word order and context |
| **Bigram** | `P(w_i | w_{i-1})` | Captures local dependencies | Misses longer context |
| **Trigram** | `P(w_i | w_{i-2}, w_{i-1})` | More contextual than bigram | More sparse and data-hungry |

#### 2. Estimating N-gram Probabilities

- **Maximum likelihood estimate:** For a bigram, estimate probability by counting how often a word follows a previous word:

```text
P(w_n | w_{n-1}) = C(w_{n-1}, w_n) / C(w_{n-1})
```

- **Counts to probabilities:** Raw N-gram counts are normalised by the count of the context.
- **Log probabilities:** Language models commonly use log probabilities because multiplying many small probabilities can cause numerical underflow.
- **Corpus choice:** A model trained on one writing style or domain will perform poorly when tested on a very different domain.

#### 3. Evaluation, Generalisation, and Sparsity

| Concept | Meaning | Relevance to Assessment 1 |
|---|---|---|
| **Training set** | Data used to estimate model parameters | Build positive and negative N-gram counts |
| **Test set** | Unseen data used to evaluate performance | Avoid evaluating only on memorised examples |
| **Perplexity** | Normalised inverse probability of a test set | Useful for language modelling, though A1 focuses on sentiment classification |
| **Sparsity** | Many valid N-grams never appear in training | Unseen tweet phrases need a fallback strategy |
| **Smoothing** | Reserve probability mass for unseen N-grams | Prevents zero-probability failures |
| **Backoff** | Use a simpler model if a higher-order N-gram is unseen | Fall back from trigram to bigram/unigram |
| **Interpolation** | Mix unigram, bigram, and trigram probabilities | Usually stronger than simple backoff |

- **Zero problem:** If an N-gram never appears in training, a pure maximum-likelihood model assigns it probability zero.
- **Add-one smoothing:** Simple but blunt; it can distort probabilities when vocabulary size is large.
- **Interpolation/backoff:** More practical ways to make N-gram models robust to unseen text.

#### Key Takeaways for DLE602

1. Assessment 1 should use a consistent N-gram order for both positive and negative sentiment evidence.
2. Preprocessing decisions matter: tokenisation, lowercasing, punctuation handling, URLs, mentions, hashtags, and train/test separation all affect counts.
3. Bigram is the pragmatic first implementation choice; trigram may capture richer local context but will be more sparse on small datasets.
4. The report should compare whether the two selected Twitter datasets produce similar or different positive, negative, and neutral patterns.
