# DLE602 Assessment 2 - Project Tracker

**Project:** Review Pulse v2 - Aspect-Based Sentiment Analysis  
**Group:** Luis, Victor and Juan  
**A2 due:** Sunday 26 July 2026, 11:55pm AEST  
**A2 deliverables:** 1,000-word proposal report, PDF slides and a 5-7 minute recorded presentation  
**A3 outcome:** implement and evaluate the proposed system

## Current status

| Workstream | Status | Evidence / next action |
|---|---|---|
| Topic and problem | Drafted | Confirm group agreement on ABSA and the core scope |
| Literature | Drafted | Convert the paper list into a critical comparison matrix |
| Method | Drafted | Tighten the model ladder, RQs and evaluation design |
| Project management | Partial | Complete owner-level tasks, risks, contingencies and milestones |
| Report | v1 drafted | Revise, format and validate against the rubric |
| Presentation | Outline drafted | Build six visual slides, scripts and recording |
| Team details | Blocked | Add Victor and Juan's surnames and student IDs |

## Scope decision

The core A3 task is **aspect sentiment classification given gold aspect terms** from SemEval-2014. Aspect extraction, Topic Modelling and cross-domain transfer are stretch goals. They must not delay the core comparison.

## How this becomes Review Pulse v2

Review Pulse v1 already demonstrated the engineering path for sentence-level sentiment using TF-IDF, BiLSTM + GloVe and a fine-tuned BERT model. Review Pulse v2 retains useful implementation patterns such as preprocessing, experiment tracking, metrics and the Streamlit interface, but changes the prediction unit:

`review -> one sentiment label` becomes `(review, aspect) -> one sentiment label per aspect`.

The A2 proposal specifies this architecture. A3 performs the implementation, model training, evaluation and demo integration.

## Experimental ladder for A3

| Stage | Model | Purpose |
|---|---|---|
| 0 | Review Pulse v1 results | Historical sentence-level reference and reusable engineering foundation |
| 1 | TF-IDF + logistic regression, sentence only | Sanity baseline; it must assign the same prediction to every aspect in a sentence |
| 2 | Target-agnostic LSTM, sentence only | Isolates whether recurrence alone solves the problem |
| 3 | ATAE-LSTM, sentence + aspect | Tests the value of explicit aspect conditioning and attention |
| 4 | DistilBERT sentence-pair, sentence + aspect | Tests contextual transfer learning against the LSTM models |
| 5 | Attention or attribution visualisation | Provides qualitative interpretation; faithfulness is claimed only if perturbation tests are added |

Core evaluation: accuracy, macro-F1, per-class precision/recall/F1, confusion matrices and performance on sentences containing aspects with conflicting sentiment.

## Timeline

### 4-10 July - align and prove feasibility

- [ ] All - confirm topic, core scope and proposed roles by 6 July
- [ ] Victor and Juan - provide official surname and student ID by 6 July
- [ ] Luis - audit SemEval files, exact split sizes, labels and conflicting-sentiment examples by 8 July
- [ ] Victor - complete the literature comparison matrix and 150-word critical synthesis by 9 July
- [ ] Juan - complete the milestone table, five-item risk register and contingencies by 9 July
- [ ] All - 15-minute review of the complete material by 10 July

### 11-17 July - produce report v2 and slide draft

- [ ] Luis - integrate the technical sections and architecture figure
- [ ] Victor - verify every literature claim and APA reference
- [ ] Juan - assemble cover, table of contents, project plan, risk table and submission checklist
- [ ] All - review the report against the five rubric criteria
- [ ] All - produce the first six-slide deck and speaking notes

### 18-23 July - finalise and rehearse

- [ ] Cut the report to 900-1,100 words and confirm the declared count
- [ ] Render and visually inspect the report and slide PDFs
- [ ] Rehearse the 5-7 minute presentation with approximately equal speaking time
- [ ] Record a complete draft and correct timing, audio or transition issues
- [ ] Perform final APA, spelling and academic-integrity checks

### 24-26 July - submission buffer

- [ ] Confirm all names, IDs, filenames and required formats
- [ ] Watch the final recording from beginning to end
- [ ] Submit one complete group package before 11:55pm AEST on 26 July

## Proposed small-task division

### Luis - technical integration

1. Validate the SemEval dataset and produce a one-page data audit.
2. Finalise the measurable research questions and fair model comparison.
3. Draw the Review Pulse v1 -> v2 architecture and integrate all sections.
4. Prepare the A3 repository structure and minimal data-loading spike after the A2 scope is approved.

### Victor - literature evidence

1. Read Pontiki et al. (2014), Wang et al. (2016) and one 2024 review/comparison paper.
2. Add each paper's task, dataset, model, result, limitation and relevance to a comparison matrix.
3. Rewrite one literature paragraph as critical synthesis rather than a list of papers.
4. Validate the reference list and in-text citations.

### Juan - project management and submission

1. Convert the timeline into a compact Gantt figure.
2. Create a five-item risk register with likelihood, impact, mitigation and contingency.
3. Maintain the report/presentation completion checklist.
4. Check cover details, word count, page numbers, captions and final filenames.

### Shared work

- Review one another's sections rather than only reviewing personal work.
- Build and rehearse the presentation together.
- Keep approximately equal speaking time and visible contribution evidence.

## Decisions log

| Decision | Status | Rationale |
|---|---|---|
| Core task is ATSC with gold aspects | Proposed | Feasible and directly measurable for A3 |
| Restaurants is the primary SemEval domain | Proposed | Strong customer-experience fit; Laptops can be secondary |
| Topic Modelling is stretch scope | Proposed | Useful for aspect discovery but not required for gold-aspect classification |
| Attention is indicative, not automatically causal | Accepted in draft | Avoids an unsupported faithfulness claim |
| Equal presentation time | Required | Explicit A2 brief requirement |

## Follow-up message for the group

> Hey Victor and Juan - quick follow-up on the Review Pulse v2 idea I sent on Wednesday. With A1 now behind us, I have turned the idea into a small proposed plan so we can decide quickly without creating a large workload for anyone.
>
> The core proposal is aspect-based sentiment analysis on SemEval-2014: compare a sentence-level baseline, an aspect-aware attention LSTM and DistilBERT, then implement it as Review Pulse v2 for A3. Topic Modelling stays optional so the scope remains realistic.
>
> Could you please send me by Monday: (1) whether you are happy with the topic, (2) your surname and student ID, and (3) whether you prefer literature or project-planning tasks? I have split the first work into small pieces: roughly three papers plus a short comparison for literature, or a timeline plus five project risks for planning. I will handle dataset validation, methods and integration.
>
> If either of you has a different project direction, send it through as well. The immediate goal is simply to lock the topic and roles, then we can work asynchronously and keep the presentation time equal.

