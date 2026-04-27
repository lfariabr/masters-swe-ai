# Dev.to Article Plan — ReviewPulse Sentiment Classifier

## Goal

Create a first dev.to draft about building `ReviewPulse` for `ISY503 Assessment 3`.

The article should read as a practical technical story, not an academic report. The core narrative is:

> ISY503 Assessment 3 moved from intelligent systems theory into a real NLP build: parse raw product review data, train and compare models, evaluate failure modes, ship a simple Streamlit interface, and explain the ethical limits honestly.

Use the assessment brief only as setup. The main story should be the engineering work behind turning labelled review files into a working sentiment-analysis demo.

## Output File

```text
2026-T1/ISY/assignments/Assessment3/DEVTO-ARTICLE-DRAFT.md
```

> Note: `/docs/refs` is in `.gitignore`, so the tracked draft should live alongside the ISY503 Assessment 3 artefacts.

## Recommended Article Shape

Target length: `1,800-2,400 words`.

Suggested tags:

```text
#machinelearning #nlp #python #streamlit #pytorch
```

Suggested structure:

1. **Hook**
   - Open with building `ReviewPulse`, a product review sentiment classifier.
   - Position it as the jump from learning NLP concepts to shipping a working model with a usable interface.

2. **Course Context**
   - Mention `ISY503 Intelligent Systems`.
   - Explain that the course moved through intelligent systems foundations, machine learning, deep learning, NLP, deployment, and ethical considerations.
   - Keep this brief. The article is about the build, not the subject outline.

3. **Assessment Requirement**
   - Explain the chosen NLP path: train a sentiment model from labelled Amazon product reviews.
   - The required interface needed a text box, a button, and an output of `Positive review` or `Negative review`.
   - Mention that the facilitator could test new inputs, so the app had to work beyond a static notebook.

4. **Why ReviewPulse**
   - The portfolio signal is ML engineering, not only model training.
   - ReviewPulse demonstrates raw data parsing, preprocessing, baseline comparison, neural modelling, evaluation, ethics, and deployment.
   - A Streamlit demo makes the model testable by non-technical users.
   - The name gives the assessment project a product-like identity without pretending it is production-ready.

5. **Dataset Walkthrough**
   - Dataset: Blitzer, Dredze, and Pereira Amazon review sentiment dataset.
   - Local dataset size: `8,000` labelled reviews.
   - Domains:
     - `books`
     - `dvd`
     - `electronics`
     - `kitchen_&_housewares`
   - Each domain has `1,000` positive and `1,000` negative reviews.
   - Labels are derived from `positive.review` and `negative.review` source files.
   - Ratings are retained for auditing and ethics discussion.

6. **Pipeline Walkthrough**
   - Parse pseudo-XML `.review` files into a structured DataFrame.
   - Extract `text`, `rating`, `label`, `domain`, and `source_file`.
   - Audit label quality and rating/text ambiguity.
   - Clean text while preserving sentiment cues such as negation.
   - Remove length outliers after EDA.
   - Create stratified train/validation/test splits with a fixed seed.
   - Build vocabulary from training data only to avoid leakage.

7. **Model Comparison**
   - Baseline: `TF-IDF + Logistic Regression`.
   - Neural model: bidirectional LSTM using GloVe 100-dimensional embeddings.
   - Training details:
     - PyTorch
     - Adam optimiser
     - `BCEWithLogitsLoss`
     - gradient clipping
     - F1-based checkpointing
     - Apple MPS support
   - Be honest about the result:
     - TF-IDF baseline test F1: `81.9%`
     - BiLSTM test F1: `80.3%`
   - Frame this as an important ML lesson: stronger architecture does not automatically mean better generalisation.

8. **Evaluation and Error Analysis**
   - Report accuracy, precision, recall, F1, and confusion matrix.
   - Mention the shared failure modes:
     - negation traps
     - sarcasm
     - mixed sentiment
     - short ambiguous inputs
     - out-of-domain reviews
   - Use examples from the demo test cases, but avoid overloading the article with tables.

9. **Streamlit Demo**
   - Explain the user-facing app:
     - review text area
     - explicit classify button
     - model selector
     - sample review generator
     - prediction label
     - confidence display
   - Include the public app link if still valid:
     - `https://review-pulse.streamlit.app/`
   - Include the GitHub repo link if useful:
     - `https://github.com/lfariabr/review-pulse`

10. **Ethics and Limitations**
    - Filename-derived labels are not the same as fresh human annotation.
    - Binary sentiment simplifies neutral, mixed, sarcastic, and context-dependent language.
    - Confidence scores are uncalibrated; high confidence does not equal guaranteed correctness.
    - The model is trained on four product review domains and may generalise poorly to logistics, services, healthcare, finance, or social media text.
    - Any production use would need human oversight, periodic audits, broader data, confidence calibration, and explainability.

