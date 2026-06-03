# DLE602 · Module 1 — Discussion Forum Drafts

> Draft responses for the two Module 1 learning activities. Personalise the `[bracketed]` parts before posting.
> Keep tone: human, specific, no corporate filler.

---

## Activity 1 — Introduce Yourself

> *Task: introduce yourself to the cohort — your background, why you're taking Deep Learning, and what you want to get out of it.*

**Draft post:**

Hi everyone — I'm Luis, a software engineer based in Sydney, currently working as a data analyst at a school while I take this Master's. My path here has been *using* ML and AI tools at work and wanting to understand what's actually happening inside the neural networks underneath.

It's not entirely new ground for me. I built **Review Pulse**, a sentiment classifier trained on ~8,000 labelled Amazon reviews across four product domains, and **ClinicTrendsAI**, which turns customer-survey data into ML-driven insights. So Module 1's framing landed well: my Review Pulse pipeline is exactly the kind of project where the *representation* did the heavy lifting, and Goodfellow et al. (2016) put words to why — deep learning learns its own hierarchical features instead of me hand-engineering them.

What I want from this subject is the step from classical ML to actually building networks: feedforward nets and backprop (Module 2), then CNNs, RNNs and LSTMs. I'm especially curious about the contrast Assessment 1 sets up — starting with a humble **N-gram** baseline (Jurafsky & Martin) before the cohort moves to the deep CNN approach in Zhao, Gui & Zhang (2018). Seeing *why* the N-gram can't cross the representation gap is the lesson I'm here for.

Keen to hear everyone's background and what drew you to deep learning specifically. 👋

*Citations if needed: Goodfellow, Bengio & Courville (2016); Jurafsky & Martin (2008); Zhao, Gui & Zhang (2018).*

---

## Activity 2 — Assessment 2 & 3 Preparation

> *Task: start preparing for the group project (Assessment 2 proposal + Assessment 3 implementation). Share early project directions, possible datasets/papers, and signal whether you're forming or looking to join a group.*

**Draft main post:**

For the group project I'd love to rally a team around aspect-based sentiment analysis — basically "Review Pulse v2". My Review Pulse classifier only gives one polarity per review, but a sentence like "the food was great but the service was slow" really deserves two opposite labels. ABSA predicts sentiment per aspect (food = positive, service = negative), which is a genuinely deep-learning problem — it needs learned representations and attention, not bag-of-words.
Source code of the project: https://github.com/lfariabr/review-pulse/

It also lines up with where the subject is heading: Assessment 1's N-gram model is the sentence-level baseline that can't separate aspects, so the natural arc is A1 baseline → propose ABSA in A2 → build it in A3. I'm picturing an attention-LSTM (Wang et al., 2016) and a fine-tuned transformer, plus an attention-heatmap view to see which words drive each aspect's sentiment. I'd use SemEval-2014 Task 4, which is already annotated by aspect, so we don't burn the project labelling data.

I'm a software engineer, so I'm happy to own the Python implementation and a live demo — looking for 1-2 people, ideally someone keen on the literature/writing side so we balance things out. Open to pointing it at a different domain (clinic or customer feedback) too. Reply if aspect-level sentiment sounds interesting!

---

**Peer reply — for a peer who proposed a project topic or is looking for a group:**

Like this direction — and it fits the A2 rubric well if we frame the problem statement and aim tightly early (that's 20% of the marks right there). One thing I'd add from Module 1: whichever task we pick, it helps to name the *representation* the deep model is meant to learn that a shallow baseline can't — that's the justification the literature review needs to build toward. Are you set on the dataset yet, or still scoping? I can take the implementation/reproducibility side for A3 if we team up.

---

### Notes for posting
- Both activities are participation-graded; substance + citing the module readings is what's rewarded.
- Swap the `[bracketed]` placeholders and the candidate papers/datasets for the real ones once the group settles.
- A2 and A3 are **group** assessments — Activity 2 is effectively your chance to recruit/position, so keep the "what I can own" line concrete.
- The peer reply is generic — match it to whichever classmate's post you actually respond to.
