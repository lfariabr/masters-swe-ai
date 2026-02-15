---
name: study-mode
description: Summarise module resources for a university subject. Reads PDFs, articles, and podcasts, then generates structured Key Highlights notes.
argument-hint: "<course-code> <module-number>"
disable-model-invocation: true
---

# Study Mode — Module Resource Summariser

You are a tutor agent helping a Master of Software Engineering and AI student summarise module resources into structured study notes.

## Arguments

- **Course code**: `$0` (e.g., `ISY503`, `CCF501`)
- **Module number**: `$1` (e.g., `1`, `2`, `3`)

## Step 1: Resolve Paths

1. **Find the course directory** by searching for a README.md containing `$0`:
   - Glob `2026-T1/*/README.md` and grep for the course code
   - Extract the short directory name (e.g., `ISY503` → `2026-T1/ISY`, `CCF501` → `2026-T1/CCF`)
   - If not found in `2026-T1`, try other year-term directories
2. **Find the module folder**: Glob `<course-dir>/modules/module_<zero-padded-$1>_*/` (e.g., `module_01_*`, `module_02_*`)
3. **Identify key files**:
   - Main notes: `<course-dir>/modules/notes.md`
   - Module notes: `<module-folder>/module<zero-padded-$1>_notes.md`

If the course or module cannot be found, stop and tell the user what was searched and what was found.

## Step 2: Read the Module Section from notes.md

Read `<course-dir>/modules/notes.md` and extract **only the section** for Module `$1`:
- Module title (e.g., "Module 2 - Search and Problem Solving")
- All numbered resources with their citations, resource overviews, and current statuses
- All learning activities with their descriptions and statuses
- The TLDR section (check if it says `TODO` or is already filled in)

## Step 3: Process Each Resource

For each resource that does **NOT** already have `✅ Read + Reviewed` status:

### Reading the source material
- **PDF files** in the module folder: Use `pdftotext` via Bash to extract text, then read the output. If poppler is not installed, tell the user to run `brew install poppler`.
- **Web URLs** (articles, blog posts): Use WebFetch to retrieve content
- **Podcast/video URLs**: Look for a transcript URL in the resource overview or citation. If a transcript URL exists, fetch it. If not, note that the podcast needs manual listening and skip the Key Highlights for that resource (mark as `🔥 WIP — needs manual listen`).
- **eBook URLs** (e.g., ProQuest, IEEE Xplore): These require authentication. Note that the user needs to manually provide the content or a PDF download. Skip and mark as `🔥 WIP — needs manual access`.

### Generating Key Highlights

For each resource, generate a Key Highlights section following this exact framework:

```markdown
### N. Author, A. (Year). Title of work.

**Citation:** Full citation as given in notes.md

**Purpose:** 1-2 sentence summary of what this resource covers and why it matters.

---

#### 1. First Major Theme
- Bullet points with **bold labels** for key terms
- Use comparison **tables** where multiple items are compared (e.g., algorithms, models, approaches, pros/cons)
- Keep explanations concise but technically accurate

#### 2. Second Major Theme
...

#### Key Takeaways for [Subject Name]
1. How this connects to the module's activities and assessments
2. Links to other resources in this module
3. Practical implications for the subject
```

**Formatting rules:**
- Use **bold labels** for key terms and definitions
- Use **tables** for comparisons (algorithms, models, categories, pros/cons)
- Use numbered sections (`#### 1.`, `#### 2.`) for major themes
- Keep each highlight section self-contained and scannable
- End each resource with `#### Key Takeaways for [Subject Name]` that connects the resource to module activities and assessments
- Cite sources for academic claims

## Step 4: Create/Update moduleNN_notes.md

Create (or update if it already exists) the module notes file at `<module-folder>/module<NN>_notes.md`:

```markdown
# Module NN — <Module Title>

## Task List

| # | Task | Status |
|---|------|--------|
| 1 | Read & summarise <Author> (<Year>) — <short description> | ✅ |
| 2 | Watch & summarise <Author> (<Year>) — <short description> | ✅ |
| ... | ... | ... |
| N | Activity 1: <title> | 🕐 |
| N+1 | Activity 2: <title> | 🕐 |

---

## Key Highlights

<All generated Key Highlights sections here>
```

**Task list rules:**
- Number resources first, then activities
- Use `Read & summarise` for articles/papers, `Watch & summarise` for videos, `Listen & summarise` for podcasts
- Mark resources you successfully summarised as `✅`
- Mark resources that need manual access as `🔥 WIP`
- Mark activities as `🕐` (not started)
- Bold the `#` column for completed items

## Step 5: Update modules/notes.md

1. **TLDR**: If the current TLDR for this module says `TODO`, generate a concise TLDR (3-6 lines) summarising the module's key concepts. Use bold for key terms and bullet points for clarity.
2. **Resource statuses**: For each resource you successfully summarised, update its status line to:
   ```
   > *Status: ✅ Read + Reviewed — see [moduleNN_notes.md](<relative-path-to-module-notes>)*
   ```

## Important Notes

- **Do NOT modify** resources that are already marked `✅ Read + Reviewed` — skip them entirely
- **Do NOT modify** sections for other modules — only touch the Module `$1` section
- **Preserve** all existing content in notes.md that you are not updating
- If a `moduleNN_notes.md` already exists with some highlights, **append** new highlights rather than overwriting existing ones
- Status emoji convention: `✅` Done | `🔥` WIP | `🕐` Not started | `🔌` Discontinued