11. **AI-Assisted Workflow**
    - Mention the workflow transparently:
      - ChatGPT and Claude supported planning, debugging, conceptual clarification, and writing polish.
      - Final decisions, implementation, evaluation, and responsibility remained human-led.
    - Frame AI as a learning and productivity assistant, not as a replacement for doing the technical work.

12. **Takeaways**
    - A working ML system is more than a model file.
    - Baselines matter.
    - Evaluation honesty is better than forcing the neural model to look superior.
    - Streamlit is useful for turning a model into something a facilitator or stakeholder can actually test.
    - Ethical limitations belong in the product story, not only in the report appendix.

## Source Files For Claude

Use these files as the factual source of truth:

```text
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/README.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/ISY503_Assessment3.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/plan.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/report/Individual_Report_Luis.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/docs/demo-test-cases.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/docs/presentation-outline.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/docs/ethics-notes.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/docs/references.md
```

Use these as style references:

```text
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/EigenAi.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/invoiceLedger.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/myRoster.md
```

## Image Placeholders

Include dev.to image placeholders in the draft. Do not embed local absolute image paths as final public URLs.

Recommended screenshot placeholders:

```markdown
![ReviewPulse Streamlit app showing the text input, model selector, and classify button](UPLOAD_IMAGE_HERE)
![ReviewPulse prediction screen showing a positive review classification with confidence](UPLOAD_IMAGE_HERE)
![ReviewPulse prediction screen showing a negative review classification with confidence](UPLOAD_IMAGE_HERE)
![Model comparison chart showing TF-IDF Logistic Regression versus BiLSTM test performance](UPLOAD_IMAGE_HERE)
![Confusion matrix from the ReviewPulse evaluation workflow](UPLOAD_IMAGE_HERE)
![Example error analysis output showing negation, sarcasm, or domain-shift failure cases](UPLOAD_IMAGE_HERE)
```

If local screenshots are not already available, capture them from:

```text
https://review-pulse.streamlit.app/
```

or from a local Streamlit run of the ReviewPulse app.

## Claude Execution Prompt

Use this prompt with Claude:

```text
Create a dev.to draft v1 at:
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/assignments/Assessment3/DEVTO-ARTICLE-DRAFT.md

Write a technical story about building ReviewPulse for ISY503 Assessment 3: a multi-domain Amazon product review sentiment classifier with a Streamlit interface.

Angle: practical ML engineering story, not academic report.
Assessment depth: use the ISY503 Assessment 3 brief as context only; do not make the article rubric-heavy.
Target: 1,800-2,400 words.

Core narrative:
ISY503 Assessment 3 moved from NLP theory into a real build: parsing raw pseudo-XML review files, auditing labels, preprocessing text, training a TF-IDF + Logistic Regression baseline, training a BiLSTM with GloVe embeddings, evaluating both models, exposing inference through Streamlit, and documenting ethical limitations.

Important factual points:
- Project name: ReviewPulse.
- Dataset: Blitzer et al. Amazon review sentiment dataset.
- Local dataset: 8,000 reviews across books, dvd, electronics, and kitchen_&_housewares.
- Each domain has 1,000 positive and 1,000 negative reviews.
- Required app output: Positive review or Negative review.
- Baseline: TF-IDF + Logistic Regression.
- Neural model: BiLSTM with GloVe 100-dimensional embeddings.
- Test result: TF-IDF baseline F1 81.9%; BiLSTM F1 80.3%.
- Be honest that the simpler baseline slightly outperformed the neural model.
- Public app: https://review-pulse.streamlit.app/
- GitHub repo: https://github.com/lfariabr/review-pulse

Use the local source files listed in DEVTO-ARTICLE-PLAN.md as factual sources. Match the writing style of the existing dev.to drafts in docs/refs/devToRefs.

Do not invent facts. Do not include student IDs, private emails, real secrets, passwords, private account details, or private submission links. Use image placeholders with clear alt text where dev.to screenshots should be uploaded later.

Include title, tags, intro, course context, why ReviewPulse, dataset walkthrough, pipeline walkthrough, model comparison, evaluation/error analysis, Streamlit demo, ethics and limitations, AI-assisted workflow, and final takeaways.
```

## Acceptance Checks

Before considering the draft done, verify:

- The article is mainly about ReviewPulse and the ISY503 Assessment 3 NLP project.
- The tone is practical, personal, technical, and build-in-public.
- The assessment brief is used as context only, not as a rubric-heavy structure.
- Dataset details match the local source files.
- Model details match the local source files.
- The baseline outperforming the BiLSTM is stated honestly.
- Ethical limitations are present and concrete.
- No student IDs, private emails, secrets, passwords, private submission URLs, or private account details are included.
- The article has image placeholders with useful alt text.
- The style is consistent with previous dev.to drafts such as EigenAI, invoiceLedger, and myRoster.
