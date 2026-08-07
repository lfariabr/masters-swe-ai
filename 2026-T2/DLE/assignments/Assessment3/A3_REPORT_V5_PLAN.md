# DLE602 A3 — Report v5 and submission hardening

## Context

Dr Tayab spent lines 24–80 of the 5 Aug lecture on A3 expectations
(`2026-T2/DLE/modules/module-10-structured-probabilistic-models/DLE602_module10_class.txt`).
Cross-checking his words against the formal brief
(`2026-T2/DLE/assignments/DLE602_Assessment 3_20240603.pdf`), the report source
(`report/DLE602_A3_Report_v3.md`) and the exported
`report/v4_DLE602_Faria_L_Assessment_3.pdf` surfaced two **submission-blocking export defects**
plus a set of content elements he named explicitly that the report does not contain.

The core model implementation and frozen experimental results are complete. Submission
hardening, independent reproduction and targeted UI retesting remain open. Everything below is
report, export and packaging work.

A2 was returned at **85/100** (`../Assessment2/A2-grade.md`). Its five comments are answered in
the section below.

### Verified against the brief, not just the lecture

| Claim | Verdict |
|---|---|
| Body stays 1,500 ±10% = 1,350–1,650 | **Confirmed** (brief line 8). His verbal "1,800–2,000 is fine" does not override the written rubric. Do not inflate the body. |
| Word count goes on the cover | **False.** Brief line 76: *"State the word count at the end of the report (before the reference section)"*. The Markdown already does this correctly at the end of Section 6. Only the export dropped it. |
| Footer needs page numbers + group id | **Confirmed** (brief lines 77–78). v4 has page numbers in the **header** and no group identifier. |
| Academic Integrity Declaration missing from v4 PDF | **Confirmed.** v4 runs Appendix F → Statement of Acknowledgment → References. The "We declare…" section is gone. He said explicitly: *"academic integrity declaration you have to sign"*. |
| Literal `placeholder` rendered in Appendix E | **Confirmed** (v4 text line 954), with a fake *"Figure E1"* caption beneath it. |

## Responding to the A2 feedback, weighted by the A3 rubric

A2 and A3 are marked on **different criteria**. A2 weighted literature at 25%; A3 does not mark
literature at all. Prioritise accordingly:

| A3 criterion | Weight | What moves it here |
|---|---:|---|
| Completeness; system runs without configuration | 20% | Artifact-mode decision (below), quickstart at archive root |
| Coding convention and code quality | 20% | Already strong; he downloads and runs the code |
| **Integration of knowledge, topic focus, depth of discussion** | **30%** | Success-criteria table, gap→RQ table, Appendix G |
| Effective communication (written) | 15% | Body stays tight and inside the limit |
| Documentation: numbered headings, labelled tables/figures, referencing | 15% | Every export fix in this plan |

The Documentation criterion reframes the export defects: the broken `placeholder`/fake Figure E1,
header-instead-of-footer pagination and the mismatched appendix numbering (`7.x` appendices then
`8. References`) are not cosmetic. They land on a graded 15% criterion whose top band requires
numbered headings and properly labelled tables and figures.

### Table X — Literature gap → research question → A3 evidence

Answers *"The connection between the research questions and the identified literature gap could
be made more explicit."* Place in Section 1 or 2. Anchor to the actual A2 literature review text:

| Gap identified in A2 | RQ | A3 evidence |
|---|---|---|
| Zhao et al. (2018) and ReviewPulse v1/v2 emit one label per text; Pontiki et al. (2014) shift the question to *which* aspect is positive | RQ1 | 228-instance mixed-polarity subset; aspect-conditioned versus review-only paired comparison |
| Tang et al. (2016) condition on the target but do not selectively weight context; Wang et al. (2016) add attention yet learn from a small benchmark and may overfit | RQ2 | ATAE-LSTM versus DistilBERT on accuracy, macro-F1, training time, latency and artifact size |
| Neither transformer attention nor post-hoc attribution is automatically a faithful causal explanation (Devlin et al., 2019; Sun et al., 2019; Jain & Wallace, 2019) | RQ3 | Offset-aligned attention and gradient × input evidence, reported as indicative |

