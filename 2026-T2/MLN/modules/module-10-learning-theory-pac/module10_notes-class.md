# Module 10 - Class Notes (Week 10 live session)

Extracted from `MLN601 - Machine Learning - Lecturer Week 1 - Week 12` (Teams recording, week 10 segment, ~1h35m).
Facilitator: Dr Kamran Shaukat. Transcript on file: `~/Downloads/MLN601-lecture-20260803-transcript.txt`.

> **Shape of the session:** ~8 min assessment admin (A2 marked, feedback releasing that day; A3 due
> **Wednesday of Week 12**) → **Week 9 recap** (clustering, distance metrics, K-means) → **next-week teaser**
> (anomaly detection + association analysis, both *off-curriculum* but "a graduate should know them") →
> **PAC main lecture** (ε, δ, error region, the 4-strip derivation, a worked sample-complexity example) →
> **slides walkthrough** (hypothesis in 3 senses, `h` vs `H`) → **Module 11 preview: the perceptron**.
>
> ⚠️ **Short lecture by design.** He deliberately kept it brief so students could start A3. The PAC material
> tracks the readings closely, but three things are **lecture-only**: the **1,753-sample worked example**, the
> **ε/4 four-strip error-region derivation**, and the **anomaly/association-analysis preview**.

---

## 1. Week 9 recap (his framing)

Quick sweep before the new topic - all covered in `module09_notes-class.md`, so just the spine:

- **ML** = "a branch of AI which performs various actions without explicitly being programmed." Supervised = label
  known; unsupervised = "you don't have any idea what you're going to do, you just explore."
- **Distance metrics:** Euclidean (square then root - kills the sign, then re-normalises), Minkowski (`r=1`
  Manhattan / `r=2` Euclidean / `r=∞` supremum), Jaccard, simple matching coefficient, cosine similarity.
- **Cluster analysis:** intra-cluster (minimise distance, maximise similarity - cohesive) vs inter-cluster
  (maximise distance - "between the states", NSW to Victoria).
- **Types:** hierarchical vs partitional; exclusive vs non-exclusive; partial vs complete.
- **K-means:** pick k centroids randomly → assign each point to nearest centroid → repeat until no point changes
  cluster. **K-medoids** uses the median instead of the mean. Struggles with varying **densities, sizes, and
  non-globular shapes**. **DBSCAN / OPTICS** (density-based, off-curriculum) don't need k specified up front.

---

## 2. Next-week teaser (lecture-only - OFF the MLN601 curriculum) ⭐

He flagged that MLN601 gives unsupervised learning only **one lecture** (straight to K-means), so he'll add two
more unsupervised topics next week even though they're not assessed - because *"somebody will ask you a very
general question that every person who passed a machine learning course should know, and you'll say I don't know
that concept."* Worth a line in your vocabulary.

- **Outlier / anomaly detection** - unsupervised task, finds the points that don't fit. (Ties straight back to
  Dr Kamran's own Module 9 malware paper - the one-class SVM boundary *is* anomaly detection.)
