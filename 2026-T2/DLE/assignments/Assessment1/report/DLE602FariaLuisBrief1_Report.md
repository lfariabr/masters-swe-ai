# Twitter Sentiment Analysis Using an N-Gram Language Model

**Student:** Luis Faria | **Subject:** DLE602 Deep Learning | **Assessment 1 — Programming Problems**
**Model:** Bigram probabilistic language model | **Datasets:** STS-Test and STS-Gold (Zhao, Gui & Zhang, 2018)

---

## Introduction

Twitter sentiment analysis assigns positive, negative, or neutral sentiment to short, noisy social-media messages. Zhao, Gui, and Zhang (2018) approached this with deep convolutional neural networks; this assessment instead implements the required probabilistic N-Gram language model. Separate positive and negative bigram models are trained from labelled tweets, and a simple threshold rule decides each tweet's sentiment. The same model, preprocessing, and rule are applied to two of the paper's five datasets — STS-Test and STS-Gold — so their outcomes can be compared on identical terms.

## Datasets

Both evaluation sets are drawn from the five datasets used by Zhao, Gui, and Zhang (2018), and were chosen because they are the only two distributed as **full tweet text**: the paper's other sources (SemEval-2014, SS-Tweet) ship only as tweet IDs that now require paid Twitter-API hydration, which would break reproducibility. The pair is also deliberately contrastive — STS-Test carries a neutral class while STS-Gold does not — which directly exposes how the same model handles a three-class versus a two-class source (Table 1).

*Table 1. Datasets used (one training corpus and two evaluation sources).*

| Role | Dataset | Rows | Classes | Source (no login) |
|---|---|---:|---|---|
| Training corpus | Sentiment140 | 80,000 (sample) | neg / pos | cs.stanford.edu |
| Dataset A | STS-Test | 498 | neg / **neutral** / pos | same Stanford zip |
| Dataset B | STS-Gold | 2,034 | neg / pos | github.com/pollockj (Saif et al., 2013) |

## Implementation method

The classifier uses a bigram model (n = 2) with add-one (Laplace) smoothing over a 49,038-token vocabulary, trained on a balanced 80,000-tweet sample of the Sentiment140 corpus (Go et al., 2009). Tweets are normalised by lowercasing, replacing URLs and usernames with placeholder tokens, stripping the hash symbol while keeping the hashtag word, and retaining exclamation marks and negation. For each test tweet, every bigram is scored under both models; a bigram counts as positive or negative when its smoothed conditional log-probability is higher under that model. Following the brief, a tweet is labelled positive when at least one quarter of its bigrams are positive and outnumber the negative ones, negative by the mirror rule, and neutral otherwise.

*Figure 1. Bigram model's training and prediction pipeline.*


```mermaid
flowchart LR
    subgraph TRAIN["TRAINING - build the two language models once"]
        direction LR
        A["Sentiment140<br/>80,000 balanced tweets"] --> B["Preprocess<br/>lowercase, &lt;url&gt;/&lt;user&gt;,<br/>keep negation and !"]
        B --> P["Positive tweets"]
        B --> N["Negative tweets"]
        P --> PM["Positive bigram model<br/>counts + add-one (k=1)"]
        N --> NM["Negative bigram model<br/>counts + add-one (k=1)"]
    end
    subgraph PRED["PREDICTION - identical for STS-Test and STS-Gold"]
        direction LR
        T["Test tweet"] --> T2["Preprocess<br/>same rules"]
        T2 --> S["Score every bigram<br/>log P_pos vs log P_neg"]
        S --> C["Count positive vs<br/>negative bigrams"]
        C --> R["25% rule"]
        R --> O["positive /<br/>negative /<br/>neutral"]
    end
    PM -. "score test bigrams" .-> S
    NM -. "score test bigrams" .-> S
```

## Results and comparison

