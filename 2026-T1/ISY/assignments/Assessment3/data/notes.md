# Multi-Domain Sentiment Dataset
This sentiment dataset was used in our paper:
> John Blitzer, Mark Dredze, Fernando Pereira. Biographies, Bollywood, Boom-boxes and Blenders: Domain Adaptation for Sentiment Classification. Association of Computational Linguistics (ACL), 2007. [PDF](https://www.cs.jhu.edu/~mdredze/publications/sentiment_acl07.pdf)

If you use this data for your research or a publication, please cite the above paper as the reference for the data. Also, please drop me a line so I know that you found the data useful.

The Multi-Domain Sentiment Dataset contains product reviews taken from Amazon.com from 4 product types (domains): Kitchen, Books, DVDs, and Electronics. Each domain has several thousand reviews, but the exact number varies by domain. Reviews contain star ratings (1 to 5 stars) that can be converted into binary labels if needed. This page contains some descriptions about the data. If you have questions, please email me directly (email found here).

A few notes regarding the data.
1) There are 4 directories corresponding to each of the four domains. Each directory contains 3 files called positive.review, negative.review and unlabeled.review. (The books directory doesn't contain the unlabeled but the link is below.) While the positive and negative files contain positive and negative reviews, these aren't necessarily the splits we used in the experiments. We randomly drew from the three files ignoring the file names.
2) Each file contains a pseudo XML scheme for encoding the reviews. Most of the fields are self explanatory. The reviews have a unique ID field that isn't very unique. If it has two unique id fields, ignore the one containing only a number.

There are always small details and I am sure that I omitted many of them. If you have a question after reading the paper and this page, please let me know.

Link to download the data:
- Multi-Domain Sentiment Dataset (30 MB) [domain_sentiment_data.tar.gz]
- Books unlabeled data (2 MB) [book.unlabeled.gz] — not needed for this assessment

Last updated: August 2, 2007

---

Based on the dataset notes and the rubric, here's how I'm considering to approach it:

**Data parsing**
The .review files are pseudo-XML. We'll need a custom parser (BeautifulSoup or regex) to extract `<review_text>` and `<rating>` fields. Convert star ratings to binary: 1–2 stars = negative, 4–5 stars = positive, skip 3-star reviews (ambiguous — this is also the ethical consideration the rubric asks us to discuss).

**Which domains to use**
Use all 4 (Kitchen, Books, DVDs, Electronics) — gives ~8k+ labelled samples and better generalization for unseen input, which is what the HD criterion requires (100% on input outside training data).

**Model recommendation**
Go with a Bidirectional LSTM with pretrained GloVe embeddings:
- Fast to train, solid accuracy on this dataset (~92–95%)
- More explainable than a transformer (better for the presentation)
- Push toward HD: fine-tune a small BERT (distilbert-base-uncased) — that's realistic 100% on clean test sentences

**Stack**
- PyTorch + DataLoader — matches brief's suggestion and my existing stack
- Streamlit for the web interface — fastest path, runs locally, easy to demo
- torchtext or manual vocab/tokenizer
- GloVe embeddings — download `glove.6B.100d.txt` from Stanford (~800MB), required before step 4

**Pipeline order (matches the rubric checklist)**
1. Parse XML → DataFrame
2. Drop 3-star reviews, assign binary labels
3. Clean text (lowercase, strip punctuation, remove HTML artifacts)
4. Build vocab / load pretrained GloVe embeddings
5. Outlier removal — heuristic: drop reviews < 10 words or > 500 words; validate thresholds against actual distribution first
6. Pad/truncate to fixed length
7. Train/val/test split (70/15/15)
8. DataLoader with batching
9. Define BiLSTM (or DistilBERT) model
10. Train + tune
11. Streamlit app wrapping the inference function

**Ethical angle for the report**
The dataset owner labelled reviews by star rating, but 3-star reviews are genuinely ambiguous and including them would pollute both classes.
We can flag that and justify dropping them — that's a solid ethical observation the rubric specifically calls for.

**Other Ideas**
TF-IDF is useful as a baseline: train a quick TF-IDF + SVM or Logistic Regression first, get ~85–88% accuracy, then show BiLSTM beats it.
That's a good framing for the presentation ("we explored classical approaches before moving to deep learning"). So the recommended structure:

| Step | Approach | Purpose |
|---|---|---|
| Baseline | TF-IDF + Logistic Regression / SVM | Quick benchmark, good for the report |
| Main model | BiLSTM + GloVe embeddings | Satisfies neural network requirement, ~92–95% |
| If aiming for HD | DistilBERT fine-tuned | Near 100% on unseen input |

The BiLSTM + GloVe path is the right main model. It's also more defensible in the presentation because you can explain embeddings, LSTM gates, and bidirectionality clearly — which maps directly to the communication rubric criteria.

---

## Next steps:
1. Download GloVe embeddings (`glove.6B.100d.txt`) — required dependency before building the model.
2. Write the XML parser to extract reviews and ratings into a DataFrame.
3. Clean and preprocess the text, assign binary labels, and drop 3-star reviews.
4. Inspect the review length distribution to validate outlier removal thresholds.
5. Implement the TF-IDF + Logistic Regression baseline, evaluate and report results.
6. Build the BiLSTM model, train it, and evaluate.
7. If time allows, fine-tune DistilBERT and evaluate on a held-out test set to demonstrate the HD criterion.
8. Build the Streamlit app wrapping the inference function.
