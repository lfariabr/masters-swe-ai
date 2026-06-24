# Module 5 - Classification and Bayes Rule

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Westbury (2010) - Bayes' rule for clinicians (base-rate fallacy) | ✅ |
| **2** | Read & summarise Zornoza (2019) - How Bayes' theorem is applied in ML | ✅ |
| **3** | Watch & summarise Andrew Ng - Naive Bayes & generative learning | ✅ |
| **4** | Read & summarise Nelson (2020) - What is Bayes theorem (Naive Bayes variants) | ✅ |
| **5** | Read & summarise Neiswanger (2019) - Modern Bayesian learning & probabilistic programming | ✅ |
| 6 | Listen & summarise Williams (2018) - PyMC3 / probabilistic programming podcast | 🔥 needs manual listen |
| 7 | Watch & summarise SAROPS - Bayesian search & rescue | 🔥 needs manual access |
| 8 | Activity 1: The German Tank Problem (notebook + article) | 🕐 |
| 9 | Activity 2: Naive Bayes classification + Titanic dataset | 🕐 |

> Step-by-step guidance for the two activities: see [module05_activities-draft.md](module05_activities-draft.md)

---

## Key Highlights

### 1. Bayes Rule for Clinicians (Westbury 2010)

**Citation:** Westbury, C. F. (2010). *Bayes' rule for clinicians: an introduction.* Frontiers in Psychology, 1:192.
**Local source:** `r1_Bayes-Rule-for-Clinicians_Westbury-2010.pdf`

**Purpose:** The clearest possible intro to Bayes' rule - and the **base-rate fallacy** that fools even trained doctors. This is the conceptual bedrock for classification.

---

#### 1. Conditional probability = "limiting the domain"
- The vertical slash `|` reads as **"given"**. `P(A | B)` = "probability of A, ignoring every case where B is false".
- Every probability is secretly conditional (a coin toss assumes "given a fair coin").
- **Picnic example:** 3 tall + 2 short men, 4 tall + 4 short women. `P(Tall | Female) = 4/8 = 0.5` - just ignore the men.

#### 2. Bayes' rule itself
```
P(A | B) = P(B | A) · P(A) / P(B)
```
| Term | Name |
|---|---|
| `P(A)` | **prior** (marginal) - belief before evidence |
| `P(B \| A)` | **likelihood** of the evidence given the hypothesis |
| `P(A \| B)` | **posterior** - updated belief after evidence |
| `P(B)` | marginal probability of the evidence |

- **Why it works:** we often know `P(symptom \| disease)` from confirmed past cases even when `P(disease \| symptom)` is unknown. Bayes flips one into the other.

#### 3. The base-rate fallacy (THE lesson)
- **Disease example:** base rate **1/1000**, false-positive **5%**, false-negative **0%**. A **positive** test means only a **2%** chance you actually have the disease.
- Why: of 10,000 people, ~10 true positives but ~500 false positives -> `10/510 ≈ 2%`. The rare disease's true positives are **swamped** by false positives.
- Posed to Harvard medical students, ~half answered **95%**; only 16% got it right.
- **Maladjusted-soldiers example:** test catches 55% of maladjusted, flags 19% of healthy -> with a 5% base rate, a positive diagnosis is right only **13%** of the time.

#### 4. Meehl's heuristic
A diagnostic test is "useful" (more right than wrong) only when:
`positive base rate / negative base rate > false-positive rate / true-positive rate`.

#### Key Takeaways for MLN601
1. This is the intuition behind **classification on imbalanced classes** - exactly your A1 `quality` problem (mostly 5-6) and the Module 4 warning that trees bias to the majority.
2. **Medical diagnosis** is the canonical Bayes classification story (COVID tests, tumour screening).
3. `prior × likelihood -> posterior` is the engine inside the **Naive Bayes classifier** (Resources 3, 4).

---

### 2. How Bayes Theorem is Applied in ML (Zornoza 2019)

**Citation:** Zornoza, J. (2019). *Probability Learning II: How Bayes' theorem is applied in machine learning.* Towards Data Science.
**Local source:** `r2_How-Bayes-Theorem-is-Applied-in-ML_Zornoza-2019.pdf`

**Purpose:** Shows how Bayes turns single-point parameter estimates into **distributions**, for both regression and classification.

---

