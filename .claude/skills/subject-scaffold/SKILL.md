---
name: subject-scaffold
description: Scaffold or refresh a subject README from local university subject notes, outline PDFs, planner PDFs, assessment briefs, and existing README placeholders. Use when asked to update a term subject README with notes contents, populate SLOs, delivery schedules, module names, assessment details, source-note links, or a new subject overview.
---

# Subject Scaffold

Use this skill to turn a subject folder's local academic documents into a useful subject README while preserving the repository's existing study-tracking style.

## Workflow

1. Resolve the target subject directory from the user request.
   - Typical path: `<term>/<subject>/`, such as `2026-T2/BDA/`.
   - Read the existing `<subject>/README.md` first.
   - Inspect `<subject>/notes/` and `<subject>/assignments/` with `rg --files` or `find`.

2. Extract source content.
   - For PDFs, prefer:
     ```bash
     pdftotext -layout path/to/file.pdf -
     ```
   - If `pdftotext` is unavailable, tell the user to install poppler and stop before guessing.
   - Prioritise subject outline and subject planner files for canonical SLOs, schedule, workload, prerequisites, facilitator, assessment weights, and module names.
   - Use assessment briefs for specific deliverable names, due dates, requirements, and rubric detail when present.

3. Build the README from source facts only.
   - Keep the existing title and overall section order where it already matches nearby subject READMEs.
   - Fill or update these sections when source material supports them:
     - `Subject Introduction`
     - `Subject Details`
     - `Subject Learning Outcomes (SLO)`
     - `Delivery Schedule`
     - `Learning Facilitator`
     - `Modules`
     - `Assignments`
     - `Source Notes`
   - Preserve any existing manual statuses, grades, deadlines, and topics unless the source documents clearly supersede them.
   - If source documents give only "Week 4" or "Module 4" for an assessment, keep any existing calendar deadline from the README instead of replacing it with a vague due marker.

4. Match repository conventions.
   - Use existing status markers: `✅` done, `🔥` WIP, `🕐` not started, `🔌` discontinued.
   - Use module checklists like:
     ```markdown
     - [ ] Module 1 🕐 - Module Title
     ```
   - Use schedule tables like the CCF and ISY READMEs:
     ```markdown
     | Week | Module | Learning Activities | Assessment Progression & Due Date | SLOs addressed |
     ```
   - Format SLO references as backticked labels, for example `` `a)` ``.
   - Link local notes with relative markdown links. Encode spaces as `%20` in PDF links.
   - Prefer ASCII punctuation in edited text unless the surrounding file already uses a specific character.

5. Handle source inconsistencies explicitly.
   - If a planner has a numbering typo, infer only when the sequence is obvious, then mention it in the final response.
   - If outline and planner disagree, prefer the more specific/current document and preserve a note in the final response.
   - Do not invent module titles, learning outcomes, assessment topics, grades, or dates.

6. Edit and verify.
   - Use `apply_patch` for README edits.
   - Verify with:
     ```bash
     sed -n '1,260p' <subject>/README.md
     git diff -- <subject>/README.md
     git status --short <subject>/README.md
     ```
   - In the final response, summarise changed sections and call out any assumptions or source quirks.
