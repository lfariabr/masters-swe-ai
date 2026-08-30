---
name: module-compression
description: Close, compress, or resume a study module by maintaining a durable learning note with demonstrated understanding, corrected misconceptions, evidence, current position, retrieval prompts, and the next learning action. Use when the user asks to close a study session, compress a module, preserve learning progress, resume previous study, or determine where a module stopped.
---

# Module Compression

Maintain a compact but sufficient source of truth that allows a learner to stop now and resume later without reconstructing the session from chat history.

## Locate the module record

Work in the subject or module directory named or implied by the user. Prefer an existing living study note. In this NTW module, the canonical record is [`networking-foundations-study-notes.md`](../../../networking-foundations-study-notes.md).

Do not treat raw transcripts such as `r1.md` as the learning record, and do not overwrite them. If no study note exists, create a clearly named Markdown note beside the module's other study material.

## Close or compress a session

Read the current study note and use the active session as evidence. Update the note so it records:

- the last-studied date;
- the exact stopping point;
- concepts the learner demonstrated correctly;
- misconceptions that were corrected and their replacement models;
- commands, outputs, experiments, or artifacts that provided evidence;
- covered and pending topics;
- the single next action;
- a short retrieval checkpoint for resumption.

Distinguish **explained** from **demonstrated**. Do not mark a concept as mastered merely because it was presented. Preserve useful existing material and the learner's own insights. Consolidate duplicates instead of appending a second version of the same explanation.

Use Mermaid only when it materially clarifies sequence, layering, state, or branching. Keep diagrams valid in GitHub-flavoured Markdown.

Do not invent results, completed exercises, confidence levels, or source claims. If the session ended with an unresolved misconception, record it as the resume point rather than silently correcting the history.

## Resume a session

Read the canonical study note before teaching. Start by reporting:

1. where the learner stopped;
2. what they had demonstrated;
3. what remains pending;
4. the next planned action.

Use one to three retrieval questions to reactivate the prior mental model. Correct the answers before adding new concepts. Continue from the recorded next action and maintain the pacing reflected in the note.

Prefer one conceptual increment followed by retrieval or observation. If the learner signals overload, reduce scope and consolidate before continuing.

## Update discipline

When meaningful learning occurs, update the canonical note before closing the session. Keep its table of contents, status markers, diagrams, CLI evidence, corrections, pending path, and resume checkpoint consistent with one another.

Use repository-relative links inside the note. Keep new content inside the current term and subject directory.
