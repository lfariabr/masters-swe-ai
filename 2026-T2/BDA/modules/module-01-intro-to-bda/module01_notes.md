# Module 1: Introduction to Big Data Analytics

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Marr (2021) - Data strategy Ch.1 | ✅ |
| **2** | Watch & summarise Rutherford (2017) - What is big data? | ✅ |
| **3** | Read & summarise EMC Education Services (2015) - Data Analytics Lifecycle | ✅ |
| **4** | Read & summarise OmniSci/HEAVY.AI - Big data analytics introduction | ✅ |
| 5 | Activity 1: Working with Jupyter Notebook | ✅ |
| 6 | Activity 2: Interactive Knowledge Check | ✅ |


---

## Key Highlights

### 1. Marr, B. (2021). Data Strategy - Chapter 1

**Citation:** Marr, B. (2021). *Data strategy: How to profit from a world of big data, analytics and artificial intelligence* (2nd ed.). Kogan Page. https://ebookcentral.proquest.com/lib/think/detail.action?docID=6735740

**Purpose:** Introduces why data has become a strategic business asset, how digital trails and IoT produce massive data growth, why value depends on using the right data, and why every organisation needs a data strategy tied to business outcomes.

---

#### 1. Data as a Strategic Asset
- **Core argument:** Data is already changing how organisations operate and will become more central to survival, competition, and business growth.
- Marr frames data as a resource that cuts across business functions, not only a technical concern for IT or analytics teams.
- The value of big data is not just its size. The important question is whether the organisation has the **right data** and can turn it into useful action.

#### 2. Growth of Data, AI, and IoT
- **Human-generated data:** browsing, credit card purchases, email, photos, mobile phone location, social media, and content consumption.
- **Machine-generated data:** CCTV, sensors, connected devices, wearables, smart home devices, medical tools, and industrial systems.
- **AI connection:** Data volumes become more useful as AI and analytics tools improve the ability to detect patterns, automate decisions, and generate predictions.
- **IoT connection:** Connected devices expand both the scale and granularity of data collection, because data can be generated continuously rather than only during explicit human transactions.

#### 3. Structured vs Unstructured Data

| Data Type | Example | Analytics Implication |
|---|---|---|
| **Structured data** | Survey counts, transaction records, labelled spreadsheet fields | Easier to store, query, and analyse using traditional databases and BI tools |
| **Unstructured data** | Video, images, maps, speech, social media posts, free text | Potentially richer, but needs more advanced processing before insight can be extracted |

- Marr uses the example of a shop wanting to understand people walking past: a manual count gives structured data, while video can capture richer behavioural signals but needs advanced analysis to unlock its value.
- This distinction directly prepares the subject's later focus on data sourcing, storage, cleaning, visualisation, and modelling.

#### 4. Data-Driven Life and Work
- Data analytics now influences ecommerce, advertising, politics, healthcare, scientific exploration, insurance, retail, and public services.
- Examples in the saved extract include loyalty-card profiling, targeted advertising, political campaign analytics, NASA mission planning, wearable health devices, medical imaging, and epidemic tracking.
- These examples show that big data analytics is not just about dashboards. It can shape decisions, predictions, interventions, and automated services.

#### 5. Privacy and Ethics Tension
- Marr presents the data revolution as both opportunity and risk: more data can improve services and decision-making, but it also creates extensive tracking and prediction of personal behaviour.
- A recurring tradeoff is **benefit exchange**: people often share data when they perceive a clear benefit, but that does not remove the need for privacy, consent, governance, and responsible use.

#### 6. Industry 4.0 and Connected Operations
- Marr connects big data with **Industry 4.0**, where smart factories, sensors, cameras, connected machines, and cyber-physical systems monitor production and support decentralised decisions.
- Data can be used to simulate operational changes before they are made in the real world, such as machinery speed, component replacement, failure risk, supply-chain constraints, and maintenance timing.
- Benefits include safer dangerous workplaces, better supply-chain control, more consistent output, less waste, higher productivity, and higher profitability.
- Risks include data security, system reliability, skills gaps, technical outages, lower human oversight, and job displacement.

#### 7. Other Data-Enabled Technologies

| Technology | Data Connection | Business Relevance |
|---|---|---|
| **AI** | Learns patterns from large and complex datasets | Automates analysis, prediction, language, image recognition, and decision support |
| **IoT** | Generates continuous sensor and device data | Expands monitoring across homes, cities, factories, vehicles, and services |
| **Genomics** | Uses computational analysis of biological data | Supports medical treatments, gene editing, food/agriculture innovation |
| **Blockchain** | Stores tamper-resistant distributed records | Tracks transactions, inventory, logistics, and sales records |
| **Extended reality** | Uses digital/physical data overlays | Supports education, entertainment, training, and operational use |

