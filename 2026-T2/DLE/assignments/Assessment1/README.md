# DLE602 Assessment 1 - Twitter Sentiment Analysis with an N-Gram Language Model

**Student:** Luis Faria (A00187785) | **Subject:** DLE602 Deep Learning | **Assessment 1 - Programming Problems**

This submission implements the required probabilistic **N-Gram (bigram) sentiment classifier** and
compares its behaviour on two of the five datasets from Zhao, Gui & Zhang (2018): **STS-Test** and
**STS-Gold**. No deep CNN is used; the N-Gram model is the required deliverable.

## Where to start

| If you want to... | Open |
|---|---|
| Read the writeup | `report/` (the PDF) |
| Run the classifier | `code/dle602_sentiment_ngram.py` (instructions below + at the top of the file) |
| See it run end-to-end with outputs inline | `notebook/DLE602FariaLuisBrief1.ipynb` |
| Inspect generated metrics/figures | `outputs/` |

## What's in this submission

| Folder | Contents |
|---|---|
| `report/` | The report (PDF) |
| `code/` | `dle602_sentiment_ngram.py` (the classifier CLI), `bias_variance_sweep.py` (bias-variance analysis), `requirements.txt` |
| `dataset/` | The datasets as CSV, the `download.py` reproduction script, and source links (`dataset/README.md`) |
| `notebook/` | An executed Jupyter notebook that imports the classifier and shows the pipeline |
| `outputs/` | Generated metrics (CSV) and figures (confusion matrices, distributions, bias-variance) |

## How to run (no configuration needed)

The datasets are already included in `dataset/`, so the program runs directly:

```bash
pip install -r code/requirements.txt

python code/dle602_sentiment_ngram.py \
  --train dataset/sentiment140_train_sample.csv \
  --eval-a dataset/sts_test.csv --eval-a-name STS-Test \
  --eval-b dataset/sts_gold.csv --eval-b-name STS-Gold \
  --ngram 2 --out outputs
```

It prints the metrics table and writes CSVs + figures to `outputs/`. Re-running gives **identical**
numbers (training is pure counting; the only sampling is fixed). Full run/test notes are in the
comment block at the top of `code/dle602_sentiment_ngram.py`.

## Expected output (so you can confirm a correct run)

| Metric | STS-Test | STS-Gold |
|---|---:|---:|
| Records evaluated | 498 | 2,034 |
| Accuracy | 0.452 | 0.719 |
| Macro-F1 | 0.401 | 0.726 |

## Datasets used (links)

- **Sentiment140** (training corpus): https://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip
- **STS-Test** (evaluation A): same Stanford zip (`testdata.manual.2009.06.14.csv`)
- **STS-Gold** (evaluation B): https://raw.githubusercontent.com/pollockj/world_mood/master/sts_gold_v03/sts_gold_tweet.csv

Schema and licensing notes are in `dataset/README.md`; `dataset/download.py` reproduces the CSVs from these sources.

## References

- Zhao, J., Gui, X., & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. *IEEE Access, 6*, 23253-23260. https://doi.org/10.1109/ACCESS.2017.2776930
- Go, A., Bhayani, R., & Huang, L. (2009). *Twitter sentiment classification using distant supervision* (CS224N Project Report, Stanford).
- Saif, H., Fernández, M., He, Y., & Alani, H. (2013). Evaluation datasets for Twitter sentiment analysis: the STS-Gold.
