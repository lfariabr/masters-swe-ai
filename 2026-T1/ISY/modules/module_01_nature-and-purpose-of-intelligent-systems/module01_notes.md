# Module 01 — The Nature and Purpose of Intelligent Systems

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Sarker (2021) — ML algorithms overview | ✅ |
| **2** | Read & summarise Magnimid (2019) — 10 AI applications | ✅ |
| **3** | Read & summarise Keshav (2007) — How to read a paper | ✅ |
| **4** | Read & summarise Land et al. (2007) — Ethics of knowledge management | ✅ |
| **5** | Listen & summarise Channington (2019) — Responsible AI podcast | ✅ |
| **6** | Read & summarise Hulten (2018) — Building intelligent systems | ✅ |
| **7** | Listen & summarise Polich (2020) — Algorithmic fairness podcast | ✅ |
| **8** | Activity 1: Introduce Yourself forum post | ✅ |
| **9** | Activity 2: Discussion Forum — Ethics of bank loan AI | ✅ |
| **10** | Activity 3: Summarise two intelligent systems articles (journal) | ✅ |

---

## Key Highlights

### 1. Sarker, I. H. (2021). Machine Learning: Algorithms, Real-World Applications and Research Directions

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

---

### 2. Magnimid. (2019, 15 March). 10 powerful examples of AI applications in today's world.

**Citation:** Magnimid. (2019, 15 March). 10 powerful examples of AI applications in today's world. Retrieved from https://becominghuman.ai/10-powerful-examples-of-ai-applications-553f7f062d9f

**Purpose:** Short overview of 10 real-world AI application domains, demonstrating how pervasive AI has become in daily life — with a closing warning about trust and negative applications.

---

#### 1. Ten AI Application Domains

| # | Domain | AI Technique / Role | Example |
|---|--------|-------------------|---------|
| 1 | Automated Customer Support | NLP chatbots | Order status, product search, upselling |
| 2 | Personalised Shopping | Recommendation engines, behavioural tracking | Dynamic content, personalised alerts |
| 3 | Healthcare | Workflow AI, image analysis | Tissue sample diagnosis, patient record security |
| 4 | Finance | Algorithmic trading, ML forecasting | Automated portfolio advisors, report generation |
| 5 | Smart Cars & Drones | Computer vision, sensor fusion | Autonomous vehicles, drone delivery (Amazon, Walmart) |
| 6 | Travel & Navigation | Route optimisation, NLP chatbots | Google Maps AI routing, travel assistant chatbots |
| 7 | Social Media | Content curation, behaviour modelling | Facebook/Instagram feed algorithms, spam filtering |
| 8 | Smart Home Devices | Behavioural learning, voice assistants | Smart thermostats, adaptive lighting |
| 9 | Creative Arts | Generative AI, NLP | Watson BEAT (music), Chef Watson (recipes) |
| 10 | Security & Surveillance | Facial/voice recognition, video analytics | Multi-camera monitoring, identity detection |

#### 2. Ethical Warning (Final Note)

- AI-powered robots and marketing tools operate with **minimal human intervention**
- Society's **trust** in AI is crucial for wider adoption — requires convenience, speed, accuracy, and assurance
- The article's embedded video highlights **negative applications** of AI that could be detrimental to human society
- Key question: who is accountable when AI systems cause harm?

#### Key Takeaways for ISY503

- Directly supports **Activity 2** — the bank loan AI scenario uses NLP and computer vision (domains 1, 3, 4 from the table), raising the same trust and accountability concerns
- Supports **Activity 3** — provides examples of intelligent systems to contextualise article summaries
- Complements Sarker (2021) by showing *where* ML algorithms are applied in practice

---

### 3. Keshav, S. (2007). How to read a paper. ACM SIGCOMM Computer Communication Review, 37(3), 83–84.

**Citation:** Keshav, S. (2007). How to read a paper. ACM SIGCOMM Computer Communication Review, 37(3), 83–84. Retrieved from http://ccr.sigcomm.org/online/files/p83-keshavA.pdf

