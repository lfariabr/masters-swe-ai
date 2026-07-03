# Module 6 - Linear Factor Models

> Key Highlights from the Module 6 resources: latent variables, dimensionality reduction, source separation, temporal invariance, sparse representations, and the bridge from classical statistical models to deep representation learning.

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow et al. (2016) - Linear Factor Models (Ch.13) | ✅ |
| **2** | Watch & summarise Poulson (2019) - Factor Analysis and Principal Component Analysis | ✅ |
| **3** | Read & summarise Hyvärinen (2019) - Independent Component Analysis | ✅ |
| **4** | Read & summarise Hlynsson (2017) - Slow Feature Analysis | ✅ |
| **5** | Read & summarise UFLDL Tutorial (2017) - Sparse Coding | ✅ |
| **6** | Read & summarise Srivastava (2015) - Machine Learning vs Statistical Modelling | ✅ |
| 7 | Activity 1: Comparison - when ICA should be preferred over PCA | 🕐 |
| 8 | Activity 2: Idea Generation - NLP, speech, and vision applications | 🕐 |
| 9 | Activity 3: Open Forum - latent variables and factor analysis | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning - Chapter 13: Linear Factor Models.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning*. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/ (Chapter 13)

**Purpose:** Introduces the simplest probabilistic models that learn latent representations. The chapter provides one common framework for PCA, factor analysis, ICA, SFA, and sparse coding, then explains how these linear methods lead toward autoencoders and deeper probabilistic models.

---

#### 1. The shared model: observed data from hidden factors
- **Latent variable `h`:** an unobserved explanatory factor inferred from observed data `x`. Examples include the separate speakers hidden inside a mixed audio recording or the underlying concepts represented by many correlated measurements.
- **Linear decoder:** the model assumes that data is generated as `x = Wh + b + noise`, where `W` mixes the latent factors, `b` is an offset, and the noise captures residual variation.
- **Factorial prior:** the latent factors are usually assigned a simple distribution `p(h) = product_i p(h_i)`. Different factor models are produced by changing the prior, noise assumptions, or learning objective.
- **Representation learning:** instead of working directly with a high-dimensional `x`, the model describes it using a smaller or more structured `h`.

#### 2. The main linear factor models compared

| Model | What it tries to preserve or discover | Main assumption | Typical use |
|---|---|---|---|
| **PCA / probabilistic PCA** | Directions with maximum variance and low reconstruction error | Orthogonal components; equal isotropic observation noise in probabilistic PCA | Dimensionality reduction, compression, visualisation |
| **Factor analysis** | Shared latent causes behind correlated variables | Gaussian latent factors; different noise variance per observed variable | Surveys, psychometrics, discovering constructs |
| **ICA** | Statistically independent source signals | Non-Gaussian independent latent factors | Speech separation, EEG artefact removal, blind source separation |
| **SFA** | Features that change slowly through time | Meaningful latent properties vary more slowly than raw measurements | Video, sensor streams, invariant temporal features |
| **Sparse coding** | Reconstructions using only a few active basis vectors | Sparse latent code, commonly encouraged by an L1 penalty | Unsupervised feature learning, image patches, low-label settings |

#### 3. PCA and factor analysis (§13.1)
- **PCA:** projects data onto a lower-dimensional orthogonal subspace. The first component explains the greatest variance, the second explains the greatest remaining variance, and so on.
- **Probabilistic PCA:** treats PCA as a latent-variable generative model with equal observation-noise variance. As the noise approaches zero, it becomes ordinary PCA.
- **Factor analysis:** allows each observed variable to have a different noise variance. Its latent factors model dependencies shared across observations, while variable-specific noise remains separate.
- **Important distinction:** PCA is primarily variance-preserving compression; factor analysis is primarily an explanatory model of covariance.

#### 4. ICA, SFA, and sparse coding (§13.2-§13.4)
- **ICA:** goes beyond PCA's decorrelation and seeks full statistical independence. It requires non-Gaussian sources because Gaussian sources cannot be uniquely separated under arbitrary rotations.
- **SFA:** minimises the change in learned features between adjacent time steps, subject to zero mean, unit variance, and decorrelation constraints. The constraints prevent constant or duplicate solutions.
- **Sparse coding:** balances reconstruction error against a sparsity penalty: `reconstruction loss + lambda * ||h||_1`. A larger `lambda` favours fewer active features.
- **Sparse coding trade-off:** its optimisation-based encoder can find a strong code for each new sample, but inference is slower than a fixed feedforward pass and is awkward to fine-tune with backpropagation.

