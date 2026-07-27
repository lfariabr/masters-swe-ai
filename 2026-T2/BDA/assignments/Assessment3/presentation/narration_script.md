# BDA601 Assessment 3 - narration script

**Target: ~9:00 of a 7-10 minute video, across 10 slides.** Read at a calm pace; numbers are exact from
`outputs/metrics.json`. Audience = the focal country's non-bordering neighbours (policymakers).
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
That one cluster ran at roughly seven times the overall weekly average. Clustering turns 'cases went up' into 'here is exactly when, and how hard.'"

### Slide 6 - Graph analytics  (~0:55)

"Now the decision step. I connect the US to two non-bordering neighbours - Canada and Mexico, which
don't border each other - and weight each link by how strongly that neighbour's weekly new cases
correlate with the US. Canada comes in at 0.85, a strong correlation; Mexico at 0.70. The obvious
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

### Slide 10 - Limitations & close  (~0:50)

"Some honest caveats. On the data: these are *confirmed* cases, so they measure testing and reporting as
much as transmission, and the Johns Hopkins series stopped on the 9th of March 2023. On the method: I
used week number as a clustering input, so the phases are partly temporal by construction; 'neighbour'
here means geography rather than true population mobility; and I fit a single lag averaged over three
years, when different variants clearly travelled at different speeds. And correlation is not causation -
a lagged match may simply mean a new variant reached both countries in sequence. The natural next steps
are mobility and vaccination data, and a lag estimated per wave rather than once. But the core result
stands: the same-week number said Canada. Shifting the series by two weeks said Mexico - and that is the
recommendation that would actually have bought someone time. Thank you."

---

## Recording checklist
- Export `slides.md` to PDF (the `BDA601_Assessment3_Slides.pdf` next to this file) or open it in
  Marp / Google Slides; keep figures large and readable.
- Screen-record the slides with this narration; aim for **8-9 minutes**, hard cap 10:00.
- Submit: notebook (`.ipynb`) + the video file + the slides PDF, zipped.
