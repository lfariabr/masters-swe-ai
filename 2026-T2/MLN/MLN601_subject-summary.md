# MLN601 Machine Learning - Subject Summary

**Status:** Complete

**Term:** T2 2026

**Facilitator:** Dr. Kamran Shaukat

**Release:** v4.1.0

## TL;DR

MLN601 moved from choosing algorithms to designing evidence for decisions. The subject began with CRISP-DM, data quality, regression, trees, Bayes, and SVMs; expanded into explainability, logistic regression, clustering, PAC learning, and perceptrons; and ended with enterprise-grade ML, model lineage, MLOps, and weak supervision.

The main practical outcome was the **Sommelier API**: two models over the same 6,497 wine records, but with different decision contracts. The regression lens estimates quality; the classification lens screens potentially weak lots for expert review. The larger lesson is that a useful ML system is defined by its decision, validation protocol, deployment boundary, and human owner, not by model accuracy alone.

## Learning Arc

| Phase | Modules | What became operational knowledge |
|---|---|---|
| Frame the problem | 1-2 | Translate an organisational question into a measurable ML task; use CRISP-DM as an iterative control loop; treat ethics and data provenance as design inputs. |
| Supervised foundations | 3-6 | Compare regression, decision trees, Bayes classifiers, ensembles, and SVMs; choose metrics and baselines that reflect the cost of errors. |
| Evaluate and explain | 7-8 | Use explainability as evidence rather than decoration; keep preprocessing inside validation pipelines; distinguish threshold choice from model training. |
| Learn structure and limits | 9-11 | Use clustering without pretending clusters are truth; reason about generalisation through PAC concepts; connect the perceptron's linear boundary to modern neural networks. |
| Operate ML responsibly | 12 | Treat models as software derived from data; train in cloud, score near governed data where justified, preserve lineage, monitor drift, and use weak supervision only when label scarcity warrants it. |

## Assessments

### Assessment 1 - Wine-quality regression - 84/100

- Compared linear, regularised, tree, and ensemble regressors under CRISP-DM.
- The Random Forest achieved approximately `RMSE 0.61` and `R2 0.50`, outperforming the mean baseline and linear family.
- The key correction from feedback was to connect business success criteria, model approval, data-quality validation, and feature engineering more explicitly.

### Assessment 2 - Wine-lot classification - 89.5/100

- Reframed the same wine data as a quality-control screening decision rather than another prediction exercise.
- Compared nine model families and controlled scaling, resampling, weighting, thresholding, and explainability inside the validation design.
- The approved class-weighted Random Forest achieved test `AUC 0.834`, sensitivity `0.714`, specificity `0.806`, and balanced accuracy `0.760`.
- The operational contract remained human-in-the-loop: flag lots for expert tasting, never automate release or rejection.

### Assessment 3 - Capital Bikeshare demand regression - submitted, grade pending

- Compared regression families against two different baselines under separate random-holdout and forward-temporal protocols.
- The selected model improved MAE by `73.9%` over the training-mean baseline on the conditional holdout.
- It failed the stronger deployment gate, recording a `-23.5%` advantage against the rolling-seven-day baseline on forward time.
- The honest conclusion was therefore conditional approval for explanatory estimation, not approval as a frozen forward forecasting service.

## Portfolio Outcome - Sommelier API

The wine assessments became a production-oriented portfolio service instead of remaining disconnected notebooks:

- a regression endpoint for quality estimation;
- a classification endpoint for lot screening;
- leakage-audited training and assessment-to-artifact provenance;
- parity tests between notebook evidence and served behaviour;
- FastAPI and Streamlit interfaces with model-card and decision-contract thinking.

Project: [Sommelier API](https://github.com/lfariabr/sommelier-api)

Article: [I gave the same 6,497 wines to two models and asked them different questions](https://dev.to/lfariaus/i-gave-the-same-6497-wines-to-two-models-and-asked-them-different-questions-4hdn)

## Strategic Takeaways

1. **Problem framing dominates algorithm choice.** The same rows support materially different products when the target, error cost, threshold, and user action change.
2. **Validation must match deployment time.** Random holdouts answer interpolation questions; forward tests expose whether a frozen model survives changing conditions.
3. **Baselines are competitors.** A simple recent-history rule can be harder to beat than a sophisticated model and may be the correct production choice.
4. **Pipelines are part of the model.** Imputation, scaling, feature construction, resampling, and threshold selection must be versioned and validated without leakage.
5. **Metrics require an owner and an action.** AUC, RMSE, and R2 are evidence, not decisions. Business thresholds and interventions need accountable human owners.
6. **Explainability is role-specific.** Developers need diagnostics and reproducibility; operators need actionable reasons; governance needs lineage, intended use, and audit evidence.
7. **Production is the majority of the work.** Packaging, observability, drift response, rollback, access control, and decision logging determine whether a notebook becomes a defensible system.
8. **Weak supervision is conditional.** Snorkel-style labelling functions help when reliable labels are scarce and noisy sources overlap; they do not replace a separate gold set or expert review.

## Closure State

- All 12 modules completed with notes and revision one-pagers.
- All three assessments submitted; Assessment 3 grade remains pending.
- Sommelier API shipped as the subject portfolio project.
- Module 12 follow-up quiz scheduled for Thursday, 20 August 2026.
- Next learning edge: production monitoring, temporal retraining policy, calibration, and governed human intervention.
