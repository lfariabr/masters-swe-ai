# Assessment 3 - NLP Sentiment Analysis: Implementation Plan
> codex resume 019d7f44-8706-7ba2-ac81-5d3281016979
> claude --resume "isy-assessment-3"

## Portfolio Direction

Build the NLP option as a reproducible **multi-domain product review sentiment classifier**. The portfolio signal is ML engineering: raw dataset parsing, auditable preprocessing, baseline comparison, neural model training, evaluation/error analysis, and a simple deployed inference UI.

The local dataset contains 8,000 labelled Amazon reviews across four domains:
- books
- dvd
- electronics
- kitchen_&_housewares

Each domain has 1,000 positive and 1,000 negative labelled reviews.

## Project Structure

```text
Assessment3/
  README.md
  app.py                         # Streamlit inference UI
  requirements.txt
  src/
    __init__.py
    parser.py                    # pseudo-XML parser -> DataFrame
    preprocess.py                # label audit, cleaning, outlier removal, splits
    features.py                  # EDA helpers and feature summaries
    dataset.py                   # vocab, optional GloVe, PyTorch Dataset/DataLoader
    baseline.py                  # TF-IDF + LogisticRegression pipeline
    model.py                     # BiLSTMSentiment nn.Module
    train.py                     # BiLSTM training loop + checkpointing
    inference.py                 # predict_sentiment() shared by app/evaluation
    evaluate.py                  # metrics, confusion matrix, error analysis
  tests/
    test_parser.py
    test_preprocess.py
    test_dataset.py
    test_baseline.py
    test_model.py
    test_inference.py
  notebooks/
    EDA.ipynb
    distilbert.ipynb             # optional stretch only
  data/                          # already populated review files
  outputs/                       # generated artifacts; ignored except .gitkeep
  embeddings/                    # optional GloVe files; ignored except .gitkeep
  docs/
    github-issue-list.md
    presentation-outline.md
    individual-report-template.md
    contribution-log.md
    team-contribution-table.md
    references.md
    ethics-notes.md
    demo-test-cases.md
    submission-checklist.md
```

## Implementation Steps

### 1. Project setup and reproducibility
- Add package structure, `requirements.txt`, `.gitignore`, and `README.md`.
- Define a fixed random seed and split configuration used by preprocessing, training, and evaluation.
- Keep generated model files, plots, and embeddings out of Git unless intentionally small.

### 2. `src/parser.py` - Load local review data
- Parse `.review` files with BeautifulSoup using `html.parser`.
- Extract at minimum `review_text`, `rating`, `domain`, `source_file`, and `label`.
- Use the filename as the primary sentiment label:
  - `positive.review` -> `1`
  - `negative.review` -> `0`
- Retain `rating` for auditing, ethics, and error analysis.
- Return a DataFrame with columns: `text`, `rating`, `label`, `domain`, `source_file`.

### 3. `src/preprocess.py` - Audit, clean, and split
- Implement `audit_labels()` to flag ambiguous or contradictory rows:
  - 3-star reviews
  - positive-file reviews with low ratings
  - negative-file reviews with high ratings
- Decide from EDA whether flagged rows are dropped or retained with a documented limitation.
- Clean text: lowercase, strip HTML artifacts, normalize punctuation/whitespace, and preserve enough negation signal for sentiment.
- Remove outliers using configurable word-count thresholds after inspecting length distribution.
- Create stratified 70/15/15 train/validation/test splits with a fixed seed.

### 4. `src/features.py` and `notebooks/EDA.ipynb` - EDA
- Compute class balance, domain balance, rating distribution, review length distribution, and label-audit counts.
- Save charts to `outputs/length_distribution.png` and `outputs/domain_balance.png`.
- Use EDA findings in the presentation, ethics notes, and report.

### 5. `src/dataset.py` - PyTorch input pipeline
- Build vocabulary from training text only to avoid data leakage.
- Implement tokenization, integer encoding, padding/truncation (`max_len=256`), `ReviewDataset`, and DataLoaders.
- Default to learned embeddings so training works without large external downloads.
- Add optional GloVe loading: if `embeddings/glove.6B.100d.txt` exists, initialize embedding weights from it; otherwise continue with learned embeddings.

### 6. `src/baseline.py` - Classical benchmark
- Train `TfidfVectorizer(max_features=30_000, ngram_range=(1,2)) + LogisticRegression`.
- Evaluate on validation and test splits.
- Save `outputs/baseline.joblib`.
- Use baseline results as the comparison point in the presentation.

