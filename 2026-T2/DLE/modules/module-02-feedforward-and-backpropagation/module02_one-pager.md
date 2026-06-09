# DLE602 · Module 2 - One-Pager

> **Feedforward Neural Networks & Backpropagation - the anatomy, the forward pass, the learning engine**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape, 4 zones).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **A feedforward net = a stack of simple nonlinear functions that learns its own features to approximate a mapping `y = f(x; θ)`, trained by gradient descent.**
> (Goodfellow Ch.6's spine. Pays off M1's promise: backprop is the engine that trains the internal representations.)

## 🖤 Zone 1 - Anatomy of a Network ⭐ (draw input → hidden → output, left to right)
```
x ─►(•)─►(•)─► ŷ      one neuron = Σ(w·x) + b → activation
   input  hidden  output
```
| Part | What it does |
|---|---|
| **Input layer** | raw feature vector enters here |
| **Weights (w)** | scale / combine signals - the learned knobs |
| **Bias (b)** | shifts the activation threshold |
| **Hidden layer(s)** | learn intermediate representations |
| **Activation** | injects nonlinearity (the whole point) |
| **Output layer** | converts features → prediction format |

- 🔴 **Hidden = "hidden" because the data never says what they should output** - the net *discovers* these representations itself.
- 🔵 "MLN" / **MLP** (multi-layer perceptron) = the classic feedforward net.

## 🖤 Zone 2 - Feedforward Flow = the forward pass
- Info travels **one way only**: input → hidden → output. **No loops** (that's what "feedforward" means).
- 🔵 Pathmind's loop in plain words:
```
input · weight = guess
truth - guess  = error
error · contribution = weight adjustment
```
- 🔵 **Depth = composition:** `f(x) = f3( f2( f1(x) ) )` - each layer hands a better representation to the next.
- 🔴 **Trap:** stack linear layers only and the whole thing **collapses to one linear layer**. Nonlinear activations are *mandatory*, not decoration.

## 🖤 Zone 3 - Activation Functions + XOR ⭐ (the teacher's focus + Activity 1)
| Activation | Use | Gotcha |
|---|---|---|
| **ReLU** `max(0,z)` | **default** hidden unit | dead units if always ≤ 0 |
| **Sigmoid** | binary output prob | **saturates** → tiny gradients |
| **tanh** | zero-centred hidden | also saturates at extremes |
| **Softmax** | multiclass output | probs across classes sum to 1 |

- 🔵 **XOR = the canonical proof:** a linear model **cannot** separate XOR; **one hidden layer can** by remapping inputs into a space where a line *does* split them.
- 🔴 **Activity 1 in one breath:** "A hidden layer learns a nonlinear representation, then a linear output reads it off." That's the whole XOR story.

## 🖤 Zone 4 - Backpropagation = the Learning Engine ⭐
```
forward pass → loss → BACKWARD chain-rule gradients → optimiser (SGD) updates w,b → repeat
```
- 🔴 **#1 EXAM TRAP:** backprop **only computes the gradients**. It is **NOT** the whole learning algorithm - the **optimiser (SGD/Adam)** does the actual weight update.
- 🔵 Works on a **computational graph**, reusing shared subexpressions → efficient (no naive chain-rule blowup).

| Output unit | Task | Loss |
|---|---|---|
| **Linear** | regression | MSE |
| **Sigmoid** | binary class | binary cross-entropy |
| **Softmax** | multiclass | cross-entropy |

## 🔴 Class-Discussion Prep (answer the teacher's 2 questions out loud)
- **Why are NNs useful?** → they **learn features automatically** (no hand-engineering), are **universal approximators**, and **scale** with more data + compute.
- **How do they differ from traditional ML?** → classic ML leans on **hand-built features**; NNs **build their own abstractions** via depth. Cost: **more data, more compute, less interpretable** (← that's Activity 3's "disadvantages").

## 🔴 Assessment Hook (bottom red strip)
> **A1 is still classical N-grams** (Programming Problems, 30%, due **28/06/2026**) - **no neural net there**. But FNN + backprop + activations are the **foundation for A2/A3**: the **ABSA "Review Pulse v2"** proposal, where attention-LSTM and a fine-tuned transformer replace the N-gram baseline.

## 🔴 If you only memorise 5 things
1. **Neuron = `Σ(w·x)+b → activation`**; net = input → hidden → output, info flows **one way**.
2. **Hidden layers are unsupervised internally** - the net discovers the representations.
3. **No nonlinearity ⇒ the deep net is just one linear layer.** Activations earn the depth.
4. **XOR** = the proof a hidden layer lets a linear output solve a nonlinear task.
5. **Backprop computes gradients; the optimiser updates weights.** Don't conflate them.

---

### Margin prompts (answer in blue while you write)
1. Sketch XOR's 4 points - why can't one line split them, and what does the hidden layer do to fix it?
2. Name one **disadvantage** of NNs you'd defend in Activity 3 (data-hungry? compute? black-box?).

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] Activity 1 - **Understanding Feedforward Networks** (the 100-word XOR description)
- [ ] Activity 2 - **Backpropagation** knowledge-share + pose a question
- [ ] Activity 3 - **Disadvantages of Neural Networks** (≤100 words)
- [ ] Finish 🔥 Fernandes video - *Neurons & Artificial Neurons* (LinkedIn Learning)
