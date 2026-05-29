# Twitter Sentiment Analysis Using an N-Gram Language Model
*DLE602 Deep Learning - Assessment 1 Report Skeleton v1*

## Working Metadata

| Item | Detail |
|---|---|
| Subject | DLE602 - Deep Learning |
| Assessment | Assessment 1 - Programming Problems |
| Task | Twitter sentiment analysis using an N-Gram probabilistic language model |
| Deliverables | Source code, dataset links, and 500-word report (+/-10%) |
| Weight | 30% |
| Due | Sunday at end of Module 4; README currently records 28/06/2026 |
| Learning outcomes | SLO a, SLO b |
| Current status | v1 scaffold: brief analysis, implementation plan, report shell, rubric checklist, and source plan |

---

## Brief Requirements Snapshot

| Required element | How this skeleton handles it | Evidence target |
|---|---|---|
| Read Zhao, Gui, and Zhang (2018) closely | Reference starter list and implementation assumptions keep the assignment aligned with the paper without reproducing the paper's deep CNN experiments | Cite the paper in the report and explain that this submission implements the required N-Gram model only |
| Use any two of the five datasets from the paper | Dataset plan lists candidate paper datasets and asks for final source-link verification before coding | Include direct links in the submitted zip and in the code header |
| Implement Twitter sentiment analysis in Python | Code architecture section defines a small CLI-based Python program with preprocessing, train/test loading, N-Gram model, classification, evaluation, and export | Main file contains run instructions, comments, and no hidden manual configuration |
| Use Bigram or Trigram consistently | v1 recommends Bigram first because it is easier to debug and less sparse than Trigram on small Twitter datasets | Same `n` value used for positive and negative language models, and for both datasets |
| Classify positive, negative, or neutral | Decision rule section translates the "one fourth" threshold into a testable rule | Report the exact threshold interpretation in the report and code comments |
| Compare outcomes from two data sources | Report draft includes a compact results table and comparison paragraphs | Compare sentiment distribution, accuracy, neutral-rate, and behaviour differences |
| Submit clean, commented source code | Rubric strategy defines quality gates for naming, comments, exceptions, and run instructions | Code passes `python -m py_compile` and a small sample run |

## Rubric Strategy

| Rubric area | Weight | High-distinction move |
|---|---:|---|
| Completeness and efficiency | 25% | End-to-end CLI runs on both datasets with short setup, clear errors, deterministic output files, and no long manual configuration |
| Coding convention and quality | 25% | PEP 8 naming, small functions, type hints where useful, comments only around non-obvious threshold/model decisions |
| Accuracy of outcomes | 25% | Same model logic across both datasets; train/test split or provided split; confusion matrix, accuracy, and class distribution for each dataset |
| Effective written communication | 25% | 500 words, short and direct, explicitly compares similarities/differences and explains likely dataset/preprocessing causes |

## Suggested Word Budget

| Section | Target words | Notes |
|---|---:|---|
| Introduction and model scope | 80-100 | Explain N-Gram sentiment analysis and paper context |
| Implementation method | 110-130 | Preprocessing, Bigram/Trigram choice, smoothing, threshold rule |
| Dataset comparison results | 180-220 | Similarities/differences across two sources; include metrics from final run |
| Critical reflection | 80-100 | Explain limitations: sparse N-Grams, slang, negation, class imbalance |
| Conclusion | 40-60 | One tight closing judgement |
| Total body | 500 | Keep tables outside the 500 words if allowed |

## Draft Thesis

The submitted program implements a transparent Bigram N-Gram language model for Twitter sentiment analysis, then applies the same preprocessing and classification rule to two Twitter sentiment datasets. The report should argue that the model is useful as a simple baseline because it exposes how local word-pair evidence differs between sources, but it is weaker than deep CNN approaches because sparse N-Grams struggle with unseen slang, sarcasm, negation, and topic-specific vocabulary.

---

# Implementation Plan

## 1. Recommended Submission Structure

```text
Assessment1/
  DLE602_Assessment1_Report_Skeleton.md
  code/
    dle602_sentiment_ngram.py
    requirements.txt
  data/
    README.md
    dataset_a/
    dataset_b/
  outputs/
    dataset_a_metrics.csv
    dataset_b_metrics.csv
    comparison_summary.csv
  report/
    DLE602_Faria_L_Assessment_1_Report.md
```

> Keep raw dataset files out of git if they are large or licence-restricted. The submitted zip can include permitted files or a dataset download/readme link, depending on licence terms.

## 2. Dataset Source Plan

The assessment brief does not enumerate the five dataset names, only stating that two of the five datasets from Zhao, Gui, and Zhang (2018) must be used. Secondary summaries of the paper commonly list these candidate datasets; verify the final pair against the paper before locking the implementation.

