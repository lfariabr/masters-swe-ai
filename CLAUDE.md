# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Master of Software Engineering and Artificial Intelligence (Advanced) repository at Torrens University (program code: MSEAIA18). It serves as both **academic evidence** and a **public GitHub portfolio**. All outputs must be academically credible and industry-practical.

**Program structure:** 13 subjects over 2 years (3 trimesters/year) — 7 SWE core, 4 AI core, 2 electives. Some subjects have prerequisites/corequisites that affect sequencing.

**AI assistant role:** Act as a tutor agent — provide subject guidance, help with core concepts, and align academic work with career goals in AI-driven software engineering. Portfolio and employability should inform recommendations.

## Repository Structure

```
<YEAR>-T<N>/              ← Term directory (e.g. 2026-T1)
  <SUBJECT_CODE>/          ← Subject (e.g. CCF, ISY)
    README.md              ← Subject overview, delivery schedule, SLOs, checklist
    assignments/
      Assessment1/         ← PDF briefs + submission work
      Assessment2/
      Assessment3/
    modules/
      notes.md             ← Consolidated study notes (TLDR → Intro → Resources → Activities)
      module_NN_<slug>/    ← Per-module content folders
    notes/
      notes.md             ← General study notes
    comms/                 ← Lecturer announcements (optional)
  T<N>-Extra/              ← Extracurricular projects for that term
docs/
  devToRefs/               ← dev.to article drafts (portfolio pieces)
  release<X.Y>.md          ← Release notes per term milestone
```

**Current term (2026-T1):** ISY503 (Intelligent Systems) and CCF501 (Cloud Computing Fundamentals).

## Conventions

### Commit Messages

Conventional Commits format with scope and issue references:

```
<type>(<scope>): <description> (Relates|Closes #<issue>)
```

Types: `feat`, `fix`, `chore`. Scopes are subject/project identifiers (e.g. `study-isy503`, `ccf-501`, `southB`, `docs`).

### Status Emoji

`✅` Done | `🔥` WIP | `🕐` Not started | `🔌` Discontinued

### Notes Format

Study notes in `modules/notes.md` follow: **TL;DR** section first, then Introduction, Resources, Learning Activities. Cite sources for academic claims.

### Module Folder Naming

Current convention: `module_NN_<kebab-slug>` (e.g. `module_01_traditional-vs-modern-computing`). Older terms used `moduleN-<slug>` without zero-padding.

## Tech Stack

**Languages:** Python, TypeScript/JavaScript, C#
**Frontend:** React, Next.js, Streamlit
**Backend:** Node.js, Express, FastAPI, GraphQL
**AI/ML:** scikit-learn, PyTorch, transformers, BERTopic
**Databases:** MongoDB, PostgreSQL, Supabase, Redis
**Cloud & DevOps:** AWS, Docker, GitHub Actions
**Testing:** pytest, jest/vitest, xUnit (match to project stack)

## Engineering Guidelines (from `.github/copilot-instructions.md`)

- Prefer simple, maintainable solutions; match existing style and folder conventions
- Keep changes minimal and scoped; avoid unrelated refactors
- Type hints (Python), strict typing (TypeScript), clear interfaces
- If writing code: include "How to run" and "How to test"
- If writing notes: include TL;DR, key concepts, practical examples
- ML pipelines: fixed seeds, explicit splits, tracked metrics, no data leakage
- Use Mermaid diagrams where relevant in documentation

## Build / CI

No centralized build system — this is primarily a documentation/notes repo with isolated project directories. The one CI workflow (`.github/workflows/build-windows-exe.yml`) builds the TTrack PyQt5 app via PyInstaller (manual trigger only).

Individual projects have their own setup; check each project's README for run/test instructions.

## Versioning

GitHub Releases track term milestones (e.g. v3.0.0 = T1-2026 launch). See the README version table for the full roadmap.
