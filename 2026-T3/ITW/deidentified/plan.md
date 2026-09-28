# DataWrestler — implementation handoff

> **De-identified public copy** for ITW601. People appear by role, the school and its vendor systems by generic names (SIS = student information system, LMS = learning management system). Generated from the private original; do not edit by hand.

- **Identity:** DataWrestler
- **Tagline:** From scattered records to trusted learning insight.
- **Academic home:** ITW601, 2026 Term 3
- **Owner:** Luis Faria
- **Prepared:** 24 September 2026
- **Status:** execution plan for a future implementer; no DataWrestler pipeline has been built by this planning work.

## 1. Mission and product identity

DataWrestler turns fragmented school data into traceable, validated, versioned datasets for staff reporting, exploratory data analysis (EDA) and an offline learning-enhancement ML experiment.

**One challenge across the term:** can we trust the academic data enough to use it consistently, explain how it changed, and assess whether it supports a useful learning-related model?

The relationship between the products is deliberate:

- **DataWrestler:** extraction, retained snapshots, validation, identity mapping, curated history, EDA and experimental dataset creation.
- **Student360:** the existing student-profile interface, consuming approved academic data.
- **The school portal `/admin`:** the intended staff application surface and access boundary.
- **The LMS report server and SIS:** current source systems, reached through approved adapters rather than embedded throughout application code.

The architecture should make replacing a source possible without rewriting the profile interface. Long-term, Luis wants to investigate whether the school portal could also absorb workflows currently performed in LMS. That ambition belongs in a staged source/workflow replacement programme, not in the first extractor release.

### The EigenAI pattern to reuse

The local EigenAI article describes one identity spanning MFA501's four assessment components, with the app implementing the coding case studies (2A, 2B, 3); A1 was a quiz. Reuse the continuity: one question, modular implementation, increasingly strong evidence and a recognizable demonstration. ITW has **three individual reflective journals**, so do not copy EigenAI's assessment structure or pretend a code release replaces a journal.

Use the same title/tagline across the README, architecture diagram, demo cover, release notes and assessment project references. Keep Student360's existing identity on its app. Visual direction: the navy print style used by the school portal, clear process diagrams, source/date labels and real fictional-data screenshots. A logo or mascot is optional later; avoid spending implementation time on branding before the first working data slice.

## 2. Read before implementation

The implementation lives in the school's private workplace repository, next to the existing
ingestion, warehouse and Student360 code. It is not reproduced here. Before any slice, the
implementer reads that repository's agent instructions, inspects the working tree and deployed
baseline, and preserves unrelated work.

Evidence the plan relies on, described by kind rather than path: the academic cohort lineage and
modernisation outcome records (modern academic work already delivered); the hardcoded-values
inventory and the two legacy SSIS packages (embedded rules and table rebuilds); the Year 12 awards
exploration log, runbook and markbook builder (source gaps, chronology and award-policy
discrepancies); Student360's agent guide, academic contracts and audit findings (reuse boundaries);
and the staff-session boundary in the school portal (separate staff role families, staff cookie
restricted to `/admin`). The identity pattern follows the author's EigenAI article.

Static inspection found table deletion/recreation statements, not whole-database deletion. Some source documentation is older than the nightly-job evidence. Inspect runtime schedules before making claims about current execution. Preserve distinctions between observed source code, dated operational evidence and newly verified runtime behaviour.

## 3. Scope this term

**Smallest useful end-to-end delivery:** two approved source adapters → retained runs → validated academic facts → EDA report → existing Student360 academic view → separate offline ML evaluation.

Start with LMS academic results and SIS identity/cohort context. Use synthetic exports first; approved de-identified academic data only where permitted. A controlled markbook adapter is a fallback for an explicit use case, not a backdoor around source visibility decisions.

First cohort, periods, metric definitions, ML question and target remain to be agreed. Do not expand into medical, finance, pastoral notes, raw narratives, broad sensitive demographics or other prototype tabs just because they exist. Operational rank/awards visibility needs its separate rule and access decision.

Do not add live prediction, automatic interventions, source-system writes, a new cloud platform or a full LMS replacement to the term's minimum acceptance criteria.

## 4. Proposed technical shape

Prefer a small Python ingestion/validation package and SQL migrations/views that extend the existing academic model. Keep the UI in the existing TypeScript apps. Confirm versions, dependencies and local instructions at implementation time rather than copying stale setup commands.

Proposed workplace code location: `ssis/datawrestler/` in the workplace repository, unless the repository owner chooses another location after inspecting existing reusable modules. Do not create a second independent warehouse model without documenting why the existing modern contract is insufficient.

