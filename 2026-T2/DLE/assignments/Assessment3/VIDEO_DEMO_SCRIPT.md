# ReviewPulse v3.0 — Optional Video Demo Script

This optional demonstration should take approximately four to five minutes. It is a practical walkthrough, not a second presentation of the report.

## 0:00–0:30 — Introduction

> Hi, this is ReviewPulse v3.0, the DLE602 implementation of our Assessment 2 proposal.
>
> The previous ISY503 version assigned one binary sentiment label to an entire review. This version performs three-class aspect-based sentiment analysis, so the user supplies a review and one or more aspects, and the system predicts positive, neutral or negative sentiment for each aspect separately.
>
> The main research question is whether giving the model the aspect explicitly helps when the same sentence contains different opinions.

## 0:30–1:15 — Show the interface

Open the v3 page and load a curated sample.

> The application accepts a review and manually supplied aspects. The examples are curated from the official SemEval test split, so the application can also display the gold polarity where it is available.
>
> I will use this example: “The pasta was bland, the staff were friendly, and the atmosphere was lovely.”

Show the aspect fields and the comparison control.

## 1:15–2:15 — Compare mode

> The comparison view shows the same aspects against the four core models.
>
> TF-IDF and the target-agnostic LSTM receive only the review. Therefore, their prediction is repeated across the aspect rows.
>
> ATAE-LSTM and DistilBERT receive both the review and the aspect. They can therefore produce different predictions for pasta, staff and atmosphere.
>
> This is the main visible demonstration of RQ1: aspect conditioning allows the model to respond to the target aspect instead of producing one sentence-level sentiment for everything.
>
> The GRU and TextCNN are also included as exploratory extensions, but the canonical comparison focuses on the four models committed in the original proposal.

## 2:15–3:15 — Token evidence

Select ATAE-LSTM and then DistilBERT.

> For the supported models, ReviewPulse exposes token-level evidence.
>
> ATAE-LSTM displays its learned attention weights, while DistilBERT displays gradient-times-input attribution aggregated onto visible tokens.
>
> Darker tokens received higher relative scores for the selected aspect. The scores change when I change the aspect, which makes the model’s sensitivity inspectable.
>
> However, these are diagnostic visualisations. They do not expose the model’s reasoning, and attention or attribution should not automatically be interpreted as a faithful causal explanation.

## 3:15–3:50 — Show an honest failure

Use the sentence “Great food but the service was dreadful!”.

> This example is also important because the system does not hide its failures. The gold labels are positive for food and negative for service, but the models may fail to separate both clauses correctly.
>
> This shows why the gold column and the error analysis matter: the visualisation helps us inspect model behaviour, but it does not guarantee a correct prediction.

## 3:50–4:20 — Reproducibility

Briefly show the README or terminal.

> The implementation is packaged with reproducibility instructions, pinned dependencies, six model artifacts and two archive modes.
>
> The complete package includes all six v3 models, while the lightweight package excludes the large DistilBERT checkpoint. The source repository, release tag, package manifests and SHA-256 checksums are documented separately.
>
> The report uses frozen evaluation artifacts, so the displayed results are not generated ad hoc during this demonstration.

## 4:20–4:35 — Closing

> In summary, ReviewPulse v3 makes aspect conditioning visible in the interface and exposes indicative token-level evidence for the models that support it.
>
> It also keeps limitations and failed predictions visible. That combination of implementation, comparison, evidence and reproducibility is the main outcome of the project.
>
> Thank you.

## Recording checklist

- Record the screen at a readable resolution; a webcam is optional.
- Keep the cursor visible and use the prepared samples instead of a random example.
- Do not show credentials, personal paths or restricted SemEval files.
- Do not explain all six models in detail; keep the focus on the research questions.
- Say “indicative token-level evidence”, not “the model’s reasoning”.
- A single take is sufficient; no editing, music or polished production is required.

The video is optional. The report, source code, execution instructions and reproducibility package remain the assessable deliverables.
