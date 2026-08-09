# MLN601 · Module 11 - One-Pager

> **The perceptron · inputs·weights + bias → activation → output · the online update rule · linear separability & its limits · XOR → multilayer · step → smooth activation → deep learning**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **The perceptron (Rosenblatt, 1958) is the first *trainable* artificial neuron and the atom every deep net is built from: `inputs × weights + bias → weighted sum → activation → output`. It learns by nudging weights after each wrong example - and it only converges when the data is linearly separable.**
> (Rosenblatt 1958 original; Bhardwaj 2020 mechanics; Golden 2014 LM101-015 theory)

## 🖤 Zone 1 - The mechanism (draw this first)
- 🖤 **The pipeline (most testable diagram in the module):**
  ```
  x1..xn ──(× w1..wn)──▶ Σ wᵢxᵢ + b ──▶ activation ──▶ output
                                          (step)         (0/1 or ±1)
  ```
- 🔵 **Four parts** (Bhardwaj): ① inputs `x1…xn` ② weights + **bias** `w1…wn, b` ③ weighted sum `Σwᵢxᵢ` ④ activation.
- 🔵 **Bias = the threshold** the sum must clear; it shifts the boundary off the origin. Fold it in as `w₀` with `x₀ = 1` (Roach/Ritvikmath) → net input `z = w·x`.
- 🔵 **Classify:** `sign(w·x)` - `> 0` → class A, `≤ 0` → class B. Boundary `w·x = 0` is a line/plane/hyperplane.
- 🔴 **Example (Bhardwaj):** `wx=−0.5, wy=0.5, b=0` → boundary `−0.5x + 0.5y = 0` i.e. `y = x`; step labels each side.

## 🖤 Zone 2 - The learning rule ⭐ SLO a) - THE GRADED CORE
- 🖤 **Online update, per misclassified point** (know it cold):
  ```
  w ← w + η·(target − pred)·x        (Roach)
  ωᵢ ← ωᵢ + ν·D·xᵢ    D=+1 upper / −1 lower   (Ritvikmath)
  ```
- 🔵 **η / ν = learning rate** ∈ (0,1). High → fast but overshoots; low → slow, fewer mistakes.
- 🔵 **All weights update simultaneously**; loop over passes; a fix can briefly break a correct point → keep looping.
- 🔵 **Online (per-example)** ≠ **batch** gradient descent - say this out loud (Data Skeptic).
- 🔴 **Stopping criterion:** all correct **OR** cap `n_iter` / no gain for ~20 epochs (Forsyth). Iris demo → **converges at iteration 6, 0 errors**.

## 🖤 Zone 3 - Convergence & its limit (the caveat that gets marked)
- 🖤 **Perceptron Convergence / Learning Theorem** (Rosenblatt 1962): *if* a perfect separator exists, the rule **will** find it.
- 🔴 **Two fundamental limits** (Golden):
  1. **Assumes a solution exists** - on non-separable data there is **NO guarantee**; updates **cycle forever** (Forsyth: Iris versicolor/virginica → ~89%; JS dataset #8 → never settles). → **cap the epochs.**
  2. **Memorization, not generalization** - guarantees it fits the *training* data, says nothing about unseen inputs.
- 🔴 **Memorization vs generalization = the exam distinction.** Perceptron Theorem = memorization guarantee; **PAC (Module 10) = generalization guarantee.** This module is the foil to the last one.
- 🔵 **5 traits (revision checklist, Data Skeptic):** *online · step · linear-only · converges-if-separable · efficient.*

## 🖤 Zone 4 - XOR, the fix, and the road to deep learning
- 🖤 **XOR / poisonous-flowers (Golden):** one neuron faces an algebraically **inconsistent** system → **impossible**. Add **one hidden unit** → solvable. **Minsky-Papert (1969)** → first AI winter.
- 🖤 **Two advances that unlocked deep learning (Art of the Problem):**

  | Change | From → To | Why it mattered |
  |---|---|---|
  | **Activation** | step → **smooth** | proportional error → learn direction+magnitude → **backprop** across all weights |
  | **Hardware** (~2009) | CPU → **GPU** | parallel math → the "Big Bang" of deep learning |
- 🔵 **Activation functions (Lang)** - need **non-linearity** + **differentiability**:

  | Fn | Range | Use | Weakness |
  |---|---|---|---|
  | Sigmoid | 0→1 | binary prob | vanishing gradient |
  | Tanh | −1→1 | zero-centred | still saturates |
  | **ReLU** `max(0,x)` | 0→∞ | **hidden-layer default** | dying ReLU |
  | Softmax | 0→1 Σ=1 | multi-class out | overconfident |
- 🔵 **Rule of thumb:** hidden → ReLU/Leaky ReLU; output → sigmoid (binary) / softmax (multi-class) / linear (regression).

## 🖤 Zone 5 - The family (ties back to earlier modules)
- 🔵 Same **McCulloch-Pitts linear-neuron lineage**, *not* the same objective/guarantee:

  | Model | Twist | Fixes |
  |---|---|---|
  | **Perceptron** | hard step, ±1 | baseline; memorizes, needs separability |
  | **SVM** (Mod 6) | max-margin ±1 | soft margin tolerates errors → generalization |
  | **Logistic reg.** (Mod 8) | sigmoid → prob | probabilities, smoother boundary |
- 🔵 **Non-separable rescue:** map to polar / feature space (Ritvikmath) → foreshadows the **kernel trick** (SVM).

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Machine Learning Project** · notebook + model selection, up to **2000 words** · **40%** · due **19/08/2026** (🔥 9 days) · SLOs **a) b) c) d)** (Module 11 feeds **a, d**).
> This module hands you the vocabulary to **compare model families** (SLO a: perceptron vs SVM vs logistic) and **justify model choice + honest evaluation** in the write-up (SLO d). Convergence-only-if-separable and train/test discipline are exactly the caveats markers look for.

## 🔴 If you only memorise 5 things
1. **`inputs × weights + bias → activation → output`** - the perceptron pipeline.
2. **`w ← w + η·(target − pred)·x`** - the online update rule.
3. **Converges only if linearly separable; else it cycles → cap the epochs.**
4. **Memorization (Perceptron Theorem) vs generalization (PAC)** - Module 11 is the foil to Module 10.
5. **XOR → add a hidden layer; step → smooth activation → backprop → deep learning.**

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. St Catherine's attendance flags = a **binary classifier**: which two St Catherine's features (like the Bhardwaj `x, y`) would you feed a perceptron to flag an at-risk student, and would those two be **linearly separable** or would you need a hidden layer?
2. Your Student 360 data almost never splits with a clean line - so when a perceptron **never converges** on it, is that a data problem or a model problem, and which family member (SVM soft-margin? logistic probability?) would you reach for instead?

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] **Activity 1** - `a1_MLN601_Module11_perceptron_with_visualization.ipynb`: tune **η** and **n_iter**, watch the errors-per-epoch curve, post to forum.
- [ ] **Activity 2** - interactive demos (owenshen24 / TF Playground / Khan): break XOR with one layer, then fix it by adding a hidden layer.
- [ ] **Assessment 3** (due 19/08) - use the family table to justify your model choice in the write-up.
