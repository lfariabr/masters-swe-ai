# Module 10 — Learning Theory: PAC

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Pedregosa et al. (2015) — scikit-learn `1.4 Support Vector Machines` (context for PAC) | ✅ |
| **2** | Read & summarise Daumé III (2017) — *A Course in ML*, Ch.12 Learning Theory | ✅ |
| **3** | Read & summarise Brownlee (2019) — What is a hypothesis in machine learning? | ✅ |
| **4** | Read & summarise Kelly (2020) — PAC learning theory for the everyman | ✅ |
| **5** | Read & summarise Pavlus (2016) — The hunt for the algorithms that drive life on earth (Wired/Quanta) | ✅ |
| **6** | Read & summarise Sarkar (2018) — Reaching for the gut of ML: a brief intro to CLT | ✅ |
| **7** | Watch & summarise Worrell (2019) — Computational Learning Theory I (transcript on file) | ✅ |
| 8 | Activity 1: On-device ML + Federated Learning (Dhar et al. 2020; McMahan & Ramage 2017) — forum | 🔥 |

> **One-line frame:** PAC (**Probably Approximately Correct**) is the *theory* that says why machine
> learning works at all. Perfect learning is **impossible** (noise + finite sampling), so the best you can
> hope is to be **approximately correct** (error ≤ **ε**) **probably** (with confidence ≥ **1 − δ**). The theory
> then bounds **how many training examples** you need (sample complexity) in terms of the **size/complexity
> of your hypothesis space** (|H|, or the **VC dimension** when |H| is infinite). Its punchline for practice:
> **simple hypotheses generalise** (Occam's Razor) — which is exactly why you regularise, split train/test,
> and prefer the smaller model.

> ⚠️ **This is a theory module (Week 10), and it is graded differently.** In the README, Module 10 addresses
> SLOs `a)` + `d)` only (*evaluate/compare concepts* + *communicate*), **not** `b)`/`c)` (implement).
> There is **no coding assessment tied to it** — Assessment 3 is a regression project. The value here is
> conceptual vocabulary (ε, δ, hypothesis space, sample complexity, VC dimension, Occam) and being able to
> *justify* the ML steps you already perform.

> 🎥 **Week 10 live session** (lecture-only material — ε/4 four-strip derivation, the ~1,753-sample worked
> example, CRISP-DM success-criteria framing, and the Module 11 preview): see
> [module10_notes-class.md](module10_notes-class.md).

---

## Key Highlights

### 1. Pedregosa et al. (2015). scikit-learn — `1.4 Support Vector Machines`.

**Citation:** Pedregosa, F., et al. (2015). Scikit-learn: Machine learning in Python. *JMLR, 12*, 2825–2830. [`1.4 Support Vector Machines`]

**Purpose:** Odd one out — this is the SVM API doc, not a PAC text. The module includes it because SVMs are the
cleanest real example of the theory's core lever: **the margin**. A big margin = a *simpler* effective
hypothesis = better generalisation, which is PAC/Occam made concrete. It's also a reminder of the ML *steps*
(fit/predict, kernels, regularisation) that PAC theory justifies.

---

#### 1. What SVM is
- **Supervised** method for **classification, regression, and outlier detection**. Finds the **maximum-margin
  separating hyperplane** — the boundary with the widest gap to the nearest points.
- **Support vectors** = the subset of training points that sit on the margin and *define* the boundary. The
  decision function depends only on them → **memory efficient** (`support_vectors_`, `support_`, `n_support_`).

#### 2. Why it belongs in a theory module
- **Effective in high dimensions**, even when `n_features > n_samples` — the theory-relevant property.
- **The margin is a complexity control.** A wider margin restricts the effective hypothesis space, so the
  learned classifier is "simpler" in the Occam sense → generalises better. This is the practical face of
  Module 10's abstract "complexity ↔ generalisation" relationship (Daumé §12.5, §12.7).
- **Kernels** (`linear`, `rbf`, `poly`, `sigmoid`) let a linear-in-feature-space boundary become non-linear in
  input space — expanding the hypothesis space when you need a **richer** (not just bigger) one (Sarkar's point).
- ⚠️ SVMs **don't give probabilities directly** (an expensive 5-fold CV approximates them); regularisation `C`
  matters most when `n_features ≫ n_samples` (overfitting risk).

#### Key Takeaways for MLN601
1. The **margin = regularisation = complexity control** is the bridge from this doc to the whole module: it's
   *why* a maximum-margin classifier is a good PAC learner.
2. Connects backward to **Module 6 (SVM)** and **Module 8 (`C` = 1/λ regularisation)** — same idea, now with a
   theoretical justification.
3. **Vapnik** (SVM's inventor) also gives us **VC dimension** (below) — the two are the same lineage.

---

### 2. Daumé III, H. (2017). Learning Theory (Ch.12, *A Course in Machine Learning*).

**Citation:** Daumé III, H. (2017, January). Chapter 12: Learning Theory. In *A Course in Machine Learning* (pp. 154–163).

**Purpose:** The mathematical spine of the module. Builds PAC from first principles: proves learning is
impossible in general, defines (ε, δ)-PAC, proves Occam's Bound (simple ⇒ generalises), and extends to
infinite hypothesis spaces via VC dimension. **This is the resource to actually study.**

---

#### 1. Induction is impossible (the setup)
- Dream: an ultimate algorithm `A_awesome` that, from any dataset `D`, returns `f` with **perfect** accuracy on
  all future data from the same distribution. **Provably impossible**, for two reasons:
  - **Label noise:** if 20% of a distribution has `x ≠ y`, no function beats 20% error.
  - **Finite sampling:** you only see samples; a *bad draw* (4 coin flips, no tails) can mislead any learner.
- So drop two hopes: perfect accuracy → settle for **approximately** correct; works every time → settle for
  **probably**. *"The best we can reasonably hope is that it does pretty well, most of the time."*

#### 2. (ε, δ)-PAC — the formal definition
| Symbol | Role | "Previous example" value |
|---|---|---|
| **ε** (epsilon) | **accuracy** — max acceptable test error (a "bad" function errs > ε) | 0.05 |
| **δ** (delta) | **failure prob.** — chance of returning a bad function | 0.1 |

- **Definition:** algorithm `A` is **(ε, δ)-PAC** if, for *all* distributions `D`, the probability it returns a
  "bad function" (test error > ε) is **at most δ**.
- **Two efficiencies:** **computational complexity** (CPU cycles) and **sample complexity** (number of labelled
  examples). An **efficient** PAC learner runs in time **polynomial in 1/ε and 1/δ** (tightening error 5%→4%
  must not cost an exponential blow-up).

#### 3. Occam's Razor: simple solutions generalise ⭐
- **Hypothesis class H** = the set of candidate functions the algorithm searches (all boolean formulas; all
  linear classifiers; …).
- **Occam's Bound (Theorem 15):** if `A` learns an `f` from a **finite** H that gets **zero training error**,
  the **sample complexity is at most ~log |H|**. → **Fewer/simpler hypotheses ⇒ fewer examples needed ⇒ better
  generalisation.** This is the theorem behind "if 5 features explain it, don't use 10,000."
- Captures **decision trees** too (finite H in the no-noise case).

#### 4. Infinite hypothesis spaces → VC dimension
- Occam's Bound is **useless when |H| = ∞** (you can't "throw out" your way down from infinity).
- **VC (Vapnik–Chervonenkis) dimension** = complexity measured as *"the max number of points the class can
  **shatter**"* — i.e., classify correctly **under every possible labelling**.
- **The shattering game:** you pick K points → adversary labels them any way → you must fit them with some
  `f ∈ H`. VC dim = the largest K you can **always** win. (Linear classifiers in 2-D: VC = 3 — you can shatter
  any 3 non-collinear points, but not all labellings of 4.)
- "≥ some value" is easy (show one example set); "≤ some value" is hard (rule out *all* larger sets).

#### Key Takeaways for MLN601
1. **ε = accuracy, δ = confidence.** Memorise which is which — the single most testable fact in the module.
2. **Occam's Bound ≈ "simple generalises"** is the theoretical licence for **regularisation** and feature
   selection you already do (Modules 8–9, PCA in Module 9).
3. **VC dimension** is how theory handles infinite H (e.g. linear/SVM classifiers) — and it's **Vapnik again**,
   tying straight back to Resource 1.

---

### 3. Brownlee, J. (2019). What is a Hypothesis in Machine Learning?

**Citation:** Brownlee, J. (2019, 25 June). *What is a hypothesis in machine learning?* [Web log post]. Machine Learning Mastery.

**Purpose:** Disambiguates the word **"hypothesis"** — which PAC theory uses constantly and which collides with
its statistics/science meanings. Fixes the vocabulary so the rest of the module reads cleanly.

---

#### 1. Three meanings of "hypothesis"
| Field | Meaning |
|---|---|
| **Science** | a provisional, **falsifiable** explanation that fits evidence and predicts new observations |
| **Statistics** | a **probabilistic** claim about a relationship between populations (null `H0` = no effect vs alternative `H1`) |
| **Machine Learning** | a **candidate model** that approximates a target function mapping inputs → outputs |

#### 2. The ML framing (the one that matters here)
- Supervised learning = **function approximation**: approximate an unknown **target function** that maps inputs
  to outputs on all possible observations.
- **Notation (used all over PAC):** **`h`** = a single hypothesis (one candidate model); **`H`** = the
  **hypothesis space/set** being searched. Learning = **searching H for a good `h`**.
- **Realizable** learning problem = H **contains** the true function. You often can't tell if a problem is
  realizable, because the true function is unknown.
- **Expressiveness ↔ tractability trade-off:** a bigger/ richer H is more likely to contain a good `h`, but is
  harder (slower) to search. So you deliberately **constrain** H.

#### Key Takeaways for MLN601
1. **`h` vs `H`** is the exact notation Daumé and Worrell use — learn it before reading them.
2. **"Model" (ML practice) ≈ "hypothesis" (PAC theory)** — same object, different dialect.
3. The **expressiveness↔tractability** trade-off *is* the practical reason VC dimension / Occam matter.

---

### 4. Kelly, A. (2020). PAC Learning Theory for the Everyman.

**Citation:** Kelly, A. (2020, 21 April). *PAC learning theory for the everyman: An uncomplicated introduction to the theory behind supervised machine learning*. The Startup (Medium).

**Purpose:** The gentle on-ramp. Explains PAC by analogy to how children learn categories, and states the one
formula in plain English. Read this **first**, then Daumé.

---

#### 1. The intuition (Valiant's children analogy)
- Valiant (1984): PAC formalises learning the way **children learn cats vs dogs** — after a few examples they
  **generalise** to new ones, and different children converge on similar notions with high agreement.
- **Perfect prediction is unattainable** (the green-California-orange vs green-apple example) → predictions are
  **approximately** correct.
- **More data ⇒ more trust:** a larger sample **narrows the confidence interval** around the truth, but you can
  **never be 100% confident** (a novel instance may never have appeared in training) → **probably** correct.

#### 2. The formula, in plain English
- `f(x) = y` is the true function; the learner returns `h(x)` as close to `f` as it can.
- **Success** = the error between `f` and `h` falls within an acceptable bound; inputs `x` occur with
  probabilities under a distribution **D** (total = 1).
- Plain-English statement: *the error rate is the probability, over `x ~ D`, that `h(x) ≠ f(x)`* — and PAC asks
  that this probability be small (≤ ε) with high confidence (≥ 1 − δ).

#### Key Takeaways for MLN601
1. **"Probably" = the δ/confidence part; "Approximately" = the ε/error part.** This article is where that
   clicks.
2. **Sample size ↔ confidence interval** is the statistician's view of **sample complexity**.
3. Lowest-maths entry point — use it to prime before the Daumé proofs and the Worrell video.

---

### 5. Pavlus, J. (2016). The Hunt for the Algorithms That Drive Life on Earth.

**Citation:** Pavlus, J. (2016, 7 February). *The hunt for the algorithms that drive life on earth*. Wired (reprinted from Quanta Magazine). [Interview with Leslie Valiant]

**Purpose:** The *why it matters* / big-picture resource. A Valiant interview on where PAC came from and his
grander claim: PAC describes not just machine learning but **biological evolution** — via the **"ecorithm."**

---

#### 1. Who and why
- **Leslie Valiant** (Harvard) invented PAC in **1984** and won the **2010 Turing Award** ("Nobel of computing")
  for it; it **spawned computational learning theory**.
- His motivation: make **one aspect of AI quantitative**, and he picked **learning**. Learning is
  "**statistical but also computational**" — statistics alone couldn't explain it, so PAC fuses both.

#### 2. Algorithm → "ecorithm"
- **Ecorithm** = a learning algorithm whose performance is judged against input from an **uncontrolled,
  unpredictable world** — it can run on a computer **or a biological organism/species**.
- Valiant's provocation: *"machine learning" is redundant* — a toddler with a ball and a deep net classifying
  cats are both learning; the "machine" label is a distinction without a difference.
- **Evolution as PAC learning:** protein-expression networks modified under Darwinian constraints are, he
  argues, a PAC-style learning process — a possible "theory of everything" fusing life science and CS.

#### Key Takeaways for MLN601
1. **PAC is theory-of-learning, not theory-of-*machine*-learning** — the module intro's exact point ("does not
   distinguish ML from non-ML/humans").
2. Know the **ecorithm vs algorithm** distinction (the module explicitly asks you to watch the embedded video
   for it) — an ecorithm is judged by an **unpredictable external world**.
3. **Valiant, 1984, Turing Award** — the three facts to remember about PAC's origin.

---

### 6. Sarkar, T. (2018). Reaching for the Gut of Machine Learning: A Brief Intro to CLT.

**Citation:** Sarkar, T. (2018, 15 July). *Reaching for the gut of machine learning: A brief intro to CLT*. Towards Data Science.

**Purpose:** Positions PAC inside the wider **Computational Learning Theory (CLT)**, defines the working
vocabulary (target concept, hypothesis space, predictor/response), and introduces the **Haussler bound** — the
concrete sample-complexity inequality.

---

#### 1. What CLT asks
- CLT reasons about **classes** of learners (via their hypothesis spaces), not individual algorithms. Core
  questions: *which problems are inherently hard/easy? how many examples suffice? how many mistakes before
  success?* — General answers are **still unknown**; PAC handles the common **inductive** setting.

#### 2. Vocabulary (memorise)
| Term | Meaning |
|---|---|
| **Data** | the examples you learn from |
| **Target concept `c`** | the hidden true rule (often propositional logic: `(X1 ∧ X2) ∨ (X3 ∧ X4)`) |
| **Hypothesis space `H`** | the set of candidate rules you search |
| **Predictor / response** | features vs the thing predicted |

#### 3. The "richness" trap ⭐
- **Bigger H ≠ better.** A linear regression has an **infinite** hypothesis space (all straight lines) yet
  **still can't** capture a quadratic truth — the true concept lives in a "**bigger infinity**."
- Moral: you often need a **richer** space (add a 2nd-degree term), **not merely a bigger** one. *"Like Thanos,
  we must search which infinity-sized space is best for the data."*

#### 4. The three quantities + the Haussler bound
- **Sample complexity** (how many examples to converge), **computational complexity** (how much compute),
  **mistake bound** (how many errors before success).
- **Haussler bound** — the sample-complexity inequality. It formalises three practical truths:
  1. **more training data ⇒ lower generalisation error**;
  2. **more data ⇒ higher confidence** (lower failure prob.);
  3. **richer/bigger H ⇒ needs more data** to search.
- Note: these bounds are often criticised as **too pessimistic** vs real practice. **VC dimension** keeps sample
  complexity **finite even for infinite H** (e.g. linear/kernel machines).

#### Key Takeaways for MLN601
1. **Richer, not just bigger** hypothesis space — the sharpest single insight in the module (explains why adding
   the *right* feature beats piling on parameters).
2. The **Haussler bound** ties the three abstractions (data ↑, confidence ↑, complexity ↑) into one inequality —
   the same story as Daumé's Occam's Bound.
3. **VC dimension** recurs here as the fix for infinite H → the natural bridge to Worrell (Resource 7).

---

### 7. Worrell, J. (2019). Computational Learning Theory I.

**Citation:** Worrell, J. (2019, 22 July). *James Worrell: Computational learning theory I* [Video]. (Transcript on file: `r7_Computational-Learning-Theory-transcript_Worrell-2019.md`.)

**Purpose:** The rigorous lecture — formalises the PAC model and presents **VC dimension as the
characterization of PAC learnability**, from a logic/verification angle. Watch the **first ~30 min** (the module's
instruction).

---

#### 1. The PAC model, formally
- A PAC problem is specified by an **input space X**, a **concept class C** (a class of functions X → {0,1}),
  and an unknown **distribution** on X.
- **PAC-learnable:** C is PAC-learnable with **sample complexity M**, **accuracy ε**, **confidence δ** if there
  is a learner that, from M samples, returns a hypothesis with **error ≤ ε** with probability **≥ 1 − δ**.
- **Distribution-independent:** crucially, the sample complexity depends **only on ε and δ** (and the class),
  **not on the underlying distribution** — this is what the module intro means by "the learner is independent of
  the data distribution."

#### 2. Realizable setting & VC dimension
- He works in the **realizable setting** (the true concept **is** in C, no noise) — the same simplifying
  assumption as Daumé.
- **Headline result:** **VC dimension is *equivalent to* PAC learnability** — a concept class is PAC-learnable
  **iff** it has **finite VC dimension**. VC dimension is *the* characterization, not just one bound among many.
- Comes at it from **logic & verification** (his field), emphasising connections between learning and formal
  reasoning.

#### Key Takeaways for MLN601
1. **Finite VC dimension ⇔ PAC-learnable** — the deepest single theorem in the module; know it as a slogan.
2. **Sample complexity depends on ε, δ (not the distribution)** — this is the formal justification for why
   train/test splitting and hyperparameter tuning are *distribution-agnostic* disciplines.
3. Reinforces Daumé's VC material from a proof-oriented angle — watch **the first 30 minutes**, don't drown in
   the rest.

---

## Synthesis — how the seven fit together

```
     WHY IT MATTERS            THE FORMALISM                  THE PRACTICAL PUNCHLINE
  PAC = theory of learning   perfect learning impossible    simple hypotheses generalise
    (Valiant, ecorithm)         (noise + sampling)             = Occam's Bound (Daume)
        (Pavlus R5)                 (Daume R2)                        (Daume R2)

  learning = search of H     (epsilon, delta)-PAC:          more data -> lower error +
    h vs H, realizable          eps=accuracy,                 higher confidence
      (Brownlee R3)             delta=confidence               = Haussler bound (Sarkar R6)
                              (Daume R2 / Kelly R4)

  richer != bigger H         infinite H -> VC dimension     finite VC <=> PAC-learnable
    (Sarkar R6)                 (shatter K points)             (Worrell R7)
                              (Daume R2 / Worrell R7)        margin = complexity control
                                                              => SVM is a good learner (R1)
```

**The through-line:** Module 10 is the **"why does any of this work?"** module. It has **no implementation
assessment** — it feeds SLOs `a)` (evaluate/compare concepts) and `d)` (communicate to stakeholders). Its payoff
is a vocabulary — **ε, δ, hypothesis space, sample complexity, VC dimension, Occam's Razor** — that lets you
*justify* the habits from Modules 1–9 (train/test split, regularisation, feature selection, preferring simpler
models). Activity 1 (on-device / federated learning) applies that lens to edge ML: *why* is PAC relevant when
compute and data are scarce, and what are its limits?

---

## Learning Activity 1 — On-Device ML & Federated Learning (forum draft)

> **Refs:** Dhar et al. (2020), *On-device ML: an algorithms and learning theory perspective* (arXiv:1911.00623,
> §4.2) · McMahan & Ramage (2017), *Federated learning* (Google AI Blog). **Status: 🔥 draft.**

**1. Why is PAC relevant to edge ML?** PAC connects two things: how big/complex your model is allowed to be, and
how many examples you need to train it well. A phone or sensor has very little memory and very little data, so you
are forced to use a **small, simple model**. The nice news from PAC (Occam's Razor) is that simpler models need
*less* data to work - which suits the edge perfectly. The catch is you can go too simple: shrink the model too
far and it just can't learn the pattern well enough. PAC is basically the theory that helps you find that
sweet spot.

**2. What limits does PAC have that hold edge ML back?**
- Its rules are **too cautious** - the theory asks for far more training data than devices actually get away with
  in practice.
- It assumes the data you *train* on looks like the data you *test* on. On real devices that is not true - every
  phone sees a different, personal, changing slice of the world.
- It only counts **data and compute**. It says nothing about the things that actually break an edge device:
  battery life, memory, and speed. A model can look "cheap" on paper and still be too big to fit.

**3. What theory ideas are the authors discussing (Dhar et al. §4.2)?** In plain terms: making a model smaller
changes how much data it needs and how accurate it can get; there is always a gap between how well a model does on
its training data vs new data; and the data on different devices doesn't match, which is the hard part.

**4. How could we actually make on-device ML work?** Train a big model in the cloud, then teach a small one to
copy it (distillation); trim and compress the model until it fits in memory; start from a pre-trained model and
only fine-tune a little (same trick as Dr Kamran's Module 9 paper); or use **Federated Learning** - keep the raw
data on the device and only send back the model's *updates*, so everyone's device helps train a shared model
without their private data ever leaving.

**5. Use cases (from my day job at St Catherine's).** An early-warning tool that spots at-risk students from
attendance/grades *without* ever sending a student's data to the cloud; a phone keyboard that learns your typing
locally (Google's own example); offline sensors that have to work with no internet and a small battery; and a
**campus-wide federated model** where every device improves a shared model but the raw student data never moves -
privacy built into the design, not just the policy.

> **Forum hook:** the irony is that PAC *likes* the small, simple models edge devices force on us (they need less
> data) - but it also assumes the data never changes, which is exactly what breaks on real devices. Federated
> Learning is the workaround.
