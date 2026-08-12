# DLE602 · Module 11 - One-Pager

> **Visual analytics in deep learning · interpretability & explainability · attribution vs feature visualisation · activations vs gradients · bias & adversarial robustness**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Your model scored well. Accuracy cannot tell you whether it learned the thing you wanted or something else that happened to correlate. Visual analytics turns the internals into a picture so a human can check.**
> (Hohman, Kahng, Pienta & Chau, 2018 - *Visual Analytics in Deep Learning: An Interrogative Survey*)

---

## 🖤 Zone 1 - The Five W's and How (the framework - memorise the six headings)

```
  WHY  ── interpretability & explainability · debugging & improving
          comparing & selecting models · teaching DL concepts
  WHO  ── model developers  >  model users  >  non-experts
  WHAT ── computational graph · learned params (weights, filters)
          individual units (activations, GRADIENTS) · neurons as
          high-dim space · aggregated (groups, metrics)
  HOW  ── node-link · dim-reduction+scatter · line charts
          instance analysis · interactive experimentation · attribution
  WHEN ── during training      |      after training
  WHERE── domains (NMT, RL, medical, driving) + hybrid VIS/AI community
```

- 🔵 **Their template sentence** (use it to position ANY tool, including yours):
  *"To interpret representations (why), model developers (who) visualise neuron activations in CNNs (what) using t-SNE (how) after training (when) to solve an urban planning problem (where)."*
- 🔵 **Interpretation vs explanation** (Montavon et al.): an **interpretation** maps an abstract concept into a human-sensible domain; an **explanation** is the set of interpretable-domain features that produced *this* decision (e.g. a heatmap). Lipton: an explanation can show predictions **without** revealing the mechanism.
- 🔴 **There is NO agreed formal definition of interpretability.** The survey says so about itself. This is your critical-edge sentence.
- 🔵 **Visualisation vs visual analytics** (Tayab named this as a learning outcome): **visualisation** = the picture (chart, heatmap, confusion matrix); **visual analytics** = picture **+ interaction + a human reasoning loop**. That is why the survey studies *systems*, not images.
- 🔴 **What actually opens the black box** (his answer, after pushing the class): **domain expertise + critical thinking.** The visualisation supports the judgement; it does not replace it.

## 🖤 Zone 2 - WHAT maps to HOW ⭐ SLOs c) + d) - THE GRADED CORE

| You want to inspect | You draw | Weakness |
|---|---|---|
| architecture / dataflow | **node-link diagram** (TensorBoard) | "hairball" at scale; needs edge bundling |
| activations of many instances | **t-SNE / PCA scatter** | t-SNE very sensitive to hyperparameters |
| loss, accuracy per epoch | **line chart** | one number hides the model |
| one instance's behaviour | **instance analysis**, confusion matrix | doesn't generalise |
| learned filters / class concept | **feature visualisation** | trustworthiness questioned |
| **gradients during BPTT** | **RNNbow stacked bars** | `O(n²)`, huge logs |

## 🖤 Zone 3 - Activations vs Gradients (the sharpest idea in the module)

```
   ACTIVATIONS  ──>  how the network DECIDES   (inference, usually after training)
   GRADIENTS    ──>  how the network LEARNS    (training, the update signal)

   Most surveyed work sits in the activation box.
   RNNbow is the counterexample: gradients, DURING training.
```

- 🔵 **CNNComparator** (Zeng et al., 2017): compares **two snapshots of ONE training run** (epoch 10 vs 100), 4 linked views, `model -> layer -> channel -> neuron`. *Not* two different models - random init makes cross-run comparison uninterpretable.
  - 🔴 **The finding:** epoch 100 still called a **daffodil a buttercup** because it latched onto **yellow**. A shortcut feature.
- 🔵 **RNNbow** (Cashman et al., 2017): stacked bars per timestep; **dark = short gradient horizon** (local loss only), **light/spread = long-range dependencies being learned**. Only visualises `W` because `W` is the memory. Chose `k = 5` empirically - past 5 steps nothing was left.
  - 🔴 Renders the **vanishing gradient** from Module 8 as a shape, not a formula.

## 🖤 Zone 4 - The CNN toolkit you can actually run (Pal, 2019)

- 🔵 **The motivation - snow leopard vs Arabian leopard.** Snow backgrounds vs desert. The model can score high by learning **snow vs sand** and never look at the cat. Accuracy cannot reveal this.
- 🔵 **Layerwise outputs:** early layers = **edges**; deep layers = **object parts** (roof, exhaust).
- 🔵 **Activation maximisation** = what the model **expects**. Optimise a random image to maximise a class. Elephant → tusks, eyes, trunk = dataset is fine. Elephant → grass and trees = **your dataset is too narrow**.