#### 5. Why this chapter belongs in a deep learning course (§13.5)
- **Manifold view:** PCA approximates data as lying near a flat, low-dimensional surface inside a higher-dimensional space. The discarded directions are treated mostly as noise.
- **Linear limitation:** real data often lies on curved, nonlinear manifolds. Linear factor models cannot represent those structures well with one flat subspace.
- **Bridge to deep learning:** a linear encoder-decoder becomes a nonlinear autoencoder when neural-network layers and activation functions are added. Deep models extend the same goal with more flexible representations.

#### Key Takeaways for Deep Learning (DLE602)
1. Memorise the common equation `x = Wh + b + noise`. The five methods differ mainly in what properties they demand from `h`.
2. For Activity 1, prefer ICA when the objective is to recover **independent non-Gaussian sources**, not merely lower-dimensional directions of maximum variance.
3. For A2/A3, these methods are defensible preprocessing or baseline techniques, but a modern portfolio project should compare them with learned nonlinear embeddings or autoencoders rather than present them as the final model.

---

### 2. Poulson, B. (2019). SPSS Statistics Essential Training: Factor Analysis and Principal Component Analysis.

**Citation:** Poulson, B. (2019). *SPSS statistics essential training: Factor analysis and principle component analysis* [Video file]. Retrieved from https://www.linkedin.com/learning/spss-statistics-essential-training-2/factor-analysis-and-principal-component-analysis?u=56744473

**Purpose:** Provides a practical dimensionality-reduction walkthrough. It shows how many correlated variables can be condensed into fewer components and how eigenvalues, loadings, scree plots, and rotation support interpretation.

---

#### 1. Reducing many measurements into a few useful factors
- **Signal versus noise:** if several variables measure approximately the same underlying concept, analysing every variable separately retains unnecessary redundancy and variable-specific error.
- **Dimensionality reduction:** the example reduces 12 search-related variables to four components explaining more than three-quarters of the original variance.
- **Eigenvalue:** the amount of variance captured by a component. A common rough rule retains components with eigenvalues greater than one, though this should not be treated as universally optimal.
- **Scree plot:** displays component eigenvalues in descending order. The elbow provides visual evidence for where additional components offer diminishing returns.

#### 2. Loading and rotation make components interpretable
- **Component loading:** a coefficient similar to a correlation between an original variable and a component. Large absolute values indicate that the variable strongly contributes to the component.
- **Orthogonal rotation:** keeps components uncorrelated. This simplifies the mathematics but may be unrealistic when real-world constructs are related.
- **Oblique rotation:** permits correlation among components and can produce a more natural interpretation.
- **Interpretation is still human:** the model groups variables, but an analyst must identify the shared concept and assign a meaningful label.

#### Key Takeaways for Deep Learning (DLE602)
1. PCA compresses features before modelling, which can reduce noise and computation but may also discard useful information.
2. Loadings provide interpretability that dense learned embeddings often lack. This makes PCA a useful baseline when evaluating richer representations.
3. The video makes the Module 6 idea concrete: a latent component is not directly observed, but is inferred from patterns shared across observed variables.

---

### 3. Hyvärinen, A. (2019). What is Independent Component Analysis?

**Citation:** Hyvärinen, A. (2019). *What is independent component analysis?* Retrieved from https://www.cs.helsinki.fi/u/ahyvarin/whatisica.shtml

**Purpose:** Gives a concise definition of ICA as a method for discovering hidden independent sources from observed mixtures, with emphasis on blind source separation.

---

#### 1. ICA as source separation
- **Observed mixtures:** each sensor records a different linear combination of the same unknown sources.
- **Independent components:** ICA estimates both the hidden source signals and the unknown mixing process by assuming that the sources are mutually independent and non-Gaussian.
- **Blind source separation:** the original sources and mixing weights are not supplied to the algorithm. The cocktail-party problem is the canonical example.

