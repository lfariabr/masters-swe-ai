# DLE602 · Module 4 - One-Pager

> **Regularization: how to make a model generalise to NEW data, not just memorise the training set**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape, 4 zones).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Regularization = any technique that makes a model generalise better (lower TEST error), bought by trading a little bias for a lot less variance. It is the cure for overfitting.**
> (Goodfellow Ch.7. The payoff of M1-M3: the nets don't just *work*, they work on data they've never seen.)

## 🖤 Zone 1 - Why regularize? The bias-variance trade ⭐
- 🔵 **Bias** = too simple, lazy assumptions → **underfits** (misses the real pattern). **Variance** = too sensitive → **overfits** (memorises noise, dies on new data).
- 🔵 **The trade:** spend a little bias to kill a lot of variance. A *good* regularizer makes a profitable trade.
- 🖤 **3 regimes:** (1) model excludes the truth = underfit/bias · (2) matches = sweet spot · (3) includes truth **+ noise** = overfit/variance. **Goal: drag the model from 3 → 2.**
- 🔴 **Tell-tale sign of overfitting:** train accuracy ≫ test accuracy. *(You saw it live: A1 trigram = 0.99 train vs 0.55 test.)*

## 🖤 Zone 2 - Parameter norm penalties: L1 vs L2 (§7.1)
- 🖤 Add a penalty to the loss: `J̃ = J + α·Ω(w)`. `α` = strength (0 = none). **Penalise weights `w`, not biases.**

| | **L2 (weight decay / ridge)** | **L1 (lasso)** |
|---|---|---|
| Penalty | `½‖w‖²` (squares) | `‖w‖₁` (absolutes) |
| Effect | shrinks weights toward 0 | drives weights to **exactly 0** |
| Gives you | smaller, smoother, noise-robust | **sparse** model → feature selection |
| Prior (MAP) | Gaussian | Laplace |

- 🔵 **§7.2:** a penalty ≈ a **constraint** (L2 ≈ keep the weight vector inside a ball). Same idea, two framings.

## 🖤 Zone 3 - The practical toolkit (Shubham + Goodfellow)
- 🔵 **Dropout** (§7.12): randomly switch off ~25% of units each step → trains an **ensemble of shared-weight sub-nets** = cheap bagging. Test time: weight-scaling rule.
- 🔵 **Early stopping** (§7.8): watch the **validation** error, stop when it turns upward. **The most-used regularizer**; a "free lunch".
- 🔵 **Data augmentation** (§7.4): cheap fake data (flip / rotate / scale). Best for **vision**; never flip the label (6↔9, b↔d).
- 🔵 **Bagging** (§7.11): average several models on bootstrap samples → variance down.
- 🔴 **Keras one-liners** (Shubham, Activity 1): `regularizers.l2(λ)` · `Dropout(0.25)` · `ImageDataGenerator(...)` · `EarlyStopping(patience=k)`. **Augmentation gave the biggest accuracy leap.**

## 🖤 Zone 4 - The map + unsupervised ⭐
- 🖤 **Kukačka's 5 levers** (where can you regularize? every method files under one):
  **① Data · ② Architecture · ③ Error function · ④ Regularization term · ⑤ Optimization.**
- 🔵 Broad working definition: *"any supplementary technique that makes the model generalise better."* (Augmentation, dropout, batch-norm are surprisingly close cousins.)
- 🔴 **Wang & Klabjan:** overfitting hits **unsupervised** nets too (RBM/DBN/DBM). Their **partial DropConnect (PDC)** keeps the *important* weights and drops the rest → most stable fix.

## 🔴 Activity Prep - the 3 Module 4 forum tasks
- **Act 1 Programming:** run Shubham's **MNIST + Keras** case study, log each regularizer's accuracy (augmentation wins).
- **Act 2 Analysis:** name a domain where **overfitting is actually desirable** (e.g. memorising a fixed lookup, security canaries, overfit-then-distill).
- **Act 3 "I Wish":** would regularization knowledge have improved your **A1**? *(Yes - and you have the numbers below.)*

## 🔴 Assessment Hook (bottom red strip)
> **Your A1 already regularizes - it's called smoothing.** add-k = the n-gram's regularizer (stops unseen bigrams getting probability 0 = overfitting the training counts). Your own sweep proved the trade: **n=1 underfits** (bias), **n=3 memorises training 0.99 but test collapses to 0.55** (variance), **n=2 bigram is the data-validated sweet spot (test 0.72)**, and **k=1 is near-optimal**. Activity 3 writes itself. The deep trio (dropout / early-stop / L2) is your **A3 Review Pulse v2** toolkit. *(A1 due 28/06/2026, 30%.)*

## 🔴 If you only memorise 5 things
1. **Regularization = trade a little bias for a lot less variance** → beat overfitting.
2. **Overfitting smell:** train acc ≫ test acc (your trigram: 0.99 vs 0.55).
3. **L2 shrinks** weights (ridge, Gaussian); **L1 zeros** them (lasso, Laplace, feature select).
4. **The practical big 3:** dropout (cheap bagging), early stopping (most-used), data augmentation (biggest leap in vision).
5. **5 levers (Kukačka):** data · architecture · error · reg-term · optimization. *Smoothing is your n-gram's lever.*

---

### Margin prompts (answer in blue while you write)
1. Why does the trigram memorise training yet fail on test? *(3-word combos almost never recur → sparsity → variance)*
2. Match the Keras line to the Goodfellow section: `Dropout`→§7.12 · `EarlyStopping`→§7.8 · `l2`→§7.1 · `ImageDataGenerator`→§7.4.

### This-week to-dos (still 🕐 in your notes)
- [ ] Activity 1 - run Shubham MNIST, log each regularizer's accuracy
- [ ] Activity 2 - find a "overfitting is good" domain + rationale
- [ ] Activity 3 - "I Wish" post using your A1 bias-variance numbers
- [ ] (optional) drop the bias-variance figure into your A1 report's limitations section
