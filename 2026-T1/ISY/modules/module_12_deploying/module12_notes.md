# Module 12 — Deploying Intelligent Systems
## ISY503 Intelligent Systems

## TL;DR

- **MLOps ≠ DevOps**: ML systems are data-driven, not rule-driven — training data, model artifacts, and concept drift create an entirely different deployment lifecycle.
- **Three maturity levels**: Manual (Level 0) → automated ML pipeline with CT (Level 1) → full CI/CD pipeline automation (Level 2).
- **Four deployment dimensions to get right**: data, technology, organisation, and environment — each carries distinct risks in public vs. private sectors.
- **Bias is not optional**: CCS auditing and algorithmic fairness must be built in from design, not bolted on after deployment.
- **AIOps closes the loop**: full-stack observability (user → app → infrastructure → network) using AI-driven pattern recognition replaces agent-based monitoring in microservices environments.

---

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | **Read & summarise Dawson (2020) — Why DevOps for ML is so different** | ✅ |
| **2** | **Read & summarise Google Cloud (2020) — MLOps CI/CD pipelines** | ✅ |
| **3** | **Read & summarise Desouza et al. (2020) — Design/deploy lessons from public sector** | ✅ |
| 4 | Read Dash Documentation — deploying intelligent systems in Python | 🔥 WIP — practical notebook activity |
| **5** | **Watch & summarise CA Technologies (2020) — FullStack AIOps** | ✅ |
| **6** | **Activity 1: AIOps Discussion Forum Post** | 🔥 WIP — draft below |

---

## Key Highlights

---

### 1. Dawson, R. (2020). Why is DevOps for Machine Learning so Different?

**Citation:** Dawson, R. (2020, 17 January). Why is DevOps for machine learning so different? Retrieved from https://hackernoon.com/why-is-devops-for-machine-learning-so-different-384z32f1

**Purpose:** Explains the fundamental differences between traditional DevOps and MLOps, focusing on how ML's data-driven nature changes every stage of the deployment lifecycle — from training through rollout and monitoring.

---

#### 1. The Core Difference: Rules vs. Patterns

- **Traditional software**: actions are codified as **explicit rules** (if/else, control structures). The developer writes the logic.
- **Machine learning**: rules are **indirectly learned** from data. A model (e.g., linear regression) fits weights to minimise error on training data.
- Key insight for DevOps: the ML "executable" is a **trained/weighted model**, not compiled code. It can go stale, require retraining, and its quality is quantitative, not binary.

#### 2. Workflow Comparison

| Stage | Traditional DevOps | MLOps |
|---|---|---|
| **Trigger** | Code commit to git | Code change OR new data |
| **Artifact** | Docker image | Trained model (e.g., pickle file) |
| **Tests** | Pass/fail unit/integration tests | Quantifiable performance metrics |
| **Versioning** | Source code in git | Model + data + parameters + code |
| **Monitoring** | HTTP errors, latency | Domain-specific metrics, data drift |

#### 3. Training Infrastructure

- **Local → cloud**: as dataset size grows, training moves to platforms like **Kubeflow Pipelines** or **MLFlow**.
- **Parallelism**: training runs with different parameters can execute in parallel for hyperparameter search.
- **Continuous Integration for training**: a commit can trigger a training run and push a new model to production — but only if performance passes business thresholds.

#### 4. Model Serving

- **Offline predictions**: batch inference on a file of data points.
- **Real-time serving**: model exposed via HTTP endpoint (e.g., Seldon on Kubernetes, using sklearn pickle from cloud storage).
- Serving solutions like **Seldon** and **KFServing** abstract away Kubernetes routing so data scientists don't need DevOps skills.

#### 5. Rollout Strategies

| Strategy | How it Works | Best For |
|---|---|---|
| **Canary** | Small % of traffic to new model, then full switch | Low-risk, quick validation |
| **A/B Test** | Split traffic long-term, compare metrics statistically | Performance comparison with sample size |
| **Shadowing** | All traffic to both models; only old model responds | Zero-risk testing of new model |