#### 1. Bayes in regression
- A normal linear model learns **one** value per parameter (θ) via gradient descent or **MLE**.
- The Bayesian view treats each θ as a **distribution**: start with a **prior** `P(model)`, observe data, update to the **posterior** `P(model \| data)`; repeat (posterior becomes next prior). The variance shrinks as data grows.
- Pick the **MAP** (maximum a posteriori) value for prediction.

#### 2. Bayes in classification - the Bayes optimal classifier
- Want the posterior class probability `P(wᵢ \| x) ∝ P(x \| wᵢ) · P(wᵢ)`.
- **Height example:** classify 172 cm as male/female from 25 males + 9 females. Priors `P(male)=25/34`, `P(female)=9/34` shift the decision boundary vs a plain MLE classifier.

#### 3. MAP vs MLE
| | **MLE** (Maximum Likelihood) | **MAP** (Maximum A Posteriori) |
|---|---|---|
| Uses prior? | ❌ no | ✅ yes |
| Best when | lots of clean data, no prior info | few / unreliable data + good prior |
| Result | data speaks for itself | prior makes estimates **robust** |

#### Key Takeaways for MLN601
1. Connects **Module 3** (linear-regression parameters) to Bayesian thinking - same θ, but now a distribution.
2. **MAP vs MLE** is a classic exam distinction: MAP = MLE + prior.
3. Leads directly into the **Naive Bayes** simplification (next resources).

---

### 3. Naive Bayes and Generative Learning (Andrew Ng)

**Citation:** Ng, A. (Zhiyang, W., 2015). *Naive Bayes / generative learning algorithms* [Video, Stanford CS229].
**Local source:** `r3_Naive-Bayes-and-Generative-Learning_Andrew-Ng.txt` (transcript)

**Purpose:** The key distinction between **discriminative** and **generative** classifiers, and where Naive Bayes / GDA sit.

---

#### 1. Discriminative vs Generative
| | **Discriminative** | **Generative** |
|---|---|---|
| Learns | `P(y \| x)` directly | `P(x \| y)` and `P(y)`, then **Bayes rule** -> `P(y \| x)` |
| Examples | logistic / linear regression | **Naive Bayes**, **GDA** |
| Idea | draw the boundary between classes | model what each class "looks like", then compare |

#### 2. Gaussian Discriminant Analysis (GDA)
- Model each class as a **Gaussian** (mean vector + covariance). Classify a new point by which class's bell-curve makes it more likely (× prior).
- Often **simpler and more data-efficient** than logistic regression on **small** datasets, but makes stronger assumptions.

#### 3. Naive Bayes (the spam example)
- Models `P(features \| class)` with a **naive** assumption: features are **conditionally independent given the class**.
- **Spam classifier:** represent an email as which words appear; estimate `P(word \| spam)` and `P(word \| ham)`; multiply and apply Bayes rule.
- **Laplace smoothing:** add 1 to every count so a never-before-seen word doesn't force the probability to **zero**.

#### 4. The trade-off
- **Generative** (Naive Bayes/GDA): fewer data needed, strong assumptions, fast.
- **Discriminative** (logistic): usually wins with **lots** of data because it makes fewer assumptions. (No Free Lunch again.)

#### Key Takeaways for MLN601
1. **Naive Bayes is the Module 5 classifier** you implement in **Activity 2**.
2. **Generative vs discriminative** is a top-tier exam concept - know that Naive Bayes is generative and uses Bayes rule under the hood.
3. **Spam filtering** is the textbook application; Laplace smoothing is the practical "gotcha".

---

### 4. What is Bayes Theorem (Nelson 2020)

**Citation:** Nelson, D. (2020). *What is Bayes Theorem?* Unite.AI.
**Local source:** `r4_What-is-Bayes-Theorem_Nelson-2020.txt`

**Purpose:** A concise bridge from the formula to the **Naive Bayes classifier** and its scikit-learn variants.

---

#### 1. Why "naive"?
Naive Bayes assumes every feature (B1, B2, B3...) is **independent of the others given the class**. That is almost never literally true, but the simplification makes the maths tractable - and it **still performs well**.

#### 2. The three sklearn variants
| Variant | Feature type | Typical use |
|---|---|---|
| **Gaussian NB** | continuous (assumed normal) | numeric features (e.g. Titanic **fare**) |
| **Multinomial NB** | counts / frequencies | **document** classification (word counts) |
| **Bernoulli NB** | binary (present / absent) | text with yes/no word features |

#### 3. Pros / cons
- ✅ Fast, simple, works on small data, good baseline, handles multi-class.
- ⚠️ The independence assumption is unrealistic; probabilities themselves are poorly calibrated.
- **Applications:** spam, sentiment, text classification.