The two sources produced clearly different outcomes (Table 2). On STS-Gold the model reached 0.72 accuracy and 0.73 macro-F1; on STS-Test it managed only 0.45 accuracy and 0.40 macro-F1. Three factors explain the gap. First, STS-Gold is a two-class problem, whereas STS-Test adds a neutral class the model struggles with: it predicted neutral for only 38 of 498 tweets, far below the 139 truly neutral ones. With Laplace smoothing almost every bigram leans slightly positive or negative, so the 25% threshold is easily crossed and neutral is rarely chosen. Second, STS-Gold's informal tweet style closely matches the emoticon-labelled training corpus, giving denser, more reliable bigram evidence. Third, both datasets share a positive-leaning bias — predicted positives exceed true positives in each — inherited from the training data. The shared model behaviour is therefore consistent, but its usefulness depends heavily on the target source. A capacity sweep makes the model-selection choice concrete (Appendix C): as the N-Gram order rises from unigram to bigram to trigram, training accuracy climbs from 0.71 to 0.93 to 0.99 while the train-test gap widens from 0.25 to 0.48 to 0.57 — the textbook overfitting signature of variance growing with capacity. The trigram memorises the training tweets almost perfectly yet generalises worst (0.42 and 0.55 accuracy), so the bigram is the submitted model; here the add-k smoothing acts as a regularization dial that trades a little training fit for better generalisation.

*Figure 2. Confusion matrices illustrating the model's performance.*

| STS-Test | STS-Gold |
|:--:|:--:|
| ![STS-Test confusion matrix](../outputs/figures/confusion_sts_test.png) | ![STS-Gold confusion matrix](../outputs/figures/confusion_sts_gold.png) |


## Critical reflection

The errors reveal the core limitation of N-Grams. Sarcasm ("worked on 5 bone marrow cases today! All + for cancer!"), emoji sentiment, and long-range negation ("no. it is too big. I'm quite happy") are misread, because local word-pair counts carry no contextual meaning and unseen phrases receive only smoothed probabilities. The model also has no learned concept of neutrality; that class emerges purely from the threshold. These weaknesses are exactly what the deep CNN of Zhao, Gui, and Zhang (2018) addresses through learned word embeddings and wider context.

## Conclusion

The N-Gram model is a transparent, reproducible baseline that classifies tweets reasonably when training and test language overlap, as on STS-Gold, but degrades on harder, multi-class sources such as STS-Test. Its accuracy depends on dataset vocabulary, class balance, and preprocessing rather than genuine language understanding.

---

# Appendices

## Appendix A - Glossary

**Table A1. Glossary of key terms.**

| Term | Definition |
|---|---|
| N-gram | A contiguous sequence of *n* tokens used to model language by counting how often each sequence occurs. |
| Unigram / Bigram / Trigram | N-grams with n = 1, 2, 3. A bigram conditions each word on the **1** previous word; a trigram on the **2** previous words. |
| Language model | A model that assigns a probability to a sequence of words, or predicts the next word given the preceding ones. |
| Markov assumption | The simplification that the next word depends only on the last *n*-1 words, not the full history. Its cost is the loss of long-range context. |
| Maximum Likelihood Estimation (MLE) | Estimating a bigram probability directly from counts: `P(w | prev) = C(prev, w) / C(prev)`. |
| Add-one (Laplace) smoothing | Adding a pseudo-count *k* = 1 to every n-gram so unseen pairs get a small non-zero probability: `(C + k) / (C(context) + k·V)`. Prevents zero probabilities. |
| Vocabulary (V) | The set of distinct tokens seen in training. Here V = 49,038, which sets the denominator term `k·V` in smoothing. |
| Log-probability | The logarithm of a probability. Summing log-probabilities avoids numerical underflow when multiplying many tiny values, and preserves ranking. |
| Out-of-vocabulary (OOV) | A token unseen in training; mapped to a placeholder so the model can still score it via smoothing. |
| 25% rule | The brief's decision rule: label a tweet positive if at least one quarter of its bigrams are positive (and outnumber the negatives), negative by the mirror rule, otherwise neutral. |
| Accuracy | Proportion of tweets whose predicted label matches the true label. |
| Macro-F1 | The unweighted mean of the per-class F1 scores; treats each sentiment class equally regardless of class size. |
| Confusion matrix | A table cross-tabulating true labels (rows) against predicted labels (columns) to expose which classes are confused. |
| Sentiment140 | A 1.6M-tweet corpus auto-labelled by emoticons (0 = negative, 4 = positive); used here as the training source. |
| STS-Test | The Stanford Twitter Sentiment test set (498 manually labelled tweets, three classes including neutral). |
| STS-Gold | A gold-standard Twitter set (2,034 tweets, positive/negative only) from Saif et al. (2013). |