**Purpose:** Practical guide to efficiently reading research papers using a structured three-pass method, plus a technique for conducting literature surveys.

---

#### 1. The Three-Pass Method

| Pass | Goal | Time | What to Do |
|------|------|------|-----------|
| **1st — Bird's-eye** | General idea; decide if worth reading further | 5–10 min | Read title, abstract, intro; scan headings; read conclusions; glance references |
| **2nd — Content** | Grasp content, not details | ~1 hr | Study figures/diagrams carefully; mark unread references; jot key points in margins |
| **3rd — Re-implement** | Deep understanding; identify innovations and hidden flaws | 4–5 hr (beginners) | Virtually re-create the work; challenge every assumption; note ideas for future work |

#### 2. The Five Cs (After Pass 1)

- **Category** — What type of paper? (measurement, analysis, prototype, survey)
- **Context** — Related papers? Theoretical bases used?
- **Correctness** — Are assumptions valid?
- **Contributions** — Main contributions of the paper?
- **Clarity** — Is it well written?

#### 3. Literature Survey Method (3 Steps)

1. **Find seed papers** — Use Google Scholar / CiteSeer with well-chosen keywords → find 3–5 recent papers → do Pass 1 → read related work sections → look for a survey paper
2. **Identify key researchers** — Find shared citations and repeated author names in bibliographies → download key papers → visit researchers' websites to find top conferences
3. **Scan top conferences** — Browse recent proceedings for high-quality related work → make two passes through these papers → iterate if they cite key papers you missed

#### 4. Writing Implication

- Most reviewers and readers will only do **one pass** — so write coherent headings and concise abstracts
- If a reader cannot understand highlights in 5 minutes, the paper will likely never be read

#### Key Takeaways for ISY503

- Directly supports **Activity 3** — use the three-pass method and Five Cs to summarise the two intelligent systems articles
- Provides a reusable skill for all future ISY503 modules and assessments requiring literature analysis
- The literature survey method is useful for Assessment 1 (case study) background research

---

### 4. Land, F., Amjad, U., & Nolas, S. (2007). The ethics of knowledge management. International Journal of Knowledge Management, 3(1), 1–9.

**Citation:** Land, F., Amjad, U., & Nolas, S. (2007). The ethics of knowledge management. International Journal of Knowledge Management, 3(1), 1–9. Retrieved from https://www.proquest.com/scholarly-journals/ethics-knowledge-management/docview/2937274100/se-2?accountid=176901

**Purpose:** Discussion paper arguing that knowledge management (KM) research and practice needs an ethics dimension — covering research ethics, practice ethics, and intellectual property rights, with real-world examples of knowledge manipulation.

---

#### 1. Why KM Needs an Ethics Dimension

- **KM Research ethics** — Researchers face dilemmas: should they whistle-blow illegal practices? IS researchers have been slow to flag ethical issues (Hosein, 2005), partly because funding depends on sponsor goodwill
- **KM Practice ethics** — KM systems enable knowledge to be created, omitted, withheld, suppressed, amplified, diminished, or distorted — sometimes accidentally, often instrumentally
- Key distinction: **Knowledge Management** (IS discipline, ~20 years old) vs **Management of Knowledge** (older concept — manipulation/distortion of knowledge for desired outcomes)

#### 2. Three Ethical Dimensions

| Dimension | Core Issue | Example |
|-----------|-----------|---------|
| **Socio-economic** | Hidden agenda — KM may increase organisational power over knowledge workers; capturing tacit knowledge makes workers dispensable | Bryant (2006): KM as euphemism for downsizing |
| **Technical** | Data mining systems that gather citizen data without consent, profile groups as threats, sell data onwards | Hosein (2005): surveillance system suspended after policy-makers raised ethics concerns |
| **Legalistic** | Intellectual property rights — who owns knowledge? Balance between corporate rights and societal benefit | Human Genome debate; Open Source movement |

#### 3. The "Dark Side" of KM — Knowledge Manipulation