### Table Y — Success criteria and delivered status

Answers *"The measures used to determine the overall success of the project could be stated more
explicitly."* This is the single highest-value addition, because criterion 3 (30%) demands a
*"clear list of the requirements/functionalities manageable within the project scope."*

**Do not invent retrospective thresholds.** A2 already committed a scope contract at its
Section 4: *"the accepted minimum product remains the audited baselines, ATAE-LSTM, shared
evaluation and working interface. DistilBERT is retained when compute and validation checks pass;
optional Laptops transfer, automatic aspect extraction, Topic Modelling, a GRU variant and a CNN
baseline are cut first."* Anchor the table to that.

| Committed in A2 | Measure | Status |
|---|---|---|
| Accepted minimum product: audited baselines, ATAE-LSTM, shared evaluation, working interface | All load and return three-class predictions per aspect under one evaluation contract | Met |
| DistilBERT retained if compute and validation checks pass | Trained and evaluated under the same contract | Met |
| RQ1 | Mixed-polarity macro-F1 plus paired disagreement analysis | Met |
| RQ2 | Accuracy, macro-F1, training time, latency, artifact size | Met; timing observational, not a controlled comparison |
| RQ3 | Offset-aligned indicative evidence where supported, explicit unsupported state otherwise | Met in implementation; independent UI retest pending |
| Reproducibility: fixed seed, grouped splits, versioned artifacts, single evaluation script | Splits, seeds, provenance, clean install, test suite | Met on the pre-release baseline |
| Cut-first list under compute pressure | Scope discipline | Laptops, automatic extraction and Topic Modelling correctly cut; GRU and TextCNN delivered as exploratory extras only after the core gates passed |
| Release: public access, final archive, tag | — | Pending |

The last row is worth keeping: it shows scope discipline *and* overdelivery against a
pre-committed cut list, which is exactly what the planning criterion rewards.

### Literature synthesis — optional, and not in counted prose

A2 asked for *"further critical comparison of the selected studies and models."* A3 has no
literature criterion, and the word budget does not allow it as prose. If included, make it a
table (uncounted): Tang et al. motivates conditioning without explicit attention; ATAE-LSTM is
light and aspect-conditioned but its attention is not causal; DistilBERT wins on the benchmark at
roughly 100× the storage; TextCNN approximates Zhao et al. and confirms that swapping the
review-only encoder does not supply the missing aspect signal.

### Rejected: the "duplicated LSTM row" in Table 2

A review flagged Table 2 as rendering five rows with `LSTM review-only` twice. **This is false.**
Table 2 has four rows in both the Markdown source and the v4 PDF. The string appears twice in the
extracted PDF text because **Table 2** (headline comparison) and **Table 3** (per-class F1)
legitimately list the same four models. Do not delete anything.

## The two defects that must be fixed regardless of anything else

**1. Restore the Academic Integrity Declaration.** Present in `DLE602_A3_Report_v3.md` §14, absent
from the PDF. Highest-severity item in this plan.

**2. Remove the broken image block in Appendix E.** Author-facing instructions (a fenced markdown
snippet showing the image syntax) were placed inside the report body, and the exporter rendered
the broken image as the word `placeholder` plus a caption that reads as a real figure. Move that
guidance out of the report into `docs/dle602-a3/validation-juan.md` in review-pulse.

> Distinction that matters: keeping **"Pending"** rows visible is a deliberate honesty choice.
> A broken-image `placeholder` masquerading as Figure E1 is a rendering bug. Fix the second,
> keep the first.

## Report changes

### Body — Sections 1–6, target 1,580–1,630 words (ceiling 1,650)

