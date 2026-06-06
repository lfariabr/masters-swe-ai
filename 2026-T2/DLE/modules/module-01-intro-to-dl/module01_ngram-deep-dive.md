# N-Gram Language Models — Deep Dive (DLE602 Assessment 1)

> Study consolidation from an assisted active-recall session. Anchored to two things I already know: **SQL/warehouse tables** and **my own Assessment 1 code** (`assignments/Assessment1/code/dle602_sentiment_ngram.py`). Built to be re-run as active recall later — see the **Self-test** at the bottom.

---

## TL;DR — the 5 things

1. **An N-gram model is just a GROUP BY counts table.** Training = counting; predicting = a divide.
2. **Markov assumption**: approximate the full history by only the last **N−1** words. Price = no long-range context.
3. **MLE** turns counts into probability: `P(word | context) = C(context, word) / C(context)`.
4. **Zero problem**: an unseen n-gram has count 0 → probability 0 → `log(0) = −∞` → the classifier goes blind. **Smoothing** is the fix (the `COALESCE` for missing keys).
5. **More N → more sparsity.** Possible bigrams = V², trigrams = V³. With fixed data, trigrams almost never recur, so smoothing dominates and accuracy drops — which is exactly why my **bigram (0.72) beat my trigram (0.55)**.

---

## The warehouse mental model (the anchor)

A trained bigram model is **two aggregation tables**:

```sql
-- ngram_counts  →  in code: self.ngram_counts  (a Counter)
SELECT prev_word, word, COUNT(*) AS c
FROM   bigrams
GROUP  BY prev_word, word;

-- context_counts  →  in code: self.context_counts  (a Counter)
SELECT prev_word, COUNT(*) AS c_ctx
FROM   bigrams
GROUP  BY prev_word;
```

Predicting the probability of a word is a **JOIN + divide**:

```sql
SELECT prev_word, word, c * 1.0 / c_ctx AS prob
FROM   ngram_counts JOIN context_counts USING (prev_word);
```

Everything below is a refinement of this one idea.

---

## Concept 1 — What an N-gram LM is, and the Markov assumption

A **language model** assigns a probability to a word sequence / predicts the next word given the words before it. The "true" probability `P(wₙ | w₁ … wₙ₋₁)` conditions on the *entire* history — impossible to estimate (infinite combinations, almost all unseen).

**Markov assumption**: assume only the last **N−1** words matter.

```
P(wₙ | w₁ … wₙ₋₁)  ≈  P(wₙ | wₙ₋(N₋₁) … wₙ₋₁)
```

> ⚠️ **Off-by-one (the classic trap):** the number in the name counts the **target word too**.

| Model | N | Context words (N−1) | Conditions on |
|---|---|---|---|
| unigram | 1 | **0** | nothing — raw word frequency `P(w)`, ignores order entirely |
| **bigram** | 2 | **1** | the 1 previous word |
| **trigram** | 3 | **2** | the 2 previous words |

**The price of Markov:** anything older than N−1 words is thrown away → no long-range dependencies.
🔗 *A1 evidence:* my model misread *"...no. it is too big. I'm quite happy with the Kindle2"* (true=positive, pred=negative). The positive cue "happy" is too far from the local context — a bigram can never connect them. **That error is the Markov price in action.**

---

## Concept 2 — MLE: counts → probability

The **Maximum Likelihood Estimate** of the bigram conditional probability:

```
P(wₙ | wₙ₋₁) = C(wₙ₋₁, wₙ) / C(wₙ₋₁)        (bigram count ÷ context count)
```

🔗 *Code:* this is the `numerator / denominator` inside `NGramSentimentModel._logprob()`.

---

## Concept 3 — Why log probabilities

A tweet's probability is the **product** of its n-gram probabilities. Each one is tiny (e.g. `~0.0003`). Multiply ~15+ of them:

- **Problem — numerical underflow:** the product becomes so small it rounds to **0** in floating point → information lost. And `log(0) = −∞` then blows up any comparison.
- **Fix:** `log(a · b) = log(a) + log(b)`. So instead of multiplying tiny numbers, **sum their logs**:

```
log(p₁·p₂·…·pₙ) = Σ log(pᵢ)        e.g. (−8) + (−8) + … = −120   (safe range)
```

Bonus: `log` is **monotonic**, so it preserves the positive-vs-negative ranking my classifier relies on.
🔗 *Code:* every score in `_logprob()` is computed with `math.log(...)`; `classify()` compares summed log-probs.

---

## Concept 4 — The zero problem (sparsity)

At test time a bigram like `("kindle2", "rocks")` may never have appeared in training:

```
C("kindle2","rocks") = 0   →   P("rocks" | "kindle2") = 0
P(tweet) = P(b₁) × … × 0 × … = 0          (one zero kills the whole product)
```

Tweets are full of never-seen pairs (slang, typos, hashtags), so **without a fix almost every tweet collapses to probability 0**, and if both the positive and negative models return −∞ the classifier cannot choose. **Fatal.**

🔗 *Warehouse view:* a `JOIN` that misses the key returns `NULL`/0; then `SUM(log(prob))` hits `log(0) = −inf` and the whole aggregate is `−inf`. You need a **default for missing keys** → that default is smoothing.

---

## Concept 5 — Smoothing (add-k / Laplace) = the COALESCE

```
P_smoothed(word | context) = ( C(context, word) + k ) / ( C(context) + k·V )
```

