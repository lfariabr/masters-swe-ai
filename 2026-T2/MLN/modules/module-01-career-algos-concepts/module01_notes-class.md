# MLN601 · Module 1 — Class Notes (Live Lecture)

> Dr. Kamran Shaukat · Week 1 lecture (1h52m). Lean recap of the live session.
> Companions: [one-pager](module01_one-pager.md) · [reading notes](module01_notes.md).

## TL;DR
- **AI** = "computer systems capable of performing tasks that typically require human intelligence."
- **Algorithm** = the recipe (step-by-step instructions to learn patterns); **Model** = the trained output after running that algorithm on data.
- **Supervised** (label known) → classification / regression · **Unsupervised** (no label) → clustering / association.
- Clustering goal: **intra-cluster** tight · **inter-cluster** far apart.

## Hierarchy
`Science ⊃ Computer Science ⊃ AI ⊃ ML ⊃ (NN) ⊃ DL`
ML = learns patterns from data and acts on *new, unseen* data **without being explicitly programmed**.

## Data split (school analogy)
**Training** = fit the model (lessons taught) · **Validation** = tune during training (end-of-chapter questions) · **Test** = final performance (final exam).

## Supervised learning — label = the attribute you predict
- **Classification** → categorical target
  - **Binary** (2 classes): spam/ham, fraud/legit, COVID/not
  - **Multi-class** (>2): sunny/rainy/windy, grades HD/credit/pass/fail
- **Regression** → continuous target: house price, temperature, BMI, share price
- Quick test: *predicting a number → regression; predicting a category → classification.*

## Unsupervised learning — no designated label, let the data group itself
- **Clustering**: supermarket aisles, Amazon "related items", Uber ride-share pooling, YouTube playlists.
- **Intra-cluster** similarity = HIGH (same cluster → points close together).
- **Inter-cluster** similarity = LOW (different clusters → far apart, distinct).
  - 🧠 *interstate* = truck NSW→VIC, **between** states → **inter = between** clusters.
- **Outlier / anomaly detection** = unsupervised sub-type (fraud, faulty sensors, cancer cells vs normal).
- *(Reinforcement learning = "learning on the fly", critique/reward, AlphaGo — mentioned, not in this course.)*

## Explainable AI (XAI)
In life-critical use (medical, cyber) accuracy isn't enough — you must know **how** the model decided. A doctor justifies a diagnosis from symptoms; a model must be just as accountable.

## 💡 My in-class insight *(mine — not lectured)*
When Nomair framed his **sentiment-analysis** project as supervised **classification**, it clicked: that's exactly where **logistic regression** lives — despite the word "regression", it's a **classifier** (predicts a category, not a continuous value). Same baseline I used in **ReviewPulse** (TF-IDF + Logistic Regression → positive/negative). Logistic regression returns later in the course outline → revisit properly in **Module 8**.

> 🏷️ Dr. Kamran credited my definition live: *"algorithm is the process/recipe of learning; model is the output generated after applying the algorithm to training data."* ✅

## Course admin (heard in lecture)
3 **individual** assessments — A1 wk4 (linear regression) · A2 wk8 (classification) · A3 wk12 (regression). Extensions: ≤7 days no docs (valid reason); >7 days needs a certificate. *"Apply for the extension, but give 100%."*
