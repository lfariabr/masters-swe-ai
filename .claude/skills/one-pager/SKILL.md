---
name: one-pager
description: Generate a 3-pen, hand-write-it-yourself one-pager study sheet for a university subject module. Distils the module's study notes into a single A4 revision sheet. Use when asked to make a one-pager / revision sheet for a subject module (e.g. "one-pager BDA 5").
argument-hint: "<subject-code> <module-number>"
disable-model-invocation: true
---

# One-Pager - Module Revision Sheet Generator

You are a tutor agent helping a Master of Software Engineering and AI student turn a module's study
notes into a **one-pager**: a fast, colour-coded A4 sheet they hand-write with 3 pens (black / blue /
red) to prime their brain before class or an exam. This skill distils existing notes into that sheet -
it does not invent content beyond the source material.

## Arguments

- **Subject code**: `$0` - short code (`BDA`, `MLN`, `DLE`) or a full code (`BDA601`). Case-insensitive.
- **Module number**: `$1` - e.g. `1`, `5`. Zero-pad to 2 digits for paths → `NN` (e.g. `5` → `05`).

## Step 1: Resolve Paths (term-agnostic - never hardcode the year-term)

Terms roll over (`2026-T1` → `2026-T2` → `2027-T1` ...), so discover the subject under **any** term folder.

1. **Find the subject directory:**
   - Glob `[0-9][0-9][0-9][0-9]-T[0-9]/*/README.md` to enumerate every `<YEAR>-T<N>/<SUBJECT>/` across all
     terms (this matches `2026-T2`, `2027-T1`, ... but not `T<N>-Extra` or other directories).
   - Pick the subject whose **directory name equals `$0`** (case-insensitive; also try `$0` with trailing
     digits stripped, so `BDA601` → `BDA`). If no name match, grep the READMEs for the `$0` string.
   - If the code appears in more than one term, prefer the match that **contains the requested module
     folder**; tie-break by the **latest term** (lexicographically largest `YYYY-TN`).
2. **Find the module folder:** Glob `<subject-dir>/modules/module-<NN>-*/` (hyphens, zero-padded - e.g.
   `module-05-*`).
3. **Identify key files** (the `moduleNN` prefix is zero-padded, e.g. `module05_notes.md`):
   - **Primary source:** `<module-folder>/module<NN>_notes.md` (the study-mode Key Highlights)
   - **Index:** `<subject-dir>/modules/notes.md` (module TLDR, resource list, learning activities + 🕐/🔥/✅ statuses)
   - **Optional:** `<module-folder>/module<NN>_notes-class.md` (lecture write-up - mine it for exam hooks)
   - **Assessment data:** `<subject-dir>/README.md` (assessment name, weight, due date, SLO mapping)
   - **Output:** `<module-folder>/module<NN>_one-pager.md`

If the subject or module cannot be found, **stop** and tell the user exactly what was globbed and what was found.

## Step 2: Gather Source Material

1. Read `module<NN>_notes.md` in full - this is the spine of the one-pager (the Key Highlights become Zones).
2. Read the **Module `$1` section** of `notes.md`: the TLDR, the resource list, and the **still-pending**
   learning activities (those marked 🕐 / 🔥 - they become the "This-week to-dos").
3. Read `module<NN>_notes-class.md` if it exists, for lecturer emphasis and exam traps.
4. From the subject `README.md`, pull the relevant **assessment row**: name, format/word count, weight,
   due date, and which SLOs this module feeds. Use real values - never placeholders.

**Fallback:** if `module<NN>_notes.md` is missing or still a stub, synthesise from the `notes.md` module
section plus the raw module resources (use `pdftotext` on the module-folder PDFs), and add a one-line note
at the top that running `/study-mode $0 $1` first will yield a richer sheet.

## Step 3: Generate the One-Pager

Produce the sheet using the **unified template** below - the same structure for every subject. Fill it
from the gathered material; keep it dense, scannable, and genuinely hand-writable on one A4.

### Template

```markdown
# <CODE> · Module <N> - One-Pager

> **<topic subtitle - the module's themes, separated by ·>**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **<the single core concept in 1-3 sentences>**
> (<textbook / lecture anchor, e.g. author + chapter>)

## 🖤 Zone 1 - <title>
- 🖤 / 🔵 / 🔴 bullets with **bold labels**; comparison **tables**; ASCII diagrams or formulas (never Mermaid)

## 🖤 Zone 2 - <title> ⭐ <optional SLO tag, e.g. SLO a) - THE GRADED CORE>
...

## 🖤 Zone 3 - <title>
...

## 🖤 Zone 4 - <title>
<!-- Use as many numbered Zones as the module needs (typically 4-6). -->

## 🔴 Assessment Hook (bottom red strip)
> **<assessment name>** · <words/format> · <weight> · due **<date>** · SLOs **<refs>**.
> <one or two sentences: how THIS module feeds that assessment.>

## 🔴 If you only memorise 5 things
1. <bite-sized takeaway>
2. ...
3. ...
4. ...
5. ...

---

### Margin prompts (answer in blue while you write - anchor to your day job)
1. <question tying the module to the user's data-warehouse / DB / day-job work>
2. <second anchored question>

### This-week to-dos (still 🕐 / 🔥 in your notes)
- [ ] <pending activity pulled from notes.md>
- [ ] <pending activity / knowledge check>
```

### Conventions (apply to every one-pager)

- **Hyphens, never em-dashes.** Use `-` (never the `—` character) anywhere in the output: title,
  zone headers, prose. This is a standing rule for all writing in this repo.
- **Every subject gets the full layout:** numbered Zones **+** "If you only memorise 5 things" **+**
  "This-week to-dos". Do not drop these blocks for any subject.
- **Three pens, always:** 🖤 = skeleton / always-true, 🔵 = definitions & examples, 🔴 = exam +
  assessment hooks. To-dos use 🕐 (not started) / 🔥 (WIP).
- **Big Idea is mandatory** and framed as "box it" - the one sentence the whole module hangs on.
- **Assessment Hook uses real data** from the README (name, weight, due date, SLOs). If a value is
  genuinely unavailable, say so rather than inventing it.
- **Anchor to the user's day job** in the margin prompts and where natural in the Zones - relate concepts
  to their data-warehouse / database / real work, which is how they retain material.
- **Tables** for comparisons (algorithms, models, pros/cons); **ASCII** (not Mermaid) for flows, pipelines,
  and formulas. Keep `inline code` for technical terms and equations.
- Mirror the tone and density of the existing one-pagers in the same `modules/` tree.

## Step 4: Write the File

- Write the sheet to `<module-folder>/module<NN>_one-pager.md` (overwrite if it already exists - it is a
  derived artifact).
- **Do not commit, push, or open a PR** - generation only (consistent with `/study-mode`). Report the
  output path so the user can review and commit it themselves.

## Important Notes

- **Read-only on the source material.** This skill reads `notes.md`, `module<NN>_notes.md`, the class
  notes, and the README - it does **not** edit them. The only file it writes is the one-pager.
- Status emoji convention: `✅` Done · `🔥` WIP · `🕐` Not started · `🔌` Discontinued.
- Keep it to a single page's worth of content - if the module is huge, prioritise the graded/exam-critical
  material (🔴) over completeness.
