# MLN601 · Module 2 — One-Pager

> **Managing ML Projects · CRISP-DM · CRISP-ML(Q) · Ethics by Design · Data Sets**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4.

**Pen legend:** 🖤 Black = core facts / skeleton · 🔵 Blue = examples & connections · 🔴 Red = traps, ethics & assessment hooks

---

## 🖤 The Big Idea (box it, top of page)
> **CRISP-DM = the de-facto standard *process* for running an ML project** — 6 phases, **iterative** (loop back any time). It organises the *how*, it is **not** an algorithm.
> 🔵 It **starts and ends at the business**, not the tech (Shearer 2017). General enough for retail, IoT, healthcare alike.

## 🖤 The 6 Phases (write as a spine down the left, with a loop arrow)
```
1  Business Understanding  → objectives + success criteria
2  Data Understanding      → collect · describe · verify quality
3  Data Preparation        → select · clean · features · missing values
4  Modeling                → pick technique · build · tune
5  Evaluation              → judge vs BUSINESS criteria (not just accuracy)
6  Deployment              → ship + monitor
    ↑________ backtrack to any earlier phase any time ________↓
```
🔴 *Memorise the 6 — your A1 report is literally these 6 headings.*

## 🖤 CRISP-DM → CRISP-ML(Q) (two columns)
| CRISP-DM (1999, classic) | CRISP-ML(Q) (Studer 2020, for ML) |
|---|---|
| 6 phases, built for data mining | **Merges** Business + Data Understanding |
| stops at Deployment | **+ 7th idea: Monitoring & Maintenance** |
| no quality method | **+ Quality Assurance per task** (catch risk early) |

🔵 Why the extra phase? **Models degrade** — data drifts, sensors age, a system update silently rescales an input. 🔴 *75–85% of ML projects miss expectations → process > cleverness.*

## 🖤 One Skeleton, 4 Lenses (blue connections)
- 🗺️ **Reference map** — Leaper (2009) single-page visual guide
- ✅ **Checklist** — Tyagi (2020): keep a live task list in your notebook
- 🔍 **Audit** — Clark (2018): bias-by-**sampling** (feed pseudo-data, inspect outputs)
- ⚖️ **Ethics** — Cunningham (2020): one ethical question per phase

## 🔴 Ethics by Design (Cunningham — one Q per phase)
- **Business** → what are the **externalities**?
- **Data underst.** → does my data hold **unethical bias**?
- **Data prep** → how do I **cleanse** the bias?
- **Modeling** → open to **outside influence**? 🔵 *MS Tay bot*
- **Eval / Deploy** → how do I **quantify** the harm? 🔵 *predictive policing → over-policing*

## 🖤 Success = 3 levels of criteria (CRISP-ML(Q))
**Business** ("failure rate < 3%") · **ML** ("accuracy > 97%") · **Economic / KPI** ("$ saved per check")
🔵 6 model quality measures beyond accuracy: **performance · robustness · scalability · explainability · complexity · resource demand.**

## 🔴 Pitfalls (red box — these are marks-losers)
- **Data leakage / "too good to be true"** 🔵 *vgsales R²=0.9999 because `Global = NA+EU+JP+Other` → predicting a sum from its own parts. Drop the leaky cols.*
- **Model drift** → monitor + retrain (don't ship-and-forget)
- **Technical debt / correction cascades** → don't stack rule-"fixes" on a broken model
- **"Accurate ≠ acceptable"** → a 90% model can still discriminate (zip-code bias)
- **No reproducibility** → fix seeds, report mean±variance (not the top run)

## 🔵 Module 2 in practice (your two activities)
- **A1 template** = `a1_template.ipynb` → red-wine quality (1,599 × 11 physicochemical features) → fill in the 6 stages.
- **Activity 2** = replicate Mishra (2019) vgsales notebook → *spot the leakage yourself*.

## 🔴 Assessment Hook (bottom red strip)
**A1 = Regression Analysis, due 28 Jun (20%).** Build the **whole report on the 6 CRISP-DM stages** using the template. Marks live in:
1. Clear **business framing** + success criteria  2. **Data quality** (missing values, outliers via IQR)  3. Honest **train/test** split  4. **Business-level** evaluation, not just charts  5. **Lessons learned** in Deployment.

---

### Margin prompts (answer in blue while you write)
1. Which CRISP-DM phase do you personally rush — and what breaks downstream because of it?
2. Pick one of your projects (Review Pulse / ClinicTrends): where could **leakage** sneak in between a feature and the label?