### 7. `src/model.py` and `src/train.py` - BiLSTM neural model
- Implement `BiLSTMSentiment`: `Embedding -> Dropout -> bidirectional LSTM -> Linear`.
- Train with Adam, `BCEWithLogitsLoss`, gradient clipping, and validation tracking.
- Log loss, accuracy, and F1 per epoch.
- Save best validation checkpoint to `outputs/bilstm.pt`.

### 8. `src/evaluate.py` - Metrics and error analysis
- Evaluate baseline and BiLSTM on the same held-out test split.
- Report accuracy, precision, recall, F1, and confusion matrix.
- Save `outputs/confusion_matrix.png` and `outputs/error_examples.csv`.
- Include representative false positives/false negatives for the presentation and ethics discussion.

### 9. `src/inference.py` and `app.py` - Required demo
- Implement `predict_sentiment(text, model_name)` returning:
  - `Positive review`
  - `Negative review`
- Build a Streamlit app with:
  - review text area
  - explicit classify button
  - model selector for baseline/BiLSTM
  - visible prediction output and confidence
- Ensure the facilitator can enter new positive or negative statements and receive the required output on the page.

### 10. Documentation and assessment artifacts
- `docs/demo-test-cases.md`: positive, negative, ambiguous, domain-shifted, and outside-training examples with observed outputs.
- `docs/presentation-outline.md`: 10-15 minute structure with speaker allocation, rationale, architecture, metrics, demo, ethics, limitations, and future work.
- `docs/individual-report-template.md`: 250-word individual report scaffold with contribution percentages and ethics note.
- `docs/contribution-log.md` and `docs/team-contribution-table.md`: ownership, commits/branches, team member IDs, and percentage contribution evidence.
- `docs/references.md` and `docs/ethics-notes.md`: APA references and ethical considerations.
- `docs/submission-checklist.md`: final group code, GitHub link, presentation/video, individual report, and backup-copy checklist.

## Optional Enhancements

- **GloVe embeddings**: optional initialization for the BiLSTM, not required to run the project.
- **DistilBERT**: optional stretch comparison after the core BiLSTM path works. Keep transformer code/notebook separate from the assessed critical path.

## Ethical Considerations

- **Label ambiguity**: filename labels may hide mixed reviews, rating mismatches, or 3-star ambiguity.
- **Domain bias**: training data covers only four Amazon product domains, so predictions may not generalize to services, social media, healthcare, finance, or informal speech.
- **Binary simplification**: real sentiment can be neutral, mixed, sarcastic, or context-dependent; forcing every input into positive/negative can misrepresent user intent.
- **Fairness and reliability**: the model should not be presented as universally accurate; report observed failure modes and confidence limitations.

## Verification Checkpoints

| Check | Command | Expected |
|---|---|---|
| Parser loads data | `python -c "from src.parser import load_all_domains; print(load_all_domains().shape)"` | 8,000 rows with text/rating/label/domain/source_file |
| Tests pass | `pytest` | Parser, preprocessing, dataset, model, and inference tests pass |
| Baseline trains | `python src/baseline.py` | Classification report and `outputs/baseline.joblib` |
| BiLSTM trains | `python src/train.py` | Per-epoch logs and `outputs/bilstm.pt` |
| Evaluation runs | `python src/evaluate.py` | Metrics, confusion matrix, and error examples |
| App runs | `streamlit run app.py` | Local UI accepts text and returns sentiment |
| Demo cases pass | Manual run through `docs/demo-test-cases.md` | Clear positive/negative examples classify plausibly |

## Assessment Submission Coverage

| Brief requirement | Planned artifact |
|---|---|
| Group code | `src/`, `tests/`, `app.py`, `README.md`, model/evaluation artifacts |
| Simple website or executable | `app.py` Streamlit interface |
| Train/test neural network | `dataset.py`, `model.py`, `train.py`, `evaluate.py` |
| Inference on positive and negative inputs | `inference.py`, `app.py`, `docs/demo-test-cases.md` |
| Ethical considerations | `docs/ethics-notes.md`, `docs/references.md`, presentation ethics section |
| Git/version control evidence | GitHub repo link, contribution log, branch/commit evidence |
| Group presentation | `docs/presentation-outline.md` and final video/slides |
| Individual 250-word report | `docs/individual-report-template.md`, `docs/team-contribution-table.md` |
| Team contribution percentages and IDs | `docs/team-contribution-table.md` |
| Final submission checklist | `docs/submission-checklist.md` |
