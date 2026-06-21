# Twitter Sentiment Analysis Using an N-Gram Language Model
*DLE602 Deep Learning - Assessment 1 Report Skeleton v2*

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
| Current status | v3: CLI at `code/dle602_sentiment_ngram.py` + bias-variance harness `code/bias_variance_sweep.py`; datasets downloaded and normalised; model executed end-to-end (bigram) on both datasets with real metrics, figures and a companion notebook; report at `report/DLE602FariaLuisBrief1_Report.md` expanded to ~658 words (Datasets section + Tables 1-2, Figures 1-3, Appendix C bias-variance) under the facilitator's verbal 700-800 allowance. Remaining: final APA pass + submission zip |

---

## Brief Requirements Snapshot

| Required element | How this skeleton handles it | Evidence target |
|---|---|---|
| Read Zhao, Gui, and Zhang (2018) closely | Reference starter list and implementation assumptions keep the assignment aligned with the paper without reproducing the paper's deep CNN experiments | Cite the paper in the report and explain that this submission implements the required N-Gram model only |
| Use any two of the five datasets from the paper | Final pair locked: **STS-Test** and **STS-Gold**, both among the paper's five datasets and both downloadable as full tweet text (no Twitter-API hydration). Bigram models are trained on a balanced 80k Sentiment140 sample | Direct download links and schema are in `dataset/README.md`; `dataset/download.py` reproduces the CSVs |
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
| Total body | 500 (verbal extension to 700-800; current draft ~658) | Keep tables, figures and appendices outside the word count |

## Draft Thesis

The submitted program implements a transparent Bigram N-Gram language model for Twitter sentiment analysis, then applies the same preprocessing and classification rule to two Twitter sentiment datasets. The report should argue that the model is useful as a simple baseline because it exposes how local word-pair evidence differs between sources, but it is weaker than deep CNN approaches because sparse N-Grams struggle with unseen slang, sarcasm, negation, and topic-specific vocabulary.

---

# Implementation Plan

## 1. Recommended Submission Structure

```text
Assessment1/
  DLE602_Assessment1_Report_Skeleton.md      # this file (report draft + plan)
  code/
    dle602_sentiment_ngram.py                # CLI N-Gram classifier (stdlib core)
    requirements.txt
  dataset/
    README.md                                # sources, licence, schema, download
    download.py                              # fetch + normalise the datasets
    sentiment140_train_sample.csv            # 80k balanced training sample (committed)
    sts_test.csv                             # 498 tweets, 3 classes (committed)
    sts_gold.csv                             # 2034 tweets, 2 classes (committed)
  notebook/
    DLE602FariaLuisBrief1.ipynb              # executed portfolio companion
  report/
    DLE602FariaLuisBrief1_Report.md          # final 500-word report (532 words)
  outputs/
    comparison_summary.csv                   # side-by-side metrics
    sts_test_metrics.csv / sts_gold_metrics.csv
    error_examples.txt
    figures/
      sentiment_distribution.png
      confusion_sts_test.png / confusion_sts_gold.png
```

> The 81 MB Sentiment140 zip and the 1.6M-row raw CSV are kept out of git (`dataset/_raw/`, git-ignored). Only the small normalised CSVs and the 80k training sample are committed, so the project clones-and-runs without the large download.

## 2. Dataset Source Plan (locked)

The brief requires two of the five datasets from Zhao, Gui, and Zhang (2018). Most of the paper's datasets (SemEval-2014, SS-Tweet) are distributed only as **tweet IDs** and need Twitter-API "hydration" (now paid/restricted), so they are not reproducible for a clean submission. The two chosen datasets are the ones that ship as **full tweet text** while still being among the paper's five:

