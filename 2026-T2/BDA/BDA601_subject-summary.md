# BDA601 Big Data and Analytics - Subject Summary

**Status:** Complete

**Term:** T2 2026

**Facilitator:** Dr. Chen Zhan

**Release:** v4.2.0 (planned T2 completion release)

## TL;DR

BDA601 developed one end-to-end discipline: start with a decision and its data requirements, build a governed path from source to usable evidence, choose analytical methods that fit the question, and communicate limitations without overstating what the model proves. The subject moved from the Vs, sourcing and lakehouse architecture through Spark, cleaning, classification, evaluation, regression, clustering, association rules and graph analytics, then closed with privacy, security and accountable data governance.

The three assessments formed a practical progression. A governed Big Retail lakehouse design established the data foundation; a Spark MLlib churn study tested leakage-safe classification and decision thresholds; and a global COVID-19 pipeline joined regression, K-Means, graph relationships and lead-lag analysis into a stakeholder recommendation.

## Learning Arc

| Phase | Modules | What became operational knowledge |
|---|---|---|
| Frame Big Data value | 1-3 | Use the Vs to connect scale and complexity to a business decision; assess source fitness, ingestion, identity resolution, integration and storage architecture. |
| Build the analytics platform | 4-5 | Use Spark's distributed model deliberately; profile and clean data before modelling; preserve training/test boundaries and data-quality evidence. |
| Predict and evaluate | 6-8 | Build classification and regression models; compare them with meaningful baselines and class-specific metrics; separate ranking quality from threshold policy. |
| Discover structure and relationships | 9-11 | Select and interpret clusters without treating them as truth; distinguish association from causation; represent relationships through graph nodes, edges and defensible weights. |
| Govern the lifecycle | 12 | Separate privacy from security; classify before controlling; protect data at rest, in motion and in use; prevent, detect and respond; manage re-identification and disclosure risk. |

## Assessments

### Assessment 1 - Big Retail data pipeline - 93/100

- Designed a governed lakehouse that integrated customer, session, order, product, marketing and external-context data for personalisation and conversion recovery.
- Addressed schema alignment, duplicate identities, guest checkout, batch/streaming ingestion, quality controls and source reliability before storage.
- Used Bronze, Silver, Gold and Serving layers with an AWS-oriented implementation and explicit governance and low-latency access paths.
- Main feedback edge: make diagram text larger, keep core evidence in the body, and show concrete confidence rules for identity matching.

### Assessment 2 - Telco churn modelling - 91/100

- Built a leakage-safe Spark MLlib workflow with deterministic stratified train/validation/test partitions and training-only preprocessing.
- Showed why accuracy was inadequate against a `73.5%` majority baseline and made churn recall, precision, F1 and AUC visible.
- The tuned Random Forest achieved `AUC 0.833`, churn recall `0.754`, and churn F1 `0.618` at threshold `0.30`; a lower cost-based threshold could raise recall at a substantial precision cost.
- Main feedback edge: preserve the analytical quality while cutting material that exceeds the brief, and phrase model outputs as risk signals rather than certainties.

### Assessment 3 - Global COVID-19 analytics - submitted, grade pending

- Analysed 164 weeks of JHU confirmed-case data across regression, K-Means, graph analytics and stakeholder visualisation.
- Selected the US as the focal country using consistently defined weekly-case variance, then selected `k=3` with silhouette `0.705` and a supporting elbow result.
- Found a five-week surge phase averaging about `7.04x` the overall US weekly mean.
- Same-week correlation favoured Canada (`r=0.848`) over Mexico (`r=0.697`), but lead-lag analysis reversed the operational recommendation: Mexico followed the US by about two weeks at `r=0.805`, while Canada moved with or ahead of it.
- Kept the conclusion conditional: correlation is not causation, confirmed cases depend on testing/reporting, and one fixed lag averages over changing variants and policies.

## Portfolio Outcome

BDA601 produced three connected portfolio artifacts rather than one standalone application:

- an auditable Big Retail data-platform architecture tied to campaigns, recommendation, association analysis and conversion;
- an executed Spark churn notebook and report that connect data quality, model evaluation and operating thresholds to a retention decision;
- an executed COVID-19 notebook, visual deck and recording that turn multiple analytical methods into one restrained recommendation.

Together they show the complete path from architecture to modelling to communication, with governance treated as part of the system rather than an appendix.

## Strategic Takeaways

1. **Value starts with the decision.** Volume and tooling do not justify a pipeline unless the data and outputs support a defined organisational action.
2. **Integration errors are modelling errors upstream.** Schema mismatch, duplicate identities, timestamps and source reliability can invalidate later results silently.
3. **Validation design is part of the claim.** Splits, baselines, preprocessing boundaries and metric choice determine what evidence a model actually provides.
4. **Thresholds encode operating costs.** AUC measures ranking; the chosen cut-off decides the precision/recall trade-off people experience.
5. **Clusters and graph edges are definitions, not discoveries from nature.** Features, distance, `k`, nodes and weights must be justified before their patterns are interpreted.
6. **Correlation needs temporal and causal restraint.** Lead-lag analysis can improve an operational hypothesis, but it does not prove transmission or policy impact.
7. **Privacy is broader than security.** Strong encryption cannot legitimise excessive collection, secondary use, indefinite retention or unsafe disclosure.
8. **Governance must leave evidence.** Owners, approvals, logs, access reviews, retention decisions and incident workflows make controls auditable.

## Closure State

- All 12 modules completed with study notes and revision one-pagers.
- Module 12 closed with the 18 August class synthesis and a scheduled closed-book follow-up quiz.
- All three assessments submitted; Assessment 3 grade remains pending.
- BDA601 module and assessment epics are ready to close.
- Next learning edge: production-scale streaming, causal/temporal validation, privacy-preserving analytics, and measurable data-product operations.
