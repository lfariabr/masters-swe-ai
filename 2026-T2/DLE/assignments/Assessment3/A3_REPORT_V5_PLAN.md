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

> **Priority change.** Juan's QA landed (review-pulse PRs #120/#121) with **overall result: Fail**
> — three failures and two blocked checks. Two of the failures are on the token-evidence views
> that RQ3 depends on. Triage (below) now outranks the appendix work.

### Verified against the brief, not just the lecture

| Claim | Verdict |
|---|---|
| Body stays 1,500 ±10% = 1,350–1,650 | **Confirmed** (brief line 8). His verbal "1,800–2,000 is fine" does not override the written rubric. Do not inflate the body. |
| Word count goes on the cover | **False.** Brief line 76: *"State the word count at the end of the report (before the reference section)"*. The Markdown already does this correctly at the end of Section 6. Only the export dropped it. |
| Footer needs page numbers + group id | **Confirmed** (brief lines 77–78). v4 has page numbers in the **header** and no group identifier. |
| Academic Integrity Declaration missing from v4 PDF | **Confirmed.** v4 runs Appendix F → Statement of Acknowledgment → References. The "We declare…" section is gone. He said explicitly: *"academic integrity declaration you have to sign"*. |
| Literal `placeholder` rendered in Appendix E | **Confirmed** (v4 text line 954), with a fake *"Figure E1"* caption beneath it. |

## Workstream 0 — Triage the defects Juan's QA found (do this first)

To be precise about terminology: **"Fail" is a status on the application, not on Juan's work.**
His QA record is a completed, well-structured deliverable that did its job — it found things.
Three of twelve UI checks failed and two were blocked.

The record is also deliberately non-conclusive. For UI-07 and UI-08 it states that the
screenshots *"require technical review to determine whether this is a rendering defect or a
misunderstanding of the evidence view"*, and it correctly separates model-quality observations
from UI acceptance failures (*"the incorrect prediction alone would not make the UI test fail"*).
Do not treat these as confirmed bugs until triaged.

They also cannot be adjudicated from the repository alone: the `Word document figure/page` fields
are blank and the screenshots sit in a companion Word document on Torrens SharePoint. **Get the
screenshots before debugging.**

From `docs/dle602-a3/validation-juan.md`, validated 2026-08-04 against the deployed app in an
**authenticated** session:

| ID | Check | Result | Note |
|---|---|---|---|
| UI-06 | Model switching, stale-result prevention | Blocked | Exact stale field and model transition not recorded |
| UI-07 | ATAE-LSTM attention evidence | **Fail** | Aspect change and alignment require triage |
| UI-08 | DistilBERT attribution evidence | **Fail** | Aspect change and alignment require triage |
| UI-10 | Empty review validation | **Fail** | Misclassified message and stale output observed |
| UI-12 | v2/v3 compatibility | Blocked | Exact leaked state and navigation direction not recorded |

**Hypothesis worth testing before treating these as five separate bugs:** UI-06 (stale on model
switch), UI-07/UI-08 (evidence does not change with the aspect), UI-10 (stale output) and UI-12
(leaked state) are all consistent with **one root cause — stale Streamlit session/cache state**,
not five independent defects. The local suite passes `test_attention.py` and
`test_attribution.py`, which assert exactly the alignment Juan saw fail, so the defect is more
likely in the page/session layer than in the predictors.

Second possibility to rule out first: the **deployed app may be behind `main`**. Check the
deployed commit before debugging anything.

Third, and specific to UI-07/UI-08: the difference between aspect views may be **real but
visually subtle rather than absent**. When the heatmap was reworked earlier in this project, the
measured gap between the `food` and `service` attention views on this style of example was a
maximum absolute difference of **0.031** — which is exactly why normalisation moved from
max-only to min-max. If that is what Juan saw, this is a presentation problem, not a correctness
one, and it is an honest RQ3 finding rather than a defect. Measure the two views on his exact
input before changing any code.

