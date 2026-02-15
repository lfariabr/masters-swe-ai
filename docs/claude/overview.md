# Claude Code — Overview

How this repo leverages [Claude Code](https://claude.ai/code) (paid subscription) to accelerate study, automate repetitive work, and build a portfolio-grade academic workflow during the Master of Software Engineering & AI at Torrens University.

---

## Why Claude Code?

As a senior engineer with 10+ years of experience pivoting into a masters program, the goal is not just to study — it's to **study smart, ship fast, and build leverage**. Claude Code acts as a tutor agent embedded directly in the development environment, turning raw module resources into structured notes, enforcing consistency, and freeing up time for deep work on projects and assessments.

**Key benefits for this workflow:**
- **Automated study notes** — PDFs, articles, and videos summarised into structured Key Highlights in seconds
- **Consistent formatting** — every module follows the same template (task list → highlights → takeaways)
- **Idempotent re-runs** — safe to invoke repeatedly; already-reviewed resources are skipped
- **Project-aware context** — `CLAUDE.md` gives Claude full understanding of repo structure, conventions, and tech stack

---

## CLAUDE.md — Project Configuration

**Location:** `CLAUDE.md` (repo root)

This is the primary configuration file that gives Claude Code context about the entire repository. It's read automatically at the start of every session.

**What it contains:**
- **Repository purpose** — academic evidence + public GitHub portfolio
- **Directory structure** — year-term layout, subject folders, module conventions
- **Commit conventions** — Conventional Commits format with scope and issue refs
- **Status emoji** — `✅` Done | `🔥` WIP | `🕐` Not started | `🔌` Discontinued
- **Notes format** — TLDR → Introduction → Resources → Activities
- **Tech stack** — Python, TypeScript, React, FastAPI, scikit-learn, PyTorch, AWS, Docker, etc.
- **Engineering guidelines** — minimal changes, type hints, Mermaid diagrams, ML best practices
- **Build/CI info** — no centralized build; individual project READMEs for run/test instructions
- **Versioning** — GitHub Releases track term milestones (e.g. v3.0.0 = T1-2026)

**Why it matters:** Without `CLAUDE.md`, Claude would need to be re-briefed every session. With it, every conversation starts with full project awareness — folder naming, commit style, academic context, and engineering standards.

---

## Skills

### What Are Skills?

Skills are reusable instruction sets stored in `.claude/skills/` that teach Claude Code how to perform a specific, repeatable task. Think of them as **executable SOPs** — Claude reads the skill definition and follows it step by step.

Each skill is a Markdown file with YAML frontmatter:

```yaml
---
name: skill-name
description: What the skill does
argument-hint: "<arg1> <arg2>"
disable-model-invocation: true   # manual-only = must use /skill-name
---
```

**Key properties:**
- **Manual invocation** (`disable-model-invocation: true`) — skill only runs when you explicitly call `/skill-name`
- **Arguments** — passed as positional args (`$0`, `$1`, etc.)
- **Markdown body** — step-by-step instructions Claude follows

### How to Create a New Skill

1. Create a folder: `.claude/skills/<skill-name>/`
2. Add `SKILL.md` with YAML frontmatter + step-by-step instructions
3. Use `$0`, `$1`, etc. for arguments
4. Set `disable-model-invocation: true` if you want manual-only triggering
5. Invoke with `/skill-name <args>`

### Current Skills

| Skill | Purpose | Invocation |
|---|---|---|
| **[study-mode](study-mode.md)** | Summarise module resources into structured Key Highlights notes | `/study-mode <course-code> <module-number>` |

### Future Skill Ideas

| Skill | Purpose | Status |
|---|---|---|
| **assessment-checker** | Validate assessment submissions against rubric criteria, flag missing requirements, check formatting | Planned |
| **article-summarizer** | Summarise dev.to / blog articles into structured notes for portfolio reference | Planned |
| **module-planner** | Generate a weekly study schedule from a module's resources and activities | Idea |
| **seo-analyzer** | Analyze website SEO performance and suggest improvements | Idea |

---

## Permissions

**Location:** `.claude/settings.local.json`

Controls what Claude Code is allowed to do without asking for confirmation.

**Current permissions:**

| Permission | Why |
|---|---|
| `Bash(cat:*)` | Read any file via `cat` |
| `Bash(git ... log --oneline ...)` | View recent commit history |
| `Bash(git ... branch:*)` | List and inspect branches |
| `WebSearch` | Search the web for references |
| `WebFetch(domain:claude.ai)` | Fetch Claude docs |
| `Bash(brew install:*)` | Install dependencies (e.g. `poppler` for PDF extraction) |

These are intentionally conservative — destructive operations (file deletion, force push, etc.) always require manual approval.

---

## File Structure

All Claude Code configuration lives in these locations:

```
CLAUDE.md                              ← Project-level context (repo root)
.claude/
  settings.local.json                  ← Permissions config
  skills/
    study-mode/
      SKILL.md                         ← study-mode skill definition
docs/claude/
  overview.md                          ← This file — Claude Code overview
  study-mode.md                        ← study-mode usage documentation
```

---

## Workflow Tips

- **Start every Claude Code session** by letting it read `CLAUDE.md` — it auto-loads, but if context seems off, ask Claude to re-read it
- **Run study-mode per module** as you begin each week's content — it front-loads the reading and gives you structured notes to review
- **Re-run safely** — if a module gets new resources or you manually reviewed an eBook, re-run `/study-mode` and it will only process the new items
- **Check the task list** in `moduleNN_notes.md` for a quick view of what's done vs. pending per module
- **Use Key Takeaways** at the end of each resource highlight to connect readings back to assessments — saves time during assignment prep
- **Extend with new skills** as patterns emerge — if you find yourself giving Claude the same instructions repeatedly, that's a skill waiting to be created