- **`+k` in the numerator** (here k=1, "add-one"): pretend every possible n-gram was seen `k` extra times. The unseen pair now has count `0+1 = 1` → a tiny but **non-zero** probability. The zero problem is gone.
- **`+k·V` in the denominator** (V = vocabulary size): you added `k` pseudo-count to **every** word that could follow the context — that's `k·V` fake counts total. The denominator must grow by the same mass so the distribution still **sums to 1**.
- **Cost (why add-one is "blunt"):** it steals probability mass from seen events and spreads it across the *huge* set of unseen events (V ≈ 49k here), so it over-feeds the never-seen. Backoff (drop to a lower order) and interpolation (mix orders) usually beat it.

🔗 *Code:* exactly the `_logprob()` lines —
```python
numerator   = ngram_count   + self.k                  # +k
denominator = context_count + self.k * self.vocab_size  # +k·V
```

---

## The payoff — why bigram (0.72) beat trigram (0.55) on my data

Possible n-grams explode with N. With my real vocab **V = 49,038**:

| | Possible n-grams | Observed in ~1M training tokens | Situation |
|---|---|---|---|
| **bigram** | V² ≈ **2.4 billion** | ~1M, and **many recur** | sparse, but real co-occurrence evidence survives |
| **trigram** | V³ ≈ **118 trillion** | ~1M, **almost all unique** | near-total sparsity |

At the trigram level almost every test trigram is unseen → `C = 0` → the prediction falls back on the **generic smoothing prior**, not on evidence. The signal drowns. That is why my measured trigram accuracy dropped to **0.420 (STS-Test) / 0.550 (STS-Gold)** vs the bigram's **0.452 / 0.719**.

### Bias–variance framing (precise terminology)
The trigram has **too much capacity for the dataset size** (high variance). It *overfits* — memorises the few triples it saw — but those don't recur at test time, so the prediction collapses onto the generic smoothing prior.
- **Overfitting** = the cause (too many parameters relative to data; great on train, bad on test).
- "Prediction becomes generic/uninformative" = the *consequence*, not "generalising too much" (generalising well would be good).

---

## Map to my Assessment 1 code

| Concept | Where it lives in `dle602_sentiment_ngram.py` |
|---|---|
| Tokenise + Twitter normalisation | `preprocess()` |
| Build the two GROUP-BY count tables (per class) | `NGramSentimentModel.train()` → `ngram_counts`, `context_counts` |
| MLE + smoothing + log | `_logprob()` (`(c+k) / (c_ctx + k·V)`, wrapped in `math.log`) |
| Compare positive vs negative, apply the 25% rule | `classify()` |
| Accuracy / macro-F1 / confusion | `evaluate()` |

---

## Common misconceptions to avoid (ones I actually tripped on)

- ❌ "Unigram = the last word with most weight." → Unigram uses **no context** at all.
- ❌ "Bigram = last 2 words, trigram = last 3." → It's **1 and 2** context words (N counts the target word).
- ❌ "Markov is like backpropagation." → N-grams have **no gradients**; they are pure counting.
- ❌ "The counts table is like TF-IDF." → TF-IDF weights terms for search/similarity; an n-gram LM is **co-occurrence counts → conditional probability**.
- ❌ "Trigram is worse because it generalises too much." → It's **overfitting from sparsity**; the generic output is the symptom.

---

## Self-test (cover the answers, recall first)

1. In one sentence, what does an N-gram LM estimate, and how many context words does a bigram use?
2. State the Markov assumption and name its cost.
3. Write the bigram MLE formula. What is each term in SQL?
4. Why use log probabilities instead of multiplying?
5. Walk through the zero problem and why it is fatal.
6. Write the add-one smoothing formula and explain why the denominator gets `+k·V`.
7. Using "sparsity" and "smoothing", explain why a trigram scored worse than a bigram on short tweets.

<details>
<summary>Answers</summary>

1. Probability of the next word given the previous words; a **bigram uses 1** context word.
2. `P(wₙ|history) ≈ P(wₙ| last N−1 words)`; cost = **no long-range context**.
3. `P(wₙ|wₙ₋₁) = C(wₙ₋₁,wₙ) / C(wₙ₋₁)` = `ngram_counts.c / context_counts.c_ctx` (JOIN on the context, then divide).
4. To avoid **underflow** when multiplying many tiny probabilities; `log` turns the product into a **sum** and is monotonic.
5. Unseen n-gram → `C=0` → `P=0` → the tweet's product = 0 → `log(0)=−∞`; both class models can return −∞ so you can't compare. Tweets are full of unseen pairs → fatal.
6. `P = (C+k)/(C(context)+k·V)`; the denominator grows by `k·V` because `k` was added to **every** word in V, keeping the distribution summing to 1.
7. Possible trigrams (V³) ≫ possible bigrams (V²), so with fixed data almost every trigram is unseen (**sparsity**); predictions fall back on the generic **smoothing** prior instead of real evidence, so accuracy drops.

</details>

---

## References
- Jurafsky, D., & Martin, J. H. *Speech and Language Processing* (3rd ed. draft), Ch. 3 — N-gram Language Models. https://web.stanford.edu/~jurafsky/slp3/3.pdf
- Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253–23260. https://doi.org/10.1109/ACCESS.2017.2776930
- My Assessment 1 implementation: `2026-T2/DLE/assignments/Assessment1/` (`code/`, `report/`, `notebook/`).
