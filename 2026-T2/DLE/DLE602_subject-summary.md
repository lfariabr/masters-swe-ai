# DLE602 Deep Learning - Subject Summary

**Status:** Complete

**Term:** T2 2026

**Facilitator:** Dr. Tayab Din Memon

**Release:** v4.2.0 (planned T2 completion release)

## TL;DR

DLE602 built one continuous line from a shallow N-gram baseline through the full deep learning stack to an aspect-aware sentiment system with an explainability layer on top. The subject moved from feedforward networks and backpropagation through CNNs, linear factor models, autoencoders, RNN/LSTM sequence modelling, representation learning and structured probabilistic models, then closed with visual analytics for interpretability and the practical methodology that ties evidence-driven iteration to a stated future direction for the field.

The three assessments formed one deepening line of work on the same problem - review sentiment classification. A programming-problems assignment built the N-gram foundation; a project proposal scoped ReviewPulse as a group aspect-based sentiment system; and the final project delivered ReviewPulse v3.0, a six-model ladder from TF-IDF through DistilBERT with attention and gradient x input attribution for interpretability.

## Learning Arc

| Phase | Modules | What became operational knowledge |
|---|---|---|
| Foundations | 1-2 | Representation quality drives performance more than raw features; feedforward networks and backpropagation compute and propagate gradients through a computational graph. |
| Applications and generalisation | 3-4 | Deep learning's three flagship domains (NLP, speech, vision) share GPU-scale infrastructure; regularisation trades a little bias for a lot less variance across five identifiable levers. |
| Structured and generative representations | 5-7 | CNNs exploit sparse interactions, parameter sharing and translation equivariance on grid data; linear factor models and autoencoders recover and generalise structure such as PCA under a bottleneck. |
| Sequence and structure modelling | 8-10 | RNN/LSTM gating manages vanishing/exploding gradients across time; representation learning is always defined relative to a downstream task; graphical models trade tractability for structure via conditional independence. |
| Interpretability and methodology | 11-12 | Visual analytics turns activations and gradients into pictures a human can check for shortcut learning; practical methodology closes the loop with metric selection, baseline-first iteration, and evidence-based diagnosis before adding complexity. |

## Assessments

### Assessment 1 - Programming Problems - 90/100

- Implemented the N-gram language-modelling foundation and companion programming exercises, establishing the technical baseline later extended into ReviewPulse.
- Delivered source code plus a 500-word report against SLOs `a)` and `b)`.

### Assessment 2 - Deep Learning Project Proposal Presentation - 85/100

- Scoped ReviewPulse as a group aspect-based sentiment analysis system, defining the problem, dataset (SemEval-2014 Task 4 Restaurants), model ladder, and evaluation plan.
- Delivered a 1000-word report and a 5-7 minute group presentation against SLOs `b)`, `c)`, `d)`, `e)`.

### Assessment 3 - Deep Learning Final Project - submitted, grade pending

- Delivered ReviewPulse v3.0: a shared label/evaluation contract across six models (TF-IDF, target LSTM, target GRU, TextCNN review-only, ATAE-LSTM, DistilBERT aspect-conditioned).
- DistilBERT led on predictive metrics; the two aspect-conditioned models (ATAE-LSTM, DistilBERT) showed the smallest accuracy drop on the 228-instance mixed-polarity subset, evidence that reading the aspect specifically helps on the hardest cases.
- Delivered interpretability alongside prediction: gradient x input attribution aligned to visible token spans, plus attention-weight inspection, in place of CNN-only techniques that do not transfer to text.
- Retained negative and partial results rather than presenting only the winning model, matching the module's practical-methodology standard of reporting evidence honestly over chasing a clean narrative.
- Submitted as a group project with Victor Javier Dorantes Meneses and Juan Sebastian Martinez Contreras.

## Portfolio Outcome

DLE602 produced one connected portfolio artifact rather than three disconnected assignments:

- an N-gram baseline that framed the sentiment-classification problem and its limitations;
- a scoped, dataset-grounded project proposal for an aspect-based sentiment system;
- a deployed six-model ReviewPulse v3.0 application (Streamlit, compare mode, gold-label column) with a documented model ladder, mixed-polarity error analysis, confusion matrices, and an interpretability layer built specifically for a text model rather than borrowed wholesale from CNN visual-analytics tooling.

Together they show the complete path from a shallow classical baseline to a deep, aspect-aware, explainable system, with interpretability treated as a deliverable rather than an afterthought.

## Strategic Takeaways

1. **Representation quality dominates raw feature engineering.** Depth exists to build higher-level concepts from simpler ones, not to add parameters for their own sake.
2. **Regularisation is a small number of levers, not a bag of unrelated tricks.** Data, architecture, error function, regularisation term, and optimisation cover augmentation, dropout, and batch norm alike.
3. **Sequence models must fight their own gradient dynamics.** LSTM gating manages, but does not remove, the vanishing-gradient problem that plain RNNs cannot survive past roughly ten to twenty steps.
4. **A representation is only "good" relative to a task.** There is no representation quality in the abstract, only in what it makes easier downstream.
5. **Structure trades expressiveness for tractability.** Graphical models, and factor models before them, work by asserting which variables do not interact, not by modelling everything.
6. **Accuracy alone cannot reveal a shortcut feature.** Visual analytics - activations, gradients, attribution - exists because a model can be confidently right for the wrong reason, and the wrong reason costs more once deployed.
7. **Method beats novelty without evidence.** Goal, metric, baseline, diagnosis, one controlled change, and re-measurement outperform reaching for a bigger architecture on instinct.
8. **Interpretability must match the model's modality.** Grad-CAM assumes a spatial feature map; a text model needs attention weights and gradient x input aligned to tokens instead.
9. **The strongest project conclusion states cost and failure mode, not just a winner.** DistilBERT's lead came with a storage cost, and every model in the ladder failed somewhere specific and reportable.

## Closure State

- All 12 modules completed with study notes and revision one-pagers.
- Module 12 closed with a closed-book follow-up quiz; no further live lecture was scheduled - Dr Tayab Din Memon's final session (19 August 2026) was feedback-only, with the next scheduled touchpoint roughly six to eight weeks into Work Integrated Learning I.
- All three assessments submitted; Assessment 3 grade remains pending.
- DLE602 module and assessment epics are ready to close.
- Next learning edge: extending the ReviewPulse interpretability layer (attention, gradient x input) into production monitoring, and carrying the evidence-driven methodology from Module 12 into Work Integrated Learning I.
