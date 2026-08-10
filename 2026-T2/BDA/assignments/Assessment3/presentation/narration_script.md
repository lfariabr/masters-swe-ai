# BDA601 Assessment 3 - narration script

**Target: ~9:00 of a 7-10 minute video, across 10 slides.** Read at a calm pace; numbers are exact from
`outputs/metrics.json`. Audience = the focal country's neighbours (policymakers).
Narrate the *decision*, not the code. Times are per-slide; rehearse once to confirm you land under 10:00 -
if you are running long, slide 8 (the summary panel) is the safest one to shorten, since slides 6, 7 and 9
carry the argument.

---

### Slide 1 - Title / hook  (~0:30)

"Hi, I'm Luis Faria. This is my BDA601 model-evaluation project on the Johns Hopkins COVID-19 data,
covering January 2020 to March 2023. Here's the hook: the United States recorded over 103 million
confirmed cases - the worst outbreak in the dataset. The question that actually matters for its
neighbours is this: *could they have seen their own waves coming?* That's what this analysis answers."

### Slide 2 - The approach  (~0:45)

"Every big-data project runs the same way: prepare the data, analyse it, then make a decision. My
analysis is one connected chain. I find the three worst-hit countries, fit a regression to each, pick
the most volatile one, use K-Means clustering to expose its infection waves, then build a graph to its
neighbours to turn that into an early-warning recommendation. The engine is Apache Spark's MLlib for
the regression and clustering, and networkx for the graph - across 164 weeks of data."

### Slide 3 - The three worst-hit countries  (~0:45)

"Ranking every country by total confirmed cases, the top three are the United States at 103.8 million,
India at 44.7 million, and France at 39.9 million. You can see all three climb steadily on this chart -
but they climb at very different rates and with very different shapes. So the next question is: which
of these three is the *most volatile* - the one whose surges are sharpest and most worth studying?"

### Slide 4 - Predictive modelling  (~0:55)

"I fit a linear regression of cumulative cases on week number, per country - these are the three fits.
The US line looks strong: R-squared of 0.97, slope of about 760 thousand cases a week. But look at the
residuals below - they trace a clear S-curve, not noise. The US residual only changes sign five times
across 164 weeks, when pure noise would flip it about eighty, and even with that 0.97 R-squared the
typical miss is 6.47 million cases. So the line is confidently wrong: it hides exactly when the surges
hit. To choose who goes into clustering, I rank all three by the variance of their *weekly new cases* -
the US is clearly highest, 6.4 times ten-to-the-eleven against 2.5 for India and 1.6 for France."

### Slide 5 - Clustering reveals the waves  (~1:15)

"So for the US I run K-Means clustering on each week's number and its weekly new cases. I test K from
two to six and pick K equals 3 by the highest silhouette score, 0.705, cross-checked against the WCSS
elbow - both agree. What the clusters reveal is exactly what the straight line hid: the growth was not
steady, it came in waves. Most strikingly, the algorithm isolates a single mega-surge - around 4.46
million new cases a week, across weeks 102 to 106, which is January 2022, the Omicron wave - as its own
distinct cluster. That one cluster ran at roughly seven times the overall weekly average. Clustering
turns 'cases went up' into 'here is exactly when, and how hard.'"

### Slide 6 - Graph analytics  (~0:55)

"Now the decision step. I connect the US to two of its neighbours - Canada and Mexico, which as the
brief requires do not border each other - and weight each link by how strongly that neighbour's
weekly new cases correlate with the US. Canada comes in at 0.85, a strong correlation; Mexico at 0.70. The obvious
reading is that Canada's waves move almost in lockstep with the United States, so Canada is the one to
warn. But that same-week correlation is answering the wrong question. It asks whether two curves *look*
alike. What a neighbour actually needs to know is whether its own wave arrives *after* the American one -
because if both peak in the same week, there is nothing to warn about."

### Slide 7 - Lead-lag: who can actually be warned?  (~1:10)

"So I recomputed the correlation at a range of time offsets, sliding each neighbour's series against the
US week by week, from four weeks early to six weeks late. I fixed the decision rule before looking:
recommend an early-warning arrangement only if the correlation peaks at a lag of at least one week, and
is at least 0.6 at that lag. The result reverses the ranking. Canada's correlation peaks at *minus* one
week, at 0.88 - meaning Canada moves with, or even slightly ahead of, the United States. There is no
warning window there. Mexico is the opposite: its correlation climbs from 0.70 in the same week to 0.81
when you shift it forward two weeks. Mexico genuinely follows the US, by about a fortnight. The
neighbour that looked weaker is the one that can actually act on the signal."

### Slide 8 - The whole story in one frame  (~0:40)

"This panel ties it together. On the left, the US infection waves coloured by their cluster phase. In the
middle, the same-week correlation that pointed at Canada. On the right, the lead-lag profile that
overturns it. You can read the whole argument left to right: raw cases, then the phases clustering found,
then which neighbour those phases can genuinely warn."

### Slide 9 - Recommendations  (~1:10)

"So what should the neighbours actually do? Mexico is the real early-warning case: at a two-week lag the
correlation is 0.81, so when the US enters a surge phase, Mexico should pre-position testing and hospital
capacity roughly two weeks ahead of its own expected peak. Judging on same-week correlation alone would
have missed this entirely. Canada is the opposite lesson: highly correlated, but synchronous. The US is
not a leading indicator for Canada, so Canada's investment belongs in its own domestic surveillance -
by the time American numbers climb, Canadian ones already are. And for everyone: plan capacity for the
Omicron-style mega-surge cluster, not the steady baseline, because that single cluster carried about
seven times the overall weekly average. Planning for the average is how you get overwhelmed by the peak."

### Slide 10 - Limitations & close  (~0:45)

"Some honest caveats. These are *confirmed* cases, so they reflect testing and reporting as much as
transmission - and the file ends 9 March 2023, just before Johns Hopkins stopped collecting data. On
method: week number is a clustering input, so phases are partly temporal by construction; 'neighbour'
means geography, not real mobility; and I used one lag averaged over three years, when variants actually
moved at different speeds. Correlation isn't causation either - a lagged match could just mean a variant
hit both countries in sequence. Next steps: mobility data, and a lag per wave. But the core result
stands: same-week said Canada. Shift the series two weeks and it says Mexico - the recommendation that
would actually have bought someone time. Thank you."

---

## Recording checklist
- Export `slides.md` to PDF (the `BDA601_Assessment3_Slides.pdf` next to this file) or open it in
  Marp / Google Slides; keep figures large and readable.
- Screen-record the slides with this narration; aim for **8-9 minutes**, hard cap 10:00.
- Submit: notebook (`.ipynb`) + the video file + the slides PDF, zipped.