- **Enron** — Reputation for knowledge-sharing, but senior management engineered massive fraud via knowledge manipulation; final stages involved shredding documents (with auditors' help)
- **NGOs** (Ebrahim, 2003) — Information flows from local NGOs to international funding agencies are manipulated for survival; budget validation is a political process requiring accountability

#### 4. Seven Ethical Questions for KM Systems

1. What ethical issues (discrimination, domination) arise from sponsor–designer–user interactions?
2. How is accountability built into all aspects of KM?
3. Who promulgates ethical standards and enforces them?
4. How are disputes involving contested value systems resolved?
5. Can accountability systems avoid stifling innovation?
6. How do we respond to unintended ethical consequences of new systems?
7. How do we ensure transparency and uncover hidden agendas?

#### 5. Intellectual Property Rights

- **Human Genome debate** — US team (Collins): IP belongs to sponsoring org → patent results. Cambridge team (Sulston): genome belongs to humanity → share freely. Both eventually agreed to share. Yet 20% of known human genome has been patented by private companies
- **Open Source / Wikipedia** — Inverts traditional IP; contributors receive no reward; raises its own ethical issues (special interest groups adding bias to entries)

#### Key Takeaways for ISY503

- Directly supports **Activity 2** — the bank loan AI scenario involves knowledge manipulation (training only on "similar feeling" writing), lack of accountability (who audits the algorithm?), and fairness concerns (socio-economic bias in handwriting analysis)
- The seven ethical questions provide a framework for evaluating any intelligent system's ethics
- Connects to Channington (2019) and Polich (2020) on the *practical* side of fairness and accountability

---

### 5. Channington, S. (2019). Responsible AI in Practice with Sarah Bird.

**Citation:** Channington, S. (Interviewer). (2019, 4 December). Responsible AI in practice with Sarah Bird [Audio podcast]. Retrieved from https://twimlai.com/twiml-talk-322-responsible-ai-in-practice-with-sarah-bird/Links to an external site `&&` Channington, S. (Interviewer). (2019, 4 December). Responsible AI in practice with Sarah Bird [Transcript]. Retrieved from https://twimlai.com/twiml-talk-322-responsible-ai-in-practice-with-sarah-bird-transcript/

**Purpose:** TWIML AI Podcast interview with Sarah Bird (Microsoft Azure ML) covering practical responsible AI tooling — interpretability, fairness, and differential privacy — with emphasis on building ethics into engineering processes.

---

#### 1. Responsible AI Is Everyone's Job

- AI ethics is **not a solved problem** — fundamentally hard and will always need attention
- Analogy to **security**: not one person's job; must be built into processes and tooling so every developer considers it
- User research and design teams are naturally equipped to think about people — bring them into the conversation early
- Build responsible AI into **MLOps pipelines**: reproducible, repeatable processes with fairness checks before production

#### 2. Interpretability — InterpretML Toolkit (12–20 min)

- Open-source toolkit for model interpretability: SHAP, LIME, and others unified in one API
- **Glass-Box explainers** — inherently interpretable models (linear models, decision trees) you can inspect directly
- **Black-Box explainers** — algorithms that explain opaque models (e.g., neural nets) via feature importance, local/global explanations
- Interactive dashboard for exploring model behaviour
- Interpretability is *one way* to ensure ethical AI, but robust testing regimes are another — the industry hasn't settled the debate

#### 3. Fairness — FairLearn Toolkit (20–26 min)

- Collection of **fairness techniques** from research, unified in one toolkit
- Over **21 different fairness metrics** catalogued in published research; common ones built into FairLearn
- Compare model performance across **sensitive attribute groups** (e.g., gender, age) — does the model have the same accuracy/outcomes for men and women?
- **Mitigation techniques**: post-processing (threshold adjustment per group), iterative retraining to reduce disparity
- **Pareto trade-off**: plot accuracy vs disparity — models on the Pareto curve show the best available trade-offs; optimising for one sensitive attribute may not transfer to another
- Start with **domain expertise** to define fairness for your setting, *then* find metrics that align — don't start from the metrics

#### 4. Differential Privacy (26–30 min)

- Open-source privacy platform built with **Harvard**; first published by Microsoft Research in 2006
- Adds **mathematical noise** to query results so you cannot reconstruct underlying individual data
- Enables **data sharing for research** (e.g., medical datasets) without compromising participant privacy
- Particularly valuable for **societal datasets** where privacy concerns currently limit what researchers can do
- Built in **open source** because privacy algorithms are easy to implement incorrectly — community inspection is essential
- US Census Bureau was adopting differential privacy for the 2020 Census (first real large-scale deployment)

#### Key Takeaways for ISY503

- Directly supports **Activity 2** — the bank loan AI needs fairness analysis: which sensitive attributes (writing style as proxy for socio-economic status?) are used? What fairness metric applies? FairLearn's Pareto approach shows you can't just maximise accuracy
- Complements Land et al. (2007) — Land asks *who* ensures ethics; Bird answers with *tooling and processes*
- The "responsible AI = security" analogy is a useful framing for Assessment 1 (case study)

---

### 6. Hulten, G. (2018). Building intelligent systems: A guide to machine learning engineering.

**Citation:** Hulten, G. (2018). Building intelligent systems : A guide to machine learning engineering. New York : Apress. Retrieved from https://ebookcentral.proquest.com/lib/think/reader.action?docID=5357977&c=UERG

**Purpose:** Practical guide to leveraging ML in production — covers end-to-end design of intelligent systems (IS) that use ML and user data to improve over time. The introduction frames the book's scope, audience, and what each role will learn.

---

#### 1. Book Scope — Five Key Learnings

- **When to use an IS** and how to make it achieve your goals
- **User interaction design** — effective interactions between users and the IS
- **Implementation** — client, service, and back-end architecture
- **Building intelligence** — powering the IS with ML and growing it over time
- **Lifecycle orchestration** — managing an IS throughout its lifecycle

#### 2. Target Audience Roles

| Role | What They'll Learn |
|------|-------------------|
| **Software Engineers** | Entities/abstractions in IS, conceptual ML understanding, IS design patterns |
| **ML Practitioners** | System constraints on modelling, how to influence other participants, supporting systems (escalation paths, guardrails) |
| **Managers** | Intuition for when ML is appropriate, ROI estimation, investment level decisions |
| **Program Managers** | Planning, staffing, and managing IS projects; lifecycle; team skills |

#### 3. Three Pillars for Software Engineers

- **Entities and abstractions** — runtime, context, features, models, telemetry, training data, intelligence management, orchestration
- **Conceptual ML understanding** — enough to discuss tradeoffs between engineering and modelling investments (not deep statistics/maths)
- **IS patterns** — pros/cons of running intelligence in client vs service; bounding probabilistic components; telemetry for system evolution

#### 4. Key Distinction from Other ML Books

- Most ML books teach data and modelling skills (like programming language books)
- This book is more like a **software engineering book** — teaches how to take base ML skills and produce working systems
- Based on 10+ years building Internet-scale IS with hundreds of millions of daily user interactions

#### Key Takeaways for ISY503

- Provides the **practical engineering perspective** that complements Sarker's (2021) theoretical algorithm overview
- The user interaction design focus connects to Channington/Bird's point about UX in responsible AI
- Useful framing for Assessment 1: an intelligent system is more than just a model — it's client + service + backend + intelligence + orchestration

---

### 7. Polich, K. (2020). Algorithmic fairness.

**Citation:** Polich, K. (Interviewer). (2020, 13 January). Algorithmic fairness [Audio podcast]. Retrieved from http://dataskeptic.libsyn.com/algorithmic-fairness

**Purpose:** Data Skeptic podcast interview with Aaron Roth (UPenn, co-author of *The Ethical Algorithm*) covering differential privacy's definition, mechanisms, and real-world deployment — with insights on interpretability, fairness, and the policy dimensions of privacy.

---

#### 1. Why Anonymization Fails

- Traditional approach: remove names, SSNs → declare data "anonymized"
- This is **fundamentally broken** — datasets can be cross-referenced with public data
- **Latanya Sweeney** (1997): Massachusetts released "anonymized" medical records; Sweeney cross-referenced with voter registration using just zip code + age + gender → identified Governor Bill Weld's medical records
- Anonymization is **heuristic** — "I think I'm clever" today, but someone cleverer may break it tomorrow

#### 2. Differential Privacy — Definition (9–12 min)

- **Core idea**: imagine the study was conducted *without* your data — if the results would be essentially the same, your privacy hasn't been violated
- **Formal guarantee**: no one can tell, substantially better than random guessing, whether your data was included in the dataset
- Unlike anonymization, differential privacy provides **mathematical proof** of privacy — no future attacker can break it regardless of cleverness
- Analogous to encryption: linked to a **computational hardness** guarantee

#### 3. The Coin-Flip Mechanism (Plausible Deniability)

- Example: surveying an embarrassing question (e.g., "Have you had an affair?")
- **Mechanism**: flip a coin. Heads → answer truthfully. Tails → flip again and answer yes/no based on second flip
- Every respondent has **plausible deniability** — any "yes" answer could be the coin, not the truth
- **Law of large numbers**: aggregate statistics remain accurate because noise is known and averages out over many respondents
- This is differential privacy made **visceral and understandable**

#### 4. Privacy vs Accuracy Trade-off

- Differential privacy makes it impossible to determine facts about any single individual
- **Cost**: you need **more data** to achieve the same accuracy with privacy protections than without
- This trade-off is **unavoidable** — more privacy = less accuracy for a fixed dataset size
- Rare conditions/small subgroups may get "washed away" in the noise

#### 5. Privacy as a Policy Question

- Differential privacy has a tuneable **parameter** (the "knob") — more privacy or more accuracy
- **Who controls the knob?** This is a **policy question**, not a mathematical one
- Different stakeholders care about different things — the trade-off between privacy and accuracy of statistical products is at some level fundamentally at odds
- **US Census 2020**: first large-scale deployment; Census committed to releasing all statistical products with differential privacy guarantees. Previous heuristic methods were shown to be breakable via database reconstruction attacks

#### 6. Interpretability ≠ Fairness

- Ethics **transcends the tool** — "a hammer can pound a nail or pound a finger"
- A black-box algorithm *can* be ethical; an interpretable one *can* be unethical
- Interpretability is linked to fairness (you can inspect for bias) but is neither necessary nor sufficient for fairness
- Fairness guarantees can potentially come from **mathematical/algorithmic techniques** rather than human inspection

#### Key Takeaways for ISY503

- Directly supports **Activity 2** — the bank loan AI raises fairness questions: is the algorithm fair even if we can't inspect it? Differential privacy is relevant if the bank shares loan data for research
- The Latanya Sweeney example is a concrete case to cite in discussions about data ethics
- Complements Channington/Bird (2019) — Bird covers fairness *tooling* (FairLearn); Roth covers the *theoretical foundations* (why anonymization fails, what differential privacy guarantees)
- The "privacy as policy" framing connects to Land et al.'s question: *who promulgates ethical standards?*

---

## Activities

### Activity 1: Introduce Yourself
Hi everyone, I'm Luis — Software Engineer with 10+ years experience building systems across healthcare, fintech, marketing, and education. Currently working part-time as a Data Analyst (SQL pipelines, Power BI, analytics) while pursuing this masters in SWE/AI.

I've implemented ML models in production including recommendation systems, NLP sentiment analysis, and topic modeling with BERTopic, and I'm here to deepen the understanding I have of the theoretical foundations and ethical frameworks behind intelligent systems - particularly excited about Module 8 (Computer Vision) and Module 9 (NLP).

Looking forward to collaborating with you all on case studies and learning how to balance tech performance with fairness!

### Activity 2: Discussion Forum Post
> *(Bank using ML + NLP for loan approval)*
> - Using the resources you have read in this Module, discuss the ethics of the situation given above. Ensure you also discuss the concept of fairness in the scenario.
> - Describe each of these (ethics and fairness) in no more than 100 words.

#### Ethics
The bank's system raises several ethical concerns. 
1. It judges the ability to repay the loan based on handwriting style and tone (factors unrelated to financial responsibility). 
2. It lacks transparency: customers don't know they're being assessed on handwriting, preventing informed consent. 
3. Handwriting might correlate with education level, cultural background, or language proficiency, meaning the system could reject marginalized groups. 
4. Finally, the bank assumes correlation equals causation: just because polite writers historically repaid loans doesn't mean politeness causes repayment. The real factors (income, job stability) remain hidden, making this ethically questionable.

#### Fairness
This system violates individual and group fairness. 
1. Individual fairness requires that people with similar financial profiles receive similar treatment, yet 2 applicants with identical incomes and credit scores could get different decisions based on handwriting style. 
2. Group fairness demands that protected groups aren't systematically disadvantaged, but handwriting correlates with education, culture, and language proficiency, meaning immigrants, non-native speakers, or those with less formal education face higher rejection rates for reasons unrelated to their ability to repay the loan. 
3. The system also lacks procedural fairness: decision criteria should be transparent and relevant, but handwriting assessment is neither, creating unjust outcomes hidden hidden behind a 'the computer said no' excuse.


### Activity 3: Summarising Two Intelligent Systems Articles
> The summaries should be posted to your private journal for Module 1, be no more than 200 words each (400 total) and should address:
> - Why solving that specific problem was important;
> - What intelligent system or AI technique was used; and
> - What were the ethics discussed in the work.

#### Summary: Lee & Park AI Ethics via Text Mining 
The problem they tried to solve was spotting new AI ethics problems before they blew up. Traditionally, this meant paying expert panels to read tons of articles and guess what's coming, which was slow, expensive, and subjective.

Lee & Park used a combination of text mining and semantic network analysis to scan 708 articles (1994–2016) and categorize ethical issues as strong signals (already big news, e.g., privacy breaches), weak signals (emerging issues experts discuss but the public doesn't know yet, e.g., who's legally responsible when a self-driving car kills someone?), and latent signals (barely discussed, might become important later, e.g., emotional robots). They used Natural Language Processing to extract keywords and mapped them using Degree of Visibility and Degree of Diffusion metrics.

The ethics discussed in the work revolved around the need for a more systematic approach to AI ethics, highlighting the importance of early detection of emerging ethical issues and the need for a more objective and data-driven method for identifying these issues.

The ethics discussed included privacy violations from AI surveillance, safety and accountability for autonomous vehicles, human abuse by malicious AI, and emerging concerns like legal liability, killer military robots, and AI singularity (the risk of AI surpassing human control).

#### Summary: Calvo et al. (2019) - Human Autonomy in AI Systems
As AI systems increasingly mediate human experience, from health to politics, designing them in ways that genuinely serve users rather than exploit them has become an urgent ethical imperative. Calvo et al. argued that existing engineering ethics frameworks focus on machine autonomy and productivity, leaving human autonomy largely unexamined and at risk.

The intelligent system examined was an AI-enhanced video recommender system, specifically YouTube's, used as a real-world case study. The authors did not build a new system; instead, they applied the METUX model (Motivation, Engagement and Thriving in User Experience) grounded in Self-Determination Theory (SDT) as an analytical framework. METUX defines six spheres of technology experience: Adoption, Interface, Task, Behaviour, Life, and Society, enabling designers to evaluate how AI design decisions impact human autonomy at each level.

The ethics discussed centred on autonomy violations: algorithmic filter bubbles that distort users' social reality, autoplay features that bypass informed consent, clickbait-driven deception, and attention-harvesting business models that treat users as means rather than ends. The paper argues that autonomy-supportive AI design is not optional, it's an ethical imperative, and that multi-sphere analysis is necessary to capture contradictory and downstream effects on human wellbeing.