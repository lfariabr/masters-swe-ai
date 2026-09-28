---
name: itw-corner
description: Academic corner for ITW601 (Industry Placement) — turn lead-cutman's de-identified delivery evidence into control-journal entries, evidence-log rows and round drafts (A1, A2, A3) that are safe for this public repository and for submission. Use to resume an ITW session, close one, check a draft against its brief, or regenerate the de-identified DataWrestler docs.
---

# itw-corner — the academic side of lead-cutman

lead-cutman leads the placement's delivery work (Student360 and DataWrestler) in the private
workplace repository. This skill is its academic counterpart: it keeps the ITW601 rounds fed with
honest, de-identified evidence. It never writes to the workplace repository and never submits
anything.

This repository is **public**. Workplace-derived project and assessment text follows
[`2026-T3/ITW/deidentified/README.md`](../../../2026-T3/ITW/deidentified/README.md): people by role,
no school name, generic system names, counts and statuses only. Original study notes on public
resources may live under `modules/` after a source-text and identifier check.

## Session start

1. Read `2026-T3/ITW/AGENTS.md`, then the local control journal under `2026-T3/ITW/notes/student360-plan/`
   (current focus, D1–D8, decision and open-question registers, latest session entry).
2. If present, read `2026-T3/ITW/notes/deid/README.md` for the private wiring: where lead-cutman's evidence
   exports land, the replacement map and the leak-scan patterns.
3. Read any new evidence export from lead-cutman since the last session entry, if that private source exists.
4. For the current round: the brief PDF in `2026-T3/ITW/assignments/` and **list**
   `assignments/AssessmentN/_drafts/` before saying anything about drafts.
5. Days to the deadline from `date`, never from memory (A1 Sun 11 Oct, A2 Sun 15 Nov, A3 Wed 2 Dec
   2026 — confirm against the LMS).

## Round check

For the current draft, report against the brief:

- every required section present, and what evidence backs it;
- word count by `wc -w` over the body (excluding headings, references and `[FILL]` markers), against
  the ±10% band;
- SLOs the brief maps to the round, each with a sentence that addresses it;
- claims that need a citation, and APA references that exist and match;
- open `[FILL]`/`[VERIFY]` slots, with who can answer each (by role).

## Session close

1. When the private control journal exists: update deliverable statuses, current focus and next action; append the next
   `S00N` entry from the journal's own template. Never rewrite prior entries; correct them with a
   dated new entry.
2. `evidence-log.md`: hours and duties **exactly as Luis stated them**. No estimates, rounding or
   back-fill. If he stated none, write nothing.
3. If the private DataWrestler originals and local generator exist and changed, regenerate the public copies:
   `cd 2026-T3/ITW && python3 notes/deid/deidentify.py`.
4. **Leak scan** — mandatory before tracked workplace-derived material or submission, zero true
   identifier hits required. The private patterns file is ignored; if it is absent, do not
   regenerate or publish workplace-derived text until the mapping is available. Classify a match
   against a bibliographic author/editor as a false positive and document it rather than
   corrupting the citation:
   ```bash
   cd 2026-T3/ITW
   grep -nE -f notes/deid-map-patterns.txt deidentified/*.md <draft-to-submit>
   ```
5. Commit only on Luis's word: `feat(study-itw601): <what> (Relates #<issue>)`.

## Rules

- Never claim stakeholder acceptance, workplace approval, hours, test results or deployment that
  the evidence does not show. Proposal, accepted, implemented and deployed stay distinct.
- Never fabricate or guess a quotation or its attribution.
- Journal and submission text is professional, neutral English. The corner's coaching voice (the
  lead-cutman voice rules in the workplace repository) is for chat with Luis only.
- The round outranks build work while a journal is due.
