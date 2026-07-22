# Module 8 - Class Notes (Week 8 Live Lecture)
## Recurrent Neural Networks & LSTM · Dr. Tayab Din Memon

> **Source:** Week 8 live lecture, 22 July 2026, ~1h31m (Teams recording). Captures what the **lecture** added on top of the four readings in [module08_notes.md](module08_notes.md). Where they overlap (recurrence, BPTT, vanishing gradient, gates) the resource notes carry the depth. **This was also the class where our group presented Assessment 2 live.**

---

## TL;DR
- **Order is the whole point.** His opener: *"the dog chased the cat"* vs *"the cat chased the dog"* - same five words, different order, opposite meaning. Feedforward nets cannot remember order; that is the gap RNNs fill.
- **The hidden state IS the memory.** *"The main change between the normal neural network and recurrent neural network is a hidden state, and this hidden state acts as a memory."*
- **New content not in my resource notes: the input/output structures** (one-to-one, one-to-many, **many-to-one**, many-to-many) and which task each fits. He quizzed it and the answer for a customer review is **many-to-one**.
- **His LSTM analogy: the waiter.** A waiter working a 5-hour shift with hundreds of customers cannot remember every detail - he keeps what matters and forgets the rest. That is the forget gate.
- 🔴 **We presented Review Pulse (A2) live.** He liked the differentiator but gave **two pointers** (dataset sufficiency + "why compare two LSTM variants?"). Details in §6.
- 🔴 **A NEW reflection activity was assigned** (critique a generative-AI answer about LSTM vs RNN) - see §7.

---

## 1. Why feedforward fails, and the memory fix
- **The framing question:** *"Does the order of information matter?"* → *"the dog chased the cat / the cat chased the dog... just by changing the order, the context changes. Order of the words is very important."*
- **Traditional feedforward cannot remember order.** *"In a simple feedforward neural network, they have an input link, hidden link, and output - that's it... Each word may be treated without remembering the words that happened earlier. There is no way to store information."*
- **The shared feature of all sequential data** (his exact phrasing): *"the current prediction depends on information from earlier steps."* His examples: music, temperature, stock market, heart rate, website activity over time, frames in a video.
- **Answer = memory** → the **hidden state**. New hidden state = f(current input + previous memory), initial memory = 0.
- **The maths he showed:** `h(t) = activation(W·h(t-1) + U·x(t) + b)`. He framed it as *"kind of a linear regression"* extended: a normal neuron is `activation(W·x + b)`; the RNN adds the `W·h(t-1)` term. That single extra term is the entire difference.

### His sentiment examples (reuse these - they are his own)
| Example | Point |
|---|---|
| *"The movie was **not** very good"* | remove "not" and the sentiment flips. The net must store **both** "not" and "good" |
| *"The service was excellent"* → positive · *"The service was **not** excellent"* → negative | the hidden state has to carry the negation forward |
| *"The film was surprisingly **good**"* | he asked which word most changes the hidden state → **"good"**, because it carries the sentiment |
| *"I grew up in **France**... I speak fluent **French**"* | the long-range dependency; a vanilla RNN **struggles to connect them when many words sit in between** |

## 2. 🆕 Input/output structures (NOT in the readings - examinable)
| Structure | Typical task |
|---|---|
| **One-to-one** | image classification |
| **One-to-many** | image caption generation |
| **Many-to-one** ⭐ | **sentiment analysis / classifying an entire review** |
| **Many-to-many** | machine translation, sequence labelling |

- 🔴 **His quiz:** *"Which structure would you use to classify an entire customer review?"* → **many-to-one**. Reason he gave: *"you have so many words, you have to just bring one word out of that as a sentiment."*
- **Nuance he added:** many-to-many only applies to translation-style output, because you need a *continuous* sequence out. Even a Likert-scale sentiment (strongly positive / positive / neutral...) is still **one class out**, so still many-to-one.

## 3. BPTT and the vanishing gradient - his version
- **Gradient, defined by him:** *"a derivative, collection of partial derivatives showing how the loss changes with respect to each weight."* (Matches the textbook exactly.)
- **Weight update equation he showed:** `w ← w - η · (∂L/∂w)`, where `η` = learning rate. *"The job of the optimizer is to look at the direction and update the weight accordingly."*
- **BPTT** = backprop, but *"through time"* - the error propagates backwards **through the sequence**, adjusting the **shared** weights based on how earlier timesteps contributed to the error.
- **Why it breaks (his causal chain):** every step multiplies by the hidden state → the network becomes very complex → *"that complexity impacts upon gradient calculation"* → *"the gradient becomes weak... it's not supporting to update the weights as it can predict correctly."*
- **Vanishing in his plain terms:** *"weights are not updated as quickly and appropriately as required."* Result: the **earliest** neurons never get updated properly, so early-sequence information is never learned.
- **Exploding** = *"gradient becomes very heavy instead of thin"*, but he was explicit: **the main issue is vanishing**.
- **Other RNN costs he listed:** sequential computation is slow, and compute cost for long sequences is too high.