#### 2. ICA versus PCA

| Question | PCA | ICA |
|---|---|---|
| Main objective | Maximise retained variance | Recover independent sources |
| Relationship between outputs | Orthogonal and uncorrelated | Statistically independent |
| Distribution assumption | Often Gaussian-friendly | Sources must be non-Gaussian |
| Good example | Compress correlated measurements | Separate simultaneous speakers or biological signals |

- **Core distinction:** independence is stronger than zero correlation. PCA may decorrelate signals while leaving nonlinear statistical dependence; ICA explicitly seeks independence.
- **Applications:** microphone mixtures, mobile-phone interference, EEG/brain measurements, image components, economic indicators, and industrial sensor streams.

#### Key Takeaways for Deep Learning (DLE602)
1. Activity 1's direct answer is: choose ICA when observations are mixtures of hidden sources and recovering those sources matters more than preserving maximum variance.
2. ICA can clean or separate input signals before a speech, health, or computer-vision model is trained.
3. ICA is not automatically better than PCA. Its stronger assumptions must match the data-generating process.

---

### 4. Hlynsson, H. (2017). A Quick Introduction to Slow Feature Analysis.

**Citation:** Hlynsson, H. (2017, 21 October). *A quick introduction to slow feature analysis* [Web log post]. Retrieved from https://towardsdatascience.com/a-brief-introduction-to-slow-feature-analysis-18c901bc2a58

**Purpose:** Builds intuition for SFA through a chaotic time-series example. It demonstrates how slowly changing latent dynamics can be recovered from rapidly changing observations.

---

#### 1. The slowness principle
- **Core intuition:** raw measurements can change quickly while the underlying cause changes slowly. Pixel values move rapidly as an object crosses a video, but the object's identity remains stable.
- **Objective:** find features that minimise the average squared change between consecutive time steps.
- **Constraints:** zero mean removes arbitrary offsets; unit variance prevents the trivial all-zero solution; decorrelation prevents every output from copying the same slowest feature.
- **Ordering:** the first output is the slowest feature, followed by progressively faster features that remain decorrelated from earlier outputs.

#### 2. Linear method, nonlinear features
- **Nonlinear expansion:** SFA itself learns linear combinations, but polynomial expansion or time-delay embedding can transform the input first. A linear feature in the expanded space can represent a nonlinear feature of the original data.
- **Worked example:** delayed copies and cubic expansion allow SFA to recover a smooth driver from an apparently chaotic logistic-map sequence.
- **Hyperparameters:** expansion or reduction method, expanded dimensionality, number of delayed copies, and number of slow features.
- **Limitation:** slowness can be too strong a prior. A rapidly moving object's position may still be useful even though it changes quickly.

#### Key Takeaways for Deep Learning (DLE602)
1. SFA is suitable when observations form a time sequence and meaningful properties are expected to remain stable or predictable across adjacent steps.
2. Candidate Activity 2 uses include speaker identity from audio, stable object identity in video, and slowly changing topics or user intent in text streams.
3. SFA illustrates a recurring DL design principle: the learning objective encodes what kind of representation the model should discover.

---

### 5. UFLDL Tutorial. (2017). Sparse Coding.

**Citation:** UFLDL Tutorial. (2017). *Sparse coding*. Retrieved from http://ufldl.stanford.edu/tutorial/unsupervised/SparseCoding/

**Purpose:** Explains sparse coding as unsupervised dictionary learning: represent each input with a linear combination of basis vectors while keeping most coefficients at or near zero.

---

#### 1. Dictionary learning and over-complete bases
- **Dictionary:** a collection of learned basis vectors `phi_i`, such as edges, textures, or recurring local patterns.
- **Code:** coefficients `a_i` specify which basis vectors reconstruct an input: `x approximately equals sum_i a_i phi_i`.
- **Over-complete basis:** the dictionary may contain more basis vectors than input dimensions. This increases flexibility but makes the coefficients non-unique.
- **Sparsity resolves ambiguity:** requiring most coefficients to be zero or near zero selects compact representations from many possible reconstructions.

