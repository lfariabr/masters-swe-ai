# BDA601 Assessment 3 - Video presentation outline (skeleton)

**Format:** 8-10 slides, video <= 10 minutes. Audience = the focal country's **non-bordering neighbours**, who need it to make COVID policy decisions. Tie together predictive modelling + clustering + graph analytics + visualisation (the rubric rewards "all analytical tasks correlated").

**Deliverables to submit (zip):** Python source code (the notebook, with run instructions in a comment at the top) + the video file + this slide deck exported to PDF.

**Numbers below are the real outputs from `outputs/metrics.json`** - swap in fresh ones if you re-run on a newer download.

---

### Slide 1 - Title / hook (~30s)
- **Title:** "What the world's worst outbreak can teach its neighbours - a COVID-19 data story"
- You: Luis Faria · BDA601 Assessment 3 · Johns Hopkins CSSE data (22 Jan 2020 - 9 Mar 2023).
- Hook line: *"The US recorded 103 million cases. The question that matters for its neighbours: could they have seen their own waves coming?"*

### Slide 2 - The approach (~45s)
- Every big-data project = **prepare -> analyse -> decide**.
- The analytical chain (one feeds the next): top-3 countries -> linear regression -> pick most volatile -> K-Means waves -> graph to neighbours -> recommendation.
- Tools: Apache Spark MLlib (regression + K-Means), networkx (graph).

### Slide 3 - The three worst-hit countries (~45s) · **fig01_top3_cumulative.png**
- Top 3 by total confirmed: **US 103.8M · India 44.7M · France 39.9M**.
- All three rise, but at very different rates and shapes - which one is the most volatile?

### Slide 4 - Predictive modelling: a line is not enough (~60s) · **fig02_regression_fits.png**
- Linear regression of cumulative cases on week number, per country.
- US has the **highest variance** (slope ~760k cases/week, R2 = 0.97) -> carried forward.
- Key point: even R2 = 0.97 **hides** the story - a straight line cannot show *when* the surges hit.

### Slide 5 - Clustering reveals the waves (~75s) · **fig03_clusters_waves.png**
- K-Means on `[week, weekly new cases]`, best **K = 3** (silhouette 0.705).
- The clusters expose phases - and isolate a **mega-surge of ~4.46M new cases/week around weeks 102-106 (the Omicron wave, Jan 2022)** as its own cluster.
- This **validates** that growth was *not* steady: it came in waves (up - down - up).

### Slide 6 - Graph analytics: who moves with the US? (~60s) · **fig04_neighbour_graph.png**
- The US linked to non-bordering neighbours (Canada, Mexico - they do not border each other).
- Edge = correlation of weekly new cases: **Canada r = 0.85 (strong)**, **Mexico r = 0.70**.
- Canada's waves track the US most closely -> strongest early-warning candidate.

### Slide 7 - The whole story in one frame (~45s) · **fig05_story_panel.png**
- Left: US waves by phase. Right: how strongly each neighbour correlates.
- The line from raw data -> phases -> a neighbour recommendation.

### Slide 8 - Recommendations to the neighbours (~75s)
- **Canada (r = 0.85):** treat the US trajectory as a leading indicator; when the US enters a surge phase, pre-position testing + hospital capacity ~1-2 weeks ahead.
- **Mexico (r = 0.70):** moderate coupling; watch US surges but weight local signals more.
- General: the isolated Omicron-style cluster is the scenario to plan capacity for, not the steady baseline.

### Slide 9 - Limitations & close (~45s)
- Data caveats: counts are **cumulative** and **reporting-dependent**; the JHU series **stopped 10 Mar 2023**; "neighbour" defined by geography, not true mobility.
- Next steps: model **weekly new cases** directly, add mobility/vaccination data, test lead-lag (cross-correlation) to quantify the warning window.
- Close: data turned a wall of numbers into a concrete, actionable warning for neighbours.

---

## Recording tips
- ~10 min / 9 slides = ~1 min each; rehearse once to stay under 10:00 (the rubric penalises going over).
- Narrate the *decision*, not the code - the audience is policymakers, not engineers.
- Export the deck to PDF for submission; keep the figures large and readable.