Why this outranks everything else: UI-07 and UI-08 are the views that answer RQ3, and they are
what Appendix E is meant to screenshot. Publishing a screenshot of a view that is under triage
would be worse than publishing nothing.

**Evidence status is settled.** Juan's companion Word document holds a complete screenshot set,
EV-01 through EV-12 including the six per-model smoke captures. The `Repository evidence status`
field in `validation-juan.md` still says captures are pending and is stale; ignore it. The
outstanding task is exporting four readable composites into `report/assets/`, not chasing
evidence.

One labelling slip to check in the source document: the six-model smoke set lists **EV-02E and
EV-02F both as ATAE-LSTM**. EV-02F is presumably DistilBERT. As written the sixth model is absent
and the fifth appears twice, in the exact section meant to prove all six run.

The SharePoint link needs an access check. Tayab downloads and runs things, and a link he cannot
open is worse than no link. If access cannot be granted, the four in-report captures carry the
appendix alone.

## Responding to the A2 feedback, weighted by the A3 rubric

A2 and A3 are marked on **different criteria**. A3 has **no standalone literature-review
criterion**; literature is assessed indirectly through knowledge integration and the connection
between theory, implementation and outcomes, and the brief does require integrating the A2
literature review. So the gap→RQ table still matters — a 90-word generic review does not.

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

> Tables X and Y are specified separately below for clarity, but **ship as one merged table**
> (`A2 gap/commitment | RQ or requirement | Pre-committed measure | A3 outcome`) to cut the
> all-inclusive word cost. See the body word-budget section.

### Table X — Literature gap → research question → A3 evidence

Answers *"The connection between the research questions and the identified literature gap could
be made more explicit."* Place in Section 1 or 2. Anchor to the actual A2 literature review text:

| Gap identified in A2 | RQ | A3 evidence |
|---|---|---|
| Sentence-level models emit one label per text (Zhao et al., 2018; ReviewPulse v1/v2); Pontiki et al. (2014) shift the question to *which* aspect is positive, and Tang et al. (2016) motivate target conditioning | RQ1 | 228-instance mixed-polarity subset; aspect-conditioned versus review-only paired comparison |
| Wang et al. (2016) give a light aspect-conditioned model learned from a small benchmark; Sanh et al. (2019) and Sun et al. (2019) offer pretrained contextual transfer at higher cost | RQ2 | ATAE-LSTM versus DistilBERT on accuracy, macro-F1, training time, latency and artifact size |
| Attention can vary without changing a prediction and need not identify causal features (Jain & Wallace, 2019) | RQ3 | Offset-aligned attention and gradient × input evidence, reported as indicative |

**Anchor precision:** the not-causal claim rests on **Jain & Wallace (2019)** alone. Devlin et al.
and Sun et al. concern pretraining and the sentence-pair reformulation and do not support it.
Jain & Wallace, Sanh, Sun, Tang, Wang and Pontiki are all already cited in A3. **Zhao et al.
(2018) is not** — either add the full reference (it strengthens the 15% referencing criterion) or
drop it and anchor RQ1 on Pontiki plus our own v1/v2 lineage.

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
| RQ3 | Offset-aligned indicative evidence where supported, explicit unsupported state otherwise | **Implemented; independent acceptance pending** (UI-07/UI-08 under triage) |
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

Both counts were measured on the current source:

| Counting basis | Now | After planned additions |
|---|---:|---:|
| Declared rule (tables and captions excluded) | **1,550** | ~1,620 |
| All-inclusive (tables and captions counted) | **1,867** | ~2,050 if X and Y stay separate |

This kills the idea of holding *both* counts under 1,650 — the all-inclusive figure is already
1,867 before adding anything, and stripping tables to fix it would wreck the report.

The defensible position: the **declared count stays inside the written brief** (1,350–1,650), and
the all-inclusive figure lands inside the **1,800–2,000 Tayab explicitly blessed verbally**. Both
readings are safe — but only if the additions stay small.