```text
datawrestler/
  README.md                 # purpose, run/verify/recovery commands
  pyproject.toml            # pinned/reproducible package configuration
  src/datawrestler/
    adapters/               # source-specific acquisition and parsing
    manifests/              # run metadata and checksums
    validation/             # schemas, domains and quality gates
    identity/               # explicit ID bridge and ambiguity handling
    academic/               # task facts, semester facts, corrections
    eda/                    # coverage and longitudinal quality summaries
    datasets/               # versioned offline experiment exports
  sql/                      # additive migrations and serving contracts
  config/                   # non-secret, versioned field/rule mappings
  tests/fixtures/           # entirely synthetic inputs and expected results
  docs/                     # ADRs, runbook, source inventory, release notes
```

Data storage is outside this source tree. Retain approved raw extracts in school-controlled storage and use the existing SQL warehouse for manifests/validated facts where suitable. Any new storage technology needs a demonstrated requirement.

### Required contracts

| Contract | Minimum information |
|---|---|
| Source inventory | Owner, approved fields, acquisition method, refresh cadence, publication scope, failure/contact path |
| Run manifest | Run ID, source, period/filter scope, observed/extracted times, checksum, schema/config/code versions, row counts, status, parent/previous accepted run |
| Academic identity | Canonical student ID, source ID, effective period, mapping method and ambiguity state; no name-based join |
| Semester fact | Student, subject, school/course year as applicable, reporting period, mark, grade, effort, source run and field state |
| Task fact | Student, course/programme, task, assessment date/window, score/scale/weight, publication/load states and source run |
| Exception | Run, rule, reason, affected key reference stored only in approved storage, resolution status; no raw student payload in general logs |
| Dataset manifest | Input run IDs, cohort/filters, feature/target definitions, de-identification version, split policy, code version and dataset checksum |

Keep school year, course year, year sat and reporting period distinct. Missing is not zero. Task results and semester results are not interchangeable. Never infer complete course coverage from the presence of some rows or a recent job timestamp.

### Refresh lifecycle

`received → validated → staged → accepted → published`, with `failed/quarantined` paths.

Each ingest preserves traceability under an agreed retention policy. Validate before publishing. Repeating the same accepted run must not duplicate facts. A failed or incomplete replacement must leave the previous accepted dataset available and visibly dated. Corrections require a traceable supersession/version policy. Support rollback to an accepted run.

Incremental loading is an optimization only where reliable change/deletion markers exist. Full exports remain valid inputs if safely retained, compared and published. The target is trustworthy updates, not an unsupported promise that every source can provide live deltas.

## 5. Execution backlog and release gates

All items below are future work. Release labels identify reviewable milestones, not versions already shipped.

| ID / proposed release | Work | Dependency | Acceptance evidence |
|---|---|---|---|
| DW-00 / discovery | Inventory runtime sources/jobs, existing modern model, owners and scope; define baseline | Read-first pack | Current-vs-historical source map; approved first cohort and ML question; reuse ADR; no invented runtime facts |
| DW-01 / v0.1 | Create package, synthetic fixtures, versioned mappings and manifest model | DW-00 | One command processes synthetic LMS and SIS inputs with no network/credentials; both sources accounted for |
| DW-02 / v0.2 | Implement adapter boundary, retained-run handling and staging | DW-01 | Checksums/manifests persist; repeat ingest is idempotent; malformed file is quarantined; prior accepted run survives failure |
| DW-03 / v0.3 | Identity bridge, typed semester/task facts and quality rules | DW-02 | Duplicate/ambiguous joins rejected or withheld; grade/effort domains explicit; corrections traceable; no task/semester conflation |
| DW-04 / v0.4 | EDA and coverage report, reproducible dated dataset | DW-03 | Source/year/subject/period coverage, missingness, duplicate/conflict counts and history consistency; exact denominators and exclusions |
| DW-05 / v0.5 | Adapt Student360 academic reads to curated contract; integrate minimal staff route | DW-03 plus app approvals | Browser → authorized staff API → accepted dataset → existing academic view; parity and cross-role/cohort denial evidence |
| DW-06 / v0.6 | Separate award calculation snapshots and rule versions | DW-04 plus the academic stakeholder rules | Accepted reference cases, ties, missing inputs, accelerants/prior-year results, unknown units and snapshot replay; no silent rank on incomplete inputs |
| DW-07 / research milestone | Offline baseline and one candidate ML model | DW-04 plus agreed target/data | Leakage-controlled evaluation, appropriate target-specific metrics, error analysis and dataset/model lineage; no operational intervention |
| DW-08 / term handover | Pilot review, support, rollback and academic evidence | Relevant prior slices | Actual outcomes vs baseline, known limitations, named owner, repeatable runbook and sanitized journal evidence |

DW-05, DW-06 and DW-07 can use the same accepted dataset independently once their prerequisites are met. Their completion order depends on approvals and evidence, not on forcing a single implementation sequence.