| | Granularity | Gradients? | Cost |
|---|---|---|---|
| **Occlusion map** | patch | no, forward only | expensive |
| **Saliency map** | pixel | yes, 1 backward pass | cheap, noisy |
| **Grad-CAM** | coarse region, class-specific | yes, into last conv layer | cheap - the default |

- 🔵 **Grad-CAM in 4 steps:** final conv feature map (`14x14x512` VGG16) → gradient of output w.r.t. it → global-average-pool the gradients → weight each map.
- 🔴 **Guided backprop** truncates negative gradients to 0, so only positively-influencing pixels survive.

## 🖤 Zone 5 - Open problems 🔴 (this is where the marks are)

1. **Furthering interpretability** - new representations + interactions + cheaper attribution.
2. **Scalability** - visual (clutter, dim-reduction point limits) and system (real-time, web).
3. **Design studies** - most AI-side work has **no user study**; multi-view interfaces overwhelm; bring in HCI/UX.
4. **The human role** - human-understandable output; **human-AI pairing** / intelligence augmentation.
5. **Bias detection** - Google **Facets** previews class imbalance *before* training; equal opportunity is **not** automatically preserved by ML algorithms (loan-granting example).
6. **Adversarial attacks** - imperceptible perturbations fool classifiers; Adversarial Playground. Survey argues visualisation should **detect and defend**, not just display.

---

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Deep Learning Final Project** · source code + **1500-word report ±10%** · **group** · **40%** · due **19/08/2026** (end of Module 12) · SLOs **c) d) e)**.
> **What Tayab asked for in the Wk 12 class:** (1) pick **ONE visualisation** from your project and write **2-3 sentences** on what it shows; (2) for sentiment projects the expected minimum is a **confusion matrix** with the results explained; (3) an **optional 4-6 min demo video** of the running code, submitted with the report and code - *"just show the exact thing running"*, no commentary.
> Anything richer (attention, gradient × input) sits **above** that bar, not instead of it, and feeds the 30% "integration / depth of discussion" criterion.
> ⚠ For a **text** model the CNN techniques do not transfer: use **attention weights** aligned to token offsets and **gradient × input**, not Grad-CAM.
> 🔴 His stated standard: ***"Do not expect very high accuracy. Expect to know why."*** (from his own paper - a PhD student's "exceptionally good" bacterial-detection results turned out to contain discrepancies).

## 🔴 If you only memorise 5 things
1. **Five W's and How** = Why · Who · What · How · When · Where. It is the survey's whole structure and a template for positioning any tool.
2. **Activations show how it decides; gradients show how it learns.** RNNbow is the gradient counterexample.
3. **The snow-leopard problem** = shortcut feature. Right answer, wrong reason. CNNComparator's version = daffodil misread as buttercup because of **yellow**.
4. **Occlusion (patch, no gradients) < Saliency (pixel, 1 backward pass) < Grad-CAM (coarse, class-specific, the default).** Activation maximisation diagnoses the **dataset**, not the input.
5. **Epistemic honesty is graded.** No agreed definition of interpretability; some attribution methods have been shown to return **incorrect** results; most tools ship with **no user study**. Present visual evidence as *indicative*, never as proof.

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. St Catherine's attendance flagging: if a model predicted "at-risk" students and it were secretly keying off **year group or house** instead of the actual attendance pattern, which of the six techniques above would expose that, and at what point in the pipeline would you run it?
2. Take the teacher-comment sentiment work: which tokens in a comment actually drove the label? Sketch what a **gradient × input** row would look like over one real comment, and write the one-sentence caveat you would put under it before showing it to Lucas.

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] 🕐 **Activity 1 - Opinion Matters** (≤100 words, forum): react to Hohman et al.'s claim about visual analytics in modern AI. *Agree, then qualify with the survey's own three admissions.*
- [ ] 🕐 **Activity 2 - Interactive Learning Activity** (≤100 words, forum): play with **playground.tensorflow.org**, report whether the visualisation helped you understand the model. *He set this as PRE-class work: change 1-2 parameters, record ONE observation.*
- [ ] 🕐 **Activity 3 - Discussion** (no submission): will you use visual analytics in A3? Any unique benefit discovered while building?
- [ ] 🕐 **A3 (his explicit ask):** choose ONE visualisation from ReviewPulse + write 2-3 sentences on what it shows. Confusion matrix is the floor.
- [ ] 🕐 Decide on the **optional 4-6 min demo video** (running code only).
- [ ] 🔥 Produce ONE real figure for A3 (attention + gradient × input on a mixed-polarity case) and write its limitation caption.