**Therefore merge Tables X and Y into one table**, which removes a duplicated lead-in and roughly
120 all-inclusive words:

| A2 gap / commitment | RQ or requirement | Pre-committed measure | A3 outcome |
|---|---|---|---|

Spend the counted headroom on:

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
- **Appendix E has been rewritten** (done). Its real flaw was duplication: Table E1 and the four
  figure captions described the same four captures twice over. The table is gone, EV traceability
  moved into the captions (`Figure E1 (EV-01, EV-02)`), and the case-by-case census gave way to
  the line that actually lands: seven passed, five did not, and the five that did not are the
  valuable ones. Juan now reads as the project's independent QA validator, with selected examples
  in the report and the complete record behind the link.
- Export four readable composites from Juan's Word evidence into `report/assets/` as `e1`–`e4`
  and insert them above the existing captions. Never render an empty image placeholder.
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
7. **Static code-quality audit** — criterion 2 is 20% and "already strong" is not evidence. Run a
   read-only lint pass over `app.py`, `pages/`, `src/`, `scripts/` and `tests/`, checking naming,
   imports, formatting and dead code, and confirm docstrings on the principal functions. Record
   the result in `release-verification.md`. **No linter is currently configured and `ruff` is not
   installed**, so treat this as an audit, not a cleanup: fix only clear naming or dead-code
   findings. A mass reformat days before submission risks more than it gains.
8. **Record the skips explicitly** rather than leaving a reader to infer them:
   *"363 passed, 3 expected skips; every skipped test requires the non-redistributed legacy
   Amazon dataset, and no ReviewPulse v3 test was skipped."* Chasing zero skips by shipping data
   we cannot redistribute is not an option.
9. Build **both** archives, extract each to a clean directory, and run the documented quickstart
   with `quickstart.md` at the archive root.
10. Record the final commit and both ZIP SHA-256 digests, then tag `v3.0.0`.

### Distribution decision — ship both packages

**Both `lightweight` (~52 MB) and `all` (~288 MB) go to the LMS regardless of which one fits.**
If the LMS refuses the larger archive, upload `all` to OneDrive and put the share link in the
submission and the archive root README. The marker therefore always has a one-click route to the
complete six-model build, and the LMS limit stops being a blocking gate.

This removes the artifact-mode decision from the critical path. It also protects criterion 1
(20%, *"the system functions without any additional conditions"*): a marker who wants every model
never has to reconstruct anything. Note the rubric is holistic, so `lightweight` alone would not
mechanically cap the mark — but requiring a manual DistilBERT download is a real risk against
that criterion, and shipping both retires it.

Still required for the lightweight archive, since it may be the one opened first: the missing
model, its one-command retrieval, its checksum, the controlled error state, and the link to the
full release must be the first thing visible in the root README.

## Low-cost parallel task

A short Module 10 discussion-forum post — he invited it and addressed the project directly.
Frame: observed variables (review tokens, supplied aspect, polarity); latent representations
(recurrent hidden states, Transformer contextual states); modelled dependency
(review + aspect → representation → polarity); attention as **indicative** evidence, not a causal
graph; how a graphical model could future-represent inter-aspect dependency and uncertainty.

Do not call ATAE-LSTM a structured probabilistic model.

## Decisions carried in

- No group identifier issued → student IDs in the footer.
- **Appendix E is delivered**, not pending: Juan's QA is complete and merged (PRs #120/#121) and
  the screenshot set exists. Only the asset export remains.
- Appendix F still ships **with "Pending" visible** if Victor's evidence does not arrive. The risk
  is that it contradicts the "we have divided well the rows" statement made in class at transcript
  line 355.
- **Both archives ship**: `lightweight` and `all` both go to the LMS; if the larger is refused,
  `all` goes to OneDrive and the link travels with the submission. The LMS limit is no longer a
  blocking gate.
- No retraining. Every number above already exists in frozen artifacts.
- Body stays inside the written brief; the verbal 1,800–2,000 allowance is not used.
