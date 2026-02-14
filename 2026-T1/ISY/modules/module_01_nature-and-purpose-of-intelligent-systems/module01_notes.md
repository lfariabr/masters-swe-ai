# Module 01 — The Nature and Purpose of Intelligent Systems

## Task List

| # | Task | Status |
|---|------|--------|
| 1 | Read & summarise Sarker (2021) — ML algorithms overview | ✅ |
| 2 | Read & summarise Magnimid (2019) — 10 AI applications | 🕐 |
| 3 | Read & summarise Keshav (2007) — How to read a paper | 🕐 |
| 4 | Read & summarise Land et al. (2007) — Ethics of knowledge management | 🕐 |
| 5 | Listen & summarise Channington (2019) — Responsible AI podcast | 🕐 |
| 6 | Activity 1: Introduce Yourself forum post | 🕐 |
| 7 | Activity 2: Discussion Forum — Ethics of bank loan AI | 🕐 |
| 8 | Activity 3: Summarise two intelligent systems articles (journal) | 🕐 |

---

## Key Highlights

### Sarker, I. H. (2021). Machine Learning: Algorithms, Real-World Applications and Research Directions

**Citation:** Sarker, I. H. (2021). Machine learning: Algorithms, real-world applications and research directions. *SN Computer Science*, 2(3), 160. https://doi.org/10.1007/s42979-021-00592-x

**Purpose:** Comprehensive review of ML algorithm types, their principles, real-world applications across domains, and research directions — positioned as a reference for academia and industry in the Fourth Industrial Revolution (Industry 4.0).

---

#### 1. Data Types for ML

| Type | Description | Examples |
|------|-------------|----------|
| **Structured** | Well-defined schema, tabular format | Names, dates, credit card numbers, relational DBs |
| **Unstructured** | No pre-defined format, hard to process | Emails, images, videos, PDFs, sensor data |
| **Semi-structured** | Some organisational properties but not relational | HTML, XML, JSON, NoSQL databases |
| **Metadata** | "Data about data" — describes data properties | Author, file size, date created, keywords |

---

#### 2. Four ML Learning Approaches

| Approach | Drive | Data | Common Tasks | Key Insight |
|----------|-------|------|-------------|-------------|
| **Supervised** | Task-driven | Labelled | Classification, Regression | Maps input → output using labelled examples |
| **Unsupervised** | Data-driven | Unlabelled | Clustering, Dimensionality reduction, Associations | Discovers hidden patterns without human labels |
| **Semi-supervised** | Hybrid | Labelled + Unlabelled | Classification, Clustering | Useful when labelled data is scarce but unlabelled data is abundant |
| **Reinforcement** | Environment-driven | Reward/Penalty signals | Control, Sequential decision-making | Agent learns optimal behaviour via trial-and-error (MDP framework) |

---

#### 3. Supervised Learning — Classification Algorithms

| Algorithm | Type | Key Strengths | Key Limitations |
|-----------|------|---------------|-----------------|
| **Naive Bayes** | Probabilistic | Fast, works with small data, good for text classification | Strong feature independence assumption |
| **Logistic Regression** | Statistical/Probabilistic | Good for linearly separable data, interpretable | Assumes linearity between variables |
| **KNN** | Instance-based (lazy) | Simple, robust to noise | Sensitive to choice of *k* and computationally expensive at prediction |
| **SVM** | Hyperplane-based | Effective in high-dimensional spaces | Poor with noisy/overlapping classes |
| **Decision Tree** | Rule-based | Interpretable, handles high-dimensional data, fast | Prone to overfitting |
| **Random Forest** | Ensemble (bagging) | Reduces overfitting, higher accuracy than single DT | Less interpretable |
| **AdaBoost** | Ensemble (sequential boosting) | Boosts weak classifiers' performance | Sensitive to noisy data and outliers |
| **XGBoost** | Ensemble (gradient boosting) | Fast, handles large datasets, advanced regularisation (L1 + L2) | More complex to tune |

**Classification types:**
- **Binary** — two classes (e.g., spam/not spam, cancer detected/not detected)
- **Multiclass** — more than two classes (e.g., network attack types)
- **Multi-label** — each example can belong to multiple classes simultaneously (e.g., news categorisation)

---

#### 4. Supervised Learning — Regression

| Algorithm | Use Case | Notes |
|-----------|----------|-------|
| **Simple/Multiple Linear Regression** | Linear relationships | y = a + bx + e; multiple extends to n predictors |
| **Polynomial Regression** | Non-linear relationships | nth degree polynomial; derived from linear |
| **LASSO** | Feature selection + prediction | L1 regularisation; shrinks coefficients to zero |
| **Ridge** | Multicollinearity handling | L2 regularisation; shrinks but never zeros coefficients |

---

#### 5. Unsupervised Learning — Clustering

| Method Type | Algorithms | Key Idea |
|-------------|-----------|----------|
| **Partitioning** | K-Means, K-Medoids, CLARA | Divide data into *k* groups by distance to centroids |
| **Density-based** | DBSCAN, OPTICS | Clusters = contiguous high-density regions; handles noise |
| **Hierarchical** | Agglomerative (bottom-up), Divisive (top-down) | Builds tree of clusters (dendrogram) |
| **Grid-based** | STING, CLIQUE | Summarise on grid then combine cells; good for large data |
| **Model-based** | GMM, SOM | Statistical or neural network models for cluster membership |

