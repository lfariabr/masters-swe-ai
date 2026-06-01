# MLN601 · Module 1 — Discussion Forum Drafts

> Draft responses for the two Module 1 learning activities. Personalise the `[bracketed]` parts before posting.
> Keep tone: human, specific, no corporate filler.

---

## Activity 1 — Self-Introduction & Machine Learning Jobs

> *Task: introduce yourself via the forum and share some of the ML jobs capturing your interest. Consult job sites (LinkedIn, Indeed) and the cited articles.*

**Draft post:**

Hi everyone — I'm Luis, a software engineer in Sydney, now working as a data analyst at a school while I take this Master's. I came in wanting to move from *using* ML tools to actually building and evaluating the models behind them.

It's not new ground: I recently built **Review Pulse**, a sentiment classifier trained on ~8,000 labelled Amazon reviews across four product domains, and **ClinicTrendsAI**, which turns customer-survey data into ML-driven insights. So the `fit → predict → evaluate` loop from this module is already familiar — what I want from the subject is the rigour: clean feature matrices, honest validation, and being explicit about a model's limits.

Two roles have my attention: **ML Engineer** (postings ask for exactly this stack — Python, scikit-learn, preprocessing, evaluation) and **AI/ML Specialist**, which LinkedIn's 2020 Emerging Jobs Report ranked the #1 emerging role (~74% growth, 2016–2020). Townes (2017) sums up why: "skilled in machine learning" is becoming the new "proficient in Excel."

Keen to hear which roles you're all chasing. 👋

*Citations if needed: LinkedIn (2020) Emerging Jobs Report; Townes (2017), Quartz.*

---

## Activity 2 — Machine Learning Applications

> *Task: post 2–3 sentences on what you learned this module and how you'd apply it, then reply to two peers.*

**Draft main post (2–3 sentences):**

The biggest takeaway from this module is that the value of ML lives in a repeatable workflow — frame the target, build features and labels, split train/test, fit, evaluate, then interpret — not in any single clever algorithm. The Target pregnancy-prediction case (Hill, 2012) and the COVID-19 severity study (Jiang et al., 2020) both showed me that accuracy is only half the story: privacy, class imbalance, and external validation decide whether a model is actually *usable*. I'm already applying this in **Review Pulse**, my sentiment classifier trained on ~8,000 labelled Amazon reviews — the same `X → fit → predict → evaluate` loop, where the discipline this module stresses (honest validation, watching for imbalance) matters far more than the choice of algorithm.

---

**Peer reply #1 — for a peer who posted about a *predictive / business* application:**

Really like your example — it maps cleanly onto the Module 1 workflow. The one thing I'd add from the Target case (Hill, 2012) is the ethics edge: when a model predicts something sensitive accurately, "accurate" still isn't the same as "acceptable." Did you think about who the stakeholders are and how each of them would feel about the prediction being made?

---

**Peer reply #2 — for a peer who posted about a *healthcare / high-stakes* application:**

Good pick — this connects straight to the Jiang et al. (2020) COVID-19 study, where the model hit ~80% with KNN/SVM but only had 53 patients and 5 positive cases. That tiny, imbalanced sample is exactly why accuracy alone can mislead and why they stressed external validation before any real deployment. How would you handle the class-imbalance problem if you were building your version of this model?

---

### Notes for posting
- Activity 1 and 2 are graded as participation; substance + citing the module readings is what's rewarded.
- Swap the `[bracketed]` placeholders for real details so it reads as yours, not a template.
- Peer replies are written generically — match them to whichever two classmates' posts you actually respond to.