For every slice: implement the smallest coherent change, run relevant checks, attach evidence, update the operational release notes and this academic control journal, and present the artifact to Luis. Do not mark a gate passed because documentation was written.

### Required meaningful tests

- Same source content twice: no duplicate facts; run lineage remains inspectable.
- Schema/column drift, malformed marks and incomplete files: fail/quarantine visibly; never publish partial data as complete.
- Duplicate canonical identities, conflicting marks and ambiguous subject mappings: withhold; do not choose arbitrary row order.
- Missing effort, historical scale variation and zero-variance statistics: explicit states and correct handling.
- Course membership, current Y11 accelerants, prior-year completed courses, unknown units and ties: reference cases agreed for each award.
- Failed publish and source outage: previous accepted snapshot retained; freshness is truthful; rollback works.
- Staff reader succeeds; anonymous, parent-only, uniform ordering-only, mandatory data collection-only and out-of-cohort requests fail; no mock bypass in live mode.
- Dataset split and feature timestamps: no student/time overlap that invalidates the evaluation, and no target leakage.

Use existing app-specific required tests when editing either app. Source examples and implementation tests stay synthetic. Live verification requires the approved environment and should record sanitized counts/status, not pupil records.

## 6. ITW assessment story: one project, three reflective stages

| Journal | DataWrestler narrative | Evidence to carry forward |
|---|---|---|
| A1 — 11 October, 500 words ±10% | **Understand the problem:** fragmented sources, manual rules, publication gaps and staff decisions | Organization/team/role, relationships, gathered responsibilities, current flow, proposed foundation; not a product brochure |
| A2 — 15 November, 1,000 words ±10% | **Design and justify the response:** source contracts, inquiry method, governance and staged delivery | Interview preparation, ICT challenges, project synopsis, technical/managerial plan, tools, ethics and actual prototype progress |
| A3 — 2 December, 3,000 words ±10% | **Evaluate the outcome:** reliability, usefulness, learning and limitations | Updated organizational context, positioning, review of A2, critical reflection, actual validation/feedback and offline experiment results |

Use the section allocations and hour requirements in the existing delivery plan. Confirm LMS dates and revised scope with the academic facilitator. Assessment titles and required structures remain those of ITW; DataWrestler is the project identity within them.

Evaluate what was actually achieved. EDA may demonstrate that the data cannot support the proposed target; that is evidence to discuss and a reason to revise the method, not permission to claim successful prediction or intervention effectiveness.

## 7. Longer-term horizon: reduce and potentially replace LMS dependency

**Horizon 1 — independent reporting data.** Keep LMS as an authoritative source while DataWrestler retains approved history, documents lineage and supplies stable reporting contracts. Student360's academic display becomes less tied to a specific report-server report shape.

**Horizon 2 — staff reporting in the school portal.** Move approved reporting/profile workflows to `/admin`, with role/cohort access, audit, freshness and award snapshots. Retire duplicate reports only after parity and owners' acceptance. A consolidated interface alone does not replace the source system.

**Horizon 3 — decide whether to replace operational workflows.** Inventory every LMS capability the school actually uses: candidate categories include markbook entry, assessment setup, report authoring/publication, attendance, pastoral workflows, parent/student access and integrations. These categories require local confirmation. Identify each system of record, responsible staff, policy/retention requirements, migration needs and alternatives; compare benefits and costs before committing.

**Horizon 4 — controlled source migration and retirement, if the school chooses it.** Prove accepted historical migration and ongoing writes, permissions and student/parent experience; run parallel reconciliation; rehearse cutover/rollback; settle archive access and retention; obtain formal operational acceptance before disabling any source job or service.

Do not delete a database, disable LMS, change parent publication, cancel services or turn off legacy jobs under this planning request. Long-term decommissioning requires a separate executable migration plan and specific authorization. This plan authorizes no destructive operation.

## 8. Decisions to settle before dependent work

- The academic stakeholder: first cohort, useful academic questions, metric meanings, award rules and reviewer.
- The ICT sponsor: delivery capacity, owning repository/runtime, source access and staff pilot boundary.
- The academic facilitator: how DataWrestler's foundation plus offline experiment satisfies the approved ML intervention project; interview framing and evidence expectations.
- Data owners: approved extraction fields/method, publication scope, retention, identity mapping and correction authority.
- Luis: first review slice and timing; proposed Wednesday 30–45 minute reviews are availability, not booked meetings.

Independent synthetic scaffolding and source inventory can proceed while these questions remain open. Do not block all progress on decisions unrelated to the current slice.

## 9. First session for the next implementer