Currently 1,550, so roughly 100 counted words are available. Tables and captions are excluded
under the declared rule, which is what makes the two new tables nearly free:

| Addition | Counted cost | Running total |
|---|---:|---:|
| Table X lead-in (gap → RQ) | ~15 | 1,565 |
| Table Y lead-in (success criteria) | ~15 | 1,580 |
| Libraries sentence in Section 3 | ~40 | 1,620 |
| *Literature synthesis as prose* | *~90* | *1,710 — over the limit, do not* |

Spend the headroom on:

- **Section 3** — one sentence naming the libraries and their roles: `defusedxml` (safe XML
  parsing), `scikit-learn` (TF-IDF + logistic regression), `PyTorch` (LSTM, GRU, TextCNN,
  ATAE-LSTM), `transformers` (DistilBERT), `pandas`/`NumPy` (evidence tables), `matplotlib`
  (confusion matrices), `streamlit` (application). Zero mentions of any of these today.
- **Section 4** — one clause pointing at the frozen hyperparameters and the TextCNN configuration
  search in the new Appendix G.
- **Section 1 or 2** — insert **Table X** (gap → RQ → evidence) and **Table Y** (success criteria
  and status) with short lead-ins. Both tables are uncounted; only the lead-ins cost words.

Renumber the existing tables after insertion: today's Table 1 (dataset audit) through Table 4
(token evidence) shift, and every in-text reference plus the ToC must follow. The Documentation
criterion marks exactly this.

Do not claim all models were tuned. **Only TextCNN has a recorded configuration search.** The rest
used predefined configurations with development macro-F1 checkpoint selection.

### New Appendix G — Implementation Walkthrough and Configuration Evidence

One appendix, not two. Appendices are excluded from the declared count, so this is free.

**Table G1 — Parsed dataset preview.** Three records: `sentence_id`, shortened review text,
aspect, gold polarity, offset validity. Answers his *"put a header of the data set"*. Use only
sentences already vetted as attributed demo samples in `src/absa/samples.py` — do not
redistribute XML or a row-level dataset.

**Table G2 — Libraries and frozen versions.** From `constraints-a3.txt`: torch 2.13.0,
scikit-learn 1.8.0, transformers 5.14.1, streamlit 1.59.2, pandas 3.0.3, Python 3.12.10.

**Table G3 — Frozen model configurations.** All values verified present in the metrics JSONs:

| Model | Batch | LR | Weight decay | Max len | Best epoch | Other |
|---|---:|---:|---:|---:|---:|---|
| Target LSTM | 64 | 1e-3 | 1e-4 | 80 | 8 | patience 2 |
| Target GRU | 64 | 1e-3 | 1e-4 | 80 | 8 | emb 100, hidden 128, dropout 0.5 |
| TextCNN | 64 | 1e-3 | 1e-4 | 80 | 6 | emb 100, dropout 0.5 |
| ATAE-LSTM | 64 | 1e-3 | 1e-4 | 80 | 6 | patience 2 |
| DistilBERT | 8 | 2e-5 | 1e-2 | 128 | 2 | patience 2 |

**Table G4 — TextCNN configuration search.** The direct answer to *"if you have made some changes
into the parameters, what was the effect"*. From `outputs/absa/text_cnn_config_search.json`
(seed 42, 4 epochs, `official_test_evaluated: false`):

| Filter widths | Filters | Dev macro-F1 | Params | Time |
|---|---:|---:|---:|---:|
| (2,3,4) | 64 | 0.4309 | 393,371 | 7.7 s |
| (3,4,5) | 64 | 0.3776 | 412,571 | 8.9 s |
| (3,4,5) | 100 | **0.4722** | 456,203 | 12.1 s |

The narrative matters more than the table: **widening the filters alone made it worse**
(0.4309 → 0.3776); the gain came from added capacity, not receptive field. State that the
official test split took no part in selection.

