# Module 7 — Automated and Explainable Machine Learning

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Watch & summarise Olson (2018) — the past, present & future of Auto ML (TPOT) | ✅ |
| 2 | Listen & summarise Linear Digressions (2018) — AutoML podcast | 🔥 needs manual listen |
| **3** | Read & summarise Mark (2020) — awesome-autoML-papers (curated map) | ✅ |
| **4** | Watch & summarise Aha (2019) — DARPA Explainable AI (XAI) colloquium | ✅ |
| **5** | Watch & summarise Sowden (2018) — transparency & accountability of NZ government algorithms | ✅ |
| **6** | Read & summarise Molnar (2019) — Interpretable ML book (Ch. 4 focus) | ✅ |
| 7 | Activity 1: Google What-If Tool — probe 2+ notebooks (wine, COMPAS, census, smile) | 🕐 |
| 8 | Activity 2: IBM AI Explainability 360 — bank-loan scenario (CEM + Protodash explainers) | 🕐 |
| 9 | Activity 3: SHAP + explainerdashboard on the Titanic classifier | 🕐 |

---

## Key Highlights

### 1. Olson, R. (2018). The past, present and future of automated machine learning.

**Citation:** Olson, R. (2018, 15 July). The past, present, and future of automated machine learning [Video file]. https://www.youtube.com/watch?v=QrJlj0VCHys

**Purpose:** Dr Randal Olson (creator of TPOT) explains what Auto ML actually is, why it saves time, and demos an Auto ML run live in a scikit-learn notebook. This is the anchor "what is Auto ML" resource for the module.

---

#### 1. What Auto ML is (and is not)

- **The one-sentence answer:** "Auto ML aims to automate the process of applying machine learning algorithms to data sets." Everything else is detail.
- **What it is NOT:** early-90s "Auto ML" that only did **hyperparameter tuning** (grid/random search) over a fixed model. Olson is emphatic: *tuning alone is not modern Auto ML*. Many commercial tools mis-sell tuning as Auto ML.
- **Modern Auto ML** tunes the **entire pipeline** — data cleaning → pre-processing → feature construction/selection → model selection → hyperparameters — as one optimisation problem.

| | Early Auto ML (90s) | Modern Auto ML |
|---|---|---|
| Scope | tune params of one chosen model | tune the whole ML pipeline |
| Search | grid search, random search | meta-learning, **Bayesian optimisation**, **genetic programming**, multi-armed bandits |
| Why the change | small search space (2-3 params) | pipelines = huge, combinatorial search space |

#### 2. Why Auto ML is worth it — three evidence-backed advantages

- **Default parameters are almost always bad.** Across ~160 datasets, tuning gives ~**5% average accuracy lift** (small but real, and free if automated).
- **No single best algorithm** (the "gladiator ring" experiment): gradient boosting / random forests / SVM usually win, but even Naive Bayes beats them on ~1% of problems. Humans get **biased** toward favourite algorithms (Olson admits his is XGBoost); Auto ML has no such bias and tries everything.
- **Time saver:** survey said **~60% of a data scientist's time is data cleaning/organising**. Auto ML increasingly absorbs that grunt work.

#### 3. The tool landscape + the honest caveat

