# study-mode — Module Resource Summariser

A Claude Code skill that reads all resources for a university module (PDFs, articles, videos) and generates structured study notes with Key Highlights, comparison tables, and takeaways.

**Skill definition:** `.claude/skills/study-mode/SKILL.md`  
**Invocation:** Manual only (`disable-model-invocation: true`)

---

## Usage

```
/study-mode <course-code> <module-number>
```

**Examples:**

```
/study-mode CCF501 1    # Cloud Computing Fundamentals — Module 1
/study-mode ISY503 2    # Intelligent Systems — Module 2
```

The course code must match the code in the subject's `README.md`. The module number is a simple integer (1, 2, 3…).

---

## How It Works

The skill runs a **5-step pipeline**:

### Step 1 — Resolve Paths
- Searches `2026-T1/*/README.md` (then other year-term dirs) for the course code
- Maps it to the short directory (e.g. `ISY503` → `2026-T1/ISY`)
- Locates the module folder via glob: `modules/module_<NN>_*/`
- Identifies two key files: `modules/notes.md` and `module<NN>_notes.md`

### Step 2 — Read Module Section from `notes.md`
- Extracts only the target module's section (title, resources, activities, TLDR)
- Checks each resource's current status to determine what needs processing

### Step 3 — Process Each Resource
- Skips anything already marked `✅ Read + Reviewed`
- Reads/fetches each remaining resource based on type (see [Resource Handling](#resource-handling))
- Generates **Key Highlights** per resource using a structured template

### Step 4 — Create/Update `moduleNN_notes.md`
- Creates (or appends to) the module notes file with:
  - **Task List** — numbered table of resources + activities with status
  - **Key Highlights** — structured summaries for each processed resource

### Step 5 — Update `modules/notes.md`
- Fills in the module **TLDR** if it currently says `TODO`
- Updates each summarised resource's status to `✅ Read + Reviewed` with a link to the module notes

---

## Output Format

### Task List (in `moduleNN_notes.md`)

```markdown
| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise McHaney (2021) — Cloud technologies Ch.1 | ✅ |
| **2** | Watch & summarise Nishimura (2022) — Intro to AWS videos | ✅ |
| 3 | Activity 1: Introduce Yourself | 🕐 |
```

- Resources first, activities last
- Completed items get **bold** row numbers
- Verb matches type: `Read & summarise`, `Watch & summarise`, `Listen & summarise`

### Key Highlights (in `moduleNN_notes.md`)

Each resource gets a self-contained section:

```markdown
### N. Author, A. (Year). Title of work.

**Citation:** Full citation from notes.md
**Purpose:** 1-2 sentence summary

---

#### 1. First Major Theme
- **Bold labels** for key terms
- Comparison **tables** where applicable

#### Key Takeaways for [Subject Name]
1. Connection to module activities and assessments
2. Links to other resources in this module
```

### Status Updates (in `modules/notes.md`)

```markdown
> *Status: ✅ Read + Reviewed — see [module01_notes.md](relative-path)*
```

---

## Resource Handling

| Resource Type | How It's Processed | Fallback |
|---|---|---|
| **PDF** (in module folder) | Extracted via `pdftotext` (requires `poppler`) | Tells user to run `brew install poppler` |
| **Web article / blog** | Fetched via WebFetch | — |
| **Video** (LinkedIn Learning, YouTube) | Fetched via WebFetch (transcript if available) | — |
| **Podcast / audio** | Looks for transcript URL; fetches if found | Marked `🔥 WIP — needs manual listen` |
| **eBook** (ProQuest, IEEE, O'Reilly) | Requires authentication — cannot auto-fetch | Marked `🔥 WIP — needs manual access` |

---

## Status Conventions

| Emoji | Meaning |
|---|---|
| ✅ | Done — read, watched, or reviewed |
| 🔥 | WIP — in progress or needs manual action |
| 🕐 | Not started |
| 🔌 | Discontinued |

---

## Example Output

**CCF501 Module 1** is a fully completed example:

- **Module notes:** `2026-T1/CCF/modules/module_01_traditional-vs-modern-computing/module01_notes.md`
  - 5 resources summarised with Key Highlights (McHaney, Nishimura, Eliaçık, Accenture, Manvi & Shyam)
  - 3 activities listed as `🕐`
  - Comparison tables for deployment models, service models, virtualisation characteristics
- **Source tracking:** `2026-T1/CCF/modules/notes.md`
  - TLDR filled in, all 5 resources marked `✅` with links to highlights

---

## Limitations & Tips

- **Idempotent** — re-running the skill on a module skips all `✅` resources; only processes new or WIP items
- **Module-scoped** — only touches the target module's section in `notes.md`; other modules are untouched
- **Poppler dependency** — PDF extraction requires `poppler`. Install with `brew install poppler` if not already present
- **Authenticated resources** — eBooks behind university login (ProQuest, IEEE Xplore, O'Reilly) cannot be auto-fetched. Download the PDF manually and place it in the module folder, or paste the content for Claude to process
- **Append-only** — if `moduleNN_notes.md` already exists with some highlights, new highlights are appended, not overwritten
- **TLDR preservation** — if a TLDR is already written (not `TODO`), it won't be overwritten