#### 6. Monitoring

- Traditional: HTTP error codes, latency.
- ML requires: **domain-specific metrics** (e.g., purchase conversion rate, customer churn), **outlier detection**, and **concept drift** monitoring.
- **Concept drift**: when live data distributions diverge from training data → model predictions degrade across the board.
- Some ground-truth labels (e.g., "was this transaction actually fraudulent?") arrive days later → full request + prediction logging is needed for offline analysis.

#### 7. Governance and Reproducibility

- Reproducing an ML failure requires: request logs, model version, source code version, training parameters, AND training data.
- **Data versioning** (e.g., DVC, Pachyderm) is needed but standards are not yet mature.
- **Bias and explainability**: "black box" models (neural networks) are problematic where fairness must be demonstrated. White-box techniques preferred where explainability is required.

#### Key Takeaways for ISY503
1. MLOps tooling (Kubeflow, Seldon, MLFlow) directly maps to deployment patterns discussed in Activities — Dash/Heroku deployment is a simplified form of model serving.
2. Canary/A/B/Shadowing strategies will reappear in any production ML deployment scenario.
3. Concept drift and monitoring connect to Assessment themes on responsible AI system maintenance.

---

### 2. Google Cloud. (2020). MLOps: Continuous Delivery and Automation Pipelines in Machine Learning.

**Citation:** Google Cloud. (April 4, 2020). MLOps: Continuous delivery and automation pipelines in machine learning. Retrieved from https://cloud.google.com/solutions/machine-learning/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

**Purpose:** A definitive reference from Google on applying CI/CD principles to ML systems. Introduces the three MLOps maturity levels (0–2) and the components needed at each level, including CT (Continuous Training) as an ML-specific concept.

---

#### 1. Why ML Is Different From Other Software

| Dimension | Traditional Software | ML System |
|---|---|---|
| **Team skills** | Software engineers | Data scientists + ML engineers |
| **Development** | Deterministic, rule-based | Experimental, iterative |
| **Testing** | Unit + integration tests | + Data validation + model quality evaluation |
| **Deployment** | Deploy one service | Deploy a full training pipeline |
| **Production decay** | Bugs only | Bugs + data drift + concept drift |

New concept unique to ML: **CT (Continuous Training)** — automatically retrain the model on new data in production.

#### 2. Data Science Steps in ML (The Pipeline)

1. **Data extraction** — gather from sources
2. **Data analysis (EDA)** — understand schema and feature needs
3. **Data preparation** — cleaning, splits, feature engineering
4. **Model training** — fit algorithms, tune hyperparameters
5. **Model evaluation** — metrics on holdout test set
6. **Model validation** — confirm it beats the current baseline
7. **Model serving** — REST API microservice / edge / batch
8. **Model monitoring** — detect performance degradation, trigger retraining

#### 3. MLOps Maturity Levels

| Level | Name | Key Characteristic |
|---|---|---|
| **0** | Manual process | Script-driven, no CI/CD, models deployed a few times per year |
| **1** | ML pipeline automation | Automated CT; pipeline triggers on data/schedule/drift |
| **2** | CI/CD pipeline automation | Fully automated build, test, deploy of the training pipeline itself |

**Level 0 weaknesses**: no active monitoring, infrequent retraining, training-serving skew risk, data scientists hand off a pickle file to engineers.

**Level 1 additions**:
- **Feature store**: centralised repository for feature definitions — avoids training-serving skew by sharing features between training and inference.
- **ML metadata store**: logs every pipeline run (versions, timestamps, parameters, artifacts, metrics) for reproducibility and debugging.
- **Pipeline triggers**: on-demand / scheduled / new-data / performance-degradation / concept drift.

**Level 2 pipeline stages**:
1. Development & experimentation
2. Pipeline CI (build, unit tests, integration tests)
3. Pipeline CD (deploy to target env)
4. Automated triggering (schedule/drift)
5. Model CD (serve trained model as prediction service)
6. Monitoring (statistics → trigger new experiment cycle)

