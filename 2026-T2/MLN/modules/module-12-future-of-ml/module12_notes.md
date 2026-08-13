# Module 12 - Future of Machine Learning (ML): Enterprise Grade ML and Weak Supervision

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Listen & summarise Macey/Dewalt (2019) - Building ML Projects in the Enterprise (podcast #69) | ✅ |
| **2** | Read & summarise Casey (2020) - Machine Learning in the Enterprise: 5 Hard Truths | ✅ |
| **3** | Read & summarise Xu (2020) - Where Will the Next Trillion Dollars of Value Accrue? *(paywalled - intro only)* | 🔥 |
| **4** | Read & summarise Algorithmia (2020) - State of Enterprise ML: 7 Key Findings *(see citation note)* | ✅ |
| **5** | Read & summarise Agrawal et al. (2020) - Cloudy with High Chance of DBMS (EGML vision paper) | ✅ |
| **6** | Watch & summarise Bell (2019) - Weak Supervision: A New Paradigm for Unreliable Data | ✅ |
| **7** | Listen & summarise Macey/Ratner (2018) - Snorkel: Extracting Value from Dark Data (podcast #15) | ✅ |
| **8** | Read & summarise Powell (2020) - The Cold-Start Problem with Stanford Snorkel | ✅ |
| 9 | Activity 1: Azure SQL Edge + ONNX (model-in-DBMS / edge) - forum | 🕐 |
| 10 | Activity 2: Snorkel Introduction Tutorial (spam labelling) - forum | 🕐 |
| 11 | Activity 3: The Human Factor in ML Adoption (change management) - forum | 🕐 |

> **One-line frame:** the final module is about the **two bottlenecks that stop ML models reaching the real world**.
> **(1) Production / the last mile:** a model in a notebook is <20% of the job - the value only lands when it is
> **deployed, governed and maintained** across an enterprise (MLOps, the data-engineer role, "score in the DBMS,
> govern everywhere"). **(2) Training data / labels:** supervised ML is starved of **labelled** data, and hand-
> labelling does not scale - **weak supervision** (Snorkel) lets domain experts write noisy **labelling functions**
> that a generative model fuses into **probabilistic labels**, programmatically building large training sets. Both
> bottlenecks are where the next decade of ML value - and jobs - will be won.

> ℹ️ **Citation notes (files on hand vs the brief).**
> - **Resource 4:** the brief cites **Bayern (2019, TechRepublic)** "State of enterprise ML in 2020: 7 key findings",
>   which is a write-up **of** the primary source on file - the **Algorithmia (2020) State of Enterprise ML** report.
>   Highlights below are summarised from the Algorithmia report itself; the seven findings are the same.
> - **Resource 3:** the Forbes article (**Xu, 2020**) is **paywalled** - only the opening thesis is accessible, so its
>   highlight is partial (marked 🔥).

---

## Key Highlights

### 1. Macey, T. (Interviewer) & Dewalt, K. (2019). Building Machine Learning Projects in the Enterprise (Episode #69).

**Citation:** Macey, T. (Interviewer). (2019, 11 February). *Episode #69: Building machine learning projects in the enterprise* [Audio podcast]. Data Engineering Podcast. https://www.dataengineeringpodcast.com/prolego-ml-consulting-episode-69/

**Purpose:** A practitioner's view (Kevin Dewalt, founder of Prolego) of getting a Fortune 500 company's *first* ML model into production - why it needs new capabilities, how to build the team, and how the work actually splits.

---

#### 1. Why enterprise ML needs new capabilities
- ML is not "just software": it needs **new CI/CD-style pipelines**, data plumbing, and a **highly iterative,
  scientific** workflow. Much of a sales cycle is spent **educating clients** on what AI/ML realistically can and
  cannot do.
- **The data-engineer role is the unlock.** Someone has to lay the **plumbing** (data pipelines, SQL, storage)
  *before* a model can be deployed. **SQL skills** are called out as essential - the data engineer bridges the data
  scientist and production IT.

#### 2. Team, time split, and production reality
- Build the team from a **mix of internal and external** people; don't expect one "unicorn."
- **Most of the effort is not modelling.** Time goes to **data wrangling** and **pipeline/data-engineering** work;
  model development is the small slice - the same "<20%" reality the Agrawal paper (R5) quantifies.
- **Deployable artifact + monitoring:** production needs a packaged artifact, a real **tech stack**, and **health
  metrics** tracked after release. Major risks (data drift, silent failure) are mitigated by **DevOps-style**
  discipline - the same lesson as Casey's R2 truth #5.

#### Key Takeaways for MLN601
1. The **notebook-to-production handoff** is the module's core theme, told from the trenches - connects directly to
   Assessment 3's CRISP-DM **deployment** phase.
2. **Data engineer + SQL** is the emerging job the subject README foregrounds - the role that makes ML real.
3. "Model dev is the easy 20%" is the through-line linking R1 → R4 → R5.

---

### 2. Casey, K. (2020). Machine Learning in the Enterprise: 5 Hard Truths.

**Citation:** Casey, K. (2020, 30 July). *Machine learning in the enterprise: 5 hard truths*. The Enterprisers Project. https://enterprisersproject.com/article/2020/7/machine-learning-5-lessons-learned

**Purpose:** Five blunt lessons companies learn the hard way when they "charge into production" with ML - the human and process failures, not the algorithms.

---

#### 1. The five hard truths
| # | Hard truth | What it really means |
|---|---|---|
| **1** | We didn't build the right team | ML needs a **tight-knit interdisciplinary team** (modelling, data pipelines, back-end/API, front-end, UI/UX, product). No single person has all of it. |
| **2** | No bridge between business & tech | Need an **"AI Product Manager"** (even unofficially) to close the chasm between business expectations and technical reality. Best ones are often ex-data-scientists. |
| **3** | Too many versions of the truth | A model is "a very intelligent **parrot**" - only as good as its labels. Six people labelled the same data six ways → poor model → forced a valuable "**ground truth**" conversation. |
| **4** | Training data was treated as a finish line | "You can't just train a model and believe it will perform." Needs an **iterative** process + ongoing metric tracking; defining the **right metric** is one of the hardest tasks. |
| **5** | We repeated traditional software mistakes | Silos, scope creep, broken tooling. Fix = apply **DevOps thinking**: automated, repeatable, containerised pipelines. |

#### 2. The new disciplines emerging to fill the gap
- **MLOps, DataOps, DataViz, MLUX** (ML user experience) are blossoming because ML adds considerations on top of
  normal product development. Data scientists know ML but are often **less versed** in DevOps, UX, and product than
  software engineers are.

#### Key Takeaways for MLN601
1. Truth #3 (**labelling is subjective and scarce**) is the exact pain that **weak supervision / Snorkel** (R6-R8)
   sets out to solve - the two halves of the module meet here.
2. Truth #5 (**do DevOps**) = the MLOps theme shared with R1, R4, and R5.
3. A ready-made checklist for the **Activity 3** essay on driving ML adoption (people and process, not models).

---

### 3. Xu, L. (2020). Machine Learning in the Enterprise: Where Will the Next Trillion Dollars of Value Accrue?

**Citation:** Xu, L. (2020, 15 July). *Machine learning in the enterprise: Where will the next trillion dollars of value accrue?* Forbes. *(Paywalled - only the opening thesis is accessible; see citation note.)*

**Purpose:** A market-strategy lens on *who captures* the value ML creates. **Partial summary** - the article body is behind a paywall.

---

#### 1. The accessible thesis
- **"Software has been eating the world; ML is starting to eat software"** - and it is supercharging trillion-dollar
  industries: **healthcare, security, agriculture**.
- The value question ("where will it accrue?") is answered across **three company types**:
  1. **Traditional companies applying ML** to their existing business.
  2. Companies building **industry-agnostic ML tools** (horizontal platforms).
  3. Companies building **vertically-integrated ML applications** (deep in one domain).
- **"ML is not just for the tech giants"** - value will spread beyond FAANG.

#### Key Takeaways for MLN601
1. The **three value-capture archetypes** are a useful framing for the Assessment 3 discussion of ML's business impact.
2. Aligns with Algorithmia's (R4) prediction of a **boom in third-party ML tooling companies** (archetype 2).
3. 🔥 **Action:** if the full article is needed, access via the university library / a Forbes subscription.

---

### 4. Algorithmia. (2020). 2020 State of Enterprise Machine Learning: Seven Key Findings.

**Citation:** Algorithmia. (2020). *2020 state of enterprise machine learning* [Research report]. *(The module brief cites Bayern, M. (2019), TechRepublic, a write-up of this report - see citation note.)* Survey of 745 respondents (Group A: 303 blind; Group B: 442).

**Purpose:** Hard survey data on where enterprises actually are with ML - hiring, use cases, maturity, and the deployment bottleneck.

---

#### 1. The seven key findings
| # | Finding | Standout number |
|---|---|---|
| **1** | Data-science teams are **small but growing fast** | Half of companies have **1-10** data scientists; the **11+** bracket jumped 18% → **39%** since 2018 |
| **2** | **Cost-cutting** takes centre stage as companies grow | Top 3 use cases: **reduce costs**, generate customer insights, improve CX. Big firms → internal/cost; small firms → customer-facing |
| **3** | **Overcrowding at early maturity** ("AI for AI's sake") | **55% have never deployed** an ML model; only **8%** are "sophisticated" (5+ yrs in production) |
| **4** | **An unreasonably long road to deployment** | Most take **31-90 days** to deploy one model; **18%** take >90 days. ≥25% of data-scientist time is lost to deployment plumbing |
| **5** | **Scale is the #1 challenge** | **43%** cite scaling (up 13% YoY); **41%** cite versioning/reproducibility; **34%** cite org alignment/buy-in |
| **6** | **Budgets are growing** | Most commonly **+1-25%**; banking, manufacturing, IT lead the growth |
| **7** | **Success is measured two ways, split by role** | ICs value **technical** metrics (accuracy, drift); execs value **business** ROI; **directors** bridge both |

#### 2. The narrative underneath the numbers
- The **last mile (deployment) is the bottleneck**, not model-building - "an insight that comes 10 days too late is
  overcome by events." Expect a **boom in ML-tooling vendors** selling the last-mile solution (their own pitch).
- **Warning: "snake-oil AI."** A flood of third-party vendors risks selling non-technical buyers things they don't
  need ("AI for AI's sake").

#### Key Takeaways for MLN601
1. **Deployment time + "55% never deployed"** are the headline stats that justify this whole module's focus on
   production - quotable in Assessment 3.
2. **Scaling, versioning, reproducibility** = the concrete MLOps problems R1/R2/R5 keep naming.
3. The **role-split on "what is success"** (finding 7) reinforces SLO d) - communicating ML value to *different*
   stakeholders.

---

### 5. Agrawal, A. et al. (2020). Cloudy with High Chance of DBMS: A 10-year Prediction for Enterprise-Grade ML.

**Citation:** Agrawal, A., Chatterjee, R., Curino, C., Floratou, A., ... Zhu, Y. (2019/2020). *Cloudy with a high chance of DBMS: A 10-year prediction for enterprise-grade ML*. CIDR 2020. http://cidrdb.org/cidr2020/papers/p8-agrawal-cidr20.pdf

**Purpose:** Microsoft's **vision paper** - the boldest claim in the module: over the next decade, ML models will migrate **into database systems**, and data governance becomes central. Coins **EGML** (Enterprise-Grade ML).

---

#### 1. The core prediction (EGML)
- **EGML = Enterprise-Grade ML:** the next wave is not "unicorn" apps (web search) built by huge teams, but
  **millions of moderately-valuable ML apps** built by **small domain-expert teams** - yet with **far stricter**
  demands (auditing, security, privacy, fairness, bias), especially in regulated industries.
  > *"Copying CSV files on a laptop and maximizing average model accuracy just doesn't cut it."*
- **Key insight: "An ML model is software derived from data"** - it has a **dual nature**:
  - **models-as-software** → needs CI/CD, testing, tooling, DevOps.
  - **models-as-data** → needs lineage, versioning, access control, provenance.

#### 2. The three-part vision (Flock reference architecture)
| Pillar | Prediction | Why |
|---|---|---|
| **Train in the Cloud** | Model dev/training → public or private **cloud** | Needs centralised data, spiky compute, newest hardware |
| **Score in the DBMS** | Inference runs **inside the database**, next to the data | Avoids exfiltrating data; models can be uniformly represented and compiled → early experiments show **5×-24× speedups** |
| **Govern everywhere** | Provenance tracked from **training data → model → decision** | GDPR, bias, explainability; models are "derived data" needing DB-grade governance |

#### 3. The reality check
- **Model development is <20% of the project lifecycle** - most time is data collection/cleaning + operationalising.
- Analysis of **>4M GitHub Python notebooks**: **>70% are ML**; **numpy/pandas/sklearn** are consolidating as the
  dominant core, but **testing/CI-CD/model-tracking (e.g. MLFlow) adoption is still low**.

#### Key Takeaways for MLN601
1. **"Score in the DBMS"** is the exact idea behind **Activity 1** (Azure SQL Edge running ML over sensor data) -
   the future has already arrived.
2. The **software-derived-from-data dual nature** is the theoretical spine of MLOps - links to R1/R2/R4.
3. **<20% is modelling** appears in three resources (R1, R4, R5) - if you remember one number from this module, this
   is it.

---

### 6. Bell, E. (2019). Weak Supervision: A New Paradigm for Unreliable Data.

**Citation:** Bell, E. (2019, 19 July). *Eddie Bell: Weak supervision: A new paradigm for unreliable data* [Video, PyData London 2019]. https://www.youtube.com/watch?v=KRcgteDTm3k

**Purpose:** The best conceptual explainer in the module - what weak supervision is, why it exists, and how Snorkel works, grounded in a **fraud-detection** case study (Ravelin).

---

#### 1. Why labels are the bottleneck (the fraud case)
- The big ML leaps came from **new labelled datasets** (e.g. ImageNet → the CNN boom). Labels are **scarce,
  expensive, slow, or ethically hard** to collect.
- **Fraud labels ("chargebacks") are high-quality but very slow** (2 weeks to 4 months) → you train on 4-month-old
  data. Worse, **success destroys your labels**: block a fraudster → no chargeback → the model **overfits hard cases
  and forgets easy ones**. You have many **dubious** label sources (manual reviews, rules, network/graph signals,
  3DS) but none is a true supervised label.

#### 2. The supervision spectrum + the historical arc
- **Supervised** (use only good labels) → **semi-supervised** (propagate good labels to nearby unlabelled points via
  similarity) → **weakly supervised** (fuse **good + many low-quality** labels; "shotgun the whole instance space").
- **The evolution of what we engineer:** 1970s **expert systems** (engineer the *decision function*) → 1990s **ML**
  (engineer the *features*) → **deep learning** (engineer the *architecture*) → **weak supervision** (engineer the
  **labels themselves**).

#### 3. How Snorkel works
- **Labelling functions (LFs):** small functions returning **+1 / −1 / 0** (vote for the class / vote against /
  **abstain**). Example: ">5 credit cards in a day" → suspicious. Sources can be rules, humans, graph/similarity
  methods, weaker models, even data augmentations (rotate/crop images).
- **Two-model pipeline:** the noisy LF votes feed a **generative label model** (correlation-aware; learns a latent
  variable = P(fraud) via factor graphs) → outputs a **probabilistic label** → which trains a normal
  **discriminative model** (usually deep; must accept a probabilistic label, so **log-loss / binary cross-entropy**,
  not a random forest).
- **Result:** ~**20 LFs → +2% recall** on an already-mature model (strong). With **zero** starting labels the gain is
  huge.

#### 4. The honest caveats
- **Evaluation paradox:** if you *generate* your labels, how do you evaluate the model without ground truth?
- **LF-instance density is a Goldilocks problem:** too **few** LFs per instance → collapses to **majority vote** /
  plain supervised; too **many** → majority vote is already fine. The **generative model only wins in the middle**.
- Optimising LF thresholds against true labels just builds "a **bad random forest**" - defeats the point.

#### Key Takeaways for MLN601
1. The **+1/−1/0 labelling function** and the **generative → discriminative** two-model pipeline are the mechanics to
   know for **Activity 2** (the Snorkel tutorial).
2. **"Engineer the labels"** is the module's second big idea (paired with "productionise the model") - both are about
   removing the bottlenecks to real-world ML.
3. **Probabilistic labels** tie back to Module 8 (logistic regression) and Module 11 (smooth outputs) - the model
   must consume a probability, not a hard label.

---

### 7. Macey, T. (Interviewer) & Ratner, A. (2018). Snorkel: Extracting Value from Dark Data (Episode #15).

**Citation:** Macey, T. (Interviewer). (2018, 22 January). *Episode #15: Snorkel: Extracting value from dark data* [Audio podcast]. Data Engineering Podcast. https://www.dataengineeringpodcast.com/snorkel-with-alex-ratner-episode-15/

**Purpose:** Snorkel co-creator **Alex Ratner** (Stanford, Christopher Ré's HazyResearch/DAWN lab) on the **dark data** problem and how weak supervision **democratises** ML for organisations without giant labelled datasets.

---

#### 1. Dark data + democratisation
- **Dark data** = the vast majority of enterprise knowledge that is **unstructured and untapped** (not the clean,
  structured sets most ML talks assume). Snorkel targets **extracting value from it**.
- **Domain experts write labelling functions** to programmatically **generate training sets** - no manual labelling
  marathon. This **democratises ML**: it becomes feasible for orgs with **smaller datasets** than mainstream tooling
  demands. (Origin: **DARPA Memex**; used in domains like the FDA, National Library of Medicine, conflict studies.)

#### 2. Architecture (same two-stage design as R6)
- **Generative model** learns to weight/de-noise the LFs → **probabilistic training labels** → a **discriminative
  model** (PyTorch/TensorFlow) trains on them. Poorly suited when you **can already easily get abundant gold labels**
  (then just supervise directly).

#### Key Takeaways for MLN601
1. **Dark data + democratisation** is the "why it matters" business case for weak supervision - pairs with Bell's
   (R6) "how it works."
2. Same **generative → discriminative** architecture confirmed from the source - reinforces the Activity 2 mechanics.
3. **Snorkel came from academic research (Stanford)** now widely used - a credible portfolio talking point.

---

### 8. Powell, A. (2020). The Cold-Start Problem with Stanford Snorkel.

**Citation:** Powell, A. (2020, 8 February). *The cold-start problem with Stanford Snorkel*. Analytics Vidhya (Medium). https://medium.com/analytics-vidhya/the-cold-start-problem-with-stanford-snorkel-6fc5b55ec216

**Purpose:** An honest, hands-on field report - a practitioner's real experience using Snorkel on an authorship-attribution task, including where it under-delivers.

---

#### 1. The cold-start problem + how he used it
- **Cold-start problem:** you want `ŷ` from `X`, but you have **no `y`** to train on. Hand-labelling (or paying
  **Mechanical Turk**) is costly and **inconsistent between humans** - the motivation for Snorkel.
- **His workflow:** (1) hand-label **~100 messages** as a **gold standard**; (2) write a few **labelling functions**
  and iterate; (3) validate coverage/conflict as you write; (4) stop when the golden set hits **~90%**; (5) train a
  model on the Snorkel-labelled data and test on a held-out set.

#### 2. LF-writing tips + honest verdict
- **Tips:** balance positive/negative LFs; **don't fear conflicting LFs** (insightful > perfectly logical); aim for
  **high coverage**; always keep a **golden hold-out set** ("the labellers are not humans - only you know the true
  label").
- **Verdict (refreshingly mixed):** often the simple **majority-label rule beat** the probabilistic Snorkel method on
  his gold set; he got **>90%** but was **unsure it beat just labelling more by hand** as a sole contributor.
  Snorkel's diagnostics (**conflict, polarity, coverage**) were useful. Its real payoff is the **many-noisy-labellers
  / Mechanical-Turk** setting - exactly Bell's (R6) point.

#### Key Takeaways for MLN601
1. A **concrete, reproducible recipe** for **Activity 2**: gold set → LFs → iterate to ~90% → train → test.
2. **Honest limitation:** for a single expert with time, hand-labelling may still win; Snorkel shines when labels are
   **many, noisy, and crowd-sourced** - a nuanced take worth citing in the forum post.
3. **coverage / conflict / polarity** are the LF-quality diagnostics to actually watch - the practical version of
   Bell's "LF-density Goldilocks" point.

---

## Synthesis - how the eight fit together

```
   THE PRODUCTION BOTTLENECK              THE LABEL BOTTLENECK
   (get the model OUT the door)           (get the training DATA)

  notebook is <20% of the job           labels are scarce/slow/costly
   (Dewalt R1, Agrawal R5)                (Bell R6, Ratner R7)
        │                                       │
  5 hard truths: team, PM,               engineer the LABELS:
   ground-truth, metrics, DevOps          expert systems→features→
   (Casey R2)                             architecture→labels (R6)
        │                                       │
  survey reality: 55% never              Snorkel: LFs (+1/−1/0)
   deploy; 31-90 days; scale              → generative model
   is #1 (Algorithmia R4)                 → probabilistic labels
        │                                 → discriminative model
  the 10-yr vision: train in                    │
   cloud, SCORE IN THE DBMS,             works best with MANY NOISY
   govern everywhere (R5)                 labellers; honest caveats
        │                                 (Powell R8)
  "next trillion $" accrues to
   3 company types (Xu R3)
```

**The through-line:** Module 12 is the **"from notebook to the real world"** module. ML value is blocked by two
bottlenecks. **Production:** a trained model is <20% of the work; the last mile (deployment, scaling, versioning,
governance) is where **55% of companies get stuck** - solved by **MLOps, the data-engineer role, and Agrawal's vision
of scoring models inside the DBMS** with governance throughout. **Labels:** supervised ML starves without labelled
data, and hand-labelling does not scale - solved by **weak supervision (Snorkel)**, where domain experts write noisy
**labelling functions** that a **generative model** fuses into **probabilistic labels** to train a normal
**discriminative model**. The three activities exercise both halves: **Azure SQL Edge + ONNX** (model-in-DBMS / edge),
the **Snorkel spam tutorial** (weak supervision hands-on), and the **human factor** (change management to get an
enterprise to actually adopt ML).

> **Assessment link:** this module directly feeds **Assessment 3 - Machine Learning Project** (notebook + model
> selection, up to 2000 words, 40%, due **19/08/2026**, SLOs a/b/c/d). It is the **deployment/communication** end of
> CRISP-DM: justify not just the model but how it would be **productionised, governed, and kept fed with data** - the
> difference between a notebook and an enterprise system.