#### Key Takeaways for MLN601
1. **Activity 2 uses `GaussianNB`** on the Titanic `fare` (continuous) - this resource tells you *why* the Gaussian variant.
2. The variants map 1:1 to sklearn classes (`GaussianNB`, `MultinomialNB`, `BernoulliNB`).
3. Reinforces the "naive" independence assumption from Resource 3.

---

### 5. Modern Bayesian Learning and Probabilistic Programming (Neiswanger 2019)

**Citation:** Neiswanger, W. / Petuum (2019). *Intro to modern Bayesian learning and probabilistic programming.* Medium.
**Local source:** `r5_Modern-Bayesian-Learning-and-Probabilistic-Programming_Neiswanger-2019.pdf`

**Purpose:** What Bayesian ML and **probabilistic programming** are, and when they earn their keep.

---

#### 1. Standard ML vs Bayesian ML
- **Standard ML:** define a model -> pick data -> learn **one** set of parameters.
- **Bayesian ML:** define a **generative process** + **priors** over parameters -> observe data -> end with an updated **distribution** over parameters (not a single value).

#### 2. When Bayesian is worth it
- You have **prior knowledge** worth injecting.
- You have **few data** or **many parameters**.
- You need **uncertainty quantification** - "how sure is the model?" - not just one answer.

#### 3. "Has my milk gone bad?" (the worked intuition)
- Prior: 50/50 good vs bad. Likelihood: distributions of "smelliness" for good vs bad milk.
- Observe smell = 5/10 -> posterior updates to **33% good / 67% bad**. That is Bayesian inference in one sentence.

#### 4. Probabilistic Programming Languages (PPLs)
- **Stan, PyMC (PyMC3), Pyro, Edward, Infer.NET** - you *write down* the generative model + priors, hand it data, and it **auto-computes** the posterior (no hand-deriving inference).
- **Inference engines:** MCMC and variational inference. **Challenges:** cost on big data / big models, verifying correctness, usability.

#### Key Takeaways for MLN601
1. This is the **"probabilistic programming (Bayesian) with pymc3"** step in **Activity 1** (German Tank).
2. **Uncertainty quantification** is the Bayesian selling point - a posterior over N, not just a point estimate.
3. Connects to Resource 2: priors + posteriors, now made executable in code.

---

### 6. Probabilistic Programming and PyMC3 Podcast (Williams 2018)

**Citation:** Reisz, W. (Interviewer) (2018). *Mike Lee Williams on probabilistic programming, Bayesian inference, and languages like PyMC3* [Audio podcast]. InfoQ.

**Status:** 🔥 Audio only, no transcript supplied - **listen manually**.

**Primer (what to listen for):** probabilistic programming and **Bayesian inference** in practice; the headline benefit is **predictions that come with a measure of uncertainty**; applications include **clinical trials** and **streaming data**; Python/R tools (PyMC3) abstract away the deep maths so you can describe a problem in Bayesian terms. Pairs directly with Resource 5.

---

### 7. Search and Rescue with Bayes (SAROPS)

**Citation:** SAROPS (Search and Rescue Optimal Planning System), US Coast Guard / Metron.

**Status:** 🔥 Video/audio - **access manually**.

**Primer (the story):** SAROPS is a direct, life-saving use of Bayes' rule. Start with a **prior probability map** of where a person/object lost at sea might be; each **search or sighting (evidence)** updates the map into a **posterior**, concentrating effort on the highest-probability cells. Built by **Metron**, the approach (Bayesian search theory) helped locate the **USS Scorpion**, **SS Central America**, and the **Air France 447** black boxes. It is the same `prior -> evidence -> posterior` loop as the milk and disease examples, applied to a map.

---

## Synthesis - how Module 5 fits together

| Concept | One-line takeaway | Resource |
|---|---|---|
| Bayes' rule | `posterior ∝ likelihood × prior` | R1, R4 |
| Base-rate fallacy | rare-class positives are mostly false positives | R1 |
| MAP vs MLE | MAP = MLE + a prior | R2 |
| Generative vs discriminative | model `P(x\|y)` vs `P(y\|x)` directly | R3 |
| Naive Bayes | conditional-independence shortcut; Gaussian/Multinomial/Bernoulli | R3, R4 |
| Probabilistic programming | write the model, auto-infer the posterior (PyMC3) | R5, R6 |
| Real-world Bayes | search & rescue, spam, medical tests | R1, R3, R7 |
