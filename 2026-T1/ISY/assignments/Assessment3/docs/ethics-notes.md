# Ethics Notes - ISY503 Assessment 3

## Key Ethical Considerations

### Label Noise And Ambiguity

The dataset is split into positive and negative review files, but individual review text and star ratings may not always align. A review can contain mixed sentiment, sarcasm, or a rating that does not cleanly match its text. The project should audit rating/filename mismatches and document how these cases were handled.

### 3-Star And Neutral Sentiment

The assessment asks for binary output: `Positive review` or `Negative review`. Real sentiment may be neutral or mixed. If any 3-star or ambiguous records appear, they should be flagged because forcing them into a binary class may reduce fairness and reliability.

### Domain Bias

The model is trained on Amazon product reviews from books, DVDs, electronics, and kitchen/housewares. It may not generalize to restaurants, hotels, medical feedback, social media, or workplace communication. The demo should include at least one domain-shifted example to make this limitation visible.

### Overconfidence

The app may show confidence scores, but confidence is not the same as correctness. The presentation should avoid claiming the model understands sentiment like a human. It is a statistical classifier trained on a specific dataset.

### Binary Sentiment Limits

Binary labels can hide useful nuance such as "positive about quality but negative about delivery." Error analysis should include mixed examples and explain why the system can fail.

## How The Project Addresses These Issues

- Keep rating metadata for label auditing.
- Report class/domain distribution.
- Use held-out test data and outside-training demo examples.
- Include false positives and false negatives in the presentation.
- Document limitations in the individual report and ethics slide.