#### 8. Why Every Business Must Become a Data Business
- Data is becoming a key source of **competitive advantage** because organisations compete on how well they leverage data, analytics, and new technologies.
- Marr argues that data-driven businesses showed stronger adaptability during the Covid-19 pandemic because data helped them adjust processes and operations.
- Data projects fail when organisations focus on tools and techniques before clarifying **why** the work matters.
- Data strategy starts with business purpose: what needs to change, what needs to be understood, and what outcome the organisation wants.

#### 9. Six Business Uses of Data

| Area | What Data Improves |
|---|---|
| **Decision-making** | Better evidence for strategic and operational choices |
| **Understanding customers and markets** | Deeper insight into needs, behaviour, demand, and segmentation |
| **Making better products** | Product design, quality, personalisation, and innovation |
| **Making better services** | Service design, delivery, targeting, and experience |
| **Improving operations** | Efficiency, productivity, risk control, and process optimisation |
| **Monetising data** | Creating revenue or strategic value from data assets |

#### Key Takeaways for BDA601

1. Big data value comes from turning digital trails into decisions, not from data accumulation alone.
2. Unstructured data is central to modern analytics because it captures behaviour, context, images, speech, and text that traditional structured records miss.
3. This resource sets up SLO `a)` by explaining why volume, variety, velocity, veracity, valence, and value matter in real organisational settings.
4. Big data analytics must be tied to business strategy; otherwise, projects can fail even when the technology works.
5. The six business uses of data provide a practical checklist for later BDA601 assessments: decision-making, customers/markets, products, services, operations, and monetisation.

---

### 2. Rutherford, A. (2017). What is Big Data? Think Data

**Citation:** Rutherford, A. (2017, February 20). *What is big data? Think data* [Video]. YouTube. https://www.youtube.com/watch?v=91tncL3gA6I

**Purpose:** Introduces a broad, practical definition of big data, explains the five V characteristics, distinguishes human-source, business-system, and machine-generated data, and highlights preparation, linkage, privacy, and value challenges.

---

#### 1. Big Data Is Relative
- Rutherford stresses that big data has no single agreed definition.
- Big data is not only "too large for conventional computers"; it can also be complex relative to an organisation's available technology, people, skills, and resources.
- Data that is big for one organisation may be routine for another.
- Many traditional data principles still apply, but the scale, complexity, connectivity, and everyday role of data have changed.

#### 2. The Big Data Vs

| V | Meaning | Why It Matters |
|---|---|---|
| **Volume** | Massive amounts of data are collected and stored | Storage, access, processing, and security become difficult at scale |
| **Variety** | Data includes many types, sources, and structures | Analysts must handle social media, healthcare data, video, wearables, survey data, administrative data, and non-standard structures |
| **Velocity** | Data is generated and analysed quickly, sometimes in real time | Organisations face pressure to produce timely intelligence even when they do not need live decisioning like Google or Facebook |
| **Veracity** | Data may contain errors, duplicates, abbreviations, missingness, and non-research coding | Analysts need to understand data quality before trusting outputs |
| **Value** | The intelligence generated must help the organisation | Analysis should improve impact reporting, service delivery, decisions, or organisational design |
| **Valence** | The degree of connectivity among data items, added in the module overview | Linked data can create richer insights but increases modelling, privacy, and governance complexity |

#### 3. Types of Big Data

| Type | Examples | Notes |
|---|---|---|
| **Human-source information** | Essays, reports, doctors' notes, social media posts, website text/images/video | Often unstructured and rich in context |
| **Traditional business systems** | Health records, hospital admissions, education records, income/pension records, service-user databases | Often structured administrative data collected while delivering services |
| **Machine-generated data** | Mobile-phone positioning, satellite images, weather data, maps, earthquake/atmosphere data, CCTV, traffic monitoring | Often high-volume, continuous, and sensor-driven |

#### 4. Data Preparation Challenges
- Analysts need to understand the data structure, variable coding, accuracy, missing data, terms, and values.
- Large datasets can exceed an organisation's storage and processing capacity.
- Linked data increases the need to manage privacy, confidentiality, anonymity, and effects on data subjects.
- Administrative and activity-generated data can be more complete than survey samples, but completeness does not remove quality or interpretation issues.

