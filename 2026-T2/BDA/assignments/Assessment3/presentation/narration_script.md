# BDA601 Assessment 3 - narration script

**Target: ~8:15 of a 7-10 minute video.** Read at a calm pace; numbers are exact from
`outputs/metrics.json`. Audience = the focal country's non-bordering neighbours (policymakers).
Narrate the *decision*, not the code. Times are per-slide; rehearse once to confirm you land under 10:00.

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

### Slide 4 - Predictive modelling  (~1:05)

"I fit a Spark linear regression of cumulative cases on week number for each country. To pick the most
volatile one I rank them by the variance of their *weekly new cases* - a real measure of volatility -
rather than the variance of the cumulative total, which would just pick the biggest country by default.
On that measure the US is clearly the most volatile: 6.4 times ten-to-the-eleven, against 2.5 for India
and 1.6 for France. Its regression slope is about 760 thousand cases a week, with an R-squared of 0.97.
But here's the key point: even an R-squared of 0.97 *hides* the real story. A straight line tells you
the average growth - it can't tell you *when* the surges hit. For that, we need clustering."

### Slide 5 - Clustering reveals the waves  (~1:15)

"So for the US I run K-Means clustering on each week's number and its weekly new cases. I test K from
two to six and pick K equals 3 by the highest silhouette score, which was 0.705 - a clean separation.
What the clusters reveal is exactly what the straight line hid: the growth was not steady, it came in
waves. Most strikingly, the algorithm isolates a single mega-surge - around 4.46 million new cases a
week, across weeks 102 to 106, which is January 2022, the Omicron wave - as its own distinct cluster.
That one cluster ran at roughly eight times the average weekly load. Clustering turns 'cases went up' into 'here is exactly when, and how hard.'"

### Slide 6 - Graph analytics  (~1:00)

"Now the decision step. I connect the US to two non-bordering neighbours - Canada and Mexico, which
don't border each other - and weight each link by how strongly that neighbour's weekly new cases
correlate with the US. Canada comes in at 0.85, a strong correlation; Mexico at 0.70. In plain terms,
Canada's waves move almost in lockstep with the United States. That makes Canada the strongest
candidate to use the US trajectory as an early-warning signal."

### Slide 7 - The whole story in one frame  (~0:45)

"This panel ties it together. On the left, the US infection waves coloured by their cluster phase; on
the right, how strongly each neighbour's curve correlates with the US. You can read the entire argument
left to right: raw cases, then the phases clustering found, then the neighbour most exposed to them."

### Slide 8 - Recommendations  (~1:15)

"So what should the neighbours actually do? For Canada, with a 0.85 correlation: treat the US trajectory
as a leading indicator. When the US enters a surge phase, pre-position testing and hospital capacity one
to two weeks ahead - don't wait for your own numbers to climb. For Mexico, at 0.70: the coupling is
moderate, so watch US surges but weight your own local signals more heavily. And for everyone: plan your
capacity for the Omicron-style mega-surge cluster, not the steady baseline - because that single cluster
carried about eight times the average weekly load. Planning for the average is how you get overwhelmed
by the peak."

### Slide 9 - Limitations & close  (~0:50)

"Two honest caveats. On the data: these counts are cumulative and depend on each country's reporting,
and the Johns Hopkins series stopped on the 10th of March 2023. On the method: I used week number as a
clustering input, so the phases are partly temporal by construction, and 'neighbour' here means
geography, not true population mobility. The next steps would be to model weekly new cases directly, add
mobility and vaccination data, and test the lead-lag explicitly to quantify the warning window. But the
core result stands: data turned a wall of numbers into a concrete, actionable warning for neighbours.
Thank you."

---

## Recording checklist
- Export `slides.md` to PDF (the `BDA601_Assessment3_Slides.pdf` next to this file) or open it in
  Marp / Google Slides; keep figures large and readable.
- Screen-record the slides with this narration; aim for **8-9 minutes**, hard cap 10:00.
- Submit: notebook (`.ipynb`) + the video file + the slides PDF, zipped.
