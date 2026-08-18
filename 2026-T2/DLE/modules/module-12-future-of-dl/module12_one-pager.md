# DLE602 · Module 12 - One-Pager

> **Practical DL methodology · metrics & baselines · diagnosis before complexity · error vs ablative analysis · high-dimensional paradoxes · future DL systems**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Successful deep learning is an evidence loop: define the real objective, build the simplest end-to-end baseline, diagnose the dominant failure, make one controlled change, and measure again. The future needs better reasoning and reuse, not only bigger pattern recognisers.**
> (Goodfellow, Bengio & Courville, 2016, Ch. 11 · Smith, 2017 · Sejnowski, 2020 · Chollet, 2017)

```text
GOAL + METRIC -> BASELINE -> INSTRUMENT -> DIAGNOSE -> ONE CHANGE -> MEASURE
       ^                                                           |
       +-----------------------------------------------------------+
```

## 🖤 Zone 1 - Define success before training ⭐ SLO c)

| Metric | Use when | Trap |
|---|---|---|
| **Accuracy** | classes and error costs are balanced | hides rare-class failure |
| **Precision** | false positives are expensive | can rise by predicting fewer positives |
| **Recall** | false negatives are expensive | can rise by predicting more positives |
| **F1** | one score must balance precision + recall | hides the decision threshold |
| **Coverage** | model may abstain / defer to human | perfect accuracy at 0% coverage is useless |

- 🖤 **Training loss != evaluation metric.** Loss must be differentiable for weight updates; the metric must represent product value, safety, cost, and real error asymmetry (Goodfellow et al., 2016).
- 🔵 **Rare-event trap:** 99.9999% accuracy can detect nobody if the model always predicts the majority class.
- 🔵 **Street View target:** reach human-level **98% accuracy**, then maximise coverage toward **95%** by deferring uncertain cases.
- 🔴 **Assessment language:** state the metric, target, baseline, decision threshold, and why each matches the application. Do not report accuracy alone.

## 🖤 Zone 2 - Baseline, diagnose, then act ⭐ THE PRACTICAL CORE

| Train | Validation / test | Likely diagnosis | Evidence-based next move |
|---|---|---|---|
| poor | poor | underfit, optimisation, input, or code failure | fit tiny set; tune LR; inspect data/code; add capacity |
| good | poor | overfit or train/test mismatch | regularise; gather representative data; verify pipeline |
| good | good | target reached | stop, or justify the cost of further gains |

- 🖤 **Start from structure:** fixed vector -> logistic / feedforward; image -> CNN; sequence -> LSTM/GRU; related solved task -> transfer learning.
- 🔵 **Defaults:** SGD + momentum + LR decay or Adam; early stopping almost always; mild regularisation; batch normalisation if optimisation is difficult.
- 🔴 **Learning rate first.** Too high diverges; too low stalls or wastes compute. Grid search suits about 3 or fewer dimensions; random search covers influential dimensions better.
- 🔵 **Debug order:** visualise worst errors -> overfit one/few examples -> compare analytical/numerical gradients -> inspect activation/gradient histograms -> verify identical preprocessing.
- 🔴 **More data is not a universal fix.** If training performance is poor, extra examples do not repair capacity, optimisation, code, or bad inputs. Use log-scale learning curves to test whether data is likely to help.
- 🔵 **Street View lesson:** high-confidence errors exposed cropped digits; widening the crop improved coverage by **10 percentage points**. The winning fix was the data pipeline, not a novel model.

## 🖤 Zone 3 - Smith's seven phases + two analyses

```text
1 PREPARE -> 2 DATA -> 3 ANALOGY -> 4 SIMPLE BASELINE
     ^                                      |
     |                                      v
7 ADD COMPLEXITY <- 6 FINE-TUNE <- 5 VISUALISE / DEBUG
```

- 🖤 **Prepare:** is DL worthwhile? Define target, assumptions, compute, and success.
- 🔵 **Analogy before architecture:** find the closest solved problem, reproduce its result, inspect its code, then record exactly how the new domain differs (Smith, 2017).
- 🔵 **Limited data:** transfer learning, domain adaptation, synthetic data, or the nearest pretraining set. Representative coverage matters beyond class balance.
- 🔴 **Complexity is phase 7.** Ensembles and elaborate architectures need measured residual error and a cost-benefit case.

| Analysis | Compare | Question |
|---|---|---|
| **Error analysis** | current -> realistic ceiling | which failure categories block success? |
| **Ablative analysis** | baseline -> current | which added components caused the gain? |

- 🔴 **Activity 1 trap:** "perfect performance" may be impossible due to ambiguity, label noise, missing inputs, or Bayes error. Compare against a realistic human/reference ceiling; prioritise errors by frequency, cost, and fixability.

