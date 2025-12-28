# GitHub Copilot Instructions (masters-swe-ai)

You are assisting in a repository that documents a Master of Software Engineering / AI journey.
Outputs must be academically credible *and* industry-practical.

Treat this repo as both assessment evidence and a GitHub portfolio.

## Repo intent
- Notes, projects, insights, experiments in AI/ML + software engineering
- Code in Python, TypeScript/JavaScript, and C#
- Deliverables should be portfolio-ready and assessment-friendly

## Default behavior
- Ask 1–2 clarifying questions only if blocked; otherwise make reasonable assumptions and proceed.
- Prefer simple, maintainable solutions over clever ones.
- Match the existing style and folder conventions of the repo.
- Keep changes minimal and scoped; avoid unrelated refactors.

## Engineering standards
- Provide production-quality code: validation, error handling, logging, and clear naming.
- Include tests when it’s reasonable (pytest / jest / vitest / xUnit depending on stack).
- Write small functions, avoid duplication, and keep modules cohesive.
- Prefer type hints (Python), strict typing (TS), and clear interfaces/contracts.

## Documentation standards
When adding docs (README, .md notes, reports):
- Use clear headings, short paragraphs, and bullet points.
- Include: purpose, assumptions, steps to run, and expected outputs.
- If relevant: add diagrams in Mermaid and example commands.
- Cite sources when making factual/academic claims.

## Data/ML work
- Make pipelines reproducible: fixed seeds, explicit splits, and tracked metrics.
- Include evaluation (baseline + improved model), error analysis, and limitations.
- Avoid data leakage; document features and target clearly.

## What to output
- If writing code: include brief “How to run” and “How to test”.
- If writing notes: include a short TL;DR, key concepts, and practical examples.
- If unsure: provide 2 options with tradeoffs and pick a recommendation.