| Role | Dataset (paper name) | File | Rows | Classes | Source (no login) |
|---|---|---|---:|---|---|
| Training corpus | Stanford Twitter Sentiment / Sentiment140 | `sentiment140_train_sample.csv` (80k balanced sample of the 1.6M corpus) | 80,000 | neg / pos | [cs.stanford.edu zip](https://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip) |
| **Dataset A** | **STS-Test** (Stanford Twitter Sentiment Test) | `sts_test.csv` | 498 | neg / **neutral** / pos | same Stanford zip (`testdata.manual.2009.06.14.csv`) |
| **Dataset B** | **STS-Gold** (Stanford Twitter Sentiment Gold) | `sts_gold.csv` | 2,034 | neg / pos | [github.com/pollockj/world_mood](https://raw.githubusercontent.com/pollockj/world_mood/master/sts_gold_v03/sts_gold_tweet.csv) |

**Actual class distribution (from the executed run):**

| Dataset | negative | neutral | positive |
|---|---:|---:|---:|
| STS-Test | 177 | 139 | 182 |
| STS-Gold | 1,402 | 0 | 632 |

**Why this is a good comparison pair:** STS-Test carries a neutral class, STS-Gold does not, which directly exposes how the same model handles a two-class vs three-class source - exactly the "compare outcomes from two data sources" requirement. `dataset/download.py` downloads both, maps the polarity codes (0=neg, 2=neutral, 4=pos), and writes tidy `label,text` CSVs.

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

The program used a **bigram** model with the same `n = 2` for the positive and negative language models, applied identically to both datasets. Tweets were normalised by lowercasing, replacing URLs and usernames with `<url>`/`<user>` placeholders, stripping the `#` but keeping hashtag words, and retaining `!`/`?` and negation-sensitive tokens. Separate positive and negative bigram models were trained on a balanced 80k Sentiment140 sample with **add-1 (Laplace) smoothing** over a 49,038-token vocabulary. Each test tweet was converted into bigrams; a bigram counts as positive (negative) when its smoothed conditional log-probability is higher under the positive (negative) model. The brief's rule was applied with the **N-Gram count as the denominator**: classify positive if at least 25% of the tweet's bigrams are positive and outnumber the negative ones, negative by the mirror rule, otherwise neutral.

Run command:

```bash
python dataset/download.py        # one-off: build the dataset CSVs
python code/dle602_sentiment_ngram.py --ngram 2   # trains + evaluates both datasets
```

## 3. Results and Comparison

| Metric | Dataset A: STS-Test | Dataset B: STS-Gold |
|---|---:|---:|
| Records evaluated | 498 | 2,034 |
| Positive labels (true) | 182 | 632 |
| Negative labels (true) | 177 | 1,402 |
| Neutral labels (true) | 139 | 0 |
| Accuracy | 0.452 | 0.719 |
| Macro-F1 | 0.401 | 0.726 |
| Predicted positive | 274 | 788 |
| Predicted negative | 186 | 1,110 |
| Predicted neutral | 38 | 136 |

> Bigram vs trigram (optional experiment, same settings): trigram accuracy drops to **0.420** (STS-Test) and **0.550** (STS-Gold), confirming that trigrams are too sparse on short tweets - so bigram is the submitted model.

The outcomes were **clearly different** across the two sources. On STS-Gold the bigram model reached a solid baseline (0.72 accuracy, 0.73 macro-F1), helped by it being a two-class problem whose informal tweet style is close to the Sentiment140 training corpus. On STS-Test accuracy was much lower (0.45) because it is a harder three-class task and the model **rarely predicts neutral** (only 38 of 498): with add-1 smoothing almost every bigram leans slightly positive or negative, so the 25% threshold is easily crossed and the neutral class is under-produced. The shared behaviour across both sources is a **positive-leaning bias** (predicted positive exceeds true positive in both), driven by the emoticon-labelled training corpus. The main difference - one source needs a neutral decision the other never does - is exactly what makes the comparison informative, because the N-Gram model has no learned notion of "neutral"; it only emerges from the threshold.

## 4. Critical Reflection

The model behaved consistently because the same preprocessing, N-Gram size, smoothing, and threshold rule were used for both sources. However, its accuracy is constrained by sparsity: a Bigram or Trigram model only recognises local phrase patterns seen during training. It does not understand sarcasm, long-range negation, or semantic similarity between different expressions. This explains why a simple N-Gram system is useful as a transparent baseline, but less robust than the deep CNN approach discussed by Zhao, Gui, and Zhang (2018).

## 5. Conclusion

Overall, the experiment shows that N-Gram sentiment analysis can classify some Twitter text effectively when training and test language overlap, but performance depends strongly on dataset vocabulary, label balance, and preprocessing quality.

---

# Appendices

## Appendix A - Rubric Checklist

| Checklist item | Status |
|---|---|
| Assessment brief read and summarised | Done |
| Zhao et al. (2018) paper cited | Done |
| Two valid paper datasets selected | Done (STS-Test + STS-Gold) |
| Dataset links included | Done (`dataset/README.md` + skeleton table) |
| Code has run instructions at top of main file | Done (module docstring) |
| Bigram/Trigram choice used consistently | Done (bigram, `n=2` both datasets; trigram shown as optional) |
| Positive, negative, neutral outputs implemented | Done |
| Same behaviour across both datasets | Done (identical model/preprocessing/threshold) |
| Exception handling for missing files/columns | Done (`load_dataset` validates columns/rows) |
| Metrics generated for both datasets | Done (`outputs/comparison_summary.csv` + figures) |
| 500-word report compares outcomes | Done (`report/DLE602FariaLuisBrief1_Report.md`, 532 words) |
| APA references checked | To do (final pass) |
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

1. ✅ Selected two datasets (STS-Test + STS-Gold) and recorded source links in `dataset/README.md`.
2. ✅ Implemented `code/dle602_sentiment_ngram.py` as a small CLI.
3. ✅ Ran both datasets with identical settings (bigram, add-1, 0.25 threshold).
4. ✅ Exported metrics, confusion matrices and figures into `outputs/`.
5. ✅ Replaced all `TBD` placeholders in the report shell with real numbers.
6. ✅ Wrote the 500-word report (`report/DLE602FariaLuisBrief1_Report.md`, 532 words; table/refs kept separate).
7. ✅ Added a bias-variance sweep (`code/bias_variance_sweep.py`) and **Appendix C** (Tables C1-C2 + Figure 3) demonstrating the capacity dial (N-Gram order) vs the regularization dial (add-k) on the A1 model.
8. ✅ Expanded the report to ~658 words: added a **Datasets** section (rationale + Table 1) and folded the bias-variance finding into Results, under the facilitator's verbal 700-800 allowance.
9. 🕐 Final APA reference pass and prepare the submission zip (source code, report, outputs, dataset links).

---

# Reference Starter List

Go, A., Bhayani, R., & Huang, L. (2009). *Twitter sentiment classification using distant supervision* (CS224N Project Report, Stanford). https://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf

Jurafsky, D., & Martin, J. H. (2008). *Speech and language processing*. Pearson. https://web.stanford.edu/~jurafsky/slp3/3.pdf

Rosenthal, S., Ritter, A., Nakov, P., & Stoyanov, V. (2014). SemEval-2014 Task 9: Sentiment Analysis in Twitter. *Proceedings of the 8th International Workshop on Semantic Evaluation*, 73-80. https://aclanthology.org/S14-2009/

Saif, H., Fernández, M., He, Y., & Alani, H. (2013). Evaluation datasets for Twitter sentiment analysis: A survey and a new dataset, the STS-Gold. *Proceedings of the 1st International Workshop on Emotion and Sentiment in Social and Expressive Media (ESSEM)*. https://oro.open.ac.uk/40660/

Torrens University Australia. (2024). *DLE602 Assessment 1 brief: Programming Problems*.

Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253-23260. https://doi.org/10.1109/ACCESS.2017.2776930