**K-Means vs DBSCAN:** K-Means is faster but needs predefined *k* and is sensitive to outliers; DBSCAN discovers arbitrary shapes and is robust to outliers but struggles with similar-density clusters.

---

#### 6. Dimensionality Reduction & Feature Engineering

| Technique | Category | Purpose |
|-----------|----------|---------|
| **Variance Threshold** | Feature selection | Remove low-variance features |
| **Pearson Correlation** | Feature selection | Measure linear relationships between features |
| **ANOVA / Chi-Square** | Feature selection | Test statistical significance of features |
| **RFE** | Feature selection | Recursively remove weakest features |
| **PCA** | Feature extraction | Transform to uncorrelated principal components in lower dimensions |

**Key distinction:** Feature *selection* keeps a subset of original features; feature *extraction* creates new features (e.g., PCA).

---

#### 7. Association Rule Learning

| Algorithm | Approach | Strengths |
|-----------|----------|-----------|
| **Apriori** | Bottom-up candidate generation | Most widely used; leverages frequent itemset property to prune search |
| **ECLAT** | Depth-first, vertical data representation | More efficient than Apriori for small/medium datasets |
| **FP-Growth** | Frequent pattern tree (divide & conquer) | Avoids candidate generation; faster but memory-intensive |

**Core metrics:** Support (frequency of itemset) and Confidence (conditional probability of consequent given antecedent).

---

#### 8. Reinforcement Learning

| Algorithm | Type | Notes |
|-----------|------|-------|
| **Monte Carlo Methods** | Model-free | Uses random sampling for numerical results |
| **Q-Learning** | Model-free | Learns action quality without environment model; "Q" = quality |
| **Deep Q-Learning** | Model-free + Deep Learning | Neural networks as function approximators for complex state spaces |
| **AlphaZero / AlphaGo** | Model-based | Learns environment model + policy network |

**Key distinction:** Model-based RL learns a model of the environment (needs policy network); Model-free RL directly learns value/policy from experience.

---

#### 9. Deep Learning

| Architecture | Strength | Common Applications |
|-------------|----------|-------------------|
| **MLP** (Multilayer Perceptron) | Base DL architecture, fully connected | General-purpose, uses backpropagation |
| **CNN** (Convolutional Neural Network) | Exploits 2D spatial structure, auto feature detection | Image recognition, video, NLP, medical imaging |
| **LSTM-RNN** | Handles sequential/temporal data via feedback links | Time series, NLP, speech recognition |
| **GAN** | Generates realistic synthetic data | Data augmentation, image generation |
| **Autoencoder** | Dimensionality reduction + feature extraction | Unsupervised representation learning |
| **Transfer Learning** | Re-uses pre-trained models for new tasks | Low-data scenarios |

**Deep Learning vs Traditional ML:** DL outperforms traditional ML with large datasets but performance advantage diminishes with smaller datasets.

---

#### 10. Real-World Application Domains

| Domain | ML Role |
|--------|---------|
| **Predictive Analytics** | Credit fraud detection, consumer behaviour, demand forecasting |
| **Cybersecurity** | Intrusion detection, malware classification, threat intelligence |
| **IoT & Smart Cities** | Traffic prediction, parking availability, energy usage optimisation |
| **Healthcare & COVID-19** | Disease prediction, medical imaging, outbreak forecasting |
| **E-commerce** | Product recommendations, inventory management, personalised marketing |
| **NLP & Sentiment Analysis** | Chatbots, machine translation, opinion mining |
| **Image & Speech Recognition** | Face detection, voice assistants, pattern recognition |
| **Agriculture** | Crop yield prediction, disease detection, supply chain optimisation |
| **Transportation** | Traffic flow prediction, route optimisation |
| **Context-aware Apps** | Smart notifications, personalised mobile services |

---

#### 11. Challenges & Research Directions

| Challenge | Detail |
|-----------|--------|
| **Data collection** | Useful domain-specific data is hard to gather despite data abundance |
| **Data quality** | Ambiguous values, missing data, outliers, noise degrade models |
| **Algorithm selection** | No one-size-fits-all; wrong algorithm → poor outcomes |
| **Hybrid models** | Ensemble methods and modified algorithms are promising future directions |
| **Data–algorithm dependency** | Model success depends on both data quality *and* appropriate algorithm choice |

---

#### Key Takeaways for ISY503

1. **Four learning paradigms** (supervised, unsupervised, semi-supervised, reinforcement) form the foundation of intelligent systems — each suited to different data availability and task types.
2. **ISY503 focus:** The subject primarily uses supervised learning and models, with reinforcement learning for AI agents and environment discovery.
3. **Algorithm selection matters:** Choosing the right algorithm depends on data characteristics, problem type, and domain context — there is no universal best algorithm.
4. **Deep learning scales:** DL excels with large datasets but traditional ML can be equally effective with smaller, well-structured data.
5. **Ethics gap:** The paper focuses on technical capabilities but does not deeply address ethical considerations — a critical gap that other Module 1 resources (Land et al., 2007; Channington, 2019) are intended to fill.
