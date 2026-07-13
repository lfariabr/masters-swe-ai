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

## 🔴 Assessment Hook (bottom red strip) - straight from the Week 7 lecture
> **Assessment 2 - Classification** · **40%** · due **26/07/2026** · SLOs **b) c) d)**. Same wine dataset as A1.
> **Target (his encoding, counter-intuitive):** `quality < 6` → **1 = bad** · `quality >= 6` → **0 = good**. **The positive class is the BAD wine** - read every recall/SHAP sign against that.
> **His four levers for a high mark:** (1) many models, each with a *rationale*, not just a score · (2) **SMOTE** if imbalanced - he ties this to *"distinction / high distinction"* · (3) **`GridSearchCV(cv=5)`** · (4) **XAI** - *"just copy paste that code and explain it"*.
> **Submission:** four files, **NO ZIP** - `.ipynb` · **PDF of that same notebook** · `.txt` (the `.py` code) · `.mp4`. Video **7-10 min**, Jupyter screen-share + **webcam + student ID card**, **NO PowerPoint**. *"Don't worry about the word count"* - the explanation lives in the notebook.

## 🔴 What the lecture actually spent 63 minutes on
> ⚠️ **The lecture never says "Auto ML" once.** Zone 1 is readings-only (still fair game for SLO a), but **XAI is the graded lever**. And he sets the bar low: *"what is SHAP, its theory - we don't need to go into detail. We are more into how it could be implemented."* Which is exactly why `activities/` is cheap points.

## 🔴 If you only memorise 5 things
1. **Auto ML = whole pipeline, not just tuning** - and it's a productivity tool, NOT a DS replacement.
2. **Intrinsic vs post-hoc** = transparent-by-design (tree/logistic) vs explain-a-black-box-after (SHAP/LIME).
3. **Global vs local** = overall behaviour (feature importance) vs one prediction (SHAP-on-one-instance). ← the exam line. *He walks straight into this: "alcohol has the maximum contribution" is a **global** claim; Activity 4 shows SHAP ranking alcohol **8th of 11** on one specific wine.*
4. **A wrong explanation is worse than none** (Aha/DARPA) - the risk quote. *Activity 4 turns it into a demonstrated result: Eli5's local signs are inverted, and rank correlation (ρ = +0.98) cannot see it.*
5. **Governance:** NZ Algorithm Charter + Data Ethics Advisory Group make explainability a **public-policy expectation** (Sowden).

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. Your warehouse/DB reporting: which columns are your "features," and if a manager asks *why this SKU was flagged*, is your current logic **intrinsic** (a readable SQL rule) or a **black box** that would need SHAP-style post-hoc explanation?
2. Where in your data work does ~60% go to **cleaning**? That's exactly the grunt work Auto ML claims to absorb - would a TPOT/Optuna pass actually save you time, or just hide judgement you need to keep?

### Module status: ✅ closed
All 6 resources reviewed, all 4 activities executed ([`activities/`](activities/)), both lectures transcribed
([`module07_notes-class.md`](module07_notes-class.md)). He only asked for **two** activities - you did four.

### Carry into Assessment 2 (due 26/07)
- [ ] Check the **label polarity**: A2 uses `quality < 6` → 1 (bad). The activity notebooks use `>= 7` → good. **Opposite.** Don't copy code across without flipping the reading.
- [ ] Add **SMOTE** + **`GridSearchCV(cv=5)`** to the A2 notebook - his two named grade levers.
- [ ] Add the **XAI section**: SHAP, plus a **sign check by intervention** (change the feature, re-predict, see which way it moves). That is the HD move - see [`activities/README.md`](activities/README.md).
- [ ] Record the video: **7-10 min**, notebook + webcam + **ID card**, **no slides**.
