# Module 12 Follow-up Quiz - Answer Key

Use this after completing `module12_follow-up-quiz.md` closed book. Equivalent answers earn credit when they preserve the same technical and governance distinctions.

## 1. DBMS versus warehouse (8 points)

A **database management system (DBMS)** is software that defines, stores, queries, secures, and manages access to data. A **data warehouse** is an analytics-oriented data architecture, normally implemented using a DBMS or cloud data platform, that integrates historical data from multiple sources; operational DBMSs can instead serve transactional workloads.

## 2. Enterprise-grade ML (10 points)

`train in cloud -> score in DBMS -> govern everywhere`

- Cloud training centralises data and provides elastic compute.
- DBMS scoring brings inference close to governed data, reducing movement, latency, and exfiltration risk.
- End-to-end governance preserves access control, versioning, provenance, fairness evidence, and auditability from source data to decision.

## 3. Snorkel workflow (10 points)

`unlabelled data -> labelling functions -> generative label model -> probabilistic labels -> discriminative model`

LFs emit noisy votes or abstain. The generative label model estimates LF quality and dependencies, then produces probabilistic labels. The discriminative model learns from those labels and input features. This differs from majority vote because it can learn that some LFs are more reliable or correlated than others.

## 4. St Catherine's architecture (12 points)

One defensible flow is:

`authorised source snapshots -> governed warehouse features -> versioned model scored in warehouse -> immutable score record -> counsellor/teacher review -> documented intervention`

Warehouse scoring is reasonable when the platform supports controlled model execution, versioning, monitoring, and audit logs: data remains near its governed source. It is not automatically correct merely because "the data sits there". A separate service may be preferable if the warehouse cannot meet latency, model-runtime, rollback, isolation, or operational-support requirements.

## 5. Ownership and accountability (12 points)

| Stage | Example accountable owner | Why |
|---|---|---|
| Source-data quality | Registrar or source-system business owner | Defines the authoritative record and correction process. |
| Warehouse and feature pipeline | Data/platform owner | Owns ingestion, transformations, access, freshness, and reliability. |
| Model validation and deployment | ML owner with independent risk review | Owns model evidence and operation without self-approving high-impact policy. |
| Decision policy and threshold | Student-services leadership with governance approval | Chooses the acceptable trade-off and authorised use. |
| Student intervention | Teacher, year coordinator, or counsellor | Applies context and communicates support. |
| Appeals and safeguarding | Designated safeguarding/privacy authority | Provides independent review and protects student rights. |

One engineer may implement sources, warehouse, and model, but accountable business ownership and independent review must remain visible.

## 6. Decision lineage (12 points)

Minimum lineage includes:

- source record identifiers, event times, consent/access basis, and extraction snapshot;
- transformation code version, feature definitions, feature values, and pipeline run;
- training dataset snapshot, model artifact/version, hyperparameters, validation results, and deployment environment;
- scoring timestamp, input feature vector, output score, model version, and monitoring state;
- threshold/policy version, intended use, approval, and explanation shown to the reviewer;
- reviewer identity, contextual checks, final decision, intervention, notification, correction, and appeal history.

The chain must reproduce the score and distinguish it from the later human decision.

## 7. Three abstaining LFs (12 points)

```python
def lf_poor_grades(row):
    if row.assessments_observed < 2:
        return ABSTAIN
    if row.current_average < 50:
        return 1
    if row.current_average >= 65:
        return 0
    return ABSTAIN

def lf_repeated_absences(row):
    if row.school_days_observed < 10:
        return ABSTAIN
    if row.unexplained_absences_20d >= 3:
        return 1
    if row.unexplained_absences_20d == 0:
        return 0
    return ABSTAIN

def lf_negative_trend(row):
    if row.prior_periods < 2:
        return ABSTAIN
    if row.grade_change <= -10:
        return 1
    if row.grade_change >= 0:
        return 0
    return ABSTAIN
```

Thresholds are hypotheses to validate, not policy truths. Missing context and borderline cases should abstain.

## 8. Gold set (10 points)

Sample 100 historical cases across classes, year groups, risk-score ranges, outcomes, demographic groups, missing-data patterns, and difficult boundary cases. Two authorised domain professionals independently label each case under a written rubric; a third adjudicates disagreement. Keep a development portion for LF iteration and an untouched held-out test portion for final evaluation. Do not tune LF thresholds against the final hold-out.

## 9. Coverage and conflict (8 points)

Example distrust signals:

- Aggregate LF coverage below **30%** means most students receive no weak-supervision signal, so claimed scale is unsupported.
- Conflict above **40% of covered examples**, especially between LFs using similar inputs, suggests unstable thresholds, hidden correlation, or an unclear label policy.

These are diagnostic warning thresholds, not universal laws. Compare them with held-out accuracy, subgroup behaviour, and the expected prevalence of follow-up needs.

## 10. Defensible decision (6 points)

A score is a versioned statistical signal with uncertainty, not a conclusion about a student. A trained and authorised human reviewer must verify context, apply the approved policy, document the rationale, and provide correction or appeal before a consequential intervention.