| Candidate dataset from paper | Why it may fit | v1 action |
|---|---|---|
| Stanford Twitter Sentiment Test dataset | Twitter-specific and commonly used for baseline sentiment experiments | Candidate A; verify accessible labelled format |
| SE2014 / SemEval-2014 Twitter sentiment dataset | Public shared-task benchmark with positive, negative, and neutral labels | Strong candidate; official task site has test/gold files |
| Stanford Twitter Sentiment Gold dataset (STS-Gold) | Gold-standard tweet/entity sentiment dataset | Candidate if labels and text are easy to access |
| Sentiment Evaluation dataset | Mentioned in paper summaries, but name is ambiguous | Verify exact source before use |
| Sentiment Strength Twitter dataset | Twitter-specific dataset linked to sentiment strength scoring | Candidate B; verify licence/access |

**Preferred v1 pair:** SemEval-2014 Twitter sentiment dataset and Sentiment Strength Twitter dataset, because they are both Twitter-oriented and should expose useful contrast in sentiment distribution and text style.

**Fallback pair:** SemEval-2014 Twitter sentiment dataset and Stanford Twitter Sentiment Gold dataset, if Sentiment Strength access is difficult.

## 3. Model Interpretation Decision

The brief states: if the N-Gram model identifies one fourth of the words in a tweet as positive, classify the tweet as positive; if one fourth are negative, classify it as negative; otherwise classify as neutral.

For a reproducible implementation, use this v1 rule:

1. Choose `n = 2` for Bigram unless Trigram performance is clearly better.
2. Train separate positive and negative N-Gram language models from labelled training tweets.
3. For each input tweet, generate the same N-Grams after preprocessing.
4. For each N-Gram, compare smoothed log-probability under the positive model versus the negative model.
5. Count an N-Gram as positive if `log_p_positive > log_p_negative + margin`.
6. Count an N-Gram as negative if `log_p_negative > log_p_positive + margin`.
7. Classify:
   - positive if `positive_hits / total_ngrams >= 0.25` and positive hits exceed negative hits;
   - negative if `negative_hits / total_ngrams >= 0.25` and negative hits exceed positive hits;
   - neutral otherwise.

This is slightly more precise than "one fourth of words" because the model operates on N-Grams. If the facilitator insists on token count as the denominator, change the denominator to `total_tokens` and document the change.

## 4. Preprocessing Design

| Step | Decision | Rationale |
|---|---|---|
| Case | Lowercase text | Reduces sparse duplicates |
| URLs | Replace with `<url>` | URL presence may carry signal, but the exact URL should not |
| Mentions | Replace with `<user>` | Preserves social-media pattern without overfitting to usernames |
| Hashtags | Keep tag word, strip only `#` | Hashtags often encode sentiment/topic |
| Emoji/emoticons | Keep common emoticons or map to tokens | Strong polarity signal in Twitter data |
| Punctuation | Keep `!`, `?`, and negation apostrophes if tokenizer allows | Useful sentiment cues |
| Stop words | Do not remove in v1 | N-Grams need short function-word context, especially for negation |
| Unknowns | Add `<unk>` and Laplace/add-k smoothing | Avoid zero probabilities for unseen N-Grams |

## 5. Minimal Code Shape

```python
def load_dataset(path: Path) -> list[TweetExample]:
    """Load text and label rows from a CSV/TSV dataset."""

def preprocess(text: str) -> list[str]:
    """Normalise tweet text and return tokens."""

def build_ngram_counts(examples: list[TweetExample], n: int) -> NGramModel:
    """Build positive and negative N-Gram count tables."""

def score_tweet(tokens: list[str], model: NGramModel, n: int) -> Prediction:
    """Apply the 25 percent threshold rule."""

def evaluate(examples: list[TweetExample], model: NGramModel, n: int) -> Metrics:
    """Return accuracy, per-class counts, and confusion matrix."""

def main() -> None:
    """Parse CLI arguments, run both datasets, and write output summaries."""
```

Suggested CLI:

```bash
python code/dle602_sentiment_ngram.py \
  --dataset-a data/dataset_a/train.csv \
  --dataset-b data/dataset_b/train.csv \
  --ngram 2 \
  --output outputs/comparison_summary.csv
```

## 6. Evaluation Outputs to Capture

| Output | Why it matters for the report |
|---|---|
| Total records per dataset | Shows comparability and class imbalance |
| Label distribution | Explains why neutral or positive predictions dominate |
| Accuracy | Supports the rubric's "correct results" criterion |
| Confusion matrix | Shows whether errors are systematic |
| Positive/negative/neutral prediction ratio | Directly feeds the 500-word comparison |
| Five example errors per dataset | Gives material for critical reflection |

---

# 500-Word Report Draft Shell

## 1. Introduction

Twitter sentiment analysis classifies short social-media texts into positive, negative, or neutral sentiment. Zhao, Gui, and Zhang (2018) used deep convolutional neural networks with word vectors and N-Gram features for Twitter sentiment analysis, but this assessment implements the required simpler N-Gram probabilistic language model. The aim is to test whether local word-pair or word-triple evidence can classify tweets consistently across two labelled Twitter sentiment datasets.

