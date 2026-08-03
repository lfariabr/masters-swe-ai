# A3 K-Means section - update plan (shipped)

**Status:** done. Implemented on `study-bda601/a3-kmeans-wcss-elbow`, PR [#233](https://github.com/lfariabr/masters-swe-ai/pull/233).

**Source of the ideas:** MLN601 module 9 notes (`2026-T2/MLN/modules/module-09-kmeans-clustering/module09_notes.md`, `module09_notes-class.md`) and Dr Kamran's writing-style guidance (same folder, Appendix A-E).

**Target file:** `2026-T2/BDA/assignments/Assessment3/notebook/build_nb.py` only - section 4 (clustering), the glossary, section 9 (Limitations), Appendix B (decision log), Appendix C (reproducibility), and the `metrics.json` persist block. Nothing changes the analytical chain or any pre-existing number (top-3, regression, K=3, silhouette scores, lead-lag) - confirmed by diffing `metrics.json` before/after: the only additions are `clustering.wcss` and `clustering.elbow_k`.

**Confirmed out of scope, unaffected:** `presentation/slides.md`, `slides_outline.md`, `narration_script.md` all state "K=3 (silhouette 0.705)" as the sole justification - that remains true since silhouette stays authoritative, so none of the three needed edits. `README.md` has no clustering references.

---

## 1. WCSS elbow alongside silhouette

**Why:** module09_notes.md lists elbow and silhouette as the two standard methods for choosing K. The notebook previously reported only silhouette, so K=3 rested on one signal.

**What shipped:**
- `km.summary.trainingCost` (verified against `pyspark==3.5.3` in the `bda-spark` kernel - `KMeansSummary.trainingCost`, "equivalent to sklearn's inertia") captured per K alongside silhouette, in the existing `for k in range(2, 7)` loop.
- WCSS is monotonically non-increasing in K, so it can't be chosen by `min()` - that would always return K=6. The elbow is instead the K whose WCSS point sits furthest from the straight chord joining the first and last tested K (a small numpy-only knee-detection heuristic, no `np.cross` - that's deprecated for 2D vectors in NumPy 2.x, so the perpendicular-distance formula is written out directly).
- New figure `fig08_k_selection.png` (not `fig03b` - existing figures are numbered by logical/slide order, not code position, so a trailing `fig08` fits the convention without renumbering anything).
- **Decision rule fixed before results:** silhouette stays authoritative (`best_k` unchanged); WCSS is corroborating evidence only. If they disagreed, the notebook prints a note rather than silently picking one. In the actual run both agree on K=3 (silhouette 0.705 at K=3; WCSS elbow also K=3), so the disagreement branch exists in code but wasn't exercised.
- `metrics.json`: added `clustering.wcss` (K → trainingCost) and `clustering.elbow_k`, siblings of the existing `clustering.silhouette`.

---

## 2. Name the initialisation method (k-means||)

**What shipped:** inline comment on the `KMeans(...)` call noting Spark's `initMode` default is `"k-means||"` (parallel k-means++), so no separate multi-run/`n_init` loop is needed. Glossary's `K-Means` row extended with the same clause; new `WCSS (inertia)` row added directly after `Silhouette score`, matching the glossary's one-concept-per-row pattern.

---

## 3. Honest limitation: convex-cluster assumption

**What shipped:** merged into the *existing* `week is a clustering input` bullet (section 9) rather than added as a new adjacent one. The original plan's draft had two separate bullets explaining the same observed contiguity from different angles (mechanical: week is a feature; geometric: K-means favours convex shapes) - stacking them read as two competing explanations for the same thing. One merged bullet naming both is internally consistent.

---

## 4. Ripple effects (found during plan review, not in the original draft)

- **Appendix B** (decision log): row 4 ("Choice of K") updated to mention the WCSS cross-check; new row 9 added for the silhouette-vs-WCSS tie-break rule itself, matching the table's own stated purpose of recording rules fixed before results.
- **Appendix C** (reproducibility): `fig08_k_selection.png` added to the generated-artefacts table; "seven figures" → "eight figures" (the only place in the file stating a figure count); "Sources of determinism" extended to note WCSS is deterministic under the same seed.

These were missed in the first draft of this plan - it scoped edits to section 4 and one Limitations line without checking that Appendix B and C, in the same file, describe exactly the things this change touches.

---

## Execution order (as run)

1. Edited `build_nb.py` (all five points above, one file).
2. `python3 build_nb.py` → 32 cells (was 31).
3. Re-executed via `jupyter nbconvert ... --ExecutePreprocessor.kernel_name=bda-spark` - zero errors.
4. Diffed `metrics.json` before/after: only `clustering.wcss` and `clustering.elbow_k` added, everything else byte-identical.
5. Visually checked `fig08_k_selection.png` - clean elbow at K=3, matches the silhouette peak.
6. Committed on branch `study-bda601/a3-kmeans-wcss-elbow`, pushed, opened PR #233 for review (not committed straight to master).

## Explicitly out of scope (unchanged from v1)

- DBSCAN/K-medoids comparison - the brief scores K-Means specifically; would be scope creep.
- MiniBatchKMeans - the per-country weekly series is small (~164 rows), doesn't apply.
- Gap statistic as a third K-selection method - not needed once silhouette and WCSS agree.