## 4. LSTM - the waiter analogy and the gates
- 🔵 **The analogy worth reusing:** *"if you go to a restaurant and there is a waiter, and the waiter is serving... the restaurant is open for five hours and there are hundreds of customers visiting, then it's not necessary for a waiter to remember each and every detail of five hours. So it has to keep some information and it has to remove or forget other that is not necessary. That is basically the context of LSTM."*
- **The design principle in one line:** *"do not memorize everything, just remember the important components."*
- **Cell state** = *"a long-term memory path through the sequence"*. It is the **additional** input/output vs a plain RNN.
- **Gates:** forget (what to discard), input (what to add), output (what to emit). *"0 means block or forget information, 1 means retain or allow information."* The **forget gate is the additional thing** vs an RNN.
- **Flow:** forget → update → create new cell state → produce output.
- **His worked example:** *"The movie appeared interesting at first but the ending was disappointing."* The LSTM remembers the topic is a movie, stores "interesting" as positive, recognises **"but"** as a change signal, **reduces the importance of the earlier positive**, stores "disappointing", and predicts negative overall. He explicitly linked this to our project.

### 🔴 Delta vs the textbook - GRU
He said: *"GRU is enhanced version of LSTM. It has two main gates instead of three... and it's better than LSTM to some extent, it overcomes the LSTM issues."* His comparison table:

| | Gates | Training complexity | Common use |
|---|---|---|---|
| **Basic RNN** | none | lower | simple sequences |
| **LSTM** | 3 | higher | complex, longer sequences |
| **GRU** | 2 | moderate | efficient sequence modelling |

> ⚠️ **Careful:** Goodfellow §10.10.2 is more cautious - Greff et al. (2015) and Jozefowicz et al. (2015) found **no variant clearly beats both** LSTM and GRU across tasks. His "GRU is better" is a practical generalisation, not a settled result. In a written answer, prefer the hedged version and cite Goodfellow.

## 5. CNN vs RNN - his table (Activity 1 gold)
| | CNN | RNN |
|---|---|---|
| Pattern type | **spatial** | **sequential** |
| Common data | images | sequences |
| Processing | inputs **independently**, **in parallel** | uses **previous states**, **step by step** |
| Memory | not required | **required** |
| Good for | spatial **feature extraction** | **order and context** |

- 🔴 **His own caveat, which is exactly the Activity 1 "when would you still prefer CNN" answer:** *"CNN can also be used for some sequential problems, **particularly when local patterns are more important than long-term dependencies**."*
- **His CNN-or-RNN quiz (all confirmed in class):** objects in a photograph → **CNN** · sentiment of a review → **RNN** · recognising spoken words → **RNN** · visual defect in a product → **CNN** · next value in a sensor sequence → **RNN**.

### Applications he listed
Sentiment analysis · speech recognition · **energy demand forecasting** · weather prediction · financial forecasting · **predictive maintenance** · healthcare monitoring.
- 🔵 **His own published work:** LSTM for **predictive maintenance in railway projects**, and **motor health monitoring**. Worth mentioning back to him - it is his research area.
- 🔵 **His energy example maps 1:1 onto the Laib et al. (2019) reading:** inputs = historical consumption, time of day, day of week, weather, seasonal patterns.

---

## 6. 🔴🔴 Assessment 2 - we presented, and his feedback

**Status: A2 presented live on 22/07/2026** (Luis / Victor / Juan). Order in class: Lhendup+Bikash's group (crop leaf disease detection) first, us second, Timothy's group not ready.

**What we pitched:** Review Pulse aspect-based sentiment - the ladder TF-IDF → LSTM (no target) → **ATAE-LSTM** → DistilBERT, on SemEval-2014 restaurants, with attention heat-maps as the explainability differentiator and a Streamlit demo for A3.

**His verdict:** *"It is a good project"* and *"thank you for a very nice presentation, I really liked it."* He specifically liked **the differentiator**: *"in such kind of conflicting comments, where positive and negative both are going, instead of averaging, you are bringing some pointers."*

