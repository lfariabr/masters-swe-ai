---
name: module-compression
description: Compress completed university module notes into a small mental model after the student has made a first pass through the detailed material. Use when the user asks for module compression, says the notes are dense or overwhelming, wants the core concepts to click, or has returned after reading notes and taking a break.
---

# Module Compression

Run a second-pass consolidation session. Preserve the structure the student already encountered, but remove detail until the module becomes easy to hold in working memory. Do not replace first-pass reading or create repository files.

## Arguments

- **Subject code:** first argument, such as `DLE`, `MLN`, or `BDA601`.
- **Module number:** second argument, such as `6`. Zero-pad it to `NN` for paths.

## 1. Resolve the module

1. Glob `[0-9][0-9][0-9][0-9]-T[0-9]/*/README.md` from the repository root.
2. Match the subject directory case-insensitively. Also try the code with trailing digits removed.
3. Prefer the latest term that contains `<subject-dir>/modules/module-<NN>-*/`.
4. Require `<module-folder>/module<NN>_notes.md`. If it is absent or only a stub, stop and recommend `/study-mode <SUBJECT> <N>` first.

## 2. Read the minimum useful context

Read:

1. `module<NN>_notes.md` as the primary source.
2. The module TLDR and learning activities in `<subject-dir>/modules/notes.md`.
3. `module<NN>_one-pager.md` and `module<NN>_notes-class.md` only when present.
4. The subject README only for assessment connections.

Do not read raw references unless the notes contain a contradiction or unsupported gap. Do not read assignment answers or submission artifacts unless the user explicitly requests assessment grounding.

## 3. Produce the compression

Match the user's language. Keep the whole response compact enough to absorb in approximately two minutes.

### A. The one mental model

Express the whole module as one sentence, equation, pipeline, or question. Prefer language such as:

```text
Everything in this module is trying to answer: <one question>.
```

### B. The concept compression

Use one of these, based on the content:

- **Comparison table:** for sibling methods, architectures, or algorithms. Use no more than seven rows and the columns `Concept`, `Question it asks`, and `Use it when`.
- **Small diagram:** for stages, causality, hierarchy, or information flow. Use Mermaid in chat when it materially improves understanding; otherwise use compact ASCII.
- Use both only when the second visual adds new information.

### C. Why the distinctions matter

Give no more than three bullets connecting the compressed model to:

- a learning activity or assessment;
- a familiar project, job, or earlier module;
- the limitation that motivates the next technique or module.

### D. Friction questions

Predict three concepts that are likely to remain unclear and phrase them as the student's next questions. Answer each in one or two plain-language sentences. Prioritise foundational terms such as variance, gradient, latent variable, eigenvalue, attention, or probability when relevant.

### E. Retrieval handoff

End with exactly two options:

1. `/active-recall <SUBJECT> <N>` to measure retrieval and expose gaps.
2. `/one-pager <SUBJECT> <N>` to create the hand-written consolidation artifact.

## Guardrails

- Treat compression as a **second pass after exposure**, not a shortcut around the source material.
- Preserve technically important boundaries. Simple must not become wrong.
- Explain jargon using the user's existing projects or prior coursework when possible.
- State when an analogy is only an analogy.
- Do not flatter, grade, commit, push, or edit files.
- Use hyphens, never em dashes.
