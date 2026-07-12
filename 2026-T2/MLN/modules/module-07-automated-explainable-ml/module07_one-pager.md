# MLN601 · Module 7 - One-Pager

> **Automated ML (build the pipeline for me) · Explainable ML (justify the prediction) · Governance (institutions must explain)**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Two questions close the ML loop: "can the machine BUILD the pipeline?" (Auto ML) and "can it EXPLAIN the decision?" (XAI).**
> **Auto ML attacks the *how to build*; XAI attacks the *why to trust*. A model that is strong but unexplainable is only half-done.**
> (Olson 2018 · Aha/DARPA 2019 · Molnar Ch.4 · Sowden 2018)

## 🖤 Zone 1 - Auto ML: what it is (and is NOT)
- 🖤 **One line:** "automate the process of applying ML algorithms to data sets."
- 🔴 **Trap:** early-90s Auto ML = **hyperparameter tuning only** (grid/random search over one fixed model). Modern Auto ML tunes the **whole pipeline**: clean → features → model select → HPO. *Tuning alone ≠ Auto ML* (vendors mis-sell this).
- 🔵 **Modern search engines:** Bayesian optimisation (dominant HPO), genetic programming (**TPOT**), meta-learning, multi-armed bandits.
- 🔵 **Five automation domains** (awesome-autoML map): data cleaning · **AutoFE** (feature eng.) · **HPO** · **meta-learning** · **NAS** (neural architecture search).
- 🔵 **Tools:** TPOT (`TPOTClassifier`, same `.fit()/.score()`), Auto-sklearn, Auto-WEKA, H2O AutoML, DataRobot; HPO libs **Optuna / Hyperopt / SMAC3**.
- 🔴 **Three evidence bullets:** ~**5% avg accuracy lift** from tuning across ~160 datasets · **"no best algorithm"** (gladiator ring — even Naive Bayes wins ~1%) · **~60% of a DS's time is data cleaning**.
- 🔴 **Caveat (exam gold):** Auto ML is a **productivity tool, NOT a data-scientist replacement**, and it's **slow** (fire-and-check-back).

## 🖤 Zone 2 - Explainable ML: the taxonomy ⭐ SLO a) - THE GRADED DISTINCTION
- 🖤 **Central trade-off:** performance **vs** explainability. Deep learning bought accuracy at the cost of explainability; XAI wants the **top-right corner** (both). (Aha/DARPA)

| Axis | Left | Right |
|---|---|---|
| **How you get it** | **Intrinsic** = transparent by design (linear/logistic reg, **decision trees**, rules) | **Post-hoc / model-agnostic** = explain any black box after (SHAP, LIME, PDP, ALE) |
| **Scope** | **Global** = overall behaviour (permutation importance, PDP) | **Local** = one prediction (**SHAP**, LIME, counterfactuals) |

- 🖤 **The 2x2 map** (copy this square - it's the whole zone on one glance):

```
                 GLOBAL                    LOCAL
              (whole model)            (one prediction)
        +---------------------+---------------------+
INTRIN- |  tree feature       |  read the if/else   |
  SIC   |  importance;        |  path for THIS row  |
(built  |  logistic coeffs    |  (tree/rule)        |
 -in)   |                     |                     |
        +---------------------+---------------------+
POST-   |  permutation imp.,  |  * SHAP *  LIME,     |
  HOC   |  PDP, ALE           |  counterfactuals    |
(any    |  (shuffle & measure)|  <- Activity 3      |
 model) |                     |                     |
        +---------------------+---------------------+
   ^ pick a ROW by the model you have; a COLUMN by the question you ask.
```

- 🔵 **SHAP** = Shapley values (1953, cooperative game) split a prediction across features; local per-instance, aggregates to global → **Activity 3**.
- 🔵 **LIME** = fits a simple surrogate around one point (fast approximation). **Permutation importance** = shuffle a feature, measure the accuracy drop (global).
- 🔴 **The one-line exam distinction:** *feature importance = global; SHAP-on-one-passenger = local.*

## 🖤 Zone 3 - Why explainability matters + its danger
- 🔵 A raw prediction leaves the user unable to answer *why? when do I trust it? what next?* — XAI adds an **explanation interface** to interrogate.
- 🔵 **DARPA techniques to name-drop:** **RISE** (mask image regions → saliency heat map, any black box) · **Network Dissection** (label hidden-unit semantics) · finite-state/**Moore-machine** extraction from RNN agents · self-driving **video-to-text** justifications.
- 🔴 **Quotable risk line:** an **incorrect explanation is worse than none** — it actively damages trust. XAI must engender *appropriate* trust, not blind trust.

## 🖤 Zone 4 - Governance: explainability as public policy (Sowden / NZ)
- 🔵 **2018 NZ government-wide review** of how the **14 biggest data agencies** use algorithms in significant decisions, judged on **6 data-use principles** (with the Privacy Commissioner) → **Algorithm Assessment Report**.
- 🔵 **Three concrete responses:** **Algorithm Charter** (public transparency commitment agencies sign) · **Data Ethics Advisory Group** (external experts, public debate on *when* to use algorithms) · **workforce data-ethics uplift**.
- 🔴 Explainability is not just a technique - it's a **governance requirement**. Charters + ethics boards, not heat maps. Strong framing for A2/A3 discussion sections.

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 2 - Classification** · notebook + source + 7-10 min presentation + 1500 words (±10%) · **40%** · due **26/07/2026** · SLOs **b) c) d)**.
> Module 7 seeds A2 two ways: (1) the "no best algorithm" + 5% tuning lift arguments justify **comparing** Decision Tree / LogReg / Naive Bayes / SVM instead of defending one; (2) **SHAP on your Titanic classifier** (Activity 3, same dataset) is the interpret-your-results layer that lifts the discussion section. Module 7 itself is graded on SLOs **a) + d)** (evaluate/compare concepts + communicate clearly).

## 🔴 If you only memorise 5 things
1. **Auto ML = whole pipeline, not just tuning** - and it's a productivity tool, NOT a DS replacement.
2. **Intrinsic vs post-hoc** = transparent-by-design (tree/logistic) vs explain-a-black-box-after (SHAP/LIME).
3. **Global vs local** = overall behaviour (feature importance) vs one prediction (SHAP-on-one-instance). ← the exam line.
4. **A wrong explanation is worse than none** (Aha/DARPA) - the risk quote.
5. **Governance:** NZ Algorithm Charter + Data Ethics Advisory Group make explainability a **public-policy expectation** (Sowden).

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your warehouse/DB reporting: which columns are your "features," and if a manager asks *why this SKU was flagged*, is your current logic **intrinsic** (a readable SQL rule) or a **black box** that would need SHAP-style post-hoc explanation?
2. Where in your data work does ~60% go to **cleaning**? That's exactly the grunt work Auto ML claims to absorb - would a TPOT/Optuna pass actually save you time, or just hide judgement you need to keep?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🔥 Listen to the **Linear Digressions AutoML podcast** (Res. 2) and summarise - only resource still open.
- [ ] 🕐 Activity 1: **Google What-If Tool** - probe 2+ notebooks (wine, COMPAS, census, smile) - see global + local visually.
- [ ] 🕐 Activity 2: **IBM AI Explainability 360** - bank-loan scenario (CEM + Protodash) - the *local* + legal-obligation twist.
- [ ] 🕐 Activity 3: **SHAP + explainerdashboard** on the Titanic classifier - reuse your A2 dataset.
