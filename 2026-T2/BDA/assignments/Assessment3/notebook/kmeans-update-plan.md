# A3 K-Means section - update plan

**Source of the ideas:** MLN601 module 9 notes (`2026-T2/MLN/modules/module-09-kmeans-clustering/module09_notes.md`, `module09_notes-class.md`) and Dr Kamran's writing-style guidance (same folder, Appendix A-E). Nothing here changes the analytical chain or any already-reported number (top-3, regression, K=3, silhouette scores, lead-lag) - all three items are additive.

**Target file:** `2026-T2/BDA/assignments/Assessment3/notebook/build_nb.py`, section 4 ("Clustering - K-Means on the most volatile country"), plus one line in section 9 ("Limitations").

**Not in scope:** slides, narration script, `metrics.json` restructuring beyond adding the new WCSS values, or the graph/lead-lag sections - none of that is touched by this plan.

---

## 1. Elbow (WCSS) alongside silhouette

**Why:** module09_notes.md lists elbow and silhouette as the two standard methods for choosing K ("Three ways to choose k"). The notebook currently only reports silhouette per K, so the choice of K=3 rests on one signal. Plotting WCSS next to silhouette costs nothing (the `KMeans` fit already happening in the `for k in range(2, 7)` loop exposes `.summary.trainingCost`, Spark's inertia) and directly strengthens the "Analysis and insights" rubric criterion (30%) by showing two independent methods agree.

**Where:** `build_nb.py` lines ~320-327, inside the existing K-search loop.

**Change:**
- Capture `km.summary.trainingCost` per K alongside the existing silhouette score.
- Print both series (K → silhouette, K → WCSS) in the existing print statement.
- Add a small two-panel figure (silhouette vs K, WCSS vs K with the elbow visible) - reuse the existing `fig03`-adjacent figure numbering, likely `fig03b_k_selection.png` inserted before the current `fig03_clusters_waves.png`.
- One sentence in the markdown cell above section 4's code: "K is chosen by the highest silhouette score over K=2..6, cross-checked against the WCSS elbow."
- `metrics.json`: add a `clustering.wcss` dict (K → trainingCost) next to the existing `clustering.silhouette` dict.

**Risk:** none to existing numbers - `best_k` selection logic (`max(sil, key=sil.get)`) is unchanged, only a second metric is now computed and reported alongside it.

---

## 2. Name the initialisation method (k-means||)

**Why:** Pedregosa/module09_notes.md flags initialisation as the reason K-means can converge to a local minimum, and recommends k-means++ explicitly. Spark's `KMeans` already defaults to `initMode="k-means||"` (the scalable, parallel k-means++ variant) - this is correct practice already in place, it's just never stated. A one-line comment plus a clause in the glossary closes that gap without changing any code behaviour.

**Where:**
- `build_nb.py` ~line 323: inline comment on the `KMeans(...)` call noting `initMode` defaults to `"k-means||"` (parallel k-means++), so no explicit `n_init`/multi-run loop is needed the way scikit-learn would need one.
- Glossary table (~line 679-682): add or extend the `K-Means` row to mention k-means|| initialisation.

**Risk:** none - documentation-only, zero code/number changes.

---

## 3. Honest limitation: spherical/convex-cluster assumption

**Why:** both Pedregosa (module09_notes.md §3, "known drawbacks") and Dr Kamran's lecture (module09_notes-class.md §6) name the same weakness: K-means assumes roughly spherical, similar-size, similar-density clusters. Our clusters are contiguous week-ranges on a 2D `[week, new_cases]` feature space - defensible, but worth naming rather than leaving implicit, matching the "honest Limitations section" habit Kamran's own paper models (module09_notes-class.md Appendix, habit #4).

**Where:** section 9 Limitations list (~line 614 area, where the "week is a clustering input" caveat already lives) - add one adjacent bullet, not a new subsection.

**Draft wording:** "K-Means assumes clusters are roughly convex and similarly sized; the phases found here read as contiguous week-ranges partly because the true underlying structure (sequential pandemic waves) happens to fit that assumption reasonably well, not because K-Means would flag a mismatch if it did not."

**Risk:** none - prose-only addition to an existing list.

---

## Execution order

1. Edit `build_nb.py` (all three items).
2. Rebuild: `python3 build_nb.py`.
3. Re-execute: `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=bda-spark --ExecutePreprocessor.timeout=600`.
4. Diff-check `metrics.json` - confirm every pre-existing key/value is untouched, only `clustering.wcss` and (if added) a new `fig03b` entry appear.
5. Confirm zero-error execution via the existing error-scan check.
6. No deck/slides/script changes required - this plan only touches the notebook.

## Explicitly out of scope (flagged, not actioned)

- DBSCAN/K-medoids comparison (Kamran's lecture, §6) - genuinely interesting but the brief scores K-Means specifically; adding a second algorithm would be scope creep, not requested.
- MiniBatchKMeans (Pedregosa, large-data variant) - our per-country weekly series is small (~164 rows), doesn't apply.
- Gap statistic as a third K-selection method - diminishing return once silhouette + WCSS agree; not planned unless the two disagree once results are in.