#### 4. CI at Level 2 — What Gets Tested

- Feature engineering logic
- Model training convergence (loss decreases, no NaN values)
- Per-component artifact outputs
- Integration between pipeline components

#### 5. CD at Level 2 — Deployment Rigour

- Verify model compatibility with serving infrastructure
- API contract testing (expected inputs → expected outputs)
- Load testing (QPS, latency)
- Data validation before batch retraining
- Staged rollout: dev branch → pre-prod → manual PROD promotion

#### Key Takeaways for ISY503
1. The 8-step ML pipeline mirrors the workflow in ISY503 assignments — every step has an operational counterpart in MLOps Level 1+.
2. Feature stores solve the training-serving skew problem that Dawson (R1) identifies as a key DevOps challenge.
3. Level 0 describes what most ISY503 projects look like — understanding Levels 1 and 2 shows the path to production-ready systems.

---

### 3. Desouza, K., Dawson, G. & Chenok, D. (2020). Designing, Developing and Deploying Artificial Intelligence Systems.

**Citation:** Desouza, K., Dawson, G. & Chenok, D. (2020). Designing, developing and deploying artificial intelligence systems: Lessons from and for the public sector. *Business Horizons, 63*(2), 205–213.

**Purpose:** Draws on 6 years of AI project experience across public and private sectors to identify recurring challenges in CCS (Cognitive Computing System) design, development, and deployment. Organised around four thematic domains: Data, Technology, Organisation, and Environment.

---

#### 1. What Are Cognitive Computing Systems (CCSs)?

Five defining characteristics:
- Learn from **data and human interactions** (both required)
- **Context-sensitive**: draw on user profiles, prior interactions
- **Recall history** in producing recommendations
- Interact via **natural language processing**
- Provide **confidence-weighted outcomes** (not binary)

| Learning Type | How It Works | Example |
|---|---|---|
| **Supervised** | Labelled training data, learns class boundaries | Fraud detection (fraudulent/not) |
| **Unsupervised** | Discovers unknown patterns | Citizen segmentation by state |

#### 2. Design Phase — Four Domains

| Domain | Key Challenge | Public Sector | Private Sector |
|---|---|---|---|
| **Data** | Availability, legality, bias | Walk away if data unacceptable | Hire experts, build repeatable process |
| **Technology** | IT assets, partner capability | Risk-focused decisions | Balance risk vs. value |
| **Organisation** | Lack of in-house CCS skills | Agile acquisition strategy | Buy/hire/contract expertise |
| **Environment** | Competitor landscape, transparency | Leverage govt transparency | Speculate on competitor maturity |

**Low-hanging fruit vs. bold challenge**: organisations with immature IS capability should start small (automation of mundane tasks) before attempting business-model transformation.

#### 3. Development Phase — Bias Is the Central Risk

Real-world bias examples documented in the paper:
- **Facial recognition**: 12% more likely to misidentify Black males (MIT study)
- **Recidivism prediction**: overstated risk for Black defendants
- **NLP training data**: "sexist semantic connections" — "programmer" tagged masculine

**Response mechanisms**:
- Open-source audit tools to detect (not remove) bias
- **Agile acquisition** in government: iterative procurement of CCS components rather than one monolithic contract — lowers risk, builds internal skills
- Data and algorithm validation required before deployment

#### 4. Deployment Phase — Two Critical Post-Deployment Obligations

1. **Auditing**: CCSs that continuously learn can absorb new biases. Algorithmic audits must be ongoing, not one-time. No universal standards yet exist.
2. **Value capture**: beyond efficiency, deployment must deliver across four dimensions:

| Value Type | Description |
|---|---|
| **Process gains** | Costs saved, time cut |
| **Output gains** | Increased effectiveness |
| **Outcome gains** | Customer experience, ethical outcomes |
| **Network gains** | Ecosystem influence, brand trust |