### 🔴 Pointer 1 - dataset sufficiency / imbalance
> *"There should be **enough samples, differentiator samples**, because usually people write feedback in a positive way or negative way, mostly positive way. So there should be enough samples for the context that you are bringing."*

Translation: he is worried we will not have **enough reviews that actually contain conflicting aspects** (the exact cases our differentiator exists to solve). **Action for A3:** report the count of multi-aspect / conflicting-sentiment reviews and the class balance per aspect polarity, not just total rows.

> ⚠️ **Correction we need to make.** When he asked the dataset size, Luis answered *"around on the thousands"* and Tayab replied *"100,000, yeah."* **Neither is right.** SemEval-2014 Task 4 restaurants is roughly **3k training sentences** - genuinely small. That makes his imbalance concern **more** valid, not less. Get the exact number into the report before submission.

### 🔴 Pointer 2 - "why two LSTM variants?"
> *"While comparing 2 LSTM variants, **what value addition would be in your project?** ... Why not choose any other algorithm and comparing? Just from your learning perspective - your learning could be enhanced if you consider these aspects."*

Translation: comparing an LSTM baseline against ATAE-LSTM looks like comparing two flavours of the same thing. He wants **architectural diversity** in the comparison. **Action for A3:** either (a) lean on the fact that the ladder already spans four *different* families (TF-IDF/linear → CNN or plain LSTM → attention-LSTM → transformer), and say so explicitly, or (b) swap the aspect-agnostic LSTM baseline for a genuinely different model. Framing it as **four families, not two LSTMs** answers him directly.

- He will write **formal feedback after the report is submitted**; the in-class comments were instant feedback.
- A2 report still due **26/07/2026**. **A3 due 19/08/2026** - he expects the crop group's 99% vs 64% lab-versus-field honesty framing, and our aspect work, to show up in the final.

---

## 7. 🆕 NEW reflection activity he assigned (do this)
> Ask a **generative AI tool**: *"LSTM is always better than a basic RNN because it has more memory - is this statement correct?"* Then **critique the AI's answer** against these checks:
> 1. Is the claim **too general**?
> 2. Does it explain the **role of the gates** correctly?
> 3. Does it consider **computational cost**? (*"LSTM training is very expensive. RNN training is expensive than CNN."*)
> 4. Does it consider **short and simple sequences**?

Post the response on the **discussion forum** - he said to put it under the existing RNN-vs-CNN activity, or he may create a separate reflection thread. *"A short response is enough, but please write your response."*

- 🔵 **We are well positioned:** our forum answer already argues LSTM is *not* always better (≈4× more parameters, overfits on small data), and Review Pulse has the empirical proof (BiLSTM 81.0% losing to TF-IDF 82.7%).

---

## 8. Module 7 recap quiz he ran first (answers)
- Purpose of a basic autoencoder → **reconstruct / compress the input** (not decision trees).
- Bottleneck layer represents → **the compressed representation of the input**.
- Autoencoder trained on corrupted input → **denoising**.
- Loss to compare input with reconstruction → **MSE**. 🔴 *"Accuracy is not a loss function"* - accuracy/precision/recall are for **discrete** outputs; reconstruction loss measures actual minus predicted.
- He restated that autoencoders are dimensionality reduction but **non-linear**, unlike PCA.

---

### Day-job anchors
1. **Many-to-one is your default shape.** Any "read a whole record/sequence, emit one label" job at the school - flagging an at-risk student from a term of weekly attendance rows - is many-to-one, exactly like review sentiment.
2. **The waiter analogy is the forget gate**, and it is also your ETL: you do not persist every raw event, you keep the fields that matter for the next decision and drop the rest.
3. **His energy-forecasting example is your enrolment forecast:** historical values + time of day + day of week + seasonality. Same input recipe, different domain.

---

## References
Full citations live in **[module08_notes.md](module08_notes.md)**.
- **Goodfellow Ch.10** - Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning.* MIT Press. https://www.deeplearningbook.org/
- **Kelleher Ch.5** - Kelleher, J. D. (2019). *Deep learning.* MIT Press.
- **Laib et al. (2019)** - LSTM for natural-gas consumption forecasting. *Energy, 177*, 530-542. https://doi.org/10.1016/j.energy.2019.04.075
- **Wang et al. (2016)** - Attention-based LSTM for aspect-level sentiment classification (ATAE-LSTM). *EMNLP 2016*, 606-615. https://aclanthology.org/D16-1058/
- **Dr Tayab Din Memon** - week-8 live lecture, 22 July 2026; his own published LSTM work on railway predictive maintenance and motor health monitoring.
