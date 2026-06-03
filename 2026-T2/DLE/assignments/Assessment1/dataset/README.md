# DLE602 Assessment 1 — Datasets

Two Twitter sentiment datasets are used, both **among the five datasets in
Zhao, Gui & Zhang (2018)** and both downloadable as **full tweet text** (no
Twitter-API hydration, no login). The other paper datasets (SemEval-2014,
SS-Tweet) are distributed only as tweet IDs and would need hydration, so they are
not reproducible for this submission.

## Files

| File | Role | Rows | Classes | Committed? |
|---|---|---:|---|---|
| `sentiment140_train_sample.csv` | Train the positive/negative bigram models | 80,000 | neg / pos | ✅ |
| `sts_test.csv` | **Dataset A** — evaluation | 498 | neg / neutral / pos | ✅ |
| `sts_gold.csv` | **Dataset B** — evaluation | 2,034 | neg / pos | ✅ |
| `_raw/` | Raw downloads (zip + 1.6M-row CSV) | — | — | ❌ git-ignored |

All committed CSVs are tidy UTF-8 with two columns: `label` (`negative` /
`neutral` / `positive`) and `text`.

## Sources

- **Sentiment140 / Stanford Twitter Sentiment** — training corpus + STS-Test test set.
  `https://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip` (~81 MB).
  Original 6-column, Latin-1, no header: `polarity,id,date,query,user,text`,
  where polarity `0=negative`, `2=neutral` (test set only), `4=positive`.
  Reference: Go, Bhayani & Huang (2009).
- **STS-Gold** — `sts_gold_tweet.csv`, `;`-separated, columns `id;polarity;tweet`.
  `https://raw.githubusercontent.com/pollockj/world_mood/master/sts_gold_v03/sts_gold_tweet.csv`
  Reference: Saif, Fernández, He & Alani (2013).

## Reproduce

```bash
python dataset/download.py            # download + normalise (idempotent)
python dataset/download.py --force    # rebuild the CSVs
python dataset/download.py --per-class 25000   # smaller training sample
```

The script downloads into `dataset/_raw/`, maps the polarity codes to labels,
and writes the three normalised CSVs. The 80k training sample is a balanced draw
(40k negative + 40k positive, `random_state=42`) from the 1.6M-row corpus, kept
small enough to commit so the project clones-and-runs without the large download.

## Licence / usage note

These datasets are redistributed here for **academic, non-commercial coursework**
only. Tweet text belongs to its original authors and is subject to the X/Twitter
Terms of Service; cite the original dataset papers in any derivative work.