#### 2. The objective and its probabilistic meaning
- **Two competing terms:** reconstruction loss asks the code to preserve the input; a sparsity penalty asks it to use few active features.
- **L1 penalty:** `lambda * sum_i |a_i|` is commonly used because it encourages exact zeros while remaining tractable to optimise.
- **Probabilistic interpretation:** L1 corresponds to a Laplace prior concentrated near zero. The model assumes each observation is a sparse combination of source features plus Gaussian noise.
- **Basis constraint:** basis-vector norms must be limited, otherwise the model can shrink coefficients and enlarge basis vectors without genuinely improving sparsity.

#### 3. Learning and practical cost
- **Alternating optimisation:** first infer codes for examples while the dictionary is fixed; then update the dictionary while codes are fixed.
- **Benefit:** sparse features can work well when labelled data is limited because the dictionary is learned from unlabelled inputs.
- **Cost:** encoding each new sample requires an optimisation procedure, making inference slower than a fixed neural-network forward pass.

#### Key Takeaways for Deep Learning (DLE602)
1. Sparse coding connects directly to Module 4: L1 is not just weight shrinkage here, but a mechanism that selects a small set of active latent features.
2. It provides a classical unsupervised-feature baseline against which an autoencoder or learned embedding can be compared.
3. In Review Pulse, sparse coding could compress review embeddings or create interpretable topic-like features, but a transformer remains better suited to contextual meaning and aspect interactions.

---

### 6. Srivastava, T. (2015). Difference between Machine Learning and Statistical Modeling.

**Citation:** Srivastava, T. (2015, 1 July). *Difference between machine learning and statistical modeling* [Web log post]. Retrieved from https://www.analyticsvidhya.com/blog/2015/07/difference-machine-learning-statistical-modeling/

**Purpose:** Offers a practitioner-oriented comparison of two traditions that both learn from data. It is useful for terminology and historical framing, but several contrasts are broad generalisations rather than hard technical boundaries.

---

#### 1. Different emphasis, shared foundations

| Statistical modelling often emphasises | Machine learning often emphasises |
|---|---|
| Explanation, inference, uncertainty, explicit assumptions | Prediction, generalisation, scalable optimisation |
| Interpretable parameters and relationships | Flexible functions and empirical validation |
| A specified probabilistic data-generating process | Performance on held-out or future data |

- **Shared objective:** both traditions learn patterns or relationships from data and rely on probability, optimisation, and validation.
- **No hard boundary:** regression, probabilistic latent-variable models, regularisation, and neural networks draw from both statistics and computer science.
- **Critical reading:** model families do not become superior merely because they are labelled machine learning. Dataset size, assumptions, loss function, evaluation design, and deployment constraints determine suitability.

#### 2. Why the comparison matters in Module 6
- **Linear factor models are statistical and machine-learning tools:** PCA, factor analysis, and ICA have explicit assumptions, but are also algorithms for learning representations from data.
- **Interpretability versus flexibility:** classical factors may be easier to inspect; deep nonlinear representations may capture richer structure but require stronger evaluation and explanation methods.
- **Prediction versus explanation:** an accurate latent representation is not automatically a causal explanation of the world.

#### Key Takeaways for Deep Learning (DLE602)
1. Treat the article as a discussion starter, not an authoritative dividing line. Modern ML and statistics overlap extensively.
2. For assessments, justify a method using the problem, data, assumptions, and evaluation evidence rather than calling one approach inherently more powerful.
3. Module 6 is the bridge: it shows how statistical latent-variable ideas became foundations for modern representation learning.

---

### How Module 6 connects to the assessments
- **Assessment 1:** the n-gram model works with directly observed token counts and does not learn latent representations. Module 6 introduces the opposite idea: compress observations into hidden factors that may remove noise or expose structure.
- **Assessment 2 proposal:** PCA, ICA, or sparse coding can serve as interpretable baselines or preprocessing steps, but the proposal should explain why an attention model or transformer is needed for nonlinear, contextual aspect sentiment.
- **Assessment 3 build:** a strong experiment could compare raw embeddings, PCA-reduced embeddings, and fine-tuned transformer representations. Report accuracy/F1 together with compute cost and retained dimensionality.
- **Portfolio link:** Review Pulse already demonstrates learned representations through GloVe and DistilBERT. Module 6 supplies the classical representation-learning baselines needed to explain what deep representations improve.
