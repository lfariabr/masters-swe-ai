# DataWrestler: current data flow and proposed ML foundation

> **De-identified public copy** for ITW601. People appear by role, the school and its vendor systems by generic names (SIS = student information system, LMS = learning management system). Generated from the private original; do not edit by hand.

Planning synthesis, 24 September 2026. Execution handoff: [plan.md](plan.md). Companion: printable flow sheet. This proposal extends the ITW plan; it does not claim a deployed multi-source platform or changed placement approval.

## The project proposition

**A multi-source extraction and data-quality pipeline for longitudinal academic analysis, supplying Student360 and an offline learning-enhancement experiment.**

Extraction acquires the data. EDA examines its quality, coverage, distributions and relationships. Keep these as explicit stages: an extractor alone does not establish that data is reliable or suitable for ML. Student360 becomes a consumer of a trusted academic dataset, rather than a second place to recalculate inconsistent exports.

## Current academic flow — evidence and boundaries

1. **LMS → the report server → scheduled CSV exports → file landing → SSIS warehouse staging.** Source report/domain selection limits what reaches the files. The July lineage identifies scheduled and manually filtered per-term export paths. The March architecture records a 14-file set; this is a historical inventory, not a confirmed count of today's live schedules.
2. **Legacy SSIS transformation → reporting tables → Power BI / Excel.** Selected staging data is cleared, and many intermediate/output tables are dropped and recreated. Year suffixes, year filters, report-type text and other mappings are embedded in package SQL.
3. **SIS identity and context are joined through the academic identity bridge.** The July lineage retains the legacy student bridge and subject-membership inputs. This evidence does not establish every upstream SIS-to-LMS synchronization or its current timing; diagram only the reporting relationships we can support.
4. **A modern academic lane already exists.** July work introduced typed raw report results, protected accepted history, audited historical recovery, a controlled academic model and a stable consumer contract. It still depends on selected legacy identity/subject inputs. This is an existing foundation to extend, not a proposed clean-sheet rebuild.
5. **The source completeness problem remains separate.** September investigation found hidden Trial marks absent from the warehouse after refresh. Freshness and completeness must both be measured. The markbook fallback preserves source-provided cumulative figures for that workflow.

### What “delete everything daily” can accurately mean here

Read-only inspection of `SqlStatementSource` attributes in the two versioned packages, with SQL comments removed, found:

| Package | DROP TABLE statements | DELETE FROM statements | DROP DATABASE statements |
|---|---:|---:|---:|
| `the source-to-warehouse load package` | 22 | 26 | 0 |
| `the academic-analysis transformation package` | 106 | 0 | 0 |

These are static statement counts, not distinct tables or observed execution counts. Some DELETE statements are filtered cleanup. They do not prove every task executes nightly or that the whole warehouse is erased. No package was executed for this review.

The 28 August source investigation records nightly landing and fresh staging output. Its 4 September correction says legacy job retirement was not established and the current step state must be checked. March documentation describing semester reporting must not be used to infer that ingestion runs only twice per year.

**Meeting wording:** “The legacy reporting pipeline repeatedly reloads source extracts and rebuilds reporting tables. Important year, period and mapping rules are embedded in the jobs. We need retained, traceable data so a refresh does not become our only record of what the report previously showed.”

Downloading everything again, clearing a landing table and rebuilding derived data are different operations. Confirm the actual report-server scheduling/downloader configuration, file replacement behaviour, task dependencies and recovery behaviour before redesigning those operations. Do not claim the two package files prove all of that.

## Proposed pipeline: acquire → retain → validate → analyse → serve

