# MLN601 · Module 10 - One-Pager

> **PAC Learning Theory · ε & δ · hypothesis space · Occam's Razor · VC dimension · the "why ML works" module**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **PAC = *Probably Approximately Correct*. Perfect learning is impossible (noise + finite sampling), so the best you can hope is: be *approximately* correct (error ≤ ε) *probably* (with confidence ≥ 1 − δ). It's the *theory of learning* - it explains WHY ML works and bounds HOW MUCH data it needs.**
> (Valiant 1984, Turing Award · Daumé Ch.12 · Worrell 2019)

⚠️ **Theory module: no code assessment.** Feeds **SLO a)** (evaluate/compare concepts) + **SLO d)** (communicate). The payoff is *vocabulary to justify* what you already do.

---

## 🖤 Zone 1 - Why perfect learning is impossible
- 🖤 **No `A_awesome`** that gets 100% on all future data. Two killers:
  - 🔵 **Label noise:** if 20% of a distribution has `x ≠ y`, no function beats 20% error.
  - 🔵 **Finite sampling:** you only see samples; a bad draw (4 coin flips, no tails) misleads any learner.
- 🖤 So drop two hopes → **approximately** correct (not perfect) + **probably** correct (not every time). *"Do pretty well, most of the time."*

## 🖤 Zone 2 - The two dials: ε and δ ⭐ SLO a) - THE GRADED CORE
| Symbol | Measures | Lives at |
|---|---|---|
| **ε** (epsilon) | **accuracy** - max acceptable *prediction* error | inside one model ("errs ≤ 5%") |
| **δ** (delta) | **confidence** - chance the *whole training* returns a bad model | one level up ("1 in 10 runs is junk") |

- 🔴 **The trap:** ε = per-prediction error; **δ = the luck of the training draw.** Train 10× → each good model errs ≤ ε (that's ε); δ=0.1 → ~1 run produces a lemon (that's δ). Don't conflate them.
- 🔵 **(ε, δ)-PAC:** for *all* distributions, P(returns a "bad function", error > ε) ≤ δ. **Efficient** = runtime polynomial in 1/ε and 1/δ (5%→4% mustn't cost an exponential blow-up).

## 🖤 Zone 3 - Hypothesis space + Occam's Razor ⭐
- 🔵 **`h` vs `H`** (Brownlee): `h` = one candidate model; **H** = the whole set searched. **Learning = search H for a good `h`.** "Model" (practice) ≈ "hypothesis" (theory).
- 🔴 **Occam's Bound (Daumé):** if a **simple** model from a **finite** H fits the training data, sample complexity ~ **log |H|**. → **Simple hypotheses generalise + need less data.** This is the theory behind regularisation + feature selection.
- 🔵 **Richer ≠ bigger H (Sarkar):** infinite straight lines still can't fit a quadratic - add the *right* term, don't pile on parameters.
- 🔵 **3 quantities:** sample complexity (how many examples) · computational complexity (how much compute) · mistake bound. Tied by the **Haussler bound**: more data → lower error + higher confidence; richer H → needs more data.

## 🖤 Zone 4 - Infinite H → VC dimension
- 🖤 Occam's Bound dies when **|H| = ∞**. Fix: measure complexity by **what the class can do**, not how many members it has.
- 🔵 **VC (Vapnik-Chervonenkis) dimension** = max points the class can **shatter** (fit under *every* labelling). The **shatter game:** you pick K points → adversary labels them → you must fit. VC = largest K you **always** win. *(2-D linear classifier: VC = 3.)*
- 🔴 **The deepest theorem (Worrell): finite VC ⇔ PAC-learnable.** And sample complexity depends only on **ε, δ (not the distribution)** - the formal reason train/test splitting is distribution-agnostic.

## 🖤 Zone 5 - Ecorithm + the security twist
- 🔵 **Ecorithm (Valiant/Pavlus):** an algorithm judged by an **unpredictable world** - runs on a computer *or* an organism. PAC is theory of *learning*, not *machine* learning ("machine" is redundant). He even frames **evolution as PAC**.
- 🔴 **Adversarial ML breaks PAC's core premise** (same fixed distribution for train + test). The attacker perturbs inputs at test time to cross the boundary → learning theory's premise becomes a security hole. *(Ties to Dr Kamran's 2022 adversarial-robustness paper.)*

---

## 🔴 Assessment Hook (bottom red strip)
> **No assessment implements PAC.** But every assessment is PAC *in disguise* → say so out loud for **SLO d)** marks:
> `train_test_split` (A1) = estimating ε on unseen data · **5-fold CV + GridSearchCV** (A2) = beating down δ · **`C=1/λ` regularisation** (A2) = Occam's Razor · **PCA / feature selection** (A2/A3) = shrinking |H| · **5+ models compared** (A2) = No-Free-Lunch searching hypothesis spaces · **overfit vs underfit** = the complexity↔generalisation curve PAC formalises.

## 🔴 If you only memorise 5 things
1. **PAC = Probably Approximately Correct.** Perfect is impossible (noise + sampling) → aim ε-close, δ-confident.
2. **ε = accuracy (per prediction); δ = confidence (luck of the training draw).** Don't mix them up.
3. **Occam's Bound: simple hypotheses generalise** (~log |H|) = the theory that licenses regularisation.
4. **Richer ≠ bigger H** - add the right feature, not more parameters.
5. **Finite VC ⇔ PAC-learnable** - how theory handles infinite H (lines, SVM). Margin = complexity control.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. When you split your school's data into train/test before a model, you're estimating **ε** on unseen rows. Why would reporting accuracy on the *training* set (skipping the split) be a lie PAC theory predicts?
2. If you fit a student-risk model on **5,000 rows** vs **50,000**, which PAC quantity shrinks - and does more data lower your **error (ε)** or your **chance of a fluke model (δ)**? (Answer: both, but say which is which.)

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 Activity 1: On-device ML (Dhar et al. 2020) + Federated Learning (McMahan & Ramage 2017) - forum: *why is PAC relevant to edge devices, and what are its limits?*
- [ ] 🔥 Knowledge check: state the (ε, δ) definition from memory, then explain `train_test_split` as PAC in one sentence (SLO d practice)
