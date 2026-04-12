# ReviewPulse — Diagrams

Use these diagrams in the README, presentation, and teammate handoff. Each diagram has a one-line purpose so Samiran and Victor can quickly understand where it fits.

## 1. Inference Data Flow

**Purpose:** Shows how a user's review moves through the Streamlit app, selected model, inference layer, and final sentiment output.

```mermaid
flowchart LR
    A([User types review text]) --> B[app.py]
    B --> C{Model selector}
    C -->|BiLSTM| D[inference.py\npredict_sentiment]
    C -->|Baseline| E[baseline.joblib\nTF-IDF + LogReg]
    D --> F[bilstm.pt]
    F --> D
    D --> G([Positive review / Negative review\n+ confidence])
    E --> G
    B --> G
```

---

## 2. Training Pipeline

**Purpose:** Shows the end-to-end ML workflow from raw `.review` files through preprocessing, model training, evaluation, and saved artifacts.

```mermaid
flowchart TD
    A[".review files\n(8,000 labelled reviews\n4 domains)"] --> B[parser.py\nload_all_domains]
    B --> C[preprocess.py\naudit_labels · clean_text\nremove_outliers · split_data]
    C --> D[features.py / EDA.ipynb\nlength dist · class balance\ndomain balance]
    C --> E[dataset.py\nbuild_vocab · tokenize_and_pad\nReviewDataset · DataLoader]
    E -->|optional| F[load_glove\nGloVe 100d]
    E --> G[train.py\nAdam · BCEWithLogitsLoss\ngrad clipping · checkpointing]
    G --> H[(outputs/bilstm.pt\nbest val checkpoint)]
    H --> I[evaluate.py\naccuracy · F1\nconfusion matrix\nerror analysis]
    C --> J[baseline.py\nTF-IDF + LogReg]
    J --> K[(outputs/baseline.joblib)]
    K --> I
```

---

## 3. Project Module Architecture

**Purpose:** Shows the main source modules and how data/model responsibilities connect across the codebase.

```mermaid
graph TD
    subgraph src
        PA[parser.py] --> PR[preprocess.py]
        PR --> FE[features.py]
        PR --> DS[dataset.py]
        PR --> BL[baseline.py]
        DS --> TR[train.py]
        TR --> EV[evaluate.py]
        BL --> EV
        TR --> IN[inference.py]
        BL --> IN
    end

    subgraph app
        AP[app.py]
    end

    subgraph tests
        TE[tests/]
    end

    IN --> AP
    PA --> TE
    PR --> TE
    DS --> TE
    BL --> TE
    TR --> TE
    IN --> TE
```

---

## 4. BiLSTM Model Architecture

**Purpose:** Shows the required neural-network path: encoded review tokens become embeddings, sequence features, a raw logit, and a positive/negative prediction.

```mermaid
flowchart TD
    A["Input token IDs\n(batch × max_len)"] --> B["Embedding layer\n(vocab_size × 100d)\noptional GloVe init"]
    B --> C["Dropout (p=0.5)"]
    C --> D["BiLSTM\n2 layers · bidirectional\nhidden_dim=256"]
    D --> E["Forward hidden state\n(last timestep)"]
    D --> F["Backward hidden state\n(last timestep)"]
    E --> G["Concat → 512d vector"]
    F --> G
    G --> H["Dropout (p=0.5)"]
    H --> I["Linear(512 → 1)\nraw logit"]
    I --> J["BCEWithLogitsLoss\n(training)"]
    I --> K["Sigmoid → confidence\n(inference)"]
    K --> L(["Positive review\nor Negative review"])
```

---

## 5. Assessment Submission Coverage

**Purpose:** Shows how the project artifacts map to the three required Assessment 3 submissions.

```mermaid
flowchart TD
    A[Assessment 3 Submission] --> B[Group Code]
    A --> C[Group Presentation Video]
    A --> D[Individual Report]

    B --> B1[src package]
    B --> B2[tests]
    B --> B3[Streamlit app.py]
    B --> B4[README and GitHub link]
    B --> B5[model and evaluation artifacts]

    C --> C1[presentation-outline.md]
    C --> C2[architecture and pipeline diagrams]
    C --> C3[metrics and demo results]
    C --> C4[ethics and limitations]

    D --> D1[individual-report-template.md]
    D --> D2[team-contribution-table.md]
    D --> D3[contribution-log.md]
    D --> D4[references.md]
```

---

## 6. Team Ownership Split

**Purpose:** Gives the team a low-risk ownership model where Luis owns the technical critical path and Samiran/Victor own bounded submission artifacts.

```mermaid
flowchart LR
    A[ReviewPulse] --> L[Luis\nTechnical critical path]
    A --> S[Samiran\nPresentation and ethics]
    A --> V[Victor\nEDA support and QA]

    L --> L1[Parser and preprocessing]
    L --> L2[Baseline and BiLSTM]
    L --> L3[Evaluation and app integration]
    L --> L4[Final code review]

    S --> S1[presentation-outline.md]
    S --> S2[references.md]
    S --> S3[ethics-notes.md]
    S --> S4[demo-test-cases.md]

    V --> V1[EDA notes and chart interpretation]
    V --> V2[contribution-log.md]
    V --> V3[team-contribution-table.md]
    V --> V4[submission-checklist.md]
```

---

## 7. Baseline vs Neural Model Comparison

**Purpose:** Shows the comparison story for the presentation: a simple classical model establishes a benchmark, then the BiLSTM provides the required neural-network solution.

```mermaid
flowchart TD
    A[Cleaned train/validation/test splits] --> B[Baseline path]
    A --> C[Neural path]

    B --> B1[TF-IDF vectorizer]
    B1 --> B2[Logistic Regression]
    B2 --> B3[baseline.joblib]

    C --> C1[Vocabulary and padded sequences]
    C1 --> C2[BiLSTM]
    C2 --> C3[bilstm.pt]

    B3 --> D[evaluate.py]
    C3 --> D
    D --> E[accuracy precision recall F1]
    D --> F[confusion matrix]
    D --> G[error_examples.csv]
```