## Appendix B - Results

*Table 2 — Results (bigram model, identical settings)*

| Metric | STS-Test | STS-Gold |
|---|---:|---:|
| Records evaluated | 498 | 2,034 |
| True negative / neutral / positive | 177 / 139 / 182 | 1,402 / 0 / 632 |
| Predicted negative / neutral / positive | 186 / 38 / 274 | 1,110 / 136 / 788 |
| Accuracy | 0.452 | 0.719 |
| Macro-F1 | 0.401 | 0.726 |

## Appendix C - Bias-variance and regularization

The N-Gram order is a model-capacity dial and the add-k smoothing constant is a regularization dial. Sweeping both on the Assessment 1 data (`code/bias_variance_sweep.py`) reproduces the bias-variance trade-off on this exact model: raising capacity lowers bias but raises variance, and stronger smoothing buys some of that variance back.

*Table C1. Capacity dial (add-k fixed at 1.0). Training accuracy rises with capacity while test accuracy falls and the train-test gap widens — the overfitting signature.*

| N-Gram order | Train acc | STS-Test | STS-Gold | Train−Test gap |
|---|---:|---:|---:|---:|
| Unigram (n=1) | 0.71 | 0.46 | 0.69 | 0.25 |
| Bigram (n=2) | 0.93 | 0.45 | 0.72 | 0.48 |
| Trigram (n=3) | 0.99 | 0.42 | 0.55 | 0.57 |

*Table C2. Regularization dial (bigram, add-k swept). Increasing k trades a little training fit for slightly better generalisation on STS-Gold.*

| add-k | Train acc | STS-Gold |
|---|---:|---:|
| 0.001 | 0.94 | 0.69 |
| 0.1 | 0.93 | 0.72 |
| 1.0 | 0.93 | 0.72 |
| 25 | 0.93 | 0.72 |

![Bias-variance sweep](../outputs/figures/bias_variance.png)

*Figure 3. Left: capacity dial — higher N-Gram order memorises the training set and generalises worse. Right: regularization dial — add-k smoothing is the finer knob once capacity is fixed. Generated by `code/bias_variance_sweep.py`.*

---

# Statement of Acknowledgement

I acknowledge that I have used the following AI tool(s) in the creation of this report:
- OpenAI ChatGPT (Codex-5.5)
- Anthropic Claude (Opus 4.8)

These tools were used to assist with understanding N-Gram probabilistic language models and the Markov assumption, structuring the Python classifier pipeline (preprocessing, bigram counting, add-one smoothing, and the 25% decision rule), debugging code and improving comment quality, interpreting the comparison between the two datasets, improving the clarity of academic language, and supporting APA 7th referencing conventions.

Prompt examples:
1. "Explain why add-one (Laplace) smoothing is needed in a bigram language model and how it changes the conditional probability formula."
2. "My classifier predicts neutral for very few tweets - how does the 25% threshold rule interact with smoothing to produce that, and how should I explain it critically in the report?"
3. "Format this as APA 7th: Go, Bhayani & Huang (2009), Twitter sentiment classification using distant supervision, Stanford CS224N project report."

I confirm that the use of these tools has been in accordance with the Torrens University Australia Academic Integrity Policy and the TUA, Think and MDS Position Paper on the Use of AI. I confirm that the final output is authored by me and represents my own critical thinking, analysis, and synthesis of sources. I take full responsibility for the final content of this report.

---

## References

Go, A., Bhayani, R., & Huang, L. (2009). *Twitter sentiment classification using distant supervision* (CS224N Project Report, Stanford). https://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf

Saif, H., Fernández, M., He, Y., & Alani, H. (2013). Evaluation datasets for Twitter sentiment analysis: A survey and a new dataset, the STS-Gold. *Proceedings of the 1st International Workshop on Emotion and Sentiment in Social and Expressive Media (ESSEM)*. https://oro.open.ac.uk/40660/

Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253–23260. https://doi.org/10.1109/ACCESS.2017.2776930