Public sector: first two (process + output) justify "advancing the business of today"; last two (outcome + network) justify "advancing the business of tomorrow."

#### 5. The Fourth Industrial Revolution Context

Schwab (2017): CCSs are part of a technological convergence that is as transformative as previous industrial revolutions but with greater reach. Governance and ethics are not optional additions — they are load-bearing requirements.

#### Key Takeaways for ISY503
1. The four-domain framework (Data/Technology/Organisation/Environment) is a practical checklist for any IS deployment proposal or case study.
2. Bias must be addressed at the **development** phase — not patched post-deployment. This is directly testable in assignments involving model fairness.
3. The value-capture typology (process/output/outcome/network) can frame the "business case" section of any AI project report.

---

### 4. Dash Documentation (Plotly) — Deploying Intelligent Systems in Python

**Citation:** Dash Documentation & User Guide | Plotly. (n.d.). Retrieved from https://dash.plotly.com/

**Purpose:** Practical reference for the Jupyter Notebook activity: deploying an ML model as a web application via Dash (built on Flask + Plotly) to Heroku.

> *Status: 🔥 WIP — practical notebook activity. Follow the Jupyter Notebook steps for Heroku deployment. Use https://dash.plotly.com/ as supplementary reference.*

---

### 5. CA Technologies. (2020). Lightboard Edition: AIOps Full-Stack Observability.

**Citation:** CA Technologies. (2020, 5 February). Lightboard edition: AIOps full-stack observability [Video file]. Retrieved from https://www.youtube.com/watch?v=-9I4zvcxn4o

**Purpose:** Demonstrates how AIOps applies full-stack observability (user → app → infrastructure → network) using AI/ML to manage the complexity of modern microservices environments — replacing traditional agent-based monitoring that cannot scale to containerised architectures.

---

#### 1. The Modern Application Architecture Problem

Traditional monitoring used **agent-based** tools: agents installed inside servers/mainframes pulled health data at intervals. This breaks in containerised microservices because:
- Containers are small and modular — an agent would consume all resources
- Environments are **highly distributed, highly dynamic, highly complex**
- Disparate tools create data silos — no complete picture

#### 2. Observability vs. Monitoring

| Traditional Monitoring | Modern Observability |
|---|---|
| Agent-based, pull model | Agentless, push model via libraries/APIs |
| Per-infrastructure health | Per-service transactional tracing |
| Infrastructure-level view | End-to-end user journey view |
| Static topology | Dynamic topology from service mesh |

Developers now **build observability in** to each service using libraries and APIs that push health, performance, and transaction data outward — not inward to an agent.

#### 3. Full-Stack AIOps Coverage

Four layers that must be monitored end-to-end:

| Layer | What Is Measured |
|---|---|
| **User** | End-user experience, device, session, behavior journey |
| **Application** | Transactional traces across microservices |
| **Infrastructure** | Container health, Kubernetes orchestration |
| **Network** | Service mesh routing, inter-service communication |

AIOps aggregates all four layers into a unified model with topology context.

#### 4. Role of the Service Mesh and Topology

- **Service mesh** (e.g., Istio): provides physical routing at nodes + centralised distributed routing for microservice communication.
- AIOps treats observability data as a **first-class citizen** in its data model — the service mesh topology provides the dependency map that the AI system needs for **causal pattern recognition**.
- Static topology maps are replaced by dynamic auto-discovered dependency graphs.

#### 5. How AI Reduces Noise and Improves Operations

With full-stack data + topology context + ML algorithms, AIOps can:
- **Reduce alert noise** in highly complex systems
- **Improve root-cause analysis** — identify which service or node is the actual failure source
- **Predict performance degradation** before it impacts users
- **Improve customer experience** by correlating backend health with user-facing behaviour

