# Module 12 Follow-up Quiz

**Scheduled:** Thursday, 20 August 2026, early morning

**Time box:** 20 minutes

**Mode:** Closed book, written answers, then check the separate answer key

Do not open `module12_follow-up-quiz-answers.md` until every question has an answer. Use precise system boundaries, owners, and evidence rather than broad statements such as "keep it transparent."

## Questions

### 1. DBMS versus warehouse (8 points)

Define a DBMS in one sentence. Then explain why a data warehouse is a use of database technology rather than a synonym for every DBMS.

### 2. Enterprise-grade ML (10 points)

Complete and explain the Module 12 architecture in three clauses:

`train in ______ -> score in ______ -> govern ______`

What problem does each clause solve?

### 3. Snorkel workflow (10 points)

Put these components in order and state the output of each model:

- discriminative model
- labelling functions
- generative label model
- unlabelled data
- probabilistic labels

Why is this not ordinary majority voting?

### 4. St Catherine's architecture (12 points)

Sketch an attendance-risk flow containing at least:

`SIS + attendance + learning results + authorised wellbeing signals -> warehouse -> feature/model version -> risk score -> human review -> intervention`

Mark the exact scoring location. Give one reason to score in the warehouse and one reason not to place scoring there automatically.

### 5. Ownership and accountability (12 points)

Assign an accountable owner to each stage below. You may own technical implementation, but do not assign yourself policy authority that belongs elsewhere.

| Stage | Accountable owner | Why |
|---|---|---|
| Source-data quality | | |
| Warehouse and feature pipeline | | |
| Model validation and deployment | | |
| Decision policy and threshold | | |
| Student intervention | | |
| Appeals and safeguarding | | |

### 6. Decision lineage (12 points)

A teacher asks, "Why was this student flagged at 08:15 on 20 August?" List the minimum lineage needed to reproduce and defend that specific score. Include data, code/model, policy, and human-action evidence.

### 7. Three abstaining LFs (12 points)

Write pseudocode for three labelling functions for `NEEDS_FOLLOW_UP`. Each must emit `1`, `0`, or `ABSTAIN` and use one of these signals:

- poor grades
- repeated absences
- negative academic trend

Avoid making a positive vote the same as proof that intervention is required.

### 8. Gold set (10 points)

Design a 100-example gold set for the attendance-risk use case. Explain:

- who labels it;
- how examples are sampled;
- how disagreement is resolved;
- which split must remain untouched while LFs are developed.

### 9. Coverage and conflict (8 points)

Give one numerical result that would make you distrust the LF set because of low coverage, and one that would make you distrust it because of conflict. Explain why each is a problem.

### 10. Defensible decision (6 points)

In two sentences, distinguish a model-generated risk score from a defensible student-facing decision. Name the human control that must sit between them.

## Score Guide

- **90-100:** Can explain and govern the end-to-end system.
- **75-89:** Core concepts are sound; tighten ownership or lineage.
- **60-74:** Review EGML and Snorkel diagnostics before applying them.
- **Below 60:** Re-read the one-pager, then retake the quiz closed book.