| Stage | Proposed responsibility | Concrete output / acceptance |
|---|---|---|
| Source adapters | Read approved LMS exports and SIS academic identity/context; retain a controlled markbook-file adapter where needed | Source owner, fields, extraction method and cadence documented; source publication scope retained |
| Landing and run register | Save each permitted extract with source/period/run ID, observation time, extraction time, schema version, row count and checksum | A rerun is recognizable; previous accepted snapshots are not silently replaced; failed/partial loads do not become current |
| Typed validation | Validate types, missingness, domains, duplicate keys, course membership and identity joins | Exception/quarantine output; accepted records separated from ambiguous ones; no student-name joins |
| Curated academic history | Store facts at explicit student × subject/course × task or reporting-period grain | Task and semester facts remain distinct; corrections are traceable; published/marked/loaded states remain distinct |
| EDA output | Summarize coverage by source/year/subject/period, missingness, duplicate rates, distributions and longitudinal consistency | Reproducible data-quality report with denominators and visible exclusions; no claims of causation from associations |
| Dataset snapshots | Build versioned features and an agreed target from accepted facts | Lineage to inputs; approved de-identification; no future-information leakage; repeatable student/time split |
| Consumers | Serve approved academic views to Student360 and frozen award-review snapshots; separately run offline ML evaluation | Same metric definitions across views; reproducible award dataset; model results remain experimental |

**Storage direction:** extend the existing SQL warehouse and approved school file storage rather than selecting new cloud infrastructure now. Separate raw extracts, validated facts, derived measures and experimental datasets logically and by permissions. Raw retention needs an agreed duration and deletion process; “append-only” does not mean keeping identifiable records forever. Keep large snapshots, pupil data and model outputs outside Git and outside the university repository.

Use incremental extraction only if the source supports a reliable change marker and correction/deletion semantics. Where it does not, a full extract can still be retained and compared safely, validated, then published as a new accepted snapshot. Do not promise that replacing SSIS alone removes source/report limitations.

## A feasible ITW slice

1. Inventory two source families: LMS academic results and SIS student/cohort identity. Use existing permitted exports and the modern academic contract; no unsupported API assumption.
2. Demonstrate one reporting period and one agreed cohort, including two dated source snapshots where available. Use synthetic fixtures or approved de-identified inputs for academic artifacts.
3. Produce a run manifest, typed academic dataset, exception report and EDA report. Prove reruns do not double-count, ambiguous joins are quarantined, and a failed run preserves the last accepted dataset.
4. Feed the existing Student360 academic adapter with the approved curated shape. Reconcile against the accepted report before adding fresher calculations.
5. With the academic facilitator, define a learning-related question and target. Compare a simple baseline with one offline candidate model using suitable data and a split that prevents leakage. If target labels are inadequate, document that limitation rather than inventing intervention effectiveness.

This is how the infrastructure work can support the approved ML direction. An EDA pipeline alone does not establish that the ML placement objective is satisfied; confirm the revised framing with the academic facilitator. The operational pilot remains read-only and carries no automated intervention decision.

## Proposed Wednesday checkpoints

| Checkpoint | Artifact to review | Decision |
|---|---|---|
| 1 | Current source map and first-profile screens | First cohort, academic question and useful metrics |
| 2 | Extract manifest and coverage/exception report | Trusted sources and acceptable missingness |
| 3 | Versioned academic history and Student360 view | Result parity and practical usefulness |
| 4 | EDA findings and offline experiment design | Whether available data supports the agreed target |
| Later | Pilot/evaluation results | What to retain, improve or defer |

Sequence is proposed, not a scheduled commitment or guarantee of one-week completion. Luis is available Wednesdays for 30–45 minutes; stakeholder attendance is pending.

## Evidence references

The evidence sits in the school's private workplace repository and is described here by kind only:
the two legacy SSIS packages (SQL attributes inspected, not executed); the hardcoded-values
inventory; the March legacy architecture and its historical 14-file inventory; the academic cohort
lineage; the July modernisation outcome; the Year 12 awards exploration log (August nightly evidence
and the September correction on job retirement); and the Year 12 reporting runbook (September
source-coverage corrections and markbook fallback).

## Broader platform direction

DataWrestler is the shared data foundation for a modular school-portal platform. The wider ambition includes replacing SIS screens and LMS workflows progressively, covering parent forms, staff review, academic progress, attendance, grade release, administration, finance, timetable and rollover. See [plan.md](plan.md), section 10, for the capability roadmap and the distinction between replacing a screen, owning an operational workflow and retiring its source system.