- **TPOT** (Olson's tool) — genetic-programming search, drops straight into scikit-learn as `TPOTClassifier` (same `.fit()`/`.score()` API). "Generations" of candidate pipelines evolve toward better 5-fold CV scores.
- Others: **Auto-sklearn / Auto-WEKA** (first movers, Bayesian), **H2O AutoML** (great web UI), plus deep-learning variants and commercial **DataRobot**.
- **Caveat (critical for exams):** Auto ML is a **productivity tool, NOT a data-scientist replacement** — "do not believe" vendors who say otherwise. It is also **slow** — treat it like an assistant you fire off and check back on hours/a day later.

#### Key Takeaways for MLN601
1. Directly seeds **Activity 1's wine-model comparison** and the whole "let the tool try many models" mindset — the same philosophy behind comparing Decision Tree / LogReg / Naive Bayes / SVM in **Assessment 2**.
2. Pairs with the Awesome-AutoML map (Res. 3) — Olson gives the intuition, Mark gives the taxonomy.
3. Practical: the 5% tuning lift + "no best algorithm" justify why A2/A3 should compare several classifiers rather than defend one.

---

### 3. Mark, L. (Ed.). (2020). Awesome-autoML-papers.

**Citation:** Mark, L. (Ed.). (2020, 15 August). Awesome-autoML-papers. https://github.com/hibayesian/awesome-automl-papers

**Purpose:** A curated map of the Auto ML research field — the taxonomy that organises the ideas Olson demos. Use it as a reference index, not a read-through.

---

#### 1. The five automation domains

AutoML = "making ML available to non-ML experts" by automating what used to need expertise:

| Domain | What it automates |
|---|---|
| Automated data cleaning | fixing/formatting raw data |
| **Automated feature engineering** (AutoFE) | expand-reduce & hierarchical feature transforms |
| **Hyperparameter optimisation** (HPO) | tuning model settings |
| **Meta-learning** | reusing knowledge from prior tasks/datasets |
| **Neural architecture search** (NAS) | designing network topologies |

#### 2. The optimisation approaches (the engine room)

- **Bayesian optimisation** — the dominant HPO method (builds a surrogate model of the search space; matches Olson's "red = promising, guess where to try next" animation).
- **Random search & Hyperband** — cheap, surprisingly strong baselines.
- **Evolutionary / genetic programming** — TPOT's approach; "generations" of pipelines.
- **Reinforcement learning** — mainly for NAS and feature engineering.
- **Meta-learning / transfer learning** — warm-start from past problems.

#### 3. Tools cross-referenced

Auto-sklearn, TPOT, Auto-WEKA, Auto-Keras, H2O AutoML, Google AutoML, plus HPO libraries **Hyperopt, Optuna, SMAC3**.

#### Key Takeaways for MLN601
1. Gives the vocabulary (HPO, NAS, AutoFE, meta-learning) to *name* what Olson demos.
2. Optuna/Hyperopt are the practical HPO libraries you could bolt onto an A2/A3 pipeline if you want tuning beyond `GridSearchCV`.
3. Reference-only — cite it for the "AutoML field landscape" claim; don't try to read every paper.

---

### 4. Aha, D. (2019). DARPA Explainable AI (XAI) colloquium.

**Citation:** Aha, D. (2019, 26 March). Artificial intelligence colloquium: Explainable AI. https://www.youtube.com/watch?v=YSsYXAn_L00

**Purpose:** David Aha (US Naval Research Lab, XAI evaluation lead) frames *why* explainability matters in high-stakes settings and walks through six concrete DARPA techniques. This is the flagship "explainability" resource.

---

#### 1. The core problem & the core trade-off

- **The problem:** a model outputs a prediction **with no justification** — leaving users (especially in critical apps) unable to answer *why did it do that? when can I trust it? what will it do next?*
- **The XAI fix:** produce an **explainable model** + an **explanation interface** the user can interrogate.
- **The central trade-off — performance vs. explainability:** deep learning boosted accuracy on raw sensor data *at the cost of* explainability. XAI's goal is the **top-right corner**: high accuracy AND high explainability, not one or the other.

#### 2. Six techniques (3 data-analytics, 3 autonomy)

| # | Method (team) | What it explains | How |
|---|---|---|---|
| 1 | **RISE** (BU/Berkeley) | "why this prediction?" | mask random image regions, see which flips the output → **saliency heat maps**; works on **any black box** |
| 2 | **Network Dissection** (MIT/Raytheon) | "what's inside the model?" | probe hidden units with concept images → label each unit's **semantics** (detects trees, faces…) |
| 3 | Differentiable physics engine | faster + explainable RL | embed a physics model in a network layer → Atari training drops from 10^8 to 10^4 steps |
| 4 | Finite-state extraction (Oregon State) | policy of an RNN agent | splice **quantized bottleneck networks** in → extract simple **Moore machines**; found Pong ignores memory, Bowling ignores inputs |
| 5 | Self-driving explanation (UCB) | why the car acted | heat maps + attention → **video-to-text** natural-language justifications grounded in what the controller saw |
| 6 | (causal / stochastic / probabilistic-logic models) | broader XAI | listed as the wider program beyond deep learning |

#### 3. What the human-subject evaluation found

- Users **given explanations perform better** and prefer to use them.
- Explanations engender **appropriate trust** and help align the user's mental model with the system.
- **Key danger:** an **incorrect explanation is actively damaging** to trust — worse than none. This is now a focus area (with a psychology-of-explanation sub-team).

#### Key Takeaways for MLN601
1. Provides the "why explainability matters" argument for the module intro (the bank-loan / high-stakes framing) and for **Activity 2** (IBM AIX360 bank loan).
2. RISE = the intuition behind saliency/heat-map methods; conceptually cousins of **SHAP/LIME** (Res. 6, Activity 3) — all answer "which inputs drove this prediction?"
3. The "incorrect explanation is damaging" point is a strong, quotable exam line on the *risks* of XAI.

---

### 6. Molnar, C. (2019). Interpretable Machine Learning.

**Citation:** Molnar, C. (2019). Interpretable machine learning: A guide for making black box models explainable. https://christophm.github.io/interpretable-ml-book/ (read Ch. 4)

**Purpose:** The standard free reference on *how* to make models interpretable. Gives the taxonomy (intrinsic vs post-hoc, global vs local) and the named methods you will use in the activities.

---

#### 1. Two ways to get interpretability

| | Intrinsically interpretable | Post-hoc / model-agnostic |
|---|---|---|
| Idea | model is transparent by design | explain *any* trained black box afterward |
| Examples | linear reg, **logistic reg**, GLM/GAM, **decision trees**, decision rules, RuleFit | SHAP, LIME, permutation importance, PDP, ALE |
| Cost | may sacrifice some accuracy | keeps the accurate model, adds an explanation layer |

- Why those models are "interpretable": their decision logic is **directly readable** — a linear coefficient = effect per unit; a tree = a followable path of if/else splits.

#### 2. Two scopes of interpretation

- **Global** — the model's *overall* behaviour / general feature→prediction relationships. Methods: **permutation feature importance**, **partial dependence plots (PDP)**, accumulated local effects (ALE).
- **Local** — *one individual prediction*. Methods: **LIME**, **SHAP / Shapley values**, counterfactual explanations.

#### 3. The named model-agnostic methods (map these to the activities)

- **SHAP (SHapley Additive exPlanations):** attributes a prediction to each feature's contribution using cooperative-game Shapley values (1953). Both local (per-instance) and can aggregate to global. → **Activity 3**.
- **LIME:** fits a simple local surrogate around one prediction.
- **Permutation feature importance:** shuffle a feature, measure the drop in performance = its importance (global).
- **Partial dependence plot:** how the average prediction changes as one feature varies (global).

#### Key Takeaways for MLN601
1. This is the **methods backbone** of the module's activities: SHAP + the explainerdashboard (Activity 3) sit directly on Ch. 4/SHAP; the What-If tool (Activity 1) and AIX360 (Activity 2) are UIs over these same ideas.
2. The intrinsic-vs-post-hoc split explains why earlier modules' **decision trees / logistic regression** were "interpretable by design," while SVM/deep nets need post-hoc tools.
3. Global vs local is the exam distinction: "feature importance = global, SHAP-on-one-passenger = local."

---

### 2. Kennedy, M., Jaffe, B. & Malone, K. (2018). AutoML — Linear Digressions podcast. — 🔥 needs manual listen

**Citation:** Kennedy, M. Jaffe, B. & Malone, K. (2018, 29 April). AutoML [Audio podcast]. http://lineardigressions.com/episodes/2018/4/29/automl

No local transcript available and no public transcript URL in the resource overview. Listen manually (it covers the same "AutoML in plain English" framing as Olson). Summarise after listening.

### 5. Sowden, M. (2018). Transparency and accountability of government algorithms.

**Citation:** Sowden, M. (2018, 15 July). Transparency and accountability of government algorithms [Video file]. https://www.youtube.com/watch?v=Jpbd-5r3xO8

**Purpose:** Mark Sowden (NZ Government Statistician / Chief Data Steward, Stats NZ) gives the **governance and policy** angle on explainability — how a *government* makes its algorithmic decision-making transparent and accountable to citizens. Complements Aha's technical XAI (Res. 4) with the "so what should institutions actually do?" answer.

---

#### 1. The trigger: algorithms in public service delivery

- Growing use of algorithms in **services delivered to New Zealanders** prompted a **2018 government-wide review**.
- Scope: how the **14 biggest data agencies** use algorithms that **inform significant decisions** about people.
- Assessed against **6 principles for safe & effective data use**, co-developed with the **NZ Privacy Commissioner**.
- Output: the **Algorithm Assessment Report** — tells citizens how algorithms are (and are *not*) used in decision-making, and what data/ethics safeguards exist.

#### 2. What the review found

- Good safeguards already in place, **but** more was needed on **including citizens' views** in how algorithms are developed and used — i.e. more **transparency and accountability**.

#### 3. Three concrete responses (the actionable part)

| Initiative | What it is |
|---|---|
| **Algorithm Charter** | a public commitment agencies sign up to, on transparency & accountability to their customers |
| **Data Ethics Advisory Group** | external experts reviewing innovative/ethical data use; fostering public debate on *when* to use algorithms |
| **Workforce data-ethics uplift** | building data-ethics understanding across the government workforce that handles data |

- **The balance he's after:** access the *power* of algorithms to deliver better services **while keeping public trust and confidence**.

#### Key Takeaways for MLN601
1. This is the **institutional/regulatory** complement to the module's technical XAI — the same trust concern as Aha (Res. 4), but answered with *charters, ethics boards and accountability*, not heat maps.
2. Directly reinforces **Activity 2's** legal-obligation twist (bank *must* explain a loan rejection): explainability is not just a technique, it's a **governance requirement**.
3. Strong, citable real-world case that explainability + accountability are now **public-policy expectations**, not optional — useful framing for A2/A3 discussion sections.