- **Association analysis** - finds which items co-occur; the classic algorithm is **a priori**. His examples:
  - chips shelved next to a fridge of drinks (unrelated categories, but people buy them together);
  - halal meat sold inside traditional grocery shops;
  - medical family-history links (cardiac / diabetic risk);
  - **recommendation engines** - playlists and movie suggestions are association, *not* clustering ("a horror
    movie and a love movie aren't similar, yet they're recommended together because you watched both").
  - A student (Renato) connected it to **social-network recommendation algorithms** mapping hidden links between
    users, interests, and behaviour - Dr Kamran confirmed and said he'll cover the **a priori algorithm** next week.

> **For Module 11:** expect **perceptron + anomaly detection + association analysis (a priori)** bundled
> together next week. The perceptron is the assessed one; the other two are "graduate general knowledge."

---

## 3. PAC - the main lecture

His one-line goal, almost verbatim: *"PAC learning is a framework for the mathematical analysis of machine
learning - same family as error analysis and the confusion matrix, but it's a **framework**. The goal is: with
high probability (**probably**), the selected hypothesis will have low error (**approximately correct**)."*

### 3.1 The everyday intuition (his on-ramp)
- You run a decision tree and claim **95% accuracy** → error rate 5%, "which is okay for you."
- The **plus/minus 10% margin** analogy: a 1,000-word report accepted at 1,050 words; a 12:00 deadline accepted at
  12:30. *"You're giving a bit of margin in the error."* That margin **is ε**.
- **Two parameters that matter:** how much error you'll tolerate (**ε**), and how confident you are you'll hit it
  (**1 − δ**).

### 3.2 The two dials (his words)
| Symbol | His phrasing | Meaning |
|---|---|---|
| **ε** (epsilon) | *"upper bound on the error in accuracy"* | max acceptable error - hypothesis is "approximately correct" if error ≤ ε |
| **δ** (delta) | *"probability of failure in achieving this accuracy"* | so **confidence = 1 − δ** - how sure you are you'll stay under ε |

- **The worked mini-example:** ε = 5%, confidence = 80% (so δ = 0.2). Ten hypotheses generated; count how many
  land within the error limit. **Hypothesis 1:** 8 of 10 within limit → 80% ≥ 80% → **PAC ✅.** **Hypothesis 2:**
  only 7 of 10 within limit (three bad values: 0.06, 0.059, 0.55) → 70% < 80% → **not PAC ❌.**

### 3.3 The error region (the medium-build example) ⭐ lecture-only derivation
- Setup: predict **medium-build or not** from **height + weight** (two features → a Boolean label). Same shape as
  "COVID / not", "fraud / not", "will play tennis / not".
- **C** = the true concept boundary; **H** = your model's learned boundary. They never match exactly → the gap
  between them is the **error region**.
- **The XOR framing:** error is where **C and H disagree**. Lay it out like a truth table - `0-0` and `1-1` agree
  (true negative / true positive, no problem); `0-1` and `1-0` disagree → **false positive + false negative** →
  *that's* the error region.
- **Don't make the boundary too tight:** a hypothesis clamped hard around the positives turns every nearby point
  into a false negative. You *want* a cushion of ε on each side.
- **The 4-strip derivation** (this is the bit the readings skip): error leaks from **all four sides** of the
  rectangle boundary → total error = sum of **four rectangular strips**. To keep the total ≤ ε, allow **≤ ε/4 per
  strip**. Push that inequality through the probability algebra (probability a positive lands in a strip; that all
  m samples miss it; the factor of 4 for four strips) and you get the sample-complexity theorem.

### 3.4 The sample-complexity punchline
- **Result:** to guarantee accuracy ε with confidence 1 − δ, pick sample size **m ≥ (4/ε) · ln(4/δ)** (his
  rectangle-hypothesis form).
- **His worked number:** want **99% correctness (ε = 1%)** with **95% confidence (δ = 5%)** → plug in → **≈ 1,753
  samples** needed for the learner to learn this concept. *(Memorise the shape, not the digits: tighter ε or
  higher confidence → more data.)*

### 3.5 How he tied it to your assessments
This is the reason the topic is graded at all (SLO a + d, no code):
- PAC's ε/confidence *is* the **"success criteria"** you set in the **business-understanding** phase of CRISP-DM.
- In the **modelling / evaluation** phase you must state **whether you met that target** - "I said I'd hit 80%
  accuracy; did I?" That sentence is literally a PAC statement.
- In **deployment** you say what went wrong and how you'd improve. His A2 feedback comment was exactly this:
  *"clearly mention whether you met your defined success criteria or not."*
- Different models (decision tree, logistic regression, Naive Bayes, SVM) give different error because *"their
  boundary is slightly different to the exact hypothesis"* - No-Free-Lunch, seen from the boundary.

---

## 4. Slides walkthrough - hypothesis in three senses

He shared the `w10_PAC.pdf` slides and walked the **hypothesis** disambiguation (Brownlee's exact point):

| Field | Meaning (his words) |
|---|---|
| **Science** | a provisional explanation that can be **confirmed or disproved** ("the Earth is stationary" - prove or disprove it) |
| **Statistics** | a **probabilistic** claim about a relationship - e.g. *"did hybrid/online classes improve student learning?"*; **null** hypothesis negates it |
| **Machine learning** | a **candidate model** that approximates the target function mapping input → output |

- **`h` vs `H`:** lowercase `h` = a single hypothesis; capital `H` = the **space** of all possible hypotheses.
- **Function approximation:** supervised learning = *"use available data to learn a function that best maps input
  to output on all possible observations"* - and "approximate" is where PAC re-enters.
- **Good hypothesis = testable** → you always carry a **null** (no effect) and an **alternative** (try a different
  model if the first fails).
- He pointed at a **1,000+-view external recording** in the resources as an alternative explanation, noting the
  slides go a bit deeper than the live session on the formula.

---

## 5. Student Q&A (worth keeping)

- **Renato → association analysis powering social networks?** Confirmed; a priori algorithm coming next week.
- **Luis (you) → "PAC is a framework stating perfect learning isn't possible, so it forces us to aim to be right
  almost always - a theory layer on top of the CRISP structure to guide us?"** Dr Kamran: *"That's true, that's
  true."* → your Module 10 mental model is confirmed correct, from the source.

---

## 6. What this adds beyond the readings / study-mode notes

- ✅ **Validates** `module10_notes.md` almost point-for-point (ε = accuracy, δ = confidence; h vs H; hypothesis in
  three senses; Occam-style boundary/cushion). Your study-mode read was accurate.
- ➕ **New lecture-only material** to fold into revision:
  1. the **ε/4 four-strip error-region derivation** (why sample complexity has the `4/ε` shape);
  2. the **worked number: 99% + 95% → ~1,753 samples**;
  3. the **CRISP-DM success-criteria = PAC** framing (directly reusable language for A3's writeup);
  4. the **anomaly-detection + association-analysis (a priori)** preview → **Module 11** alongside the perceptron.
- 🎯 **A3 reminder from the horse's mouth:** due **Wednesday of Week 12**; A2 feedback out; A3 walkthrough next
  class. State your **success criteria up front** and **whether you met them** - that's the PAC lens graded via
  SLO d).
