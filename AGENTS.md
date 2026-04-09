# Repository Guidelines

## Project Structure & Module Organization
This repository is organized by academic term and subject, not as a single application. Use `2025-T1/`, `2025-T2/`, and `2026-T1/` as the top-level term folders, then work inside the relevant subject directory such as `2026-T1/CCF/` or `2026-T1/ISY/`.

Typical subject layout:
- `README.md`: subject overview, schedule, and status
- `modules/`: study notes plus per-module folders such as `module_09_governance-and-legal/`
- `assignments/Assessment1|2|3/`: briefs, drafts, and submission artifacts
- `notes/` or `comms/`: optional supporting material
- `T<N>-Extra/`: side projects for that term

Keep new content inside the correct term/subject path. Follow module folder naming like `module_01_<kebab-slug>`.

## Build, Test, and Development Commands
There is no repository-wide build system. Run commands from the relevant project folder and document them in that folder’s `README`.

Common examples:
- `python -m venv venv && source venv/bin/activate`: create a local Python environment
- `pip install -r requirements.txt`: install Python dependencies for small projects such as `2025-T2/T2-Extra/southB/`
- `streamlit run app.py`: run the South B Streamlit app
- `npm install && npm test`: use for isolated Node/TS projects when a local `package.json` exists

CI is minimal: `.github/workflows/build-windows-exe.yml` manually builds the TTrack Windows executable.

## Coding Style & Naming Conventions
Prefer small, maintainable changes. Match the existing style of the folder you are editing.

- Python: 4-space indentation, type hints where practical, descriptive snake_case names
- TypeScript/JavaScript: clear interfaces, camelCase for variables/functions, PascalCase for components/classes
- Markdown: short sections, direct bullets, and source citations for academic claims

For notes, keep a `TL;DR` first when the surrounding subject already uses that pattern.

## Testing Guidelines
There is no enforced repo-wide coverage threshold. Use the test framework that matches the local stack: `pytest`, `jest`/`vitest`, or `xUnit`. Name tests after the unit under test, for example `test_filters.py` or `analytics.test.ts`. If a folder has no tests yet, add focused tests only when you introduce executable logic.

## Commit & Pull Request Guidelines
Follow the repository’s Conventional Commit pattern:

`feat(study-ccf501): add Module 9 refs (Relates #111)`

Use `feat`, `fix`, or `chore`, with a subject or project scope such as `study-isy503`, `study-ccf501`, `southB`, or `docs`. PRs should stay narrow, explain the academic or project context, link the issue when available, and include screenshots only for UI changes.
