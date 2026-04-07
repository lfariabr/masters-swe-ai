# Assessment 3 — NLP Sentiment Analysis: Implementation Plan

## Project Structure

```
Assessment3/
  app.py                  ← Streamlit inference UI
  requirements.txt
  src/
    __init__.py
    parser.py             ← pseudo-XML parser → DataFrame
    preprocess.py         ← cleaning, labeling, outlier removal, split
    dataset.py            ← vocab, GloVe loader, PyTorch Dataset + DataLoader
    baseline.py           ← TF-IDF + LogisticRegression pipeline
    model.py              ← BiLSTMSentiment nn.Module
    train.py              ← training loop + checkpointing
    inference.py          ← predict() shared by app.py
  data/                   ← already populated (books, dvd, electronics, kitchen)
  outputs/                ← saved models land here (.gitkeep)
  embeddings/             ← GloVe files go here (.gitkeep, ~800MB, not committed)
```

---

## Steps

### 1. Download GloVe embeddings
Download `glove.6B.zip` from Stanford NLP and place `glove.6B.100d.txt` in `embeddings/`.
This is a hard dependency for `dataset.py`.

### 2. `src/parser.py` — Load data
- Use BeautifulSoup (`html.parser`) to parse pseudo-XML `.review` files.
- Extract `<review_text>` and `<rating>` from each `<review>` block.
- Iterate all 4 domain directories (books, dvd, electronics, kitchen_&_housewares).
- Return a flat `pd.DataFrame` with columns: `text`, `rating`, `label`, `domain`.

### 3. `src/preprocess.py` — Clean and prepare
- **Drop 3-star reviews** — genuinely ambiguous; justification goes in the ethics section of the report.
- Assign binary labels: 1–2 stars → 0 (negative), 4–5 stars → 1 (positive).
- Clean text: lowercase, strip HTML artifacts, remove punctuation, collapse whitespace.
- `inspect_length_distribution()` — plot word count histogram → saved to `outputs/length_distribution.png`. Validate thresholds before committing to them.
- `remove_outliers()` — drop reviews < 10 words or > 500 words (heuristic, tune after EDA).
- Stratified 70 / 15 / 15 train/val/test split.

### 4. `src/dataset.py` — PyTorch pipeline
- `build_vocab()` — built from **training set only** (no data leakage into val/test).
- `load_glove()` — map vocab → 100-dimensional GloVe vectors; random init for OOV words.
- `tokenize_and_pad()` — convert text → fixed-length token ID tensors (max_len=256).
- `ReviewDataset` — standard `torch.utils.data.Dataset`.
- `make_dataloaders()` — wraps train/val/test into `DataLoader` with batching + shuffling.

### 5. `src/baseline.py` — TF-IDF + Logistic Regression
- `sklearn.pipeline.Pipeline`: `TfidfVectorizer(max_features=30_000, ngram_range=(1,2))` + `LogisticRegression`.
- Train, print classification report (~85–88% expected), save to `outputs/baseline.joblib`.
- Used as the comparison point in the presentation.

### 6. `src/model.py` — BiLSTM
- `BiLSTMSentiment`: `Embedding → Dropout → BiLSTM (2 layers, bidirectional) → concat final fwd+bwd hidden → Linear(hidden*2, 1)`.
- Accepts optional pretrained GloVe embedding matrix.
- Output: raw logit (sigmoid applied at loss/inference time).

### 7. `src/train.py` — Training loop
- Adam optimizer, `BCEWithLogitsLoss`, gradient clipping (`clip_grad_norm_`, max=1.0).
- Saves best val-accuracy checkpoint to `outputs/bilstm.pt`.
- Prints per-epoch: loss, train acc, val acc.

### 8. `src/inference.py` — Single-string prediction
- `predict(text, model, vocab)` → `{"label": "positive"|"negative", "confidence": float}`.
- Reused by `app.py` and any evaluation scripts.

### 9. `app.py` — Streamlit UI
- Text area for review input.
- Sidebar model selector: BiLSTM (GloVe) or Baseline (TF-IDF).
- Calls `predict()`, displays label + confidence.
- `st.cache_resource` for model/vocab loading (so it doesn't reload on every interaction).

---

## Ethical Considerations (report section)
- **3-star ambiguity**: the dataset owner assigned labels by star rating, but 3-star reviews don't carry a clear sentiment signal — including them would pollute both classes. We explicitly drop them and document this decision.
- **Domain bias**: the dataset skews toward certain product categories. A model trained here may not generalise to all sentiment contexts.
- **Label noise**: even 1-star or 5-star reviews can contain mixed sentiment; the model may misclassify edge cases.

---

## Verification checkpoints
| Check | Command | Expected |
|---|---|---|
| Data loads | `python -c "from src.parser import load_all_domains; df = load_all_domains(); print(df.shape)"` | `(~8000+, 4)` |
| Baseline trains | `python src/baseline.py` | Classification report, ~85–88% val acc |
| BiLSTM trains | `python src/train.py` | Per-epoch log, checkpoint saved |
| App runs | `streamlit run app.py` | UI opens on localhost |