**Figures G1–G4 — code-plus-output captures**, his most repeated ask:

- G1 dataset parser/audit command and output
- G2 training run showing best-epoch selection
- G3 TextCNN configuration search output
- G4 evaluation runner, or one multi-aspect prediction

Captures must come from the frozen commit and stay legible on A4.

> **Redaction gate:** `text_cnn_config_search.json` and every `*_metrics.json` embed absolute
> paths (`/Users/luisfaria/Desktop/...`). Crop or redact them — do not publish the local path.

## Export and formatting fixes

- Restore the **Academic Integrity Declaration**, signed by all three members.
- Remove the Appendix E broken-image block; move the instructions to `validation-juan.md`.
- Move page numbers to the **footer**. No group identifier was issued, so use
  `A00187785 · A00179705 · A00167145 | Page X` and add one line stating that no group identifier
  was assigned.
- Restore the **word count at the end of Section 6, before References** (brief line 76). Cover
  placement is optional and not the requirement.
- Retitle the cover to *ReviewPulse v3.0 — Aspect-Based Sentiment Analysis* and drop the generic
  copyright/distribution notice.
- Fix Table B2: restore the **Status** column and the caveat sentence *"Assignments are not
  treated as completed contributions…"*, both dropped in v4. Restore the Appendix E/F
  cross-references.
- Rename Appendix F to *Independent Reproduction Record* (v4 says "Reproducible"), restore the
  `Owner:` lines on E and F, and update the ToC.
- Export **both DOCX and PDF**. He said *"better you submit the word file as I can add"* — he
  annotates. Ship both in the ZIP.

## Verification

1. Recount the body under the declared rule; confirm 1,350 ≤ count ≤ 1,650.
2. `pdftotext` the export and grep for: the word count, "We declare", "Statement of
   Acknowledgment", each library name, the Table G values — and confirm **zero** hits for
   `placeholder`, `TODO`, `Short alt text`.
3. Render every page and check footer, pagination, captions, ToC and figure legibility.
4. Confirm no `/Users/luisfaria/` string survives in any figure.
5. Full suite on the frozen commit (currently 363 passed / 3 skipped).
6. Test the public Streamlit link in an incognito session. It currently redirects to
   authentication — do not put the link in the report or package until it opens clean.
7. **Confirm the LMS upload limit before choosing the artifact mode — this is a grade decision,
   not admin.** Criterion 1 (20%) bands read *"The system functions only if certain additional
   conditions are met"* (74%) versus *"functions without any additional conditions"* (84%+).
   Shipping `lightweight` leaves DistilBERT absent, so the marker must fetch it separately, which
   is by the rubric's own wording an additional condition. Tayab also said *"I usually try to
   download the code and check it's working."* **If 288 MB fits, ship `all`.** If it does not,
   the missing model and its one-command retrieval must be the first thing visible in the archive
   root README.
8. Build the chosen ZIP, extract to a clean directory, run the documented quickstart with
   `quickstart.md` at the archive root.
9. Record the final commit and ZIP SHA-256, then tag `v3.0.0`.

## Low-cost parallel task

A short Module 10 discussion-forum post — he invited it and addressed the project directly.
Frame: observed variables (review tokens, supplied aspect, polarity); latent representations
(recurrent hidden states, Transformer contextual states); modelled dependency
(review + aspect → representation → polarity); attention as **indicative** evidence, not a causal
graph; how a graphical model could future-represent inter-aspect dependency and uncertainty.

Do not call ATAE-LSTM a structured probabilistic model.

## Decisions carried in

- No group identifier issued → student IDs in the footer.
- Appendices E and F ship **with "Pending" visible** if evidence does not arrive. The risk is that
  it contradicts the "we have divided well the rows" statement made to him in class at transcript
  line 355.
- No retraining. Every number above already exists in frozen artifacts.
- Body stays inside the written brief; the verbal 1,800–2,000 allowance is not used.