## 🖤 Zone 4 - Why DL works better than old intuition predicts

| Conventional intuition | Deep learning observation |
|---|---|
| too many parameters -> overfit | overparameterised networks can generalise |
| nonconvex optimisation -> trapped | SGD often finds useful solutions |
| must locate one good optimum | many parameter settings perform well |

- 🔵 **High-dimensional geometry:** many critical points are saddles, and overparameterisation may create many good routes and solutions - a "haystack of needles" (Sejnowski, 2020).
- 🔴 **Theory gap:** no complete explanation yet links SGD, architecture, inductive bias, sample complexity, and generalisation. Modern success does not prove that scaling alone yields AGI.
- 🔵 **Brain inspiration != brain equivalence.** CNN locality and reward-prediction ideas borrow from biology, but artificial units lack the brain's rich memory, routing, sleep, control, and lifelong adaptation.
- 🔴 **Future capability checklist:** self-supervision · imitation / generation · long-term memory · planning · specialist routing · social intelligence · stable lifelong learning without catastrophic forgetting.

## 🖤 Zone 5 - Chollet's future: pattern recognition + programs

```text
GEOMETRIC MODULES             ALGORITHMIC MODULES
patterns / intuition    +     logic / search / memory / abstraction
gradients                     search / RL / evolution
             -> modular, reusable, lifelong systems
```

| Direction | Change | Intended gain |
|---|---|---|
| **Models as programs** | loops, branches, variables, memory, graphs | abstraction + reasoning |
| **Beyond backprop alone** | gradients + search / RL / evolution | optimise discrete structures |
| **Automated ML** | learn architecture + weights | reduce manual design labour |
| **Lifelong modular reuse** | reusable features, procedures, subroutines | transfer with little data |

- 🖤 **Current limit = local generalisation:** networks interpolate well among familiar examples but struggle with systematic reasoning and extreme transfer (Chollet, 2017).
- 🔴 **Backprop stays.** It becomes one tool inside richer, partly non-differentiable systems.
- 🔴 **Engineer moves up the value chain:** less knob turning; more responsibility for data, objectives, constraints, evaluation, safety, and affected people. A loss function is a product specification.

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Deep Learning Final Project** · source code + **1500-word report +/- 10%** · **group** · **40%** · due **19/08/2026** · assessment SLOs **c) d) e)**; Module 12 directly addresses **c) e)**.
> ReviewPulse v3 demonstrates the methodology through one label/evaluation contract, a six-model ladder, aspect-aware comparisons, mixed-polarity error subsets, confusion matrices, latency and artifact-size evidence, regression tests, and retained negative results. The critical conclusion is not merely "DistilBERT won": explain why, what it cost, where every model failed, and which controlled experiment should come next.
> 🔴 **Next experiments justified by measured gaps:** multi-seed uncertainty · same-device efficiency · cross-domain evaluation · calibration / abstention · automatic aspect extraction.

## 🔴 If you only memorise 5 things

1. **Goal -> baseline -> diagnose -> one change -> measure.** Method beats novelty without evidence.
2. **Loss trains; metric judges.** Match precision, recall, F1, coverage, and thresholds to real error costs.
3. **Poor train + poor validation = fix capacity/optimisation/data/code. Good train + poor validation = overfit or pipeline mismatch.**
4. **Error analysis asks what still fails; ablation asks what actually helped.** Compare with realistic ceilings, not imaginary perfection.
5. **Future DL = geometric pattern recognition + algorithmic reasoning + modular lifelong reuse.** Bigger models alone are not the thesis.

---

### Margin prompts (answer in blue while you write - anchor to your day job)

1. For a St Catherine's attendance-risk model, what costs more: a false alarm or a missed at-risk student? Choose the metric, threshold, and human-abstention rule that reflects that decision.
2. In a school data warehouse pipeline, a high-confidence prediction is wrong because a source-system field was truncated. Which diagnostic exposes it, and why would changing the network architecture be the wrong first move?

### This-week to-dos (still 🕐 / 🔥 in your notes)

- [ ] 🕐 **Activity 1 - Last Opinion** (<=100 words, forum): qualify Smith's "current vs perfect" error-analysis definition using a realistic ceiling, irreducible ambiguity, and frequency/cost/fixability.
- [ ] 🕐 **Activity 2 - The Future is Here** (<=100 words, forum): propose one currently infeasible DL application and name the exact missing capability - learning, memory, reasoning, data, safety, or compute.
- [ ] 🕐 **Activity 3 - Final Discussion** (no submission): identify the subject's strongest topic, hardest interesting topic, weakest DL capability, and one credible route to improve it.
