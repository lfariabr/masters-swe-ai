# Module 2: Managing Machine Learning Projects: CRISP-DM, Ethics by Design (Australasia), and Data Sets

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Watch & summarise Houston Analytics / Shearer (2017) — the timeless value of CRISP-DM | ✅ |
| **2** | Read & summarise Leaper (2009) — a visual guide to CRISP-DM methodology | ✅ |
| **3** | Read & summarise Tyagi (2020) — task checklist for almost every ML project | ✅ |
| **4** | Read & summarise Studer et al. (2020) — Towards CRISP-ML(Q) | ✅ |
| **5** | Read & summarise Clark (2018) — the machine learning audit (CRISP-DM framework) | ✅ |
| **6** | Read & summarise Cunningham (2020) — ethical CRISP-DM: the short version | ✅ |
| **7** | Activity 1: load CRISP-DM template + draft forum question — see [activities](module02_activities.md#activity-1--loading-up-the-crisp-dm-template) | ✅ draft |
| 8 | Activity 2: replicate Mishra (2019) vgsales notebook + draft reflection — see [activities](module02_activities.md#activity-2--understanding-crisp-dm-using-video-game-sales-data-mishra-2019) | 🔥 |

---

## Key Highlights

### 1. Houston Analytics (2017). The Timeless Value of CRISP-DM

**Citation:** Houston Analytics. (2017, 7 April). Colin Shearer: CRISP DM [Video file]. Retrieved from https://www.youtube.com/watch?v=-K-GGW9827Q

**Purpose:** A first-hand account from **Colin Shearer**, one of the originators of CRISP-DM, on why a 1990s data-mining methodology is still the de facto standard for advanced analytics. It frames the *why* behind the framework before the other resources drill into the *how*.

---

#### 1. How CRISP-DM Was Built (and why that matters)
- Born in the **early days of data mining**, out of a worry shared by practitioners: *"are we doing things the right way?"*
- Vendors (tool suppliers) + the first large-scale industrial users formed a **consortium** to distil their experience into something **repeatable, usable and effective**.
- **Key surprise:** they expected huge diversity in how people worked, but found **uniformity** — the same basic "formula for success", just under different labels. That convergence is *why* the model generalises.

#### 2. Why It Has Endured
- **"Frankly, because it works."** Still the de facto standard methodology for advanced analytics.
- **Generality** — the same framework guides *customer analytics*, *IoT machine-health prediction*, and *healthcare diagnosis/treatment* alike.
- **Business-anchored** — the single most important property: **CRISP-DM starts and ends at the business level**, not the technology level.

| Direction | What happens |
|-----------|--------------|
| **Top-down** | Define business goals → challenges → success measures → **map down** to technical/analytical goals |
| **Apply** | Use analytics technology to address those technical goals; measure technical accuracy |
| **Bottom-up** | **Map results back up** to the business level; evaluate against **business success criteria** |

> 🔑 *"It's not about the technology… it's about ensuring you use advanced analytics to deliver satisfactory business outcomes and the best possible business value."*

#### Key Takeaways for Machine Learning (MLN601)
1. **Frame before you fit.** Every assessment notebook should open by stating the *business* question and a measurable success criterion — the same `business → ML → business` round-trip you'll formalise in CRISP-ML(Q) (Resource 4).
2. **The methodology is the constant, the algorithm is the variable** — this echoes Module 1's takeaway that the value lives in the workflow, not in any single clever model.
3. Directly relevant to my own projects (Review Pulse, ClinicTrendsAI): a high test F1 means nothing if it doesn't map back to a stakeholder decision.

---

### 2. Leaper (2009). A Visual Guide to CRISP-DM Methodology

**Citation:** Leaper, N. (2009, 13 March). A visual guide to CRISP-DM methodology. Retrieved from https://exde.wordpress.com/2009/03/13/a-visual-guide-to-crisp-dm-methodology/

**Purpose:** A single-page poster that lays out **all six phases of CRISP-DM 1.0 (1999)** together with the generic tasks and output documents of each — the missing "one diagram" that the original spec never provided.

---

#### 1. The Six Phases (the Data Mining Life Cycle)

| # | Phase | One-line intent |
|---|-------|-----------------|
| 1 | **Business Understanding** | Identify project objectives |
| 2 | **Data Understanding** | Collect and review data |
| 3 | **Data Preparation** | Select and cleanse data |
| 4 | **Modeling** | Manipulate data and draw conclusions |
| 5 | **Evaluation** | Evaluate model and conclusions |
| 6 | **Deployment** | Apply conclusions to the business |

- The phases form a **loop**, not a straight line — arrows run *forward* and *backward* (e.g. Modeling ↔ Data Preparation), with an outer **life-cycle ring** back from Deployment to Business Understanding.

#### 2. Generic Tasks → Output Documents (per phase)

| Phase | Generic tasks (selected) | Key outputs |
|-------|--------------------------|-------------|
| Business Understanding | Determine business objectives; assess situation; determine **data-mining goals**; produce project plan | Background, success criteria, risks/costs, project plan |
| Data Understanding | Collect initial data; describe; explore; **verify data quality** | Data collection / description / exploration / **quality** reports |
| Data Preparation | Select; **clean**; construct (derived attributes); integrate; format | Cleaned dataset + rationale for inclusion/exclusion |
| Modeling | Select technique; generate **test design**; build model; **assess model** | Model + test design + model assessment + revised parameters |
| Evaluation | **Evaluate results vs business success criteria**; review process; determine next steps | Approved models, list of possible actions, decision |
| Deployment | Plan deployment; **plan monitoring & maintenance**; produce final report; review project | Deployment + monitoring plan, final report, lessons learned |

- The poster distinguishes three reading levels: **Generic Tasks** → **Specialized Tasks** → **Process Instances**, and stamps *"(Log and Report Process)"* on almost every step — documentation is treated as a first-class deliverable.

#### Key Takeaways for Machine Learning (MLN601)
1. This is the **canonical reference diagram** for the subject — worth sketching by hand once so the 6 phases + their loops are muscle memory.
2. Note the two things CRISP-DM 1.0 *under-specifies* and that later resources fix: **no explicit monitoring/maintenance after deployment** (added in CRISP-ML(Q), Resource 4) and **no ethics questions** (added by Cunningham, Resource 6).
3. "Verify data quality" and "data preparation" being their *own* phases reinforces the module sub-theme — **data sets and missing values** are where most project time actually goes.

---

### 3. Tyagi (2020). Task Cheat Sheet for Almost Every ML Project

**Citation:** Tyagi, H. (2020, 4 July). Task cheatsheet for almost every machine learning project. A checklist of tasks for building end-to-end ML projects. Retrieved from https://towardsdatascience.com/task-cheatsheet-for-almost-every-machine-learning-project-d0946861c6d0

> *Note: the saved PDF carries the byline "Selva Prabhakaran / MachineLearningPlus" — the same checklist content circulates under both names. Cited here as listed in the module notes.*

**Purpose:** A hands-on, periodically-reusable checklist for end-to-end ML projects. The author never names CRISP-DM, but the structure is **CRISP-DM repurposed** — exactly the point the module makes ("he has clearly repurposed the methodology as his own").

---

#### 1. The Checklist Mapped onto CRISP-DM

| Checklist section | CRISP-DM phase |
|-------------------|----------------|
| 1. Define the DS problem from a **business pain point** | Business Understanding |
| 2. Discover data sources & map associations | Data Understanding |
| 3. Clean, transform & engineer features | Data Preparation |
| 4. Deep-dive **EDA** | Data Understanding ↔ Preparation |
| 5. Develop ML models | Modeling |
| 6. Fine-tune & iteratively improve | Modeling |
| 7. **Model interpretability** | Evaluation |
| 8. Deploy in production | Deployment |
| 9. Extra checks for senior DS/managers | Business + Deployment |

#### 2. The Highest-Value Practical Reminders
- **Frame the problem first:** *Is ML even the right approach, or would a quick rule-based solution do?* Decide problem type (supervised / unsupervised / clustering / recommendation / optimization) and the label **Y** before touching data.
- **Baseline models:** start with **regularized logistic regression for classification**, Random Forest for regression. (This is *exactly* the baseline I used in Review Pulse.)
- **Class imbalance:** check the naive-prediction performance first; pick an imbalance strategy before celebrating accuracy.
- **Avoid data leakage:** *"suspect if model performance is too good."* Use **k-fold cross-validation**.
- **Interpretability toolkit:** Feature Importances, **PDP / ICE plots, SHAP values, LIME**, tree interpreters, confusion matrices.
- **Deployment ≠ done:** monitor **data drift, target drift, model drift**, and performance degradation; budget for **retraining**.

#### 3. The Non-Technical Questions That Sink Projects
Senior-level checks to clarify *at the start*: Who are the end users? Do they understand ML? How many will use it and for how long? How often must it be retrained (and is that cost budgeted)? Is a staging environment needed? Is RACI defined?

#### Key Takeaways for Machine Learning (MLN601)
1. This is the **operational companion** to the abstract CRISP-DM diagram — keep a living task list inside the Jupyter notebook for each assessment (A1 wk4 regression, A2 wk8 classification, A3 wk12 regression).
2. The "regularized logistic regression as classification baseline" line connects straight to my Module 1 insight and to Review Pulse's TF-IDF + Logistic Regression baseline.
3. The "data leakage = suspiciously good performance" warning is the same discipline CRISP-ML(Q) (Resource 4) formalises as a **test-set leakage risk**.

---

### 4. Studer et al. (2020). Towards CRISP-ML(Q): A Machine Learning Process Model with Quality Assurance Methodology

**Citation:** Studer, S., Bui, T. B., Drescher, C., Hanuschkin, A., Winkler, L., Peters, S. & Mueller, R. (2020, 11 March). Towards CRISP-ML(Q): A machine learning process model with quality assurance methodology. Manuscript submitted for publication. Retrieved from https://arxiv.org/pdf/2003.05155.pdf

**Purpose:** The academic heavyweight of the module. It extends CRISP-DM into a process model purpose-built for **ML applications** (deployed + maintained, not one-off data mining), attaching **per-task Quality Assurance (Q)** to mitigate risks. Motivated by a stark stat: **75–85% of practical ML projects miss their sponsors' expectations.**

---

#### 1. Why CRISP-DM Falls Short for ML — Two Shortcomings
- **(a) Long-running inference & model degradation.** Data mining *extracts* knowledge once; an **ML application** trains a model then **infers on new data over a long period**. A changing environment degrades performance, so **permanent monitoring/maintenance** is required — which CRISP-DM omits.
- **(b) No quality-assurance methodology.** CRISP-DM tells you *what* tasks to do but not *how* to verify each was done well. Quality here = fitness for purpose **plus** the quality of every task execution (catch errors early → cheaper than fixing them late).

#### 2. The Six Phases — CRISP-ML(Q) vs CRISP-DM

| CRISP-ML(Q) | CRISP-DM | Change |
|-------------|----------|--------|
| **Business & Data Understanding** | Business Understanding + Data Understanding | **Merged** (objectives depend on available data) |
| Data Preparation | Data Preparation | same |
| Modeling | Modeling | + QA |
| Evaluation | Evaluation | + QA |
| Deployment | Deployment | + QA |
| **Monitoring & Maintenance** | — | **New 6th phase** |

#### 3. The QA Loop (applied to every task)
`Define requirements & constraints → instantiate step/task → identify risks → if risks not feasible, choose a QA method to mitigate → repeat until phase finished.`

#### 4. Three Levels of Success Criteria (defined up front, kept consistent)

| Level | Question | Example |
|-------|----------|---------|
| **Business** | Purpose from a business view | "failure rate < 3%" |
| **ML** | Business objective translated to a metric | "accuracy > 97%" |
| **Economic (KPI)** | Economical relevance | "cost savings per automated check" |

#### 5. Six Model Quality Measures (don't optimise accuracy alone)

| Measure | Meaning |
|---------|---------|
| **Performance** | Accuracy on unseen data |
| **Robustness** | Resilience to inconsistent inputs / runtime failures |
| **Scalability** | Handles high data volume in production |
| **Explainability** | Direct or post-hoc interpretability |
| **Model Complexity** | Capacity suited to data complexity |
| **Resource Demand** | Compute/memory cost to deploy |

- **No Free Lunch theorem:** no model is best on all problems → **start with a low-capacity baseline and increase capacity only when validation proves it helps.**
- **Reproducibility** is split into *method* (share data, hyper-params, **random seeds**, runtime) and *result* (report mean ± variance across seeds, not just the top run).

#### 6. Monitoring & Maintenance — Why Models Go Stale
Root cause: production data drifts from the training distribution. Three drivers:

| Cause | Example |
|-------|---------|
| **Non-stationary data distribution** | Stock-market data shifts fast; elephant images don't |
| **Hardware degradation** | Sensors get noisier / fail over time |
| **System updates** | A software update silently changes a signal's units |

→ **Monitor** (compare incoming stats vs training stats; flag anomalies via the data schema) → **Update** (re-collect/label, prefer **fine-tuning** over training from scratch, re-evaluate before redeploy, keep a **fallback** to a previous model).

#### Key Takeaways for Machine Learning (MLN601)
1. This paper is the bridge from "classical CRISP-DM" to modern **MLOps** — the Monitoring & Maintenance phase is what makes a model a *product*.
2. **Fixed seeds, explicit splits, tracked metrics, no leakage** (the repo's ML guidelines) are *literally* the QA methods named here — cite this paper when justifying those choices in assessments.
3. The 75–85% failure stat + "right answers to the wrong questions" is the strongest argument for the business-first framing from Resource 1.
4. The six quality measures give me a ready-made evaluation rubric beyond F1 for Review Pulse / ClinicTrendsAI write-ups.

---

### 5. Clark (2018). The Machine Learning Audit (CRISP-DM Framework)

**Citation:** Clark, A. (2018, 6 January). The machine learning audit—CRISP-DM framework. ISACA Journal, 1, 1–6. Retrieved from https://www.isaca.org/-/media/files/isacadp/project/isaca/articles/journal/2018/volume-1/the-machine-learning-audit-crisp-dm-framework_joa_eng_0118.pdf

**Purpose:** Reframes CRISP-DM as an **audit framework**, so an auditor (even without deep ML maths) can give **high-level assurance** that an ML system is sound and unbiased. A different lens on the same six phases — "the ability to audit ML projects is likely to become a highly sought-after skill."

---

#### 1. The Audit Strategy — Pareto + Sampling
- Apply the **80/20 principle**: ~80% of audit value comes from ~20% of the work (a high-level CRISP-DM walkthrough), with deeper assurance if SMEs examine each step.
- The one step that needs **no advanced maths**: **sampling**. Feed a **pseudo-dataset** of crafted inputs into the live model and inspect outputs for bias — *without* needing to explain how the model works internally. This yields **practical accuracy** vs the **mathematical accuracy** data scientists train on.

#### 2. The Six Phases Through an Auditor's Eyes

| Phase | Audit focus |
|-------|-------------|
| **Business Understanding** | What's the use case? Which attributes belong in the model (income, job title, education)? Iterative — revisited often |
| **Data Understanding** | Watch **scales** (Celsius/Fahrenheit, km/miles); examine **correlation & covariance** matrices for conflicting/biasing variables |
| **Data Preparation** | Preprocessing (regex to extract e.g. an IP from logs); **z-score standardization** (mean 0, sd 1) removes individual scales |
| **Modeling** | Hyper-parameters & grid search; **local vs global minima**; **GDPR "right to explanation"** rules out black-box models (e.g. non-linear SVM) where explanations are required |
| **Evaluation** | **Most important from an audit view** — 90% accuracy can still **violate business principles** (e.g. discriminating by zip code). Build a test grid across zip/income/ethnicity to expose unintended effects |
| **Deployment** | Watch **technical debt**, especially **correction cascades** (rule-based "fixes" stacked on a model that cap its learning capacity) |

#### 3. The Train/Test Discipline (called out as a key checklist item)
- *"An extremely important ML audit checklist item should be examining if the data were bifurcated into training and test sets."*
- Traditional **80/20 split** → modern best practice **k-fold cross-validation** to guard against **overfitting**.
- **LIME** and **FairML** are named as interpretability tools that plug into the **Evaluation** phase (they explain weights, but aren't a holistic risk view — hence CRISP-DM around them).

#### Key Takeaways for Machine Learning (MLN601)
1. Auditing reframes **Explainable AI** (Module 1) as a *governance* requirement, not a nicety — "high accuracy" is not the same as "acceptable".
2. The **bias-by-sampling** technique is a concrete, examinable method for the ethics/data-sets theme of this module.
3. **Technical debt / correction cascades** connect directly to CRISP-ML(Q)'s Monitoring & Maintenance — both warn that the cost of an ML system is mostly *after* deployment.
4. The GDPR "right to explanation" point is a ready citation for why interpretable baselines (logistic regression) can beat black boxes in regulated settings.

---

### 6. Cunningham (2020). Ethical CRISP-DM: The Short Version

**Citation:** Cunningham, C. (2020, 11 April). Ethical CRISP-DM: The short version [Web log post]. Retrieved from https://blogs.ischool.berkeley.edu/w231/2020/04/15/ethical-crisp-dm-the-short-version/

**Purpose:** Bolts an **ethical guardrail** onto each CRISP-DM phase by attaching **one reflection question per stage**. Directly serves the module's "Ethics by Design" sub-theme — ethics is built *into* the workflow, not added afterwards.

---

#### 1. Why Ethics Belongs in the Process
- Junior data scientists are trained on **manicured academic datasets**; reality is **vague requirements, messy/non-existent data, and causality hidden behind spurious correlations**.
- CRISP-DM smooths that academia→industry transition — but the *singular* lesson the author would teach is **ethics**: *"Without instilling ethics… we are arming millions of young professionals with tools of immense power but no notion of responsibility."*

#### 2. One Ethical Question per Phase

| CRISP-DM phase | Ethical question | Anchor example |
|----------------|------------------|----------------|
| **Business Understanding** | What are the potential **externalities** of this solution? | Lean on domain SMEs to spot who's affected |
| **Data Understanding** | Does my data reflect **unethical bias**? | Humans are biased → human-generated data inherits it |
| **Data Preparation** | How do I **cleanse data of bias**? | Filtering racist words is easy; removing sex↔career correlations is hard — impossible to fully scrub, still worth attempting |
| **Modeling** | Is my model prone to **outside influence**? | **Microsoft Tay** — Twitter users perverted the model into a racist bot |
| **Evaluation & Deployment** | How can I **quantify an unethical consequence**? | **Predictive policing** must monitor crime distribution to avoid over-policing |

#### 3. The Core Principle
> *"Ultimately, we are responsible for the entire products we deliver, including their consequences."* Ethical CRISP-DM enforces a **regime of reflection throughout the development lifecycle.**

#### Key Takeaways for Machine Learning (MLN601)
1. Pairs cleanly with Clark (Resource 5): Cunningham asks the **ethical questions**, Clark gives the **audit techniques** (sampling/test grids) to *answer* them.
2. The five questions are a lightweight, examinable checklist to drop into any assessment notebook's introduction and conclusion.
3. **Tay** and **predictive policing** are vivid, citable cautionary tales for the "real applications raise fairness/governance concerns" thread running from Module 1.

---

## Module 2 Synthesis — One Skeleton, Four Lenses

CRISP-DM's six phases are the spine; each resource views them differently:

| Lens | Resource | What it adds |
|------|----------|--------------|
| **Origin / why** | Shearer (2017) | Business-anchored, general, "it works" |
| **Reference map** | Leaper (2009) | The canonical 6-phase diagram + outputs |
| **Operational** | Tyagi (2020) | A reusable end-to-end task checklist |
| **Modernised + QA** | Studer et al. (2020) | Merged understanding phase + Monitoring/Maintenance + per-task quality assurance |
| **Governance** | Clark (2018) | CRISP-DM as an audit framework (bias by sampling) |
| **Ethics** | Cunningham (2020) | One ethical question per phase |

**Through-line:** the framework is the constant; rigour (honest splits, no leakage, fixed seeds, interpretability) and **responsibility** (bias, fairness, monitoring) are what turn a model into a trustworthy product.
