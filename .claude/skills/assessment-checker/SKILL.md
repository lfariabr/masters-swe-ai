---
name: assessment-checker
description: Run an automated pre-submission check on an academic assessment report. Verifies structural compliance with the brief, checks citation consistency, and spot-checks references via web search.
argument-hint: "<SUBJECT_CODE> <ASSESSMENT_NUMBER>"
disable-model-invocation: true
---

# Skill: assessment-checker

## Invocation

`/assessment-check <SUBJECT_CODE> <ASSESSMENT_NUMBER>`

Examples:
- `/assessment-check ISY 1`
- `/assessment-check CCF 2`

Arguments:
- `$0` = subject code (e.g. `ISY`, `CCF`)
- `$1` = assessment number (e.g. `1`, `2`)

---

## Instructions

You are running an automated pre-submission check on an academic assessment report. Follow **all 5 steps** in order. Output a final structured markdown report at the end.

---

### Step 1 — Resolve and Read Files

**Find the subject directory:**
1. Glob `*/*/README.md` and read each to grep for `$0` (case-insensitive subject code match). The parent directory of the matching README is the subject dir (e.g. `2026-T1/ISY`).
2. Fallback: Glob `*/$0*/` then `*/$0[0-9]*/` to find a matching subject directory.
3. If no subject directory is found, print an error and stop:
   ```
   ❌ Could not find a subject directory matching "$0". Check the subject code and try again.
   ```

**Find the assessment directory:**
- Path: `<subject-dir>/assignments/Assessment<$1>/`
- If not found, print an error and stop.

**Find the brief file:**
- Glob `<assessment-dir>/*Assessment<$1>.md` — match files that do NOT contain `_Report_Skeleton` or `_Skeleton`.
- If not found, note "brief not found" and skip brief-dependent checks (structural compliance, rubric).

**Find the skeleton file:**
- Glob `<assessment-dir>/*Assessment<$1>*Skeleton*.md` or `<assessment-dir>/*Assessment<$1>*Report*.md`.
- If not found, print an error and stop.

**Read both files** into memory for the steps below.

---

### Step 2 — Structural Compliance

Using the brief (if found):
- Extract the list of required report sections from the brief.
- Compare against the headings present in the skeleton.
- Flag any required sections that are missing or significantly misnamed.

Word count:
- Count words in the skeleton's **assessable content only**: exclude front matter, appendices, working notes sections (e.g. sections marked "Working Notes", "Checklist", "Rubric Alignment", "AI Usage Declaration").
- Check against the brief's stated word limit (or ±10% tolerance if a target is given).
- Report: `NNN words — PASS / WARN (within tolerance) / FAIL`.

---

### Step 3 — Citation Consistency Audit

1. **Extract inline citations** from body text using the pattern `(Author[s], Year)` or `(Author et al., Year)`. Include all parenthetical author-year pairs.
2. **Extract reference list entries** — typically numbered or bulleted lines in a `## References` section, each containing an author name and 4-digit year.
3. **Cross-check:**
   - For each unique inline citation `(Author, Year)`, verify there is a matching reference list entry with the same first author surname and year.
   - For each reference list entry, verify there is at least one matching inline citation.
4. Report:
   - (a) Inline citations with **no** reference entry (orphaned citations)
   - (b) Reference entries with **no** inline citation (unused references)

---

### Step 4 — Reference Spot-Check (Web Verification)

For **each reference** in the reference list:
1. Web-search: `"<FirstAuthorSurname>" "<Title keywords>" "<Year>" site:scholar.google.com OR site:arxiv.org OR site:aclanthology.org OR site:pubmed.ncbi.nlm.nih.gov`
2. Verify: author names (especially full author list), publication year, journal/venue, volume/pages if listed.
3. Assign severity:
   - 🔴 **Critical** — wrong first author, wrong year, paper does not appear to exist under this title
   - 🟡 **Minor** — author list incomplete/reordered, minor phrasing in title, page numbers off
   - ✅ **Verified** — all key fields match a credible source

Focus spot-check effort on references with full author lists (most likely to contain errors). Statistical spot-check is acceptable for long reference lists (>10 entries): verify all, flag any with issues.

---

### Step 5 — Output Report

Print the following structured report:

```markdown
## Assessment Check: <Subject> Assessment <N>

**Files checked:**
- Brief: `<path or "not found">`
- Skeleton: `<path>`

---

### Structural Compliance      [PASS / FAIL / SKIPPED — no brief]

| Required Section | Found in Skeleton |
|------------------|-------------------|
| <section>        | ✅ / ❌           |
...

---

### Word Count                 [NNN words — PASS / WARN / FAIL]

Assessable content: NNN words
Limit: NNN words (±10% = NNN–NNN)

---

### Citation Consistency       [N issues / PASS]

**Orphaned inline citations (no reference entry):**
- (Author, Year) — ...

**Unused references (no inline citation):**
- Author (Year). Title...

---

### Reference Spot-Check       [N issues / PASS]

| # | Reference | Status | Notes |
|---|-----------|--------|-------|
| 1 | Author (Year)... | ✅ Verified | — |
| 2 | Author (Year)... | 🟡 Minor | Author list differs: ... |
| 3 | Author (Year)... | 🔴 Critical | ... |
...

---

### Rubric Coverage            [SKIPPED — no brief / table below]

| Criterion | Weight | Covered in Skeleton |
|-----------|--------|---------------------|
| <criterion> | N% | ✅ / ❌ / ⚠️ Partial |
...

---

### Issues Summary

The following issues require action before submission:

1. 🔴 [Critical] <issue description> — fix: <suggestion>
2. 🟡 [Minor] <issue description> — fix: <suggestion>
...

_(No issues found — report appears ready for submission.)_  ← use this line if no issues
```

---

## Notes for the Agent

- Always run all 5 steps even if some have nothing to report — output the section with "PASS" or "No issues found."
- Web verification (Step 4) is mandatory — do not skip it.
- If the brief file is not found, mark brief-dependent checks (Structural Compliance, Rubric Coverage) as SKIPPED, but still run Steps 3 and 4.
- The word count must exclude non-assessable boilerplate — check for headings like "Working Notes", "AI Usage", "Checklist", "Rubric" to identify exclusion zones.
- Keep the final report concise. Avoid restating the full text of references or lengthy explanations — one line per finding is sufficient.