#### 5. Linkage and Organisational Value
- Data can become "big" when internal data is linked with external sources, even if the starting dataset is not large.
- Linkage can happen at individual, organisational, or geographic level.
- Rutherford's practical focus is on helping organisations use available data better: understanding operations, service distribution, and impact.

#### Key Takeaways for BDA601

1. The Vs are a diagnostic checklist for evaluating whether a dataset creates technical, quality, linkage, or business challenges.
2. Value is the anchor V: big data analysis is not done for data's sake, but to improve decisions, demonstrate impact, or improve services.
3. Veracity matters because big datasets are often generated through activity, administration, or measurement rather than designed research.
4. Data linkage is powerful, but it raises privacy and confidentiality risks that need to be handled from the start.

---

### 3. EMC Education Services. (2015). Data Science and Big Data Analytics - Chapter 2

**Citation:** EMC Education Services. (2015). *Data science and big data analytics: Discovering, analyzing, visualizing and presenting data*. John Wiley & Sons. Retrieved from https://ebookcentral-proquest-com.torrens.idm.oclc.org/lib/think/reader.action?docID=1908952&ppg=46

**Purpose:** Defines a six-phase Data Analytics Lifecycle for big data and data science projects, with roles, methods, checkpoints, and deliverables from discovery through operational deployment.

---

#### 1. Why a Lifecycle Is Needed
- Data science projects are exploratory, so teams need structure without making the process too rigid.
- A common failure pattern is rushing into data collection or modelling before the business problem, requirements, available data, and success criteria are clear.
- A documented lifecycle improves repeatability, credibility, and handover when teams need to reproduce or extend the work.

#### 2. Key Project Roles

| Role | Primary Contribution |
|---|---|
| **Business User** | Explains the domain, uses the results, and helps operationalise outputs |
| **Project Sponsor** | Defines the business problem, funds the work, sets priorities, and judges value |
| **Project Manager** | Keeps milestones, timing, and quality on track |
| **Business Intelligence Analyst** | Understands KPIs, reports, dashboards, and existing data feeds |
| **Database Administrator** | Provides database access, configuration, and security controls |
| **Data Engineer** | Extracts, shapes, moves, and prepares data for the analytics team |
| **Data Scientist** | Designs analytical methods, builds models, and ensures analytical objectives are met |

#### 3. Six Phases of the Data Analytics Lifecycle

| Phase | Main Question | Core Output |
|---|---|---|
| **1. Discovery** | What business problem are we solving? | Problem statement, stakeholders, success criteria, initial hypotheses, candidate data sources |
| **2. Data Preparation** | What data can we safely use and how should it be shaped? | Analytic sandbox, ETLT/ELT process, data inventory, cleaned and conditioned data |
| **3. Model Planning** | Which analytical methods fit the problem and data? | Candidate models, selected variables, modelling workflow |
| **4. Model Building** | Does the model work on training and test data? | Trained model, test results, refinements, performance evidence |
| **5. Communicate Results** | What did we learn and why does it matter? | Key findings, business value, caveats, stakeholder narrative |
| **6. Operationalize** | How will this work in production? | Reports, briefings, code, technical specifications, pilot deployment, monitoring plan |

#### 4. Discovery Phase
- The team learns the business domain, checks whether similar projects have been attempted, and assesses resources: people, technology, systems, data, time, and tools.
- Framing the problem is critical. The analytics team should write down the problem statement and share it with stakeholders to align assumptions.
- Initial hypotheses give the team testable ideas and create a bridge from business intuition to later analytical work.
- Data source identification should include volume, type, time span, availability, raw data access, and whether the data can actually test the hypotheses.

#### 5. Data Preparation Phase
- The team creates an **analytic sandbox** separate from production systems so analysts can explore high-volume and high-variety data without affecting live operations.
- The chapter distinguishes traditional ETL from sandbox-oriented **ELT/ETLT**, where raw data may be loaded before transformation to preserve details that could be analytically useful.
- Data preparation includes inventorying data, comparing available data against needed data, assessing gaps, checking quality, and conditioning data for later modelling.
- This phase often requires collaboration with IT, DBAs, data owners, and data engineers.

#### 6. Model Planning and Model Building
- Model planning selects candidate analytical techniques based on the business goal, hypotheses, available data, and variable relationships.
- Data exploration in this phase focuses on relationships between variables, not just data hygiene.
- Model building creates training, testing, and production datasets, runs the selected methods, checks model validity, and refines inputs or variables.
- The chapter stresses that data preparation and communication usually take more project time than the modelling work itself.