- [ ] Read local instructions, control journal and evidence references; check working trees.
- [ ] Confirm no newer runtime/source findings supersede this plan.
- [ ] Produce a concise reuse map of existing academic model, adapters, SQL contracts and tests.
- [ ] Turn DW-00/DW-01 into small tasks with exact owning paths and acceptance checks.
- [ ] Record unresolved business decisions without inventing answers.
- [ ] Prepare the synthetic two-source example and run-manifest contract.
- [ ] Present the first review artifact to Luis; record actual session changes and checks.

**First delivery to review:** a source inventory + reuse decision + runnable synthetic extraction/manifest example. The existing app screenshots remain the product demonstration; new screenshots should show a concrete data-quality or profile improvement.

**Handoff prompt:** “Implement DataWrestler incrementally from this plan. Start with DW-00 and DW-01, reuse the existing modern academic foundation, use synthetic fixtures, and preserve the current applications. Verify each slice and update the owning backlog/release notes plus the ITW control journal. Do not infer deployment, sensitive-data access or decommissioning authorization.”

## 10. Expanded vision — a modular school platform

**Luis's direction, 24 September 2026:** progressively replace the whole SIS user interface and the LMS workflows with a unified experience in the school portal, then evaluate retirement of underlying vendor dependencies where the replacement is complete. Near-term ambition is to expand the interface; dates and full replacement feasibility are not yet established.

### Product responsibilities

- **The school portal:** one modular experience for parents, operational administrators, academic staff and other approved school roles.
- **Student360:** the student/family-centred view connecting academic progress and approved operational context.
- **DataWrestler:** source adapters, canonical identity, retained history, quality, lineage, datasets and source-independent read contracts.
- **Domain services:** validated commands, workflow state, approvals, audit and integration for operations such as attendance marking, grade publication, billing and rollover. These are additional capabilities; an EDA extractor does not implement them.

“Plug in” means explicit module contracts: navigation, role/cohort permissions, read APIs, command APIs where needed, domain events, ownership and validation. Avoid a generic database editor or an unrestricted student/family payload shared across every role.

### Capability-by-capability roadmap

| Capability | Starting position | Next bounded slice | Evidence before replacing the incumbent workflow |
|---|---|---|---|
| Parent access and forms | The school portal exists; current deployment details require verification | Unified form status, receipts and approved family information | Correct family authorization, submission history and correction handling |
| Administrative review | Mandatory data collection and uniform ordering are existing patterns | Reusable form review workspace with domain-specific permissions | Complete received/reviewed/applied lifecycle; no cross-module privilege leakage |
| Student academic progress | Student360 prototype and modern academic foundation exist | Governed academic profile within the school portal | Accepted source parity, freshness, coverage and role/cohort checks |
| Attendance | Future operational module, not part of the delivered profile | Teacher-owned roll marking for an agreed pilot context | Valid enrolment/session roster, correction audit, authorized write path and reconciliation |
| Assessment / markbook / grade release | LMS currently supplies relevant data/workflows | Separate assessment entry, moderation and publication workflow discovery | Correct calculations, teacher permissions, publication controls and complete history |
| Student/family administration | SIS remains a source of identity/context | Replace one staff screen through a supported read/command contract | Identity/relationship integrity and controlled corrections; system of record remains explicit |
| Finance | Existing gated prototype context is not a replacement ledger | Discover balances, charges, statements, payments and reconciliation separately | Opening/closing balances, transaction audit, reconciliation, period controls and recovery |
| Timetable | Existing read slices are a starting point | Validated timetable display before scheduling/editing | Staff/student/resource constraints, calendar alignment and accepted changes |
| Term/year rollover | Future operational capability | Model and rehearse one rollover in an isolated environment | Enrolment, curriculum, timetable and financial-period consistency; rollback and audit |
| Vendor retirement | Strategic option, not an authorized action | Capability inventory, dependency map and migration proposal | Complete accepted coverage, historical access, parallel run, recovery, ownership and explicit cutover decision |

### Replacement ladder

1. **Observe:** inventory a workflow, its source of truth, users, inputs, outputs and dependencies.
2. **Read:** present trusted information in the school portal while the incumbent remains authoritative.
3. **Act:** introduce a controlled workflow backed by an approved integration, with commands and audit separate from analytical reads.
4. **Own:** after domain parity and migration, move that capability's authoritative records into the replacement service if the school chooses.
5. **Retire:** remove the redundant screen/integration/service only when the dependent capability is accepted and recoverable.

At every stage, declare which system owns each field and transaction. Avoid uncontrolled dual writes. Plan idempotent commands, retries, conflict handling and reconciliation before allowing edits across systems. Preserve source identifiers through migration.

This is the long-term architecture direction, not an expansion of the ITW minimum scope. The term's two-source ingestion, EDA, Student360 academic slice and offline ML experiment are the first coherent part of it. Keep operational module delivery incremental and review one visible outcome at a time.