> Tighten after coding. Keep this section around 80-100 words.

## 2. Implementation Method

The program used a [Bigram/Trigram] model with the same `n` value for positive and negative examples in both datasets. Tweets were normalised by lowercasing text, replacing URLs and usernames with placeholder tokens, preserving hashtag words, and retaining negation-sensitive tokens. Separate positive and negative N-Gram count models were trained with add-k smoothing. Each test tweet was converted into N-Grams and classified using the brief's 25 percent rule: [insert exact final denominator and tie-breaking rule].

> Add dataset names and code run command once finalised.

## 3. Results and Comparison

| Metric | Dataset A: [name] | Dataset B: [name] |
|---|---:|---:|
| Records evaluated | TBD | TBD |
| Positive labels | TBD | TBD |
| Negative labels | TBD | TBD |
| Neutral labels | TBD | TBD |
| Accuracy | TBD | TBD |
| Predicted positive | TBD | TBD |
| Predicted negative | TBD | TBD |
| Predicted neutral | TBD | TBD |

The outcomes were [similar/different] across the two sources. Dataset A produced [insert trend], while Dataset B produced [insert trend]. The strongest similarity was [insert evidence: e.g., both datasets had many neutral predictions because the 25 percent threshold is conservative]. The main difference was [insert evidence: e.g., one dataset had more informal spelling, hashtags, sarcasm, or topic-specific language], which affected the N-Gram model because unseen phrases receive smoothed probabilities rather than learned contextual meaning.

## 4. Critical Reflection

The model behaved consistently because the same preprocessing, N-Gram size, smoothing, and threshold rule were used for both sources. However, its accuracy is constrained by sparsity: a Bigram or Trigram model only recognises local phrase patterns seen during training. It does not understand sarcasm, long-range negation, or semantic similarity between different expressions. This explains why a simple N-Gram system is useful as a transparent baseline, but less robust than the deep CNN approach discussed by Zhao, Gui, and Zhang (2018).

## 5. Conclusion

Overall, the experiment shows that N-Gram sentiment analysis can classify some Twitter text effectively when training and test language overlap, but performance depends strongly on dataset vocabulary, label balance, and preprocessing quality.

---

# Appendices

## Appendix A - Rubric Checklist

| Checklist item | Status |
|---|---|
| Assessment brief read and summarised | Drafted |
| Zhao et al. (2018) paper cited | Drafted; verify dataset list from paper |
| Two valid paper datasets selected | To do |
| Dataset links included | To do |
| Code has run instructions at top of main file | To do |
| Bigram/Trigram choice used consistently | Drafted |
| Positive, negative, neutral outputs implemented | To do |
| Same behaviour across both datasets | To do |
| Exception handling for missing files/columns | To do |
| Metrics generated for both datasets | To do |
| 500-word report compares outcomes | Drafted shell |
| APA references checked | To do |
| Final zip prepared | To do |

## Appendix B - Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Paper datasets are hard to access | Could delay coding | Verify dataset URLs first; use SemEval official data if available |
| Dataset schemas differ | Loader complexity increases | Implement small mapping config for `text` and `label` columns |
| Neutral labels unavailable in one source | Report comparison becomes uneven | Train positive/negative models and still allow neutral prediction through threshold; evaluate only available labels clearly |
| Trigrams are too sparse | Low accuracy | Start with Bigram; only compare Trigram as optional experiment |
| "One fourth of words" threshold is ambiguous | Marker may question rule | Document the denominator in code and report; keep it consistent |

## Appendix C - Next Draft Tasks

1. Open Zhao, Gui, and Zhang (2018) and verify the exact five dataset names.
2. Select two datasets and record download/source links in `data/README.md`.
3. Implement `dle602_sentiment_ngram.py` as a small CLI.
4. Run Dataset A and Dataset B with identical settings.
5. Export metrics and confusion matrices into `outputs/`.
6. Replace all `TBD` placeholders in the report shell.
7. Cut the body to 450-550 words and keep tables/appendices separate if allowed.
8. Prepare the final zip with source code, report, outputs, and dataset links.

---

# Reference Starter List

Jurafsky, D., & Martin, J. H. (2008). *Speech and language processing*. Pearson. https://web.stanford.edu/~jurafsky/slp3/3.pdf

Rosenthal, S., Ritter, A., Nakov, P., & Stoyanov, V. (2014). SemEval-2014 Task 9: Sentiment Analysis in Twitter. *Proceedings of the 8th International Workshop on Semantic Evaluation*, 73-80. https://aclanthology.org/S14-2009/

Torrens University Australia. (2024). *DLE602 Assessment 1 brief: Programming Problems*.

Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253-23260. https://doi.org/10.1109/ACCESS.2017.2776930