#### 7. Communicating and Operationalising Results
- Communication compares outcomes against the original success/failure criteria and translates the technical findings into stakeholder-relevant value.
- Good communication includes caveats, assumptions, limitations, methodology, and business impact.
- Operationalisation should usually start with a pilot deployment rather than a full rollout.
- Production use requires monitoring model accuracy, detecting out-of-bounds inputs, and retraining when the model degrades.

#### 8. Final Deliverables

| Audience | Expected Deliverable |
|---|---|
| **Sponsors/executives** | Short presentation focused on value, impact, risks, and decisions |
| **Analysts/data scientists** | Deeper technical presentation with methodology, diagnostics, and process changes |
| **Technical team** | Code and implementation-ready artefacts |
| **Production/engineering team** | Technical specifications for deployment and maintenance |

#### Key Takeaways for BDA601

1. Big data analytics is an iterative lifecycle, not a straight line from data to model.
2. Discovery and data preparation control project quality because they define the problem, data, hypotheses, and sandbox.
3. Model evaluation must connect back to Phase 1 success criteria, not only technical accuracy.
4. Communication and operationalisation are part of analytics work; a model has limited value if stakeholders cannot use it safely.

---

### 4. OmniSci / HEAVY.AI. (n.d.). Big Data Analytics - A Complete Introduction

**Citation:** Omni.sci. (n.d.). *Big data analytics - A complete introduction*. Retrieved from https://www.omnisci.com/learn/big-data-analytics  
**Current accessible source:** HEAVY.AI. (n.d.). *Big data analytics - A complete introduction*. https://www.heavy.ai/learn/big-data-analytics

**Purpose:** Provides an accessible overview of big data analytics definitions, history, tool categories, examples, best practices, and business value.

---

#### 1. What Big Data Analytics Does
- Big data analytics helps organisations reveal patterns, trends, correlations, and information that would otherwise remain hidden.
- It handles data of different sources, sizes, and structures, including structured and unstructured data.
- Compared with traditional BI, big data analytics uses more advanced predictive models, statistical algorithms, visualisation, and machine learning techniques.

#### 2. History and Technology Shift
- The rise of big data analytics followed the growth of search engines, mobile devices, social media, cloud computing, and IoT.
- Traditional data warehouses and relational databases are limited when data becomes extremely large, fast, unstructured, or real-time.
- Distributed platforms such as Hadoop and cloud-based clusters made big data processing more accessible beyond the largest technology companies.

#### 3. Tool Ecosystem

| Tool / Category | Role in Big Data Analytics |
|---|---|
| **NoSQL databases** | Store and organise semi-structured or unstructured data more flexibly than relational tables |
| **Kafka** | Supports high-volume publish/subscribe messaging and streaming data |
| **HBase** | Column-oriented key/value storage on the Hadoop Distributed File System |
| **Hive** | Data warehouse style querying over Hadoop datasets |
| **MapReduce** | Parallel processing framework for large distributed datasets |
| **Pig** | Higher-level scripting for MapReduce jobs |
| **Spark** | Large-scale parallel analytics and stream processing |
| **YARN** | Cluster resource management in Hadoop ecosystems |
| **Presto** | SQL engine for ad-hoc analytics and fast reporting |

#### 4. Best Practices and Analytical Methods
- Use both internal and external data sources where they improve the business question.
- For real-time needs, use streaming architectures and fast processing engines.
- Organise raw data carefully in data lakes or distributed storage so it can be queried and governed.
- Common analytical methods include **data mining**, **predictive analytics**, **machine learning**, and **deep learning**.

#### 5. Big Data Analytics vs Traditional BI

| Traditional BI | Big Data Analytics |
|---|---|
| Often relies on structured warehouse data | Uses structured, semi-structured, and unstructured data |
| Often explains what happened and where | Can investigate why something happened and predict what may happen next |
| Works well with stable reporting and dashboards | Works well with high-volume, high-variety, and fast-changing data |
| Usually retrospective | Often predictive or near-real-time |

#### 6. Business Importance
- Big data analytics can improve customer service, operational efficiency, fraud detection, product development, and strategic decision-making.
- The business benefits highlighted include cost reduction, faster decisions, and creation of new products or services based on better customer understanding.
- The article reinforces that big data analytics matters because traditional systems cannot handle the scale, speed, and unstructured nature of modern data.

#### Key Takeaways for BDA601

1. Tool choice should follow the data characteristics and business problem, not the other way around.
2. Big data analytics extends BI by adding unstructured data, real-time demands, and predictive/explanatory modelling.
3. This resource bridges Module 1 concepts with later modules on ingestion, storage, Spark, modelling, visualisation, and evaluation.