#### Key Takeaways for ISY503
1. AIOps is the operational counterpart to MLOps — MLOps deploys the model, AIOps monitors the system that hosts it.
2. The four-layer observability model (User/App/Infra/Network) maps directly onto Activity 1's AIOps use cases (minute 6 of the Kampakis video).
3. Agentless observability is an architectural pattern that affects how intelligent systems are designed from the ground up — not just monitored after the fact.

---

## Activity 1 — AIOps Discussion Forum Post

### Video: Kampakis, S. (2019). Artificial Intelligence in Operations (AIOps).

**Citation:** Kampakis, S. (2019, 26 March). Artificial intelligence in operations (AIOps) [Video file]. Retrieved from https://www.youtube.com/watch?v=GSS_rTXkpFU

**Purpose:** Overview of AIOps — its definition, business case, core architecture, and the five main use cases — to prepare students to choose one use case and advise on how to tackle it within an organisation.

---

#### 1. What Is AIOps?

- **Operational analytics**: applying data mining and business analytics to operational data to extract insights and optimise decision making.
- **AIOps** = Artificial Intelligence for IT Operations — uses data science and AI to analyse big data from IT and business operations tools.
- Goals: increase delivery speed, improve IT service efficiency, deliver superior user experience, and move teams away from siloed operations.

#### 2. Why Organisations Need AIOps

From a survey of 100+ IT professionals:
- **70%+ identified alert correlation and proactive issue detection** as their two biggest challenges.
- Key pain points: costly downtime, slow services, too many alerts for humans to handle (**alert fatigue**).
- AIOps promise: automate root-cause analysis, event analysis, and alert noise reduction.

#### 3. AIOps Architecture Stack

| Layer | Components |
|---|---|
| **Data sources** | Events/alerts, metrics (server load), tickets, logs |
| **Processing** | Real-time processing, rules/patterns, domain algorithms |
| **Intelligence** | ML models (including deep neural networks) |
| **Outputs** | Monitoring, service desk automation, continuous insights |

The outer ring is always **business value** — cost reduction + service quality improvement.

#### 4. AIOps Maturity Phases (Gartner)

| Phase | Focus |
|---|---|
| **Establishment** | Identify operational challenges |
| **Reactive** | Solve problems after they occur (simpler ML) |
| **Proactive** | Predict problems before they occur (advanced ML) |
| **Expansion** | Automate as many operations as possible |

#### 5. AIOps Use Cases (Minute 6 of the Video)

| Use Case | What It Does | ML Approach |
|---|---|---|
| **Root cause analysis** | Identify the source of a failure in a complex system | Bayesian/graphical models, causal inference |
| **Network availability optimisation** | Predict machine or sensor failure before it happens | ML classifiers (high accuracy demonstrated in research) |
| **Automatic ticket & problem assignment** | Prioritise, categorise, and route tickets to the right team | Classification models (90%+ accuracy in literature) |
| **Anomaly detection for cybersecurity** | Flag unusual traffic or events that signal intrusion | Outlier/anomaly detection on time series |
| **Storage management** | Optimise storage allocation and predict capacity needs | Predictive analytics |

---

### Suggested Forum Post — Activity 1

> **Chosen use case: Anomaly Detection for Cybersecurity**
>
> Organisations adopting AIOps for cybersecurity should treat anomaly detection as a complement to, not a replacement for, human analysts. My advice:
> - **Start with baseline modelling**: train the model on normal traffic patterns over at least 30 days before going live — a poor baseline generates noise, not signal.
> - **Tune for precision first**: in a security context, false negatives (missed attacks) are costly, but alert fatigue from false positives defeats the purpose. Calibrate thresholds iteratively.
> - **Integrate with the ticket workflow**: wire anomaly alerts directly into the service desk so they are actioned, not just logged. Unactioned alerts erode trust in the system.
> - **Plan for adversarial drift**: attackers adapt — schedule quarterly model retraining and review detected patterns with the security team to avoid the model going stale.

*(~100 words — ready to post)*

---

*Last updated: 2026-05-01*
